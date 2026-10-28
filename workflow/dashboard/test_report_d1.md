Tested d_v1.html in Chrome at 1280 px. All 7 headline tiles match my independent Python calculation from data.csv
(203; 80.8 % / 164; 41.4 % / 84; 16.7 % / 34; 33.0 % / 67; 31 handheld, 26 robot-free; median 2,100 over 27).
Stacked year chart, table (203 rows) and the calculation notes are good. No console errors. Please fix:

1. Section 1 (collection methods) and section 5 (end-effectors): every bar is drawn solid BLACK and the value labels
   ("69 (34.0%)") are black text on top of the black bar, so they are unreadable. Give bars a colour (use the same
   colour per method as in the stacked chart; one neutral colour for end-effectors) and put the value label to the
   right of the bar end in dark text, never inside it.
2. Section 4 text is wrong: "Of these, 26 (12.8% of handheld-gripper papers) can collect demonstrations without a
   robot present." 12.8 % is 26 / 203. The share of handheld-gripper papers must be 26 / 31 = 83.9 %. Compute it
   with the handheld-gripper count as the denominator. Also show it next to the field-wide robot-free share
   (41.4 %) so the contrast is visible.
3. Section 6 dot chart uses a linear x scale: the 1,200,000 point squeezes every other point onto the axis and its
   label is cut off at the right edge. Use a log10 scale with ticks at 10, 100, 1k, 10k, 100k, 1M, label every
   point with its value without clipping (keep labels inside the plot area), and sort points by value.
4. Stacked chart: y-axis ticks are odd numbers (24, 47, 71, 94). Use round ticks (0, 20, 40, 60, 80, 100).
5. Add to the labels note: "Some handheld devices for dexterous hands are labelled other_teleop (e.g. DexPort,
   DEX-PHD), so the handheld-gripper count is a lower bound." (This is a known annotation error in the data.)
Keep everything else as it is, including the placeholder `const ROWS = /*__DATA__*/[];` and all element ids.
