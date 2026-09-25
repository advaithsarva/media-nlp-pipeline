"""Formalizes the reasoning_effort observation already made informally in groq_client.py's
own docstring (low cut tokens but silently returned empty on known-biased passages; medium,
used for the paper's real numbers, got 46% completion) into an actual side-by-side ablation:
low/medium/high on the same shared passage sub-sample, gpt-oss-120b only (this parameter is
not exposed the same way on the 20b arm's default config -- kept to the model already
established in the paper for a clean, single-variable ablation)."""
import json
import time
from pathlib import Path

from groq_client import call_groq
from prompt import build_prompt
from compute_metrics import load_corpus, extract_json_array

HERE = Path(__file__).resolve().parent
N_PASSAGES = 15
LEVELS = ["low", "medium", "high"]


def run_level(effort, passages):
    records = []
    for i, p in enumerate(passages):
        prompt = build_prompt(p["text"])
        try:
            resp = call_groq(prompt, temperature=0.0, max_tokens=5000, reasoning_effort=effort)
            error = None
        except Exception as e:
            resp = {"text": "", "prompt_tokens": 0, "completion_tokens": 0}
            error = str(e)
        records.append({
            "passage_id": p["passage_id"], "effort": effort, "raw_text": resp["text"],
            "prompt_tokens": resp["prompt_tokens"], "completion_tokens": resp["completion_tokens"],
            "error": error,
        })
        if error:
            print(f"  ERROR {effort} passage {i}: {error}", flush=True)
        time.sleep(0.3)
    return records


def score_level(records, corpus):
    n = len(records)
    n_completed = 0
    n_offset_checkable = 0
    n_offset_correct = 0
    total_tokens = 0
    for rec in records:
        total_tokens += rec["prompt_tokens"] + rec["completion_tokens"]
        spans = extract_json_array(rec["raw_text"]) if rec["raw_text"] else None
        if not spans and rec["raw_text"].strip() != "[]":
            continue  # empty/unparseable -- not completed
        n_completed += 1
        passage = corpus.get(rec["passage_id"])
        if passage is None or not spans:
            continue
        passage_text = passage["text"]
        for span in spans:
            start, end = span.get("start_char"), span.get("end_char")
            quote = span.get("quote", "")
            if isinstance(start, int) and isinstance(end, int) and 0 <= start < end <= len(passage_text):
                n_offset_checkable += 1
                if passage_text[start:end] == quote:
                    n_offset_correct += 1
    return {
        "n": n,
        "completion_rate": n_completed / n if n else None,
        "offset_accuracy": n_offset_correct / n_offset_checkable if n_offset_checkable else None,
        "mean_tokens_per_call": total_tokens / n if n else None,
    }


def main():
    corpus_list = [json.loads(l) for l in open(HERE / "corpus.jsonl", encoding="utf-8")]
    passages = corpus_list[:N_PASSAGES]
    corpus = load_corpus()

    results = {}
    raw_all = []
    for effort in LEVELS:
        print(f"=== reasoning_effort={effort} ({N_PASSAGES} passages) ===")
        records = run_level(effort, passages)
        raw_all.extend(records)
        results[effort] = score_level(records, corpus)
        print(json.dumps(results[effort], indent=2))

    with open(HERE / "raw_reasoning_ablation.jsonl", "w", encoding="utf-8") as f:
        for r in raw_all:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(HERE / "reasoning_ablation.json", "w") as f:
        json.dump(results, f, indent=2)
    print("wrote reasoning_ablation.json")


if __name__ == "__main__":
    main()
