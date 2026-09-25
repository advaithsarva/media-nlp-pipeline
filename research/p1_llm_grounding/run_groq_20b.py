"""Size-diversity arm: openai/gpt-oss-20b, same family as the already-tested
openai/gpt-oss-120b (Groq free tier), different size -- controls for architecture/training,
varies only scale. Same corpus, same prompt, same sample sizes as the 120b arm."""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from groq_client import call_groq   # noqa: E402
from prompt import build_prompt     # noqa: E402

HERE = Path(__file__).resolve().parent
MODEL = "openai/gpt-oss-20b"


def load_corpus():
    return [json.loads(l) for l in open(HERE / "corpus.jsonl", encoding="utf-8")]


def run(corpus, out_path, repeats=1, tag=""):
    results = []
    with open(out_path, "w", encoding="utf-8") as f:
        for i, passage in enumerate(corpus):
            for rep in range(repeats):
                prompt = build_prompt(passage["text"])
                try:
                    resp = call_groq(prompt, temperature=0.0, model=MODEL)
                    error = None
                    text = resp["text"]
                except Exception as e:
                    error = str(e)
                    text = ""
                rec = {"passage_id": passage["passage_id"], "rep": rep,
                       "model": MODEL, "raw_text": text, "error": error}
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                f.flush()
                results.append(rec)
                if error:
                    print(f"  ERROR passage {i} rep {rep}: {error}", flush=True)
                time.sleep(0.3)
            if (i + 1) % 10 == 0:
                print(f"{tag} {i + 1}/{len(corpus)}", flush=True)
    print(f"{tag} done: {len(results)} calls, wrote {out_path}")
    return results


def main():
    corpus = load_corpus()
    print(f"=== {MODEL}: main pass (50 passages, 1x) ===")
    run(corpus, HERE / "raw_groq20b_main.jsonl", repeats=1, tag="groq20b-main")
    print(f"\n=== {MODEL}: instability sub-sample (10 passages, 3x) ===")
    run(corpus[:10], HERE / "raw_groq20b_instability.jsonl", repeats=3, tag="groq20b-instab")


if __name__ == "__main__":
    main()
