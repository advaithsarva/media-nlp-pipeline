"""Bare REST calls to Groq's OpenAI-compatible endpoint via stdlib urllib -- same pattern
as gemini_client.py, no new SDK dependency.

Two things that aren't obvious from the API docs and were confirmed by hand before this
was written:
  1. Groq sits behind Cloudflare bot protection. A bare urllib request with the default
     Python User-Agent gets HTTP 403 "error code: 1010" -- a Cloudflare block, not an auth
     failure. Fixed by sending an ordinary browser/curl-like User-Agent.
  2. gpt-oss-120b is a reasoning model: it spends completion tokens on an internal
     `message.reasoning` field before writing the actual answer into `message.content`.
     Too small a max_tokens budget starves the real answer -- content comes back empty
     while reasoning silently ate the whole budget. Measured directly against this task's
     real prompt (not a toy "say OK" prompt): at default effort ("medium"), reasoning alone
     ran 2000+ tokens and still hadn't finished at a 2000-token cap (empty content); at
     4000-5000 it typically finishes. `reasoning_effort: "low"` (a Groq-specific parameter
     this model supports) was tried first to fit the free tier's tight TPM budget (8000
     tokens per short rolling window, confirmed via the `x-ratelimit-*` response headers)
     -- it cut token usage to ~700/call, but silently degraded task quality: spot-checked
     on 4 passages independently confirmed to contain annotated bias, low effort returned
     an empty `[]` on all 4. This is not a speed/quality tradeoff worth taking for a paper
     -- a fast wrong number is worse than a slow real one -- so this defaults to medium
     effort and accepts the slower TPM-limited pace.

GROQ_API_KEY is set via `setx` (persists at the Windows user level) rather than in this
process's own environment, since that predates the setx call -- read from os.environ first,
fall back to the Windows registry (the User env var) if it's not there, so this script
works whether or not the calling shell happens to have inherited it.
"""

import json
import os
import time
import urllib.error
import urllib.request

ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "openai/gpt-oss-120b"


def _get_api_key():
    key = os.environ.get("GROQ_API_KEY")
    if key:
        return key
    import winreg
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as reg_key:
        return winreg.QueryValueEx(reg_key, "GROQ_API_KEY")[0]


API_KEY = _get_api_key()


def call_groq(prompt: str, temperature: float = 0.0, max_tokens: int = 5000, max_retries: int = 5,
              reasoning_effort: str = "medium", model: str = MODEL):
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": max_tokens,
        "reasoning_effort": reasoning_effort,
    }).encode("utf-8")
    req = urllib.request.Request(ENDPOINT, data=body, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
        "User-Agent": "curl/8.4.0",
        "Accept": "*/*",
    })
    last_error = None
    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            break
        except urllib.error.HTTPError as e:
            last_error = e
            if e.code == 429 and attempt < max_retries - 1:
                time.sleep(2 ** attempt * 5)
                continue
            raise
    else:
        raise last_error

    usage = data.get("usage", {})
    message = data["choices"][0]["message"]
    return {
        "text": message.get("content", "") or "",
        "reasoning": message.get("reasoning", ""),
        "prompt_tokens": usage.get("prompt_tokens", 0),
        "completion_tokens": usage.get("completion_tokens", 0),
        "raw": data,
    }


if __name__ == "__main__":
    r = call_groq("Say the word OK and nothing else.")
    print("content:", repr(r["text"]))
    print("reasoning (truncated):", r["reasoning"][:200])
