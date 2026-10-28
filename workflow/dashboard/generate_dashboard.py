"""Ask K2 Horizon to write the dashboard as one HTML file whose numbers are all computed from embedded rows.

K2 writes the page with the placeholder /*__DATA__*/; this script injects data.csv as a JSON array there.
Usage: generate_dashboard.py <tag> [report.md <previous_tag>] [effort]
"""
import csv
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
effort = sys.argv[4] if len(sys.argv) > 4 else "low"
rows = list(csv.DictReader((HERE / "data.csv").open()))
BRIEF = (HERE / "BRIEF.md").read_text()
DICT = (HERE / "DATA_DICTIONARY.md").read_text()

SPEC = f"""Write a dashboard as ONE self-contained HTML file for this brief.

{BRIEF}

DATA DICTIONARY:
{DICT}

Example rows (the real page gets all {len(rows)}):
{json.dumps(rows[:3], indent=1, ensure_ascii=False)}

Technical rules:
- Put exactly `const ROWS = /*__DATA__*/[];` in the script; I will replace /*__DATA__*/[] with the full JSON array
  of row objects (all values are strings exactly as in the CSV; empty string = missing).
- EVERY number on the page must be computed in JavaScript from ROWS at load time. Do not hard-code any count,
  percentage or median. Percentages = 100 * count / total rows, rounded to 1 decimal. Median of num_demonstrations
  over non-empty values (average of the two middle values if even).
- Charts drawn with inline SVG or Canvas you write yourself; no external libraries, fonts, CDNs or network requests.
- Give every headline tile an id: kpi-total, kpi-recent, kpi-robotfree, kpi-releases, kpi-xemb, kpi-handheld,
  kpi-median. Put the numeric value in an element with class "value".
- Clean, readable layout that works from 360 px wide to desktop; light background; accessible colours.
- No placeholder or TODO text."""


def extract(content):
    ms = list(re.finditer(r"<!DOCTYPE html>\s*<html.*?</html>", content, re.S | re.I))
    return ms[-1].group(0) if ms else None


if report:
    prompt = (f"{SPEC}\n\nYou already wrote the page below. I tested it; fix everything in my report and return "
              f"the complete corrected file.\n\nMY TEST REPORT:\n{report}\n\nYOUR PAGE:\n"
              f"{(HERE / f'{prev}.template.html').read_text()}\n\nOutput ONLY the HTML.")
else:
    prompt = SPEC + "\n\nOutput ONLY the HTML, starting with <!DOCTYPE html> and ending with </html>."

content, reasoning, usage, latency = chat([{"role": "user", "content": prompt}], max_tokens=40000,
                                          temperature=0.3, chat_template_kwargs={"reasoning_effort": effort})
html = extract(content)
(HERE / "runs").mkdir(exist_ok=True)
(HERE / "runs" / f"{tag}.json").write_text(json.dumps(
    {"tag": tag, "from": prev, "model": MODEL, "reasoning_effort": effort, "latency_s": latency, "usage": usage,
     "report": report, "reasoning": reasoning, "content": content, "html_found": bool(html)}, indent=2,
    ensure_ascii=False))
if html:
    (HERE / f"{tag}.template.html").write_text(html)
    ok = "/*__DATA__*/[]" in html
    if ok:
        (HERE / f"{tag}.html").write_text(html.replace("/*__DATA__*/[]", json.dumps(rows, ensure_ascii=False)))
    print(f"{tag}: {latency}s {usage.get('total_tokens')} tok placeholder_found={ok}")
else:
    print(f"{tag}: {latency}s {usage.get('total_tokens')} tok NO HTML")
