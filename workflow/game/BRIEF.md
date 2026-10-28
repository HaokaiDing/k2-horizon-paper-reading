# Brief: "Gripper Rush"

A small arcade game about a robot gripper sorting objects on a conveyor belt.

**Goal.** Sort 20 objects into the correct bins before you run out of 3 lives.

**Scene.**
- A conveyor belt runs left to right across the lower-middle of the screen.
- Objects appear at the left end and ride the belt: red cubes, blue cylinders and yellow eggs.
- Three bins sit along the bottom edge on the right side, one per colour (red, blue, yellow), labelled.
- A parallel-jaw gripper hangs from a gantry at the top and can move left/right along it.

**Controls.**
- Left / Right arrows (or A / D): move the gripper along the gantry.
- Space (or Down / S): lower the gripper. If it reaches an object it closes and lifts it; if it is already
  holding an object, Space opens the jaws and drops the object straight down.
- On-screen buttons ◀ ▶ ⤓ for the same actions (touch and mouse).
- R or the on-screen Restart button: restart at any time.

**Rules.**
- Dropping an object into the matching bin: +10 points and counts toward the 20.
- Wrong bin, dropping it back on the floor, or letting an object fall off the right end of the belt: lose 1 life.
- Eggs are fragile: if the gripper is lowered onto an egg faster than normal (holding Space for "fast drop",
  i.e. pressing Space twice quickly), the egg breaks and you lose 1 life. Normal lowering is safe.
- The belt speeds up a little after every 5 sorted objects.
- Combo: three correct sorts in a row without losing a life gives +5 bonus each.

**States.**
- Start screen with the title, one-line goal and controls; any key or click starts.
- HUD: score, sorted count "n / 20", lives as 3 small icons, current belt speed level.
- Win screen when 20 objects are sorted: "Line cleared!", final score, best score (kept in localStorage,
  wrapped in try/catch), "Press R to play again".
- Lose screen when lives reach 0: "Line stopped", final score, best score, "Press R to retry".

**Look.** Clean flat shapes on a dark industrial background; the gripper jaws visibly open and close;
short particle burst on a correct sort and a crack effect when an egg breaks. Canvas scales to the window
(keep a 16:9 play area, letterboxed) and stays crisp on high-DPI screens.
