"""Second-order check on the F1 noisy-OR/smooth-max comparison.

score_and_fit.py found noisy_or and smooth_max producing byte-identical PropScore
values on BABE. That's not a bug: with at most one propaganda-family category firing
per example (confirmed: 0/1000 test sentences have 2+ categories firing), a noisy-OR
over a single value and a smooth-max over a single value are the same number by
construction (both reduce to the identity). The two aggregators only diverge when
multiple techniques co-occur in the same scored unit -- which is what the original
worked example in observe.md 10.4 (a full paragraph, 0.93 vs 0.48) actually had, and
isolated single-sentence BABE rows structurally cannot.

BABE's `news_link` groups multiple annotated sentences from the same article. This
script concatenates same-article sentences (news_link groups of size >= 2) into a
real multi-sentence document, reruns the pipeline (so segmentation, not string
concatenation, defines the sentence boundaries the detectors see), and compares the
two aggregators there -- the condition under which the fix was designed to matter.
Article label = 1 if any of its sentences was annotated biased.
"""

import json
import math
import sys
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from main import PipelineRunner   # noqa: E402

with open(ROOT / "conf" / "taxonomy_v1.yaml", encoding="utf-8") as f:
    TAXONOMY_RAW = yaml.safe_load(f)
with open(ROOT / "conf" / "scoring_v1.yaml", encoding="utf-8") as f:
    SCORING_CONF = yaml.safe_load(f)["scoring"]
with open(ROOT / "conf" / "scoring_v1.yaml", encoding="utf-8") as f:
    WEIGHTS = yaml.safe_load(f)["category_weights"]

FAMILY_OF = {c["id"]: c.get("family") for c in TAXONOMY_RAW["categories"]}
PROPAGANDA_IDS = [c for c, fam in FAMILY_OF.items() if fam == "propaganda"]
LAM = float(SCORING_CONF.get("lambda", 4.0))
BETA = float(SCORING_CONF.get("beta", 0.5))
GAMMA = float(SCORING_CONF.get("prop_score_gamma", 4.0))


def group_articles(split):
    rows = [json.loads(l) for l in
            open(ROOT / "research" / "data" / f"babe_{split}_raw.jsonl", encoding="utf-8")]
    groups = defaultdict(list)
    for r in rows:
        if r.get("news_link"):
            groups[r["news_link"]].append(r)
    return [g for g in groups.values() if len(g) >= 2]


def prop_score_both(spans, word_count):
    raw_by_cat = defaultdict(float)
    for s in spans:
        raw_by_cat[s.category] += s.confidence * float(WEIGHTS.get(s.category, 1.0))
    present = []
    for cat in PROPAGANDA_IDS:
        raw = raw_by_cat.get(cat, 0.0)
        if raw <= 0:
            continue
        density = raw / (max(word_count, 1) ** BETA)
        present.append(1.0 - math.exp(-LAM * density))
    if not present:
        return 0.0, 0.0, 0
    prod = 1.0
    for v in present:
        prod *= (1.0 - v)
    noisy_or = min(max(1.0 - prod, 0.0), 1.0)
    total = sum(math.exp(GAMMA * v) for v in present)
    smooth_max = min(max(math.log(total / len(present)) / GAMMA, 0.0), 1.0)
    return noisy_or, smooth_max, len(present)


def main():
    runner = PipelineRunner()
    all_results = []
    for split in ("train", "test"):
        groups = group_articles(split)
        for group in groups:
            text = " ".join(r["text"] for r in group)
            label = 1 if any(r["label"] == 1 for r in group) else 0
            normalized = runner.processor.normalize(
                runner.router.route_push_input({"text": text, "source_type": "api_rest"})
            )
            runner.segmenter.segment(normalized)
            if runner.entities is not None:
                runner.entities.analyze(normalized)
            result = runner.rules.classify(normalized)
            noisy_or, smooth_max, n_present = prop_score_both(result.spans, normalized.word_count)
            all_results.append({
                "split": split, "n_sentences": len(group), "label": label,
                "n_propaganda_categories_present": n_present,
                "noisy_or": noisy_or, "smooth_max": smooth_max,
                "gap": noisy_or - smooth_max,
            })
        print(f"{split}: {len(groups)} multi-sentence articles (news_link groups size>=2)")

    multi_cat = [r for r in all_results if r["n_propaganda_categories_present"] >= 2]
    print(f"\narticles with >=2 propaganda categories co-firing: {len(multi_cat)} / {len(all_results)}")
    if multi_cat:
        mean_gap = sum(r["gap"] for r in multi_cat) / len(multi_cat)
        max_gap = max(r["gap"] for r in multi_cat)
        print(f"mean noisy_or - smooth_max gap on those: {mean_gap:.4f}, max gap: {max_gap:.4f}")
        for r in sorted(multi_cat, key=lambda r: -r["gap"])[:5]:
            print(f"  n_cats={r['n_propaganda_categories_present']} noisy_or={r['noisy_or']:.4f} "
                  f"smooth_max={r['smooth_max']:.4f} gap={r['gap']:.4f} label={r['label']}")

    out = ROOT / "research" / "data" / "article_level_results.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2)
    print("\nwrote", out)


if __name__ == "__main__":
    main()
