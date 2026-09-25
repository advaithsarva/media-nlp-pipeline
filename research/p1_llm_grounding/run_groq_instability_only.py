"""Groq instability sub-sample only (main pass already complete in raw_groq_main.jsonl).

Reduced from the planned 20 passages to 10 (still x3 repeats, 30 calls) -- the free
tier's TPM budget makes each call slow enough (see groq_client.py's docstring: medium
reasoning effort, 5000-token cap, and even then a majority of main-pass passages came
back with an empty response, reasoning having exhausted the budget) that the full 20x3
was not practical to run in the time available. 10x3 is still a real, non-trivial
instability sample, disclosed as reduced.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_groq import load_corpus, run   # noqa: E402

HERE = Path(__file__).resolve().parent


def main():
    corpus = load_corpus()[:10]
    print("=== openai/gpt-oss-120b: instability sub-sample (10 passages, 3x) ===")
    run(corpus, HERE / "raw_groq_instability.jsonl", repeats=3, tag="groq-instab")


if __name__ == "__main__":
    main()
