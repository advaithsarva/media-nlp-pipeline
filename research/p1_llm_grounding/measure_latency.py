"""Bounded latency add-on for the DL coursework rubric's inference-latency requirement.
None of the raw JSONL files logged per-call wall-clock time, so this runs a small fresh
timed sample per tier rather than re-running the full corpus again.

Groq caveat, left in the code rather than silently worked around: at the time this was run,
the free tier's TPM budget was still recovering from the full P1 run (research/p1_llm_grounding/
run_groq.py's 50 + 30 calls), so most calls in this script hit 429 and only succeeded via
groq_client.py's own retry/backoff -- the one number this produced (~7.65s, n=1) includes that
backoff wait, not pure generation time, and is too small a sample to trust on its own. Re-run
this after the TPM window has fully reset (a few minutes idle) for a cleaner number.
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prompt import build_prompt      # noqa: E402
from run_gemini import load_corpus   # noqa: E402

corpus = load_corpus()[:8]

print("=== gemini-3.5-flash-lite ===")
from gemini_client import call_gemini   # noqa: E402
times = []
for p in corpus:
    t0 = time.perf_counter()
    call_gemini("gemini-3.5-flash-lite", build_prompt(p["text"]), temperature=0.0)
    times.append(time.perf_counter() - t0)
print(f"n={len(times)} mean={sum(times)/len(times):.2f}s max={max(times):.2f}s")

print("\n=== openai/gpt-oss-120b (Groq) -- expect possible 429s, see module docstring ===")
from groq_client import call_groq   # noqa: E402
times = []
for p in corpus:
    t0 = time.perf_counter()
    try:
        call_groq(build_prompt(p["text"]), temperature=0.0)
        dt = time.perf_counter() - t0
        times.append(dt)
        print(f"  {dt:.2f}s")
    except Exception as e:
        print(f"  failed: {e}")
if times:
    print(f"n={len(times)} mean={sum(times)/len(times):.2f}s max={max(times):.2f}s "
          f"(includes retry/backoff wait where a call was rate-limited)")

print("\n=== Qwen2.5-0.5B-Instruct (local CPU) ===")
import torch   # noqa: E402
from transformers import AutoModelForCausalLM, AutoTokenizer   # noqa: E402

tok = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-0.5B-Instruct")
qmodel = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-0.5B-Instruct", dtype=torch.float32)
qmodel.eval()
times = []
for p in corpus[:5]:   # smaller sample, CPU generation is slow (~20-50s/passage)
    prompt = build_prompt(p["text"])
    messages = [{"role": "user", "content": prompt}]
    inputs = tok.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt",
                                      return_dict=True)
    t0 = time.perf_counter()
    with torch.no_grad():
        qmodel.generate(**inputs, max_new_tokens=200, do_sample=False,
                         pad_token_id=tok.eos_token_id)
    times.append(time.perf_counter() - t0)
print(f"n={len(times)} mean={sum(times)/len(times):.2f}s max={max(times):.2f}s")
