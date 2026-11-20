#!/usr/bin/env python3
"""
Pre-Launch Step 1:
Upgrades the remaining 8 unupgraded service pages (in both public/ and dist/):
  1. LinkedIn Ads (TR 2 routes + EN 1 route) + adds 'LinkedIn Ads' tag to Homepage Performans Pazarlaması
  2. Facebook Ads (TR 2 routes + EN 1 route)
  3. Main Services Hub (/hizmetler/ & /en/services/) with all 6 core Roasist pillars,
     bespoke SVG stages, and working 'Detaylı İncele' / 'Explore Service' links.
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
from sync_performans_statistics_cards import get_homepage_statistics, update_target_page as sync_stats
from update_performans_process import TR_STEPS, EN_STEPS, update_page as update_process
from update_tiktok_yandex_pages import SHARED_STAGE_CSS, extract_flight_chunks, update_channel_campaigns
from update_meta_ads_page import TR_META_CAMPAIGNS, EN_META_CAMPAIGNS, update_campaigns_and_stages as update_meta_campaigns

# ===========================================================================
# 1. LINKEDIN ADS — 5 B2B Campaign Formats + 5 White-Stage SVG Animations
# ===========================================================================

TR_LINKEDIN_CAMPAIGNS = [
    {"title": "Sponsored Content (Akış İçi Kurumsal Reklamlar)", "desc": "Karar verici yöneticilerin (CEO, CMO, CFO, Satın Alma Direktörleri) profesyonel LinkedIn akışında tek görsel, carousel ve belge (Document Ads) formatlarıyla yüksek otorite kurun."},
    {"title": "LinkedIn Lead Gen Forms (Hazır B2B Formlar)", "desc": "Kullanıcının adı, iş e-postası, unvanı ve şirket bilgisinin LinkedIn profilinden otomatik dolduğu formlarla sürtünmesiz ve yüksek dönüşümlü kurumsal talepler toplayın."},
    {"title": "Message & Conversation Ads (InMail)", "desc": "Hedeflediğiniz karar vericilerin doğrudan LinkedIn mesaj kutusuna kişiselleştirilmiş kurumsal teklifler, etkinlik davetleri ve demo randevu akışları gönderin."},
    {"title": "Account-Based Marketing (ABM & Şirket Hedefleme)", "desc": "Hedef müşteri listenizdeki (Target Accounts) spesifik şirketleri, çalışan büyüklüğünü ve departmanları nokta atışı eşleştirerek kurumsal satış döngünüzü hızlandırın."},
    {"title": "Video & Thought Leader Reklamları", "desc": "Kurucularınızın ve yöneticilerinizin uzmanlık paylaşımlarını (Thought Leader Ads) ve kurumsal video içeriklerinizi hedef sektördeki karar vericilere ölçekli biçimde ulaştırın."},
]

EN_LINKEDIN_CAMPAIGNS = [
    {"title": "Sponsored Content & Document Ads", "desc": "Engage C-suite executives, VPs, and key decision-makers directly in the LinkedIn feed with single-image, carousel, and gated Document Ads."},
    {"title": "LinkedIn Lead Gen Forms", "desc": "Capture high-intent B2B pipeline seamlessly using pre-filled forms populated automatically with verified work email, job title, and company data."},
    {"title": "Message & Conversation Ads (InMail)", "desc": "Deliver personalized executive invitations, product demos, and whitepapers straight into target decision-makers' LinkedIn inboxes."},
    {"title": "Account-Based Marketing (ABM Targeting)", "desc": "Upload target company lists and layer industry, company size, and seniority filters to surround buying committees across enterprise accounts."},
    {"title": "Video & Thought Leader Ads", "desc": "Amplify authentic founder and executive insights alongside crisp B2B video storytelling to build category trust and pipeline."},
]

SVG_LI_FEED = """
<div class="roasist-brand-stage li-sub-stage">
  <svg viewBox="0 0 600 320" class="sub-brand-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="LinkedIn Sponsored Content">
    <defs><filter id="liF1" x="-15%" y="-15%" width="130%" height="140%"><feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#0F172A" flood-opacity="0.08"/></filter></defs>
    <g class="sub-p1-slide" filter="url(#liF1)">
      <rect x="164" y="68" width="272" height="184" rx="18" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <rect x="184" y="86" width="32" height="32" rx="8" fill="#0A66C2"/>
      <rect x="226" y="90" width="118" height="9" rx="4.5" fill="#0F172A"/>
      <rect x="226" y="105" width="76" height="7" rx="3.5" fill="#64748B"/>
      <rect x="184" y="130" width="232" height="78" rx="12" fill="#EFF6FF"/>
      <rect x="204" y="150" width="128" height="10" rx="5" fill="#0A66C2"/>
      <rect x="204" y="168" width="92" height="8" rx="4" fill="#93C5FD"/>
      <rect x="184" y="218" width="72" height="18" rx="9" fill="#0A66C2"/>
    </g>
    <g class="sub-emblem-162">
      <rect x="262" y="122" width="76" height="76" rx="18" fill="#0A66C2"/>
      <circle cx="284" cy="145" r="5.5" fill="#FFFFFF"/>
      <rect x="279" y="155" width="10" height="24" rx="2" fill="#FFFFFF"/>
      <path d="M297 155 h9 v4 c2-3 5.5-4.5 9.5-4.5 c7 0 11.5 4.5 11.5 12.5 v12 h-10 v-10.5 c0-4-1.8-6-5-6 c-3.2 0-5 2.2-5 6 v10.5 h-10 z" fill="#FFFFFF"/>
    </g>
    <g class="sub-wordmark"><text x="190" y="174" font-family="'Inter', Arial, sans-serif" font-size="34" font-weight="700" fill="#0F172A" letter-spacing="-0.8">Sponsored Ads</text></g>
  </svg>
</div>
""".strip()

SVG_LI_LEADS = """
<div class="roasist-brand-stage li-sub-stage">
  <svg viewBox="0 0 600 320" class="sub-brand-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="LinkedIn Lead Gen Forms">
    <defs><filter id="liF2" x="-15%" y="-15%" width="130%" height="140%"><feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#0F172A" flood-opacity="0.08"/></filter></defs>
    <g class="sub-p1-slide" filter="url(#liF2)">
      <rect x="196" y="62" width="208" height="196" rx="20" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <rect x="214" y="82" width="32" height="32" rx="8" fill="#0A66C2"/>
      <rect x="256" y="88" width="104" height="9" rx="4.5" fill="#0F172A"/>
      <rect x="214" y="126" width="172" height="26" rx="8" fill="#F8FAFC" stroke="#CBD5E1"/>
      <rect x="224" y="136" width="112" height="7" rx="3.5" fill="#0A66C2"/>
      <rect x="214" y="160" width="172" height="26" rx="8" fill="#F8FAFC" stroke="#CBD5E1"/>
      <rect x="224" y="170" width="134" height="7" rx="3.5" fill="#475569"/>
      <rect x="214" y="198" width="172" height="36" rx="18" fill="#0A66C2"/>
      <text x="300" y="221" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="12">B2B LEAD ✓</text>
    </g>
    <g class="sub-emblem-152">
      <rect x="262" y="120" width="76" height="80" rx="18" fill="#0A66C2"/>
      <rect x="278" y="140" width="44" height="7" rx="3.5" fill="#FFFFFF"/>
      <rect x="278" y="155" width="32" height="7" rx="3.5" fill="#93C5FD"/>
      <circle cx="328" cy="188" r="17" fill="#10B981" stroke="#FFFFFF" stroke-width="3"/>
      <path d="M321 188 L326 193 L336 183" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
    </g>
    <g class="sub-wordmark"><text x="206" y="174" font-family="'Inter', Arial, sans-serif" font-size="36" font-weight="700" fill="#0F172A" letter-spacing="-0.8">Lead Gen Forms</text></g>
  </svg>
</div>
""".strip()

SVG_LI_INMAIL = """
<div class="roasist-brand-stage li-sub-stage">
  <svg viewBox="0 0 600 320" class="sub-brand-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="LinkedIn InMail Ads">
    <defs><filter id="liF3" x="-15%" y="-15%" width="130%" height="140%"><feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#0F172A" flood-opacity="0.08"/></filter></defs>
    <g class="sub-p1-pop" filter="url(#liF3)">
      <rect x="148" y="76" width="304" height="168" rx="22" fill="#FFFFFF" stroke="#0A66C2" stroke-width="1.8"/>
      <circle cx="186" cy="112" r="16" fill="#0A66C2"/>
      <rect x="214" y="102" width="132" height="9" rx="4.5" fill="#0F172A"/>
      <rect x="214" y="117" width="84" height="7" rx="3.5" fill="#64748B"/>
      <rect x="170" y="144" width="260" height="44" rx="14" fill="#EFF6FF"/>
      <rect x="188" y="162" width="176" height="8" rx="4" fill="#0A66C2"/>
      <rect x="170" y="200" width="108" height="26" rx="13" fill="#0A66C2"/>
      <text x="224" y="217" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="10.5">BOOK DEMO</text>
    </g>
    <g class="sub-emblem-138">
      <rect x="262" y="122" width="76" height="76" rx="22" fill="#0A66C2"/>
      <rect x="278" y="142" width="44" height="34" rx="6" fill="#FFFFFF"/>
      <path d="M280 145 L300 160 L320 145" fill="none" stroke="#0A66C2" stroke-width="3.2" stroke-linecap="round"/>
    </g>
    <g class="sub-wordmark"><text x="224" y="174" font-family="'Inter', Arial, sans-serif" font-size="40" font-weight="700" fill="#0F172A" letter-spacing="-0.8">InMail Ads</text></g>
  </svg>
</div>
""".strip()

SVG_LI_ABM = """
<div class="roasist-brand-stage li-sub-stage">
  <svg viewBox="0 0 600 320" class="sub-brand-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Account Based Marketing">
    <g class="sub-p1-pop">
      <circle cx="300" cy="160" r="86" fill="none" stroke="#CBD5E1" stroke-width="1.6" stroke-dasharray="5 6"/>
      <circle cx="300" cy="160" r="54" fill="none" stroke="#0A66C2" stroke-width="1.8" opacity="0.45"/>
      <circle cx="300" cy="160" r="26" fill="#0A66C2"/>
      <circle cx="300" cy="154" r="6.5" fill="#FFFFFF"/>
      <path d="M288 170 c0-5.5 5.5-8.5 12-8.5 s12 3 12 8.5" fill="#FFFFFF"/>
      <rect x="268" y="64" width="64" height="24" rx="12" fill="#0F172A"/>
      <text x="300" y="80" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="10">C-SUITE</text>
      <circle cx="222" cy="196" r="13" fill="#0A66C2"/>
      <circle cx="378" cy="196" r="13" fill="#0EA5E9"/>
    </g>
    <g class="sub-emblem-156">
      <circle cx="300" cy="160" r="38" fill="#0A66C2"/>
      <circle cx="300" cy="160" r="20" fill="none" stroke="#FFFFFF" stroke-width="4"/>
      <circle cx="300" cy="160" r="7" fill="#FFFFFF"/>
    </g>
    <g class="sub-wordmark"><text x="198" y="174" font-family="'Inter', Arial, sans-serif" font-size="36" font-weight="700" fill="#0F172A" letter-spacing="-0.8">ABM Targeting</text></g>
  </svg>
</div>
""".strip()

SVG_LI_VIDEO = """
<div class="roasist-brand-stage li-sub-stage">
  <svg viewBox="0 0 600 320" class="sub-brand-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Thought Leader Video Ads">
    <defs><filter id="liF5" x="-15%" y="-15%" width="130%" height="140%"><feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#0F172A" flood-opacity="0.09"/></filter></defs>
    <g class="sub-p1-slide" filter="url(#liF5)">
      <rect x="144" y="74" width="312" height="172" rx="20" fill="#0F172A"/>
      <rect x="158" y="88" width="284" height="122" rx="12" fill="#1E293B"/>
      <rect x="272" y="130" width="56" height="38" rx="12" fill="#0A66C2"/>
      <polygon points="295,141 295,157 310,149" fill="#FFFFFF"/>
      <rect x="166" y="222" width="196" height="6" rx="3" fill="#0A66C2"/>
    </g>
    <g class="sub-emblem-162">
      <rect x="256" y="124" width="88" height="72" rx="18" fill="#0A66C2"/>
      <polygon points="290,144 290,176 318,160" fill="#FFFFFF"/>
    </g>
    <g class="sub-wordmark"><text x="192" y="174" font-family="'Inter', Arial, sans-serif" font-size="35" font-weight="700" fill="#0F172A" letter-spacing="-0.8">Thought Leader</text></g>
  </svg>
</div>
""".strip()

LINKEDIN_STAGES = [SVG_LI_FEED, SVG_LI_LEADS, SVG_LI_INMAIL, SVG_LI_ABM, SVG_LI_VIDEO]

# ===========================================================================
# 2. MAIN SERVICES HUB (/hizmetler/ & /en/services/) — 6 Pillars WITH Buttons
# ===========================================================================

TR_HUB_SERVICES = [
    {"title": "Performans Pazarlaması & Reklam", "desc": "Google, Meta, TikTok, Yandex, Bing ve LinkedIn reklamlarını veri odaklı teklif stratejileriyle yöneterek gerçek ciro ve yüksek ROAS üretiyoruz.", "href": "/hizmetler/performans-pazarlamasi/", "btn": "Detaylı İncele"},
    {"title": "Kurumsal Web Tasarım & UI/UX", "desc": "Şablonlardan uzak, ultra hızlı, mobil öncelikli ve yüksek dönüşüm (ROI) odaklı modern kurumsal web siteleri ve e-ticaret deneyimleri tasarlıyoruz.", "href": "/hizmetler/web-tasarim/", "btn": "Detaylı İncele"},
    {"title": "Grafik & Kreatif Reklam Stüdyosu", "desc": "Tıklama oranlarını (CTR) artıran performans reklam kreatifleri, motion videolar ve güçlü kurumsal kimlik sistemleri üretiyoruz.", "href": "/hizmetler/grafik-tasarim/", "btn": "Detaylı İncele"},
    {"title": "Dönüşüm Oranı Optimizasyonu (CRO)", "desc": "Isı haritaları, huni analizi ve bilimsel A/B testleriyle mevcut web trafiğinizden elde ettiğiniz satış ve form dönüşümlerini katlıyoruz.", "href": "/hizmetler/donusum-optimizasyonu/", "btn": "Detaylı İncele"},
    {"title": "Teknik SEO & Yapay Zeka Aramaları (AEO & GEO)", "desc": "Markanızı hem Google organik sonuçlarında hem de ChatGPT, Gemini ve Perplexity yanıtlarında birincil kaynak konumuna taşıyoruz.", "href": "/hizmetler/seo/", "btn": "Detaylı İncele"},
    {"title": "360° Dijital Büyüme Yönetimi", "desc": "Performans reklamları, SEO/AEO, kreatif üretim, web yazılım ve analitiği tek bir uzman büyüme ekibiyle uçtan uca senkronize ediyoruz.", "href": "/hizmetler/360-derece-dijital-pazarlama-yonetimi/", "btn": "Detaylı İncele"},
]

EN_HUB_SERVICES = [
    {"title": "Performance Marketing & Paid Media", "desc": "We manage Google, Meta, TikTok, Yandex, Bing, and LinkedIn campaigns around unit economics to scale measurable revenue and ROAS.", "href": "/en/performance-marketing/", "btn": "Explore Service"},
    {"title": "Bespoke Web Design & UI/UX", "desc": "Template-free, sub-second, mobile-first corporate websites and e-commerce stores engineered for brand authority and high conversion rates.", "href": "/en/web-design/", "btn": "Explore Service"},
    {"title": "Graphic & Ad Creative Studio", "desc": "High-CTR performance ad creatives, motion design, and cohesive visual identity systems built for rapid creative iteration.", "href": "/en/graphic-design/", "btn": "Explore Service"},
    {"title": "Conversion Rate Optimization (CRO)", "desc": "Heatmaps, funnel diagnostics, and statistically rigorous A/B testing that turn more of your existing traffic into qualified leads and sales.", "href": "/en/conversion-optimization/", "btn": "Explore Service"},
    {"title": "Enterprise SEO & AI Search (AEO & GEO)", "desc": "Compound organic visibility across Google SERPs and become the primary cited brand in ChatGPT, Gemini, and Perplexity.", "href": "/en/seo/", "btn": "Explore Service"},
    {"title": "360° Digital Growth Management", "desc": "Unify paid acquisition, organic/AI search, creative production, web engineering, and attribution under one dedicated growth pod.", "href": "/en/360-digital-marketing-management/", "btn": "Explore Service"},
]

from update_seo_aeo_360_pages import SVG_360_OMNI, SVG_SEO_TECH, SVG_AEO_CITE
from update_web_design_page import SVG_WEB_UIUX, SVG_WEB_CRO
from update_creative_and_cro_pages import SVG_GD_ADS

HUB_STAGES = [
    SVG_360_OMNI.replace("g360-sub-stage", "hub-sub-stage"),
    SVG_WEB_UIUX.replace("wd-sub-stage", "hub-sub-stage"),
    SVG_GD_ADS.replace("gd-sub-stage", "hub-sub-stage"),
    SVG_WEB_CRO.replace("wd-sub-stage", "hub-sub-stage"),
    SVG_AEO_CITE.replace("aeo-sub-stage", "hub-sub-stage"),
    SVG_SEO_TECH.replace("seo-sub-stage", "hub-sub-stage"),
]

ARROW_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 17.1 15.17" '
    'class="Button_buttonArrow__0W9XI"><path d="m17.1,7.58s-.01-.04-.01-.06c.01-.22-.06-.45-.24-.61'
    'L9.23.19c-.31-.27-.78-.24-1.06.07-.27.31-.24.78.07,1.06l6.26,5.52H.75c-.41,0-.75.34-.75.75'
    's.34.75.75.75h13.74l-6.26,5.52c-.31.27-.34.75-.07,1.06.15.17.35.25.56.25.18,0,.35-.06.5-.19'
    'l7.62-6.72c.18-.16.25-.39.24-.61,0-.02.01-.04.01-.06Z" fill="currentColor"></path></svg>'
)


def add_linkedin_tag_to_homepage(home_path, is_en=False):
    text = open(home_path, "r", encoding="utf-8").read()
    changed = False
    if is_en:
        ssr_anchor = '<a class="ServicesPanel_tag__JYwRk" href="service/bing-ads">Bing Ads</a>'
        ssr_add = '<a class="ServicesPanel_tag__JYwRk" href="service/linkedin-ads">LinkedIn Ads</a>'
        if ssr_add not in text and ssr_anchor in text:
            text = text.replace(ssr_anchor, ssr_anchor + ssr_add, 1)
            changed = True
        fl_anchor = '\\"slug\\":\\"bing-ads\\",\\"title\\":\\"Bing Ads\\"}'
        fl_add = ',{\\"id\\":\\"cG9zdDo4ODk=\\",\\"slug\\":\\"linkedin-ads\\",\\"title\\":\\"LinkedIn Ads\\"}'
        if '\\"slug\\":\\"linkedin-ads\\"' not in text and fl_anchor in text:
            text = text.replace(fl_anchor, fl_anchor + fl_add, 1)
            changed = True
    else:
        ssr_anchor = '<a class="ServicesPanel_tag__JYwRk" href="service/bing-reklamlari">Bing Ads</a>'
        ssr_add = '<a class="ServicesPanel_tag__JYwRk" href="service/linkedin-reklamlari">LinkedIn Ads</a>'
        if ssr_add not in text and ssr_anchor in text:
            text = text.replace(ssr_anchor, ssr_anchor + ssr_add, 1)
            changed = True
        fl_anchor = '\\"slug\\":\\"bing-reklamlari\\",\\"title\\":\\"Bing Ads\\"}'
        fl_add = ',{\\"id\\":\\"cG9zdDo4ODk=\\",\\"slug\\":\\"linkedin-reklamlari\\",\\"title\\":\\"LinkedIn Ads\\"}'
        if '\\"slug\\":\\"linkedin-reklamlari\\"' not in text and fl_anchor in text:
            text = text.replace(fl_anchor, fl_anchor + fl_add, 1)
            changed = True
    if changed:
        open(home_path, "w", encoding="utf-8").write(text)
        print(f"[OK] Added 'LinkedIn Ads' tag to {os.path.relpath(home_path, REPO_ROOT)}")


def update_services_hub_page(target_path, items, stages, is_gh_pages=False):
    text = open(target_path, "r", encoding="utf-8").read()
    placeholder = "/roasist-web/roasist-logo.svg" if is_gh_pages else "/roasist-logo.svg"
    url_prefix = "/roasist-web" if is_gh_pages else ""
    style_id = "roasist-hub-brand-stages-css"
    script_id = "roasist-hub-brand-stages-js"

    # Keep buttons visible on the Services Hub!
    hub_css = SHARED_STAGE_CSS.replace(
        ".TextImageRows_textImageRows__lOU02 .TextImageRows_buttonContainer___PqVy {\n  display: none !important;\n}",
        ""
    )
    style_block = f'<style id="{style_id}">{hub_css}</style>'
    style_re = re.compile(rf'<style id="{style_id}">.*?</style>', re.S)
    if style_re.search(text):
        text = style_re.sub(style_block, text, count=1)
    else:
        head_end = text.find("</head>")
        text = text[:head_end] + style_block + text[head_end:]

    esc = lambda s: html_lib.escape(str(s), quote=True)
    ssr_rows = []
    fl_rows = []
    for idx, it in enumerate(items):
        href = url_prefix + it["href"] if (url_prefix and it["href"].startswith("/")) else it["href"]
        ssr_rows.append(
            '<div class="TextImageRows_row__PPlpB">'
            '<div class="TextImageRows_text__bRCSP">'
            f'<h3 class="TextImageRows_heading__RS3OS"><span class="LineByLine_headingOuter__JmusT"><span>{esc(it["title"])}</span></span></h3>'
            f'<div class="TextImageRows_text__bRCSP"><span class="FadeIn_container__bjQVL" data-fill="false"><span><p>{esc(it["desc"])}</p>\n</span></span></div>'
            '<div class="TextImageRows_buttonContainer___PqVy"><span class="FadeIn_container__bjQVL" data-fill="false">'
            '<div class="Magnetic_magnetic__LncOy" data-fill="false"><div class="Button_button__JJiqJ" data-direction="forwards">'
            f'<a class="Button_inner__fnyH6" href="{esc(href)}"><span class="Button_border__hirH2"></span>'
            f'<span class="Button_text__IZaCD"><span class="Button_textInner__JTTHe">{esc(it["btn"])}</span>{ARROW_SVG}</span></a>'
            '</div></div></span></div></div>'
            '<figure class="TextImageRows_media__twu3R"><div class="ImageEnter_image__FSEP_" data-fill="true">'
            f'<span class="Image_image__RAAdZ Image_fill__EiIzS"><img data-srcset="" data-src="{esc(placeholder)}" alt="" fetchPriority="low" height="1224" width="1224" sizes="auto" class="lazyload"/></span>'
            '</div></figure></div>'
        )
        fl_rows.append([
            "$", "div", str(idx), {
                "className": "TextImageRows_row__PPlpB",
                "children": [
                    ["$", "div", None, {
                        "className": "TextImageRows_text__bRCSP",
                        "children": [
                            ["$", "h3", None, {"className": "TextImageRows_heading__RS3OS", "children": ["$", "$L2c", None, {"children": ["$", "span", None, {"dangerouslySetInnerHTML": {"__html": it["title"]}}]}]}],
                            ["$", "div", None, {"className": "TextImageRows_text__bRCSP", "children": ["$", "$L2e", None, {"delay": 0.3, "children": ["$", "span", None, {"dangerouslySetInnerHTML": {"__html": f"<p>{it['desc']}</p>\n"}}]}]}],
                            ["$", "div", None, {"className": "TextImageRows_buttonContainer___PqVy", "children": ["$", "$L2e", None, {"delay": 0.3, "children": ["$", "$L21", None, {"href": href, "type": "a-internal", "text": it["btn"]}]}]}],
                        ],
                    }],
                    ["$", "figure", None, {
                        "className": "TextImageRows_media__twu3R",
                        "children": ["$", "$L4a", None, {"fill": True, "children": [["$", "$L47", None, {"image": {"altText": "", "srcSet": "", "sourceUrl": placeholder, "mediaDetails": {"width": 1224, "height": 1224}}, "layout": "fill"}], False]}],
                    }],
                ],
            }
        ])

    sec_re = re.compile(r'(<section class="TextImageRows_textImageRows__lOU02"><div class="container">)(.*?)(</div></section>)', re.S)
    text = sec_re.sub(lambda m: m.group(1) + "".join(ssr_rows) + m.group(3), text, count=1)

    matches, _, full = extract_flight_chunks(text)
    recs = parse_flight_stream(full)
    for i, rec in enumerate(recs):
        if rec[0] == "line" and "TextImageRows_textImageRows__lOU02" in rec[2]:
            obj = json.loads(rec[2])
            obj[3]["children"][3]["children"][0] = fl_rows
            recs[i] = ["line", rec[1], json.dumps(obj, ensure_ascii=False, separators=(",", ":"))]
            break
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

    mount_js = f"""<script id="{script_id}">
(function() {{
  var STAGES = {json.dumps(stages, ensure_ascii=False)};
  function mount() {{
    var medias = document.querySelectorAll('.TextImageRows_textImageRows__lOU02 .TextImageRows_media__twu3R');
    medias.forEach(function(fig, idx) {{
      if (idx >= STAGES.length) return;
      if (fig.querySelector('.hub-sub-stage')) return;
      fig.style.position = 'relative';
      var wrap = document.createElement('div');
      wrap.innerHTML = STAGES[idx];
      var stage = wrap.firstElementChild;
      if (stage) fig.appendChild(stage);
      fig.querySelectorAll('video, img').forEach(function(el) {{
        el.style.opacity = '0';
        el.style.pointerEvents = 'none';
      }});
    }});
  }}
  if (document.readyState === 'loading') {{ document.addEventListener('DOMContentLoaded', mount); }} else {{ mount(); }}
  new MutationObserver(mount).observe(document.documentElement, {{ childList: true, subtree: true }});
  setTimeout(mount, 400);
  setTimeout(mount, 1500);
}})();
</script>"""
    script_re = re.compile(rf'<script id="{script_id}">.*?</script>', re.S)
    if script_re.search(text):
        text = script_re.sub(lambda _: mount_js, text, count=1)
    else:
        body_end = text.rfind("</body>")
        text = text[:body_end] + mount_js + text[body_end:]

    open(target_path, "w", encoding="utf-8").write(text)
    print(f"[OK] Upgraded Services Hub {os.path.relpath(target_path, REPO_ROOT)} ({len(text):,} bytes)")


def main():
    for rel, is_en in [
        ("public/kota-roasist-local.html", False),
        ("public/en/index.html", True),
        ("dist/index.html", False),
        ("dist/en/index.html", True),
    ]:
        p = os.path.join(REPO_ROOT, rel)
        if os.path.exists(p):
            add_linkedin_tag_to_homepage(p, is_en=is_en)

    # 1. LinkedIn Ads
    li_jobs = [
        ("public/kota-roasist-local.html", "public/hizmetler/performans-pazarlamasi/linkedin-reklamlari/index.html", False, False),
        ("public/kota-roasist-local.html", "public/hizmetler/linkedin-reklamlari/index.html", False, False),
        ("public/en/index.html", "public/en/linkedin-ads/index.html", True, False),
        ("dist/index.html", "dist/hizmetler/performans-pazarlamasi/linkedin-reklamlari/index.html", False, True),
        ("dist/index.html", "dist/hizmetler/linkedin-reklamlari/index.html", False, True),
        ("dist/en/index.html", "dist/en/linkedin-ads/index.html", True, True),
    ]
    for home_rel, target_rel, is_en, is_gh in li_jobs:
        hs, tg = os.path.join(REPO_ROOT, home_rel), os.path.join(REPO_ROOT, target_rel)
        if os.path.exists(hs) and os.path.exists(tg):
            sync_stats(tg, get_homepage_statistics(hs), is_en=is_en, is_gh_pages=is_gh)
            update_process(tg, EN_STEPS if is_en else TR_STEPS, is_en=is_en, is_gh_pages=is_gh)
            update_channel_campaigns(tg, "li", EN_LINKEDIN_CAMPAIGNS if is_en else TR_LINKEDIN_CAMPAIGNS, LINKEDIN_STAGES, is_gh_pages=is_gh)

    # 2. Facebook Ads (uses Meta ODAX 6 campaigns + stages)
    fb_jobs = [
        ("public/kota-roasist-local.html", "public/hizmetler/performans-pazarlamasi/facebook-reklamlari/index.html", False, False),
        ("public/kota-roasist-local.html", "public/hizmetler/facebook-reklamlari/index.html", False, False),
        ("public/en/index.html", "public/en/facebook-ads/index.html", True, False),
        ("dist/index.html", "dist/hizmetler/performans-pazarlamasi/facebook-reklamlari/index.html", False, True),
        ("dist/index.html", "dist/hizmetler/facebook-reklamlari/index.html", False, True),
        ("dist/en/index.html", "dist/en/facebook-ads/index.html", True, True),
    ]
    for home_rel, target_rel, is_en, is_gh in fb_jobs:
        hs, tg = os.path.join(REPO_ROOT, home_rel), os.path.join(REPO_ROOT, target_rel)
        if os.path.exists(hs) and os.path.exists(tg):
            sync_stats(tg, get_homepage_statistics(hs), is_en=is_en, is_gh_pages=is_gh)
            update_process(tg, EN_STEPS if is_en else TR_STEPS, is_en=is_en, is_gh_pages=is_gh)
            update_meta_campaigns(tg, EN_META_CAMPAIGNS if is_en else TR_META_CAMPAIGNS, is_gh_pages=is_gh)

    # 3. Main Services Hub (/hizmetler/ & /en/services/)
    hub_jobs = [
        ("public/kota-roasist-local.html", "public/hizmetler/index.html", False, False),
        ("public/en/index.html", "public/en/services/index.html", True, False),
        ("dist/index.html", "dist/hizmetler/index.html", False, True),
        ("dist/en/index.html", "dist/en/services/index.html", True, True),
    ]
    for home_rel, target_rel, is_en, is_gh in hub_jobs:
        hs, tg = os.path.join(REPO_ROOT, home_rel), os.path.join(REPO_ROOT, target_rel)
        if os.path.exists(hs) and os.path.exists(tg):
            sync_stats(tg, get_homepage_statistics(hs), is_en=is_en, is_gh_pages=is_gh)
            update_process(tg, EN_STEPS if is_en else TR_STEPS, is_en=is_en, is_gh_pages=is_gh)
            update_services_hub_page(tg, EN_HUB_SERVICES if is_en else TR_HUB_SERVICES, HUB_STAGES, is_gh_pages=is_gh)


if __name__ == "__main__":
    main()
