#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hydration-safe updater for /hizmetler/performans-pazarlamasi/:
  - Preserves 100% of KOTA layout, design, CSS, and animations
  - Updates both public/hizmetler/performans-pazarlamasi/index.html and
    dist/hizmetler/performans-pazarlamasi/index.html in place (preserving jsDelivr CDN assets in dist/)
  - Expands <section class="TextImageRows_textImageRows__lOU02"> and React Flight record 34
    from 3 channel rows (Google Ads, Instagram & Facebook / Meta Ads, TikTok Ads)
    to 6 channel rows by adding Yandex Ads, Bing Ads, and LinkedIn Ads
  - Updates channel summary lists on the page with byte-exact Flight T<hex>, recomputation.
"""

import json
import os
import re
import sys

ROOT = "/home/antigravity/Roasist/roasist-web"
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from update_about_page import parse_flight_stream, serialize_flight_stream  # noqa: E402

ARROW_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 17.1 15.17" '
    'class="Button_buttonArrow__0W9XI"><path d="m17.1,7.58s-.01-.04-.01-.06c.01-.22-.06-.45-.24-.61'
    "L9.23.19c-.31-.27-.78-.24-1.06.07-.27.31-.24.78.07,1.06l6.26,5.52H.75c-.41,0-.75.34-.75.75s.34.75.75.75"
    'h13.74l-6.26,5.52c-.31.27-.34.75-.07,1.06.15.17.35.25.56.25.18,0,.35-.06.5-.19l7.62-6.72'
    'c.18-.16.25-.39.24-.61,0-.02.01-.04.01-.06Z" fill="currentColor"></path></svg>'
)

CHANNELS = [
    {
        "key": "0",
        "title": "Google Ads (Arama, Alışveriş, PMax, YouTube)",
        "description": (
            "Google arama sonuçlarında (SERP), Alışveriş sekmesinde, YouTube ve GDN ağında "
            "satın alma niyeti en yüksek kullanıcılara tam aradıkları anda ulaşın."
        ),
        "href": "/hizmetler/performans-pazarlamasi/google-reklamlari/",
        "button_text": "Detaylı İncele",
        "media_type": "video",
        "src": "https://kota-content.b-cdn.net/app/uploads/2023/11/Animation-1-Bipsync-1.mp4",
    },
    {
        "key": "1",
        "title": "Instagram & Facebook (Meta Ads)",
        "description": (
            "Gelişmiş kitle segmentasyonu, katalog reklamları (DPA), Reels/Story kreatifleri "
            "ve Conversions API kurulumuyla sosyal medyada ölçeklenebilir satış yakalayın."
        ),
        "href": "/hizmetler/performans-pazarlamasi/instagram-reklamlari/",
        "button_text": "Detaylı İncele",
        "media_type": "image",
        "src": "https://kota-content.b-cdn.net/app/uploads/2023/11/Web-Development-backrate-2.png",
        "srcset": (
            "https://kota-content.b-cdn.net/app/uploads/2023/11/Web-Development-backrate-2.png 1224w, "
            "https://kota-content.b-cdn.net/app/uploads/2023/11/Web-Development-backrate-2-500x500.png 500w, "
            "https://kota-content.b-cdn.net/app/uploads/2023/11/Web-Development-backrate-2-768x768.png 768w"
        ),
    },
    {
        "key": "2",
        "title": "TikTok Ads",
        "description": (
            "Kısa video dinamiklerine uygun dikkat çekici kreatifler ve Spark Ads modelleriyle "
            "markanızı milyonlarca aktif kullanıcıyla buluşturun."
        ),
        "href": "/hizmetler/performans-pazarlamasi/tiktok-reklamlari/",
        "button_text": "Detaylı İncele",
        "media_type": "image",
        "src": "https://kota-content.b-cdn.net/app/uploads/2023/11/Wordpress-and-cms-mealeo.png",
        "srcset": (
            "https://kota-content.b-cdn.net/app/uploads/2023/11/Wordpress-and-cms-mealeo.png 1224w, "
            "https://kota-content.b-cdn.net/app/uploads/2023/11/Wordpress-and-cms-mealeo-500x500.png 500w, "
            "https://kota-content.b-cdn.net/app/uploads/2023/11/Wordpress-and-cms-mealeo-768x768.png 768w"
        ),
    },
    {
        "key": "3",
        "title": "Yandex Ads",
        "description": (
            "Rusya, BDT ülkeleri ve uluslararası pazarlarda hedef kitlenize Yandex Direct arama "
            "reklamları, ürün katalogları ve Yandex Reklam Ağı (YAN) üzerinden doğrudan ulaşarak "
            "global satışlarınızı ölçeklendirin."
        ),
        "href": "/hizmetler/performans-pazarlamasi/yandex-reklamlari/",
        "button_text": "Detaylı İncele",
        "media_type": "video",
        "src": "https://kota-content.b-cdn.net/app/uploads/2023/11/seo-geo-V2.mp4",
    },
    {
        "key": "4",
        "title": "Bing Ads",
        "description": (
            "Masaüstü ve kurumsal aramalarda yüksek satın alma gücüne sahip kitlelere Bing, Yahoo, "
            "DuckDuckGo ve Microsoft reklam ağında daha düşük tıklama maliyetleriyle (CPC) ulaşarak "
            "yüksek ROAS elde edin."
        ),
        "href": "/hizmetler/performans-pazarlamasi/bing-reklamlari/",
        "button_text": "Detaylı İncele",
        "media_type": "image",
        "src": "https://kota-content.b-cdn.net/app/uploads/2023/11/copywriting-2-1.jpg",
        "srcset": (
            "https://kota-content.b-cdn.net/app/uploads/2023/11/copywriting-2-1.jpg 1224w, "
            "https://kota-content.b-cdn.net/app/uploads/2023/11/copywriting-2-1-500x500.jpg 500w, "
            "https://kota-content.b-cdn.net/app/uploads/2023/11/copywriting-2-1-768x768.jpg 768w"
        ),
    },
    {
        "key": "5",
        "title": "LinkedIn Ads",
        "description": (
            "Şirket büyüklüğü, sektör, karar verici iş unvanı (CEO, CMO, Satın Alma Direktörü vb.) "
            "ve profesyonel ilgi alanlarına göre nokta atışı hedefleme yaparak yüksek nitelikli "
            "kurumsal B2B potansiyel müşteriler kazanın."
        ),
        "href": "/hizmetler/performans-pazarlamasi/linkedin-reklamlari/",
        "button_text": "Detaylı İncele",
        "media_type": "image",
        "src": "https://kota-content.b-cdn.net/app/uploads/2023/11/sitecare.jpg",
        "srcset": (
            "https://kota-content.b-cdn.net/app/uploads/2023/11/sitecare.jpg 1224w, "
            "https://kota-content.b-cdn.net/app/uploads/2023/11/sitecare-500x500.jpg 500w, "
            "https://kota-content.b-cdn.net/app/uploads/2023/11/sitecare-768x768.jpg 768w"
        ),
    },
]

TEXT_REPLACEMENTS = [
    (
        "Google Ads, Meta, TikTok, LinkedIn ve Yandex reklam uzmanlığı.",
        "Google Ads, Meta, TikTok, Yandex, Bing ve LinkedIn reklam uzmanlığı.",
    ),
    (
        "Google Ads, Meta, TikTok, LinkedIn ve Yandex kanallarını kapsayan veri odaklı büyüme stratejisidir.",
        "Google Ads, Meta, TikTok, Yandex, Bing ve LinkedIn kanallarını kapsayan veri odaklı büyüme stratejisidir.",
    ),
    (
        "Google, Instagram, Facebook, TikTok, LinkedIn ve Yandex entegrasyonu",
        "Google, Instagram, Facebook, TikTok, Yandex, Bing ve LinkedIn entegrasyonu",
    ),
    (
        "(Google Ads, Meta Business, TikTok, LinkedIn, Yandex)",
        "(Google Ads, Meta Business, TikTok, Yandex, Bing, LinkedIn)",
    ),
]


def build_ssr_row(ch: dict) -> str:
    if ch["media_type"] == "video":
        media_inner = (
            '<span class="AutoplayVideo_video__zckWy AutoplayVideo_fill__ZPgCR">'
            '<video loop="" muted="" playsInline=""></video></span>'
        )
    else:
        media_inner = (
            '<span class="Image_image__RAAdZ Image_fill__EiIzS">'
            f'<img data-srcset="{ch["srcset"]}" data-src="{ch["src"]}" '
            'alt="" fetchPriority="low" height="1224" width="1224" sizes="auto" class="lazyload"/></span>'
        )

    return (
        '<div class="TextImageRows_row__PPlpB">'
        '<div class="TextImageRows_text__bRCSP">'
        '<h3 class="TextImageRows_heading__RS3OS">'
        f'<span class="LineByLine_headingOuter__JmusT"><span>{ch["title"]}</span></span>'
        "</h3>"
        '<div class="TextImageRows_text__bRCSP">'
        '<span class="FadeIn_container__bjQVL" data-fill="false">'
        f'<span><p>{ch["description"]}</p>\n</span>'
        "</span>"
        "</div>"
        '<div class="TextImageRows_buttonContainer___PqVy">'
        '<span class="FadeIn_container__bjQVL" data-fill="false">'
        '<div class="Magnetic_magnetic__LncOy" data-fill="false">'
        '<div class="Button_button__JJiqJ" data-direction="forwards">'
        f'<a class="Button_inner__fnyH6" href="{ch["href"]}">'
        '<span class="Button_border__hirH2"></span>'
        '<span class="Button_text__IZaCD">'
        f'<span class="Button_textInner__JTTHe">{ch["button_text"]}</span>'
        f"{ARROW_SVG}"
        "</span>"
        "</a>"
        "</div>"
        "</div>"
        "</span>"
        "</div>"
        "</div>"
        '<figure class="TextImageRows_media__twu3R">'
        f'<div class="ImageEnter_image__FSEP_" data-fill="true">{media_inner}</div>'
        "</figure>"
        "</div>"
    )


def build_ssr_section(channels: list) -> str:
    rows_html = "".join(build_ssr_row(ch) for ch in channels)
    return f'<section class="TextImageRows_textImageRows__lOU02"><div class="container">{rows_html}</div></section>'


def build_flight_row(ch: dict) -> list:
    if ch["media_type"] == "video":
        media_children = [
            False,
            ["$", "$L32", None, {"src": ch["src"], "layout": "fill"}],
        ]
    else:
        media_children = [
            [
                "$",
                "$L47",
                None,
                {
                    "image": {
                        "altText": "",
                        "srcSet": ch["srcset"],
                        "sourceUrl": ch["src"],
                        "mediaDetails": {"width": 1224, "height": 1224},
                    },
                    "layout": "fill",
                },
            ],
            False,
        ]

    return [
        "$",
        "div",
        ch["key"],
        {
            "className": "TextImageRows_row__PPlpB",
            "children": [
                [
                    "$",
                    "div",
                    None,
                    {
                        "className": "TextImageRows_text__bRCSP",
                        "children": [
                            [
                                "$",
                                "h3",
                                None,
                                {
                                    "className": "TextImageRows_heading__RS3OS",
                                    "children": [
                                        "$",
                                        "$L2c",
                                        None,
                                        {
                                            "children": [
                                                "$",
                                                "span",
                                                None,
                                                {"dangerouslySetInnerHTML": {"__html": ch["title"]}},
                                            ]
                                        },
                                    ],
                                },
                            ],
                            [
                                "$",
                                "div",
                                None,
                                {
                                    "className": "TextImageRows_text__bRCSP",
                                    "children": [
                                        "$",
                                        "$L2e",
                                        None,
                                        {
                                            "delay": 0.3,
                                            "children": [
                                                "$",
                                                "span",
                                                None,
                                                {
                                                    "dangerouslySetInnerHTML": {
                                                        "__html": f'<p>{ch["description"]}</p>\n'
                                                    }
                                                },
                                            ],
                                        },
                                    ],
                                },
                            ],
                            [
                                "$",
                                "div",
                                None,
                                {
                                    "className": "TextImageRows_buttonContainer___PqVy",
                                    "children": [
                                        "$",
                                        "$L2e",
                                        None,
                                        {
                                            "delay": 0.3,
                                            "children": [
                                                "$",
                                                "$L21",
                                                None,
                                                {
                                                    "href": ch["href"],
                                                    "type": "a-internal",
                                                    "text": ch["button_text"],
                                                },
                                            ],
                                        },
                                    ],
                                },
                            ],
                        ],
                    },
                ],
                [
                    "$",
                    "figure",
                    None,
                    {
                        "className": "TextImageRows_media__twu3R",
                        "children": [
                            "$",
                            "$L4a",
                            None,
                            {"fill": True, "children": media_children},
                        ],
                    },
                ],
            ],
        },
    ]


def build_flight_record_34(channels: list) -> str:
    payload = [
        "$",
        "section",
        None,
        {
            "className": "TextImageRows_textImageRows__lOU02",
            "children": [
                "$",
                "div",
                None,
                {
                    "className": "container",
                    "children": [[build_flight_row(ch) for ch in channels], False],
                },
            ],
        },
    ]
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))


def update_html_file(rel_path: str):
    abs_path = os.path.join(ROOT, rel_path)
    with open(abs_path, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Verify existing SSR section (if still 3 rows, assert 100% parity with CHANNELS[:3])
    sec_re = re.compile(r'<section class="TextImageRows_textImageRows__lOU02">.*?</section>', re.S)
    m_sec = sec_re.search(html)
    if not m_sec:
        raise RuntimeError(f"Could not find TextImageRows section in {rel_path}")

    existing_sec = m_sec.group(0)
    if "Yandex Ads</h3>" not in existing_sec and "<span>Yandex Ads</span>" not in existing_sec:
        expected_3_ssr = build_ssr_section(CHANNELS[:3])
        if existing_sec != expected_3_ssr:
            raise RuntimeError(f"SSR parity check for existing 3 rows failed in {rel_path}!")

    new_ssr_sec = build_ssr_section(CHANNELS)
    html = html[: m_sec.start()] + new_ssr_sec + html[m_sec.end() :]

    # 2. Update Flight push stream
    push_re = re.compile(r"self\.__next_f\.push\(\[1,\s*(\"(?:\\.|[^\"\\])*\")\]\)")
    pushes = list(push_re.finditer(html))
    if len(pushes) != 1:
        raise RuntimeError(f"Expected 1 Flight push in {rel_path}, found {len(pushes)}")

    pm = pushes[0]
    flight_str = json.loads(pm.group(1))
    records = parse_flight_stream(flight_str)

    found_34 = False
    for rec in records:
        kind, key, val = rec
        if kind == "line" and key == "34":
            found_34 = True
            if "Yandex Ads" not in val:
                expected_3_flight = build_flight_record_34(CHANNELS[:3])
                if val != expected_3_flight:
                    raise RuntimeError(f"Flight 34 parity check for existing 3 rows failed in {rel_path}!")
            rec[2] = build_flight_record_34(CHANNELS)
        else:
            for old_txt, new_txt in TEXT_REPLACEMENTS:
                if old_txt in rec[2]:
                    rec[2] = rec[2].replace(old_txt, new_txt)

    if not found_34:
        raise RuntimeError(f"Record 34 not found in Flight stream of {rel_path}")

    new_flight_str = serialize_flight_stream(records)
    # Re-parse to guarantee 100% Flight stream validity
    verify_records = parse_flight_stream(new_flight_str)
    assert serialize_flight_stream(verify_records) == new_flight_str

    encoded_flight = json.dumps(new_flight_str, ensure_ascii=False).replace("</script>", "<\\/script>")
    new_push = f"self.__next_f.push([1,{encoded_flight}])"

    # Replace non-Flight SSR/head occurrences of channel summary text, then splice new_push
    before_push = html[: pm.start()]
    after_push = html[pm.end() :]
    for old_txt, new_txt in TEXT_REPLACEMENTS:
        before_push = before_push.replace(old_txt, new_txt)
        after_push = after_push.replace(old_txt, new_txt)

    final_html = before_push + new_push + after_push
    with open(abs_path, "w", encoding="utf-8") as f:
        f.write(final_html)

    print(f"[OK] Updated {rel_path} ({len(final_html):,} bytes, 6 channel rows)")


def main():
    targets = [
        "public/hizmetler/performans-pazarlamasi/index.html",
        "dist/hizmetler/performans-pazarlamasi/index.html",
    ]
    for rel in targets:
        update_html_file(rel)


if __name__ == "__main__":
    main()
