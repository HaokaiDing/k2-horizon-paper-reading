Tested d_v2.html. All fixes from the last round work: coloured bars with readable labels, handheld share 26/31 =
83.9 % next to 41.4 %, log-scale dataset chart, round y ticks, the lower-bound note. Headline tiles, the stacked
chart (2026: 30/16/16/8/11/7/3/3 = 94) and the filters (handheld 31, handheld 2026 16, title "UMI" 18) all match my
Python calculation. No console errors, no horizontal overflow.

Remaining issues:
1. On a 375 px phone the SVG charts are simply scaled down, so all chart text (axis ticks, bar labels, point
   labels) becomes ~4 px and unreadable. Re-render the charts for the actual container width (re-draw on resize):
   keep chart text at least 11 px on screen; on narrow widths the method bar chart should put the method name above
   its bar instead of in a left column, the stacked chart can drop every other year label if needed, and the dataset
   size chart can drop point labels below 1,000 on narrow screens.
2. The log axis of the dataset-size chart shows the label "1M" twice at the right end; show each tick once
   (1, 10, 100, 1k, 10k, 100k, 1M).
3. On a phone the paper table makes the page ~36,000 px tall. Below 600 px wide, show the table inside a scroll
   container (max-height about 70 vh, own vertical scroll), keeping the filters above it.
Keep everything else as it is, including the placeholder `const ROWS = /*__DATA__*/[];` and all element ids.
