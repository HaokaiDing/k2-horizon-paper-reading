# Dataset: robot-manipulation demonstration-collection systems on arXiv

**Real task.** I work on UMI-style (handheld gripper) data collection for robot manipulation. To survey the field and
pick baselines I need a structured list of papers that present demonstration-collection systems: how the data are
collected (handheld gripper, glove, exoskeleton, VR/AR, leader-follower, ...), for which end-effector, whether a robot
is needed during collection, and whether data are released.

**Files**
- `demo_collection_systems.csv`: the dataset, 203 rows, delivered in full.
- `DATA_DICTIONARY.md`: every column's type, meaning and origin; the data source.
- `TRANSFORMATION_LOG.md` / `transformation_log.json`: steps in order with row counts (360 -> 298 -> 295 -> 295 -> 295 -> 203 -> 203 -> 203).
- `QUALITY_CHECKS.md` / `quality_checks.json`: missing values, duplicates, types, outliers, category counts.
- `MANUAL_CHECK.md`: my check of K2's labels on a random sample of 20 (relevance 19/20 correct).
- `k2_annotations.jsonl`: K2 Horizon's raw annotation for all 295 candidate papers.
- `scripts/`: `build_dataset.py` (fetch, clean, annotate, validate), `quality_checks.py`, `write_docs.py`, `k2.py` (API client; key read from the environment, none included).

**How K2 Horizon was used.** `IFM/K2-Horizon-375B-A23B` read each candidate's title and abstract (10 per call) and
decided relevance plus six structured fields. The scripts validate every value against allowed types/categories.

**Reproduce:** `export K2_API_KEY=...; python3 scripts/build_dataset.py && python3 scripts/quality_checks.py`
(network access to api.datacite.org and api.ifm.ai; Python 3 standard library only).

No personal data: author names and abstracts are not included; only bibliographic IDs, titles, years, categories,
licences and the model's labels.
