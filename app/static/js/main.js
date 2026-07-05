(function () {
  "use strict";

  function showToast(message) {
    var toast = document.getElementById("toast");
    if (!toast) return;
    toast.textContent = message;
    toast.classList.add("toast--visible");
    clearTimeout(toast._timer);
    toast._timer = setTimeout(function () {
      toast.classList.remove("toast--visible");
    }, 2200);
  }

  function copyText(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      return navigator.clipboard.writeText(text).then(function () {
        showToast("Copied to clipboard");
      });
    }
    var textarea = document.createElement("textarea");
    textarea.value = text;
    textarea.style.position = "fixed";
    textarea.style.opacity = "0";
    document.body.appendChild(textarea);
    textarea.select();
    try {
      document.execCommand("copy");
      showToast("Copied to clipboard");
    } catch (e) {
      showToast("Copy failed");
    }
    document.body.removeChild(textarea);
    return Promise.resolve();
  }

  function getCopyText(el) {
    if (el.dataset.plain) return el.dataset.plain;
    return el.textContent.trim();
  }

  document.querySelectorAll("[data-copy]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var target = document.querySelector(btn.getAttribute("data-copy"));
      if (target) copyText(getCopyText(target));
    });
  });

  document.querySelectorAll("[data-toggle-secret]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var target = document.querySelector(btn.getAttribute("data-toggle-secret"));
      if (!target) return;
      var isMasked = target.classList.contains("secret-display__value--masked");
      if (isMasked) {
        target.classList.remove("secret-display__value--masked");
        target.textContent = target.dataset.plain || target.textContent;
        btn.setAttribute("aria-pressed", "true");
      } else {
        target.classList.add("secret-display__value--masked");
        var plain = target.textContent.trim();
        target.dataset.plain = plain;
        target.textContent = "\u2022".repeat(Math.min(plain.length, 24));
        btn.setAttribute("aria-pressed", "false");
      }
    });
  });

  var rangeInput = document.getElementById("length-range");
  var rangeOutput = document.getElementById("length-value");
  var hiddenLength = document.getElementById("length-hidden");

  if (rangeInput && rangeOutput) {
    function syncRange() {
      rangeOutput.textContent = rangeInput.value;
      if (hiddenLength) hiddenLength.value = rangeInput.value;
    }
    rangeInput.addEventListener("input", syncRange);
    syncRange();
  }

  var generatedEl = document.getElementById("generated-password");
  var strengthFill = document.getElementById("strength-fill");
  var strengthLabel = document.getElementById("strength-label");

  if (generatedEl && strengthFill && strengthLabel) {
    var pwd = generatedEl.textContent.trim();
    var score = 0;
    if (pwd.length >= 12) score++;
    if (pwd.length >= 16) score++;
    if (/[a-z]/.test(pwd) && /[A-Z]/.test(pwd)) score++;
    if (/\d/.test(pwd)) score++;
    if (/[^a-zA-Z0-9]/.test(pwd)) score++;

    var levels = [
      { cls: "strength-bar__fill--weak", label: "Weak — consider increasing length" },
      { cls: "strength-bar__fill--fair", label: "Fair — acceptable for most uses" },
      { cls: "strength-bar__fill--good", label: "Good — strong password" },
      { cls: "strength-bar__fill--strong", label: "Excellent — very strong password" },
    ];
    var level = levels[Math.min(Math.floor(score / 1.5), levels.length - 1)];
    strengthFill.className = "strength-bar__fill " + level.cls;
    strengthLabel.textContent = level.label;
  }
})();
