"""P1's small, CPU-runnable open-model tier: Qwen2.5-0.5B-Instruct, locally, free.
Same prompt template, same corpus, temperature 0 for the main pass and 3x repeats on the
same 20-passage sub-sample as the Flash-Lite instability check, so the three tiers are
comparable on both metrics and sample.
"""

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prompt import build_prompt   # noqa: E402

HERE = Path(__file__).resolve().parent
MODEL_ID = "Qwen/Qwen2.5-0.5B-Instruct"


def load_corpus():
    return [json.loads(l) for l in open(HERE / "corpus.jsonl", encoding="utf-8")]


def main():
    import time
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    torch.set_num_threads(max(1, os.cpu_count() or 1))
    print("threads:", torch.get_num_threads(), flush=True)

    print("loading", MODEL_ID, flush=True)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(MODEL_ID, dtype=torch.float32)
    model.eval()

    def generate(passage_text):
        prompt = build_prompt(passage_text)
        messages = [{"role": "user", "content": prompt}]
        inputs = tokenizer.apply_chat_template(
            messages, add_generation_prompt=True, return_tensors="pt",
            return_dict=True)
        with torch.no_grad():
            out = model.generate(
                **inputs, max_new_tokens=200, do_sample=False,
                pad_token_id=tokenizer.eos_token_id)
        text = tokenizer.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)
        return text

    corpus = load_corpus()

    print(f"=== {MODEL_ID}: main pass ({len(corpus)} passages, 1x) ===")
    results = []
    main_out = HERE / "raw_qwen_main.jsonl"
    with open(main_out, "w", encoding="utf-8") as f:
        for i, passage in enumerate(corpus):
            t0 = time.time()
            text = generate(passage["text"])
            rec = {"passage_id": passage["passage_id"], "rep": 0, "model": MODEL_ID,
                   "raw_text": text}
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            f.flush()
            print(f"main {i + 1}/{len(corpus)} ({time.time() - t0:.1f}s)", flush=True)
    print("wrote", main_out)

    print("=== instability sub-sample (20 passages, 3x) ===")
    subsample = corpus[:20]
    instab_out = HERE / "raw_qwen_instability.jsonl"
    with open(instab_out, "w", encoding="utf-8") as f:
        for i, passage in enumerate(subsample):
            for rep in range(3):
                text = generate(passage["text"])
                rec = {"passage_id": passage["passage_id"], "rep": rep,
                       "model": MODEL_ID, "raw_text": text}
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                f.flush()
            print(f"instab {i + 1}/{len(subsample)}", flush=True)
    print("wrote", instab_out)


if __name__ == "__main__":
    main()
