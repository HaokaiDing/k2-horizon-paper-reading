"""Check the deck's visible text: every number must occur in SOURCES.md or BRIEF.md; every [n] must be a listed reference."""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent


class Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts, self.skip = [], False

    def handle_starttag(self, tag, attrs):
        self.skip = tag in ("style", "script")

    def handle_endtag(self, tag):
        self.skip = False

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)


def numbers(s):
    return {n.replace(",", "") for n in re.findall(r"\d+(?:,\d{3})*(?:\.\d+)?", s)}


html = (HERE / f"{sys.argv[1]}.html").read_text()
p = Text()
p.feed(html)
text = " ".join(p.parts)
known = numbers((HERE / "SOURCES.md").read_text() + (HERE / "BRIEF.md").read_text())
# chart data lives in the inline script; check those numbers too
script = " ".join(re.findall(r"<script>(.*?)</script>", html, re.S))
body = re.sub(r"\[\d+\]", " ", text)
refs = re.findall(r"arXiv:(\d{4}\.\d{4,5})|DOI:(10\.\S+?)\.?(?=\s|$)", text)
src = (HERE / "SOURCES.md").read_text().lower()
print("numbers in slide text not in sources/brief:", sorted(numbers(body) - known, key=float))
print("numbers in chart script not in sources/brief:", sorted(numbers(script) - known, key=float))
print("reference IDs not in sources:", [a or d for a, d in refs if (a or d).lower() not in src])
print("citations used:", sorted({int(n) for n in re.findall(r"\[(\d+)\]", text)}))
