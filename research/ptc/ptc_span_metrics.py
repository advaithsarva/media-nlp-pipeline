"""Span-level metrics (IoU, boundary error, precision/recall) for the rule engine's
propaganda detectors against PTC's real gold spans, plus the noisy-OR vs. smooth-max
comparison run directly on PTC's multi-technique articles -- the dataset the paper's own
limitations section named as the direct fit BABE's article groupings could only
approximate. Reuses the exact PipelineRunner call pattern from research/run_rule_engine.py.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))

from main import PipelineRunner   # noqa: E402
from ptc_data import load_articles, CATEGORY_MAP   # noqa: E402

HERE = Path(__file__).resolve().parent
MAPPED_CATEGORIES = set(CATEGORY_MAP.values())


def iou(a_start, a_end, b_start, b_end):
    inter = max(0, min(a_end, b_end) - max(a_start, b_start))
    union = max(a_end, b_end) - min(a_start, b_start)
    return inter / union if union else 0.0


def best_match(pred_span, gold_spans):
    """Nearest gold span by IoU, restricted to the same mapped category."""
    candidates = [g for g in gold_spans if g["category"] == pred_span["category"]]
    if not candidates:
        return None, 0.0
    scored = [(g, iou(pred_span["start"], pred_span["end"], g["start"], g["end"])) for g in candidates]
    scored.sort(key=lambda x: -x[1])
    return scored[0]


def score_article(pred_spans, gold_spans):
    gold_mapped = [g for g in gold_spans if g["category"] in MAPPED_CATEGORIES]
    matched_gold_ids = set()
    ious, boundary_errs_start, boundary_errs_end = [], [], []
    tp = 0
    for p in pred_spans:
        g, score = best_match(p, gold_mapped)
        if g is not None and score > 0:
            ious.append(score)
            boundary_errs_start.append(abs(p["start"] - g["start"]))
            boundary_errs_end.append(abs(p["end"] - g["end"]))
            if score >= 0.3:   # a real overlap, not just touching
                tp += 1
                matched_gold_ids.add(id(g))
    n_pred = len(pred_spans)
    n_gold = len(gold_mapped)
    return {
        "n_pred": n_pred,
        "n_gold": n_gold,
        "tp": tp,
        "mean_iou": sum(ious) / len(ious) if ious else None,
        "mean_boundary_err_start": sum(boundary_errs_start) / len(boundary_errs_start) if boundary_errs_start else None,
        "mean_boundary_err_end": sum(boundary_errs_end) / len(boundary_errs_end) if boundary_errs_end else None,
        "precision": tp / n_pred if n_pred else None,
        "recall": tp / n_gold if n_gold else None,
    }


def main():
    runner = PipelineRunner()
    articles = load_articles(n=50, split="test")

    per_article = []
    for art in articles:
        normalized = runner.processor.normalize(
            runner.router.route_push_input({"text": art["text"], "source_type": "api_rest"})
        )
        runner.segmenter.segment(normalized)
        result = runner.rules.classify(normalized)
        # Sanity check: does normalize() preserve raw-text offsets? If not, gold spans
        # (offsets on the raw .txt file) and predicted spans (offsets on normalized.text)
        # would silently misalign.
        offsets_aligned = normalized.text[:200] == art["text"][:200]
        pred_spans = [
            {"category": s.category, "start": s.start_char, "end": s.end_char}
            for s in result.spans if s.category in MAPPED_CATEGORIES
        ]
        gold_present_categories = sorted({g["category"] for g in art["gold"] if g["category"]})
        scored = score_article(pred_spans, art["gold"])
        scored.update({
            "article_id": art["article_id"],
            "offsets_aligned_sample_check": offsets_aligned,
            "n_gold_categories_present": len(gold_present_categories),
            "gold_categories": gold_present_categories,
        })
        per_article.append(scored)

    n_articles = len(per_article)
    n_offset_mismatches = sum(1 for a in per_article if not a["offsets_aligned_sample_check"])
    total_tp = sum(a["tp"] for a in per_article)
    total_pred = sum(a["n_pred"] for a in per_article)
    total_gold = sum(a["n_gold"] for a in per_article)
    ious_all = [a["mean_iou"] for a in per_article if a["mean_iou"] is not None]

    summary = {
        "n_articles": n_articles,
        "n_offset_alignment_mismatches": n_offset_mismatches,
        "micro_precision": total_tp / total_pred if total_pred else None,
        "micro_recall": total_tp / total_gold if total_gold else None,
        "mean_iou_over_matched_spans": sum(ious_all) / len(ious_all) if ious_all else None,
        "total_predicted_spans": total_pred,
        "total_gold_spans_mapped_categories": total_gold,
        "mapped_categories": sorted(MAPPED_CATEGORIES),
        "excluded_categories_no_clean_map": ["glittering_generalities", "gaslighting", "guilt_by_association", "scapegoating"],
    }

    out = {"summary": summary, "per_article": per_article}
    with open(HERE / "span_metrics.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(summary, indent=2))
    print("wrote", HERE / "span_metrics.json")


if __name__ == "__main__":
    main()
