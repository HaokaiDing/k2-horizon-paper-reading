"""Generate the slide deck (one self-contained HTML file) with K2 Horizon from BRIEF.md + SOURCES.md.
Usage: generate_slides.py <tag> [report.md <previous_tag>] [effort]
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

FORMAT = """Technical format (needed so the deck prints to a PDF, one slide per page):
- One self-contained HTML file: inline CSS, inline SVG for charts, no external scripts, fonts or images.
- Every slide is <section class="slide"> with a fixed size of exactly 1280px by 720px, overflow hidden,
  page-break-after: always; add @page { size: 1280px 720px; margin: 0 } and body { margin: 0 }.
- Text must fit inside its slide at that size: titles at most 2 lines, body text at least 20px, footnotes at least 14px.
- Charts are inline <svg> with numeric axis labels, drawn from the exact numbers in Source 2.
- A small slide number in a corner of every slide except the title slide."""

prompt = (f"Make the slide deck described in this brief, using only the source material.\n\nBRIEF:\n"
          f"{(HERE / 'BRIEF.md').read_text()}\n\n{FORMAT}\n\nSOURCE MATERIAL:\n{(HERE / 'SOURCES.md').read_text()}\n\n")
if report:
    prompt += (f"You already made the deck below. I rendered and checked it; fix every point in my review and return "
               f"the complete revised file.\n\nMY REVIEW:\n{report}\n\nYOUR DECK:\n{(HERE / f'{prev}.html').read_text()}\n\n")
prompt += "Output ONLY the HTML file, starting with <!DOCTYPE html>."

content, reasoning, usage, latency = chat([{"role": "user", "content": prompt}], max_tokens=40000, temperature=0.3,
                                          chat_template_kwargs={"reasoning_effort": effort})
# Reasoning can leak into content (and may itself contain "<!DOCTYPE html>"): keep the last complete document.
m = ([None] + list(re.finditer(r"<!DOCTYPE html>\s*<html.*?</html>", content, re.S | re.I)))[-1]
html = m.group(0) if m else None
(HERE / "runs").mkdir(exist_ok=True)
(HERE / "runs" / f"{tag}.json").write_text(json.dumps(
    {"tag": tag, "from": prev, "model": MODEL, "reasoning_effort": effort, "latency_s": latency, "usage": usage,
     "report": report, "reasoning": reasoning, "content": content, "html_found": bool(html)},
    indent=2, ensure_ascii=False))
if html:
    (HERE / f"{tag}.html").write_text(html + "\n")
print(f"{tag}: {latency}s {usage.get('total_tokens')} tok html_found={bool(html)} "
      f"slides={html.count('class=\"slide') if html else 0}")
