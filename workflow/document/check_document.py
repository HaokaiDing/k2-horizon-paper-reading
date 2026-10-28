"""Check a generated document against SOURCES.md: numbers, references, citations, placeholders, length."""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
doc = (HERE / f"{sys.argv[1]}.md").read_text()
src = (HERE / "SOURCES.md").read_text()
src_nums = set(re.sub(r"(?<=\d),(?=\d{3})", "", n) for n in re.findall(r"\d+(?:,\d{3})*(?:\.\d+)?", src))

body, _, refs = doc.partition("## 7. References") if "## 7. References" in doc else doc.partition("References")
words = len(re.sub(r"[#*`>\[\]()|-]", " ", body).split())

# numbers in the body that do not occur anywhere in the sources (ignoring citation markers and section numbers)
text = re.sub(r"\[\d+(?:[,–-]\s*\d+)*\]", "", body)
text = re.sub(r"^#+\s*\d+\.", "", text, flags=re.M)
nums = [re.sub(r"(?<=\d),(?=\d{3})", "", n) for n in re.findall(r"\d+(?:,\d{3})*(?:\.\d+)?", text)]
unsupported = sorted({n for n in nums if n not in src_nums and n.rstrip(".0") not in src_nums})

ref_ids = re.findall(r"(?:arXiv:\s*|arxiv\.org/abs/)(\d{4}\.\d{4,5})|(?:DOI:\s*|doi\.org/)(10\.\d{4,9}/[^\s)\]]+)", refs)
ids = [a or d.rstrip(".") for a, d in ref_ids]
missing_ids = sorted({i for i in ids if i.lower() not in src.lower()})
ref_entries = re.findall(r"^\s*(?:\[(\d+)\]|(\d+)\.)", refs, re.M)
ref_nums = {int(a or b) for a, b in ref_entries}
cited = {int(n) for grp in re.findall(r"\[(\d+(?:[,–-]\s*\d+)*)\]", body) for n in re.split(r"[,–-]\s*", grp)}
placeholders = re.findall(r"\[(?:TODO|TBD|citation needed|insert[^\]]*)\]|lorem ipsum|as an AI|XX+|\?\?\?", doc, re.I)

print(f"words in body: {words}")
print(f"reference entries: {sorted(ref_nums)}")
print(f"cited in text: {sorted(cited)}; cited but not listed: {sorted(cited - ref_nums)}; listed but never cited: {sorted(ref_nums - cited)}")
print(f"reference IDs found: {len(ids)}; IDs not in sources: {missing_ids}")
print(f"numbers in body not found in sources: {unsupported}")
print(f"placeholders: {placeholders}")
