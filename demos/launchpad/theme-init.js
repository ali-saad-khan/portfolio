/* Sets the theme before first paint. External (not inline) so a strict `script-src 'self'` CSP allows it. */
(function () {
  try {
    var pref = JSON.parse(localStorage.getItem("lp-theme")); // stored via JSON.stringify
    var theme = pref === "light" || pref === "dark" ? pref : null;
    if (theme) document.documentElement.setAttribute("data-theme", theme);
  } catch (e) {}
})();
