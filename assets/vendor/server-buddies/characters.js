// Character definitions. Every character shares one 160x120 viewBox, one face system and one
// state machine; a character only supplies its body artwork, where the face sits, and a palette.
//
// Body colours are CSS variables (--sb-main, --sb-dark, --sb-light, --sb-shell, --sb-screen) so
// `color` / `colors` options and host CSS can restyle them.

const M = 'style="fill:var(--sb-main)"';
const D = 'style="fill:var(--sb-dark)"';
const L = 'style="fill:var(--sb-light)"';
const SH = 'style="fill:var(--sb-shell)"';
const SC = 'style="fill:var(--sb-screen)"';

const led = (cx, cy, r, fill, cls = "") =>
  `<circle class="sb-led ${cls}" cx="${cx}" cy="${cy}" r="${r}" fill="${fill}"/>`;

// Face palettes: dark screens get light eyes, light bodies get outlined eyes.
const SCREEN_FACE = {
  sclera: "#f8fafc",
  scleraStroke: "",
  pupil: "#0f172a",
  line: "#e2e8f0",
  mouth: "#38bdf8",
  down: "#f87171",
  cheek: "#f472b6"
};
const BODY_FACE = {
  sclera: "#ffffff",
  scleraStroke: "#475569",
  pupil: "#0f172a",
  line: "#334155",
  mouth: "#334155",
  down: "#dc2626",
  cheek: "#fb7185"
};

export const CHARACTERS = {
  server: {
    id: "server",
    name: "Server",
    blurb: "The classic rack-mount server.",
    colors: { main: "#0058c3", shell: "#1e293b", screen: "#0b1220" },
    theme: SCREEN_FACE,
    face: { dx: 0, dy: 0, k: 1 },
    anchor: { y: 14, hw: 60, earY: 36 },
    body: (S) => `
      <line x1="80" y1="14" x2="80" y2="5" stroke="#475569" stroke-width="3" stroke-linecap="round"/>
      ${led(80, 4, 4, S.led)}
      <rect x="20" y="14" width="120" height="44" rx="13" ${SH}/>
      <rect x="28" y="20" width="104" height="32" rx="9" ${SC}/>
      <rect x="20" y="62" width="120" height="38" rx="13" ${M}/>
      <rect x="30" y="71" width="62" height="7" rx="3.5" ${D}/>
      <rect x="30" y="83" width="62" height="7" rx="3.5" ${D}/>
      ${led(108, 75, 3.2, S.led)}${led(120, 75, 3.2, "#93c5fd", "sb-led-b")}
      ${led(108, 87, 3.2, "#93c5fd", "sb-led-c")}${led(120, 87, 3.2, S.led, "sb-led-d")}
      <rect x="34" y="100" width="22" height="7" rx="3.5" fill="#334155"/>
      <rect x="104" y="100" width="22" height="7" rx="3.5" fill="#334155"/>`
  },

  robot: {
    id: "robot",
    name: "Robot",
    blurb: "Round visor, tiny arms, big opinions.",
    colors: { main: "#f97316", shell: "#e2e8f0", screen: "#0b1220" },
    theme: SCREEN_FACE,
    face: { dx: 0, dy: 1, k: 1 },
    anchor: { y: 12, hw: 56, earY: 40 },
    body: (S) => `
      <line x1="80" y1="12" x2="80" y2="5" stroke="#64748b" stroke-width="3" stroke-linecap="round"/>
      ${led(80, 4, 4.5, S.led)}
      <rect x="17" y="30" width="12" height="22" rx="6" ${D}/>
      <rect x="131" y="30" width="12" height="22" rx="6" ${D}/>
      <rect x="24" y="12" width="112" height="56" rx="26" ${SH}/>
      <rect x="34" y="20" width="92" height="40" rx="19" ${SC}/>
      <rect x="27" y="74" width="13" height="26" rx="6.5" ${D}/>
      <rect x="120" y="74" width="13" height="26" rx="6.5" ${D}/>
      <rect x="46" y="72" width="68" height="30" rx="11" ${M}/>
      <rect x="55" y="80" width="30" height="6" rx="3" ${D}/>
      <rect x="55" y="90" width="30" height="6" rx="3" ${D}/>
      ${led(98, 83, 3.4, S.led)}${led(98, 93, 3.4, "#fed7aa", "sb-led-b")}
      <rect x="50" y="102" width="24" height="7" rx="3.5" fill="#475569"/>
      <rect x="86" y="102" width="24" height="7" rx="3.5" fill="#475569"/>`
  },

  cat: {
    id: "cat",
    name: "Cat",
    blurb: "Collar tag doubles as the status light.",
    colors: { main: "#f59e0b", shell: "#fef3c7", screen: "#0b1220" },
    theme: { ...BODY_FACE, sclera: "#ffffff", scleraStroke: "", line: "#44403c", mouth: "#44403c" },
    face: { dx: 0, dy: 8, k: 1 },
    anchor: { y: 15, hw: 56, earY: 52 },
    body: (S) => `
      <path d="M112 98C142 98 148 70 134 62" fill="none" stroke-width="8" stroke-linecap="round" style="stroke:var(--sb-dark)"/>
      <ellipse cx="80" cy="92" rx="34" ry="17" ${M}/>
      <ellipse cx="62" cy="106" rx="11" ry="5" ${L}/>
      <ellipse cx="98" cy="106" rx="11" ry="5" ${L}/>
      <path d="M26 44L30 10L58 26Z" ${M}/>
      <path d="M134 44L130 10L102 26Z" ${M}/>
      <path d="M33 34L35 19L49 27Z" fill="#fbcfe8"/>
      <path d="M127 34L125 19L111 27Z" fill="#fbcfe8"/>
      <ellipse cx="80" cy="52" rx="58" ry="38" ${M}/>
      <ellipse cx="80" cy="63" rx="22" ry="14" ${L}/>
      <rect x="62" y="82" width="36" height="6" rx="3" fill="#ef4444"/>
      ${led(80, 91, 4.5, S.led)}
      <path d="M30 60H10M32 67L12 73M130 60H150M128 67L148 73" stroke="#64748b" stroke-width="2" stroke-linecap="round" fill="none"/>`
  },

  ghost: {
    id: "ghost",
    name: "Ghost",
    blurb: "Friendly, floaty, slightly judgemental.",
    colors: { main: "#e0e7ff", shell: "#1e293b", screen: "#0b1220" },
    theme: BODY_FACE,
    face: { dx: 0, dy: 3, k: 1 },
    anchor: { y: 8, hw: 50, earY: 40 },
    blush: true,
    body: (S) => `
      <path d="M28 100V52C28 24 50 8 80 8C110 8 132 24 132 52V100Q122 110 112 100Q102 90 92 100Q82 110 72 100Q62 90 52 100Q42 110 28 100Z" ${M}/>
      <ellipse cx="27" cy="68" rx="10" ry="6" transform="rotate(35 27 68)" ${M}/>
      <ellipse cx="133" cy="68" rx="10" ry="6" transform="rotate(-35 133 68)" ${M}/>
      <ellipse cx="80" cy="82" rx="30" ry="12" ${L} opacity=".55"/>
      ${led(80, 83, 5, S.led)}`
  },

  cloud: {
    id: "cloud",
    name: "Cloud",
    blurb: "Perfect for hosting and cloud products.",
    colors: { main: "#7dd3fc", shell: "#1e293b", screen: "#0b1220" },
    theme: BODY_FACE,
    face: { dx: 0, dy: 6, k: 1 },
    anchor: { y: 12, hw: 38, earY: 44 },
    body: (S) => `
      <g ${M}>
        <circle cx="46" cy="62" r="24"/>
        <circle cx="80" cy="44" r="32"/>
        <circle cx="114" cy="60" r="26"/>
        <rect x="34" y="56" width="92" height="34" rx="17"/>
      </g>
      <ellipse cx="80" cy="84" rx="38" ry="5" ${L} opacity=".6"/>
      <path class="sb-led" d="M84 92l-11 13h8l-5 12 15-16h-8l5-9z" fill="${S.led}"/>`
  },

  database: {
    id: "database",
    name: "Database",
    blurb: "Stacked drives with status lights.",
    colors: { main: "#10b981", shell: "#1e293b", screen: "#0b1220" },
    theme: { ...BODY_FACE, scleraStroke: "", line: "#064e3b", mouth: "#064e3b", down: "#7f1d1d" },
    face: { dx: 0, dy: 3, k: 1 },
    anchor: { y: 13, hw: 46, earY: 42 },
    body: (S) => `
      <path d="M30 24V92C30 102 52 108 80 108C108 108 130 102 130 92V24Z" ${M}/>
      <path d="M30 58C30 68 52 74 80 74C108 74 130 68 130 58" fill="none" stroke-width="4" style="stroke:var(--sb-dark)"/>
      <path d="M30 84C30 94 52 100 80 100C108 100 130 94 130 84" fill="none" stroke-width="4" style="stroke:var(--sb-dark)"/>
      <ellipse cx="80" cy="24" rx="50" ry="13" ${L}/>
      <rect x="40" y="81" width="38" height="6" rx="3" ${D}/>
      ${led(102, 85, 3.2, S.led)}${led(114, 85, 3.2, "#a7f3d0", "sb-led-b")}`
  },

  rocket: {
    id: "rocket",
    name: "Rocket",
    blurb: "Ships to prod on Fridays. Porthole doubles as the face.",
    colors: { main: "#ef4444", shell: "#e2e8f0", screen: "#0b1220" },
    theme: SCREEN_FACE,
    face: { dx: 0, dy: 0, k: 1 },
    anchor: { y: 10, hw: 46, earY: 40 },
    body: (S) => `
      <path d="M42 70L20 92C18 95 20 98 23 98H44Z" ${D}/>
      <path d="M118 70L140 92C142 95 140 98 137 98H116Z" ${D}/>
      <path class="sb-led" d="M64 96Q80 120 96 96Z" fill="#fbbf24"/>
      <path class="sb-led" d="M72 96Q80 111 88 96Z" fill="#fef08a"/>
      <path d="M80 5C52 12 34 36 34 62V90C34 94 36 96 40 96H120C124 96 126 94 126 90V62C126 36 108 12 80 5Z" ${SH}/>
      <path d="M80 5C68 9 58 16 50 25H110C102 16 92 9 80 5Z" ${M}/>
      <ellipse cx="80" cy="40" rx="37" ry="19" ${SC}/>
      <rect x="34" y="72" width="92" height="8" ${M}/>
      ${led(54, 87, 3.2, S.led)}${led(80, 87, 3.2, "#fca5a5", "sb-led-b")}${led(106, 87, 3.2, S.led, "sb-led-c")}`
  },
  octopus: {
    id: "octopus",
    name: "Octopus",
    blurb: "A clever cephalopod in lab goggles, with eight arms for multitasking.",
    colors: { main: "#8b5cf6", shell: "#1e293b", screen: "#0b1220" },
    theme: BODY_FACE,
    face: { dx: 0, dy: 6, k: 1 },
    anchor: { y: 8, hw: 48, earY: 48 },
    blush: true,
    body: (S) => `
      <g fill="none" stroke-width="12" stroke-linecap="round" style="stroke:var(--sb-main)">
        <path d="M44 80C28 92 26 106 42 110"/>
        <path d="M63 86C56 100 62 112 76 110"/>
        <path d="M97 86C104 100 98 112 84 110"/>
        <path d="M116 80C132 92 134 106 118 110"/>
      </g>
      <g ${L}>
        <circle cx="35" cy="95" r="2.4"/><circle cx="58" cy="102" r="2.4"/><circle cx="102" cy="102" r="2.4"/><circle cx="125" cy="95" r="2.4"/>
      </g>
      <ellipse cx="80" cy="48" rx="50" ry="42" ${M}/>
      <ellipse cx="66" cy="22" rx="16" ry="7" ${L} opacity=".45"/>
      <rect x="30" y="35" width="100" height="11" rx="5.5" fill="#1f2937"/>
      <rect x="45" y="39" width="70" height="3" rx="1.5" fill="#f59e0b" opacity=".55"/>
      <path d="M74 41h12" stroke="#b45309" stroke-width="4" stroke-linecap="round"/>
      <g fill="#e0f2fe" stroke="#b45309" stroke-width="3.6">
        <circle cx="62" cy="41" r="14"/><circle cx="98" cy="41" r="14"/>
      </g>
      <path d="M53 33Q57 29 62 29M89 33Q93 29 98 29" stroke="#fff" stroke-width="2.4" stroke-linecap="round" fill="none" opacity=".8"/>
      ${led(80, 15, 3.5, S.led)}`
  }
};

export const CHARACTER_IDS = Object.keys(CHARACTERS);
export const ACCESSORIES = ["auto", "none", "nightcap", "partyhat", "crown", "glasses", "shades", "headphones"];

// Accessories that sit on / around the head. `a` is the character anchor.
export function accessoryOnHead(name, a) {
  const y = a.y;
  if (name === "nightcap") {
    return `<path d="M58 ${y + 2}Q62 ${y - 36} 102 ${y - 22}L104 ${y + 2}Z" fill="#ef4444"/>
      <rect x="54" y="${y - 3}" width="52" height="8" rx="4" fill="#f8fafc"/>
      <circle cx="103" cy="${y - 22}" r="5.5" fill="#f8fafc"/>`;
  }
  if (name === "partyhat") {
    return `<path d="M63 ${y + 2}L80 ${y - 34}L97 ${y + 2}Z" fill="#f472b6"/>
      <path d="M70 ${y - 12}L90 ${y - 12}M66 ${y - 3}L94 ${y - 3}" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/>
      <circle cx="80" cy="${y - 35}" r="4.5" fill="#fde047"/>`;
  }
  if (name === "crown") {
    return `<path d="M58 ${y + 3}L57 ${y - 18}L69 ${y - 7}L80 ${y - 22}L91 ${y - 7}L103 ${y - 18}L102 ${y + 3}Z" fill="#facc15" stroke="#ca8a04" stroke-width="2" stroke-linejoin="round"/>
      <circle cx="80" cy="${y - 8}" r="3" fill="#ef4444"/><circle cx="66" cy="${y - 1}" r="2" fill="#38bdf8"/><circle cx="94" cy="${y - 1}" r="2" fill="#38bdf8"/>`;
  }
  if (name === "headphones") {
    const l = 80 - a.hw;
    const r = 80 + a.hw;
    return `<path d="M${l + 1} ${a.earY}C${l + 1} ${y - 24} ${r - 1} ${y - 24} ${r - 1} ${a.earY}" fill="none" stroke="#1f2937" stroke-width="5" stroke-linecap="round"/>
      <rect x="${l - 6}" y="${a.earY - 11}" width="12" height="22" rx="6" fill="#111827"/>
      <rect x="${r - 6}" y="${a.earY - 11}" width="12" height="22" rx="6" fill="#111827"/>
      <rect x="${l - 3}" y="${a.earY - 6}" width="4" height="12" rx="2" fill="#38bdf8"/>
      <rect x="${r - 1}" y="${a.earY - 6}" width="4" height="12" rx="2" fill="#38bdf8"/>`;
  }
  return "";
}

// Accessories that sit on the face are drawn inside the (offset) face group.
export function accessoryOnFace(name) {
  if (name === "glasses") {
    return `<g fill="rgba(186,230,253,.18)" stroke="#0f172a" stroke-width="2.6">
      <circle cx="62" cy="35" r="12"/><circle cx="98" cy="35" r="12"/><path d="M74 35h12" fill="none"/></g>`;
  }
  if (name === "shades") {
    return `<g fill="#0f172a"><rect x="47" y="25" width="28" height="18" rx="7"/><rect x="85" y="25" width="28" height="18" rx="7"/></g>
      <path d="M75 31h10" stroke="#0f172a" stroke-width="3.2"/>
      <path d="M52 29l7 0M90 29l7 0" stroke="#e2e8f0" stroke-width="2" stroke-linecap="round" opacity=".55"/>`;
  }
  return "";
}

// The shared face: eyes, mouth and cheeks for every character and state.
export function faceMarkup(ch, S, acc) {
  const t = ch.theme;
  const { dx, dy, k } = ch.face;
  const down = S.state === "down";
  const closed = S.eyesClosed;
  const squint = S.squint && !down && !closed;
  const curious = S.state === "curious";
  const sclera = `fill="${t.sclera}"${t.scleraStroke ? ` stroke="${t.scleraStroke}" stroke-width="1.6"` : ""}`;
  let g = "";

  if (down) {
    g += `<g stroke="${t.down}" stroke-width="3" stroke-linecap="round"><path d="M56 29l12 12M68 29L56 41"/><path d="M92 29l12 12M104 29L92 41"/></g>`;
  } else if (closed) {
    g += `<g stroke="${t.line}" stroke-width="3" stroke-linecap="round" fill="none"><path d="M56 36q6 5 12 0"/><path d="M92 36q6 5 12 0"/></g>`;
  } else if (squint) {
    g += `<g stroke="${t.line}" stroke-width="3" stroke-linecap="round" fill="none"><path d="M56 38q6-9 12 0"/><path d="M92 38q6-9 12 0"/></g>`;
  } else {
    const r = curious ? 8.5 : 7.5;
    g += `<circle cx="62" cy="35" r="${r}" ${sclera}/><circle cx="98" cy="35" r="${r}" ${sclera}/>
      <g class="sb-pupils"><circle cx="62" cy="35" r="3.6" fill="${t.pupil}"/><circle cx="98" cy="35" r="3.6" fill="${t.pupil}"/>
      <circle cx="63.2" cy="33.6" r="1.1" fill="#fff"/><circle cx="99.2" cy="33.6" r="1.1" fill="#fff"/></g>`;
  }

  if (squint || ch.blush) {
    g += `<g fill="${t.cheek}" opacity="${squint ? 0.6 : 0.32}"><ellipse cx="46" cy="${squint ? 42 : 44}" rx="5" ry="3"/><ellipse cx="114" cy="${squint ? 42 : 44}" rx="5" ry="3"/></g>`;
  }

  if (down) {
    g += `<path d="M71 49q9-7 18 0" stroke="${t.down}" stroke-width="2.6" stroke-linecap="round" fill="none"/>`;
  } else if (S.idleAct === "yawn") {
    g += `<ellipse cx="80" cy="46" rx="4.5" ry="5.5" fill="${t.mouth}"/>`;
  } else if (S.state === "sleeping") {
    g += `<path d="M75 46h10" stroke="${t.mouth}" stroke-width="2.4" stroke-linecap="round"/>`;
  } else if (curious) {
    g += `<circle cx="80" cy="46" r="2.8" fill="none" stroke="${t.mouth}" stroke-width="2.4"/>`;
  } else {
    g += `<path d="M71 45q9 7 18 0" stroke="${t.mouth}" stroke-width="2.6" stroke-linecap="round" fill="none"/>`;
  }

  g += accessoryOnFace(acc);
  return `<g transform="translate(${80 + dx} ${40 + dy}) scale(${k}) translate(-80 -40)">${g}</g>`;
}

// Full <svg> inner markup for a character in a given state.
export function characterMarkup(ch, S, acc) {
  const parts = [`<g class="sb-body">`, ch.body(S), faceMarkup(ch, S, acc), accessoryOnHead(acc, ch.anchor), `</g>`];

  if (S.state === "down" || S.nervous) {
    parts.push(`<path class="sb-sweat" d="M138 20q5 8 0 12q-5-4 0-12z" fill="#7dd3fc"/>`);
  }
  if (S.state === "down") {
    parts.push(
      `<g class="sb-smoke" fill="#94a3b8"><circle class="sb-smoke-1" cx="64" cy="2" r="4"/><circle class="sb-smoke-2" cx="76" cy="-2" r="3"/><circle class="sb-smoke-3" cx="96" cy="2" r="4"/></g>`
    );
  }
  if (S.state === "sleeping") {
    parts.push(
      `<g class="sb-zzz" fill="#64748b" font-weight="700" font-family="sans-serif"><text x="124" y="14" font-size="11">z</text><text x="134" y="6" font-size="8">z</text></g>`
    );
  }
  return parts.join("");
}
