# Generate a Document: short technical review with K2 Horizon

**Finished document:** `handheld-transfer-review.pdf` (6 pages, A4), with the same text in `doc_final.md`.
It is a review titled "Moving handheld-gripper demonstrations to other robot hands: where the field stands
(October 2026)". It is written for new lab members who will work on UMI-style data collection.

## Inputs
- `BRIEF.md`: what I asked for, covering reader, length (1,400 to 1,900 words), the seven sections, and the rules (only
  facts from the sources, [n] citations, every reference with its arXiv ID or DOI and a link, no placeholders).
- `SOURCES.md`: the only material K2 was allowed to use. It is built from my earlier challenge work:
  - A: the FastUMI takeaways
  - B: the verified related-work reading list
  - C: the key numbers from the 203-paper dataset

## How it was made
1. `generate_document.py doc_v1` had K2 Horizon (reasoning effort medium) write the first draft from the brief and the
   sources. The full output, including reasoning, is in `runs/doc_v1.json`.
2. I checked the draft with `check_document.py`, which counts words, matches citations to references, flags reference
   IDs that are not in the sources, flags numbers that are not in the sources, and looks for placeholders. I also read
   it against the sources. My findings are in `review_v1.md`:
   - too long
   - "Source B" left in a heading
   - reference [14] had no link
   - two caveats about the dataset were missing
   - one misleading sentence about FastUMI
3. `generate_document.py doc_v2 review_v1.md doc_v1` had K2 revise the draft. Four points were fixed; the text was still about 30 words over the limit (`runs/doc_v2.json`).
4. Hand edits in `doc_final.md` (the only changes to K2's text):
   - restored the section numbers K2 dropped
   - cut about 50 words of repetition to reach the length limit: the full method list stated twice, the year-by-year
     counts, one sentence restating the fingertip approach, and the wired-transfer limit in section 3, which section 6 repeats
   - shortened one sentence on the fisheye camera
5. Converted to HTML with pandoc (`print.css`) and printed to PDF in a Chromium browser.

## Checks on the final text (`python3 check_document.py doc_final`)
- Body length is 1,883 words, counting whitespace-separated words without [n] markers. The brief allows 1,400 to 1,900.
- 14 references, every one cited in the text. None is cited without being listed.
- References 1 to 13 each carry an arXiv ID or DOI and a link, and all 26 IDs or links appear in the sources. Reference
  14 is the survey dataset compiled for this work, with its data-source link.
- Every number in the body occurs in the sources.
- No placeholders.

## Limitations
- The field statistics (section 5) come from model-made labels on abstracts. The document states this, and states
  that the handheld count is a lower bound.
- The review only covers what is in the sources: one main paper (FastUMI), 12 related papers, and the dataset. It is
  an orientation, not a full survey.
