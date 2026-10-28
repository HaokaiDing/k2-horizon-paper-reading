"""Test-only: copy a game version and expose a read-only state probe (window.__g) for scripted playtests.
The probe file is never shipped; the submitted game is K2's file unchanged."""
import sys
from pathlib import Path

tag = sys.argv[1]
src = Path(f"{tag}.html").read_text()
probe = """
  window.__g = { get s(){return {state,score,sorted,lives,combo,level,gripperX,gripperY,gripperState,
    holding: holdingObj && {type:holdingObj.type,color:holdingObj.color},
    objects: objects.map(o=>({x:o.x,w:o.w,type:o.type,color:o.color})), falling: falling.length}},
    bins: () => getBins(), setX: v => { gripperX = v; } };
})();"""
i = src.rindex("})();")
Path(f"_probe_{tag}.html").write_text(src[:i] + probe + src[i + 5:])
print("ok")
