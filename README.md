# Reading a robotics paper with K2 Horizon: what held up and what didn't

*Haokai Ding · October 2026 · written for the K2 Horizon Ascent Challenge*

I work on robot manipulation, and a lot of my week goes into reading papers on handheld data collection: UMI-style grippers that a person carries around to record demonstrations. My open question right now is:

> How can demonstrations collected with a handheld, UMI-style gripper be transferred to robots whose end-effectors differ from the data-collection gripper?

I wanted to know if K2 Horizon (the hosted `IFM/K2-Horizon-375B-A23B` model) could take some of that reading work off my hands. I built one small workflow around one paper, [FastUMI (arXiv:2409.19499)](https://arxiv.org/abs/2409.19499), and then **checked every output against the source** instead of trusting it. This post covers what I built, the numbers, and the parts that broke.

All code, prompts and raw model outputs are in this repository ([`workflow/`](workflow/)).

## The workflow

```
arXiv HTML ──► extract_text.py ──► paper body (65K chars) + reference list (15K chars)
                                         │
             ┌───────────────────────────┼─────────────────────────────┐
             ▼                           ▼                             ▼
   Step 1: takeaways           Step 2a: related work          Step 2b: related work
   (whole paper in one         from the question only         from the question + the
    prompt; every point         (model memory)                 paper's own reference list
    needs a verbatim quote)                                    (grounded)
             │                           │                             │
             └───────────────► Step 3: verify.py ◄─────────────────────┘
                 quotes vs. paper text · arXiv IDs vs. DataCite · titles vs. DataCite/Crossref
```

* `k2.py` is a client of about 40 lines, written with only the Python standard library. It talks to the OpenAI-compatible endpoint `https://api.ifm.ai/v1/chat/completions`.
* `run_workflow.py` holds the three prompts. Each run is saved to `runs/<step>.json` with its latency, token usage, the reasoning trace and the raw content.
* `verify.py` has no LLM in it. It checks K2's outputs with plain string matching and public metadata APIs.

## Results

| Step | Latency | Tokens (in / out) | Outcome |
|---|---|---|---|
| 1. Takeaways (full paper in context) | 39 s | 13,015 / 2,686 | 18 points. **18/18 quotes found verbatim in the paper** (16/18 with strict matching, because two quotes dropped `[30]`-style citation markers) |
| 2a. Related work from memory | 57 s | 211 / 5,094 | 11 papers. **0/11 could be verified.** 4 had arXiv IDs, and **all 4 IDs point to unrelated physics/math papers** |
| 2b. Related work from the reference list | 39 s | 4,509 / 2,859 | 12 papers in 4 themes. **12/12 real**: 10 verified automatically, 2 by hand |
| Failed first attempts (2a, 2b) | 6 s / 143 s | 28,685 total | Ran out of `max_tokens` with no usable JSON (see below) |

The whole experiment, failures included, used about 57K tokens, well under the 10M/day per-key allowance.

### What worked: long-context extraction with evidence

I put the entire 65K-character paper into one prompt and asked for findings, methods and limitations. Each item had to come with a verbatim quote of at most 40 words, and each limitation had to say whether the authors stated it or the model inferred it.

The output was good. The six findings carry the paper's real numbers, and I grep-checked them against the text:

* depth from Depth Anything V2 raises Diffusion Policy success from 53.33% to 80.00% on *Pick Lid*;
* T265 tracking error is 10.5 mm vs. 15.2 mm for the MINI sensor in low occlusion;
* *Pick Cup* success grows from 20.00% to 53.33% as demonstrations go from 200 to 800.

All five limitations were marked `stated_by_authors: true`, and they match the paper's own discussion: vision only, no tactile sensing; wired data transfer; not every gripper has a fingertip attachment; T265 drift under occlusion or low light. The only defect was cosmetic: in two quotes K2 silently removed in-text citation markers such as `[30]`. That matters if you plan to match quotes by exact string.

### What didn't work (1): related work from memory is fabricated

When I asked for related work with only the research question as input, K2 returned 11 confident, well-structured entries, organised by theme, each with a plausible "why it matters" paragraph. None of them could be verified:

* Titles such as *"Cross-Embodiment Transfer of Manipulation Policies"* (attributed to "R. Rusu, M. Vecerik, …, 2020") and *"Self-Supervised Adaptation of Policies to New Grippers"* do not exist in DataCite's arXiv records or in Crossref.
* For 4 entries K2 gave an arXiv ID even though the prompt said *"use null for identifiers you are unsure of"*. Those IDs resolve to *Tightening Time-Energy Uncertainty Relations*, *Canonical X-Ray Fluorescence Line Intensities as Column Density Indicators*, *Non-Hermitian skin effect of dislocations and its topological origin*, and *Ellipsephic harmonic series revisited*.
* Even well-known work came back with the wrong title. MimicGen became *"MimicGen: Learning from Human Demonstrations for Robot Manipulation"*.

The output looks equally confident whether it is right or wrong, and that is why this failure is dangerous. **Lesson: never ask the model to recall citations. Give it the candidates.**

### What fixed it: ground the model in the paper's own reference list

Step 2b asks the same question, but it passes in FastUMI's reference list (51 entries) and asks K2 to choose and organise at least 8 of them. All 12 picks are real. Ten were confirmed automatically: 6 through their arXiv ID, and 4 through a title match because the reference had no ID. The remaining two were *Open X-Embodiment* and Hussein et al.'s imitation-learning survey; my verifier missed them only because of messy reference-entry titles, and I checked both by hand. The grouping also makes sense for my question:

1. **UMI and cross-embodiment frameworks**: UMI, Open X-Embodiment, human-to-robot imitation in the wild
2. **Morphological gap and handheld grippers**: *On hand-held grippers and the morphological gap in human manipulation*, wearable human-to-robot skill transfer, DexCap
3. **Large-scale demonstration datasets and collection**: RT-1, VR teleoperation imitation, *Grasping in the Wild*
4. **Policy learning from demonstrations**: Diffusion Policy, *Data Quality in Imitation Learning*, imitation-learning survey

The limit here is coverage. A grounded list can only contain papers that FastUMI already cites, so anything newer than the paper (2025 onward) is invisible. Some "why it matters" notes also stretch a little. For example, it says UMI "abstracts away the specific gripper geometry", which overstates what UMI does for different end-effectors. I still read every note before I use it.

### What didn't work (2): reasoning that never ends

My first runs of 2a and 2b used plain prompts that asked for JSON, with `max_tokens=12000`. Both used up the whole budget:

* **2a** stopped after 6 s. All 12,000 completion tokens were counted as reasoning, the separate `reasoning` field was empty, and `content` held about 40K characters of thinking out loud ("I think there's a paper by Google DeepMind or similar…"). It never reached the JSON.
* **2b** produced about 39K characters of reasoning and then a JSON object cut off halfway.

The fix came from the [IFM docs](https://docs.ifm.ai/): set `response_format: {"type": "json_object"}` and cap the thinking with `chat_template_kwargs: {"reasoning_effort": "medium"}`. Both steps then finished in under a minute with valid JSON, and 2b used 2.9K output tokens instead of 12K. One small detail: the docs say the trace comes back in `reasoning_content`, but the API returned it as `reasoning`, so my client reads both.

## Lessons

1. **K2 Horizon is strong at reading what's in front of it.** Full-paper extraction with evidence quotes was accurate and quick (39 s for 13K input tokens). This is the part of the workflow I will keep using.
2. **It is not a citation database.** Without grounding, it invents papers and IDs, and nothing in the output warns you. Any citation it gives needs an automated check.
3. **Set reasoning effort and JSON mode for every structured call.** The default can spend the whole token budget on thinking.
4. **The verifier was most of the work.** The K2 calls took about 40 lines of code; checking the outputs took about 150. Public metadata APIs had their own trouble too: the arXiv API rate-limited me (HTTP 429/503) and OpenAlex now needs paid credits. I ended up using DataCite (every arXiv paper has a `10.48550/arXiv.<id>` DOI there) and Crossref.

## Reproduce

```bash
cd workflow
curl -sL https://arxiv.org/html/2409.19499v2 -o data/fastumi.html
python3 extract_text.py data/fastumi.html data
export K2_API_KEY=...            # from platform.ifm.ai
python3 run_workflow.py          # steps 1, 2a, 2b -> runs/*.json
python3 verify.py                # step 3 -> runs/3_verification.json
```

Only the Python 3 standard library is needed. Outputs vary from run to run (temperature 0.2), so your counts may differ a little from mine.
