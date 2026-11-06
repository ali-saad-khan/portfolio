"use strict";
/* Live double-entry ledger shown in the home hero.
   Every transaction posts balanced debit/credit lines. Hover a line to see the API call
   behind it; press the button to try posting an unbalanced entry and watch it get refused. */
(function () {
  const root = document.getElementById("ledger");
  if (!root) return;
  const body = root.querySelector(".ledger-body");
  const dTot = root.querySelector("[data-total=debit]");
  const cTot = root.querySelector("[data-total=credit]");
  const delta = root.querySelector("[data-delta]");
  const callEl = root.querySelector(".ledger-call");
  const statusEl = root.querySelector(".ledger-status");
  const tryBtn = root.querySelector(".ledger-try");
  const reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const DEFAULT_CALL = "Hover a line to see the API call behind it.";

  // Amounts are integer cents so debits and credits can never drift.
  const TXNS = [
    { memo: "Wallet top-up via card", call: "POST /v1/topups", lines: [["Gateway clearing", "D", 450000], ["Customer wallet", "C", 450000]] },
    { memo: "Order paid from wallet", call: "POST /v1/payments", lines: [["Customer wallet", "D", 189900], ["Merchant payable", "C", 179900], ["Fee revenue", "C", 10000]] },
    { memo: "Webhook retried (same key)", call: "POST /v1/webhooks/gateway", dup: true, lines: [["replayed, nothing posted", "D", 0], ["idempotent", "C", 0]] },
    { memo: "Partial refund issued", call: "POST /v1/refunds", lines: [["Merchant payable", "D", 65000], ["Customer wallet", "C", 65000]] },
    { memo: "Merchant payout", call: "POST /v1/payouts", lines: [["Merchant payable", "D", 1200000], ["Bank settlement", "C", 1200000]] },
    { memo: "Subscription renewal", call: "POST /v1/subscriptions/renew", lines: [["Customer wallet", "D", 290000], ["Subscription revenue", "C", 290000]] },
  ];

  let debit = 0, credit = 0, seq = 1040, cursor = 0, timer = null, hovering = false;
  const fmt = (c) => (c / 100).toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  const idemKey = () => Math.random().toString(36).slice(2, 10);

  function el(tag, cls, text) {
    const n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text !== undefined) n.textContent = text;
    return n;
  }

  function line(ref, acct, side, cents, call, extra) {
    const r = el("div", "ledger-row" + (extra ? " " + extra : ""));
    r.append(el("span", "ref", ref), el("span", "acct" + (side === "C" ? " credit" : ""), acct),
      el("span", "amt", side === "D" && cents ? fmt(cents) : ""), el("span", "amt", side === "C" && cents ? fmt(cents) : ""));
    r.dataset.call = call;
    return r;
  }

  function trim() {
    // Keep roughly the latest 16 rows on screen.
    while (body.children.length > 16) body.lastElementChild.remove();
  }

  function setTotals() {
    dTot.textContent = fmt(debit);
    cTot.textContent = fmt(credit);
    const ok = debit === credit;
    delta.querySelector(".num").textContent = ok ? "0.00" : fmt(Math.abs(debit - credit));
    delta.querySelector(".seal").textContent = ok ? "Balanced" : "Check";
  }

  function post(txn, instant) {
    seq += 1;
    const ref = "TX-" + seq;
    const memo = el("div", "ledger-row memo");
    const label = el("span");
    const b = el("b", "", txn.memo);
    label.append(b, el("span", "stamp-ok", txn.dup ? "↺ ignored" : "✓ posted"));
    memo.append(label);
    memo.dataset.call = txn.call + "  Idempotency-Key: " + idemKey();
    const rows = [memo].concat(txn.lines.map((l) => line(ref, l[0], l[1], l[2], memo.dataset.call, txn.dup ? "dup" : "")));
    // Prepend so newest is on top; insert in reverse to keep order.
    for (let i = rows.length - 1; i >= 0; i--) body.prepend(rows[i]);
    txn.lines.forEach((l) => { if (l[1] === "D") debit += l[2]; else credit += l[2]; });
    setTotals();
    trim();
  }

  function next() {
    post(TXNS[cursor % TXNS.length]);
    cursor += 1;
  }

  function start() { if (!timer && !reduced) timer = setInterval(() => { if (!hovering) next(); }, 2400); }
  function stop() { clearInterval(timer); timer = null; }

  // Hover / focus a row: reveal the API call behind it
  function showCall(e) {
    const row = e.target.closest(".ledger-row");
    if (!row) return;
    body.querySelectorAll(".is-active").forEach((n) => n.classList.remove("is-active"));
    row.classList.add("is-active");
    const parts = row.dataset.call.split("  ");
    callEl.textContent = "";
    const code = el("code", "", parts[0]);
    callEl.append(code);
    if (parts[1]) callEl.append(document.createTextNode("  " + parts[1]));
  }
  body.addEventListener("pointerover", (e) => { hovering = true; showCall(e); });
  body.addEventListener("pointerleave", () => {
    hovering = false;
    body.querySelectorAll(".is-active").forEach((n) => n.classList.remove("is-active"));
    callEl.textContent = DEFAULT_CALL;
  });

  // The unbalanced-entry demo
  tryBtn.addEventListener("click", () => {
    const ref = "TX-????";
    const d = line(ref, "Customer wallet", "D", 50000, "POST /v1/transfers  Idempotency-Key: " + idemKey(), "draft");
    const c = line(ref, "Merchant payable", "C", 45000, "", "draft");
    body.prepend(c); body.prepend(d);
    statusEl.textContent = "Posting…";
    setTimeout(() => {
      statusEl.textContent = "422 Rejected: debits 500.00 ≠ credits 450.00. Nothing was written; totals unchanged.";
      d.classList.add("out"); c.classList.add("out");
      setTimeout(() => { d.remove(); c.remove(); }, 700);
    }, 550);
    setTimeout(() => { if (statusEl.textContent.startsWith("422")) statusEl.textContent = ""; }, 6000);
  });

  // Seed with a few transactions, then run live while visible
  const seed = reduced ? 3 : 2;
  for (let i = 0; i < seed; i++) next();
  callEl.textContent = DEFAULT_CALL;

  if ("IntersectionObserver" in window && !reduced) {
    new IntersectionObserver((es) => es.forEach((e) => (e.isIntersecting ? start() : stop())), { threshold: 0.2 }).observe(root);
  } else {
    start();
  }
  document.addEventListener("visibilitychange", () => (document.hidden ? stop() : start()));
})();
