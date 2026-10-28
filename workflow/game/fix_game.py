"""Round 2: give K2 its own v1 code plus my test report and ask for a corrected, complete file."""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from k2 import MODEL, chat  # noqa: E402

HERE = Path(__file__).resolve().parent
src, out, report = sys.argv[1], sys.argv[2], (HERE / sys.argv[3]).read_text()
EFFORT = sys.argv[4] if len(sys.argv) > 4 else "medium"  # "low" when medium reasoning runs out of tokens
code = (HERE / f"{src}.html").read_text()
BRIEF = (HERE / "BRIEF.md").read_text()

PROMPT = f"""You wrote the game below for this brief. I played it in Chrome and found bugs. Fix ALL of them and
return the complete corrected file (not a diff). Keep it one self-contained HTML file, Canvas 2D, no external
resources, no placeholder code.

BRIEF:
{BRIEF}

MY TEST REPORT:
{report}

YOUR CODE:
{code}

Output ONLY the corrected HTML, starting with <!DOCTYPE html> and ending with </html>."""

content, reasoning, usage, latency = chat([{"role": "user", "content": PROMPT}], max_tokens=40000, temperature=0.3,
                                          chat_template_kwargs={"reasoning_effort": EFFORT})
# reasoning can leak into content and mention "<!DOCTYPE html>": take the last real document
m = ([None] + list(re.finditer(r"<!DOCTYPE html>\s*<html.*?</html>", content, re.S | re.I)))[-1]
(HERE / "runs").mkdir(exist_ok=True)
(HERE / "runs" / f"{out}.json").write_text(json.dumps(
    {"tag": out, "from": src, "reasoning_effort": EFFORT, "model": MODEL, "latency_s": latency, "usage": usage, "report": report,
     "reasoning": reasoning, "content": content, "html_found": bool(m)}, indent=2, ensure_ascii=False))
if m:
    (HERE / f"{out}.html").write_text(m.group(0))
print(f"{out}: {latency}s {usage.get('total_tokens')} tok html_found={bool(m)} chars={len(m.group(0)) if m else 0}")
