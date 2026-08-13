import json
import os
import urllib.request
from pathlib import Path
from xml.sax.saxutils import escape


TOKEN = os.environ["GITHUB_TOKEN"]
USERNAME = os.environ["GITHUB_USERNAME"]


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


# ============================================================
# GET GITHUB CONTRIBUTION DATA
# ============================================================

payload = json.dumps({
    "query": QUERY,
    "variables": {
        "login": USERNAME
    }
}).encode("utf-8")


request = urllib.request.Request(
    "https://api.github.com/graphql",
    data=payload,
    headers={
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "User-Agent": "Cyber-Contribution-Grid"
    },
    method="POST"
)


with urllib.request.urlopen(request) as response:
    data = json.loads(
        response.read().decode("utf-8")
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
# SVG CONFIGURATION
# ============================================================

CELL_SIZE = 11
GAP = 5
STEP = CELL_SIZE + GAP

LEFT = 42
TOP = 118

ROWS = 7
COLUMNS = len(weeks)

GRID_WIDTH = (
    COLUMNS * STEP
    - GAP
)

GRID_HEIGHT = (
    ROWS * STEP
    - GAP
)

WIDTH = (
    LEFT * 2
    + GRID_WIDTH
)

HEIGHT = 235


# ============================================================
# CONTRIBUTION COLORS
# ============================================================

COLORS = {

    "NONE":
        "#0a2230",

    "FIRST_QUARTILE":
        "#12394a",

    "SECOND_QUARTILE":
        "#1c91a8",

    "THIRD_QUARTILE":
        "#39d9ff",

    "FOURTH_QUARTILE":
        "#7dff8a"
}


# ============================================================
# SVG HELPER
# ============================================================

def create_cell(
    x,
    y,
    color
):

    return (
        f'<rect '
        f'x="{x}" '
        f'y="{y}" '
        f'width="{CELL_SIZE}" '
        f'height="{CELL_SIZE}" '
        f'rx="3" '
        f'fill="{color}"/>'
    )


# ============================================================
# SVG START
# ============================================================

svg = []


svg.append(
f'''
<svg
xmlns="http://www.w3.org/2000/svg"
width="{WIDTH}"
height="{HEIGHT}"
viewBox="0 0 {WIDTH} {HEIGHT}">

<defs>

    <linearGradient
        id="background"
        x1="0"
        y1="0"
        x2="1"
        y2="1">

        <stop
            offset="0%"
            stop-color="#050816"/>

        <stop
            offset="55%"
            stop-color="#07152a"/>

        <stop
            offset="100%"
            stop-color="#03130f"/>

    </linearGradient>


    <linearGradient
        id="titleGradient"
        x1="0"
        x2="1">

        <stop
            offset="0%"
            stop-color="#39d9ff"/>

        <stop
            offset="100%"
            stop-color="#7dff8a"/>

    </linearGradient>


    <filter id="glow">

        <feGaussianBlur
            stdDeviation="2.5"
            result="blur"/>

        <feMerge>

            <feMergeNode
                in="blur"/>

            <feMergeNode
                in="SourceGraphic"/>

        </feMerge>

    </filter>


    <filter id="softGlow">

        <feGaussianBlur
            stdDeviation="7"
            result="blur"/>

        <feMerge>

            <feMergeNode
                in="blur"/>

            <feMergeNode
                in="SourceGraphic"/>

        </feMerge>

    </filter>


    <pattern
        id="scanlines"
        width="4"
        height="4"
        patternUnits="userSpaceOnUse">

        <rect
            width="4"
            height="2"
            fill="#ffffff"
            opacity="0.018"/>

    </pattern>

</defs>


<!-- BACKGROUND -->

<rect
    width="100%"
    height="100%"
    rx="18"
    fill="url(#background)"/>


<rect
    width="100%"
    height="100%"
    rx="18"
    fill="url(#scanlines)"/>


<!-- CIRCUIT DECORATION -->

<g
    fill="none"
    stroke="#39d9ff"
    stroke-width="1"
    opacity="0.25">

    <path d="M18 32 H105 V17 H190"/>

    <path d="M710 20 H790 V40 H880"/>

    <path d="M20 207 H92 V225 H180"/>

    <path d="M720 225 H805 V205 H880"/>

</g>


<g
    fill="#39d9ff"
    filter="url(#glow)">

    <circle
        cx="105"
        cy="32"
        r="2.5"/>

    <circle
        cx="790"
        cy="40"
        r="2.5"/>

    <circle
        cx="92"
        cy="207"
        r="2.5"/>

    <circle
        cx="805"
        cy="205"
        r="2.5"/>

</g>


<!-- HEADER -->

<text
    x="{LEFT}"
    y="38"
    font-family="monospace"
    font-size="11"
    fill="#7dff8a">

    SYSTEM://CONTRIBUTION_MATRIX

</text>


<text
    x="{LEFT}"
    y="68"
    font-family="Arial, sans-serif"
    font-size="25"
    font-weight="700"
    fill="url(#titleGradient)">

    CYBER CONTRIBUTION GRID

</text>


<text
    x="{LEFT}"
    y="90"
    font-family="monospace"
    font-size="10"
    fill="#8ba3b8">

    ACTIVITY SIGNAL | {total} CONTRIBUTIONS | {escape(USERNAME)}

</text>


<!-- GRID GLOW -->

<rect
    x="{LEFT - 8}"
    y="{TOP - 8}"
    width="{GRID_WIDTH + 16}"
    height="{GRID_HEIGHT + 16}"
    rx="10"
    fill="#39d9ff"
    opacity="0.025"
    filter="url(#softGlow)"/>

'''
)


# ============================================================
# DRAW CONTRIBUTION GRID
# ============================================================

points = []


for column, week in enumerate(weeks):

    days = week["contributionDays"]


    for row, day in enumerate(days):

        x = (
            LEFT
            + column * STEP
        )

        y = (
            TOP
            + row * STEP
        )


        level = day[
            "contributionLevel"
        ]


        count = day[
            "contributionCount"
        ]


        color = COLORS.get(
            level,
            COLORS["NONE"]
        )


        # Glow untuk contribution tinggi

        if level in (
            "THIRD_QUARTILE",
            "FOURTH_QUARTILE"
        ):

            svg.append(
                f'''
<rect
    x="{x - 2}"
    y="{y - 2}"
    width="{CELL_SIZE + 4}"
    height="{CELL_SIZE + 4}"
    rx="5"
    fill="{color}"
    opacity="0.18"
    filter="url(#softGlow)"/>
'''
            )


        # Cell

        svg.append(
            create_cell(
                x,
                y,
                color
            )
        )


        # Highlight kecil

        if count > 0:

            svg.append(
                f'''
<rect
    x="{x + 2}"
    y="{y + 2}"
    width="3"
    height="2"
    rx="1"
    fill="#ffffff"
    opacity="0.16"/>
'''
            )


    # ========================================================
    # CARI CELL PALING AKTIF DALAM MINGGU
    # ========================================================

    active_days = [

        (
            row,
            day["contributionCount"]
        )

        for row, day
        in enumerate(days)

        if day["contributionCount"] > 0
    ]


    if active_days:

        strongest_row = max(
            active_days,
            key=lambda item: item[1]
        )[0]


        points.append(

            (
                LEFT
                + column * STEP
                + CELL_SIZE / 2,

                TOP
                + strongest_row * STEP
                + CELL_SIZE / 2
            )

        )


# ============================================================
# CYBER CIRCUIT LINE
# ============================================================

if len(points) >= 2:

    path = (
        f"M {points[0][0]:.1f} "
        f"{points[0][1]:.1f}"
    )


    for x, y in points[1:]:

        path += (
            f" L {x:.1f} "
            f"{y:.1f}"
        )


    svg.append(
        f'''
<path
    d="{path}"
    fill="none"
    stroke="#7dff8a"
    stroke-width="1"
    opacity="0.22"
    filter="url(#glow)"/>
'''
    )


# ============================================================
# FOOTER
# ============================================================

footer_y = (
    TOP
    + GRID_HEIGHT
    + 17
)


svg.append(
f'''
<text
    x="{LEFT}"
    y="{footer_y}"
    font-family="monospace"
    font-size="9"
    fill="#557087">

    STATUS: ONLINE

</text>
'''
)


# ============================================================
# LEGEND
# ============================================================

legend_colors = [

    "#0a2230",
    "#12394a",
    "#1c91a8",
    "#39d9ff",
    "#7dff8a"

]


legend_x = (
    WIDTH
    - LEFT
    - 130
)


svg.append(
f'''
<text
    x="{legend_x - 30}"
    y="{footer_y}"
    font-family="monospace"
    font-size="9"
    fill="#557087">

    LESS

</text>
'''
)


for index, color in enumerate(
    legend_colors
):

    svg.append(
        f'''
<rect
    x="{legend_x + index * 17}"
    y="{footer_y - 9}"
    width="11"
    height="11"
    rx="3"
    fill="{color}"/>
'''
    )


svg.append(
f'''
<text
    x="{WIDTH - LEFT}"
    y="{footer_y}"
    font-family="monospace"
    font-size="9"
    text-anchor="end"
    fill="#7dff8a">

    MORE

</text>

</svg>
'''
)


# ============================================================
# WRITE SVG
# ============================================================

output_directory = Path("dist")

output_directory.mkdir(
    exist_ok=True
)


output_file = (
    output_directory
    / "cyber-contribution-grid.svg"
)


output_file.write_text(
    "".join(svg),
    encoding="utf-8"
)


print(
    f"Generated: {output_file}"
)

print(
    f"User: {USERNAME}"
)

print(
    f"Total contributions: {total}"
)
