#!/usr/bin/env python3
"""Optimise certificate PNGs from the source folder into assets/images/certificates/<slug>.webp (800px wide)."""
import os, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(__file__))
from certs import CERTS
SRC = os.environ.get("CERT_SRC", os.path.expanduser("~/Documents/personal/certificates"))
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "images", "certificates")
os.makedirs(OUT, exist_ok=True)
for c in CERTS:
    cand = [f for f in os.listdir(SRC) if f.replace("\n", "").rsplit(".", 1)[0].strip() == c["img"]]
    if not cand:
        raise SystemExit("missing source image for " + c["slug"])
    im = Image.open(os.path.join(SRC, cand[0])).convert("RGB")
    im = im.resize((800, round(im.height * 800 / im.width)), Image.LANCZOS)
    im.save(os.path.join(OUT, c["slug"] + ".webp"), "WEBP", quality=82, method=6)
print("wrote", len(CERTS), "images")
