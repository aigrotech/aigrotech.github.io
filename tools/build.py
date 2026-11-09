"""Builds the bilingual static AIgro site from src/ into the repository root.

Turkish pages are written to the root, English pages to en/.

Each page in src/pages/<lang>/*.html starts with a small front-matter block:

    title: Page title
    description: Meta description
    header: overlay | solid
    active: index | dozaj | su | dikey | iletisim   (page key, shared by both languages)
    og_image: assets/img/og-cover.jpg
    ---
    <main> ... </main>

Macros:
    [[U <unsplash-id> <width>]]  -> Unsplash CDN URL at that width
    [[S <unsplash-id>]]          -> responsive srcset for that photo
    [[I <icon> [classes]]]       -> inline SVG icon from the sprite
    {{email}}                    -> contact e-mail address (single source: CONTACT_EMAIL)
    {{href:<key>}}               -> URL of a page in the current language
    {{t:<key>}}                  -> layout string in the current language

Run:  python tools/build.py
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
SITE_URL = "https://tarikyil.github.io/aigro-web/"
CONTACT_EMAIL = "muhammed.kurdas@aksiyomtech.com"  # TODO: replace once the new company domain is live

LANGS = {
    "tr": {"dir": "", "root": "", "locale": "tr_TR"},
    "en": {"dir": "en/", "root": "../", "locale": "en_GB"},
}

PAGES = {
    "tr": {"index": "index.html", "dozaj": "akilli-dozajlama.html", "su": "su-takibi.html",
           "dikey": "dikey-tarim.html", "iletisim": "iletisim.html"},
    "en": {"index": "index.html", "dozaj": "smart-dosing.html", "su": "water-monitoring.html",
           "dikey": "vertical-farming.html", "iletisim": "contact.html"},
}

STRINGS = {
    "tr": {
        "skip": "İçeriğe geç",
        "home_label": "AIgro ana sayfa",
        "menu_open": "Menüyü aç",
        "nav_label": "Ana menü",
        "solutions": "Çözümler",
        "dozaj_title": "Akıllı Besin Dozajlama",
        "dozaj_chip": "Pilot",
        "dozaj_desc": "pH ve EC'yi öngören, güvenlik sınırlı otonom dozaj",
        "su_title": "Su Takip Sistemi",
        "su_chip": "Sahada",
        "su_desc": "Depo seviyesi, sıcaklık, bulanıklık ve alarm",
        "dikey_title": "Dikey Tarım Modülü",
        "dikey_chip": "Ar-Ge",
        "dikey_desc": "Kafe ve restoranlar için yerinde yetiştirme",
        "platform": "Platform",
        "field": "Sahadan",
        "about": "Hakkımızda",
        "contact": "İletişim",
        "cta": "Görüşme planlayın",
        "lang_switch": "EN",
        "lang_switch_label": "English version",
        "refs_title": "Referanslarımız",
        "refs_label": "Referans firmalar",
        "footer_about": "AIgro; topraksız tarım ve su yönetimi için sensörden panele uçtan uca akıllı sistemler. Sensör, kontrol kartı, yazılım ve kurulum aynı ekipten.",
        "footer_solutions": "Çözümler",
        "footer_company": "Kurumsal",
        "footer_contact": "İletişim",
        "rights": "Tüm hakları saklıdır.",
        "footer_note": "Hedef oranlar literatüre dayalıdır, garanti değildir. Panel ve konsept görselleri üzerinde belirtilmiştir. Sera atmosfer fotoğrafları temsilidir (Unsplash lisansı).",
    },
    "en": {
        "skip": "Skip to content",
        "home_label": "AIgro home",
        "menu_open": "Open menu",
        "nav_label": "Main menu",
        "solutions": "Solutions",
        "dozaj_title": "Smart Nutrient Dosing",
        "dozaj_chip": "Pilot",
        "dozaj_desc": "Autonomous dosing that forecasts pH and EC, within safety limits",
        "su_title": "Water Monitoring System",
        "su_chip": "In the field",
        "su_desc": "Tank level, temperature, turbidity and alarms",
        "dikey_title": "Vertical Farming Module",
        "dikey_chip": "R&D",
        "dikey_desc": "Grow-on-site module for cafés and restaurants",
        "platform": "Platform",
        "field": "In the field",
        "about": "About",
        "contact": "Contact",
        "cta": "Book a meeting",
        "lang_switch": "TR",
        "lang_switch_label": "Türkçe sürüm",
        "refs_title": "References",
        "refs_label": "Reference companies",
        "footer_about": "AIgro builds end-to-end smart systems for soilless farming and water management, from sensor to dashboard. Sensors, controller board, software and installation from one team.",
        "footer_solutions": "Solutions",
        "footer_company": "Company",
        "footer_contact": "Contact",
        "rights": "All rights reserved.",
        "footer_note": "Target figures are based on the literature and are not guaranteed. Dashboard and concept visuals are labelled as such. Greenhouse mood photos are illustrative (Unsplash licence).",
    },
}

UNSPLASH = "https://images.unsplash.com/photo-{id}?auto=format&fit=crop&q=72&w={w}"
WIDTHS = (640, 960, 1400, 2000)


def unsplash(photo_id: str, width: int) -> str:
    return UNSPLASH.format(id=photo_id, w=width)


def srcset(photo_id: str) -> str:
    return ", ".join(f"{unsplash(photo_id, w)} {w}w" for w in WIDTHS)


def icon(name: str, cls: str = "icon") -> str:
    return f'<svg class="{cls}" aria-hidden="true" focusable="false"><use href="#i-{name}"/></svg>'


def expand_macros(html: str) -> str:
    html = re.sub(r"\[\[U ([\w-]+) (\d+)\]\]", lambda m: unsplash(m[1], int(m[2])), html)
    html = re.sub(r"\[\[S ([\w-]+)\]\]", lambda m: srcset(m[1]), html)
    html = re.sub(r"\[\[I ([\w-]+)(?: ([\w -]+))?\]\]", lambda m: icon(m[1], m[2] or "icon"), html)
    return html


def wrap_brand(html: str) -> str:
    """Wrap the brand name in visible text so its capital I renders with serifs (never reads "Algro")."""
    head, sep, body = html.partition("<body>")
    body = re.sub(r">([^<]*)<", lambda m: ">" + m[1].replace("AIgro", '<span class="aigro"><span class="ai">AI</span>gro</span>') + "<", body)
    return head + sep + body


def parse_page(path: Path) -> tuple[dict[str, str], str]:
    raw = path.read_text(encoding="utf-8")
    head, body = raw.split("\n---\n", 1)
    meta = {}
    for line in head.strip().splitlines():
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip()
    return meta, body


def page_url(lang: str, key: str) -> str:
    return SITE_URL + LANGS[lang]["dir"] + ("" if PAGES[lang][key] == "index.html" else PAGES[lang][key])


def build() -> None:
    layout = (SRC / "layout.html").read_text(encoding="utf-8")
    sprite = (SRC / "icons.svg").read_text(encoding="utf-8")
    for lang, conf in LANGS.items():
        other = "en" if lang == "tr" else "tr"
        out_dir = ROOT / conf["dir"]
        out_dir.mkdir(exist_ok=True)
        for page in sorted((SRC / "pages" / lang).glob("*.html")):
            meta, body = parse_page(page)
            key = meta["active"]
            other_href = ("en/" if lang == "tr" else "../") + PAGES[other][key]
            hreflang = "\n  ".join(
                f'<link rel="alternate" hreflang="{code}" href="{page_url(code, key)}">' for code in LANGS
            ) + f'\n  <link rel="alternate" hreflang="x-default" href="{page_url("tr", key)}">'
            html = layout.replace("{{body}}", body)
            replacements = {
                "{{lang}}": lang,
                "{{title}}": meta["title"],
                "{{description}}": meta["description"],
                "{{canonical}}": page_url(lang, key),
                "{{hreflang}}": hreflang,
                "{{og_locale}}": conf["locale"],
                "{{og_image}}": SITE_URL + meta.get("og_image", "assets/img/og-cover.jpg"),
                "{{header_class}}": "is-overlay" if meta.get("header") == "overlay" else "is-solid",
                "{{sprite}}": sprite,
                "{{other_href}}": other_href,
                "{{other_lang}}": other,
                "{{email}}": CONTACT_EMAIL,
                "{{cur_cozum}}": ' data-current="true"' if key in {"dozaj", "su", "dikey"} else "",
            }
            for k, v in replacements.items():
                html = html.replace(k, v)
            for k in PAGES[lang]:
                html = html.replace(f"{{{{cur:{k}}}}}", ' aria-current="page"' if k == key else "")
            html = re.sub(r"\{\{href:(\w+)\}\}", lambda m: PAGES[lang][m[1]], html)
            html = re.sub(r"\{\{t:(\w+)\}\}", lambda m: STRINGS[lang][m[1]], html)
            html = expand_macros(html)
            html = wrap_brand(html)
            if conf["root"]:
                html = re.sub(r'(src|href|srcset)="assets/', rf'\1="{conf["root"]}assets/', html)
            leftover = re.findall(r"\{\{[\w:]+\}\}|\[\[[A-Z] [^\]]*\]\]", html)
            if leftover:
                raise SystemExit(f"{lang}/{page.name}: unresolved placeholders {leftover}")
            out = out_dir / PAGES[lang][key]
            out.write_text(html, encoding="utf-8", newline="\n")
            print(f"built {out.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    build()
