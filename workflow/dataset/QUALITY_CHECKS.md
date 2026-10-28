# Quality checks

Run by `quality_checks.py` on the delivered file (203 rows); full output in `quality_checks.json`.

| Check | Result |
|---|---|
| Missing values | 0 in every column except `license` (109: no rights entry in the DataCite record) and `num_demonstrations` (176: abstract states no count; empty by design) |
| Duplicate arXiv IDs | 0 |
| Duplicate titles (normalised) | 0 |
| arXiv ID format | 0 errors |
| DOI = 10.48550/arxiv.<id> | 0 mismatches |
| `year` integer and equal to the year encoded in the arXiv ID | 0 errors |
| `num_demonstrations` positive integer | 0 errors |
| Category columns within their allowed values | 0 errors (checked in build step 6; 0 rows rejected) |
| Year range | 2019-2026, none outside 2015-2026 |
| `num_demonstrations` outliers (above Q3 + 1.5 IQR = 24850) | 2412.13877: 107,000, 2606.10244: 1,200,000, 2607.21588: 50,000, 2609.23755: 179,049. All four checked against their abstracts and are real (large datasets such as RoboMIND 107k, YUBI 1.20M episodes); kept. |
| `num_demonstrations` vs abstract | 27/27 values found in the abstract (3 written as 2.1K, 10.3k, 1.20M) |

## Category counts

- **collection_method:** other_teleop 69, vr_ar_teleop 36, handheld_gripper 31, exoskeleton 21, glove_or_mocap 15, human_video 14, other 9, leader_follower 8
- **end_effector:** unspecified 108, dexterous_hand 56, parallel_gripper 18, other 11, both 10
- **robot_free_collection:** no 107, yes 84, unclear 12
- **cross_embodiment:** unclear 70, yes 67, no 66
- **releases_dataset:** no 149, yes 34, unclear 20
- **rows per year:** 2019: 2, 2020: 3, 2021: 1, 2022: 4, 2023: 5, 2024: 24, 2025: 70, 2026: 94
