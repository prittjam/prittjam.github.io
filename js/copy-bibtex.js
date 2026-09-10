/* Copy-to-clipboard for the BibTeX dropdowns. Hand-written, no dependencies. */
(function () {
  "use strict";

  var RESET_MS = 1600;

  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text);
    }
    // file:// and plain http fall back to the legacy path
    return new Promise(function (resolve, reject) {
      var ta = document.createElement("textarea");
      ta.value = text;
      ta.setAttribute("readonly", "");
      ta.style.position = "fixed";
      ta.style.top = "-1000px";
      document.body.appendChild(ta);
      ta.select();
      var ok = false;
      try { ok = document.execCommand("copy"); } catch (e) { ok = false; }
      document.body.removeChild(ta);
      ok ? resolve() : reject();
    });
  }

  function flash(btn, state) {
    btn.dataset.state = state;
    btn.setAttribute("aria-label", state === "copied" ? "BibTeX copied" : "Copy failed");
    window.clearTimeout(btn._resetTimer);
    btn._resetTimer = window.setTimeout(function () {
      delete btn.dataset.state;
      btn.setAttribute("aria-label", "Copy BibTeX");
    }, RESET_MS);
  }

  document.addEventListener("click", function (ev) {
    var btn = ev.target.closest(".copy-btn");
    if (!btn) return;
    var pre = btn.parentNode.querySelector("pre");
    if (!pre) return;
    copyText(pre.textContent).then(
      function () { flash(btn, "copied"); },
      function () { flash(btn, "failed"); }
    );
  });
})();
