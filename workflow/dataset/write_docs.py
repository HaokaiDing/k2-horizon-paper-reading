"""Write the documentation files for the dataset package from the build outputs."""
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
log = json.loads((HERE / "transformation_log.json").read_text())
qc = json.loads((HERE / "quality_checks.json").read_text())
rows = list(csv.DictReader((HERE / "demo_collection_systems.csv").open()))
calls = [json.loads(l) for l in (HERE / "work" / "annotation_calls.jsonl").read_text().splitlines()]
assert log["steps"][-1]["rows_after"] == len(rows) == qc["rows"]

DICT = [
    ("arxiv_id", "string", "arXiv identifier YYMM.NNNNN (no version)", "DataCite DOI suffix"),
    ("doi", "string", "DataCite DOI, always 10.48550/arxiv.<arxiv_id>", "DataCite"),
    ("title", "string", "Paper title (whitespace normalised)", "DataCite titles"),
    ("year", "integer", "Publication year on arXiv", "DataCite publicationYear"),
    ("arxiv_subjects", "string", "arXiv categories, '; '-separated (all include Robotics (cs.RO))", "DataCite subjects"),
    ("license", "string (SPDX id) or empty", "Licence of the arXiv record; empty when the DataCite record has no rights entry", "DataCite rightsList"),
    ("collection_method", "category", "Main demonstration-collection method: handheld_gripper, glove_or_mocap, exoskeleton, vr_ar_teleop, leader_follower, other_teleop, human_video, other", "K2 Horizon, from title + abstract"),
    ("end_effector", "category", "parallel_gripper, dexterous_hand, both, other, unspecified", "K2 Horizon"),
    ("robot_free_collection", "category", "yes / no / unclear: can demonstrations be collected without a robot present", "K2 Horizon"),
    ("cross_embodiment", "category", "yes / no / unclear: does the work transfer data or policies across robots / end-effectors", "K2 Horizon"),
    ("releases_dataset", "category", "yes / no / unclear: does the abstract say a dataset is released", "K2 Horizon"),
    ("num_demonstrations", "integer or empty", "Number of demonstrations/trajectories/episodes when the abstract states one; empty otherwise", "K2 Horizon, all 27 values checked against the abstract"),
    ("k2_rationale", "string", "K2's one-line reason for its labels, in its own words (<= 25 words)", "K2 Horizon"),
]

d = ["# Data dictionary: demo_collection_systems.csv", "",
     f"{len(rows)} rows, one per arXiv paper that presents (or depends on) a system for collecting human demonstrations "
     "for robot manipulation. Delivered in full (not a sample).", "",
     "**Source.** Metadata of arXiv records registered with DataCite (client `arxiv.content`), fetched through the "
     "public DataCite REST API (https://api.datacite.org) on 2026-10-28. DataCite metadata is released under CC0. "
     "Abstracts were used only as input to the annotation and are not included (their licences vary). "
     "No author names or other personal data are included.", "",
     "| Column | Type | Meaning | Origin |", "|---|---|---|---|"]
d += [f"| `{c}` | {t} | {m} | {o} |" for c, t, m, o in DICT]
(HERE / "DATA_DICTIONARY.md").write_text("\n".join(d) + "\n")

t = ["# Transformation log", "", "Steps in order, with the row count after each step "
     "(from `transformation_log.json`, written by `build_dataset.py`).", "",
     "| # | Step | Rows after | What it does |", "|---|---|---|---|"]
t += [f"| {s['step']} | {s['name']} | {s['rows_after']} | {s['note']} |" for s in log["steps"]]
leaked = sum(c.get("reasoning_leaked", False) for c in calls)
failed = [c for c in calls if c.get("error")]
t += ["", f"**Final row count of the delivered file:** {len(rows)} (`demo_collection_systems.csv`).", "",
      "Notes on the annotation step:",
      "- K2 annotated 10 papers per call with `response_format: json_object` and `reasoning_effort: medium`.",
      f"- The run was interrupted once (session ended) and resumed from `work/annotations.jsonl`; already annotated "
      f"papers were not re-sent. Calls logged for the resumed part: {len(calls)}, of which {leaked} put reasoning "
      f"text before the JSON (handled by parsing the last JSON object) and {len(failed)} returned unparseable JSON "
      "and was retried with `reasoning_effort: low`.",
      "- Queries used in step 1 are listed in `build_dataset.py` (`QUERIES`)."]
(HERE / "TRANSFORMATION_LOG.md").write_text("\n".join(t) + "\n")

o = qc["outliers"]
q = ["# Quality checks", "", f"Run by `quality_checks.py` on the delivered file ({qc['rows']} rows); full output in "
     "`quality_checks.json`.", "",
     "| Check | Result |", "|---|---|",
     f"| Missing values | 0 in every column except `license` ({qc['missing_values']['license']}: no rights entry in the "
     f"DataCite record) and `num_demonstrations` ({qc['missing_values']['num_demonstrations']}: abstract states no count; "
     "empty by design) |",
     f"| Duplicate arXiv IDs | {len(qc['duplicates']['arxiv_id'])} |",
     f"| Duplicate titles (normalised) | {len(qc['duplicates']['normalised_title'])} |",
     f"| arXiv ID format | {len(qc['type_errors']['arxiv_id_not_YYMM.NNNNN'])} errors |",
     f"| DOI = 10.48550/arxiv.<id> | {len(qc['type_errors']['doi_mismatch'])} mismatches |",
     f"| `year` integer and equal to the year encoded in the arXiv ID | {len(qc['type_errors']['year_not_int']) + len(qc['type_errors']['year_vs_arxiv_id'])} errors |",
     f"| `num_demonstrations` positive integer | {len(qc['type_errors']['num_demonstrations_not_int'])} errors |",
     "| Category columns within their allowed values | 0 errors (checked in build step 6; 0 rows rejected) |",
     f"| Year range | {o['year_range'][0]}-{o['year_range'][1]}, none outside 2015-2026 |",
     f"| `num_demonstrations` outliers (above Q3 + 1.5 IQR = {o['num_demonstrations_summary']['iqr_upper_fence']:g}) | "
     + ", ".join(f"{a}: {n:,}" for a, n in o["num_demonstrations_above_fence"])
     + ". All four checked against their abstracts and are real (large datasets such as RoboMIND 107k, YUBI 1.20M episodes); kept. |",
     "| `num_demonstrations` vs abstract | 27/27 values found in the abstract (3 written as 2.1K, 10.3k, 1.20M) |", "",
     "## Category counts", ""]
for c, counts in qc["category_counts"].items():
    if c != "license":
        q.append(f"- **{c}:** " + ", ".join(f"{k} {v}" for k, v in counts.items()))
q.append("- **rows per year:** " + ", ".join(f"{k}: {v}" for k, v in qc["rows_per_year"].items()))
(HERE / "QUALITY_CHECKS.md").write_text("\n".join(q) + "\n")
print("docs written")
