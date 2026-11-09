"""Builds the static AIgro site from src/ into the repository root.

Each page in src/pages/*.html starts with a small front-matter block:

    title: Page title
    description: Meta description
    header: overlay | solid
    active: index | dozaj | su | dikey | iletisim
    ---
    <main> ... </main>

Macros inside pages:
    [[U <unsplash-id> <width>]]  -> Unsplash CDN URL at that width
    [[S <unsplash-id>]]          -> responsive srcset for that photo
    [[I <icon>]]                 -> inline SVG icon from the sprite

Run:  python tools/build.py
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
SITE_URL = "https://tarikyil.github.io/aigro-web/"

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


def nav_current(meta: dict[str, str], key: str) -> str:
    return ' aria-current="page"' if meta.get("active") == key else ""


def build() -> None:
    layout = (SRC / "layout.html").read_text(encoding="utf-8")
    sprite = (SRC / "icons.svg").read_text(encoding="utf-8")
    for page in sorted((SRC / "pages").glob("*.html")):
        meta, body = parse_page(page)
        out_name = page.name
        canonical = SITE_URL + ("" if out_name == "index.html" else out_name)
        html = layout
        replacements = {
            "{{title}}": meta["title"],
            "{{description}}": meta["description"],
            "{{canonical}}": canonical,
            "{{og_image}}": SITE_URL + meta.get("og_image", "assets/img/og-cover.jpg"),
            "{{header_class}}": "is-overlay" if meta.get("header") == "overlay" else "is-solid",
            "{{sprite}}": sprite,
            "{{body}}": body,
            "{{cur_dozaj}}": nav_current(meta, "dozaj"),
            "{{cur_su}}": nav_current(meta, "su"),
            "{{cur_dikey}}": nav_current(meta, "dikey"),
            "{{cur_iletisim}}": nav_current(meta, "iletisim"),
            "{{cur_cozum}}": ' data-current="true"' if meta.get("active") in {"dozaj", "su", "dikey"} else "",
        }
        for key, value in replacements.items():
            html = html.replace(key, value)
        html = expand_macros(html)
        html = wrap_brand(html)
        leftover = re.findall(r"\{\{\w+\}\}|\[\[[A-Z] [^\]]*\]\]", html)
        if leftover:
            raise SystemExit(f"{page.name}: unresolved placeholders {leftover}")
        (ROOT / out_name).write_text(html, encoding="utf-8", newline="\n")
        print(f"built {out_name}")


if __name__ == "__main__":
    build()
