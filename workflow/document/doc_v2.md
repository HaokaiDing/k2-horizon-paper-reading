# Moving handheld-gripper demonstrations to other robot hands: where the field stands (October 2026)

## Summary

FastUMI released a large-scale real-world dataset of over 10,000 demonstration trajectories spanning 22 everyday tasks, 19 object categories, and 12 manipulation skills, with demonstrations lasting approximately 6–12 seconds [1]. The central obstacle to reusing such handheld-gripper data is the embodiment gap: UMI-style interfaces assume the robot wears the same fingers as the handheld gripper, and FastUMI does not relax that assumption but extends it to more robots by fitting plug-in fingertip attachments that cover over 90% of the grippers in Open X-Embodiment [1][2][3]. The literature offers several complementary routes—cross-embodiment data pooling, explicit retargeting between mismatched hands, and policy-level fixes—but each leaves part of the gap unaddressed [4][5][6][7][8][9][10][11][12][13]. Field statistics from 203 papers show a very recent and fast-growing area in which robot-free collection is common, dataset release is rare, and cross-embodiment work is still a minority [14]. For a newcomer, the most promising first steps are to clean and re-annotate handheld recordings, build a retargeting baseline for unsupported grippers, and evaluate transfer on mismatched end-effectors using cross-embodiment benchmarks.

## Why handheld-gripper data, and what FastUMI changed

Handheld-gripper collection separates the human teacher from the robot platform: UMI-style interfaces let a person demonstrate with a hand-held tool and replay those demonstrations directly on a robot [2]. FastUMI makes this practical at scale by making the interface hardware-independent and by open-sourcing a large dataset [1].

On hardware, FastUMI uses ISO-standard flange plates, plug-in fingertip attachments for five common grippers, and adjustable camera mounts that keep GoPro viewpoints consistent across platforms [1]. The five attachments were designed for commonly used grippers in open-source datasets such as Open X-Embodiment, covering over 90% of the grippers in those datasets [1][3]. Rather than retargeting demonstrations to a different end-effector, FastUMI makes the robot wear the same fingers as the handheld gripper.

On tracking, FastUMI replaces UMI's GoPro-based VIO pipeline with an off-the-shelf RealSense T265 module, eliminating complex calibration and coordinate transformations [1]. A caveat from the paper's own data: in the low-occlusion Pick Cup task T265 averages 10.5 mm error versus MINI's 15.2 mm, but in the occluded Open Container task T265 degrades to 17.7 mm while MINI improves to 11.2 mm [1].

The dataset contains over 10,000 real-world demonstration trajectories spanning 22 everyday tasks, 19 object categories, and 12 manipulation skills, with demonstrations lasting approximately 6–12 seconds [1]. Several results matter for transfer. Adding estimated depth to Diffusion Policy yields large gains on precision tasks: success rises from 53.33% to 80.00% on Pick Lid and from 20.00% to 93.33% on Open Ricecooker [1]. Policy performance scales with training data size: on Pick Cup, success rates increase from 20.00% with 200 demonstrations to 26.67% with 400 and 53.33% with 800 demonstrations [1]. A single fisheye GoPro at the end-effector achieves performance comparable to multi-view camera setups, e.g., 100.00% on Open Container for both fisheye first-person and D435i multi-view configurations [1].

## The embodiment gap: what breaks when the robot's end-effector differs from the handheld gripper

The embodiment gap is the mismatch between the end-effector used to collect demonstrations and the end-effector that executes them. UMI assumes the robot wears the same fingers as the handheld gripper, which is exactly the constraint that cross-end-effector transfer wants to relax [2]. FastUMI's answer is to make the robot wear the same fingers via fingertip attachments, but this only works for grippers covered by the five attachments; not all gripper types are yet supported, though the design can be readily adapted [1].

When the end-effector differs, several things break. First, shape and kinematic differences change grasp geometry and the relationship between commanded end-effector pose and actual contact points; Doshi et al. analyze these challenges specifically for hand-held grippers and offer insights into compensating for shape and kinematic differences [5]. Second, the action representation matters: Diffusion Policy's relative TCP poses decide how much of the gripper mismatch the policy sees, and the policy does not by itself handle a different embodiment [11]. Third, tracking and perception degrade: T265 is susceptible to severe close-range visual occlusion and low-light conditions, which reduce confidence and increase drift, requiring reinitialization when loop closure fails [1]. Fourth, mechanical details such as non-parallel gripper jaws introduce TCP displacement that FastUMI corrects with a dynamic error-compensation algorithm that shifts the commanded TCP along the gripper's local Z-axis before inverse kinematics [1]. Finally, FastUMI's limitations are relevant: it relies only on visual data, which is insufficient for tasks requiring precise force or tactile feedback such as handling fragile objects; it supports single-arm and dual-arm platforms but is not yet adapted to more complex morphologies such as mobile manipulators requiring whole-body control; and wired data transfer constrains portability and limits field applications [1].

## Approaches in the literature

### Universal Manipulation Interface (UMI) and cross-embodiment frameworks

- **UMI** defines the handheld-to-robot interface with relative end-effector trajectories, a wrist fisheye camera, and latency matching, letting handheld demos drive a robot directly; but it assumes the robot wears the same fingers as the handheld gripper, which is the constraint to relax [2].
- **Open X-Embodiment** pools data from many robot embodiments and reports that RT-X models trained on the mix can beat single-robot models, so cross-embodiment pooling can help; FastUMI sized its fingertip attachments to cover over 90% of the grippers in this dataset, making it the natural target set for transferred handheld data [3].
- **Human-to-robot imitation in the wild** learns robot policies from third-person videos of people with no handheld tool by mapping human motion to the robot; it is the far end of the embodiment gap and a useful contrast to handheld-gripper data where the gap is much smaller [4].

### Morphological gap and handheld-gripper specific studies

- **Doshi et al.** analyze the specific challenges introduced by hand-held grippers, offering insights into how to compensate for shape and kinematic differences when transferring data to robot end-effectors [5].
- **Sanches et al.** map human hand motion captured with wearable interfaces onto robot hands for dexterous tasks; this is an example of explicit retargeting between different end-effectors, a step UMI-style pipelines skip by matching grippers [6].
- **Dexcap** records human hand motion with mocap gloves and retargets it to a dexterous robot hand with inverse kinematics; it is a concrete retargeting pipeline between mismatched hands that a handheld-gripper pipeline could borrow [7].

### Large-scale demonstration datasets and teleoperation collection methods

- **RT-1** is a large robot-collected dataset of about 130k episodes, mostly one robot type; it also reports that adding data from a different robot (Kuka) can help. It is mainly a contrast case: data collected on the target robot itself, versus handheld data that must cross an embodiment gap [8].
- **VR teleoperation** collects demonstrations directly on the target robot, so there is no embodiment gap to bridge; it is the baseline that handheld collection trades against—cheaper and more scalable, but mismatched [9].
- **Grasping in the Wild** is an early handheld grabber with a camera, used to collect grasping demonstrations in the wild and train a closed-loop 6DoF grasping policy that runs on a robot arm; it is a direct ancestor of UMI-style collection, but transfer to differently shaped grippers is not its focus [10].

### Policy learning from demonstrations (diffusion, imitation, data quality)

- **Diffusion Policy** is the policy class that UMI and FastUMI train on handheld data; its action representation (relative TCP poses) decides how much of the gripper mismatch the policy sees, and it does not by itself handle a different embodiment [11].
- **Data Quality in Imitation Learning** analyzes how noise and bias in demonstration data affect downstream policies, guiding the cleaning and re-annotation of handheld-gripper recordings before cross-embodiment transfer [12].
- **Imitation learning: A survey** gives a general taxonomy of imitation learning and of how demonstrations are captured; it is background for choosing a learning method, with no specific treatment of handheld grippers [13].

## What the numbers say about the field

The field statistics come from a 203-paper dataset of demonstration-collection systems on arXiv from 2019 to October 2026 [14]. The area is very recent: 80.8% of the papers (164) are from 2025 or later, with year counts of 2 in 2019, 3 in 2020, 1 in 2021, 4 in 2022, 5 in 2023, 24 in 2024, 70 in 2025, and 94 in 2026 through October [14]. Teleoperation dominates: other_teleop has 69 papers and vr_ar_teleop has 36, while handheld grippers are third with 31 papers [14]. The full method breakdown is other_teleop 69, vr_ar_teleop 36, handheld_gripper 31, exoskeleton 21, glove_or_mocap 15, human_video 14, other 9, and leader_follower 8 [14].

Robot-free collection is common but not universal: 41.4% of systems (84 papers) collect without a robot [14]. Only 16.7% (34 papers) release a dataset, and 33.0% (67 papers) address cross-embodiment [14]. Handheld grippers are robot-free far more often than the field as a whole: 26 of the 31 handheld-gripper papers (83.9%) are robot-free, compared with 41.4% across all papers [14]. The number of handheld-gripper papers grew from 5 in 2024 to 16 in 2026 [14].

End-effector reporting is sparse: 108 abstracts do not specify an end-effector, while 56 name a dexterous hand, 18 a parallel gripper, 11 other, and 10 both [14]. Only 27 papers state a dataset size; the median is 2,100 demonstrations, with a range from 3 to 1,200,000 [14]. The caveats stated with these numbers are that 2026 is partial through October, only 27 papers state a size, and 108 abstracts do not say which end-effector was used [14]. In addition, the labels were produced by a language model from abstracts, with a relevance spot check of 19/20, and some handheld devices for dexterous hands are labelled other_teleop, so the handheld count of 31 is a lower bound [14].

## Open problems and what a newcomer should try first

1. **Start with data quality and re-annotation.** Data Quality in Imitation Learning shows that noise and bias in demonstrations affect downstream policies [12], and FastUMI's own tracking data show that T265 degrades under occlusion [1]. Before attempting cross-end-effector transfer, clean and re-annotate handheld recordings, especially for occluded or close-range segments.

2. **Build a retargeting baseline for unsupported grippers.** FastUMI's attachment approach covers over 90% of Open X-Embodiment grippers but not all gripper types [1][3]. Doshi et al., Sanches et al., and Dexcap provide concrete retargeting ideas for shape and kinematic differences [5][6][7]; a newcomer should implement one of these for a gripper outside FastUMI's five attachments and measure the drop relative to matched-gripper transfer.

3. **Evaluate on mismatched end-effectors with cross-embodiment benchmarks.** Open X-Embodiment shows that pooling data across embodiments can help [3], and RT-1 shows that adding data from a different robot can help [8], yet only 33.0% of papers in the field address cross-embodiment [14]. A newcomer should run a policy trained on FastUMI-style handheld data on a robot with a different gripper and report success rates per task.

4. **Address sensing and morphology limitations.** FastUMI is visual-only, which is insufficient for tasks requiring precise force or tactile feedback such as handling fragile objects; it is not yet adapted to mobile manipulators requiring whole-body control; and wired data transfer limits field applications [1]. A newcomer should test whether adding tactile or force sensing, or moving to a wireless setup, improves transfer on fragile-object or mobile-manipulation tasks.

5. **Use policy-level fixes as a first lever.** Diffusion Policy's action representation determines how much gripper mismatch the policy sees [11], and FastUMI shows that depth-enhanced Diffusion Policy and more training data can substantially improve success on precision tasks [1]. A newcomer should first try these algorithmic enhancements on a mismatched-gripper benchmark before building new hardware.

## References

1. Zhaxizhuoma et al. FastUMI: A Scalable and Hardware-Independent Universal Manipulation Interface with Dataset. 2025. arXiv:2409.19499 - https://arxiv.org/abs/2409.19499
2. Cheng Chi, Zhenjia Xu, Chuer Pan, Eric Cousineau, Benjamin Burchfiel, Siyuan Feng, Russ Tedrake, and Shuran Song. Universal manipulation interface: In-the-wild robot teaching without in-the-wild robots. 2024. arXiv:2402.10329 - https://arxiv.org/abs/2402.10329
3. Open X-Embodiment Collaboration (A. O'Neill, A. Rehman, A. Maddukuri, A. Gupta, A. Padalkar, et al.). Open X-Embodiment: Robotic Learning Datasets and RT-X Models. 2024. arXiv:2310.08864 - https://arxiv.org/abs/2310.08864
4. Shikhar Bahl, Abhinav Gupta, and Deepak Pathak. Human-to-robot imitation in the wild. 2022. arXiv:2207.09450 - https://arxiv.org/abs/2207.09450
5. Kiran Doshi, Yijiang Huang, and Stelian Coros. On hand-held grippers and the morphological gap in human manipulation demonstration. 2023. arXiv:2311.01832 - https://arxiv.org/abs/2311.01832
6. Felipe Sanches, Geng Gao, Nathan Elangovan, Ricardo V Godoy, Jayden Chapman, Ke Wang, Patrick Jarvis, and Minas Liarokapis. Scalable. intuitive human to robot skill transfer with wearable human machine interfaces: On complex, dexterous tasks. 2023. DOI:10.1109/iros55552.2023.10341661 - https://doi.org/10.1109/iros55552.2023.10341661
7. Chen Wang, Haochen Shi, Weizhuo Wang, Ruohan Zhang, Li Fei-Fei, and C Karen Liu. Dexcap: Scalable and portable mocap data collection system for dexterous manipulation. 2024. arXiv:2403.07788 - https://arxiv.org/abs/2403.07788
8. Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, et al. Rt-1: Robotics transformer for real-world control at scale. 2022. arXiv:2212.06817 - https://arxiv.org/abs/2212.06817
9. Tianhao Zhang, Zoe McCarthy, Owen Jow, Dennis Lee, Xi Chen, Ken Goldberg, and Pieter Abbeel. Deep imitation learning for complex manipulation tasks from virtual reality teleoperation. 2018. arXiv:1710.04615 - https://arxiv.org/abs/1710.04615
10. Shuran Song, Andy Zeng, Johnny Lee, and Thomas Funkhouser. Grasping in the Wild: Learning 6DoF Closed-Loop Grasping From Low-Cost Demonstrations. 2020. DOI:10.1109/lra.2020.3004787 - https://doi.org/10.1109/lra.2020.3004787
11. Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. 2023. arXiv:2303.04137 - https://arxiv.org/abs/2303.04137
12. Suneel Belkhale, Yuchen Cui, and Dorsa Sadigh. Data Quality in Imitation Learning. 2023. arXiv:2306.02437 - https://arxiv.org/abs/2306.02437
13. Ahmed Hussein, Mohamed Medhat Gaber, Eyad Elyan, and Chrisina Jayne. Imitation learning: A survey of learning methods. 2017. DOI:10.1145/3054912 - https://doi.org/10.1145/3054912
14. Survey dataset of 203 arXiv papers on demonstration-collection systems (2019 to October 2026), compiled for this review from arXiv metadata via DataCite (https://api.datacite.org); labels by K2 Horizon from abstracts.
