"""F1 (noisy-OR vs smooth-max, measured) and F2 (fitting lambda/beta/gamma) against BABE.

Reads the cached spans from run_rule_engine.py. Recomputes ScoringEngine's two formulas
by hand (category saturation + PropScore) rather than importing the class, because the
cache stores plain dicts, not the dataclasses ScoringEngine expects -- reimplementing ~15
lines here is simpler and safer than reconstructing EvidenceSpan/NormalizedDocument
objects just to satisfy an interface. The formulas are copied verbatim from
scoring_engine.py; conf/scoring_v1.yaml's hand-chosen constants (lambda 4.0, beta 0.5,
gamma 4.0) are the ones being tested and fit here.
"""

import json
import math
import pickle
import sys
from itertools import product
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = Path(__file__).resolve().parent / "data"

with open(ROOT / "conf" / "scoring_v1.yaml", encoding="utf-8") as f:
    SCORING_CONF = yaml.safe_load(f)["scoring"]
with open(ROOT / "conf" / "taxonomy_v1.yaml", encoding="utf-8") as f:
    TAXONOMY_RAW = yaml.safe_load(f)

FAMILY_OF = {c["id"]: c.get("family") for c in TAXONOMY_RAW["categories"]}
WEIGHTS = yaml.safe_load(open(ROOT / "conf" / "scoring_v1.yaml", encoding="utf-8"))["category_weights"]
PROPAGANDA_IDS = [c for c, fam in FAMILY_OF.items() if fam == "propaganda"]
NON_STYLE_IDS = [c for c, fam in FAMILY_OF.items() if fam != "style"]
INCREMENTS = yaml.safe_load(open(ROOT / "conf" / "scoring_v1.yaml", encoding="utf-8"))["additive_increments"]

HAND_LAMBDA = float(SCORING_CONF.get("lambda", 4.0))
HAND_BETA = float(SCORING_CONF.get("beta", 0.5))
HAND_GAMMA = float(SCORING_CONF.get("prop_score_gamma", 4.0))


def load_cache(split):
    with open(DATA_DIR / f"babe_{split}_spans.pkl", "rb") as f:
        return pickle.load(f)


def _category_scores(doc, lam, beta, ids):
    """raw -> density -> saturation, per category, restricted to `ids`."""
    raw_by_cat = {}
    for span in doc["spans"]:
        w = float(WEIGHTS.get(span["category"], 1.0))
        raw_by_cat.setdefault(span["category"], 0.0)
        raw_by_cat[span["category"]] += span["confidence"] * w
    word_count = max(doc["word_count"], 1)
    scores = {}
    for cat in ids:
        raw = raw_by_cat.get(cat, 0.0)
        if raw <= 0:
            scores[cat] = 0.0
            continue
        density = raw / (word_count ** beta)
        scores[cat] = 1.0 - math.exp(-lam * density)
    return scores


def prop_score(doc, method, lam, beta, gamma):
    scores = _category_scores(doc, lam, beta, PROPAGANDA_IDS)
    present = [v for v in scores.values() if v > 0]
    if not present:
        return 0.0
    if method == "noisy_or":
        product_ = 1.0
        for v in present:
            product_ *= (1.0 - v)
        value = 1.0 - product_
    else:
        total = sum(math.exp(gamma * v) for v in present)
        value = math.log(total / len(present)) / gamma
    return min(max(value, 0.0), 1.0)


def additive_manipulation(doc, lam, beta):
    scores = _category_scores(doc, lam, beta, NON_STYLE_IDS)
    fired = [(cat, sc) for cat, sc in scores.items() if sc > 0]
    total = sum(INCREMENTS.get(cat, 0.1) for cat, _ in fired)
    return min(total, 1.0)


def _prf1(tp, fp, fn):
    p = tp / (tp + fp) if (tp + fp) else 0.0
    r = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * p * r / (p + r) if (p + r) else 0.0
    return p, r, f1


def score_threshold(values, labels, threshold):
    tp = fp = fn = tn = 0
    for v, y in zip(values, labels):
        pred = 1 if v >= threshold else 0
        if pred == 1 and y == 1:
            tp += 1
        elif pred == 1 and y == 0:
            fp += 1
        elif pred == 0 and y == 1:
            fn += 1
        else:
            tn += 1
    p, r, f1 = _prf1(tp, fp, fn)
    return {"threshold": threshold, "precision": p, "recall": r, "f1": f1,
            "tp": tp, "fp": fp, "fn": fn, "tn": tn}


def best_threshold(values, labels, grid=None):
    grid = grid or [i / 100 for i in range(1, 100)]
    best = max((score_threshold(values, labels, t) for t in grid), key=lambda r: r["f1"])
    return best


def span_level_prf1(docs):
    """Word-overlap P/R/F1 between fired-span text and BABE's biased_words list."""
    tp = fp = fn = 0
    for doc in docs:
        predicted_words = set()
        for s in doc["spans"]:
            predicted_words.update(w.lower().strip(".,!?\"'") for w in s["text"].split())
        gold_words = set(w.lower().strip(".,!?\"'") for w in doc["biased_words"])
        tp += len(predicted_words & gold_words)
        fp += len(predicted_words - gold_words)
        fn += len(gold_words - predicted_words)
    p, r, f1 = _prf1(tp, fp, fn)
    return {"precision": p, "recall": r, "f1": f1, "tp": tp, "fp": fp, "fn": fn}


def main():
    train = load_cache("train")
    test = load_cache("test")
    train_labels = [d["label"] for d in train]
    test_labels = [d["label"] for d in test]

    results = {}

    # ---- F1: noisy_or vs smooth_max, hand-chosen constants, threshold fit on train only ----
    for method in ("noisy_or", "smooth_max"):
        train_vals = [prop_score(d, method, HAND_LAMBDA, HAND_BETA, HAND_GAMMA) for d in train]
        test_vals = [prop_score(d, method, HAND_LAMBDA, HAND_BETA, HAND_GAMMA) for d in test]
        op_point = best_threshold(train_vals, train_labels)
        test_score = score_threshold(test_vals, test_labels, op_point["threshold"])
        results[f"prop_score_{method}"] = {
            "train_fitted_threshold": op_point["threshold"],
            "train_f1_at_threshold": op_point["f1"],
            "test": test_score,
            "mean_value_train": sum(train_vals) / len(train_vals),
            "mean_value_test": sum(test_vals) / len(test_vals),
        }

    # ---- additive_manipulation, hand-chosen constants (general predictor, not the F1 target) ----
    train_vals = [additive_manipulation(d, HAND_LAMBDA, HAND_BETA) for d in train]
    test_vals = [additive_manipulation(d, HAND_LAMBDA, HAND_BETA) for d in test]
    op_point = best_threshold(train_vals, train_labels)
    results["additive_manipulation"] = {
        "train_fitted_threshold": op_point["threshold"],
        "train_f1_at_threshold": op_point["f1"],
        "test": score_threshold(test_vals, test_labels, op_point["threshold"]),
    }

    # ---- span-level P/R/F1 against biased_words ----
    results["span_level"] = {"train": span_level_prf1(train), "test": span_level_prf1(test)}

    # ---- F2: fit lambda, beta, gamma on train (smooth_max prop_score, maximise F1), test held out ----
    lam_grid = [1.0, 2.0, 4.0, 6.0, 8.0, 12.0]
    beta_grid = [0.0, 0.25, 0.5, 0.75, 1.0]
    gamma_grid = [1.0, 2.0, 4.0, 6.0, 8.0, 12.0]

    best = None
    for lam, beta, gamma in product(lam_grid, beta_grid, gamma_grid):
        train_vals = [prop_score(d, "smooth_max", lam, beta, gamma) for d in train]
        op = best_threshold(train_vals, train_labels, grid=[i / 20 for i in range(1, 20)])
        if best is None or op["f1"] > best["f1"]:
            best = {"lambda": lam, "beta": beta, "gamma": gamma,
                    "threshold": op["threshold"], "f1": op["f1"]}

    fitted_test_vals = [prop_score(d, "smooth_max", best["lambda"], best["beta"], best["gamma"])
                         for d in test]
    fitted_test_score = score_threshold(fitted_test_vals, test_labels, best["threshold"])

    results["f2_fitting"] = {
        "hand_chosen": {"lambda": HAND_LAMBDA, "beta": HAND_BETA, "gamma": HAND_GAMMA},
        "fitted_on_train": best,
        "fitted_test_score": fitted_test_score,
        "hand_chosen_test_score": results["prop_score_smooth_max"]["test"],
    }

    out = DATA_DIR / "f1_f2_results.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(json.dumps(results, indent=2))
    print("\nwrote", out)


if __name__ == "__main__":
    main()
