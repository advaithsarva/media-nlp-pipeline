"""The evaluation harness, and the gold set it reads.

Two things are checked here: that the metric arithmetic is right (a scorer with a bug is
worse than no scorer, because it produces confident wrong numbers), and that the bundled
gold set still passes -- which is what makes it a regression tripwire rather than a
document nobody runs.
"""

import json

import pytest

from conftest import ROOT
from evaluation.evaluator import load_gold, evaluate, to_markdown, _counts_to_scores

GOLD = ROOT / "eval" / "gold" / "annotations.jsonl"


# ---- the arithmetic ----

def test_precision_and_recall_are_computed_correctly():
    # 8 correct, 2 spurious, 5 missed
    precision, recall, f1 = _counts_to_scores(8, 2, 5)

    assert precision == 8 / 10
    assert recall == 8 / 13
    assert abs(f1 - 2 * precision * recall / (precision + recall)) < 1e-12


def test_a_detector_that_never_fires_and_was_never_wanted_has_no_score():
    """None, not zero. Scoring it 0 would drag the macro average down for no reason."""
    assert _counts_to_scores(0, 0, 0) == (None, None, None)


def test_firing_only_wrongly_scores_zero():
    precision, recall, f1 = _counts_to_scores(0, 4, 0)

    assert precision == 0.0
    assert f1 == 0.0


def test_missing_everything_scores_zero():
    precision, recall, f1 = _counts_to_scores(0, 0, 4)

    assert recall == 0.0
    assert f1 == 0.0


# ---- the gold set ----

def test_the_gold_set_loads():
    examples = load_gold(GOLD)

    assert len(examples) >= 30
    for example in examples:
        assert example["text"].strip()
        assert isinstance(example["categories"], list)


def test_the_gold_set_names_only_real_categories(taxonomy):
    """A typo in a label would silently become a permanent false negative."""
    known = set(taxonomy.ids())

    for example in load_gold(GOLD):
        unknown = set(example["categories"]) - known
        assert unknown == set(), example["id"] + " names unknown categories: " + str(unknown)


def test_the_gold_set_has_enough_negatives():
    """Negative examples carry most of the value: a detector that fires on everything
    scores perfect recall."""
    examples = load_gold(GOLD)
    negatives = [e for e in examples if not e["categories"]]

    assert len(negatives) >= len(examples) * 0.25


def test_every_category_appears_in_the_gold_set(taxonomy):
    covered = set()
    for example in load_gold(GOLD):
        covered.update(example["categories"])

    missing = sorted(set(taxonomy.ids()) - covered)
    assert missing == [], "no gold example for: " + str(missing)


def test_comment_lines_are_skipped(tmp_path):
    path = tmp_path / "g.jsonl"
    path.write_text(
        "// a comment\n\n" + json.dumps({"id": "a", "text": "hello", "categories": []}) + "\n",
        encoding="utf-8")

    assert len(load_gold(path)) == 1


def test_a_malformed_line_is_reported_with_its_number(tmp_path):
    path = tmp_path / "bad.jsonl"
    path.write_text('{"id": "a", "text": "ok", "categories": []}\n{not json}\n', encoding="utf-8")

    with pytest.raises(ValueError, match="line 2"):
        load_gold(path)


# ---- the run ----

@pytest.fixture(scope="module")
def results():
    from main import PipelineRunner
    return evaluate(load_gold(GOLD), PipelineRunner())


def test_the_gold_set_still_passes(results):
    """The tripwire. If a change breaks a detector, or a new lexicon entry starts firing
    on the neutral examples, this fails and the report says exactly where."""
    disagreements = [e for e in results["per_example"] if e["missed"] or e["spurious"]]

    assert disagreements == [], json.dumps(disagreements, indent=2)


def test_verbatim_grounding_is_perfect(results):
    """1.0 by construction for a rule engine. If it is ever below 1.0, offsets are broken."""
    assert results["verbatim"]["checked"] > 0
    assert results["verbatim"]["rate"] == 1.0


def test_no_detector_is_left_unmeasured(results):
    assert results["unmeasured"] == []


def test_the_report_renders(results):
    report = to_markdown(results, GOLD)

    assert "# Detector evaluation" in report
    # the warning has to survive; a report quoted without it would mislead
    assert "not accuracy figures" in report
    assert "Verbatim grounding" in report


def test_the_report_warns_when_the_score_is_perfect(results):
    report = to_markdown(results, GOLD)

    if results["micro"]["f1"] == 1.0:
        assert "expected result, not a good one" in report
