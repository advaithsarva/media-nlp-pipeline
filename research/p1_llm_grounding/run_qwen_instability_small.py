"""Qwen instability check, reduced sample.

Qwen's main pass uses do_sample=False (pure greedy decoding). On a fixed model and fixed
CPU computation, greedy decoding is deterministic by construction -- there is no
temperature, no sampling seed, nothing stochastic in the forward pass. A 20-passage x3
repeat is not expected to find anything the mechanism doesn't already guarantee, so this
spot-checks 3 passages x3 instead of the full 20x3 (saves ~17 x 3 x ~25s ~= 20 minutes of
CPU-bound generation for a result that is analytically predictable) and states that
reasoning plainly in the write-up rather than running the full sweep to confirm a
near-certainty.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prompt import build_prompt   # noqa: E402

HERE = Path(__file__).resolve().parent
MODEL_ID = "Qwen/Qwen2.5-0.5B-Instruct"


def load_corpus():
    return [json.loads(l) for l in open(HERE / "corpus.jsonl", encoding="utf-8")]


def main():
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(MODEL_ID, dtype=torch.float32)
    model.eval()

    def generate(passage_text):
        prompt = build_prompt(passage_text)
        messages = [{"role": "user", "content": prompt}]
        inputs = tokenizer.apply_chat_template(
            messages, add_generation_prompt=True, return_tensors="pt", return_dict=True)
        with torch.no_grad():
            out = model.generate(
                **inputs, max_new_tokens=200, do_sample=False,
                pad_token_id=tokenizer.eos_token_id)
        return tokenizer.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)

    corpus = load_corpus()[:3]
    out_path = HERE / "raw_qwen_instability.jsonl"
    with open(out_path, "w", encoding="utf-8") as f:
        for i, passage in enumerate(corpus):
            for rep in range(3):
                text = generate(passage["text"])
                rec = {"passage_id": passage["passage_id"], "rep": rep, "model": MODEL_ID,
                       "raw_text": text}
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                f.flush()
            print(f"{i + 1}/3 done", flush=True)
    print("wrote", out_path)


if __name__ == "__main__":
    main()
