#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Faz 4 — Roasist Global (/en/*) Full 1:1 KOTA English Site, TR|EN Language Switcher,
KVKK/GDPR Consent Bar, Bidirectional hreflang, and Sitemap/Robots Generator.

Steps executed:
  A. Fixes the 3 minor TR SSR/Flight remnants (gizlilik LargeCta, referanslar subtitle,
     and Homepage ServicesPanels SSR<->Flight sync).
  B. Builds all 22 English (/en/*) pages in BOTH public/en/ and dist/en/ with 100%
     SSR + Flight AST parity (<html lang="en">, en_US Open Graph, English Schema.org,
     NAV_NODES_EN, English Footer, and localized page content).
  C. Injects bidirectional hreflang tags (<link rel="alternate" hreflang="tr|en|x-default">)
     and the post-hydration <script data-roasist-ui> + <style data-roasist-ui-css> across
     ALL TR and EN KOTA pages in public/ and dist/.
  D. Generates public/sitemap.xml, dist/sitemap.xml, public/robots.txt, and dist/robots.txt.
"""

import glob
import html as html_mod
import json
import os
import re
import sys
import urllib.parse
from datetime import datetime, timezone

ROOT = "/home/antigravity/Roasist/roasist-web"
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from apply_phase1_cleanup import (  # noqa: E402
    BADGE_CDN,
    BUTTON_ARROW_PATH_D,
    CDN_BASE,
    OFFICIAL_PHONE_DISPLAY,
    OFFICIAL_PHONE_TEL,
    PUSH_RE,
    ROASIST_LOGO_PATH_D,
    ROASIST_SOCIALS,
    SOCIAL_ARROW_PATH_D,
    find_node_by_class,
    rewrite_flight_in_html,
)
from apply_phase3_seo_gtm import (  # noqa: E402
    DEFAULT_OG_IMAGE,
    GTM_HEAD_SNIPPET,
    ROASIST_LOGO_PNG,
    ROASIST_SAME_AS,
    SITE_ORIGIN,
    get_route_for_file,
    sanitize_ast0,
    update_meta_ast,
)
from build_1to1_kota_pages import (  # noqa: E402
    SERVICES_BY_SLUG,
    build_json_pairs,
    localize_flight_stream,
    normalize_service_dict,
    transform_with_pairs,
)
from en_translations import (  # noqa: E402
    ABOUT_TR_TO_EN_PAIRS,
    BLOG_CATEGORIES_EN,
    BLOG_POSTS_EN,
    CONTACT_TR_TO_EN_PAIRS,
    EN_SERVICES_SPECS,
    EN_TO_TR_ROUTES,
    FOOTER_NAV_EN,
    FOOTER_SERVICES_EN,
    HOME_TR_TO_EN_PAIRS,
    NAV_NODES_EN,
    PRIVACY_EN_HTML,
    REFERENCES_TR_TO_EN_PAIRS,
    ROASIST_TESTIMONIALS_EN,
    TIMELINE_TR_TO_EN,
    TR_TO_EN_ROUTES,
)
from update_performans_channels import CHANNELS as TR_PERF_CHANNELS  # noqa: E402


# ==============================================================================
# SHARED HELPERS
# ==============================================================================
def find_key_dict(node, key_name: str):
    """Return the first dict containing `key_name` in a nested JSON tree."""
    if isinstance(node, dict):
        if key_name in node:
            return node
        for v in node.values():
            res = find_key_dict(v, key_name)
            if res is not None:
                return res
    elif isinstance(node, list):
        for item in node:
            res = find_key_dict(item, key_name)
            if res is not None:
                return res
    return None


DIV_TAG_RE = re.compile(r"<div(?:\s[^>]*)?>|</div>")


def replace_exact_div(html_str: str, open_tag_exact: str, replacement: str) -> str:
    """Replaces the exact balanced <div>...</div> block starting at `open_tag_exact`."""
    start = html_str.find(open_tag_exact)
    if start == -1:
        raise RuntimeError(f"Could not find {open_tag_exact!r} in HTML")
    depth = 0
    for m in DIV_TAG_RE.finditer(html_str, start):
        tok = m.group(0)
        if tok.startswith("</div"):
            depth -= 1
            if depth == 0:
                end = m.end()
                return html_str[:start] + replacement + html_str[end:]
        else:
            depth += 1
    raise RuntimeError(f"Unbalanced <div> starting at {open_tag_exact!r}")


def build_rich_html_pairs(pairs: list[tuple[str, str]]) -> list[tuple[str, str]]:
    """Expand string pairs to cover HTML entity encodings (&amp;, &quot;, &#x27;) in SSR."""
    expanded = []
    seen = set()

    def add(o: str, n: str):
        if o and o != n and o not in seen:
            seen.add(o)
            expanded.append((o, n))

    for old, new in pairs:
        add(old, new)
        new_amp = new.replace("&", "&amp;")
        v1 = old.replace("&", "&amp;").replace("'", "&#x27;")
        add(v1, new_amp)
        v2 = v1.replace("’", "&#x27;")
        add(v2, new_amp)
        if '"' in old:
            new_q = new_amp.replace('"', "&quot;")
            add(old.replace("&", "&amp;").replace('"', "&quot;"), new_q)
            add(v1.replace('"', "&quot;"), new_q)
            add(v2.replace('"', "&quot;"), new_q)

    expanded.sort(key=lambda kv: -len(kv[0]))
    return expanded


def apply_pairs_to_page(html_text: str, raw_pairs: list[tuple[str, str]]) -> str:
    """
    Applies sorted (tr, en) pairs across both SSR HTML (protecting client-hydrated form/nav
    containers whose strings come from JS bundles) and React Flight stream (with UTF-8 T<hex>,
    byte recalculation).
    """
    dedup = []
    seen = set()
    for o, n in sorted(raw_pairs, key=lambda kv: -len(kv[0])):
        if o and o != n and o not in seen:
            seen.add(o)
            dedup.append((o, n))

    pushes = list(PUSH_RE.finditer(html_text))
    if not pushes:
        return html_text

    ssr = html_text[: pushes[0].start()]
    joined_flight = "".join(json.loads(m.group(1)) for m in pushes)
    after_flight = html_text[pushes[-1].end() :]

    protected_blocks = []

    def protect_pattern(pattern: str):
        nonlocal ssr

        def _repl(m):
            tok = f"<!--__ROASIST_PROTECT_{len(protected_blocks)}__-->"
            protected_blocks.append((tok, m.group(0)))
            return tok

        ssr = re.sub(pattern, _repl, ssr, flags=re.S)

    protect_pattern(r'<section class="Form_contactForm__X6bdS"[^>]*>.*?</section>')
    protect_pattern(r'<div class="PrimaryNavigation_buttonContainer__iiKTy"[^>]*>.*?</div></div></div>')
    protect_pattern(r'<div class="FloatingStartButton_linkContainer__eZz7z"[^>]*>.*?</div>')
    protect_pattern(r'<script[^>]*>.*?</script>')
    protect_pattern(r'<style[^>]*>.*?</style>')

    html_pairs = build_rich_html_pairs(dedup)
    ssr = transform_with_pairs(ssr, html_pairs)

    for tok, orig_block in reversed(protected_blocks):
        ssr = ssr.replace(tok, orig_block)

    json_pairs = build_json_pairs(dedup)
    json_pairs.sort(key=lambda kv: -len(kv[0]))
    new_flight = localize_flight_stream(joined_flight, dedup, json_pairs)
    encoded = json.dumps(new_flight, ensure_ascii=False).replace("</script>", "<\\/script>")
    return f"{ssr}<script>self.__next_f.push([1,{encoded}])</script>{after_flight}"


# ==============================================================================
# STEP A: FIX 3 MINOR TR REMNANTS IN public/ AND dist/
# ==============================================================================
HOMEPAGE_PANELS_TR = [
    {
        "heading": "Performans Pazarlaması",
        "slug": "performans-pazarlamasi",
        "mainText": (
            "Reklam bütçenizi sadece harcamıyor, kârlı yatırıma dönüştürüyoruz. Google, Meta, TikTok, "
            "LinkedIn, Yandex ve Bing’de veri odaklı ROAS mimarisiyle satışlarınızı ölçeklendiriyoruz."
        ),
        "tags": [
            {"id": "cG9zdDo4ODQ=", "slug": "google-reklamlari", "title": "Google Ads Yönetimi"},
            {"id": "cG9zdDo4ODg=", "slug": "instagram-reklamlari", "title": "Meta Ads"},
            {"id": "cG9zdDo4ODY=", "slug": "tiktok-reklamlari", "title": "TikTok Ads"},
            {"id": "cG9zdDo4ODc=", "slug": "yandex-reklamlari", "title": "Yandex Ads"},
        ],
    },
    {
        "heading": "Web Tasarım & Kreatif Stüdyo",
        "slug": "web-tasarim",
        "mainText": (
            "Estetiğin yüksek dönüşüm oranlarıyla (ROI) buluştuğu, ultra hızlı, mobil öncelikli web "
            "deneyimleri ve dikkat çekici kreatif reklam görselleri tasarlıyoruz."
        ),
        "tags": [
            {"id": "cG9zdDoxMzEy", "slug": "web-tasarim", "title": "UI/UX & Web Tasarım"},
            {"id": "cG9zdDoxMzM1", "slug": "grafik-tasarim", "title": "Grafik & Kreatif Tasarım"},
            {"id": "cG9zdDo4NzA=", "slug": "web-tasarim", "title": "Dönüşüm Optimizasyonu (CRO)"},
        ],
    },
    {
        "heading": "SEO, AEO & 360° Dijital Büyüme",
        "slug": "seo",
        "mainText": (
            "Google organik aramalarında ve ChatGPT, Gemini, Perplexity gibi yapay zeka yanıt "
            "motorlarında (AEO & GEO) markanızı sektör lideri konumuna taşıyoruz."
        ),
        "tags": [
            {"id": "cG9zdDo4OTI=", "slug": "seo", "title": "Teknik & Kurumsal SEO"},
            {"id": "cG9zdDo4OTQ=", "slug": "seo", "title": "Yapay Zeka Aramaları (AEO & GEO)"},
            {"id": "cG9zdDo4OTA=", "slug": "360-derece-dijital-pazarlama-yonetimi", "title": "360° Dijital Yönetim"},
        ],
    },
]

HOMEPAGE_PANELS_EN = [
    {
        "heading": "Performance Marketing",
        "slug": "performance-marketing",
        "mainText": (
            "We don't just spend media budgets—we engineer profitable returns. Scale your sales with "
            "data-driven ROAS systems across Google, Meta, TikTok, LinkedIn, Yandex, and Bing."
        ),
        "tags": [
            {"id": "cG9zdDo4ODQ=", "slug": "google-ads", "title": "Google Ads"},
            {"id": "cG9zdDo4ODg=", "slug": "instagram-ads", "title": "Meta Ads"},
            {"id": "cG9zdDo4ODY=", "slug": "tiktok-ads", "title": "TikTok Ads"},
            {"id": "cG9zdDo4ODc=", "slug": "yandex-ads", "title": "Yandex Ads"},
        ],
    },
    {
        "heading": "Web Design & Creative Studio",
        "slug": "web-design",
        "mainText": (
            "Ultra-fast, mobile-first web experiences and scroll-stopping ad creatives where "
            "distinctive aesthetics meet measurable conversion rates."
        ),
        "tags": [
            {"id": "cG9zdDoxMzEy", "slug": "web-design", "title": "UI/UX & Web Design"},
            {"id": "cG9zdDoxMzM1", "slug": "graphic-design", "title": "Graphic & Ad Creative"},
            {"id": "cG9zdDo4NzA=", "slug": "web-design", "title": "Conversion Optimization (CRO)"},
        ],
    },
    {
        "heading": "SEO, AEO & 360° Digital Growth",
        "slug": "seo",
        "mainText": (
            "Position your brand at the top of Google organic search and AI answer engines "
            "including ChatGPT, Gemini, and Perplexity."
        ),
        "tags": [
            {"id": "cG9zdDo4OTI=", "slug": "seo", "title": "Enterprise & Technical SEO"},
            {"id": "cG9zdDo4OTQ=", "slug": "seo", "title": "AI Search (AEO & GEO)"},
            {"id": "cG9zdDo4OTA=", "slug": "360-digital-marketing-management", "title": "360° Growth Management"},
        ],
    },
]


def sync_homepage_services_panels(html_text: str, panels_spec: list[dict]) -> str:
    """
    Synchronizes ServicesPanels_panels__NpKkK in SSR and `services` array in Flight rec 11
    so SSR and client hydration ($L34) match 100% (`href="service/" + slug`, text `"Detaylı İncele"`).
    """
    pushes = list(PUSH_RE.finditer(html_text))
    ssr = html_text[: pushes[0].start()]
    tail = html_text[pushes[0].start() :]

    panel_blocks_ssr = []
    for p in panels_spec:
        tags_ssr = "".join(
            f'<a class="ServicesPanel_tag__JYwRk" href="service/{t["slug"]}">{html_mod.escape(t["title"])}</a>'
            for t in p["tags"]
        )
        panel_blocks_ssr.append(
            '<div class="AnimatedPanel_panel__eAXfR"><div>'
            '<div class="ServicesPanel_panel__YF4OS servicePanel">'
            '<div class="ServicesPanel_panelText__iyjwZ">'
            f'<h3 class="ServicesPanel_panelHeading__5Sy4s">{html_mod.escape(p["heading"])}</h3>'
            f'<div class="ServicesPanel_tags__6NQOl">{tags_ssr}</div>'
            f'<p class="ServicesPanel_panelMainText__4F0TZ">{html_mod.escape(p["mainText"])}</p>'
            '<div class="Magnetic_magnetic__LncOy" data-fill="false">'
            '<div class="Button_button__JJiqJ" data-direction="forwards">'
            f'<a class="Button_inner__fnyH6" href="service/{p["slug"]}">'
            '<span class="Button_border__hirH2"></span>'
            '<span class="Button_text__IZaCD">'
            '<span class="Button_textInner__JTTHe">Detaylı İncele</span>'
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 17.1 15.17" class="Button_buttonArrow__0W9XI"><path d="{BUTTON_ARROW_PATH_D}" fill="currentColor"></path></svg>'
            "</span></a></div></div></div>"
            '<div class="ServiceMedia_mediaContainer__WGgZa">'
            '<span class="AutoplayVideo_video__zckWy AutoplayVideo_fill__ZPgCR"><video loop="" muted="" playsInline=""></video></span>'
            "</div>"
            '<div class="ServicesPanel_panelBackground__O9mDV"></div>'
            "</div></div>"
            '<div class="AnimatedPanel_spacer__w4GTD"></div></div>'
        )

    new_panels_ssr = (
        f'<div class="ServicesPanels_panels__NpKkK"><div class="container">{"".join(panel_blocks_ssr)}</div></div>'
    )
    ssr = replace_exact_div(ssr, '<div class="ServicesPanels_panels__NpKkK">', new_panels_ssr)

    def sp_mutator(records):
        changed = False
        for rec in records:
            if rec[0] == "line" and '"services":[' in rec[2]:
                ast = json.loads(rec[2])
                holder = find_key_dict(ast, "services")
                if holder and isinstance(holder["services"], list) and len(holder["services"]) == 3:
                    for idx, spec in enumerate(panels_spec):
                        s_obj = holder["services"][idx]
                        s_obj["heading"] = spec["heading"]
                        s_obj["link"] = {"slug": spec["slug"], "parent": None}
                        s_obj["mainText"] = spec["mainText"]
                        s_obj["tags"] = spec["tags"]
                        if isinstance(s_obj.get("image"), dict):
                            s_obj["image"]["altText"] = spec["heading"]
                    rec[2] = json.dumps(ast, ensure_ascii=False, separators=(",", ":"))
                    changed = True
        return changed

    return ssr + rewrite_flight_in_html(tail, sp_mutator)


def fix_tr_remnants():
    # 1. gizlilik-politikasi-ve-kullanim-sartlari LargeCta
    for base_name in ("public", "dist"):
        fp = os.path.join(ROOT, base_name, "gizlilik-politikasi-ve-kullanim-sartlari", "index.html")
        if os.path.exists(fp):
            txt = open(fp, "r", encoding="utf-8").read()
            pushes = list(PUSH_RE.finditer(txt))
            ssr = txt[: pushes[0].start()]
            tail = txt[pushes[0].start() :]
            ssr = ssr.replace(
                "Have a new project you&#x27;d like help with?",
                "Yeni bir dijital büyüme projeniz mi var?",
            ).replace(
                "Have a new project you'd like help with?",
                "Yeni bir dijital büyüme projeniz mi var?",
            )
            ssr = ssr.replace(
                "Let&#x27;s get <!-- --><em>started</em>",
                "Hemen <!-- --><em>başlayalım</em>",
            ).replace(
                "Let's get <em>started</em>",
                "Hemen <em>başlayalım</em>",
            )
            ssr = ssr.replace('href="/start-your-project"', 'href="/iletisim/"')

            def gz_mut(records):
                c = False
                for rec in records:
                    if rec[0] == "line" and "LargeCta_largeCta__ylf5C" in rec[2]:
                        s = rec[2]
                        s = s.replace("Have a new project you'd like help with?", "Yeni bir dijital büyüme projeniz mi var?")
                        s = s.replace('"href":"/start-your-project"', '"href":"/iletisim/"')
                        s = s.replace('"Let\'s get "', '"Hemen "')
                        s = s.replace('"children":"started"', '"children":"başlayalım"')
                        rec[2] = s
                        c = True
                return c

            with open(fp, "w", encoding="utf-8") as f:
                f.write(ssr + rewrite_flight_in_html(tail, gz_mut))
            print(f"[TR FIX] Updated LargeCta in {base_name}/gizlilik-politikasi-ve-kullanim-sartlari/index.html")

    # 2. referanslar subtitle
    kota_ref_sub_rn = (
        "KOTA is a progressive and insightful \r\ndesign agency, technically and \r\n"
        "creatively skilled to translate your brand \r\ninto its best digital self."
    )
    kota_ref_sub_n = kota_ref_sub_rn.replace("\r\n", "\n")
    tr_ref_sub = "Veri odaklı performans pazarlaması, kurumsal SEO ve dönüşüm mimarisiyle büyüttüğümüz markaları keşfedin."
    for base_name in ("public", "dist"):
        fp = os.path.join(ROOT, base_name, "referanslar", "index.html")
        if os.path.exists(fp):
            txt = open(fp, "r", encoding="utf-8").read()
            txt = apply_pairs_to_page(
                txt,
                [
                    (kota_ref_sub_rn, tr_ref_sub),
                    (kota_ref_sub_n, tr_ref_sub),
                ],
            )
            with open(fp, "w", encoding="utf-8") as f:
                f.write(txt)
            print(f"[TR FIX] Updated Hero subtitle in {base_name}/referanslar/index.html")

    # 3. Homepage ServicesPanels SSR <-> Flight sync
    for rel_fp in ("public/kota-roasist-local.html", "dist/index.html"):
        fp = os.path.join(ROOT, rel_fp)
        if os.path.exists(fp):
            txt = open(fp, "r", encoding="utf-8").read()
            txt = sync_homepage_services_panels(txt, HOMEPAGE_PANELS_TR)
            with open(fp, "w", encoding="utf-8") as f:
                f.write(txt)
            print(f"[TR FIX] Synced ServicesPanels SSR & Flight in {rel_fp}")


# ==============================================================================
# STEP B: SHARED ENGLISH CHROME (NAV, HEADER, FOOTER, SEO, SCHEMA.ORG)
# ==============================================================================
SSR_NAV_UL_EN = (
    "<ul>"
    '<li><a href="/en/references/">Work</a></li>'
    '<li><a href="/en/who-we-are/">About Us</a></li>'
    '<li><div class="PrimaryNavigation_parent__bfX37">Services'
    '<figure class="PrimaryNavigation_toggleSign__XESvT "><span class="PrimaryNavigation_toggleInner__Lz3QB">'
    '<span class="PrimaryNavigation_toggleLine__QUlfd"></span><span class="PrimaryNavigation_toggleLine__QUlfd"></span>'
    "</span></figure></div>"
    '<ul class="PrimaryNavigation_submenu__ryGWu ">'
    '<li><a href="/en/performance-marketing/">Performance Marketing</a></li>'
    '<li><a href="/en/seo/">SEO</a></li>'
    '<li><a href="/en/graphic-design/">Graphic Design</a></li>'
    '<li><a href="/en/web-design/">Web Design</a></li>'
    '<li><a href="/en/360-digital-marketing-management/">360° Digital Marketing</a></li>'
    "</ul></li>"
    '<li><a href="/en/blog/">Blog</a></li>'
    '<li><a href="/en/contact-us/">Contact</a></li>'
    "</ul>"
)


def build_footer_ssr_en(is_dist: bool) -> str:
    badge_prefix = f"{BADGE_CDN}/images" if is_dist else "/images"
    socials_html = "".join(
        f'<a href="{url}" target="_blank" rel="noopener noreferrer">{name}'
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 12.69 12.69">'
        f'<path fill="#fff" stroke-width="0" d="{SOCIAL_ARROW_PATH_D}"></path></svg></a>'
        for name, url in ROASIST_SOCIALS
    )
    last_nav_items = "".join(f'<li><a href="{href}">{lbl}</a></li>' for lbl, href in FOOTER_NAV_EN)
    sector_items = "".join(
        f'<a class="Footer_sectorItem__0Cx14" href="{href}">{lbl}</a>' for lbl, href in FOOTER_SERVICES_EN
    )
    badges = [
        f"{badge_prefix}/badge-google-partner-w.svg",
        f"{badge_prefix}/badge-meta-partner-w.svg",
        f"{badge_prefix}/badge-tiktok-partner-w.svg",
        f"{badge_prefix}/badge-ai-seo-w.svg",
    ]
    badges_html = "".join(f'<img src="{b}" alt=""/>' for b in badges)

    return (
        '<footer class="Footer_footer__pQtti" data-theme="dark">'
        '<div class="container">'
        '<div class="Footer_top__623B4">'
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 820 200" class="Footer_logo__b602f">'
        f'<path fill="#fff" stroke-width="0" d="{ROASIST_LOGO_PATH_D}"></path></svg>'
        '<a class="Footer_email__nLajh CopyText_copyText__OtWNq">info@roasist.com'
        '<div class="CopyText_tooltip__HuxWa ">Copy email address</div></a></div>'
        '<div class="Footer_bottom__wxP7Z">'
        f'<div class="Footer_socialLinks__tA7gt">{socials_html}</div>'
        f'<ul class="Footer_lastNav__at6Kh" data-type="mobile">{last_nav_items}</ul>'
        '<div class="Footer_sectorsWrap__UM4Zx" data-type="mobile">'
        '<span class="Footer_sectorTitle__yEZhb">Our Services :</span>'
        f'<ul class="Footer_sectorMenu__GX7QZ">{sector_items}</ul></div>'
        f'<div class="Footer_logos__jFNys">{badges_html}</div></div>'
        '<div class="Footer_last__auU9C">'
        f'<ul class="Footer_lastNav__at6Kh" data-type="desktop">{last_nav_items}</ul>'
        '<a class="Footer_newsletterButton__wp2hz" href="/en/contact-us/">Get a Free Digital Audit</a></div>'
        '<div class="Footer_copyright__j4atB">'
        '<div class="Footer_sectorsWrap__UM4Zx" data-type="desktop">'
        '<span class="Footer_sectorTitle__yEZhb">Our Services :</span>'
        f'<ul class="Footer_sectorMenu__GX7QZ">{sector_items}</ul></div>'
        '<div class="Footer_copyrightTextWrap__uhQWh">'
        '<span class="Footer_copyrightText__f_Lte">© Roasist <!-- -->2026</span>'
        f'<a href="{OFFICIAL_PHONE_TEL}" class="Footer_cyberEssestials__2qh89">{OFFICIAL_PHONE_DISPLAY} • Istanbul</a>'
        "</div></div></div></footer>"
    )


def build_footer_flight_ast_en(copy_id: str, link_id: str, is_dist: bool) -> list:
    badge_prefix = f"{BADGE_CDN}/images" if is_dist else "/images"
    social_arrow = [
        "$",
        "svg",
        None,
        {
            "xmlns": "http://www.w3.org/2000/svg",
            "viewBox": "0 0 12.69 12.69",
            "children": ["$", "path", None, {"fill": "#fff", "strokeWidth": "0", "d": SOCIAL_ARROW_PATH_D}],
        },
    ]
    social_nodes = [
        [
            "$",
            "a",
            str(idx),
            {
                "href": url,
                "target": "_blank",
                "rel": "noopener noreferrer",
                "children": [name, social_arrow],
            },
        ]
        for idx, (name, url) in enumerate(ROASIST_SOCIALS)
    ]

    def make_last_nav(dtype: str):
        return [
            "$",
            "ul",
            None,
            {
                "className": "Footer_lastNav__at6Kh",
                "data-type": dtype,
                "children": [
                    [
                        "$",
                        "li",
                        None,
                        {"className": "$undefined", "children": ["$", link_id, None, {"href": href, "children": lbl}]},
                    ]
                    for lbl, href in FOOTER_NAV_EN
                ],
            },
        ]

    def make_sectors_wrap(dtype: str):
        return [
            "$",
            "div",
            None,
            {
                "className": "Footer_sectorsWrap__UM4Zx",
                "data-type": dtype,
                "children": [
                    ["$", "span", None, {"className": "Footer_sectorTitle__yEZhb", "children": "Our Services :"}],
                    [
                        "$",
                        "ul",
                        None,
                        {
                            "className": "Footer_sectorMenu__GX7QZ",
                            "children": [
                                [
                                    "$",
                                    link_id,
                                    str(idx),
                                    {"className": "Footer_sectorItem__0Cx14", "href": href, "children": lbl},
                                ]
                                for idx, (lbl, href) in enumerate(FOOTER_SERVICES_EN)
                            ],
                        },
                    ],
                ],
            },
        ]

    badge_nodes = [
        ["$", "img", "4739", {"src": f"{badge_prefix}/badge-google-partner-w.svg", "alt": ""}],
        ["$", "img", "154", {"src": f"{badge_prefix}/badge-meta-partner-w.svg", "alt": ""}],
        ["$", "img", "155", {"src": f"{badge_prefix}/badge-tiktok-partner-w.svg", "alt": ""}],
        ["$", "img", "153", {"src": f"{badge_prefix}/badge-ai-seo-w.svg", "alt": ""}],
    ]

    return [
        "$",
        "footer",
        None,
        {
            "className": "Footer_footer__pQtti",
            "data-theme": "dark",
            "children": [
                "$",
                "div",
                None,
                {
                    "className": "container",
                    "children": [
                        [
                            "$",
                            "div",
                            None,
                            {
                                "className": "Footer_top__623B4",
                                "children": [
                                    [
                                        "$",
                                        "svg",
                                        None,
                                        {
                                            "xmlns": "http://www.w3.org/2000/svg",
                                            "viewBox": "0 0 820 200",
                                            "className": "Footer_logo__b602f",
                                            "children": [
                                                "$",
                                                "path",
                                                None,
                                                {"fill": "#fff", "strokeWidth": "0", "d": ROASIST_LOGO_PATH_D},
                                            ],
                                        },
                                    ],
                                    ["$", copy_id, None, {"text": "info@roasist.com", "className": "Footer_email__nLajh"}],
                                ],
                            },
                        ],
                        [
                            "$",
                            "div",
                            None,
                            {
                                "className": "Footer_bottom__wxP7Z",
                                "children": [
                                    ["$", "div", None, {"className": "Footer_socialLinks__tA7gt", "children": social_nodes}],
                                    make_last_nav("mobile"),
                                    make_sectors_wrap("mobile"),
                                    ["$", "div", None, {"className": "Footer_logos__jFNys", "children": badge_nodes}],
                                ],
                            },
                        ],
                        [
                            "$",
                            "div",
                            None,
                            {
                                "className": "Footer_last__auU9C",
                                "children": [
                                    make_last_nav("desktop"),
                                    [
                                        "$",
                                        link_id,
                                        None,
                                        {
                                            "className": "Footer_newsletterButton__wp2hz",
                                            "href": "/en/contact-us/",
                                            "children": "Get a Free Digital Audit",
                                        },
                                    ],
                                ],
                            },
                        ],
                        [
                            "$",
                            "div",
                            None,
                            {
                                "className": "Footer_copyright__j4atB",
                                "children": [
                                    make_sectors_wrap("desktop"),
                                    [
                                        "$",
                                        "div",
                                        None,
                                        {
                                            "className": "Footer_copyrightTextWrap__uhQWh",
                                            "children": [
                                                [
                                                    "$",
                                                    "span",
                                                    None,
                                                    {
                                                        "className": "Footer_copyrightText__f_Lte",
                                                        "children": ["© Roasist ", 2026],
                                                    },
                                                ],
                                                [
                                                    "$",
                                                    "a",
                                                    None,
                                                    {
                                                        "href": OFFICIAL_PHONE_TEL,
                                                        "className": "Footer_cyberEssestials__2qh89",
                                                        "children": f"{OFFICIAL_PHONE_DISPLAY} • Istanbul",
                                                    },
                                                ],
                                            ],
                                        },
                                    ],
                                ],
                            },
                        ],
                    ],
                },
            ],
        },
    ]


def build_roasist_schema_en(canonical_url: str, en_route: str, title: str, description: str) -> str:
    crumbs = [{"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE_ORIGIN}/en/"}]
    if en_route != "/en/":
        clean_title = title.split("|")[0].split(" - Roasist")[0].replace("Roasist - ", "").strip()
        crumbs.append({"@type": "ListItem", "position": 2, "name": clean_title, "item": canonical_url})

    graph = [
        {
            "@type": "WebPage",
            "@id": canonical_url,
            "url": canonical_url,
            "name": title,
            "isPartOf": {"@id": f"{SITE_ORIGIN}/en/#website"},
            "about": {"@id": f"{SITE_ORIGIN}/#organization"},
            "description": description,
            "breadcrumb": {"@id": f"{canonical_url}#breadcrumb"},
            "inLanguage": "en-US",
            "potentialAction": [{"@type": "ReadAction", "target": [canonical_url]}],
        },
        {
            "@type": "BreadcrumbList",
            "@id": f"{canonical_url}#breadcrumb",
            "itemListElement": crumbs,
        },
        {
            "@type": "WebSite",
            "@id": f"{SITE_ORIGIN}/en/#website",
            "url": f"{SITE_ORIGIN}/en/",
            "name": "Roasist Global",
            "description": "Data-Driven 360° Digital Marketing, Performance & Growth Agency",
            "publisher": {"@id": f"{SITE_ORIGIN}/#organization"},
            "inLanguage": "en-US",
        },
        {
            "@type": "Organization",
            "@id": f"{SITE_ORIGIN}/#organization",
            "name": "Roasist",
            "alternateName": "Roasist Digital Growth Agency",
            "url": f"{SITE_ORIGIN}/en/",
            "email": "info@roasist.com",
            "telephone": OFFICIAL_PHONE_DISPLAY,
            "address": {
                "@type": "PostalAddress",
                "addressLocality": "Istanbul",
                "addressCountry": "TR",
            },
            "logo": {
                "@type": "ImageObject",
                "@id": f"{SITE_ORIGIN}/#/schema/logo/image/",
                "url": ROASIST_LOGO_PNG,
                "contentUrl": ROASIST_LOGO_PNG,
                "width": 512,
                "height": 512,
                "caption": "Roasist",
            },
            "sameAs": ROASIST_SAME_AS,
        },
    ]
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))


def apply_en_chrome_and_seo(
    html_text: str,
    en_route: str,
    en_title: str,
    en_desc: str,
    is_dist: bool,
    is_home: bool = False,
) -> str:
    """
    Synchronizes <html lang="en">, <head> SEO/OG/Schema, Header, PrimaryNavigation, and Footer
    across both SSR and Flight for any English (/en/*) KOTA page.
    """
    canonical = f"{SITE_ORIGIN}{en_route}"
    pushes = list(PUSH_RE.finditer(html_text))
    ssr = html_text[: pushes[0].start()]
    tail = html_text[pushes[0].start() :]

    og_img_m = re.search(r'<meta property="og:image" content="(.*?)"', ssr)
    cur_og_img = og_img_m.group(1) if og_img_m else DEFAULT_OG_IMAGE
    if not cur_og_img or "kota" in cur_og_img:
        cur_og_img = DEFAULT_OG_IMAGE

    esc_title = html_mod.escape(en_title, quote=True)
    esc_desc = html_mod.escape(en_desc, quote=True)

    # 1. SSR <html lang="en"> & <head> tags
    ssr = re.sub(r'<html\s+lang="[^"]*"', '<html lang="en"', ssr, count=1)
    ssr = re.sub(r"<title>.*?</title>", lambda _: f"<title>{html_mod.escape(en_title)}</title>", ssr, count=1, flags=re.S)
    ssr = re.sub(r'<meta name="description" content="[^"]*"\s*/>', f'<meta name="description" content="{esc_desc}"/>', ssr)
    ssr = re.sub(r'<link rel="canonical" href="[^"]*"\s*/>', f'<link rel="canonical" href="{canonical}"/>', ssr)
    ssr = re.sub(r'<meta property="og:locale" content="[^"]*"\s*/>', '<meta property="og:locale" content="en_US"/>', ssr)
    ssr = re.sub(r'<meta property="og:title" content="[^"]*"\s*/>', f'<meta property="og:title" content="{esc_title}"/>', ssr)
    ssr = re.sub(
        r'<meta property="og:description" content="[^"]*"\s*/>',
        f'<meta property="og:description" content="{esc_desc}"/>',
        ssr,
    )
    ssr = re.sub(r'<meta property="og:url" content="[^"]*"\s*/>', f'<meta property="og:url" content="{canonical}"/>', ssr)
    ssr = re.sub(r'<meta name="twitter:title" content="[^"]*"\s*/>', f'<meta name="twitter:title" content="{esc_title}"/>', ssr)
    ssr = re.sub(
        r'<meta name="twitter:description" content="[^"]*"\s*/>',
        f'<meta name="twitter:description" content="{esc_desc}"/>',
        ssr,
    )

    schema_en = build_roasist_schema_en(canonical, en_route, en_title, en_desc)
    ssr = re.sub(
        r'<script type="application/ld\+json" class="yoast-schema-graph">.*?</script>',
        lambda _: f'<script type="application/ld+json" class="yoast-schema-graph">{schema_en}</script>',
        ssr,
        flags=re.S,
    )

    ssr = re.sub(r"<script data-roasist-gtm>.*?</script>", "", ssr, flags=re.S)
    ssr = ssr.replace("</head>", f"{GTM_HEAD_SNIPPET}</head>", 1)

    # 2. SSR Header (logo -> /en/, CTA -> /en/contact-us/, Celebrating -> EN)
    btn_label_en = "Get a Proposal" if is_home else "Get in Touch"
    celebrating_en = "ROASIST GLOBAL — 360° DIGITAL GROWTH & PERFORMANCE : "
    has_celebrating_ssr = "Celebrating_celebrating__MdmnM" in ssr

    ssr = re.sub(
        r'(<a class="Header_logo____uDV" href=")[^"]*(")',
        r"\1/en/\2",
        ssr,
        count=1,
    )
    ssr = re.sub(
        r'<a class="Header_button__yG4_K" href="[^"]*">(.*?)</a>',
        lambda m: (
            '<a class="Header_button__yG4_K" href="/en/contact-us/">'
            + re.sub(
                r'(<span class="Header_buttonTextInner[^"]*">).*?(</span>)',
                lambda sm: f"{sm.group(1)}{btn_label_en}{sm.group(2)}",
                re.sub(
                    r"(<span>)(?:Teklif Al|Bize Ulaşın|Get a Proposal|Get in Touch)(</span>)",
                    lambda sm2: f"{sm2.group(1)}{btn_label_en}{sm2.group(2)}",
                    m.group(1),
                ),
            )
            + "</a>"
        ),
        ssr,
        count=1,
        flags=re.S,
    )
    if has_celebrating_ssr:
        ssr = re.sub(
            r'<p class="Celebrating_celebrating__MdmnM"[^>]*>.*?</p>',
            (
                '<p class="Celebrating_celebrating__MdmnM" data-modal-hide="true">'
                f'<a href="/en/who-we-are/">{html_mod.escape(celebrating_en)}<!-- -->2026</a></p>'
            ),
            ssr,
            flags=re.S,
        )

    # 3. SSR PrimaryNavigation (replace ONLY <ul>...</ul>, keeping buttonContainer untouched for hydration)
    ssr, n_nav = re.subn(
        r'(<nav class="PrimaryNavigation_navigation__l8Jgb">)<ul>.*?</ul>(<div class="PrimaryNavigation_buttonContainer__iiKTy">)',
        lambda m: m.group(1) + SSR_NAV_UL_EN + m.group(2),
        ssr,
        count=1,
        flags=re.S,
    )
    if n_nav != 1:
        raise RuntimeError(f"Failed to replace PrimaryNavigation <ul> in {en_route}")

    # 4. SSR Footer
    new_footer_ssr = build_footer_ssr_en(is_dist)
    ssr, n_ft = re.subn(
        r'<footer class="Footer_footer__pQtti".*?</footer>',
        lambda _: new_footer_ssr,
        ssr,
        count=1,
        flags=re.S,
    )
    if n_ft != 1:
        raise RuntimeError(f"Failed to replace Footer in {en_route}")

    # 5. Flight AST updates (0:, Header, PrimaryNavigation, Footer, Metadata, Schema)
    meta_updates = {
        "title": en_title,
        "description": en_desc,
        "canonical": canonical,
        "og:locale": "en_US",
        "og:image": cur_og_img,
        "twitter:site": "@Roasistt",
    }

    def en_chrome_mutator(records):
        for rec in records:
            kind, rid, val = rec[0], rec[1], rec[2]
            if kind == "line" and rid == "0":
                ast0 = json.loads(val)
                sanitize_ast0(ast0, lang="en")
                update_meta_ast(ast0, meta_updates)
                rec[2] = json.dumps(ast0, ensure_ascii=False, separators=(",", ":"))
            elif kind == "line" and "menuItems" in val and "nodes" in val:
                nav_ast = json.loads(val)
                holder = find_key_dict(nav_ast, "menuItems")
                if holder and "nodes" in holder["menuItems"]:
                    holder["menuItems"]["nodes"] = NAV_NODES_EN
                    rec[2] = json.dumps(nav_ast, ensure_ascii=False, separators=(",", ":"))
            elif kind == "line" and "Header_header__KwdYD" in val:
                hdr_ast = json.loads(val)

                def walk_hdr(n):
                    if isinstance(n, list):
                        if len(n) >= 4 and n[0] == "$" and isinstance(n[3], dict):
                            cls = str(n[3].get("className", ""))
                            if "Header_logo____uDV" in cls:
                                n[3]["href"] = "/en/"
                            elif "Header_button__yG4_K" in cls:
                                n[3]["href"] = "/en/contact-us/"
                                txt_span = n[3].get("children")
                                if isinstance(txt_span, list) and len(txt_span) >= 4 and isinstance(txt_span[3], dict):
                                    ch_list = txt_span[3].get("children")
                                    if isinstance(ch_list, list) and len(ch_list) >= 1 and isinstance(ch_list[0], list):
                                        ch_list[0][3]["children"] = btn_label_en
                        for item in n:
                            walk_hdr(item)
                    elif isinstance(n, dict):
                        for v in n.values():
                            walk_hdr(v)

                if isinstance(hdr_ast, list) and len(hdr_ast) >= 2:
                    walk_hdr(hdr_ast[0])
                    if has_celebrating_ssr:
                        hdr_ast[1] = [
                            "$",
                            "p",
                            None,
                            {
                                "className": "Celebrating_celebrating__MdmnM",
                                "data-modal-hide": True,
                                "children": [
                                    "$",
                                    "a",
                                    None,
                                    {
                                        "href": "/en/who-we-are/",
                                        "children": [celebrating_en, 2026],
                                    },
                                ],
                            },
                        ]
                    else:
                        hdr_ast[1] = None
                    rec[2] = json.dumps(hdr_ast, ensure_ascii=False, separators=(",", ":"))
            elif kind == "line" and "Footer_footer__pQtti" in val:
                m_ids = re.search(
                    r'"(\$L[0-9a-f]+)",null,\{"text":"[^"]+","className":"Footer_email__nLajh".*?"(\$L[0-9a-f]+)",null,\{(?:"className":"[^"]+",)?"href":',
                    val,
                )
                if m_ids:
                    copy_id, link_id = m_ids.group(1), m_ids.group(2)
                    rec[2] = json.dumps(build_footer_flight_ast_en(copy_id, link_id, is_dist), ensure_ascii=False, separators=(",", ":"))
            elif kind == "line" and ('"rel":"canonical"' in val or '"og:locale"' in val or val.startswith('[[["$","title"')):
                meta_ast = json.loads(val)
                update_meta_ast(meta_ast, meta_updates)
                rec[2] = json.dumps(meta_ast, ensure_ascii=False, separators=(",", ":"))
            elif kind == "text" and '"@context":"https://schema.org"' in val:
                rec[2] = schema_en
        return True

    return ssr + rewrite_flight_in_html(tail, en_chrome_mutator)


def write_en_output(base_name: str, en_rel_dir: str, content: str):
    out_dir = os.path.join(ROOT, base_name, "en", en_rel_dir) if en_rel_dir else os.path.join(ROOT, base_name, "en")
    os.makedirs(out_dir, exist_ok=True)
    out_fp = os.path.join(out_dir, "index.html")
    with open(out_fp, "w", encoding="utf-8") as f:
        f.write(content)


# ==============================================================================
# PAGE BUILDER 1: ENGLISH HOMEPAGE (/en/index.html)
# ==============================================================================
EXTRA_HOME_PAIRS_EN = [
    ("1 yıl içinde dijital kanallardan elde edilen toplam satış hacminde artış.", "Increase in total digital channel revenue within 12 months."),
    (
        '"Lansman sonrasında da Roasist, yürüttüğü stratejik SEO ve performans çalışmalarıyla görünürlüğümüzü ve organik büyümemizi istikrarlı biçimde artırdı. Uzun vadeli değer üreten gerçek bir dijital büyüme ortağı."',
        '"Post-launch, Roasist steadily expanded our organic visibility and revenue through disciplined SEO and performance campaigns. A true long-term digital growth partner."',
    ),
    (
        '"Roasist’in fikirleri yenilikçi ve heyecan vericiydi; Marka Stratejisi, Kreatif Tasarım, Web Geliştirme, SEO ve Performans Pazarlamasını tek çatı altında 360° sunabilmeleri sayesinde tüm süreci kusursuz tamamladık."',
        '"Roasist brought fresh, bold strategic thinking—and having Brand Strategy, Creative Design, Web Engineering, SEO, and Performance Marketing under one 360° roof made execution effortless."',
    ),
    (
        "Roasist; 360° Dijital Pazarlama Yönetimi, Performans Pazarlaması (Google Ads, Instagram, Facebook, TikTok, LinkedIn ve Yandex Reklamları), Arama Motoru Optimizasyonu (SEO & AEO), Dönüşüm Odaklı Web Tasarım ve Kreatif Grafik Tasarım hizmetlerini veri odaklı bir yaklaşımla sunar.",
        "Roasist delivers 360° Digital Marketing Management, Performance Marketing (Google, Instagram, Facebook, TikTok, LinkedIn, Yandex, and Bing Ads), Enterprise SEO & AEO, Conversion Web Design, and Graphic & Ad Creative through a data-driven methodology.",
    ),
    ("Blog'u İncele", "Explore Blog"),
    ('href="/referanslar/"', 'href="/en/references/"'),
    ('href="/referanslar"', 'href="/en/references/"'),
    ('"href":"/referanslar/"', '"href":"/en/references/"'),
    ('"href":"/referanslar"', '"href":"/en/references/"'),
    ('"url":"/referanslar/"', '"url":"/en/references/"'),
    ('"url":"/referanslar"', '"url":"/en/references/"'),
    ('href="/hakkimizda/"', 'href="/en/who-we-are/"'),
    ('href="/hakkimizda"', 'href="/en/who-we-are/"'),
    ('"href":"/hakkimizda/"', '"href":"/en/who-we-are/"'),
    ('"href":"/hakkimizda"', '"href":"/en/who-we-are/"'),
    ('href="/hizmetler/"', 'href="/en/services/"'),
    ('"href":"/hizmetler/"', '"href":"/en/services/"'),
    ('href="/blog/"', 'href="/en/blog/"'),
    ('"href":"/blog/"', '"href":"/en/blog/"'),
]


def update_en_homepage_articles(html_text: str) -> str:
    """Replaces Homepage Articles_articlesList__CXW8a with the 3 English blog posts in SSR & Flight."""
    pushes = list(PUSH_RE.finditer(html_text))
    ssr = html_text[: pushes[0].start()]
    tail = html_text[pushes[0].start() :]

    ssr_items = "".join(
        f'<a data-animation="grid-item" href="/en/blog/{p["slug"]}/">'
        f'<article class="Articles_article__3ZS4Y">'
        f'<figure class="Articles_image__Cvgsi"><span class="Image_image__RAAdZ Image_fill__EiIzS">'
        f'<img data-srcset="{p["image"]} 1400w" data-src="{p["image"]}" alt="{html_mod.escape(p["title"], quote=True)}" fetchPriority="low" height="{p["img_h"]}" width="{p["img_w"]}" sizes="auto" class="lazyload"/>'
        f"</span></figure>"
        f'<div class="Articles_text__HhO2L">'
        f'<p class="Articles_filterNames__mCWt8">{html_mod.escape(p["category"]["name"])}</p>'
        f'<h3 class="Articles_title__h86PB">{html_mod.escape(p["title"])}</h3>'
        f"</div></article></a>"
        for p in BLOG_POSTS_EN
    )

    ssr, n_al = re.subn(
        r'(<div class="Articles_articlesList__CXW8a">).*?(<div class="Articles_mobileButton__Df7CF">)',
        lambda m: m.group(1) + ssr_items + m.group(2),
        ssr,
        count=1,
        flags=re.S,
    )
    if n_al != 1:
        raise RuntimeError("Failed to update EN Homepage Articles_articlesList__CXW8a in SSR")

    def mut(records):
        c = False
        for rec in records:
            if rec[0] == "line" and "Articles_articlesList__CXW8a" in rec[2]:
                ast = json.loads(rec[2])
                alist = find_node_by_class(ast, "Articles_articlesList__CXW8a")
                first_card = alist[3]["children"][0][0]
                link_id = first_card[1]
                img_id = first_card[3]["children"][3]["children"][0][3]["children"][1]
                alist[3]["children"][0] = [
                    [
                        "$",
                        link_id,
                        str(p["databaseId"]),
                        {
                            "href": f"/en/blog/{p['slug']}/",
                            "data-animation": "grid-item",
                            "children": [
                                "$",
                                "article",
                                None,
                                {
                                    "className": "Articles_article__3ZS4Y",
                                    "children": [
                                        [
                                            "$",
                                            "figure",
                                            None,
                                            {
                                                "className": "Articles_image__Cvgsi",
                                                "children": [
                                                    "$",
                                                    img_id,
                                                    None,
                                                    {
                                                        "image": {
                                                            "altText": p["title"],
                                                            "srcSet": f"{p['image']} 1400w",
                                                            "sourceUrl": p["image"],
                                                            "mediaDetails": {"width": p["img_w"], "height": p["img_h"]},
                                                        }
                                                    },
                                                ],
                                            },
                                        ],
                                        [
                                            "$",
                                            "div",
                                            None,
                                            {
                                                "className": "Articles_text__HhO2L",
                                                "children": [
                                                    [
                                                        "$",
                                                        "p",
                                                        None,
                                                        {"className": "Articles_filterNames__mCWt8", "children": p["category"]["name"]},
                                                    ],
                                                    [
                                                        "$",
                                                        "h3",
                                                        None,
                                                        {"className": "Articles_title__h86PB", "children": p["title"]},
                                                    ],
                                                ],
                                            },
                                        ],
                                    ],
                                },
                            ],
                        },
                    ]
                    for p in BLOG_POSTS_EN
                ]
                rec[2] = json.dumps(ast, ensure_ascii=False, separators=(",", ":"))
                c = True
        return c

    return ssr + rewrite_flight_in_html(tail, mut)


def build_en_homepage():
    en_title = "Roasist | 360° Digital Marketing, Performance & Growth Agency"
    en_desc = (
        "Roasist is a data-driven 360° digital growth agency scaling ambitious brands through high-ROAS "
        "performance marketing, AI-ready SEO & AEO, and conversion web design."
    )
    pairs = HOME_TR_TO_EN_PAIRS + EXTRA_HOME_PAIRS_EN + REFERENCES_TR_TO_EN_PAIRS
    for base_name, src_rel in (("public", "kota-roasist-local.html"), ("dist", "index.html")):
        src_fp = os.path.join(ROOT, base_name, src_rel)
        html = open(src_fp, "r", encoding="utf-8").read()
        html = sync_homepage_services_panels(html, HOMEPAGE_PANELS_EN)
        html = update_en_homepage_articles(html)
        html = apply_pairs_to_page(html, pairs)
        html = apply_en_chrome_and_seo(html, "/en/", en_title, en_desc, is_dist=(base_name == "dist"), is_home=True)
        write_en_output(base_name, "", html)
    print("[EN] Built /en/index.html (public + dist)")


# ==============================================================================
# PAGE BUILDER 2: WHO WE ARE (/en/who-we-are/index.html)
# ==============================================================================
EXTRA_ABOUT_PAIRS_EN = [
    ("Vizyon", "Vision"),
    ("Misyon", "Mission"),
    ("Markalar", "Partner Brands"),
    ('href="/iletisim/"', 'href="/en/contact-us/"'),
    ('href="/iletisim"', 'href="/en/contact-us/"'),
    ('"href":"/iletisim/"', '"href":"/en/contact-us/"'),
    ('"href":"/iletisim"', '"href":"/en/contact-us/"'),
]


def build_en_about():
    en_title = "Who We Are | About Roasist Digital Growth Agency"
    en_desc = (
        "Roasist is a next-generation digital growth and performance marketing agency defined by tailored "
        "strategy, process discipline, creative quality, and speed."
    )
    pairs = ABOUT_TR_TO_EN_PAIRS + EXTRA_ABOUT_PAIRS_EN
    for base_name in ("public", "dist"):
        src_fp = os.path.join(ROOT, base_name, "hakkimizda", "index.html")
        html = open(src_fp, "r", encoding="utf-8").read()
        html = apply_pairs_to_page(html, pairs)
        html = apply_en_chrome_and_seo(html, "/en/who-we-are/", en_title, en_desc, is_dist=(base_name == "dist"))
        write_en_output(base_name, "who-we-are", html)
    print("[EN] Built /en/who-we-are/index.html (public + dist)")


# ==============================================================================
# PAGE BUILDER 3: 13 ENGLISH SERVICE PAGES (/en/<slug>/index.html)
# ==============================================================================
HUB_TR_NORM = normalize_service_dict(
    {
        "slug": "hizmetler",
        "seoTitle": "Hizmetlerimiz | 360° Dijital Pazarlama & Web Tasarım | Roasist",
        "seoDescription": "Performans pazarlaması, Google & Meta reklamları, SEO, kreatif tasarım ve web yazılım çözümleriyle markanızı büyütüyoruz.",
        "h1": "360° Dijital Büyüme & Pazarlama Hizmetlerimiz",
        "heroLines": ["Markanızı", "<em>büyüten</em>", "360° çözümler."],
        "introText": "Performans pazarlaması, SEO, kreatif tasarım ve yüksek dönüşümlü web geliştirme uzmanlığımızı tek bir stratejik çatı altında birleştirerek markanızın cirosunu ve ROAS verimliliğini ölçeklendiriyoruz.",
        "introHeading": "Veri, teknoloji ve yaratıcılık tek merkezde.",
        "introBody": "Roasist olarak reklam yönetiminden arama motoru optimizasyonuna, kullanıcı deneyimi tasarımından dönüşüm hunisi (CRO) mimarisine kadar tüm dijital büyüme kanallarınızı birbiriyle tam entegre biçimde yönetiyoruz.",
        "features": [
            {
                "title": "Performans Pazarlaması & Reklam.",
                "text": "Google Ads, Meta (Instagram & Facebook), TikTok, LinkedIn ve Yandex reklamlarında yapay zeka destekli teklif stratejileri ve CAPI entegrasyonuyla kârlı büyüme sağlıyoruz.",
                "href": "/hizmetler/performans-pazarlamasi/",
            },
            {
                "title": "Teknik SEO & Organik Büyüme.",
                "text": "Teknik SEO, semantik içerik mimarisi ve AI arama (GEO/AEO) optimizasyonuyla markanızı arama motorlarında kalıcı olarak zirveye taşıyoruz.",
                "href": "/hizmetler/seo/",
            },
            {
                "title": "Yüksek Dönüşümlü Web & Kreatif.",
                "text": "Hızlı, modern ve dönüşüm odaklı web siteleri ile dikkat çeken reklam kreatifleri tasarlayarak tıklamaları gerçek müşterilere dönüştürüyoruz.",
                "href": "/hizmetler/web-tasarim/",
            },
        ],
        "metrics": [
            {"value": "6.4x", "label": "Yönetilen performans kampanyalarında ortalama ROAS."},
            {"value": "+185%", "label": "Organik ve ücretli kanallarda yıllık ciro büyümesi."},
            {"value": "-38%", "label": "Dönüşüm hunisi optimizasyonuyla düşen edinim maliyeti (CPA)."},
            {"value": "360°", "label": "Tüm dijital kanallarda tek elden entegre büyüme yönetimi."},
        ],
        "processHeading": "Roasist 360° Büyüme Metodolojimiz.",
        "processSubheading": "Teşhis ve stratejiden çok kanallı icraya, kreatif testlerden canlı veri raporlamasına kadar her adımı şeffaf biçimde yönetiyoruz.",
        "processSteps": SERVICES_BY_SLUG["360-derece-dijital-pazarlama-yonetimi"]["processSteps"],
        "faqs": SERVICES_BY_SLUG["360-derece-dijital-pazarlama-yonetimi"]["faqs"],
    }
)


def build_related_posts_ssr_cards_en(posts: list[dict]) -> str:
    return "".join(
        f'<a class="BlogPostCard_post__fNGbL" data-animation="grid-item" href="/en/blog/{p["slug"]}/">'
        f'<div class="BlogPostCard_postImage__Q4k_I">'
        f'<div class="BlogPostCard_tags__RKboe"><span class="BlogPostCard_tag__Dv5HS">{html_mod.escape(p["category"]["name"])}</span></div>'
        f'<span class="Image_image__RAAdZ Image_fill__EiIzS">'
        f'<img data-srcset="{p["image"]} 1400w" data-src="{p["image"]}" alt="{html_mod.escape(p["title"], quote=True)}" fetchPriority="low" height="{p["img_h"]}" width="{p["img_w"]}" sizes="auto" class="lazyload"/>'
        f"</span></div>"
        f'<div class="BlogPostCard_postText__V0sxg"><h3>{html_mod.escape(p["title"])}</h3></div></a>'
        for p in posts
    )


def build_related_posts_flight_cards_en(posts: list[dict], link_id: str, img_id: str) -> list:
    return [
        [
            "$",
            link_id,
            str(p["databaseId"]),
            {
                "className": "BlogPostCard_post__fNGbL",
                "href": f"/en/blog/{p['slug']}/",
                "data-animation": "grid-item",
                "children": [
                    [
                        "$",
                        "div",
                        None,
                        {
                            "className": "BlogPostCard_postImage__Q4k_I",
                            "children": [
                                [
                                    "$",
                                    "div",
                                    None,
                                    {
                                        "className": "BlogPostCard_tags__RKboe",
                                        "children": [
                                            False,
                                            [
                                                [
                                                    "$",
                                                    "span",
                                                    p["category"]["name"],
                                                    {"className": "BlogPostCard_tag__Dv5HS", "children": p["category"]["name"]},
                                                ]
                                            ],
                                        ],
                                    },
                                ],
                                [
                                    "$",
                                    img_id,
                                    None,
                                    {
                                        "fill": True,
                                        "image": {
                                            "altText": p["title"],
                                            "srcSet": f"{p['image']} 1400w",
                                            "sourceUrl": p["image"],
                                            "mediaDetails": {"width": p["img_w"], "height": p["img_h"]},
                                        },
                                    },
                                ],
                            ],
                        },
                    ],
                    [
                        "$",
                        "div",
                        None,
                        {"className": "BlogPostCard_postText__V0sxg", "children": ["$", "h3", None, {"children": p["title"]}]},
                    ],
                ],
            },
        ]
        for p in posts
    ]


def update_en_service_related_posts(html_text: str) -> str:
    ssr_cards = build_related_posts_ssr_cards_en(BLOG_POSTS_EN)
    pushes = list(PUSH_RE.finditer(html_text))
    ssr = html_text[: pushes[0].start()]
    tail = html_text[pushes[0].start() :]

    def repl_rp(m):
        sec = m.group(0)
        sec = sec.replace('href="/blog/"', 'href="/en/blog/"').replace('href="/blog"', 'href="/en/blog/"')
        sec = sec.replace("İlgili Blog Yazıları", "Related Insights").replace("Tüm Yazıları Gör", "View All Articles")
        sec, _ = re.subn(
            r'(<div class="AnimatedGrid_grid__otAMD"><div class="container">).*?(</div></div><div class="container"><div class="RelatedPosts_viewAllLinkMobile__joii8">)',
            lambda gm: gm.group(1) + ssr_cards + gm.group(2),
            sec,
            count=1,
            flags=re.S,
        )
        return sec

    ssr = re.sub(r'<section class="RelatedPosts_relatedPosts__xfLkb">.*?</section>', repl_rp, ssr, count=1, flags=re.S)

    def mut(records):
        c = False
        for rec in records:
            if rec[0] == "line" and "RelatedPosts_relatedPosts__xfLkb" in rec[2]:
                ast = json.loads(rec[2])
                rp = find_node_by_class(ast, "RelatedPosts_relatedPosts__xfLkb")
                rp_s = (
                    json.dumps(rp, ensure_ascii=False, separators=(",", ":"))
                    .replace('"href":"/blog/"', '"href":"/en/blog/"')
                    .replace('"href":"/blog"', '"href":"/en/blog/"')
                    .replace("İlgili Blog Yazıları", "Related Insights")
                    .replace("Tüm Yazıları Gör", "View All Articles")
                )
                rp_new = json.loads(rp_s)
                grid_c = rp_new[3]["children"][2][3]["children"]
                fc = grid_c[3]["children"][0]
                c_link_id = fc[1]
                c_img_id = fc[3]["children"][0][3]["children"][1][1]
                grid_c[3]["children"] = build_related_posts_flight_cards_en(BLOG_POSTS_EN, c_link_id, c_img_id)
                rp[:] = rp_new
                rec[2] = json.dumps(ast, ensure_ascii=False, separators=(",", ":"))
                c = True
        return c

    return ssr + rewrite_flight_in_html(tail, mut)


def build_tr_to_en_service_pairs(en_spec: dict) -> list[tuple[str, str]]:
    src_tr = en_spec["src_tr"]
    if src_tr == "hizmetler":
        tr_norm = HUB_TR_NORM
    else:
        tr_slug = src_tr[len("hizmetler/") :]
        raw_tr = dict(SERVICES_BY_SLUG[tr_slug])
        if tr_slug == "performans-pazarlamasi":
            for k in ("seoDescription", "aeoDirectAnswer"):
                if k in raw_tr:
                    raw_tr[k] = raw_tr[k].replace(
                        "Google Ads, Meta, TikTok, LinkedIn ve Yandex",
                        "Google Ads, Meta, TikTok, Yandex, Bing ve LinkedIn",
                    )
        tr_norm = normalize_service_dict(raw_tr)
        if tr_slug == "performans-pazarlamasi/bing-reklamlari":
            yandex_norm = normalize_service_dict(SERVICES_BY_SLUG["performans-pazarlamasi/yandex-reklamlari"])
            tr_norm["heroLines"] = ["Küresel aramada", "<em>Bing Ads</em>", "verimliliği."]
            tr_norm["processSteps"] = yandex_norm["processSteps"]
            tr_norm["metrics"] = [
                {"value": "Microsoft Ağı", "label": "Masaüstü ve kurumsal aramalarda yüksek satın alma gücü"},
                {"value": "Düşük CPC", "label": "Daha düşük rekabet ve birim tıklama maliyetiyle kârlı dönüşüm"},
                {"value": "LinkedIn Verisi", "label": "Microsoft ekosistemi üzerinden şirket, sektör ve unvan hedeflemesi"},
            ]

    tr_lines = tr_norm["heroLines"]
    en_lines = en_spec["heroLines"]
    tr_h2_rn = f"{tr_lines[0]} <br />\r\n{tr_lines[1]}<br />\r\n{tr_lines[2]}"
    tr_h2_n = f"{tr_lines[0]} <br />\n{tr_lines[1]}<br />\n{tr_lines[2]}"
    en_h2_rn = f"{en_lines[0]} <br />\r\n{en_lines[1]}<br />\r\n{en_lines[2]}"
    en_h2_n = f"{en_lines[0]} <br />\n{en_lines[1]}<br />\n{en_lines[2]}"

    pairs = [
        (tr_norm["title"], en_spec["title"]),
        (tr_norm["metaDesc"], en_spec["metaDesc"]),
        (tr_norm["h1"], en_spec["h1"]),
        (tr_h2_rn, en_h2_rn),
        (tr_h2_n, en_h2_n),
        (tr_norm["introText"], en_spec["introText"]),
        (tr_norm["introHeading"], en_spec["introHeading"]),
        (tr_norm["introBody"], en_spec["introBody"]),
        (tr_norm["processHeading"], en_spec["processHeading"]),
        (tr_norm["processSubheading"], en_spec["processSubheading"]),
    ]

    if en_spec["en_slug"] == "performance-marketing":
        for tr_ch, en_feat in zip(TR_PERF_CHANNELS, en_spec["features"]):
            pairs.append((tr_ch["title"], en_feat["title"]))
            pairs.append((tr_ch["description"], en_feat["text"]))
            pairs.append((f'"{tr_ch["href"]}"', f'"{en_feat["href"]}"'))
    else:
        for tr_feat, en_feat in zip(tr_norm["features"], en_spec["features"]):
            pairs.append((tr_feat["title"], en_feat["title"]))
            pairs.append((tr_feat["text"], en_feat["text"]))

    for tr_m, en_m in zip(tr_norm["metrics"], en_spec["metrics"]):
        pairs.append((tr_m["label"], en_m["label"]))
        if tr_m["value"] != en_m["value"]:
            pairs.append((f">{tr_m['value']}<", f">{en_m['value']}<"))
            pairs.append((f'"{tr_m["value"]}"', f'"{en_m["value"]}"'))

    for tr_st, (en_st_title, en_st_text) in zip(tr_norm["processSteps"], en_spec["steps"]):
        pairs.append((f">{tr_st['title']}<", f">{en_st_title}<"))
        pairs.append((f'"{tr_st["title"]}"', f'"{en_st_title}"'))
        pairs.append((tr_st["title"], en_st_title))
        pairs.append((tr_st["text"], en_st_text))

    for tr_fq, (en_fq_q, en_fq_a) in zip(tr_norm["faqs"], en_spec["faqs"]):
        pairs.append((tr_fq["q"], en_fq_q))
        pairs.append((tr_fq["a"], en_fq_a))

    pairs.extend(TIMELINE_TR_TO_EN)
    pairs.extend(REFERENCES_TR_TO_EN_PAIRS)
    pairs.extend(
        [
            ("Müşterilerimiz Ne Diyor?", "What Our Clients Say"),
            (
                '"Reklam sürecinde projeye yaklaşımları, anlaşmamızın ötesinde sorumluluk alarak grafik tasarım katkısı sunmaları ve 7/24 destekleriyle işimiz için en az bizim kadar dertlenen bir ekiple çalıştığımız için şanslıyız. Roasist ile gönül rahatlığıyla çalışabilirsiniz."',
                ROASIST_TESTIMONIALS_EN[0]["text"],
            ),
            (
                '"Roasist ile yaklaşık iki senedir çalışıyoruz. Her sorumuza dürüstlükle yanıt alıyor, tüm sorunlarımızı efektif bir şekilde çözüyorlar. Öncesi-sonrası değerlendirmesi yaptığımda kazanç konusunda bize çok büyük katkıları oldu. Profesyonel yaklaşımları için çok teşekkür ederim."',
                ROASIST_TESTIMONIALS_EN[1]["text"],
            ),
            ("Girişimci & Kurucu", "Entrepreneur & Founder"),
            (
                '"Mesai kavramı olmaksızın sizin için çalışıyorlar. İşinde profesyonel, şeffaf ve doğrudan sonuç odaklı bir dijital pazarlama ajansı arıyorsanız Roasist\'i kesinlikle tavsiye ederim."',
                ROASIST_TESTIMONIALS_EN[2]["text"],
            ),
            ("İşletme Sahibi", "Business Owner"),
            ("Diğer Hizmetlerimiz", "Explore Our Services"),
            ("Google Reklamları", "Google Ads"),
            ("SEO Hizmeti", "Enterprise SEO"),
            ("Web Tasarım & Yazılım", "Web Design & Dev"),
            ('"/hizmetler/performans-pazarlamasi/"', '"/en/performance-marketing/"'),
            ('"/hizmetler/performans-pazarlamasi/google-reklamlari/"', '"/en/google-ads/"'),
            ('"/hizmetler/google-reklamlari/"', '"/en/google-ads/"'),
            ('"/hizmetler/performans-pazarlamasi/instagram-reklamlari/"', '"/en/instagram-ads/"'),
            ('"/hizmetler/instagram-reklamlari/"', '"/en/instagram-ads/"'),
            ('"/hizmetler/performans-pazarlamasi/facebook-reklamlari/"', '"/en/facebook-ads/"'),
            ('"/hizmetler/facebook-reklamlari/"', '"/en/facebook-ads/"'),
            ('"/hizmetler/performans-pazarlamasi/tiktok-reklamlari/"', '"/en/tiktok-ads/"'),
            ('"/hizmetler/tiktok-reklamlari/"', '"/en/tiktok-ads/"'),
            ('"/hizmetler/performans-pazarlamasi/linkedin-reklamlari/"', '"/en/linkedin-ads/"'),
            ('"/hizmetler/linkedin-reklamlari/"', '"/en/linkedin-ads/"'),
            ('"/hizmetler/performans-pazarlamasi/yandex-reklamlari/"', '"/en/yandex-ads/"'),
            ('"/hizmetler/yandex-reklamlari/"', '"/en/yandex-ads/"'),
            ('"/hizmetler/performans-pazarlamasi/bing-reklamlari/"', '"/en/bing-ads/"'),
            ('"/hizmetler/bing-reklamlari/"', '"/en/bing-ads/"'),
            ('"/hizmetler/seo/"', '"/en/seo/"'),
            ('"/hizmetler/grafik-tasarim/"', '"/en/graphic-design/"'),
            ('"/hizmetler/web-tasarim/"', '"/en/web-design/"'),
            ('"/hizmetler/360-derece-dijital-pazarlama-yonetimi/"', '"/en/360-digital-marketing-management/"'),
            ('"/referanslar/"', '"/en/references/"'),
            ('"/referanslar"', '"/en/references/"'),
            ('"/iletisim/"', '"/en/contact-us/"'),
            ('"/iletisim"', '"/en/contact-us/"'),
            ('"/start-your-project"', '"/en/contact-us/"'),
            ("Estetik Tasarım. Ölçülebilir Büyüme.", "Strategic Craft. Measurable Growth."),
            ("Verilerle Kanıtlanmış Performans.", "Data-Backed Performance."),
            ("Detaylı İncele", "Explore Service"),
            ("Başarı Hikayelerimiz", "Selected Case Studies"),
            ("Tüm Referansları Gör", "View All Case Studies"),
            ("Projeyi İncele", "View Case Study"),
            ("Sıkça Sorulan Sorular", "Frequently Asked Questions"),
            ("Markanızı Roasist ile büyütmeye hazır mısınız?", "Ready to scale your brand with Roasist?"),
            (
                '<p>Bize hemen ulaşın:<br />\n<a href="mailto:info@roasist.com">info@roasist.com</a></p>\n',
                '<p>Drop us a line today:<br />\n<a href="mailto:info@roasist.com">info@roasist.com</a></p>\n',
            ),
            (
                "Performans pazarlaması, Google & Meta reklamları, SEO, kreatif tasarım ve web yazılım çözümleriyle markanızı kârlı biçimde ölçeklendiren 360° dijital büyüme ajansıyız.",
                "We are a 360° digital growth agency scaling ambitious brands profitably through performance marketing, Google & Meta Ads, enterprise SEO, creative design, and web engineering.",
            ),
            ("Projeye Başlayın", "Start a Project"),
            ("Yüksek ROAS Verimliliği", "High ROAS Efficiency"),
            ("Profil Bazlı Hedefleme", "Profile-Based Targeting"),
            ("Microsoft Ağı — ", "Microsoft Network — "),
            ("Düşük CPC — ", "Low CPC — "),
            ("LinkedIn Verisi — ", "LinkedIn Data — "),
            ("Ortalama dönüşüm ve ROAS artışı.", "Average conversion and ROAS uplift."),
        ]
    )
    return pairs


def build_en_services():
    for spec in EN_SERVICES_SPECS:
        en_slug = spec["en_slug"]
        en_route = f"/en/{en_slug}/"
        pairs = build_tr_to_en_service_pairs(spec)
        for base_name in ("public", "dist"):
            src_fp = os.path.join(ROOT, base_name, spec["src_tr"], "index.html")
            html = open(src_fp, "r", encoding="utf-8").read()
            html = update_en_service_related_posts(html)
            html = apply_pairs_to_page(html, pairs)
            html = apply_en_chrome_and_seo(
                html,
                en_route,
                spec["title"],
                spec["metaDesc"],
                is_dist=(base_name == "dist"),
            )
            write_en_output(base_name, en_slug, html)
        print(f"[EN] Built {en_route}index.html (public + dist)")


# ==============================================================================
# PAGE BUILDER 4: REFERENCES / CASE STUDIES (/en/references/index.html)
# ==============================================================================
def build_en_references():
    en_title = "Our Work & Case Studies | Roasist"
    en_desc = (
        "Explore how Roasist scales ambitious brands across healthcare, real estate, e-commerce, SaaS, "
        "hospitality, and B2B through performance marketing, SEO, and web design."
    )
    pairs = REFERENCES_TR_TO_EN_PAIRS + [
        (
            "Roasist; performans pazarlaması, SEO, kreatif tasarım ve web teknolojilerini birleştirerek ulusal ve global markalar için ölçülebilir büyüme hikayeleri yaratır.",
            "Roasist unites performance marketing, enterprise SEO, creative design, and web engineering to build measurable growth stories for national and global brands.",
        ),
        (">Referanslar<", ">Our Work<"),
        ('"children":"Referanslar"', '"children":"Our Work"'),
        ("Web Tasarım & Yazılım", "Web Design & Dev"),
        ("Kreatif & Marka", "Creative & Brand"),
        ("Projeyi İncele", "View Case Study"),
        ("Markanızı Roasist ile büyütmeye hazır mısınız?", "Ready to scale your brand with Roasist?"),
        (
            '<p>Bize hemen ulaşın:<br />\n<a href="mailto:info@roasist.com">info@roasist.com</a></p>\n',
            '<p>Drop us a line today:<br />\n<a href="mailto:info@roasist.com">info@roasist.com</a></p>\n',
        ),
        (
            "Performans pazarlaması, Google & Meta reklamları, SEO, kreatif tasarım ve web yazılım çözümleriyle markanızı kârlı biçimde ölçeklendiren 360° dijital büyüme ajansıyız.",
            "We are a 360° digital growth agency scaling ambitious brands profitably through performance marketing, Google & Meta Ads, enterprise SEO, creative design, and web engineering.",
        ),
        ("Projeye Başlayın", "Start a Project"),
        ('"/iletisim/"', '"/en/contact-us/"'),
        ('"/iletisim"', '"/en/contact-us/"'),
        ('"/start-your-project"', '"/en/contact-us/"'),
    ]
    for base_name in ("public", "dist"):
        src_fp = os.path.join(ROOT, base_name, "referanslar", "index.html")
        html = open(src_fp, "r", encoding="utf-8").read()
        html = apply_pairs_to_page(html, pairs)
        html = apply_en_chrome_and_seo(html, "/en/references/", en_title, en_desc, is_dist=(base_name == "dist"))
        write_en_output(base_name, "references", html)
    print("[EN] Built /en/references/index.html (public + dist)")


# ==============================================================================
# PAGE BUILDER 5: BLOG INDEX (/en/blog/) & 3 ENGLISH ARTICLES (/en/blog/<slug>/)
# ==============================================================================
def build_en_blog():
    blog_title = "Digital Growth & Performance Marketing Blog | Roasist"
    blog_desc = (
        "Actionable guides on high-ROAS performance marketing, Google & Meta Ads, enterprise technical SEO, "
        "AI search (AEO/GEO), and conversion optimization from the Roasist strategy team."
    )
    featured = BLOG_POSTS_EN[0]

    flight_cat_nodes = [
        {
            "node": {
                "slug": c["slug"],
                "name": c["name"],
                "databaseId": c["databaseId"],
                "id": f"dGVybTo{c['databaseId']}=",
                "isContentNode": False,
                "isTermNode": True,
                "count": 1,
            }
        }
        for c in BLOG_CATEGORIES_EN
    ]

    flight_posts_nodes = [
        {
            "node": {
                "title": p["title"],
                "databaseId": p["databaseId"],
                "categories": {"edges": [{"node": {"slug": p["category"]["slug"], "name": p["category"]["name"]}}]},
                "slug": p["slug"],
                "singlePost": {
                    "postDetails": {
                        "featuredImage": {
                            "altText": p["title"],
                            "srcSet": f"{p['image']} 1400w",
                            "sourceUrl": p["image"],
                            "mediaDetails": {"width": p["img_w"], "height": p["img_h"]},
                        }
                    }
                },
            }
        }
        for p in BLOG_POSTS_EN
    ]

    blog_common_pairs = REFERENCES_TR_TO_EN_PAIRS + [
        ("Markanızı Roasist ile büyütmeye hazır mısınız?", "Ready to scale your brand with Roasist?"),
        (
            '<p>Bize hemen ulaşın:<br />\n<a href="mailto:info@roasist.com">info@roasist.com</a></p>\n',
            '<p>Drop us a line today:<br />\n<a href="mailto:info@roasist.com">info@roasist.com</a></p>\n',
        ),
        (
            "Performans pazarlaması, Google & Meta reklamları, SEO, kreatif tasarım ve web yazılım çözümleriyle markanızı kârlı biçimde ölçeklendiren 360° dijital büyüme ajansıyız.",
            "We are a 360° digital growth agency scaling ambitious brands profitably through performance marketing, Google & Meta Ads, enterprise SEO, creative design, and web engineering.",
        ),
        ("Projeye Başlayın", "Start a Project"),
        ("Öne Çıkan", "Featured"),
        ('"/iletisim/"', '"/en/contact-us/"'),
        ('"/iletisim"', '"/en/contact-us/"'),
        ('"/start-your-project"', '"/en/contact-us/"'),
    ]

    for base_name in ("public", "dist"):
        src_fp = os.path.join(ROOT, base_name, "blog", "index.html")
        html = open(src_fp, "r", encoding="utf-8").read()
        pushes = list(PUSH_RE.finditer(html))
        ssr = html[: pushes[0].start()]
        tail = html[pushes[0].start() :]

        new_featured_ssr = (
            '<div class="FeaturedBlogPost_featuredPost__aRcs9"><div class="container">'
            '<span class="AnimatedFeaturedBlog_container__mnIll" data-fill="false">'
            f'<a class="BlogPostCard_post__fNGbL BlogPostCard_large__STeKf" data-animation="grid-item" href="/en/blog/{featured["slug"]}/">'
            '<div class="BlogPostCard_postImage__Q4k_I">'
            '<div class="BlogPostCard_tags__RKboe">'
            '<span class="BlogPostCard_tag__Dv5HS">Featured</span>'
            f'<span class="BlogPostCard_tag__Dv5HS">{html_mod.escape(featured["category"]["name"])}</span>'
            "</div>"
            '<span class="Image_image__RAAdZ Image_fill__EiIzS">'
            f'<img data-srcset="{featured["image"]} 1400w" data-src="{featured["image"]}" alt="{html_mod.escape(featured["title"], quote=True)}" fetchPriority="low" height="{featured["img_h"]}" width="{featured["img_w"]}" sizes="auto" class="lazyload"/>'
            "</span></div>"
            f'<div class="BlogPostCard_postText__V0sxg"><h3>{html_mod.escape(featured["title"])}</h3></div>'
            "</a></span></div></div>"
        )
        ssr, _ = re.subn(
            r'<div class="FeaturedBlogPost_featuredPost__aRcs9">.*?(<div class="Blog_postsWithFilters__aXNNs">)',
            lambda m: new_featured_ssr + m.group(1),
            ssr,
            count=1,
            flags=re.S,
        )
        en_grid_cards_ssr = build_related_posts_ssr_cards_en(BLOG_POSTS_EN)
        ssr = re.sub(
            r'(<div class="PostsGrid_grid__[^"]*">).*?(</div></div></div></div>)',
            lambda m: m.group(1) + en_grid_cards_ssr + m.group(2),
            ssr,
            count=1,
            flags=re.S,
        )

        def blog_idx_mut(records):
            for rec in records:
                if rec[0] == "line" and rec[1] == "d":
                    ast = json.loads(rec[2])
                    main_ch = ast[2][3]["children"]
                    feat_wrap = main_ch[1]
                    feat_card = feat_wrap[3]["children"][3]["children"][3]["children"]
                    feat_card[2] = str(featured["databaseId"])
                    feat_card[3]["href"] = f"/en/blog/{featured['slug']}/"
                    feat_tags = feat_card[3]["children"][0][3]["children"][0][3]["children"]
                    feat_tags[0] = ["$", "span", None, {"className": "BlogPostCard_tag__Dv5HS", "children": "Featured"}]
                    feat_tags[1] = [
                        [
                            "$",
                            "span",
                            featured["category"]["name"],
                            {"className": "BlogPostCard_tag__Dv5HS", "children": featured["category"]["name"]},
                        ]
                    ]
                    feat_card[3]["children"][0][3]["children"][1][3]["image"] = {
                        "altText": featured["title"],
                        "srcSet": f"{featured['image']} 1400w",
                        "sourceUrl": featured["image"],
                        "mediaDetails": {"width": featured["img_w"], "height": featured["img_h"]},
                    }
                    feat_card[3]["children"][1][3]["children"][3]["children"] = featured["title"]

                    pwf = main_ch[2]
                    inner_pair = pwf[3]["children"][3]["children"][3]["children"][3]["children"]
                    inner_pair[0][3]["children"][3]["categories"] = flight_cat_nodes
                    inner_pair[1][3]["posts"] = flight_posts_nodes
                    rec[2] = json.dumps(ast, ensure_ascii=False, separators=(",", ":"))
            return True

        combined = ssr + rewrite_flight_in_html(tail, blog_idx_mut)
        combined = apply_pairs_to_page(combined, blog_common_pairs)
        combined = apply_en_chrome_and_seo(combined, "/en/blog/", blog_title, blog_desc, is_dist=(base_name == "dist"))
        write_en_output(base_name, "blog", combined)
    print("[EN] Built /en/blog/index.html (public + dist)")

    icon_url = f"{CDN_BASE}/icon.png"
    article_extra_pairs = blog_common_pairs + [
        ("Başarı Hikayelerimiz", "Selected Case Studies"),
        ("Tüm Referansları Gör", "View All Case Studies"),
        ("Projeyi İncele", "View Case Study"),
        ('"/referanslar/"', '"/en/references/"'),
        ('"/referanslar"', '"/en/references/"'),
    ]

    for post in BLOG_POSTS_EN:
        en_route = f"/en/blog/{post['slug']}/"
        canonical_url = f"{SITE_ORIGIN}{en_route}"
        enc_url = urllib.parse.quote(canonical_url, safe="")
        prose_full = f"<p class=\"lead\">{post['intro']}</p>\n{post['body_html']}"

        for base_name in ("public", "dist"):
            src_fp = os.path.join(ROOT, base_name, "blog", "Performans-Pazarlamasi-Nedir", "index.html")
            tpl = open(src_fp, "r", encoding="utf-8").read()
            pushes = list(PUSH_RE.finditer(tpl))
            ssr = tpl[: pushes[0].start()]
            tail = tpl[pushes[0].start() :]

            m_rp_proj = re.search(
                r'(<section class="RelatedProjects_relatedProjects__6931f">.*?</section><section class="LargeCta_largeCta__ylf5C">.*?</section>)',
                ssr,
                flags=re.S,
            )
            rp_and_cta_ssr = m_rp_proj.group(1) if m_rp_proj else ""

            new_article_ssr = (
                '<article class="BlogPost_blogPost__Mtvlq">'
                '<div class="Hero_hero__mn1R_"><div class="container">'
                '<div class="Hero_left__0LdJX">'
                '<div><span class="FadeIn_container__bjQVL" data-fill="false">'
                f'<div class="Hero_categoriesInner__G68BO"><button class="Hero_category__qOhtb">{html_mod.escape(post["category"]["name"])}</button></div>'
                "</span></div>"
                f'<h1><span class="FadeIn_container__bjQVL" data-fill="false"><span>{html_mod.escape(post["title"])}</span></span></h1>'
                "</div>"
                '<div class="Hero_right__AZ10b"><div class="Hero_author__3asj1">'
                '<figure class="Hero_authorImage__h9wNd"><span class="FadeIn_container__bjQVL" data-fill="true">'
                f'<span class="Image_image__RAAdZ Image_fill__EiIzS"><img src="{icon_url}" alt="Roasist" loading="eager" fetchPriority="high" height="512" width="512" sizes="100vw"/></span>'
                "</span></figure>"
                f'<p class="Hero_date__30zpk"><span class="FadeIn_container__bjQVL" data-fill="false"><span>{html_mod.escape(post["read_time"])} • {html_mod.escape(post["date_label"])}</span></span></p>'
                '<p class="Hero_name__eLY42"><span class="FadeIn_container__bjQVL" data-fill="false"><span>Author: <!-- -->Roasist Strategy Team</span></span></p>'
                "</div></div>"
                '<figure class="Hero_image__1mu0E"><div class="ImageEnter_image__FSEP_" data-fill="true">'
                f'<span class="Image_image__RAAdZ Image_fill__EiIzS"><img srcSet="{post["image"]} 1400w" src="{post["image"]}" alt="{html_mod.escape(post["title"], quote=True)}" loading="eager" fetchPriority="low" height="{post["img_h"]}" width="{post["img_w"]}" sizes="100vw"/></span>'
                "</div></figure></div></div>"
                '<section class="ContentBuilder_contentBuilder__jY2p_">'
                '<section class="Text_text__jOaGN"><span class="FadeInUp_container___uxva" data-fill="false">'
                f'<div class="container"><div class="Text_textInner__lCgQa"><div class="prose">{prose_full}</div></div></div>'
                "</span></section></section>"
                '<section class="Share_share__5W87u"><span class="FadeIn_container__bjQVL" data-fill="false">'
                '<div class="container"><div class="Share_links__CutyY">'
                "<p>Share : </p>"
                f'<a class="Share_link__ERF_r" href="https://www.linkedin.com/shareArticle?mini=true&amp;url={enc_url}" target="_blank" rel="noopener noreferrer">LinkedIn</a>'
                f'<a class="Share_link__ERF_r" href="https://www.facebook.com/sharer/sharer.php?u={enc_url}" target="_blank" rel="noopener noreferrer">Facebook</a>'
                f'<a class="Share_link__ERF_r" href="https://twitter.com/intent/tweet?&amp;url={enc_url}" target="_blank" rel="noopener noreferrer">𝕏</a>'
                "</div></div></span></section>"
                '<div class="container"><div class="BlogPost_buttonOuter__M9Wmd">'
                '<span class="FadeIn_container__bjQVL" data-fill="false"><div class="Magnetic_magnetic__LncOy" data-fill="false">'
                '<div class="Button_button__JJiqJ" data-direction="backwards"><a class="Button_inner__fnyH6" href="/en/blog/">'
                '<span class="Button_border__hirH2"></span><span class="Button_text__IZaCD">'
                '<span class="Button_textInner__JTTHe">Back to Blog</span>'
                f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 17.1 15.17" class="Button_buttonArrow__0W9XI"><path d="{BUTTON_ARROW_PATH_D}" fill="currentColor"></path></svg>'
                "</span></a></div></div></span></div></div>"
                '<section class="RelatedPosts_relatedPosts__xfLkb">'
                '<div class="DarkThemeSwitch_cover__hn_xc"></div>'
                '<div class="container"><div class="RelatedPosts_headingOuter__r3TEg">'
                '<p class="RelatedPosts_heading__3kOeH"><span class="FadeInUp_container___uxva" data-fill="false">Related Insights</span></p>'
                '<div class="RelatedPosts_viewAllLinkDesktop__db363"><span class="FadeInUp_container___uxva" data-fill="false">'
                '<div class="Magnetic_magnetic__LncOy" data-fill="false"><div class="Button_button__JJiqJ Button_white__MQaf2" data-direction="forwards">'
                '<a class="Button_inner__fnyH6" href="/en/blog/"><span class="Button_border__hirH2"></span><span class="Button_text__IZaCD">'
                '<span class="Button_textInner__JTTHe">View All Articles</span>'
                f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 17.1 15.17" class="Button_buttonArrow__0W9XI"><path d="{BUTTON_ARROW_PATH_D}" fill="currentColor"></path></svg>'
                "</span></a></div></div></span></div></div></div>"
                f'<div class="AnimatedGrid_grid__otAMD"><div class="container">{build_related_posts_ssr_cards_en(BLOG_POSTS_EN)}</div></div>'
                '<div class="container"><div class="RelatedPosts_viewAllLinkMobile__joii8"><div class="Magnetic_magnetic__LncOy" data-fill="false">'
                '<div class="Button_button__JJiqJ Button_white__MQaf2" data-direction="forwards"><a class="Button_inner__fnyH6" href="/en/blog/">'
                '<span class="Button_border__hirH2"></span><span class="Button_text__IZaCD">'
                '<span class="Button_textInner__JTTHe">View All Articles</span>'
                f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 17.1 15.17" class="Button_buttonArrow__0W9XI"><path d="{BUTTON_ARROW_PATH_D}" fill="currentColor"></path></svg>'
                "</span></a></div></div></div></div></section>"
                f"{rp_and_cta_ssr}"
                "</article>"
            )

            ssr, _ = re.subn(
                r'<article class="BlogPost_blogPost__Mtvlq">.*?</article>',
                lambda _: new_article_ssr,
                ssr,
                count=1,
                flags=re.S,
            )

            def en_post_mut(records):
                for rec in records:
                    kind, key, val = rec
                    if kind == "line" and key == "0":
                        ast0 = json.loads(val)
                        ast0[3]["urlParts"] = ["", "en", "blog", post["slug"]]
                        rec[2] = json.dumps(ast0, ensure_ascii=False, separators=(",", ":"))
                    elif kind == "text" and key == "2d":
                        rec[2] = prose_full
                    elif kind == "line" and key == "f":
                        ast = json.loads(val)
                        art_ch = ast[2][3]["children"]
                        hero_ch = art_ch[0][3]["children"][3]["children"]
                        left_ch = hero_ch[0][3]["children"]
                        fade_id = left_ch[0][3]["children"][1]
                        left_ch[0][3]["children"][3]["children"][3]["children"] = [
                            ["$", "button", post["category"]["slug"], {"className": "Hero_category__qOhtb", "children": post["category"]["name"]}]
                        ]
                        left_ch[1][3]["children"][3]["children"][3]["children"] = post["title"]

                        author_ch = hero_ch[1][3]["children"][3]["children"]
                        author_ch[0][3]["children"][3]["children"][3]["image"] = {
                            "altText": "Roasist",
                            "srcSet": None,
                            "sourceUrl": icon_url,
                            "mediaDetails": {"width": 512, "height": 512},
                        }
                        author_ch[1][3]["children"][3]["children"][3]["children"] = f"{post['read_time']} • {post['date_label']}"
                        author_ch[2][3]["children"][3]["children"][3]["children"] = ["Author: ", "Roasist Strategy Team"]

                        hero_ch[2][3]["children"][3]["children"][3]["image"] = {
                            "altText": post["title"],
                            "srcSet": f"{post['image']} 1400w",
                            "sourceUrl": post["image"],
                            "mediaDetails": {"width": post["img_w"], "height": post["img_h"]},
                        }

                        art_ch[2] = [
                            "$",
                            "section",
                            None,
                            {
                                "className": "Share_share__5W87u",
                                "children": [
                                    "$",
                                    fade_id,
                                    None,
                                    {
                                        "children": [
                                            "$",
                                            "div",
                                            None,
                                            {
                                                "className": "container",
                                                "children": [
                                                    "$",
                                                    "div",
                                                    None,
                                                    {
                                                        "className": "Share_links__CutyY",
                                                        "children": [
                                                            ["$", "p", None, {"children": "Share : "}],
                                                            [
                                                                "$",
                                                                "a",
                                                                None,
                                                                {
                                                                    "className": "Share_link__ERF_r",
                                                                    "href": f"https://www.linkedin.com/shareArticle?mini=true&url={enc_url}",
                                                                    "target": "_blank",
                                                                    "rel": "noopener noreferrer",
                                                                    "children": "LinkedIn",
                                                                },
                                                            ],
                                                            [
                                                                "$",
                                                                "a",
                                                                None,
                                                                {
                                                                    "className": "Share_link__ERF_r",
                                                                    "href": f"https://www.facebook.com/sharer/sharer.php?u={enc_url}",
                                                                    "target": "_blank",
                                                                    "rel": "noopener noreferrer",
                                                                    "children": "Facebook",
                                                                },
                                                            ],
                                                            [
                                                                "$",
                                                                "a",
                                                                None,
                                                                {
                                                                    "className": "Share_link__ERF_r",
                                                                    "href": f"https://twitter.com/intent/tweet?&url={enc_url}",
                                                                    "target": "_blank",
                                                                    "rel": "noopener noreferrer",
                                                                    "children": "𝕏",
                                                                },
                                                            ],
                                                        ],
                                                    },
                                                ],
                                            },
                                        ]
                                    },
                                ],
                            },
                        ]

                        back_btn = art_ch[3][3]["children"][3]["children"][3]["children"]
                        back_btn[3]["href"] = "/en/blog/"
                        back_btn[3]["text"] = "Back to Blog"

                        rp_sec = json.loads(
                            json.dumps(art_ch[4], ensure_ascii=False, separators=(",", ":"))
                            .replace('"href":"/blog/"', '"href":"/en/blog/"')
                            .replace('"href":"/blog"', '"href":"/en/blog/"')
                            .replace("İlgili Blog Yazıları", "Related Insights")
                            .replace("Tüm Yazıları Gör", "View All Articles")
                        )
                        grid_c = rp_sec[3]["children"][2][3]["children"]
                        fc = grid_c[3]["children"][0]
                        grid_c[3]["children"] = build_related_posts_flight_cards_en(
                            BLOG_POSTS_EN, fc[1], fc[3]["children"][0][3]["children"][1][1]
                        )
                        art_ch[4] = rp_sec
                        rec[2] = json.dumps(ast, ensure_ascii=False, separators=(",", ":"))
                return True

            combined = ssr + rewrite_flight_in_html(tail, en_post_mut)
            combined = apply_pairs_to_page(combined, article_extra_pairs)
            combined = apply_en_chrome_and_seo(
                combined,
                en_route,
                post["seo_title"],
                post["meta_desc"],
                is_dist=(base_name == "dist"),
            )
            combined = re.sub(
                r'<meta property="og:image" content="[^"]*"\s*/>',
                f'<meta property="og:image" content="{post["image"]}"/>',
                combined,
            )
            write_en_output(base_name, f"blog/{post['slug']}", combined)
        print(f"[EN] Built {en_route}index.html (public + dist)")


# ==============================================================================
# PAGE BUILDER 6: CONTACT US (/en/contact-us/index.html)
# ==============================================================================
def build_en_contact():
    en_title = "Contact Us | Roasist Digital Marketing Agency"
    en_desc = (
        "Get in touch with Roasist's growth specialists for performance marketing, Google & Meta Ads, "
        "enterprise SEO, and conversion web design."
    )
    pairs = CONTACT_TR_TO_EN_PAIRS + REFERENCES_TR_TO_EN_PAIRS + [
        ("Pzt - Cum: 09:00 - 18:00", "Mon - Fri: 09:00 - 18:00"),
        ('"/referanslar/"', '"/en/references/"'),
        ('"/referanslar"', '"/en/references/"'),
        ('"/gizlilik-politikasi-ve-kullanim-sartlari/"', '"/en/privacy-policy-and-terms-of-use/"'),
    ]
    for base_name in ("public", "dist"):
        src_fp = os.path.join(ROOT, base_name, "iletisim", "index.html")
        html = open(src_fp, "r", encoding="utf-8").read()
        html = apply_pairs_to_page(html, pairs)
        html = apply_en_chrome_and_seo(html, "/en/contact-us/", en_title, en_desc, is_dist=(base_name == "dist"))
        write_en_output(base_name, "contact-us", html)
    print("[EN] Built /en/contact-us/index.html (public + dist)")


# ==============================================================================
# PAGE BUILDER 7: PRIVACY POLICY (/en/privacy-policy-and-terms-of-use/index.html)
# ==============================================================================
def build_en_privacy():
    en_title = "Privacy Policy & Terms of Use | Roasist"
    en_desc = (
        "Roasist Digital Marketing Agency privacy policy, cookie consent notice, GDPR & KVKK data "
        "protection principles, and website terms of use."
    )
    for base_name in ("public", "dist"):
        src_fp = os.path.join(ROOT, base_name, "gizlilik-politikasi-ve-kullanim-sartlari", "index.html")
        html = open(src_fp, "r", encoding="utf-8").read()
        pushes = list(PUSH_RE.finditer(html))
        ssr = html[: pushes[0].start()]
        tail = html[pushes[0].start() :]

        ssr = replace_exact_div(
            ssr,
            '<div class="prose">',
            f'<div class="prose"><h1>Privacy Policy &amp; Terms of Use</h1><div>{PRIVACY_EN_HTML}</div></div>',
        )
        ssr = ssr.replace("Yeni bir dijital büyüme projeniz mi var?", "Have a new digital growth project?")
        ssr = ssr.replace("Hemen <!-- --><em>başlayalım</em>", "Let&#x27;s get <!-- --><em>started</em>")
        ssr = ssr.replace("Hemen <em>başlayalım</em>", "Let&#x27;s get <em>started</em>")
        ssr = ssr.replace('href="/iletisim/"', 'href="/en/contact-us/"')

        def priv_mut(records):
            for rec in records:
                kind, rid, val = rec
                if kind == "text" and rid == "27":
                    rec[2] = PRIVACY_EN_HTML
                elif kind == "line" and rid == "f":
                    rec[2] = (
                        val.replace("Gizlilik Politikası ve Kullanım Şartları", "Privacy Policy & Terms of Use")
                        .replace("Gizlilik Politikası & KVKK", "Privacy Policy & Terms of Use")
                        .replace("Gizlilik Politikası \\u0026 KVKK", "Privacy Policy & Terms of Use")
                    )
                elif kind == "line" and "LargeCta_largeCta__ylf5C" in val:
                    s = val.replace("Yeni bir dijital büyüme projeniz mi var?", "Have a new digital growth project?")
                    s = s.replace('"Hemen "', '"Let\'s get "')
                    s = s.replace('"children":"başlayalım"', '"children":"started"')
                    s = s.replace('"/iletisim/"', '"/en/contact-us/"')
                    rec[2] = s
            return True

        combined = ssr + rewrite_flight_in_html(tail, priv_mut)
        combined = apply_en_chrome_and_seo(
            combined,
            "/en/privacy-policy-and-terms-of-use/",
            en_title,
            en_desc,
            is_dist=(base_name == "dist"),
        )
        write_en_output(base_name, "privacy-policy-and-terms-of-use", combined)
    print("[EN] Built /en/privacy-policy-and-terms-of-use/index.html (public + dist)")


# ==============================================================================
# STEP C: HREFLANG + UNIFIED POST-HYDRATION UI ENHANCER (SWITCHER, ROUTER, CONSENT)
# ==============================================================================
ROASIST_UI_CSS = """<style data-roasist-ui-css>
.roasist-lang-switch{
  display:inline-flex;align-items:center;gap:2px;
  padding:4px 6px;border-radius:999px;
  border:1px solid rgba(15,23,42,0.14);
  background:rgba(255,255,255,0.82);
  backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);
  font-size:12px;line-height:1;font-weight:600;letter-spacing:0.02em;
  font-variant-numeric:tabular-nums;
  margin-right:10px;pointer-events:all;z-index:40;
  transition:border-color 160ms cubic-bezier(0.22,1,0.36,1),background-color 160ms cubic-bezier(0.22,1,0.36,1);
}
body.dark .roasist-lang-switch{
  border-color:rgba(255,255,255,0.22);
  background:rgba(15,23,42,0.68);
}
.roasist-lang-switch a{
  display:inline-flex;align-items:center;justify-content:center;
  padding:5px 8px;border-radius:999px;text-decoration:none!important;
  color:#475569;transition:color 160ms cubic-bezier(0.22,1,0.36,1),background-color 160ms cubic-bezier(0.22,1,0.36,1);
}
body.dark .roasist-lang-switch a{color:#cbd5e1;}
.roasist-lang-switch a.is-active{
  background:#0f172a;color:#ffffff!important;pointer-events:none;
}
body.dark .roasist-lang-switch a.is-active{
  background:#ffffff;color:#0f172a!important;
}
.roasist-lang-switch a:not(.is-active):hover{
  color:#0f172a;background:rgba(15,23,42,0.06);
}
body.dark .roasist-lang-switch a:not(.is-active):hover{
  color:#ffffff;background:rgba(255,255,255,0.12);
}
@media (max-width:768px){
  .Header_header__KwdYD .roasist-lang-switch{margin-right:6px;padding:3px 4px;font-size:11px;}
  .Header_header__KwdYD .roasist-lang-switch a{padding:4px 6px;}
}
.roasist-cookie-bar{
  position:fixed;left:24px;bottom:24px;z-index:9999;
  max-width:420px;width:calc(100vw - 48px);
  background:#ffffff;color:#0f172a;
  border:1px solid rgba(15,23,42,0.10);
  border-radius:16px;padding:20px 24px;
  box-shadow:0 16px 40px rgba(15,23,42,0.12);
  display:flex;flex-direction:column;gap:14px;
  font-size:13.5px;line-height:1.55;
  opacity:0;transform:translateY(10px);
  transition:opacity 180ms cubic-bezier(0.22,1,0.36,1),transform 180ms cubic-bezier(0.22,1,0.36,1);
}
.roasist-cookie-bar.is-visible{opacity:1;transform:translateY(0);}
.roasist-cookie-bar p{margin:0;color:#475569;font-size:13px;line-height:1.55;}
.roasist-cookie-bar p a{color:#0f172a;text-decoration:underline;text-underline-offset:3px;}
.roasist-cookie-actions{display:flex;align-items:center;justify-content:flex-end;gap:10px;}
.roasist-cookie-btn{
  appearance:none;border-radius:999px;padding:8px 16px;
  font-size:12.5px;font-weight:600;line-height:1;cursor:pointer;
  min-width:88px;height:34px;display:inline-flex;align-items:center;justify-content:center;
  transition:background-color 160ms cubic-bezier(0.22,1,0.36,1),color 160ms cubic-bezier(0.22,1,0.36,1),border-color 160ms cubic-bezier(0.22,1,0.36,1);
}
.roasist-cookie-btn--ghost{
  background:transparent;color:#64748b;border:1px solid rgba(15,23,42,0.12);
}
.roasist-cookie-btn--ghost:hover{color:#0f172a;border-color:rgba(15,23,42,0.28);}
.roasist-cookie-btn--primary{
  background:#0f172a;color:#ffffff;border:1px solid #0f172a;
}
.roasist-cookie-btn--primary:hover{background:#1e293b;}
@media (max-width:640px){
  .roasist-cookie-bar{left:16px;bottom:16px;width:calc(100vw - 32px);padding:18px 20px;}
}
</style>"""

ROASIST_UI_SCRIPT_TEMPLATE = """<script data-roasist-ui data-lang="__LANG__" data-tr-route="__TR_ROUTE__" data-en-route="__EN_ROUTE__">
(function(){
  var scriptEl = document.currentScript;
  var pageLang = (scriptEl && scriptEl.getAttribute('data-lang')) || (document.documentElement.lang === 'en' ? 'en' : 'tr');
  var trRoute = (scriptEl && scriptEl.getAttribute('data-tr-route')) || '/';
  var enRoute = (scriptEl && scriptEl.getAttribute('data-en-route')) || '/en/';

  function getBase() {
    return window.__ROASIST_BASE__ || (window.location.pathname.indexOf('/roasist-web') === 0 ? '/roasist-web' : '');
  }

  function withBase(path) {
    var b = getBase();
    if (!path || !path.startsWith('/') || path.startsWith('//')) return path;
    if (b && path !== b && path.indexOf(b + '/') !== 0) {
      return b + path;
    }
    return path;
  }

  var SERVICE_MAP_TR = {
    'performans-pazarlamasi': '/hizmetler/performans-pazarlamasi/',
    'brand-strategy-and-identity': '/hizmetler/performans-pazarlamasi/',
    'google-reklamlari': '/hizmetler/performans-pazarlamasi/google-reklamlari/',
    'brand-strategy': '/hizmetler/performans-pazarlamasi/google-reklamlari/',
    'instagram-reklamlari': '/hizmetler/performans-pazarlamasi/instagram-reklamlari/',
    'brand-identity-design': '/hizmetler/performans-pazarlamasi/instagram-reklamlari/',
    'tiktok-reklamlari': '/hizmetler/performans-pazarlamasi/tiktok-reklamlari/',
    'tone-of-voice': '/hizmetler/performans-pazarlamasi/tiktok-reklamlari/',
    'yandex-reklamlari': '/hizmetler/performans-pazarlamasi/yandex-reklamlari/',
    'bing-reklamlari': '/hizmetler/performans-pazarlamasi/bing-reklamlari/',
    'linkedin-reklamlari': '/hizmetler/performans-pazarlamasi/linkedin-reklamlari/',
    'web-tasarim': '/hizmetler/web-tasarim/',
    'web-design-development': '/hizmetler/web-tasarim/',
    'creative-web-design': '/hizmetler/web-tasarim/',
    'web-development': '/hizmetler/web-tasarim/',
    'wordpress-cms': '/hizmetler/web-tasarim/',
    'grafik-tasarim': '/hizmetler/grafik-tasarim/',
    'graphic-design': '/hizmetler/grafik-tasarim/',
    'seo': '/hizmetler/seo/',
    'seo-geo': '/hizmetler/seo/',
    'sitecare': '/hizmetler/seo/',
    'copywriting': '/hizmetler/360-derece-dijital-pazarlama-yonetimi/',
    'growth-marketing': '/hizmetler/seo/',
    '360-derece-dijital-pazarlama-yonetimi': '/hizmetler/360-derece-dijital-pazarlama-yonetimi/'
  };

  var SERVICE_MAP_EN = {
    'performance-marketing': '/en/performance-marketing/',
    'google-ads': '/en/google-ads/',
    'instagram-ads': '/en/instagram-ads/',
    'facebook-ads': '/en/facebook-ads/',
    'tiktok-ads': '/en/tiktok-ads/',
    'linkedin-ads': '/en/linkedin-ads/',
    'yandex-ads': '/en/yandex-ads/',
    'bing-ads': '/en/bing-ads/',
    'seo': '/en/seo/',
    'graphic-design': '/en/graphic-design/',
    'web-design': '/en/web-design/',
    '360-digital-marketing-management': '/en/360-digital-marketing-management/'
  };

  function resolveRoasistHref(rawHref) {
    if (!rawHref) return rawHref;
    if (rawHref.startsWith('#') || rawHref.startsWith('mailto:') || rawHref.startsWith('tel:') || rawHref.startsWith('javascript:')) return rawHref;
    if (/^https?:\\/\\//i.test(rawHref) && !/^https?:\\/\\/(?:www\\.)?kota\\.co\\.uk/i.test(rawHref)) return rawHref;

    var h = rawHref.replace(/^https?:\\/\\/(?:www\\.)?kota\\.co\\.uk/i, '');
    var b = getBase();
    if (b && (h === b || h.indexOf(b + '/') === 0)) {
      h = h.slice(b.length) || '/';
    }

    if (h.indexOf('service/') === 0) h = '/' + h;
    if (h.indexOf('/service/') === 0) {
      var s = h.slice('/service/'.length).replace(/\\/$/, '');
      if (pageLang === 'en') {
        h = SERVICE_MAP_EN[s] || ('/en/' + s + '/');
      } else {
        h = SERVICE_MAP_TR[s] || ('/hizmetler/' + s + '/');
      }
    } else if (pageLang === 'en') {
      if (h === '/iletisim' || h === '/iletisim/' || h === '/start-your-project' || h === '/start-your-project/' || h === '/contact' || h === '/contact/') {
        h = '/en/contact-us/';
      } else if (h === '/referanslar' || h === '/referanslar/' || h === '/work' || h === '/work/' || h.indexOf('/work/') === 0) {
        h = '/en/references/';
      } else if (h === '/hakkimizda' || h === '/hakkimizda/' || h === '/agency' || h === '/agency/') {
        h = '/en/who-we-are/';
      } else if (h === '/blog') {
        h = '/en/blog/';
      }
    } else {
      if (h === '/iletisim' || h === '/start-your-project' || h === '/start-your-project/') h = '/iletisim/';
      else if (h === '/referanslar') h = '/referanslar/';
      else if (h === '/hakkimizda') h = '/hakkimizda/';
      else if (h === '/hizmetler') h = '/hizmetler/';
      else if (h === '/blog') h = '/blog/';
      else if (h.indexOf('/hizmetler/') === 0 && !h.endsWith('/')) h = h + '/';
    }

    if (h.startsWith('/') && !h.startsWith('//')) {
      return withBase(h);
    }
    return h;
  }

  document.addEventListener('click', function(event) {
    var anchor = event.target && event.target.closest ? event.target.closest('a[href]') : null;
    if (!anchor) return;
    if (anchor.closest('.roasist-lang-switch')) return;
    var raw = anchor.getAttribute('href');
    if (!raw || raw.startsWith('#') || raw.startsWith('mailto:') || raw.startsWith('tel:') || raw.startsWith('javascript:')) return;
    if (/^https?:\\/\\//i.test(raw) && !/^https?:\\/\\/(?:www\\.)?kota\\.co\\.uk/i.test(raw)) return;
    if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey || anchor.target === '_blank') return;

    var dest = resolveRoasistHref(raw);
    if (dest && dest.startsWith('/')) {
      event.preventDefault();
      event.stopImmediatePropagation();
      window.location.href = dest;
    }
  }, true);

  function applyPostHydrationEnhancements() {
    var header = document.querySelector('header[class*="Header_header"]');
    if (header) {
      var logo = header.querySelector('a[class*="Header_logo"]');
      if (logo) {
        var wantLogoHref = withBase(pageLang === 'en' ? '/en/' : '/');
        if (logo.getAttribute('href') !== wantLogoHref) logo.setAttribute('href', wantLogoHref);
      }
      if (!header.querySelector('.roasist-lang-switch')) {
        var sw = document.createElement('div');
        sw.className = 'roasist-lang-switch';
        sw.setAttribute('role', 'navigation');
        sw.setAttribute('aria-label', pageLang === 'en' ? 'Language selector' : 'Dil seçimi');

        var aTr = document.createElement('a');
        aTr.href = withBase(trRoute);
        aTr.textContent = 'TR';
        aTr.setAttribute('hreflang', 'tr');
        if (pageLang === 'tr') aTr.className = 'is-active';

        var aEn = document.createElement('a');
        aEn.href = withBase(enRoute);
        aEn.textContent = 'EN';
        aEn.setAttribute('hreflang', 'en');
        if (pageLang === 'en') aEn.className = 'is-active';

        sw.appendChild(aTr);
        sw.appendChild(aEn);

        var rightWrap = header.querySelector('[class*="Header_right"]') || header.querySelector('a[class*="Header_button"]');
        if (rightWrap && rightWrap.className && String(rightWrap.className).indexOf('Header_right') !== -1) {
          rightWrap.insertBefore(sw, rightWrap.firstChild);
        } else if (rightWrap && rightWrap.parentNode) {
          rightWrap.parentNode.insertBefore(sw, rightWrap);
        } else {
          header.appendChild(sw);
        }
      }
    }

    document.querySelectorAll('a[href^="service/"], a[href^="/service/"]').forEach(function(a) {
      var clean = resolveRoasistHref(a.getAttribute('href'));
      if (clean && a.getAttribute('href') !== clean) a.setAttribute('href', clean);
    });

    if (pageLang === 'en') {
      document.querySelectorAll('[class*="PrimaryNavigation_buttonContainer"] a, [class*="FloatingStartButton_linkContainer"] a').forEach(function(a) {
        var contactHref = withBase('/en/contact-us/');
        if (a.getAttribute('href') !== contactHref) a.setAttribute('href', contactHref);
        a.querySelectorAll('span').forEach(function(sp) {
          if (sp.children.length === 0 && (sp.textContent === 'Projeye Başla' || sp.textContent === 'Projeye Başlayın')) {
            sp.textContent = 'Start a Project';
          }
        });
      });

      document.querySelectorAll('[class*="ServicesPanel_panel"] [class*="Button_textInner"]').forEach(function(sp) {
        if (sp.textContent === 'Detaylı İncele') sp.textContent = 'Explore Service';
      });

      document.querySelectorAll('button, span').forEach(function(el) {
        if (el.children.length === 0) {
          if (el.textContent === 'Filtrele') el.textContent = 'Filter';
          else if (el.textContent === 'Tüm Kategoriler' || el.textContent === 'Tümü') el.textContent = 'All';
        }
      });

      var formSec = document.querySelector('section[class*="Form_contactForm"]');
      if (formSec && !formSec.dataset.roasistEnDone) {
        formSec.dataset.roasistEnDone = '1';
        var formMap = {
          'İlgilendiğiniz Hizmet :': 'Services of Interest :',
          'Web Tasarım & Geliştirme': 'Web Design & Development',
          'Branding': 'Brand & Creative Strategy',
          'SEO & İçerik Stratejisi': 'Enterprise SEO & AEO',
          'E-Ticaret': 'Performance Marketing & ROAS',
          '360° Dijital Pazarlama': '360° Digital Marketing',
          'Kreatif & Grafik Tasarım': 'Graphic & Ad Creative',
          'Dosya Ekle': 'Attach Brief',
          'Roasist dijital büyüme bültenini almak istiyorum': 'Subscribe to Roasist digital growth insights',
          'Verilerimin Gizlilik Politikası ve KVKK kapsamında güvenle işlenmesini kabul ediyorum.': 'I agree to the processing of my data under the Privacy Policy.',
          'Gönder': 'Send Inquiry'
        };
        var walker = document.createTreeWalker(formSec, NodeFilter.SHOW_TEXT, null);
        var tNode;
        while ((tNode = walker.nextNode())) {
          var trimmed = tNode.nodeValue.trim();
          if (formMap[trimmed]) {
            tNode.nodeValue = tNode.nodeValue.replace(trimmed, formMap[trimmed]);
          } else if (trimmed.indexOf('Bütçe planlaması ve hizmet kapsamlarımız') !== -1) {
            tNode.nodeValue = 'Explore our tailored digital growth scopes ';
          } else if (trimmed === 'buradan ulaşabilirsiniz') {
            tNode.nodeValue = 'on our services page';
            if (tNode.parentElement && tNode.parentElement.tagName === 'A') {
              tNode.parentElement.setAttribute('href', withBase('/en/services/'));
            }
          }
        }
        formSec.querySelectorAll('input[placeholder]').forEach(function(inp) {
          if (inp.placeholder.indexOf('Budget') !== -1) inp.placeholder = 'Monthly Budget ($ / €)';
        });
      }
    } else {
      var trFormSec = document.querySelector('section[class*="Form_contactForm"]');
      if (trFormSec && !trFormSec.dataset.roasistTrDone) {
        trFormSec.dataset.roasistTrDone = '1';
        var phMapTr = {
          'First name*': 'Adınız*',
          'Last name*': 'Soyadınız*',
          'Email*': 'Kurumsal E-posta*',
          'Budget (£)': 'Aylık Reklam / Proje Bütçesi',
          'Message': 'Projenizden ve büyüme hedeflerinizden bahsedin...'
        };
        trFormSec.querySelectorAll('input[placeholder], textarea[placeholder]').forEach(function(inp) {
          if (phMapTr[inp.placeholder]) inp.placeholder = phMapTr[inp.placeholder];
        });
      }
    }
  }

  function mountCookieBanner() {
    var saved = null;
    try { saved = localStorage.getItem('roasist_cookie_consent'); } catch (e) {}
    if (saved || document.querySelector('.roasist-cookie-bar')) return;

    var bar = document.createElement('aside');
    bar.className = 'roasist-cookie-bar';
    bar.setAttribute('role', 'dialog');
    bar.setAttribute('aria-label', pageLang === 'en' ? 'Cookie preferences' : 'Çerez tercihleri');

    var privHref = withBase(pageLang === 'en' ? '/en/privacy-policy-and-terms-of-use/' : '/gizlilik-politikasi-ve-kullanim-sartlari/');
    var copyHtml = pageLang === 'en'
      ? 'We use cookies to measure performance and improve your experience in accordance with our <a href="' + privHref + '">Privacy Policy</a>.'
      : 'Deneyiminizi iyileştirmek ve performans analizi yapmak için <a href="' + privHref + '">Gizlilik ve Çerez Politikamız</a> kapsamında çerezler kullanıyoruz.';

    bar.innerHTML = '<p>' + copyHtml + '</p>' +
      '<div class="roasist-cookie-actions">' +
      '<button type="button" class="roasist-cookie-btn roasist-cookie-btn--ghost" data-consent="denied">' + (pageLang === 'en' ? 'Decline' : 'Reddet') + '</button>' +
      '<button type="button" class="roasist-cookie-btn roasist-cookie-btn--primary" data-consent="granted">' + (pageLang === 'en' ? 'Accept' : 'Kabul Et') + '</button>' +
      '</div>';

    function closeWith(choice) {
      try { localStorage.setItem('roasist_cookie_consent', choice); } catch (e) {}
      if (typeof window.gtag === 'function') {
        window.gtag('consent', 'update', {
          analytics_storage: choice,
          ad_storage: choice,
          ad_user_data: choice,
          ad_personalization: choice
        });
      }
      bar.classList.remove('is-visible');
      setTimeout(function() { if (bar.parentNode) bar.parentNode.removeChild(bar); }, 200);
      document.removeEventListener('keydown', onEsc);
    }

    function onEsc(ev) {
      if (ev.key === 'Escape') closeWith('denied');
    }

    bar.querySelectorAll('button[data-consent]').forEach(function(btn) {
      btn.addEventListener('click', function() {
        closeWith(btn.getAttribute('data-consent'));
      });
    });
    document.addEventListener('keydown', onEsc);
    document.body.appendChild(bar);
    requestAnimationFrame(function() { bar.classList.add('is-visible'); });
  }

  function scheduleEnhancements() {
    setTimeout(applyPostHydrationEnhancements, 450);
    setTimeout(applyPostHydrationEnhancements, 1200);
    setTimeout(mountCookieBanner, 1300);
    var timer = null;
    new MutationObserver(function() {
      if (timer) return;
      timer = setTimeout(function() {
        timer = null;
        applyPostHydrationEnhancements();
      }, 250);
    }).observe(document.documentElement, { childList: true, subtree: true });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', scheduleEnhancements);
  } else {
    scheduleEnhancements();
  }
})();
</script>"""


def resolve_language_pair_for_route(route: str) -> tuple[str, str, str]:
    """Returns (lang, tr_route, en_route) for any TR or EN route."""
    if route == "/en" or route.startswith("/en/"):
        en_r = route if route.endswith("/") else route + "/"
        tr_r = EN_TO_TR_ROUTES.get(en_r, "/")
        return ("en", tr_r, en_r)
    else:
        tr_r = route if route.endswith("/") else route + "/"
        if tr_r in TR_TO_EN_ROUTES:
            en_r = TR_TO_EN_ROUTES[tr_r]
        elif tr_r.startswith("/blog/"):
            en_r = "/en/blog/"
        elif tr_r.startswith("/hizmetler/"):
            en_r = "/en/services/"
        else:
            en_r = "/en/"
        return ("tr", tr_r, en_r)


def inject_hreflang_and_ui_across_all_pages():
    count = 0
    for base_name in ("public", "dist"):
        base_dir = os.path.join(ROOT, base_name)
        for fp in sorted(glob.glob(os.path.join(base_dir, "**", "*.html"), recursive=True)):
            if os.path.basename(fp) == "404.html":
                continue
            html = open(fp, "r", encoding="utf-8").read()
            if "self.__next_f.push" not in html:
                continue

            route = get_route_for_file(fp, base_dir)
            lang, tr_route, en_route = resolve_language_pair_for_route(route)
            tr_abs = f"{SITE_ORIGIN}{tr_route}"
            en_abs = f"{SITE_ORIGIN}{en_route}"

            html = re.sub(r'<link rel="alternate" hreflang="[^"]+" href="[^"]+"\s*/>', "", html)
            html = re.sub(r"<style data-roasist-ui-css>.*?</style>", "", html, flags=re.S)
            html = re.sub(r"<script data-roasist-ui[^>]*>.*?</script>", "", html, flags=re.S)

            hreflang_tags = (
                f'<link rel="alternate" hreflang="tr" href="{tr_abs}"/>'
                f'<link rel="alternate" hreflang="en" href="{en_abs}"/>'
                f'<link rel="alternate" hreflang="x-default" href="{tr_abs}"/>'
            )
            ui_script = (
                ROASIST_UI_SCRIPT_TEMPLATE.replace("__LANG__", lang)
                .replace("__TR_ROUTE__", tr_route)
                .replace("__EN_ROUTE__", en_route)
            )

            html = html.replace("</head>", f"{hreflang_tags}{ROASIST_UI_CSS}</head>", 1)
            if "</body>" in html:
                html = html.replace("</body>", f"{ui_script}</body>", 1)
            else:
                html = html + ui_script

            with open(fp, "w", encoding="utf-8") as f:
                f.write(html)
            count += 1
    print(f"[HREFLANG + UI] Injected hreflang, TR|EN switcher, router & consent bar into {count} HTML files")


# ==============================================================================
# STEP D: GENERATE sitemap.xml AND robots.txt IN public/ AND dist/
# ==============================================================================
def generate_sitemap_and_robots():
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    canonical_tr_routes = [
        "/",
        "/hakkimizda/",
        "/hizmetler/",
        "/hizmetler/performans-pazarlamasi/",
        "/hizmetler/performans-pazarlamasi/google-reklamlari/",
        "/hizmetler/performans-pazarlamasi/instagram-reklamlari/",
        "/hizmetler/performans-pazarlamasi/facebook-reklamlari/",
        "/hizmetler/performans-pazarlamasi/tiktok-reklamlari/",
        "/hizmetler/performans-pazarlamasi/linkedin-reklamlari/",
        "/hizmetler/performans-pazarlamasi/yandex-reklamlari/",
        "/hizmetler/performans-pazarlamasi/bing-reklamlari/",
        "/hizmetler/seo/",
        "/hizmetler/grafik-tasarim/",
        "/hizmetler/web-tasarim/",
        "/hizmetler/360-derece-dijital-pazarlama-yonetimi/",
        "/referanslar/",
        "/blog/",
        "/blog/Performans-Pazarlamasi-Nedir/",
        "/blog/performans-pazarlamasinda-roas-optimizasyonu/",
        "/blog/kurumsal-seo-ve-yapay-zeka-aramalari-aeo-rehberi/",
        "/blog/360-dijital-pazarlama-kanallar-arasi-sinerji/",
        "/blog/Veriye-Dayali-Dijital-Pazarlama-Stratejisi-Nedir/",
        "/blog/Reklam-Harcamalarinin-Geri-Donusu-ROAS-Nasil-Hesaplanir/",
        "/iletisim/",
        "/gizlilik-politikasi-ve-kullanim-sartlari/",
    ]
    canonical_en_routes = list(EN_TO_TR_ROUTES.keys())

    url_entries = []
    for r in canonical_tr_routes + canonical_en_routes:
        _, tr_r, en_r = resolve_language_pair_for_route(r)
        loc = f"{SITE_ORIGIN}{r}"
        tr_loc = f"{SITE_ORIGIN}{tr_r}"
        en_loc = f"{SITE_ORIGIN}{en_r}"
        prio = "1.0" if r in ("/", "/en/") else ("0.9" if "/hizmetler/" in r or (r.startswith("/en/") and "/blog/" not in r) else "0.8")
        url_entries.append(
            "  <url>\n"
            f"    <loc>{loc}</loc>\n"
            f'    <xhtml:link rel="alternate" hreflang="tr" href="{tr_loc}"/>\n'
            f'    <xhtml:link rel="alternate" hreflang="en" href="{en_loc}"/>\n'
            f'    <xhtml:link rel="alternate" hreflang="x-default" href="{tr_loc}"/>\n'
            f"    <lastmod>{now_iso}</lastmod>\n"
            f"    <priority>{prio}</priority>\n"
            "  </url>"
        )

    sitemap_xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + "\n".join(url_entries)
        + "\n</urlset>\n"
    )

    robots_txt = (
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /_next/\n\n"
        f"Sitemap: {SITE_ORIGIN}/sitemap.xml\n"
    )

    for base_name in ("public", "dist"):
        with open(os.path.join(ROOT, base_name, "sitemap.xml"), "w", encoding="utf-8") as f:
            f.write(sitemap_xml)
        with open(os.path.join(ROOT, base_name, "robots.txt"), "w", encoding="utf-8") as f:
            f.write(robots_txt)
        for old_sm in ("sitemap-index.xml", "sitemap-0.xml"):
            old_p = os.path.join(ROOT, base_name, old_sm)
            if os.path.exists(old_p):
                os.remove(old_p)

    print(f"[SITEMAP + ROBOTS] Generated sitemap.xml ({len(url_entries)} URLs) & robots.txt in public/ and dist/")


def main():
    fix_tr_remnants()
    build_en_homepage()
    build_en_about()
    build_en_services()
    build_en_references()
    build_en_blog()
    build_en_contact()
    build_en_privacy()
    inject_hreflang_and_ui_across_all_pages()
    generate_sitemap_and_robots()
    print("[FAZ 4 COMPLETE] All 22 English pages, TR|EN switcher, hreflang, consent bar & sitemap built!")


if __name__ == "__main__":
    main()
