"""Reads conf/taxonomy_v1.yaml into checked objects.

The point of loading rather than using the raw dict is to fail here, at startup, with a
clear message, instead of failing later inside the rules engine with a KeyError.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any

VALID_DETECTORS = ("lexicon", "regex")


@dataclass
class Category:
    id: str
    name: str
    detector: str
    base_confidence: float
    description: str = ""
    terms: List[str] = field(default_factory=list)
    patterns: List[str] = field(default_factory=list)


@dataclass
class Taxonomy:
    version: str
    default_threshold: float
    categories: List[Category]

    def ids(self) -> List[str]:
        return [c.id for c in self.categories]


def load_taxonomy(conf: Dict[str, Any]) -> Taxonomy:
    if not conf or "categories" not in conf:
        raise ValueError("taxonomy config is empty or has no 'categories' key")

    header = conf.get("taxonomy", {})
    categories = []
    seen = set()

    for raw in conf["categories"]:
        cat_id = raw.get("id")
        if not cat_id:
            raise ValueError(f"category with no id: {raw}")
        # duplicate ids would silently overwrite each other in every downstream dict
        if cat_id in seen:
            raise ValueError(f"duplicate category id: {cat_id}")
        seen.add(cat_id)

        detector = raw.get("detector")
        if detector not in VALID_DETECTORS:
            raise ValueError(f"{cat_id}: detector must be one of {VALID_DETECTORS}, got {detector!r}")

        rules = raw.get("terms") if detector == "lexicon" else raw.get("patterns")
        if not rules:
            raise ValueError(f"{cat_id}: a {detector} category needs a non-empty rule list")

        categories.append(Category(
            id=cat_id,
            name=raw.get("name", cat_id),
            detector=detector,
            base_confidence=float(raw.get("base_confidence", 0.8)),
            description=raw.get("description", "").strip(),
            terms=raw.get("terms", []),
            patterns=raw.get("patterns", []),
        ))

    return Taxonomy(
        version=str(header.get("version", "0.0.0")),
        default_threshold=float(header.get("default_threshold", 0.8)),
        categories=categories,
    )
