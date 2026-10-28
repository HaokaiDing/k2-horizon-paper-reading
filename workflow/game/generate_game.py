"""Ask K2 Horizon to write a single-file HTML game from a brief; save the raw run and the HTML."""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from k2 import MODEL, chat  # noqa: E402

HERE = Path(__file__).resolve().parent
BRIEF = (HERE / "BRIEF.md").read_text()

PROMPT = f"""Write a complete browser game as ONE self-contained HTML file, following this brief exactly.

{BRIEF}

Technical rules:
- One file: inline <style> and <script>, no external URLs, no images or fonts to load, no build step.
- Draw with the Canvas 2D API. Use requestAnimationFrame with delta time so speed does not depend on frame rate.
- Must work with keyboard AND with on-screen/touch buttons.
- No console errors. No placeholder or TODO code.

Output ONLY the HTML, starting with <!DOCTYPE html> and ending with </html>."""


def main(tag):
    content, reasoning, usage, latency = chat([{"role": "user", "content": PROMPT}], max_tokens=32000,
                                              temperature=0.4,
                                              chat_template_kwargs={"reasoning_effort": "medium"})
    # reasoning can leak into content and mention "<!DOCTYPE html>": take the last real document
    m = ([None] + list(re.finditer(r"<!DOCTYPE html>\s*<html.*?</html>", content, re.S | re.I)))[-1]
    run = {"tag": tag, "model": MODEL, "latency_s": latency, "usage": usage, "prompt": PROMPT,
           "reasoning": reasoning, "content": content, "html_found": bool(m),
           "reasoning_leaked_into_content": not content.lstrip().lower().startswith(("<!doctype", "```"))}
    (HERE / "runs").mkdir(exist_ok=True)
    (HERE / "runs" / f"{tag}.json").write_text(json.dumps(run, indent=2, ensure_ascii=False))
    if m:
        (HERE / f"{tag}.html").write_text(m.group(0))
    print(f"{tag}: {latency}s {usage.get('total_tokens')} tok html_found={bool(m)} chars={len(m.group(0)) if m else 0}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "k2_v1")
