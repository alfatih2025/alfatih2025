import json
import os
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


# ============================================================
# CONFIG
# ============================================================

TOKEN = os.environ["GITHUB_TOKEN"]
USERNAME = os.environ["GITHUB_USERNAME"]

WIDTH = 1000
HEIGHT = 300

CELL = 12
GAP = 5
STEP = CELL + GAP

GRID_X = 42
GRID_Y = 125

FRAMES = 24
FRAME_DURATION = 90


# ============================================================
# COLORS
# ============================================================

BG = (3, 7, 18)

CYAN = (57, 217, 255)
GREEN = (125, 255, 138)

LEVEL_COLORS = {
    "NONE": (8, 30, 42),
    "FIRST_QUARTILE": (18, 57, 74),
    "SECOND_QUARTILE": (28, 145, 168),
    "THIRD_QUARTILE": (57, 217, 255),
    "FOURTH_QUARTILE": (125, 255, 138),
}


# ============================================================
# GITHUB GRAPHQL
# ============================================================

QUERY = """
query($login: String!) {

    user(login: $login) {

        contributionsCollection {

            contributionCalendar {

                totalContributions

                weeks {

                    contributionDays {

                        date

                        contributionCount

                        contributionLevel

                    }

                }

            }

        }

    }

}
"""


payload = json.dumps({
    "query": QUERY,
    "variables": {
        "login": USERNAME
    }
}).encode()


request = urllib.request.Request(

    "https://api.github.com/graphql",

    data=payload,

    headers={
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "User-Agent": "CyberContributionGrid"
    },

    method="POST"
)


with urllib.request.urlopen(request) as response:

    data = json.loads(
        response.read().decode()
    )


if data.get("errors"):

    raise RuntimeError(
        json.dumps(
            data["errors"],
            indent=2
        )
    )


calendar = (
    data["data"]
    ["user"]
    ["contributionsCollection"]
    ["contributionCalendar"]
)


weeks = calendar["weeks"]

total = calendar["totalContributions"]


# ============================================================
# PREPARE CELLS
# ============================================================

cells = []

max_columns = len(weeks)

for column, week in enumerate(weeks):

    for row, day in enumerate(
        week["contributionDays"]
    ):

        x = (
            GRID_X
            + column * STEP
        )

        y = (
            GRID_Y
            + row * STEP
        )

        level = day[
            "contributionLevel"
        ]

        count = day[
            "contributionCount"
        ]

        color = LEVEL_COLORS.get(
            level,
            LEVEL_COLORS["NONE"]
        )

        cells.append({
            "x": x,
            "y": y,
            "color": color,
            "count": count,
            "column": column,
            "row": row
        })


# ============================================================
# FIND STRONGEST POINT PER WEEK
# ============================================================

points = []

for column, week in enumerate(weeks):

    best = None

    for row, day in enumerate(
        week["contributionDays"]
    ):

        count = day[
            "contributionCount"
        ]

        if count <= 0:
            continue

        if best is None or count > best[1]:

            best = (
                row,
                count
            )

    if best:

        row = best[0]

        points.append(
            (
                GRID_X
                + column * STEP
                + CELL // 2,

                GRID_Y
                + row * STEP
                + CELL // 2
            )
        )


# ============================================================
# INTERPOLATION
# ============================================================

def interpolate_points(points, amount):

    if len(points) < 2:

        return None

    position = (
        amount
        * (len(points) - 1)
    )

    index = int(position)

    if index >= len(points) - 1:

        return points[-1]

    fraction = (
        position
        - index
    )

    x1, y1 = points[index]

    x2, y2 = points[index + 1]

    x = (
        x1
        + (x2 - x1)
        * fraction
    )

    y = (
        y1
        + (y2 - y1)
        * fraction
    )

    return (
        int(x),
        int(y)
    )


# ============================================================
# DRAW TEXT
# ============================================================

def draw_header(draw):

    draw.text(
        (GRID_X, 32),
        "SYSTEM://CONTRIBUTION_MATRIX",
        fill=GREEN
    )

    draw.text(
        (GRID_X, 58),
        "CYBER CONTRIBUTION GRID",
        fill=CYAN
    )

    draw.text(
        (GRID_X, 88),
        (
            f"ACTIVITY SIGNAL  |  "
            f"{total} CONTRIBUTIONS  |  "
            f"{USERNAME}"
        ),
        fill=(130, 160, 180)
    )


# ============================================================
# GENERATE FRAMES
# ============================================================

frames = []


for frame_index in range(FRAMES):

    image = Image.new(
        "RGB",
        (WIDTH, HEIGHT),
        BG
    )


    # --------------------------------------------------------
    # BACKGROUND GRID
    # --------------------------------------------------------

    draw = ImageDraw.Draw(
        image
    )


    # subtle horizontal scanlines

    for y in range(
        0,
        HEIGHT,
        4
    ):

        draw.line(
            (0, y, WIDTH, y),
            fill=(5, 15, 28)
        )


    draw_header(draw)


    # --------------------------------------------------------
    # CONTRIBUTION CELLS
    # --------------------------------------------------------

    glow_layer = Image.new(
        "RGBA",
        (WIDTH, HEIGHT),
        (0, 0, 0, 0)
    )

    glow_draw = ImageDraw.Draw(
        glow_layer
    )


    for index, cell in enumerate(
        cells
    ):

        x = cell["x"]

        y = cell["y"]

        color = cell["color"]

        count = cell["count"]


        # Base cell

        draw.rounded_rectangle(

            (
                x,
                y,
                x + CELL,
                y + CELL
            ),

            radius=3,

            fill=color
        )


        if count <= 0:

            continue


        # ----------------------------------------------------
        # Individual pulse
        # ----------------------------------------------------

        phase = (

            frame_index
            * 0.35

            + index
            * 0.11

        )


        pulse = (
            (phase % 6.28)
        )


        if pulse < 1.0:

            strength = (
                1.0
                - pulse
            )

            alpha = int(
                70
                * strength
            )

            glow_color = (
                color[0],
                color[1],
                color[2],
                alpha
            )


            glow_draw.rounded_rectangle(

                (
                    x - 4,
                    y - 4,
                    x + CELL + 4,
                    y + CELL + 4
                ),

                radius=6,

                fill=glow_color
            )


    # Blur cell glow

    glow_layer = glow_layer.filter(
        ImageFilter.GaussianBlur(5)
    )


    image = Image.alpha_composite(
        image.convert("RGBA"),
        glow_layer
    )


    draw = ImageDraw.Draw(
        image
    )


    # --------------------------------------------------------
    # CYBER ENERGY PATH
    # --------------------------------------------------------

    if len(points) >= 2:

        draw.line(
            points,
            fill=(
                57,
                217,
                255,
                55
            ),
            width=2
        )


        # Moving energy node

        progress = (
            frame_index
            / FRAMES
        )


        node = interpolate_points(
            points,
            progress
        )


        if node:

            nx, ny = node


            energy = Image.new(
                "RGBA",
                (WIDTH, HEIGHT),
                (0, 0, 0, 0)
            )


            energy_draw = ImageDraw.Draw(
                energy
            )


            energy_draw.ellipse(

                (
                    nx - 16,
                    ny - 16,
                    nx + 16,
                    ny + 16
                ),

                fill=(
                    125,
                    255,
                    138,
                    100
                )
            )


            energy = energy.filter(
                ImageFilter.GaussianBlur(
                    8
                )
            )


            image = Image.alpha_composite(
                image,
                energy
            )


            draw = ImageDraw.Draw(
                image
            )


            draw.ellipse(

                (
                    nx - 5,
                    ny - 5,
                    nx + 5,
                    ny + 5
                ),

                fill=GREEN
            )


            draw.ellipse(

                (
                    nx - 2,
                    ny - 2,
                    nx + 2,
                    ny + 2
                ),

                fill=(255, 255, 255)
            )


    # --------------------------------------------------------
    # SCANNING BEAM
    # --------------------------------------------------------

    scan_progress = (
        frame_index
        / FRAMES
    )

    scan_x = int(
        GRID_X
        + scan_progress
        * (
            max_columns
            * STEP
        )
    )


    beam = Image.new(
        "RGBA",
        (WIDTH, HEIGHT),
        (0, 0, 0, 0)
    )


    beam_draw = ImageDraw.Draw(
        beam
    )


    beam_draw.rectangle(

        (
            scan_x - 3,
            GRID_Y - 5,
            scan_x + 3,
            GRID_Y + 7 * STEP
        ),

        fill=(
            125,
            255,
            138,
            90
        )
    )


    beam = beam.filter(
        ImageFilter.GaussianBlur(5)
    )


    image = Image.alpha_composite(
        image,
        beam
    )


    draw = ImageDraw.Draw(
        image
    )


    # --------------------------------------------------------
    # FOOTER
    # --------------------------------------------------------

    draw.text(
        (GRID_X, 276),
        "STATUS: ONLINE",
        fill=(80, 110, 130)
    )


    draw.text(
        (
            WIDTH - 150,
            276
        ),
        "● ACTIVE",
        fill=GREEN
    )


    # --------------------------------------------------------
    # SAVE FRAME
    # --------------------------------------------------------

    frames.append(
        image.convert("P", palette=Image.Palette.ADAPTIVE)
    )


# ============================================================
# SAVE GIF
# ============================================================

output_dir = Path(
    "dist"
)

output_dir.mkdir(
    exist_ok=True
)


output = (
    output_dir
    / "cyber-contribution-grid.gif"
)


frames[0].save(

    output,

    save_all=True,

    append_images=frames[1:],

    duration=FRAME_DURATION,

    loop=0,

    optimize=False
)


print(
    "Generated:",
    output
)

print(
    "Username:",
    USERNAME
)

print(
    "Total contributions:",
    total
)

print(
    "Frames:",
    FRAMES
)
