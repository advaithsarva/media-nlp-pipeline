"""Measures the detectors against a labelled set.

Read this first, because it decides what the numbers mean.

**The bundled gold set was written by the same person who wrote the detectors.** That makes
it a *specification conformance* set, not an independent evaluation. It answers "does each
detector fire where it was designed to fire, and stay silent where it was designed to stay
silent" -- which catches regressions and is genuinely useful. It does **not** answer "do
these detectors agree with how a human reads the article", because the labels and the rules
came from the same head. A number from this harness must never be quoted as accuracy.

Getting a real number needs annotations someone else made: SemEval-2020 Task 11 PTC for
propaganda spans, BABE for bias, Jin et al. for fallacies. The loader takes any file in the
same JSONL shape, so pointing it at converted external data is the only change needed.

What is measured:

    precision   of the times a detector fired, how often it should have
    recall      of the times it should have fired, how often it did
    F1          the harmonic mean, which punishes a detector that is good at only one
    verbatim    fraction of findings whose quoted text really is the article at those
                offsets. This is 1.0 by construction for a rule engine, and it is the
                baseline the research track compares LLM extraction against.

Run it:

    python -m evaluation.evaluator --gold eval/gold/annotations.jsonl --report eval/report.md
"""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from main import PipelineRunner        # noqa: E402

DEFAULT_GOLD = ROOT / "eval" / "gold" / "annotations.jsonl"


def load_gold(path):
    """One JSON object per line: {id, text, categories, note}.

    `categories` is the complete set expected to fire. An empty list means the example
    must produce nothing -- those are the false-positive cases and they carry most of the
    value, because a detector that fires on everything scores perfect recall.
    """
    examples = []
    with open(path, encoding="utf-8") as f:
        for line_number, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("//"):
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError("bad JSON on line " + str(line_number) + ": " + str(error))
            if "text" not in record:
                raise ValueError("line " + str(line_number) + " has no 'text'")
            record.setdefault("id", "example_" + str(line_number))
            record.setdefault("categories", [])
            examples.append(record)
    return examples


def _counts_to_scores(true_positive, false_positive, false_negative):
    precision = true_positive / (true_positive + false_positive) if (true_positive + false_positive) else None
    recall = true_positive / (true_positive + false_negative) if (true_positive + false_negative) else None
    if precision and recall:
        f1 = 2 * precision * recall / (precision + recall)
    elif precision is None and recall is None:
        f1 = None       # the detector was never expected and never fired: no opinion
    else:
        f1 = 0.0
    return precision, recall, f1


def evaluate(examples, runner=None):
    runner = runner or PipelineRunner()
    categories = runner.taxonomy.ids()

    counts = {c: {"tp": 0, "fp": 0, "fn": 0} for c in categories}
    verbatim_ok = 0
    verbatim_total = 0
    per_example = []
    exact_matches = 0

    for example in examples:
        record = runner.process_document({"text": example["text"], "source_type": "api_rest"})
        fired = {f["category"] for f in record["findings"]}
        expected = set(example["categories"])

        for category in categories:
            if category in fired and category in expected:
                counts[category]["tp"] += 1
            elif category in fired:
                counts[category]["fp"] += 1
            elif category in expected:
                counts[category]["fn"] += 1

        # the substring check, run against the text the caller actually submitted
        for finding in record["findings"]:
            verbatim_total += 1
            if example["text"][finding["start_char"]:finding["end_char"]] == finding["text"]:
                verbatim_ok += 1

        if fired == expected:
            exact_matches += 1

        per_example.append({
            "id": example["id"],
            "expected": sorted(expected),
            "fired": sorted(fired),
            "missed": sorted(expected - fired),
            "spurious": sorted(fired - expected),
            "note": example.get("note", ""),
        })

    per_category = {}
    for category in categories:
        c = counts[category]
        precision, recall, f1 = _counts_to_scores(c["tp"], c["fp"], c["fn"])
        per_category[category] = {
            "true_positive": c["tp"], "false_positive": c["fp"], "false_negative": c["fn"],
            "precision": precision, "recall": recall, "f1": f1,
            # a detector nobody wrote an example for has not been measured at all
            "measured": (c["tp"] + c["fp"] + c["fn"]) > 0,
        }

    # macro averages skip the unmeasured detectors: averaging in a None as zero would
    # make the whole system look worse than the evidence supports
    scored = [v for v in per_category.values() if v["f1"] is not None]
    macro_f1 = sum(v["f1"] for v in scored) / len(scored) if scored else None

    total_tp = sum(c["tp"] for c in counts.values())
    total_fp = sum(c["fp"] for c in counts.values())
    total_fn = sum(c["fn"] for c in counts.values())
    micro_p, micro_r, micro_f1 = _counts_to_scores(total_tp, total_fp, total_fn)

    return {
        "examples": len(examples),
        "exact_match": exact_matches,
        "exact_match_rate": round(exact_matches / len(examples), 6) if examples else None,
        "micro": {"precision": micro_p, "recall": micro_r, "f1": micro_f1,
                  "tp": total_tp, "fp": total_fp, "fn": total_fn},
        "macro_f1": macro_f1,
        "verbatim": {
            "checked": verbatim_total,
            "exact": verbatim_ok,
            # 1.0 by construction for a rule engine. It is reported anyway, because it is
            # the baseline an LLM extractor has to be compared against.
            "rate": round(verbatim_ok / verbatim_total, 6) if verbatim_total else None,
        },
        "unmeasured": sorted(c for c, v in per_category.items() if not v["measured"]),
        "per_category": per_category,
        "per_example": per_example,
    }


def _cell(value):
    return "-" if value is None else ("%.3f" % value)


def to_markdown(results, gold_path):
    lines = []
    lines.append("# Detector evaluation")
    lines.append("")
    lines.append("Gold set: `" + str(gold_path) + "` (" + str(results["examples"]) + " examples)")
    lines.append("")
    lines.append("> **These are conformance figures, not accuracy figures.** The labels and")
    lines.append("> the detectors were written by the same person, so this measures whether")
    lines.append("> each detector does what it was specified to do -- not whether the")
    lines.append("> specification matches how a reader would judge the article. Quoting any")
    lines.append("> number here as accuracy would be wrong. See `observe.md` for what an")
    lines.append("> independent evaluation would need.")
    lines.append("")

    micro = results["micro"]
    lines.append("## Overall")
    lines.append("")
    lines.append("| Measure | Value |")
    lines.append("|---|---|")
    lines.append("| Exact match (every category right) | " + str(results["exact_match"])
                 + " / " + str(results["examples"]) + " = " + _cell(results["exact_match_rate"]) + " |")
    lines.append("| Micro precision | " + _cell(micro["precision"]) + " |")
    lines.append("| Micro recall | " + _cell(micro["recall"]) + " |")
    lines.append("| Micro F1 | " + _cell(micro["f1"]) + " |")
    lines.append("| Macro F1 (measured detectors only) | " + _cell(results["macro_f1"]) + " |")
    lines.append("| Verbatim grounding | " + str(results["verbatim"]["exact"]) + " / "
                 + str(results["verbatim"]["checked"]) + " = "
                 + _cell(results["verbatim"]["rate"]) + " |")
    lines.append("")
    lines.append("Verbatim grounding is 1.0 by construction: a rule engine can only report a")
    lines.append("span it matched in the text. It is reported because it is the baseline for")
    lines.append("comparing against an LLM, which can and does return quotes that are not in")
    lines.append("the source.")
    lines.append("")

    if micro["f1"] is not None and micro["f1"] >= 0.999:
        lines.append("**A perfect score here is the expected result, not a good one.** The")
        lines.append("examples were written from the same rules the detectors implement, so")
        lines.append("agreement is close to circular. What this run is actually good for is")
        lines.append("catching a regression: if a future change breaks a detector, or a new")
        lines.append("lexicon entry starts firing on the neutral examples, this drops below 1.0")
        lines.append("and says exactly where. Treat it as a tripwire, not as evidence.")
        lines.append("")

    lines.append("## Per detector")
    lines.append("")
    lines.append("| Detector | TP | FP | FN | Precision | Recall | F1 |")
    lines.append("|---|---|---|---|---|---|---|")
    for category in sorted(results["per_category"]):
        v = results["per_category"][category]
        if not v["measured"]:
            continue
        lines.append("| `" + category + "` | " + str(v["true_positive"]) + " | "
                     + str(v["false_positive"]) + " | " + str(v["false_negative"]) + " | "
                     + _cell(v["precision"]) + " | " + _cell(v["recall"]) + " | "
                     + _cell(v["f1"]) + " |")
    lines.append("")

    if results["unmeasured"]:
        lines.append("**Not measured** (no example in the gold set): "
                     + ", ".join("`" + c + "`" for c in results["unmeasured"]))
        lines.append("")

    problems = [e for e in results["per_example"] if e["missed"] or e["spurious"]]
    lines.append("## Disagreements (" + str(len(problems)) + ")")
    lines.append("")
    if not problems:
        lines.append("None. Every example produced exactly the expected set of categories.")
    else:
        lines.append("| Example | Missed | Spurious | Note |")
        lines.append("|---|---|---|---|")
        for e in problems:
            lines.append("| `" + e["id"] + "` | " + (", ".join(e["missed"]) or "-") + " | "
                         + (", ".join(e["spurious"]) or "-") + " | " + e["note"] + " |")
    lines.append("")
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Evaluate the detectors against a labelled set.")
    parser.add_argument("--gold", default=str(DEFAULT_GOLD))
    parser.add_argument("--report", help="write a markdown report here")
    parser.add_argument("--json", help="write the raw results here")
    parser.add_argument("--conf", help="config directory")
    parser.add_argument("--fail-under", type=float,
                        help="exit non-zero if micro F1 falls below this (for CI)")
    args = parser.parse_args(argv)

    examples = load_gold(args.gold)
    runner = PipelineRunner(args.conf) if args.conf else PipelineRunner()
    results = evaluate(examples, runner)

    report = to_markdown(results, args.gold)
    print(report)

    if args.report:
        Path(args.report).parent.mkdir(parents=True, exist_ok=True)
        Path(args.report).write_text(report + "\n", encoding="utf-8")
    if args.json:
        Path(args.json).parent.mkdir(parents=True, exist_ok=True)
        Path(args.json).write_text(
            json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if args.fail_under is not None:
        micro_f1 = results["micro"]["f1"] or 0.0
        if micro_f1 < args.fail_under:
            print("\nFAIL: micro F1 %.3f is below %.3f" % (micro_f1, args.fail_under))
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
