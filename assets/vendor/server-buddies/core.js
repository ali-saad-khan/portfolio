import { ACCESSORIES, CHARACTERS, CHARACTER_IDS, characterMarkup } from "./characters.js";
import { CSS, STYLE_ID } from "./styles.js";

const isBrowser = typeof window !== "undefined" && typeof document !== "undefined";
const clamp = (v, min, max) => Math.max(min, Math.min(max, v));

export const ACTIONS = ["eyes", "swing", "drag", "boop", "combos", "idle", "sleep", "hover", "timeOfDay", "effects"];
export const HANG_STYLES = ["rope", "chain", "spring", "thread", "balloon", "none"];
export const POSITIONS = ["top-right", "top-left", "top-center", "bottom-right", "bottom-left", "bottom-center"];
export const MOODS = ["happy", "curious", "down"];

// Pendulum physics per tether: k = spring stiffness, damp = damping, max = max swing (deg).
const HANG = {
  rope: { len: 150, k: 14, damp: 0.9, max: 60 },
  chain: { len: 150, k: 18, damp: 1.5, max: 48 },
  spring: { len: 120, k: 14, damp: 0.5, max: 55, bounce: true },
  thread: { len: 210, k: 8, damp: 0.3, max: 75 },
  balloon: { len: 90, k: 8, damp: 0.6, max: 40 },
  none: { len: 0, k: 40, damp: 3, max: 9 }
};

const DEFAULT_MESSAGES = {
  boop: ["Beep!", "Boop!", "Hi there!", "Ping!", "200 OK"],
  hello: "Here we go!",
  ouch: "Ouch!",
  celebrate: "Looking healthy!",
  panic: "Mayday!",
  paste: "Got it!",
  throw: "Wheee!",
  spin: "Wheee!",
  fall: "Whoa!!",
  recover: "Phew!",
  watch: "Hmm… {time}?"
};

const CONFETTI_COLORS = ["#0058c3", "#22c55e", "#f59e0b", "#ec4899", "#38bdf8"];
const CONFETTI = Array.from({ length: 22 }, (_, i) => ({
  x: ((i * 37) % 120) - 60,
  delay: (i % 7) * 0.07,
  rotate: (i * 53) % 360,
  size: 5 + (i % 3) * 2,
  color: CONFETTI_COLORS[i % CONFETTI_COLORS.length]
}));

// ---------- colour helpers ----------
function parseHex(c) {
  if (typeof c !== "string") return null;
  let h = c.trim().replace(/^#/, "");
  if (h.length === 3) h = h.split("").map((x) => x + x).join("");
  if (!/^[0-9a-f]{6}$/i.test(h)) return null;
  return [0, 2, 4].map((i) => parseInt(h.slice(i, i + 2), 16));
}
function mix(hex, target, amount) {
  const a = parseHex(hex);
  if (!a) return hex;
  const out = a.map((v, i) => Math.round(v + (target[i] - v) * amount));
  return "#" + out.map((v) => v.toString(16).padStart(2, "0")).join("");
}
function buildPalette(ch, o) {
  const base = { ...ch.colors, ...(o.color ? { main: o.color } : {}), ...(o.colors || {}) };
  return {
    main: base.main,
    dark: base.dark || mix(base.main, [0, 0, 0], 0.3),
    light: base.light || mix(base.main, [255, 255, 255], 0.55),
    shell: base.shell,
    screen: base.screen,
    balloon: base.balloon || "#f43f5e"
  };
}

// ---------- option handling ----------
function normaliseActions(actions) {
  const out = {};
  if (Array.isArray(actions)) {
    for (const a of ACTIONS) out[a] = actions.includes(a);
  } else {
    for (const a of ACTIONS) out[a] = !(actions && actions[a] === false);
  }
  return out;
}

export function resolveOptions(raw = {}) {
  const character = CHARACTER_IDS.includes(raw.character) ? raw.character : "server";
  const position = POSITIONS.includes(raw.position) ? raw.position : "top-right";
  const bottom = position.startsWith("bottom");
  let hang = HANG_STYLES.includes(raw.hang) ? raw.hang : "rope";
  if (bottom) hang = "none";
  const size = clamp(Number(raw.size) || 104, 40, 400);
  const offset = typeof raw.offset === "number" ? { x: raw.offset, y: 0 } : { x: 28, y: 0, ...(raw.offset || {}) };
  return {
    ...raw,
    character,
    position,
    hang,
    size,
    offset,
    length: Number.isFinite(raw.length) ? clamp(raw.length, 0, 2000) : HANG[hang].len,
    accessory: ACCESSORIES.includes(raw.accessory) ? raw.accessory : "auto",
    zIndex: raw.zIndex ?? 40,
    hideBelow: Number(raw.hideBelow) || 0,
    mood: MOODS.includes(raw.mood) ? raw.mood : "happy",
    sleepAfter: raw.sleepAfter ?? 15000,
    idleAfter: raw.idleAfter ?? 7000,
    label: raw.label ?? "Server buddy: click to boop, drag to swing",
    injectStyles: raw.injectStyles !== false,
    actions: normaliseActions(raw.actions),
    messages: { ...DEFAULT_MESSAGES, ...(raw.messages || {}) }
  };
}

export function ensureStyles() {
  if (!isBrowser || document.getElementById(STYLE_ID)) return;
  const el = document.createElement("style");
  el.id = STYLE_ID;
  el.textContent = CSS;
  document.head.appendChild(el);
}

function paletteStyle(p) {
  return `--sb-main:${p.main};--sb-dark:${p.dark};--sb-light:${p.light};--sb-shell:${p.shell};--sb-screen:${p.screen};--sb-balloon:${p.balloon}`;
}

// ---------- tether artwork ----------
function tetherMarkup(hang, len) {
  if (hang === "none" || len <= 0) return "";
  if (hang === "rope") return `<span class="sb-tether sb-tether-rope" style="height:${len}px" aria-hidden="true"></span>`;
  if (hang === "thread") return `<span class="sb-tether sb-tether-thread" style="height:${len}px" aria-hidden="true"></span>`;
  if (hang === "chain") {
    let links = "";
    for (let i = 0, y = 6; y < len; i++, y += 9) {
      links +=
        i % 2
          ? `<ellipse cx="8" cy="${y}" rx="1.7" ry="6" fill="#64748b"/>`
          : `<ellipse cx="8" cy="${y}" rx="4.6" ry="6" fill="none" stroke="#94a3b8" stroke-width="2.2"/>`;
    }
    return `<svg class="sb-tether sb-tether-svg" width="16" height="${len}" viewBox="0 0 16 ${len}" aria-hidden="true">${links}</svg>`;
  }
  if (hang === "spring") {
    let d = "M11 0";
    for (let y = 0; y + 12 <= len; y += 12) d += `Q22 ${y + 3} 11 ${y + 6}Q0 ${y + 9} 11 ${y + 12}`;
    return `<svg class="sb-tether sb-tether-svg" width="22" height="${len}" viewBox="0 0 22 ${len}" preserveAspectRatio="none" aria-hidden="true"><path d="${d}" fill="none" stroke="#94a3b8" stroke-width="2.6" stroke-linecap="round"/></svg>`;
  }
  if (hang === "balloon") {
    return `<span class="sb-tether sb-tether-balloon" aria-hidden="true">
      <svg class="sb-balloon" viewBox="0 0 60 76"><path d="M30 2C9 2 2 21 4 36C6 52 20 64 30 66C40 64 54 52 56 36C58 21 51 2 30 2Z" style="fill:var(--sb-balloon)"/>
      <path d="M30 66l-5 8h10z" style="fill:var(--sb-balloon)"/><ellipse cx="19" cy="22" rx="5" ry="9" fill="#fff" opacity=".35" transform="rotate(20 19 22)"/></svg>
      <span class="sb-balloon-string" style="height:${len}px"></span></span>`;
  }
  return "";
}

// Static preview (used by the docs configurator). Safe to call during SSR.
export function renderPreview(character, options = {}) {
  const ch = CHARACTERS[character] || CHARACTERS.server;
  const o = resolveOptions({ ...options, character: ch.id });
  const p = buildPalette(ch, o);
  const S = { state: options.state || "happy", eyesClosed: false, squint: false, idleAct: "", nervous: false, led: "#22c55e" };
  if (S.state === "down") S.led = "#ef4444";
  else if (S.state === "curious") S.led = "#f59e0b";
  const acc = o.accessory === "auto" ? "none" : o.accessory;
  ensureStyles();
  return `<svg class="sb-svg sb-static" viewBox="0 0 160 120" role="img" aria-label="${ch.name} character" style="${paletteStyle(p)};overflow:visible">${characterMarkup(ch, S, acc)}</svg>`;
}

function noopHandle() {
  const fn = () => {};
  return {
    el: null, update: fn, say: fn, setMood: fn, celebrate: fn, panic: fn, flinch: fn, pass: fn, nod: fn,
    nervous: fn, boop: fn, sleep: fn, wake: fn, show: fn, hide: fn, destroy: fn
  };
}

// ---------- public factory ----------
export function createBuddy(userOptions = {}) {
  if (!isBrowser) return noopHandle();

  let raw = { ...userOptions };
  let inst = mountInstance(resolveOptions(raw));
  let destroyed = false;

  const call = (name) => (...args) => (destroyed ? undefined : inst[name](...args));
  const handle = {
    get el() {
      return destroyed ? null : inst.root;
    },
    update(patch = {}) {
      if (destroyed) return;
      raw = { ...raw, ...patch };
      const carry = { mood: inst.S.mood, hidden: inst.isHidden() };
      inst.destroy();
      inst = mountInstance(resolveOptions({ ...raw, mood: "mood" in patch ? patch.mood : carry.mood }));
      if (carry.hidden) inst.hide();
    },
    say: call("say"),
    setMood: call("setMood"),
    celebrate: call("celebrate"),
    panic: call("panic"),
    flinch: call("flinch"),
    pass: call("pass"),
    nod: call("nod"),
    nervous: call("nervous"),
    boop: call("boop"),
    sleep: call("sleep"),
    wake: call("wake"),
    show: call("show"),
    hide: call("hide"),
    destroy() {
      if (destroyed) return;
      destroyed = true;
      inst.destroy();
    }
  };
  return handle;
}

// ---------- one mounted buddy ----------
function mountInstance(o) {
  const ch = CHARACTERS[o.character];
  const A = o.actions;
  const H = HANG[o.hang];
  const palette = buildPalette(ch, o);
  if (o.injectStyles) ensureStyles();

  const timers = new Set();
  const later = (fn, ms) => {
    const id = setTimeout(() => {
      timers.delete(id);
      fn();
    }, ms);
    timers.add(id);
    return id;
  };

  // state
  const S = {
    mood: o.mood,
    sleeping: false,
    idleAct: "",
    squint: false,
    typing: false,
    nod: false,
    flinch: false,
    pass: false,
    nervous: false,
    fx: "",
    combo: "",
    period: "day"
  };
  const phys = { angle: 0, velocity: 0, y: 0, vy: 0, running: false, last: 0, lastX: null };
  const drag = { active: false, moved: false, startX: 0, startY: 0, lastAngle: 0, lastT: 0, velocity: 0 };
  let pupilOffset = "translate(0px, 0px)";
  let aimFrame = 0;
  let reduceMotion = false;
  let lastActive = Date.now();
  let nextActAt = 0;
  let typingUntil = 0;
  let typingTimer = 0;
  let hoverTimer = 0;
  let suppressClick = false;
  let clicks = [];
  let clickCount = 0;
  let lastBubbleAt = 0;
  let apiHidden = false;
  let mqHidden = false;
  let lastMarkup = "";
  let alive = true;

  // ----- DOM -----
  const pos = o.position;
  const mountEl = typeof o.mount === "string" ? document.querySelector(o.mount) : o.mount || null;
  const root = document.createElement("div");
  root.className = "sb-hanger" + (mountEl ? " sb-in-mount" : "");
  root.setAttribute("data-server-buddy", o.character);
  root.setAttribute("data-hang", o.hang);
  root.setAttribute("data-pivot", pos.startsWith("bottom") || o.hang === "none" ? "bottom" : "top");
  root.setAttribute("data-side", pos.endsWith("left") ? "right" : "left");
  root.style.cssText = paletteStyle(palette);
  root.style.width = `${o.size}px`;
  root.style.zIndex = String(o.zIndex);
  const topSide = pos.startsWith("top");
  const yOff = o.offset.y + (topSide && o.hang === "none" ? 12 : 0);
  root.style[topSide ? "top" : "bottom"] = `${yOff}px`;
  if (pos.endsWith("right")) root.style.right = `${o.offset.x}px`;
  else if (pos.endsWith("left")) root.style.left = `${o.offset.x}px`;
  else {
    root.style.left = "50%";
    root.style.marginLeft = `${-o.size / 2}px`;
  }

  root.innerHTML = `<div class="sb-sway"><div class="sb-swing">${tetherMarkup(o.hang, o.length)}<div class="sb-drop"><button type="button" class="sb-buddy"><span class="sb-bubble" aria-hidden="true"></span><span class="sb-fxlayer" aria-hidden="true"></span><svg class="sb-svg" viewBox="0 0 160 120" aria-hidden="true"></svg></button></div></div></div>`;

  const swing = root.querySelector(".sb-swing");
  const dropEl = root.querySelector(".sb-drop");
  const tetherEl = root.querySelector(".sb-tether");
  const buddy = root.querySelector(".sb-buddy");
  const bubble = root.querySelector(".sb-bubble");
  const fxLayer = root.querySelector(".sb-fxlayer");
  const svg = root.querySelector(".sb-svg");
  let pupilsEl = null;

  buddy.setAttribute("data-drag", A.drag && H.len > 0 ? "on" : "off");
  buddy.setAttribute("data-boop", A.boop ? "on" : "off");
  if (A.boop || A.drag) buddy.setAttribute("aria-label", o.label);
  else {
    buddy.setAttribute("aria-hidden", "true");
    buddy.tabIndex = -1;
  }

  let restoreMountPosition = null;
  if (mountEl) {
    if (getComputedStyle(mountEl).position === "static") {
      restoreMountPosition = mountEl.style.position;
      mountEl.style.position = "relative";
    }
    mountEl.appendChild(root);
  } else {
    document.body.appendChild(root);
  }

  // ----- painting -----
  const derivedState = () => (S.mood === "down" ? "down" : S.sleeping ? "sleeping" : S.mood === "curious" || S.typing ? "curious" : "happy");

  function paint() {
    if (!alive) return;
    const state = derivedState();
    const isDown = state === "down";
    const eyesClosed = state === "sleeping" || (S.idleAct === "yawn" && !isDown);
    const led = isDown ? "#ef4444" : state === "curious" ? "#f59e0b" : "#22c55e";
    const view = {
      state,
      eyesClosed,
      squint: S.squint,
      idleAct: S.idleAct,
      nervous: S.nervous && !isDown,
      led
    };
    const acc = o.accessory === "auto" ? (A.timeOfDay && S.period === "night" ? "nightcap" : "none") : o.accessory;

    buddy.dataset.state = state;
    buddy.dataset.act = S.idleAct;
    buddy.dataset.fx = S.fx;
    buddy.dataset.combo = S.combo;
    buddy.dataset.period = A.timeOfDay ? S.period : "day";
    svg.classList.toggle("sb-flinch", S.flinch);
    svg.classList.toggle("sb-pass", S.pass);
    svg.classList.toggle("sb-nod", S.nod);
    svg.classList.toggle("sb-nervous", view.nervous);

    const markup = characterMarkup(ch, view, acc);
    if (markup !== lastMarkup) {
      lastMarkup = markup;
      svg.innerHTML = markup;
      pupilsEl = svg.querySelector(".sb-pupils");
      if (pupilsEl) pupilsEl.style.transform = pupilOffset;
    }
  }

  function renderFx() {
    if (S.fx === "celebrate") {
      const colors = [palette.main, ...CONFETTI_COLORS.slice(1)];
      fxLayer.innerHTML =
        `<span class="sb-confetti">` +
        CONFETTI.map(
          (c, i) =>
            `<i style="--x:${c.x}px;--r:${c.rotate}deg;width:${c.size}px;height:${c.size}px;background:${colors[i % colors.length]};animation-delay:${c.delay}s"></i>`
        ).join("") +
        `</span>`;
    } else if (S.fx === "panic") {
      fxLayer.innerHTML = `<span class="sb-alarm"></span>`;
    } else {
      fxLayer.innerHTML = "";
    }
  }

  function set(patch) {
    let changed = false;
    for (const k in patch) {
      if (S[k] !== patch[k]) {
        S[k] = patch[k];
        changed = true;
      }
    }
    if (changed) paint();
  }

  function say(text) {
    if (!alive || !text) return;
    lastBubbleAt = Date.now();
    bubble.textContent = text;
    bubble.classList.remove("sb-bubble-show");
    void bubble.offsetWidth; // restart the animation
    bubble.classList.add("sb-bubble-show");
  }

  // ----- physics -----
  function applyBounce() {
    if (!H.bounce) return;
    dropEl.style.transform = `translateY(${phys.y}px)`;
    if (tetherEl) tetherEl.style.transform = `scaleY(${(o.length + phys.y) / Math.max(o.length, 1)})`;
  }

  function step(now) {
    if (!alive) return;
    if (drag.moved) {
      phys.running = false;
      return;
    }
    const dt = Math.min((now - phys.last) / 1000, 0.04);
    phys.last = now;
    phys.velocity += (-H.k * phys.angle - H.damp * phys.velocity) * dt;
    phys.angle = clamp(phys.angle + phys.velocity * dt, -H.max, H.max);
    swing.style.transform = `rotate(${phys.angle}deg)`;

    let settledY = true;
    if (H.bounce) {
      phys.vy += (-70 * phys.y - 3.2 * phys.vy) * dt;
      phys.y = clamp(phys.y + phys.vy * dt, -30, 60);
      applyBounce();
      settledY = Math.abs(phys.y) < 0.05 && Math.abs(phys.vy) < 0.5;
    }

    if (Math.abs(phys.angle) < 0.05 && Math.abs(phys.velocity) < 0.3 && settledY) {
      phys.angle = phys.velocity = phys.y = phys.vy = 0;
      swing.style.transform = "";
      if (H.bounce) {
        dropEl.style.transform = "";
        if (tetherEl) tetherEl.style.transform = "";
      }
      phys.running = false;
      return;
    }
    requestAnimationFrame(step);
  }

  function kick(impulse, bounceImpulse = 0) {
    if (reduceMotion || !A.swing) return;
    phys.velocity = clamp(phys.velocity + impulse, -400, 400);
    if (H.bounce) phys.vy = clamp(phys.vy + bounceImpulse, -300, 300);
    if (!phys.running) {
      phys.running = true;
      phys.last = performance.now();
      requestAnimationFrame(step);
    }
  }

  // ----- eyes -----
  function aimAt(x, y) {
    const rect = svg.getBoundingClientRect();
    const dx = x - (rect.left + rect.width / 2);
    const dy = y - (rect.top + rect.height * 0.3);
    const distance = Math.hypot(dx, dy) || 1;
    const strength = Math.min(distance / 220, 1) * 3.5;
    pupilOffset = `translate(${(dx / distance) * strength}px, ${(dy / distance) * strength}px)`;
    if (pupilsEl) pupilsEl.style.transform = pupilOffset;
  }

  function markActive() {
    lastActive = Date.now();
    if (S.sleeping) set({ sleeping: false });
  }

  // ----- events -----
  const mq = window.matchMedia ? window.matchMedia("(prefers-reduced-motion: reduce)") : null;
  const syncReduce = () => {
    reduceMotion = Boolean(mq && mq.matches);
  };
  syncReduce();
  mq && mq.addEventListener && mq.addEventListener("change", syncReduce);

  const matches = (el, sel) => Boolean(sel && el instanceof Element && el.matches(sel));

  const onPointerMove = (event) => {
    markActive();

    if (drag.active) {
      if (!drag.moved && Math.hypot(event.clientX - drag.startX, event.clientY - drag.startY) > 6) {
        drag.moved = true;
        phys.velocity = 0;
        drag.lastAngle = phys.angle;
        drag.lastT = performance.now();
        buddy.classList.add("sb-grabbed");
      }
      if (drag.moved) {
        const box = root.getBoundingClientRect();
        const angle = clamp((Math.atan2(event.clientX - (box.left + box.width / 2), event.clientY - box.top) * 180) / Math.PI, -55, 55);
        const now = performance.now();
        const dt = Math.max((now - drag.lastT) / 1000, 0.001);
        drag.velocity = drag.velocity * 0.6 + ((angle - drag.lastAngle) / dt) * 0.4;
        drag.lastAngle = angle;
        drag.lastT = now;
        phys.angle = angle;
        swing.style.transform = `rotate(${angle}deg)`;
      }
      return;
    }

    if (A.eyes) {
      const target = o.lookAt && event.target instanceof Element ? event.target.closest(o.lookAt) : null;
      if (target) {
        const r = target.getBoundingClientRect();
        aimAt(r.left + r.width / 2, r.top + r.height / 2);
      } else if (Date.now() > typingUntil) {
        cancelAnimationFrame(aimFrame);
        aimFrame = requestAnimationFrame(() => aimAt(event.clientX, event.clientY));
      }
    }

    if (A.swing && phys.lastX !== null) {
      const box = buddy.getBoundingClientRect();
      const dist = Math.hypot(event.clientX - (box.left + box.width / 2), event.clientY - (box.top + box.height / 2));
      const reach = 170 * (o.size / 104);
      if (dist < reach) kick(clamp(event.clientX - phys.lastX, -30, 30) * 1.4 * (1 - dist / reach));
    }
    phys.lastX = event.clientX;
  };

  const endDrag = () => {
    if (!drag.active) return;
    const wasThrown = drag.moved;
    drag.active = false;
    buddy.classList.remove("sb-grabbed");
    if (wasThrown) {
      suppressClick = true;
      later(() => (suppressClick = false), 50);
      drag.moved = false;
      const speed = clamp(drag.velocity, -400, 400);
      drag.velocity = 0;
      kick(speed);
      if (A.boop && Math.abs(speed) > 120) say(o.messages.throw);
    }
  };

  const caretAim = (input) => {
    const rect = input.getBoundingClientRect();
    const caret = input.selectionStart ?? (input.value || "").length;
    aimAt(rect.left + Math.min(rect.width - 24, 8 + caret * 8.6), rect.top + rect.height / 2);
  };
  const onInput = (event) => {
    if (!A.eyes || !matches(event.target, o.watchInput)) return;
    markActive();
    typingUntil = Date.now() + 1800;
    caretAim(event.target);
    set({ typing: true });
    clearTimeout(typingTimer);
    typingTimer = setTimeout(() => set({ typing: false }), 350);
  };
  const onFocusIn = (event) => {
    if (!A.eyes || !matches(event.target, o.watchInput)) return;
    markActive();
    typingUntil = Date.now() + 1500;
    caretAim(event.target);
  };
  const onPaste = (event) => {
    if (!matches(event.target, o.watchInput)) return;
    set({ nod: true });
    say(o.messages.paste);
    later(() => set({ nod: false }), 700);
  };

  let lastScrollY = window.scrollY;
  const onScroll = () => {
    const dy = window.scrollY - lastScrollY;
    lastScrollY = window.scrollY;
    markActive();
    if (Math.abs(dy) < 8) return;
    kick(clamp(dy, -60, 60) * 0.6, clamp(dy, -60, 60) * 1.6);
    if (A.eyes) {
      const box = buddy.getBoundingClientRect();
      aimAt(box.left + box.width / 2, box.top + box.height / 2 + (dy > 0 ? 300 : -300));
    }
  };
  const onKeyDown = () => markActive();

  const tick = setInterval(() => {
    const now = Date.now();
    const idle = now - lastActive;
    if (A.sleep && idle > o.sleepAfter) {
      set({ sleeping: true, idleAct: "" });
      return;
    }
    if (A.idle && idle > o.idleAfter && now > nextActAt && S.mood !== "down" && !reduceMotion && !drag.active) {
      const acts = ["yawn", "watch", "dance"];
      const act = acts[Math.floor(Math.random() * acts.length)];
      nextActAt = now + 5000 + Math.random() * 3000;
      set({ idleAct: act });
      if (act === "watch") {
        const time = new Date().toLocaleTimeString([], { hour: "numeric", minute: "2-digit" });
        say(o.messages.watch.replace("{time}", time));
      }
      later(() => set({ idleAct: "" }), 2400);
    }
  }, 1000);

  window.addEventListener("pointermove", onPointerMove, { passive: true });
  window.addEventListener("pointerup", endDrag);
  window.addEventListener("pointercancel", endDrag);
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("keydown", onKeyDown, { passive: true });
  if (o.watchInput) {
    document.addEventListener("input", onInput, true);
    document.addEventListener("focusin", onFocusIn, true);
    document.addEventListener("paste", onPaste, true);
  }

  // button interactions
  const onClick = () => {
    if (suppressClick || !A.boop) return;
    doBoop();
  };
  const onPointerDown = (event) => {
    if (!A.drag || H.len <= 0) return;
    if (event.button !== 0 && event.pointerType === "mouse") return;
    drag.active = true;
    drag.moved = false;
    drag.startX = event.clientX;
    drag.startY = event.clientY;
    drag.velocity = 0;
  };
  const onEnter = () => {
    if (!A.hover) return;
    clearTimeout(hoverTimer);
    hoverTimer = setTimeout(() => set({ squint: true }), 1100);
  };
  const onLeave = () => {
    clearTimeout(hoverTimer);
    set({ squint: false });
  };
  buddy.addEventListener("click", onClick);
  buddy.addEventListener("pointerdown", onPointerDown);
  buddy.addEventListener("pointerenter", onEnter);
  buddy.addEventListener("pointerleave", onLeave);

  // hide on small viewports
  let hideMq = null;
  const onHideMq = () => {
    mqHidden = Boolean(hideMq && hideMq.matches);
    root.hidden = apiHidden || mqHidden;
  };
  if (o.hideBelow > 0 && window.matchMedia) {
    hideMq = window.matchMedia(`(max-width:${o.hideBelow - 1}px)`);
    hideMq.addEventListener && hideMq.addEventListener("change", onHideMq);
    onHideMq();
  }

  // ----- behaviours -----
  function doBoop() {
    markActive();
    clickCount += 1;
    kick(clickCount % 2 ? 110 : -110, 120);

    const now = Date.now();
    clicks = clicks.filter((t) => now - t < 3500);
    clicks.push(now);
    const n = clicks.length;

    if (A.combos && n >= 10 && !reduceMotion) {
      clicks = [];
      set({ combo: "fall" });
      say(o.messages.fall);
      later(() => {
        set({ combo: "" });
        say(o.messages.recover);
      }, 3300);
      return;
    }
    if (A.combos && n === 5 && !reduceMotion) {
      set({ combo: "spin" });
      say(o.messages.spin);
      later(() => set({ combo: "" }), 900);
      return;
    }
    const list = o.messages.boop;
    say(S.mood === "down" ? o.messages.ouch : list[clickCount % list.length]);
  }

  function celebrate() {
    kick(90);
    say(o.messages.celebrate);
    if (reduceMotion || !A.effects) return;
    set({ fx: "celebrate" });
    renderFx();
    later(() => {
      set({ fx: "" });
      renderFx();
    }, 3200);
  }
  function panic() {
    kick(160);
    say(o.messages.panic);
    if (reduceMotion || !A.effects) return;
    set({ fx: "panic" });
    renderFx();
    later(() => {
      set({ fx: "" });
      renderFx();
    }, 3600);
  }
  function flinch() {
    set({ flinch: true });
    later(() => set({ flinch: false }), 500);
    if (Date.now() - lastBubbleAt > 1500) say(o.messages.ouch);
  }
  function pass() {
    set({ pass: true });
    later(() => set({ pass: false }), 300);
  }
  function nod() {
    set({ nod: true });
    later(() => set({ nod: false }), 700);
  }

  // time of day
  if (A.timeOfDay) {
    const hour = new Date().getHours();
    S.period = hour >= 21 || hour < 5 ? "night" : hour < 9 ? "morning" : "day";
  }

  paint();

  const api = {
    root,
    S,
    say,
    setMood(mood) {
      if (MOODS.includes(mood)) set({ mood });
    },
    celebrate,
    panic,
    flinch,
    pass,
    nod,
    nervous(on = true) {
      set({ nervous: Boolean(on) });
    },
    boop: doBoop,
    sleep() {
      set({ sleeping: true, idleAct: "" });
    },
    wake: markActive,
    show() {
      apiHidden = false;
      root.hidden = mqHidden;
    },
    hide() {
      apiHidden = true;
      root.hidden = true;
    },
    isHidden: () => apiHidden,
    destroy() {
      if (!alive) return;
      alive = false;
      clearInterval(tick);
      clearTimeout(typingTimer);
      clearTimeout(hoverTimer);
      timers.forEach(clearTimeout);
      timers.clear();
      cancelAnimationFrame(aimFrame);
      mq && mq.removeEventListener && mq.removeEventListener("change", syncReduce);
      hideMq && hideMq.removeEventListener && hideMq.removeEventListener("change", onHideMq);
      window.removeEventListener("pointermove", onPointerMove);
      window.removeEventListener("pointerup", endDrag);
      window.removeEventListener("pointercancel", endDrag);
      window.removeEventListener("scroll", onScroll);
      window.removeEventListener("keydown", onKeyDown);
      document.removeEventListener("input", onInput, true);
      document.removeEventListener("focusin", onFocusIn, true);
      document.removeEventListener("paste", onPaste, true);
      root.remove();
      if (restoreMountPosition !== null && mountEl) mountEl.style.position = restoreMountPosition;
    }
  };
  return api;
}
