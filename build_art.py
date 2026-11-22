#!/usr/bin/env python3
"""Draw the Twenty-Two front page for 22 November 2026.

Local painter only -- never run by the grader. It renders entry.png
with PIL and this machine's DejaVu fonts: a broadsheet front page
summing up Sunday 22 November 2026. No network, no photos, no made-up
quotes; every story is paraphrased from the day's news cycle and
sourced in README.md.

    python3 build_art.py     # writes entry.png beside this file
"""

import hashlib
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W = 1024
PAD = 40
BG = (247, 242, 231)
INK = (18, 18, 18)
GREY = (64, 64, 64)
RED = (163, 22, 33)
FAINT = (150, 142, 128)
WHITE = (255, 255, 255)
SOFT = (200, 200, 200)
SEAM = (90, 90, 90)

FONTDIR = "/usr/share/fonts/truetype/dejavu"
SERIF = os.path.join(FONTDIR, "DejaVuSerif.ttf")
SERIFB = os.path.join(FONTDIR, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FONTDIR, "DejaVuSans.ttf")
SANSB = os.path.join(FONTDIR, "DejaVuSans-Bold.ttf")


def face(path, px):
    return ImageFont.truetype(path, px)


def wrap_text(canvas, text, font, limit):
    """Split text into lines no wider than `limit` pixels."""
    lines, cur = [], ""
    for word in text.split():
        nxt = f"{cur} {word}".strip()
        if not cur or canvas.textlength(nxt, font=font) <= limit:
            cur = nxt
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_para(canvas, x, y, text, font, color, limit, leading):
    """Paint a wrapped paragraph; hand back the y below it."""
    for ln in wrap_text(canvas, text, font, limit):
        canvas.text((x, y), ln, font=font, fill=color)
        y += leading
    return y


def draw_centered(canvas, y, text, font, color):
    w = canvas.textlength(text, font=font)
    canvas.text(((W - w) / 2, y), text, font=font, fill=color)


def double_rule(canvas, y):
    canvas.line([PAD, y, W - PAD, y], fill=INK, width=3)
    canvas.line([PAD, y + 5, W - PAD, y + 5], fill=INK, width=1)


def story_block(canvas, x, y, width, tag, head, body,
                head_px, head_lead, body_px, body_lead, tag_px=17):
    """Kicker in red, bold headline, grey body. Returns the bottom y."""
    canvas.text((x, y), tag, font=face(SANSB, tag_px), fill=RED)
    y += tag_px + 8
    y = draw_para(canvas, x, y, head, face(SERIFB, head_px),
                  INK, width, head_lead)
    y += 6
    y = draw_para(canvas, x, y, body, face(SERIF, body_px),
                  GREY, width, body_lead)
    return y


# ---------------------------------------------------------------- stories
LEAD = (
    "LEAD STORY  \u2022  THE GULF",
    "Iran hits US bases in Bahrain as the Gulf war widens",
    "Iran fired drones and missiles at US bases in Bahrain on Saturday "
    "night, its fourth attack there in nine days, and hit tankers in the "
    "Strait of Hormuz. Bahrain said its defences intercepted them.",
)

GRID = [
    (
        "SINALOA, MEXICO",
        "Mexico captures \u2018El Chapo Isidro\u2019",
        "Mexican special forces captured FBI most-wanted cartel boss "
        "Fausto Isidro Meza Flores in a Sinaloa raid. Eleven people were "
        "killed in the violence that followed.",
    ),
    (
        "ANTALYA",
        "COP31 deadlocked over fossil fuels",
        "The COP31 climate summit opened in Antalya, but the talks stalled "
        "as countries fought over fossil fuels, leaving the negotiations "
        "in deadlock.",
    ),
    (
        "NEW YORK",
        "Nvidia after Huang: down 14%, no way back",
        "Nvidia fell about 14% after founder Jensen Huang resigned amid "
        "affair and spy-link claims. Colette Kress is interim chief; the "
        "board ruled out his return.",
    ),
    (
        "LIMA",
        "Magnitude 6.9 quake shakes Peru\u2019s Andes",
        "A magnitude 6.9 earthquake shook Peru\u2019s Andes, with tremors "
        "felt in Lima. No damage or casualties were immediately reported.",
    ),
]

STATS = [
    ("4", "Iran attacks on Bahrain"),
    ("11", "killed after cartel capture"),
    ("6.9", "Peru quake magnitude"),
    ("-14%", "Nvidia's fall since Huang quit"),
    ("$1tn", "China trade surplus, 10 mo"),
]

BRIEFS = [
    ("TOKYO", "Japan and India agree deeper military ties, with Japanese "
              "live-fire training on Indian ranges."),
    ("BALTIC SEA", "A Russian cargo ship is hit by drones; Finland "
                   "tightens security."),
    ("TALLINN", "Estonia to close its border with Russia; Moscow decries "
                "a \u201cnew Iron Curtain\u201d."),
    ("MOSCOW", "US envoys Witkoff and Kushner meet Putin after the Abu "
               "Dhabi talks end without a breakthrough."),
    ("JERUSALEM", "Eisenkot invites Netanyahu\u2019s Likud to coalition "
                  "talks."),
    ("LONDON", "TikTok launches a global deepfake-detection tool for "
               "public figures."),
]


# ---------------------------------------------------------------- sections
def header(canvas):
    draw_centered(canvas, 14, "TWENTY-TWO", face(SERIFB, 88), INK)
    double_rule(canvas, 118)
    draw_centered(canvas, 134, "SUNDAY  \u2022  22  NOVEMBER  2026",
                  face(SANSB, 27), RED)
    draw_centered(canvas, 168, "THE WORLD IN ONE PAGE \u2014 ELEVEN STORIES "
                  "THAT DEFINED THE DAY", face(SANS, 18), GREY)
    double_rule(canvas, 194)


def lead_story(canvas):
    tag, head, body = LEAD
    end = story_block(canvas, PAD, 210, W - 2 * PAD, tag, head, body,
                      head_px=40, head_lead=45, body_px=19, body_lead=25,
                      tag_px=18)
    return end + 18


def story_grid(canvas, top):
    col_w = (W - 2 * PAD - 36) // 2
    x_left, x_right = PAD, PAD + col_w + 36
    end_l = story_block(canvas, x_left, top, col_w, *GRID[0],
                        head_px=29, head_lead=33, body_px=15, body_lead=20)
    end_r = story_block(canvas, x_right, top, col_w, *GRID[1],
                        head_px=29, head_lead=33, body_px=15, body_lead=20)
    y = max(end_l, end_r) + 10
    canvas.line([PAD, y, W - PAD, y], fill=FAINT, width=1)
    y += 10
    end_l = story_block(canvas, x_left, y, col_w, *GRID[2],
                        head_px=29, head_lead=33, body_px=15, body_lead=20)
    end_r = story_block(canvas, x_right, y, col_w, *GRID[3],
                        head_px=29, head_lead=33, body_px=15, body_lead=20)
    return max(end_l, end_r)


def stat_band(canvas, top):
    band_h = 60
    canvas.rectangle([PAD, top, W - PAD, top + band_h], fill=INK)
    cell_w = (W - 2 * PAD) // len(STATS)
    for idx, (num, cap) in enumerate(STATS):
        cx = PAD + idx * cell_w
        num_font = face(SANSB, 24)
        num_w = canvas.textlength(num, font=num_font)
        canvas.text((cx + (cell_w - num_w) / 2, top + 8), num,
                    font=num_font, fill=WHITE)
        cap_font = face(SANS, 11)
        cap_w = canvas.textlength(cap, font=cap_font)
        canvas.text((cx + (cell_w - cap_w) / 2, top + 38), cap,
                    font=cap_font, fill=SOFT)
        if idx:
            canvas.line([cx, top + 12, cx, top + band_h - 12],
                        fill=SEAM, width=1)
    return top + band_h


def brief_list(canvas, top):
    canvas.text((PAD, top), "THE DAY IN BRIEF",
                font=face(SANSB, 19), fill=INK)
    canvas.line([PAD, top + 28, W - PAD, top + 28], fill=INK, width=2)
    col_w = (W - 2 * PAD - 36) // 2
    x_left, x_right = PAD, PAD + col_w + 36
    y_left = y_right = top + 38
    for idx, (place, text) in enumerate(BRIEFS):
        if idx % 2 == 0:
            x, y = x_left, y_left
        else:
            x, y = x_right, y_right
        canvas.text((x, y), "\u2022", font=face(SANSB, 15), fill=RED)
        after = draw_para(canvas, x + 16, y, f"{place}: {text}",
                          face(SERIF, 14), GREY, col_w - 16, 18)
        if idx % 2 == 0:
            y_left = after + 6
        else:
            y_right = after + 6
    return max(y_left, y_right)


def colophon(canvas, y):
    canvas.text((PAD, y),
                "All stories as reported on 22 November 2026. "
                "Drawn with PIL; no photos, no invented quotes.",
                font=face(SANS, 13), fill=FAINT)


def render():
    sheet = Image.new("RGB", (W, W), BG)
    canvas = ImageDraw.Draw(sheet)
    header(canvas)
    y = lead_story(canvas)
    y = story_grid(canvas, y)
    y = stat_band(canvas, y + 14)
    brief_list(canvas, y + 16)
    colophon(canvas, W - 20)
    return sheet


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "entry.png")
    render().save(out, "PNG", optimize=True)
    blob = open(out, "rb").read()
    print("painted %s (%d bytes, sha256 %s)"
          % (out, len(blob), hashlib.sha256(blob).hexdigest()))
    if len(blob) > 1024 * 1024:
        print("ERROR: entry.png exceeds 1 MiB", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
