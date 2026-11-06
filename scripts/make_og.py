"""Regenerates every Open Graph card (assets/images/og/*.png and og-image.png) in the Ledger brand.
Reads each page's og:image / og:title, renders an HTML card and screenshots it with headless Chrome.
Run: python3 scripts/make_og.py   (needs google-chrome)"""
import glob, html, os, re, subprocess, tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
COVER_FALLBACK = {"contact": "about", "certifications": "certifications"}

CARD = """<!doctype html><meta charset="utf-8"><style>
html,body{{margin:0}}
body{{width:1200px;height:630px;background:#F3EFE4;position:relative;overflow:hidden;color:#11261D;font-family:"Liberation Sans",Arial,sans-serif}}
.rules{{position:absolute;inset:0;background-image:linear-gradient(rgba(17,38,29,.09) 1px,transparent 1px);background-size:100% 36px}}
.top{{position:absolute;left:70px;top:58px;display:flex;align-items:center;gap:18px;font-family:"Liberation Mono",monospace;font-size:24px;letter-spacing:.04em}}
.mark{{width:54px;height:54px;border:3px solid #11261D;border-radius:5px;display:grid;place-items:center;font-weight:700;font-size:22px;color:#B3361A;transform:rotate(-4deg);box-shadow:4px 4px 0 #11261D;background:#F3EFE4}}
.kick{{position:absolute;left:70px;top:196px;font-family:"Liberation Mono",monospace;font-size:22px;letter-spacing:.18em;text-transform:uppercase;color:#B3361A;display:flex;align-items:center;gap:16px}}
.kick:before{{content:"";width:44px;height:2px;background:#B3361A}}
h1{{position:absolute;left:70px;top:246px;width:520px;margin:0;font-family:"Liberation Serif","Times New Roman",serif;font-weight:700;font-size:{fs}px;line-height:1.08;letter-spacing:-.02em}}
.foot{{position:absolute;left:70px;bottom:52px;font-size:25px;color:#44544B}}
.frame{{position:absolute;left:650px;top:96px;width:560px;height:440px;border:3px solid #11261D;border-radius:10px 0 0 10px;background:#0F1F18;box-shadow:12px 12px 0 #0F4D3A;overflow:hidden}}
.frame img{{width:880px;height:auto;position:absolute;left:-40px;top:-10px}}
.bar{{position:absolute;left:0;right:0;bottom:0;height:14px;background:#0F4D3A}}
.bar:after{{content:"";position:absolute;right:0;top:0;width:35%;height:100%;background:#B3361A}}
</style><div class="rules"></div>
<div class="top"><div class="mark">SK</div>saadconsulting.tech</div>
<div class="kick">{kicker}</div><h1>{title}</h1>
<div class="foot">Saad Ali Khan &middot; Full Stack Developer &middot; Karachi</div>
<div class="frame"><img src="file://{cover}"></div><div class="bar"></div>"""


def kicker(path, name):
    if name.startswith("blog"): return "Engineering notes"
    if path.startswith("projects/"): return "Case study"
    if path.startswith("services/"): return "Service"
    return "Portfolio"


def main():
    chrome = "google-chrome"
    jobs = []
    for f in sorted(glob.glob(ROOT + "/**/*.html", recursive=True)):
        rel = os.path.relpath(f, ROOT)
        if rel.startswith(("demos/", "scripts/")): continue
        s = open(f).read()
        m = re.search(r'property="og:image" content="[^"]*/assets/images/(og/[^"]+|og-image)\.png"', s)
        t = re.search(r'property="og:title" content="([^"]*)"', s)
        if not (m and t): continue
        out = os.path.join(ROOT, "assets/images", m.group(1) + ".png")
        name = os.path.basename(m.group(1))
        title = html.unescape(t.group(1)).replace(" | Saad Ali Khan", "")
        if name == "og-image": title = "Software where every number adds up"
        c = re.search(r"/assets/images/covers/([a-z0-9-]+)\.svg", s)
        cover = (c.group(1) if c else COVER_FALLBACK.get(name, "about"))
        fs = 62 if len(title) < 38 else 50 if len(title) < 62 else 42
        jobs.append((out, CARD.format(title=html.escape(title), kicker=kicker(rel, name), fs=fs,
                                      cover=os.path.join(ROOT, "assets/images/covers", cover + ".svg"))))
    seen = set()
    with tempfile.TemporaryDirectory() as d:
        for out, doc in jobs:
            if out in seen: continue
            seen.add(out)
            p = os.path.join(d, "card.html")
            open(p, "w").write(doc)
            subprocess.run([chrome, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                            "--allow-file-access-from-files", "--window-size=1200,630",
                            f"--screenshot={out}", "file://" + p], check=True, capture_output=True)
    print("wrote", len(seen), "cards")


if __name__ == "__main__":
    main()
