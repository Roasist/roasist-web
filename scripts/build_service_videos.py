"""Generate custom 1080x1080 60fps service showcase videos for the homepage '360° Hizmetler' section.

Currently builds:
  - public/images/services/performans-pazarlamasi.mp4 (and .jpg poster)
    Replicates the exact 1080x1080 60fps circular-orbit + stepped Z-stack square-card
    format of KOTA's Branding-1.mp4 using 8 real Roasist client reference videos.
"""

import math
import pathlib
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = pathlib.Path("/home/antigravity/Roasist/roasist-web")
OUT_DIR = ROOT / "public" / "images" / "services"

CANVAS = 1080
CARD_SIZE = 418
CORNER_RADIUS = 18
ORBIT_RADIUS = 212.0
FPS = 60
STEP_FRAMES = 24
NUM_CARDS = 8
TOTAL_STEPS = NUM_CARDS * 2  # 16 Z-steps = 1 full 360° orbital revolution
TOTAL_FRAMES = TOTAL_STEPS * STEP_FRAMES  # 384 frames = 6.40s @ 60fps
CROSSFADE_FRAMES = 36  # 0.60s seamless sub-video loop cross-dissolve

# 8 diverse Roasist client production videos (16:9 -> 1:1 center crop)
CLIENT_CLIPS = [
    ("cordelia", "public/images/references/cordelia.mp4", 1.0),
    ("medistate", "public/images/projects/medistate.mp4", 2.0),
    ("pedalbox", "public/images/references/pedalbox.mp4", 2.0),
    ("livaneli-hotels", "public/images/references/livaneli-group.mp4", 3.0),
    ("istanbul-medya-akademisi", "public/images/references/istanbul-medya-akademisi.mp4", 1.5),
    ("gekoo", "public/images/references/gekoo.mp4", 1.5),
    ("izmir-balik-restaurant", "public/images/references/izmir-balik-restaurant.mp4", 1.0),
    ("bonus-vip", "public/images/projects/bonus-vip-office.mp4", 1.5),
]


def load_seamless_square_clip(rel_path: str, start_sec: float) -> np.ndarray:
    """Decode (TOTAL_FRAMES + CROSSFADE_FRAMES) @ 60fps 418x418 and build a seamless 384-frame loop."""
    need = TOTAL_FRAMES + CROSSFADE_FRAMES
    dur = need / FPS + 0.15
    src = ROOT / rel_path
    vf = f"fps={FPS},crop=ih:ih:(iw-ih)/2:0,scale={CARD_SIZE}:{CARD_SIZE}:flags=lanczos"
    cmd = [
        "ffmpeg",
        "-v", "error",
        "-ss", f"{start_sec:.2f}",
        "-t", f"{dur:.2f}",
        "-i", str(src),
        "-vf", vf,
        "-frames:v", str(need),
        "-f", "rawvideo",
        "-pix_fmt", "rgb24",
        "pipe:1",
    ]
    raw_bytes = subprocess.check_output(cmd)
    frames = np.frombuffer(raw_bytes, dtype=np.uint8).reshape((-1, CARD_SIZE, CARD_SIZE, 3))
    if len(frames) < need:
        # Tile if slightly short
        reps = (need // len(frames)) + 2
        frames = np.tile(frames, (reps, 1, 1, 1))[:need]

    # Build boundary-continuous loop of length TOTAL_FRAMES:
    # frame[TOTAL_FRAMES - 1] = raw[TOTAL_FRAMES - 1]
    # frame[0]                = raw[TOTAL_FRAMES]  (exact consecutive camera frame!)
    # frames[0..CROSSFADE-1]  smoothly cross-dissolve raw[TOTAL_FRAMES..] -> raw[0..CROSSFADE-1]
    loop = np.empty((TOTAL_FRAMES, CARD_SIZE, CARD_SIZE, 3), dtype=np.uint8)
    loop[CROSSFADE_FRAMES:] = frames[CROSSFADE_FRAMES:TOTAL_FRAMES]
    for i in range(CROSSFADE_FRAMES):
        t = (i + 1) / (CROSSFADE_FRAMES + 1)
        w = t * t * (3.0 - 2.0 * t)  # smoothstep
        blended = (
            w * frames[i].astype(np.float32)
            + (1.0 - w) * frames[TOTAL_FRAMES + i].astype(np.float32)
        )
        loop[i] = np.clip(blended + 0.5, 0, 255).astype(np.uint8)
    return loop


def make_card_masks():
    """Return supersampled rounded alpha mask, subtle inner border overlay, and soft drop shadow."""
    ss = 4
    big = CARD_SIZE * ss
    rad = CORNER_RADIUS * ss

    mask_big = Image.new("L", (big, big), 0)
    ImageDraw.Draw(mask_big).rounded_rectangle((0, 0, big - 1, big - 1), radius=rad, fill=255)
    card_alpha = mask_big.resize((CARD_SIZE, CARD_SIZE), Image.Resampling.LANCZOS)

    # Subtle 1px inner border so dark video frames still keep crisp card geometry on #000
    rim_big = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    ImageDraw.Draw(rim_big).rounded_rectangle(
        (ss // 2, ss // 2, big - 1 - ss // 2, big - 1 - ss // 2),
        radius=rad,
        outline=(255, 255, 255, 24),
        width=ss,
    )
    rim_rgba = rim_big.resize((CARD_SIZE, CARD_SIZE), Image.Resampling.LANCZOS)

    # Soft drop shadow (padded by 28px on each side)
    pad = 28
    sh_size = CARD_SIZE + pad * 2
    sh = Image.new("RGBA", (sh_size, sh_size), (0, 0, 0, 0))
    sh_mask = Image.new("L", (sh_size, sh_size), 0)
    sh_mask.paste(card_alpha, (pad, pad + 6))
    sh_mask = sh_mask.filter(ImageFilter.GaussianBlur(radius=11))
    sh_arr = np.zeros((sh_size, sh_size, 4), dtype=np.uint8)
    sh_arr[..., 3] = (np.array(sh_mask, dtype=np.float32) * 0.58).astype(np.uint8)
    shadow_rgba = Image.fromarray(sh_arr, mode="RGBA")

    return card_alpha, rim_rgba, shadow_rgba, pad


def place_subpixel_rgba(canvas_rgba: Image.Image, sprite_rgba: Image.Image, x: float, y: float):
    """Composite sprite_rgba onto canvas_rgba at sub-pixel top-left (x, y) using bilinear affine."""
    ix = int(math.floor(x))
    iy = int(math.floor(y))
    fx = x - ix
    fy = y - iy
    w, h = sprite_rgba.size
    # Shift by fractional (fx, fy) inside a (w+2, h+2) patch for zero integer jitter
    shifted = sprite_rgba.transform(
        (w + 2, h + 2),
        Image.Transform.AFFINE,
        (1, 0, -fx, 0, 1, -fy),
        resample=Image.Resampling.BILINEAR,
    )
    canvas_rgba.alpha_composite(shifted, dest=(ix, iy))


def build_performans_pazarlamasi():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_mp4 = OUT_DIR / "performans-pazarlamasi.mp4"
    out_jpg = OUT_DIR / "performans-pazarlamasi.jpg"

    print(f"Loading & looping {NUM_CARDS} client clips ({TOTAL_FRAMES} frames @ {FPS}fps)...")
    clips = []
    for slug, rel, ss in CLIENT_CLIPS:
        print(f"  -> {slug} ({rel} @ {ss}s)")
        clips.append(load_seamless_square_clip(rel, ss))

    card_alpha, rim_rgba, shadow_rgba, sh_pad = make_card_masks()

    ffmpeg_cmd = [
        "ffmpeg",
        "-y",
        "-v", "error",
        "-f", "rawvideo",
        "-pix_fmt", "rgb24",
        "-s", f"{CANVAS}x{CANVAS}",
        "-r", str(FPS),
        "-i", "pipe:0",
        "-c:v", "libx264",
        "-profile:v", "high",
        "-preset", "slow",
        "-crf", "20",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        "-an",
        str(out_mp4),
    ]

    print(f"Rendering {TOTAL_FRAMES} frames ({TOTAL_FRAMES / FPS:.2f}s) -> {out_mp4.relative_to(ROOT)} ...")
    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)
    assert proc.stdin is not None

    for f in range(TOTAL_FRAMES):
        canvas = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 255))
        step = f // STEP_FRAMES
        # Exact Branding-1.mp4 Z-stack order from back (0) to front (7)
        draw_order = [(step + 1 + i) % NUM_CARDS for i in range(NUM_CARDS)]

        for k in draw_order:
            angle_deg = -30.0 - k * (360.0 / NUM_CARDS) - (360.0 * f / TOTAL_FRAMES)
            rad = math.radians(angle_deg)
            cx = CANVAS / 2.0 + ORBIT_RADIUS * math.cos(rad)
            cy = CANVAS / 2.0 + ORBIT_RADIUS * math.sin(rad)
            top_left_x = cx - CARD_SIZE / 2.0
            top_left_y = cy - CARD_SIZE / 2.0

            # 1. Soft drop shadow behind card
            place_subpixel_rgba(canvas, shadow_rgba, top_left_x - sh_pad, top_left_y - sh_pad)

            # 2. Rounded video card + subtle rim
            card_rgb = Image.fromarray(clips[k][f], mode="RGB")
            card_rgba = card_rgb.convert("RGBA")
            card_rgba.putalpha(card_alpha)
            card_rgba = Image.alpha_composite(card_rgba, rim_rgba)
            place_subpixel_rgba(canvas, card_rgba, top_left_x, top_left_y)

        rgb_frame = canvas.convert("RGB")
        if f == 0:
            rgb_frame.save(out_jpg, quality=90, optimize=True)
        proc.stdin.write(rgb_frame.tobytes())

    proc.stdin.close()
    rc = proc.wait()
    if rc != 0:
        raise RuntimeError(f"ffmpeg exited with status {rc}")

    size_mb = out_mp4.stat().st_size / (1024 * 1024)
    print(f"Done! {out_mp4.relative_to(ROOT)} ({size_mb:.2f} MB), poster: {out_jpg.relative_to(ROOT)}")


if __name__ == "__main__":
    build_performans_pazarlamasi()
