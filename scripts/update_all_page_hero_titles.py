#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Standardizes the hero page-name indicator across all non-homepage pages in public/ and dist/
to match the exact `/hakkimizda/` ("| hakkımızda") format:
  - Font: var(--syne), font-size: var(--fs-60), lowercase, letter-spacing: -0.03em
  - Leading vertical bar: <i></i> (1px wide, 0.5em tall, margin-right: 0.25em)
  - Updates both static SSR HTML and Next.js React Flight JSON AST with 100% parity
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

HERO_PAGE_LABEL_CSS = """
/* Unified "| sayfa ismi" Hero Page Title Format (matching /hakkimizda/) */
.roasist-hero-page-label,
.Hero_hero__18Xqo h1.roasist-hero-page-label,
.Hero_hero___ImMv h1.roasist-hero-page-label,
.Content_content__6vnSh .prose h1.roasist-hero-page-label {
  position: static !important;
  top: auto !important;
  left: auto !important;
  right: auto !important;
  bottom: auto !important;
  transform: none !important;
  width: auto !important;
  max-width: 100% !important;
  height: auto !important;
  padding: 0 !important;
  font-family: var(--syne) !important;
  font-size: var(--fs-60) !important;
  font-weight: 700 !important;
  text-transform: lowercase !important;
  letter-spacing: calc(-30em / 1000) !important;
  line-height: 1 !important;
  color: #000000 !important;
  margin: 0 !important;
  z-index: 2 !important;
  display: block !important;
}
body.dark .roasist-hero-page-label,
body.dark .Hero_hero__18Xqo h1.roasist-hero-page-label,
body.dark .Hero_hero___ImMv h1.roasist-hero-page-label,
body.dark .Content_content__6vnSh .prose h1.roasist-hero-page-label {
  color: #ffffff !important;
}
.roasist-hero-page-label::before,
.Hero_hero__18Xqo h1.roasist-hero-page-label::before {
  display: none !important;
  content: none !important;
}
.roasist-hero-page-label > span,
.Hero_hero__18Xqo h1.roasist-hero-page-label > span,
.Hero_hero___ImMv h1.roasist-hero-page-label > span,
.Content_content__6vnSh .prose h1.roasist-hero-page-label > span {
  display: flex !important;
  align-items: baseline !important;
  line-height: 1 !important;
}
.roasist-hero-page-label i,
.Hero_hero__18Xqo h1.roasist-hero-page-label i,
.Hero_hero___ImMv h1.roasist-hero-page-label i,
.Content_content__6vnSh .prose h1.roasist-hero-page-label i {
  display: block !important;
  width: 1px !important;
  height: 0.5em !important;
  background-color: currentColor !important;
  margin-right: 0.25em !important;
  flex-shrink: 0 !important;
  font-style: normal !important;
}
@media (min-width: 769px) {
  .Hero_bottom__5uvI_ h1.roasist-hero-page-label {
    grid-column: 1 / -1 !important;
    margin: clamp(2rem, 3.4vw, 3.25rem) 0 clamp(1.75rem, 2.6vw, 2.5rem) 0 !important;
  }
}
@media (max-width: 768px) {
  .Hero_bottom__5uvI_ h1.roasist-hero-page-label {
    order: 2 !important;
    width: calc(100% - 4rem) !important;
    margin: 2rem 0 0 0 !important;
    align-self: flex-end !important;
  }
  .Hero_bottom__5uvI_ .Hero_arrow__CVNIo {
    order: 3 !important;
    width: auto !important;
    margin-top: 2rem !important;
    margin-left: auto !important;
    align-self: flex-end !important;
  }
}
.Hero_hero___ImMv {
  height: auto !important;
  min-height: 76svh !important;
  margin-bottom: 2rem !important;
  padding-bottom: 2rem !important;
}
.Hero_bottom___aF_2 {
  position: static !important;
  transform: none !important;
  display: grid !important;
  grid-template-columns: repeat(12, 1fr) !important;
  grid-column: span 12 !important;
  align-items: baseline !important;
  gap: 0.75rem !important;
  margin: clamp(3rem, 5vw, 5.5rem) 0 0 0 !important;
}
.Hero_bottom___aF_2 h1.roasist-hero-page-label {
  grid-column: 1 / span 11 !important;
}
.Hero_bottom___aF_2 .Hero_arrow__k_3kI {
  grid-column: 12 / span 1 !important;
  display: flex !important;
  justify-content: flex-end !important;
}
.Heading_heading__fhmAd {
  margin: calc(8vh + 5rem) 0 clamp(2.25rem, 3.8vw, 3.5rem) !important;
}
.Heading_heading__fhmAd + .roasist-hero-page-label {
  grid-column: 1 / -1 !important;
  margin: 0 0 clamp(3.25rem, 5.5vh, 5rem) 0 !important;
}
.Hero_left__0LdJX > .roasist-hero-page-label {
  margin: clamp(2rem, 3.2vw, 2.75rem) 0 0.5rem 0 !important;
}
.Content_content__6vnSh .prose > h1.roasist-hero-page-label {
  margin: 0 0 clamp(2.5rem, 4vw, 3.75rem) 0 !important;
}
.LineByLine_headingOuter__JmusT .split-line-mask,
.LineByLine_headingOuter__JmusT .split-line {
  padding-bottom: 0.16em !important;
  margin-bottom: -0.16em !important;
}
"""


def get_page_label_for_route(route: str) -> str | None:
    norm = route if route.endswith("/") else route + "/"
    if norm in ("/", "/en/"):
        return None
    if norm in ROUTE_PAGE_LABELS:
        return ROUTE_PAGE_LABELS[norm]
    if norm.startswith("/blog/") or norm.startswith("/en/blog/"):
        return "blog"
    return None


def make_label_ast_node(tag: str, label: str) -> list:
    return [
        "$",
        tag,
        None,
        {
            "className": "roasist-hero-page-label",
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
    ]


def find_blog_heading_container(node):
    """Finds the <div class="container"> parent of Heading_heading__fhmAd in the Flight AST."""
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


def mutate_flight_for_page_label(records: list, label: str) -> bool:
    changed = False
    for rec in records:
        if rec[0] != "line" or not rec[2] or rec[2][0] not in "[{":
            continue
        try:
            ast = json.loads(rec[2])
        except Exception:
            continue

        rec_changed = False

        # 1. About (Hero_hero__zbooM) or References (Hero_hero__Oyf4n)
        for cls in ("Hero_hero__zbooM", "Hero_hero__Oyf4n"):
            hero_node = find_node_by_class(ast, cls)
            if hero_node is not None:
                raw_json = json.dumps(hero_node, ensure_ascii=False)
                new_raw = re.sub(
                    r'"__html":\s*"\\u003ci>\\u003c/i>[^"]*"|"__html":\s*"<i></i>[^"]*"',
                    f'"__html":"<i></i>{label}"',
                    raw_json,
                )
                if new_raw != raw_json:
                    new_hero = json.loads(new_raw)
                    hero_node.clear()
                    hero_node.extend(new_hero)
                    rec_changed = True

        # 2. Service pages (Hero_hero__18Xqo)
        srv_hero = find_node_by_class(ast, "Hero_hero__18Xqo")
        if srv_hero is not None and isinstance(srv_hero[3], dict):
            ch = srv_hero[3].get("children")
            if isinstance(ch, list):
                new_ch = [
                    c
                    for c in ch
                    if not (isinstance(c, list) and len(c) >= 2 and c[0] == "$" and c[1] == "h1")
                ]
                if len(new_ch) != len(ch):
                    srv_hero[3]["children"] = new_ch
                    rec_changed = True
            bottom_node = find_node_by_class(srv_hero, "Hero_bottom__5uvI_")
            if bottom_node is not None and isinstance(bottom_node[3], dict):
                bch = bottom_node[3].get("children")
                if isinstance(bch, list):
                    bch = [
                        c
                        for c in bch
                        if not (
                            isinstance(c, list)
                            and len(c) >= 4
                            and c[0] == "$"
                            and isinstance(c[3], dict)
                            and c[3].get("className") == "roasist-hero-page-label"
                        )
                    ]
                    bch.insert(1, make_label_ast_node("h1", label))
                    bottom_node[3]["children"] = bch
                    rec_changed = True

        # 3. Contact pages (Hero_hero___ImMv / Hero_bottom___aF_2)
        contact_bottom = find_node_by_class(ast, "Hero_bottom___aF_2")
        if contact_bottom is not None and isinstance(contact_bottom[3], dict):
            arrow_node = find_node_by_class(contact_bottom, "Hero_arrow__k_3kI")
            if arrow_node is not None:
                contact_bottom[3]["children"] = [
                    make_label_ast_node("h1", label),
                    arrow_node,
                ]
                rec_changed = True

        # 4. Blog Index / Category / Tag pages (Heading_heading__fhmAd)
        blog_cont = find_blog_heading_container(ast)
        if blog_cont is not None and isinstance(blog_cont[3], dict):
            h1_node = find_node_by_class(blog_cont, "Heading_heading__fhmAd")
            if h1_node is not None:
                blog_cont[3]["children"] = [
                    h1_node,
                    make_label_ast_node("div", label),
                ]
                rec_changed = True

        # 5. Blog Post Detail pages (Hero_left__0LdJX)
        blog_post_left = find_node_by_class(ast, "Hero_left__0LdJX")
        if blog_post_left is not None and isinstance(blog_post_left[3], dict):
            lch = blog_post_left[3].get("children")
            if isinstance(lch, list):
                lch = [
                    c
                    for c in lch
                    if not (
                        isinstance(c, list)
                        and len(c) >= 4
                        and c[0] == "$"
                        and isinstance(c[3], dict)
                        and c[3].get("className") == "roasist-hero-page-label"
                    )
                ]
                lch.append(make_label_ast_node("div", label))
                blog_post_left[3]["children"] = lch
                rec_changed = True

        # 6. Privacy Policy pages (Content_content__6vnSh)
        priv_sec = find_node_by_class(ast, "Content_content__6vnSh")
        if priv_sec is not None:
            prose_node = find_node_by_class(priv_sec, "prose")
            if prose_node is not None and isinstance(prose_node[3], dict):
                pch = prose_node[3].get("children")
                if isinstance(pch, list) and len(pch) >= 1:
                    pch[0] = make_label_ast_node("h1", label)
                    prose_node[3]["children"] = pch
                    rec_changed = True

        if rec_changed:
            rec[2] = json.dumps(ast, ensure_ascii=False, separators=(",", ":"))
            changed = True

    return changed


def mutate_ssr_html_for_page_label(html: str, label: str) -> str:
    esc_label = html_mod.escape(label)
    h1_label_html = f'<h1 class="roasist-hero-page-label"><span><i></i>{esc_label}</span></h1>'
    div_label_html = f'<div class="roasist-hero-page-label"><span><i></i>{esc_label}</span></div>'

    # Clean up any previous .roasist-hero-page-label tags in SSR
    html = re.sub(
        r'<(?:h1|div) class="roasist-hero-page-label"><span><i></i>.*?</span></(?:h1|div)>',
        "",
        html,
        flags=re.S,
    )

    # 1. About & References
    if "Hero_hero__zbooM" in html or "Hero_hero__Oyf4n" in html:
        html = re.sub(
            r"(<i></i>)([^<]+)(</span></div></span></h1>)",
            lambda m: f"{m.group(1)}{esc_label}{m.group(3)}",
            html,
            count=1,
        )

    # 2. Service pages (Hero_hero__18Xqo)
    if '<section class="Hero_hero__18Xqo">' in html:
        html = re.sub(
            r'(<section class="Hero_hero__18Xqo">)<h1>.*?</h1>(<div class="container">)',
            r"\1\2",
            html,
            count=1,
            flags=re.S,
        )
        html = re.sub(
            r'(<div class="Hero_bottom__5uvI_"><h3 class="Hero_introText__HLM02">.*?</h3>)(<nav class="DiscoverMore_discoverMore__hYPtP")',
            lambda m: f"{m.group(1)}{h1_label_html}{m.group(2)}",
            html,
            count=1,
            flags=re.S,
        )

    # 3. Contact pages (Hero_hero___ImMv)
    if '<div class="Hero_bottom___aF_2">' in html:
        html = html.replace(
            '<div class="Hero_bottom___aF_2"><div class="Hero_arrow__k_3kI">',
            f'<div class="Hero_bottom___aF_2">{h1_label_html}<div class="Hero_arrow__k_3kI">',
            1,
        )

    # 4. Blog Index / Category / Tag pages (Heading_heading__fhmAd)
    if 'class="Heading_heading__fhmAd"' in html:
        html = re.sub(
            r'(<h1 class="Heading_heading__fhmAd">.*?</h1>)(</div><div class="FeaturedBlogPost_featuredPost__aRcs9">)',
            lambda m: f"{m.group(1)}{div_label_html}{m.group(2)}",
            html,
            count=1,
            flags=re.S,
        )

    # 5. Blog Post Detail pages (Hero_left__0LdJX)
    if 'class="Hero_left__0LdJX"' in html:
        html = re.sub(
            r'(<div class="Hero_left__0LdJX">.*?</h1>)(</div><div class="Hero_right__AZ10b">)',
            lambda m: f"{m.group(1)}{div_label_html}{m.group(2)}",
            html,
            count=1,
            flags=re.S,
        )

    # 6. Privacy Policy pages (Content_content__6vnSh)
    if '<section class="Content_content__6vnSh">' in html:
        html = re.sub(
            r'(<section class="Content_content__6vnSh"><div class="container"><div class="prose">)(?:<h1[^>]*>.*?</h1>)?',
            lambda m: f"{m.group(1)}{h1_label_html}",
            html,
            count=1,
            flags=re.S,
        )

    return html


def update_all_pages_hero_titles():
    updated_count = 0
    for base_name in ("public", "dist"):
        base_dir = os.path.join(ROOT, base_name)
        for fp in sorted(glob.glob(os.path.join(base_dir, "**", "index.html"), recursive=True)):
            route = get_route_for_file(fp, base_dir)
            label = get_page_label_for_route(route)
            if not label:
                continue

            with open(fp, "r", encoding="utf-8") as f:
                html = f.read()

            html = mutate_ssr_html_for_page_label(html, label)
            html = rewrite_flight_in_html(
                html, lambda records, lbl=label: mutate_flight_for_page_label(records, lbl)
            )

            # Inject or update HERO_PAGE_LABEL_CSS inside <style data-roasist-ui-css>
            if "<style data-roasist-ui-css>" in html:
                html = re.sub(
                    r"\n?/\* Unified \"\| sayfa ismi\" Hero Page Title Format.*?(?=</style>)",
                    "",
                    html,
                    flags=re.S,
                )
                html = re.sub(
                    r"(<style data-roasist-ui-css>.*?)(</style>)",
                    lambda m: f"{m.group(1)}{HERO_PAGE_LABEL_CSS}{m.group(2)}",
                    html,
                    count=1,
                    flags=re.S,
                )

            with open(fp, "w", encoding="utf-8") as f:
                f.write(html)
            updated_count += 1

    print(f"[HERO PAGE TITLES] Standardized '| <page name>' across {updated_count} HTML files in public/ and dist/")


if __name__ == "__main__":
    update_all_pages_hero_titles()
