#!/usr/bin/env python3
"""Minimal stdin -> OpenAI-compatible chat completion -> stdout adapter for byo_run.py.

Works with local servers (llama.cpp llama-server, ollama /v1, vLLM) and hosted
OpenAI-compatible APIs. The optional API key is read from the environment
variable named by --key-env and is only sent to --base-url.

  python tools/byo_run.py --handle me-local-1 --label "model via llama.cpp" -- \
      python tools/oai_chat.py --base-url http://127.0.0.1:8080/v1 --model my-model
  OPENROUTER_API_KEY=... python tools/byo_run.py --handle me-or-1 --label "<model>:free via OpenRouter" -- \
      python tools/oai_chat.py --base-url https://openrouter.ai/api/v1 --model <model>:free --key-env OPENROUTER_API_KEY
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request

RETRY_CODES = {429, 500, 502, 503, 504}


def post(req, timeout, retries, sleep=time.sleep):
    """POST with backoff on rate limits and transient server errors (free tiers return 429 often)."""
    for i in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code not in RETRY_CODES or i == retries:
                raise
            wait = e.headers.get("Retry-After") if e.headers else None
            delay = min(int(wait), 120) if wait and wait.isdigit() else 15 * 2 ** i
            print("HTTP %d, retry %d/%d in %ds" % (e.code, i + 1, retries, delay), file=sys.stderr)
            sleep(delay)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--base-url", required=True)
    p.add_argument("--model", required=True)
    p.add_argument("--key-env", help="environment variable holding the API key (optional)")
    p.add_argument("--max-tokens", type=int, default=16384)
    p.add_argument("--temperature", type=float, default=0.6)
    p.add_argument("--timeout", type=int, default=900)
    p.add_argument("--retries", type=int, default=4, help="retries on HTTP 429/5xx with backoff")
    a = p.parse_args(argv)
    headers = {"Content-Type": "application/json"}
    if a.key_env:
        key = os.environ.get(a.key_env)
        if not key:
            p.error("environment variable %s is not set" % a.key_env)
        headers["Authorization"] = "Bearer " + key
    body = {"model": a.model, "messages": [{"role": "user", "content": sys.stdin.read()}],
            "max_tokens": a.max_tokens, "temperature": a.temperature}
    req = urllib.request.Request(a.base_url.rstrip("/") + "/chat/completions",
                                 data=json.dumps(body).encode(), headers=headers)
    reply = post(req, a.timeout, a.retries)
    sys.stdout.write(reply["choices"][0]["message"]["content"] or "")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
