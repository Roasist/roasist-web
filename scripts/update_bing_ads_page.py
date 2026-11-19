#!/usr/bin/env python3
"""
1. Adds the 'Bing Ads' tag under 'Performans Pazarlaması' / 'Performance Marketing'
   on the Homepage (TR & EN, in both public/ and dist/).
2. Upgrades all 3 Bing Ads detail pages (TR: /hizmetler/performans-pazarlamasi/bing-reklamlari/
   and /hizmetler/bing-reklamlari/, EN: /en/bing-ads/) in both public/ and dist/:
     - 5 official Microsoft Advertising (Bing Ads) campaign types with 5 bespoke
       white-stage SVG + CSS brand-motion animations (no 'Detaylı İncele' buttons).
     - Synced 5 Homepage 'ÖLÇÜLEBİLİR SONUÇLAR' / 'MEASURABLE RESULTS' dark cards + heading.
     - Upgraded 6-step 'Hizmet Sürecimiz' cards (zero duplicate sections).
"""
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
from update_tiktok_yandex_pages import update_channel_campaigns

# ---------------------------------------------------------------------------
# 5 Official Microsoft Advertising (Bing Ads) Campaign Types (TR & EN)
# ---------------------------------------------------------------------------

TR_BING_CAMPAIGNS = [
    {
        "title": "Microsoft Arama Ağı (Bing, Yahoo, DuckDuckGo)",
        "desc": "Masaüstü ve kurumsal aramalarda yüksek satın alma gücüne sahip kitlelere Bing, Yahoo ve DuckDuckGo arama sonuçlarında daha düşük tıklama maliyetleriyle (CPC) ulaşın.",
    },
    {
        "title": "Microsoft Audience Network (MSAN)",
        "desc": "MSN, Outlook, Microsoft Edge ve iş ortağı haber portallarında doğal (native) görsel reklamlarla marka bilinirliği ve yüksek dönüşümlü yeniden pazarlama yapın.",
    },
    {
        "title": "Alışveriş (Microsoft Shopping) & PMax",
        "desc": "Ürün kataloğunuzu Microsoft Merchant Center üzerinden zengin görsel ve fiyat kartlarıyla sergileyerek e-ticaret satışlarınızı ve ROAS performansınızı artırın.",
    },
    {
        "title": "LinkedIn Profil Tabanlı Kurumsal Hedefleme",
        "desc": "Yalnızca Microsoft Advertising'e özel LinkedIn entegrasyonu sayesinde arama reklamlarınızda şirket, sektör ve iş unvanı bazlı nokta atışı B2B hedefleme yapın.",
    },
    {
        "title": "Multimedya & Video Reklamları",
        "desc": "Arama sonuçlarının ana ve sağ sütununda dikkat çeken büyük görsel ve video reklam formatlarıyla rakiplerinizden ayrışarak tıklama oranınızı (CTR) yükseltin.",
    },
]

EN_BING_CAMPAIGNS = [
    {
        "title": "Microsoft Search Network (Bing, Yahoo, DuckDuckGo)",
        "desc": "Reach high-purchasing-power desktop and enterprise audiences across Bing, Yahoo, and DuckDuckGo with lower average CPCs and stronger ROI.",
    },
    {
        "title": "Microsoft Audience Network (MSAN)",
        "desc": "Engage decision-makers natively across MSN, Outlook, Microsoft Edge, and premium partner feeds with high-impact visual remarketing.",
    },
    {
        "title": "Microsoft Shopping & Performance Max",
        "desc": "Sync your Merchant Center catalog to showcase product imagery, pricing, and offers directly in Microsoft Search to scale e-commerce ROAS.",
    },
    {
        "title": "LinkedIn Profile Targeting for B2B",
        "desc": "Leverage Microsoft Advertising's exclusive LinkedIn integration to target search and native ads by company, industry, and job function.",
    },
    {
        "title": "Multimedia & Video Ads",
        "desc": "Stand out on the SERP with rich visual and video ad placements engineered to capture attention and elevate click-through rates.",
    },
]

# ---------------------------------------------------------------------------
# 5 Bespoke White-Stage Brand-Motion SVG Animations (Bing Teal #00809D / Azure #0078D4)
# ---------------------------------------------------------------------------

SVG_BING_SEARCH = """
<div class="roasist-brand-stage bg-sub-stage">
  <svg viewBox="0 0 600 320" class="sub-brand-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Microsoft Search Network">
    <defs><filter id="bgSh1" x="-15%" y="-15%" width="130%" height="140%"><feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#0F172A" flood-opacity="0.07"/></filter></defs>
    <g class="sub-p1-slide" filter="url(#bgSh1)">
      <rect x="132" y="76" width="336" height="52" rx="26" fill="#FFFFFF" stroke="#00809D" stroke-width="2"/>
      <circle cx="164" cy="102" r="9" fill="none" stroke="#00809D" stroke-width="2.6"/>
      <line x1="170.5" y1="108.5" x2="177" y2="115" stroke="#00809D" stroke-width="2.6" stroke-linecap="round"/>
      <rect x="190" y="97" width="168" height="10" rx="5" fill="#CBD5E1"/>
      <rect x="394" y="88" width="60" height="28" rx="14" fill="#0078D4"/>
      <rect x="132" y="146" width="336" height="96" rx="18" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <rect x="154" y="164" width="44" height="20" rx="6" fill="#E0F2FE"/>
      <text x="176" y="178" text-anchor="middle" fill="#0369A1" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="10.5">BING</text>
      <rect x="208" y="170" width="118" height="8" rx="4" fill="#E2E8F0"/>
      <rect x="154" y="194" width="218" height="12" rx="6" fill="#0078D4"/>
      <rect x="154" y="216" width="176" height="8" rx="4" fill="#CBD5E1"/>
      <rect x="398" y="182" width="52" height="24" rx="12" fill="#ECFDF5"/>
      <text x="424" y="198" text-anchor="middle" fill="#059669" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="10">-CPC</text>
    </g>
    <g class="sub-emblem-162">
      <path d="M276 116 L296 123 L296 176 L326 160 L314 154 L308 139 L336 149 L336 173 L296 196 L276 185 Z" fill="#00809D"/>
      <path d="M296 176 L336 149 L336 173 L296 196 Z" fill="#0078D4"/>
    </g>
    <g class="sub-wordmark"><text x="190" y="174" font-family="'Inter', Arial, sans-serif" font-size="36" font-weight="700" fill="#0F172A" letter-spacing="-0.8">Microsoft Search</text></g>
  </svg>
</div>
""".strip()

SVG_BING_MSAN = """
<div class="roasist-brand-stage bg-sub-stage">
  <svg viewBox="0 0 600 320" class="sub-brand-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Microsoft Audience Network">
    <defs><filter id="bgSh2" x="-15%" y="-15%" width="130%" height="140%"><feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#0F172A" flood-opacity="0.07"/></filter></defs>
    <g class="sub-p1-pop" filter="url(#bgSh2)">
      <rect x="136" y="76" width="328" height="58" rx="14" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <rect x="150" y="90" width="30" height="30" rx="8" fill="#0078D4"/>
      <rect x="194" y="95" width="132" height="9" rx="4.5" fill="#0F172A"/>
      <rect x="194" y="110" width="88" height="7" rx="3.5" fill="#CBD5E1"/>
      <rect x="394" y="92" width="56" height="26" rx="13" fill="#00809D"/>
      <rect x="136" y="148" width="154" height="96" rx="16" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <rect x="150" y="162" width="126" height="48" rx="10" fill="#E0F2FE"/>
      <circle cx="182" cy="186" r="12" fill="#0078D4"/>
      <rect x="150" y="220" width="84" height="8" rx="4" fill="#CBD5E1"/>
      <rect x="306" y="148" width="158" height="96" rx="16" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <rect x="320" y="162" width="130" height="48" rx="10" fill="#CCFBF1"/>
      <rect x="336" y="178" width="66" height="8" rx="4" fill="#00809D"/>
      <rect x="320" y="220" width="88" height="8" rx="4" fill="#CBD5E1"/>
    </g>
    <g class="sub-emblem-162">
      <rect x="260" y="122" width="80" height="76" rx="18" fill="#0078D4"/>
      <rect x="274" y="136" width="22" height="22" rx="6" fill="#FFFFFF"/>
      <rect x="304" y="136" width="22" height="22" rx="6" fill="#38BDF8"/>
      <rect x="274" y="166" width="52" height="18" rx="6" fill="#2DD4BF"/>
    </g>
    <g class="sub-wordmark"><text x="190" y="174" font-family="'Inter', Arial, sans-serif" font-size="35" font-weight="700" fill="#0F172A" letter-spacing="-0.8">Audience Network</text></g>
  </svg>
</div>
""".strip()

SVG_BING_SHOP = """
<div class="roasist-brand-stage bg-sub-stage">
  <svg viewBox="0 0 600 320" class="sub-brand-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Microsoft Shopping and PMax">
    <defs><filter id="bgSh3" x="-15%" y="-15%" width="130%" height="140%"><feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#0F172A" flood-opacity="0.07"/></filter></defs>
    <g class="sub-card-1" filter="url(#bgSh3)">
      <rect x="128" y="94" width="104" height="134" rx="16" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <rect x="142" y="108" width="76" height="62" rx="10" fill="#E0F2FE"/>
      <circle cx="180" cy="139" r="14" fill="#0078D4"/>
      <rect x="142" y="182" width="54" height="8" rx="4" fill="#CBD5E1"/>
      <rect x="142" y="198" width="48" height="18" rx="9" fill="#CCFBF1"/>
      <text x="166" y="211" text-anchor="middle" fill="#00809D" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="10">FEED</text>
    </g>
    <g class="sub-card-2" filter="url(#bgSh3)">
      <rect x="248" y="76" width="104" height="152" rx="18" fill="#FFFFFF" stroke="#00809D" stroke-width="1.8"/>
      <rect x="262" y="90" width="76" height="68" rx="10" fill="#CCFBF1"/>
      <path d="M285 112 h30 l4 28 h-38 z" fill="#00809D"/>
      <path d="M292 112 a8 8 0 0 1 16 0" fill="none" stroke="#00809D" stroke-width="2.8"/>
      <rect x="262" y="170" width="64" height="9" rx="4.5" fill="#0F172A"/>
      <rect x="262" y="186" width="46" height="7" rx="3.5" fill="#CBD5E1"/>
      <rect x="262" y="200" width="62" height="18" rx="9" fill="#0078D4"/>
      <text x="293" y="213" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="10">ROAS ↑</text>
    </g>
    <g class="sub-card-3" filter="url(#bgSh3)">
      <rect x="368" y="94" width="104" height="134" rx="16" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <rect x="382" y="108" width="76" height="62" rx="10" fill="#F1F5F9"/>
      <rect x="406" y="125" width="28" height="28" rx="8" fill="#0F172A"/>
      <rect x="382" y="182" width="56" height="8" rx="4" fill="#CBD5E1"/>
      <rect x="382" y="198" width="48" height="18" rx="9" fill="#E0F2FE"/>
      <text x="406" y="211" text-anchor="middle" fill="#0078D4" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="10">PMax</text>
    </g>
    <g class="sub-emblem-162">
      <rect x="262" y="122" width="76" height="76" rx="22" fill="#00809D"/>
      <path d="M284 148 h32 l4 32 h-40 z" fill="#FFFFFF"/>
      <path d="M291 148 a9 9 0 0 1 18 0" fill="none" stroke="#FFFFFF" stroke-width="3.2"/>
    </g>
    <g class="sub-wordmark"><text x="196" y="174" font-family="'Inter', Arial, sans-serif" font-size="36" font-weight="700" fill="#0F172A" letter-spacing="-0.8">Shopping &amp; PMax</text></g>
  </svg>
</div>
""".strip()

SVG_BING_B2B = """
<div class="roasist-brand-stage bg-sub-stage">
  <svg viewBox="0 0 600 320" class="sub-brand-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="LinkedIn Profile Targeting on Bing">
    <g class="sub-p1-pop">
      <line x1="300" y1="100" x2="236" y2="164" stroke="#93C5FD" stroke-width="2.5"/>
      <line x1="300" y1="100" x2="364" y2="164" stroke="#93C5FD" stroke-width="2.5"/>
      <line x1="236" y1="164" x2="196" y2="220" stroke="#CBD5E1" stroke-width="2"/>
      <line x1="236" y1="164" x2="276" y2="220" stroke="#CBD5E1" stroke-width="2"/>
      <line x1="364" y1="164" x2="324" y2="220" stroke="#CBD5E1" stroke-width="2"/>
      <line x1="364" y1="164" x2="404" y2="220" stroke="#CBD5E1" stroke-width="2"/>
      <circle cx="196" cy="220" r="11" fill="#E2E8F0"/>
      <circle cx="276" cy="220" r="11" fill="#E2E8F0"/>
      <circle cx="324" cy="220" r="11" fill="#E2E8F0"/>
      <circle cx="404" cy="220" r="11" fill="#E2E8F0"/>
      <circle cx="236" cy="164" r="16" fill="#00809D"/>
      <circle cx="364" cy="164" r="16" fill="#0078D4"/>
      <circle cx="300" cy="100" r="24" fill="#0A66C2"/>
      <circle cx="300" cy="94" r="6" fill="#FFFFFF"/>
      <path d="M289 109 c0-5 5-8 11-8 s11 3 11 8" fill="#FFFFFF"/>
    </g>
    <g class="sub-emblem-152">
      <rect x="262" y="122" width="76" height="76" rx="20" fill="#0A66C2"/>
      <circle cx="300" cy="148" r="10" fill="#FFFFFF"/>
      <path d="M282 178 c0-9 8-14 18-14 s18 5 18 14" fill="#FFFFFF"/>
    </g>
    <g class="sub-wordmark"><text x="206" y="174" font-family="'Inter', Arial, sans-serif" font-size="38" font-weight="700" fill="#0F172A" letter-spacing="-0.8">B2B Targeting</text></g>
  </svg>
</div>
""".strip()

SVG_BING_MEDIA = """
<div class="roasist-brand-stage bg-sub-stage">
  <svg viewBox="0 0 600 320" class="sub-brand-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Microsoft Multimedia Ads">
    <defs><filter id="bgSh5" x="-15%" y="-15%" width="130%" height="140%"><feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#0F172A" flood-opacity="0.09"/></filter></defs>
    <g class="sub-p1-slide" filter="url(#bgSh5)">
      <rect x="136" y="76" width="328" height="174" rx="20" fill="#0F172A"/>
      <rect x="148" y="88" width="204" height="128" rx="12" fill="#1E293B"/>
      <rect x="224" y="132" width="52" height="38" rx="11" fill="#00809D"/>
      <polygon points="245,143 245,159 259,151" fill="#FFFFFF"/>
      <rect x="364" y="88" width="88" height="58" rx="10" fill="#0078D4" opacity="0.85"/>
      <rect x="364" y="156" width="88" height="60" rx="10" fill="#2DD4BF" opacity="0.85"/>
      <rect x="156" y="230" width="288" height="6" rx="3" fill="#334155"/>
      <rect x="156" y="230" width="186" height="6" rx="3" fill="#00809D"/>
    </g>
    <g class="sub-emblem-162">
      <rect x="256" y="124" width="88" height="72" rx="18" fill="#0078D4"/>
      <polygon points="290,144 290,176 318,160" fill="#FFFFFF"/>
    </g>
    <g class="sub-wordmark"><text x="194" y="174" font-family="'Inter', Arial, sans-serif" font-size="36" font-weight="700" fill="#0F172A" letter-spacing="-0.8">Multimedia Ads</text></g>
  </svg>
</div>
""".strip()

BING_STAGES = [SVG_BING_SEARCH, SVG_BING_MSAN, SVG_BING_SHOP, SVG_BING_B2B, SVG_BING_MEDIA]


def add_bing_tag_to_homepage(home_path, is_en=False):
    text = open(home_path, "r", encoding="utf-8").read()
    changed = False

    if is_en:
        ssr_anchor = '<a class="ServicesPanel_tag__JYwRk" href="service/yandex-ads">Yandex Ads</a>'
        ssr_add = '<a class="ServicesPanel_tag__JYwRk" href="service/bing-ads">Bing Ads</a>'
        if ssr_add not in text and ssr_anchor in text:
            text = text.replace(ssr_anchor, ssr_anchor + ssr_add, 1)
            changed = True

        # Flight stream tag array (escaped JSON inside script)
        fl_anchor = '\\"slug\\":\\"yandex-ads\\",\\"title\\":\\"Yandex Ads\\"}'
        fl_add = ',{\\"id\\":\\"cG9zdDo4ODg=\\",\\"slug\\":\\"bing-ads\\",\\"title\\":\\"Bing Ads\\"}'
        if '\\"slug\\":\\"bing-ads\\"' not in text and fl_anchor in text:
            text = text.replace(fl_anchor, fl_anchor + fl_add, 1)
            changed = True
    else:
        ssr_anchor = '<a class="ServicesPanel_tag__JYwRk" href="service/yandex-reklamlari">Yandex Ads</a>'
        ssr_add = '<a class="ServicesPanel_tag__JYwRk" href="service/bing-reklamlari">Bing Ads</a>'
        if ssr_add not in text and ssr_anchor in text:
            text = text.replace(ssr_anchor, ssr_anchor + ssr_add, 1)
            changed = True

        fl_anchor = '\\"slug\\":\\"yandex-reklamlari\\",\\"title\\":\\"Yandex Ads\\"}'
        fl_add = ',{\\"id\\":\\"cG9zdDo4ODg=\\",\\"slug\\":\\"bing-reklamlari\\",\\"title\\":\\"Bing Ads\\"}'
        if '\\"slug\\":\\"bing-reklamlari\\"' not in text and fl_anchor in text:
            text = text.replace(fl_anchor, fl_anchor + fl_add, 1)
            changed = True

    if changed:
        with open(home_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"[OK] Added 'Bing Ads' tag under Performans Pazarlaması in {os.path.relpath(home_path, REPO_ROOT)}")
    else:
        print(f"[OK] 'Bing Ads' tag already present in {os.path.relpath(home_path, REPO_ROOT)}")


def main():
    # 1. Add 'Bing Ads' tag under Performans Pazarlaması on Homepages (TR & EN, public + dist)
    for rel, is_en in [
        ("public/kota-roasist-local.html", False),
        ("public/en/index.html", True),
        ("dist/index.html", False),
        ("dist/en/index.html", True),
    ]:
        p = os.path.join(REPO_ROOT, rel)
        if os.path.exists(p):
            add_bing_tag_to_homepage(p, is_en=is_en)

    # 2. Upgrade all 3 Bing Ads detail pages (public + dist)
    jobs = [
        ("public/kota-roasist-local.html", "public/hizmetler/performans-pazarlamasi/bing-reklamlari/index.html", False, False),
        ("public/kota-roasist-local.html", "public/hizmetler/bing-reklamlari/index.html", False, False),
        ("public/en/index.html", "public/en/bing-ads/index.html", True, False),
        ("dist/index.html", "dist/hizmetler/performans-pazarlamasi/bing-reklamlari/index.html", False, True),
        ("dist/index.html", "dist/hizmetler/bing-reklamlari/index.html", False, True),
        ("dist/en/index.html", "dist/en/bing-ads/index.html", True, True),
    ]
    for home_rel, target_rel, is_en, is_gh in jobs:
        home_src = os.path.join(REPO_ROOT, home_rel)
        target = os.path.join(REPO_ROOT, target_rel)
        if not os.path.exists(home_src) or not os.path.exists(target):
            print(f"[SKIP] Missing {target_rel} or {home_rel}")
            continue
        stats = get_homepage_statistics(home_src)
        sync_stats(target, stats, is_en=is_en, is_gh_pages=is_gh)
        update_process(target, EN_STEPS if is_en else TR_STEPS, is_en=is_en, is_gh_pages=is_gh)
        update_channel_campaigns(target, "bg", EN_BING_CAMPAIGNS if is_en else TR_BING_CAMPAIGNS, BING_STAGES, is_gh_pages=is_gh)


if __name__ == "__main__":
    main()
