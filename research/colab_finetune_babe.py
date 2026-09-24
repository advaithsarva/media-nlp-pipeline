"""Runs on the Colab T4 VM. Fine-tunes distilbert-base-uncased on BABE train,
evaluates on BABE test (clean + two noise rates), and dumps predicted
probabilities for train and test so the local machine can fit an alpha blend
with the rule engine (hybrid_router) without needing the GPU again.

This is the actual Deep Learning coursework artifact (CO3: RNN/LSTM/Transformer-
style NLP model), not a simulated result -- it really trains and really evaluates.
"""

import json
import random
import re

import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModelForSequenceClassification, get_linear_schedule_with_warmup

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print("device:", DEVICE)

MODEL_NAME = "distilbert-base-uncased"
MAX_LEN = 64
BATCH_SIZE = 16
EPOCHS = 3
LR = 2e-5

# ---------------- noise (same shapes as research/noise.py, kept inline so this file
# is self-contained on the VM and doesn't depend on uploading a second module) ----------------

KEYBOARD_ADJACENT = {
    "a": "qwsz", "b": "vghn", "c": "xdfv", "d": "erfcxs", "e": "wsdr", "f": "rtgdvc",
    "g": "tyhfvb", "h": "yujgbn", "i": "ujko", "j": "uikhnm", "k": "iojlm", "l": "opk",
    "m": "njk", "n": "bhjm", "o": "iklp", "p": "ol", "q": "wa", "r": "edft", "s": "awedxz",
    "t": "rfgy", "u": "yhji", "v": "cfgb", "w": "qase", "x": "zsdc", "y": "tghu", "z": "asx",
}


def noise_text(text, rate, seed):
    rng = random.Random(seed)
    out = []
    for ch in text:
        lower = ch.lower()
        if lower in KEYBOARD_ADJACENT and rng.random() < rate:
            op = rng.choice(("sub", "del"))
            if op == "del":
                continue
            replacement = rng.choice(KEYBOARD_ADJACENT[lower])
            out.append(replacement.upper() if ch.isupper() else replacement)
        else:
            out.append(ch)
    return "".join(out)


# ---------------- data ----------------

def load_jsonl(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            rows.append(json.loads(line))
    return rows


train_rows = load_jsonl("babe_train_raw.jsonl")
test_rows = load_jsonl("babe_test_raw.jsonl")
print("train", len(train_rows), "test", len(test_rows))

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)


class BabeDataset(Dataset):
    def __init__(self, rows, texts=None):
        self.rows = rows
        self.texts = texts if texts is not None else [r["text"] for r in rows]

    def __len__(self):
        return len(self.rows)

    def __getitem__(self, idx):
        return self.texts[idx], int(self.rows[idx]["label"])


def collate(batch):
    texts, labels = zip(*batch)
    enc = tokenizer(list(texts), truncation=True, padding=True, max_length=MAX_LEN, return_tensors="pt")
    return enc, torch.tensor(labels, dtype=torch.float32)


model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=1).to(DEVICE)

train_loader = DataLoader(BabeDataset(train_rows), batch_size=BATCH_SIZE, shuffle=True, collate_fn=collate)
optim = torch.optim.AdamW(model.parameters(), lr=LR)
total_steps = len(train_loader) * EPOCHS
sched = get_linear_schedule_with_warmup(optim, num_warmup_steps=int(0.1 * total_steps), num_training_steps=total_steps)
loss_fn = torch.nn.BCEWithLogitsLoss()

model.train()
for epoch in range(EPOCHS):
    total_loss = 0.0
    for enc, labels in train_loader:
        enc = {k: v.to(DEVICE) for k, v in enc.items()}
        labels = labels.to(DEVICE)
        optim.zero_grad()
        out = model(**enc).logits.squeeze(-1)
        loss = loss_fn(out, labels)
        loss.backward()
        optim.step()
        sched.step()
        total_loss += loss.item()
    print(f"epoch {epoch + 1}/{EPOCHS} mean_loss={total_loss / len(train_loader):.4f}")


@torch.no_grad()
def predict_probs(texts, batch_size=32):
    model.eval()
    probs = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        enc = tokenizer(batch, truncation=True, padding=True, max_length=MAX_LEN, return_tensors="pt")
        enc = {k: v.to(DEVICE) for k, v in enc.items()}
        logits = model(**enc).logits.squeeze(-1)
        probs.extend(torch.sigmoid(logits).cpu().tolist())
    return probs


def prf1(preds, labels):
    tp = sum(1 for p, y in zip(preds, labels) if p == 1 and y == 1)
    fp = sum(1 for p, y in zip(preds, labels) if p == 1 and y == 0)
    fn = sum(1 for p, y in zip(preds, labels) if p == 0 and y == 1)
    p = tp / (tp + fp) if (tp + fp) else 0.0
    r = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * p * r / (p + r) if (p + r) else 0.0
    return {"precision": p, "recall": r, "f1": f1, "tp": tp, "fp": fp, "fn": fn}


train_texts = [r["text"] for r in train_rows]
train_labels = [int(r["label"]) for r in train_rows]
test_texts = [r["text"] for r in test_rows]
test_labels = [int(r["label"]) for r in test_rows]

train_probs = predict_probs(train_texts)
test_probs = predict_probs(test_texts)

# fit threshold on train, evaluate at that operating point on test -- same discipline as
# the rule-engine side (score_and_fit.py) so the two are comparable
best_thr, best_f1 = 0.5, -1
for thr in [i / 100 for i in range(1, 100)]:
    preds = [1 if p >= thr else 0 for p in train_probs]
    f1 = prf1(preds, train_labels)["f1"]
    if f1 > best_f1:
        best_f1, best_thr = f1, thr

clean_test_preds = [1 if p >= best_thr else 0 for p in test_probs]
results = {
    "model": MODEL_NAME,
    "epochs": EPOCHS,
    "fitted_threshold": best_thr,
    "clean_test": prf1(clean_test_preds, test_labels),
}

for rate in (0.05, 0.15):
    noised_texts = [noise_text(t, rate, seed=hash((t, rate)) & 0xFFFFFFFF) for t in test_texts]
    noised_probs = predict_probs(noised_texts)
    noised_preds = [1 if p >= best_thr else 0 for p in noised_probs]
    results[f"noise_{rate}"] = prf1(noised_preds, test_labels)
    print(f"noise {rate}: f1={results[f'noise_{rate}']['f1']:.4f}")

print(json.dumps(results, indent=2))

with open("neural_results.json", "w") as f:
    json.dump(results, f, indent=2)

with open("neural_probs.json", "w") as f:
    json.dump({
        "train_uuid": [r["uuid"] for r in train_rows], "train_probs": train_probs,
        "test_uuid": [r["uuid"] for r in test_rows], "test_probs": test_probs,
    }, f)

print("done")
