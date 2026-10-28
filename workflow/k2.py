"""Minimal K2 Horizon client (OpenAI-compatible chat completions), stdlib only."""
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path


def load_env(path=Path(__file__).resolve().parent.parent / ".env"):
    if path.exists():
        for line in path.read_text().splitlines():
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


load_env()
BASE_URL = os.environ.get("IFM_BASE_URL", "https://api.ifm.ai/v1")
MODEL = os.environ.get("IFM_MODEL", "IFM/K2-Horizon-375B-A23B")


def chat(messages, max_tokens=8000, temperature=0.2, retries=4, **extra):
    """Return (content, reasoning, usage, latency_s)."""
    body = {"model": MODEL, "messages": messages, "max_tokens": max_tokens,
            "temperature": temperature, **extra}
    req = urllib.request.Request(
        f"{BASE_URL}/chat/completions",
        data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {os.environ['K2_API_KEY']}",
                 "Content-Type": "application/json"},
    )
    for attempt in range(retries):
        t0 = time.time()
        try:
            with urllib.request.urlopen(req, timeout=600) as r:
                data = json.load(r)
            msg = data["choices"][0]["message"]
            return (msg.get("content") or "", msg.get("reasoning") or msg.get("reasoning_content") or "",
                    data.get("usage", {}), round(time.time() - t0, 2))
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503) and attempt < retries - 1:
                time.sleep(int(e.headers.get("Retry-After", 5 * (attempt + 1))))
                continue
            raise RuntimeError(f"HTTP {e.code}: {e.read()[:500]!r}") from e
