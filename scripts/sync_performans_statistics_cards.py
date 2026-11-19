#!/usr/bin/env python3
"""
Syncs the 5 case-study cards from the Homepage's 'ÖLÇÜLEBİLİR SONUÇLAR' / 'MEASURABLE RESULTS'
section into the Performance Marketing page's 'Estetik Tasarım. Ölçülebilir Büyüme.' /
'Strategic Craft. Measurable Growth.' section (both TR and EN, in both public/ and dist/).

Updates:
  1. React Flight stream `statistics` prop (for Next.js client hydration).
  2. SSR HTML inside `.StatisticsCarousel_swiper__PLGJ6 .swiper-wrapper` (zero hydration mismatch).
  3. Idempotent `<style id="roasist-perf-stats-cards">` in `<head>` to match the Homepage's
     dark violet-bordered card design, un-inverted white client logos, rainbow stat typography,
     white description copy, and white outline CTA button.
"""
import html as html_lib
import json
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

from update_about_page import parse_flight_stream, serialize_flight_stream

STYLE_ID = "roasist-perf-stats-cards"

DARK_STATS_CSS = f"""<style id="{STYLE_ID}">
/* Match Homepage 'ÖLÇÜLEBİLİR SONUÇLAR' dark cards inside Performance Marketing page */
.StatisticsPanel_panel__C_sZ2 {{
  background: #050508 !important;
  border: 2px solid rgba(118, 2, 255, 0.45) !important;
  box-shadow: 0 24px 64px -18px rgba(118, 2, 255, 0.25) !important;
  color: #ffffff !important;
}}
.StatisticsPanel_backgroundImage__o9T5M {{
  opacity: 1 !important;
}}
.StatisticsPanel_panelWrap__iNrBj {{
  position: relative;
  z-index: 2;
}}
.StatisticsPanel_visual__crBRi,
.StatisticsPanel_visualMobile__4w9EW {{
  position: relative;
  z-index: 2;
}}
.StatisticsPanel_logo__pnjFD img {{
  filter: none !important;
  height: 68px !important;
  width: auto !important;
  max-width: 210px !important;
  object-fit: contain !important;
  margin-bottom: 1.5rem !important;
}}
@media screen and (min-width: 1024px) {{
  .StatisticsPanel_logo__pnjFD img {{
    margin-bottom: 2.25rem !important;
  }}
}}
.StatisticsPanel_heading__Xqlyh {{
  background-image: linear-gradient(90deg, #7602FF, #00D2FF, #EC4899, #7602FF) !important;
  background-size: 200% 200% !important;
  -webkit-background-clip: text !important;
  background-clip: text !important;
  color: transparent !important;
  font-variant-numeric: tabular-nums !important;
  margin-bottom: 0.75rem !important;
}}
.StatisticsPanel_description__NM4c_ {{
  color: rgba(248, 250, 252, 0.92) !important;
  font-size: clamp(1.15rem, 1.5vw, 1.5rem) !important;
  line-height: 1.42 !important;
  margin-bottom: 2rem !important;
  max-width: 36ch !important;
}}
@media screen and (min-width: 1024px) {{
  .StatisticsPanel_description__NM4c_ {{
    margin-bottom: 2.5rem !important;
  }}
}}
.StatisticsPanel_buttons__IavWc .Button_button__JJiqJ {{
  border-color: #ffffff !important;
}}
.StatisticsPanel_buttons__IavWc .Button_button__JJiqJ .Button_inner__fnyH6,
.StatisticsPanel_buttons__IavWc .Button_button__JJiqJ svg {{
  color: #ffffff !important;
}}
.StatisticsPanel_buttons__IavWc .Button_button__JJiqJ .Button_border__hirH2 {{
  border-color: #ffffff !important;
}}
.StatisticsCarousel_swiperNavNext__OgPJn {{
  border-color: #ffffff !important;
}}
.StatisticsCarousel_swiperNavNext__OgPJn::before {{
  color: #ffffff !important;
}}
</style>"""

ARROW_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 17.1 15.17" '
    'class="Button_buttonArrow__0W9XI"><path d="m17.1,7.58s-.01-.04-.01-.06c.01-.22-.06-.45-.24-.61'
    'L9.23.19c-.31-.27-.78-.24-1.06.07-.27.31-.24.78.07,1.06l6.26,5.52H.75c-.41,0-.75.34-.75.75'
    's.34.75.75.75h13.74l-6.26,5.52c-.31.27-.34.75-.07,1.06.15.17.35.25.56.25.18,0,.35-.06.5-.19'
    'l7.62-6.72c.18-.16.25-.39.24-.61,0-.02.01-.04.01-.06Z" fill="currentColor"></path></svg>'
)


def extract_flight_chunks(html_text):
    pattern = re.compile(r'(<script>self\.__next_f\.push\(\[1,")((?:\\.|[^"\\])*)("\]\)</script>)')
    matches = list(pattern.finditer(html_text))
    decoded_parts = [json.loads('"' + m.group(2) + '"') for m in matches]
    return matches, decoded_parts, "".join(decoded_parts)


def find_statistics_list(obj):
    if isinstance(obj, dict):
        if "statistics" in obj and isinstance(obj["statistics"], list):
            return obj
        for v in obj.values():
            res = find_statistics_list(v)
            if res is not None:
                return res
    elif isinstance(obj, list):
        for v in obj:
            res = find_statistics_list(v)
            if res is not None:
                return res
    return None


def get_homepage_statistics(home_path):
    text = open(home_path, "r", encoding="utf-8").read()
    _, _, full = extract_flight_chunks(text)
    recs = parse_flight_stream(full)
    for rec in recs:
        if rec[0] != "line":
            continue
        payload = rec[2]
        if not payload or payload[0] not in "[{":
            continue
        try:
            obj = json.loads(payload)
        except Exception:
            continue
        holder = find_statistics_list(obj)
        if holder is not None:
            return holder["statistics"]
    raise RuntimeError(f"Could not find statistics array in {home_path}")


def render_ssr_slide(item, url_prefix=""):
    esc = lambda s: html_lib.escape(str(s or ""), quote=True)
    bg = item["backgroundImage"]
    logo = item["brandLogo"]
    vis = item["brandVisual"]
    btn = item["button"]

    bg_src = esc(bg.get("sourceUrl", ""))
    bg_srcset = esc(bg.get("srcSet") or "")
    bg_w = esc(bg.get("mediaDetails", {}).get("width", ""))
    bg_h = esc(bg.get("mediaDetails", {}).get("height", ""))

    logo_src = esc(logo.get("sourceUrl", ""))
    logo_alt = esc(logo.get("altText", ""))
    logo_w = esc(logo.get("mediaDetails", {}).get("width", ""))
    logo_h = esc(logo.get("mediaDetails", {}).get("height", ""))

    vis_src = esc(vis.get("sourceUrl", ""))
    vis_srcset = esc(vis.get("srcSet") or "")
    vis_alt = esc(vis.get("altText", ""))
    vis_w = esc(vis.get("mediaDetails", {}).get("width", ""))
    vis_h = esc(vis.get("mediaDetails", {}).get("height", ""))

    stat = esc(item.get("mainStatistic", ""))
    desc = esc(item.get("description", ""))
    btn_title = esc(btn.get("title", ""))
    btn_url = btn.get("url", "/")
    if url_prefix and btn_url.startswith("/") and not btn_url.startswith(url_prefix):
        btn_url = url_prefix + btn_url
    btn_url = esc(btn_url)

    return (
        '<div class="StatisticsCarousel_swiperSlide__4gGXN swiper-slide">'
        '<div class="StatisticsPanel_panel__C_sZ2 statisticPanel">'
        '<figure class="StatisticsPanel_backgroundImage__o9T5M">'
        '<span class="Image_image__RAAdZ Image_fill__EiIzS">'
        f'<img data-srcset="{bg_srcset}" data-src="{bg_src}" src="{bg_src}" alt="" fetchPriority="low" '
        f'height="{bg_h}" width="{bg_w}" sizes="auto" class="lazyload"/>'
        '</span></figure>'
        '<div class="StatisticsPanel_panelWrap__iNrBj">'
        '<figure class="StatisticsPanel_logo__pnjFD">'
        '<span class="Image_image__RAAdZ Image_intrinsic__JRoea">'
        f'<img data-srcset="" data-src="{logo_src}" src="{logo_src}" alt="{logo_alt}" fetchPriority="low" '
        f'height="{logo_h}" width="{logo_w}" sizes="auto" class="lazyload"/>'
        '</span></figure>'
        '<figure class="StatisticsPanel_visualMobile__4w9EW">'
        '<span class="Image_image__RAAdZ Image_intrinsic__JRoea">'
        f'<img data-srcset="{vis_srcset}" data-src="{vis_src}" src="{vis_src}" alt="{vis_alt}" fetchPriority="low" '
        f'height="{vis_h}" width="{vis_w}" sizes="auto" class="lazyload"/>'
        '</span></figure>'
        f'<h3 class="StatisticsPanel_heading__Xqlyh">{stat}</h3>'
        f'<span class="StatisticsPanel_description__NM4c_">{desc}</span>'
        '<div class="StatisticsPanel_buttons__IavWc">'
        '<div class="Magnetic_magnetic__LncOy" data-fill="false">'
        '<div class="Button_button__JJiqJ Button_white__MQaf2" data-direction="forwards">'
        f'<a class="Button_inner__fnyH6" href="{btn_url}">'
        '<span class="Button_border__hirH2"></span>'
        '<span class="Button_text__IZaCD">'
        f'<span class="Button_textInner__JTTHe">{btn_title}</span>'
        f'{ARROW_SVG}'
        '</span></a></div></div></div></div>'
        '<figure class="StatisticsPanel_visual__crBRi">'
        '<span class="Image_image__RAAdZ Image_contain__awbZj">'
        f'<img data-srcset="{vis_srcset}" data-src="{vis_src}" src="{vis_src}" alt="{vis_alt}" fetchPriority="low" '
        f'height="{vis_h}" width="{vis_w}" sizes="auto" class="lazyload"/>'
        '</span></figure>'
        '</div></div>'
    )


def update_target_page(target_path, home_stats, is_en=False, is_gh_pages=False):
    text = open(target_path, "r", encoding="utf-8").read()

    # 0. Update section heading to match Homepage ('ÖLÇÜLEBİLİR SONUÇLAR' / 'MEASURABLE RESULTS')
    old_heading = "Strategic Craft. Measurable Growth." if is_en else "Estetik Tasarım. Ölçülebilir Büyüme."
    new_heading = "MEASURABLE RESULTS" if is_en else "ÖLÇÜLEBİLİR SONUÇLAR"
    text = text.replace(old_heading, new_heading)

    # 1. Inject / replace CSS style block in <head>
    style_re = re.compile(rf'<style id="{STYLE_ID}">.*?</style>', re.S)
    if style_re.search(text):
        text = style_re.sub(DARK_STATS_CSS, text, count=1)
    else:
        head_end = text.find("</head>")
        if head_end == -1:
            raise RuntimeError(f"No </head> in {target_path}")
        text = text[:head_end] + DARK_STATS_CSS + text[head_end:]

    # 2. Replace SSR slides inside StatisticsCarousel_swiper__PLGJ6 .swiper-wrapper
    wrapper_re = re.compile(
        r'(<div class="StatisticsCarousel_swiper__PLGJ6 swiper"><div class="swiper-wrapper">)'
        r'(.*?)'
        r'(</div><div class="StatisticsCarousel_swiperNav__)',
        re.S,
    )
    if not wrapper_re.search(text):
        raise RuntimeError(f"Could not find StatisticsCarousel swiper-wrapper in {target_path}")

    url_prefix = "/roasist-web" if is_gh_pages else ""
    new_slides_html = "".join(render_ssr_slide(item, url_prefix=url_prefix) for item in home_stats)
    text = wrapper_re.sub(lambda m: m.group(1) + new_slides_html + m.group(3), text, count=1)

    # 3. Update React Flight stream `statistics` prop cleanly
    matches, decoded_parts, full = extract_flight_chunks(text)
    recs = parse_flight_stream(full)
    replaced_flight = False
    for i, rec in enumerate(recs):
        if rec[0] != "line":
            continue
        payload = rec[2]
        if not payload or payload[0] not in "[{":
            continue
        try:
            obj = json.loads(payload)
        except Exception:
            continue
        holder = find_statistics_list(obj)
        if holder is not None:
            holder["statistics"] = home_stats
            new_payload = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
            recs[i] = ["line", rec[1], new_payload]
            replaced_flight = True
            break

    if not replaced_flight:
        raise RuntimeError(f"Could not find statistics array in Flight stream of {target_path}")

    new_full = serialize_flight_stream(recs)

    out_parts = []
    last_end = 0
    for idx, m in enumerate(matches):
        out_parts.append(text[last_end : m.start()])
        if idx == 0:
            encoded = json.dumps(new_full, ensure_ascii=False)[1:-1].replace("</", "\\u003c/")
            out_parts.append(m.group(1) + encoded + m.group(3))
        else:
            out_parts.append("")
        last_end = m.end()
    out_parts.append(text[last_end:])
    text = "".join(out_parts)

    with open(target_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"[OK] Synced {len(home_stats)} Homepage Statistics cards & heading ({new_heading}) into {os.path.relpath(target_path, REPO_ROOT)} ({len(text):,} bytes)")


def main():
    jobs = [
        # (home_source, target_page, is_en, is_gh_pages)
        (
            os.path.join(REPO_ROOT, "public", "kota-roasist-local.html"),
            os.path.join(REPO_ROOT, "public", "hizmetler", "performans-pazarlamasi", "index.html"),
            False,
            False,
        ),
        (
            os.path.join(REPO_ROOT, "public", "en", "index.html"),
            os.path.join(REPO_ROOT, "public", "en", "performance-marketing", "index.html"),
            True,
            False,
        ),
        (
            os.path.join(REPO_ROOT, "dist", "index.html"),
            os.path.join(REPO_ROOT, "dist", "hizmetler", "performans-pazarlamasi", "index.html"),
            False,
            True,
        ),
        (
            os.path.join(REPO_ROOT, "dist", "en", "index.html"),
            os.path.join(REPO_ROOT, "dist", "en", "performance-marketing", "index.html"),
            True,
            True,
        ),
    ]

    for home_src, target, is_en, is_gh in jobs:
        if not os.path.exists(home_src) or not os.path.exists(target):
            print(f"[SKIP] Missing {os.path.relpath(target, REPO_ROOT)} or {os.path.relpath(home_src, REPO_ROOT)}")
            continue
        stats = get_homepage_statistics(home_src)
        update_target_page(target, stats, is_en=is_en, is_gh_pages=is_gh)


if __name__ == "__main__":
    main()
