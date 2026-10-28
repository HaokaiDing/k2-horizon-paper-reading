# Brief: "How are robot-manipulation demonstrations collected?" dashboard

**Audience.** Me and my lab: we build UMI-style (handheld gripper) data-collection systems and need a quick
picture of the field to position our work.

**Data.** `data.csv`, 203 arXiv papers (2019 to Oct 2026) that present or depend on a system for collecting human
demonstrations for robot manipulation. One row per paper. See `DATA_DICTIONARY.md`. 2026 is a partial year.

**Questions the dashboard must answer**
1. Which collection methods are most common? (count and share per `collection_method`)
2. How fast is the area growing, and which methods drive the growth? (papers per year, stacked by method)
3. How much of the field can collect data without a robot present? How often are datasets released? How often is
   cross-embodiment transfer addressed? (share of `yes` for `robot_free_collection`, `releases_dataset`,
   `cross_embodiment`)
4. Where do handheld-gripper systems stand: how many are there, and how many are robot-free?
5. Which end-effectors are targeted? (`end_effector` counts)
6. How large are the datasets that state a size? (count and median of `num_demonstrations`; list the largest)

**Key numbers to show as headline tiles:** total papers; share of papers from 2025 or later; % robot-free (yes);
% releasing a dataset (yes); % addressing cross-embodiment (yes); number of handheld-gripper papers and how many of
them are robot-free; median stated number of demonstrations (and how many papers state one).

**Also required:** a searchable/filterable table of all papers (title linking to arxiv.org/abs/<id>, year, method,
end-effector, robot-free, releases data, demos); a "How these numbers are calculated" section stating each key
number's formula in plain words; a note that labels were produced by K2 Horizon from abstracts (relevance spot
check 19/20) and that 2026 is a partial year.
