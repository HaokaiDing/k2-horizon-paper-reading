Tested k2_v5.html in Chrome at 1280x720 with a scripted player. Everything works: overlay layout fixed; start,
win (20/20, score 290) and lose screens; egg fast-drop breaks the egg (-1 life, lowering 0.32 s instead of ~0.7 s);
normal lowering onto an egg is safe; wrong bin and floor drop cost a life and reset the combo; R and the Restart
button restart; on-screen arrow buttons move and stop on pointerleave. No console errors.

One gap against the brief: the start screen shows the title, goal and best score but NOT the controls. Add the
controls to the start screen as their own short lines, for example:
"← → or A / D: move   ·   Space / ↓ / S: lower, grab, drop"
"Tap Space twice quickly = fast drop (breaks eggs!)   ·   R: restart"
Change only the start screen text; keep everything else exactly as it is.
