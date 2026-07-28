"""Generate branded placeholder 'methodology' thumbnails for publications.
Swap these out with real methodology figures anytime (keep the same filenames)."""
import math, random
from PIL import Image, ImageDraw, ImageFont

W, H = 320, 220  # 2x for crispness

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# venue -> (top color, bottom color)
THEMES = {
    "icra":   ((233, 108, 44),  (176, 63, 18)),    # orange
    "miccai": ((123, 79, 196),  (90, 47, 158)),     # purple
    "journal":((26, 154, 140),  (15, 111, 102)),    # teal
}

def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

def make(name, acronym, tag, theme):
    top, bot = THEMES[theme]
    img = Image.new("RGB", (W, H))
    px = img.load()
    for y in range(H):
        c = lerp(top, bot, y / H)
        for x in range(W):
            px[x, y] = c
    d = ImageDraw.Draw(img, "RGBA")

    # faint schematic: layered nodes + connections (a 'pipeline / network' motif)
    random.seed(hash(name) & 0xffff)
    cols = [45, 130, 215, 285]
    layers = []
    for i, cx in enumerate(cols):
        n = [2, 3, 3, 2][i]
        ys = [H * (k + 1) / (n + 1) for k in range(n)]
        layers.append([(cx, y) for y in ys])
    # connections
    for i in range(len(layers) - 1):
        for (x1, y1) in layers[i]:
            for (x2, y2) in layers[i + 1]:
                d.line([(x1, y1), (x2, y2)], fill=(255, 255, 255, 32), width=1)
    # nodes
    for layer in layers:
        for (x, y) in layer:
            r = 6
            d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, 55))

    # subtle dark scrim for text legibility
    d.rectangle([0, H - 92, W, H], fill=(0, 0, 0, 55))

    # acronym
    size = 46
    fb = ImageFont.truetype(FB, size)
    while d.textlength(acronym, font=fb) > W - 36 and size > 22:
        size -= 2
        fb = ImageFont.truetype(FB, size)
    d.text((22, H - 84), acronym, font=fb, fill=(255, 255, 255, 255))

    # tag line
    tsize = 23
    fr = ImageFont.truetype(FR, tsize)
    tg = tag.upper()
    while d.textlength(tg, font=fr) > W - 36 and tsize > 15:
        tsize -= 1
        fr = ImageFont.truetype(FR, tsize)
    d.text((23, H - 36), tg, font=fr, fill=(255, 255, 255, 230))

    img.save(f"pub/{name}.png")
    print("wrote", name)

items = [
    ("spread",   "SPREAD",     "Subspace Distillation",             "icra"),
    ("wildcross","WildCross",  "Place Recognition · Depth",         "icra"),
    ("dual3dfed","DUAL3D-Fed",  "3D Federated · VLM",               "journal"),
    ("m2distill","M2Distill",  "Multi-Modal Distillation",          "icra"),
    ("l3dmc",    "L3DMC",      "Mixed-Curvature Distillation",      "miccai"),
    ("subspace", "Subspace",   "Continual Learning",                "journal"),
    ("cl3",      "CL3",        "Contrastive Lifelong Loss",         "journal"),
    ("ddp",      "DDP",        "Directional Pattern · BG Sub",      "journal"),
    ("fusion",   "Fusion",     "Color–Edge Feature Fusion",         "miccai"),
]

import os
os.makedirs("pub", exist_ok=True)
for it in items:
    make(*it)
print("done")
