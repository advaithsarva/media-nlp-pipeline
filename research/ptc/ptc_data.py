"""Loads PTC train articles + technique-classification gold spans. Only the train split
has public gold labels (dev/test labels are held back by the task organizers), so "test"
below means a held-out slice of train, disclosed as such -- not the competition's own
blind test set."""
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
ART_DIR = HERE / "datasets" / "train-articles"
LABEL_DIR = HERE / "datasets" / "train-labels-task2-technique-classification"

# Direct, unambiguous mappings only -- categories with no clean 1:1 PTC correspondence
# (glittering_generalities, gaslighting, guilt_by_association, scapegoating in this
# project's taxonomy) are excluded rather than force-mapped to an approximate PTC label.
CATEGORY_MAP = {
    "Loaded_Language": "loaded_language",
    "Name_Calling,Labeling": "name_calling",
    "Appeal_to_fear-prejudice": "appeal_to_fear",
    "Whataboutism,Straw_Men,Red_Herring": "whataboutism",
    "Thought-terminating_Cliches": "thought_terminating_cliche",
    "Repetition": "repetition",
}


def load_articles(n=50, seed=20260925, split="test"):
    """split='test' returns a deterministic held-out slice of the train set (last n by
    sorted id); split='fit' would return the rest, not currently used."""
    ids = sorted(p.stem.replace("article", "") for p in ART_DIR.glob("article*.txt"))
    rng = random.Random(seed)
    rng.shuffle(ids)
    chosen = ids[:n] if split == "test" else ids[n:]
    out = []
    for aid in chosen:
        text = (ART_DIR / f"article{aid}.txt").read_text(encoding="utf-8")
        label_file = LABEL_DIR / f"article{aid}.task2-TC.labels"
        gold = []
        if label_file.exists():
            for line in label_file.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                _, technique, start, end = line.split("\t")
                mapped = CATEGORY_MAP.get(technique)
                gold.append({
                    "technique_raw": technique,
                    "category": mapped,
                    "start": int(start),
                    "end": int(end),
                })
        out.append({"article_id": aid, "text": text, "gold": gold})
    return out
