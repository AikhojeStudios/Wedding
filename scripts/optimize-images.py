#!/usr/bin/env python3
"""Rebuild images/opt/*.webp and images/og.jpg from the JPEGs in images/.

GitHub Pages serves the committed files directly. Run this after adding or
replacing a gallery JPEG, then point that photo's srcset at the new WebP
files (640w, and 1200w or the original width when it is smaller than 1200).

Requires Pillow: pip install pillow
"""

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "images"
OUT = SRC / "opt"


def target_widths(width: int) -> list[int]:
    widths = [640] if width > 700 else []
    large = 1200 if width >= 1200 else width
    if large not in widths:
        widths.append(large)
    return widths or [width]


def main() -> None:
    OUT.mkdir(exist_ok=True)
    for path in sorted(SRC.glob("*.jpg")):
        if path.name == "og.jpg":
            continue
        image = Image.open(path).convert("RGB")
        width, height = image.size
        for tw in target_widths(width):
            resized = image
            if tw != width:
                th = max(1, round(height * (tw / width)))
                resized = image.resize((tw, th), Image.Resampling.LANCZOS)
            dest = OUT / f"{path.stem}-{tw}.webp"
            resized.save(dest, "WEBP", quality=74, method=4)
            print(dest.relative_to(ROOT))

    source = Image.open(SRC / "film-beach-couple.jpg").convert("RGB")
    ow, oh = source.size
    ratio = 1200 / 630
    if ow / oh > ratio:
        new_w = int(oh * ratio)
        left = (ow - new_w) // 2
        crop = source.crop((left, 0, left + new_w, oh))
    else:
        new_h = int(ow / ratio)
        top = (oh - new_h) // 2
        crop = source.crop((0, top, ow, top + new_h))
    og = crop.resize((1200, 630), Image.Resampling.LANCZOS)
    og_path = SRC / "og.jpg"
    og.save(og_path, "JPEG", quality=80, optimize=True, progressive=True)
    print(og_path.relative_to(ROOT))


if __name__ == "__main__":
    main()
