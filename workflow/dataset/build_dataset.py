"""Build a dataset of robot-manipulation demonstration-collection systems from arXiv metadata.

Source: DataCite metadata for arXiv records (client arxiv.content); DataCite metadata is CC0.
Steps (each logs its row count to transformation_log.json):
  1 fetch      keyword queries over titles + abstracts
  2 dedupe     one row per arXiv DOI
  3 filter_ro  keep records whose arXiv subjects include Robotics (cs.RO)
  4 annotate   K2 Horizon reads title + abstract -> relevance + structured fields
  5 relevant   keep rows K2 marks as presenting or substantially using a demo-collection system
  6 validate   type/enum checks, drop rows that fail (none expected), write final CSV
Abstracts are used for annotation but not shipped (their licences vary).
"""
import csv
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from k2 import MODEL, chat  # noqa: E402

HERE = Path(__file__).resolve().parent
WORK = HERE / "work"
WORK.mkdir(exist_ok=True)
UA = {"User-Agent": "k2-dataset-builder/0.1 (research use)"}

QUERIES = [
    '"handheld gripper"', '"hand-held gripper"', '"universal manipulation interface"',
    '"data collection" AND teleoperation AND manipulation', '"demonstration collection" AND robot',
    'exoskeleton AND teleoperation AND manipulation', '"data glove" AND robot',
    '"motion capture" AND demonstrations AND manipulation', '"augmented reality" AND demonstrations AND robot',
    '"leader-follower" AND teleoperation', '"in-the-wild" AND demonstrations AND manipulation',
]

METHODS = ["handheld_gripper", "glove_or_mocap", "exoskeleton", "vr_ar_teleop", "leader_follower",
           "other_teleop", "human_video", "other"]
EFFECTORS = ["parallel_gripper", "dexterous_hand", "both", "other", "unspecified"]
TRISTATE = ["yes", "no", "unclear"]
LOG = []


def log(step, n, note):
    LOG.append({"step": len(LOG) + 1, "name": step, "rows_after": n, "note": note})
    print(f"{step:<10} rows={n:<5} {note}")


def get_json(url):
    for attempt in range(6):
        try:
            time.sleep(1.0)
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90) as r:
                return json.load(r)
        except Exception as e:  # DataCite occasionally 5xx/429s; back off
            print("  retry", attempt, e)
            time.sleep(10 * (attempt + 1))
    raise RuntimeError(url)


def fetch():
    rows = []
    for q in QUERIES:
        query = f"titles.title:({q}) OR descriptions.description:({q})"
        url = "https://api.datacite.org/dois?" + urllib.parse.urlencode(
            {"client-id": "arxiv.content", "query": query, "page[size]": 100, "page[cursor]": 1})
        while url:
            d = get_json(url)
            for rec in d["data"]:
                a = rec["attributes"]
                abstract = next((x["description"] for x in a.get("descriptions", [])
                                 if x.get("descriptionType") == "Abstract"), "")
                rows.append({
                    "doi": rec["id"].lower(),
                    "arxiv_id": rec["id"].lower().split("arxiv.")[-1],
                    "title": re.sub(r"\s+", " ", a["titles"][0]["title"]).strip(),
                    "year": a.get("publicationYear"),
                    "subjects": "; ".join(s["subject"] for s in a.get("subjects", [])
                                          if s.get("subjectScheme") == "arXiv"),
                    "license": (a.get("rightsList") or [{}])[0].get("rightsIdentifier", ""),
                    "abstract": re.sub(r"\s+", " ", abstract).strip(),
                    "matched_query": q,
                })
            url = d.get("links", {}).get("next")
        print(f"  {q}: {len(rows)} cumulative")
    return rows


ANNOTATE_PROMPT = """You are building a dataset of systems for collecting human demonstrations for robot manipulation.
For each paper below (title + abstract), return one JSON object per paper. Use only what the abstract says.

Fields:
- "arxiv_id": copy from input
- "relevant": true if the paper PRESENTS a system/device/interface for collecting manipulation demonstrations,
  or its main contribution depends on such a system (e.g. a new dataset collected with one). false otherwise
  (pure policy-learning papers, surveys, locomotion, non-manipulation teleoperation, etc.).
- "collection_method": one of {methods} (main method; "other" if relevant=false)
- "end_effector": one of {effectors}
- "robot_free_collection": one of {tri}  (can demonstrations be collected without a robot present?)
- "cross_embodiment": one of {tri}  (does it transfer data/policies across different robots or end-effectors?)
- "releases_dataset": one of {tri}  (does the abstract say a dataset is released/open-sourced?)
- "num_demonstrations": integer or null (only if the abstract states a number of demonstrations/trajectories/episodes)
- "rationale": <= 25 words in your own words, no copying from the abstract

Return ONLY a JSON object: {{"papers": [ ... ]}} with exactly one entry per input paper, same order.

PAPERS:
{papers}"""


def annotate(rows, batch=10):
    out_path = WORK / "annotations.jsonl"
    done = {}
    if out_path.exists():
        for line in out_path.read_text().splitlines():
            r = json.loads(line)
            done[r["arxiv_id"]] = r
    todo = [r for r in rows if r["arxiv_id"] not in done]
    calls = []
    for i in range(0, len(todo), batch):
        chunk = todo[i:i + batch]
        papers = json.dumps([{"arxiv_id": r["arxiv_id"], "title": r["title"], "abstract": r["abstract"]}
                             for r in chunk], ensure_ascii=False, indent=1)
        prompt = ANNOTATE_PROMPT.format(methods=METHODS, effectors=EFFECTORS, tri=TRISTATE, papers=papers)
        for effort in ("medium", "low"):
            content, _, usage, latency = chat([{"role": "user", "content": prompt}], max_tokens=16000,
                                              response_format={"type": "json_object"},
                                              chat_template_kwargs={"reasoning_effort": effort})
            calls.append({"batch": i // batch, "effort": effort, "latency_s": latency, "usage": usage,
                          "reasoning_leaked": not content.lstrip().startswith("{")})
            try:
                start = content.rfind('{"papers"')
                if start < 0:
                    start = content.find("{")
                papers_out = json.JSONDecoder().raw_decode(content[start:])[0]["papers"]
                if len(papers_out) != len(chunk):
                    raise ValueError(f"{len(papers_out)} answers for {len(chunk)} papers")
                break
            except Exception as e:
                calls[-1]["error"] = str(e)
                print(f"  batch {i // batch} ({effort}) failed: {e}")
                papers_out = None
        if papers_out is None:
            continue
        with out_path.open("a") as f:
            for src, ann in zip(chunk, papers_out):
                ann["arxiv_id"] = src["arxiv_id"]  # trust input order, not the echoed id
                done[src["arxiv_id"]] = ann
                f.write(json.dumps(ann, ensure_ascii=False) + "\n")
        print(f"  batch {i // batch}: {latency}s {usage.get('total_tokens')} tok")
    with (WORK / "annotation_calls.jsonl").open("a") as f:
        for c in calls:
            f.write(json.dumps(c) + "\n")
    return done


def validate(row):
    errs = []
    if not re.fullmatch(r"\d{4}\.\d{4,5}", row["arxiv_id"]):
        errs.append("arxiv_id format")
    if not isinstance(row["year"], int) or not 1990 <= row["year"] <= 2026:
        errs.append("year range")
    if row["collection_method"] not in METHODS:
        errs.append("collection_method enum")
    if row["end_effector"] not in EFFECTORS:
        errs.append("end_effector enum")
    for k in ("robot_free_collection", "cross_embodiment", "releases_dataset"):
        if row[k] not in TRISTATE:
            errs.append(f"{k} enum")
    n = row["num_demonstrations"]
    if n not in (None, "") and (not isinstance(n, int) or n <= 0):
        errs.append("num_demonstrations type")
    return errs


COLUMNS = ["arxiv_id", "doi", "title", "year", "arxiv_subjects", "license", "collection_method", "end_effector",
           "robot_free_collection", "cross_embodiment", "releases_dataset", "num_demonstrations", "k2_rationale"]


def main():
    raw_path = WORK / "raw.json"
    if raw_path.exists():
        raw = json.loads(raw_path.read_text())
    else:
        raw = fetch()
        raw_path.write_text(json.dumps(raw, ensure_ascii=False))
    log("fetch", len(raw), f"{len(QUERIES)} keyword queries over arXiv titles+abstracts in DataCite")

    seen, rows = set(), []
    for r in raw:
        if r["arxiv_id"] not in seen:
            seen.add(r["arxiv_id"])
            rows.append(r)
    log("dedupe", len(rows), "one row per arXiv ID (same paper matched by several queries)")

    rows = [r for r in rows if "cs.RO" in r["subjects"]]
    log("filter_ro", len(rows), "kept records with Robotics (cs.RO) among their arXiv subjects")

    rows = [r for r in rows if len(r["abstract"]) >= 200]
    log("has_abstract", len(rows), "kept records with an abstract of >= 200 characters (needed for annotation)")

    ann = annotate(rows)
    rows = [dict(r, **{k: v for k, v in ann[r["arxiv_id"]].items() if k != "arxiv_id"})
            for r in rows if r["arxiv_id"] in ann]
    log("annotate", len(rows), f"K2 Horizon ({MODEL}) annotated each record from title + abstract")

    rows = [r for r in rows if r.get("relevant") is True]
    log("relevant", len(rows), "kept rows K2 marked as presenting/depending on a demonstration-collection system")

    final, rejected = [], []
    for r in rows:
        r["num_demonstrations"] = r.get("num_demonstrations")
        errs = validate(r)
        (rejected if errs else final).append((r, errs))
    log("validate", len(final), f"type/enum checks; {len(rejected)} rows rejected")
    final = sorted((r for r, _ in final), key=lambda r: (r["year"], r["arxiv_id"]))

    with (HERE / "demo_collection_systems.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        for r in final:
            w.writerow({**{c: r.get(c) for c in COLUMNS}, "arxiv_subjects": r["subjects"],
                        "k2_rationale": r.get("rationale", ""),
                        "num_demonstrations": "" if r["num_demonstrations"] is None else r["num_demonstrations"]})
    log("write", len(final), "final file demo_collection_systems.csv")
    (HERE / "transformation_log.json").write_text(json.dumps(
        {"steps": LOG, "rejected": [{"arxiv_id": r["arxiv_id"], "errors": e} for r, e in rejected]}, indent=2))


if __name__ == "__main__":
    main()
