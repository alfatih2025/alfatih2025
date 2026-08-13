from pathlib import Path
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = Path("dist")
OUT.mkdir(exist_ok=True)

W, H = 1000, 380
FRAMES = 48
DURATION = 75

BG = (3, 7, 18)
CYAN = (57, 217, 255)
GREEN = (125, 255, 138)
MUTED = (90, 120, 145)
GRID = (5, 18, 30)
PANEL = (4, 12, 24)


def font(size):
    for p in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

F10 = font(10)
F12 = font(12)
F14 = font(14)
F18 = font(18)
F28 = font(28)


def background(draw):
    draw.rectangle((0, 0, W, H), fill=BG)
    for y in range(0, H, 5):
        draw.line((0, y, W, y), fill=(5, 14, 25))
    for x in range(0, W, 50):
        draw.line((x, 0, x, H), fill=(4, 13, 23))


def glow_line(base, points, color=CYAN, width=3):
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.line(points, fill=(*color, 130), width=width * 5, joint="curve")
    layer = layer.filter(ImageFilter.GaussianBlur(7))
    base.alpha_composite(layer)
    ImageDraw.Draw(base).line(points, fill=(*color, 230), width=width, joint="curve")


def glow_dot(base, x, y, radius=5, color=CYAN):
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse((x-radius*4, y-radius*4, x+radius*4, y+radius*4), fill=(*color, 80))
    layer = layer.filter(ImageFilter.GaussianBlur(7))
    base.alpha_composite(layer)
    ImageDraw.Draw(base).ellipse((x-radius, y-radius, x+radius, y+radius), fill=(*color, 255))


def panel(draw, box, title):
    x1, y1, x2, y2 = box
    draw.rounded_rectangle(box, radius=14, outline=(18, 60, 78), width=2, fill=PANEL)
    draw.text((x1 + 18, y1 + 14), title, font=F12, fill=GREEN)
    draw.line((x1 + 18, y1 + 38, x2 - 18, y1 + 38), fill=(18, 60, 78))


# Software-development pipeline:
# EDITOR -> CODE -> BUILD -> API -> DATABASE -> DEPLOY
nodes = [
    (100, 210, "CODE"),
    (260, 210, "BUILD"),
    (420, 210, "API"),
    (580, 210, "DATABASE"),
    (740, 210, "CLOUD"),
    (900, 210, "DEPLOY"),
]

stacks = [
    "PYTHON  C++  JS/TS  PHP",
    "REACT  VITE  TAILWIND",
    "LARAVEL  REST  MQTT",
    "MYSQL  SUPABASE",
    "VERCEL  RAILWAY  CLOUD",
    "CI/CD  GIT  GITHUB",
]

frames = []

for f in range(FRAMES):
    im = Image.new("RGBA", (W, H), BG + (255,))
    d = ImageDraw.Draw(im)
    background(d)
    panel(d, (20, 20, 980, 360), "SOFTWARE://DEVELOPMENT_CORE")

    d.text((42, 68), "SOFTWARE DEVELOPMENT", font=F28, fill=CYAN)
    d.text((42, 104), "CODE → BUILD → API → DATA → CLOUD → DEPLOY", font=F10, fill=MUTED)

    # Code-editor style window on the left.
    d.rounded_rectangle((45, 135, 250, 320), radius=10, fill=(3, 10, 20), outline=(15, 55, 72), width=2)
    d.text((62, 150), "main.py", font=F12, fill=GREEN)
    code_lines = [
        "def build_system():",
        "    api = connect()",
        "    data = process()",
        "    deploy(api, data)",
        "    return ONLINE",
    ]
    for i, text in enumerate(code_lines):
        d.text((62, 180 + i * 22), text, font=F10, fill=CYAN if i != 4 else GREEN)

    # Pipeline.
    for i in range(len(nodes) - 1):
        x1, y1, _ = nodes[i]
        x2, y2, _ = nodes[i + 1]
        glow_line(im, [(x1 + 50, y1), (x2 - 50, y2)], CYAN, 2)

    for i, (x, y, label) in enumerate(nodes):
        pulse = 1 + 0.18 * math.sin(f * 0.3 + i)
        r = 18 * pulse
        glow_dot(im, x, y, 5, GREEN if i == 5 else CYAN)
        d = ImageDraw.Draw(im)
        d.rounded_rectangle((x - 52, y - 35, x + 52, y + 35), radius=9, fill=(5, 18, 30), outline=GREEN if i == 5 else CYAN, width=2)
        d.text((x - 35 if label != "DATABASE" else x - 40, y - 7), label, font=F10, fill=GREEN if i == 5 else CYAN)
        d.text((x - 48, y + 43), stacks[i], font=F10, fill=MUTED)

    # Animated data packet traversing the software pipeline.
    segment_count = len(nodes) - 1
    pos = (f / FRAMES) * segment_count
    seg = min(int(pos), segment_count - 1)
    t = pos - seg
    x1, y1, _ = nodes[seg]
    x2, y2, _ = nodes[seg + 1]
    px = x1 + (x2 - x1) * t
    py = y1 + (y2 - y1) * t
    glow_dot(im, px, py, 6, GREEN)

    # Terminal status / progress.
    scan = (f * 8) % 170
    d = ImageDraw.Draw(im)
    d.text((280, 300), "> BUILD PIPELINE", font=F10, fill=MUTED)
    d.rectangle((280, 320, 750, 326), fill=(8, 25, 38))
    d.rectangle((280, 320, 280 + scan, 326), fill=GREEN)
    d.text((765, 316), "ONLINE", font=F10, fill=GREEN)

    frames.append(im.convert("P"))

frames[0].save(
    OUT / "software-development.gif",
    save_all=True,
    append_images=frames[1:],
    duration=DURATION,
    loop=0,
    optimize=False,
)

print("Generated", OUT / "software-development.gif")
