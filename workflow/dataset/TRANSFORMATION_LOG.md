# Transformation log

Steps in order, with the row count after each step (from `transformation_log.json`, written by `build_dataset.py`).

| # | Step | Rows after | What it does |
|---|---|---|---|
| 1 | fetch | 360 | 11 keyword queries over arXiv titles+abstracts in DataCite |
| 2 | dedupe | 298 | one row per arXiv ID (same paper matched by several queries) |
| 3 | filter_ro | 295 | kept records with Robotics (cs.RO) among their arXiv subjects |
| 4 | has_abstract | 295 | kept records with an abstract of >= 200 characters (needed for annotation) |
| 5 | annotate | 295 | K2 Horizon (IFM/K2-Horizon-375B-A23B) annotated each record from title + abstract |
| 6 | relevant | 203 | kept rows K2 marked as presenting/depending on a demonstration-collection system |
| 7 | validate | 203 | type/enum checks; 0 rows rejected |
| 8 | write | 203 | final file demo_collection_systems.csv |

**Final row count of the delivered file:** 203 (`demo_collection_systems.csv`).

Notes on the annotation step:
- K2 annotated 10 papers per call with `response_format: json_object` and `reasoning_effort: medium`.
- The run was interrupted once (session ended) and resumed from `work/annotations.jsonl`; already annotated papers were not re-sent. Calls logged for the resumed part: 10, of which 7 put reasoning text before the JSON (handled by parsing the last JSON object) and 1 returned unparseable JSON and was retried with `reasoning_effort: low`.
- Queries used in step 1 are listed in `build_dataset.py` (`QUERIES`).
