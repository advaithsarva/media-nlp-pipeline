"""Bounded latency measurement: rule engine wall-clock per document, 20 BABE test passages.
Not a new eval harness -- just timing the existing pipeline path (research/run_rule_engine.py
already runs this same code over BABE; this only adds a stopwatch around it)."""

import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "research"))

from main import PipelineRunner   # noqa: E402
from babe_data import load_split  # noqa: E402

runner = PipelineRunner()
test = load_split("test")[:20]

times = []
for rec in test:
    t0 = time.perf_counter()
    normalized = runner.processor.normalize(
        runner.router.route_push_input({"text": rec["text"], "source_type": "api_rest"})
    )
    runner.segmenter.segment(normalized)
    if runner.entities is not None:
        runner.entities.analyze(normalized)
    runner.rules.classify(normalized)
    times.append(time.perf_counter() - t0)

mean_ms = sum(times) / len(times) * 1000
sorted_ms = sorted(t * 1000 for t in times)
median_ms = sorted_ms[len(sorted_ms) // 2]
print(f"n={len(times)} mean={mean_ms:.2f}ms median={median_ms:.2f}ms "
      f"min={min(times)*1000:.2f}ms max={max(times)*1000:.2f}ms")
print("per-doc (ms):", [f"{t*1000:.1f}" for t in times])

# first call includes one-time lazy-loaded model warmup (spaCy) -- report steady-state too
steady = times[1:]
print(f"excluding first (warmup) call: mean={sum(steady)/len(steady)*1000:.2f}ms "
      f"max={max(steady)*1000:.2f}ms")
