#!/usr/bin/env python3
"""
Roasist Web — Comprehensive UI/UX, Design Engineering, Navigation & Route Overhaul:
  1. Renames `/hizmetler/yapay-zeka-seo/` -> `/hizmetler/aeo-geo/` and
     `/en/ai-search-aeo-geo/` -> `/en/aeo-geo/` across directories, sitemap, and all links.
  2. Upgrades PrimaryNavigation (SSR + Flight AST) to include all 7 core service pillars (TR & EN).
  3. Unifies CTA labels (`Teklif Al` / `Get a Proposal`, `Projeye Başla` / `Start a Project`)
     and fixes bidirectional `hreflang` + `data-roasist-ui` route pairs across all pages.
  4. Injects Design Engineering CSS (`roasist-ux-overhaul-css`) & Progressive UX/A11y Enhancer
     (`roasist-ux-overhaul-js`):
       - Fixes mobile Intro heading/paragraph overlap & Contact Hero/Form collision
       - Replaces clipped `1px` eyebrow hair with crisp `#7602FF` optical dot + clickable Breadcrumbs
       - Enables above-the-fold mobile `Teklif Al` CTA & moves Cookie Bar away from partner badges
       - Adds Quick Contact Strip (`+90 540 507 53 50`, WhatsApp, Email, SLA), `Telefon*` input,
         multi-line `<textarea>`, `autocomplete`, unhides 7th AEO/GEO pill, hides dead file input
       - Expands `Diğer Hizmetlerimiz` to 7 pillars, adds 6-channel Paid Media pill bar, and adds
         `TR | EN` switcher inside the opened Navigation Menu
       - Ensures 1 semantic `<h1>` per page, `aria-label` on icon controls, Skip-to-Content link,
         `:focus-visible` outlines, `ESC` menu close, `>=44px` touch targets, and `tabular-nums`.
"""
import glob
import json
import os
import re
import shutil
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
PUBLIC_DIR = os.path.join(REPO_ROOT, "public")
sys.path.insert(0, SCRIPT_DIR)

from prelaunch_step3_forms_links_en import apply_replacements_flight_safe
from update_about_page import parse_flight_stream, serialize_flight_stream
from update_tiktok_yandex_pages import extract_flight_chunks

SITE_ORIGIN = "https://www.roasist.com"

TR_TO_EN_MAP = {
    "/": "/en/",
    "/hakkimizda/": "/en/who-we-are/",
    "/hizmetler/": "/en/services/",
    "/hizmetler/performans-pazarlamasi/": "/en/performance-marketing/",
    "/hizmetler/performans-pazarlamasi/google-reklamlari/": "/en/google-ads/",
    "/hizmetler/google-reklamlari/": "/en/google-ads/",
    "/hizmetler/performans-pazarlamasi/instagram-reklamlari/": "/en/instagram-ads/",
    "/hizmetler/instagram-reklamlari/": "/en/instagram-ads/",
    "/hizmetler/performans-pazarlamasi/facebook-reklamlari/": "/en/facebook-ads/",
    "/hizmetler/facebook-reklamlari/": "/en/facebook-ads/",
    "/hizmetler/performans-pazarlamasi/tiktok-reklamlari/": "/en/tiktok-ads/",
    "/hizmetler/tiktok-reklamlari/": "/en/tiktok-ads/",
    "/hizmetler/performans-pazarlamasi/yandex-reklamlari/": "/en/yandex-ads/",
    "/hizmetler/yandex-reklamlari/": "/en/yandex-ads/",
    "/hizmetler/performans-pazarlamasi/bing-reklamlari/": "/en/bing-ads/",
    "/hizmetler/bing-reklamlari/": "/en/bing-ads/",
    "/hizmetler/performans-pazarlamasi/linkedin-reklamlari/": "/en/linkedin-ads/",
    "/hizmetler/linkedin-reklamlari/": "/en/linkedin-ads/",
    "/hizmetler/seo/": "/en/seo/",
    "/hizmetler/aeo-geo/": "/en/aeo-geo/",
    "/hizmetler/web-tasarim/": "/en/web-design/",
    "/hizmetler/donusum-optimizasyonu/": "/en/conversion-optimization/",
    "/hizmetler/grafik-tasarim/": "/en/graphic-design/",
    "/hizmetler/360-derece-dijital-pazarlama-yonetimi/": "/en/360-digital-marketing-management/",
    "/referanslar/": "/en/references/",
    "/blog/": "/en/blog/",
    "/iletisim/": "/en/contact-us/",
    "/start-your-project/": "/en/start-your-project/",
    "/gizlilik-politikasi-ve-kullanim-sartlari/": "/en/privacy-policy-and-terms-of-use/",
}

EN_TO_TR_MAP = {
    "/en/": "/",
    "/en/who-we-are/": "/hakkimizda/",
    "/en/services/": "/hizmetler/",
    "/en/performance-marketing/": "/hizmetler/performans-pazarlamasi/",
    "/en/google-ads/": "/hizmetler/performans-pazarlamasi/google-reklamlari/",
    "/en/instagram-ads/": "/hizmetler/performans-pazarlamasi/instagram-reklamlari/",
    "/en/facebook-ads/": "/hizmetler/performans-pazarlamasi/facebook-reklamlari/",
    "/en/tiktok-ads/": "/hizmetler/performans-pazarlamasi/tiktok-reklamlari/",
    "/en/yandex-ads/": "/hizmetler/performans-pazarlamasi/yandex-reklamlari/",
    "/en/bing-ads/": "/hizmetler/performans-pazarlamasi/bing-reklamlari/",
    "/en/linkedin-ads/": "/hizmetler/performans-pazarlamasi/linkedin-reklamlari/",
    "/en/seo/": "/hizmetler/seo/",
    "/en/aeo-geo/": "/hizmetler/aeo-geo/",
    "/en/web-design/": "/hizmetler/web-tasarim/",
    "/en/conversion-optimization/": "/hizmetler/donusum-optimizasyonu/",
    "/en/graphic-design/": "/hizmetler/grafik-tasarim/",
    "/en/360-digital-marketing-management/": "/hizmetler/360-derece-dijital-pazarlama-yonetimi/",
    "/en/references/": "/referanslar/",
    "/en/blog/": "/blog/",
    "/en/contact-us/": "/iletisim/",
    "/en/start-your-project/": "/start-your-project/",
    "/en/privacy-policy-and-terms-of-use/": "/gizlilik-politikasi-ve-kullanim-sartlari/",
}

NAV_NODES_TR = [
    {"databaseId": 936, "label": "Referanslar", "uri": "/referanslar/", "childItems": {"nodes": []}},
    {"databaseId": 946, "label": "Hakkımızda", "uri": "/hakkimizda/", "childItems": {"nodes": []}},
    {
        "databaseId": 937,
        "label": "Hizmetler",
        "uri": "#",
        "childItems": {
            "nodes": [
                {"databaseId": 942, "label": "Performans Pazarlaması", "uri": "/hizmetler/performans-pazarlamasi/"},
                {"databaseId": 944, "label": "Teknik & Kurumsal SEO", "uri": "/hizmetler/seo/"},
                {"databaseId": 947, "label": "Yapay Zeka Aramaları (AEO & GEO)", "uri": "/hizmetler/aeo-geo/"},
                {"databaseId": 943, "label": "Web Tasarım & Yazılım", "uri": "/hizmetler/web-tasarim/"},
                {"databaseId": 948, "label": "Dönüşüm Optimizasyonu (CRO)", "uri": "/hizmetler/donusum-optimizasyonu/"},
                {"databaseId": 945, "label": "Grafik & Kreatif Tasarım", "uri": "/hizmetler/grafik-tasarim/"},
                {"databaseId": 941, "label": "360° Dijital Pazarlama Yönetimi", "uri": "/hizmetler/360-derece-dijital-pazarlama-yonetimi/"},
            ]
        },
    },
    {"databaseId": 938, "label": "Blog", "uri": "/blog/", "childItems": {"nodes": []}},
    {"databaseId": 940, "label": "İletişim", "uri": "/iletisim/", "childItems": {"nodes": []}},
]

NAV_NODES_EN = [
    {"databaseId": 936, "label": "Case Studies", "uri": "/en/references/", "childItems": {"nodes": []}},
    {"databaseId": 946, "label": "Who We Are", "uri": "/en/who-we-are/", "childItems": {"nodes": []}},
    {
        "databaseId": 937,
        "label": "Services",
        "uri": "#",
        "childItems": {
            "nodes": [
                {"databaseId": 942, "label": "Performance Marketing", "uri": "/en/performance-marketing/"},
                {"databaseId": 944, "label": "Technical & Enterprise SEO", "uri": "/en/seo/"},
                {"databaseId": 947, "label": "AI Search (AEO & GEO)", "uri": "/en/aeo-geo/"},
                {"databaseId": 943, "label": "Web Design & UI/UX", "uri": "/en/web-design/"},
                {"databaseId": 948, "label": "Conversion Optimization (CRO)", "uri": "/en/conversion-optimization/"},
                {"databaseId": 945, "label": "Graphic & Ad Creative", "uri": "/en/graphic-design/"},
                {"databaseId": 941, "label": "360° Digital Growth", "uri": "/en/360-digital-marketing-management/"},
            ]
        },
    },
    {"databaseId": 938, "label": "Blog", "uri": "/en/blog/", "childItems": {"nodes": []}},
    {"databaseId": 940, "label": "Contact", "uri": "/en/contact-us/", "childItems": {"nodes": []}},
]


def build_ssr_nav(is_en: bool) -> str:
    nodes = NAV_NODES_EN if is_en else NAV_NODES_TR
    cta_href = "/en/start-your-project/" if is_en else "/iletisim/"
    cta_label = "Start a Project" if is_en else "Projeye Başla"
    items_html = []
    for item in nodes:
        children = item["childItems"]["nodes"]
        if not children:
            items_html.append(f'<li><a href="{item["uri"]}">{item["label"]}</a></li>')
        else:
            sub_li = "".join(f'<li><a href="{c["uri"]}">{c["label"]}</a></li>' for c in children)
            items_html.append(
                f'<li><div class="PrimaryNavigation_parent__bfX37">{item["label"]}'
                '<figure class="PrimaryNavigation_toggleSign__XESvT "><span class="PrimaryNavigation_toggleInner__Lz3QB">'
                '<span class="PrimaryNavigation_toggleLine__QUlfd"></span><span class="PrimaryNavigation_toggleLine__QUlfd"></span>'
                f'</span></figure></div><ul class="PrimaryNavigation_submenu__ryGWu ">{sub_li}</ul></li>'
            )
    return (
        '<nav class="PrimaryNavigation_navigation__l8Jgb"><ul>'
        + "".join(items_html)
        + '</ul>'
        + '<div class="PrimaryNavigation_buttonContainer__iiKTy"><div class="Magnetic_magnetic__LncOy" data-fill="false">'
        + f'<div class="Button_button__JJiqJ" data-direction="forwards"><a class="Button_inner__fnyH6" href="{cta_href}">'
        + '<span class="Button_border__hirH2"></span><span class="Button_text__IZaCD">'
        + f'<span class="Button_textInner__JTTHe">{cta_label}</span>'
        + '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 17.1 15.17" class="Button_buttonArrow__0W9XI">'
        + '<path d="m17.1,7.58s-.01-.04-.01-.06c.01-.22-.06-.45-.24-.61L9.23.19c-.31-.27-.78-.24-1.06.07-.27.31-.24.78.07,1.06l6.26,5.52H.75c-.41,0-.75.34-.75.75s.34.75.75.75h13.74l-6.26,5.52c-.31.27-.34.75-.07,1.06.15.17.35.25.56.25.18,0,.35-.06.5-.19l7.62-6.72c.18-.16.25-.39.24-.61,0-.02.01-.04.01-.06Z" fill="currentColor"></path>'
        + '</svg></span></a></div></div></div></nav>'
    )


UX_STYLE_ID = "roasist-ux-overhaul-css"
UX_SCRIPT_ID = "roasist-ux-overhaul-js"

UX_CSS = f"""<style id="{UX_STYLE_ID}">
/* === ROASIST DESIGN ENGINEERING & UX OVERHAUL === */
:root {{
  --roasist-ease: cubic-bezier(0.22, 1, 0.36, 1);
}}

/* 1. Keyboard Accessibility: Skip Link & Crisp Focus Ring */
.roasist-skip-link {{
  position: fixed;
  top: -100px;
  left: 16px;
  z-index: 10000;
  padding: 0.7rem 1.2rem;
  border-radius: 999px;
  background: #0f172a;
  color: #ffffff !important;
  font-size: 0.875rem;
  font-weight: 600;
  text-decoration: none;
  transition: top 160ms var(--roasist-ease);
}}
.roasist-skip-link:focus {{
  top: 16px;
  outline: 2px solid #7602FF;
  outline-offset: 2px;
}}
a:focus-visible,
button:focus-visible,
input:focus-visible,
textarea:focus-visible,
select:focus-visible {{
  outline: 2px solid #7602FF !important;
  outline-offset: 3px !important;
}}

/* 2. Global Tabular Numbers & Optical Heading Tracking */
.StatisticsPanel_heading__d3H3j,
.StatisticsPanel_panel__d3H3j h3,
[class*="StatisticsPanel"] h3,
[class*="Timeline"] [class*="step"],
.roasist-quick-contact__val,
.Footer_cyberEssestials__2qh89,
input[type="tel"],
input[name="budget"] {{
  font-variant-numeric: tabular-nums !important;
}}

/* 3. Fix Mobile Intro Heading/Paragraph Overlap across all Service Pages */
@media (max-width: 849px) {{
  .Intro_intro__B7xXJ .container,
  .Intro_intro__L3nUM .container {{
    display: flex !important;
    flex-direction: column !important;
    align-items: flex-start !important;
    gap: 1.5rem !important;
  }}
  .Intro_intro__B7xXJ h2,
  .Intro_intro__L3nUM h2 {{
    font-size: clamp(2rem, 8.2vw, 2.75rem) !important;
    line-height: 1.16 !important;
    letter-spacing: -0.02em !important;
    margin: 0 0 0.35rem 0 !important;
    width: 100% !important;
  }}
  .Intro_intro__B7xXJ .LineByLine_headingOuter__JmusT .split-line,
  .Intro_intro__L3nUM .LineByLine_headingOuter__JmusT .split-line {{
    transform: none !important;
    opacity: 1 !important;
  }}
  .Intro_text__4DPtt,
  .Intro_text__yXuAA {{
    width: 100% !important;
    margin-top: 0 !important;
  }}
  .Intro_text__4DPtt.prose p,
  .Intro_text__yXuAA.prose p {{
    font-size: 1.05rem !important;
    line-height: 1.58 !important;
  }}
}}

/* 4. Fix Eyebrow Clipped Line -> Crisp #7602FF Brand Dot + Breadcrumbs */
.roasist-hero-page-label i,
.Hero_hero__18Xqo .roasist-hero-page-label i,
.Hero_hero___ImMv .roasist-hero-page-label i,
.Content_content__6vnSh .prose .roasist-hero-page-label i {{
  display: inline-block !important;
  width: 8px !important;
  height: 8px !important;
  border-radius: 999px !important;
  background-color: #7602FF !important;
  margin-right: 0.55em !important;
  align-self: center !important;
  transform: translateY(-0.04em) !important;
}}
.roasist-breadcrumb {{
  grid-column: 1 / -1 !important;
  width: 100% !important;
  display: flex !important;
  flex-direction: row !important;
  flex-wrap: wrap !important;
  align-items: center !important;
  gap: 0.45rem !important;
  margin: 0 0 0.75rem 0 !important;
  padding: 0 !important;
  list-style: none !important;
  font-size: 0.84rem !important;
  line-height: 1.4 !important;
  color: #64748b !important;
  pointer-events: auto !important;
  position: relative !important;
  z-index: 4 !important;
}}
.roasist-breadcrumb li {{
  display: inline-flex !important;
  align-items: center !important;
}}
.roasist-breadcrumb a {{
  color: #475569;
  text-decoration: none;
  transition: color 150ms var(--roasist-ease);
}}
.roasist-breadcrumb a:hover {{
  color: #7602FF;
}}
.roasist-breadcrumb__sep {{
  color: #94a3b8;
  user-select: none;
}}
.roasist-breadcrumb__current {{
  color: #0f172a;
  font-weight: 500;
}}

/* 5. Preserve Identical Hero Display Typography When Promoted to Semantic <h1> */
.Hero_hero__18Xqo .Hero_top__fPz2U h1.roasist-promoted-h1 {{
  position: static !important;
  top: auto !important;
  left: auto !important;
  transform: none !important;
  padding: 0 !important;
  font-family: var(--montreal), Inter, sans-serif !important;
  font-weight: 400 !important;
  line-height: 0.98 !important;
  font-size: var(--fs-100) !important;
  letter-spacing: -0.02em !important;
  text-transform: none !important;
  margin: 0 !important;
  grid-column: span 12 !important;
}}
.Hero_hero___ImMv .Hero_top__9AiY_ h1.roasist-promoted-h1 {{
  position: static !important;
  font-family: var(--montreal), Inter, sans-serif !important;
  font-weight: 400 !important;
  text-transform: none !important;
}}
.Hero_hero__18Xqo .Hero_top__fPz2U h1.roasist-promoted-h1 em,
.Hero_hero___ImMv .Hero_top__9AiY_ h1.roasist-promoted-h1 em {{
  font-style: normal !important;
}}

/* 6. Mobile Header Primary CTA Visibility & Brand Hover (Replace KOTA Neon Pink) */
.Header_header__KwdYD .Header_button__yG4_K {{
  transition: background-color 170ms var(--roasist-ease), color 170ms var(--roasist-ease), transform 170ms var(--roasist-ease) !important;
}}
.Header_header__KwdYD .Header_button__yG4_K:hover {{
  background-color: #7602FF !important;
  color: #ffffff !important;
}}
@media (max-width: 550px) {{
  .Header_header__KwdYD .Header_button__yG4_K {{
    display: inline-flex !important;
    font-size: 0.84rem !important;
    font-weight: 600 !important;
    padding: 0.65rem 1rem !important;
    min-height: 40px !important;
    margin-left: auto !important;
    margin-right: 3.55rem !important;
  }}
}}

/* 7. Cookie Bar Right-Aligned So Hero Partner Badges Stay 100% Uncovered */
.roasist-cookie-bar {{
  left: auto !important;
  right: 24px !important;
  bottom: 20px !important;
  max-width: 380px !important;
}}
@media (max-width: 640px) {{
  .roasist-cookie-bar {{
    left: 14px !important;
    right: 14px !important;
    bottom: 14px !important;
    width: auto !important;
    max-width: none !important;
    padding: 14px 16px !important;
  }}
}}

/* 8. Primary Navigation Submenu Height for 7 Services & Menu Language Switcher */
.PrimaryNavigation_submenuOpen__uJhU7 {{
  max-height: 440px !important;
}}
.roasist-menu-lang {{
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  margin-top: 1.25rem;
  padding: 0.3rem;
  border-radius: 999px;
  background: transparent;
  border: 1px solid rgba(15, 23, 42, 0.14);
}}
.roasist-menu-lang a {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 44px;
  min-height: 36px;
  padding: 0.35rem 0.85rem;
  border-radius: 999px;
  font-size: 0.85rem !important;
  font-weight: 600 !important;
  text-decoration: none !important;
  color: #475569 !important;
  transition: background 160ms var(--roasist-ease), color 160ms var(--roasist-ease);
}}
.roasist-menu-lang a.is-active {{
  background: #0f172a;
  color: #ffffff !important;
}}

/* 9. DiscoverMore 7-Pillar Bar & Paid Channels 6-Pill Bar */
@media (max-width: 768px) {{
  .DiscoverMore_discoverMore__hYPtP {{
    display: block !important;
    order: 4 !important;
    width: 100% !important;
    margin-top: 1.5rem !important;
    overflow-x: auto !important;
    -webkit-overflow-scrolling: touch;
  }}
  .DiscoverMore_linksInner__Vgx11 {{
    display: flex !important;
    flex-wrap: wrap !important;
    gap: 0.5rem !important;
  }}
}}
.roasist-channel-pills {{
  grid-column: 1 / -1;
  width: 100%;
  margin-top: 1.5rem;
  padding-top: 1.25rem;
  border-top: 1px solid rgba(15, 23, 42, 0.08);
  pointer-events: auto;
}}
.roasist-channel-pills__label {{
  font-size: 0.82rem;
  font-weight: 600;
  letter-spacing: 0.01em;
  color: #64748b;
  margin: 0 0 0.65rem 0;
}}
.roasist-channel-pills__list {{
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}}
.roasist-channel-pill {{
  display: inline-flex;
  align-items: center;
  min-height: 40px;
  padding: 0.45rem 1rem;
  border-radius: 999px;
  font-size: 0.88rem;
  font-weight: 500;
  color: #0f172a;
  background: transparent;
  border: 1px solid rgba(15, 23, 42, 0.22);
  text-decoration: none;
  transition: border-color 160ms var(--roasist-ease), background 160ms var(--roasist-ease), color 160ms var(--roasist-ease);
}}
.roasist-channel-pill:hover {{
  border-color: #0f172a;
  background: transparent;
}}
.roasist-channel-pill.is-active {{
  background: #0f172a;
  border-color: #0f172a;
  color: #ffffff !important;
}}

/* 10. Contact & Start-Your-Project Above-the-Fold Layout, Quick Contact Strip & Form UX */
.Hero_hero___ImMv {{
  height: auto !important;
  min-height: auto !important;
  padding-top: clamp(5.75rem, 8vw, 7.25rem) !important;
  padding-bottom: 1rem !important;
  margin-bottom: 0 !important;
}}
.Hero_hero___ImMv h2,
.Hero_hero___ImMv h1.roasist-promoted-h1 {{
  margin: 1.15rem 0 0.5rem 0 !important;
  font-size: clamp(2.25rem, 4.4vw, 3.85rem) !important;
  line-height: 1.06 !important;
  letter-spacing: -0.025em !important;
  max-width: 18ch !important;
}}
.Hero_hero___ImMv .Hero_bottom___aF_2 {{
  display: none !important;
}}
.Form_contactForm__X6bdS,
.Form_contactForm__X6bdS .FadeIn_container__bjQVL,
.Form_contactForm__X6bdS .FadeIn_container__bjQVL > span {{
  opacity: 1 !important;
  transform: none !important;
  visibility: visible !important;
}}
.Form_form___noC4 label.Form_hp__cVydL {{
  display: inline-flex !important;
  position: static !important;
  opacity: 1 !important;
  visibility: visible !important;
  pointer-events: auto !important;
  width: auto !important;
  height: auto !important;
  clip: auto !important;
  overflow: visible !important;
}}
.Form_form___noC4 input.Form_inputfile__ZF6M3,
.Form_form___noC4 label[for="files"] {{
  display: none !important;
}}
.roasist-quick-contact {{
  width: 100%;
  grid-column: 1 / -1;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  padding: 1.5rem;
  margin: 0.5rem 0 2.25rem 0;
  border-radius: 16px;
  background: #f8fafc;
  border: 1px solid rgba(15, 23, 42, 0.08);
}}
.roasist-quick-contact__item {{
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  text-decoration: none;
  color: #0f172a;
}}
.roasist-quick-contact__lbl {{
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.78rem;
  font-weight: 600;
  color: #64748b;
  letter-spacing: 0.01em;
}}
.roasist-quick-contact__val {{
  font-size: 0.98rem;
  font-weight: 600;
  color: #0f172a;
  transition: color 150ms var(--roasist-ease);
}}
a.roasist-quick-contact__item:hover .roasist-quick-contact__val {{
  color: #7602FF;
}}
.roasist-textarea {{
  width: 100%;
  min-height: 96px;
  resize: vertical;
  font-family: inherit;
  font-size: inherit;
  line-height: 1.5;
  padding-top: 0.75rem;
  background: transparent;
  border: none;
  border-bottom: 1px solid rgba(15, 23, 42, 0.22);
  color: inherit;
}}

/* 11. Mobile >=42px Touch Target Ergonomics */
@media (max-width: 768px) {{
  footer[class*="Footer_footer"] ul li a {{
    display: inline-flex !important;
    align-items: center !important;
    min-height: 40px !important;
    padding: 0.25rem 0 !important;
  }}
  .Form_form___noC4 fieldset label .Form_button__WKdUX {{
    min-height: 44px !important;
    display: inline-flex !important;
    align-items: center !important;
  }}
  .Form_form___noC4 label {{
    min-height: 42px;
    display: inline-flex;
    align-items: center;
  }}
}}
</style>"""

UX_SCRIPT = f"""<script id="{UX_SCRIPT_ID}">
(function() {{
  var isEn = document.documentElement.lang === 'en' || window.location.pathname.indexOf('/en/') === 0 || window.location.pathname === '/en';

  var PILLARS_TR = [
    {{ label: 'Performans Pazarlaması', href: '/hizmetler/performans-pazarlamasi/' }},
    {{ label: 'Teknik & Kurumsal SEO', href: '/hizmetler/seo/' }},
    {{ label: 'Yapay Zeka Aramaları (AEO & GEO)', href: '/hizmetler/aeo-geo/' }},
    {{ label: 'Web Tasarım & Yazılım', href: '/hizmetler/web-tasarim/' }},
    {{ label: 'Dönüşüm Optimizasyonu (CRO)', href: '/hizmetler/donusum-optimizasyonu/' }},
    {{ label: 'Grafik & Kreatif Tasarım', href: '/hizmetler/grafik-tasarim/' }},
    {{ label: '360° Dijital Pazarlama', href: '/hizmetler/360-derece-dijital-pazarlama-yonetimi/' }}
  ];
  var PILLARS_EN = [
    {{ label: 'Performance Marketing', href: '/en/performance-marketing/' }},
    {{ label: 'Technical & Enterprise SEO', href: '/en/seo/' }},
    {{ label: 'AI Search (AEO & GEO)', href: '/en/aeo-geo/' }},
    {{ label: 'Web Design & UI/UX', href: '/en/web-design/' }},
    {{ label: 'Conversion Optimization (CRO)', href: '/en/conversion-optimization/' }},
    {{ label: 'Graphic & Ad Creative', href: '/en/graphic-design/' }},
    {{ label: '360° Digital Growth', href: '/en/360-digital-marketing-management/' }}
  ];

  var PAID_TR = [
    {{ label: 'Tüm Kanallar', href: '/hizmetler/performans-pazarlamasi/' }},
    {{ label: 'Google Ads', href: '/hizmetler/performans-pazarlamasi/google-reklamlari/' }},
    {{ label: 'Meta & Instagram Ads', href: '/hizmetler/performans-pazarlamasi/instagram-reklamlari/' }},
    {{ label: 'TikTok Ads', href: '/hizmetler/performans-pazarlamasi/tiktok-reklamlari/' }},
    {{ label: 'Yandex Ads', href: '/hizmetler/performans-pazarlamasi/yandex-reklamlari/' }},
    {{ label: 'Bing Ads', href: '/hizmetler/performans-pazarlamasi/bing-reklamlari/' }},
    {{ label: 'LinkedIn Ads', href: '/hizmetler/performans-pazarlamasi/linkedin-reklamlari/' }}
  ];
  var PAID_EN = [
    {{ label: 'All Channels', href: '/en/performance-marketing/' }},
    {{ label: 'Google Ads', href: '/en/google-ads/' }},
    {{ label: 'Instagram & Meta Ads', href: '/en/instagram-ads/' }},
    {{ label: 'TikTok Ads', href: '/en/tiktok-ads/' }},
    {{ label: 'Yandex Ads', href: '/en/yandex-ads/' }},
    {{ label: 'Bing Ads', href: '/en/bing-ads/' }},
    {{ label: 'LinkedIn Ads', href: '/en/linkedin-ads/' }}
  ];

  function normPath(p) {{
    if (!p) return '/';
    var c = p.split('?')[0].split('#')[0];
    return c.endsWith('/') ? c : (c + '/');
  }}

  function ensureSkipAndA11y() {{
    var mainEl = document.querySelector('main') || document.querySelector('section[class*="Hero_"]') || document.querySelector('section');
    if (mainEl && !mainEl.id) mainEl.id = 'main-content';

    if (mainEl && !document.querySelector('.roasist-skip-link')) {{
      var skip = document.createElement('a');
      skip.className = 'roasist-skip-link';
      skip.href = '#main-content';
      skip.textContent = isEn ? 'Skip to main content' : 'Ana içeriğe atla';
      document.body.insertBefore(skip, document.body.firstChild);
    }}

    var logo = document.querySelector('a[class*="Header_logo"]');
    if (logo && !logo.getAttribute('aria-label')) {{
      logo.setAttribute('aria-label', isEn ? 'Roasist Home' : 'Roasist Ana Sayfa');
    }}
    var navBtn = document.querySelector('button[class*="PrimaryNavigation_icon"]');
    if (navBtn && !navBtn.getAttribute('aria-label')) {{
      navBtn.setAttribute('aria-label', isEn ? 'Toggle navigation menu' : 'Gezinme menüsünü aç veya kapat');
    }}
    document.querySelectorAll('button[class*="HeroVideo_icon"]').forEach(function(b) {{
      if (!b.getAttribute('aria-label')) b.setAttribute('aria-label', isEn ? 'Play video' : 'Videoyu oynat');
    }});
    document.querySelectorAll('.roasist-hero-title-arrow, [class*="Hero_arrow"]').forEach(function(a) {{
      a.setAttribute('aria-hidden', 'true');
    }});

    // Promote primary Hero display heading to semantic <h1> when page lacks a real <h1>
    if (document.querySelectorAll('h1').length === 0) {{
      var heroH2 = document.querySelector('.Hero_top__fPz2U h2, .Hero_top__9AiY_ h2, section h2');
      if (heroH2) {{
        var h1 = document.createElement('h1');
        h1.className = (heroH2.className ? heroH2.className + ' ' : '') + 'roasist-promoted-h1';
        while (heroH2.firstChild) h1.appendChild(heroH2.firstChild);
        heroH2.parentNode.replaceChild(h1, heroH2);
      }}
      document.querySelectorAll('.roasist-hero-page-label[aria-level="1"]').forEach(function(lbl) {{
        lbl.removeAttribute('role');
        lbl.removeAttribute('aria-level');
      }});
    }}
  }}

  function ensureBreadcrumbs() {{
    var cur = normPath(window.location.pathname);
    if (cur === '/' || cur === '/en/' || document.querySelector('.roasist-breadcrumb')) return;
    var titleRow = document.querySelector('.roasist-hero-title-row');
    if (!titleRow || !titleRow.parentNode) return;

    var crumbs = [];
    crumbs.push({{ label: isEn ? 'Home' : 'Ana Sayfa', href: isEn ? '/en/' : '/' }});

    if (!isEn && cur.indexOf('/hizmetler/') === 0 && cur !== '/hizmetler/') {{
      crumbs.push({{ label: 'Hizmetler', href: '/hizmetler/' }});
      if (cur.indexOf('/hizmetler/performans-pazarlamasi/') === 0 && cur !== '/hizmetler/performans-pazarlamasi/') {{
        crumbs.push({{ label: 'Performans Pazarlaması', href: '/hizmetler/performans-pazarlamasi/' }});
      }}
    }} else if (isEn && cur !== '/en/services/' && (
      cur.indexOf('-ads/') !== -1 ||
      cur === '/en/performance-marketing/' ||
      cur === '/en/seo/' ||
      cur === '/en/aeo-geo/' ||
      cur === '/en/web-design/' ||
      cur === '/en/conversion-optimization/' ||
      cur === '/en/graphic-design/' ||
      cur === '/en/360-digital-marketing-management/'
    )) {{
      crumbs.push({{ label: 'Services', href: '/en/services/' }});
      if (cur.indexOf('-ads/') !== -1) {{
        crumbs.push({{ label: 'Performance Marketing', href: '/en/performance-marketing/' }});
      }}
    }} else if (cur.indexOf('/blog/') === 0 && cur !== '/blog/') {{
      crumbs.push({{ label: 'Blog', href: '/blog/' }});
    }} else if (cur.indexOf('/referanslar/') === 0 && cur !== '/referanslar/') {{
      crumbs.push({{ label: 'Referanslar', href: '/referanslar/' }});
    }}

    var pageLblEl = titleRow.querySelector('.roasist-hero-page-label');
    var currentLabel = pageLblEl ? pageLblEl.textContent.trim() : document.title.split('|')[0].split('-')[0].trim();
    if (currentLabel) {{
      currentLabel = currentLabel.charAt(0).toUpperCase() + currentLabel.slice(1);
    }}

    var ol = document.createElement('ol');
    ol.className = 'roasist-breadcrumb';
    ol.setAttribute('aria-label', isEn ? 'Breadcrumb' : 'Sayfa konumu');

    crumbs.forEach(function(c) {{
      var li = document.createElement('li');
      var a = document.createElement('a');
      a.href = c.href;
      a.textContent = c.label;
      li.appendChild(a);
      ol.appendChild(li);

      var sep = document.createElement('li');
      sep.className = 'roasist-breadcrumb__sep';
      sep.setAttribute('aria-hidden', 'true');
      sep.textContent = '›';
      ol.appendChild(sep);
    }});

    var curLi = document.createElement('li');
    curLi.className = 'roasist-breadcrumb__current';
    curLi.setAttribute('aria-current', 'page');
    curLi.textContent = currentLabel;
    ol.appendChild(curLi);

    titleRow.parentNode.insertBefore(ol, titleRow);
  }}

  function ensureDiscoverAndChannelPills() {{
    var cur = normPath(window.location.pathname);
    var dmInner = document.querySelector('.DiscoverMore_linksInner__Vgx11');
    if (dmInner && !dmInner.dataset.roasistUpgraded) {{
      dmInner.dataset.roasistUpgraded = '1';
      var heading = dmInner.querySelector('.DiscoverMore_heading__fBuVc');
      var headingText = heading ? heading.textContent : (isEn ? 'Explore Services' : 'Diğer Hizmetlerimiz');
      while (dmInner.firstChild) dmInner.removeChild(dmInner.firstChild);

      var p = document.createElement('p');
      p.className = 'DiscoverMore_heading__fBuVc';
      p.textContent = headingText;
      dmInner.appendChild(p);

      var list = isEn ? PILLARS_EN : PILLARS_TR;
      list.forEach(function(item) {{
        var a = document.createElement('a');
        a.href = item.href;
        a.textContent = item.label;
        var isAct = (cur === item.href) || (!isEn && item.href === '/hizmetler/performans-pazarlamasi/' && cur.indexOf('/hizmetler/performans-pazarlamasi/') === 0) || (isEn && item.href === '/en/performance-marketing/' && cur.indexOf('-ads/') !== -1);
        if (isAct) {{
          a.className = 'DiscoverMoreLink_active__6IF37';
          a.setAttribute('aria-current', 'page');
        }}
        dmInner.appendChild(a);
      }});
    }}

    // Inject 6-channel Paid Media quick-switch bar on Performance Marketing & its sub-pages
    var isPaidPage = (!isEn && (cur.indexOf('/hizmetler/performans-pazarlamasi/') === 0 || /-reklamlari\\/$/.test(cur)))
      || (isEn && (cur === '/en/performance-marketing/' || /-ads\\/$/.test(cur)));

    if (isPaidPage && !document.querySelector('.roasist-channel-pills')) {{
      var heroBottom = document.querySelector('.Hero_bottom__5uvI_');
      if (heroBottom) {{
        var wrap = document.createElement('nav');
        wrap.className = 'roasist-channel-pills';
        wrap.setAttribute('aria-label', isEn ? 'Paid media channels' : 'Performans pazarlaması reklam kanalları');

        var lbl = document.createElement('p');
        lbl.className = 'roasist-channel-pills__label';
        lbl.textContent = isEn ? 'Paid Media Channels' : 'Reklam Kanalları (Alt Hizmetler)';
        wrap.appendChild(lbl);

        var row = document.createElement('div');
        row.className = 'roasist-channel-pills__list';
        (isEn ? PAID_EN : PAID_TR).forEach(function(ch) {{
          var a = document.createElement('a');
          a.href = ch.href;
          a.className = 'roasist-channel-pill';
          var slugEnd = ch.href.split('/').filter(Boolean).pop();
          if (cur === ch.href || (slugEnd !== 'performans-pazarlamasi' && slugEnd !== 'performance-marketing' && cur.endsWith('/' + slugEnd + '/'))) {{
            a.className += ' is-active';
            a.setAttribute('aria-current', 'page');
          }}
          a.textContent = ch.label;
          row.appendChild(a);
        }});
        wrap.appendChild(row);
        heroBottom.appendChild(wrap);
      }}
    }}
  }}

  function ensureMenuLangSwitcher() {{
    var nav = document.querySelector('nav[class*="PrimaryNavigation_navigation"]');
    if (!nav || nav.querySelector('.roasist-menu-lang')) return;
    var uiScript = document.querySelector('script[data-roasist-ui]');
    var trR = (uiScript && uiScript.getAttribute('data-tr-route')) || '/';
    var enR = (uiScript && uiScript.getAttribute('data-en-route')) || '/en/';

    var box = document.createElement('div');
    box.className = 'roasist-menu-lang roasist-lang-switch';
    box.setAttribute('role', 'navigation');
    box.setAttribute('aria-label', isEn ? 'Language switcher' : 'Dil seçimi');

    var aTr = document.createElement('a');
    aTr.href = trR;
    aTr.textContent = 'TR';
    if (!isEn) aTr.className = 'is-active';

    var aEn = document.createElement('a');
    aEn.href = enR;
    aEn.textContent = 'EN';
    if (isEn) aEn.className = 'is-active';

    box.appendChild(aTr);
    box.appendChild(aEn);
    nav.appendChild(box);
  }}

  function enhanceContactFormAndStrip() {{
    var form = document.querySelector('form.Form_form___noC4');
    if (!form) return;
    form.id = 'roasist-lead-form';

    // 1. Inject Quick Contact Strip above form once
    var outer = form.closest('.Form_formOuter__NHTHq') || form.parentElement;
    if (outer && outer.parentElement && !document.querySelector('.roasist-quick-contact')) {{
      var strip = document.createElement('div');
      strip.className = 'roasist-quick-contact';

      var items = isEn
        ? [
            {{ lbl: 'Direct Phone', val: '+90 540 507 53 50', href: 'tel:+905405075350' }},
            {{ lbl: 'WhatsApp Priority', val: 'Message Strategy Team →', href: 'https://wa.me/905405075350', ext: true }},
            {{ lbl: 'Corporate Email', val: 'info@roasist.com', href: 'mailto:info@roasist.com' }},
            {{ lbl: 'Response SLA', val: 'Within Same Business Day', href: null }}
          ]
        : [
            {{ lbl: 'Doğrudan Telefon', val: '+90 540 507 53 50', href: 'tel:+905405075350' }},
            {{ lbl: 'WhatsApp Hızlı Hat', val: 'Anında Mesaj Gönder →', href: 'https://wa.me/905405075350', ext: true }},
            {{ lbl: 'Kurumsal E-posta', val: 'info@roasist.com', href: 'mailto:info@roasist.com' }},
            {{ lbl: 'Ortalama Yanıt Süresi', val: 'Aynı İş Günü İçinde', href: null }}
          ];

      items.forEach(function(it) {{
        var el = document.createElement(it.href ? 'a' : 'div');
        el.className = 'roasist-quick-contact__item';
        if (it.href) {{
          el.href = it.href;
          if (it.ext) {{
            el.target = '_blank';
            el.rel = 'noopener noreferrer';
          }}
        }}
        var l = document.createElement('span');
        l.className = 'roasist-quick-contact__lbl';
        l.textContent = it.lbl;
        var v = document.createElement('span');
        v.className = 'roasist-quick-contact__val';
        v.textContent = it.val;
        el.appendChild(l);
        el.appendChild(v);
        strip.appendChild(el);
      }});

      outer.parentElement.insertBefore(strip, outer);
    }}

    // 2. Autocomplete & Phone input & Multi-line Textarea
    var fn = form.querySelector('input[name="firstName"]');
    if (fn) fn.setAttribute('autocomplete', 'given-name');
    var ln = form.querySelector('input[name="lastName"]');
    if (ln) ln.setAttribute('autocomplete', 'family-name');
    var em = form.querySelector('input[name="email"]');
    if (em) em.setAttribute('autocomplete', 'email');

    if (em && !form.querySelector('input[name="contactPhone"]')) {{
      var ph = document.createElement('input');
      ph.type = 'tel';
      ph.name = 'contactPhone';
      ph.required = true;
      ph.setAttribute('inputmode', 'tel');
      ph.setAttribute('autocomplete', 'tel');
      ph.className = 'Form_halfWidth__mwquS';
      ph.placeholder = isEn ? 'Phone / WhatsApp Number*' : 'Telefon / WhatsApp Numaranız*';
      em.insertAdjacentElement('afterend', ph);
    }}

    var msgInp = form.querySelector('input[name="message"]');
    if (msgInp) {{
      var ta = document.createElement('textarea');
      ta.name = 'message';
      ta.rows = 3;
      ta.className = msgInp.className + ' roasist-textarea';
      ta.placeholder = msgInp.placeholder || (isEn ? 'Project Goals & Notes' : 'Projeniz veya Hedefleriniz');
      msgInp.parentNode.replaceChild(ta, msgInp);
    }}

    // Smooth-scroll header CTA to form when already on contact page
    var hdrBtn = document.querySelector('header a[class*="Header_button"]');
    if (hdrBtn && !hdrBtn.dataset.roasistScrollBound) {{
      hdrBtn.dataset.roasistScrollBound = '1';
      hdrBtn.addEventListener('click', function(ev) {{
        ev.preventDefault();
        ev.stopImmediatePropagation();
        form.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
        var firstField = form.querySelector('input[name="firstName"]');
        if (firstField) setTimeout(function() {{ firstField.focus({{ preventScroll: true }}); }}, 450);
      }}, true);
    }}
  }}

  // Close open navigation menu on Escape key
  document.addEventListener('keydown', function(ev) {{
    if (ev.key !== 'Escape') return;
    var openNav = document.querySelector('[class*="PrimaryNavigation_open"], nav[data-open="true"]');
    var toggleBtn = document.querySelector('button[class*="PrimaryNavigation_icon"]');
    if (toggleBtn && (openNav || document.body.style.overflow === 'hidden')) {{
      toggleBtn.click();
    }}
  }});

  function runAll() {{
    try {{ ensureSkipAndA11y(); }} catch (e) {{}}
    try {{ ensureBreadcrumbs(); }} catch (e) {{}}
    try {{ ensureDiscoverAndChannelPills(); }} catch (e) {{}}
    try {{ ensureMenuLangSwitcher(); }} catch (e) {{}}
    try {{ enhanceContactFormAndStrip(); }} catch (e) {{}}
  }}

  if (document.readyState === 'loading') {{
    document.addEventListener('DOMContentLoaded', function() {{
      setTimeout(runAll, 150);
      setTimeout(runAll, 700);
    }});
  }} else {{
    setTimeout(runAll, 150);
    setTimeout(runAll, 700);
  }}
}})();
</script>"""


def resolve_pair(rel_html_path: str) -> tuple[str, str, str]:
    if rel_html_path == "kota-roasist-local.html" or rel_html_path == "index.html":
        route = "/"
    else:
        d = os.path.dirname(rel_html_path).replace(os.sep, "/")
        route = f"/{d}/" if d else "/"

    if route == "/en/" or route.startswith("/en/"):
        tr_r = EN_TO_TR_MAP.get(route, "/")
        return ("en", tr_r, route)
    else:
        if route in TR_TO_EN_MAP:
            en_r = TR_TO_EN_MAP[route]
        elif route.startswith("/blog/"):
            en_r = "/en/blog/"
        elif route.startswith("/referanslar/"):
            en_r = "/en/references/"
        else:
            en_r = "/en/"
        return ("tr", route, en_r)


def update_flight_nav_nodes(full_stream: str, is_en: bool) -> str:
    nodes = NAV_NODES_EN if is_en else NAV_NODES_TR
    cta_href = "/en/start-your-project/" if is_en else "/iletisim/"
    cta_title = "Start a Project" if is_en else "Projeye Başla"

    recs = parse_flight_stream(full_stream)
    for rec in recs:
        val = rec[2]
        if "menuItems" in val and "nodes" in val and val.startswith("["):
            try:
                arr = json.loads(val)
                target = None
                if isinstance(arr, list) and len(arr) >= 4 and isinstance(arr[3], dict):
                    target = arr[3]
                elif isinstance(arr, list) and len(arr) >= 2 and isinstance(arr[1], dict):
                    target = arr[1]
                if target and "menuItems" in target:
                    target["menuItems"]["nodes"] = nodes
                    target["ctaButton"] = {"url": cta_href, "title": cta_title, "target": ""}
                    rec[2] = json.dumps(arr, ensure_ascii=False, separators=(",", ":"))
            except Exception:
                pass
    return serialize_flight_stream(recs)


def step1_migrate_aeo_geo_slugs():
    old_tr = os.path.join(PUBLIC_DIR, "hizmetler", "yapay-zeka-seo")
    new_tr = os.path.join(PUBLIC_DIR, "hizmetler", "aeo-geo")
    if os.path.exists(old_tr):
        if os.path.exists(new_tr):
            shutil.rmtree(new_tr)
        shutil.move(old_tr, new_tr)
        print("[1/4] Moved public/hizmetler/yapay-zeka-seo -> public/hizmetler/aeo-geo")

    old_en = os.path.join(PUBLIC_DIR, "en", "ai-search-aeo-geo")
    new_en = os.path.join(PUBLIC_DIR, "en", "aeo-geo")
    if os.path.exists(old_en):
        if os.path.exists(new_en):
            shutil.rmtree(new_en)
        shutil.move(old_en, new_en)
        print("[1/4] Moved public/en/ai-search-aeo-geo -> public/en/aeo-geo")

    # Update sitemap.xml & helper scripts
    for rel_f in (
        "public/sitemap.xml",
        "scripts/update_seo_aeo_360_pages.py",
        "scripts/prelaunch_step4_seo_sitemap_404.py",
    ):
        fp = os.path.join(REPO_ROOT, rel_f)
        if os.path.exists(fp):
            s = open(fp, "r", encoding="utf-8").read()
            s2 = (
                s.replace("/hizmetler/yapay-zeka-seo/", "/hizmetler/aeo-geo/")
                .replace('"yapay-zeka-seo"', '"aeo-geo"')
                .replace("/en/ai-search-aeo-geo/", "/en/aeo-geo/")
                .replace('"ai-search-aeo-geo"', '"aeo-geo"')
            )
            if s2 != s:
                open(fp, "w", encoding="utf-8").write(s2)


def step2_and_3_and_4_upgrade_all_pages():
    slug_and_cta_reps_tr = [
        ("/hizmetler/yapay-zeka-seo/", "/hizmetler/aeo-geo/"),
        ("/hizmetler/yapay-zeka-seo", "/hizmetler/aeo-geo"),
        ("service/yapay-zeka-seo", "/hizmetler/aeo-geo/"),
        ('"slug":"yapay-zeka-seo"', '"slug":"aeo-geo"'),
        ("'yapay-zeka-seo':", "'aeo-geo':"),
        ("/en/ai-search-aeo-geo/", "/en/aeo-geo/"),
        ("/en/ai-search-aeo-geo", "/en/aeo-geo"),
        ("service/ai-search-aeo-geo", "/en/aeo-geo/"),
        ('"slug":"ai-search-aeo-geo"', '"slug":"aeo-geo"'),
        ("'ai-search-aeo-geo':", "'aeo-geo':"),
        (">Bize Ulaşın<", ">Teklif Al<"),
        ('"Bize Ulaşın"', '"Teklif Al"'),
        (">Projeye Başlayın<", ">Projeye Başla<"),
        ('"Projeye Başlayın"', '"Projeye Başla"'),
    ]
    slug_and_cta_reps_en = [
        ("/hizmetler/yapay-zeka-seo/", "/hizmetler/aeo-geo/"),
        ("/hizmetler/yapay-zeka-seo", "/hizmetler/aeo-geo"),
        ("service/yapay-zeka-seo", "/hizmetler/aeo-geo/"),
        ('"slug":"yapay-zeka-seo"', '"slug":"aeo-geo"'),
        ("'yapay-zeka-seo':", "'aeo-geo':"),
        ("/en/ai-search-aeo-geo/", "/en/aeo-geo/"),
        ("/en/ai-search-aeo-geo", "/en/aeo-geo"),
        ("service/ai-search-aeo-geo", "/en/aeo-geo/"),
        ('"slug":"ai-search-aeo-geo"', '"slug":"aeo-geo"'),
        ("'ai-search-aeo-geo':", "'aeo-geo':"),
    ]

    updated = 0
    for fp in sorted(glob.glob(os.path.join(PUBLIC_DIR, "**", "*.html"), recursive=True)):
        rel = os.path.relpath(fp, PUBLIC_DIR)
        if rel == "404.html" or rel.endswith("-3d.html"):
            continue

        orig = open(fp, "r", encoding="utf-8").read()
        lang, tr_r, en_r = resolve_pair(rel)
        is_en = lang == "en"

        # 1. Flight-safe route & CTA text unification
        text = apply_replacements_flight_safe(
            orig, slug_and_cta_reps_en if is_en else slug_and_cta_reps_tr
        )

        # 2. Update SSR PrimaryNavigation + Flight menuItems.nodes
        ssr_nav = build_ssr_nav(is_en=is_en)
        if '<nav class="PrimaryNavigation_navigation__l8Jgb">' in text:
            text = re.sub(
                r'<nav class="PrimaryNavigation_navigation__l8Jgb">.*?</nav>',
                lambda _: ssr_nav,
                text,
                count=1,
                flags=re.S,
            )

        matches, _, full = extract_flight_chunks(text)
        if matches:
            new_full = update_flight_nav_nodes(full, is_en=is_en)
            if new_full != full:
                parts = []
                last_end = 0
                for idx, m in enumerate(matches):
                    parts.append(text[last_end : m.start()])
                    if idx == 0:
                        encoded = json.dumps(new_full, ensure_ascii=False)[1:-1].replace("</", "\\u003c/")
                        parts.append(m.group(1) + encoded + m.group(3))
                    else:
                        parts.append("")
                    last_end = m.end()
                parts.append(text[last_end:])
                text = "".join(parts)

        # 3. Fix hreflang & data-roasist-ui attributes + remove stale E-Ticaret formMap override
        tr_abs = f"{SITE_ORIGIN}{tr_r}"
        en_abs = f"{SITE_ORIGIN}{en_r}"
        text = re.sub(r'<link rel="alternate" hreflang="[^"]+" href="[^"]+"\s*/>', "", text)
        hreflang_block = (
            f'<link rel="alternate" hreflang="tr" href="{tr_abs}"/>'
            f'<link rel="alternate" hreflang="en" href="{en_abs}"/>'
            f'<link rel="alternate" hreflang="x-default" href="{tr_abs}"/>'
        )
        head_end = text.find("</head>")
        if head_end != -1:
            text = text[:head_end] + hreflang_block + text[head_end:]

        text = re.sub(
            r'<script data-roasist-ui[^>]*>',
            f'<script data-roasist-ui data-lang="{lang}" data-tr-route="{tr_r}" data-en-route="{en_r}">',
            text,
        )
        text = text.replace(
            "'E-Ticaret': 'Performance Marketing & ROAS',",
            "'E-Ticaret': 'Conversion Optimization (CRO)',",
        ).replace(
            "'Branding': 'Brand & Creative Strategy',",
            "'Branding': 'Performance Marketing (Ads)',",
        )

        # 4. Inject UX Overhaul CSS & JS idempotently
        css_re = re.compile(rf'<style id="{UX_STYLE_ID}">.*?</style>', re.S)
        if css_re.search(text):
            text = css_re.sub(lambda _: UX_CSS, text, count=1)
        else:
            he = text.find("</head>")
            if he != -1:
                text = text[:he] + UX_CSS + text[he:]

        js_re = re.compile(rf'<script id="{UX_SCRIPT_ID}">.*?</script>', re.S)
        if js_re.search(text):
            text = js_re.sub(lambda _: UX_SCRIPT, text, count=1)
        else:
            be = text.rfind("</body>")
            if be != -1:
                text = text[:be] + UX_SCRIPT + text[be:]

        if text != orig:
            m_chk, _, f_chk = extract_flight_chunks(text)
            if m_chk:
                parse_flight_stream(f_chk)
            open(fp, "w", encoding="utf-8").write(text)
            updated += 1

    print(f"[2-4/4] Upgraded navigation, CTAs, hreflang, and UI/UX layer across {updated} HTML pages")


def main():
    step1_migrate_aeo_geo_slugs()
    step2_and_3_and_4_upgrade_all_pages()


if __name__ == "__main__":
    main()
