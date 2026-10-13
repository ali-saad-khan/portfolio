#!/usr/bin/env python3
"""Generates the SVG illustrations in assets/images/ (covers for case studies,
services and the About page). Run from anywhere: python3 scripts/make_images.py"""
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "images")
V, C, P, G, Y = "#8B7CFF", "#22D3EE", "#F472B6", "#34D399", "#FBBF24"
TXT, DIM = "#E5E7EB", "#8B93A7"
SANS = "Inter, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def t(x, y, s, size=18, fill=TXT, weight=500, mono=False, anchor="start", opacity=1):
    fam = MONO if mono else SANS
    return (f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}" opacity="{opacity}">{esc(s)}</text>')


def rect(x, y, w, h, fill="#ffffff", op=0.06, r=10, stroke=None, sop=0.14):
    st = f' stroke="{stroke}" stroke-opacity="{sop}"' if stroke else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" fill-opacity="{op}"{st}/>'


def win(x, y, w, h, title=""):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="#12152A" fill-opacity="0.92" '
            f'stroke="#fff" stroke-opacity="0.14"/>'
            f'<path d="M{x} {y+46}H{x+w}" stroke="#fff" stroke-opacity="0.1"/>'
            f'<circle cx="{x+24}" cy="{y+23}" r="6" fill="#FF5F56"/><circle cx="{x+44}" cy="{y+23}" r="6" fill="#FFBD2E"/>'
            f'<circle cx="{x+64}" cy="{y+23}" r="6" fill="#27C93F"/>'
            + t(x + w - 20, y + 28, title, 14, DIM, 500, True, "end"))


def chip(x, y, s, color=V, size=15, w=None, mono=True):
    w = w or int(len(s) * size * 0.62 + 28)
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{size+16}" rx="{(size+16)/2}" fill="{color}" fill-opacity="0.16" '
            f'stroke="{color}" stroke-opacity="0.5"/>' + t(x + w / 2, y + size + 2, s, size, color, 600, mono, "middle"))


def bar(x, y, w, color=V, op=0.35, h=10):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" fill="{color}" fill-opacity="{op}"/>'


def arrow(x1, y1, x2, y2, color=C):
    return (f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{color}" stroke-width="2.5" stroke-linecap="round" stroke-dasharray="2 7"/>'
            f'<circle cx="{x2}" cy="{y2}" r="5" fill="{color}"/>')


def base(inner, uid):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 675" width="1200" height="675" role="img">
<defs>
<linearGradient id="bg{uid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0B0D18"/><stop offset="1" stop-color="#1A1240"/></linearGradient>
<linearGradient id="gr{uid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{V}"/><stop offset="0.55" stop-color="{C}"/><stop offset="1" stop-color="{P}"/></linearGradient>
<filter id="bl{uid}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="70"/></filter>
<pattern id="gd{uid}" width="48" height="48" patternUnits="userSpaceOnUse"><path d="M48 0H0V48" fill="none" stroke="#fff" stroke-opacity="0.045"/></pattern>
</defs>
<rect width="1200" height="675" fill="url(#bg{uid})"/>
<rect width="1200" height="675" fill="url(#gd{uid})"/>
<circle cx="180" cy="80" r="230" fill="{V}" opacity="0.38" filter="url(#bl{uid})"/>
<circle cx="1080" cy="560" r="240" fill="{C}" opacity="0.25" filter="url(#bl{uid})"/>
<circle cx="760" cy="40" r="150" fill="{P}" opacity="0.2" filter="url(#bl{uid})"/>
{inner}
</svg>'''.replace("url(#gr)", f"url(#gr{uid})")


def grad(uid):
    return f"url(#gr{uid})"


def ledger(u):
    s = win(80, 100, 640, 470, "ledger_entries")
    s += t(112, 190, "ACCOUNT", 13, DIM, 600, True) + t(430, 190, "DEBIT", 13, DIM, 600, True) + t(560, 190, "CREDIT", 13, DIM, 600, True)
    rows = [("wallet:alice", "250.0000", ""), ("ledger:float", "", "250.0000"), ("wallet:alice", "", "75.5000"),
            ("wallet:bob", "75.5000", ""), ("reversal #41", "40.0000", ""), ("wallet:bob", "", "40.0000")]
    for i, (a, d, c) in enumerate(rows):
        y = 232 + i * 46
        s += rect(104, y - 26, 592, 38, "#fff", 0.04, 8)
        s += t(120, y, a, 17, TXT, 500, True)
        if d: s += t(430, y, d, 17, C, 600, True)
        if c: s += t(560, y, c, 17, P, 600, True)
    s += chip(112, 510, "Σ debits = Σ credits  ✓", G, 16)
    s += win(760, 130, 360, 200, "POST /transfers")
    s += t(782, 205, "Idempotency-Key: 9f2c…a41", 15, C, 500, True) + t(782, 238, "→ 201 Created", 16, G, 600, True)
    s += t(782, 272, "retry → 200 (stored response)", 15, TXT, 500, True) + t(782, 304, "changed payload → 409", 15, Y, 500, True)
    s += win(760, 360, 360, 210, "reconcile")
    s += t(782, 430, "cached balance", 15, DIM, 500, True) + bar(782, 442, 310, V, 0.5, 12)
    s += t(782, 486, "ledger balance", 15, DIM, 500, True) + bar(782, 498, 310, C, 0.5, 12)
    s += chip(782, 522, "0 drift detected", G, 15)
    return base(s, u)


def store(u):
    s = win(70, 90, 740, 500, "my-store.app / products")
    for i in range(6):
        x, y = 100 + (i % 3) * 232, 150 + (i // 3) * 210
        s += rect(x, y, 212, 190, "#fff", 0.05, 14, "#fff")
        s += f'<rect x="{x+12}" y="{y+12}" width="188" height="108" rx="10" fill="{[V,C,P,G,Y,V][i]}" fill-opacity="0.28"/>'
        s += f'<circle cx="{x+106}" cy="{y+66}" r="26" fill="{[V,C,P,G,Y,V][i]}" fill-opacity="0.55"/>'
        s += bar(x + 12, y + 136, 120, TXT, 0.5, 10) + bar(x + 12, y + 156, 60, DIM, 0.5, 9)
    s += chip(108, 160, "−20%", P, 14)
    s += win(850, 120, 290, 300, "cart")
    for i in range(3):
        y = 190 + i * 52
        s += rect(872, y, 44, 38, [V, C, P][i], 0.35, 8) + bar(928, y + 6, 120, TXT, 0.5, 9) + bar(928, y + 24, 70, DIM, 0.5, 8)
    s += f'<rect x="872" y="352" width="246" height="42" rx="21" fill="{grad(u)}"/>' + t(995, 379, "Place order · COD", 16, "#fff", 700, False, "middle")
    s += rect(850, 450, 290, 130, "#12152A", 0.92, 14, "#fff")
    s += t(872, 486, "inventory_movements", 13, DIM, 600, True) + t(872, 520, "− 2   order #1042", 16, P, 600, True)
    s += t(872, 552, "+ 40  manual adjust", 16, G, 600, True)
    return base(s, u)


def practical(u):
    s = win(70, 100, 680, 470, "meal_plan.week")
    days = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
    for i, d in enumerate(days):
        s += t(112 + i * 90, 182, d, 13, DIM, 600, True)
        for j in range(3):
            col = [V, C, P][(i + j) % 3]
            on = (i * 3 + j) % 4 != 3
            s += rect(98 + i * 90, 196 + j * 90, 78, 76, col if on else "#fff", 0.28 if on else 0.05, 12, col if on else "#fff")
            if on: s += bar(110 + i * 90, 222 + j * 90, 54, col, 0.8, 8) + bar(110 + i * 90, 242 + j * 90, 34, col, 0.5, 8)
    s += chip(100, 500, "slot reserved · no overlap", G, 15)
    s += f'<rect x="790" y="120" width="340" height="210" rx="22" fill="{grad(u)}" fill-opacity="0.9"/>'
    s += t(816, 168, "WALLET", 14, "#fff", 700, True, opacity=0.8) + t(816, 232, "4,250.00", 44, "#fff", 800)
    s += t(816, 296, "top-up · refund · deduct", 15, "#fff", 500, True, opacity=0.85)
    s += win(790, 360, 340, 210, "dispatch.list")
    for i in range(4):
        s += rect(812, 420 + i * 36, 296, 28, "#fff", 0.05, 8) + bar(826, 430 + i * 36, 120 - i * 14, TXT, 0.45, 8) + chip(1030, 421 + i * 36, "OK", G, 11, 56)
    return base(s, u)


def wordpress(u):
    import math
    s = ""
    cx, cy = 360, 340
    s += f'<circle cx="{cx}" cy="{cy}" r="46" fill="{V}" fill-opacity="0.4" stroke="{V}"/>' + t(cx, cy + 6, "Home", 16, "#fff", 700, False, "middle")
    types = [("Services", C), ("Locations", P), ("Resources", G), ("News", Y), ("Team", V)]
    for i, (n, col) in enumerate(types):
        a = -math.pi / 2 + i * 2 * math.pi / 5
        x, y = cx + 190 * math.cos(a), cy + 190 * math.sin(a)
        s += f'<path d="M{cx} {cy}L{x:.0f} {y:.0f}" stroke="{col}" stroke-opacity="0.5" stroke-width="2"/>'
        for k in range(7):
            b = a + (k - 3) * 0.2
            lx, ly = x + 82 * math.cos(b), y + 82 * math.sin(b)
            s += f'<path d="M{x:.0f} {y:.0f}L{lx:.0f} {ly:.0f}" stroke="{col}" stroke-opacity="0.25"/><circle cx="{lx:.0f}" cy="{ly:.0f}" r="6" fill="{col}" fill-opacity="0.8"/>'
        s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="34" fill="#12152A" stroke="{col}" stroke-width="2"/>' + t(f"{x:.0f}", f"{y+5:.0f}", n, 13, col, 700, False, "middle")
    s += chip(60, 590, "800+ pages", V, 20)
    s += win(740, 110, 390, 300, "acf · field group")
    for i, (k, v) in enumerate([("hero_title", "text"), ("services", "repeater"), ("related_posts", "relationship"), ("locale", "select")]):
        y = 180 + i * 56
        s += rect(764, y, 342, 44, "#fff", 0.05, 10, "#fff") + t(782, y + 28, k, 16, TXT, 500, True) + chip(960, y + 8, v, C, 12, 130)
    s += win(740, 440, 390, 150, "wp_postmeta")
    s += t(764, 512, "autoload cleanup", 16, TXT, 500, True) + bar(764, 528, 300, G, 0.55, 12) + chip(764, 550, "TTFB ↓", G, 13)
    return base(s, u)


def shopify(u):
    s = win(70, 100, 700, 480, "product.liquid")
    s += rect(100, 160, 300, 300, V, 0.28, 16) + f'<circle cx="250" cy="310" r="70" fill="{C}" fill-opacity="0.5"/>'
    s += bar(430, 170, 240, TXT, 0.6, 16) + bar(430, 204, 150, DIM, 0.5, 11) + t(430, 262, "$ 49.00", 28, TXT, 800)
    s += chip(430, 286, "Bundle: 3 items", P, 14) + chip(430, 330, "Size · M", C, 14) + chip(540, 330, "Color · Ink", V, 14)
    s += f'<rect x="430" y="390" width="300" height="48" rx="24" fill="{grad(u)}"/>' + t(580, 421, "Add to cart", 17, "#fff", 700, False, "middle")
    s += t(100, 515, "{% section 'bundle-selector' %}", 15, C, 500, True)
    s += f'<rect x="800" y="70" width="330" height="540" rx="20" fill="#12152A" stroke="#fff" stroke-opacity="0.2"/>'
    s += t(826, 118, "Your cart", 20, TXT, 700) + chip(1040, 94, "3", P, 14, 44)
    for i in range(3):
        y = 150 + i * 92
        s += rect(826, y, 64, 64, [V, C, P][i], 0.35, 12) + bar(906, y + 8, 150, TXT, 0.5, 10) + bar(906, y + 30, 90, DIM, 0.5, 9) + t(906, y + 62, f"${[49,18,22][i]}.00", 14, DIM, 600, True)
    s += f'<rect x="826" y="500" width="278" height="50" rx="25" fill="{grad(u)}"/>' + t(965, 532, "Checkout", 18, "#fff", 700, False, "middle")
    s += t(826, 585, "/cart.js · /cart/change.js", 13, DIM, 500, True)
    return base(s, u)


def payments(u):
    s = ""
    nodes = [("Client", V), ("Gateway", C), ("Webhook", P), ("Verified", G)]
    for i, (n, col) in enumerate(nodes):
        x = 110 + i * 290
        s += f'<rect x="{x}" y="130" width="190" height="110" rx="20" fill="#12152A" stroke="{col}" stroke-width="2"/>'
        s += f'<circle cx="{x+95}" cy="170" r="16" fill="{col}" fill-opacity="0.5"/>' + t(x + 95, 215, n, 20, TXT, 700, False, "middle")
        if i < 3:
            s += arrow(x + 200, 185, x + 280, 185, col)
    s += t(405, 168, "signed", 12, DIM, 500, True, "middle") + t(695, 168, "async", 12, DIM, 500, True, "middle") + t(985, 168, "SHA256 ✓", 12, G, 600, True, "middle")
    s += win(110, 300, 600, 290, "payment_logs")
    logs = [("12:01:07", "init  ref=A-4821", C), ("12:01:09", "redirect → gateway", DIM), ("12:01:41", "webhook  sig=valid", G),
            ("12:01:41", "duplicate  ignored (idempotent)", Y), ("12:01:43", "status=PAID  settled", G)]
    for i, (a, b, col) in enumerate(logs):
        s += t(134, 372 + i * 42, a, 15, DIM, 500, True) + t(236, 372 + i * 42, b, 16, col, 500, True)
    s += f'<path d="M930 330l110 40v90c0 70-50 110-110 140c-60-30-110-70-110-140v-90z" fill="{G}" fill-opacity="0.15" stroke="{G}" stroke-width="3"/>'
    s += '<path d="M885 465l32 32l60-70" fill="none" stroke="#34D399" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>'
    s += t(930, 625, "no card data stored", 14, DIM, 600, True, "middle")
    return base(s, u)


def code(u):
    s = win(70, 100, 700, 470, "OrderService.php")
    lines = [(0, V, 180), (0, C, 120), (20, TXT, 240), (20, P, 160), (40, G, 280), (40, TXT, 200), (40, Y, 140), (20, TXT, 100), (0, V, 60), (0, TXT, 220), (20, C, 300)]
    for i, (ind, col, w) in enumerate(lines):
        y = 150 + i * 36
        s += t(98, y + 10, f"{i+1:02d}", 13, DIM, 500, True, opacity=0.6) + bar(138 + ind * 2, y, w, col, 0.7, 12)
    s += win(810, 100, 320, 250, "app/")
    for i, (n, col) in enumerate([("Http/Controllers", V), ("Services", C), ("Policies", P), ("Repositories", G)]):
        s += chip(834, 160 + i * 44, n, col, 14, 250)
    s += win(810, 380, 320, 190, "phpunit")
    s += t(834, 450, "✓ transfer_is_atomic", 15, G, 500, True) + t(834, 484, "✓ policy_blocks_other_user", 15, G, 500, True) + t(834, 518, "✓ validation_rejects_bad_input", 15, G, 500, True)
    return base(s, u)


def api(u):
    s = win(70, 100, 640, 470, "routes/api.php")
    eps = [("POST", "/auth/login", "200", G, V), ("GET", "/wallets", "200", G, C), ("POST", "/wallets/{id}/credit", "201", G, V),
           ("POST", "/transfers", "201", G, V), ("GET", "/transactions", "200", G, C), ("DELETE", "/tokens/{id}", "204", Y, P)]
    for i, (m, p, st, sc, mc) in enumerate(eps):
        y = 160 + i * 62
        s += rect(96, y, 588, 48, "#fff", 0.05, 12, "#fff") + chip(108, y + 8, m, mc, 13, 78) + t(204, y + 31, p, 17, TXT, 500, True) + chip(610, y + 8, st, sc, 13, 60)
    s += win(750, 100, 380, 300, "response.json")
    for i, (k, v, col) in enumerate([("id", '"01HZX…"', C), ("status", '"completed"', G), ("amount", '"250.0000"', P), ("created_at", '"2026-…"', DIM)]):
        s += t(776, 172 + i * 44, f'"{k}":', 16, V, 500, True) + t(920, 172 + i * 44, v, 16, col, 500, True)
    s += chip(750, 430, "Bearer token · Sanctum", V, 14) + chip(750, 474, "Idempotency-Key", C, 14) + chip(750, 518, "429 rate limited", Y, 14)
    return base(s, u)


def db(u):
    s = ""
    tables = [(80, 120, "users", ["id PK", "email", "role"], V), (440, 90, "wallets", ["id PK", "user_id FK", "balance"], C),
              (800, 120, "transactions", ["id PK", "wallet_id FK", "type", "amount"], P), (440, 370, "ledger_entries", ["id PK", "txn_id FK", "account", "debit", "credit"], G)]
    for x, y, n, cols, col in tables:
        h = 70 + len(cols) * 38
        s += f'<rect x="{x}" y="{y}" width="320" height="{h}" rx="16" fill="#12152A" stroke="{col}" stroke-width="2"/>'
        s += f'<rect x="{x}" y="{y}" width="320" height="46" rx="16" fill="{col}" fill-opacity="0.25"/>' + t(x + 20, y + 30, n, 18, TXT, 700, True)
        for i, c in enumerate(cols):
            s += t(x + 20, y + 80 + i * 38, c, 16, DIM if "FK" not in c else col, 500, True)
    for (a, b, c, d) in [(400, 190, 440, 190), (760, 190, 800, 190), (600, 280, 600, 370), (800, 260, 760, 430)]:
        s += f'<path d="M{a} {b}L{c} {d}" stroke="#fff" stroke-opacity="0.45" stroke-width="2.5" stroke-dasharray="5 7"/>'
    s += chip(80, 420, "indexed foreign keys", G, 15) + chip(80, 468, "ACID transactions", C, 15) + chip(80, 516, "EXPLAIN-checked queries", V, 15)
    return base(s, u)


def about(u):
    s = f'<circle cx="330" cy="340" r="190" fill="none" stroke="{grad(u)}" stroke-width="6"/>'
    s += f'<circle cx="330" cy="340" r="170" fill="#12152A"/>' + f'<circle cx="330" cy="340" r="170" fill="{V}" fill-opacity="0.12"/>'
    s += t(330, 378, "SK", 120, "#fff", 800, False, "middle")
    s += chip(120, 120, "Laravel", V, 18) + chip(470, 150, "PHP 8", C, 18) + chip(90, 560, "MySQL", P, 18) + chip(470, 540, "REST APIs", G, 18)
    s += win(700, 110, 430, 250, "about.php")
    for i, (k, v) in enumerate([("role", "Software Engineer"), ("company", "Technyx"), ("city", "Karachi, PK"), ("focus", "Backend & APIs")]):
        s += t(724, 184 + i * 40, f"${k}", 16, C, 500, True) + t(850, 184 + i * 40, f'= "{v}";', 16, G, 500, True)
    s += chip(700, 400, "● Open to new projects", G, 17) + chip(700, 452, "3+ years in production", V, 17) + chip(700, 504, "Remote · worldwide", C, 17)
    return base(s, u)


IMAGES = {
    "fincore-ledger": ledger, "my-store-ecommerce": store, "practical-subscriptions": practical,
    "wordpress-revamp": wordpress, "shopify-store": shopify, "payment-gateways": payments,
    "laravel-code": code, "rest-api": api, "database-schema": db, "about": about,
}

if __name__ == "__main__":
    os.makedirs(os.path.join(OUT, "covers"), exist_ok=True)
    for i, (name, fn) in enumerate(IMAGES.items()):
        with open(os.path.join(OUT, "covers", name + ".svg"), "w") as f:
            f.write(fn(str(i)))
    print("wrote", len(IMAGES), "covers")
