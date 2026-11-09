(() => {
  const btn = document.querySelector(".menu-btn");
  const menu = document.getElementById("menu");
  if (!btn || !menu) return;

  const label = btn.querySelector(".sr-only");
  const setOpen = (open) => {
    btn.setAttribute("aria-expanded", String(open));
    menu.classList.toggle("open", open);
    if (label) label.textContent = open ? "Menüyü kapat" : "Menüyü aç";
  };

  btn.addEventListener("click", () => setOpen(btn.getAttribute("aria-expanded") !== "true"));
  menu.addEventListener("click", (e) => { if (e.target.closest("a")) setOpen(false); });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && btn.getAttribute("aria-expanded") === "true") { setOpen(false); btn.focus(); }
  });

  const year = document.getElementById("yil");
  if (year) year.textContent = String(new Date().getFullYear());
})();
