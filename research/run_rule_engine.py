"""Runs the rule engine once over all of BABE and caches the raw findings.

Scoring is cheap arithmetic over spans; re-running spaCy/regex detectors for every
point in a grid search would not be. So this script does the expensive part exactly
once per split and pickles the result; everything downstream (threshold selection,
noisy-OR vs smooth-max, lambda/beta/gamma fitting) reads the cache.
"""

import pickle
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from main import PipelineRunner    # noqa: E402
from babe_data import load_split   # noqa: E402

CACHE_DIR = Path(__file__).resolve().parent / "data"


def run_split(runner, name):
    records = load_split(name)
    cached = []
    t0 = time.time()
    for i, rec in enumerate(records):
        normalized = runner.processor.normalize(
            runner.router.route_push_input({"text": rec["text"], "source_type": "api_rest"})
        )
        runner.segmenter.segment(normalized)
        if runner.entities is not None:
            runner.entities.analyze(normalized)
        result = runner.rules.classify(normalized)
        cached.append({
            "uuid": rec["uuid"],
            "label": rec["label"],
            "biased_words": rec["biased_words"],
            "word_count": normalized.word_count,
            "spans": [
                {"text": s.text, "category": s.category, "confidence": s.confidence}
                for s in result.spans
            ],
        })
        if (i + 1) % 500 == 0:
            print(f"  {name}: {i + 1}/{len(records)} ({time.time() - t0:.1f}s)")
    print(f"{name}: {len(cached)} docs in {time.time() - t0:.1f}s")
    return cached


def main():
    runner = PipelineRunner()
    for split in ("train", "test"):
        cached = run_split(runner, split)
        out = CACHE_DIR / f"babe_{split}_spans.pkl"
        with open(out, "wb") as f:
            pickle.dump(cached, f)
        print("wrote", out)


if __name__ == "__main__":
    main()
