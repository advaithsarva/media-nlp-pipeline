"""Dumps per-document rule-engine composite scores keyed by BABE uuid, for the hybrid
alpha-blend sweep in run_hybrid.py (needs rule and neural scores aligned by document)."""

import json
import math
import pickle
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = Path(__file__).resolve().parent / "data"

with open(ROOT / "conf" / "taxonomy_v1.yaml", encoding="utf-8") as f:
    TAXONOMY_RAW = yaml.safe_load(f)
with open(ROOT / "conf" / "scoring_v1.yaml", encoding="utf-8") as f:
    SCORING_CONF_FULL = yaml.safe_load(f)
SCORING_CONF = SCORING_CONF_FULL["scoring"]
WEIGHTS = SCORING_CONF_FULL["category_weights"]
INCREMENTS = SCORING_CONF_FULL["additive_increments"]
FAMILY_OF = {c["id"]: c.get("family") for c in TAXONOMY_RAW["categories"]}
NON_STYLE_IDS = [c for c, fam in FAMILY_OF.items() if fam != "style"]
LAM = float(SCORING_CONF.get("lambda", 4.0))
BETA = float(SCORING_CONF.get("beta", 0.5))


def additive_manipulation(spans, word_count):
    raw_by_cat = {}
    for s in spans:
        w = float(WEIGHTS.get(s["category"], 1.0))
        raw_by_cat.setdefault(s["category"], 0.0)
        raw_by_cat[s["category"]] += s["confidence"] * w
    total = 0.0
    for cat in NON_STYLE_IDS:
        raw = raw_by_cat.get(cat, 0.0)
        if raw <= 0:
            continue
        density = raw / (max(word_count, 1) ** BETA)
        score = 1.0 - math.exp(-LAM * density)
        if score > 0:
            total += INCREMENTS.get(cat, 0.1)
    return min(total, 1.0)


def main():
    for split in ("train", "test"):
        with open(DATA_DIR / f"babe_{split}_spans.pkl", "rb") as f:
            docs = pickle.load(f)
        out = {d["uuid"]: additive_manipulation(d["spans"], d["word_count"]) for d in docs}
        with open(DATA_DIR / f"rule_scores_{split}.json", "w", encoding="utf-8") as f:
            json.dump(out, f)
        print(split, len(out), "written")


if __name__ == "__main__":
    main()
