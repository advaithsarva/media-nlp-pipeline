"""Retry only the passages that previously failed for gpt-oss-120b/20b (rate-limited,
network error, or genuine empty non-convergence), using a fresh account's quota. Merges
successful retries into the existing raw_*.jsonl files in place -- does not touch already-
successful records, does not duplicate the run."""
import json
import time
from pathlib import Path

from groq_client import call_groq
from prompt import build_prompt

HERE = Path(__file__).resolve().parent


def is_failed(rec):
    if rec.get("error"):
        return True
    rt = (rec.get("raw_text") or "").strip()
    return rt == "" or rt == "[]"


def load_corpus_by_id():
    return {json.loads(l)["passage_id"]: json.loads(l) for l in
            open(HERE / "corpus.jsonl", encoding="utf-8")}


def retry_file(path, model, corpus_by_id):
    records = [json.loads(l) for l in open(path, encoding="utf-8")]
    failed_idx = [i for i, r in enumerate(records) if is_failed(r)]
    print(f"{path.name}: {len(failed_idx)} failed of {len(records)}")

    n_retried_ok = 0
    n_still_failed = 0
    still_failed_ids = []
    for i in failed_idx:
        rec = records[i]
        passage = corpus_by_id[rec["passage_id"]]
        prompt = build_prompt(passage["text"])
        try:
            resp = call_groq(prompt, temperature=0.0, model=model)
            new_text, new_error = resp["text"], None
        except Exception as e:
            new_text, new_error = "", str(e)

        ok = new_error is None and new_text.strip() not in ("", "[]")
        if ok:
            n_retried_ok += 1
        else:
            n_still_failed += 1
            still_failed_ids.append(rec["passage_id"])
        records[i] = {**rec, "raw_text": new_text, "error": new_error,
                      "retried": True, "retry_ok": ok}
        time.sleep(0.3)

    with open(path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"  retried {len(failed_idx)}: {n_retried_ok} now succeed, "
          f"{n_still_failed} still fail")
    if still_failed_ids:
        print(f"  still-failing passage_ids: {still_failed_ids}")
    return {"n_failed_before": len(failed_idx), "n_retried_ok": n_retried_ok,
            "n_still_failed": n_still_failed, "still_failed_ids": still_failed_ids}


def main():
    corpus_by_id = load_corpus_by_id()
    summary = {}
    summary["gpt-oss-120b"] = retry_file(
        HERE / "raw_groq_main.jsonl", "openai/gpt-oss-120b", corpus_by_id)
    summary["gpt-oss-20b"] = retry_file(
        HERE / "raw_groq20b_main.jsonl", "openai/gpt-oss-20b", corpus_by_id)
    with open(HERE / "retry_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    print("\nwrote retry_summary.json")


if __name__ == "__main__":
    main()
