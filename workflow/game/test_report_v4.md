Tested k2_v4.html in Chrome at 1280x720 with a scripted player. Balance is fixed: the player sorted 20/20 in
56 s with 0 lives lost, win screen shown, score 290 (200 + 18 combo bonuses of 5) is correct. HUD bar and Restart
button placement are fixed.

One regression: the start / win / lose overlay now lays its lines out side by side on ONE row
("Gripper Rush Sort 20 objects ... Best score: 0Press any key or click to start"), with no spacing between them.
The overlay must stack its lines vertically and centred (title, then goal/result, then best score, then the
prompt), each line its own block with some spacing. Change only what is needed for this; keep everything else.
