"""Generates the social preview cards (assets/img/og-cover.jpg, og-cover-en.jpg).

Run:  python tools/og_cards.py   (Windows fonts: Segoe UI, Georgia)
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "assets" / "img"
FONTS = Path("C:/Windows/Fonts")
CHIP_COLOURS = [(111, 227, 210), (169, 201, 255), (233, 169, 200)]


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONTS / name), size)


def card(lines: list[str], tagline: str, chips: list[str], out: Path) -> None:
    w, h = 1200, 630
    im = Image.new("RGB", (w, h), (12, 26, 46))
    glow = Image.new("L", (w, h), 0)
    ImageDraw.Draw(glow).ellipse((700, -250, 1400, 450), fill=90)
    im.paste(Image.new("RGB", (w, h), (0, 191, 165)), (0, 0), glow.filter(ImageFilter.GaussianBlur(120)))
    d = ImageDraw.Draw(im)

    panel = Image.open(IMG / "dozaj-panel.webp").convert("RGB")
    panel = panel.resize((640, round(panel.height * 640 / panel.width)), Image.LANCZOS)
    mask = Image.new("L", panel.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, *panel.size), 18, fill=255)
    im.paste(panel, (640, 175), mask)

    mark = Image.new("RGB", (64, 64))
    md = ImageDraw.Draw(mark)
    for i in range(64):
        md.line((0, i, 64, i), fill=(round(36 * i / 64), round(191 - 67 * i / 64), round(165 + 90 * i / 64)))
    mmask = Image.new("L", (64, 64), 0)
    ImageDraw.Draw(mmask).rounded_rectangle((0, 0, 63, 63), 17, fill=255)
    im.paste(mark, (64, 64), mmask)
    d.polygon([(96, 80), (80, 106), (84, 116), (96, 122), (108, 116), (112, 106)], fill="white")

    serif, bold = font("georgiab.ttf", 46), font("segoeuib.ttf", 46)
    d.text((144, 66), "AI", font=serif, fill=(0, 191, 165))
    d.text((144 + d.textlength("AI", font=serif) + 2, 62), "gro", font=bold, fill="white")

    y = 200
    for line in lines:
        d.text((64, y), line, font=font("segoeuib.ttf", 44), fill="white")
        y += 56
    d.text((64, y + 16), tagline, font=font("segoeui.ttf", 27), fill=(195, 208, 226))

    small, x = font("seguisb.ttf", 22), 64
    for text, colour in zip(chips, CHIP_COLOURS):
        tw = d.textlength(text, font=small)
        d.rounded_rectangle((x, 540, x + tw + 32, 580), 20, outline=colour, width=2)
        d.text((x + 16, 546), text, font=small, fill=colour)
        x += tw + 46
    im.save(out, quality=88)
    print(f"wrote {out.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    card(["Yapay zekâ ile akıllı", "dozajlama, su takibi", "ve dikey tarım"], "Ölçer, öngörür, güvenle uygular.",
         ["Su takibi", "Akıllı dozajlama", "Dikey tarım"], IMG / "og-cover.jpg")
    card(["AI-powered dosing,", "water monitoring and", "vertical farming"], "Measures, forecasts, acts safely.",
         ["Water monitoring", "Smart dosing", "Vertical farming"], IMG / "og-cover-en.jpg")
