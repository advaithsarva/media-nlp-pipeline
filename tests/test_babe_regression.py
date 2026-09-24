"""Regression tripwire for the BABE measurement in research/ (2026-09-24).

Mirrors the existing gold-set tripwire in test_evaluation.py: this does not claim
BABE F1 0.107 is a good number (it is not -- see research/data/f1_f2_results.json
and observe.md 15), only that it should not get quietly worse. Runs a small, fixed
subset (not the full 1000) so this stays fast enough for every `pytest` run.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "research"))

from main import PipelineRunner
from babe_data import load_split

N_EXAMPLES = 100
FLOOR_F1 = 0.06   # measured on the full 1000: 0.107. Leaves headroom for sampling noise.


def _additive_manipulation(spans, word_count, weights, increments, non_style_ids, lam, beta):
    import math
    raw_by_cat = {}
    for s in spans:
        w = float(weights.get(s.category, 1.0))
        raw_by_cat.setdefault(s.category, 0.0)
        raw_by_cat[s.category] += s.confidence * w
    total = 0.0
    for cat in non_style_ids:
        raw = raw_by_cat.get(cat, 0.0)
        if raw <= 0:
            continue
        density = raw / (max(word_count, 1) ** beta)
        if 1.0 - math.exp(-lam * density) > 0:
            total += increments.get(cat, 0.1)
    return min(total, 1.0)


def test_babe_subset_f1_has_not_regressed():
    runner = PipelineRunner()
    weights = runner.scoring_conf["category_weights"]
    increments = runner.scoring_conf["additive_increments"]
    non_style_ids = [c.id for c in runner.taxonomy.categories if c.family != "style"]
    lam = float(runner.scoring_conf["scoring"].get("lambda", 4.0))
    beta = float(runner.scoring_conf["scoring"].get("beta", 0.5))

    examples = load_split("test")[:N_EXAMPLES]
    tp = fp = fn = 0
    for rec in examples:
        normalized = runner.processor.normalize(
            runner.router.route_push_input({"text": rec["text"], "source_type": "api_rest"})
        )
        runner.segmenter.segment(normalized)
        if runner.entities is not None:
            runner.entities.analyze(normalized)
        result = runner.rules.classify(normalized)
        value = _additive_manipulation(
            result.spans, normalized.word_count, weights, increments, non_style_ids, lam, beta)
        pred = 1 if value >= 0.01 else 0
        if pred == 1 and rec["label"] == 1:
            tp += 1
        elif pred == 1 and rec["label"] == 0:
            fp += 1
        elif pred == 0 and rec["label"] == 1:
            fn += 1

    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0

    assert f1 >= FLOOR_F1, (
        f"rules-only F1 against BABE dropped to {f1:.4f} (floor {FLOOR_F1}) on the first "
        f"{N_EXAMPLES} test examples -- a detector regression, not noise, if this fires"
    )
