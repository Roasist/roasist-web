#!/usr/bin/env python3
"""
Upgrades all Google Ads detail pages (TR: /hizmetler/performans-pazarlamasi/google-reklamlari/
and /hizmetler/google-reklamlari/, EN: /en/google-ads/) in both public/ and dist/:

  1. Builds all 7 official Google Ads campaign types (Search, Performance Max, Demand Gen,
     Display, Shopping, Video, App) in TextImageRows_textImageRows__lOU02 (SSR + Flight),
     with NO 'Detaylı İncele' buttons under the campaign cards.
  2. Injects 7 bespoke, lightweight white-stage SVG + CSS brand-motion animations matching
     the Performance Marketing page style.
  3. Syncs the 5 Homepage 'ÖLÇÜLEBİLİR SONUÇLAR' / 'MEASURABLE RESULTS' dark case-study
     cards + heading + Turkish diacritic top-clearance fix.
  4. Upgrades 'Hizmet Sürecimiz' (Timeline_timeline__KvsOC) to the elevated 6-step
     architectural white card design (with balanced <div> tags so zero sections duplicate).
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

STYLE_ID = "roasist-gads-brand-stages-css"
SCRIPT_ID = "roasist-gads-brand-stages-js"

# ---------------------------------------------------------------------------
# 7 Official Google Ads Campaign Types (TR & EN) — NO 'Detaylı İncele' button
# ---------------------------------------------------------------------------

TR_CAMPAIGNS = [
    {
        "title": "Arama Ağı (Search) Kampanyaları",
        "desc": "Google arama sonuçları sayfalarında (SERP) ürün veya hizmetinizle ilgili yüksek satın alma niyetli anahtar kelimelerde en üst sırada yer alın.",
    },
    {
        "title": "Performance Max (PMax) Kampanyaları",
        "desc": "Google Arama, YouTube, Alışveriş, Keşfet, Gmail ve Haritalar envanterinin tamamında yapay zeka destekli teklif optimizasyonuyla doğru müşteriye doğru anda ulaşın.",
    },
    {
        "title": "Talep Oluşturma (Demand Gen) Kampanyaları",
        "desc": "YouTube, Shorts, Keşfet ve Gmail akışlarında dikkat çekici görsel ve video reklamlarla yeni talep oluşturun, markanız için yüksek nitelikli dönüşümler üretin.",
    },
    {
        "title": "Görüntülü Reklam Ağı (Display) Kampanyaları",
        "desc": "3 milyondan fazla haber sitesi, blog ve mobil uygulamada yaratıcı banner reklamlarınızla marka bilinirliği ve etkili yeniden pazarlama (remarketing) yapın.",
    },
    {
        "title": "Alışveriş (Shopping) Kampanyaları",
        "desc": "Google Merchant Center ürün kataloğunuzu doğrudan arama sonuçlarında ürün fotoğrafı, güncel fiyat ve mağaza adıyla sergileyerek e-ticaret satışlarınızı artırın.",
    },
    {
        "title": "YouTube Video Kampanyaları",
        "desc": "Dünyanın en büyük video platformunda hedef kitlenize ilgi alanlarına ve arama niyetlerine göre kurgulanmış performans odaklı video reklamlarla ulaşın.",
    },
    {
        "title": "Uygulama (App) Kampanyaları",
        "desc": "Android ve iOS mobil uygulamalarınızı Google Arama, Google Play, YouTube ve iş ortağı ağlarında tanıtarak düşük maliyetle yüksek kaliteli indirme ve uygulama içi aksiyon kazanın.",
    },
]

EN_CAMPAIGNS = [
    {
        "title": "Search Campaigns",
        "desc": "Capture high-intent demand at the exact moment buyers search for your products or services on Google Search with precision keyword and bidding strategies.",
    },
    {
        "title": "Performance Max Campaigns",
        "desc": "Reach the right customers wherever they browse across Search, YouTube, Shopping, Discover, Gmail, and Maps with unified AI-powered optimization.",
    },
    {
        "title": "Demand Gen Campaigns",
        "desc": "Spark new demand and drive conversions across YouTube, Shorts, Discover, and Gmail with high-impact image and video storytelling.",
    },
    {
        "title": "Display Campaigns",
        "desc": "Build awareness and run precision remarketing across 3+ million websites and mobile apps with responsive visual banner creatives.",
    },
    {
        "title": "Shopping Campaigns",
        "desc": "Showcase your Merchant Center product catalog directly in Google Search with rich imagery, live pricing, and store details to scale e-commerce ROAS.",
    },
    {
        "title": "Video Campaigns",
        "desc": "Drive measurable action and brand lift on YouTube with audience-targeted, conversion-engineered video ads.",
    },
    {
        "title": "App Campaigns",
        "desc": "Promote your Android or iOS app across Google Search, Google Play, YouTube, and partner networks to scale profitable installs and in-app events.",
    },
]

# ---------------------------------------------------------------------------
# 7 Bespoke White-Stage Brand-Motion SVG + CSS Animations
# ---------------------------------------------------------------------------

SVG_SEARCH = """
<div class="roasist-brand-stage gads-sub-stage">
  <svg viewBox="0 0 600 320" class="gads-sub-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Google Search Ads">
    <defs>
      <filter id="gsSh" x="-15%" y="-15%" width="130%" height="140%">
        <feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#0F172A" flood-opacity="0.07"/>
      </filter>
    </defs>
    <!-- Phase 1: Search Bar + Top Sponsored Ad Result -->
    <g class="gs-searchbar" filter="url(#gsSh)">
      <rect x="132" y="76" width="336" height="52" rx="26" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <circle cx="164" cy="102" r="9" fill="none" stroke="#4285F4" stroke-width="2.6"/>
      <line x1="170.5" y1="108.5" x2="177" y2="115" stroke="#4285F4" stroke-width="2.6" stroke-linecap="round"/>
      <rect x="190" y="97" width="168" height="10" rx="5" fill="#CBD5E1" class="gs-query-bar"/>
      <rect x="364" y="91" width="2.5" height="22" rx="1.25" fill="#4285F4" class="gs-cursor"/>
      <circle cx="426" cy="102" r="4" fill="#4285F4"/>
      <circle cx="438" cy="102" r="4" fill="#EA4335"/>
      <circle cx="450" cy="102" r="4" fill="#FBBC05"/>
    </g>
    <g class="gs-adcard" filter="url(#gsSh)">
      <rect x="132" y="146" width="336" height="96" rx="18" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <rect x="154" y="164" width="38" height="20" rx="6" fill="#E6F4EA"/>
      <text x="173" y="178" text-anchor="middle" fill="#1E8E3E" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="11">Ad</text>
      <rect x="202" y="170" width="112" height="8" rx="4" fill="#E2E8F0"/>
      <rect x="154" y="194" width="218" height="12" rx="6" fill="#4285F4"/>
      <rect x="154" y="216" width="176" height="8" rx="4" fill="#CBD5E1"/>
      <circle cx="430" cy="194" r="20" fill="#34A853"/>
      <path d="M421 194 L427.5 200.5 L440 187.5" fill="none" stroke="#FFFFFF" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>
      <circle cx="430" cy="194" r="20" fill="none" stroke="#34A853" stroke-width="2" class="gs-ripple"/>
    </g>
    <!-- Phase 2: 4-Color Search Emblem + Wordmark -->
    <g class="gs-emblem">
      <path d="M300 108 A38 38 0 0 1 338 146" fill="none" stroke="#4285F4" stroke-width="13" stroke-linecap="round"/>
      <path d="M338 146 A38 38 0 0 1 300 184" fill="none" stroke="#34A853" stroke-width="13" stroke-linecap="round"/>
      <path d="M300 184 A38 38 0 0 1 262 146" fill="none" stroke="#FBBC05" stroke-width="13" stroke-linecap="round"/>
      <path d="M262 146 A38 38 0 0 1 300 108" fill="none" stroke="#EA4335" stroke-width="13" stroke-linecap="round"/>
      <line x1="328" y1="174" x2="354" y2="200" stroke="#4285F4" stroke-width="14" stroke-linecap="round"/>
    </g>
    <g class="gs-wordmark">
      <text x="228" y="174" font-family="'Product Sans', 'Inter', Arial, sans-serif" font-size="42" font-weight="600" fill="#202124" letter-spacing="-0.8">Search Ads</text>
    </g>
  </svg>
</div>
""".strip()

SVG_PMAX = """
<div class="roasist-brand-stage gads-sub-stage">
  <svg viewBox="0 0 600 320" class="gads-sub-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Google Performance Max">
    <!-- Phase 1: 6 Google Ecosystem Channels Converging into Central AI Core -->
    <g class="pm-orbit">
      <circle cx="300" cy="160" r="90" fill="none" stroke="#E2E8F0" stroke-width="1.5" stroke-dasharray="5 6"/>
      <line x1="300" y1="160" x2="300" y2="70"  stroke="#4285F4" stroke-width="1.6" opacity="0.45"/>
      <line x1="300" y1="160" x2="378" y2="115" stroke="#EA4335" stroke-width="1.6" opacity="0.45"/>
      <line x1="300" y1="160" x2="378" y2="205" stroke="#FBBC05" stroke-width="1.6" opacity="0.45"/>
      <line x1="300" y1="160" x2="300" y2="250" stroke="#34A853" stroke-width="1.6" opacity="0.45"/>
      <line x1="300" y1="160" x2="222" y2="205" stroke="#4285F4" stroke-width="1.6" opacity="0.45"/>
      <line x1="300" y1="160" x2="222" y2="115" stroke="#EA4335" stroke-width="1.6" opacity="0.45"/>
      <!-- 6 Channel Nodes (Search, YouTube, Gmail, Maps, Discover, Display) -->
      <circle cx="300" cy="70"  r="16" fill="#4285F4"/>
      <circle cx="300" cy="70"  r="6"  fill="#FFFFFF"/>
      <circle cx="378" cy="115" r="16" fill="#EA4335"/>
      <polygon points="375,109 375,121 385,115" fill="#FFFFFF"/>
      <circle cx="378" cy="205" r="16" fill="#FBBC05"/>
      <rect x="370" y="199" width="16" height="12" rx="2.5" fill="#FFFFFF"/>
      <circle cx="300" cy="250" r="16" fill="#34A853"/>
      <circle cx="300" cy="248" r="5.5" fill="#FFFFFF"/>
      <circle cx="222" cy="205" r="16" fill="#4285F4"/>
      <rect x="214" y="199" width="16" height="12" rx="2.5" fill="#FFFFFF"/>
      <circle cx="222" cy="115" r="16" fill="#EA4335"/>
      <path d="M222 108 l2.2 4.8 l4.8 2.2 l-4.8 2.2 l-2.2 4.8 l-2.2 -4.8 l-4.8 -2.2 l4.8 -2.2 z" fill="#FFFFFF"/>
      <!-- Center Core Pulse -->
      <circle cx="300" cy="160" r="28" fill="#0F172A"/>
      <path d="M300 144 l4 12 l12 4 l-12 4 l-4 12 l-4 -12 l-12 -4 l12 -4 z" fill="#FFFFFF"/>
    </g>
    <!-- Phase 2: 4-Color PMax Spark Emblem + Wordmark -->
    <g class="pm-emblem">
      <path d="M300 108 L314 146 L300 160 L286 146 Z" fill="#4285F4"/>
      <path d="M352 160 L314 174 L300 160 L314 146 Z" fill="#EA4335"/>
      <path d="M300 212 L286 174 L300 160 L314 174 Z" fill="#34A853"/>
      <path d="M248 160 L286 146 L300 160 L286 174 Z" fill="#FBBC05"/>
      <circle cx="300" cy="160" r="11" fill="#FFFFFF"/>
    </g>
    <g class="pm-wordmark">
      <text x="194" y="173" font-family="'Product Sans', 'Inter', Arial, sans-serif" font-size="38" font-weight="600" fill="#202124" letter-spacing="-0.8">Performance Max</text>
    </g>
  </svg>
</div>
""".strip()

SVG_DEMAND_GEN = """
<div class="roasist-brand-stage gads-sub-stage">
  <svg viewBox="0 0 600 320" class="gads-sub-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Google Demand Gen">
    <defs>
      <filter id="dgSh" x="-15%" y="-15%" width="130%" height="140%">
        <feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#0F172A" flood-opacity="0.08"/>
      </filter>
    </defs>
    <!-- Phase 1: Visual Social Feed Cards (Shorts + Discover + Gmail) -->
    <g class="dg-card-1" filter="url(#dgSh)">
      <rect x="136" y="96" width="96" height="132" rx="16" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <rect x="148" y="108" width="72" height="84" rx="10" fill="#FEE2E2"/>
      <polygon points="178,139 178,161 196,150" fill="#EA4335"/>
      <rect x="148" y="202" width="52" height="8" rx="4" fill="#CBD5E1"/>
    </g>
    <g class="dg-card-2" filter="url(#dgSh)">
      <rect x="246" y="76" width="108" height="156" rx="18" fill="#FFFFFF" stroke="#4285F4" stroke-width="1.8"/>
      <rect x="258" y="88" width="84" height="92" rx="12" fill="#EFF6FF"/>
      <circle cx="300" cy="134" r="22" fill="#4285F4"/>
      <path d="M300 122 l3.5 8.5 l8.5 3.5 l-8.5 3.5 l-3.5 8.5 l-3.5 -8.5 l-8.5 -3.5 l8.5 -3.5 z" fill="#FFFFFF"/>
      <rect x="258" y="192" width="68" height="9" rx="4.5" fill="#1E293B"/>
      <rect x="258" y="208" width="48" height="8" rx="4" fill="#34A853"/>
    </g>
    <g class="dg-card-3" filter="url(#dgSh)">
      <rect x="368" y="96" width="96" height="132" rx="16" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <rect x="380" y="108" width="72" height="84" rx="10" fill="#FEF3C7"/>
      <rect x="396" y="136" width="40" height="28" rx="6" fill="#FBBC05"/>
      <path d="M398 139 L416 152 L434 139" fill="none" stroke="#FFFFFF" stroke-width="2.6" stroke-linecap="round"/>
      <rect x="380" y="202" width="56" height="8" rx="4" fill="#CBD5E1"/>
    </g>
    <!-- Phase 2: Demand Gen Signal Wave Emblem + Wordmark -->
    <g class="dg-emblem">
      <circle cx="278" cy="160" r="14" fill="#EA4335"/>
      <path d="M300 132 A34 34 0 0 1 300 188" fill="none" stroke="#FBBC05" stroke-width="11" stroke-linecap="round"/>
      <path d="M320 116 A54 54 0 0 1 320 204" fill="none" stroke="#4285F4" stroke-width="11" stroke-linecap="round"/>
      <circle cx="342" cy="160" r="9" fill="#34A853"/>
    </g>
    <g class="dg-wordmark">
      <text x="218" y="173" font-family="'Product Sans', 'Inter', Arial, sans-serif" font-size="40" font-weight="600" fill="#202124" letter-spacing="-0.8">Demand Gen</text>
    </g>
  </svg>
</div>
""".strip()

SVG_DISPLAY = """
<div class="roasist-brand-stage gads-sub-stage">
  <svg viewBox="0 0 600 320" class="gads-sub-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Google Display Ads">
    <defs>
      <filter id="gdSh" x="-15%" y="-15%" width="130%" height="140%">
        <feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#0F172A" flood-opacity="0.07"/>
      </filter>
    </defs>
    <!-- Phase 1: Responsive Banner Grid (Leaderboard + Visual Square + Mobile Card) -->
    <g class="gd-tile-1" filter="url(#gdSh)">
      <rect x="136" y="76" width="328" height="58" rx="14" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <rect x="150" y="90" width="30" height="30" rx="8" fill="#4285F4"/>
      <circle cx="165" cy="105" r="7" fill="#FFFFFF" opacity="0.9"/>
      <rect x="194" y="95" width="132" height="9" rx="4.5" fill="#1E293B"/>
      <rect x="194" y="110" width="88" height="7" rx="3.5" fill="#CBD5E1"/>
      <rect x="394" y="92" width="56" height="26" rx="13" fill="#4285F4"/>
    </g>
    <g class="gd-tile-2" filter="url(#gdSh)">
      <rect x="136" y="148" width="152" height="98" rx="16" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <rect x="150" y="162" width="124" height="50" rx="10" fill="#FEF3C7"/>
      <circle cx="176" cy="182" r="9" fill="#FBBC05"/>
      <path d="M158 212 L196 184 L222 204 L244 188 L266 212 Z" fill="#34A853" opacity="0.85"/>
      <rect x="150" y="222" width="80" height="8" rx="4" fill="#CBD5E1"/>
    </g>
    <g class="gd-tile-3" filter="url(#gdSh)">
      <rect x="304" y="148" width="160" height="98" rx="16" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <rect x="318" y="162" width="132" height="44" rx="10" fill="#DBEAFE"/>
      <rect x="334" y="176" width="66" height="8" rx="4" fill="#4285F4"/>
      <rect x="334" y="190" width="44" height="6" rx="3" fill="#93C5FD"/>
      <rect x="318" y="216" width="86" height="16" rx="8" fill="#34A853"/>
    </g>
    <!-- Phase 2: Layered Display Banner Emblem + Wordmark -->
    <g class="gd-emblem">
      <rect x="256" y="114" width="86" height="62" rx="14" fill="#FBBC05" transform="rotate(-7 299 145)"/>
      <rect x="264" y="124" width="86" height="62" rx="14" fill="#4285F4"/>
      <circle cx="290" cy="146" r="8" fill="#FFFFFF"/>
      <path d="M276 176 L302 152 L322 168 L338 156 L342 176 Z" fill="#34A853"/>
    </g>
    <g class="gd-wordmark">
      <text x="226" y="173" font-family="'Product Sans', 'Inter', Arial, sans-serif" font-size="40" font-weight="600" fill="#202124" letter-spacing="-0.8">Display Ads</text>
    </g>
  </svg>
</div>
""".strip()

SVG_SHOPPING = """
<div class="roasist-brand-stage gads-sub-stage">
  <svg viewBox="0 0 600 320" class="gads-sub-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Google Shopping Ads">
    <defs>
      <filter id="shSh" x="-15%" y="-15%" width="130%" height="140%">
        <feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#0F172A" flood-opacity="0.07"/>
      </filter>
    </defs>
    <!-- Phase 1: 3 Merchant Center Product Cards Fanning Upward -->
    <g class="sh-card-1" filter="url(#shSh)">
      <rect x="128" y="92" width="104" height="136" rx="16" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <rect x="142" y="106" width="76" height="62" rx="10" fill="#EFF6FF"/>
      <path d="M167 129 h26 l3 26 h-32 z" fill="#4285F4"/>
      <path d="M173 129 a7 7 0 0 1 14 0" fill="none" stroke="#4285F4" stroke-width="2.5"/>
      <rect x="142" y="180" width="52" height="8" rx="4" fill="#CBD5E1"/>
      <rect x="142" y="196" width="44" height="18" rx="9" fill="#E6F4EA"/>
      <text x="164" y="209" text-anchor="middle" fill="#1E8E3E" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="11">4.9 ★</text>
    </g>
    <g class="sh-card-2" filter="url(#shSh)">
      <rect x="248" y="76" width="104" height="152" rx="16" fill="#FFFFFF" stroke="#4285F4" stroke-width="1.8"/>
      <rect x="262" y="90" width="76" height="68" rx="10" fill="#FEF3C7"/>
      <path d="M284 110 h18 l14 14 l-18 18 l-14 -14 z" fill="#FBBC05"/>
      <circle cx="292" cy="118" r="3" fill="#FFFFFF"/>
      <rect x="262" y="170" width="64" height="9" rx="4.5" fill="#1E293B"/>
      <rect x="262" y="186" width="46" height="7" rx="3.5" fill="#CBD5E1"/>
      <rect x="262" y="200" width="56" height="18" rx="9" fill="#34A853"/>
      <text x="290" y="213" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="10.5">ROAS ↑</text>
    </g>
    <g class="sh-card-3" filter="url(#shSh)">
      <rect x="368" y="92" width="104" height="136" rx="16" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <rect x="382" y="106" width="76" height="62" rx="10" fill="#FEE2E2"/>
      <circle cx="420" cy="137" r="14" fill="#EA4335"/>
      <text x="420" y="142" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="14">%</text>
      <rect x="382" y="180" width="58" height="8" rx="4" fill="#CBD5E1"/>
      <rect x="382" y="196" width="48" height="18" rx="9" fill="#DBEAFE"/>
      <text x="406" y="209" text-anchor="middle" fill="#1D4ED8" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="10.5">Feed</text>
    </g>
    <!-- Phase 2: 4-Color Google Shopping Price Tag + Wordmark -->
    <g class="sh-emblem">
      <path d="M264 114 L306 114 L348 156 L306 198 L264 156 Z" fill="#4285F4"/>
      <path d="M264 114 L306 114 L306 156 L264 156 Z" fill="#34A853" opacity="0.92"/>
      <path d="M306 114 L348 156 L306 156 Z" fill="#FBBC05"/>
      <path d="M264 156 L306 156 L306 198 Z" fill="#EA4335"/>
      <circle cx="282" cy="132" r="7" fill="#FFFFFF"/>
    </g>
    <g class="sh-wordmark">
      <text x="214" y="173" font-family="'Product Sans', 'Inter', Arial, sans-serif" font-size="40" font-weight="600" fill="#202124" letter-spacing="-0.8">Shopping Ads</text>
    </g>
  </svg>
</div>
""".strip()

SVG_VIDEO = """
<div class="roasist-brand-stage gads-sub-stage">
  <svg viewBox="0 0 600 320" class="gads-sub-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="YouTube Video Ads">
    <defs>
      <filter id="vdSh" x="-15%" y="-15%" width="130%" height="140%">
        <feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#0F172A" flood-opacity="0.09"/>
      </filter>
    </defs>
    <!-- Phase 1: Widescreen YouTube Video Player + Animated Progress Bar -->
    <g class="vd-player" filter="url(#vdSh)">
      <rect x="136" y="76" width="328" height="174" rx="20" fill="#0F172A"/>
      <!-- Soft inner video frame -->
      <rect x="148" y="88" width="304" height="128" rx="12" fill="#1E293B"/>
      <!-- Play button center -->
      <rect x="272" y="132" width="56" height="40" rx="12" fill="#EA4335"/>
      <polygon points="295,143 295,161 311,152" fill="#FFFFFF"/>
      <!-- Ad badge top-left -->
      <rect x="160" y="100" width="34" height="18" rx="5" fill="#FBBC05"/>
      <text x="177" y="113" text-anchor="middle" fill="#0F172A" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="10">Ad</text>
      <!-- Progress track & animated red fill -->
      <rect x="156" y="230" width="288" height="6" rx="3" fill="#334155"/>
      <rect x="156" y="230" width="288" height="6" rx="3" fill="#EA4335" class="vd-progress"/>
    </g>
    <!-- Phase 2: Official Red YouTube Play Badge + Wordmark -->
    <g class="vd-emblem">
      <rect x="248" y="122" width="104" height="74" rx="22" fill="#EA4335"/>
      <polygon points="290,143 290,175 318,159" fill="#FFFFFF"/>
    </g>
    <g class="vd-wordmark">
      <text x="234" y="173" font-family="'Product Sans', 'Inter', Arial, sans-serif" font-size="42" font-weight="600" fill="#202124" letter-spacing="-0.8">Video Ads</text>
    </g>
  </svg>
</div>
""".strip()

SVG_APP = """
<div class="roasist-brand-stage gads-sub-stage">
  <svg viewBox="0 0 600 320" class="gads-sub-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Google App Ads">
    <defs>
      <filter id="apSh" x="-15%" y="-15%" width="130%" height="140%">
        <feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#0F172A" flood-opacity="0.08"/>
      </filter>
    </defs>
    <!-- Phase 1: Clean Smartphone App Store Listing + Install Pulse -->
    <g class="ap-phone" filter="url(#apSh)">
      <rect x="234" y="56" width="132" height="208" rx="24" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="2"/>
      <rect x="282" y="66" width="36" height="5" rx="2.5" fill="#E2E8F0"/>
      <!-- App Icon Tiles -->
      <rect x="252" y="86" width="42" height="42" rx="11" fill="#4285F4"/>
      <path d="M273 98 l6 18 l-12 0 z" fill="#FFFFFF"/>
      <rect x="304" y="92" width="44" height="9" rx="4.5" fill="#1E293B"/>
      <rect x="304" y="108" width="34" height="7" rx="3.5" fill="#FBBC05"/>
      <!-- App Screenshots Strip -->
      <rect x="252" y="142" width="44" height="56" rx="8" fill="#EFF6FF"/>
      <rect x="304" y="142" width="44" height="56" rx="8" fill="#ECFDF5"/>
      <!-- Install Pill Button -->
      <rect x="252" y="212" width="96" height="28" rx="14" fill="#34A853"/>
      <text x="300" y="230" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="12">INSTALL</text>
    </g>
    <!-- Phase 2: 4-Color Google Play Prism Emblem + Wordmark -->
    <g class="ap-emblem">
      <polygon points="266,112 314,160 266,208" fill="#4285F4"/>
      <polygon points="266,112 332,148 314,160" fill="#34A853"/>
      <polygon points="266,208 332,172 314,160" fill="#EA4335"/>
      <polygon points="332,148 352,160 332,172 314,160" fill="#FBBC05"/>
    </g>
    <g class="ap-wordmark">
      <text x="240" y="173" font-family="'Product Sans', 'Inter', Arial, sans-serif" font-size="42" font-weight="600" fill="#202124" letter-spacing="-0.8">App Ads</text>
    </g>
  </svg>
</div>
""".strip()

GADS_STAGES_CSS = f"""<style id="{STYLE_ID}">
/* Bespoke White-Stage Brand-Motion SVG Animations for Google Ads Sub-Page (7 Campaign Types) */
.TextImageRows_media__twu3R {{
  background: #FFFFFF !important;
  box-shadow: 0 20px 56px -24px rgba(15, 23, 42, 0.14) !important;
  border: 1px solid rgba(15, 23, 42, 0.06) !important;
}}
.TextImageRows_row__PPlpB:nth-child(odd) .TextImageRows_media__twu3R,
.TextImageRows_row__PPlpB:nth-child(odd) .roasist-brand-stage {{
  border-radius: 20px 80px 20px 20px !important;
}}
.TextImageRows_row__PPlpB:nth-child(2n) .TextImageRows_media__twu3R,
.TextImageRows_row__PPlpB:nth-child(2n) .roasist-brand-stage {{
  border-radius: 80px 20px 20px 20px !important;
}}
@media (min-width: 850px) {{
  .TextImageRows_row__PPlpB:nth-child(odd) .TextImageRows_media__twu3R,
  .TextImageRows_row__PPlpB:nth-child(odd) .roasist-brand-stage {{
    border-radius: 32px 12.5rem 32px 32px !important;
  }}
  .TextImageRows_row__PPlpB:nth-child(2n) .TextImageRows_media__twu3R,
  .TextImageRows_row__PPlpB:nth-child(2n) .roasist-brand-stage {{
    border-radius: 12.5rem 32px 32px 32px !important;
  }}
}}
.roasist-brand-stage.gads-sub-stage {{
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  background: #FFFFFF;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  z-index: 4;
}}
.gads-sub-svg {{
  width: 92%;
  max-width: 580px;
  height: auto;
  display: block;
}}
/* Hide any residual Detaylı İncele button container in campaign rows */
.TextImageRows_textImageRows__lOU02 .TextImageRows_buttonContainer___PqVy {{
  display: none !important;
}}

/* ---- 1. SEARCH ADS ---- */
.gs-searchbar {{ transform-origin: 300px 102px; animation: gsBar 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }}
.gs-query-bar {{ transform-origin: 190px 102px; animation: gsType 7s ease-in-out infinite; }}
.gs-cursor {{ animation: gsBlink 7s steps(2, start) infinite; }}
.gs-adcard {{ transform-origin: 300px 194px; animation: gsCard 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }}
.gs-ripple {{ transform-origin: 430px 194px; animation: gsRipple 7s ease-out infinite; }}
.gs-emblem {{ transform-origin: 300px 154px; animation: gsEmblem 7s cubic-bezier(0.25, 1, 0.5, 1) infinite; }}
.gs-wordmark {{ animation: gadsWord 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }}
@keyframes gsBar {{ 0% {{ opacity:0; transform:translateY(18px) scale(.92); }} 10%,30% {{ opacity:1; transform:translateY(0) scale(1); }} 38%,100% {{ opacity:0; transform:translateY(-16px) scale(.86); }} }}
@keyframes gsType {{ 0%,6% {{ transform:scaleX(.15); }} 18%,100% {{ transform:scaleX(1); }} }}
@keyframes gsBlink {{ 0%,100% {{ opacity:1; }} 12%,22% {{ opacity:0; }} }}
@keyframes gsCard {{ 0%,9% {{ opacity:0; transform:translateY(28px) scale(.94); }} 19%,30% {{ opacity:1; transform:translateY(0) scale(1); }} 38%,100% {{ opacity:0; transform:translateY(-10px) scale(.84); }} }}
@keyframes gsRipple {{ 0%,18% {{ opacity:0; transform:scale(.9); }} 22% {{ opacity:.7; transform:scale(1.05); }} 31%,100% {{ opacity:0; transform:scale(1.65); }} }}
@keyframes gsEmblem {{ 0%,35% {{ opacity:0; transform:translateX(0) scale(.65) rotate(-24deg); }} 44% {{ opacity:1; transform:translateX(0) scale(1.06) rotate(0); }} 53% {{ opacity:1; transform:translateX(0) scale(.74); }} 62%,92% {{ opacity:1; transform:translateX(-142px) scale(.74); }} 98%,100% {{ opacity:0; transform:translateX(-142px) scale(.74); }} }}

/* ---- 2. PERFORMANCE MAX ---- */
.pm-orbit {{ transform-origin: 300px 160px; animation: pmOrbit 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }}
.pm-emblem {{ transform-origin: 300px 160px; animation: pmEmblem 7s cubic-bezier(0.25, 1, 0.5, 1) infinite; }}
.pm-wordmark {{ animation: gadsWord 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }}
@keyframes pmOrbit {{ 0% {{ opacity:0; transform:scale(.6) rotate(-30deg); }} 14%,30% {{ opacity:1; transform:scale(1) rotate(0deg); }} 38%,100% {{ opacity:0; transform:scale(.35) rotate(45deg); }} }}
@keyframes pmEmblem {{ 0%,35% {{ opacity:0; transform:translateX(0) scale(.5) rotate(-45deg); }} 44% {{ opacity:1; transform:translateX(0) scale(1.08) rotate(0); }} 53% {{ opacity:1; transform:translateX(0) scale(.72); }} 62%,92% {{ opacity:1; transform:translateX(-166px) scale(.72); }} 98%,100% {{ opacity:0; transform:translateX(-166px) scale(.72); }} }}

/* ---- 3. DEMAND GEN ---- */
.dg-card-1 {{ transform-origin: 184px 162px; animation: shCard1 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }}
.dg-card-2 {{ transform-origin: 300px 154px; animation: shCard2 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }}
.dg-card-3 {{ transform-origin: 416px 162px; animation: shCard3 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }}
.dg-emblem {{ transform-origin: 308px 160px; animation: dgEmblem 7s cubic-bezier(0.25, 1, 0.5, 1) infinite; }}
.dg-wordmark {{ animation: gadsWord 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }}
@keyframes dgEmblem {{ 0%,35% {{ opacity:0; transform:translateX(0) scale(.6); }} 44% {{ opacity:1; transform:translateX(0) scale(1.05); }} 53% {{ opacity:1; transform:translateX(0) scale(.76); }} 62%,92% {{ opacity:1; transform:translateX(-154px) scale(.76); }} 98%,100% {{ opacity:0; transform:translateX(-154px) scale(.76); }} }}

/* ---- 4. DISPLAY ADS ---- */
.gd-tile-1 {{ transform-origin: 300px 105px; animation: gdTile1 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }}
.gd-tile-2 {{ transform-origin: 212px 197px; animation: gdTile2 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }}
.gd-tile-3 {{ transform-origin: 384px 197px; animation: gdTile3 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }}
.gd-emblem {{ transform-origin: 304px 154px; animation: gdEmblem 7s cubic-bezier(0.25, 1, 0.5, 1) infinite; }}
.gd-wordmark {{ animation: gadsWord 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }}
@keyframes gdTile1 {{ 0% {{ opacity:0; transform:translateY(-20px) scale(.92); }} 11%,29% {{ opacity:1; transform:translateY(0) scale(1); }} 37%,100% {{ opacity:0; transform:translateY(28px) scale(.6); }} }}
@keyframes gdTile2 {{ 0%,5% {{ opacity:0; transform:translateX(-24px) scale(.9); }} 15%,29% {{ opacity:1; transform:translateX(0) scale(1); }} 37%,100% {{ opacity:0; transform:translateX(48px) scale(.55); }} }}
@keyframes gdTile3 {{ 0%,9% {{ opacity:0; transform:translateX(24px) scale(.9); }} 19%,29% {{ opacity:1; transform:translateX(0) scale(1); }} 37%,100% {{ opacity:0; transform:translateX(-48px) scale(.55); }} }}
@keyframes gdEmblem {{ 0%,35% {{ opacity:0; transform:translateX(0) scale(.62); }} 44% {{ opacity:1; transform:translateX(0) scale(1.08); }} 53% {{ opacity:1; transform:translateX(0) scale(.78); }} 62%,92% {{ opacity:1; transform:translateX(-146px) scale(.78); }} 98%,100% {{ opacity:0; transform:translateX(-146px) scale(.78); }} }}

/* ---- 5. SHOPPING ADS ---- */
.sh-card-1 {{ transform-origin: 180px 160px; animation: shCard1 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }}
.sh-card-2 {{ transform-origin: 300px 152px; animation: shCard2 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }}
.sh-card-3 {{ transform-origin: 420px 160px; animation: shCard3 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }}
.sh-emblem {{ transform-origin: 300px 156px; animation: shEmblem 7s cubic-bezier(0.25, 1, 0.5, 1) infinite; }}
.sh-wordmark {{ animation: gadsWord 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }}
@keyframes shCard1 {{ 0% {{ opacity:0; transform:translateY(36px) rotate(-6deg) scale(.88); }} 12%,29% {{ opacity:1; transform:translateY(0) rotate(-3deg) scale(1); }} 37%,100% {{ opacity:0; transform:translateX(90px) scale(.5); }} }}
@keyframes shCard2 {{ 0%,4% {{ opacity:0; transform:translateY(42px) scale(.88); }} 15%,29% {{ opacity:1; transform:translateY(0) scale(1); }} 37%,100% {{ opacity:0; transform:scale(.5); }} }}
@keyframes shCard3 {{ 0%,8% {{ opacity:0; transform:translateY(36px) rotate(6deg) scale(.88); }} 18%,29% {{ opacity:1; transform:translateY(0) rotate(3deg) scale(1); }} 37%,100% {{ opacity:0; transform:translateX(-90px) scale(.5); }} }}
@keyframes shEmblem {{ 0%,35% {{ opacity:0; transform:translateX(0) scale(.6) rotate(22deg); }} 44% {{ opacity:1; transform:translateX(0) scale(1.1) rotate(0); }} 53% {{ opacity:1; transform:translateX(0) scale(.76); }} 62%,92% {{ opacity:1; transform:translateX(-154px) scale(.76); }} 98%,100% {{ opacity:0; transform:translateX(-154px) scale(.76); }} }}

/* ---- 6. VIDEO ADS ---- */
.vd-player {{ transform-origin: 300px 163px; animation: vdPlayer 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }}
.vd-progress {{ transform-origin: 156px 233px; animation: vdProg 7s linear infinite; }}
.vd-emblem {{ transform-origin: 300px 159px; animation: vdEmblem 7s cubic-bezier(0.25, 1, 0.5, 1) infinite; }}
.vd-wordmark {{ animation: gadsWord 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }}
@keyframes vdPlayer {{ 0% {{ opacity:0; transform:scale(.88) translateY(18px); }} 12%,29% {{ opacity:1; transform:scale(1) translateY(0); }} 37%,100% {{ opacity:0; transform:scale(.68); }} }}
@keyframes vdProg {{ 0%,8% {{ transform:scaleX(.05); }} 30%,100% {{ transform:scaleX(1); }} }}
@keyframes vdEmblem {{ 0%,35% {{ opacity:0; transform:translateX(0) scale(.6); }} 44% {{ opacity:1; transform:translateX(0) scale(1.06); }} 53% {{ opacity:1; transform:translateX(0) scale(.74); }} 62%,92% {{ opacity:1; transform:translateX(-132px) scale(.74); }} 98%,100% {{ opacity:0; transform:translateX(-132px) scale(.74); }} }}

/* ---- 7. APP ADS ---- */
.ap-phone {{ transform-origin: 300px 160px; animation: apPhone 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }}
.ap-emblem {{ transform-origin: 306px 160px; animation: apEmblem 7s cubic-bezier(0.25, 1, 0.5, 1) infinite; }}
.ap-wordmark {{ animation: gadsWord 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }}
@keyframes apPhone {{ 0% {{ opacity:0; transform:translateY(30px) scale(.88); }} 12%,29% {{ opacity:1; transform:translateY(0) scale(1); }} 37%,100% {{ opacity:0; transform:translateY(-16px) scale(.62); }} }}
@keyframes apEmblem {{ 0%,35% {{ opacity:0; transform:translateX(0) scale(.58) rotate(-18deg); }} 44% {{ opacity:1; transform:translateX(0) scale(1.08) rotate(0); }} 53% {{ opacity:1; transform:translateX(0) scale(.76); }} 62%,92% {{ opacity:1; transform:translateX(-132px) scale(.76); }} 98%,100% {{ opacity:0; transform:translateX(-132px) scale(.76); }} }}

@keyframes gadsWord {{
  0%, 58%   {{ opacity: 0; transform: translateX(-16px); }}
  67%, 92%  {{ opacity: 1; transform: translateX(0); }}
  98%, 100% {{ opacity: 0; transform: translateX(0); }}
}}
</style>"""

STAGES_HTML = [
    SVG_SEARCH,
    SVG_PMAX,
    SVG_DEMAND_GEN,
    SVG_DISPLAY,
    SVG_SHOPPING,
    SVG_VIDEO,
    SVG_APP,
]

MOUNT_SCRIPT = f"""<script id="{SCRIPT_ID}">
(function() {{
  var STAGES = {json.dumps(STAGES_HTML, ensure_ascii=False)};
  function mount() {{
    var medias = document.querySelectorAll('.TextImageRows_textImageRows__lOU02 .TextImageRows_media__twu3R');
    medias.forEach(function(fig, idx) {{
      if (idx >= STAGES.length) return;
      if (fig.querySelector('.gads-sub-stage')) return;
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
  if (document.readyState === 'loading') {{
    document.addEventListener('DOMContentLoaded', mount);
  }} else {{
    mount();
  }}
  var obs = new MutationObserver(mount);
  obs.observe(document.documentElement, {{ childList: true, subtree: true }});
  setTimeout(mount, 400);
  setTimeout(mount, 1500);
}})();
</script>"""


def extract_flight_chunks(html_text):
    pattern = re.compile(r'(<script>self\.__next_f\.push\(\[1,")((?:\\.|[^"\\])*)("\]\)</script>)')
    matches = list(pattern.finditer(html_text))
    decoded_parts = [json.loads('"' + m.group(2) + '"') for m in matches]
    return matches, decoded_parts, "".join(decoded_parts)


def render_ssr_campaign_rows(campaigns, placeholder):
    esc = lambda s: html_lib.escape(str(s), quote=True)
    rows = []
    for c in campaigns:
        rows.append(
            '<div class="TextImageRows_row__PPlpB">'
            '<div class="TextImageRows_text__bRCSP">'
            '<h3 class="TextImageRows_heading__RS3OS">'
            f'<span class="LineByLine_headingOuter__JmusT"><span>{esc(c["title"])}</span></span>'
            '</h3>'
            '<div class="TextImageRows_text__bRCSP">'
            f'<span class="FadeIn_container__bjQVL" data-fill="false"><span><p>{esc(c["desc"])}</p>\n</span></span>'
            '</div>'
            '</div>'
            '<figure class="TextImageRows_media__twu3R">'
            '<div class="ImageEnter_image__FSEP_" data-fill="true">'
            '<span class="Image_image__RAAdZ Image_fill__EiIzS">'
            f'<img data-srcset="" data-src="{esc(placeholder)}" alt="" fetchPriority="low" height="1224" width="1224" sizes="auto" class="lazyload"/>'
            '</span></div></figure>'
            '</div>'
        )
    return "".join(rows)


def build_flight_campaign_rows(campaigns, placeholder):
    rows = []
    for idx, c in enumerate(campaigns):
        rows.append([
            "$", "div", str(idx), {
                "className": "TextImageRows_row__PPlpB",
                "children": [
                    [
                        "$", "div", None, {
                            "className": "TextImageRows_text__bRCSP",
                            "children": [
                                [
                                    "$", "h3", None, {
                                        "className": "TextImageRows_heading__RS3OS",
                                        "children": ["$", "$L2c", None, {
                                            "children": ["$", "span", None, {
                                                "dangerouslySetInnerHTML": {"__html": c["title"]}
                                            }]
                                        }]
                                    }
                                ],
                                [
                                    "$", "div", None, {
                                        "className": "TextImageRows_text__bRCSP",
                                        "children": ["$", "$L2e", None, {
                                            "delay": 0.3,
                                            "children": ["$", "span", None, {
                                                "dangerouslySetInnerHTML": {"__html": f"<p>{c['desc']}</p>\n"}
                                            }]
                                        }]
                                    }
                                ],
                                False,
                            ],
                        }
                    ],
                    [
                        "$", "figure", None, {
                            "className": "TextImageRows_media__twu3R",
                            "children": ["$", "$L4a", None, {
                                "fill": True,
                                "children": [
                                    ["$", "$L47", None, {
                                        "image": {
                                            "altText": "",
                                            "srcSet": "",
                                            "sourceUrl": placeholder,
                                            "mediaDetails": {"width": 1224, "height": 1224},
                                        },
                                        "layout": "fill",
                                    }],
                                    False,
                                ],
                            }],
                        }
                    ],
                ],
            },
        ])
    return rows


def update_campaigns_and_stages(target_path, campaigns, is_gh_pages=False):
    text = open(target_path, "r", encoding="utf-8").read()
    placeholder = "/roasist-web/roasist-logo.svg" if is_gh_pages else "/roasist-logo.svg"

    # 1. Inject / replace CSS in <head>
    style_re = re.compile(rf'<style id="{STYLE_ID}">.*?</style>', re.S)
    if style_re.search(text):
        text = style_re.sub(GADS_STAGES_CSS, text, count=1)
    else:
        head_end = text.find("</head>")
        if head_end == -1:
            raise RuntimeError(f"No </head> in {target_path}")
        text = text[:head_end] + GADS_STAGES_CSS + text[head_end:]

    # 2. Replace SSR <section class="TextImageRows_textImageRows__lOU02">...</section>
    sec_re = re.compile(
        r'(<section class="TextImageRows_textImageRows__lOU02"><div class="container">)(.*?)(</div></section>)',
        re.S,
    )
    if not sec_re.search(text):
        raise RuntimeError(f"Could not find TextImageRows_textImageRows__lOU02 in {target_path}")
    ssr_rows = render_ssr_campaign_rows(campaigns, placeholder)
    text = sec_re.sub(lambda m: m.group(1) + ssr_rows + m.group(3), text, count=1)

    # 3. Replace Record 34 (TextImageRows) in React Flight stream
    matches, _, full = extract_flight_chunks(text)
    recs = parse_flight_stream(full)
    replaced = False
    for i, rec in enumerate(recs):
        if rec[0] == "line" and "TextImageRows_textImageRows__lOU02" in rec[2]:
            obj = json.loads(rec[2])
            # obj = ["$","section",null,{"className":"TextImageRows_textImageRows__lOU02","children":["$","div",null,{"className":"container","children":[ROWS, false]}]}]
            container = obj[3]["children"]
            container[3]["children"][0] = build_flight_campaign_rows(campaigns, placeholder)
            recs[i] = ["line", rec[1], json.dumps(obj, ensure_ascii=False, separators=(",", ":"))]
            replaced = True
            break

    if not replaced:
        raise RuntimeError(f"Could not find TextImageRows in Flight stream of {target_path}")

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

    # 4. Inject / replace mount script before </body>
    script_re = re.compile(rf'<script id="{SCRIPT_ID}">.*?</script>', re.S)
    if script_re.search(text):
        text = script_re.sub(lambda _: MOUNT_SCRIPT, text, count=1)
    else:
        body_end = text.rfind("</body>")
        if body_end == -1:
            raise RuntimeError(f"No </body> in {target_path}")
        text = text[:body_end] + MOUNT_SCRIPT + text[body_end:]

    with open(target_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"[OK] Updated 7 Google Ads campaigns (no buttons) + 7 SVG stages in {os.path.relpath(target_path, REPO_ROOT)} ({len(text):,} bytes)")


def main():
    jobs = [
        # (home_source, target_page, is_en, is_gh_pages)
        (
            os.path.join(REPO_ROOT, "public", "kota-roasist-local.html"),
            os.path.join(REPO_ROOT, "public", "hizmetler", "performans-pazarlamasi", "google-reklamlari", "index.html"),
            False,
            False,
        ),
        (
            os.path.join(REPO_ROOT, "public", "kota-roasist-local.html"),
            os.path.join(REPO_ROOT, "public", "hizmetler", "google-reklamlari", "index.html"),
            False,
            False,
        ),
        (
            os.path.join(REPO_ROOT, "public", "en", "index.html"),
            os.path.join(REPO_ROOT, "public", "en", "google-ads", "index.html"),
            True,
            False,
        ),
        (
            os.path.join(REPO_ROOT, "dist", "index.html"),
            os.path.join(REPO_ROOT, "dist", "hizmetler", "performans-pazarlamasi", "google-reklamlari", "index.html"),
            False,
            True,
        ),
        (
            os.path.join(REPO_ROOT, "dist", "index.html"),
            os.path.join(REPO_ROOT, "dist", "hizmetler", "google-reklamlari", "index.html"),
            False,
            True,
        ),
        (
            os.path.join(REPO_ROOT, "dist", "en", "index.html"),
            os.path.join(REPO_ROOT, "dist", "en", "google-ads", "index.html"),
            True,
            True,
        ),
    ]

    for home_src, target, is_en, is_gh in jobs:
        if not os.path.exists(home_src) or not os.path.exists(target):
            print(f"[SKIP] Missing {os.path.relpath(target, REPO_ROOT)} or {os.path.relpath(home_src, REPO_ROOT)}")
            continue
        # 1. Sync 5 Homepage Statistics cards + heading + Turkish diacritic fix
        stats = get_homepage_statistics(home_src)
        sync_stats(target, stats, is_en=is_en, is_gh_pages=is_gh)
        # 2. Update 6-step Process cards (with balanced <div> tags!)
        update_process(target, EN_STEPS if is_en else TR_STEPS, is_en=is_en, is_gh_pages=is_gh)
        # 3. Replace TextImageRows with 7 campaign types (no Detaylı İncele buttons) + 7 SVG stages
        update_campaigns_and_stages(target, EN_CAMPAIGNS if is_en else TR_CAMPAIGNS, is_gh_pages=is_gh)


if __name__ == "__main__":
    main()
