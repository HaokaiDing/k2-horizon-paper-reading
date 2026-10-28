Tested k2_v2.html in Chrome at 1280x720. Start screen, HUD, clearing and arrow keys now work, no console errors.
Remaining bugs:

1. Down arrow and S set keys['down'] but nothing reads it, so they never lower the gripper. They must do exactly
   what Space does (lower / drop), triggered once per key press (ignore key auto-repeat via e.repeat).
2. The held object is drawn in the wrong place. drawGripper() translates to the gripper and then calls
   drawObject(holdingObj), but drawObject() itself translates by o.x + o.w/2, o.y + o.h/2 (the object's old belt
   position), so the held object is drawn far from the jaws. Draw it centred between the jaws.
3. The held object is only drawn when gripperState === 'holding'; while 'lifting' it disappears. Draw it in both.
4. Falling objects: dropObject() sets fall.x = gripperX (a centre), but drawObject() and the bin test treat x as
   the left edge. Use one convention (store left edge = gripperX - w/2) for drawing and use the object's centre
   for the bin test.
5. Fast drop (Space pressed twice quickly) should visibly lower the gripper faster (e.g. 3x speed); it currently
   only sets a flag. Normal lowering must stay safe for eggs.
6. While the gripper is lowering, the grab check uses only gripperX inside [o.x, o.x+o.w]; widen it by the jaw
   width so grabbing an object under the jaws is not pixel-perfect.
7. Pressing R on the start screen should also start the game (it is swallowed by the start-screen handler).
