"""Build the submission folders for the two Research quests from the verified runs."""
import json
import re
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUNS, DATA = HERE / "runs", HERE / "data"
OUT = HERE.parent / "submission"
PAPER = "FastUMI: A Scalable and Hardware-Independent Universal Manipulation Interface with Dataset"
PAPER_LINK = "https://arxiv.org/abs/2409.19499"
CODE = ["k2.py", "extract_text.py", "run_workflow.py", "verify.py", "build_packages.py"]

# ---------------------------------------------------------------- takeaways
# My manual check of each point against the paper (line numbers refer to data/paper_body.txt).
TAKEAWAY_CHECKS = {
    ("findings", 0): "All numbers match the dataset paragraph: 22 tasks, 19 object categories, 12 manipulation skills, 6-12 s demos (line 597); >10,000 trajectories (abstract).",
    ("findings", 1): "Matches Table I text: 10.5 vs 15.2 mm on Pick Cup, 17.7 vs 11.2 mm on Open Container (line 804).",
    ("findings", 2): "Matches Table III: Pick Lid 53.33 -> 80.00 %, Open Ricecooker 20.00 -> 93.33 %. Note: each rate is over 15 trials and only these two tasks were tested.",
    ("findings", 3): "Matches Table IV (ACT / Smooth-ACT / PoseACT-Abs / PoseACT-Rel): Pick Bear 20.00 / 60.00 / 80.00 / 73.33 %, Sweep Trash 6.67 / 26.67 / 53.33 / 60.00 %.",
    ("findings", 4): "Matches Table VI: 20.00 / 26.67 / 53.33 % for 200 / 400 / 800 demos.",
    ("findings", 5): "Matches Table V: Open Container 100.00 % for D435i first+third person and for the GoPro fisheye. Same table: the GoPro fisheye gets 80.00 % vs 86.67 % for the multi-view setup on Pick Bear, so 'comparable' rather than equal.",
    ("methods", 0): "Matches section II-C (ISO-standard-compatible mounts, five fingertip attachments, >90 % of Open X-Embodiment grippers).",
    ("methods", 1): "Matches the introduction. Caveat: 'maintaining pose accuracy under partial occlusion' is the authors' framing; their own Table I shows T265 error rising to 17.7 mm under partial occlusion, worse than MINI (11.2 mm).",
    ("methods", 2): "Matches section III-A: 200 Hz / 60 Hz streams, 20 Hz common rate, nearest-pose pairing, sub-millisecond offsets (lines 333-334).",
    ("methods", 3): "Matches section III-A: reinitialization at a marked reference pose and loop closure on a blue 3D-printed groove (lines 339-345).",
    ("methods", 4): "Matches section IV-C: GRU on top of the Transformer decoder (Smooth-ACT); PoseACT predicts TCP pose, converted to joints by IK.",
    ("methods", 5): "Matches section IV-D: 448x448 crops, three-channel pseudo-colour depth, shared ViT-B/16 CLIP encoder, 20 Hz on an RTX 4090 (lines 540-545).",
    ("methods", 6): "Matches section IV-E: width-dependent compensation distance d(i), TCP shifted along the gripper's local Z axis.",
    ("limitations", 0): "Stated by the authors in section VII (limited sensing modalities).",
    ("limitations", 1): "Stated by the authors in section VII.",
    ("limitations", 2): "Stated by the authors in section VII (line 967 names a wireless solution as future work).",
    ("limitations", 3): "Stated by the authors in section II-C (line 259).",
    ("limitations", 4): "Stated by the authors: close-range occlusion (section VI-A) and low light (line 355); reinitialization when loop closure fails (line 345).",
}


def build_takeaways():
    d = OUT / "get-the-key-takeaways"
    shutil.rmtree(d, ignore_errors=True)
    (d / "code").mkdir(parents=True)
    rec = json.loads((RUNS / "1_takeaways.json").read_text())
    ver = {(r["kind"], r["point"]): r for r in
           json.loads((RUNS / "3_verification.json").read_text())["1_takeaways_quotes"]["rows"]}
    body = (DATA / "paper_body.txt").read_text().replace(",", "")

    lines = [f"# Key takeaways: {PAPER}", "",
             f"**Paper:** {PAPER} (Zhaxizhuoma et al., 2025) - arXiv:2409.19499 - {PAPER_LINK}", "",
             "Summary drafted by K2 Horizon (`IFM/K2-Horizon-375B-A23B`) from the full paper text in one prompt, "
             "then checked point by point against the paper. Every point has a verbatim quote from the paper, "
             "an automatic check, and my manual check of each number and claim.", ""]
    total_nums = 0
    for kind, heading in (("findings", "Findings"), ("methods", "Methods"), ("limitations", "Limitations")):
        lines += [f"## {heading}", ""]
        for i, item in enumerate(rec["parsed"][kind], 1):
            v = ver[(kind, item["point"])]
            nums = re.findall(r"\d[\d,]*(?:\.\d+)?", item["point"])
            found = [n for n in nums if n.replace(",", "") in body]
            total_nums += len(nums)
            quote_status = ("verbatim" if v["verbatim"] else
                            "verbatim except dropped citation marker" if v["verbatim_ignoring_citation_markers"]
                            else "NOT FOUND")
            lines += [f"{i}. **{item['point']}**",
                      f"   - Evidence ({item['section']}): \"{item['evidence_quote']}\"",
                      f"   - Automatic check: quote {quote_status}; numbers found in paper {len(found)}/{len(nums)}",
                      f"   - Manual check: {TAKEAWAY_CHECKS[(kind, i - 1)]}", ""]
    lines += ["## How it was checked", "",
              "- `verify.py` searches the paper text for every evidence quote: 18/18 found "
              "(16/18 strictly verbatim; two dropped `[30]`/`[43]` citation markers).",
              f"- Every number in every point ({total_nums} in total) was searched for in the paper text: all found.",
              "- I then read each point against its section/table (manual check lines above). No point was wrong; "
              "two needed a caveat (findings 6, methods 2).",
              "- Raw model output: `k2_output_1_takeaways.json`. Code: `code/`. "
              "Run took 39 s, 13,015 input / 2,686 output tokens.", ""]
    (d / "SUMMARY.md").write_text("\n".join(lines))
    shutil.copy(RUNS / "1_takeaways.json", d / "k2_output_1_takeaways.json")
    for c in CODE:
        shutil.copy(HERE / c, d / "code" / c)
    (d / "PAPER_LINK.txt").write_text(f"{PAPER}\n{PAPER_LINK}\nhttps://arxiv.org/pdf/2409.19499\n")
    return d


# ---------------------------------------------------------------- related work
QUESTION = ("How can manipulation demonstrations collected with a handheld, UMI-style gripper be "
            "transferred to robots whose end-effectors differ from the data-collection gripper?")

# Identifiers for entries the verifier could not resolve automatically (checked by hand).
MANUAL_IDS = {30: ("arXiv", "2310.08864"), 22: ("DOI", "10.1145/3054912")}

# My reviewed note per reference number. "kept" = K2's note used as is.
NOTES = {
    10: ("edited", "Defines the handheld-to-robot interface my question starts from: relative end-effector trajectories, a wrist fisheye camera and latency matching let handheld demos drive a robot directly. But UMI assumes the robot wears the same fingers as the handheld gripper, which is exactly the constraint my question wants to relax.",
         "K2 said UMI 'abstracts away the specific gripper geometry' - it does not; it matches the geometry."),
    30: ("edited", "Pools data from many robot embodiments and reports that RT-X models trained on the mix can beat single-robot models, so cross-embodiment pooling can help. FastUMI sized its fingertip attachments to cover >90 % of the grippers in this dataset, making it the natural target set for transferred handheld data.",
         "Added the FastUMI link and toned down 'policies trained on one embodiment can be transferred'."),
    3: ("edited", "Learns robot policies from third-person videos of people (no handheld tool) by mapping human motion to the robot; the far end of the embodiment gap, useful as a contrast to handheld-gripper data where the gap is much smaller.",
        "K2 said demonstrations included 'handheld tools'; they do not."),
    14: ("kept", None, None),
    33: ("edited", "Maps human hand motion captured with wearable interfaces onto robot hands for dexterous tasks; an example of explicit retargeting between different end-effectors, a step UMI-style pipelines skip by matching grippers.",
         "K2 framed it as converting 'handheld-gripper demonstrations'; it uses wearable interfaces, not a handheld gripper."),
    41: ("edited", "Records human hand motion with mocap gloves and retargets it to a dexterous robot hand with inverse kinematics; a concrete retargeting pipeline between mismatched hands that a handheld-gripper pipeline could borrow.",
         "K2's 'embodiment-agnostic features' is not something the paper claims."),
    5: ("edited", "Large robot-collected dataset (about 130k episodes, mostly one robot type); it also reports that adding data from a different robot (Kuka) can help. Mainly a contrast case: data collected on the target robot itself, versus handheld data that must cross an embodiment gap.",
        "K2 said it generalizes 'across robot platforms'; RT-1 is mostly single-platform."),
    48: ("edited", "VR teleoperation collects demonstrations directly on the target robot, so there is no embodiment gap to bridge; it is the baseline that handheld collection trades against (cheaper and more scalable, but mismatched).",
         "K2 said the data 'can be re-targeted to different robot morphologies'; the paper does not do this."),
    36: ("edited", "An early handheld grabber with a camera, used to collect grasping demonstrations in the wild and train a closed-loop 6DoF grasping policy that runs on a robot arm; a direct ancestor of UMI-style collection. Transfer to differently shaped grippers is not its focus.",
         "K2 said policies 'transfer to varied robot grippers'; overstated."),
    9: ("edited", "The policy class that UMI and FastUMI train on handheld data; its action representation (relative TCP poses) decides how much of the gripper mismatch the policy sees. It does not by itself handle a different embodiment.",
        "K2 said it can 'ingest demonstrations from any embodiment'; overstated."),
    4: ("kept", None, None),
    22: ("edited", "General taxonomy of imitation learning (behaviour cloning, inverse RL, etc.) and of how demonstrations are captured; background for choosing a learning method, with no specific treatment of handheld grippers.",
         "K2 said the methods are 'robust to embodiment mismatches'; the survey makes no such claim."),
}


def ident(p, vrow):
    if p.get("arxiv_id"):
        return f"arXiv:{p['arxiv_id']} - https://arxiv.org/abs/{p['arxiv_id']}"
    if p["ref_number"] in MANUAL_IDS:
        kind, val = MANUAL_IDS[p["ref_number"]]
        return (f"arXiv:{val} - https://arxiv.org/abs/{val}" if kind == "arXiv"
                else f"DOI:{val} - https://doi.org/{val}")
    fid = vrow.get("found_doi") or vrow.get("found_id")
    if fid and "arxiv." in fid.lower():
        aid = fid.lower().split("arxiv.")[1]
        return f"arXiv:{aid} - https://arxiv.org/abs/{aid}"
    return f"DOI:{fid} - https://doi.org/{fid}"


def build_related():
    d = OUT / "find-the-related-work"
    shutil.rmtree(d, ignore_errors=True)
    (d / "code").mkdir(parents=True)
    rec = json.loads((RUNS / "2b_related_refs.json").read_text())["parsed"]
    ver = json.loads((RUNS / "3_verification.json").read_text())
    vrows = {r["title"]: r for r in ver["2b_related_refs"]["rows"]}

    lines = ["# Reading list: transferring handheld-gripper demonstrations across end-effectors", "",
             f"**Research question:** {QUESTION}", "",
             "**Why I care:** I work on UMI-style data collection; today handheld data only transfers to robots that "
             "wear the same fingers as the handheld gripper.", "",
             "**How this list was made:** K2 Horizon (`IFM/K2-Horizon-375B-A23B`) chose and grouped 12 sources by theme "
             f"from the reference list of FastUMI ({PAPER_LINK}). Every source was then checked: existence and "
             "identifier against DataCite (arXiv DOIs) / Crossref, and every 'why it matters' note was read and "
             "corrected by me where K2 overstated the connection (10 of 12 notes edited; see VERIFICATION.md).", ""]
    n = 0
    for theme in rec["themes"]:
        lines += [f"## {theme['theme']}", ""]
        for p in theme["papers"]:
            n += 1
            status, note, _ = NOTES[p["ref_number"]]
            note = note or p["why_it_matters"]
            authors = p["authors"].strip().rstrip(".")
            if p["ref_number"] == 30:
                authors = "Open X-Embodiment Collaboration (A. O'Neill, A. Rehman, A. Maddukuri, A. Gupta, A. Padalkar, et al.)"
                title = "Open X-Embodiment: Robotic Learning Datasets and RT-X Models"
            else:
                title = p["title"].rstrip(".")
            lines += [f"{n}. **{title}**",
                      f"   - Authors: {authors}",
                      f"   - Year: {p['year']}",
                      f"   - ID: {ident(p, vrows[p['title']])}",
                      f"   - Why it matters: {note}", ""]
    (d / "READING_LIST.md").write_text("\n".join(lines))

    v = ["# Verification of every source", "",
         "| # | Source (FastUMI ref) | Exists? | How checked | Note |", "|---|---|---|---|---|"]
    n = 0
    for theme in rec["themes"]:
        for p in theme["papers"]:
            n += 1
            r = vrows[p["title"]]
            how = {"verified_id": "arXiv ID resolves to the same title (DataCite)",
                   "found_by_title": "title matched in DataCite/Crossref",
                   "not_found": "checked by hand (entry title was messy)"}[r["status"]]
            status, _, why = NOTES[p["ref_number"]]
            v.append(f"| {n} | {p['title'][:60].rstrip('.')} [{p['ref_number']}] | yes | {how} | "
                     f"{'note kept' if status == 'kept' else 'note edited: ' + why} |")
    free = ver["2a_related_free"]
    v += ["", "## What did not work: asking K2 without the reference list", "",
          f"Before grounding K2 in the reference list, I asked the same question with no sources (run "
          f"`k2_output_2a_related_free.json`). K2 returned {free['n']} confident entries; "
          f"**{free['counts'].get('not_found', 0)}/{free['n']} could not be found** in DataCite or Crossref. "
          "Four came with arXiv IDs, and all four IDs belong to unrelated physics/maths papers:", ""]
    for r in free["rows"]:
        if r.get("claimed_arxiv_id"):
            v.append(f"- \"{r['title']}\" -> arXiv:{r['claimed_arxiv_id']} is actually \"{r['arxiv_title_at_id']}\"")
    v += ["", "None of those entries is in the reading list. The list above uses only the grounded run "
          "(`k2_output_2b_related_refs.json`), and every item in it was checked.", ""]
    (d / "VERIFICATION.md").write_text("\n".join(v))
    for s in ("2b_related_refs", "2a_related_free"):
        shutil.copy(RUNS / f"{s}.json", d / f"k2_output_{s}.json")
    shutil.copy(RUNS / "3_verification.json", d / "verification_results.json")
    for c in CODE:
        shutil.copy(HERE / c, d / "code" / c)
    return d


# ---------------------------------------------------------------- citation audit
# My review of K2's verdict per reference: (final status, replacement quote or None, my note).
CITATION_REVIEW = {
    3: ("supported", None, "Agree. The quote is contiguous in the paper; pdftotext split it with the Fig. 2 caption, so the automatic check missed it."),
    5: ("supported", None, "Agree."),
    6: ("incorrect", None, "Agree. Reward sketching is an annotation interface for batch RL, not a sensor-enhanced data-collection interface."),
    8: ("incorrect", None, "Agree, for one of two uses: ARCap is a portable AR data-collection system, not an AR controller for teleoperation. The second use (learning from human hand motion) is fine."),
    10: ("supported", None, "Agree."),
    13: ("incorrect", None, "Agree, borderline: Bunny-VisionPro is a teleoperation system with haptic feedback to the operator; its control input is Vision Pro hand tracking, not a haptic controller."),
    14: ("supported", None, "Overrode K2 ('incorrect'). The paper is about hand-held grippers whose recorded poses become robot end-effector targets, i.e. data from a handheld device, which is what FastUMI cites it for."),
    15: ("supported", "Domain shift remains a fundamental challenge across all subgroups. The disparity between human and robot domains, the so-called embodiment gap, often hinders the direct transfer of skills, as the visual appearance, dynamics, and even the action spaces differ substantially.",
         "Agree with the status. Shortened K2's quote: it silently skipped a sentence in the middle."),
    19: ("supported", None, "Agree."),
    24: ("supported", None, "Agree."),
    25: ("supported", None, "Agree."),
    26: ("incorrect", "To train our network, we collected over 800,000 grasp attempts over the course of two months, using between 6 and 14 robotic manipulators at any given time",
         "Overrode K2 ('supported'). FastUMI lists it under 'vision-driven demonstrations', but the data are robots' own grasp attempts; the paper uses no demonstrations."),
    31: ("supported", None, "Agree."),
    35: ("supported", None, "Agree."),
    40: ("incorrect", "We use an off-the-shelf hand detector [49] to identify hand locations from two viewpoints, reconstructing a 3D hand trajectory based on the calibrated camera parameters.",
         "Overrode K2 ('supported'), for one of three uses: FastUMI cites [40] for 'motion capture systems', but MimicPlay tracks hands with a detector on two calibrated cameras, no motion capture. Its use for video without action labels is fine."),
    41: ("supported", None, "Agree."),
    43: ("supported", "We offer models of different scales (ranging from 25M to 1.3B params) to support extensive scenarios.",
         "Overrode K2 ('unverifiable'). FastUMI cites [43] only for the tool and its large model; the 20 Hz on an RTX 4090 is FastUMI's own measurement, not attributed to [43]."),
    46: ("supported", None, "Agree."),
    48: ("supported", None, "Agree (first run returned a placeholder quote '...'; rerun, see k2_runs/)."),
    49: ("supported", None, "Agree."),
    50: ("incorrect", None, "Agree. AlignBot (the authors' own earlier paper) is about household task planning with user reminders and says nothing about scarce manipulation data."),
}


# Where K2's one-line summary of the citing claim was incomplete.
CLAIM_OVERRIDE = {
    40: "FastUMI cites MimicPlay as a sensor-enhanced interface, as an example of 'motion capture systems' for tracking, and as video-based observations without action labels.",
    43: "FastUMI cites Depth Anything V2 as the open-source depth estimation tool (and its large pre-trained model) it uses to add depth maps.",
}


def norm_src(s):
    return re.sub(r"[^a-z0-9]", "", re.sub(r"-\s*\n\s*", "", s.lower()))


def build_citations():
    d = OUT / "check-the-citations"
    shutil.rmtree(d, ignore_errors=True)
    (d / "code").mkdir(parents=True)
    (d / "k2_runs").mkdir()
    ids = json.loads((DATA / "ref_arxiv_ids.json").read_text())
    rows, lines = [], []
    for n, aid in sorted(ids.items(), key=lambda kv: int(kv[0])):
        n = int(n)
        rec = json.loads((RUNS / "citations" / f"ref_{n:02d}.json").read_text())
        k2 = rec["parsed"]
        status, quote, note = CITATION_REVIEW[n]
        quote = quote or k2["quote"]
        src = (DATA / "cited" / f"{n}.txt").read_text(errors="ignore")
        found = norm_src(quote) in norm_src(src)
        if not found and n != 3:
            raise SystemExit(f"quote for [{n}] not found in source")
        reason = k2["reason"] if status == k2["status"] and n not in (8, 40) else note
        rows.append({"ref": n, "arxiv_id": aid, "status": status, "k2_status": k2["status"],
                     "changed_by_reviewer": status != k2["status"] or quote != k2["quote"],
                     "quote_verbatim_in_extracted_text": found})
        lines += [f"### [{n}] {rec['entry'][:200]}", "",
                  f"- **ID:** arXiv:{aid} - https://arxiv.org/abs/{aid}",
                  f"- **Cited in FastUMI for:** {CLAIM_OVERRIDE.get(n, k2['claim'])}",
                  *[f"  - \"{c}\"" for c in rec["contexts"]],
                  f"- **Status:** **{status.upper()}**" + ("" if status == k2["status"] else f" (K2 said {k2['status']})"),
                  f"- **Quote from the cited paper:** \"{quote}\"",
                  f"- **Reason:** {reason}",
                  f"- **Reviewer check:** {note}", ""]
        shutil.copy(RUNS / "citations" / f"ref_{n:02d}.json", d / "k2_runs" / f"ref_{n:02d}.json")
    for f in (RUNS / "citations").glob("ref_*_failed_*.json"):
        shutil.copy(f, d / "k2_runs" / f.name)
    counts = {s: sum(r["status"] == s for r in rows) for s in ("supported", "incorrect", "unverifiable")}
    changed = sum(r["changed_by_reviewer"] for r in rows)
    head = ["# Citation audit: FastUMI (arXiv:2409.19499)", "",
            f"**Paper audited:** {PAPER} - {PAPER_LINK}", "",
            "**Sample (stated rule):** every reference whose entry in FastUMI's reference list contains an arXiv ID: "
            f"**{len(rows)} of 51 references**. All {len(rows)} are audited against the full text of the cited paper.", "",
            f"**Result:** {counts['supported']} supported, {counts['incorrect']} incorrect, {counts['unverifiable']} unverifiable.", "",
            "**Method:**",
            "1. For each reference, the FastUMI sentences that cite it were extracted automatically (handles `[3, 8-10]`-style brackets).",
            "2. The cited paper's arXiv PDF was converted to text (pdftotext) and given to K2 Horizon (`IFM/K2-Horizon-375B-A23B`) "
            "with those sentences; K2 returned the claim, a status, a verbatim quote and a reason (`k2_runs/`).",
            "3. A script checked each quote against the cited paper's text; I then reviewed every verdict against the source.",
            f"4. I changed {changed} of {len(rows)} K2 outputs (status or quote); each change is explained under 'Reviewer check'.", "",
            "**What did not work with K2:** in 19 of 26 calls (14 of the 21 final ones) the model wrote its reasoning into the answer field "
            "before the JSON, even with `response_format: json_object`, so the script takes the last JSON object; 4 calls were cut off "
            "at the 16K-token limit and had to be rerun with "
            "`reasoning_effort: low`; one run returned a literal `\"...\"` as its quote. K2 also got 4 of 21 verdicts wrong "
            "(refs 14, 26, 40, 43), so its statuses cannot be used without review. All 26 calls used 679K tokens.", "",
            "| Ref | arXiv | Status | K2 status | Changed by me |", "|---|---|---|---|---|"]
    head += [f"| [{r['ref']}] | {r['arxiv_id']} | {r['status']} | {r['k2_status']} | {'yes' if r['changed_by_reviewer'] else 'no'} |" for r in rows]
    (d / "CITATION_AUDIT.md").write_text("\n".join(head + ["", "## Details", ""] + lines))
    (d / "citation_audit.json").write_text(json.dumps(rows, indent=2))
    for c in CODE + ["audit_citations.py"]:
        shutil.copy(HERE / c, d / "code" / c)
    return d


if __name__ == "__main__":
    for b in (build_takeaways, build_related, build_citations):
        print(b())
