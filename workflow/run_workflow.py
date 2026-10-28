"""Paper close-reading + related-work workflow on K2 Horizon.

Step 1  takeaways   : whole paper body -> findings / methods / limitations, each with a supporting quote
Step 2a related_free: research question only -> >=8 related papers from model memory (ungrounded)
Step 2b related_refs: research question + the paper's reference list -> >=8 papers grouped by theme (grounded)
Step 3  verify.py   : checks every returned paper against arXiv / Crossref (separate script)
"""
import json
import re
import sys
from pathlib import Path

from k2 import MODEL, chat

HERE = Path(__file__).resolve().parent
DATA, RUNS = HERE / "data", HERE / "runs"
RUNS.mkdir(exist_ok=True)

QUESTION = ("How can manipulation demonstrations collected with a handheld, UMI-style gripper be "
            "transferred to robots whose end-effectors differ from the data-collection gripper "
            "(cross-embodiment transfer of handheld-gripper data)?")


def parse_json(text):
    text = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.M).strip()
    start, end = text.find("{"), text.rfind("}")
    return json.loads(text[start:end + 1])


# v1 ran without these and failed on steps 2a/2b (see runs/*_v1_fail.json).
JSON_MODE = {"response_format": {"type": "json_object"},
             "chat_template_kwargs": {"reasoning_effort": "medium"}}


def run(step, messages, max_tokens=20000, **extra):
    content, reasoning, usage, latency = chat(messages, max_tokens=max_tokens, **extra)
    record = {"step": step, "model": MODEL, "latency_s": latency, "usage": usage, "request_extra": extra,
              "prompt": messages[-1]["content"][:2000], "reasoning": reasoning, "content": content}
    try:
        record["parsed"] = parse_json(content)
        record["parse_ok"] = True
    except Exception as e:  # keep raw output so the failure can be reported
        record["parse_ok"], record["parse_error"] = False, str(e)
    (RUNS / f"{step}.json").write_text(json.dumps(record, indent=2, ensure_ascii=False))
    print(f"[{step}] latency={latency}s usage={usage} parse_ok={record['parse_ok']}")
    return record


def takeaways():
    body = (DATA / "paper_body.txt").read_text()
    prompt = f"""Below is the full text of a robotics paper. Extract its key takeaways.

Return ONLY a JSON object:
{{"title": str,
  "findings":    [{{"point": str, "evidence_quote": str, "section": str}}],
  "methods":     [{{"point": str, "evidence_quote": str, "section": str}}],
  "limitations": [{{"point": str, "evidence_quote": str, "section": str, "stated_by_authors": bool}}]}}

Rules: 4-6 items per list. "evidence_quote" must be copied verbatim from the paper (max 40 words).
Findings must include concrete numbers where the paper reports them. For limitations, mark
stated_by_authors=false if it is your own inference rather than something the paper says.

PAPER:
{body}"""
    return run("1_takeaways", [{"role": "user", "content": prompt}])


def related_free():
    prompt = f"""Research question: {QUESTION}

List at least 8 published papers (2019-2025) that matter for this question, organised by theme.
Return ONLY a JSON object:
{{"themes": [{{"theme": str, "papers": [{{"title": str, "authors": str, "year": int,
  "arxiv_id": str or null, "doi": str or null, "why_it_matters": str}}]}}]}}
"why_it_matters" must say how the paper bears on the question, not restate its abstract.
Only list papers you are confident exist; use null for identifiers you are unsure of."""
    return run("2a_related_free", [{"role": "user", "content": prompt}], **JSON_MODE)


def related_refs():
    refs = (DATA / "paper_refs.txt").read_text()
    prompt = f"""Research question: {QUESTION}

Below is the reference list of the FastUMI paper (arXiv 2409.19499). Choose at least 8 of these
references that matter most for the research question and organise them by theme.
Return ONLY a JSON object:
{{"themes": [{{"theme": str, "papers": [{{"ref_number": int, "title": str, "authors": str, "year": int,
  "arxiv_id": str or null, "doi": str or null, "url": str or null, "why_it_matters": str}}]}}]}}
Copy title, authors, year and any URL from the reference entry. Extract an arXiv ID only if it
appears in the entry. "why_it_matters" must relate the paper to the question, not restate its abstract.

REFERENCES:
{refs}"""
    return run("2b_related_refs", [{"role": "user", "content": prompt}], **JSON_MODE)


if __name__ == "__main__":
    steps = sys.argv[1:] or ["takeaways", "related_free", "related_refs"]
    for s in steps:
        globals()[s]()
