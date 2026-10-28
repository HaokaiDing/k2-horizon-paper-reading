Tested k2_v7.html: Restart button label now fits. On a phone (375 px wide, touch) the page has no
<meta name="viewport">, so mobile browsers lay it out 980 px wide and scale it down. Add
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no"> in <head>
(and prevent double-tap zoom on the on-screen buttons, which already have touch-action: manipulation).
Change only this; keep everything else exactly as it is.
