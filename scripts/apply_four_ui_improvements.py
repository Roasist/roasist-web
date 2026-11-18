#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Applies the 4 UI/UX improvements requested by the user across all TR and EN HTML pages
in both public/ and dist/:
  1. Footer redesign (.roasist-footer-v2 inside <footer class="Footer_footer__pQtti" data-theme="dark">)
     while keeping the dark WebGL animated background 100% untouched.
  2. Page title row (.roasist-hero-title-row: "| <sayfa başlığı>" + right arrow) moved to the
     VERY TOP of the Hero section on all non-home pages (above all h2/h3/h1/category content).
  3. Scroll-driven rotating arrow animation (#roasist-arrow-rotator) on ALL heading and
     page-title arrows across the website: starts pointing left (48deg) toward the heading
     and rotates smoothly in place on scroll to point downward (0deg), with clean alignment.
  4. Removes the Showreel section (#kotaverceCta / .KotaverseCta_kotaverseCta__bBpWa) above
     the footer on the Homepage (and contact pages) while keeping a 0px anchor for ScrollTrigger.
"""

import glob
import html as html_mod
import json
import os
import re
import sys

ROOT = "/home/antigravity/Roasist/roasist-web"
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from apply_phase1_cleanup import (  # noqa: E402
    find_node_by_class,
    rewrite_flight_in_html,
)
from apply_phase3_seo_gtm import get_route_for_file  # noqa: E402

ROASIST_WHITE_SVG_PATH = (
    "M176.71,198.48v1.32l-35.19.2c-1.72-2.67-2.88-6.5-3.64-11.52-.59-4.79-1.15-10-1.55-15.35"
    "s-.56-10.76-1-15.75a95,95,0,0,0-1.16-12.48c-1-4.42-2.51-8.08-4.62-10.56a20.66,20.66,0,0,0-7.46-6.17,"
    "32.19,32.19,0,0,0-9.81-2.88c-3.66-.36-7.29-.56-11.15-.56h-47v-35h56.29v18.62L164.6,77.1,110.46,45.8V64.42"
    "H54.17v16L0,49.07,54.17,17.74V34.08h64.9c18.26,0,32.29,3.47,41.89,10.17,9.78,6.93,14.6,18.06,14.6,33.41,"
    "0,10.4-2.12,18.85-6.34,24.79C165,108.79,158.06,114,148.65,118.2a28.6,28.6,0,0,1,11.52,7.29,35.16,35.16,0,0,1,"
    "6.18,11.13A60.62,60.62,0,0,1,169,149.69c.4,4.62.56,9.21.76,13.44.2,6.33.4,11.52.79,15.74.36,4.06,1,7.5,1.32,10"
    "A24.35,24.35,0,0,0,174,195,8.76,8.76,0,0,0,176.71,198.48Z M186,84q1.68-15.32,7.38-26.28a41.37,41.37,0,0,1,"
    "16.45-17.12q10.74-6.15,28.86-6.15t28.86,6.15A41.37,41.37,0,0,1,284,57.73q5.7,11,7.38,26.28a308.26,308.26,0,0,1,"
    "1.68,33.45A307.5,307.5,0,0,1,291.39,151q-1.68,15.21-7.38,26.17A39.24,39.24,0,0,1,267.56,194q-10.74,5.82-28.86,"
    "5.82T209.84,194a39.24,39.24,0,0,1-16.45-16.78Q187.69,166.25,186,151a307.5,307.5,0,0,1-1.68-33.57A308.26,308.26,"
    "0,0,1,186,84Zm31.32,60.86a76.29,76.29,0,0,0,3.13,18.35q2.35,7,6.72,10.29c2.91,2.17,6.74,3.25,11.52,3.25s8.61-1.08,"
    "11.52-3.25,5.15-5.59,6.71-10.29a76.24,76.24,0,0,0,3.14-18.35q.78-11.3.78-27.41t-.78-27.29a77.72,77.72,0,0,0-3.14-"
    "18.35q-2.34-7.16-6.71-10.4T238.7,58.17c-4.78,0-8.61,1.09-11.52,3.25s-5.15,5.63-6.72,10.4a77.78,77.78,0,0,0-3.13,"
    "18.35q-.78,11.19-.78,27.29T217.33,144.87Z M383,37.59,425.3,197.34H391.74l-7.39-33.79H341.84l-7.38,33.79H300.9"
    "L343.19,37.59Zm-4.25,99.56L363.32,65.33h-.44l-15.44,71.82Z M462.44,152.14a53,53,0,0,0,.9,10.18,17.61,17.61,0,0,0,"
    "3.35,7.72,16.6,16.6,0,0,0,6.6,4.93,26.39,26.39,0,0,0,10.41,1.79A20.56,20.56,0,0,0,497,172q5.92-4.81,5.93-14.88"
    "a26.93,26.93,0,0,0-1.45-9.29,18.47,18.47,0,0,0-4.82-7.05,34.1,34.1,0,0,0-8.83-5.7,126.18,126.18,0,0,0-13.54-5.26,"
    "115.68,115.68,0,0,1-18.57-7.83,49.79,49.79,0,0,1-13.09-10,35.53,35.53,0,0,1-7.72-13.2,55.56,55.56,0,0,1-2.46-17.34"
    "q0-23.72,13.2-35.35t36.25-11.63a79.06,79.06,0,0,1,19.8,2.34,41.63,41.63,0,0,1,15.66,7.61,35.58,35.58,0,0,1,10.29,"
    "13.43q3.69,8.16,3.69,19.57v4.48H500.48q0-11.42-4-17.56T483,58.17a22.43,22.43,0,0,0-8.95,1.57,15.1,15.1,0,0,0-5.71,"
    "4.14,14.16,14.16,0,0,0-2.91,5.93,30.48,30.48,0,0,0-.78,6.93,23.06,23.06,0,0,0,3.13,12.42q3.13,5,13.43,9.29l24.83,"
    "10.74a75.73,75.73,0,0,1,15,8.39,41,41,0,0,1,9.29,9.39,31.46,31.46,0,0,1,4.81,11.08,62.31,62.31,0,0,1,1.34,13.42"
    "q0,25.29-14.65,36.81T481,199.8q-27.3,0-39-11.86t-11.75-34v-6.48h32.22Z M554.17,37.59h32.22V197.34H554.17ZM582.81,"
    "26.4H557.75V0h25.06Z M636.29,152.14a53.81,53.81,0,0,0,.89,10.18,17.74,17.74,0,0,0,3.36,7.72,16.6,16.6,0,0,0,6.6,"
    "4.93,26.37,26.37,0,0,0,10.4,1.79A20.59,20.59,0,0,0,670.86,172q5.92-4.81,5.93-14.88a26.68,26.68,0,0,0-1.46-9.29,"
    "18.33,18.33,0,0,0-4.81-7.05,34.17,34.17,0,0,0-8.84-5.7,125.1,125.1,0,0,0-13.53-5.26,115.68,115.68,0,0,1-18.57-7.83,"
    "49.63,49.63,0,0,1-13.09-10,35.53,35.53,0,0,1-7.72-13.2,55.56,55.56,0,0,1-2.46-17.34q0-23.72,13.2-35.35t36.24-11.63"
    "a79.2,79.2,0,0,1,19.81,2.34,41.63,41.63,0,0,1,15.66,7.61,35.58,35.58,0,0,1,10.29,13.43Q705.2,66,705.2,77.41v4.48"
    "H674.33q0-11.42-4-17.56t-13.43-6.16a22.46,22.46,0,0,0-9,1.57,15,15,0,0,0-5.7,4.14,14.16,14.16,0,0,0-2.91,5.93,"
    "29.93,29.93,0,0,0-.78,6.93,23.06,23.06,0,0,0,3.13,12.42q3.14,5,13.42,9.29l24.84,10.74a76,76,0,0,1,15,8.39A41,41,"
    "0,0,1,704.2,127a31.44,31.44,0,0,1,4.8,11.08,61.66,61.66,0,0,1,1.35,13.42q0,25.29-14.66,36.81T654.86,199.8q-27.3,0-"
    "39-11.86t-11.75-34v-6.48h32.22Z M820,64h-34.9V197.34H752.86V64H718V37.59H820Z"
)

ARROW_SVG_HTML = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 75.91 75.65">'
    '<path d="m13.65 67.65 61.93-62L69.92 0 8 61.99V.25H0v75.4h75.91v-8H13.65z" fill="currentColor"></path>'
    "</svg>"
)

EXT_ARROW_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 12.69 12.69" class="roasist-footer__ext-icon">'
    '<path fill="currentColor" d="M12.65.31a.504.504 0 00-.46-.31H.5C.22 0 0 .22 0 .5s.22.5.5.5h10.49L.55 11.43'
    'c-.2.2-.2.51 0 .71a.485.485 0 00.7 0L11.69 1.71v10.47c0 .28.22.5.5.5s.5-.22.5-.5V.52c0-.07 0-.14-.04-.21z"></path>'
    "</svg>"
)

ROUTE_PAGE_LABELS: dict[str, str] = {
    # About
    "/hakkimizda/": "hakkımızda",
    "/en/who-we-are/": "who we are",
    # References
    "/referanslar/": "referanslar",
    "/en/references/": "our work",
    # Contact
    "/iletisim/": "iletişim",
    "/start-your-project/": "iletişim",
    "/en/contact-us/": "contact us",
    # Privacy
    "/gizlilik-politikasi-ve-kullanim-sartlari/": "gizlilik politikası & kvkk",
    "/en/privacy-policy-and-terms-of-use/": "privacy policy & terms of use",
    # Services (TR)
    "/hizmetler/": "hizmetlerimiz",
    "/hizmetler/performans-pazarlamasi/": "performans pazarlaması",
    "/hizmetler/google-reklamlari/": "google reklamları",
    "/hizmetler/performans-pazarlamasi/google-reklamlari/": "google reklamları",
    "/hizmetler/instagram-reklamlari/": "instagram reklamları",
    "/hizmetler/performans-pazarlamasi/instagram-reklamlari/": "instagram reklamları",
    "/hizmetler/facebook-reklamlari/": "facebook reklamları",
    "/hizmetler/performans-pazarlamasi/facebook-reklamlari/": "facebook reklamları",
    "/hizmetler/tiktok-reklamlari/": "tiktok reklamları",
    "/hizmetler/performans-pazarlamasi/tiktok-reklamlari/": "tiktok reklamları",
    "/hizmetler/linkedin-reklamlari/": "linkedin reklamları",
    "/hizmetler/performans-pazarlamasi/linkedin-reklamlari/": "linkedin reklamları",
    "/hizmetler/yandex-reklamlari/": "yandex reklamları",
    "/hizmetler/performans-pazarlamasi/yandex-reklamlari/": "yandex reklamları",
    "/hizmetler/bing-reklamlari/": "bing reklamları",
    "/hizmetler/performans-pazarlamasi/bing-reklamlari/": "bing reklamları",
    "/hizmetler/seo/": "seo",
    "/hizmetler/grafik-tasarim/": "grafik tasarım",
    "/hizmetler/web-tasarim/": "web tasarım",
    "/hizmetler/360-derece-dijital-pazarlama-yonetimi/": "360° dijital pazarlama yönetimi",
    # Services (EN)
    "/en/services/": "our services",
    "/en/performance-marketing/": "performance marketing",
    "/en/google-ads/": "google ads",
    "/en/instagram-ads/": "instagram ads",
    "/en/facebook-ads/": "facebook ads",
    "/en/tiktok-ads/": "tiktok ads",
    "/en/linkedin-ads/": "linkedin ads",
    "/en/yandex-ads/": "yandex ads",
    "/en/bing-ads/": "bing ads",
    "/en/seo/": "seo",
    "/en/graphic-design/": "graphic design",
    "/en/web-design/": "web design",
    "/en/360-digital-marketing-management/": "360° digital marketing",
}


def get_page_label_for_route(route: str) -> str | None:
    norm = route if route.endswith("/") else route + "/"
    if norm in ("/", "/en/"):
        return None
    if norm in ROUTE_PAGE_LABELS:
        return ROUTE_PAGE_LABELS[norm]
    if norm.startswith("/referanslar/"):
        return "referanslar"
    if norm.startswith("/en/references/"):
        return "our work"
    if norm.startswith("/blog/") or norm.startswith("/en/blog/"):
        return "blog"
    return None


def build_footer_inner_html(lang: str, is_dist: bool) -> str:
    img_base = (
        "https://cdn.jsdelivr.net/gh/Roasist/roasist-web@c766063e6a19824bf5e1a598d275bf05cbf2226f/public/images"
        if is_dist
        else "/images"
    )
    if lang == "en":
        home_href = "/en/"
        eyebrow = "next growth chapter"
        cta_heading = "Ready to scale your brand with data-driven strategy?"
        cta_btn = "Get a Free Digital Audit"
        cta_href = "/en/contact-us/"
        brand_desc = (
            "Next-generation 360° digital growth and performance marketing agency turning ad spend "
            "into measurable revenue, qualified global leads, and sustainable ROAS."
        )
        col1_title = "Our Services"
        services = [
            ("Performance Marketing", "/en/performance-marketing/"),
            ("Google Ads Management", "/en/google-ads/"),
            ("Instagram & Meta Ads", "/en/instagram-ads/"),
            ("Enterprise SEO & AEO", "/en/seo/"),
            ("Web Design & Development", "/en/web-design/"),
            ("360° Digital Marketing", "/en/360-digital-marketing-management/"),
        ]
        col2_title = "Explore"
        explore = [
            ("Who We Are", "/en/who-we-are/"),
            ("Case Studies & Work", "/en/references/"),
            ("Medistate — Case Study", "/en/references/medistate/"),
            ("Summer Homes — Case Study", "/en/references/summer-homes/"),
            ("Blog & Insights", "/en/blog/"),
            ("Contact Us", "/en/contact-us/"),
        ]
        col3_title = "Contact & Office"
        loc_text = "Istanbul, Turkiye"
        hours_text = "Mon – Fri · 09:00 – 18:30 (GMT+3)"
        priv_label = "Privacy Policy & Terms"
        priv_href = "/en/privacy-policy-and-terms-of-use/"
        copy_text = "© 2026 Roasist Digital Marketing Agency. All rights reserved."
    else:
        home_href = "/"
        eyebrow = "yeni bir büyüme hikayesi"
        cta_heading = "Markanızı veriye dayalı stratejiyle ölçeklendirmeye hazır mısınız?"
        cta_btn = "Ücretsiz Dijital Analiz Alın"
        cta_href = "/iletisim/"
        brand_desc = (
            "Reklam bütçenizi ölçülebilir ciroya, nitelikli global lead akışına ve sürdürülebilir ROAS "
            "büyümesine dönüştüren yeni nesil 360° dijital performans ve büyüme ajansı."
        )
        col1_title = "Hizmetlerimiz"
        services = [
            ("Performans Pazarlaması", "/hizmetler/performans-pazarlamasi/"),
            ("Google Reklamları (Ads)", "/hizmetler/google-reklamlari/"),
            ("Instagram & Meta Reklamları", "/hizmetler/instagram-reklamlari/"),
            ("Kurumsal SEO & AEO", "/hizmetler/seo/"),
            ("Web Tasarım & Yazılım", "/hizmetler/web-tasarim/"),
            ("360° Dijital Pazarlama", "/hizmetler/360-derece-dijital-pazarlama-yonetimi/"),
        ]
        col2_title = "Keşfet"
        explore = [
            ("Hakkımızda", "/hakkimizda/"),
            ("Referanslar & Başarı Hikayeleri", "/referanslar/"),
            ("Medistate — Vaka Analizi", "/referanslar/medistate/"),
            ("Summer Homes — Vaka Analizi", "/referanslar/summer-homes/"),
            ("Blog & İçgörüler", "/blog/"),
            ("İletişim", "/iletisim/"),
        ]
        col3_title = "İletişim & Ofis"
        loc_text = "İstanbul, Türkiye"
        hours_text = "Pzt – Cum · 09:00 – 18:30"
        priv_label = "Gizlilik Politikası & KVKK"
        priv_href = "/gizlilik-politikasi-ve-kullanim-sartlari/"
        copy_text = "© 2026 Roasist Dijital Pazarlama Ajansı. Tüm hakları saklıdır."

    srv_items = "".join(f'<li><a href="{href}">{html_mod.escape(lbl)}</a></li>' for lbl, href in services)
    exp_items = "".join(f'<li><a href="{href}">{html_mod.escape(lbl)}</a></li>' for lbl, href in explore)

    socials = [
        ("Instagram", "https://www.instagram.com/roasist"),
        ("LinkedIn", "https://www.linkedin.com/company/roasist"),
        ("X", "https://twitter.com/Roasistt"),
        ("Facebook", "https://www.facebook.com/roasistt"),
        ("YouTube", "https://www.youtube.com/channel/UCY3G_IU2YJ326zGwU3_YlyA"),
    ]
    soc_items = "".join(
        f'<a href="{url}" target="_blank" rel="noopener noreferrer" class="roasist-footer__social-pill">'
        f"<span>{name}</span>{EXT_ARROW_SVG}</a>"
        for name, url in socials
    )

    badges = [
        (f"{img_base}/badge-google-partner-w.svg", "Google Partner"),
        (f"{img_base}/badge-meta-partner-w.svg", "Meta Business Partner"),
        (f"{img_base}/badge-tiktok-partner-w.svg", "TikTok Marketing Partner"),
        (f"{img_base}/badge-ai-seo-w.svg", "AI SEO Partner"),
    ]
    badge_items = "".join(
        f'<div class="roasist-footer__badge-item"><img src="{src}" alt="{alt}" loading="lazy"/></div>'
        for src, alt in badges
    )

    return (
        '<div class="roasist-footer-v2">'
        '<div class="roasist-footer__cta">'
        '<div class="roasist-footer__cta-copy">'
        f'<span class="roasist-footer__eyebrow"><i></i>{html_mod.escape(eyebrow)}</span>'
        f'<h2 class="roasist-footer__cta-title">{html_mod.escape(cta_heading)}</h2>'
        "</div>"
        '<div class="roasist-footer__cta-action">'
        f'<a href="{cta_href}" class="roasist-footer__cta-btn">'
        f"<span>{html_mod.escape(cta_btn)}</span>"
        f"{EXT_ARROW_SVG}"
        "</a>"
        "</div>"
        "</div>"
        '<div class="roasist-footer__grid">'
        '<div class="roasist-footer__col roasist-footer__col--brand">'
        f'<a href="{home_href}" class="roasist-footer__brand-logo" aria-label="Roasist">'
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 820 200"><path fill="#fff" d="{ROASIST_WHITE_SVG_PATH}"></path></svg>'
        "</a>"
        f'<p class="roasist-footer__brand-desc">{html_mod.escape(brand_desc)}</p>'
        f'<div class="roasist-footer__badges">{badge_items}</div>'
        "</div>"
        '<div class="roasist-footer__col">'
        f'<h3 class="roasist-footer__col-title">{html_mod.escape(col1_title)}</h3>'
        f'<ul class="roasist-footer__nav-list">{srv_items}</ul>'
        "</div>"
        '<div class="roasist-footer__col">'
        f'<h3 class="roasist-footer__col-title">{html_mod.escape(col2_title)}</h3>'
        f'<ul class="roasist-footer__nav-list">{exp_items}</ul>'
        "</div>"
        '<div class="roasist-footer__col roasist-footer__col--contact">'
        f'<h3 class="roasist-footer__col-title">{html_mod.escape(col3_title)}</h3>'
        '<div class="roasist-footer__contact-card">'
        '<a href="mailto:info@roasist.com" class="roasist-footer__contact-mail">info@roasist.com</a>'
        '<a href="tel:+905405075350" class="roasist-footer__contact-phone">+90 540 507 53 50</a>'
        f'<p class="roasist-footer__contact-meta">{html_mod.escape(loc_text)}<span>•</span>{html_mod.escape(hours_text)}</p>'
        "</div>"
        f'<div class="roasist-footer__socials">{soc_items}</div>'
        "</div>"
        "</div>"
        '<div class="roasist-footer__bottom">'
        f'<span class="roasist-footer__copy Footer_copyrightText__f_Lte">{html_mod.escape(copy_text)}</span>'
        '<div class="roasist-footer__bottom-right Footer_copyrightTextWrap__uhQWh">'
        f'<a href="{priv_href}" class="roasist-footer__legal-link">{html_mod.escape(priv_label)}</a>'
        "</div>"
        "</div>"
        "</div>"
    )


def make_hero_title_row_ssr(label: str) -> str:
    esc_label = html_mod.escape(label)
    return (
        '<div class="roasist-hero-title-row">'
        f'<div class="roasist-hero-page-label" role="heading" aria-level="1"><span><i></i>{esc_label}</span></div>'
        f'<div class="roasist-hero-title-arrow">{ARROW_SVG_HTML}</div>'
        "</div>"
    )


def make_hero_title_row_ast(label: str) -> list:
    return [
        "$",
        "div",
        "roasist-hero-title-row",
        {
            "className": "roasist-hero-title-row",
            "children": [
                [
                    "$",
                    "div",
                    "roasist-hero-page-label",
                    {
                        "className": "roasist-hero-page-label",
                        "role": "heading",
                        "aria-level": 1,
                        "children": [
                            "$",
                            "span",
                            None,
                            {
                                "children": [
                                    ["$", "i", None, {}],
                                    label,
                                ]
                            },
                        ],
                    },
                ],
                [
                    "$",
                    "div",
                    "roasist-hero-title-arrow",
                    {
                        "className": "roasist-hero-title-arrow",
                        "dangerouslySetInnerHTML": {"__html": ARROW_SVG_HTML},
                    },
                ],
            ],
        },
    ]


def is_custom_hero_title_node(node) -> bool:
    if isinstance(node, list) and len(node) >= 4 and node[0] == "$" and isinstance(node[3], dict):
        cls = str(node[3].get("className", ""))
        if cls in ("roasist-hero-title-row", "roasist-hero-page-label"):
            return True
    return False


def prepend_title_row_to_ast_container(cont_node: list, label: str) -> bool:
    if not (isinstance(cont_node, list) and len(cont_node) >= 4 and isinstance(cont_node[3], dict)):
        return False
    ch = cont_node[3].get("children")
    if ch is None:
        ch_list = []
    elif isinstance(ch, list) and (len(ch) == 0 or ch[0] != "$"):
        ch_list = [c for c in ch if not is_custom_hero_title_node(c)]
    else:
        ch_list = [] if is_custom_hero_title_node(ch) else [ch]
    ch_list.insert(0, make_hero_title_row_ast(label))
    cont_node[3]["children"] = ch_list
    return True


def find_blog_heading_container(node):
    if isinstance(node, list):
        if (
            len(node) >= 4
            and node[0] == "$"
            and node[1] == "div"
            and isinstance(node[3], dict)
            and node[3].get("className") == "container"
        ):
            ch = node[3].get("children")
            if find_node_by_class(ch, "Heading_heading__fhmAd") is not None:
                return node
        for item in node:
            res = find_blog_heading_container(item)
            if res is not None:
                return res
    elif isinstance(node, dict):
        for v in node.values():
            res = find_blog_heading_container(v)
            if res is not None:
                return res
    return None


def mutate_flight_all_four_items(records: list, label: str | None, lang: str, is_dist: bool) -> bool:
    changed = False
    footer_inner = build_footer_inner_html(lang, is_dist)

    for rec in records:
        if rec[0] != "line" or not rec[2] or rec[2][0] not in "[{":
            continue
        try:
            ast = json.loads(rec[2])
        except Exception:
            continue

        rec_changed = False

        # Item 4: Remove Showreel text & video inside #kotaverceCta while keeping DarkThemeSwitch and dark WebGL background
        kota_cta = find_node_by_class(ast, "KotaverseCta_kotaverseCta__bBpWa")
        if kota_cta is not None and isinstance(kota_cta[3], dict):
            kch = kota_cta[3].get("children")
            if isinstance(kch, list):
                new_kch = [
                    c
                    for c in kch
                    if not (
                        isinstance(c, list)
                        and len(c) >= 4
                        and isinstance(c[3], dict)
                        and str(c[3].get("className", ""))
                        in ("KotaverseCta_text__IMtZr", "KotaverseCta_backgroundVideo__FSZyH")
                    )
                ]
                if len(new_kch) != len(kch):
                    kota_cta[3]["children"] = new_kch
                    rec_changed = True
            elif kch is None:
                is_home_page = label is None
                dts_id = "$L1e" if is_home_page else "$L1d"
                wgl_id = "$L20" if is_home_page else "$L1f"
                kota_cta[3]["children"] = [
                    ["$", dts_id, None, {}],
                    [
                        "$",
                        wgl_id,
                        None,
                        {
                            "scrollTrigger": True,
                            "scrollTarget": "#carousel",
                            "variation": 4,
                            "scrollTriggerOpacity": 0,
                            "darkBackground": True,
                        },
                    ],
                ]
                kota_cta[3].pop("aria-hidden", None)
                rec_changed = True

        # Item 1: Redesign Footer_footer__pQtti interior while keeping outer <footer class="Footer_footer__pQtti" data-theme="dark">
        footer_node = find_node_by_class(ast, "Footer_footer__pQtti")
        if footer_node is not None and isinstance(footer_node[3], dict):
            footer_node[3]["children"] = [
                "$",
                "div",
                "roasist-footer-container",
                {
                    "className": "container roasist-footer-container",
                    "dangerouslySetInnerHTML": {"__html": footer_inner},
                },
            ]
            rec_changed = True

        # Items 2 & 3: Move page title row + rotating arrow to the very top of the Hero container
        if label:
            # 1) About (Hero_hero__zbooM), References (Hero_hero__Oyf4n), Services (Hero_hero__18Xqo), Contact (Hero_hero___ImMv), Blog/CaseStudy Detail (Hero_hero__mn1R_), Privacy (Content_content__6vnSh)
            for hero_cls in (
                "Hero_hero__zbooM",
                "Hero_hero__Oyf4n",
                "Hero_hero__18Xqo",
                "Hero_hero___ImMv",
                "Hero_hero__mn1R_",
                "Content_content__6vnSh",
            ):
                hero_node = find_node_by_class(ast, hero_cls)
                if hero_node is not None:
                    cont = find_node_by_class(hero_node, "container")
                    if cont is not None and prepend_title_row_to_ast_container(cont, label):
                        rec_changed = True

                    # Clean up any previously injected .roasist-hero-page-label inside sub-containers
                    for sub_cls in ("Hero_bottom__5uvI_", "Hero_bottom___aF_2", "Hero_left__0LdJX", "prose"):
                        sub_node = find_node_by_class(hero_node, sub_cls)
                        if sub_node is not None and isinstance(sub_node[3], dict):
                            sch = sub_node[3].get("children")
                            if isinstance(sch, list):
                                new_sch = [c for c in sch if not is_custom_hero_title_node(c)]
                                if len(new_sch) != len(sch):
                                    sub_node[3]["children"] = new_sch
                                    rec_changed = True

            # 2) Blog Index / Category / Tag pages (Heading_heading__fhmAd)
            blog_cont = find_blog_heading_container(ast)
            if blog_cont is not None and prepend_title_row_to_ast_container(blog_cont, label):
                rec_changed = True

        if rec_changed:
            rec[2] = json.dumps(ast, ensure_ascii=False, separators=(",", ":"))
            changed = True

    return changed


def mutate_ssr_all_four_items(html: str, label: str | None, lang: str, is_dist: bool) -> str:
    # Split after </head> and before first self.__next_f.push so we ONLY mutate body SSR markup
    m_head = re.search(r"</head>", html, flags=re.I)
    head_end = m_head.end() if m_head else 0
    head_prefix = html[:head_end]
    rest = html[head_end:]

    m_push = re.search(r"<script>self\.__next_f\.push", rest)
    if m_push:
        ssr = rest[: m_push.start()]
        tail = rest[m_push.start() :]
    else:
        ssr, tail = rest, ""

    # Item 4: Remove Showreel text & backgroundVideo inside #kotaverceCta while keeping DarkThemeSwitch & WebGL container
    ssr = re.sub(
        r'<section class="KotaverseCta_kotaverseCta__bBpWa"[^>]*id="kotaverceCta"[^>]*>.*?</section>',
        (
            '<section class="KotaverseCta_kotaverseCta__bBpWa" id="kotaverceCta">'
            '<div class="DarkThemeSwitch_cover__hn_xc"></div>'
            '<div class="webgl-background_container__Ojc1v" data-background="4" data-dark-background="true" data-position="fixed" data-noise="true"></div>'
            "</section>"
        ),
        ssr,
        flags=re.S,
    )

    # Item 1: Update <footer class="Footer_footer__pQtti" data-theme="dark"> interior in SSR
    footer_inner = build_footer_inner_html(lang, is_dist)
    ssr = re.sub(
        r'(<footer class="Footer_footer__pQtti"[^>]*>).*?(</footer>)',
        lambda m: f'{m.group(1)}<div class="container roasist-footer-container">{footer_inner}</div>{m.group(2)}',
        ssr,
        count=1,
        flags=re.S,
    )

    # Items 2 & 3: Move .roasist-hero-title-row to the very top of Hero .container in SSR
    if label:
        title_row_html = make_hero_title_row_ssr(label)

        # Remove any existing .roasist-hero-title-row or .roasist-hero-page-label in SSR
        ssr = re.sub(
            r'<div class="roasist-hero-title-row"><div class="roasist-hero-page-label"[^>]*>.*?</div><div class="roasist-hero-title-arrow">.*?</div></div>',
            "",
            ssr,
            flags=re.S,
        )
        ssr = re.sub(
            r'<(?:h1|div) class="roasist-hero-page-label"[^>]*><span><i></i>.*?</span></(?:h1|div)>',
            "",
            ssr,
            flags=re.S,
        )

        # Prepend title_row_html right after <div class="container"> inside any of the 6 hero sections
        placed = False
        for hero_cls in (
            "Hero_hero__zbooM",
            "Hero_hero__Oyf4n",
            "Hero_hero__18Xqo",
            "Hero_hero___ImMv",
            "Hero_hero__mn1R_",
            "Content_content__6vnSh",
        ):
            pat = rf'(<(?:section|div) class="{hero_cls}"[^>]*><div class="container">)'
            if re.search(pat, ssr):
                ssr = re.sub(pat, lambda m: f"{m.group(1)}{title_row_html}", ssr, count=1)
                placed = True
                break

        if not placed and 'class="Heading_heading__fhmAd"' in ssr:
            ssr = re.sub(
                r'(<div class="container">)(<h1 class="Heading_heading__fhmAd">)',
                lambda m: f"{m.group(1)}{title_row_html}{m.group(2)}",
                ssr,
                count=1,
            )

    return head_prefix + ssr + tail


FOUR_ITEMS_CSS = """
/* === FOUR UI IMPROVEMENTS (Footer v2, Top Page Title Row, Scroll Arrow Rotation, Hide Showreel) === */

/* Item 4: Remove Showreel content inside #kotaverceCta while keeping its DarkThemeSwitch & dark WebGL background active for Footer */
#kotaverceCta,
.KotaverseCta_kotaverseCta__bBpWa {
  height: 0 !important;
  min-height: 0 !important;
  max-height: 0 !important;
  margin: 0 !important;
  padding: 0 !important;
  overflow: visible !important;
  opacity: 1 !important;
  visibility: visible !important;
  border: none !important;
}
.KotaverseCta_text__IMtZr,
.KotaverseCta_backgroundVideo__FSZyH {
  display: none !important;
}

/* Item 2: Top Page Title Row (.roasist-hero-title-row) at the very top of all non-home pages */
.roasist-hero-title-row {
  grid-column: 1 / -1 !important;
  width: 100% !important;
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  gap: 1.5rem !important;
  margin: 0 0 clamp(2rem, 3.6vw, 3.25rem) 0 !important;
  padding: 0 !important;
  border-bottom: none !important;
  position: relative !important;
  z-index: 4 !important;
  order: -10 !important;
}
.roasist-hero-title-row .roasist-hero-page-label {
  position: static !important;
  margin: 0 !important;
  padding: 0 !important;
  font-family: var(--syne) !important;
  font-size: clamp(1.35rem, 2.2vw, 2.15rem) !important;
  font-weight: 700 !important;
  text-transform: lowercase !important;
  letter-spacing: calc(-30em / 1000) !important;
  line-height: 1 !important;
  color: #000000 !important;
  display: block !important;
}
body.dark .roasist-hero-title-row .roasist-hero-page-label {
  color: #ffffff !important;
}
.roasist-hero-title-row .roasist-hero-page-label > span {
  display: inline-flex !important;
  align-items: baseline !important;
  line-height: 1 !important;
}
.roasist-hero-title-row .roasist-hero-page-label i {
  display: inline-block !important;
  width: 1px !important;
  height: 0.5em !important;
  background-color: currentColor !important;
  margin-right: 0.25em !important;
  flex-shrink: 0 !important;
  font-style: normal !important;
}
.roasist-hero-title-arrow {
  display: flex !important;
  align-items: center !important;
  justify-content: flex-end !important;
  flex-shrink: 0 !important;
  width: clamp(1.5rem, 2.3vw, 2.35rem) !important;
  height: clamp(1.5rem, 2.3vw, 2.35rem) !important;
  color: #000000 !important;
}
body.dark .roasist-hero-title-arrow {
  color: #ffffff !important;
}
.roasist-hero-title-arrow svg {
  width: 100% !important;
  height: 100% !important;
  display: block !important;
  fill: currentColor !important;
}
@media (max-width: 768px) {
  .roasist-hero-title-row {
    gap: 0.75rem !important;
    margin: 0 0 1.35rem 0 !important;
  }
  .roasist-hero-title-row .roasist-hero-page-label {
    font-size: clamp(1.1rem, 4.4vw, 1.35rem) !important;
  }
  .roasist-hero-title-arrow {
    width: clamp(1.15rem, 4.2vw, 1.4rem) !important;
    height: clamp(1.15rem, 4.2vw, 1.4rem) !important;
  }
}

/* Hide legacy bottom/displaced hero page labels and arrows so only the top row shows */
.Hero_bottom__pLxrT,
.Hero_bottom___aF_2,
.Hero_bottom__ktiOH > h1,
.Hero_bottom__ktiOH > .Hero_arrow__lxSeM,
.Hero_bottom__5uvI_ > .Hero_arrow__CVNIo,
.Hero_bottom__5uvI_ > .roasist-hero-page-label,
.Hero_left__0LdJX > .roasist-hero-page-label,
.Content_content__6vnSh .prose > .roasist-hero-page-label,
.Content_arrow__vjgxh {
  display: none !important;
}

/* Normalize hero top spacing across all 7 non-home templates so .roasist-hero-title-row sits at the very top */
.Hero_hero__zbooM,
.Hero_hero__18Xqo,
.Hero_hero__Oyf4n,
.Hero_hero___ImMv {
  padding-top: clamp(7.5rem, 12vh, 9.75rem) !important;
  padding-bottom: clamp(2.5rem, 4vh, 4rem) !important;
  height: auto !important;
  min-height: auto !important;
  max-height: none !important;
  margin-bottom: 0 !important;
}
.Hero_hero__zbooM .container,
.Hero_hero__18Xqo .container,
.Hero_hero__Oyf4n .container,
.Hero_hero___ImMv .container {
  padding-top: 0 !important;
}
.Hero_hero__zbooM h2,
.Hero_hero___ImMv h2,
.Hero_hero__Oyf4n h2 {
  margin: 0.5rem 0 clamp(2rem, 3.5vh, 3.25rem) 0 !important;
}
.Hero_hero__18Xqo .split-line-mask,
.Hero_hero__zbooM .split-line-mask,
.Hero_hero__Oyf4n .split-line-mask,
.Hero_hero___ImMv .split-line-mask {
  overflow: visible !important;
}
.Hero_hero__18Xqo .split-line,
.Hero_hero__18Xqo .FadeIn_container__bjQVL {
  transform: none !important;
  opacity: 1 !important;
}
.Hero_hero__mn1R_ {
  margin: clamp(7.5rem, 12vh, 9.75rem) 0 clamp(2.5rem, 5vh, 4rem) 0 !important;
}
.Content_content__6vnSh {
  padding: clamp(7.5rem, 12vh, 9.75rem) 0 5rem 0 !important;
}
.container:has(> .Heading_heading__fhmAd) {
  padding-top: clamp(7.5rem, 12vh, 9.75rem) !important;
}
.Heading_heading__fhmAd {
  margin: 0.5rem 0 clamp(2.5rem, 4vw, 3.75rem) 0 !important;
}

/* Item 3: Scroll-Driven Rotating Arrow Animation (45deg left -> -45deg down) & Heading Alignment Fixes */
.roasist-hero-title-arrow svg,
.AnimatedArrow_innerArrow__6mwTB svg,
.ServicesHeading_arrow__L7E0F,
.Partners_arrowWrapper__Xq8Wc svg,
.Approach_arrow__3EkCM svg {
  transform: rotate(var(--roasist-arrow-rot, 45deg)) !important;
  transform-origin: 50% 50% !important;
  will-change: transform !important;
}
/* Neutralize GSAP wrapper transforms/opacities so our scroll-scrubbed SVG rotation controls all arrows uniformly */
.AnimatedArrow_animatedArrow__Q4v7Q,
.AnimatedArrow_innerArrow__6mwTB,
.Partners_arrowWrapper__Xq8Wc .FadeInRotate_container__QE9u9 {
  opacity: 1 !important;
  visibility: visible !important;
  transform: none !important;
}
.Approach_arrow__3EkCM,
.Partners_partners__jBo8y:has(.Partners_introText__3_Pu8) .Partners_arrowWrapper__Xq8Wc {
  display: none !important;
}
h2.Partners_heading__AOTNV {
  width: auto !important;
  flex: 1 1 auto !important;
  min-width: 0 !important;
}
.Partners_heading__AOTNV,
.Partners_arrowWrapper__Xq8Wc {
  font-size: clamp(2.2rem, 6.5vw, 6.6rem) !important;
}
.Partners_heading__AOTNV.Partners_bottom__5DSXe {
  padding-left: 6.5% !important;
}
.Partners_headingInner__vdhDe,
.Partners_bottom__5DSXe {
  white-space: nowrap !important;
}
.Partners_bottom__5DSXe {
  display: flex !important;
  flex-direction: row !important;
  align-items: flex-end !important;
  justify-content: space-between !important;
  width: 100% !important;
  gap: 2rem !important;
}
.LargeHeading_headingOuter__i9qcd .split-word {
  overflow: visible !important;
}
.LargeHeading_headingOuter__i9qcd .split-char {
  transform: none !important;
  opacity: 1 !important;
}
body.roasist-footer-in-view .FloatingStartButton_linkContainer__eZz7z,
body.roasist-footer-in-view [class*="FloatingStartButton_"] {
  opacity: 0 !important;
  visibility: hidden !important;
  pointer-events: none !important;
}

/* Animated Gradient Wave on Ölçülebilir Sonuçlar (StatisticsPanel_heading) */
@keyframes roasist-stat-rainbow {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
.StatisticsPanel_heading__UrLlt,
[class*="StatisticsPanel_heading__"] {
  background-image: linear-gradient(90deg, #7602FF, #00D2FF, #EC4899, #7602FF) !important;
  background-size: 200% 200% !important;
  -webkit-background-clip: text !important;
  background-clip: text !important;
  color: transparent !important;
  animation: roasist-stat-rainbow 3s ease-in-out infinite !important;
}

/* Item 1: Redesigned Footer (.roasist-footer-v2) inside untouched dark WebGL Footer_footer__pQtti */
.Footer_footer__pQtti .roasist-footer-container {
  display: block !important;
  padding-top: clamp(3.5rem, 6vw, 5.5rem) !important;
  padding-bottom: clamp(2.5rem, 4vw, 3.75rem) !important;
}
.roasist-footer-v2 {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: clamp(3rem, 5vw, 4.5rem);
  color: #f8fafc;
}
.roasist-footer__cta {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 2rem;
  padding-bottom: clamp(2.5rem, 4vw, 3.5rem);
  border-bottom: 1px solid rgba(255, 255, 255, 0.14);
  flex-wrap: wrap;
}
.roasist-footer__cta-copy {
  max-width: 46rem;
  display: flex;
  flex-direction: column;
  gap: 0.9rem;
}
.roasist-footer__eyebrow {
  display: inline-flex;
  align-items: center;
  font-family: var(--syne);
  font-size: clamp(1rem, 1.35vw, 1.25rem);
  font-weight: 700;
  text-transform: lowercase;
  letter-spacing: -0.02em;
  color: rgba(255, 255, 255, 0.85);
}
.roasist-footer__eyebrow i {
  display: inline-block;
  width: 1px;
  height: 0.65em;
  background-color: currentColor;
  margin-right: 0.35em;
}
.roasist-footer__cta-title {
  margin: 0;
  font-size: clamp(1.85rem, 3.4vw, 3.1rem);
  font-weight: 500;
  line-height: 1.12;
  letter-spacing: -0.025em;
  color: #ffffff;
}
.roasist-footer__cta-action {
  flex-shrink: 0;
}
.roasist-footer__cta-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1.05rem 1.85rem;
  border-radius: 9999px;
  background: #ffffff;
  color: #0f172a !important;
  font-size: 1rem;
  font-weight: 600;
  letter-spacing: -0.01em;
  text-decoration: none !important;
  transition: transform 160ms cubic-bezier(0.22, 1, 0.36, 1), background-color 160ms cubic-bezier(0.22, 1, 0.36, 1);
}
.roasist-footer__cta-btn:hover {
  transform: translateY(-2px);
  background: #f1f5f9;
}
.roasist-footer__ext-icon {
  width: 0.78rem;
  height: 0.78rem;
  flex-shrink: 0;
  transition: transform 160ms cubic-bezier(0.22, 1, 0.36, 1);
}
.roasist-footer__cta-btn:hover .roasist-footer__ext-icon,
.roasist-footer__social-pill:hover .roasist-footer__ext-icon {
  transform: translate(2px, -2px);
}
.roasist-footer__grid {
  display: grid;
  grid-template-columns: 1.45fr 1fr 1fr 1.2fr;
  gap: clamp(2rem, 3.5vw, 3.5rem);
  align-items: start;
}
.roasist-footer__col {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}
.roasist-footer__brand-logo {
  display: inline-block;
  width: clamp(9.5rem, 13vw, 12.5rem);
}
.roasist-footer__brand-logo svg {
  width: 100%;
  height: auto;
  display: block;
}
.roasist-footer__brand-desc {
  margin: 0;
  font-size: 0.95rem;
  line-height: 1.65;
  color: rgba(248, 250, 252, 0.76);
  max-width: 34ch;
}
.roasist-footer__badges {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.65rem;
  margin-top: 0.35rem;
}
.roasist-footer__badge-item {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.45rem 0.75rem;
  border-radius: 0.65rem;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.12);
}
.roasist-footer__badge-item img {
  height: 1.35rem;
  width: auto;
  display: block;
  opacity: 0.92;
}
.roasist-footer__col-title {
  margin: 0;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: rgba(248, 250, 252, 0.56);
}
.roasist-footer__nav-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
.roasist-footer__nav-list li a {
  color: rgba(248, 250, 252, 0.88);
  text-decoration: none;
  font-size: 0.96rem;
  line-height: 1.4;
  transition: color 150ms cubic-bezier(0.22, 1, 0.36, 1), transform 150ms cubic-bezier(0.22, 1, 0.36, 1);
  display: inline-block;
}
.roasist-footer__nav-list li a:hover {
  color: #ffffff;
  transform: translateX(3px);
}
.roasist-footer__contact-card {
  display: flex;
  flex-direction: column;
  gap: 0.55rem;
  padding: 1.25rem 1.35rem;
  border-radius: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.12);
}
.roasist-footer__contact-mail {
  font-family: var(--syne);
  font-size: clamp(1.1rem, 1.5vw, 1.35rem);
  font-weight: 700;
  color: #ffffff !important;
  text-decoration: none;
  letter-spacing: -0.02em;
}
.roasist-footer__contact-phone {
  font-size: 1.02rem;
  font-weight: 500;
  font-variant-numeric: tabular-nums;
  color: rgba(248, 250, 252, 0.9) !important;
  text-decoration: none;
}
.roasist-footer__contact-meta {
  margin: 0.15rem 0 0 0;
  font-size: 0.84rem;
  color: rgba(248, 250, 252, 0.62);
  display: flex;
  flex-wrap: wrap;
  gap: 0.45rem;
  align-items: center;
  font-variant-numeric: tabular-nums;
}
.roasist-footer__socials {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}
.roasist-footer__social-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.45rem 0.85rem;
  border-radius: 9999px;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.12);
  color: rgba(248, 250, 252, 0.9) !important;
  font-size: 0.84rem;
  font-weight: 500;
  text-decoration: none !important;
  transition: background-color 150ms cubic-bezier(0.22, 1, 0.36, 1), border-color 150ms cubic-bezier(0.22, 1, 0.36, 1);
}
.roasist-footer__social-pill:hover {
  background: rgba(255, 255, 255, 0.14);
  border-color: rgba(255, 255, 255, 0.28);
  color: #ffffff !important;
}
.roasist-footer__bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1.25rem;
  padding-top: 1.75rem;
  border-top: 1px solid rgba(255, 255, 255, 0.14);
  font-size: 0.88rem;
  color: rgba(248, 250, 252, 0.68);
  font-variant-numeric: tabular-nums;
}
.roasist-footer__bottom-right {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 1.25rem;
}
.roasist-footer__legal-link {
  color: rgba(248, 250, 252, 0.78) !important;
  text-decoration: none;
  transition: color 150ms cubic-bezier(0.22, 1, 0.36, 1);
}
.roasist-footer__legal-link:hover {
  color: #ffffff !important;
}
@media (max-width: 1024px) {
  .roasist-footer__grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}
@media (max-width: 640px) {
  .roasist-footer__grid {
    grid-template-columns: 1fr;
  }
  .roasist-footer__cta {
    align-items: flex-start;
  }
}
"""

ARROW_ROTATOR_SCRIPT = """<script id="roasist-arrow-rotator">(function(){
  function clamp(v, min, max) { return v < min ? min : (v > max ? max : v); }
  function updateArrows() {
    var sy = window.scrollY || window.pageYOffset || 0;
    var vh = window.innerHeight || 900;

    // 1. Top Page Title Row arrows: 45deg (pointing straight left <- at page title) at top -> 0deg (bottom-left ↙) on scroll
    var heroArrows = document.querySelectorAll('.roasist-hero-title-arrow svg');
    var heroProg = clamp((sy - 2) / 105, 0, 1);
    var heroAngle = 45 - 45 * heroProg;
    for (var i = 0; i < heroArrows.length; i++) {
      heroArrows[i].style.setProperty('--roasist-arrow-rot', heroAngle.toFixed(2) + 'deg');
    }

    // 2. Section Heading arrows ("360° HİZMETLER", "MARKA ORTAKLARIMIZ", "Özgün Yaklaşım", "Güçlü Markalar")
    var secArrows = document.querySelectorAll(
      '.AnimatedArrow_innerArrow__6mwTB svg, svg.ServicesHeading_arrow__L7E0F, .Partners_arrowWrapper__Xq8Wc svg, .Approach_arrow__3EkCM svg'
    );
    var startY = vh * 0.85;
    var endY = vh * 0.46;
    var span = Math.max(1, startY - endY);
    for (var j = 0; j < secArrows.length; j++) {
      var el = secArrows[j];
      var r = el.getBoundingClientRect();
      var prog = clamp((startY - r.top) / span, 0, 1);
      var angle = 45 - 45 * prog;
      el.style.setProperty('--roasist-arrow-rot', angle.toFixed(2) + 'deg');
    }

    // 3. Hide floating CTA button when Footer enters the viewport so it never overlaps footer links/language switcher
    var ftr = document.querySelector('footer.Footer_footer__pQtti');
    var flt = document.querySelector('.FloatingStartButton_linkContainer__eZz7z');
    if (ftr) {
      var fr = ftr.getBoundingClientRect();
      var inView = fr.top < vh * 0.96;
      if (inView) {
        document.body.classList.add('roasist-footer-in-view');
        if (flt) {
          flt.style.setProperty('opacity', '0', 'important');
          flt.style.setProperty('pointer-events', 'none', 'important');
        }
      } else {
        document.body.classList.remove('roasist-footer-in-view');
        if (flt) {
          flt.style.removeProperty('opacity');
          flt.style.removeProperty('pointer-events');
        }
      }
    }
  }

  var ticking = false;
  function onScroll() {
    if (!ticking) {
      ticking = true;
      window.requestAnimationFrame(function() {
        ticking = false;
        updateArrows();
      });
    }
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll, { passive: true });
  document.addEventListener('DOMContentLoaded', function() {
    updateArrows();
    setTimeout(updateArrows, 300);
    setTimeout(updateArrows, 1000);
  });
  updateArrows();
})();</script>"""


def inject_css_and_arrow_script(html: str) -> str:
    # Remove any previous FOUR_ITEMS_CSS block inside <style data-roasist-ui-css>
    if "<style data-roasist-ui-css>" in html:
        html = re.sub(
            r"\n?/\* === FOUR UI IMPROVEMENTS.*?(?=</style>)",
            "",
            html,
            flags=re.S,
        )
        html = re.sub(
            r"(<style data-roasist-ui-css>.*?)(</style>)",
            lambda m: f"{m.group(1)}{FOUR_ITEMS_CSS}{m.group(2)}",
            html,
            count=1,
            flags=re.S,
        )

    # Remove any previous #roasist-arrow-rotator script and inject before </body>
    html = re.sub(
        r'<script id="roasist-arrow-rotator">.*?</script>',
        "",
        html,
        flags=re.S,
    )
    if "</body>" in html:
        html = html.replace("</body>", f"{ARROW_ROTATOR_SCRIPT}</body>", 1)
    else:
        html += ARROW_ROTATOR_SCRIPT

    return html


def process_all_html_files():
    total = 0
    for base_name in ("public", "dist"):
        is_dist = base_name == "dist"
        base_dir = os.path.join(ROOT, base_name)
        candidates = sorted(glob.glob(os.path.join(base_dir, "**", "*.html"), recursive=True))
        for fp in candidates:
            rel = os.path.relpath(fp, base_dir)
            if rel.startswith("_next/"):
                continue
            route = get_route_for_file(fp, base_dir)
            lang = "en" if (route == "/en" or route.startswith("/en/")) else "tr"
            label = get_page_label_for_route(route)

            with open(fp, "r", encoding="utf-8") as f:
                html = f.read()

            if "Footer_footer__pQtti" not in html:
                continue

            html = mutate_ssr_all_four_items(html, label, lang, is_dist)
            html = rewrite_flight_in_html(
                html,
                lambda records, lbl=label, lg=lang, dst=is_dist: mutate_flight_all_four_items(
                    records, lbl, lg, dst
                ),
            )
            html = inject_css_and_arrow_script(html)

            with open(fp, "w", encoding="utf-8") as f:
                f.write(html)
            total += 1

    print(f"[FOUR UI IMPROVEMENTS] Updated {total} HTML files across public/ and dist/")


if __name__ == "__main__":
    process_all_html_files()
