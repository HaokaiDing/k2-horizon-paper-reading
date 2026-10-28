Tested k2_v1.html in Chrome at 1280x720 and in a narrow window.

1. Text is drawn on top of itself every frame (HUD becomes an unreadable smear). Cause: draw() clears with
   fillRect(0,0,VIRTUAL_W,VIRTUAL_H) BEFORE the letterbox transform, i.e. only a 16x9-pixel corner is cleared.
   Clear the whole canvas in screen pixels each frame.
2. ctx.font uses 'vh' units ('0.3vh Arial', '0.5vh Arial'). Canvas ignores invalid font strings, so the size is
   wrong. Use a size in virtual units, e.g. `${0.35}px` inside the scaled transform, or draw text in screen space.
3. The start screen never appears: the overlay is only shown in endGame(). Show title, goal and controls before
   the first game, as the brief requires.
4. Arrow keys do not move the gripper: e.key is 'ArrowLeft'/'ArrowRight', but update() checks keys['left'] /
   keys['right']. Down arrow and S (lower) are not handled at all.
5. A grabbed object stays in `objects`, keeps moving with the belt and is still drawn on the belt; if it reaches
   the right end while held you lose a life. It must leave the belt when grabbed and move with the gripper.
6. The gripper never visibly lifts after grabbing (it stays at belt height while holding); per the brief it should
   close, lift back up to the gantry, and only then can it be moved to a bin.
7. Dropping: the object should fall straight down from the gripper into the bin (or onto the floor) and be scored
   when it lands, not instantly.
8. Lowering targets the object found at the moment Space is pressed, but objects keep moving; the gripper should
   grab whatever object is under the jaws when they reach belt height (or miss).
9. dt is not clamped: after switching tabs objects jump far along the belt. Clamp dt (e.g. to 0.05 s).
10. The on-screen buttons: releasing outside the button leaves the gripper moving (only pointerup is handled);
    also handle pointerleave/pointercancel.
11. HUD should also show the combo, and lives as icons; the win/lose overlay should say "Press R to play again" /
    "Press R to retry" and the Restart button must work from those screens.
