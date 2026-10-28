"""Step 3: check K2's outputs against ground truth.

- 1_takeaways: is every evidence_quote really in the paper text?
- 2a / 2b related work: does each paper exist (DataCite arXiv records / Crossref), and does its arXiv ID
  point to the same title (DataCite record of 10.48550/arXiv.<id>)?
"""
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from difflib import SequenceMatcher
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUNS, DATA = HERE / "runs", HERE / "data"
UA = {"User-Agent": "k2-workflow-verify/0.1 (research use)"}


def norm(s):
    return re.sub(r"[^a-z0-9 ]", "", re.sub(r"\s+", " ", (s or "").lower())).strip()


def sim(a, b):
    return round(SequenceMatcher(None, norm(a), norm(b)).ratio(), 2)


CACHE_FILE = RUNS / "verify_cache.json"
CACHE = json.loads(CACHE_FILE.read_text()) if CACHE_FILE.exists() else {}


def get(url, retries=8):
    if url in CACHE:
        return CACHE[url].encode()
    for attempt in range(retries):
        time.sleep(1.5)  # be polite to public APIs
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                body = r.read()
            CACHE[url] = body.decode()
            CACHE_FILE.write_text(json.dumps(CACHE))
            return body
        except urllib.error.HTTPError as e:
            if e.code == 404:
                CACHE[url] = "__404__"
                CACHE_FILE.write_text(json.dumps(CACHE))
            if e.code not in (429, 503) or attempt == retries - 1:
                raise
            time.sleep(min(int(e.headers.get("Retry-After") or 10), 30))


def arxiv_by_id(aid):
    """Title registered for this arXiv ID (via its DataCite DOI 10.48550/arXiv.<id>)."""
    aid = re.sub(r"^(arxiv:)?", "", aid.strip(), flags=re.I).split("v")[0]
    try:
        raw = get(f"https://api.datacite.org/dois/10.48550/arxiv.{aid}")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise
    if raw == b"__404__":
        return None
    attrs = json.loads(raw)["data"]["attributes"]
    return attrs["titles"][0]["title"]


def datacite_arxiv_by_title(title):
    """Best title match among arXiv records in DataCite."""
    words = " ".join(re.findall(r"[A-Za-z0-9]+", title)[:14])
    q = urllib.parse.urlencode({"query": f"titles.title:({words})", "client-id": "arxiv.content",
                                "page[size]": 10})
    best = None
    for d in json.loads(get(f"https://api.datacite.org/dois?{q}"))["data"]:
        t = d["attributes"]["titles"][0]["title"]
        if best is None or sim(t, title) > best[2]:
            best = (d["id"], t, sim(t, title))
    return best


def crossref_by_title(title):
    q = urllib.parse.urlencode({"query.bibliographic": title, "rows": 1})
    items = json.loads(get(f"https://api.crossref.org/works?{q}"))["message"]["items"]
    if not items:
        return None
    t = (items[0].get("title") or [""])[0]
    return items[0].get("DOI"), t, sim(t, title)


def check_paper(p):
    title, aid = p.get("title", ""), p.get("arxiv_id")
    out = {"title": title, "claimed_arxiv_id": aid}
    if aid:
        real = arxiv_by_id(aid)
        out["arxiv_title_at_id"] = real
        out["id_title_similarity"] = sim(real, title) if real else 0
        if real and out["id_title_similarity"] >= 0.85:
            out["status"] = "verified_id"
            return out
    hit = datacite_arxiv_by_title(title)
    if hit and hit[2] >= 0.85:
        out.update(found_id=hit[0], found_title=hit[1], status="wrong_id" if aid else "found_by_title")
        return out
    cr = crossref_by_title(title)
    if cr and cr[2] >= 0.85:
        out.update(found_doi=cr[0], found_title=cr[1], status="wrong_id" if aid else "found_by_title")
        return out
    out["status"] = "not_found"
    return out


def verify_related(step):
    rec = json.loads((RUNS / f"{step}.json").read_text())
    rows = []
    for theme in rec["parsed"]["themes"]:
        for p in theme["papers"]:
            r = check_paper(p)
            r["theme"] = theme["theme"]
            rows.append(r)
            print(f"  [{r['status']:<14}] {r['title'][:70]}")
    counts = {}
    for r in rows:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    return {"n": len(rows), "counts": counts, "rows": rows}


def verify_quotes():
    raw = (DATA / "paper_body.txt").read_text()
    body = norm(raw)
    body_nocite = norm(re.sub(r"\s*\[\d+(?:[,–-]\s*\d+)*\]", "", raw))  # drop "[30]"-style markers
    rec = json.loads((RUNS / "1_takeaways.json").read_text())["parsed"]
    rows = []
    for kind in ("findings", "methods", "limitations"):
        for item in rec[kind]:
            q = norm(item["evidence_quote"])
            rows.append({"kind": kind, "point": item["point"], "quote": item["evidence_quote"],
                         "verbatim": q in body, "verbatim_ignoring_citation_markers": q in body_nocite,
                         "stated_by_authors": item.get("stated_by_authors")})
    return {"n": len(rows), "verbatim": sum(r["verbatim"] for r in rows),
            "verbatim_ignoring_citation_markers": sum(r["verbatim_ignoring_citation_markers"] for r in rows),
            "rows": rows}


if __name__ == "__main__":
    report = {"1_takeaways_quotes": verify_quotes()}
    q = report["1_takeaways_quotes"]
    print(f"quotes verbatim: {q['verbatim']}/{q['n']} strict, "
          f"{q['verbatim_ignoring_citation_markers']}/{q['n']} ignoring [n] citation markers")
    for step in ("2a_related_free", "2b_related_refs"):
        print(step)
        report[step] = verify_related(step)
        print("  ->", report[step]["counts"])
    (RUNS / "3_verification.json").write_text(json.dumps(report, indent=2, ensure_ascii=False))
