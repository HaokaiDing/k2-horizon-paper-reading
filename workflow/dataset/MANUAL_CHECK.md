# Manual check of K2's annotations

20 records drawn at random (`random.seed(20261028)`, IDs in `work/manual_sample_ids.json`) from all 295
annotated records, so papers K2 excluded were checked too. I read each title and abstract and compared K2's labels.

| # | arXiv | K2 relevant | My verdict | Notes |
|---|---|---|---|---|
| 1 | 2610.26169 | yes (exoskeleton) | correct | G1Exo isomorphic exoskeleton for demonstrations |
| 2 | 2310.16014 | yes (other_teleop, 2100) | correct | "2.1K demos" in abstract |
| 3 | 2508.14042 | no | correct | demonstrations generated in simulation |
| 4 | 2305.14584 | yes (vr_ar_teleop) | correct | VR demonstration platform |
| 5 | 2609.23755 | yes (human_video, 179,049) | correct | egocentric in-the-wild human data |
| 6 | 2610.12046 | yes (other_teleop) | correct | teleoperation + kinesthetic teaching |
| 7 | 2504.01301 | no | correct (borderline) | uses leader-follower data, but the contribution is the policy |
| 8 | 2510.20774 | yes (other_teleop) | correct | teleoperated pre-manipulation + generated trajectories |
| 9 | 1908.04692 | yes (vr_ar_teleop) | correct | HoloLens hand guidance for demonstrations |
| 10 | 2607.27784 | yes (other_teleop) | correct | kinesthetic arm guidance + webcam hand retargeting |
| 11 | 2509.14530 | yes (other_teleop) | correct (borderline) | system includes a teleoperation interface for data collection |
| 12 | 2509.03222 | no | **wrong** | compares teleoperation interfaces for data collection; should be relevant (vr_ar_teleop) |
| 13 | 2212.04708 | yes (other_teleop) | correct | policy-assisted teleoperation for data collection |
| 14 | 1309.2084 | no | correct | gesture recognition, not demonstration collection |
| 15 | 2606.14665 | yes (handheld_gripper) | correct | UMI-style robot-free interface |
| 16 | 2603.28542 | yes (glove_or_mocap) | correct | tactile glove for dexterous teleoperation |
| 17 | 2508.00097 | yes (vr_ar_teleop) | correct | XR teleoperation framework |
| 18 | 2509.02437 | yes (leader_follower, releases data) | correct | "open-sourced real-world manipulation data" |
| 19 | 2608.01834 | yes (vr_ar_teleop, 96) | correct | "96 successful demonstrations" |
| 20 | 2410.07554 | yes (other, releases data) | correct | force-motion capture device; data released |

**Result:** relevance correct in 19/20 (95 %). On the 16 sampled rows K2 marked relevant, `collection_method`,
`end_effector`, `releases_dataset` and `num_demonstrations` were all consistent with the abstract.
All 27 non-empty `num_demonstrations` values in the full file were also checked against the abstracts (27/27).

**Limitation.** Labels come from abstracts only; where an abstract is silent K2 answers `unclear`/`unspecified`
(e.g. `end_effector` is `unspecified` in 108 of 203 rows). K2's labels were left as produced, including the error
found in row 12, so the file reflects the model's annotation quality honestly; users who need higher precision
should re-check rows they rely on.
