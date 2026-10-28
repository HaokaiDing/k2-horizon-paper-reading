# Checking the sample outputs against what I expected

**Real run:** FastUMI (arXiv:2409.19499), on 2026-10-28. All 21 references with an arXiv ID were checked: 26 K2
calls in total, including retries, using 679K tokens. The logs are in `k2_runs/`.

**Expected.** For each reference:
- a parseable verdict
- a quote that really appears in the cited paper
- a status I agree with after reading the cited paper myself

## Results
| Check | Result |
|---|---|
| Parseable JSON | 22 of 26 calls. The other 4 were cut off at the 16K-token limit with no JSON (`ref_06/15/19/25_failed_medium.json`); all 4 succeeded on the automatic retry with `reasoning_effort: low`. One parsed call returned a literal `"..."` as its quote (`ref_48_failed_placeholder.json`); the quote check rejected it and the reference was re-run. |
| Reasoning leaked into the answer field | 19 of 26 calls, so the parser takes the last JSON object (step 3). |
| Quote found verbatim in the cited paper | 20 of 21 final quotes. For [3], the quote is real but pdftotext broke it across a figure, so the automatic match fails; I confirmed it by hand. |
| Status agrees with my own reading | **17 of 21.** |
| Final result after review | 15 supported, 6 incorrect, 0 unverifiable. |

K2's status was wrong on 4 references:
- **[14]**: K2 said incorrect; I judged it supported.
- **[26]**: K2 said supported; I judged it incorrect.
- **[40]**: K2 said supported; I judged it incorrect.
- **[43]**: K2 said unverifiable; I judged it supported.

For [15] I kept the status but replaced the quote with a better one. Every change and the reason for it is written
under "Reviewer check" in `CITATION_AUDIT.md`.

## Errors and what they mean for users
- **K2's verdicts cannot be used unreviewed.** About 1 in 5 statuses was wrong in this run. The value of the
  workflow is that each verdict comes with a quote that has already been verified, so the reviewer only has to read
  one passage per reference instead of the whole cited paper.
- **Coverage is limited to references with an arXiv ID.** Here that is 21 of 51. References without one, such as
  books, journal-only papers and websites, still need to be checked by hand.
- **Long cited papers are cut to 150K characters.** In this run that affected only one paper, a 205K-character
  review.
