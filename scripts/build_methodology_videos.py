"""Generate custom 1020x788 60fps showcase videos for the homepage 'Adım adım büyüme metodolojimiz.' carousel.

Currently builds:
  1. public/images/methodology/01-veri-ve-strateji.mp4 (and .jpg poster)
     Replicates KOTA's Strategy-Firstv2-compressed.mp4 interactive FigJam strategy board
     pan/zoom + live collaborative team cursors, tailored 100% to Roasist's Turkish
     data & unit-economics methodology and real client portfolio.
"""

import math
import pathlib
import subprocess
import sys
import numpy as np
from PIL import Image

ROOT = pathlib.Path("/home/antigravity/Roasist/roasist-web")
ASSETS_DIR = ROOT / "scripts" / "assets" / "methodology"
OUT_DIR = ROOT / "public" / "images" / "methodology"

OUT_W = 1020
OUT_H = 788
ASPECT = OUT_H / OUT_W
FPS = 60


def _periodic_catmull_rom(waypoints: np.ndarray, t01: float) -> np.ndarray:
    """Evaluate C1-smooth closed periodic Catmull-Rom spline at t01 in [0, 1)."""
    n = len(waypoints)
    pos = (t01 % 1.0) * n
    i1 = int(math.floor(pos)) % n
    u = pos - math.floor(pos)
    i0 = (i1 - 1) % n
    i2 = (i1 + 1) % n
    i3 = (i1 + 2) % n

    p0, p1, p2, p3 = waypoints[i0], waypoints[i1], waypoints[i2], waypoints[i3]
    u2 = u * u
    u3 = u2 * u
    return 0.5 * (
        (2.0 * p1)
        + (-p0 + p2) * u
        + (2.0 * p0 - 5.0 * p1 + 4.0 * p2 - p3) * u2
        + (-p0 + 3.0 * p1 - 3.0 * p2 + p3) * u3
    )


def _dwell_periodic_spline(waypoints: np.ndarray, t01: float, dwell_strength: float = 0.42) -> np.ndarray:
    """Cursor spline with natural human ease-in-out hover dwells at each waypoint."""
    n = len(waypoints)
    pos = (t01 % 1.0) * n
    seg = int(math.floor(pos)) % n
    u = pos - math.floor(pos)
    # Smoothstep blend with subtle dwell near waypoint knots
    s = u * u * (3.0 - 2.0 * u)
    s2 = s * s * (3.0 - 2.0 * s)
    u_warped = (1.0 - dwell_strength) * u + dwell_strength * s2
    return _periodic_catmull_rom(waypoints, (seg + u_warped) / n)


def _load_premul_cursor(png_path: pathlib.Path, scale: float = 0.60) -> tuple[np.ndarray, int, int]:
    im = Image.open(png_path).convert("RGBA")
    nw = int(round(im.width * scale))
    nh = int(round(im.height * scale))
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    arr = np.array(im, dtype=np.float32) / 255.0
    premul = np.empty_like(arr)
    premul[..., :3] = arr[..., :3] * arr[..., 3:4]
    premul[..., 3] = arr[..., 3]
    # Pointer tip inside 440x160 padded render is at ~(14*scale, 13*scale)
    tip_x = int(round(14 * scale))
    tip_y = int(round(13 * scale))
    return premul, tip_x, tip_y


def _composite_cursor_subpixel(canvas: np.ndarray, premul_cur: np.ndarray, sx: float, sy: float):
    """Composite premultiplied cursor onto float32 RGB canvas at sub-pixel top-left (sx, sy)."""
    h, w, _ = premul_cur.shape
    ix = int(math.floor(sx))
    iy = int(math.floor(sy))
    fx = sx - ix
    fy = sy - iy

    # Bilinear shift in numpy for silky 60fps cursor motion
    pad_cur = np.zeros((h + 2, w + 2, 4), dtype=np.float32)
    pad_cur[1 : h + 1, 1 : w + 1] = premul_cur
    shifted = (
        (1.0 - fx) * (1.0 - fy) * pad_cur[1 : h + 1, 1 : w + 1]
        + fx * (1.0 - fy) * pad_cur[1 : h + 1, 0:w]
        + (1.0 - fx) * fy * pad_cur[0:h, 1 : w + 1]
        + fx * fy * pad_cur[0:h, 0:w]
    )

    cx0 = max(0, ix)
    cy0 = max(0, iy)
    cx1 = min(OUT_W, ix + w)
    cy1 = min(OUT_H, iy + h)
    if cx1 <= cx0 or cy1 <= cy0:
        return

    ux0 = cx0 - ix
    uy0 = cy0 - iy
    ux1 = ux0 + (cx1 - cx0)
    uy1 = uy0 + (cy1 - cy0)

    patch = shifted[uy0:uy1, ux0:ux1]
    roi = canvas[cy0:cy1, cx0:cx1]
    canvas[cy0:cy1, cx0:cx1] = patch[..., :3] + roi * (1.0 - patch[..., 3:4])


def build_01_veri_ve_strateji():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_mp4 = OUT_DIR / "01-veri-ve-strateji.mp4"
    out_jpg = OUT_DIR / "01-veri-ve-strateji.jpg"

    board_path = ASSETS_DIR / "board-01-strategy.png"
    print(f"Loading strategy board {board_path.relative_to(ROOT)} ...")
    board = Image.open(board_path).convert("RGB")
    bw, bh = board.size

    # Pre-filter slightly (0.85x Lanczos) so 1.1x-1.3x bicubic camera warps stay razor-sharp with zero mip pop
    mip_scale = 0.85
    src_img = board.resize((int(round(bw * mip_scale)), int(round(bh * mip_scale))), Image.Resampling.LANCZOS)

    cur_veri, tx_v, ty_v = _load_premul_cursor(ASSETS_DIR / "cursor-veri.png", scale=0.58)
    cur_strat, tx_s, ty_s = _load_premul_cursor(ASSETS_DIR / "cursor-strateji.png", scale=0.58)
    cur_medya, tx_m, ty_m = _load_premul_cursor(ASSETS_DIR / "cursor-medya.png", scale=0.58)

    # Closed periodic camera tour: (center_x, center_y, viewport_width)
    cam_waypoints = np.array(
        [
            [970.0,  640.0, 1340.0],  # 0: Unit Economics (6.4x) + Roasist Cobalt + Sticky 1
            [1560.0, 680.0, 1540.0],  # 1: Glide across Gap Matrix -> Multi-channel dark card
            [2360.0, 660.0, 1480.0],  # 2: Multi-channel + Önce Veri Lime card + Summer Homes + Sticky 2
            [2340.0, 1580.0, 1500.0], # 3: Full-Funnel + 90-Day Roadmap Plum card + HRShortlist
            [1520.0, 1740.0, 1520.0], # 4: Sticky 3 + %98.4 Magenta card + Funnel
            [930.0,  1760.0, 1460.0], # 5: Cordelia + Sticky 4 + Dark 6.4x Roadmap Output Bubbles
            [860.0,  1080.0, 1420.0], # 6: TalentFinder B2B Audit + Gap Matrix back up to Unit Economics
        ],
        dtype=np.float64,
    )

    # 3 Collaborative Figma Cursors visiting strategic targets along the camera path
    wp_strateji = np.array(
        [
            [1160.0, 520.0],  # Roasist Cobalt thesis card
            [1430.0, 880.0],  # Roasist Hedef Alanı on Gap Matrix
            [2560.0, 520.0],  # Önce Veri. Sonra Kampanya. lime card
            [2620.0, 1580.0], # 90 Gün Adım Adım Ölçeklenme Planı
            [1540.0, 1830.0], # Sticky 3
            [960.0,  1980.0], # 6.4x Hedef ROAS bubble
            [820.0,  740.0],  # Sticky 1
        ],
        dtype=np.float64,
    )

    wp_veri = np.array(
        [
            [520.0,  490.0],  # 6.4x Hedef ROAS KPI box
            [1980.0, 460.0],  # Google Arama %42 bar
            [2240.0, 760.0],  # Sticky 2
            [2080.0, 1620.0], # Full-funnel ROAS 7.8x bar
            [1280.0, 1560.0], # %98.4 Veri Doğruluğu card
            [760.0,  2060.0], # -38% Hedef CPA bubble
            [620.0,  980.0],  # TalentFinder wireframe sphere
        ],
        dtype=np.float64,
    )

    wp_medya = np.array(
        [
            [860.0,  760.0],  # Sticky 1
            [1890.0, 960.0],  # Summer Homes TR/EN/DE/RU
            [2740.0, 980.0],  # Yatırım & ROI Odaklı CPA -%34
            [2120.0, 2060.0], # HRShortlist landing page CTA
            [1020.0, 1760.0], # Sticky 4
            [580.0,  1540.0], # Cordelia creative tone card
            [1220.0, 620.0],  # Roasist Cobalt card bottom
        ],
        dtype=np.float64,
    )

    total_frames = 660  # 11.00s @ 60fps silky-smooth tour

    ffmpeg_cmd = [
        "ffmpeg",
        "-y",
        "-v", "error",
        "-f", "rawvideo",
        "-pix_fmt", "rgb24",
        "-s", f"{OUT_W}x{OUT_H}",
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

    print(f"Rendering {total_frames} frames ({total_frames / FPS:.2f}s) -> {out_mp4.relative_to(ROOT)} ...")
    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)
    assert proc.stdin is not None

    for f in range(total_frames):
        t01 = f / total_frames
        cx, cy, vw = _periodic_catmull_rom(cam_waypoints, t01)
        vh = vw * ASPECT

        x0 = cx - vw / 2.0
        y0 = cy - vh / 2.0

        sx_mul = mip_scale
        a = (vw / OUT_W) * sx_mul
        e = (vh / OUT_H) * sx_mul
        c_off = x0 * sx_mul
        f_off = y0 * sx_mul

        cropped = src_img.transform(
            (OUT_W, OUT_H),
            Image.Transform.AFFINE,
            (a, 0.0, c_off, 0.0, e, f_off),
            resample=Image.Resampling.BICUBIC,
        )
        canvas = np.array(cropped, dtype=np.float32) / 255.0

        # Project & composite the 3 collaborative Figma cursors in screen space
        for cur_arr, tip_x, tip_y, wps, phase_shift in (
            (cur_veri, tx_v, ty_v, wp_veri, 0.02),
            (cur_medya, tx_m, ty_m, wp_medya, -0.03),
            (cur_strat, tx_s, ty_s, wp_strateji, 0.0),
        ):
            wx, wy = _dwell_periodic_spline(wps, t01 + phase_shift)
            scr_x = (wx - x0) * (OUT_W / vw) - tip_x
            scr_y = (wy - y0) * (OUT_H / vh) - tip_y
            _composite_cursor_subpixel(canvas, cur_arr, scr_x, scr_y)

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


def _perspective_coeffs(dst_pts: np.ndarray, src_pts: np.ndarray) -> tuple[float, ...]:
    """Compute 8-tuple for PIL Image.Transform.PERSPECTIVE mapping dst_pts -> src_pts."""
    mat = []
    rhs = []
    for (dx, dy), (sx, sy) in zip(dst_pts, src_pts):
        mat.append([dx, dy, 1.0, 0.0, 0.0, 0.0, -sx * dx, -sx * dy])
        mat.append([0.0, 0.0, 0.0, dx, dy, 1.0, -sy * dx, -sy * dy])
        rhs.append(sx)
        rhs.append(sy)
    sol = np.linalg.solve(np.array(mat, dtype=np.float64), np.array(rhs, dtype=np.float64))
    return tuple(float(v) for v in sol)


def _smoothstep(edge0: float, edge1: float, x: float) -> float:
    if x <= edge0:
        return 0.0
    if x >= edge1:
        return 1.0
    u = (x - edge0) / (edge1 - edge0)
    return u * u * (3.0 - 2.0 * u)


def _ease_out_expo(u: float) -> float:
    u = max(0.0, min(1.0, u))
    return 1.0 - math.pow(2.0, -8.0 * u) * (1.0 - u)


def _alpha_over(dst_rgb: np.ndarray, src_rgba: np.ndarray, opacity: float = 1.0):
    if opacity <= 0.001:
        return
    a = src_rgba[..., 3:4] * opacity
    dst_rgb[:] = src_rgba[..., :3] * a + dst_rgb * (1.0 - a)


def build_02_yaratici_ve_cesur_fikir():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_mp4 = OUT_DIR / "02-yaratici-ve-cesur-fikir.mp4"
    out_jpg = OUT_DIR / "02-yaratici-ve-cesur-fikir.jpg"
    s2_dir = ASSETS_DIR / "s2"

    print("Loading Slide 2 studio assets ...")
    bento_rgba = np.array(Image.open(s2_dir / "bento-grid-overlay.png").convert("RGBA"), dtype=np.float32) / 255.0
    iso_rgba = np.array(Image.open(s2_dir / "center-iso-overlay.png").convert("RGBA"), dtype=np.float32) / 255.0
    hl1_rgba = np.array(Image.open(s2_dir / "headline-1.png").convert("RGBA"), dtype=np.float32) / 255.0
    hl2_rgba = np.array(Image.open(s2_dir / "headline-2.png").convert("RGBA"), dtype=np.float32) / 255.0
    brand_icon = np.array(Image.open(s2_dir / "brand-icon.png").convert("RGBA"), dtype=np.float32) / 255.0
    brand_lockup = np.array(Image.open(s2_dir / "brand-lockup.png").convert("RGBA"), dtype=np.float32) / 255.0

    cards_pil = [Image.open(s2_dir / f"card-{i:02d}.png").convert("RGBA") for i in range(1, 10)]

    # Pre-build Fibonacci 3D sphere points (2000 particles)
    rng = np.random.default_rng(42)
    n_pts = 2000
    idx = np.arange(n_pts, dtype=np.float32) + 0.5
    phi = np.arccos(1.0 - 2.0 * idx / n_pts)
    theta = math.pi * (1.0 + 5.0**0.5) * idx
    # Add organic jitter shell thickness
    r_shell = 1.0 + rng.normal(0.0, 0.035, size=n_pts).astype(np.float32)
    base_xyz = np.stack(
        [
            r_shell * np.sin(phi) * np.cos(theta),
            r_shell * np.cos(phi),
            r_shell * np.sin(phi) * np.sin(theta),
        ],
        axis=1,
    )
    pt_tint = rng.uniform(0.0, 1.0, size=(n_pts, 1)).astype(np.float32)

    # Pre-build radial emerald core glow for the 1200x820 center hero screen
    cw, ch = 1200, 820
    yy, xx = np.mgrid[0:ch, 0:cw].astype(np.float32)
    dist_center = np.sqrt((xx - 600.0) ** 2 + (yy - 415.0) ** 2)
    emerald_glow = np.exp(-0.5 * (dist_center / 235.0) ** 2)[..., None]
    screen_bg_grad = (
        np.array([0.03, 0.16, 0.15], dtype=np.float32)
        * np.exp(-0.5 * (dist_center / 540.0) ** 2)[..., None]
    )

    # Pre-build static bento RGB canvas (2800x2100) outside the center 1200x820 window
    bw, bh = 2800, 2100
    bento_base_rgb = bento_rgba[..., :3] * bento_rgba[..., 3:4] + np.array([5 / 255.0, 5 / 255.0, 8 / 255.0], dtype=np.float32) * (1.0 - bento_rgba[..., 3:4])
    center_chrome_rgba = bento_rgba[610 : 610 + ch, 800 : 800 + cw].copy()

    # Screen coordinates for perspective mapping
    dst_quad = np.array([[0.0, 0.0], [OUT_W, 0.0], [OUT_W, OUT_H], [0.0, OUT_H]], dtype=np.float64)

    # Pre-define 9 card fan & scatter targets on 1020x788 canvas
    fan_angles = np.linspace(-52.0, 52.0, 9)
    scatter_targets = [
        (195.0, 210.0, -24.0, 0.62),
        (515.0, 165.0,   8.0, 0.64),
        (825.0, 215.0, -16.0, 0.62),
        (165.0, 455.0,  18.0, 0.63),
        (485.0, 415.0, -32.0, 0.66),
        (815.0, 455.0,  22.0, 0.64),
        (260.0, 655.0, -12.0, 0.63),
        (565.0, 650.0,  28.0, 0.65),
        (845.0, 665.0,  -8.0, 0.62),
    ]

    total_frames = 720  # 12.00s @ 60fps

    ffmpeg_cmd = [
        "ffmpeg",
        "-y",
        "-v", "error",
        "-f", "rawvideo",
        "-pix_fmt", "rgb24",
        "-s", f"{OUT_W}x{OUT_H}",
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

    print(f"Rendering {total_frames} frames ({total_frames / FPS:.2f}s) -> {out_mp4.relative_to(ROOT)} ...")
    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)
    assert proc.stdin is not None

    poster_rgb = None
    scr_y_grid, scr_x_grid = np.mgrid[0:OUT_H, 0:OUT_W].astype(np.float32)

    for f in range(total_frames):
        t = f / FPS

        # =====================================================================
        # ACT I & II (0.00s .. 6.35s): Particle Sphere -> 3D Tilted Bento Grid
        # =====================================================================
        if t < 6.35:
            pull = _ease_out_expo(_smoothstep(2.25, 3.65, t))
            bg_tint = pull  # center screen emerald backdrop fades in as we pull back
            hero = np.empty((ch, cw, 3), dtype=np.float32)
            hero[:] = np.array([5 / 255.0, 5 / 255.0, 8 / 255.0], dtype=np.float32) + screen_bg_grad * bg_tint

            # Volumetric glow inside sphere
            glow_amt = _smoothstep(0.95, 2.15, t) * (1.0 - 0.25 * _smoothstep(3.7, 4.5, t))
            if glow_amt > 0.001:
                hero += emerald_glow * glow_amt * np.array([0.08, 0.42, 0.36], dtype=np.float32)

            # Rotate 3D particle sphere
            ang_y = t * 0.55
            ang_x = 0.22 * math.sin(t * 0.7)
            cy_r, sy_r = math.cos(ang_y), math.sin(ang_y)
            cx_r, sx_r = math.cos(ang_x), math.sin(ang_x)

            x1 = base_xyz[:, 0] * cy_r + base_xyz[:, 2] * sy_r
            z1 = -base_xyz[:, 0] * sy_r + base_xyz[:, 2] * cy_r
            y2 = base_xyz[:, 1] * cx_r - z1 * sx_r
            z2 = base_xyz[:, 1] * sx_r + z1 * cx_r

            # Intro radial burst (0.0s .. 0.85s)
            burst_in = _smoothstep(0.0, 0.22, t)
            streak_phase = 1.0 - _ease_out_expo(_smoothstep(0.08, 0.92, t))
            rad_px = 268.0 * (0.52 + 0.48 * _ease_out_expo(_smoothstep(0.0, 0.75, t)))
            sphere_cy = 410.0 - 22.0 * _smoothstep(3.65, 4.45, t)

            persp = 1.0 / (2.6 - 0.55 * z2)
            px = 600.0 + x1 * rad_px * persp * 2.15
            py = sphere_cy + y2 * rad_px * persp * 2.15

            # Draw radial motion streaks during opening burst
            if streak_phase > 0.01 and burst_in > 0.01:
                for step_s in (0.76, 0.84, 0.92, 1.06):
                    sx_p = np.clip((600.0 + (px - 600.0) * step_s).astype(np.int32), 0, cw - 1)
                    sy_p = np.clip((sphere_cy + (py - sphere_cy) * step_s).astype(np.int32), 0, ch - 1)
                    val = (0.20 * streak_phase * burst_in) * (0.45 + 0.55 * (z2 + 1.0) * 0.5)
                    np.add.at(hero[..., 0], (sy_p, sx_p), val * 0.95)
                    np.add.at(hero[..., 1], (sy_p, sx_p), val * 0.98)
                    np.add.at(hero[..., 2], (sy_p, sx_p), val * 0.88)

            # Splat 2x2 crisp luminous particles
            ix_p = np.clip(px.astype(np.int32), 1, cw - 2)
            iy_p = np.clip(py.astype(np.int32), 1, ch - 2)
            depth_b = (0.30 + 0.70 * np.clip((z2 + 1.05) * 0.5, 0.0, 1.0)) * burst_in
            col_r = depth_b * (0.72 + 0.28 * pt_tint[:, 0])
            col_g = depth_b * (0.95)
            col_b = depth_b * (0.68 + 0.25 * (1.0 - pt_tint[:, 0]))

            for dy_o, dx_o, w_o in ((0, 0, 0.85), (0, 1, 0.38), (1, 0, 0.38), (1, 1, 0.18)):
                np.add.at(hero[..., 0], (iy_p + dy_o, ix_p + dx_o), col_r * w_o)
                np.add.at(hero[..., 1], (iy_p + dy_o, ix_p + dx_o), col_g * w_o)
                np.add.at(hero[..., 2], (iy_p + dy_o, ix_p + dx_o), col_b * w_o)
            np.clip(hero, 0.0, 1.0, out=hero)

            # Kinetic Headline 1 ("Veriden Doğan Cesur Fikir"): 0.65s .. 3.85s
            h1_in = _smoothstep(0.68, 1.55, t)
            h1_out = 1.0 - _smoothstep(3.45, 3.95, t)
            h1_op = h1_in * h1_out
            if h1_op > 0.005:
                # Progressive column reveal + scramble shimmer bars during decode
                reveal_x = int(cw * _ease_out_expo(_smoothstep(0.65, 1.65, t)))
                y_top = 280
                patch = hl1_rgba.copy()
                if reveal_x < cw:
                    patch[:, reveal_x:, 3] *= 0.18
                roi = hero[y_top : y_top + 260, 0:cw]
                _alpha_over(roi, patch, h1_op)

            # Kinetic Headline 2 + Isometric 4-Layer Creative Stack: 3.70s .. 6.35s
            iso_in = _ease_out_expo(_smoothstep(3.72, 4.55, t))
            if iso_in > 0.005:
                # Headline 2 in upper half of center screen
                y_h2 = int(round(145 + (1.0 - iso_in) * 24))
                roi_h2 = hero[y_h2 : y_h2 + 260, 0:cw]
                _alpha_over(roi_h2, hl2_rgba, iso_in)

                # Isometric stack + left callout rising smoothly
                shift_y = int(round((1.0 - iso_in) * 42))
                if shift_y == 0:
                    _alpha_over(hero, iso_rgba, iso_in)
                else:
                    _alpha_over(hero[shift_y:ch, :], iso_rgba[0 : ch - shift_y, :], iso_in)

            # Composite center top nav bar as pullback begins
            if pull > 0.01:
                _alpha_over(hero, center_chrome_rgba, pull)

            # Place live hero screen into 2800x2100 bento canvas & warp with 3D perspective!
            if pull <= 0.001:
                # Direct crop of center 1044x806 inside hero (zero surrounding chrome)
                crop_w = 1044.0
                crop_h = crop_w * ASPECT
                x0 = (cw - crop_w) * 0.5
                y0 = (ch - crop_h) * 0.5
                hero_pil = Image.fromarray(np.clip(hero * 255.0 + 0.5, 0, 255).astype(np.uint8), mode="RGB")
                warped = hero_pil.transform(
                    (OUT_W, OUT_H),
                    Image.Transform.AFFINE,
                    (crop_w / OUT_W, 0.0, x0, 0.0, crop_h / OUT_H, y0),
                    resample=Image.Resampling.BICUBIC,
                )
                canvas = np.array(warped, dtype=np.float32) / 255.0
            else:
                bento_frame = bento_base_rgb.copy()
                bento_frame[610 : 610 + ch, 800 : 800 + cw] = hero
                bento_pil = Image.fromarray(np.clip(bento_frame * 255.0 + 0.5, 0, 255).astype(np.uint8), mode="RGB")

                # Smoothly interpolate source quad from tight upright center -> tilted 3D wide bento view
                drift = max(0.0, t - 2.25) * 26.0
                tight_quad = np.array(
                    [
                        [878.0, 616.0],
                        [1922.0, 616.0],
                        [1922.0, 1422.0],
                        [878.0, 1422.0],
                    ],
                    dtype=np.float64,
                )
                wide_quad = np.array(
                    [
                        [390.0 + drift, 265.0],
                        [2410.0 + drift, 215.0],
                        [2545.0 + drift, 1845.0],
                        [245.0 + drift, 1895.0],
                    ],
                    dtype=np.float64,
                )
                src_quad = (1.0 - pull) * tight_quad + pull * wide_quad
                coeffs = _perspective_coeffs(dst_quad, src_quad)
                warped = bento_pil.transform((OUT_W, OUT_H), Image.Transform.PERSPECTIVE, coeffs, resample=Image.Resampling.BICUBIC)
                canvas = np.array(warped, dtype=np.float32) / 255.0
        else:
            canvas = np.zeros((OUT_H, OUT_W, 3), dtype=np.float32)

        # =====================================================================
        # ACT III (6.05s .. 8.85s): Obsidian Roasist Brand Reveal (#7601FF) + Brand Ribbon
        # =====================================================================
        if 6.05 <= t < 8.95:
            wipe_in = _ease_out_expo(_smoothstep(6.05, 6.42, t))
            brand_canvas = np.empty((OUT_H, OUT_W, 3), dtype=np.float32)
            brand_canvas[:] = np.array([9 / 255.0, 9 / 255.0, 13 / 255.0], dtype=np.float32)

            icon_op = _smoothstep(6.25, 6.55, t) * (1.0 - _smoothstep(6.88, 7.12, t))
            lock_op = _smoothstep(7.10, 7.36, t) * (1.0 - _smoothstep(7.84, 8.02, t))
            if icon_op > 0.005:
                _alpha_over(brand_canvas, brand_icon, icon_op)
            if lock_op > 0.005:
                _alpha_over(brand_canvas, brand_lockup, lock_op)

            # Dynamic Official Roasist Purple (#7601FF) X-ribbon flood (7.96s .. 8.90s)
            rib_p = _ease_out_expo(_smoothstep(7.96, 8.42, t))
            if rib_p > 0.005:
                roasist_purple = np.array([118 / 255.0, 1 / 255.0, 255 / 255.0], dtype=np.float32)
                deep_purple = np.array([86 / 255.0, 0 / 255.0, 192 / 255.0], dtype=np.float32)
                brand_canvas[:] = brand_canvas * (1.0 - rib_p) + deep_purple * rib_p
                d1 = np.abs((scr_x_grid - OUT_W * 0.48) * 0.72 + (scr_y_grid - OUT_H * 0.50) * 0.69)
                d2 = np.abs((scr_x_grid - OUT_W * 0.52) * 0.68 - (scr_y_grid - OUT_H * 0.50) * 0.73)
                band_w = 135.0 * rib_p
                x_mask = np.clip(1.0 - np.minimum(d1, d2) / max(1.0, band_w), 0.0, 1.0)[..., None]
                brand_canvas[:] = brand_canvas * (1.0 - 0.75 * x_mask) + roasist_purple * (0.75 * x_mask)

            wipe_x = int(round(OUT_W * wipe_in))
            if wipe_x >= OUT_W:
                canvas = brand_canvas
            elif wipe_x > 0:
                canvas[:, :wipe_x] = brand_canvas[:, :wipe_x]

        # =====================================================================
        # ACT IV (8.45s .. 12.00s): Warm Alabaster Wipe -> 9 Fanning & Scattering Cards
        # =====================================================================
        if t >= 8.45:
            cream_in = _ease_out_expo(_smoothstep(8.45, 8.92, t))
            cream_canvas = Image.new("RGB", (OUT_W, OUT_H), (237, 230, 218))

            fan_p = _ease_out_expo(_smoothstep(8.75, 9.85, t))
            scat_p = _ease_out_expo(_smoothstep(9.90, 11.05, t))
            drift_t = max(0.0, t - 9.90)

            if fan_p > 0.01:
                for i, card_im in enumerate(cards_pil):
                    # State A: stacked below -> fanned arc around bottom pivot (510, 900)
                    ang_fan = fan_angles[i] * fan_p
                    rad_a = math.radians(ang_fan)
                    pivot_x, pivot_y = 510.0, 930.0 - 150.0 * fan_p
                    r_arm = 320.0
                    fx = pivot_x + math.sin(rad_a) * r_arm
                    fy = pivot_y - math.cos(rad_a) * r_arm + (1.0 - fan_p) * 260.0
                    f_scale = 0.54

                    # State B: scattered editorial studio layout + gentle float
                    tx, ty, tang, tscale = scatter_targets[i]
                    tx += math.sin(drift_t * 1.4 + i) * 10.0
                    ty += math.cos(drift_t * 1.2 + i * 0.7) * 8.0
                    tang += (1.0 if i % 2 == 0 else -1.0) * drift_t * 3.5

                    cx_i = (1.0 - scat_p) * fx + scat_p * tx
                    cy_i = (1.0 - scat_p) * fy + scat_p * ty
                    ang_i = (1.0 - scat_p) * (-ang_fan) + scat_p * tang
                    sc_i = (1.0 - scat_p) * f_scale + scat_p * tscale

                    nw = int(round(card_im.width * sc_i))
                    nh = int(round(card_im.height * sc_i))
                    scaled = card_im.resize((nw, nh), Image.Resampling.BILINEAR)
                    rotated = scaled.rotate(ang_i, resample=Image.Resampling.BICUBIC, expand=True)
                    px_i = int(round(cx_i - rotated.width * 0.5))
                    py_i = int(round(cy_i - rotated.height * 0.5))
                    cream_canvas.paste(rotated, (px_i, py_i), rotated)

            cream_arr = np.array(cream_canvas, dtype=np.float32) / 255.0
            wipe_cx = int(round(OUT_W * cream_in))
            if wipe_cx >= OUT_W:
                canvas = cream_arr
            elif wipe_cx > 0:
                canvas[:, :wipe_cx] = cream_arr[:, :wipe_cx]

            # Final midnight architectural curtain wipe back to #050508 (11.30s .. 12.00s) for seamless loop!
            if t >= 11.30:
                end_wipe = _ease_out_expo(_smoothstep(11.30, 11.96, t))
                end_x = int(round(OUT_W * end_wipe))
                dark_col = np.array([5 / 255.0, 5 / 255.0, 8 / 255.0], dtype=np.float32)
                if end_x >= OUT_W:
                    canvas[:] = dark_col
                elif end_x > 0:
                    canvas[:, :end_x] = dark_col

        rgb_bytes = np.clip(canvas * 255.0 + 0.5, 0, 255).astype(np.uint8)
        if f == 276:  # t = 4.60s: rich tilted 3D bento grid + particle sphere + isometric creative stack!
            poster_rgb = rgb_bytes.copy()
        proc.stdin.write(rgb_bytes.tobytes())

    proc.stdin.close()
    rc = proc.wait()
    if rc != 0:
        raise RuntimeError(f"ffmpeg exited with status {rc}")

    if poster_rgb is not None:
        Image.fromarray(poster_rgb, mode="RGB").save(out_jpg, quality=92, optimize=True)

    size_mb = out_mp4.stat().st_size / (1024 * 1024)
    print(f"Done! {out_mp4.relative_to(ROOT)} ({size_mb:.2f} MB), poster: {out_jpg.relative_to(ROOT)}")


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "01"
    if target in ("all", "01", "01-veri-ve-strateji"):
        build_01_veri_ve_strateji()
    if target in ("all", "02", "02-yaratici-ve-cesur-fikir"):
        build_02_yaratici_ve_cesur_fikir()

