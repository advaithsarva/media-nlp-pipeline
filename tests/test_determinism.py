"""Same input, same bytes out.

Worth being precise about what this proves: it proves the pipeline is reproducible, not
that it is correct. A system can be reproducibly wrong. Determinism is an audit property
and nothing more -- it means a result can be checked and re-derived, not that it is right.
"""

import json
import subprocess
import sys

from conftest import LOADED_TEXT, ROOT
from main import PipelineRunner
from nlp_pipeline.deterministic_utils import (
    _compute_config_hashes,
    _hash_to_document_id,
    _set_global_seeds,
)


def test_two_runs_produce_identical_json():
    first = PipelineRunner().process_document(LOADED_TEXT)
    second = PipelineRunner().process_document(LOADED_TEXT)

    assert json.dumps(first, sort_keys=True) == json.dumps(second, sort_keys=True)


def test_two_separate_processes_produce_identical_json(tmp_path):
    """A fresh interpreter each time, which is the case a single test process cannot fake."""
    sample = ROOT / "data" / "raw" / "sample_article.txt"
    outputs = []

    for name in ("first.json", "second.json"):
        target = tmp_path / name
        subprocess.run(
            [sys.executable, str(ROOT / "src" / "main.py"),
             "--input", str(sample), "--out", str(target)],
            check=True, capture_output=True,
        )
        outputs.append(target.read_bytes())

    assert outputs[0] == outputs[1]


def test_document_id_depends_only_on_the_text():
    assert _hash_to_document_id("hello") == _hash_to_document_id("hello")
    assert _hash_to_document_id("hello") != _hash_to_document_id("Hello")
    assert len(_hash_to_document_id("hello")) == 64


def test_config_hash_ignores_key_order():
    """The same settings written in a different order are the same settings."""
    first = _compute_config_hashes({"a": 1, "b": 2}, {}, {})
    second = _compute_config_hashes({"b": 2, "a": 1}, {}, {})

    assert first == second


def test_config_hash_notices_a_changed_value():
    first = _compute_config_hashes({"seed": 42}, {}, {})
    second = _compute_config_hashes({"seed": 43}, {}, {})

    assert first != second


def test_seeding_makes_random_repeatable():
    import random

    _set_global_seeds(42)
    first = [random.random() for _ in range(5)]
    _set_global_seeds(42)
    second = [random.random() for _ in range(5)]

    assert first == second


def test_a_bad_seed_is_rejected():
    import pytest

    for bad in (-1, 4294967296, "42", 1.5):
        with pytest.raises((ValueError, TypeError)):
            _set_global_seeds(bad)
