#!/usr/bin/env python3
"""
Roasist Web — 7-Point Core Web Vitals & Payload Optimization Pipeline:
  1. Removes unreferenced orphan media files in `public/images/` (~41 MB).
  2. Replaces unused 1.90 MB Spline 3D runtime chunk (`c6a54c64-52e4c013414e73d2.js`)
     with a valid 229-byte Webpack `[210]` (`63598`) module stub.
  3. Converts heavy PNG visuals (`case-studies/*-visual.png`, large client PNGs) to WebP,
     updates `app/(home)/page` JS (`lazy:!1` -> `lazy:!0`), and enables `loading="lazy" decoding="async"`.
  4. Compresses active `.mp4` videos via FFmpeg (`H.264 CRF 27`, `-an`, `+faststart`, `<=960w`)
     and defers `.ProjectCard_video__AheFz` playback to `IntersectionObserver` (`data-src`, no eager `autoPlay`).
  5. Removes low-priority `<link rel="preload" as="image">` tags and consolidates per-page
     Next.js CSS stylesheets (`10-11` requests -> `1` content-hashed bundle) Flight-safely.
  6. Removes external Google Fonts `<link>` tags from `public/*-3d.html`.
  7. Throttles Homepage 3D canvas `ensureCanvasesMounted()` layout reads (`getBoundingClientRect`)
     and halts rendering when offscreen or `document.hidden`.
"""
import glob
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
PUBLIC_DIR = os.path.join(REPO_ROOT, "public")
sys.path.insert(0, SCRIPT_DIR)

from update_about_page import parse_flight_stream, serialize_flight_stream
from update_tiktok_yandex_pages import extract_flight_chunks

LAZY_VIDEO_SCRIPT_ID = "roasist-lazy-video"
LAZY_VIDEO_SCRIPT = f"""<script id="{LAZY_VIDEO_SCRIPT_ID}">
(function() {{
  function ensureInlineAttrs(v) {{
    if (!v) return;
    v.muted = true;
    v.defaultMuted = true;
    v.playsInline = true;
    v.loop = true;
    v.setAttribute('muted', '');
    v.setAttribute('playsinline', '');
    v.setAttribute('webkit-playsinline', '');
  }}

  function primeAndPlay(v) {{
    if (!v) return;
    ensureInlineAttrs(v);
    var ds = v.getAttribute('data-src');
    if (ds && !v.getAttribute('src')) {{
      v.setAttribute('src', ds);
      try {{ v.load(); }} catch (e) {{}}
    }}
    if (v.getAttribute('src')) {{
      var p = v.play();
      if (p && typeof p.catch === 'function') p.catch(function() {{}});
    }}
  }}

  function initHeroVideos() {{
    document.querySelectorAll('video[class*="Hero_video__"]').forEach(function(v) {{
      if (window.getComputedStyle && window.getComputedStyle(v).display === 'none') return;
      primeAndPlay(v);
    }});
  }}

  var SELECTOR = 'video.ProjectCard_video__AheFz[data-src], .ServiceMedia_mediaContainer__WGgZa video[data-src]';

  if (!('IntersectionObserver' in window)) {{
    initHeroVideos();
    document.querySelectorAll(SELECTOR).forEach(primeAndPlay);
    return;
  }}

  var visibleSet = new Set();
  var io = new IntersectionObserver(function(entries) {{
    entries.forEach(function(entry) {{
      var v = entry.target;
      if (entry.isIntersecting) {{
        visibleSet.add(v);
        primeAndPlay(v);
      }} else {{
        visibleSet.delete(v);
        if (v.getAttribute('src') && !v.paused) {{
          try {{ v.pause(); }} catch (e) {{}}
        }}
      }}
    }});
  }}, {{ rootMargin: '320px 0px', threshold: 0.01 }});

  function observeVideos(root) {{
    initHeroVideos();
    (root || document).querySelectorAll(SELECTOR).forEach(function(v) {{
      if (!v.dataset.roasistObserved) {{
        v.dataset.roasistObserved = '1';
        io.observe(v);
      }}
    }});
  }}

  function resumeVisible() {{
    visibleSet.forEach(function(v) {{
      if (v.paused) primeAndPlay(v);
    }});
    document.querySelectorAll('.ServiceMedia_mediaContainer__WGgZa video, .AutoplayVideo_video__zckWy video, video[class*="Hero_video__"]').forEach(function(v) {{
      if (window.getComputedStyle && window.getComputedStyle(v).display === 'none') return;
      if ((v.getAttribute('src') || v.getAttribute('data-src')) && v.paused) {{
        primeAndPlay(v);
      }}
    }});
  }}
  window.addEventListener('touchstart', resumeVisible, {{ passive: true, once: false }});

  if (document.readyState === 'loading') {{
    document.addEventListener('DOMContentLoaded', function() {{ observeVideos(document); }});
  }} else {{
    observeVideos(document);
  }}

  if ('MutationObserver' in window && document.body) {{
    var mo = new MutationObserver(function(muts) {{
      for (var i = 0; i < muts.length; i++) {{
        if (muts[i].addedNodes && muts[i].addedNodes.length) {{
          observeVideos(document);
          break;
        }}
      }}
    }});
    mo.observe(document.body, {{ childList: true, subtree: true }});
  }}
}})();
</script>"""


def step1_clean_orphan_media():
    code_blob = []
    for ext in ("*.html", "*.css", "*.js", "*.xml"):
        for fp in glob.glob(os.path.join(PUBLIC_DIR, "**", ext), recursive=True):
            code_blob.append(open(fp, "r", encoding="utf-8", errors="ignore").read())
    joined = "\n".join(code_blob)

    removed_count = 0
    removed_bytes = 0
    for root, _, files in os.walk(os.path.join(PUBLIC_DIR, "images")):
        for fname in files:
            fp = os.path.join(root, fname)
            if fname not in joined:
                removed_bytes += os.path.getsize(fp)
                os.remove(fp)
                removed_count += 1

    # Clean empty directories inside public/images
    for root, dirs, files in os.walk(os.path.join(PUBLIC_DIR, "images"), topdown=False):
        if not os.listdir(root):
            os.rmdir(root)

    print(f"[1/7] Removed {removed_count} unreferenced media files ({removed_bytes / 1024 / 1024:.2f} MB)")


def step2_stub_spline_chunk():
    spline_chunk = os.path.join(PUBLIC_DIR, "_next", "static", "chunks", "c6a54c64-52e4c013414e73d2.js")
    if not os.path.exists(spline_chunk):
        return
    before_kb = os.path.getsize(spline_chunk) / 1024
    stub = (
        '"use strict";(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[210],'
        "{63598:function(e,t,i){class M{load(){return Promise.resolve()}addEventListener(){}"
        "removeEventListener(){}dispose(){}}i.d(t,{M:function(){return M}})}}]);\n"
    )
    open(spline_chunk, "w", encoding="utf-8").write(stub)
    after_kb = os.path.getsize(spline_chunk) / 1024
    print(f"[2/7] Replaced Spline chunk c6a54c64: {before_kb:.1f} KB -> {after_kb:.2f} KB")


def step3_convert_heavy_pngs_to_webp() -> list:
    targets = sorted(glob.glob(os.path.join(PUBLIC_DIR, "images", "case-studies", "*-visual.png")))
    for extra in ("images/clients/livaneli.png", "images/clients/bbg-call-center.png"):
        p = os.path.join(PUBLIC_DIR, extra)
        if os.path.exists(p):
            targets.append(p)

    replacements = []
    before_total = 0
    after_total = 0

    for png_path in targets:
        webp_path = os.path.splitext(png_path)[0] + ".webp"
        before_sz = os.path.getsize(png_path)
        subprocess.run(
            [
                "ffmpeg", "-y", "-loglevel", "error",
                "-i", png_path,
                "-c:v", "libwebp", "-quality", "82", "-compression_level", "6",
                webp_path,
            ],
            check=True,
        )
        after_sz = os.path.getsize(webp_path)
        before_total += before_sz
        after_total += after_sz
        os.remove(png_path)

        rel_png = "/" + os.path.relpath(png_path, PUBLIC_DIR).replace(os.sep, "/")
        rel_webp = "/" + os.path.relpath(webp_path, PUBLIC_DIR).replace(os.sep, "/")
        replacements.append((rel_png, rel_webp))

    # Enable lazy loading on StatisticsPanel brandVisual in Homepage JS chunk
    home_js = os.path.join(PUBLIC_DIR, "_next", "static", "chunks", "app", "(home)", "page-b58f77e3dc47742c.js")
    if os.path.exists(home_js):
        s = open(home_js, "r", encoding="utf-8").read()
        s2 = s.replace('brandVisual,layout:"intrinsic",lazy:!1', 'brandVisual,layout:"intrinsic",lazy:!0')
        if s2 != s:
            open(home_js, "w", encoding="utf-8").write(s2)

    # Keep sync_performans_statistics_cards.py in sync
    sync_py = os.path.join(SCRIPT_DIR, "sync_performans_statistics_cards.py")
    if os.path.exists(sync_py):
        sp = open(sync_py, "r", encoding="utf-8").read()
        for old_u, new_u in replacements:
            sp = sp.replace(old_u, new_u)
        open(sync_py, "w", encoding="utf-8").write(sp)

    print(
        f"[3/7] Converted {len(replacements)} heavy PNGs to WebP: "
        f"{before_total / 1024:.1f} KB -> {after_total / 1024:.1f} KB"
    )
    return replacements


def step4_compress_mp4s_and_patch_js():
    mp4s = sorted(glob.glob(os.path.join(PUBLIC_DIR, "images", "**", "*.mp4"), recursive=True))
    before_tot = 0
    after_tot = 0
    compressed = 0

    for mp4 in mp4s:
        orig_sz = os.path.getsize(mp4)
        before_tot += orig_sz
        tmp_out = mp4 + ".opt.mp4"
        res = subprocess.run(
            [
                "ffmpeg", "-y", "-loglevel", "error",
                "-i", mp4,
                "-an",
                "-c:v", "libx264", "-preset", "medium", "-crf", "27",
                "-pix_fmt", "yuv420p",
                "-movflags", "+faststart",
                "-vf", "scale='min(960,iw)':-2",
                tmp_out,
            ]
        )
        if res.returncode == 0 and os.path.exists(tmp_out):
            new_sz = os.path.getsize(tmp_out)
            if new_sz < orig_sz * 0.92:
                os.replace(tmp_out, mp4)
                after_tot += new_sz
                compressed += 1
            else:
                os.remove(tmp_out)
                after_tot += orig_sz
        else:
            if os.path.exists(tmp_out):
                os.remove(tmp_out)
            after_tot += orig_sz

    # Patch client-side ProjectCard video JSX in 2827 & work/page chunks so React matches SSR data-src
    for rel_js in (
        "_next/static/chunks/2827-f8fce45e8c1f0443.js",
        "_next/static/chunks/app/work/page-5b3919766e28ce0e.js",
    ):
        jp = os.path.join(PUBLIC_DIR, rel_js)
        if not os.path.exists(jp):
            continue
        js = open(jp, "r", encoding="utf-8").read()
        js2 = re.sub(
            r'\("video",\{src:([^}]+?)\|\|"",className:([a-zA-Z0-9_$]+\(\)\.video),autoPlay:!0,muted:!0,loop:!0,preload:"none",playsInline:!0\}\)',
            r'("video",{"data-src":\1||"",className:\2,muted:!0,loop:!0,preload:"none",playsInline:!0})',
            js,
        )
        if js2 != js:
            open(jp, "w", encoding="utf-8").write(js2)

    print(
        f"[4/7] Compressed {compressed}/{len(mp4s)} active MP4 videos: "
        f"{before_tot / 1024 / 1024:.2f} MB -> {after_tot / 1024 / 1024:.2f} MB"
    )


CSS_LINK_TAG_RE = re.compile(
    r'<link rel="stylesheet" href="(/_next/static/css/(?!roasist-bundle-)[^"]+\.css)" data-precedence="next"/>'
)
IMAGE_PRELOAD_RE = re.compile(r'<link rel="preload" as="image" href="[^"]+"/>')
SSR_PROJECT_VIDEO_RE = re.compile(
    r'<video src="([^"]+)" class="ProjectCard_video__AheFz" autoPlay="" muted="" loop="" preload="none" playsInline=""></video>'
)
FLIGHT_PROJECT_VIDEO_RE = re.compile(
    r'"src":"([^"]+)","className":"ProjectCard_video__AheFz","autoPlay":true,"muted":true,"loop":true,"preload":"none","playsInline":true'
)
FLIGHT_CSS_LINK_ITEM_RE = re.compile(
    r'\["\$","link","\d+",\{"rel":"stylesheet","href":"/_next/static/css/[^"]+\.css","precedence":"next","crossOrigin":"\$undefined"\}\]'
)


def build_css_bundle(css_hrefs: list, cache: dict) -> str:
    key = tuple(css_hrefs)
    if key in cache:
        return cache[key]
    parts = []
    for href in css_hrefs:
        fp = os.path.join(PUBLIC_DIR, href.lstrip("/"))
        if os.path.exists(fp):
            parts.append(f"/* {os.path.basename(fp)} */\n" + open(fp, "r", encoding="utf-8").read())
    combined = "\n".join(parts)
    digest = hashlib.sha256(combined.encode("utf-8")).hexdigest()[:12]
    bundle_rel = f"/_next/static/css/roasist-bundle-{digest}.css"
    bundle_abs = os.path.join(PUBLIC_DIR, bundle_rel.lstrip("/"))
    open(bundle_abs, "w", encoding="utf-8").write(combined)
    cache[key] = bundle_rel
    return bundle_rel


def transform_non_flight_html(seg: str, webp_reps: list, bundle_href: str | None) -> str:
    for old_u, new_u in webp_reps:
        seg = seg.replace(old_u, new_u)

    # Remove low-priority <link rel="preload" as="image"> tags
    seg = IMAGE_PRELOAD_RE.sub("", seg)

    # Consolidate <link rel="stylesheet" ... data-precedence="next"/> into 1 bundle link
    if bundle_href:
        first_done = False

        def _css_repl(_m):
            nonlocal first_done
            if not first_done:
                first_done = True
                return f'<link rel="stylesheet" href="{bundle_href}" data-precedence="next"/>'
            return ""

        seg = CSS_LINK_TAG_RE.sub(_css_repl, seg)

    # Defer ProjectCard_video__AheFz
    seg = SSR_PROJECT_VIDEO_RE.sub(
        r'<video data-src="\1" class="ProjectCard_video__AheFz" muted="" loop="" preload="none" playsInline=""></video>',
        seg,
    )

    # Make case-study *-visual.webp images lazy-loaded
    seg = re.sub(
        r'(<img\b[^>]*case-studies/[a-z0-9-]+-visual\.webp[^>]*)\bloading="eager"',
        r'\1loading="lazy" decoding="async"',
        seg,
    )
    return seg


def transform_flight_record(val: str, webp_reps: list, bundle_href: str | None) -> str:
    for old_u, new_u in webp_reps:
        val = val.replace(old_u, new_u)

    val = FLIGHT_PROJECT_VIDEO_RE.sub(
        r'"data-src":"\1","className":"ProjectCard_video__AheFz","muted":true,"loop":true,"preload":"none","playsInline":true',
        val,
    )

    if bundle_href:
        if val.startswith('HL["/_next/static/css/') and val.endswith('","style"]'):
            val = f'HL["{bundle_href}","style"]'
        elif '"rel":"stylesheet","href":"/_next/static/css/' in val:
            # Replace each array of stylesheet links: keep 1 link in the last (root layout) array and empty earlier segment arrays
            array_re = re.compile(
                r'\[(?:\["\$","link","\d+",\{"rel":"stylesheet","href":"/_next/static/css/[^"]+\.css","precedence":"next","crossOrigin":"\$undefined"\}\],?)+\]'
            )
            matches = list(array_re.finditer(val))
            if matches:
                out = []
                last = 0
                single_item = (
                    f'[["$","link","0",{{"rel":"stylesheet","href":"{bundle_href}",'
                    f'"precedence":"next","crossOrigin":"$undefined"}}]]'
                )
                for idx, m in enumerate(matches):
                    out.append(val[last : m.start()])
                    out.append(single_item if idx == len(matches) - 1 else "[]")
                    last = m.end()
                out.append(val[last:])
                val = "".join(out)
    return val


def step5_optimize_all_html_pages(webp_reps: list):
    bundle_cache = {}
    updated_pages = 0

    for fp in sorted(glob.glob(os.path.join(PUBLIC_DIR, "**", "*.html"), recursive=True)):
        rel = os.path.relpath(fp, PUBLIC_DIR)
        if rel.endswith("-3d.html") or rel == "404.html":
            continue

        orig = open(fp, "r", encoding="utf-8").read()
        css_hrefs = CSS_LINK_TAG_RE.findall(orig)
        bundle_href = build_css_bundle(css_hrefs, bundle_cache) if len(css_hrefs) > 1 else None

        matches, _, full = extract_flight_chunks(orig)
        if matches:
            recs = parse_flight_stream(full)
            for rec in recs:
                rec[2] = transform_flight_record(rec[2], webp_reps, bundle_href)
            new_full = serialize_flight_stream(recs)

            parts = []
            last_end = 0
            for idx, m in enumerate(matches):
                parts.append(transform_non_flight_html(orig[last_end : m.start()], webp_reps, bundle_href))
                if idx == 0:
                    encoded = json.dumps(new_full, ensure_ascii=False)[1:-1].replace("</", "\\u003c/")
                    parts.append(m.group(1) + encoded + m.group(3))
                else:
                    parts.append("")
                last_end = m.end()
            parts.append(transform_non_flight_html(orig[last_end:], webp_reps, bundle_href))
            upd = "".join(parts)
        else:
            upd = transform_non_flight_html(orig, webp_reps, bundle_href)

        # Inject IntersectionObserver lazy-video helper on pages with ProjectCard videos or work grid
        needs_video_io = (
            "ProjectCard_video__AheFz" in upd
            or "referanslar" in rel
            or "references" in rel
        )
        if needs_video_io:
            script_re = re.compile(rf'<script id="{LAZY_VIDEO_SCRIPT_ID}">.*?</script>', re.S)
            if script_re.search(upd):
                upd = script_re.sub(lambda _: LAZY_VIDEO_SCRIPT, upd, count=1)
            else:
                body_end = upd.rfind("</body>")
                if body_end != -1:
                    upd = upd[:body_end] + LAZY_VIDEO_SCRIPT + upd[body_end:]

        if upd != orig:
            # Verify Flight stream still parses cleanly
            m_chk, _, f_chk = extract_flight_chunks(upd)
            if m_chk:
                parse_flight_stream(f_chk)
            open(fp, "w", encoding="utf-8").write(upd)
            updated_pages += 1

    print(
        f"[5/7] Optimized {updated_pages} HTML pages "
        f"(consolidated CSS into {len(bundle_cache)} unique bundles, stripped image preloads, deferred videos)"
    )


def step6_strip_google_fonts_from_3d_html():
    count = 0
    for fp in sorted(glob.glob(os.path.join(PUBLIC_DIR, "*-3d.html"))):
        orig = open(fp, "r", encoding="utf-8").read()
        upd = re.sub(r'\s*<link[^>]+fonts\.g(?:oogleapis|static)\.com[^>]*>', "", orig)
        if upd != orig:
            open(fp, "w", encoding="utf-8").write(upd)
            count += 1
    print(f"[6/7] Removed external Google Fonts links from {count} methodology 3D HTML files")


def step7_throttle_homepage_canvas_loop():
    target_old = """  function tick(now) {
    requestAnimationFrame(tick);
    try {
      ensureCanvasesMounted();
    } catch {}

    if (isCarouselVisible && !document.hidden) {"""

    target_new = """  let lastMountCheck = -1000;
  function tick(now) {
    requestAnimationFrame(tick);
    if (document.hidden) return;
    if (!observerAttached || (isCarouselVisible && (now - lastMountCheck > 600))) {
      lastMountCheck = now;
      try {
        ensureCanvasesMounted();
      } catch {}
    }

    if (isCarouselVisible) {"""

    updated = 0
    for rel in ("public/kota-roasist-local.html", "public/en/index.html", "scripts/inject_homepage_kinetic_3d.py"):
        fp = os.path.join(REPO_ROOT, rel)
        if not os.path.exists(fp):
            continue
        s = open(fp, "r", encoding="utf-8").read()
        if target_old in s:
            open(fp, "w", encoding="utf-8").write(s.replace(target_old, target_new, 1))
            updated += 1
    print(f"[7/7] Throttled 60fps DOM/layout reads & added hidden-tab pause in {updated} files")


def main():
    step1_clean_orphan_media()
    step2_stub_spline_chunk()
    webp_reps = step3_convert_heavy_pngs_to_webp()
    step4_compress_mp4s_and_patch_js()
    step5_optimize_all_html_pages(webp_reps)
    step6_strip_google_fonts_from_3d_html()
    step7_throttle_homepage_canvas_loop()


if __name__ == "__main__":
    main()
