"""Generate the site's code-made graphics.

Run from the repository root:  python scripts/make_graphics.py
Needs Pillow (pip install pillow). Outputs go to assets/img/.

- scatter-to-order.svg  decorative home-page strip: scattered points on the
                        left settle into orderly columns on the right.
- favicon.svg           simple mark: three ascending bars.
- og-image.png          1200x630 social-share card.
"""
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path("assets/img")
ACCENT = "#0E6B69"      # keep in sync with $accent in assets/css/custom.scss
NEUTRAL = "#8A9197"     # mid-grey that reads on light and dark backgrounds
PAPER = "#FAFAF7"
INK = "#1C2024"


def scatter_to_order(w=960, h=200, seed=7):
    rng = random.Random(seed)
    cols, gap, r_dot = 32, 18, 4.5
    step = (w - 20) / (cols - 1)
    circles = []
    for c in range(cols):
        t = c / (cols - 1)                   # 0 = messy (left), 1 = ordered (right)
        ease = t * t * (3 - 2 * t)           # smoothstep
        # Ordered state: a gently rising "bar chart" of stacked dots.
        height = 2 + round(6 * (1 - math.cos(t * math.pi)) / 2)
        for row in range(height):
            x_ord, y_ord = 10 + c * step, h - 12 - row * gap
            x_mess = x_ord + rng.uniform(-step * 1.5, step * 1.5)
            y_mess = rng.uniform(12, h - 12)
            x = x_mess * (1 - ease) + x_ord * ease
            y = y_mess * (1 - ease) + y_ord * ease
            colour = ACCENT if t > 0.5 else NEUTRAL
            opacity = 0.5 + 0.5 * ease
            circles.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r_dot}" fill="{colour}" fill-opacity="{opacity:.2f}"/>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
           f'role="presentation" aria-hidden="true">' + "".join(circles) + "</svg>\n")
    (OUT / "scatter-to-order.svg").write_text(svg, encoding="utf-8")


def favicon():
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
<rect width="64" height="64" rx="12" fill="{ACCENT}"/>
<rect x="14" y="36" width="9" height="14" rx="2" fill="#fff"/>
<rect x="27.5" y="26" width="9" height="24" rx="2" fill="#fff"/>
<rect x="41" y="14" width="9" height="36" rx="2" fill="#fff"/>
</svg>
'''
    (OUT / "favicon.svg").write_text(svg, encoding="utf-8")


def og_image():
    w, h = 1200, 630
    img = Image.new("RGB", (w, h), PAPER)
    d = ImageDraw.Draw(img)
    try:
        title = ImageFont.truetype("georgiab.ttf", 72)
        body = ImageFont.truetype("georgia.ttf", 34)
    except OSError:
        title = body = ImageFont.load_default()
    d.rectangle((80, 150, 150, 156), fill=ACCENT)
    d.text((80, 190), "Daniel Yorke Consulting", font=title, fill=INK)
    d.text((80, 300), "Analytics, data, and 1:1 AI consulting", font=body, fill="#545B62")
    d.text((80, 350), "for small businesses and busy professionals.", font=body, fill="#545B62")
    rng = random.Random(3)
    for c in range(14):
        for r in range(2 + c // 2):
            d.ellipse((620 + c * 38, 560 - r * 30, 632 + c * 38, 572 - r * 30), fill=ACCENT)
    for _ in range(40):
        x, y = rng.uniform(80, 580), rng.uniform(430, 580)
        d.ellipse((x, y, x + 12, y + 12), fill=NEUTRAL)
    img.save(OUT / "og-image.png", optimize=True)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    scatter_to_order()
    favicon()
    og_image()
    print("Wrote graphics to", OUT)
