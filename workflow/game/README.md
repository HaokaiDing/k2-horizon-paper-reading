# Gripper Rush: a single-file HTML game built with K2 Horizon

**Play:** open `gripper-rush.html` in any modern browser (double-click). One self-contained file: inline CSS and
JavaScript, Canvas 2D, no external URLs, libraries, images or fonts, no build step.

## The game

A robot gripper on an overhead gantry sorts objects coming down a conveyor belt into colour-matched bins.

- **Goal:** sort 20 objects into the correct bins before you lose 3 lives.
- **Controls:** ← → or A / D move the gripper. Space, ↓ or S lowers and grabs, and drops while holding.
  Pressing Space twice quickly is a fast drop, which breaks eggs. R restarts. On-screen ◀ ▶ ⤓ buttons do the same
  for touch and mouse, and a Restart button sits in the top-right.
- **Score:** +10 per correct sort, and +5 bonus for each sort while the combo is 3 or more. A wrong bin, a drop on
  the floor, an object falling off the end of the belt, or a fast drop onto an egg each cost 1 life. The belt speeds
  up every 5 sorts (level 1 to 5).
- **States:** a start screen with goal and controls; a HUD showing score, sorted n/20, lives, level and combo;
  a win screen ("Line cleared!") and a lose screen ("Line stopped"), each with final and best score (best score kept
  in localStorage); restart with R or the button.

## How K2 Horizon built it

`IFM/K2-Horizon-375B-A23B` wrote every line of the game. I wrote the brief (`BRIEF.md`), tested each version, and
sent K2 a written test report (`test_reports/`). K2 then returned the complete corrected file. I did not edit the
game code by hand. `gripper-rush.html` is K2's v8 output, byte-for-byte.

| Version | Input | Reasoning effort | Latency | Tokens in / out | Result |
|---|---|---|---|---|---|
| v1 | brief | medium | 36 s | 673 / 6,001 | Ran, but broken: canvas not cleared (text smeared), invalid `vh` font units, no start screen, arrow keys dead, held object stayed on the belt |
| v2 | v1 + report 1 (11 bugs) | medium | 5 s | 5,726 / 7,050 | Start screen, HUD, arrows fixed; Down/S dead, held/falling objects drawn in the wrong place |
| v3 (1st try) | v2 + report 2 | medium | 16 s | 6,321 / 40,000 | **Failed:** reasoning used all 40K tokens, no code returned |
| v3 | v2 + report 2 | low | 263 s | 6,356 / 21,412 | Grab, lift, drop and scoring correct; **game unwinnable** (scripted perfect player sorted only 4) |
| v4 | v3 + report 3 | low | 186 s | 6,486 / 24,730 | Rebalanced (perfect player wins 20/20), HUD bar; regression: overlay lines on one row |
| v5 | v4 + report 4 | low | 3 s | 6,655 / 6,201 | Overlay fixed (2-line CSS change) |
| v6 (1st try) | v5 + report 5 | low | 14 s | 6,708 / 40,000 | **Failed:** ran out of tokens again |
| v6 | v5 + report 5 | low | 3 s | 6,708 / 6,299 | Controls listed on start screen |
| v7 | v6 + report 6 | low | 3 s | 6,720 / 6,081 | Restart button label no longer clipped |
| v8 | v7 + report 7 | low | 60 s | 6,751 / 6,301 | Viewport meta for phones. **Final** |

10 calls, 223K tokens. The raw request and response of every call is in `k2_runs/`.

## How it was tested

- **Scripted playtests** in Chrome at 1280×720. A test-only copy of each version exposed a read-only state probe;
  real keyboard events drove the game, and the script checked each state transition. The probe was never part of
  the shipped file.
- **Final checks** (v6 logic, unchanged through v8, which only touched CSS and the meta tag):
  - Any key starts the game.
  - ← / A and → / D move the gripper. Space, ↓ and S lower it.
  - Empty lowering returns to the top. Grab, lift and hold work, and the held object is drawn under the jaws.
  - Correct bin: +10 and sorted +1.
  - Wrong bin: −1 life and combo reset. Floor drop: −1 life.
  - Fast drop on an egg: −1 life, egg removed, lowering takes 0.32 s instead of about 0.7 s.
  - Normal lowering onto an egg is safe.
  - Win: 20/20 in 56 s with 0 lives lost, score 290 (= 200 + 18 × 5 combo bonus, as expected). Lose screen shown
    at 0 lives.
  - R and the Restart button reset all values. The on-screen ▶ button moves the gripper and stops on pointer leave.
  - No console errors.
- **Phone check** at 375 px with touch emulation: the start screen shows, the layout uses the device width, and the
  touch buttons are usable.

## Limitations and lessons

- The first version K2 wrote looked complete but was not playable. Every fix came from a concrete test report;
  vague requests ("make it work") were not tried.
- Twice K2 spent its whole 40K-token budget reasoning and returned no code. `reasoning_effort: low` fixed it, and
  small targeted change requests came back in about 3 s.
- K2's reasoning sometimes leaked into the answer and even contained the text `<!DOCTYPE html>`. The extraction
  takes the last complete document in the reply.
- K2 introduced one regression (v4 overlay layout), caught by retesting every version.
- In portrait on a phone the 16:9 play area is small; landscape plays better.

## Files

- `gripper-rush.html`: the game (the only HTML file).
- `BRIEF.md`: the brief given to K2.
- `test_reports/`: my report for each round, which was K2's input for the next version.
- `k2_runs/`: the raw K2 call records (JSON), including the two failed calls.
- `scripts/`: `generate_game.py`, `fix_game.py` (call the K2 API; key read from the environment, none included),
  `make_probe.py` (test-only state probe), `k2.py` (API client).
