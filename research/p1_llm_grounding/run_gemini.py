"""Runs a Gemini model over the P1 corpus once (temp=0) and, optionally, N instability
repeats over a smaller sub-sample. Tracks a running cost total and hard-stops at
BUDGET_USD, per the session's cost guardrail -- real money, not simulated.
"""

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gemini_client import call_gemini    # noqa: E402
from prompt import build_prompt          # noqa: E402

HERE = Path(__file__).resolve().parent
BUDGET_USD = 5.0


def load_corpus():
    return [json.loads(l) for l in open(HERE / "corpus.jsonl", encoding="utf-8")]


def run_model(model, corpus, out_path, cost_state, repeats=1, tag=""):
    results = []
    for i, passage in enumerate(corpus):
        for rep in range(repeats):
            if cost_state["total"] >= BUDGET_USD:
                print(f"BUDGET STOP at ${cost_state['total']:.4f} -- "
                      f"{i}/{len(corpus)} passages done, rep {rep}")
                with open(out_path, "w", encoding="utf-8") as f:
                    for r in results:
                        f.write(json.dumps(r, ensure_ascii=False) + "\n")
                return results
            prompt = build_prompt(passage["text"])
            try:
                resp = call_gemini(model, prompt, temperature=0.0)
                error = None
            except Exception as e:
                resp = {"text": "", "input_tokens": 0, "output_tokens": 0, "cost_usd": 0.0}
                error = str(e)
            cost_state["total"] += resp["cost_usd"]
            results.append({
                "passage_id": passage["passage_id"], "rep": rep, "model": model,
                "raw_text": resp["text"], "input_tokens": resp["input_tokens"],
                "output_tokens": resp["output_tokens"], "cost_usd": resp["cost_usd"],
                "error": error,
            })
            if error:
                print(f"  ERROR passage {i} rep {rep}: {error}", flush=True)
        if (i + 1) % 10 == 0:
            print(f"{tag} {i + 1}/{len(corpus)} running_cost=${cost_state['total']:.4f}",
                  flush=True)
        time.sleep(1.5)   # the preview-tier quota is tight on requests/minute

    with open(out_path, "w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"{tag} done: {len(results)} calls, cost=${cost_state['total']:.4f}, wrote {out_path}")
    return results


def main():
    corpus = load_corpus()
    cost_state = {"total": 0.0}

    # gemini-3.1-pro-preview: confirmed 2026-09-24 that this API key's project has a
    # *free-tier limit of 0* for this specific model (the 429 body names
    # "GenerateContentInputTokensPerModelPerDay-FreeTier" ... "limit: 0" -- not a rate
    # limit that backs off, a hard block until billing is enabled on the project).
    # Retrying wastes wall-clock time for no result, so this tier is skipped rather than
    # looped on; see observe.md for what a real run would need (billing enabled).
    print("=== gemini-3.1-pro-preview: SKIPPED, free tier quota is 0 for this model ===")

    print("\n=== gemini-3.5-flash-lite: main pass (all passages, 1x) ===")
    run_model("gemini-3.5-flash-lite", corpus, HERE / "raw_flashlite_main.jsonl",
              cost_state, repeats=1, tag="flashlite-main")

    print("\n=== gemini-3.5-flash-lite: instability sub-sample (20 passages, 3x) ===")
    subsample20 = corpus[:20]
    run_model("gemini-3.5-flash-lite", subsample20, HERE / "raw_flashlite_instability.jsonl",
              cost_state, repeats=3, tag="flashlite-instab")

    print(f"\nTOTAL ESTIMATED COST: ${cost_state['total']:.4f}")
    with open(HERE / "cost_log.json", "w") as f:
        json.dump({"total_usd": cost_state["total"]}, f, indent=2)


if __name__ == "__main__":
    main()
