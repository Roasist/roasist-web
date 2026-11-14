"""Generate custom 1080x1080 60fps service showcase videos for the homepage '360° Hizmetler' section.

Builds:
  1. public/images/services/performans-pazarlamasi.mp4 (and .jpg poster)
     Replicates KOTA's Branding-1.mp4 circular-orbit + stepped Z-stack square-card format
     using 8 real Roasist client reference videos.
  2. public/images/services/web-tasarim.mp4 (and .jpg poster)
     Replicates KOTA's Websites-2026-1.mp4 3D tilted elliptical cascading gallery with
     true pinhole perspective projection and optical depth-of-field bokeh using 5 real
     Roasist client website UIs (Livaneli Hotels, TalentFinder, Summer Homes, Cordelia, HRShortlist).
"""

import math
import pathlib
import subprocess
import sys
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


# ---------------------------------------------------------------------------
# Card 2: Web Tasarım & Kreatif Stüdyo (3D Cascading Website Gallery)
# ---------------------------------------------------------------------------

WEB_SCREENS_DIR = ROOT / "scripts" / "assets" / "web-screens"
WEB_SITES = [
    ("cordelia", WEB_SCREENS_DIR / "cordelia.jpg"),
    ("talentfinder", WEB_SCREENS_DIR / "talentfinder.jpg"),
    ("livaneli", WEB_SCREENS_DIR / "livaneli.jpg"),
    ("hrshortlist", WEB_SCREENS_DIR / "hrshortlist.jpg"),
    ("summerhomes", WEB_SCREENS_DIR / "summerhomes.jpg"),
]

WEB_CARD_W = 662.0
WEB_CARD_H = 372.0
WEB_SPR_W = 860
WEB_SPR_H = 483
WEB_PAD = 48
WEB_FULL_W = WEB_SPR_W + 2 * WEB_PAD
WEB_FULL_H = WEB_SPR_H + 2 * WEB_PAD
WEB_FRAMES_PER_CARD = 75  # 1.25s per card @ 60fps (exact Websites-2026-1.mp4 cadence)
WEB_TOTAL_FRAMES = len(WEB_SITES) * WEB_FRAMES_PER_CARD  # 375 frames = 6.25s seamless half-ring loop


def _solve_homography(src_pts, dst_pts):
    """Solve 8-parameter perspective transform coefficients mapping dst -> src for PIL."""
    mat_a = []
    vec_b = []
    for (u, v), (x, y) in zip(src_pts, dst_pts):
        mat_a.append([x, y, 1.0, 0.0, 0.0, 0.0, -u * x, -u * y])
        mat_a.append([0.0, 0.0, 0.0, x, y, 1.0, -v * x, -v * y])
        vec_b.append(u)
        vec_b.append(v)
    coeffs = np.linalg.solve(np.array(mat_a, dtype=np.float64), np.array(vec_b, dtype=np.float64))
    return tuple(coeffs.tolist())


def _build_premul_bokeh_bank(img_path: pathlib.Path, n_levels: int = 49, max_sigma: float = 14.0):
    """Build premultiplied RGBA sprites across optical defocus levels (zero dark edge fringes)."""
    raw = Image.open(img_path).convert("RGB")
    card_rgb = raw.resize((WEB_SPR_W, WEB_SPR_H), Image.Resampling.LANCZOS)

    ss = 4
    rad = int(round(11.5 * ss))
    mask_big = Image.new("L", (WEB_SPR_W * ss, WEB_SPR_H * ss), 0)
    ImageDraw.Draw(mask_big).rounded_rectangle(
        (0, 0, WEB_SPR_W * ss - 1, WEB_SPR_H * ss - 1), radius=rad, fill=255
    )
    alpha_card = mask_big.resize((WEB_SPR_W, WEB_SPR_H), Image.Resampling.LANCZOS)

    premul_base = np.zeros((WEB_FULL_H, WEB_FULL_W, 4), dtype=np.float32)

    sh_canvas = Image.new("L", (WEB_FULL_W, WEB_FULL_H), 0)
    sh_canvas.paste(alpha_card, (WEB_PAD - 4, WEB_PAD + 9))
    sh_canvas = sh_canvas.filter(ImageFilter.GaussianBlur(radius=15))
    premul_base[..., 3] = (np.array(sh_canvas, dtype=np.float32) / 255.0) * 0.68

    rgb_arr = np.array(card_rgb, dtype=np.float32) / 255.0
    a_arr = np.array(alpha_card, dtype=np.float32) / 255.0

    sub = premul_base[WEB_PAD : WEB_PAD + WEB_SPR_H, WEB_PAD : WEB_PAD + WEB_SPR_W]
    inv_a = 1.0 - a_arr[..., None]
    sub[..., :3] = rgb_arr * a_arr[..., None] + sub[..., :3] * inv_a
    sub[..., 3] = a_arr + sub[..., 3] * (1.0 - a_arr)

    ch_imgs = [
        Image.fromarray(np.clip(premul_base[..., c] * 255.0 + 0.5, 0, 255).astype(np.uint8), mode="L")
        for c in range(4)
    ]
    bank = []
    for i in range(n_levels):
        sigma = (i / (n_levels - 1)) * max_sigma
        if sigma < 0.12:
            blurred_chs = ch_imgs
        else:
            blurred_chs = [ch.filter(ImageFilter.GaussianBlur(radius=sigma)) for ch in ch_imgs]
        bank.append(Image.merge("RGBA", blurred_chs))
    return bank


def build_web_tasarim():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_mp4 = OUT_DIR / "web-tasarim.mp4"
    out_jpg = OUT_DIR / "web-tasarim.jpg"

    print(f"Building 49-level optical bokeh banks for {len(WEB_SITES)} client websites...")
    banks = []
    for slug, img_path in WEB_SITES:
        print(f"  -> {slug} ({img_path.relative_to(ROOT)})")
        banks.append(_build_premul_bokeh_bank(img_path))

    # 10 slots around 3D elliptical ring ([S0..S4, S0..S4]): +180° (5 steps) is an exact seamless loop
    n_slots = 10
    slot_banks = [banks[i % len(WEB_SITES)] for i in range(n_slots)]
    n_levels = len(banks[0])

    pad_x_3d = WEB_CARD_W * (WEB_PAD / WEB_SPR_W)
    pad_y_3d = WEB_CARD_H * (WEB_PAD / WEB_SPR_H)
    local_corners = np.array(
        [
            [-WEB_CARD_W / 2 - pad_x_3d, -WEB_CARD_H / 2 - pad_y_3d, 0.0],
            [+WEB_CARD_W / 2 + pad_x_3d, -WEB_CARD_H / 2 - pad_y_3d, 0.0],
            [+WEB_CARD_W / 2 + pad_x_3d, +WEB_CARD_H / 2 + pad_y_3d, 0.0],
            [-WEB_CARD_W / 2 - pad_x_3d, +WEB_CARD_H / 2 + pad_y_3d, 0.0],
        ],
        dtype=np.float64,
    )
    src_corners = [(0.0, 0.0), (WEB_FULL_W, 0.0), (WEB_FULL_W, WEB_FULL_H), (0.0, WEB_FULL_H)]

    yaw_rad = math.radians(10.5)
    rot_local = np.stack(
        [
            local_corners[:, 0] * math.cos(yaw_rad),
            local_corners[:, 1],
            local_corners[:, 0] * math.sin(yaw_rad),
        ],
        axis=1,
    )

    cam_x = 532.0
    cam_y = 524.0
    focal = 2350.0
    r_z = 457.0
    cam_z = focal + r_z

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
        "-crf", "19",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        "-an",
        str(out_mp4),
    ]

    print(f"Rendering {WEB_TOTAL_FRAMES} frames ({WEB_TOTAL_FRAMES / FPS:.2f}s) -> {out_mp4.relative_to(ROOT)} ...")
    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)
    assert proc.stdin is not None

    for f in range(WEB_TOTAL_FRAMES):
        # Advance +pi radians (+180° = 5 slots) so slot k lands identically on slot k+5
        phase_rad = math.pi * (f / WEB_TOTAL_FRAMES)
        canvas = np.zeros((CANVAS, CANVAS, 3), dtype=np.float32)

        cards = []
        for k in range(n_slots):
            phi = phase_rad + k * (2.0 * math.pi / n_slots)
            s = math.sin(phi)
            c = math.cos(phi)
            back_tuck = (max(0.0, -c) ** 2) * 145.0
            cx_3d = -332.0 * s + 96.0 * c + back_tuck
            cy_3d = +598.0 * s
            cz_3d = r_z * c
            cards.append((cz_3d, c, k, cx_3d, cy_3d))

        cards.sort(key=lambda item: item[0])

        for cz_3d, c, k, cx_3d, cy_3d in cards:
            pts_3d = rot_local + np.array([cx_3d, cy_3d, cz_3d])
            depth = cam_z - pts_3d[:, 2]
            xs = cam_x + focal * (pts_3d[:, 0] / depth)
            ys = cam_y + focal * (pts_3d[:, 1] / depth)

            cx0 = max(0, int(math.floor(xs.min())) - 2)
            cy0 = max(0, int(math.floor(ys.min())) - 2)
            cx1 = min(CANVAS, int(math.ceil(xs.max())) + 2)
            cy1 = min(CANVAS, int(math.ceil(ys.max())) + 2)
            if cx1 <= cx0 or cy1 <= cy0:
                continue

            if c >= 0.88:
                blur_t = 0.0
            else:
                blur_t = min(1.0, ((0.88 - c) / 1.35) ** 1.3)
            lvl = int(round(blur_t * (n_levels - 1)))
            sprite = slot_banks[k][lvl]

            if c >= 0.45:
                bright = 1.0
            else:
                bright = 0.52 + 0.48 * max(0.0, (c + 1.0) / 1.45)

            dst_pts = [(float(x - cx0), float(y - cy0)) for x, y in zip(xs, ys)]
            coeffs = _solve_homography(src_corners, dst_pts)
            warped = sprite.transform(
                (cx1 - cx0, cy1 - cy0),
                Image.Transform.PERSPECTIVE,
                coeffs,
                resample=Image.Resampling.BICUBIC,
            )
            w_arr = np.array(warped, dtype=np.float32) / 255.0
            patch_rgb = w_arr[..., :3] * bright
            patch_a = w_arr[..., 3:4]

            roi = canvas[cy0:cy1, cx0:cx1]
            canvas[cy0:cy1, cx0:cx1] = patch_rgb + roi * (1.0 - patch_a)

        rgb_bytes = np.clip(canvas * 255.0 + 0.5, 0, 255).astype(np.uint8)
        if f == 0:
            Image.fromarray(rgb_bytes, mode="RGB").save(out_jpg, quality=92, optimize=True)
        proc.stdin.write(rgb_bytes.tobytes())

    proc.stdin.close()
    rc = proc.wait()
    if rc != 0:
        raise RuntimeError(f"ffmpeg exited with status {rc}")

    size_mb = out_mp4.stat().st_size / (1024 * 1024)
    print(f"Done! {out_mp4.relative_to(ROOT)} ({size_mb:.2f} MB), poster: {out_jpg.relative_to(ROOT)}")


# ---------------------------------------------------------------------------
# Card 3: SEO, AEO & 360° Dijital Büyüme (3D Z-Depth AI & Search Cloud)
# ---------------------------------------------------------------------------

GROWTH_CARDS_DIR = ROOT / "scripts" / "assets" / "growth-cards"
GROWTH_HERO_SIZE = 446.0
GROWTH_TOTAL_FRAMES = 480  # 8.00s @ 60fps seamless 360° 3D Z-cloud revolution

GROWTH_CARD_SPECS = [
    # (slug, base_dx, base_dy, orbit_rx, orbit_ry, phase_offset_deg)
    ("roasist",          +152.0,  +35.0,  92.0,  75.0,    0.0),
    ("gemini",           -180.0, +135.0, 102.0,  85.0,   45.0),
    ("google-analytics", +155.0, -135.0,  95.0,  85.0,   90.0),
    ("perplexity",       -142.0, -145.0, 100.0,  80.0,  135.0),
    ("chatgpt",          +135.0, +150.0, 105.0,  85.0,  180.0),
    ("search-console",   -168.0,  -20.0,  95.0,  85.0,  225.0),
    ("claude",            +15.0, +175.0, 110.0,  75.0,  270.0),
    ("ai-search",         -35.0, -165.0, 105.0,  80.0,  315.0),
]


def _load_premul_square_card(png_path: pathlib.Path, master_size: int = 600, pad: int = 32):
    """Load 1000x1000 square card PNG into a premultiplied RGBA master sprite with soft shadow."""
    raw = Image.open(png_path).convert("RGB").resize((master_size, master_size), Image.Resampling.LANCZOS)
    ss = 4
    rad = int(round(15 * ss))
    mask_big = Image.new("L", (master_size * ss, master_size * ss), 0)
    ImageDraw.Draw(mask_big).rounded_rectangle(
        (0, 0, master_size * ss - 1, master_size * ss - 1), radius=rad, fill=255
    )
    alpha_card = mask_big.resize((master_size, master_size), Image.Resampling.LANCZOS)

    rim_big = Image.new("RGBA", (master_size * ss, master_size * ss), (0, 0, 0, 0))
    ImageDraw.Draw(rim_big).rounded_rectangle(
        (ss // 2, ss // 2, master_size * ss - 1 - ss // 2, master_size * ss - 1 - ss // 2),
        radius=rad,
        outline=(255, 255, 255, 28),
        width=ss,
    )
    rim = rim_big.resize((master_size, master_size), Image.Resampling.LANCZOS)
    card_rgba = raw.convert("RGBA")
    card_rgba.putalpha(alpha_card)
    card_rgba = Image.alpha_composite(card_rgba, rim)

    full = master_size + 2 * pad
    premul = np.zeros((full, full, 4), dtype=np.float32)

    sh = Image.new("L", (full, full), 0)
    sh.paste(alpha_card, (pad, pad + 8))
    sh = sh.filter(ImageFilter.GaussianBlur(radius=14))
    premul[..., 3] = (np.array(sh, dtype=np.float32) / 255.0) * 0.68

    c_arr = np.array(card_rgba, dtype=np.float32) / 255.0
    rgb = c_arr[..., :3]
    a = c_arr[..., 3:4]
    sub = premul[pad : pad + master_size, pad : pad + master_size]
    sub[..., :3] = rgb * a + sub[..., :3] * (1.0 - a)
    sub[..., 3:4] = a + sub[..., 3:4] * (1.0 - a)

    sprite = Image.fromarray(np.clip(premul * 255.0 + 0.5, 0, 255).astype(np.uint8), mode="RGBA")
    return sprite, master_size, pad


def build_seo_aeo_buyume():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_mp4 = OUT_DIR / "seo-aeo-buyume.mp4"
    out_jpg = OUT_DIR / "seo-aeo-buyume.jpg"

    print(f"Loading {len(GROWTH_CARD_SPECS)} SEO/AEO square brand sprites...")
    loaded = []
    for spec in GROWTH_CARD_SPECS:
        slug = spec[0]
        p = GROWTH_CARDS_DIR / f"{slug}.png"
        print(f"  -> {slug} ({p.relative_to(ROOT)})")
        spr, m_sz, pad = _load_premul_square_card(p)
        loaded.append((spr, m_sz, pad, *spec[1:]))

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
        "-crf", "19",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        "-an",
        str(out_mp4),
    ]

    print(f"Rendering {GROWTH_TOTAL_FRAMES} frames ({GROWTH_TOTAL_FRAMES / FPS:.2f}s) -> {out_mp4.relative_to(ROOT)} ...")
    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)
    assert proc.stdin is not None

    n_cards = len(loaded)
    start_phase = math.radians(14.0)

    for f in range(GROWTH_TOTAL_FRAMES):
        phase_rad = start_phase + (2.0 * math.pi * f / GROWTH_TOTAL_FRAMES)
        canvas = np.zeros((CANVAS, CANVAS, 3), dtype=np.float32)

        items = []
        for k, (spr, m_sz, pad, base_dx, base_dy, orx, ory, p_deg) in enumerate(loaded):
            theta = phase_rad - k * (2.0 * math.pi / n_cards)
            c = math.cos(theta)
            t01 = 0.5 * (c + 1.0)
            surge = (max(0.0, c) ** 3.0) * 0.27
            scale = 0.40 + 0.35 * (t01 ** 1.15) + surge

            p_rad = math.radians(p_deg)
            pull = 0.82 + 0.24 * t01
            cx = 540.0 + base_dx * pull + orx * math.sin(theta + p_rad)
            cy = 540.0 + base_dy * pull + ory * math.cos(theta + p_rad * 0.7)

            bright = 1.0 if c >= -0.10 else (0.70 + 0.30 * ((c + 1.0) / 0.90))
            items.append((c, scale, cx, cy, bright, spr, m_sz, pad))

        items.sort(key=lambda it: it[0])

        for c, scale, cx, cy, bright, spr, m_sz, pad in items:
            card_px = GROWTH_HERO_SIZE * scale
            full_px = card_px * ((m_sz + 2.0 * pad) / m_sz)
            x0 = cx - full_px / 2.0
            y0 = cy - full_px / 2.0

            ix = int(math.floor(x0))
            iy = int(math.floor(y0))
            fx = x0 - ix
            fy = y0 - iy
            out_w = int(math.ceil(full_px)) + 3
            out_h = int(math.ceil(full_px)) + 3

            inv_s = spr.size[0] / full_px
            warped = spr.transform(
                (out_w, out_h),
                Image.Transform.AFFINE,
                (inv_s, 0.0, -fx * inv_s, 0.0, inv_s, -fy * inv_s),
                resample=Image.Resampling.BICUBIC,
            )

            cx0 = max(0, ix)
            cy0 = max(0, iy)
            cx1 = min(CANVAS, ix + out_w)
            cy1 = min(CANVAS, iy + out_h)
            if cx1 <= cx0 or cy1 <= cy0:
                continue

            sx0 = cx0 - ix
            sy0 = cy0 - iy
            sx1 = sx0 + (cx1 - cx0)
            sy1 = sy0 + (cy1 - cy0)

            w_arr = np.array(warped, dtype=np.float32)[sy0:sy1, sx0:sx1] / 255.0
            p_rgb = w_arr[..., :3] * bright
            p_a = w_arr[..., 3:4]
            roi = canvas[cy0:cy1, cx0:cx1]
            canvas[cy0:cy1, cx0:cx1] = p_rgb + roi * (1.0 - p_a)

        rgb_bytes = np.clip(canvas * 255.0 + 0.5, 0, 255).astype(np.uint8)
        if f == 0:
            Image.fromarray(rgb_bytes, mode="RGB").save(out_jpg, quality=92, optimize=True)
        proc.stdin.write(rgb_bytes.tobytes())

    proc.stdin.close()
    rc = proc.wait()
    if rc != 0:
        raise RuntimeError(f"ffmpeg exited with status {rc}")

    size_mb = out_mp4.stat().st_size / (1024 * 1024)
    print(f"Done! {out_mp4.relative_to(ROOT)} ({size_mb:.2f} MB), poster: {out_jpg.relative_to(ROOT)}")


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "all"
    if target in ("all", "performans-pazarlamasi"):
        build_performans_pazarlamasi()
    if target in ("all", "web-tasarim"):
        build_web_tasarim()
    if target in ("all", "seo-aeo-buyume"):
        build_seo_aeo_buyume()


