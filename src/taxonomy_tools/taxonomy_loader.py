"""Reads conf/taxonomy_v1.yaml into checked objects.

The point of loading rather than passing the raw dict around is to fail here, at startup,
with a message you can read -- instead of failing three modules later as a KeyError.

Each category also carries the numbers the scoring engine needs: `severity_weight` (how
badly this kind of move misleads) and `disruption` (how much it breaks the argument's
logic). Keeping them next to the detector definition means one file describes a category
completely.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any

VALID_DETECTORS = ("lexicon", "regex", "regex_unless", "cooccurrence", "repetition",
                   "entity_blame", "entity_sentiment_split")

# Detectors that cannot run without the spaCy entity stage. The runner checks this to
# decide whether to load spaCy at all -- a config with none of these stays fast.
ENTITY_DETECTORS = ("entity_blame", "entity_sentiment_split")

# which key holds the rules, per detector kind
RULE_KEY = {
    "lexicon": "terms",
    "regex": "patterns",
    "regex_unless": "patterns",
    "cooccurrence": "terms",
    "repetition": None,          # repetition is configured by numbers, not a rule list
    "entity_blame": "terms",     # the blame phrases
    "entity_sentiment_split": None,
}


@dataclass
class Category:
    id: str
    name: str
    detector: str
    base_confidence: float
    description: str = ""
    # what the category belongs to: "fallacy", "propaganda", "bias" or "style"
    family: str = "propaganda"
    # how severely this move misleads, 0-1. Used by the severity formula (claudenew 12.4).
    severity_weight: float = 0.5
    # how much it breaks the argument's logical flow, 0-1 (claudenew 21.1 formula 3).
    disruption: float = 0.3
    terms: List[str] = field(default_factory=list)
    patterns: List[str] = field(default_factory=list)
    # regex_unless: the sentence is left alone if it contains any of these
    unless_terms: List[str] = field(default_factory=list)
    unless_patterns: List[str] = field(default_factory=list)
    # cooccurrence
    min_hits: int = 2
    max_words: int = 15
    # repetition
    ngram_size: int = 3
    min_repeats: int = 3
    # entity_blame / entity_sentiment_split
    entity_labels: List[str] = field(default_factory=lambda: ["PERSON", "ORG", "NORP", "GPE"])
    min_blamed_sentences: int = 2
    # Group nouns spaCy will never tag, because NER only labels proper nouns.
    group_terms: List[str] = field(default_factory=list)
    positive_threshold: float = 0.5
    negative_threshold: float = -0.5
    min_entities: int = 2
    min_mentions: int = 2


@dataclass
class Taxonomy:
    version: str
    default_threshold: float
    categories: List[Category]

    def ids(self) -> List[str]:
        return [c.id for c in self.categories]

    def by_id(self, category_id: str) -> Category:
        for category in self.categories:
            if category.id == category_id:
                return category
        raise KeyError("no such category: " + category_id)

    def needs_entities(self) -> bool:
        """True when at least one enabled category needs the spaCy stage."""
        return any(c.detector in ENTITY_DETECTORS for c in self.categories)

    def families(self) -> Dict[str, List[str]]:
        grouped = {}
        for category in self.categories:
            grouped.setdefault(category.family, []).append(category.id)
        return grouped


def load_taxonomy(conf: Dict[str, Any]) -> Taxonomy:
    if not conf or "categories" not in conf:
        raise ValueError("taxonomy config is empty or has no 'categories' key")

    header = conf.get("taxonomy", {})
    categories = []
    seen = set()

    for raw in conf["categories"]:
        cat_id = raw.get("id")
        if not cat_id:
            raise ValueError("category with no id: " + repr(raw))
        # duplicate ids would silently overwrite each other in every downstream dict
        if cat_id in seen:
            raise ValueError("duplicate category id: " + cat_id)
        seen.add(cat_id)

        detector = raw.get("detector")
        if detector not in VALID_DETECTORS:
            raise ValueError(
                cat_id + ": detector must be one of " + str(VALID_DETECTORS)
                + ", got " + repr(detector)
            )

        rule_key = RULE_KEY[detector]
        if rule_key and not raw.get(rule_key):
            raise ValueError(cat_id + ": a " + detector + " category needs a non-empty '"
                             + rule_key + "' list")

        if detector == "regex_unless" and not (raw.get("unless_terms") or raw.get("unless_patterns")):
            raise ValueError(cat_id + ": regex_unless needs unless_terms or unless_patterns, "
                             "otherwise it is just a regex category")

        categories.append(Category(
            id=cat_id,
            name=raw.get("name", cat_id),
            detector=detector,
            base_confidence=float(raw.get("base_confidence", 0.8)),
            description=raw.get("description", "").strip(),
            family=raw.get("family", "propaganda"),
            severity_weight=float(raw.get("severity_weight", 0.5)),
            disruption=float(raw.get("disruption", 0.3)),
            terms=raw.get("terms", []),
            patterns=raw.get("patterns", []),
            unless_terms=raw.get("unless_terms", []),
            unless_patterns=raw.get("unless_patterns", []),
            min_hits=int(raw.get("min_hits", 2)),
            max_words=int(raw.get("max_words", 15)),
            ngram_size=int(raw.get("ngram_size", 3)),
            min_repeats=int(raw.get("min_repeats", 3)),
            entity_labels=raw.get("entity_labels", ["PERSON", "ORG", "NORP", "GPE"]),
            min_blamed_sentences=int(raw.get("min_blamed_sentences", 2)),
            group_terms=raw.get("group_terms", []),
            positive_threshold=float(raw.get("positive_threshold", 0.5)),
            negative_threshold=float(raw.get("negative_threshold", -0.5)),
            min_entities=int(raw.get("min_entities", 2)),
            min_mentions=int(raw.get("min_mentions", 2)),
        ))

    return Taxonomy(
        version=str(header.get("version", "0.0.0")),
        default_threshold=float(header.get("default_threshold", 0.8)),
        categories=categories,
    )
