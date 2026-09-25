"""Condition B for the offset-grounding comparison: instead of trusting the model's
self-reported (start_char, end_char), do a deterministic substring search for its returned
quote and recover the offset that way. This is the "Propose-and-Verify" pattern CLAUDE.md's
Research track already names as a method contribution to attach -- LLM proposes a candidate
quote, deterministic code (not the LLM) locates it.

Two recovery tiers, same normalize() as compute_metrics.py for consistency:
  exact recovery      -- str.find on the raw passage text (this is definitionally the same
                          population as verbatim_rate, computed independently here for rigor
                          and to check ambiguity, not assumed equal)
  normalized recovery -- for quotes that only match after normalization, locate the match in
                          normalized space and map back to a raw-text offset via re.search
                          over a regex built from the normalized tokens

Also reports how often a recovered quote is AMBIGUOUS (appears more than once in the
passage) -- a first-match recovery strategy could silently pick the wrong occurrence, and an
honest comparison needs to say so rather than assume recovery is free of its own failure mode.
"""
import json
import re
from pathlib import Path

from compute_metrics import load_corpus, extract_json_array, normalize

HERE = Path(__file__).resolve().parent


def exact_recover(quote, passage_text):
    idx = passage_text.find(quote)
    if idx == -1:
        return None
    n_occurrences = passage_text.count(quote)
    return {"start": idx, "end": idx + len(quote), "ambiguous": n_occurrences > 1}


def normalized_recover(quote, passage_text):
    """Fallback recovery for quotes that only match after normalization. Builds a regex
    from the quote's words allowing flexible whitespace/punctuation between them, run
    against the raw passage so the recovered offset is still a real raw-text span."""
    words = re.findall(r"[A-Za-z0-9']+", quote)
    if not words:
        return None
    pattern = r"\s*[\"'.,;:]*\s*".join(re.escape(w) for w in words)
    matches = list(re.finditer(pattern, passage_text, re.IGNORECASE))
    if not matches:
        return None
    m = matches[0]
    return {"start": m.start(), "end": m.end(), "ambiguous": len(matches) > 1}


def score_recovery(raw_path, corpus):
    if not raw_path.exists():
        return None
    records = [json.loads(l) for l in open(raw_path, encoding="utf-8")]
    n_quotes = 0
    n_recovered_exact = 0
    n_recovered_normalized = 0
    n_unrecoverable = 0
    n_ambiguous = 0

    for rec in records:
        passage = corpus.get(rec["passage_id"])
        if passage is None:
            continue
        spans = extract_json_array(rec["raw_text"])
        if spans is None:
            continue
        passage_text = passage["text"]
        for span in spans:
            n_quotes += 1
            quote = span["quote"]
            hit = exact_recover(quote, passage_text)
            if hit is not None:
                n_recovered_exact += 1
                if hit["ambiguous"]:
                    n_ambiguous += 1
                continue
            hit = normalized_recover(quote, passage_text)
            if hit is not None:
                n_recovered_normalized += 1
                if hit["ambiguous"]:
                    n_ambiguous += 1
                continue
            n_unrecoverable += 1

    n_recovered = n_recovered_exact + n_recovered_normalized
    return {
        "n_quotes": n_quotes,
        "n_recovered_exact": n_recovered_exact,
        "n_recovered_normalized_fallback": n_recovered_normalized,
        "n_unrecoverable": n_unrecoverable,
        "recovery_rate": n_recovered / n_quotes if n_quotes else None,
        "n_ambiguous_multi_occurrence": n_ambiguous,
        "ambiguous_rate_of_recovered": n_ambiguous / n_recovered if n_recovered else None,
    }


def main():
    corpus = load_corpus()
    results = {}
    for name, path in [
        ("flashlite_main", HERE / "raw_flashlite_main.jsonl"),
        ("qwen_main", HERE / "raw_qwen_main.jsonl"),
        ("groq_main", HERE / "raw_groq_main.jsonl"),
    ]:
        r = score_recovery(path, corpus)
        if r:
            results[name] = r
            print(f"--- {name} ---")
            print(json.dumps(r, indent=2))
    with open(HERE / "offset_recovery.json", "w") as f:
        json.dump(results, f, indent=2)
    print("wrote", HERE / "offset_recovery.json")


if __name__ == "__main__":
    main()
