# Generate a Presentation: lab-meeting talk with K2 Horizon

**Finished deck:** `handheld-transfer-talk.pdf` (11 slides, 16:9). The source is `s_final.html`, one self-contained
HTML file with inline CSS and SVG charts.

The talk is "Handheld-gripper data on other robot hands: where we stand, and what our lab should try first". It is a
10-minute lab-meeting talk and ends with an ask: approve a 4-week pilot.

## Flow
1. Title.
2. Opening: why handheld data matters, and the embodiment gap.
3. What FastUMI changed: hardware and tracking.
4. What FastUMI changed: data and results. The chart shows Pick Cup success at 200, 400 and 800 demonstrations.
5. What breaks when the end-effector differs.
6. Four ways the literature approaches the gap.
7. The field in numbers: papers per year, from the 203-paper dataset.
8. The field in numbers: robot-free share, handheld vs all papers, with the caveats.
9. Open problems.
10. **The ask:** a week-by-week pilot (task and measure for each step), what we need, and a request for approval.
11. References. Numbers 1 to 14 match the citations on the slides.

## Inputs
- `BRIEF.md`: audience, goal, slide structure, word limit per slide, and the rules (only facts from the sources,
  citations, no placeholders).
- `SOURCES.md`: the only material K2 was given:
  - the checked review document from the "Generate a Document" quest
  - the key numbers of the dataset, computed in Python (`key_numbers.json`)

## How it was made
`generate_slides.py` sends the brief, a technical format block (1280x720 slides that print one per page) and the
sources to K2 Horizon. For a revision it also sends my review and the previous deck.

After every version I rendered the deck in a Chromium browser at 1280x720 and printed it to PDF. I checked each
slide for overflow and small text, looked at every page, and wrote a review.

| Version | Effort | What my review asked for |
|---|---|---|
| s_v1 | medium | first deck from the brief |
| s_v2 | medium | `review_s1.md`: reference list missing one entry so [14] was wrong; text-document look (small text, empty lower half); slide 8 title unclear; the ask was a paragraph |
| s_v3 | low | `review_s2.md`: fill the slides, bigger charts with axis titles, larger cards on slide 6, both dataset caveats, five open problems, references overflow |
| s_v4 | low | `review_s3.md`: **charts drawn to the wrong scale** (bars did not match the axis), slide 6 and references overflow. K2 now draws the charts with a small script that computes positions from the data |

Failed runs are kept in `runs/`:
- `s_v3_failed_medium.json`: all 40,000 tokens spent on reasoning.
- `s_v3_failed_low_1.json`: a degenerate reasoning loop.
- `s_v4_failed_low_1.json`: budget used up.

Each was retried with the same prompt.

**Hand edit**, the only change to K2's file. `s_final.html` is `s_v4.html` with one CSS rule changed. The
references slide still overflowed because the rule `p, li { font-size: 30px }` overrode the reference list font
size. The new rule is `.refs li { font-size: 18px; line-height: 1.35; margin-bottom: 6px }`.

## Checks on the final deck
- Rendered at 1280x720: 11 slides, no element outside its slide, no text under 14 px.
- `python3 check_slides.py s_final`:
  - Every number in the slide text occurs in the sources or the brief.
  - Every arXiv ID or DOI on the references slide is in the sources.
  - The numbers in the chart script are layout coordinates, plus the data values that appear in the slide text.
- I compared the charts against their axes by eye: 20.00 / 26.67 / 53.33; 2 / 3 / 1 / 4 / 5 / 24 / 70 / 94;
  41.4 % / 83.9 %.

## Limitations
- Reference 13 (Hussein et al., imitation learning survey) is listed but not cited on any slide. It is kept so the
  numbering matches the review document.
- The design is plain: white background, one accent colour, no images.
