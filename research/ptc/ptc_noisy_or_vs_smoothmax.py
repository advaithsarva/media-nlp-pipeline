"""Noisy-OR vs. smooth-max PropScore, run on PTC directly -- the dataset the paper's own
limitations section named as the more direct fit for this comparison than BABE's article
groupings (which only found 2 multi-category articles out of 734). PTC articles have real,
frequent multi-technique co-occurrence, so this should be far better powered. Reuses
score_and_fit.py's prop_score() and this project's own PipelineRunner, same pattern as
ptc_span_metrics.py. Runs over all 371 PTC train articles (not just the 50-article span
sample) for statistical power, since this comparison doesn't need gold labels at all --
only spans the rule engine itself produces."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "research"))

from main import PipelineRunner   # noqa: E402
from score_and_fit import prop_score, HAND_LAMBDA, HAND_BETA, HAND_GAMMA, PROPAGANDA_IDS   # noqa: E402
from ptc_data import ART_DIR   # noqa: E402

HERE = Path(__file__).resolve().parent


def main():
    runner = PipelineRunner()
    ids = sorted(p.stem.replace("article", "") for p in ART_DIR.glob("article*.txt"))

    results = []
    for i, aid in enumerate(ids):
        text = (ART_DIR / f"article{aid}.txt").read_text(encoding="utf-8")
        normalized = runner.processor.normalize(
            runner.router.route_push_input({"text": text, "source_type": "api_rest"})
        )
        runner.segmenter.segment(normalized)
        result = runner.rules.classify(normalized)
        doc = {
            "spans": [{"category": s.category, "confidence": s.confidence} for s in result.spans],
            "word_count": max(normalized.word_count, 1),
        }
        categories_present = {s["category"] for s in doc["spans"] if s["category"] in PROPAGANDA_IDS}
        noisy_or = prop_score(doc, "noisy_or", HAND_LAMBDA, HAND_BETA, HAND_GAMMA)
        smooth_max = prop_score(doc, "smooth_max", HAND_LAMBDA, HAND_BETA, HAND_GAMMA)
        results.append({
            "article_id": aid,
            "n_propaganda_categories_present": len(categories_present),
            "noisy_or": noisy_or,
            "smooth_max": smooth_max,
            "gap": noisy_or - smooth_max,
        })
        if (i + 1) % 100 == 0:
            print(f"  {i + 1}/{len(ids)}")

    multi = [r for r in results if r["n_propaganda_categories_present"] >= 2]
    nonzero_gap = [r for r in multi if abs(r["gap"]) > 1e-9]
    mean_gap = sum(r["gap"] for r in nonzero_gap) / len(nonzero_gap) if nonzero_gap else None

    summary = {
        "n_articles_total": len(results),
        "n_articles_multi_category": len(multi),
        "n_articles_nonzero_gap": len(nonzero_gap),
        "mean_gap_noisy_or_minus_smooth_max": mean_gap,
        "max_gap": max((r["gap"] for r in nonzero_gap), default=None),
        "min_gap": min((r["gap"] for r in nonzero_gap), default=None),
        "gap_always_positive": all(r["gap"] >= -1e-9 for r in nonzero_gap) if nonzero_gap else None,
    }
    out = {"summary": summary, "multi_category_articles": multi}
    with open(HERE / "noisy_or_vs_smoothmax.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(summary, indent=2))
    print("wrote", HERE / "noisy_or_vs_smoothmax.json")


if __name__ == "__main__":
    main()
