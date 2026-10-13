// Runs in <head> before first paint so light-mode visitors don't see a dark flash.
(function () {
  try {
    var saved = localStorage.getItem("theme");
    var prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
    if (saved === "light" || (!saved && !prefersDark)) {
      document.documentElement.setAttribute("data-theme", "light");
    }
  } catch (e) {}
})();
