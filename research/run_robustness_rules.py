"""Robustness module, rule-engine half: F1 degradation under character-level noise.

Re-runs the full rule pipeline on the BABE test split at two noise rates (5%, 15%
per-character substitution/deletion), at the same operating point (composite +
threshold) chosen on clean train data in score_and_fit.py, so noised numbers are
comparable to the clean baseline rather than re-optimised against the noise. Also
reports the numbers with the difflib mitigation from noise.py applied before the
text reaches the pipeline.
"""

import json
import math
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from main import PipelineRunner                          # noqa: E402
from babe_data import load_split                          # noqa: E402
from noise import noise_text, build_vocab, spellcheck_mitigate, _bucket_by_length   # noqa: E402

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
THRESHOLD = 0.01   # fitted on clean train in score_and_fit.py for additive_manipulation


def additive_manipulation(spans, word_count):
    raw_by_cat = {}
    for s in spans:
        w = float(WEIGHTS.get(s.category, 1.0))
        raw_by_cat.setdefault(s.category, 0.0)
        raw_by_cat[s.category] += s.confidence * w
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


def run_condition(runner, texts, labels, threshold=THRESHOLD, tag=""):
    tp = fp = fn = tn = 0
    for i, (text, y) in enumerate(zip(texts, labels)):
        if i % 100 == 0:
            print(f"  {tag} {i}/{len(texts)}", flush=True)
        normalized = runner.processor.normalize(
            runner.router.route_push_input({"text": text, "source_type": "api_rest"})
        )
        runner.segmenter.segment(normalized)
        if runner.entities is not None:
            runner.entities.analyze(normalized)
        result = runner.rules.classify(normalized)
        value = additive_manipulation(result.spans, normalized.word_count)
        pred = 1 if value >= threshold else 0
        if pred == 1 and y == 1:
            tp += 1
        elif pred == 1 and y == 0:
            fp += 1
        elif pred == 0 and y == 1:
            fn += 1
        else:
            tn += 1
    p = tp / (tp + fp) if (tp + fp) else 0.0
    r = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * p * r / (p + r) if (p + r) else 0.0
    return {"precision": p, "recall": r, "f1": f1, "tp": tp, "fp": fp, "fn": fn, "tn": tn}


def main():
    import sys
    n_sample = int(sys.argv[1]) if len(sys.argv) > 1 else 1000

    train = load_split("train")
    test = load_split("test")[:n_sample]
    vocab = build_vocab([r["text"] for r in train], max_size=3000)
    buckets = _bucket_by_length(vocab)

    runner = PipelineRunner()
    test_texts = [r["text"] for r in test]
    test_labels = [r["label"] for r in test]
    print(f"running on {len(test_texts)} test examples", flush=True)

    results = {"n_examples": len(test_texts)}
    results["clean"] = run_condition(runner, test_texts, test_labels, tag="clean")

    for rate in (0.05, 0.15):
        noised = [noise_text(t, rate, seed=hash((t, rate)) & 0xFFFFFFFF) for t in test_texts]
        results[f"noise_{rate}"] = run_condition(runner, noised, test_labels, tag=f"noise_{rate}")
        mitigated = [spellcheck_mitigate(t, vocab, buckets=buckets) for t in noised]
        results[f"noise_{rate}_mitigated"] = run_condition(
            runner, mitigated, test_labels, tag=f"noise_{rate}_mitigated")
        print(f"rate={rate} noised_f1={results[f'noise_{rate}']['f1']:.4f} "
              f"mitigated_f1={results[f'noise_{rate}_mitigated']['f1']:.4f}", flush=True)

    out = ROOT / "research" / "data" / "robustness_rules.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(json.dumps(results, indent=2))
    print("wrote", out)


if __name__ == "__main__":
    main()
