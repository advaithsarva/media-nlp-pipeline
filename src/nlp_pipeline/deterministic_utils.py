"""Seeding, hashing and version stamping -- the three things that make a run reproducible
and let you prove afterwards which settings produced which output.

No state, no classes. This module depends on nothing else in the project.
"""

import hashlib
import json
import random

import numpy as np

MAX_SEED = 4294967295   # numpy rejects anything above 2**32 - 1


def _set_global_seeds(seed: int):
    # Every library keeps its own separate random generator. Seeding `random`
    # does not seed numpy, so both have to be set or half the pipeline stays random.
    if not isinstance(seed, int) or seed < 0 or seed > MAX_SEED:
        raise ValueError(f"seed must be an integer between 0 and {MAX_SEED}, got {seed!r}")
    random.seed(seed)
    np.random.seed(seed)


def _hash_to_document_id(input_str: str) -> str:
    """Same text always gets the same id -- no database, no counter, stable across machines."""
    if not isinstance(input_str, str):
        raise TypeError(f"expected a string, got {type(input_str).__name__}")
    # hashing works on bytes; utf-8 fixes how characters become bytes so the
    # same string hashes identically everywhere
    return hashlib.sha256(input_str.encode("utf-8")).hexdigest()


def _compute_config_hashes(pipeline_cfg, taxonomy_cfg, scoring_cfg) -> dict:
    """A fingerprint of the settings behind a result. Change any value, get a different hash."""
    result = {}
    for name, config in [("pipeline", pipeline_cfg),
                         ("taxonomy", taxonomy_cfg),
                         ("scoring", scoring_cfg)]:
        # sort_keys is the load-bearing bit: dicts have no guaranteed order, so
        # {a:1,b:2} and {b:2,a:1} are the same config but would hash differently
        # without it. Sorting makes one config produce exactly one hash.
        text_form = json.dumps(config, sort_keys=True, default=str)
        result[name + "_hash"] = hashlib.sha256(text_form.encode("utf-8")).hexdigest()
    return result


def _round_floats(value, places: int = 6):
    """Round every float in a nested structure.

    Float arithmetic can differ in the last bit between machines. Rounding before
    serialising is what makes two runs byte-identical rather than nearly identical.
    """
    if isinstance(value, float):
        return round(value, places)
    if isinstance(value, dict):
        return {k: _round_floats(v, places) for k, v in value.items()}
    if isinstance(value, list):
        return [_round_floats(v, places) for v in value]
    return value
