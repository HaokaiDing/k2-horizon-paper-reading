"""Quality checks on the delivered CSV: types, missing values, duplicates, outliers, category counts."""
import csv
import json
import re
import statistics
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
rows = list(csv.DictReader((HERE / "demo_collection_systems.csv").open()))
cols = rows[0].keys()
report = {"rows": len(rows)}

# Missing values ("" in CSV). num_demonstrations is optional by design (only when the abstract states it).
report["missing_values"] = {c: sum(r[c] == "" for r in rows) for c in cols}

# Duplicates
ids = Counter(r["arxiv_id"] for r in rows)
titles = Counter(re.sub(r"[^a-z0-9]", "", r["title"].lower()) for r in rows)
report["duplicates"] = {"arxiv_id": [k for k, v in ids.items() if v > 1],
                        "normalised_title": [k for k, v in titles.items() if v > 1]}

# Types
def is_int(s):
    return re.fullmatch(r"\d+", s) is not None

report["type_errors"] = {
    "arxiv_id_not_YYMM.NNNNN": [r["arxiv_id"] for r in rows if not re.fullmatch(r"\d{4}\.\d{4,5}", r["arxiv_id"])],
    "year_not_int": [r["arxiv_id"] for r in rows if not is_int(r["year"])],
    "num_demonstrations_not_int": [r["arxiv_id"] for r in rows if r["num_demonstrations"] and not is_int(r["num_demonstrations"])],
    "doi_mismatch": [r["arxiv_id"] for r in rows if r["doi"] != f"10.48550/arxiv.{r['arxiv_id']}"],
    # arXiv IDs encode YYMM; publicationYear should equal 20YY
    "year_vs_arxiv_id": [r["arxiv_id"] for r in rows if is_int(r["year"]) and int(r["year"]) != 2000 + int(r["arxiv_id"][:2])],
}

# Outliers
years = [int(r["year"]) for r in rows]
nd = sorted(int(r["num_demonstrations"]) for r in rows if r["num_demonstrations"])
q1, q3 = statistics.quantiles(nd, n=4)[0], statistics.quantiles(nd, n=4)[2]
hi = q3 + 1.5 * (q3 - q1)
report["outliers"] = {
    "year_range": [min(years), max(years)],
    "year_outside_2015_2026": [r["arxiv_id"] for r in rows if not 2015 <= int(r["year"]) <= 2026],
    "num_demonstrations_summary": {"n": len(nd), "min": nd[0], "median": statistics.median(nd), "max": nd[-1],
                                   "iqr_upper_fence": hi},
    "num_demonstrations_above_fence": [(r["arxiv_id"], int(r["num_demonstrations"])) for r in rows
                                       if r["num_demonstrations"] and int(r["num_demonstrations"]) > hi],
}

report["category_counts"] = {c: dict(Counter(r[c] for r in rows).most_common())
                             for c in ("collection_method", "end_effector", "robot_free_collection",
                                       "cross_embodiment", "releases_dataset", "license")}
report["rows_per_year"] = dict(sorted(Counter(years).items()))
(HERE / "quality_checks.json").write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
