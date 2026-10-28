# Data dictionary: demo_collection_systems.csv

203 rows, one per arXiv paper that presents (or depends on) a system for collecting human demonstrations for robot manipulation. Delivered in full (not a sample).

**Source.** Metadata of arXiv records registered with DataCite (client `arxiv.content`), fetched through the public DataCite REST API (https://api.datacite.org) on 2026-10-28. DataCite metadata is released under CC0. Abstracts were used only as input to the annotation and are not included (their licences vary). No author names or other personal data are included.

| Column | Type | Meaning | Origin |
|---|---|---|---|
| `arxiv_id` | string | arXiv identifier YYMM.NNNNN (no version) | DataCite DOI suffix |
| `doi` | string | DataCite DOI, always 10.48550/arxiv.<arxiv_id> | DataCite |
| `title` | string | Paper title (whitespace normalised) | DataCite titles |
| `year` | integer | Publication year on arXiv | DataCite publicationYear |
| `arxiv_subjects` | string | arXiv categories, '; '-separated (all include Robotics (cs.RO)) | DataCite subjects |
| `license` | string (SPDX id) or empty | Licence of the arXiv record; empty when the DataCite record has no rights entry | DataCite rightsList |
| `collection_method` | category | Main demonstration-collection method: handheld_gripper, glove_or_mocap, exoskeleton, vr_ar_teleop, leader_follower, other_teleop, human_video, other | K2 Horizon, from title + abstract |
| `end_effector` | category | parallel_gripper, dexterous_hand, both, other, unspecified | K2 Horizon |
| `robot_free_collection` | category | yes / no / unclear: can demonstrations be collected without a robot present | K2 Horizon |
| `cross_embodiment` | category | yes / no / unclear: does the work transfer data or policies across robots / end-effectors | K2 Horizon |
| `releases_dataset` | category | yes / no / unclear: does the abstract say a dataset is released | K2 Horizon |
| `num_demonstrations` | integer or empty | Number of demonstrations/trajectories/episodes when the abstract states one; empty otherwise | K2 Horizon, all 27 values checked against the abstract |
| `k2_rationale` | string | K2's one-line reason for its labels, in its own words (<= 25 words) | K2 Horizon |
