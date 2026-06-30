#!/usr/bin/env python3
"""Render the SENGOAD full network diagram (5 VMs) — a Sengoku re-skin of GOAD's
diagram-GOADv3-full.png, without the Extensions box.

Editable source for docs/img/diagram-SENGOAD-full.png. Regenerate with:
    pip install pillow            # needs a CJK font (Noto Sans CJK JP)
    python3 docs/img/diagram-SENGOAD-full.py
Names follow docs/SENGOAD_mapping_EN.md and ad/SENGOAD/data/inventory.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 2012, 1300
SS = 2  # supersample for crisp output
img = Image.new("RGB", (W * SS, H * SS), "white")
d = ImageDraw.Draw(img)

NOTO = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
NOTOB = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
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
# SCOPE BOXES (draw first, behind)
# ===================================================================
dashed_rrect(28, 64, 1984, 1248, FULL, w=3, r=34, dash=18, gap=13)
text(1006, 1226, "SENGOAD", F(30, True), FULL, anchor="mm")

dashed_rrect(70, 92, 1335, 1208, LIGHT, w=3, r=30, dash=16, gap=12)
text(440, 1196, "SENGOAD-Light", F(24, True), LIGHT, anchor="mm")

dashed_rrect(560, 118, 1132, 560, MINI, w=3, r=26, dash=14, gap=11)
text(795, 540, "SENGOAD-Mini", F(24, True), MINI, anchor="mm")

# ===================================================================
# DOMAIN TRIANGLES
# ===================================================================
def triangle(apex, bl, br, w=2):
    d.line([S(apex[0]), S(apex[1]), S(bl[0]), S(bl[1])], fill=TRI, width=int(w*SS))
    d.line([S(br[0]), S(br[1]), S(apex[0]), S(apex[1])], fill=TRI, width=int(w*SS))
    d.line([S(bl[0]), S(bl[1]), S(br[0]), S(br[1])], fill=TRI, width=int(w*SS))

# Yamato (center, tall)
triangle((1006, 60), (720, 770), (1300, 770))
text(1010, 792, "yamato.local", F(21, True), BLACK, anchor="mm")
text(1010, 814, "大和  ·  YAMATO", F(17, False), (80,80,80), anchor="mm")
# Kai (left)
triangle((565, 705), (300, 1120), (830, 1120))
text(565, 1138, "kai.yamato.local", F(20, True), BLACK, anchor="mm")
text(565, 1159, "甲斐  ·  KAI", F(16, False), (80,80,80), anchor="mm")
# Aki (right)
triangle((1450, 705), (1235, 1120), (1665, 1120))
text(1450, 1138, "aki.local", F(20, True), BLACK, anchor="mm")
text(1450, 1159, "安芸  ·  AKI", F(16, False), (80,80,80), anchor="mm")

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
P_HIRO = (1450, 830)
server(*P_HIRO)
block(1450, 866, [
    ("DC03 — hiroshima  (広島)", 17, True, BLACK),
    ("192.168.56.12 · Windows Server 2016", 14, False, (60,60,60)),
    ("ntlm downgrade · LAPS", 13, False, (120,60,60)),
    ("ADCS custom templates", 13, False, (150,90,10)),
])

# SRV03 sakai
P_SAKAI = (1450, 1000)
server_adcs(*P_SAKAI)
block(1450, 1036, [
    ("SRV03 — sakai  (堺)", 16, True, BLACK),
    ("192.168.56.23 · Win Server 2016 · LAPS", 13, False, (60,60,60)),
    ("ADCS — AKI-CA", 13, True, (150,90,10)),
    ("MSSQL + execute as + trusted link", 13, False, (60,60,60)),
])

# ===================================================================
# TRUSTS + MSSQL link
# ===================================================================
arrow((830, 740), (640, 760), BLACK, 2, label="trust", bidir=True, r1=4, r2=4, loff=(6,-12), lf=F(14))
arrow((1180, 740), (1380, 760), BLACK, 2, label="trust", bidir=True, r1=4, r2=4, loff=(-6,-12), lf=F(14))
# mssql trusted link between the two servers
a, b = shorten(P_SHIRA, P_SAKAI, 32, 32)
line(a, b, BLACK, 2)
arrowhead(a, b, BLACK); arrowhead(b, a, BLACK)
text(1012, 982, "MSSQL trusted link", F(14), BLACK, anchor="mm")

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
person(852, 150, "robert → toyotomi.hideyoshi", "豊臣秀吉", [("domain admin", RED)],
       (1006, 360), RED, "admin")
person(700, 285, "cersei → oichi", "お市の方", [("domain admin", RED)],
       (1006, 360), RED, "admin")
group(700, 400); text(700, 428, "Gotairo (五大老)", F(14), (40, 40, 40), anchor="mm")
arrow((735, 392), (1006, 360), BLUE, 2, label="RDP", r1=22, r2=30, lf=F(13))
group(700, 480); text(700, 508, "Toyotomi (豊臣)", F(14), (40, 40, 40), anchor="mm")
arrow((735, 478), (1006, 365), BLUE, 2, label="RDP", r1=22, r2=30, lf=F(13))

# --- Kai users (left) ---
person(150, 560, "catelyn → sanjo", "三条の方", [], P_KOFU, RED, "admin")
person(335, 470, "eddard → takeda.shingen", "武田信玄",
       [("bot 5min (LLMNR)", (70, 120, 180)), ("domain admin", RED)],
       P_KOFU, RED, "admin", bot=True, extra_targets=[(P_SHIRA, RED, "admin", False)])
person(140, 690, "robb → takeda.katsuyori", "武田勝頼", [("bot 3min (LLMNR)", (70, 120, 180))],
       P_SHIRA, GREEN, "RDP (active)", bot=True, dashed=True)
group(250, 830); text(250, 858, "Takeda (武田)", F(14), (40, 40, 40), anchor="mm")
arrow((288, 826), P_KOFU, BLUE, 2, label="RDP", r1=22, r2=30, lf=F(13))
arrow((285, 845), P_SHIRA, BLUE, 2, label="RDP", r1=22, r2=34, lf=F(13))
group(250, 945); text(250, 973, "Yoban (夜番)", F(14), (40, 40, 40), anchor="mm")
arrow((290, 952), P_SHIRA, BLUE, 2, label="RDP", r1=22, r2=30, lf=F(13))
person(135, 1050, "jeor → honda.tadakatsu", "本多忠勝", [], P_SHIRA, RED, "admin")
person(130, 1150, "jon.snow → sanada.yukimura", "真田幸村", [],
       P_SHIRA, PURPLE, "mssql_admin", loff=(0, -8))

# --- Aki users (right) ---
person(1820, 560, "daenerys → mori.motonari", "毛利元就", [("domain admin", RED)],
       P_HIRO, RED, "admin")
group(1880, 720); text(1880, 748, "Mori (毛利)", F(14), (40, 40, 40), anchor="mm")
arrow((1845, 716), P_HIRO, BLUE, 2, label="RDP", r1=22, r2=30, lf=F(13))
group(1880, 905); text(1880, 933, "KibaShu (騎馬衆)", F(14), (40, 40, 40), anchor="mm")
arrow((1843, 912), P_SAKAI, BLUE, 2, label="RDP", r1=22, r2=30, lf=F(13))
person(1858, 1045, "khal.drogo → date.masamune", "伊達政宗", [("admin · mssql_admin · ECS4", RED)],
       P_SAKAI, RED, "admin")
person(1665, 1150, "jorah → honda.tadatomo", "本多忠朝", [],
       P_SAKAI, ORANGE, "mapping_mssql_trust", loff=(70, 30))

# ===================================================================
# TITLE + LEGEND
# ===================================================================
text(1006, 36, "SENGOAD — 戦国 GOAD  ·  full lab (5 VMs)", F(26, True), BLACK, anchor="mm")

# legend (white backing so it sits clear of the dashed scope borders)
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

out = img.resize((W, H), Image.LANCZOS)
out.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "diagram-SENGOAD-full.png"))
print("saved", out.size)
