"""Generate the review document with K2 Horizon from BRIEF.md + SOURCES.md (optionally with a revision report).
Usage: generate_document.py <tag> [report.md <previous_tag>] [effort]
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from k2 import MODEL, chat  # noqa: E402

HERE = Path(__file__).resolve().parent
tag = sys.argv[1]
report = (HERE / sys.argv[2]).read_text() if len(sys.argv) > 3 else None
prev = sys.argv[3] if len(sys.argv) > 3 else None
effort = sys.argv[4] if len(sys.argv) > 4 else "medium"

prompt = (f"Write the document described in this brief, using only the source material.\n\nBRIEF:\n"
          f"{(HERE / 'BRIEF.md').read_text()}\n\nSOURCE MATERIAL:\n{(HERE / 'SOURCES.md').read_text()}\n\n")
if report:
    prompt += (f"You already wrote the draft below. I checked it against the sources; revise it to fix every point in "
               f"my review and return the complete revised document.\n\nMY REVIEW:\n{report}\n\nYOUR DRAFT:\n"
               f"{(HERE / f'{prev}.md').read_text()}\n\n")
prompt += "Output ONLY the finished Markdown document, starting with the title line '# '."

content, reasoning, usage, latency = chat([{"role": "user", "content": prompt}], max_tokens=30000, temperature=0.3,
                                          chat_template_kwargs={"reasoning_effort": effort})
# Reasoning can leak into content: keep from the last line that starts with the document title.
starts = [m.start() for m in re.finditer(r"^# Moving handheld", content, re.M)]
doc = content[starts[-1]:].strip() if starts else None
(HERE / "runs").mkdir(exist_ok=True)
(HERE / "runs" / f"{tag}.json").write_text(json.dumps(
    {"tag": tag, "from": prev, "model": MODEL, "reasoning_effort": effort, "latency_s": latency, "usage": usage,
     "report": report, "reasoning": reasoning, "content": content, "doc_found": bool(doc)},
    indent=2, ensure_ascii=False))
if doc:
    (HERE / f"{tag}.md").write_text(doc + "\n")
print(f"{tag}: {latency}s {usage.get('total_tokens')} tok doc_found={bool(doc)} words={len(doc.split()) if doc else 0}")
