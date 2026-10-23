#!/usr/bin/env python3
"""Render a neutral AD topology and the SENGOAD lab-family overview.

Editable source for docs/img/diagram-SENGOAD-full.png and the legacy
diagram-GOADv3-full.png paths used by the README and MkDocs. Regenerate with:
    pip install pillow            # needs a CJK font (Noto Sans CJK JP)
    python3 docs/img/diagram-SENGOAD-full.py
Set SENGOAD_FONT_DIR when the Noto Sans CJK files are installed elsewhere.
Set SENGOAD_AD_ONLY=1 to render only the neutral detailed topology.
Names follow docs/SENGOAD_mapping_EN.md and ad/SENGOAD/data/inventory.
"""
import math
import os
import subprocess
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 2012, 1300
SS = 2  # supersample for crisp output
img = Image.new("RGB", (W * SS, H * SS), "white")
d = ImageDraw.Draw(img)

FONT_DIR = os.environ.get("SENGOAD_FONT_DIR", "/usr/share/fonts/opentype/noto")
NOTO = os.path.join(FONT_DIR, "NotoSansCJK-Regular.ttc")
NOTOB = os.path.join(FONT_DIR, "NotoSansCJK-Bold.ttc")
AD_ONLY = os.environ.get("SENGOAD_AD_ONLY") == "1"
_fc = {}
def F(size, bold=False):
    key = (size, bold)
    if key not in _fc:
        _fc[key] = ImageFont.truetype(NOTOB if bold else NOTO, size * SS)
    return _fc[key]

def S(v):  # scale a coord/length
    return v * SS

# ---- colors ----
RED = (200, 35, 35)
BLUE = (45, 110, 190)
BLACK = (25, 25, 25)
GREEN = (40, 155, 80)
PURPLE = (135, 60, 185)
ORANGE = (228, 150, 40)
GREY = (90, 95, 105)
SRV = (150, 160, 172)
DISK = (55, 120, 205)
TRI = (35, 35, 35)
MINI = (55, 180, 75)
LIGHT = (124, 80, 222)
FULL = (50, 92, 222)
YAMATO_FOREST = (62, 91, 158)
YAMATO_FOREST_FILL = (248, 250, 255)
AKI_FOREST = (170, 104, 43)
AKI_FOREST_FILL = (255, 251, 244)

def text(x, y, s, font, fill=BLACK, anchor="mm"):
    d.text((S(x), S(y)), s, font=font, fill=fill, anchor=anchor)

def line(p1, p2, fill, w=2):
    d.line([S(p1[0]), S(p1[1]), S(p2[0]), S(p2[1])], fill=fill, width=int(w * SS))

def dashed_polyline(pts, fill, w=2, dash=12, gap=8):
    """Draw dashes along a polyline given as list of (x,y)."""
    seglen = dash + gap
    carry = 0.0
    for i in range(len(pts) - 1):
        x1, y1 = pts[i]; x2, y2 = pts[i + 1]
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy)
        if L == 0:
            continue
        ux, uy = dx / L, dy / L
        pos = -carry
        while pos < L:
            a = max(pos, 0.0)
            b = min(pos + dash, L)
            if b > a:
                line((x1 + ux * a, y1 + uy * a), (x1 + ux * b, y1 + uy * b), fill, w)
            pos += seglen
        carry = (carry + L) % seglen

def rrect_path(x0, y0, x1, y1, r, step=10):
    """Sample a rounded-rect perimeter into points (for dashed stroking)."""
    pts = []
    corners = [
        (x1 - r, y0 + r, 270, 360),  # top-right
        (x1 - r, y1 - r, 0, 90),     # bottom-right
        (x0 + r, y1 - r, 90, 180),   # bottom-left
        (x0 + r, y0 + r, 180, 270),  # top-left
    ]
    # build: start top edge, go clockwise
    pts.append((x0 + r, y0))
    pts.append((x1 - r, y0))
    for (cx, cy, a0, a1) in corners:
        n = max(2, int((a1 - a0) / 6))
        for k in range(n + 1):
            ang = math.radians(a0 + (a1 - a0) * k / n)
            pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
        if (cx, cy) == corners[0][:2]:
            pts.append((x1, y1 - r))
        elif (cx, cy) == corners[1][:2]:
            pts.append((x0 + r, y1))
        elif (cx, cy) == corners[2][:2]:
            pts.append((x0, y0 + r))
    pts.append((x0 + r, y0))
    return pts

def dashed_rrect(x0, y0, x1, y1, fill, w=3, r=28, dash=16, gap=12):
    dashed_polyline(rrect_path(x0, y0, x1, y1, r), fill, w, dash, gap)

def arrowhead(p_from, p_to, fill, size=13):
    x1, y1 = p_from; x2, y2 = p_to
    ang = math.atan2(y2 - y1, x2 - x1)
    for s in (1, -1):
        a = ang + s * math.radians(26)
        d.line([S(x2), S(y2), S(x2 - size * math.cos(a)), S(y2 - size * math.sin(a))],
               fill=fill, width=int(2.4 * SS))

def shorten(p1, p2, r1=0, r2=0):
    x1, y1 = p1; x2, y2 = p2
    L = math.hypot(x2 - x1, y2 - y1) or 1
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    return (x1 + ux * r1, y1 + uy * r1), (x2 - ux * r2, y2 - uy * r2)

def arrow(p1, p2, fill, w=2, label=None, dashed=False, bidir=False,
          r1=20, r2=24, lf=None, loff=(0, -10), lcolor=None):
    a, b = shorten(p1, p2, r1, r2)
    if dashed:
        dashed_polyline([a, b], fill, w, 13, 9)
    else:
        line(a, b, fill, w)
    arrowhead(a, b, fill)
    if bidir:
        arrowhead(b, a, fill)
    if label:
        mx, my = (a[0] + b[0]) / 2 + loff[0], (a[1] + b[1]) / 2 + loff[1]
        text(mx, my, label, lf or F(13), lcolor or fill)

# ---------- icons ----------
def server(cx, cy):
    """Tower server icon ~ 54x66."""
    wbox, hbox = 52, 64
    x0, y0 = cx - wbox / 2, cy - hbox / 2
    x1, y1 = cx + wbox / 2, cy + hbox / 2
    d.rounded_rectangle([S(x0), S(y0), S(x1), S(y1)], radius=S(6),
                        fill=SRV, outline=GREY, width=int(2 * SS))
    for k in range(3):
        yy = y0 + 10 + k * 9
        line((x0 + 8, yy), (x1 - 14, yy), GREY, 1.5)
        d.ellipse([S(x1 - 12), S(yy - 2), S(x1 - 8), S(yy + 2)], fill=(70, 90, 110))
    # disk badge bottom-right
    bx, by = x1 - 4, y1 - 4
    d.ellipse([S(bx - 13), S(by - 13), S(bx + 5), S(by + 5)], fill=DISK, outline="white", width=int(1.5 * SS))
    d.ellipse([S(bx - 6), S(by - 6), S(bx - 2), S(by - 2)], fill="white")

def server_adcs(cx, cy):
    server(cx, cy)
    # small certificate badge top-right
    bx, by = cx + 24, cy - 30
    d.rounded_rectangle([S(bx - 12), S(by - 9), S(bx + 12), S(by + 9)], radius=S(2),
                        fill="white", outline=(70, 70, 70), width=int(1.5 * SS))
    for k in range(3):
        line((bx - 8, by - 4 + k * 4), (bx + 4, by - 4 + k * 4), (90, 90, 90), 1)
    d.ellipse([S(bx + 2), S(by - 2), S(bx + 10), S(by + 6)], fill=(225, 180, 40), outline=(150, 110, 10), width=int(1*SS))

def user(cx, cy, color=(45, 45, 45), bot=False):
    """Single person outline icon."""
    rh = 9
    d.ellipse([S(cx - rh), S(cy - 20), S(cx + rh), S(cy - 20 + 2 * rh)], outline=color, width=int(2.2 * SS))
    d.arc([S(cx - 16), S(cy - 4), S(cx + 16), S(cy + 30)], 180, 360, fill=color, width=int(2.2 * SS))
    if bot:
        d.ellipse([S(cx + 6), S(cy - 22), S(cx + 20), S(cy - 8)], fill=(70, 150, 210), outline="white", width=int(1.5*SS))
        line((cx + 13, cy - 18), (cx + 13, cy - 15), "white", 1.4)
        line((cx + 13, cy - 15), (cx + 16, cy - 15), "white", 1.4)

def group(cx, cy, color=(70, 80, 95)):
    """Two filled people."""
    for off in (-9, 9):
        d.ellipse([S(cx + off - 8), S(cy - 18), S(cx + off + 8), S(cy - 2)], fill=color)
        d.pieslice([S(cx + off - 14), S(cy - 2), S(cx + off + 14), S(cy + 26)], 180, 360, fill=color)

# ---------- multi-line label block ----------
def block(cx, y, lines, gap=4):
    """lines: list of (text, size, bold, color). Centered on cx, top at y."""
    yy = y
    for (s, sz, bold, col) in lines:
        f = F(sz, bold)
        text(cx, yy + sz / 2, s, f, col, anchor="mm")
        yy += sz + gap
    return yy

# ===================================================================
# SCOPE / FOREST BOXES (draw first, behind)
# ===================================================================
if not AD_ONLY:
    dashed_rrect(28, 64, 1984, 1248, FULL, w=3, r=34, dash=18, gap=13)
    text(1006, 1226, "SENGOAD", F(30, True), FULL, anchor="mm")

    dashed_rrect(70, 92, 1335, 1208, LIGHT, w=3, r=30, dash=16, gap=12)
    text(440, 1196, "SENGOAD-Light", F(24, True), LIGHT, anchor="mm")

    dashed_rrect(560, 118, 1132, 560, MINI, w=3, r=26, dash=14, gap=11)
    text(795, 540, "SENGOAD-Mini", F(24, True), MINI, anchor="mm")
else:
    d.rounded_rectangle(
        [S(28), S(64), S(1318), S(1248)],
        radius=S(30), fill=YAMATO_FOREST_FILL, outline=YAMATO_FOREST,
        width=int(3 * SS),
    )
    d.rounded_rectangle(
        [S(1338), S(64), S(1984), S(1248)],
        radius=S(30), fill=AKI_FOREST_FILL, outline=AKI_FOREST,
        width=int(3 * SS),
    )
    text(673, 90, "Yamato forest  ·  2 domains", F(20, True), YAMATO_FOREST)
    text(1661, 90, "Aki forest  ·  1 domain", F(20, True), AKI_FOREST)

YAMATO_APEX_Y = 130 if AD_ONLY else 60
AKI_DX = 150 if AD_ONLY else 0

# ===================================================================
# DOMAIN TRIANGLES
# ===================================================================
def triangle(apex, bl, br, w=2):
    d.line([S(apex[0]), S(apex[1]), S(bl[0]), S(bl[1])], fill=TRI, width=int(w*SS))
    d.line([S(br[0]), S(br[1]), S(apex[0]), S(apex[1])], fill=TRI, width=int(w*SS))
    d.line([S(bl[0]), S(bl[1]), S(br[0]), S(br[1])], fill=TRI, width=int(w*SS))

# Yamato (center, tall)
triangle((1006, YAMATO_APEX_Y), (720, 770), (1300, 770))
text(1010, 792, "yamato.local", F(21, True), BLACK, anchor="mm")
text(1010, 814, "大和  ·  YAMATO", F(17, False), (80,80,80), anchor="mm")
# Kai (left)
triangle((565, 705), (300, 1120), (830, 1120))
text(565, 1138, "kai.yamato.local", F(20, True), BLACK, anchor="mm")
text(565, 1159, "甲斐  ·  KAI", F(16, False), (80,80,80), anchor="mm")
# Aki (right)
triangle((1450 + AKI_DX, 705), (1235 + AKI_DX, 1120), (1665 + AKI_DX, 1120))
text(1450 + AKI_DX, 1138, "aki.local", F(20, True), BLACK, anchor="mm")
text(1450 + AKI_DX, 1159, "安芸  ·  AKI", F(16, False), (80,80,80), anchor="mm")

# ===================================================================
# VMs
# ===================================================================
# DC01 osaka
P_OSAKA = (1006, 360)
server_adcs(*P_OSAKA)
block(1006, 396, [
    ("DC01 — osaka  (大坂)", 18, True, BLACK),
    ("192.168.56.10", 15, False, (60,60,60)),
    ("Windows Server 2019", 15, False, (60,60,60)),
    ("ADCS — YAMATO-CA", 14, True, (150,90,10)),
])

# DC02 kofu
P_KOFU = (575, 830)
server(*P_KOFU)
block(575, 866, [
    ("DC02 — kofu  (甲府)", 17, True, BLACK),
    ("192.168.56.11", 14, False, (60,60,60)),
    ("Windows Server 2019", 14, False, (60,60,60)),
    ("rpc user enum", 13, False, (120,60,60)),
])

# SRV02 shirakawa
P_SHIRA = (575, 1000)
server(*P_SHIRA)
block(575, 1036, [
    ("SRV02 — shirakawa  (白河)", 16, True, BLACK),
    ("192.168.56.22 · Win Server 2019 · no defender", 13, False, (60,60,60)),
    ("IIS + upload ASP", 13, False, (60,60,60)),
    ("MSSQL + execute as + trusted link", 13, False, (60,60,60)),
])

# DC03 hiroshima  (custom templates live on the AKI-CA at sakai; hiroshima is not a CA)
P_HIRO = (1450 + AKI_DX, 830)
server(*P_HIRO)
block(P_HIRO[0], 866, [
    ("DC03 — hiroshima  (広島)", 17, True, BLACK),
    ("192.168.56.12 · Windows Server 2016", 14, False, (60,60,60)),
    ("ntlm downgrade · LAPS", 13, False, (120,60,60)),
    ("ADCS custom templates", 13, False, (150,90,10)),
])

# SRV03 sakai
P_SAKAI = (1450 + AKI_DX, 1000)
server_adcs(*P_SAKAI)
block(P_SAKAI[0], 1036, [
    ("SRV03 — sakai  (堺)", 16, True, BLACK),
    ("192.168.56.23 · Win Server 2016 · LAPS", 13, False, (60,60,60)),
    ("ADCS — AKI-CA", 13, True, (150,90,10)),
    ("MSSQL + execute as + trusted link", 13, False, (60,60,60)),
])

# ===================================================================
# TRUSTS + MSSQL link
# ===================================================================
parent_trust_label = "parent-child trust" if AD_ONLY else "trust"
forest_trust_label = "forest trust" if AD_ONLY else "trust"
forest_trust_target = (1530, 760) if AD_ONLY else (1380, 760)
arrow((830, 740), (640, 760), BLACK, 2, label=parent_trust_label,
      bidir=True, r1=4, r2=4, loff=(6,-12), lf=F(14))
arrow((1180, 740), forest_trust_target, BLACK, 2, label=forest_trust_label,
      bidir=True, r1=4, r2=4, loff=(-6,-12), lf=F(14))
# mssql trusted link between the two servers
a, b = shorten(P_SHIRA, P_SAKAI, 32, 32)
line(a, b, BLACK, 2)
arrowhead(a, b, BLACK); arrowhead(b, a, BLACK)
mssql_label_x = 1088 if AD_ONLY else 1012
text(mssql_label_x, 982, "MSSQL trusted link", F(14), BLACK, anchor="mm")

# ===================================================================
# USERS  (login mono-ish ASCII + kanji display)
# ===================================================================
def person(cx, cy, login, disp, roles, target, ecolor, elabel,
           bot=False, dashed=False, extra_targets=None, loff=(0, -10)):
    user(cx, cy, bot=bot)
    ly = cy + 26
    text(cx, ly, login, F(14, False), (30, 30, 30), anchor="mm")
    text(cx, ly + 17, disp, F(15, False), (95, 95, 95), anchor="mm")
    yy = ly + 35
    for (rt, rc) in roles:
        text(cx, yy, rt, F(12, True), rc, anchor="mm")
        yy += 15
    if target:
        arrow((cx, cy), target, ecolor, 2, label=elabel, dashed=dashed, r1=22, r2=30, lf=F(13), loff=loff)
    for (tg, ec, el, dl) in (extra_targets or []):
        arrow((cx, cy), tg, ec, 2, label=el, dashed=dl, r1=22, r2=30, lf=F(13))

# --- Yamato users (center / mini) ---
person(852, 150, "toyotomi.hideyoshi", "豊臣秀吉", [("domain admin", RED)],
       (1006, 360), RED, "admin")
person(700, 285, "oichi", "お市の方", [("domain admin", RED)],
       (1006, 360), RED, "admin")
group(700, 400); text(700, 428, "Gotairo (五大老)", F(14), (40, 40, 40), anchor="mm")
arrow((735, 392), (1006, 360), BLUE, 2, label="RDP", r1=22, r2=30, lf=F(13))
group(700, 480); text(700, 508, "Toyotomi (豊臣)", F(14), (40, 40, 40), anchor="mm")
arrow((735, 478), (1006, 365), BLUE, 2, label="RDP", r1=22, r2=30, lf=F(13))

# --- Kai users (left) ---
person(150, 560, "sanjo", "三条の方", [], P_KOFU, RED, "admin")
person(335, 470, "takeda.shingen", "武田信玄",
       [("bot 5min (LLMNR)", (70, 120, 180)), ("domain admin", RED)],
       P_KOFU, RED, "admin", bot=True, extra_targets=[(P_SHIRA, RED, "admin", False)])
person(140, 690, "takeda.katsuyori", "武田勝頼", [("bot 3min (LLMNR)", (70, 120, 180))],
       P_SHIRA, GREEN, "RDP (active)", bot=True, dashed=not AD_ONLY)
group(250, 830); text(250, 858, "Takeda (武田)", F(14), (40, 40, 40), anchor="mm")
arrow((288, 826), P_KOFU, BLUE, 2, label="RDP", r1=22, r2=30, lf=F(13))
arrow((285, 845), P_SHIRA, BLUE, 2, label="RDP", r1=22, r2=34, lf=F(13))
group(250, 945); text(250, 973, "Yoban (夜番)", F(14), (40, 40, 40), anchor="mm")
arrow((290, 952), P_SHIRA, BLUE, 2, label="RDP", r1=22, r2=30, lf=F(13))
person(135, 1050, "honda.tadakatsu", "本多忠勝", [], P_SHIRA, RED, "admin")
person(130, 1150, "sanada.yukimura", "真田幸村", [],
       P_SHIRA, PURPLE, "mssql_admin", loff=(0, -8))

# --- Aki users (right) ---
person(1820, 560, "mori.motonari", "毛利元就", [("domain admin", RED)],
       P_HIRO, RED, "admin")
group(1880, 720); text(1880, 748, "Mori (毛利)", F(14), (40, 40, 40), anchor="mm")
arrow((1845, 716), P_HIRO, BLUE, 2, label="RDP", r1=22, r2=30, lf=F(13))
group(1880, 905); text(1880, 933, "KibaShu (騎馬衆)", F(14), (40, 40, 40), anchor="mm")
arrow((1843, 912), P_SAKAI, BLUE, 2, label="RDP", r1=22, r2=30, lf=F(13))
date_position = (1880, 980) if AD_ONLY else (1858, 1045)
person(*date_position, "date.masamune", "伊達政宗", [("admin · mssql_admin · ECS4", RED)],
       P_SAKAI, RED, "admin")
person(1665 + AKI_DX, 1150, "honda.tadatomo", "本多忠朝", [],
       P_SAKAI, ORANGE, "mapping_mssql_trust", loff=(70, 30))

# ===================================================================
# TITLE + LEGEND
# ===================================================================
title = (
    "Active Directory Environment  ·  2 forests / 3 domains"
    if AD_ONLY
    else "SENGOAD — 戦国 GOAD  ·  full lab (5 VMs)"
)
text(1006, 36, title, F(26, True), BLACK, anchor="mm")

# Legend backing keeps the key distinct from both scope and forest backgrounds.
lx, ly = 78, 132
d.rounded_rectangle([S(54), S(96), S(350), S(288)], radius=S(10),
                    fill="white", outline=(170, 170, 170), width=int(1.5 * SS))
items = [("admin", RED), ("RDP", BLUE), ("trust / MSSQL link", BLACK),
         ("LLMNR bot (active)", GREEN), ("mssql_admin", PURPLE), ("mapping_mssql_trust", ORANGE)]
text(lx, ly - 22, "Legend", F(15, True), BLACK, anchor="lm")
for i, (lab, c) in enumerate(items):
    yy = ly + i * 23
    line((lx, yy), (lx + 34, yy), c, 3)
    arrowhead((lx, yy), (lx + 34, yy), c, 9)
    text(lx + 44, yy, lab, F(13), (40,40,40), anchor="lm")

here = os.path.dirname(os.path.abspath(__file__))
out = img.resize((W, H), Image.LANCZOS)
if AD_ONLY:
    target = os.path.join(here, "diagram-SENGOAD-full.png")
    out.save(target)
    print("saved", out.size, "to", target)
    raise SystemExit

# ===================================================================
# LAB-FAMILY OVERVIEW WITH EXTENSIONS
# ===================================================================
# Keep the detailed 5-VM diagram above unchanged and add a compact extension
# strip for the README/MkDocs overview. The legacy filename remains in place so
# existing external links continue to work.
EXT_H = 310
overview = Image.new("RGB", (W * SS, (H + EXT_H) * SS), "white")
overview.paste(img, (0, S(EXT_H)))
img = overview
d = ImageDraw.Draw(img)

EXT = (238, 126, 12)

def workstation(cx, cy):
    """Simple workstation icon sized to match the server glyphs."""
    d.rounded_rectangle(
        [S(cx - 34), S(cy - 25), S(cx + 34), S(cy + 18)],
        radius=S(5), fill=(80, 145, 210), outline=GREY, width=int(2 * SS)
    )
    d.rectangle([S(cx - 27), S(cy - 18), S(cx + 27), S(cy + 10)], fill=(225, 240, 252))
    line((cx, cy + 18), (cx, cy + 30), GREY, 3)
    line((cx - 18, cy + 30), (cx + 18, cy + 30), GREY, 3)

def extension_card(cx, title, address, detail, fill, icon="server"):
    x0, x1 = cx - 215, cx + 215
    d.rounded_rectangle(
        [S(x0), S(78), S(x1), S(260)],
        radius=S(16), fill=fill, outline=EXT, width=int(1.5 * SS)
    )
    if icon == "workstation":
        workstation(cx, 132)
    else:
        server(cx, 132)
    block(cx, 176, [
        (title, 17, True, BLACK),
        (address, 14, False, (60, 60, 60)),
        (detail, 13, False, (60, 60, 60)),
    ], gap=3)

dashed_rrect(28, 28, 1984, 282, EXT, w=3, r=30, dash=18, gap=13)
text(1006, 54, "SENGOAD extensions", F(25, True), EXT, anchor="mm")
extension_card(270, "SRV01 — gifu (岐阜)", "192.168.56.21", "Exchange · Windows Server 2019", (255, 244, 214))
extension_card(760, "WS01 — azuchi (安土)", "192.168.56.31", "Windows 10 22H2", (255, 232, 208), "workstation")
extension_card(1250, "wazuh", "192.168.56.51", "Wazuh server", (232, 220, 242))
extension_card(1740, "elk", "192.168.56.50", "Elastic Stack server", (219, 234, 251))

overview_out = img.resize((W, H + EXT_H), Image.LANCZOS)
legacy_targets = [
    os.path.join(here, "diagram-GOADv3-full.png"),
    os.path.normpath(os.path.join(here, "..", "mkdocs", "docs", "img", "diagram-GOADv3-full.png")),
]
for target in legacy_targets:
    overview_out.save(target)

child_env = os.environ.copy()
child_env["SENGOAD_AD_ONLY"] = "1"
# Render the neutral topology in a second pass so the overview above keeps its
# branded scope boxes and remains backward-compatible at the legacy path.
subprocess.run([sys.executable, os.path.abspath(__file__)], check=True, env=child_env)
print("saved branded overview", overview_out.size, "and neutral topology", out.size)
