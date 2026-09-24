"""Builds the P1 passage corpus: real multi-sentence articles, not isolated sentences.

SemEval-2020 Task 11 PTC would be the better-fitting corpus (full articles, propaganda-
specific) but its HF listing (SemEvalWorkshop/sem_eval_2020_task_11) ships only a loader
script, not a direct parquet download -- pulling it needs the `datasets` library (a new,
heavier dependency this project avoids by convention) and possibly hits the original
SemEval data's own access terms. Not worth the time for a workshop-tier budget, per the
brief -- BABE's own news_link groupings (already built for the F1 article-level check,
research/run_article_level.py) are reused instead: same corpus already vetted, same
grouping logic, now with the concatenated text kept (the F1 script only kept scores).

Selection: news_link groups of size 2-10 (multi-sentence, but not so long the prompt/cost
balloons), from BOTH train and test BABE splits (this is a fresh study, not reusing the
train/test discipline from F1/F2 -- there is no fitting happening on this data). Capped to
~50 passages, chosen deterministically (sorted by uuid) so the run is reproducible.
"""

import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent / "corpus.jsonl"


def group_articles():
    groups = defaultdict(list)
    for split in ("train", "test"):
        rows = [json.loads(l) for l in
                open(ROOT / "research" / "data" / f"babe_{split}_raw.jsonl", encoding="utf-8")]
        for r in rows:
            if r.get("news_link"):
                groups[r["news_link"]].append(r)
    return groups


def main(target_n=50):
    groups = group_articles()
    candidates = [(link, rows) for link, rows in groups.items() if 2 <= len(rows) <= 10]
    candidates.sort(key=lambda kv: kv[1][0]["uuid"])   # deterministic order
    selected = candidates[:target_n]

    passages = []
    for link, rows in selected:
        rows_sorted = sorted(rows, key=lambda r: r["uuid"])
        text = " ".join(r["text"] for r in rows_sorted)
        passages.append({
            "passage_id": rows_sorted[0]["uuid"],
            "news_link": link,
            "n_sentences": len(rows_sorted),
            "text": text,
            "any_biased_sentence": any(r["label"] == 1 for r in rows_sorted),
        })

    with open(OUT, "w", encoding="utf-8") as f:
        for p in passages:
            f.write(json.dumps(p, ensure_ascii=False) + "\n")

    print(f"{len(passages)} passages, mean words "
          f"{sum(len(p['text'].split()) for p in passages) / len(passages):.1f}")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
