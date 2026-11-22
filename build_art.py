#!/usr/bin/env python3
"""Paint the Twenty-Two front page.

Run locally (never by the grader) to produce entry.png: a broadsheet
front page summing up Sunday 22 November 2026. All drawing is done
with PIL and the DejaVu fonts on this machine; no network, no photos,
no invented quotes -- every story is paraphrased from the 22 November
2026 news cycle and sourced in README.md.

Usage:
    python3 build_art.py            # writes entry.png next to this file
"""

import hashlib
import os
import sys

from PIL import Image, ImageDraw, ImageFont

PAGE = 1024
MARGIN = 40
PAPER = (247, 242, 231)
INK = (18, 18, 18)
BODY_GREY = (64, 64, 64)
RED = (163, 22, 33)
NAVY = (27, 42, 74)
FAINT = (150, 142, 128)

FONTS = "/usr/share/fonts/truetype/dejavu"
SERIF = os.path.join(FONTS, "DejaVuSerif.ttf")
SERIF_BOLD = os.path.join(FONTS, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FONTS, "DejaVuSans.ttf")
SANS_BOLD = os.path.join(FONTS, "DejaVuSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, face, width):
    """Greedy word wrap: split `text` into lines fitting `width` px."""
    lines = []
    line = ""
    for word in text.split():
        trial = (line + " " + word).strip()
        if not line or draw.textlength(trial, font=face) <= width:
            line = trial
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def block(draw, x, y, text, face, colour, width, leading):
    """Draw wrapped text starting at (x, y); return y below the block."""
    for line in wrap(draw, text, face, width):
        draw.text((x, y), line, font=face, fill=colour)
        y += leading
    return y


def centre(draw, y, text, face, colour):
    """Draw one centred line; return its width."""
    width = draw.textlength(text, font=face)
    draw.text(((PAGE - width) / 2, y), text, font=face, fill=colour)
    return width


def double_rule(draw, y, x0=MARGIN, x1=PAGE - MARGIN):
    draw.line([(x0, y), (x1, y)], fill=INK, width=3)
    draw.line([(x0, y + 5), (x1, y + 5)], fill=INK, width=1)


def item(draw, x, y, width, kicker, headline, body,
         head_size, head_lead, body_size, body_lead, kick_size=17):
    """One story: red kicker, bold headline, grey body. Return bottom y."""
    draw.text((x, y), kicker, font=font(SANS_BOLD, kick_size), fill=RED)
    y += kick_size + 8
    y = block(draw, x, y, headline, font(SERIF_BOLD, head_size),
              INK, width, head_lead)
    y += 6
    y = block(draw, x, y, body, font(SERIF, body_size),
              BODY_GREY, width, body_lead)
    return y


# ------------------------------------------------------------------ content
LEAD = (
    "LEAD STORY  \u2022  THE GULF",
    "Iran hits US bases in Bahrain as the Gulf war widens",
    "Iran fired drones and missiles at US bases in Bahrain on Saturday "
    "night, its fourth attack there in nine days, and hit tankers in the "
    "Strait of Hormuz. Bahrain said its defences intercepted them.",
)

FOUR = [
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

NUMBERS = [
    ("4", "Iran attacks on Bahrain"),
    ("11", "killed after cartel capture"),
    ("6.9", "Peru quake magnitude"),
    ("-14%", "Nvidia's fall since Huang quit"),
    ("$1tn", "China trade surplus, 10 mo"),
]

IN_BRIEF = [
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


# ------------------------------------------------------------------ sections
def draw_masthead(draw):
    centre(draw, 14, "TWENTY-TWO", font(SERIF_BOLD, 88), INK)
    double_rule(draw, 118)
    centre(draw, 134, "SUNDAY  \u2022  22  NOVEMBER  2026",
           font(SANS_BOLD, 27), RED)
    centre(draw, 168, "THE WORLD IN ONE PAGE \u2014 ELEVEN STORIES THAT "
           "DEFINED THE DAY", font(SANS, 18), BODY_GREY)
    double_rule(draw, 194)


def draw_lead(draw):
    kicker, headline, body = LEAD
    bottom = item(draw, MARGIN, 210, PAGE - 2 * MARGIN, kicker, headline,
                  body, head_size=40, head_lead=45, body_size=19,
                  body_lead=25, kick_size=18)
    return bottom + 18


def draw_four(draw, top):
    col = (PAGE - 2 * MARGIN - 36) // 2
    left = MARGIN
    right = MARGIN + col + 36
    y = top
    low_l = item(draw, left, y, col, *FOUR[0],
                 head_size=29, head_lead=33, body_size=15, body_lead=20)
    low_r = item(draw, right, y, col, *FOUR[1],
                 head_size=29, head_lead=33, body_size=15, body_lead=20)
    y = max(low_l, low_r) + 10
    draw.line([(MARGIN, y), (PAGE - MARGIN, y)], fill=FAINT, width=1)
    y += 10
    low_l = item(draw, left, y, col, *FOUR[2],
                 head_size=29, head_lead=33, body_size=15, body_lead=20)
    low_r = item(draw, right, y, col, *FOUR[3],
                 head_size=29, head_lead=33, body_size=15, body_lead=20)
    return max(low_l, low_r)


def draw_numbers(draw, top):
    height = 60
    draw.rectangle([(MARGIN, top), (PAGE - MARGIN, top + height)], fill=INK)
    cell = (PAGE - 2 * MARGIN) // len(NUMBERS)
    for i, (number, label) in enumerate(NUMBERS):
        cx = MARGIN + i * cell
        num_face = font(SANS_BOLD, 24)
        w = draw.textlength(number, font=num_face)
        draw.text((cx + (cell - w) / 2, top + 8), number, font=num_face,
                  fill=(255, 255, 255))
        lab_face = font(SANS, 11)
        w = draw.textlength(label, font=lab_face)
        draw.text((cx + (cell - w) / 2, top + 38), label, font=lab_face,
                  fill=(200, 200, 200))
        if i:
            draw.line([(cx, top + 12), (cx, top + height - 12)],
                      fill=(90, 90, 90), width=1)
    return top + height


def draw_briefs(draw, top):
    draw.text((MARGIN, top), "THE DAY IN BRIEF",
              font=font(SANS_BOLD, 19), fill=INK)
    draw.line([(MARGIN, top + 28), (PAGE - MARGIN, top + 28)],
              fill=INK, width=2)
    col = (PAGE - 2 * MARGIN - 36) // 2
    left = MARGIN
    right = MARGIN + col + 36
    y_left = y_right = top + 38
    for i, (place, text) in enumerate(IN_BRIEF):
        if i % 2 == 0:
            x, y = left, y_left
        else:
            x, y = right, y_right
        draw.text((x, y), "\u2022", font=font(SANS_BOLD, 15), fill=RED)
        new_y = block(draw, x + 16, y, place + ": " + text,
                      font(SERIF, 14), BODY_GREY, col - 16, 18)
        if i % 2 == 0:
            y_left = new_y + 6
        else:
            y_right = new_y + 6
    return max(y_left, y_right)


def draw_footer(draw, y):
    draw.text((MARGIN, y),
              "All stories as reported on 22 November 2026. "
              "Drawn with PIL; no photos, no invented quotes.",
              font=font(SANS, 13), fill=FAINT)


def paint():
    sheet = Image.new("RGB", (PAGE, PAGE), PAPER)
    draw = ImageDraw.Draw(sheet)
    draw_masthead(draw)
    after_lead = draw_lead(draw)
    after_four = draw_four(draw, after_lead)
    after_numbers = draw_numbers(draw, after_four + 14)
    draw_briefs(draw, after_numbers + 16)
    draw_footer(draw, PAGE - 20)
    return sheet


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    target = os.path.join(here, "entry.png")
    paint().save(target, "PNG", optimize=True)
    raw = open(target, "rb").read()
    size = len(raw)
    digest = hashlib.sha256(raw).hexdigest()
    print("painted %s (%d bytes, sha256 %s)" % (target, size, digest))
    if size > 1024 * 1024:
        print("ERROR: entry.png exceeds 1 MiB", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
