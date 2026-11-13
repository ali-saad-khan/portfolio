/* "Bit": a little server bot that crawls down a zig-zag trace as you scroll.
   Original code and artwork. Scroll progress maps to a point on an SVG path; the bot walks down,
   climbs back up, waves when you pause, drops code glyphs behind it and pokes the page as it passes.
   Desktop only, off for reduced motion, built with DOM APIs only so it works under the strict CSP. */
"use strict";

const NS = "http://www.w3.org/2000/svg";
const el = (tag, attrs = {}, parent) => {
  const n = document.createElementNS(NS, tag);
  for (const k in attrs) n.setAttribute(k, attrs[k]);
  if (parent) parent.appendChild(n);
  return n;
};

export function initRider() {
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const wide = window.matchMedia("(min-width: 900px)");
  if (reduced || !wide.matches || document.getElementById("bitThread")) return;

  /* ---- the trace (viewBox 100 x 1000, stretched over the whole document) ---- */
  const D = "M 6 0 C 6 36, 8 62, 22 84 C 42 112, 82 106, 92 132 C 100 156, 70 176, 44 190 " +
    "C 18 204, 6 226, 14 250 C 24 280, 72 276, 90 302 C 100 326, 66 346, 40 360 C 16 374, 6 398, 16 420 " +
    "C 28 448, 74 446, 90 472 C 100 496, 66 514, 42 528 C 18 542, 8 566, 18 588 C 30 614, 76 614, 90 640 " +
    "C 100 664, 68 682, 44 696 C 20 710, 8 734, 18 756 C 30 782, 76 782, 90 808 C 100 832, 68 850, 44 864 " +
    "C 20 878, 8 902, 18 924 C 30 950, 72 954, 88 976 C 94 986, 92 994, 90 1000";
  const thread = document.createElement("div");
  thread.id = "bitThread"; thread.className = "bit-thread"; thread.setAttribute("aria-hidden", "true");
  const tsvg = el("svg", { viewBox: "0 0 100 1000", preserveAspectRatio: "none" }, thread);
  const path = el("path", { d: D }, tsvg);

  /* ---- the bot: three poses sharing one body ---- */
  const layer = document.createElement("div");
  layer.className = "bit-layer"; layer.setAttribute("aria-hidden", "true");
  const rider = document.createElement("span");
  rider.className = "bit"; rider.dataset.pose = "walk";
  layer.appendChild(rider);

  const body = (svg) => {
    el("line", { x1: 44, y1: 8, x2: 40, y2: 0, class: "bit-ant" }, svg);
    el("circle", { cx: 40, cy: 0, r: 3, class: "bit-led" }, svg);
    el("rect", { x: 20, y: 8, width: 48, height: 52, rx: 9, class: "bit-shell" }, svg);
    el("rect", { x: 27, y: 15, width: 34, height: 26, rx: 5, class: "bit-screen" }, svg);
    el("rect", { x: 33, y: 22, width: 5, height: 8, rx: 1, class: "bit-eye" }, svg);
    el("rect", { x: 50, y: 22, width: 5, height: 8, rx: 1, class: "bit-eye" }, svg);
    el("path", { d: "M36 35 H52", class: "bit-mouth" }, svg);
    el("rect", { x: 28, y: 46, width: 6, height: 3, rx: 1.5, class: "bit-vent" }, svg);
    el("rect", { x: 38, y: 46, width: 6, height: 3, rx: 1.5, class: "bit-vent" }, svg);
    el("rect", { x: 48, y: 46, width: 6, height: 3, rx: 1.5, class: "bit-vent" }, svg);
  };
  const limb = (svg, d, cls = "bit-limb") => el("path", { d, class: cls }, svg);
  const mk = (pose) => {
    const svg = el("svg", { viewBox: "-6 -6 100 90", width: 92, height: 82, class: "bit-pose bit-pose--" + pose });
    body(svg);
    if (pose === "walk") { limb(svg, "M32 60 L26 76 M56 60 L64 74"); limb(svg, "M20 34 L8 44 M68 34 L82 28"); }
    if (pose === "climb") { limb(svg, "M34 60 L30 76 M54 60 L58 74"); limb(svg, "M22 30 L10 12 M66 30 L78 12"); el("circle", { cx: 10, cy: 12, r: 3, class: "bit-grip" }, svg); el("circle", { cx: 78, cy: 12, r: 3, class: "bit-grip" }, svg); }
    if (pose === "wave") { limb(svg, "M34 60 L32 76 M54 60 L56 76"); limb(svg, "M20 34 L8 46"); const g = el("g", { class: "bit-arm" }, svg); limb(g, "M68 32 L82 8"); }
    rider.appendChild(svg);
  };
  ["walk", "climb", "wave"].forEach(mk);

  /* wake: code glyphs dropped behind the bot */
  const GLYPHS = ["{ }", "</>", ";", "0x", "=>"];
  const wakes = GLYPHS.slice(0, 4).map((g) => {
    const s = document.createElement("span");
    s.className = "bit-wake"; s.textContent = g; layer.appendChild(s); return s;
  });

  document.body.appendChild(thread);
  document.body.appendChild(layer);
  document.documentElement.classList.add("has-bit");

  /* ---- sample the path once ---- */
  const total = path.getTotalLength();
  const N = 400, pts = new Array((N + 1) * 2);
  for (let i = 0; i <= N; i++) { const p = path.getPointAtLength(total * i / N); pts[i * 2] = p.x; pts[i * 2 + 1] = p.y; }
  const at = (g) => {
    const f = g * N, i = Math.min(N - 1, Math.floor(f)), t = f - i;
    return { x: pts[i * 2] + (pts[i * 2 + 2] - pts[i * 2]) * t, y: pts[i * 2 + 1] + (pts[i * 2 + 3] - pts[i * 2 + 1]) * t };
  };

  /* soft blip, only after a real user gesture */
  let actx = null;
  ["pointerdown", "keydown", "touchstart"].forEach((ev) =>
    window.addEventListener(ev, () => { if (actx) return; try { const AC = window.AudioContext || window.webkitAudioContext; if (AC) actx = new AC(); } catch (e) { actx = null; } }, { once: true, passive: true }));
  const blip = () => {
    if (!actx) return;
    try {
      if (actx.state === "suspended") actx.resume();
      const t = actx.currentTime, o = actx.createOscillator(), g = actx.createGain();
      o.type = "square"; o.frequency.setValueAtTime(520, t); o.frequency.setValueAtTime(780, t + 0.06);
      g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(0.03, t + 0.01); g.gain.exponentialRampToValueAtTime(0.0001, t + 0.2);
      o.connect(g); g.connect(actx.destination); o.start(t); o.stop(t + 0.22);
    } catch (e) { /* silent */ }
  };
  const pulse = (n, c, ms) => { if (!n) return; n.classList.remove(c); void n.offsetWidth; n.classList.add(c); setTimeout(() => n.classList.remove(c), ms); };

  /* ---- reactions: selector -> what happens when the bot passes ---- */
  const RULES = [
    { sel: ".hero-title .highlight", pad: 30, xfree: true, fire: (n) => { pulse(n, "bitr-wobble", 900); blip(); } },
    { sel: ".ledger", pad: 0, xfree: true, fire: (n) => pulse(n, "bitr-flash", 1000) },
    { sel: ".stat-card", pad: 0, xfree: true, fire: (n) => pulse(n, "bitr-pop", 700) },
    { sel: ".skill-category", pad: 0, xfree: true, fire: (n) => pulse(n, "bitr-pop", 700) },
    { sel: ".project-card", pad: 0, xfree: true, fire: (n) => { pulse(n, "bitr-tilt", 900); blip(); } },
    { sel: ".service-card", pad: 0, xfree: true, fire: (n) => pulse(n, "bitr-tilt", 900) },
    { sel: ".timeline-card", pad: 0, xfree: true, fire: (n) => pulse(n, "bitr-nudge", 800) },
    { sel: ".cert-card, .certificate-card", pad: 0, xfree: true, fire: (n) => pulse(n, "bitr-pop", 700) },
    { sel: ".contact-card", pad: 0, xfree: true, fire: (n) => pulse(n, "bitr-pop", 700) },
    { sel: ".form-input, .form-textarea", pad: 30, xfree: true, fire: (n) => pulse(n, "bitr-jitter", 650) },
    { sel: ".post-card, .blog-card", pad: 0, xfree: true, fire: (n) => pulse(n, "bitr-tilt", 900) },
    { sel: ".section-title", pad: 10, xfree: true, fire: (n) => pulse(n, "bitr-underline", 1200) },
  ];
  let hits = [];
  const collect = () => {
    hits = [];
    RULES.forEach((r) => document.querySelectorAll(r.sel).forEach((n) => hits.push({ box: n, pad: r.pad, xfree: r.xfree, fire: r.fire, armed: true })));
  };

  let docH = 1, vh = 1, tW = 1, tH = 1, tTop = 0, tLeft = 0, measured = 0, footTop = Infinity;
  const measure = () => {
    const sy = window.pageYOffset || 0, sx = window.pageXOffset || 0;
    docH = document.documentElement.scrollHeight; vh = window.innerHeight;
    tW = thread.offsetWidth; tH = thread.offsetHeight;
    const tr = thread.getBoundingClientRect(); tTop = tr.top + sy; tLeft = tr.left + sx;
    hits.forEach((h) => { if (!h.box.isConnected) { h.r = null; return; } const r = h.box.getBoundingClientRect(); h.r = { top: r.top + sy, bottom: r.bottom + sy, left: r.left + sx, right: r.right + sx }; });
    const f = document.querySelector(".footer"); footTop = f ? f.getBoundingClientRect().top + sy : Infinity;
    measured = performance.now();
  };
  collect(); measure();

  let prevX = null, prevY = null, prevLX = null, prevLY = null, lastProg = -1, pose = "", wi = 0, idle = null, lastX = 0;
  const setPose = (p) => { if (pose !== p) { pose = p; rider.dataset.pose = p; } };

  const place = () => {
    if (performance.now() - measured > 1000) measure();
    const sy = window.pageYOffset || 0;
    const prog = Math.max(0, Math.min(1, sy / Math.max(1, docH - vh)));
    const pt = at(prog), lx = pt.x / 100 * tW, ly = pt.y / 1000 * tH;
    /* lean into the direction of travel instead of spinning */
    const lean = Math.max(-16, Math.min(16, (lx - lastX) * 0.6)); lastX = lx;
    rider.style.transform = `translate3d(${lx.toFixed(1)}px,${ly.toFixed(1)}px,0) rotate(${lean.toFixed(1)}deg)`;
    const vx = tLeft + lx, vy = tTop + ly, vyView = vy - sy;

    if (lastProg >= 0) { if (prog > lastProg + 0.0003) setPose("walk"); else if (prog < lastProg - 0.0003) setPose("climb"); } else setPose("walk");
    lastProg = prog;
    clearTimeout(idle);
    idle = setTimeout(() => { if (vyView > 0 && vyView < vh) setPose("wave"); }, 3000);
    if (vy > footTop) setPose("wave");

    if (prevLX !== null) {
      const dx = lx - prevLX, dy = ly - prevLY;
      if (Math.hypot(dx, dy) > 42) { const w = wakes[wi]; wi = (wi + 1) % wakes.length; w.style.transform = `translate3d(${prevLX.toFixed(1)}px,${prevLY.toFixed(1)}px,0)`; w.classList.remove("is-puff"); void w.offsetWidth; w.classList.add("is-puff"); }
    }
    prevLX = lx; prevLY = ly;

    const ax = prevX === null ? vx : prevX, ay = prevY === null ? vy : prevY;
    const x0 = Math.min(ax, vx), x1 = Math.max(ax, vx), y0 = Math.min(ay, vy), y1 = Math.max(ay, vy);
    prevX = vx; prevY = vy;
    for (let j = 0; j < hits.length; j++) {
      const h = hits[j], r = h.r; if (!r || !h.box.isConnected) continue;
      const p = h.pad, inside = y1 > r.top - p && y0 < r.bottom + p && (h.xfree || (x1 > r.left - p && x0 < r.right + p));
      if (inside && h.armed) { h.armed = false; h.fire(h.box); } else if (!inside && !h.armed) h.armed = true;
    }
  };

  let tick = false;
  window.addEventListener("scroll", () => { if (!tick) { tick = true; requestAnimationFrame(() => { place(); tick = false; }); } }, { passive: true });
  window.addEventListener("resize", () => { measure(); place(); });
  window.addEventListener("load", () => { collect(); measure(); place(); });
  /* the page height changes as images and fonts land */
  if ("ResizeObserver" in window) new ResizeObserver(() => { measure(); }).observe(document.body);
  place();
}
