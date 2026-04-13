"""Generate placeholder raster assets for the project page (replace with exports from the paper when available)."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
IMG = ROOT / "static" / "images"


def _font(size: int):
    for name in ("arial.ttf", "SegoeUI.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def gradient_bg(w: int, h: int, top: tuple[int, int, int], bottom: tuple[int, int, int]) -> Image.Image:
    im = Image.new("RGB", (w, h))
    px = im.load()
    for y in range(h):
        t = y / max(h - 1, 1)
        c = (
            int(top[0] * (1 - t) + bottom[0] * t),
            int(top[1] * (1 - t) + bottom[1] * t),
            int(top[2] * (1 - t) + bottom[2] * t),
        )
        for x in range(w):
            px[x, y] = c
    return im


def draw_centered_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    y: int,
    w: int,
    fill: tuple[int, int, int],
    font: ImageFont.FreeTypeFont | ImageFont.ImageFont,
):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) // 2, y), text, font=font, fill=fill)


def social_preview():
    w, h = 1200, 630
    im = gradient_bg(w, h, (15, 23, 42), (30, 64, 175))
    draw = ImageDraw.Draw(im)
    title_f = _font(56)
    sub_f = _font(28)
    small_f = _font(22)
    draw_centered_text(draw, "FlowCoMotion", 200, w, (248, 250, 252), title_f)
    draw_centered_text(
        draw,
        "Text-to-Motion Generation via Token–Latent Flow Modeling",
        290,
        w,
        (203, 213, 225),
        sub_f,
    )
    draw_centered_text(draw, "USTC · Preprint 2026", 380, w, (148, 163, 184), small_f)
    im.save(IMG / "social_preview.png", optimize=True)


def carousel(name: str, title: str, subtitle: str, accent: tuple[int, int, int]):
    w, h = 1280, 720
    im = gradient_bg(w, h, (17, 24, 39), accent)
    draw = ImageDraw.Draw(im)
    tf = _font(44)
    sf = _font(26)
    draw_centered_text(draw, title, 280, w, (255, 255, 255), tf)
    draw_centered_text(draw, subtitle, 360, w, (226, 232, 240), sf)
    draw_centered_text(draw, "Placeholder — replace with figure export from the paper", 440, w, (148, 163, 184), _font(20))
    im.convert("RGB").save(IMG / f"{name}.jpg", quality=88, optimize=True)


def favicon():
    size = 64
    im = gradient_bg(size, size, (37, 99, 235), (15, 23, 42))
    draw = ImageDraw.Draw(im)
    f = _font(28)
    draw.text((10, 16), "FC", font=f, fill=(255, 255, 255))
    im.save(IMG / "favicon.ico", format="ICO", sizes=[(32, 32), (16, 16)])


def teaser_poster():
    """Static poster for teaser <video> when no MP4 is bundled."""
    w, h = 1280, 720
    im = gradient_bg(w, h, (30, 58, 138), (15, 23, 42))
    draw = ImageDraw.Draw(im)
    draw_centered_text(draw, "FlowCoMotion", 260, w, (248, 250, 252), _font(52))
    draw_centered_text(
        draw,
        "Teaser video: add static/videos/banner_video.mp4 or embed YouTube",
        340,
        w,
        (203, 213, 225),
        _font(24),
    )
    im.save(IMG / "teaser_poster.png", optimize=True)


def main():
    IMG.mkdir(parents=True, exist_ok=True)
    social_preview()
    favicon()
    teaser_poster()
    carousel("carousel1", "Fine-grained text-to-motion", "Token–latent coupling captures semantics and dynamics", (79, 70, 229))
    carousel("carousel2", "Method overview", "VAE branches + flow matching with ODE sampling", (14, 165, 233))
    carousel("carousel3", "Qualitative comparison", "Stronger alignment on direction, degrees, and geometry", (22, 163, 74))
    carousel("carousel4", "Benchmarks", "HumanML3D & SnapMoGen", (217, 119, 6))
    print("Wrote assets to", IMG)


if __name__ == "__main__":
    main()
