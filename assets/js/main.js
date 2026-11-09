/* AIgro — site behaviour. Progressive enhancement: everything works without JS. */
(() => {
  "use strict";
  document.documentElement.classList.add("js");
  const EN = document.documentElement.lang === "en";
  const T = EN
    ? { open: "Open menu", close: "Close menu", subject: "AIgro meeting request", name: "Name", org: "Organisation", email: "E-mail", topic: "Interest",
        sent: (to) => `Your e-mail app opened with the message ready. Press “Send” in your e-mail app. If nothing opened, write to us directly at ${to}.` }
    : { open: "Menüyü aç", close: "Menüyü kapat", subject: "AIgro görüşme talebi", name: "Ad Soyad", org: "Kurum", email: "E-posta", topic: "İlgi alanı",
        sent: (to) => `E-posta uygulamanız mesaj hazır olarak açıldı. Göndermek için e-posta uygulamanızda “Gönder”e basın. Uygulama açılmadıysa bize doğrudan ${to} adresinden yazabilirsiniz.` };

  const header = document.querySelector(".site-header");
  const nav = document.getElementById("site-nav");
  const toggle = document.querySelector(".menu-toggle");

  /* Header: solid background once the page scrolls */
  const onScroll = () => header && header.classList.toggle("is-scrolled", window.scrollY > 24);
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  /* Dropdowns: click + keyboard, never hover-only */
  const dropdownButtons = [...document.querySelectorAll("[data-dropdown]")];
  const closeDropdown = (btn, focusBtn = false) => {
    btn.setAttribute("aria-expanded", "false");
    document.getElementById(btn.getAttribute("aria-controls"))?.classList.remove("open");
    if (focusBtn) btn.focus();
  };
  const openDropdown = (btn) => {
    dropdownButtons.forEach((b) => b !== btn && closeDropdown(b));
    btn.setAttribute("aria-expanded", "true");
    document.getElementById(btn.getAttribute("aria-controls"))?.classList.add("open");
  };
  dropdownButtons.forEach((btn) => {
    const panel = document.getElementById(btn.getAttribute("aria-controls"));
    btn.addEventListener("click", () => (btn.getAttribute("aria-expanded") === "true" ? closeDropdown(btn) : openDropdown(btn)));
    btn.addEventListener("keydown", (e) => {
      if (e.key === "ArrowDown") { e.preventDefault(); openDropdown(btn); requestAnimationFrame(() => panel?.querySelector("a")?.focus()); }
    });
    panel?.addEventListener("keydown", (e) => {
      const links = [...panel.querySelectorAll("a")];
      const i = links.indexOf(document.activeElement);
      if (e.key === "ArrowDown") { e.preventDefault(); links[(i + 1) % links.length].focus(); }
      if (e.key === "ArrowUp") { e.preventDefault(); links[(i - 1 + links.length) % links.length].focus(); }
      if (e.key === "Escape") { e.preventDefault(); closeDropdown(btn, true); }
    });
    btn.closest(".has-dropdown")?.addEventListener("focusout", (e) => {
      if (!btn.closest(".has-dropdown").contains(e.relatedTarget) && window.matchMedia("(min-width: 1021px)").matches) closeDropdown(btn);
    });
  });
  document.addEventListener("click", (e) => {
    dropdownButtons.forEach((btn) => { if (!btn.closest(".has-dropdown").contains(e.target)) closeDropdown(btn); });
  });

  /* Mobile menu */
  const setMenu = (open) => {
    if (!toggle || !nav) return;
    toggle.setAttribute("aria-expanded", String(open));
    toggle.querySelector(".sr-only").textContent = open ? T.close : T.open;
    nav.classList.toggle("open", open);
    header.classList.toggle("menu-open", open);
    document.body.classList.toggle("no-scroll", open);
  };
  toggle?.addEventListener("click", () => setMenu(toggle.getAttribute("aria-expanded") !== "true"));
  nav?.addEventListener("click", (e) => { if (e.target.closest("a")) setMenu(false); });
  document.addEventListener("keydown", (e) => {
    if (e.key !== "Escape") return;
    const openDd = dropdownButtons.find((b) => b.getAttribute("aria-expanded") === "true");
    if (openDd) { closeDropdown(openDd, true); return; }
    if (toggle?.getAttribute("aria-expanded") === "true") { setMenu(false); toggle.focus(); }
  });
  window.matchMedia("(min-width: 1021px)").addEventListener("change", (e) => { if (e.matches) setMenu(false); });

  /* Tabs (WAI-ARIA pattern, arrow keys) */
  document.querySelectorAll("[data-tabs]").forEach((root) => {
    const tabs = [...root.querySelectorAll('[role="tab"]')];
    const select = (tab) => {
      tabs.forEach((t) => {
        const on = t === tab;
        t.setAttribute("aria-selected", String(on));
        t.tabIndex = on ? 0 : -1;
        document.getElementById(t.getAttribute("aria-controls")).hidden = !on;
      });
    };
    tabs.forEach((tab, i) => {
      tab.addEventListener("click", () => select(tab));
      tab.addEventListener("keydown", (e) => {
        let n = null;
        if (e.key === "ArrowRight") n = tabs[(i + 1) % tabs.length];
        if (e.key === "ArrowLeft") n = tabs[(i - 1 + tabs.length) % tabs.length];
        if (e.key === "Home") n = tabs[0];
        if (e.key === "End") n = tabs[tabs.length - 1];
        if (n) { e.preventDefault(); select(n); n.focus(); }
      });
    });
  });

  /* Reveal on scroll */
  const revealEls = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    revealEls.forEach((el) => io.observe(el));
  } else {
    revealEls.forEach((el) => el.classList.add("in"));
  }

  /* Contact form: validates, then opens the visitor's e-mail app (no backend, no fake success) */
  const form = document.getElementById("contact-form");
  if (form) {
    const status = form.querySelector(".form-status");
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      let ok = true;
      form.querySelectorAll("[required]").forEach((input) => {
        const valid = input.value.trim().length > 1 && (input.type !== "email" || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(input.value.trim()));
        input.closest(".field").classList.toggle("invalid", !valid);
        input.setAttribute("aria-invalid", String(!valid));
        if (!valid && ok) { input.focus(); ok = false; }
      });
      if (!ok) return;
      const v = (n) => (form.elements[n]?.value || "").trim();
      const subject = `${T.subject} – ${v("konu")}`;
      const body = [`${T.name}: ${v("ad")}`, `${T.org}: ${v("kurum") || "-"}`, `${T.email}: ${v("eposta")}`, `${T.topic}: ${v("konu")}`, "", v("mesaj")].join("\n");
      window.location.href = `mailto:${form.dataset.to}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
      status.textContent = T.sent(form.dataset.to);
      status.classList.add("show");
    });
  }

  const y = document.getElementById("year");
  if (y) y.textContent = String(new Date().getFullYear());
})();
