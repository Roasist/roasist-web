#!/usr/bin/env python3
"""
Updates the 'Performans Pazarlama Sürecimiz' / 'Our Performance Marketing Process'
(Timeline_timeline__KvsOC) section on the Performance Marketing page (TR & EN,
both public/ and dist/) to 6 bespoke stages and elevates the card styling.
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

STYLE_ID = "roasist-perf-process-cards"

TR_STEPS = [
    {
        "num": "01",
        "heading": "Veri & Pazar Analizi",
        "text": "Mevcut hesaplarınızı, rakiplerinizi ve birim ekonominizi (kâr marjı, başabaş ROAS) denetler; gerçekçi büyüme hedeflerini ve KPI'ları netleştiririz.",
    },
    {
        "num": "02",
        "heading": "Büyüme Stratejisi",
        "text": "Hedef kitlenize ve bütçenize en uygun kanal dağılımını, teklif kurgusunu ve dönüşüm hunisi (funnel) yol haritasını oluştururuz.",
    },
    {
        "num": "03",
        "heading": "Ölçümleme & Kurulum",
        "text": "Piksel, dönüşüm API'leri ve analitik altyapınızı kusursuz hale getirir; yüksek dönüşüm odaklı reklam kreatifleri ve kampanyalarla yayına çıkarız.",
    },
    {
        "num": "04",
        "heading": "Sürekli Optimizasyon",
        "text": "Verileri günlük olarak takip eder; A/B testleri, bütçe kaydırmaları ve kreatif yenilemeleriyle edinme maliyetlerini (CPA) düşürürüz.",
    },
    {
        "num": "05",
        "heading": "Şeffaf Raporlama",
        "text": "Hangi kanalın ve kampanyanın ne kadar kâr getirdiğini anlık panellerle şeffaf biçimde sunar, kararlarımızı net verilere dayandırırız.",
    },
    {
        "num": "06",
        "heading": "Kârlı Ölçekleme",
        "text": "Kazanan kampanyaları ve yeni pazar fırsatlarını kontrollü bütçe artışlarıyla ölçekleyerek markanız için sürdürülebilir büyüme yaratırız.",
    },
]

EN_STEPS = [
    {
        "num": "01",
        "heading": "Data & Market Analysis",
        "text": "We audit your existing accounts, competitors, and unit economics (profit margin, break-even ROAS) to define realistic growth targets and KPIs.",
    },
    {
        "num": "02",
        "heading": "Growth Strategy",
        "text": "We build the optimal channel mix, bidding architecture, and full-funnel conversion roadmap tailored to your audience and budget.",
    },
    {
        "num": "03",
        "heading": "Tracking & Setup",
        "text": "We perfect your pixel, conversion APIs, and analytics stack before launching high-converting ad creatives and structured campaigns.",
    },
    {
        "num": "04",
        "heading": "Continuous Optimization",
        "text": "We monitor performance daily—running A/B tests, reallocating budgets, and refreshing creatives to systematically lower acquisition costs (CPA).",
    },
    {
        "num": "05",
        "heading": "Transparent Reporting",
        "text": "We show exactly how much profit each channel and campaign generates through live dashboards, grounding every decision in clear data.",
    },
    {
        "num": "06",
        "heading": "Profitable Scaling",
        "text": "We scale winning campaigns and new market opportunities with disciplined budget increases to build sustainable growth for your brand.",
    },
]

PROCESS_CSS = f"""<style id="{STYLE_ID}">
/* Elevated 6-Step Performance Marketing Process Cards */
.Timeline_timeline__KvsOC {{
  padding-top: clamp(3rem, 5vw, 4.5rem) !important;
  padding-bottom: clamp(3rem, 5vw, 4.5rem) !important;
}}
.Timeline_headings__PF6gg {{
  gap: 1rem !important;
}}
.Timeline_subheading__IVqa_ {{
  color: #475569 !important;
  max-width: 58ch !important;
}}
.Timeline_inner__J706Z {{
  align-items: stretch !important;
  padding-top: 1.5rem !important;
  padding-bottom: 2rem !important;
}}
.Timeline_block__WRSOn {{
  position: relative !important;
  background-color: #ffffff !important;
  border: 1px solid rgba(15, 23, 42, 0.08) !important;
  box-shadow: 0 12px 32px -12px rgba(15, 23, 42, 0.08), 0 2px 6px rgba(15, 23, 42, 0.03) !important;
  border-radius: 20px 48px 20px 20px !important;
  padding: 2rem 1.75rem !important;
  width: 80vw !important;
  max-width: 440px !important;
  min-height: 290px !important;
  flex-direction: column !important;
  justify-content: flex-start !important;
  gap: 0 !important;
  margin-right: 1.25rem !important;
  transition: transform 180ms cubic-bezier(0.22, 1, 0.36, 1),
              border-color 180ms cubic-bezier(0.22, 1, 0.36, 1),
              box-shadow 180ms cubic-bezier(0.22, 1, 0.36, 1) !important;
}}
@media (min-width: 850px) {{
  .Timeline_block__WRSOn {{
    width: clamp(350px, 31vw, 440px) !important;
    max-width: 440px !important;
    min-height: 320px !important;
    padding: 2.5rem 2.25rem 2.25rem !important;
    border-radius: 24px 68px 24px 24px !important;
    margin-right: 1.75rem !important;
  }}
  .Timeline_block__WRSOn:hover {{
    border-color: rgba(118, 2, 255, 0.28) !important;
    box-shadow: 0 20px 44px -16px rgba(118, 2, 255, 0.14), 0 4px 12px rgba(15, 23, 42, 0.04) !important;
  }}
}}
.Timeline_image__txoKz,
.Timeline_workInvolved__Z_cYT,
.Timeline_bottomTimeline__2F2yN {{
  display: none !important;
}}
.Timeline_block__WRSOn > div {{
  display: flex !important;
  flex-direction: column !important;
  height: 100% !important;
  width: 100% !important;
}}
.Timeline_blockHeading__hif7t {{
  display: flex !important;
  flex-direction: column-reverse !important;
  align-items: flex-start !important;
  gap: 1.35rem !important;
  margin: 0 0 1rem 0 !important;
  font-size: clamp(1.45rem, 1.9vw, 1.85rem) !important;
  font-weight: 500 !important;
  letter-spacing: -0.025em !important;
  line-height: 1.2 !important;
  color: #0f172a !important;
}}
.Timeline_duration__We5gA {{
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  font-variant-numeric: tabular-nums !important;
  font-size: 0.875rem !important;
  font-weight: 600 !important;
  letter-spacing: 0.06em !important;
  line-height: 1 !important;
  color: #7602FF !important;
  background: rgba(118, 2, 255, 0.07) !important;
  border: 1px solid rgba(118, 2, 255, 0.18) !important;
  border-radius: 999px !important;
  padding: 0.42rem 0.9rem !important;
  transform: none !important;
}}
.Timeline_blockText__RV__j {{
  margin: 0 !important;
  color: #475569 !important;
  font-size: clamp(0.96rem, 1.05vw, 1.05rem) !important;
  font-weight: 400 !important;
  line-height: 1.65 !important;
  letter-spacing: -0.005em !important;
}}
</style>"""


def extract_flight_chunks(html_text):
    pattern = re.compile(r'(<script>self\.__next_f\.push\(\[1,")((?:\\.|[^"\\])*)("\]\)</script>)')
    matches = list(pattern.finditer(html_text))
    decoded_parts = [json.loads('"' + m.group(2) + '"') for m in matches]
    return matches, decoded_parts, "".join(decoded_parts)


def find_timeline_data(obj):
    if isinstance(obj, dict):
        if "blocks" in obj and isinstance(obj["blocks"], list) and "heading" in obj and "enable" in obj:
            return obj
        for v in obj.values():
            res = find_timeline_data(v)
            if res is not None:
                return res
    elif isinstance(obj, list):
        for v in obj:
            res = find_timeline_data(v)
            if res is not None:
                return res
    return None


def build_flight_blocks(steps, img_url="/roasist-logo.svg"):
    blocks = []
    for idx, st in enumerate(steps, start=1):
        blocks.append({
            "heading": st["heading"],
            "image": {
                "altText": "",
                "srcSet": None,
                "sourceUrl": img_url,
                "mediaDetails": {"width": 426, "height": 426},
            },
            "text": st["text"],
            "duration": st["num"],
            "weekNumber": idx,
            "workInvolved": [],
        })
    return blocks


def render_ssr_blocks(steps, img_url="/roasist-logo.svg", work_label="Neler Yapıyoruz"):
    esc = lambda s: html_lib.escape(str(s), quote=True)
    parts = []
    for st in steps:
        parts.append(
            '<div class="Timeline_block__WRSOn" data-animation="grid-item">'
            '<figure class="Timeline_image__txoKz">'
            '<span class="Image_image__RAAdZ Image_fill__EiIzS">'
            f'<img data-srcset="" data-src="{esc(img_url)}" alt="" fetchPriority="low" height="426" width="426" sizes="auto" class="lazyload"/>'
            '</span></figure>'
            '<div>'
            f'<p class="Timeline_blockHeading__hif7t"><span>{esc(st["heading"])}</span>'
            f'<span class="Timeline_duration__We5gA">{esc(st["num"])}</span></p>'
            f'<p class="Timeline_blockText__RV__j">{esc(st["text"])}</p>'
            f'<div class="Timeline_workInvolved__Z_cYT"><p>{esc(work_label)}</p>'
            '<div class="Timeline_workInvolvedList__CKLML"></div></div>'
            '</div></div>'
        )
    return "".join(parts)


def render_ssr_bottom(steps):
    parts = []
    for idx, _ in enumerate(steps, start=1):
        parts.append(
            '<div class="Timeline_blockTime__5jxQS">'
            f'<span class="Timeline_weekNumber__qqgnG">Week <!-- -->{idx}</span>'
            '</div>'
        )
    return "".join(parts)


def update_page(target_path, steps, is_en=False, is_gh_pages=False):
    text = open(target_path, "r", encoding="utf-8").read()

    # 1. Inject / replace CSS in <head>
    style_re = re.compile(rf'<style id="{STYLE_ID}">.*?</style>', re.S)
    if style_re.search(text):
        text = style_re.sub(PROCESS_CSS, text, count=1)
    else:
        head_end = text.find("</head>")
        if head_end == -1:
            raise RuntimeError(f"No </head> in {target_path}")
        text = text[:head_end] + PROCESS_CSS + text[head_end:]

    img_url = "/roasist-web/roasist-logo.svg" if is_gh_pages else "/roasist-logo.svg"
    work_label = "Work involved" if is_en else "Neler Yapıyoruz"

    # 2. Replace SSR Timeline_inner__J706Z and Timeline_bottomTimeline__2F2yN
    inner_re = re.compile(
        r'(<div class="Timeline_inner__J706Z">)(.*?)(</div><div class="Timeline_bottomTimeline__2F2yN"[^>]*>)(.*?)(</div></div></div></div></div></section>)',
        re.S,
    )
    if not inner_re.search(text):
        raise RuntimeError(f"Could not find Timeline_inner__J706Z in {target_path}")

    new_blocks_html = render_ssr_blocks(steps, img_url=img_url, work_label=work_label)
    new_bottom_html = render_ssr_bottom(steps)
    text = inner_re.sub(
        lambda m: m.group(1) + new_blocks_html + m.group(3) + new_bottom_html + m.group(5),
        text,
        count=1,
    )

    # 3. Update Flight stream Timeline blocks
    matches, _, full = extract_flight_chunks(text)
    recs = parse_flight_stream(full)
    replaced = False
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
        tl = find_timeline_data(obj)
        if tl is not None:
            tl["blocks"] = build_flight_blocks(steps, img_url=img_url)
            recs[i] = ["line", rec[1], json.dumps(obj, ensure_ascii=False, separators=(",", ":"))]
            replaced = True
            break

    if not replaced:
        raise RuntimeError(f"Could not find Timeline data in Flight stream of {target_path}")

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
    print(f"[OK] Updated 6-step Process cards in {os.path.relpath(target_path, REPO_ROOT)} ({len(text):,} bytes)")


def main():
    jobs = [
        (os.path.join(REPO_ROOT, "public", "hizmetler", "performans-pazarlamasi", "index.html"), TR_STEPS, False, False),
        (os.path.join(REPO_ROOT, "public", "en", "performance-marketing", "index.html"), EN_STEPS, True, False),
        (os.path.join(REPO_ROOT, "dist", "hizmetler", "performans-pazarlamasi", "index.html"), TR_STEPS, False, True),
        (os.path.join(REPO_ROOT, "dist", "en", "performance-marketing", "index.html"), EN_STEPS, True, True),
    ]
    for path, steps, is_en, is_gh in jobs:
        if not os.path.exists(path):
            print(f"[SKIP] {os.path.relpath(path, REPO_ROOT)} does not exist")
            continue
        update_page(path, steps, is_en=is_en, is_gh_pages=is_gh)


if __name__ == "__main__":
    main()
