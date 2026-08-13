from pathlib import Path
import math

from PIL import Image, ImageDraw, ImageFont, ImageFilter


OUT = Path("dist")
OUT.mkdir(exist_ok=True)

W = 1000
H = 300

FRAMES = 48
DURATION = 70

BG = (2, 6, 16)
CYAN = (55, 220, 255)
GREEN = (120, 255, 145)
GRID = (7, 25, 38)
MUTED = (75, 105, 125)


def get_font(size):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]

    for path in paths:
        if Path(path).exists():
            return ImageFont.truetype(path, size)

    return ImageFont.load_default()


FONT_LOGO = get_font(92)
FONT_SMALL = get_font(12)
FONT_STATUS = get_font(11)


def draw_grid(draw):
    for x in range(0, W, 40):
        draw.line(
            (x, 0, x, H),
            fill=GRID,
            width=1
        )

    for y in range(0, H, 40):
        draw.line(
            (0, y, W, y),
            fill=GRID,
            width=1
        )


def glow_text(
    image,
    position,
    text,
    font,
    color,
    blur=14
):
    glow = Image.new(
        "RGBA",
        image.size,
        (0, 0, 0, 0)
    )

    glow_draw = ImageDraw.Draw(glow)

    glow_draw.text(
        position,
        text,
        font=font,
        fill=(*color, 220),
        anchor="mm"
    )

    glow = glow.filter(
        ImageFilter.GaussianBlur(blur)
    )

    image.alpha_composite(glow)

    draw = ImageDraw.Draw(image)

    draw.text(
        position,
        text,
        font=font,
        fill=(*color, 255),
        anchor="mm"
    )


def glow_point(
    image,
    x,
    y,
    radius,
    color
):
    glow = Image.new(
        "RGBA",
        image.size,
        (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(glow)

    draw.ellipse(
        (
            x - radius * 4,
            y - radius * 4,
            x + radius * 4,
            y + radius * 4
        ),
        fill=(*color, 100)
    )

    glow = glow.filter(
        ImageFilter.GaussianBlur(radius * 2)
    )

    image.alpha_composite(glow)

    draw = ImageDraw.Draw(image)

    draw.ellipse(
        (
            x - radius,
            y - radius,
            x + radius,
            y + radius
        ),
        fill=(*color, 255)
    )


frames = []


for frame in range(FRAMES):

    image = Image.new(
        "RGBA",
        (W, H),
        (*BG, 255)
    )

    draw = ImageDraw.Draw(image)

    draw_grid(draw)

    # -------------------------------------------------
    # HEADER BORDER
    # -------------------------------------------------

    draw.rounded_rectangle(
        (20, 20, W - 20, H - 20),
        radius=18,
        outline=(18, 70, 90),
        width=2
    )

    # -------------------------------------------------
    # CYBER CIRCUITS
    # -------------------------------------------------

    center_y = H // 2

    left_start = 80
    left_end = 400

    right_start = 600
    right_end = 920

    draw.line(
        (left_start, center_y, left_end, center_y),
        fill=(18, 75, 95),
        width=2
    )

    draw.line(
        (right_start, center_y, right_end, center_y),
        fill=(18, 75, 95),
        width=2
    )

    # vertical circuit branches

    draw.line(
        (180, center_y, 180, 95),
        fill=(18, 75, 95),
        width=2
    )

    draw.line(
        (820, center_y, 820, 205),
        fill=(18, 75, 95),
        width=2
    )

    # -------------------------------------------------
    # MOVING DATA PACKETS
    # -------------------------------------------------

    for side in [0, 1]:

        progress = (
            frame / FRAMES
            + side * 0.5
        ) % 1

        if side == 0:

            x = (
                left_start
                + (left_end - left_start)
                * progress
            )

        else:

            x = (
                right_start
                + (right_end - right_start)
                * progress
            )

        glow_point(
            image,
            x,
            center_y,
            3,
            CYAN
        )

    # -------------------------------------------------
    # LOGO RING
    # -------------------------------------------------

    cx = W // 2
    cy = H // 2

    pulse = (
        math.sin(
            frame * math.pi * 2 / FRAMES
        ) + 1
    ) / 2

    radius = 74 + pulse * 8

    draw = ImageDraw.Draw(image)

    draw.ellipse(
        (
            cx - radius,
            cy - radius,
            cx + radius,
            cy + radius
        ),
        outline=(20, 90, 110),
        width=2
    )

    # rotating ring segment

    angle = (
        frame / FRAMES
    ) * math.pi * 2

    segment_length = math.pi / 2

    draw.arc(
        (
            cx - radius,
            cy - radius,
            cx + radius,
            cy + radius
        ),
        start=math.degrees(angle),
        end=math.degrees(
            angle + segment_length
        ),
        fill=GREEN,
        width=4
    )

    # -------------------------------------------------
    # AL LOGO
    # -------------------------------------------------

    logo_position = (cx, cy - 3)

    glow_text(
        image,
        logo_position,
        "AL",
        FONT_LOGO,
        CYAN,
        blur=18
    )

    # -------------------------------------------------
    # TOP SYSTEM LABEL
    # -------------------------------------------------

    draw = ImageDraw.Draw(image)

    draw.text(
        (45, 43),
        "ALTECH // CORE SYSTEM",
        font=FONT_SMALL,
        fill=GREEN
    )

    draw.text(
        (W - 45, 43),
        "SOFTWARE / AI / IoT",
        font=FONT_SMALL,
        fill=MUTED,
        anchor="ra"
    )

    # -------------------------------------------------
    # BOTTOM STATUS
    # -------------------------------------------------

    draw.text(
        (45, H - 43),
        "INITIALIZING DIGITAL SYSTEM",
        font=FONT_STATUS,
        fill=MUTED
    )

    status = [
        "● SYSTEM ONLINE",
        "● CORE ACTIVE",
        "● ALL SYSTEMS ONLINE"
    ]

    status_index = (
        frame // 16
    ) % len(status)

    draw.text(
        (W - 45, H - 43),
        status[status_index],
        font=FONT_STATUS,
        fill=GREEN,
        anchor="ra"
    )

    # -------------------------------------------------
    # SCANLINE
    # -------------------------------------------------

    scan_y = (
        35
        + (frame / FRAMES) * (H - 70)
    )

    draw.line(
        (30, scan_y, W - 30, scan_y),
        fill=(55, 220, 255, 55),
        width=1
    )

    frames.append(
        image.convert("P")
    )


frames[0].save(
    OUT / "header-al.gif",
    save_all=True,
    append_images=frames[1:],
    duration=DURATION,
    loop=0,
    optimize=False
)

print("Generated:")
print(OUT / "header-al.gif")
