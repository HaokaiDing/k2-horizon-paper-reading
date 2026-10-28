"""Convert an arXiv HTML paper into plain text, split into body and references."""
import html
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

SKIP = {"script", "style", "nav", "header", "footer", "math"}
BLOCK = {"p", "div", "li", "h1", "h2", "h3", "h4", "h5", "h6", "tr", "br", "section", "figcaption", "table"}


class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts, self.skip = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in SKIP:
            self.skip += 1
        # Keep LaTeX source of math so formulas don't vanish.
        if tag == "math":
            alt = dict(attrs).get("alttext")
            if alt:
                self.parts.append(f" ${alt}$ ")
        if tag in BLOCK:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in SKIP and self.skip:
            self.skip -= 1
        if tag in BLOCK:
            self.parts.append("\n")

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)


def main(src, out_dir):
    raw = Path(src).read_text(encoding="utf-8")
    p = TextExtractor()
    p.feed(raw)
    text = html.unescape("".join(p.parts))
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text).strip()
    # Split at the last "References" heading.
    idx = max(text.rfind("\nReferences\n"), text.rfind("\nREFERENCES\n"))
    body, refs = (text[:idx], text[idx:]) if idx > 0 else (text, "")
    out = Path(out_dir)
    (out / "paper_body.txt").write_text(body, encoding="utf-8")
    (out / "paper_refs.txt").write_text(refs, encoding="utf-8")
    print(f"body chars={len(body)} refs chars={len(refs)}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
