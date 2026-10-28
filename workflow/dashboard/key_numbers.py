"""Compute the dashboard's key numbers directly from data.csv (independent of the dashboard code)."""
import csv
import json
import statistics
from collections import Counter

rows = list(csv.DictReader(open("data.csv")))
n = len(rows)
pct = lambda k: round(100 * k / n, 1)
methods = Counter(r["collection_method"] for r in rows)
years = Counter(int(r["year"]) for r in rows)
robot_free = sum(r["robot_free_collection"] == "yes" for r in rows)
releases = sum(r["releases_dataset"] == "yes" for r in rows)
xemb = sum(r["cross_embodiment"] == "yes" for r in rows)
demos = [int(r["num_demonstrations"]) for r in rows if r["num_demonstrations"]]
recent = sum(int(r["year"]) >= 2025 for r in rows)
hh = [r for r in rows if r["collection_method"] == "handheld_gripper"]
by_method_year = {m: dict(sorted(Counter(int(r["year"]) for r in rows if r["collection_method"] == m).items()))
                  for m in methods}
out = {
    "total_papers": n,
    "papers_by_method": dict(methods.most_common()),
    "papers_by_year": dict(sorted(years.items())),
    "papers_2025_or_later": recent, "pct_2025_or_later": pct(recent),
    "robot_free_yes": robot_free, "pct_robot_free_yes": pct(robot_free),
    "releases_dataset_yes": releases, "pct_releases_dataset_yes": pct(releases),
    "cross_embodiment_yes": xemb, "pct_cross_embodiment_yes": pct(xemb),
    "handheld_gripper_papers": len(hh),
    "handheld_gripper_robot_free_yes": sum(r["robot_free_collection"] == "yes" for r in hh),
    "papers_stating_num_demos": len(demos), "median_num_demos": statistics.median(demos),
    "end_effector": dict(Counter(r["end_effector"] for r in rows).most_common()),
    "papers_by_method_year": by_method_year,
}
json.dump(out, open("key_numbers.json", "w"), indent=2)
print(json.dumps({k: v for k, v in out.items() if k != "papers_by_method_year"}, indent=1))
