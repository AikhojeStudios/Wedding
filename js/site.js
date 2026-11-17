/* Aikhoje Studios — shared site script (nav, inquiry form, lightbox, gallery filters). */
(function () {
  "use strict";

  /* ---- Mobile menu ---- */
  var head = document.getElementById("site-head");
  var toggle = document.getElementById("nav-toggle");
  if (head && toggle) {
    var setMenu = function (open) {
      head.classList.toggle("menu-open", open);
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.textContent = open ? "Close" : "Menu";
    };
    toggle.addEventListener("click", function () { setMenu(!head.classList.contains("menu-open")); });
    head.addEventListener("click", function (e) { if (e.target.closest(".nav-links a")) setMenu(false); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && head.classList.contains("menu-open")) { setMenu(false); toggle.focus(); }
    });
  }

  /* ---- Mobile "Inquire" bar: show after scrolling, hide near the form ---- */
  var bar = document.getElementById("mobile-inquire");
  var contact = document.getElementById("contact");
  if (bar) {
    var updateBar = function () {
      var narrow = window.matchMedia("(max-width: 760px)").matches;
      var past = window.scrollY > window.innerHeight * 0.55;
      var near = false;
      if (contact) {
        var r = contact.getBoundingClientRect();
        near = r.top < window.innerHeight * 0.75 && r.bottom > 80;
      }
      bar.hidden = !(narrow && past && !near);
    };
    window.addEventListener("scroll", updateBar, { passive: true });
    window.addEventListener("resize", updateBar);
    updateBar();
  }

  /* ---- Inquiry form (FormSubmit AJAX) ---- */
  var form = document.getElementById("inquiry-form");
  if (form) {
    var status = document.getElementById("form-status");
    var submitBtn = form.querySelector('button[type="submit"]');
    var fail = "Something went wrong. Please try again or email aikhojestudios@gmail.com directly.";
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      submitBtn.disabled = true;
      submitBtn.textContent = "Sending…";
      status.className = "form-status";
      status.textContent = "";
      var data = {};
      new FormData(form).forEach(function (v, k) { data[k] = typeof v === "string" ? v.trim() : v; });
      fetch(form.action, {
        method: "POST",
        headers: { "Content-Type": "application/json", "Accept": "application/json" },
        body: JSON.stringify(data)
      })
        .then(function (r) { return r.json(); })
        .then(function (d) {
          if (d.success) {
            status.className = "form-status success";
            status.textContent = "Thank you! Your inquiry has been sent. You’ll hear back within 24 hours, and a confirmation is on its way to your inbox.";
            form.reset();
          } else {
            status.className = "form-status error";
            status.textContent = fail;
          }
        })
        .catch(function () { status.className = "form-status error"; status.textContent = fail; })
        .finally(function () { submitBtn.disabled = false; submitBtn.textContent = "Send inquiry"; });
    });
  }

  /* ---- Lightbox for any [data-full] trigger that is currently visible ---- */
  var lb = document.getElementById("lightbox");
  if (lb) {
    var lbImg = lb.querySelector(".lb-img");
    var lbCount = lb.querySelector(".lb-count");
    var lbStatus = document.getElementById("lb-status");
    var closeBtn = lb.querySelector(".lb-close");
    var prevBtn = lb.querySelector(".lb-prev");
    var nextBtn = lb.querySelector(".lb-next");
    var items = [];
    var idx = 0;
    var lastTrigger = null;

    var visibleTriggers = function () {
      return Array.prototype.filter.call(document.querySelectorAll("[data-full]"), function (b) {
        return b.offsetParent !== null;
      });
    };
    var pad = function (n) { return (n < 10 ? "0" : "") + n; };
    var show = function (i) {
      idx = (i + items.length) % items.length;
      var trig = items[idx];
      var thumb = trig.querySelector("img");
      lbImg.src = trig.getAttribute("data-full");
      lbImg.alt = thumb ? thumb.alt : "";
      lbCount.textContent = pad(idx + 1) + " / " + pad(items.length);
      lbStatus.textContent = "Photograph " + (idx + 1) + " of " + items.length + ". " + lbImg.alt;
    };
    var open = function (trig) {
      items = visibleTriggers();
      lastTrigger = trig;
      lb.hidden = false;
      lb.classList.add("active");
      document.body.style.overflow = "hidden";
      show(items.indexOf(trig));
      closeBtn.focus();
    };
    var close = function () {
      if (lb.hidden) return;
      lb.classList.remove("active");
      lb.hidden = true;
      lbImg.removeAttribute("src");
      document.body.style.overflow = "";
      if (lastTrigger) lastTrigger.focus();
    };

    document.addEventListener("click", function (e) {
      var trig = e.target.closest("[data-full]");
      if (trig) { e.preventDefault(); open(trig); }
    });
    closeBtn.addEventListener("click", close);
    prevBtn.addEventListener("click", function () { show(idx - 1); });
    nextBtn.addEventListener("click", function () { show(idx + 1); });
    lb.addEventListener("click", function (e) { if (e.target === lb) close(); });
    /* Swipe left/right on phones (the arrow buttons are hidden there). */
    var sx = null, sy = null;
    lb.addEventListener("touchstart", function (e) { if (e.touches.length === 1) { sx = e.touches[0].clientX; sy = e.touches[0].clientY; } }, { passive: true });
    lb.addEventListener("touchend", function (e) {
      if (sx === null) return;
      var dx = e.changedTouches[0].clientX - sx, dy = e.changedTouches[0].clientY - sy;
      sx = sy = null;
      if (Math.abs(dx) > 40 && Math.abs(dx) > Math.abs(dy) * 1.5) show(dx < 0 ? idx + 1 : idx - 1);
    }, { passive: true });
    document.addEventListener("keydown", function (e) {
      if (lb.hidden) return;
      if (e.key === "Escape") { e.preventDefault(); close(); }
      else if (e.key === "ArrowLeft") { e.preventDefault(); show(idx - 1); }
      else if (e.key === "ArrowRight") { e.preventDefault(); show(idx + 1); }
      else if (e.key === "Tab") {
        var f = [closeBtn, prevBtn, nextBtn].filter(function (b) { return b.offsetParent !== null; });
        var first = f[0], last = f[f.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    });
  }

  /* ---- Gallery filters ---- */
  var filterBar = document.getElementById("gallery-filters");
  if (filterBar) {
    var tiles = Array.prototype.slice.call(document.querySelectorAll(".wall .tile"));
    var countEl = document.getElementById("gallery-count");
    filterBar.addEventListener("click", function (e) {
      var btn = e.target.closest("button[data-filter]");
      if (!btn) return;
      var f = btn.getAttribute("data-filter");
      Array.prototype.forEach.call(filterBar.querySelectorAll("button"), function (b) {
        b.setAttribute("aria-pressed", b === btn ? "true" : "false");
      });
      var n = 0;
      tiles.forEach(function (t) {
        var on = f === "all" || (" " + t.getAttribute("data-tags") + " ").indexOf(" " + f + " ") > -1;
        t.hidden = !on;
        if (on) n++;
      });
      if (countEl) countEl.textContent = (f === "all" ? "" : btn.getAttribute("data-label") + " · ") + n + " photographs";
    });
  }
})();
