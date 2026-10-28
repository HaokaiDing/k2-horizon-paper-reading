# Workflow: citation check with K2 Horizon

**What it automates.** Checking a paper's citations means asking, for each reference, whether the cited paper
actually says what the citing paper uses it for. Done by hand, that means opening every cited paper and searching
for the passage. This workflow does it automatically and gives the reviewer a verdict and a verbatim quote to check,
instead of a blank page.

## Trigger
It is run from the command line when someone wants a paper's citations checked, for example before submitting a
draft or before relying on a paper in a reading group:

    python3 extract_text.py paper.html data/        # once per paper
    python3 audit_citations.py                      # all references with an arXiv ID
    python3 audit_citations.py 14 26                # or only some references

## Inputs
- **The citing paper as arXiv HTML.** `extract_text.py` splits it into body text and the reference list.
- **`data/ref_entries.json`.** The reference list as {number: entry}.
- **`data/ref_arxiv_ids.json`.** {number: arXiv ID} for the references that carry an arXiv ID. The sample run has
  21 of FastUMI's 51.
- **`data/cited/<n>.txt`.** The text of each cited paper, made with `pdftotext` from its arXiv PDF
  (https://arxiv.org/pdf/<id>). These full texts are not included in this zip because they are other authors'
  papers; the IDs are enough to fetch them again.

## Steps (`audit_citations.py`)
1. **Find the citing sentences.** For each reference n, the script collects every body sentence that cites [n]. It
   understands brackets such as `[3, 8-10]`.
2. **Ask K2 Horizon.** The model is `IFM/K2-Horizon-375B-A23B`, called through `k2.py` (OpenAI-compatible, JSON
   mode, `reasoning_effort` medium). K2 receives the citing sentences, the reference entry and the full text of the
   cited paper (up to 150K characters). It returns JSON with these fields:
   - `claim`: what the paper relies on [n] for
   - `status`: supported, incorrect or unverifiable
   - `quote`: a verbatim passage from the cited paper
   - `reason`
3. **Parse robustly.** K2 often writes its reasoning before the JSON, even in JSON mode, so the script takes the
   last complete JSON object.
4. **Retry on failure.** If the reply was cut off and has no JSON, the failed call is saved as
   `ref_<n>_failed_medium.json` and the reference is re-run with `reasoning_effort: low`.
5. **Verify the quote.** The script checks that the quote really occurs in the cited paper's text, after
   normalising hyphenation, case and punctuation. Quotes under 20 characters fail, so a literal "..." cannot pass.
6. **Save the log.** One file per reference goes to `runs/citations/ref_<n>.json`, holding the prompt context,
   K2's full reasoning and answer, token usage, latency and the quote check.
7. **Human review.** A person reads each verdict against the cited paper and records the final status. The final
   report is `CITATION_AUDIT.md` with `citation_audit.json`.

## Output
- One JSON log per reference (`k2_runs/`).
- The reviewed report `CITATION_AUDIT.md`: per reference the claim, the citing sentences, the status, the quote,
  the reason and the reviewer's check.
- A machine-readable summary, `citation_audit.json`.
