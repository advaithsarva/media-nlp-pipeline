"""The four P1 metrics from CLAUDE.md's protocol, plus the heuristic failure taxonomy.

verbatim rate       -- exact substring match (str.find), objective
normalized rate      -- match after whitespace/quote/case normalisation
offset accuracy       -- do the model's own stated offsets land on its own quoted text
instability            -- across 3 repeats of the same input, how often the span set changes

Reported separately per CLAUDE.md's own note: conflating verbatim and normalised hides
whether a quote "differs by a curly apostrophe" or "does not exist in the source" -- two
very different failure severities.
"""

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load_corpus():
    return {p["passage_id"]: p for p in
            (json.loads(l) for l in open(HERE / "corpus.jsonl", encoding="utf-8"))}


def extract_json_array(raw_text):
    """Models wrap JSON in prose or markdown fences fairly often; find the first [...]."""
    match = re.search(r"\[.*\]", raw_text, re.DOTALL)
    if not match:
        return None
    try:
        data = json.loads(match.group(0))
    except json.JSONDecodeError:
        return None
    if not isinstance(data, list):
        return None
    out = []
    for item in data:
        if isinstance(item, dict) and "quote" in item:
            out.append({
                "quote": str(item.get("quote", "")),
                "start_char": item.get("start_char"),
                "end_char": item.get("end_char"),
            })
    return out


def normalize(s):
    s = s.lower().strip()
    s = re.sub(r"[‘’']", "'", s)
    s = re.sub(r"[“”]", '"', s)
    s = re.sub(r"\s+", " ", s)
    s = s.strip(" \"'.,;:")
    return s


def classify_failure(quote, passage_text):
    """Heuristic, not human-annotated -- disclosed as such in the write-up. Order matters:
    checked from most to least specific."""
    if quote in passage_text:
        return None   # verbatim, not a failure
    norm_q = normalize(quote)
    norm_p = normalize(passage_text)
    if norm_q and norm_q in norm_p:
        return "boundary_or_punctuation_drift"
    # cross-sentence splice: words of the quote appear in the passage but not contiguously
    words = [w for w in re.findall(r"[A-Za-z']+", quote.lower()) if len(w) > 2]
    if not words:
        return "hallucinated_content"
    present = [w for w in words if w in passage_text.lower()]
    coverage = len(present) / len(words)
    if coverage >= 0.8:
        return "paraphrase_or_merged_span"
    if coverage >= 0.3:
        return "cross_sentence_splice_or_partial_match"
    return "hallucinated_content"


def score_run(raw_path, corpus):
    if not raw_path.exists():
        return None
    records = [json.loads(l) for l in open(raw_path, encoding="utf-8")]
    n_quotes = 0
    n_verbatim = 0
    n_normalized = 0
    n_offset_correct = 0
    n_offset_checkable = 0
    n_parse_failed = 0
    failure_taxonomy = defaultdict(int)

    for rec in records:
        passage = corpus.get(rec["passage_id"])
        if passage is None:
            continue
        spans = extract_json_array(rec["raw_text"])
        if spans is None:
            n_parse_failed += 1
            continue
        passage_text = passage["text"]
        for span in spans:
            n_quotes += 1
            quote = span["quote"]
            is_verbatim = quote in passage_text
            if is_verbatim:
                n_verbatim += 1
            is_normalized = normalize(quote) in normalize(passage_text)
            if is_normalized:
                n_normalized += 1
            if not is_verbatim:
                failure_taxonomy[classify_failure(quote, passage_text)] += 1

            start, end = span.get("start_char"), span.get("end_char")
            if isinstance(start, int) and isinstance(end, int) and 0 <= start < end <= len(passage_text):
                n_offset_checkable += 1
                if passage_text[start:end] == quote:
                    n_offset_correct += 1

    return {
        "n_responses": len(records),
        "n_parse_failed": n_parse_failed,
        "n_quotes": n_quotes,
        "verbatim_rate": n_verbatim / n_quotes if n_quotes else None,
        "normalized_rate": n_normalized / n_quotes if n_quotes else None,
        "offset_accuracy": n_offset_correct / n_offset_checkable if n_offset_checkable else None,
        "offset_checkable_rate": n_offset_checkable / n_quotes if n_quotes else None,
        "failure_taxonomy": dict(failure_taxonomy),
    }


def score_instability(raw_path, corpus):
    if not raw_path.exists():
        return None
    records = [json.loads(l) for l in open(raw_path, encoding="utf-8")]
    by_passage = defaultdict(dict)
    for rec in records:
        spans = extract_json_array(rec["raw_text"]) or []
        quote_set = frozenset(normalize(s["quote"]) for s in spans if s.get("quote"))
        by_passage[rec["passage_id"]][rec["rep"]] = quote_set

    n_passages = 0
    n_unstable = 0
    for passage_id, reps in by_passage.items():
        if len(reps) < 2:
            continue
        n_passages += 1
        unique_sets = set(reps.values())
        if len(unique_sets) > 1:
            n_unstable += 1

    return {
        "n_passages": n_passages,
        "n_unstable": n_unstable,
        "instability_rate": n_unstable / n_passages if n_passages else None,
    }


def main():
    corpus = load_corpus()
    results = {}

    for name, path in [
        ("flashlite_main", HERE / "raw_flashlite_main.jsonl"),
        ("qwen_main", HERE / "raw_qwen_main.jsonl"),
        ("groq_main", HERE / "raw_groq_main.jsonl"),
    ]:
        r = score_run(path, corpus)
        if r:
            results[name] = r
            print(f"--- {name} ---")
            print(json.dumps(r, indent=2))

    for name, path in [
        ("flashlite_instability", HERE / "raw_flashlite_instability.jsonl"),
        ("qwen_instability", HERE / "raw_qwen_instability.jsonl"),
        ("groq_instability", HERE / "raw_groq_instability.jsonl"),
    ]:
        r = score_instability(path, corpus)
        if r:
            results[name] = r
            print(f"--- {name} ---")
            print(json.dumps(r, indent=2))

    with open(HERE / "metrics.json", "w") as f:
        json.dump(results, f, indent=2)
    print("wrote", HERE / "metrics.json")


if __name__ == "__main__":
    main()
