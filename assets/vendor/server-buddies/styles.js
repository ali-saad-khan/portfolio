// All rules are prefixed `sb-` so they cannot collide with host CSS. Injected once at runtime
// (disable with `injectStyles: false`) and also shipped as `server-buddies/style.css`.
export const STYLE_ID = "server-buddies-styles";

export const CSS = `
.sb-hanger{position:fixed;z-index:40;width:104px;pointer-events:none;box-sizing:border-box}
.sb-hanger *{box-sizing:border-box}
.sb-hanger[hidden]{display:none!important}
.sb-hanger.sb-in-mount{position:absolute}
@media print{.sb-hanger{display:none!important}}

.sb-sway,.sb-swing{transform-origin:50% 0}
.sb-hanger[data-pivot="bottom"] .sb-swing,.sb-hanger[data-pivot="bottom"] .sb-sway{transform-origin:50% 100%}
.sb-hanger[data-hang="rope"] .sb-sway{animation:sb-sway 5s ease-in-out infinite}
.sb-hanger[data-hang="chain"] .sb-sway{animation:sb-sway-s 4.2s ease-in-out infinite}
.sb-hanger[data-hang="spring"] .sb-sway{animation:sb-sway-s 3s ease-in-out infinite}
.sb-hanger[data-hang="thread"] .sb-sway{animation:sb-sway-l 6.5s ease-in-out infinite}
.sb-hanger[data-hang="balloon"] .sb-sway{animation:sb-float 4.5s ease-in-out infinite}

.sb-tether{display:block;margin:0 auto;pointer-events:none}
.sb-tether-rope{width:3px;border-radius:2px;background:repeating-linear-gradient(180deg,#94a3b8 0 5px,#64748b 5px 8px)}
.sb-tether-thread{width:1.5px;border-radius:1px;background:linear-gradient(180deg,#e2e8f0,#94a3b8)}
.sb-tether-svg{overflow:visible;transform-origin:50% 0}
.sb-tether-balloon{display:flex;flex-direction:column;align-items:center}
.sb-balloon{display:block;width:54px;height:auto;overflow:visible}
.sb-balloon-string{display:block;width:1.5px;background:#94a3b8}

.sb-drop{will-change:transform}
.sb-buddy{position:relative;display:block;width:100%;margin:0;padding:0;border:0;border-radius:0;background:none;font:inherit;
  color:inherit;cursor:grab;pointer-events:auto;touch-action:none;perspective:500px;isolation:isolate;
  -webkit-tap-highlight-color:transparent;-webkit-appearance:none;appearance:none}
.sb-buddy[data-drag="off"]{touch-action:auto}
.sb-buddy[data-boop="off"][data-drag="off"]{cursor:default;pointer-events:none}
.sb-buddy:focus-visible{outline:2px solid var(--sb-main,#0058c3);outline-offset:4px;border-radius:14px}
.sb-buddy.sb-grabbed{cursor:grabbing}

.sb-svg{display:block;width:100%;height:auto;overflow:visible;transform-origin:50% 100%;transition:transform .15s ease}
.sb-buddy:active .sb-svg{transform:scale(1.06,.9)}

.sb-buddy[data-state="happy"] .sb-body,.sb-buddy[data-state="curious"] .sb-body{animation:sb-bob 3.2s ease-in-out infinite}
.sb-buddy[data-state="down"] .sb-body{animation:sb-shake .5s linear infinite}
.sb-buddy[data-state="sleeping"] .sb-body{animation:sb-breathe 4s ease-in-out infinite;transform-origin:50% 100%}
.sb-pupils{transition:transform .06s linear}
.sb-led{animation:sb-blink 1.8s ease-in-out infinite}
.sb-led-b{animation-delay:.4s}.sb-led-c{animation-delay:.9s}.sb-led-d{animation-delay:1.3s}
.sb-buddy[data-state="down"] .sb-led{animation-duration:.45s}
.sb-sweat{animation:sb-sweat 1.4s ease-in infinite}
.sb-smoke circle{opacity:0;animation:sb-smoke 2s ease-out infinite}
.sb-smoke-2{animation-delay:.6s}.sb-smoke-3{animation-delay:1.2s}
.sb-zzz{animation:sb-zzz 2.4s ease-in-out infinite}

.sb-bubble{position:absolute;right:70%;top:6px;padding:3px 9px;border-radius:10px;background:#0f172a;color:#fff;
  font:700 11px/1.35 system-ui,-apple-system,"Segoe UI",sans-serif;white-space:nowrap;opacity:0;pointer-events:none;z-index:4}
.sb-hanger[data-side="right"] .sb-bubble{right:auto;left:70%}
.sb-bubble-show{animation:sb-bubble 1.4s ease-out forwards}

.sb-svg.sb-flinch .sb-body{animation:sb-flinch .5s ease-out}
.sb-svg.sb-nervous .sb-body{animation:sb-jitter .28s linear infinite}
.sb-svg.sb-pass .sb-led{filter:brightness(2.4) drop-shadow(0 0 3px #86efac)}
.sb-svg.sb-nod .sb-body{animation:sb-nod .7s ease-in-out}
.sb-buddy[data-act="dance"] .sb-body{animation:sb-dance .45s ease-in-out infinite}
.sb-buddy[data-act="dance"] .sb-led{animation-duration:.25s}
.sb-buddy[data-act="yawn"] .sb-body{animation:sb-yawn 2.4s ease-in-out}
.sb-buddy[data-combo="spin"] .sb-svg{animation:sb-spin .8s ease-in-out}
.sb-buddy[data-combo="fall"]{animation:sb-fall 3.2s both}
.sb-buddy[data-period="morning"] .sb-svg{filter:drop-shadow(0 0 12px rgba(251,191,36,.6))}

.sb-confetti{position:absolute;left:50%;top:24px;width:0;height:0;z-index:3;pointer-events:none}
.sb-confetti i{position:absolute;left:0;top:0;border-radius:1px;opacity:0;animation:sb-confetti 2.4s ease-out forwards}
.sb-alarm{position:absolute;inset:-18px;z-index:-1;border-radius:50%;
  background:radial-gradient(circle,rgba(239,68,68,.6),transparent 65%);animation:sb-alarm .5s ease-in-out infinite alternate;pointer-events:none}

@keyframes sb-sway{0%,100%{transform:rotate(-2.2deg)}50%{transform:rotate(2.2deg)}}
@keyframes sb-sway-s{0%,100%{transform:rotate(-1.3deg)}50%{transform:rotate(1.3deg)}}
@keyframes sb-sway-l{0%,100%{transform:rotate(-3.6deg)}50%{transform:rotate(3.6deg)}}
@keyframes sb-float{0%,100%{transform:translateY(0) rotate(-1.8deg)}50%{transform:translateY(5px) rotate(1.8deg)}}
@keyframes sb-bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-3px)}}
@keyframes sb-shake{0%,100%{transform:translateX(0)}25%{transform:translateX(-1.5px)}75%{transform:translateX(1.5px)}}
@keyframes sb-breathe{0%,100%{transform:scaleY(1)}50%{transform:scaleY(.97)}}
@keyframes sb-blink{0%,100%{opacity:1}50%{opacity:.35}}
@keyframes sb-sweat{0%{transform:translateY(0);opacity:0}20%{opacity:1}100%{transform:translateY(18px);opacity:0}}
@keyframes sb-smoke{0%{transform:translateY(0) scale(.6);opacity:.7}100%{transform:translateY(-18px) scale(1.5);opacity:0}}
@keyframes sb-zzz{0%,100%{transform:translateY(0);opacity:.4}50%{transform:translateY(-4px);opacity:1}}
@keyframes sb-bubble{0%{opacity:0;transform:translateY(6px)}15%,70%{opacity:1;transform:translateY(0)}100%{opacity:0;transform:translateY(-4px)}}
@keyframes sb-bubble-static{0%,80%{opacity:1}100%{opacity:0}}
@keyframes sb-flinch{0%{transform:translate(0,0) scale(1)}20%{transform:translate(-3px,2px) scale(.94,1.04)}45%{transform:translate(3px,0) scale(1.03)}100%{transform:translate(0,0) scale(1)}}
@keyframes sb-jitter{0%,100%{transform:translateX(0)}25%{transform:translateX(-.8px)}75%{transform:translateX(.8px)}}
@keyframes sb-nod{0%,100%{transform:translateY(0)}30%{transform:translateY(5px)}60%{transform:translateY(-2px)}}
@keyframes sb-dance{0%,100%{transform:translate(0,0) rotate(0)}25%{transform:translate(-3px,-4px) rotate(-4deg)}75%{transform:translate(3px,-4px) rotate(4deg)}}
@keyframes sb-yawn{0%,100%{transform:scale(1)}40%,60%{transform:scale(1.05,.96)}}
@keyframes sb-spin{from{transform:rotateY(0)}to{transform:rotateY(360deg)}}
@keyframes sb-fall{0%{transform:translateY(0) rotate(0);animation-timing-function:cubic-bezier(.5,0,.9,.6)}22%{transform:translateY(115vh) rotate(24deg)}62%{transform:translateY(115vh) rotate(24deg);animation-timing-function:cubic-bezier(.2,.7,.3,1)}100%{transform:translateY(0) rotate(0)}}
@keyframes sb-confetti{0%{transform:translate(0,0) rotate(0);opacity:1}25%{transform:translate(calc(var(--x) * .8),-56px) rotate(var(--r));opacity:1}100%{transform:translate(var(--x),170px) rotate(calc(var(--r) + 540deg));opacity:0}}
@keyframes sb-alarm{from{opacity:.35}to{opacity:1}}

@media (prefers-reduced-motion:reduce){
  .sb-sway,.sb-buddy *,.sb-buddy .sb-body,.sb-tether{animation:none!important;transition:none!important}
  .sb-buddy .sb-bubble-show{animation:sb-bubble-static 1.8s forwards!important}
}
`.trim();
