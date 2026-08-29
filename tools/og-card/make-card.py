# Regenerates img/og-card.png, the 1200x630 Open Graph card referenced by
# _layouts/default.html. Run after changing the name, affiliation or palette:
#     python3 tools/og-card/make-card.py
# Not published: _config.yml excludes tools/ from the Jekyll build.

import pathlib

from PIL import Image, ImageDraw, ImageFont

HERE = pathlib.Path(__file__).resolve().parent

W, H = 1200, 630
BG      = (255, 255, 255)
TEXT    = (27, 29, 33)     # --text
MUTED   = (107, 114, 128)  # --muted
ACCENT  = (47, 102, 144)   # --accent

OTF  = "/usr/share/fonts/opentype/urw-base35/"
DEJA = "/usr/share/fonts/truetype/dejavu/"
f_name = ImageFont.truetype(OTF + "P052-Bold.otf", 78)
f_sub  = ImageFont.truetype(DEJA + "DejaVuSans.ttf", 26)
f_res  = ImageFont.truetype(DEJA + "DejaVuSans.ttf", 24)

# ---- lens: elliptical alpha mask, supersampled for clean edges -------------
lens = Image.open(str(HERE / "lens.png")).convert("RGB")
cx, cy, rx, ry = 625, 626, 589 + 4, 604 + 4
S = 4
m = Image.new("L", (lens.width * S, lens.height * S), 0)
ImageDraw.Draw(m).ellipse(
    [(cx - rx) * S, (cy - ry) * S, (cx + rx) * S, (cy + ry) * S], fill=255)
lens.putalpha(m.resize(lens.size, Image.LANCZOS))
lens = lens.crop((cx - rx, cy - ry, cx + rx, cy + ry))

D = 430
lens = lens.resize((D, int(D * lens.height / lens.width)), Image.LANCZOS)

card = Image.new("RGB", (W, H), BG)
lx, ly = 74, (H - lens.height) // 2
card.paste(lens, (lx, ly), lens)

d = ImageDraw.Draw(card)
X    = lx + D + 66
AVAIL = W - X - 66

def wrap(text, font):
    # an explicit "|" forces a break, so the two lines stay balanced
    if "|" in text:
        return [seg.strip() for seg in text.split("|")]
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= AVAIL:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

sub_lines = wrap("CAU Kiel · Marie Skłodowska-Curie Fellow", f_sub)
res_lines = wrap("Robust geometric estimation | for computer vision", f_res)

# ---- measure the whole block so it sits optically centred -----------------
NAME_H, RULE_GAP, RULE_H, SUB_GAP = 84, 30, 4, 30
LINE_SUB, LINE_RES, RES_GAP = 36, 34, 24
block = (NAME_H + RULE_GAP + RULE_H + SUB_GAP
         + len(sub_lines) * LINE_SUB + RES_GAP + len(res_lines) * LINE_RES)
y = (H - block) // 2

d.text((X, y), "James Pritts", font=f_name, fill=TEXT)
y += NAME_H + RULE_GAP
d.rectangle([X, y, X + 68, y + RULE_H], fill=ACCENT)
y += RULE_H + SUB_GAP
for ln in sub_lines:
    d.text((X, y), ln, font=f_sub, fill=MUTED); y += LINE_SUB
y += RES_GAP
for ln in res_lines:
    d.text((X, y), ln, font=f_res, fill=ACCENT); y += LINE_RES

card.save(str(HERE.parents[1] / "img" / "og-card.png"),
          optimize=True)
print("wrote img/og-card.png", card.size)
