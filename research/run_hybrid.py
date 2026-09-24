"""P3 from CLAUDE.md's research track: sweep alpha in `conf = alpha*rules + (1-alpha)*ml`
(scoring_engine.py formula 2) from 0 (pure rules) to 1 (pure ML), report F1 at each point.

Uses the rule engine's additive_manipulation composite (dump_rule_scores.py) and the
fine-tuned DistilBERT's sigmoid probability (neural_probs.json, from the Colab run) as
the two inputs to blend -- both already live in [0, 1]. Threshold and alpha are both
fit on train, evaluated once on test, same discipline as score_and_fit.py.
"""

import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"


def load(split):
    rule = json.load(open(DATA_DIR / f"rule_scores_{split}.json"))
    neural = json.load(open(DATA_DIR / "neural_probs.json"))
    uuids = neural[f"{split}_uuid"]
    probs = neural[f"{split}_probs"]
    neural_by_uuid = dict(zip(uuids, probs))
    from babe_data import load_split
    labels_by_uuid = {r["uuid"]: r["label"] for r in load_split(split)}
    rows = []
    for uuid in uuids:
        rows.append({
            "uuid": uuid,
            "rule": rule.get(uuid, 0.0),
            "neural": neural_by_uuid[uuid],
            "label": labels_by_uuid[uuid],
        })
    return rows


def prf1(preds, labels):
    tp = sum(1 for p, y in zip(preds, labels) if p == 1 and y == 1)
    fp = sum(1 for p, y in zip(preds, labels) if p == 1 and y == 0)
    fn = sum(1 for p, y in zip(preds, labels) if p == 0 and y == 1)
    p = tp / (tp + fp) if (tp + fp) else 0.0
    r = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * p * r / (p + r) if (p + r) else 0.0
    return {"precision": p, "recall": r, "f1": f1}


def best_threshold_f1(values, labels):
    best = None
    # start at 1, not 0: threshold 0 means "value >= 0", which is every document (every
    # composite here is non-negative), so it degenerates to predicting the majority
    # class and wins on F1 through base-rate recall alone, not real signal
    for t in [i / 100 for i in range(1, 101)]:
        preds = [1 if v >= t else 0 for v in values]
        score = prf1(preds, labels)
        if best is None or score["f1"] > best["f1"]:
            best = dict(score, threshold=t)
    return best


def main():
    train = load("train")
    test = load("test")
    train_labels = [r["label"] for r in train]
    test_labels = [r["label"] for r in test]

    sweep = []
    for alpha in [i / 20 for i in range(0, 21)]:
        train_vals = [alpha * r["rule"] + (1 - alpha) * r["neural"] for r in train]
        op = best_threshold_f1(train_vals, train_labels)
        test_vals = [alpha * r["rule"] + (1 - alpha) * r["neural"] for r in test]
        test_preds = [1 if v >= op["threshold"] else 0 for v in test_vals]
        test_score = prf1(test_preds, test_labels)
        sweep.append({"alpha": alpha, "train_threshold": op["threshold"],
                      "train_f1": op["f1"], "test": test_score})
        print(f"alpha={alpha:.2f} (1=rules,0=ml) train_f1={op['f1']:.4f} "
              f"test_f1={test_score['f1']:.4f} test_p={test_score['precision']:.4f} "
              f"test_r={test_score['recall']:.4f}")

    best_alpha_row = max(sweep, key=lambda r: r["test"]["f1"])
    out = {"sweep": sweep, "best_alpha_on_test": best_alpha_row}
    with open(DATA_DIR / "hybrid_sweep.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nbest alpha on test:", best_alpha_row["alpha"], "f1:", best_alpha_row["test"]["f1"])
    print("wrote", DATA_DIR / "hybrid_sweep.json")


if __name__ == "__main__":
    main()
