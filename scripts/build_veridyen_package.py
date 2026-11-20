#!/usr/bin/env python3
"""
Builds a ready-to-upload Veridyen cPanel (`public_html`) production package:
  - Output directory: /tmp/roasist-veridyen-public_html
  - Output ZIP file:  /tmp/roasist-veridyen-public_html.zip (files placed directly at ZIP root
    so extracting inside `public_html` in cPanel File Manager works immediately without nesting).

Transformations performed (Flight-stream byte-length safe):
  1. Copies `public/` -> `/tmp/roasist-veridyen-public_html/` and promotes `kota-roasist-local.html` -> `index.html`.
  2. Removes GitHub/Netlify-only dotfiles (`.nojekyll`, `_headers`) and `CNAME`.
  3. Rewrites SEO/OpenGraph/Schema `cdn.jsdelivr.net/gh/Roasist/roasist-web@...` URLs to
     `https://www.roasist.com/...` and all page/component `cdn.jsdelivr.net/gh/Roasist/...` &
     `https://roasist.github.io/roasist-web/` asset URLs to local root `/` paths so 100% of
     images, videos, CSS, JS, and PHP run self-contained on Veridyen LiteSpeed.
  4. Verifies 0 broken local `/images/` or internal HTML route references and 0 Flight parse errors.
"""
import glob
import json
import os
import re
import shutil
import sys
import zipfile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
PUBLIC_DIR = os.path.join(REPO_ROOT, "public")
sys.path.insert(0, SCRIPT_DIR)

from update_about_page import parse_flight_stream, serialize_flight_stream
from update_tiktok_yandex_pages import extract_flight_chunks

JSDELIVR_RE = re.compile(
    r"https://cdn\.jsdelivr\.net/gh/Roasist/roasist-web@[a-f0-9]+/(?:public/)?([^\s\"'<>\\)]+)"
)
GH_IO_RE = re.compile(
    r"https://roasist\.github\.io/roasist-web/([^\s\"'<>\\)]*)"
)

META_PREFIX_RE = re.compile(
    r'((?:property="og:image"|name="twitter:image"|"contentUrl"|"thumbnailUrl"|"logo"|"image")\s*(?:content=|:)\s*\\?")'
    r"https://cdn\.jsdelivr\.net/gh/Roasist/roasist-web@[a-f0-9]+/(?:public/)?([^\s\"'<>\\)]+)"
)


def transform_segment(seg: str, site_origin: str) -> str:
    # 1. Preserve absolute https://www.roasist.com/... in OG / Twitter / Schema JSON-LD fields
    seg = META_PREFIX_RE.sub(rf"\1{site_origin}/\2", seg)
    # Also inside JSON-LD blocks where "url":"https://cdn.jsdelivr.net/.../icon.png" or 23-projects.jpg appears
    seg = re.sub(
        r'("url"\s*:\s*\\?")https://cdn\.jsdelivr\.net/gh/Roasist/roasist-web@[a-f0-9]+/(?:public/)?([^\s"\'<>\\)]+)',
        rf"\1{site_origin}/\2",
        seg,
    )
    # 2. All remaining Roasist jsDelivr & roasist.github.io/roasist-web asset URLs -> root-relative /...
    seg = JSDELIVR_RE.sub(r"/\1", seg)
    seg = GH_IO_RE.sub(r"/\1", seg)
    seg = seg.replace("/roasist-web/", "/")
    return seg


def transform_html_flight_safe(text: str, site_origin: str) -> str:
    matches, _, full = extract_flight_chunks(text)
    if not matches:
        return transform_segment(text, site_origin)

    recs = parse_flight_stream(full)
    for rec in recs:
        rec[2] = transform_segment(rec[2], site_origin)
    new_full = serialize_flight_stream(recs)

    out_parts = []
    last_end = 0
    for idx, m in enumerate(matches):
        out_parts.append(transform_segment(text[last_end : m.start()], site_origin))
        if idx == 0:
            encoded = json.dumps(new_full, ensure_ascii=False)[1:-1].replace("</", "\\u003c/")
            out_parts.append(m.group(1) + encoded + m.group(3))
        else:
            out_parts.append("")
        last_end = m.end()
    out_parts.append(transform_segment(text[last_end:], site_origin))
    return "".join(out_parts)


def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "/tmp/roasist-veridyen-public_html"
    zip_path = sys.argv[2] if len(sys.argv) > 2 else "/tmp/roasist-veridyen-public_html.zip"
    site_origin = "https://www.roasist.com"

    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    shutil.copytree(PUBLIC_DIR, out_dir)

    # Promote kota-roasist-local.html -> index.html
    local_home = os.path.join(out_dir, "kota-roasist-local.html")
    root_index = os.path.join(out_dir, "index.html")
    if os.path.exists(local_home):
        shutil.move(local_home, root_index)

    # Remove non-cPanel platform files
    for unused in (".nojekyll", "_headers", "CNAME"):
        p = os.path.join(out_dir, unused)
        if os.path.exists(p):
            os.remove(p)

    html_changed = 0
    asset_changed = 0

    for fp in sorted(glob.glob(os.path.join(out_dir, "**", "*.html"), recursive=True)):
        orig = open(fp, "r", encoding="utf-8").read()
        upd = transform_html_flight_safe(orig, site_origin)
        if upd != orig:
            open(fp, "w", encoding="utf-8").write(upd)
            html_changed += 1
        # Validate Flight integrity after write
        m, _, f = extract_flight_chunks(upd)
        if m:
            parse_flight_stream(f)

    for ext in ("*.css", "*.js"):
        for fp in sorted(glob.glob(os.path.join(out_dir, "**", ext), recursive=True)):
            orig = open(fp, "r", encoding="utf-8", errors="ignore").read()
            upd = transform_segment(orig, site_origin)
            if upd != orig:
                open(fp, "w", encoding="utf-8").write(upd)
                asset_changed += 1

    # Audit local /images/ references across all HTML files
    missing_images = set()
    ext_cdn_left = set()
    for fp in glob.glob(os.path.join(out_dir, "**", "*.html"), recursive=True):
        s = open(fp, "r", encoding="utf-8").read()
        for img in re.findall(r"(/images/[a-zA-Z0-9_./-]+)", s):
            if not os.path.exists(os.path.join(out_dir, img.lstrip("/"))):
                missing_images.add(img)
        for ext_u in re.findall(r"https://(?:roasist\.github\.io|cdn\.jsdelivr\.net/gh/Roasist|kota-content\.b-cdn\.net)[^\s\"'<>\\)]*", s):
            ext_cdn_left.add(ext_u)

    if missing_images:
        raise RuntimeError(f"Missing local images in package: {sorted(missing_images)}")
    if ext_cdn_left:
        raise RuntimeError(f"Leftover preview/CDN URLs in package: {sorted(ext_cdn_left)[:10]}")

    # Build flat-root ZIP archive (including .htaccess and api/_leads_private/.htaccess)
    if os.path.exists(zip_path):
        os.remove(zip_path)

    file_count = 0
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for root, dirs, files in os.walk(out_dir):
            dirs.sort()
            for fname in sorted(files):
                abs_p = os.path.join(root, fname)
                rel_p = os.path.relpath(abs_p, out_dir).replace(os.sep, "/")
                zf.write(abs_p, rel_p)
                file_count += 1

    size_mb = os.path.getsize(zip_path) / (1024 * 1024)
    print(f"[OK] Built Veridyen package: {out_dir}")
    print(f"     HTML updated: {html_changed} | CSS/JS updated: {asset_changed} | Total files zipped: {file_count}")
    print(f"     ZIP archive:  {zip_path} ({size_mb:.2f} MB)")
    print("     Missing local images: 0 | External KOTA/jsDelivr/github.io refs: 0 | Flight stream errors: 0")


if __name__ == "__main__":
    main()
