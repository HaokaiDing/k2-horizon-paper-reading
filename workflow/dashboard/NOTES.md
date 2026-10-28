# Notes: key numbers and how they were calculated

Data: `data.csv` (203 rows, one per paper; columns in `DATA_DICTIONARY.md`). The dashboard (`dashboard.html`) embeds
exactly these rows and computes every number in JavaScript at load time; nothing is hard-coded.
`key_numbers.py` recomputes the same numbers independently in Python (output `key_numbers.json`); both agree.

| Key number | Value | How it is calculated |
|---|---|---|
| Total papers | 203 | number of rows |
| Papers from 2025 or later | 80.8 % (164) | rows with year >= 2025, / total rows x 100, 1 decimal |
| Robot-free collection | 41.4 % (84) | rows with robot_free_collection = yes, / total rows |
| Releases a dataset | 16.7 % (34) | rows with releases_dataset = yes, / total rows |
| Cross-embodiment | 33.0 % (67) | rows with cross_embodiment = yes, / total rows |
| Handheld-gripper papers | 31 (15.3 % of rows) | rows with collection_method = handheld_gripper |
| ... of which robot-free | 26 (83.9 % of handheld papers) | handheld rows with robot_free_collection = yes, / handheld rows |
| Median stated demonstrations | 2,100 (over 27 papers) | median of non-empty num_demonstrations (mean of two middle values if even) |
| Papers by method | other_teleop 69, vr_ar_teleop 36, handheld_gripper 31, exoskeleton 21, glove_or_mocap 15, human_video 14, other 9, leader_follower 8 | rows grouped by collection_method |
| Papers by year | 2019: 2, 2020: 3, 2021: 1, 2022: 4, 2023: 5, 2024: 24, 2025: 70, 2026: 94 | rows grouped by year (2026 is partial, through October) |
| End-effectors | unspecified 108, dexterous_hand 56, parallel_gripper 18, other 11, both 10 | rows grouped by end_effector |

## What the dashboard shows (answers to the brief)

1. Teleoperation dominates: other_teleop 69 and vr_ar_teleop 36 papers; handheld grippers are third (31).
2. The area is very recent: 80.8 % of the papers are from 2025-2026 (24 in 2024, 70 in 2025, 94 in 2026 to October); handheld-gripper papers went from 5 in 2024 to 16 in 2026.
3. 41.4 % of systems collect without a robot, only 16.7 % release a dataset, 33.0 % address cross-embodiment.
4. Handheld grippers are robot-free far more often (83.9 %) than the field (41.4 %).
5. Dexterous hands are the most named end-effector (56); 108 abstracts do not say.
6. Only 27 papers state a size; median 2,100, range 3 to 1,200,000 (log scale in the chart).

## Verification

- All 7 headline tiles read from the rendered page equal `key_numbers.json`.
- Stacked chart 2026 segments read from the SVG (30/16/16/8/11/7/3/3 = 94) equal the Python counts.
- Table filters: method = handheld_gripper -> 31 rows; + year 2026 -> 16; title search 'UMI' -> 18; all equal Python.
- No console errors; no horizontal overflow at 375 px or 1280 px.

## How K2 Horizon built it

K2 (`IFM/K2-Horizon-375B-A23B`) wrote all of `dashboard.html`. My scripts inject the CSV rows into its placeholder
`const ROWS = /*__DATA__*/[]`; I tested each version and sent K2 a written report (`test_reports/`). I did not edit
the dashboard by hand.

| Version | Input | Effort | Latency | Tokens in / out | Result |
|---|---|---|---|---|---|
| d_v1 | brief | low | 7.13 s | 1,804 / 6,612 | All 7 tiles correct; black bars with unreadable labels; handheld share used the wrong denominator (12.8 % instead of 83.9 %); linear size axis clipped |
| d_v2 | d_v1 | low | 83.65 s | 8,422 / 10,886 | All fixed; chart text unreadable on phones; '1M' tick shown twice; 36,000 px page on phones |
| d_v3_failed_low_1 | d_v2 | low | 299.65 s | 8,774 / 40,000 | Failed: used the whole 40K-token budget, no HTML |
| d_v3 | d_v2 | low | 9.34 s | 8,774 / 13,794 | Phone layout fixed. Final |

4 calls, 99,066 tokens. Raw calls in `k2_runs/`.

## Limitations

- Labels are K2 Horizon's annotations of abstracts (relevance spot check 19/20). Some handheld devices for dexterous
  hands are labelled other_teleop (DexPort, DEX-PHD), so the handheld count is a lower bound.
- 2026 covers January to October only, so the 2026 bar understates the full year.
