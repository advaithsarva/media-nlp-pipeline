"""Loads BABE (mediabiasgroup/BABE on Hugging Face) into a plain Python structure.

BABE gives one binary label per sentence (biased / not biased) plus the verbatim
words an annotator marked as biased -- it has no per-category label matching this
project's 21-category taxonomy, so it cannot be dropped straight into
`eval/gold/annotations.jsonl` (that format expects a `categories` list). It is kept
here instead, quarantined from the product per CLAUDE.md's "Research track" section.

The official HF split (train 3121 / test 1000) is used as-is rather than re-splitting,
so the test numbers are comparable to anyone else who cites BABE's own split.
"""

import ast
import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"


def _parse_biased_words(raw):
    """The field is a Python list literal (single-quoted), not JSON -- e.g. "['a', 'b']"."""
    if not raw or raw == "[]":
        return []
    try:
        return list(ast.literal_eval(raw))
    except (ValueError, SyntaxError):
        return []


def load_split(name):
    """name is 'train' or 'test'. Returns a list of dicts: text, label, biased_words, uuid."""
    path = DATA_DIR / f"babe_{name}_raw.jsonl"
    records = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            records.append({
                "uuid": row["uuid"],
                "text": row["text"],
                "label": int(row["label"]),
                "biased_words": _parse_biased_words(row.get("biased_words")),
                "outlet": row.get("outlet"),
                "topic": row.get("topic"),
            })
    return records


if __name__ == "__main__":
    train = load_split("train")
    test = load_split("test")
    print("train", len(train), "positives", sum(r["label"] for r in train))
    print("test", len(test), "positives", sum(r["label"] for r in test))
    print(train[0])
