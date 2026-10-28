"""Citation audit of FastUMI (arXiv 2409.19499) with K2 Horizon.

Sample: every reference whose entry in FastUMI's reference list contains an arXiv ID (21 of 51).
For each one, K2 gets the FastUMI sentence(s) citing it plus the full text of the cited paper
(pdftotext of the arXiv PDF) and returns a status, a quote from the cited paper and a reason.
The script then checks that each quote really occurs in the cited paper's text.
"""
import json
import re
import sys
from pathlib import Path

from k2 import MODEL, chat

HERE = Path(__file__).resolve().parent
DATA, RUNS = HERE / "data", HERE / "runs" / "citations"
RUNS.mkdir(parents=True, exist_ok=True)
MAX_SOURCE_CHARS = 150_000  # only the longest source (a 205K-char review) is truncated


def cited_numbers(bracket):
    """'[3, 8–10]' -> {3, 8, 9, 10}"""
    out = set()
    for part in re.split(r",", bracket.strip("[]")):
        part = part.strip()
        m = re.fullmatch(r"(\d+)\s*[–-]\s*(\d+)", part)
        if m:
            out.update(range(int(m.group(1)), int(m.group(2)) + 1))
        elif part.isdigit():
            out.add(int(part))
    return out


def citing_sentences(body, n):
    sents = re.split(r"(?<=[.!?])\s+(?=[A-Z])", re.sub(r"\s+", " ", body))
    return [s for s in sents
            if any(n in cited_numbers(b) for b in re.findall(r"\[[\d,\s–-]+\]", s))]


def norm(s):
    s = re.sub(r"-\s*\n\s*", "", s)  # undo pdftotext line-break hyphenation
    return re.sub(r"[^a-z0-9]", "", s.lower())


def parse_last_json(content):
    """K2 sometimes writes its reasoning into `content` before the JSON (even in JSON mode);
    take the last top-level object that starts with the "claim" key."""
    dec = json.JSONDecoder()
    for m in reversed(list(re.finditer(r'\{\s*"claim"', content))):
        try:
            return dec.raw_decode(content[m.start():])[0]
        except json.JSONDecodeError:
            continue
    raise ValueError("no complete JSON object in content")


def audit(n, aid, entry, contexts, source, effort="medium"):
    prompt = f"""You are auditing a citation in the robotics paper FastUMI (arXiv 2409.19499).

FastUMI cites reference [{n}] in these sentences:
{json.dumps(contexts, indent=1, ensure_ascii=False)}

Reference entry [{n}]: {entry}

Below is the full text of the cited paper (arXiv:{aid}, extracted from PDF; may contain layout noise).
Decide whether the cited paper supports what FastUMI uses it for.

Return ONLY a JSON object:
{{"claim": str,              // what FastUMI relies on reference [{n}] for, in one sentence
  "status": "supported" | "incorrect" | "unverifiable",
  "quote": str,              // verbatim passage from the CITED paper (max 60 words) that supports or contradicts the claim; "" if unverifiable
  "reason": str}}            // why; required for incorrect or unverifiable

Rules: "supported" = the cited paper clearly backs the claim. "incorrect" = the cited paper contradicts it
or is about something else. "unverifiable" = the cited text does not settle it (e.g. a vague or
very general claim). Copy the quote exactly from the cited text below, character for character.

CITED PAPER TEXT:
{source[:MAX_SOURCE_CHARS]}"""
    content, reasoning, usage, latency = chat(
        [{"role": "user", "content": prompt}], max_tokens=16000,
        response_format={"type": "json_object"}, chat_template_kwargs={"reasoning_effort": effort})
    rec = {"ref": n, "arxiv_id": aid, "entry": entry, "contexts": contexts, "model": MODEL,
           "latency_s": latency, "usage": usage, "source_chars": len(source),
           "source_truncated": len(source) > MAX_SOURCE_CHARS, "reasoning_effort": effort,
           "reasoning": reasoning, "content": content}
    try:
        out = parse_last_json(content)
        rec["parsed"] = out
        rec["reasoning_leaked_into_content"] = not content.lstrip().startswith("{")
        q = out.get("quote") or ""
        rec["quote_found_in_source"] = len(norm(q)) >= 20 and norm(q) in norm(source)  # "..." must not pass
    except Exception as e:
        rec["parse_error"] = str(e)
        if effort != "low":  # usually a reply cut off at max_tokens: retry with less thinking
            (RUNS / f"ref_{n:02d}_failed_{effort}.json").write_text(json.dumps(rec, indent=2, ensure_ascii=False))
            print(f"[{n}] parse failed ({e}); retrying with reasoning_effort=low")
            return audit(n, aid, entry, contexts, source, effort="low")
    (RUNS / f"ref_{n:02d}.json").write_text(json.dumps(rec, indent=2, ensure_ascii=False))
    p = rec.get("parsed", {})
    print(f"[{n}] {p.get('status')} quote_ok={rec.get('quote_found_in_source')} {latency}s {usage.get('total_tokens')} tok")


if __name__ == "__main__":
    body = (DATA / "paper_body.txt").read_text()
    entries = json.loads((DATA / "ref_entries.json").read_text())
    ids = json.loads((DATA / "ref_arxiv_ids.json").read_text())
    only = {int(a) for a in sys.argv[1:]}
    for n, aid in ids.items():
        n = int(n)
        if only and n not in only:
            continue
        source = (DATA / "cited" / f"{n}.txt").read_text(errors="ignore")
        audit(n, aid, entries[str(n)], citing_sentences(body, n), source)
