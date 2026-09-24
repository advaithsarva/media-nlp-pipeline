"""Bare REST calls to the Gemini API via stdlib urllib -- no google-genai SDK, matching
this project's delete-the-dependency-over-satisfy-it convention (see file_readers.py's
history). One function, one job.
"""

import json
import os
import time
import urllib.error
import urllib.request

API_KEY = os.environ["GEMINI_API_KEY"]
ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"

# Published per-1M-token pricing (verified via web search 2026-09-24, standard <200K
# context tier, input/output, USD) -- used only to keep a running cost estimate against
# the session's $5 budget cap, not billed from here.
PRICE_PER_M = {
    "gemini-3.1-pro-preview": {"input": 2.00, "output": 12.00},
    "gemini-3.5-flash-lite": {"input": 0.30, "output": 2.50},
}


def call_gemini(model: str, prompt: str, temperature: float = 0.0, max_retries: int = 5):
    url = ENDPOINT.format(model=model, key=API_KEY)
    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": temperature},
    }).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})

    # Free/preview-tier Gemini quotas are tight on requests-per-minute -- a plain retry
    # loop with exponential backoff on 429 is enough here, this isn't a high-throughput
    # service that needs a real queue.
    last_error = None
    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            break
        except urllib.error.HTTPError as e:
            last_error = e
            if e.code == 429 and attempt < max_retries - 1:
                wait = 2 ** attempt * 5   # 5, 10, 20, 40s
                time.sleep(wait)
                continue
            raise
    else:
        raise last_error

    usage = data.get("usageMetadata", {})
    in_tok = usage.get("promptTokenCount", 0)
    out_tok = usage.get("candidatesTokenCount", 0)
    price = PRICE_PER_M.get(model, {"input": 0, "output": 0})
    cost = (in_tok / 1_000_000) * price["input"] + (out_tok / 1_000_000) * price["output"]

    try:
        text = data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        text = ""
    return {"text": text, "input_tokens": in_tok, "output_tokens": out_tok, "cost_usd": cost,
            "raw": data}


if __name__ == "__main__":
    r = call_gemini("gemini-3.5-flash-lite", "Say OK.")
    print(r["text"], r["cost_usd"])
