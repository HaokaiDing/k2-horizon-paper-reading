Tested k2_v3.html in Chrome at 1280x720 with a scripted player (keyboard events + a read-only state probe).
Working now: start screen, arrow/A/D movement, Down/S/Space lowering, grab -> lift -> hold, held object drawn
under the jaws, drop into matching bin (+10, sorted +1), lose screen with final/best score, no console errors.

Remaining problems:

1. The game cannot be won. One pick-and-place cycle takes about 4.5 s (lowering ~1.7 s at 2.5 units/s, lifting
   ~1.7 s, moving + falling ~1 s) but a new object spawns every 1.6 s. Even a perfect scripted player sorted only
   4 objects before 3 objects fell off the belt and the game ended. Rebalance so that a skilled player can sort
   20 objects: e.g. lowering/lifting speed about 6 units/s, spawn interval about 3.0 s at level 1 shrinking by
   10 % per level (never below 1.8 s), belt speed 0.9 units/s at level 1. Keep the "objects falling off the end
   cost a life" rule.
2. HUD text (Score / Sorted / Level / Combo, top-left) overlaps the gripper and gantry when the gripper is on the
   left. Move the HUD into a top bar above the gantry (or a side panel) so nothing is drawn over it, and draw the
   gantry rail across the full width below the HUD.
3. The on-screen Restart button (bottom-right) covers part of the YELLOW bin. Move it (e.g. top-right corner).
4. The YELLOW label does not fit inside its bin; size labels to fit (e.g. measureText and shrink).
5. Win / lose / start overlay text is very small at 1280x720 (about 10 px). Use larger sizes (title ~48 px,
   lines ~20 px) that scale with the window.
