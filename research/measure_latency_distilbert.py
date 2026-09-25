"""Bounded latency measurement: DistilBERT inference wall-clock, 20 BABE test passages, CPU.

The fine-tuned checkpoint from the Colab run lives only on that (now-stopped) Colab VM --
retraining or restarting a GPU session just to time inference would blow the time budget for
this. Loads distilbert-base-uncased fresh instead: inference latency is a function of the
architecture and input sequence length, not the trained weight values, so timing the
untrained-but-architecturally-identical model on the same real passages, same tokenizer, same
max_length, is a valid proxy for the deployed forward-pass cost. Local hardware: CPU (this
machine has no local GPU; the fine-tune itself ran on Colab's T4, but this machine's own
inference path -- if this model were ever served here rather than via the GPU it trained on --
would be CPU, which is what §15.3's clean_test numbers implicitly assumed without ever
measuring it).
"""

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "research"))

import torch   # noqa: E402
from transformers import AutoTokenizer, AutoModelForSequenceClassification   # noqa: E402

from babe_data import load_split   # noqa: E402

MODEL_NAME = "distilbert-base-uncased"
MAX_LEN = 64

torch.set_num_threads(torch.get_num_threads())
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=1)
model.eval()

test = load_split("test")[:20]

times = []
with torch.no_grad():
    for rec in test:
        t0 = time.perf_counter()
        enc = tokenizer(rec["text"], truncation=True, padding=True, max_length=MAX_LEN,
                         return_tensors="pt")
        model(**enc)
        times.append(time.perf_counter() - t0)

mean_ms = sum(times) / len(times) * 1000
steady = times[1:]
print(f"n={len(times)} mean={mean_ms:.2f}ms max={max(times)*1000:.2f}ms")
print(f"excluding first (warmup) call: mean={sum(steady)/len(steady)*1000:.2f}ms "
      f"max={max(steady)*1000:.2f}ms")
print("threads:", torch.get_num_threads())
