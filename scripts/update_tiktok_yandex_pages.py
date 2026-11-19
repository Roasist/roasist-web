#!/usr/bin/env python3
"""
Upgrades all TikTok Ads & Yandex Ads detail pages (both TR & EN, in public/ and dist/):
  - TikTok Ads: 5 official campaign types (In-Feed, Spark Ads, TopView, Lead Gen, Video Shopping)
    with 5 bespoke white-stage SVG + CSS brand-motion animations, zero 'Detaylı İncele' buttons.
  - Yandex Ads: 5 official campaign types (Yandex Search, YAN, Smart Banners, Yandex Maps,
    Yandex Metrica) with 5 bespoke white-stage SVG + CSS brand-motion animations, zero buttons.
  - Both channels: synced 5 Homepage 'ÖLÇÜLEBİLİR SONUÇLAR' / 'MEASURABLE RESULTS' cards +
    heading + Turkish diacritic fix, and upgraded 6-step 'Hizmet Sürecimiz' cards (zero duplicates).
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

# ===========================================================================
# 1. TIKTOK ADS — 5 Campaign Types + 5 Bespoke White-Stage SVG Animations
# ===========================================================================

TR_TIKTOK_CAMPAIGNS = [
    {
        "title": "In-Feed (Akış İçi) Video Reklamları",
        "desc": "Kullanıcıların 'Sizin İçin' (For You) akışında doğal içerik gibi akan, ilk 3 saniyede dikkat yakalayan tam ekran dikey video reklamlarla yüksek etkileşim ve dönüşüm elde edin.",
    },
    {
        "title": "Spark Ads (Organik İçerik Güçlendirme)",
        "desc": "Kendi hesabınızdan veya iş birliği yaptığınız içerik üreticilerinin (UGC) yüksek performanslı organik videolarını reklam bütçesiyle ölçeklendirerek güven ve ROAS'ı artırın.",
    },
    {
        "title": "TopView & Marka Devralma",
        "desc": "Kullanıcı TikTok uygulamasını açtığı ilk anda tam ekran ve sesli olarak karşısına çıkan yüksek etkili reklam formatıyla lansman ve kampanyalarınızda maksimum bilinirlik kazanın.",
    },
    {
        "title": "Potansiyel Müşteri (Lead Gen) Kampanyaları",
        "desc": "Kullanıcıyı uygulamadan çıkarmadan saniyeler içinde dolan TikTok Hızlı Formları ile düşük maliyetli, yüksek dönüşümlü potansiyel müşteri talepleri toplayın.",
    },
    {
        "title": "Video Shopping & Katalog Satışları",
        "desc": "Ürün kataloğunuzu dinamik video kreatifleri, alışveriş kartları ve TikTok Events API entegrasyonuyla birleştirerek doğrudan e-ticaret satışlarınızı katlayın.",
    },
]

EN_TIKTOK_CAMPAIGNS = [
    {
        "title": "In-Feed Video Ads",
        "desc": "Blend seamlessly into the For You feed with native 9:16 vertical videos engineered with 3-second hooks to capture attention and drive scalable conversions.",
    },
    {
        "title": "Spark Ads (Creator & UGC Boosting)",
        "desc": "Amplify high-performing organic videos from your brand account or creator partners to combine authentic social proof with precision paid targeting.",
    },
    {
        "title": "TopView & Brand Takeover",
        "desc": "Command 100% share-of-voice the moment users open TikTok with sound-on, full-screen storytelling built for high-impact product launches.",
    },
    {
        "title": "Lead Generation Campaigns",
        "desc": "Capture qualified leads seamlessly inside TikTok using pre-filled Instant Forms without forcing users to leave the app.",
    },
    {
        "title": "Video Shopping & Catalog Ads",
        "desc": "Connect your product feed with dynamic video cards and TikTok Events API attribution to scale profitable e-commerce ROAS.",
    },
]

SVG_TT_INFEED = """
<div class="roasist-brand-stage tt-sub-stage">
  <svg viewBox="0 0 600 320" class="sub-brand-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="TikTok In-Feed Ads">
    <defs><filter id="ttSh1" x="-15%" y="-15%" width="130%" height="140%"><feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#0F172A" flood-opacity="0.09"/></filter></defs>
    <g class="sub-p1-slide" filter="url(#ttSh1)">
      <rect x="234" y="52" width="132" height="216" rx="24" fill="#010101"/>
      <rect x="242" y="62" width="116" height="196" rx="16" fill="#18181B"/>
      <polygon points="292,138 292,168 316,153" fill="#25F4EE" transform="translate(-2,-2)"/>
      <polygon points="292,138 292,168 316,153" fill="#FE2C55" transform="translate(2,2)"/>
      <polygon points="292,138 292,168 316,153" fill="#FFFFFF"/>
      <circle cx="342" cy="170" r="8" fill="#FE2C55"/>
      <circle cx="342" cy="194" r="8" fill="#FFFFFF" opacity="0.85"/>
      <circle cx="342" cy="218" r="8" fill="#25F4EE"/>
      <rect x="252" y="218" width="68" height="7" rx="3.5" fill="#FFFFFF" opacity="0.9"/>
      <rect x="252" y="232" width="52" height="14" rx="7" fill="#FE2C55"/>
    </g>
    <g class="sub-emblem-138">
      <rect x="262" y="122" width="76" height="76" rx="22" fill="#010101"/>
      <polygon points="290,144 290,176 318,160" fill="#25F4EE" transform="translate(-2.5,-2)"/>
      <polygon points="290,144 290,176 318,160" fill="#FE2C55" transform="translate(2.5,2)"/>
      <polygon points="290,144 290,176 318,160" fill="#FFFFFF"/>
    </g>
    <g class="sub-wordmark"><text x="228" y="174" font-family="'Inter', Arial, sans-serif" font-size="40" font-weight="700" fill="#010101" letter-spacing="-0.8">In-Feed Ads</text></g>
  </svg>
</div>
""".strip()

SVG_TT_SPARK = """
<div class="roasist-brand-stage tt-sub-stage">
  <svg viewBox="0 0 600 320" class="sub-brand-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="TikTok Spark Ads">
    <g class="sub-p1-pop">
      <circle cx="300" cy="160" r="84" fill="none" stroke="#25F4EE" stroke-width="2" stroke-dasharray="6 6"/>
      <circle cx="300" cy="160" r="54" fill="none" stroke="#FE2C55" stroke-width="2" opacity="0.6"/>
      <path d="M300 94 L315 145 L366 160 L315 175 L300 226 L285 175 L234 160 L285 145 Z" fill="#25F4EE" transform="translate(-4,-3)"/>
      <path d="M300 94 L315 145 L366 160 L315 175 L300 226 L285 175 L234 160 L285 145 Z" fill="#FE2C55" transform="translate(4,3)"/>
      <path d="M300 94 L315 145 L366 160 L315 175 L300 226 L285 175 L234 160 L285 145 Z" fill="#010101"/>
    </g>
    <g class="sub-emblem-134">
      <path d="M300 112 L312 148 L348 160 L312 172 L300 208 L288 172 L252 160 L288 148 Z" fill="#25F4EE" transform="translate(-3,-2)"/>
      <path d="M300 112 L312 148 L348 160 L312 172 L300 208 L288 172 L252 160 L288 148 Z" fill="#FE2C55" transform="translate(3,2)"/>
      <path d="M300 112 L312 148 L348 160 L312 172 L300 208 L288 172 L252 160 L288 148 Z" fill="#010101"/>
    </g>
    <g class="sub-wordmark"><text x="234" y="174" font-family="'Inter', Arial, sans-serif" font-size="40" font-weight="700" fill="#010101" letter-spacing="-0.8">Spark Ads</text></g>
  </svg>
</div>
""".strip()

SVG_TT_TOPVIEW = """
<div class="roasist-brand-stage tt-sub-stage">
  <svg viewBox="0 0 600 320" class="sub-brand-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="TikTok TopView Ads">
    <defs><filter id="ttSh3" x="-15%" y="-15%" width="130%" height="140%"><feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#0F172A" flood-opacity="0.09"/></filter></defs>
    <g class="sub-p1-pop" filter="url(#ttSh3)">
      <rect x="164" y="72" width="272" height="176" rx="22" fill="#010101"/>
      <rect x="176" y="84" width="248" height="152" rx="14" fill="#18181B"/>
      <!-- Corner spotlight brackets -->
      <path d="M196 116 L196 100 L212 100 M404 116 L404 100 L388 100 M196 204 L196 220 L212 220 M404 204 L404 220 L388 220" fill="none" stroke="#25F4EE" stroke-width="3.2" stroke-linecap="round"/>
      <rect x="262" y="142" width="76" height="36" rx="18" fill="#FE2C55"/>
      <text x="300" y="165" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="13">TOP 1</text>
    </g>
    <g class="sub-emblem-144">
      <rect x="256" y="124" width="88" height="72" rx="18" fill="#010101"/>
      <path d="M272 146 L272 138 L280 138 M328 146 L328 138 L320 138 M272 174 L272 182 L280 182 M328 174 L328 182 L320 182" fill="none" stroke="#25F4EE" stroke-width="3.2" stroke-linecap="round"/>
      <circle cx="300" cy="160" r="11" fill="#FE2C55"/>
    </g>
    <g class="sub-wordmark"><text x="224" y="174" font-family="'Inter', Arial, sans-serif" font-size="40" font-weight="700" fill="#010101" letter-spacing="-0.8">TopView Ads</text></g>
  </svg>
</div>
""".strip()

SVG_TT_LEADS = """
<div class="roasist-brand-stage tt-sub-stage">
  <svg viewBox="0 0 600 320" class="sub-brand-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="TikTok Lead Generation">
    <defs><filter id="ttSh4" x="-15%" y="-15%" width="130%" height="140%"><feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#0F172A" flood-opacity="0.08"/></filter></defs>
    <g class="sub-p1-slide" filter="url(#ttSh4)">
      <rect x="196" y="64" width="208" height="192" rx="22" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <circle cx="226" cy="94" r="12" fill="#010101"/>
      <rect x="246" y="88" width="96" height="8" rx="4" fill="#010101"/>
      <rect x="214" y="118" width="172" height="26" rx="8" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.2"/>
      <rect x="224" y="128" width="108" height="7" rx="3.5" fill="#475569"/>
      <rect x="214" y="152" width="172" height="26" rx="8" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.2"/>
      <rect x="224" y="162" width="128" height="7" rx="3.5" fill="#475569"/>
      <rect x="214" y="194" width="172" height="36" rx="18" fill="#FE2C55"/>
      <text x="300" y="217" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="13">INSTANT FORM</text>
      <circle cx="400" cy="84" r="17" fill="#25F4EE"/>
      <path d="M393 84 L398 89 L408 79" fill="none" stroke="#010101" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
    </g>
    <g class="sub-emblem-134">
      <rect x="262" y="120" width="76" height="80" rx="18" fill="#010101"/>
      <rect x="278" y="140" width="44" height="7" rx="3.5" fill="#FFFFFF"/>
      <rect x="278" y="155" width="32" height="7" rx="3.5" fill="#25F4EE"/>
      <circle cx="328" cy="188" r="17" fill="#FE2C55" stroke="#FFFFFF" stroke-width="3"/>
      <path d="M321 188 L326 193 L336 183" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
    </g>
    <g class="sub-wordmark"><text x="234" y="174" font-family="'Inter', Arial, sans-serif" font-size="40" font-weight="700" fill="#010101" letter-spacing="-0.8">Lead Gen</text></g>
  </svg>
</div>
""".strip()

SVG_TT_SHOP = """
<div class="roasist-brand-stage tt-sub-stage">
  <svg viewBox="0 0 600 320" class="sub-brand-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="TikTok Video Shopping">
    <defs><filter id="ttSh5" x="-15%" y="-15%" width="130%" height="140%"><feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#0F172A" flood-opacity="0.08"/></filter></defs>
    <g class="sub-card-1" filter="url(#ttSh5)">
      <rect x="128" y="94" width="104" height="134" rx="16" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <rect x="142" y="108" width="76" height="62" rx="10" fill="#ECFEFF"/>
      <circle cx="180" cy="139" r="14" fill="#25F4EE"/>
      <rect x="142" y="182" width="54" height="8" rx="4" fill="#CBD5E1"/>
      <rect x="142" y="198" width="48" height="18" rx="9" fill="#010101"/>
      <text x="166" y="211" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="10">SHOP</text>
    </g>
    <g class="sub-card-2" filter="url(#ttSh5)">
      <rect x="248" y="76" width="104" height="152" rx="18" fill="#FFFFFF" stroke="#FE2C55" stroke-width="1.8"/>
      <rect x="262" y="90" width="76" height="68" rx="10" fill="#FFF1F2"/>
      <path d="M285 112 h30 l4 28 h-38 z" fill="#FE2C55"/>
      <path d="M292 112 a8 8 0 0 1 16 0" fill="none" stroke="#FE2C55" stroke-width="2.8"/>
      <rect x="262" y="170" width="64" height="9" rx="4.5" fill="#010101"/>
      <rect x="262" y="186" width="46" height="7" rx="3.5" fill="#CBD5E1"/>
      <rect x="262" y="200" width="62" height="18" rx="9" fill="#FE2C55"/>
      <text x="293" y="213" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="10.5">BUY NOW</text>
    </g>
    <g class="sub-card-3" filter="url(#ttSh5)">
      <rect x="368" y="94" width="104" height="134" rx="16" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <rect x="382" y="108" width="76" height="62" rx="10" fill="#F1F5F9"/>
      <polygon points="414,129 414,149 432,139" fill="#010101"/>
      <rect x="382" y="182" width="56" height="8" rx="4" fill="#CBD5E1"/>
      <rect x="382" y="198" width="48" height="18" rx="9" fill="#ECFEFF"/>
      <text x="406" y="211" text-anchor="middle" fill="#010101" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="10">FEED</text>
    </g>
    <g class="sub-emblem-162">
      <rect x="262" y="122" width="76" height="76" rx="22" fill="#010101"/>
      <path d="M284 148 h32 l4 32 h-40 z" fill="#25F4EE" transform="translate(-2,-1.5)"/>
      <path d="M284 148 h32 l4 32 h-40 z" fill="#FE2C55" transform="translate(2,1.5)"/>
      <path d="M284 148 h32 l4 32 h-40 z" fill="#FFFFFF"/>
      <path d="M291 148 a9 9 0 0 1 18 0" fill="none" stroke="#FFFFFF" stroke-width="3.2"/>
    </g>
    <g class="sub-wordmark"><text x="198" y="174" font-family="'Inter', Arial, sans-serif" font-size="38" font-weight="700" fill="#010101" letter-spacing="-0.8">Video Shopping</text></g>
  </svg>
</div>
""".strip()

# ===========================================================================
# 2. YANDEX ADS — 5 Campaign Types + 5 Bespoke White-Stage SVG Animations
# ===========================================================================

TR_YANDEX_CAMPAIGNS = [
    {
        "title": "Yandex Arama (Search) Kampanyaları",
        "desc": "Rusya, BDT ülkeleri ve Rusça konuşan global hedef kitlelerin Yandex arama sonuçlarında ürün ve hizmetlerinizi aradığı anda en üst sırada görünür olun.",
    },
    {
        "title": "Yandex Reklam Ağı (YAN / РСЯ) Kampanyaları",
        "desc": "50.000'den fazla yüksek trafikli haber portalı, e-ticaret sitesi ve mobil uygulamada doğal (native) görsel ve video reklamlarla marka bilinirliği ve retargeting yapın.",
    },
    {
        "title": "Dinamik & Akıllı Katalog (Smart Banner)",
        "desc": "E-ticaret ürün beslemenizi (feed) Yandex Direct akıllı banner ve ürün galerileriyle otomatikleştirerek satın alma niyeti yüksek kullanıcılara dinamik teklifler sunun.",
    },
    {
        "title": "Yandex Haritalar & Geoservice Reklamları",
        "desc": "Sağlık turizmi, gayrimenkul, otelcilik ve lokal hizmetlerde Yandex Maps ile Yandex Navigator kullanıcılarına tam konum ve rota ararken ulaşın.",
    },
    {
        "title": "Yandex Metrica & Dönüşüm Optimizasyonu",
        "desc": "Yandex Metrica web analitiği, çağrı takibi ve çevrimdışı CRM dönüşümlerini kampanyalara bağlayarak yalnızca gerçek satış ve nitelikli lead getiren tıklamalara bütçe harcayın.",
    },
]

EN_YANDEX_CAMPAIGNS = [
    {
        "title": "Yandex Direct Search Campaigns",
        "desc": "Capture high-intent Russian and CIS buyers at the exact moment they search on Yandex with localized keyword clusters and precision bid strategies.",
    },
    {
        "title": "Yandex Advertising Network (YAN)",
        "desc": "Scale awareness and remarketing across 50,000+ premium publisher portals, news sites, and mobile apps using native visual and video placements.",
    },
    {
        "title": "Smart Banners & Product Catalogs",
        "desc": "Automate dynamic e-commerce creatives directly from your product feed to retarget high-intent shoppers with live pricing and offers.",
    },
    {
        "title": "Yandex Maps & Geoservice Ads",
        "desc": "Reach high-value tourism, real estate, and local customers directly inside Yandex Maps and Yandex Navigator at the point of discovery.",
    },
    {
        "title": "Yandex Metrica & Offline Attribution",
        "desc": "Connect Yandex Metrica goals, call tracking, and CRM offline conversions so bidding algorithms optimize strictly for qualified leads and revenue.",
    },
]

SVG_YX_SEARCH = """
<div class="roasist-brand-stage yx-sub-stage">
  <svg viewBox="0 0 600 320" class="sub-brand-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Yandex Search Ads">
    <defs><filter id="yxSh1" x="-15%" y="-15%" width="130%" height="140%"><feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#0F172A" flood-opacity="0.07"/></filter></defs>
    <g class="sub-p1-slide" filter="url(#yxSh1)">
      <rect x="132" y="76" width="336" height="52" rx="16" fill="#FFFFFF" stroke="#FFCC00" stroke-width="2.5"/>
      <circle cx="162" cy="102" r="14" fill="#FC3F1D"/>
      <text x="162" y="108" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="16">Я</text>
      <rect x="190" y="97" width="176" height="10" rx="5" fill="#CBD5E1"/>
      <rect x="394" y="86" width="62" height="32" rx="10" fill="#FFCC00"/>
      <rect x="132" y="146" width="336" height="96" rx="18" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <rect x="154" y="164" width="52" height="20" rx="6" fill="#FEF3C7"/>
      <text x="180" y="178" text-anchor="middle" fill="#B45309" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="10">DIRECT</text>
      <rect x="216" y="170" width="112" height="8" rx="4" fill="#E2E8F0"/>
      <rect x="154" y="194" width="218" height="12" rx="6" fill="#FC3F1D"/>
      <rect x="154" y="216" width="176" height="8" rx="4" fill="#CBD5E1"/>
    </g>
    <g class="sub-emblem-156">
      <circle cx="300" cy="160" r="38" fill="#FC3F1D"/>
      <text x="300" y="176" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="44">Я</text>
    </g>
    <g class="sub-wordmark"><text x="202" y="174" font-family="'Inter', Arial, sans-serif" font-size="38" font-weight="700" fill="#1E293B" letter-spacing="-0.8">Yandex Search</text></g>
  </svg>
</div>
""".strip()

SVG_YX_YAN = """
<div class="roasist-brand-stage yx-sub-stage">
  <svg viewBox="0 0 600 320" class="sub-brand-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Yandex Advertising Network">
    <defs><filter id="yxSh2" x="-15%" y="-15%" width="130%" height="140%"><feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#0F172A" flood-opacity="0.07"/></filter></defs>
    <g class="sub-p1-pop" filter="url(#yxSh2)">
      <rect x="136" y="76" width="328" height="58" rx="14" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <rect x="150" y="90" width="30" height="30" rx="8" fill="#FC3F1D"/>
      <rect x="194" y="95" width="132" height="9" rx="4.5" fill="#1E293B"/>
      <rect x="194" y="110" width="88" height="7" rx="3.5" fill="#CBD5E1"/>
      <rect x="394" y="92" width="56" height="26" rx="13" fill="#FFCC00"/>
      <rect x="136" y="148" width="154" height="96" rx="16" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <rect x="150" y="162" width="126" height="48" rx="10" fill="#FEF2F2"/>
      <circle cx="182" cy="186" r="12" fill="#FC3F1D"/>
      <rect x="150" y="220" width="84" height="8" rx="4" fill="#CBD5E1"/>
      <rect x="306" y="148" width="158" height="96" rx="16" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <rect x="320" y="162" width="130" height="48" rx="10" fill="#FEF9C3"/>
      <rect x="336" y="178" width="66" height="8" rx="4" fill="#1E293B"/>
      <rect x="320" y="220" width="88" height="8" rx="4" fill="#CBD5E1"/>
    </g>
    <g class="sub-emblem-144">
      <rect x="260" y="122" width="80" height="76" rx="18" fill="#1E293B"/>
      <rect x="274" y="136" width="22" height="22" rx="6" fill="#FC3F1D"/>
      <rect x="304" y="136" width="22" height="22" rx="6" fill="#FFCC00"/>
      <rect x="274" y="166" width="52" height="18" rx="6" fill="#FFFFFF" opacity="0.9"/>
    </g>
    <g class="sub-wordmark"><text x="218" y="174" font-family="'Inter', Arial, sans-serif" font-size="40" font-weight="700" fill="#1E293B" letter-spacing="-0.8">Yandex YAN</text></g>
  </svg>
</div>
""".strip()

SVG_YX_SMART = """
<div class="roasist-brand-stage yx-sub-stage">
  <svg viewBox="0 0 600 320" class="sub-brand-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Yandex Smart Banners">
    <defs><filter id="yxSh3" x="-15%" y="-15%" width="130%" height="140%"><feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#0F172A" flood-opacity="0.07"/></filter></defs>
    <g class="sub-card-1" filter="url(#yxSh3)">
      <rect x="128" y="94" width="104" height="134" rx="16" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <rect x="142" y="108" width="76" height="62" rx="10" fill="#FEF2F2"/>
      <circle cx="180" cy="139" r="14" fill="#FC3F1D"/>
      <rect x="142" y="182" width="54" height="8" rx="4" fill="#CBD5E1"/>
      <rect x="142" y="198" width="48" height="18" rx="9" fill="#FEF3C7"/>
      <text x="166" y="211" text-anchor="middle" fill="#B45309" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="10">FEED</text>
    </g>
    <g class="sub-card-2" filter="url(#yxSh3)">
      <rect x="248" y="76" width="104" height="152" rx="18" fill="#FFFFFF" stroke="#FC3F1D" stroke-width="1.8"/>
      <rect x="262" y="90" width="76" height="68" rx="10" fill="#FEF9C3"/>
      <path d="M284 110 h18 l14 14 l-18 18 l-14 -14 z" fill="#FC3F1D"/>
      <circle cx="292" cy="118" r="3" fill="#FFFFFF"/>
      <rect x="262" y="170" width="64" height="9" rx="4.5" fill="#1E293B"/>
      <rect x="262" y="186" width="46" height="7" rx="3.5" fill="#CBD5E1"/>
      <rect x="262" y="200" width="62" height="18" rx="9" fill="#FC3F1D"/>
      <text x="293" y="213" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="10">SMART</text>
    </g>
    <g class="sub-card-3" filter="url(#yxSh3)">
      <rect x="368" y="94" width="104" height="134" rx="16" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <rect x="382" y="108" width="76" height="62" rx="10" fill="#F1F5F9"/>
      <rect x="406" y="125" width="28" height="28" rx="8" fill="#1E293B"/>
      <rect x="382" y="182" width="56" height="8" rx="4" fill="#CBD5E1"/>
      <rect x="382" y="198" width="48" height="18" rx="9" fill="#FFCC00"/>
      <text x="406" y="211" text-anchor="middle" fill="#1E293B" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="10">ROAS</text>
    </g>
    <g class="sub-emblem-162">
      <rect x="262" y="122" width="76" height="76" rx="22" fill="#FFCC00"/>
      <path d="M284 142 h18 l16 16 l-18 18 l-16 -16 z" fill="#FC3F1D"/>
      <circle cx="292" cy="150" r="3.5" fill="#FFFFFF"/>
    </g>
    <g class="sub-wordmark"><text x="198" y="174" font-family="'Inter', Arial, sans-serif" font-size="38" font-weight="700" fill="#1E293B" letter-spacing="-0.8">Smart Banners</text></g>
  </svg>
</div>
""".strip()

SVG_YX_MAPS = """
<div class="roasist-brand-stage yx-sub-stage">
  <svg viewBox="0 0 600 320" class="sub-brand-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Yandex Maps Ads">
    <defs><filter id="yxSh4" x="-15%" y="-15%" width="130%" height="140%"><feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#0F172A" flood-opacity="0.07"/></filter></defs>
    <g class="sub-p1-pop" filter="url(#yxSh4)">
      <rect x="156" y="72" width="288" height="176" rx="22" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1.5"/>
      <path d="M156 128 L444 128 M156 192 L444 192 M242 72 L242 248 M358 72 L358 248" stroke="#E2E8F0" stroke-width="4"/>
      <path d="M180 218 Q242 162 300 162 T418 106" fill="none" stroke="#FFCC00" stroke-width="6" stroke-linecap="round"/>
      <!-- Location Pin -->
      <path d="M300 104 C280 104 264 120 264 140 C264 166 300 198 300 198 C300 198 336 166 336 140 C336 120 320 104 300 104 Z" fill="#FC3F1D"/>
      <circle cx="300" cy="138" r="12" fill="#FFFFFF"/>
    </g>
    <g class="sub-emblem-152">
      <path d="M300 112 C278 112 262 128 262 150 C262 178 300 210 300 210 C300 210 338 178 338 150 C338 128 322 112 300 112 Z" fill="#FC3F1D"/>
      <circle cx="300" cy="148" r="13" fill="#FFFFFF"/>
    </g>
    <g class="sub-wordmark"><text x="206" y="174" font-family="'Inter', Arial, sans-serif" font-size="38" font-weight="700" fill="#1E293B" letter-spacing="-0.8">Yandex Maps</text></g>
  </svg>
</div>
""".strip()

SVG_YX_METRICA = """
<div class="roasist-brand-stage yx-sub-stage">
  <svg viewBox="0 0 600 320" class="sub-brand-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Yandex Metrica Analytics">
    <defs><filter id="yxSh5" x="-15%" y="-15%" width="130%" height="140%"><feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#0F172A" flood-opacity="0.07"/></filter></defs>
    <g class="sub-p1-slide" filter="url(#yxSh5)">
      <rect x="150" y="76" width="300" height="168" rx="20" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <line x1="176" y1="212" x2="424" y2="212" stroke="#E2E8F0" stroke-width="1.5"/>
      <rect x="192" y="166" width="32" height="46" rx="8" fill="#FFCC00"/>
      <rect x="246" y="142" width="32" height="70" rx="8" fill="#1E293B"/>
      <rect x="300" y="122" width="32" height="90" rx="8" fill="#FFCC00"/>
      <rect x="354" y="100" width="32" height="112" rx="8" fill="#FC3F1D"/>
      <circle cx="370" cy="100" r="8" fill="#FC3F1D" stroke="#FFFFFF" stroke-width="2.5"/>
    </g>
    <g class="sub-emblem-162">
      <rect x="262" y="122" width="76" height="76" rx="22" fill="#1E293B"/>
      <rect x="278" y="162" width="12" height="22" rx="4" fill="#FFCC00"/>
      <rect x="294" y="148" width="12" height="36" rx="4" fill="#FFFFFF"/>
      <rect x="310" y="136" width="12" height="48" rx="4" fill="#FC3F1D"/>
    </g>
    <g class="sub-wordmark"><text x="196" y="174" font-family="'Inter', Arial, sans-serif" font-size="38" font-weight="700" fill="#1E293B" letter-spacing="-0.8">Yandex Metrica</text></g>
  </svg>
</div>
""".strip()

SHARED_STAGE_CSS = """
.TextImageRows_media__twu3R {
  background: #FFFFFF !important;
  box-shadow: 0 20px 56px -24px rgba(15, 23, 42, 0.14) !important;
  border: 1px solid rgba(15, 23, 42, 0.06) !important;
}
.TextImageRows_row__PPlpB:nth-child(odd) .TextImageRows_media__twu3R,
.TextImageRows_row__PPlpB:nth-child(odd) .roasist-brand-stage {
  border-radius: 20px 80px 20px 20px !important;
}
.TextImageRows_row__PPlpB:nth-child(2n) .TextImageRows_media__twu3R,
.TextImageRows_row__PPlpB:nth-child(2n) .roasist-brand-stage {
  border-radius: 80px 20px 20px 20px !important;
}
@media (min-width: 850px) {
  .TextImageRows_row__PPlpB:nth-child(odd) .TextImageRows_media__twu3R,
  .TextImageRows_row__PPlpB:nth-child(odd) .roasist-brand-stage {
    border-radius: 32px 12.5rem 32px 32px !important;
  }
  .TextImageRows_row__PPlpB:nth-child(2n) .TextImageRows_media__twu3R,
  .TextImageRows_row__PPlpB:nth-child(2n) .roasist-brand-stage {
    border-radius: 12.5rem 32px 32px 32px !important;
  }
}
.roasist-brand-stage {
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
}
.sub-brand-svg {
  width: 92%;
  max-width: 580px;
  height: auto;
  display: block;
}
.TextImageRows_textImageRows__lOU02 .TextImageRows_buttonContainer___PqVy {
  display: none !important;
}
.sub-p1-slide { transform-origin: 300px 160px; animation: sP1Slide 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }
.sub-p1-pop { transform-origin: 300px 160px; animation: sP1Pop 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }
.sub-card-1 { transform-origin: 180px 160px; animation: sCard1 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }
.sub-card-2 { transform-origin: 300px 152px; animation: sCard2 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }
.sub-card-3 { transform-origin: 420px 160px; animation: sCard3 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }
.sub-emblem-134 { transform-origin: 300px 160px; animation: sEmb134 7s cubic-bezier(0.25, 1, 0.5, 1) infinite; }
.sub-emblem-138 { transform-origin: 300px 160px; animation: sEmb138 7s cubic-bezier(0.25, 1, 0.5, 1) infinite; }
.sub-emblem-144 { transform-origin: 300px 160px; animation: sEmb144 7s cubic-bezier(0.25, 1, 0.5, 1) infinite; }
.sub-emblem-152 { transform-origin: 300px 160px; animation: sEmb152 7s cubic-bezier(0.25, 1, 0.5, 1) infinite; }
.sub-emblem-156 { transform-origin: 300px 160px; animation: sEmb156 7s cubic-bezier(0.25, 1, 0.5, 1) infinite; }
.sub-emblem-162 { transform-origin: 300px 160px; animation: sEmb162 7s cubic-bezier(0.25, 1, 0.5, 1) infinite; }
.sub-wordmark { animation: sWord 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }
@keyframes sP1Slide { 0% { opacity:0; transform:translateY(24px) scale(.9); } 13%,30% { opacity:1; transform:translateY(0) scale(1); } 38%,100% { opacity:0; transform:translateY(-16px) scale(.65); } }
@keyframes sP1Pop { 0% { opacity:0; transform:scale(.68); } 13%,30% { opacity:1; transform:scale(1); } 38%,100% { opacity:0; transform:scale(.45); } }
@keyframes sCard1 { 0% { opacity:0; transform:translateY(34px) rotate(-6deg) scale(.88); } 12%,29% { opacity:1; transform:translateY(0) rotate(-3deg) scale(1); } 37%,100% { opacity:0; transform:translateX(84px) scale(.5); } }
@keyframes sCard2 { 0%,4% { opacity:0; transform:translateY(40px) scale(.88); } 15%,29% { opacity:1; transform:translateY(0) scale(1); } 37%,100% { opacity:0; transform:scale(.5); } }
@keyframes sCard3 { 0%,8% { opacity:0; transform:translateY(34px) rotate(6deg) scale(.88); } 18%,29% { opacity:1; transform:translateY(0) rotate(3deg) scale(1); } 37%,100% { opacity:0; transform:translateX(-84px) scale(.5); } }
@keyframes sEmb134 { 0%,35% { opacity:0; transform:translateX(0) scale(.6); } 44% { opacity:1; transform:translateX(0) scale(1.06); } 53% { opacity:1; transform:translateX(0) scale(.76); } 62%,92% { opacity:1; transform:translateX(-134px) scale(.76); } 98%,100% { opacity:0; transform:translateX(-134px) scale(.76); } }
@keyframes sEmb138 { 0%,35% { opacity:0; transform:translateX(0) scale(.6); } 44% { opacity:1; transform:translateX(0) scale(1.06); } 53% { opacity:1; transform:translateX(0) scale(.76); } 62%,92% { opacity:1; transform:translateX(-138px) scale(.76); } 98%,100% { opacity:0; transform:translateX(-138px) scale(.76); } }
@keyframes sEmb144 { 0%,35% { opacity:0; transform:translateX(0) scale(.6); } 44% { opacity:1; transform:translateX(0) scale(1.06); } 53% { opacity:1; transform:translateX(0) scale(.76); } 62%,92% { opacity:1; transform:translateX(-144px) scale(.76); } 98%,100% { opacity:0; transform:translateX(-144px) scale(.76); } }
@keyframes sEmb152 { 0%,35% { opacity:0; transform:translateX(0) scale(.6); } 44% { opacity:1; transform:translateX(0) scale(1.06); } 53% { opacity:1; transform:translateX(0) scale(.74); } 62%,92% { opacity:1; transform:translateX(-152px) scale(.74); } 98%,100% { opacity:0; transform:translateX(-152px) scale(.74); } }
@keyframes sEmb156 { 0%,35% { opacity:0; transform:translateX(0) scale(.6); } 44% { opacity:1; transform:translateX(0) scale(1.06); } 53% { opacity:1; transform:translateX(0) scale(.74); } 62%,92% { opacity:1; transform:translateX(-156px) scale(.74); } 98%,100% { opacity:0; transform:translateX(-156px) scale(.74); } }
@keyframes sEmb162 { 0%,35% { opacity:0; transform:translateX(0) scale(.6); } 44% { opacity:1; transform:translateX(0) scale(1.06); } 53% { opacity:1; transform:translateX(0) scale(.74); } 62%,92% { opacity:1; transform:translateX(-162px) scale(.74); } 98%,100% { opacity:0; transform:translateX(-162px) scale(.74); } }
@keyframes sWord { 0%,58% { opacity:0; transform:translateX(-16px); } 67%,92% { opacity:1; transform:translateX(0); } 98%,100% { opacity:0; transform:translateX(0); } }
"""

TIKTOK_STAGES = [SVG_TT_INFEED, SVG_TT_SPARK, SVG_TT_TOPVIEW, SVG_TT_LEADS, SVG_TT_SHOP]
YANDEX_STAGES = [SVG_YX_SEARCH, SVG_YX_YAN, SVG_YX_SMART, SVG_YX_MAPS, SVG_YX_METRICA]


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


def update_channel_campaigns(target_path, channel_key, campaigns, stages, is_gh_pages=False):
    text = open(target_path, "r", encoding="utf-8").read()
    placeholder = "/roasist-web/roasist-logo.svg" if is_gh_pages else "/roasist-logo.svg"
    style_id = f"roasist-{channel_key}-brand-stages-css"
    script_id = f"roasist-{channel_key}-brand-stages-js"
    stage_cls = f"{channel_key}-sub-stage"

    style_block = f'<style id="{style_id}">{SHARED_STAGE_CSS}</style>'
    style_re = re.compile(rf'<style id="{style_id}">.*?</style>', re.S)
    if style_re.search(text):
        text = style_re.sub(style_block, text, count=1)
    else:
        head_end = text.find("</head>")
        text = text[:head_end] + style_block + text[head_end:]

    sec_re = re.compile(
        r'(<section class="TextImageRows_textImageRows__lOU02"><div class="container">)(.*?)(</div></section>)',
        re.S,
    )
    if not sec_re.search(text):
        raise RuntimeError(f"Could not find TextImageRows in {target_path}")
    text = sec_re.sub(lambda m: m.group(1) + render_ssr_campaign_rows(campaigns, placeholder) + m.group(3), text, count=1)

    matches, _, full = extract_flight_chunks(text)
    recs = parse_flight_stream(full)
    replaced = False
    for i, rec in enumerate(recs):
        if rec[0] == "line" and "TextImageRows_textImageRows__lOU02" in rec[2]:
            obj = json.loads(rec[2])
            obj[3]["children"][3]["children"][0] = build_flight_campaign_rows(campaigns, placeholder)
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

    mount_js = f"""<script id="{script_id}">
(function() {{
  var STAGES = {json.dumps(stages, ensure_ascii=False)};
  function mount() {{
    var medias = document.querySelectorAll('.TextImageRows_textImageRows__lOU02 .TextImageRows_media__twu3R');
    medias.forEach(function(fig, idx) {{
      if (idx >= STAGES.length) return;
      if (fig.querySelector('.{stage_cls}')) return;
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

    with open(target_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"[OK] Updated {len(campaigns)} {channel_key.upper()} campaigns + SVG stages in {os.path.relpath(target_path, REPO_ROOT)} ({len(text):,} bytes)")


def main():
    jobs = [
        # TikTok Ads (public + dist)
        ("public/kota-roasist-local.html", "public/hizmetler/performans-pazarlamasi/tiktok-reklamlari/index.html", "tt", TR_TIKTOK_CAMPAIGNS, TIKTOK_STAGES, False, False),
        ("public/kota-roasist-local.html", "public/hizmetler/tiktok-reklamlari/index.html", "tt", TR_TIKTOK_CAMPAIGNS, TIKTOK_STAGES, False, False),
        ("public/en/index.html", "public/en/tiktok-ads/index.html", "tt", EN_TIKTOK_CAMPAIGNS, TIKTOK_STAGES, True, False),
        ("dist/index.html", "dist/hizmetler/performans-pazarlamasi/tiktok-reklamlari/index.html", "tt", TR_TIKTOK_CAMPAIGNS, TIKTOK_STAGES, False, True),
        ("dist/index.html", "dist/hizmetler/tiktok-reklamlari/index.html", "tt", TR_TIKTOK_CAMPAIGNS, TIKTOK_STAGES, False, True),
        ("dist/en/index.html", "dist/en/tiktok-ads/index.html", "tt", EN_TIKTOK_CAMPAIGNS, TIKTOK_STAGES, True, True),
        # Yandex Ads (public + dist)
        ("public/kota-roasist-local.html", "public/hizmetler/performans-pazarlamasi/yandex-reklamlari/index.html", "yx", TR_YANDEX_CAMPAIGNS, YANDEX_STAGES, False, False),
        ("public/kota-roasist-local.html", "public/hizmetler/yandex-reklamlari/index.html", "yx", TR_YANDEX_CAMPAIGNS, YANDEX_STAGES, False, False),
        ("public/en/index.html", "public/en/yandex-ads/index.html", "yx", EN_YANDEX_CAMPAIGNS, YANDEX_STAGES, True, False),
        ("dist/index.html", "dist/hizmetler/performans-pazarlamasi/yandex-reklamlari/index.html", "yx", TR_YANDEX_CAMPAIGNS, YANDEX_STAGES, False, True),
        ("dist/index.html", "dist/hizmetler/yandex-reklamlari/index.html", "yx", TR_YANDEX_CAMPAIGNS, YANDEX_STAGES, False, True),
        ("dist/en/index.html", "dist/en/yandex-ads/index.html", "yx", EN_YANDEX_CAMPAIGNS, YANDEX_STAGES, True, True),
    ]

    for home_rel, target_rel, ch_key, campaigns, stages, is_en, is_gh in jobs:
        home_src = os.path.join(REPO_ROOT, home_rel)
        target = os.path.join(REPO_ROOT, target_rel)
        if not os.path.exists(home_src) or not os.path.exists(target):
            print(f"[SKIP] Missing {target_rel} or {home_rel}")
            continue
        stats = get_homepage_statistics(home_src)
        sync_stats(target, stats, is_en=is_en, is_gh_pages=is_gh)
        update_process(target, EN_STEPS if is_en else TR_STEPS, is_en=is_en, is_gh_pages=is_gh)
        update_channel_campaigns(target, ch_key, campaigns, stages, is_gh_pages=is_gh)


if __name__ == "__main__":
    main()
