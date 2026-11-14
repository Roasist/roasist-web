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


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "01"
    if target in ("all", "01", "01-veri-ve-strateji"):
        build_01_veri_ve_strateji()
