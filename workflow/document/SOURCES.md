# Source material

All sources below were produced and checked earlier in this project. Use only these sources and facts.

## Source A: FastUMI key takeaways (verified against the paper, arXiv:2409.19499)

# Key takeaways: FastUMI: A Scalable and Hardware-Independent Universal Manipulation Interface with Dataset

**Paper:** FastUMI: A Scalable and Hardware-Independent Universal Manipulation Interface with Dataset (Zhaxizhuoma et al., 2025) - arXiv:2409.19499 - https://arxiv.org/abs/2409.19499

Summary drafted by K2 Horizon (`IFM/K2-Horizon-375B-A23B`) from the full paper text in one prompt, then checked point by point against the paper. Every point has a verbatim quote from the paper, an automatic check, and my manual check of each number and claim.

## Findings

1. **FastUMI releases a large-scale real-world dataset of over 10,000 demonstration trajectories covering 22 everyday tasks, 19 object categories, and 12 manipulation skills, with demonstrations lasting approximately 6-12 seconds.**
   - Evidence (Abstract): "we have open-sourced a high-quality dataset of over 10,000 real-world demonstration trajectories spanning 22 everyday tasks, forming one of the most diverse UMI-like datasets to date."
   - Automatic check: quote verbatim; numbers found in paper 6/6
   - Manual check: All numbers match the dataset paragraph: 22 tasks, 19 object categories, 12 manipulation skills, 6-12 s demos (line 597); >10,000 trajectories (abstract).

2. **Pose tracking accuracy differs by sensor and occlusion level: in the low-occlusion Pick Cup task T265 averages 10.5 mm error versus MINI's 15.2 mm, but in the occluded Open Container task T265 degrades to 17.7 mm while MINI improves to 11.2 mm.**
   - Evidence (VI-A Data Quality): "In the "Pick Cup" scenario, where occlusion is minimal, T265 achieves an average positioning error of 10.5 mm, while MINI's error averages 15.2 mm."
   - Automatic check: quote verbatim; numbers found in paper 6/6
   - Manual check: Matches Table I text: 10.5 vs 15.2 mm on Pick Cup, 17.7 vs 11.2 mm on Open Container (line 804).

3. **Adding estimated depth to Diffusion Policy yields large gains on precision tasks: success rises from 53.33% to 80.00% on Pick Lid and from 20.00% to 93.33% on Open Ricecooker.**
   - Evidence (VI-C Algorithmic Enhancements): "success rates increase by 26.67% on "Pick Lid" and 73.33% on "Open Ricecooker.""
   - Automatic check: quote verbatim; numbers found in paper 4/4
   - Manual check: Matches Table III: Pick Lid 53.33 -> 80.00 %, Open Ricecooker 20.00 -> 93.33 %. Note: each rate is over 15 trials and only these two tasks were tested.

4. **ACT variants improve over baseline ACT: on Pick Bear, Smooth-ACT reaches 60.00% and PoseACT (Absolute) reaches 80.00% versus 20.00% for original ACT; on Sweep Trash, PoseACT (Relative) reaches 60.00% versus 6.67% baseline.**
   - Evidence (VI-C Algorithmic Enhancements): "Pick Bear 20.00% 60.00% 80.00% 73.33%"
   - Automatic check: quote verbatim; numbers found in paper 5/5
   - Manual check: Matches Table IV (ACT / Smooth-ACT / PoseACT-Abs / PoseACT-Rel): Pick Bear 20.00 / 60.00 / 80.00 / 73.33 %, Sweep Trash 6.67 / 26.67 / 53.33 / 60.00 %.

5. **Policy performance scales with training data size: on the Pick Cup task, success rates increase from 20.00% with 200 demonstrations to 26.67% with 400 and 53.33% with 800 demonstrations.**
   - Evidence (VI-D Additional Factors): "Pick Cup 20.00% 26.67% 53.33%"
   - Automatic check: quote verbatim; numbers found in paper 6/6
   - Manual check: Matches Table VI: 20.00 / 26.67 / 53.33 % for 200 / 400 / 800 demos.

6. **A single fisheye GoPro at the end-effector achieves performance comparable to multi-view camera setups, e.g., 100.00% on Open Container for both fisheye first-person and D435i multi-view configurations.**
   - Evidence (VI-D Additional Factors): "a fisheye lens at the end-effector achieves performance comparable to multi-view setups, potentially because its wide field of view captures richer contextual information for decision-making."
   - Automatic check: quote verbatim; numbers found in paper 2/2
   - Manual check: Matches Table V: Open Container 100.00 % for D435i first+third person and for the GoPro fisheye. Same table: the GoPro fisheye gets 80.00 % vs 86.67 % for the multi-view setup on Pick Bear, so 'comparable' rather than equal.

## Methods

1. **Hardware decoupling via standardized, modular components: ISO-standard flange plates, plug-in fingertip attachments for five common grippers covering over 90% of grippers in open-source datasets, and adjustable camera mounts maintain consistent GoPro viewpoints across platforms.**
   - Evidence (II-C Robot-Mounted Device Design): "we design five customized fingertip attachments (e.g., the xArm gripper and Robotiq 2f-85) based on commonly used grippers in open-source datasets such as Open X-Embodiment, covering over 90% of the grippers in these datasets."
   - Automatic check: quote verbatim except dropped citation marker; numbers found in paper 1/1
   - Manual check: Matches section II-C (ISO-standard-compatible mounts, five fingertip attachments, >90 % of Open X-Embodiment grippers).

2. **The GoPro-based VIO pipeline is replaced with an off-the-shelf RealSense T265 tracking module, eliminating complex calibration and coordinate transformations while maintaining pose accuracy under partial occlusion.**
   - Evidence (I Introduction): "we replace the UMI's VIO-based localization with a RealSense T265 module, which integrates both visual and inertial data to provide more stable tracking in partially occluded environments."
   - Automatic check: quote verbatim; numbers found in paper 1/1
   - Manual check: Matches the introduction. Caveat: 'maintaining pose accuracy under partial occlusion' is the authors' framing; their own Table I shows T265 error rising to 17.7 mm under partial occlusion, worse than MINI (11.2 mm).

3. **Multi-sensor synchronization is achieved by sub-sampling the 200 Hz T265 stream and 60 fps GoPro stream at their greatest common frequency of 20 Hz, pairing each retained frame with the temporally nearest pose for sub-millisecond alignment.**
   - Evidence (III-A Raw Data Acquisition): "We then sub-sample both streams at 20 Hz—identified as the greatest common frequency between 200 Hz and 60 Hz—by retaining one in every three camera frames and pairing each retained frame with the temporally nearest T265 pose."
   - Automatic check: quote verbatim; numbers found in paper 4/4
   - Manual check: Matches section III-A: 200 Hz / 60 Hz streams, 20 Hz common rate, nearest-pose pairing, sub-millisecond offsets (lines 333-334).

4. **T265 drift is managed through reinitialization at a predefined reference pose and loop closure using a visually distinct blue 3D-printed groove on the table as a reference region.**
   - Evidence (III-A Raw Data Acquisition): "Another strategy leverages a visually distinct reference region—a blue 3D-printed groove on the table (Fig. 5 Left)—to facilitate loop closure."
   - Automatic check: quote verbatim; numbers found in paper 2/2
   - Manual check: Matches section III-A: reinitialization at a marked reference pose and loop closure on a blue 3D-printed groove (lines 339-345).

5. **Smooth-ACT adds a GRU layer on top of the Transformer decoder to enforce local temporal continuity of joint actions, while PoseACT replaces absolute joint prediction with end-effector TCP pose prediction (absolute or relative) mapped back to joints via inverse kinematics.**
   - Evidence (IV-C Enhanced ACT for First-Person Perspectives): "we introduce Smooth-ACT, which enhances action continuity by incorporating a Gated Recurrent Unit (GRU) layer on top of the Transformer decoder"
   - Automatic check: quote verbatim; numbers found in paper 0/0
   - Manual check: Matches section IV-C: GRU on top of the Transformer decoder (Smooth-ACT); PoseACT predicts TCP pose, converted to joints by IK.

6. **Depth-Enhanced DP generates depth maps offline with Depth Anything V2 on cropped 448x448 images, encodes them as pseudo-color three-channel maps alongside RGB in a shared CLIP ViT encoder, and runs the large model at 20 Hz on an RTX 4090 during inference.**
   - Evidence (IV-D Depth-Enhanced Diffusion Policy): "we implement Depth Anything V2 with its large pre-trained model, achieving an inference frequency of 20 Hz on an RTX 4090 GPU."
   - Automatic check: quote verbatim except dropped citation marker; numbers found in paper 5/5
   - Manual check: Matches section IV-D: 448x448 crops, three-channel pseudo-colour depth, shared ViT-B/16 CLIP encoder, 20 Hz on an RTX 4090 (lines 540-545).

7. **A dynamic error-compensation algorithm corrects TCP displacement from non-parallel gripper jaws by computing a width-dependent compensation distance and shifting the commanded TCP along its local Z-axis before inverse kinematics.**
   - Evidence (IV-E Dynamic Error-Compensation Algorithm): "we propose a dynamic error-compensation algorithm that adjusts the commanded TCP in real time."
   - Automatic check: quote verbatim; numbers found in paper 0/0
   - Manual check: Matches section IV-E: width-dependent compensation distance d(i), TCP shifted along the gripper's local Z axis.

## Limitations

1. **FastUMI relies only on visual data, which is insufficient for tasks requiring precise force or tactile feedback such as handling fragile objects; integrating tactile or force sensors is left to future work.**
   - Evidence (VII Limitations): "FastUMI currently relies on visual data, which may prove insufficient for tasks requiring precise force or tactile feedback—such as handling fragile objects."
   - Automatic check: quote verbatim; numbers found in paper 0/0
   - Manual check: Stated by the authors in section VII (limited sensing modalities).

2. **The system supports single-arm and dual-arm platforms but is not yet adapted to more complex morphologies such as mobile manipulators requiring whole-body control.**
   - Evidence (VII Limitations): "Although FastUMI accommodates single-arm or dual-arm platforms, it is not yet adapted for more complex morphologies, including mobile manipulators requiring whole-body control."
   - Automatic check: quote verbatim; numbers found in paper 0/0
   - Manual check: Stated by the authors in section VII.

3. **Wired data transfer constrains portability and limits field applications where mobility or standalone operation is needed; a wireless solution is identified as future work.**
   - Evidence (VII Limitations): "Reliance on wired connections constrains portability and limits field applications where mobility or standalone operation is pivotal."
   - Automatic check: quote verbatim; numbers found in paper 0/0
   - Manual check: Stated by the authors in section VII (line 967 names a wireless solution as future work).

4. **Not all gripper types are supported by the fingertip attachments, though the design can be readily adapted as needed.**
   - Evidence (II-C Robot-Mounted Device Design): "Although not all gripper types are yet supported, our design can be readily adapted as needed."
   - Automatic check: quote verbatim; numbers found in paper 0/0
   - Manual check: Stated by the authors in section II-C (line 259).

5. **T265 tracking is susceptible to severe close-range visual occlusion and low-light conditions, which reduce confidence levels and increase drift, requiring reinitialization when loop closure fails.**
   - Evidence (VI-A Data Quality): "T265 is particularly susceptible to severe visual obstruction at close range."
   - Automatic check: quote verbatim; numbers found in paper 1/1
   - Manual check: Stated by the authors: close-range occlusion (section VI-A) and low light (line 355); reinitialization when loop closure fails (line 345).

## How it was checked

- `verify.py` searches the paper text for every evidence quote: 18/18 found (16/18 strictly verbatim; two dropped `[30]`/`[43]` citation markers).
- Every number in every point (43 in total) was searched for in the paper text: all found.
- I then read each point against its section/table (manual check lines above). No point was wrong; two needed a caveat (findings 6, methods 2).
- Raw model output: `k2_output_1_takeaways.json`. Code: `code/`. Run took 39 s, 13,015 input / 2,686 output tokens.


## Source B: Reading list on cross-end-effector transfer of handheld-gripper data (12 sources, every ID checked)

# Reading list: transferring handheld-gripper demonstrations across end-effectors

**Research question:** How can manipulation demonstrations collected with a handheld, UMI-style gripper be transferred to robots whose end-effectors differ from the data-collection gripper?

**Why I care:** I work on UMI-style data collection; today handheld data only transfers to robots that wear the same fingers as the handheld gripper.

**How this list was made:** K2 Horizon (`IFM/K2-Horizon-375B-A23B`) chose and grouped 12 sources by theme from the reference list of FastUMI (https://arxiv.org/abs/2409.19499). Every source was then checked: existence and identifier against DataCite (arXiv DOIs) / Crossref, and every 'why it matters' note was read and corrected by me where K2 overstated the connection (10 of 12 notes edited; see VERIFICATION.md).

## Universal Manipulation Interface (UMI) and cross‑embodiment frameworks

1. **Universal manipulation interface: In-the-wild robot teaching without in-the-wild robots**
   - Authors: Cheng Chi, Zhenjia Xu, Chuer Pan, Eric Cousineau, Benjamin Burchfiel, Siyuan Feng, Russ Tedrake, and Shuran Song
   - Year: 2024
   - ID: arXiv:2402.10329 - https://arxiv.org/abs/2402.10329
   - Why it matters: Defines the handheld-to-robot interface my question starts from: relative end-effector trajectories, a wrist fisheye camera and latency matching let handheld demos drive a robot directly. But UMI assumes the robot wears the same fingers as the handheld gripper, which is exactly the constraint my question wants to relax.

2. **Open X-Embodiment: Robotic Learning Datasets and RT-X Models**
   - Authors: Open X-Embodiment Collaboration (A. O'Neill, A. Rehman, A. Maddukuri, A. Gupta, A. Padalkar, et al.)
   - Year: 2024
   - ID: arXiv:2310.08864 - https://arxiv.org/abs/2310.08864
   - Why it matters: Pools data from many robot embodiments and reports that RT-X models trained on the mix can beat single-robot models, so cross-embodiment pooling can help. FastUMI sized its fingertip attachments to cover >90 % of the grippers in this dataset, making it the natural target set for transferred handheld data.

3. **Human-to-robot imitation in the wild**
   - Authors: Shikhar Bahl, Abhinav Gupta, and Deepak Pathak
   - Year: 2022
   - ID: arXiv:2207.09450 - https://arxiv.org/abs/2207.09450
   - Why it matters: Learns robot policies from third-person videos of people (no handheld tool) by mapping human motion to the robot; the far end of the embodiment gap, useful as a contrast to handheld-gripper data where the gap is much smaller.

## Morphological gap and handheld‑gripper specific studies

4. **On hand-held grippers and the morphological gap in human manipulation demonstration**
   - Authors: Kiran Doshi, Yijiang Huang, and Stelian Coros
   - Year: 2023
   - ID: arXiv:2311.01832 - https://arxiv.org/abs/2311.01832
   - Why it matters: Analyzes the specific challenges introduced by hand‑held grippers, offering insights into how to compensate for shape and kinematic differences when transferring data to robot end‑effectors.

5. **Scalable. intuitive human to robot skill transfer with wearable human machine interfaces: On complex, dexterous tasks**
   - Authors: Felipe Sanches, Geng Gao, Nathan Elangovan, Ricardo V Godoy, Jayden Chapman, Ke Wang, Patrick Jarvis, and Minas Liarokapis
   - Year: 2023
   - ID: DOI:10.1109/iros55552.2023.10341661 - https://doi.org/10.1109/iros55552.2023.10341661
   - Why it matters: Maps human hand motion captured with wearable interfaces onto robot hands for dexterous tasks; an example of explicit retargeting between different end-effectors, a step UMI-style pipelines skip by matching grippers.

6. **Dexcap: Scalable and portable mocap data collection system for dexterous manipulation**
   - Authors: Chen Wang, Haochen Shi, Weizhuo Wang, Ruohan Zhang, Li Fei-Fei, and C Karen Liu
   - Year: 2024
   - ID: arXiv:2403.07788 - https://arxiv.org/abs/2403.07788
   - Why it matters: Records human hand motion with mocap gloves and retargets it to a dexterous robot hand with inverse kinematics; a concrete retargeting pipeline between mismatched hands that a handheld-gripper pipeline could borrow.

## Large‑scale demonstration datasets and teleoperation collection methods

7. **Rt-1: Robotics transformer for real-world control at scale**
   - Authors: Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, et al
   - Year: 2022
   - ID: arXiv:2212.06817 - https://arxiv.org/abs/2212.06817
   - Why it matters: Large robot-collected dataset (about 130k episodes, mostly one robot type); it also reports that adding data from a different robot (Kuka) can help. Mainly a contrast case: data collected on the target robot itself, versus handheld data that must cross an embodiment gap.

8. **Deep imitation learning for complex manipulation tasks from virtual reality teleoperation**
   - Authors: Tianhao Zhang, Zoe McCarthy, Owen Jow, Dennis Lee, Xi Chen, Ken Goldberg, and Pieter Abbeel
   - Year: 2018
   - ID: arXiv:1710.04615 - https://arxiv.org/abs/1710.04615
   - Why it matters: VR teleoperation collects demonstrations directly on the target robot, so there is no embodiment gap to bridge; it is the baseline that handheld collection trades against (cheaper and more scalable, but mismatched).

9. **Grasping in the Wild: Learning 6DoF Closed-Loop Grasping From Low-Cost Demonstrations**
   - Authors: Shuran Song, Andy Zeng, Johnny Lee, and Thomas Funkhouser
   - Year: 2020
   - ID: DOI:10.1109/lra.2020.3004787 - https://doi.org/10.1109/lra.2020.3004787
   - Why it matters: An early handheld grabber with a camera, used to collect grasping demonstrations in the wild and train a closed-loop 6DoF grasping policy that runs on a robot arm; a direct ancestor of UMI-style collection. Transfer to differently shaped grippers is not its focus.

## Policy learning from demonstrations (diffusion, imitation, data quality)

10. **Diffusion policy: Visuomotor policy learning via action diffusion**
   - Authors: Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song
   - Year: 2023
   - ID: arXiv:2303.04137 - https://arxiv.org/abs/2303.04137
   - Why it matters: The policy class that UMI and FastUMI train on handheld data; its action representation (relative TCP poses) decides how much of the gripper mismatch the policy sees. It does not by itself handle a different embodiment.

11. **Data Quality in Imitation Learning**
   - Authors: Suneel Belkhale, Yuchen Cui, and Dorsa Sadigh
   - Year: 2023
   - ID: arXiv:2306.02437 - https://arxiv.org/abs/2306.02437
   - Why it matters: Analyzes how noise and bias in demonstration data affect downstream policies, guiding the cleaning and re‑annotation of handheld‑gripper recordings before cross‑embodiment transfer.

12. **Imitation learning: A survey of learning methods**
   - Authors: Ahmed Hussein, Mohamed Medhat Gaber, Eyad Elyan, and Chrisina Jayne
   - Year: 2017
   - ID: DOI:10.1145/3054912 - https://doi.org/10.1145/3054912
   - Why it matters: General taxonomy of imitation learning (behaviour cloning, inverse RL, etc.) and of how demonstrations are captured; background for choosing a learning method, with no specific treatment of handheld grippers.


## Source C: Field statistics from a 203-paper dataset of demonstration-collection systems (arXiv, 2019 to Oct 2026)

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

