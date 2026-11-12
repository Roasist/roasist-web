"""Compose captured website scroll frames into a premium device-mockup loop video.

Usage: python3 compose_site_video.py <capDir> <out.mp4> <out.jpg> [accentHex]
Desktop browser window (left) + phone (right, overlapping) on a dark Roasist gradient stage.
No text is drawn on the video.
"""
import math
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

cap = Path(sys.argv[1])
out_mp4, out_jpg = sys.argv[2], sys.argv[3]
accent = sys.argv[4] if len(sys.argv) > 4 else "#7602FF"
ar, ag, ab = int(accent[1:3], 16), int(accent[3:5], 16), int(accent[5:7], 16)

W, H = 1920, 1080  # render at 1080p, encode to 1280x720
OUT_W, OUT_H = 1280, 720
d_frames = sorted(cap.glob("d_*.jpg"))
m_frames = sorted(cap.glob("m_*.jpg"))
N = min(len(d_frames), len(m_frames))
FPS = 24
FADE = 10  # loop crossfade frames back to first frame


def rounded_mask(size, r):
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), r, fill=255)
    return m


def background():
    bg = Image.new("RGB", (W, H), (9, 5, 20))
    glow = Image.new("RGB", (W, H), (0, 0, 0))
    g = ImageDraw.Draw(glow)
    g.ellipse((-300, -350, 1100, 800), fill=(ar // 2, ag // 2, ab // 2))
    g.ellipse((1100, 450, 2300, 1450), fill=(40, 30, 140))
    glow = glow.filter(ImageFilter.GaussianBlur(260))
    bg = Image.blend(bg, glow, 0.85)
    # subtle grid
    grid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grid)
    for x in range(0, W, 96):
        gd.line((x, 0, x, H), fill=(255, 255, 255, 9))
    for y in range(0, H, 96):
        gd.line((0, y, W, y), fill=(255, 255, 255, 9))
    bg = Image.alpha_composite(bg.convert("RGBA"), grid)
    return bg


BG = background()

# Desktop window geometry
DW, BAR = 1340, 44
DH_CONTENT = round(DW * 900 / 1440)
DX, DY = 196, (H - (DH_CONTENT + BAR)) // 2 - 10
# Phone geometry
PW_SCREEN = 330
PH_SCREEN = round(PW_SCREEN * 844 / 390)
BEZ = 14
PX, PY = DX + DW - 170, (H - PH_SCREEN - 2 * BEZ) // 2 + 40


def shadow(size, radius, blur, alpha):
    pad = blur * 3
    s = Image.new("RGBA", (size[0] + pad * 2, size[1] + pad * 2), (0, 0, 0, 0))
    ImageDraw.Draw(s).rounded_rectangle((pad, pad, pad + size[0], pad + size[1]), radius, fill=(0, 0, 0, alpha))
    return s.filter(ImageFilter.GaussianBlur(blur)), pad


win_shadow, wpad = shadow((DW, DH_CONTENT + BAR), 22, 40, 170)
win_glow, gpad = shadow((DW, DH_CONTENT + BAR), 22, 60, 90)
win_glow = Image.merge("RGBA", (*Image.new("RGB", win_glow.size, (ar, ag, ab)).split(), win_glow.getchannel("A")))
ph_shadow, ppad = shadow((PW_SCREEN + 2 * BEZ, PH_SCREEN + 2 * BEZ), 58, 36, 200)

# Window chrome (no text)
chrome = Image.new("RGBA", (DW, DH_CONTENT + BAR), (0, 0, 0, 0))
cd = ImageDraw.Draw(chrome)
cd.rounded_rectangle((0, 0, DW - 1, DH_CONTENT + BAR - 1), 22, fill=(22, 16, 40, 255))
for i, col in enumerate([(255, 95, 87), (254, 188, 46), (40, 200, 64)]):
    cx = 30 + i * 26
    cd.ellipse((cx - 7, BAR // 2 - 7, cx + 7, BAR // 2 + 7), fill=col + (255,))
cd.rounded_rectangle((DW // 2 - 220, 11, DW // 2 + 220, BAR - 11), 11, fill=(255, 255, 255, 18))
win_mask = rounded_mask((DW, DH_CONTENT + BAR), 22)
content_mask = Image.new("L", (DW, DH_CONTENT), 255)
cmd = ImageDraw.Draw(content_mask)
# round only bottom corners
cm2 = rounded_mask((DW, DH_CONTENT + 44), 22).crop((0, 44, DW, DH_CONTENT + 44))
content_mask = cm2

phone_body = Image.new("RGBA", (PW_SCREEN + 2 * BEZ, PH_SCREEN + 2 * BEZ), (0, 0, 0, 0))
pd = ImageDraw.Draw(phone_body)
pd.rounded_rectangle((0, 0, phone_body.width - 1, phone_body.height - 1), 58, fill=(14, 10, 26, 255), outline=(ar, ag, ab, 140), width=2)
screen_mask = rounded_mask((PW_SCREEN, PH_SCREEN), 46)
island = (phone_body.width // 2 - 52, BEZ + 12, phone_body.width // 2 + 52, BEZ + 42)

tmp = Path("/tmp/compose_frames") / cap.name
tmp.mkdir(parents=True, exist_ok=True)
for p in tmp.glob("*.jpg"):
    p.unlink()


def render(i):
    t = i / max(1, N - 1)
    frame = BG.copy()
    # gentle float
    fy = math.sin(2 * math.pi * t) * 6
    py_off = math.sin(2 * math.pi * t + 1.4) * 10
    frame.alpha_composite(win_glow, (DX - gpad, int(DY + fy) - gpad + 20))
    frame.alpha_composite(win_shadow, (DX - wpad, int(DY + fy) - wpad + 30))
    win = chrome.copy()
    d = Image.open(d_frames[i]).convert("RGB").resize((DW, round(DW * 900 / 1440)), Image.LANCZOS)
    d = d.crop((0, 0, DW, DH_CONTENT))
    win.paste(d, (0, BAR), content_mask)
    win.putalpha(Image.composite(win.getchannel("A"), Image.new("L", win.size, 0), win_mask))
    ImageDraw.Draw(win).rounded_rectangle((0, 0, DW - 1, DH_CONTENT + BAR - 1), 22, outline=(ar, ag, ab, 110), width=2)
    frame.alpha_composite(win, (DX, int(DY + fy)))
    # phone
    pyy = int(PY + py_off)
    frame.alpha_composite(ph_shadow, (PX - ppad, pyy - ppad + 30))
    ph = phone_body.copy()
    m = Image.open(m_frames[i]).convert("RGB").resize((PW_SCREEN, PH_SCREEN), Image.LANCZOS)
    ph.paste(m, (BEZ, BEZ), screen_mask)
    ImageDraw.Draw(ph).rounded_rectangle(island, 15, fill=(0, 0, 0, 255))
    frame.alpha_composite(ph, (PX, pyy))
    return frame.convert("RGB").resize((OUT_W, OUT_H), Image.LANCZOS)


frames = [render(i) for i in range(N)]
first = frames[0]
for k in range(FADE):
    a = (k + 1) / (FADE + 1)
    idx = N - FADE + k
    frames[idx] = Image.blend(frames[idx], first, a)
for i, f in enumerate(frames):
    f.save(tmp / f"{i:04d}.jpg", quality=94)
first.save(out_jpg, quality=86)
subprocess.run([
    "ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", str(tmp / "%04d.jpg"),
    "-c:v", "libx264", "-preset", "slow", "-crf", "22", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-an", out_mp4,
], check=True)
print("ok", out_mp4, N, "frames")
