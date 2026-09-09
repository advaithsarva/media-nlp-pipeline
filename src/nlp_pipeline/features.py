"""Feature engineering: numeric signals derived from a NormalizedDocument.

This is deliberately not a second rule engine. `rules_engine.py` already does precision
detection with exact, quotable evidence -- duplicating loaded-word lexicons here would
just be a second, worse copy of `conf/taxonomy_v1.yaml`. What belongs here instead is the
kind of signal that is legitimately numeric rather than a quoted span: sentence-length
statistics, vocabulary richness, sentiment polarity, entity density. These are exactly
the inputs `MLClassifier` needs -- a fixed-order feature vector, not a list of matches --
which is also why every layer returns *flat, numeric* values only. Anything a reader
could quote as evidence belongs in `RuleEngine`, not here.

Every layer is a small, independent class with a `compute(doc) -> Dict[str, float]`
method, so any one of them can be tested, reused or dropped without touching the others.
`FeatureExtractor.build_features` just runs the layers configured on and flattens the
result into one bundle, `"<layer>.<name>"` -> value.

No layer reads `conf/taxonomy_v1.yaml`, and no layer is randomised -- same document, same
tokens, same sentences in, same numbers out, on any machine.
"""

import math
import re
from collections import Counter
from typing import Any, Dict, List, Optional

from nlp_pipeline.shared_types import NormalizedDocument

# --------------------------------------------------------------------------- vocabulary

# Small, hand-written and visible for the same reason preprocessing.STOPWORDS is: a
# feature layer that pulls from an nltk corpus download would not be reproducible
# without pinning and shipping that corpus too.
HEDGE_WORDS = frozenset("""
may might could perhaps possibly presumably arguably seemingly apparently suggests
indicates appears likely somewhat rather relatively
""".split())

BOOSTER_WORDS = frozenset("""
clearly obviously undeniably certainly definitely absolutely undoubtedly plainly
unquestionably surely
""".split())

FIRST_PERSON = frozenset("i me my mine we us our ours".split())
THIRD_PERSON_REPORTING = frozenset(
    "said says according reported reports stated states claims claimed".split()
)

ATTRIBUTION_CUES = re.compile(
    r"\b(?:said|says|according to|reported|stated|told|claim(?:s|ed)?)\b", re.IGNORECASE
)
NUMBER_PATTERN = re.compile(r"\d[\d,.]*")
PERCENT_PATTERN = re.compile(r"\d[\d,.]*\s*%")


def _safe_div(numerator: float, denominator: float) -> float:
    return numerator / denominator if denominator else 0.0


# --------------------------------------------------------------------------- layers

class Textual:
    """Layer 1: structural shape of the document -- length, sentence rhythm, shouting."""

    def compute(self, doc: NormalizedDocument) -> Dict[str, float]:
        words = [t for t in doc.tokens if not t.is_punct]
        sentences = doc.sentences
        sentence_lengths = [
            len([t for t in words if s.start_char <= t.idx < s.end_char])
            for s in sentences
        ]
        alpha_words = [w for w in words if w.text.isalpha()]
        upper_words = [w for w in alpha_words if w.text.isupper() and len(w.text) > 1]
        punct_count = sum(1 for t in doc.tokens if t.is_punct)
        # blank-line separated blocks; a lone document with no blank line is one paragraph
        paragraph_count = max(1, len(re.split(r"\n\s*\n", doc.text.strip()))) if doc.text.strip() else 0

        return {
            "sentence_count": float(len(sentences)),
            "word_count": float(len(words)),
            "avg_sentence_length_words": round(_safe_div(len(words), len(sentences)), 6),
            "sentence_length_stdev": round(_stdev(sentence_lengths), 6),
            "avg_word_length_chars": round(
                _safe_div(sum(len(w.text) for w in alpha_words), len(alpha_words)), 6
            ),
            "punctuation_density": round(_safe_div(punct_count, max(len(doc.tokens), 1)), 6),
            "paragraph_count": float(paragraph_count),
            "uppercase_word_ratio": round(_safe_div(len(upper_words), max(len(alpha_words), 1)), 6),
            "exclamation_count": float(doc.text.count("!")),
            "question_count": float(doc.text.count("?")),
        }


def _stdev(values: List[int]) -> float:
    if len(values) < 2:
        return 0.0
    mean = sum(values) / len(values)
    variance = sum((v - mean) ** 2 for v in values) / len(values)
    return math.sqrt(variance)


class Lexical:
    """Layer 2: vocabulary -- n-gram counts and how varied the wording is.

    Deliberately *not* called TF-IDF: idf needs document-frequency statistics from a
    corpus, and this layer sees one document at a time. What it reports instead is
    honestly named -- term frequency and type-token ratio -- rather than dressing up a
    single-document count as something it is not.
    """

    def __init__(self, max_ngram: int = 2):
        self.max_ngram = max_ngram

    def _ngrams(self, words: List[str], n: int) -> Counter:
        return Counter(tuple(words[i:i + n]) for i in range(len(words) - n + 1))

    def compute(self, doc: NormalizedDocument) -> Dict[str, float]:
        content_words = [t.lower for t in doc.tokens if not t.is_punct and not t.is_stop]
        all_words = [t.lower for t in doc.tokens if not t.is_punct]
        unigrams = Counter(content_words)
        bigrams = self._ngrams(all_words, 2) if self.max_ngram >= 2 and len(all_words) >= 2 else Counter()

        hapax = sum(1 for count in unigrams.values() if count == 1)
        top_bigram_repeats = max(bigrams.values()) if bigrams else 0

        return {
            "vocabulary_size": float(len(unigrams)),
            "type_token_ratio": round(_safe_div(len(unigrams), max(len(content_words), 1)), 6),
            "hapax_legomena_ratio": round(_safe_div(hapax, max(len(unigrams), 1)), 6),
            "top_bigram_repeat_count": float(top_bigram_repeats),
            "stopword_ratio": round(
                _safe_div(len(all_words) - len(content_words), max(len(all_words), 1)), 6
            ),
        }


class EntityAttribution:
    """Layer 5: named entities and how sourced the article is.

    Reads `doc.entities`, which is only populated when `EntityAnalyzer` ran (see
    `entity_analysis.py`). On a document without entities every value is honestly zero
    rather than guessed.
    """

    def compute(self, doc: NormalizedDocument) -> Dict[str, float]:
        entities = doc.entities
        word_count = max(len([t for t in doc.tokens if not t.is_punct]), 1)
        label_counts = Counter(e.label for e in entities)
        unique_keys = {" ".join(e.text.lower().split()) for e in entities}
        attribution_hits = sum(
            1 for s in doc.sentences if ATTRIBUTION_CUES.search(s.text)
        )

        result = {
            "entity_count": float(len(entities)),
            "unique_entity_count": float(len(unique_keys)),
            "entity_density_per_100_words": round(100.0 * _safe_div(len(entities), word_count), 6),
            "attributed_sentence_ratio": round(
                _safe_div(attribution_hits, max(len(doc.sentences), 1)), 6
            ),
        }
        for label in ("PERSON", "ORG", "NORP", "GPE"):
            result["entity_count_" + label] = float(label_counts.get(label, 0))
        return result


class SentimentSubjectivity:
    """Layer 6: emotional tone and how opinionated the writing sounds.

    Sentiment uses VADER -- a lexicon plus rules, not a model, so it cannot drift (the
    same reasoning `entity_analysis.py` already applies). Subjectivity has no equivalent
    off-the-shelf deterministic tool, so it is approximated from two visible, auditable
    counts: hedge/booster words and first-person pronoun density.

    Lazy-loaded: building a `SentimentIntensityAnalyzer` is cheap, but importing
    `vaderSentiment` costs something, and a caller that only wants the structural or
    lexical layers should not pay for it.
    """

    def __init__(self):
        self._analyzer = None

    @property
    def analyzer(self):
        if self._analyzer is None:
            from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
            self._analyzer = SentimentIntensityAnalyzer()
        return self._analyzer

    def compute(self, doc: NormalizedDocument) -> Dict[str, float]:
        if doc.sentences:
            compounds = [self.analyzer.polarity_scores(s.text)["compound"] for s in doc.sentences]
        else:
            compounds = [self.analyzer.polarity_scores(doc.text)["compound"]] if doc.text else [0.0]

        words = [t.lower for t in doc.tokens if not t.is_punct]
        hedges = sum(1 for w in words if w in HEDGE_WORDS)
        boosters = sum(1 for w in words if w in BOOSTER_WORDS)
        first_person = sum(1 for w in words if w in FIRST_PERSON)

        return {
            "polarity_mean": round(_safe_div(sum(compounds), len(compounds)), 6),
            "polarity_max_abs": round(max((abs(c) for c in compounds), default=0.0), 6),
            "polarity_stdev": round(_stdev([round(c * 1000) for c in compounds]) / 1000.0, 6),
            "hedge_word_ratio": round(_safe_div(hedges, max(len(words), 1)), 6),
            "booster_word_ratio": round(_safe_div(boosters, max(len(words), 1)), 6),
            "first_person_ratio": round(_safe_div(first_person, max(len(words), 1)), 6),
        }


class FactCheck:
    """Layer 10: how many checkable, numeric claims the text makes, and how supported."""

    def compute(self, doc: NormalizedDocument) -> Dict[str, float]:
        numbers = NUMBER_PATTERN.findall(doc.text)
        percents = PERCENT_PATTERN.findall(doc.text)
        word_count = max(len([t for t in doc.tokens if not t.is_punct]), 1)
        supported = sum(
            1 for s in doc.sentences
            if NUMBER_PATTERN.search(s.text) and re.search(r"\baccording to\b", s.text, re.IGNORECASE)
        )
        density = round(100.0 * _safe_div(len(numbers), word_count), 6)
        sourced_ratio = round(_safe_div(supported, max(len(percents) + len(numbers), 1)), 6)
        return {
            "numeric_claim_count": float(len(numbers)),
            "percentage_claim_count": float(len(percents)),
            "numeric_density_per_100_words": density,
            "sourced_numeric_claim_ratio": sourced_ratio,
        }


class Linguistic:
    """Layer: readability -- crude, deterministic proxies, no external syllable corpus."""

    VOWEL_GROUPS = re.compile(r"[aeiouyAEIOUY]+")

    def _syllables(self, word: str) -> int:
        return max(1, len(self.VOWEL_GROUPS.findall(word)))

    def compute(self, doc: NormalizedDocument) -> Dict[str, float]:
        words = [t.text for t in doc.tokens if t.text.isalpha()]
        sentences = max(len(doc.sentences), 1)
        syllables = sum(self._syllables(w) for w in words)
        word_count = max(len(words), 1)

        # Flesch reading ease, computed from our own tokens/sentences rather than any
        # external NLP call, so it stays reproducible and needs no extra dependency.
        flesch = 206.835 - 1.015 * (word_count / sentences) - 84.6 * (syllables / word_count)
        long_words = sum(1 for w in words if self._syllables(w) >= 3)

        return {
            "avg_syllables_per_word": round(_safe_div(syllables, word_count), 6),
            "flesch_reading_ease": round(flesch, 6),
            "long_word_ratio": round(_safe_div(long_words, word_count), 6),
        }


class Stance:
    """Layer 9 (framing side): first-person vs. reported-speech balance.

    A rough proxy for whether the text reads as the author's own voice (opinion,
    editorial) or as a report of what others said (news writing).
    """

    def compute(self, doc: NormalizedDocument) -> Dict[str, float]:
        words = [t.lower for t in doc.tokens if not t.is_punct]
        first_person = sum(1 for w in words if w in FIRST_PERSON)
        reporting = sum(1 for w in words if w in THIRD_PERSON_REPORTING)
        total = first_person + reporting
        return {
            "first_person_reporting_ratio": round(_safe_div(first_person, max(total, 1)), 6),
            "reported_speech_ratio": round(_safe_div(reporting, max(len(words), 1)), 6),
        }


class Mathematics:
    """Layer: summary statistics over the numbers actually printed in the text."""

    def compute(self, doc: NormalizedDocument) -> Dict[str, float]:
        raw = [m.replace(",", "") for m in NUMBER_PATTERN.findall(doc.text)]
        values = []
        for token in raw:
            try:
                values.append(float(token))
            except ValueError:
                continue
        if not values:
            return {
                "numeric_value_count": 0.0, "numeric_value_mean": 0.0,
                "numeric_value_max": 0.0, "numeric_value_stdev": 0.0,
            }
        mean = sum(values) / len(values)
        variance = sum((v - mean) ** 2 for v in values) / len(values)
        return {
            "numeric_value_count": float(len(values)),
            "numeric_value_mean": round(mean, 6),
            "numeric_value_max": round(max(values), 6),
            "numeric_value_stdev": round(math.sqrt(variance), 6),
        }


class Deterministic:
    """Not a signal about the text -- a signal about the feature bundle itself.

    A short hash of every other layer's output, so two runs of `build_features` over the
    same document can be compared for equality without diffing a large nested dict by
    hand. Matches the project-wide pattern in `deterministic_utils.py`.
    """

    def compute(self, feature_bundle: Dict[str, float]) -> Dict[str, Any]:
        import hashlib
        import json
        text_form = json.dumps(feature_bundle, sort_keys=True)
        return {"feature_hash": hashlib.sha256(text_form.encode("utf-8")).hexdigest()}


class Metadata:
    """Layer 13: source metadata passed straight through, not derived from the text."""

    def compute(self, doc: NormalizedDocument, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        meta = metadata if metadata is not None else doc.metadata
        return {
            "language": doc.language or meta.get("language"),
            "source_type": meta.get("source_type"),
            "has_title": bool(meta.get("title")),
            "has_author": bool(meta.get("author")),
        }


# The layers named in README.md's Phase 1/2/3 table that this module does not build:
# Rhetorical and LogicalFallacy are `rules_engine.py`'s job (they need to quote exact
# evidence, which a numeric feature cannot do); Framing/Narrative, Temporal/Contextual
# and Cross-Document/Network need argument mining, publication dates and a corpus of
# other articles respectively -- none of which exist yet, for the same reasons the nine
# detector categories at the bottom of conf/taxonomy_v1.yaml are parked. Building a
# layer that always returns zeros would be worse than not building it: it would look
# like a real signal that just happens to never fire.


class FeatureExtractor:
    """Runs the configured layers and flattens their output into one feature bundle.

    `feature_config["layers"]` is the list of layer names to run; defaults to every
    layer that needs no extra config. Each key in the returned dict is
    "<layer_name>.<field>", so two layers can never collide even if they happen to pick
    the same field name.
    """

    DEFAULT_LAYERS = (
        "textual", "lexical", "entity_attribution", "sentiment_subjectivity",
        "fact_check", "linguistic", "stance", "mathematics", "metadata",
    )

    def __init__(self, feature_config: Dict[str, Any] = None):
        self.config = feature_config or {}
        wanted = self.config.get("layers", self.DEFAULT_LAYERS)
        self._layers = {name: self._build_layer(name) for name in wanted}

    def _build_layer(self, name: str):
        builders = {
            "textual": Textual,
            "lexical": lambda: Lexical(max_ngram=self.config.get("max_ngram", 2)),
            "entity_attribution": EntityAttribution,
            "sentiment_subjectivity": SentimentSubjectivity,
            "fact_check": FactCheck,
            "linguistic": Linguistic,
            "stance": Stance,
            "mathematics": Mathematics,
            "metadata": Metadata,
        }
        if name not in builders:
            raise ValueError("unknown feature layer: " + repr(name))
        return builders[name]()

    def _tokenize(self, text: str) -> List[str]:
        """Kept for interface parity with the original design; tokenization already
        happened in `preprocessing.TextProcessor` by the time a document reaches here."""
        return re.findall(r"\w+", text)

    def _extract_ngrams(self, tokens: List[str]) -> Counter:
        return Counter(zip(tokens, tokens[1:])) if len(tokens) > 1 else Counter()

    def build_features(self, normalized_doc: NormalizedDocument, sentences=None,
                       metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """`sentences` is accepted for interface parity with the design in README.md
        (`FeatureExtractor.build_features(normalized, sentences, metadata)`); the
        document's own `.sentences` is what actually gets used, since that is the
        authoritative, offset-checked list `SentenceSegmenter` produced."""
        bundle: Dict[str, Any] = {}
        for name, layer in self._layers.items():
            if name == "metadata":
                values = layer.compute(normalized_doc, metadata)
            else:
                values = layer.compute(normalized_doc)
            for key, value in values.items():
                bundle[name + "." + key] = value

        bundle["deterministic.feature_hash"] = Deterministic().compute(bundle)["feature_hash"]
        return bundle

    def numeric_vector(self, feature_bundle: Dict[str, Any]) -> List[float]:
        """The subset of a feature bundle that is actually numeric, in a fixed (sorted
        by key) order -- what `MLClassifier` needs to build a vector it can feed a model."""
        return [
            float(v) for k, v in sorted(feature_bundle.items())
            if isinstance(v, (int, float)) and not isinstance(v, bool)
        ]
