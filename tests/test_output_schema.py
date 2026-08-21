"""The output contract: the backend gets exactly this shape, and every quote in it is real."""

import json

import pytest

from conftest import LOADED_TEXT, NEUTRAL_TEXT, ROOT
from main import PipelineRunner


@pytest.fixture(scope="module")
def runner():
    return PipelineRunner()


def test_output_matches_the_schema(runner):
    record = runner.process_document(LOADED_TEXT)
    runner.postprocessor.validate(record)      # raises if the shape is wrong


def test_every_finding_quotes_the_real_text(runner):
    record = runner.process_document(LOADED_TEXT)
    text = LOADED_TEXT

    assert record["findings"], "expected findings in the loaded example"
    for finding in record["findings"]:
        assert text[finding["start_char"]:finding["end_char"]] == finding["text"]
        # and again the crude way, which is what a reviewer would actually do
        assert finding["text"] in text


def test_neutral_text_produces_a_valid_empty_report(runner):
    record = runner.process_document(NEUTRAL_TEXT)

    runner.postprocessor.validate(record)
    assert record["findings"] == []
    assert record["composite"] is None


def test_no_timestamp_anywhere_in_the_record(runner):
    """A clock reading would make two runs differ, which breaks the reproducibility claim."""
    record = runner.process_document(LOADED_TEXT)
    dumped = json.dumps(record)

    for word in ("timestamp", "ingested_at", "generated_at", "processed_at"):
        assert word not in dumped


def test_config_hashes_are_stamped_on(runner):
    record = runner.process_document(LOADED_TEXT)

    for key in ("pipeline_hash", "taxonomy_hash", "scoring_hash"):
        assert len(record["config_hashes"][key]) == 64


def test_a_bad_record_is_rejected(runner):
    record = runner.process_document(LOADED_TEXT)
    record["stats"]["word_count"] = -1

    with pytest.raises(ValueError):
        runner.postprocessor.validate(record)


def test_tampered_evidence_is_caught(runner):
    record = runner.process_document(LOADED_TEXT)
    record["findings"][0]["text"] = "something the article never said"

    with pytest.raises(ValueError):
        runner.postprocessor.check_evidence(record, LOADED_TEXT)


def test_the_sample_article_runs(runner):
    sample = ROOT / "data" / "raw" / "sample_article.txt"
    record = runner.process_document(str(sample))

    runner.postprocessor.validate(record)
    assert record["stats"]["sentence_count"] > 0
