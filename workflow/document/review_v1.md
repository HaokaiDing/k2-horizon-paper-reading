I checked doc_v1 against SOURCES.md with a script and by reading it. Good: every number in the text occurs in the
sources, all 14 references are cited, every arXiv ID / DOI matches the sources, no placeholders. Please revise:

1. Too long: the body is about 2,200 words; the brief asks for 1,400 to 1,900. Cut to about 1,800, mainly by
   shortening section 2 (keep only the FastUMI results that matter for transfer: fingertip coverage, T265 vs MINI
   under occlusion, depth for DP, data scaling, fisheye camera) and by not repeating the same statistics in the
   Summary and in section 5.
2. Leftover wording from the brief: the heading "Approaches in the literature, grouped by theme as in Source B" must
   not mention "Source B". Use "Approaches in the literature". The text must never mention "Source A/B/C".
3. Reference [14] reads "Source C: ...", which is not a reference and has no link. Replace it with:
   "Survey dataset of 203 arXiv papers on demonstration-collection systems (2019 to October 2026), compiled for this
   review from arXiv metadata via DataCite (https://api.datacite.org); labels by K2 Horizon from abstracts."
4. Section 5 must also state the other caveats from the source: labels were produced by a language model from
   abstracts (relevance spot check 19/20), and some handheld devices for dexterous hands are labelled other_teleop,
   so the handheld count (31) is a lower bound.
5. Summary, sentence 2: "FastUMI relaxes this only partially" is misleading. FastUMI does not relax the
   same-fingers assumption; it extends it to more robots by fitting fingertip attachments that cover over 90 % of the
   grippers in Open X-Embodiment. Say that.
Keep everything else, including all references 1-13 exactly as they are.
