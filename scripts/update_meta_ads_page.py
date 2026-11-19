#!/usr/bin/env python3
"""
Upgrades all Meta / Instagram & Facebook Ads detail pages
(TR: /hizmetler/performans-pazarlamasi/instagram-reklamlari/ and /hizmetler/instagram-reklamlari/,
 EN: /en/instagram-ads/) in both public/ and dist/:

  1. Builds all 6 official Meta Ads (ODAX) campaign objectives (Awareness, Traffic,
     Engagement, Leads, App Promotion, Sales & Advantage+ Shopping) in
     TextImageRows_textImageRows__lOU02 (SSR + Flight), with NO 'Detaylı İncele' buttons.
  2. Injects 6 bespoke, lightweight white-stage SVG + CSS brand-motion animations.
  3. Syncs the 5 Homepage 'ÖLÇÜLEBİLİR SONUÇLAR' / 'MEASURABLE RESULTS' dark case-study
     cards + heading + Turkish diacritic top-clearance fix.
  4. Upgrades 'Hizmet Sürecimiz' (Timeline_timeline__KvsOC) to the elevated 6-step
     architectural white card design (balanced <div> tags, zero duplicate sections).
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

STYLE_ID = "roasist-meta-brand-stages-css"
SCRIPT_ID = "roasist-meta-brand-stages-js"

# ---------------------------------------------------------------------------
# 6 Official Meta Ads (ODAX) Campaign Objectives (TR & EN) — NO buttons
# ---------------------------------------------------------------------------

TR_META_CAMPAIGNS = [
    {
        "title": "Bilinirlik (Awareness) Kampanyaları",
        "desc": "Instagram Reels, Hikayeler, Keşfet ve Facebook akışlarında yüksek hatırlanırlık sağlayan kreatiflerle markanızı milyonlarca potansiyel müşteriye ulaştırın.",
    },
    {
        "title": "Trafik (Traffic) Kampanyaları",
        "desc": "Yüksek tıklama oranına (CTR) sahip reklam kurgularıyla hedef kitlenizi doğrudan web sitenize, açılış sayfalarınıza, Instagram profilinize veya WhatsApp hattınıza yönlendirin.",
    },
    {
        "title": "Etkileşim (Engagement) Kampanyaları",
        "desc": "Instagram DM, WhatsApp ve Messenger mesajlaşma reklamları, video izlenmeleri ve kaydetme odaklı içeriklerle markanız etrafında yüksek etkileşimli bir topluluk oluşturun.",
    },
    {
        "title": "Potansiyel Müşteriler (Leads) Kampanyaları",
        "desc": "Instagram ve Facebook içi Hızlı Formlar (Instant Forms), WhatsApp lead akışları ve dönüşüm odaklı formlarla düşük maliyetli, yüksek nitelikli B2C ve B2B talepler toplayın.",
    },
    {
        "title": "Uygulama Tanıtımı (App) Kampanyaları",
        "desc": "Advantage+ Uygulama Kampanyaları ile Android ve iOS mobil uygulamalarınız için yüksek hacimli indirme ve uygulama içi satın alma aksiyonları elde edin.",
    },
    {
        "title": "Satış (Sales & Advantage+) Kampanyaları",
        "desc": "Dinamik Ürün Katalogları (DPA), Advantage+ Alışveriş Kampanyaları (ASC) ve Conversions API (CAPI) entegrasyonuyla e-ticaret cironuzu ve ROAS performansınızı ölçeklendirin.",
    },
]

EN_META_CAMPAIGNS = [
    {
        "title": "Awareness Campaigns",
        "desc": "Maximize brand recall and reach across Instagram Reels, Stories, Explore, and Facebook Feeds with thumb-stopping creative storytelling.",
    },
    {
        "title": "Traffic Campaigns",
        "desc": "Drive high-intent clicks directly to your website, landing pages, Instagram profile, or WhatsApp channel with conversion-focused creatives.",
    },
    {
        "title": "Engagement Campaigns",
        "desc": "Spark Instagram DM, WhatsApp, and Messenger conversations, video views, and saves that turn passive viewers into active brand advocates.",
    },
    {
        "title": "Lead Generation Campaigns",
        "desc": "Capture frictionless B2C and B2B leads at lower CPL using Meta Instant Forms, WhatsApp lead flows, and CAPI-tracked landing pages.",
    },
    {
        "title": "App Promotion Campaigns",
        "desc": "Scale profitable Android and iOS installs and in-app events through Advantage+ App Campaigns across Instagram, Facebook, and Audience Network.",
    },
    {
        "title": "Sales & Advantage+ Shopping",
        "desc": "Scale e-commerce revenue and ROAS with Dynamic Product Ads (DPA), Advantage+ Shopping Campaigns (ASC), and server-side Conversions API (CAPI).",
    },
]

# ---------------------------------------------------------------------------
# 6 Bespoke White-Stage Brand-Motion SVG + CSS Animations for Meta Ads
# ---------------------------------------------------------------------------

SVG_AWARENESS = """
<div class="roasist-brand-stage meta-sub-stage">
  <svg viewBox="0 0 600 320" class="meta-sub-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Meta Awareness Ads">
    <defs>
      <linearGradient id="maGrad" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="#0081FB"/>
        <stop offset="55%" stop-color="#833AB4"/>
        <stop offset="100%" stop-color="#E1306C"/>
      </linearGradient>
    </defs>
    <!-- Phase 1: Expanding Broadcast Reach Rings + Audience Nodes -->
    <g class="ma-radar">
      <circle cx="300" cy="160" r="92" fill="none" stroke="#E2E8F0" stroke-width="1.5" stroke-dasharray="5 6"/>
      <circle cx="300" cy="160" r="62" fill="none" stroke="#833AB4" stroke-width="1.6" opacity="0.35"/>
      <circle cx="300" cy="160" r="34" fill="url(#maGrad)"/>
      <!-- Eye / Reach icon inside center -->
      <path d="M284 160 Q300 144 316 160 Q300 176 284 160 Z" fill="none" stroke="#FFFFFF" stroke-width="2.8"/>
      <circle cx="300" cy="160" r="5" fill="#FFFFFF"/>
      <!-- Expanding pulse ring -->
      <circle cx="300" cy="160" r="36" fill="none" stroke="#0081FB" stroke-width="2.2" class="ma-pulse"/>
      <!-- Reach audience dots -->
      <circle cx="222" cy="112" r="10" fill="#0081FB"/>
      <circle cx="384" cy="118" r="11" fill="#E1306C"/>
      <circle cx="376" cy="214" r="9"  fill="#833AB4"/>
      <circle cx="226" cy="210" r="10" fill="#F77737"/>
    </g>
    <!-- Phase 2: Awareness Emblem + Wordmark -->
    <g class="ma-emblem">
      <circle cx="300" cy="160" r="38" fill="url(#maGrad)"/>
      <path d="M278 160 Q300 140 322 160 Q300 180 278 160 Z" fill="none" stroke="#FFFFFF" stroke-width="4"/>
      <circle cx="300" cy="160" r="7" fill="#FFFFFF"/>
    </g>
    <g class="ma-wordmark">
      <text x="226" y="174" font-family="'Inter', Arial, sans-serif" font-size="40" font-weight="600" fill="#1C2B33" letter-spacing="-0.8">Awareness</text>
    </g>
  </svg>
</div>
""".strip()

SVG_TRAFFIC = """
<div class="roasist-brand-stage meta-sub-stage">
  <svg viewBox="0 0 600 320" class="meta-sub-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Meta Traffic Ads">
    <defs>
      <filter id="mtSh" x="-15%" y="-15%" width="130%" height="140%">
        <feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#0F172A" flood-opacity="0.08"/>
      </filter>
    </defs>
    <!-- Phase 1: Ad Card -> Destination Landing Page Flow -->
    <g class="mt-flow">
      <!-- Left Social Post Card -->
      <g filter="url(#mtSh)">
        <rect x="128" y="96" width="124" height="132" rx="18" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
        <circle cx="150" cy="116" r="8" fill="#E1306C"/>
        <rect x="166" y="112" width="60" height="8" rx="4" fill="#CBD5E1"/>
        <rect x="142" y="134" width="96" height="54" rx="10" fill="#EFF6FF"/>
        <rect x="142" y="196" width="96" height="20" rx="10" fill="#0081FB"/>
        <text x="190" y="210" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="10">LEARN MORE</text>
      </g>
      <!-- Animated Connector Chevrons -->
      <path d="M270 160 L328 160" stroke="#0081FB" stroke-width="3" stroke-dasharray="6 6" stroke-linecap="round"/>
      <path d="M318 150 L330 160 L318 170" fill="none" stroke="#0081FB" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>
      <!-- Right Destination Website Card -->
      <g filter="url(#mtSh)">
        <rect x="348" y="96" width="124" height="132" rx="18" fill="#FFFFFF" stroke="#0081FB" stroke-width="1.8"/>
        <rect x="362" y="110" width="96" height="14" rx="7" fill="#F1F5F9"/>
        <circle cx="372" cy="117" r="3" fill="#0081FB"/>
        <rect x="362" y="136" width="96" height="40" rx="10" fill="#DBEAFE"/>
        <rect x="362" y="186" width="64" height="8" rx="4" fill="#1E293B"/>
        <rect x="362" y="202" width="46" height="8" rx="4" fill="#CBD5E1"/>
      </g>
    </g>
    <!-- Phase 2: Crisp Meta Link / Arrow Emblem + Wordmark -->
    <g class="mt-emblem">
      <rect x="262" y="122" width="76" height="76" rx="22" fill="#0081FB"/>
      <path d="M286 174 L314 146 M292 146 L314 146 L314 168" fill="none" stroke="#FFFFFF" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round"/>
    </g>
    <g class="mt-wordmark">
      <text x="244" y="174" font-family="'Inter', Arial, sans-serif" font-size="42" font-weight="600" fill="#1C2B33" letter-spacing="-0.8">Traffic Ads</text>
    </g>
  </svg>
</div>
""".strip()

SVG_ENGAGEMENT = """
<div class="roasist-brand-stage meta-sub-stage">
  <svg viewBox="0 0 600 320" class="meta-sub-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Meta Engagement Ads">
    <defs>
      <filter id="meSh" x="-15%" y="-15%" width="130%" height="140%">
        <feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#0F172A" flood-opacity="0.08"/>
      </filter>
    </defs>
    <!-- Phase 1: Floating Heart, DM Bubble & WhatsApp Conversation Pills -->
    <g class="me-pill-1" filter="url(#meSh)">
      <rect x="148" y="84" width="136" height="58" rx="29" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <circle cx="178" cy="113" r="18" fill="#E1306C"/>
      <path d="M178 121 C178 121 169 115 169 109.5 C169 106.5 171.5 104.5 174 104.5 C176 104.5 177.5 105.8 178 107 C178.5 105.8 180 104.5 182 104.5 C184.5 104.5 187 106.5 187 109.5 C187 115 178 121 178 121 Z" fill="#FFFFFF"/>
      <rect x="206" y="106" width="58" height="10" rx="5" fill="#1E293B"/>
    </g>
    <g class="me-pill-2" filter="url(#meSh)">
      <rect x="310" y="114" width="144" height="62" rx="22" fill="#FFFFFF" stroke="#0081FB" stroke-width="1.6"/>
      <circle cx="342" cy="145" r="18" fill="#0081FB"/>
      <path d="M334 142 h16 v10 h-10 l-6 4 z" fill="#FFFFFF"/>
      <rect x="370" y="136" width="64" height="8" rx="4" fill="#1E293B"/>
      <rect x="370" y="150" width="44" height="7" rx="3.5" fill="#CBD5E1"/>
    </g>
    <g class="me-pill-3" filter="url(#meSh)">
      <rect x="184" y="176" width="148" height="58" rx="29" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <circle cx="214" cy="205" r="18" fill="#25D366"/>
      <path d="M207 205 a7 7 0 1 1 2.2 5.1 l-3.2 1 l1 -3.1 a7 7 0 0 1 0 -3 Z" fill="none" stroke="#FFFFFF" stroke-width="2.4"/>
      <rect x="242" y="198" width="68" height="10" rx="5" fill="#334155"/>
    </g>
    <!-- Phase 2: Engagement Heart-Chat Emblem + Wordmark -->
    <g class="me-emblem">
      <rect x="260" y="120" width="80" height="74" rx="24" fill="#E1306C"/>
      <polygon points="278,192 278,206 296,192" fill="#E1306C"/>
      <path d="M300 171 C300 171 285 161 285 151.5 C285 146.5 289 143 293.5 143 C296.8 143 299 145 300 147.2 C301 145 303.2 143 306.5 143 C311 143 315 146.5 315 151.5 C315 161 300 171 300 171 Z" fill="#FFFFFF"/>
    </g>
    <g class="me-wordmark">
      <text x="218" y="174" font-family="'Inter', Arial, sans-serif" font-size="40" font-weight="600" fill="#1C2B33" letter-spacing="-0.8">Engagement</text>
    </g>
  </svg>
</div>
""".strip()

SVG_LEADS = """
<div class="roasist-brand-stage meta-sub-stage">
  <svg viewBox="0 0 600 320" class="meta-sub-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Meta Lead Generation Ads">
    <defs>
      <filter id="mlSh" x="-15%" y="-15%" width="130%" height="140%">
        <feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#0F172A" flood-opacity="0.08"/>
      </filter>
    </defs>
    <!-- Phase 1: Meta Instant Lead Form Card Auto-Filling + Verified Check -->
    <g class="ml-form" filter="url(#mlSh)">
      <rect x="196" y="62" width="208" height="196" rx="22" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <!-- Header -->
      <circle cx="226" cy="92" r="12" fill="#0081FB"/>
      <rect x="246" y="84" width="94" height="8" rx="4" fill="#1E293B"/>
      <rect x="246" y="97" width="62" height="6" rx="3" fill="#CBD5E1"/>
      <!-- Auto-fill Input Rows -->
      <rect x="214" y="118" width="172" height="26" rx="8" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.2"/>
      <rect x="224" y="128" width="102" height="7" rx="3.5" fill="#475569"/>
      <rect x="214" y="152" width="172" height="26" rx="8" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.2"/>
      <rect x="224" y="162" width="128" height="7" rx="3.5" fill="#475569"/>
      <!-- Submit Pill -->
      <rect x="214" y="194" width="172" height="36" rx="18" fill="#0081FB"/>
      <text x="300" y="217" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="13">SUBMIT LEAD</text>
      <!-- Verified Floating Badge -->
      <circle cx="400" cy="84" r="18" fill="#10B981"/>
      <path d="M392 84 L397.5 89.5 L409 78" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
    </g>
    <!-- Phase 2: Lead Badge Emblem + Wordmark -->
    <g class="ml-emblem">
      <rect x="262" y="120" width="76" height="80" rx="18" fill="#0081FB"/>
      <rect x="278" y="140" width="44" height="7" rx="3.5" fill="#FFFFFF" opacity="0.9"/>
      <rect x="278" y="155" width="32" height="7" rx="3.5" fill="#FFFFFF" opacity="0.7"/>
      <circle cx="328" cy="188" r="18" fill="#10B981" stroke="#FFFFFF" stroke-width="3"/>
      <path d="M321 188 L326 193 L336 183" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
    </g>
    <g class="ml-wordmark">
      <text x="234" y="174" font-family="'Inter', Arial, sans-serif" font-size="42" font-weight="600" fill="#1C2B33" letter-spacing="-0.8">Lead Ads</text>
    </g>
  </svg>
</div>
""".strip()

SVG_META_APP = """
<div class="roasist-brand-stage meta-sub-stage">
  <svg viewBox="0 0 600 320" class="meta-sub-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Meta App Promotion Ads">
    <defs>
      <linearGradient id="mpGrad" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="#833AB4"/>
        <stop offset="100%" stop-color="#0081FB"/>
      </linearGradient>
      <filter id="mpSh" x="-15%" y="-15%" width="130%" height="140%">
        <feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#0F172A" flood-opacity="0.08"/>
      </filter>
    </defs>
    <!-- Phase 1: Vertical Reels/Story Frame with Bottom App Install Card -->
    <g class="mp-phone" filter="url(#mpSh)">
      <rect x="232" y="54" width="136" height="212" rx="26" fill="#0F172A"/>
      <rect x="242" y="66" width="116" height="188" rx="18" fill="url(#mpGrad)"/>
      <!-- Story progress bars -->
      <rect x="252" y="76" width="44" height="3.5" rx="1.75" fill="#FFFFFF"/>
      <rect x="302" y="76" width="44" height="3.5" rx="1.75" fill="#FFFFFF" opacity="0.4"/>
      <!-- App Overlay Card inside Story -->
      <rect x="250" y="174" width="100" height="70" rx="14" fill="#FFFFFF"/>
      <rect x="258" y="182" width="28" height="28" rx="8" fill="#0081FB"/>
      <rect x="292" y="186" width="48" height="7" rx="3.5" fill="#1E293B"/>
      <rect x="292" y="198" width="34" height="6" rx="3" fill="#F59E0B"/>
      <rect x="258" y="216" width="84" height="20" rx="10" fill="#0081FB"/>
      <text x="300" y="230" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="10">INSTALL</text>
    </g>
    <!-- Phase 2: App Promotion Emblem + Wordmark -->
    <g class="mp-emblem">
      <rect x="262" y="122" width="76" height="76" rx="22" fill="url(#mpGrad)"/>
      <path d="M300 142 L300 172 M288 161 L300 173 L312 161" fill="none" stroke="#FFFFFF" stroke-width="5.5" stroke-linecap="round" stroke-linejoin="round"/>
      <line x1="285" y1="181" x2="315" y2="181" stroke="#FFFFFF" stroke-width="4.5" stroke-linecap="round"/>
    </g>
    <g class="mp-wordmark">
      <text x="206" y="174" font-family="'Inter', Arial, sans-serif" font-size="38" font-weight="600" fill="#1C2B33" letter-spacing="-0.8">App Promotion</text>
    </g>
  </svg>
</div>
""".strip()

SVG_SALES_ASC = """
<div class="roasist-brand-stage meta-sub-stage">
  <svg viewBox="0 0 600 320" class="meta-sub-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Meta Sales and Advantage+ Shopping">
    <defs>
      <linearGradient id="msGrad" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="#0081FB"/>
        <stop offset="100%" stop-color="#7602FF"/>
      </linearGradient>
      <filter id="msSh" x="-15%" y="-15%" width="130%" height="140%">
        <feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#0F172A" flood-opacity="0.08"/>
      </filter>
    </defs>
    <!-- Phase 1: 3 Dynamic Catalog Product Cards (DPA / ASC) -->
    <g class="ms-card-1" filter="url(#msSh)">
      <rect x="128" y="94" width="104" height="134" rx="16" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <rect x="142" y="108" width="76" height="62" rx="10" fill="#F3E8FF"/>
      <circle cx="180" cy="139" r="15" fill="#833AB4"/>
      <rect x="142" y="182" width="54" height="8" rx="4" fill="#CBD5E1"/>
      <rect x="142" y="198" width="48" height="18" rx="9" fill="#DBEAFE"/>
      <text x="166" y="211" text-anchor="middle" fill="#0081FB" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="10.5">DPA</text>
    </g>
    <g class="ms-card-2" filter="url(#msSh)">
      <rect x="248" y="76" width="104" height="152" rx="18" fill="#FFFFFF" stroke="#0081FB" stroke-width="1.8"/>
      <rect x="262" y="90" width="76" height="68" rx="10" fill="#EFF6FF"/>
      <path d="M285 112 h30 l4 28 h-38 z" fill="#0081FB"/>
      <path d="M292 112 a8 8 0 0 1 16 0" fill="none" stroke="#0081FB" stroke-width="2.8"/>
      <rect x="262" y="170" width="64" height="9" rx="4.5" fill="#1E293B"/>
      <rect x="262" y="186" width="46" height="7" rx="3.5" fill="#CBD5E1"/>
      <rect x="262" y="200" width="62" height="18" rx="9" fill="#10B981"/>
      <text x="293" y="213" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="10.5">ASC ↑</text>
    </g>
    <g class="ms-card-3" filter="url(#msSh)">
      <rect x="368" y="94" width="104" height="134" rx="16" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <rect x="382" y="108" width="76" height="62" rx="10" fill="#FCE7F3"/>
      <circle cx="420" cy="139" r="15" fill="#E1306C"/>
      <path d="M413 139 L418 144 L428 134" fill="none" stroke="#FFFFFF" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/>
      <rect x="382" y="182" width="56" height="8" rx="4" fill="#CBD5E1"/>
      <rect x="382" y="198" width="48" height="18" rx="9" fill="#ECFDF5"/>
      <text x="406" y="211" text-anchor="middle" fill="#059669" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="10.5">CAPI</text>
    </g>
    <!-- Phase 2: Shopping Bag + Advantage+ Spark Emblem + Wordmark -->
    <g class="ms-emblem">
      <rect x="262" y="122" width="76" height="76" rx="22" fill="url(#msGrad)"/>
      <path d="M284 148 h32 l4 32 h-40 z" fill="#FFFFFF"/>
      <path d="M291 148 a9 9 0 0 1 18 0" fill="none" stroke="#FFFFFF" stroke-width="3.2"/>
    </g>
    <g class="ms-wordmark">
      <text x="220" y="174" font-family="'Inter', Arial, sans-serif" font-size="40" font-weight="600" fill="#1C2B33" letter-spacing="-0.8">Sales &amp; ASC</text>
    </g>
  </svg>
</div>
""".strip()

META_STAGES_CSS = f"""<style id="{STYLE_ID}">
/* Bespoke White-Stage Brand-Motion SVG Animations for Meta Ads Sub-Page (6 ODAX Objectives) */
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
.roasist-brand-stage.meta-sub-stage {{
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
.meta-sub-svg {{
  width: 92%;
  max-width: 580px;
  height: auto;
  display: block;
}}
.TextImageRows_textImageRows__lOU02 .TextImageRows_buttonContainer___PqVy {{
  display: none !important;
}}

/* 1. Awareness */
.ma-radar {{ transform-origin: 300px 160px; animation: mPhase1Pop 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }}
.ma-pulse {{ transform-origin: 300px 160px; animation: maPulse 7s ease-out infinite; }}
.ma-emblem {{ transform-origin: 300px 160px; animation: mEmblem148 7s cubic-bezier(0.25, 1, 0.5, 1) infinite; }}
.ma-wordmark {{ animation: mWord 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }}
@keyframes maPulse {{ 0%,10% {{ opacity:0; transform:scale(.9); }} 16% {{ opacity:.7; transform:scale(1.1); }} 30%,100% {{ opacity:0; transform:scale(2.4); }} }}

/* 2. Traffic */
.mt-flow {{ transform-origin: 300px 160px; animation: mPhase1Slide 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }}
.mt-emblem {{ transform-origin: 300px 160px; animation: mEmblem130 7s cubic-bezier(0.25, 1, 0.5, 1) infinite; }}
.mt-wordmark {{ animation: mWord 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }}

/* 3. Engagement */
.me-pill-1 {{ transform-origin: 216px 113px; animation: mePill1 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }}
.me-pill-2 {{ transform-origin: 382px 145px; animation: mePill2 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }}
.me-pill-3 {{ transform-origin: 258px 205px; animation: mePill3 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }}
.me-emblem {{ transform-origin: 300px 160px; animation: mEmblem148 7s cubic-bezier(0.25, 1, 0.5, 1) infinite; }}
.me-wordmark {{ animation: mWord 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }}
@keyframes mePill1 {{ 0% {{ opacity:0; transform:translateY(22px) scale(.88); }} 12%,29% {{ opacity:1; transform:translateY(0) scale(1); }} 37%,100% {{ opacity:0; transform:translateX(44px) scale(.6); }} }}
@keyframes mePill2 {{ 0%,5% {{ opacity:0; transform:translateX(24px) scale(.88); }} 16%,29% {{ opacity:1; transform:translateX(0) scale(1); }} 37%,100% {{ opacity:0; transform:translateX(-44px) scale(.6); }} }}
@keyframes mePill3 {{ 0%,9% {{ opacity:0; transform:translateY(24px) scale(.88); }} 19%,29% {{ opacity:1; transform:translateY(0) scale(1); }} 37%,100% {{ opacity:0; transform:translateY(-24px) scale(.6); }} }}

/* 4. Leads */
.ml-form {{ transform-origin: 300px 160px; animation: mPhase1Slide 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }}
.ml-emblem {{ transform-origin: 300px 160px; animation: mEmblem136 7s cubic-bezier(0.25, 1, 0.5, 1) infinite; }}
.ml-wordmark {{ animation: mWord 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }}

/* 5. App Promotion */
.mp-phone {{ transform-origin: 300px 160px; animation: mPhase1Slide 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }}
.mp-emblem {{ transform-origin: 300px 160px; animation: mEmblem158 7s cubic-bezier(0.25, 1, 0.5, 1) infinite; }}
.mp-wordmark {{ animation: mWord 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }}

/* 6. Sales & ASC */
.ms-card-1 {{ transform-origin: 180px 160px; animation: msCard1 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }}
.ms-card-2 {{ transform-origin: 300px 152px; animation: msCard2 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }}
.ms-card-3 {{ transform-origin: 420px 160px; animation: msCard3 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }}
.ms-emblem {{ transform-origin: 300px 160px; animation: mEmblem148 7s cubic-bezier(0.25, 1, 0.5, 1) infinite; }}
.ms-wordmark {{ animation: mWord 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }}
@keyframes msCard1 {{ 0% {{ opacity:0; transform:translateY(34px) rotate(-6deg) scale(.88); }} 12%,29% {{ opacity:1; transform:translateY(0) rotate(-3deg) scale(1); }} 37%,100% {{ opacity:0; transform:translateX(84px) scale(.5); }} }}
@keyframes msCard2 {{ 0%,4% {{ opacity:0; transform:translateY(40px) scale(.88); }} 15%,29% {{ opacity:1; transform:translateY(0) scale(1); }} 37%,100% {{ opacity:0; transform:scale(.5); }} }}
@keyframes msCard3 {{ 0%,8% {{ opacity:0; transform:translateY(34px) rotate(6deg) scale(.88); }} 18%,29% {{ opacity:1; transform:translateY(0) rotate(3deg) scale(1); }} 37%,100% {{ opacity:0; transform:translateX(-84px) scale(.5); }} }}

@keyframes mPhase1Pop {{ 0% {{ opacity:0; transform:scale(.68); }} 13%,30% {{ opacity:1; transform:scale(1); }} 38%,100% {{ opacity:0; transform:scale(.45); }} }}
@keyframes mPhase1Slide {{ 0% {{ opacity:0; transform:translateY(24px) scale(.9); }} 13%,30% {{ opacity:1; transform:translateY(0) scale(1); }} 38%,100% {{ opacity:0; transform:translateY(-16px) scale(.65); }} }}
@keyframes mEmblem130 {{ 0%,35% {{ opacity:0; transform:translateX(0) scale(.6); }} 44% {{ opacity:1; transform:translateX(0) scale(1.06); }} 53% {{ opacity:1; transform:translateX(0) scale(.76); }} 62%,92% {{ opacity:1; transform:translateX(-130px) scale(.76); }} 98%,100% {{ opacity:0; transform:translateX(-130px) scale(.76); }} }}
@keyframes mEmblem136 {{ 0%,35% {{ opacity:0; transform:translateX(0) scale(.6); }} 44% {{ opacity:1; transform:translateX(0) scale(1.06); }} 53% {{ opacity:1; transform:translateX(0) scale(.76); }} 62%,92% {{ opacity:1; transform:translateX(-136px) scale(.76); }} 98%,100% {{ opacity:0; transform:translateX(-136px) scale(.76); }} }}
@keyframes mEmblem148 {{ 0%,35% {{ opacity:0; transform:translateX(0) scale(.6); }} 44% {{ opacity:1; transform:translateX(0) scale(1.06); }} 53% {{ opacity:1; transform:translateX(0) scale(.76); }} 62%,92% {{ opacity:1; transform:translateX(-148px) scale(.76); }} 98%,100% {{ opacity:0; transform:translateX(-148px) scale(.76); }} }}
@keyframes mEmblem158 {{ 0%,35% {{ opacity:0; transform:translateX(0) scale(.6); }} 44% {{ opacity:1; transform:translateX(0) scale(1.06); }} 53% {{ opacity:1; transform:translateX(0) scale(.74); }} 62%,92% {{ opacity:1; transform:translateX(-158px) scale(.74); }} 98%,100% {{ opacity:0; transform:translateX(-158px) scale(.74); }} }}
@keyframes mWord {{ 0%,58% {{ opacity:0; transform:translateX(-16px); }} 67%,92% {{ opacity:1; transform:translateX(0); }} 98%,100% {{ opacity:0; transform:translateX(0); }} }}
</style>"""

STAGES_HTML = [
    SVG_AWARENESS,
    SVG_TRAFFIC,
    SVG_ENGAGEMENT,
    SVG_LEADS,
    SVG_META_APP,
    SVG_SALES_ASC,
]

MOUNT_SCRIPT = f"""<script id="{SCRIPT_ID}">
(function() {{
  var STAGES = {json.dumps(STAGES_HTML, ensure_ascii=False)};
  function mount() {{
    var medias = document.querySelectorAll('.TextImageRows_textImageRows__lOU02 .TextImageRows_media__twu3R');
    medias.forEach(function(fig, idx) {{
      if (idx >= STAGES.length) return;
      if (fig.querySelector('.meta-sub-stage')) return;
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
        text = style_re.sub(META_STAGES_CSS, text, count=1)
    else:
        head_end = text.find("</head>")
        if head_end == -1:
            raise RuntimeError(f"No </head> in {target_path}")
        text = text[:head_end] + META_STAGES_CSS + text[head_end:]

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
    print(f"[OK] Updated 6 Meta Ads campaigns (no buttons) + 6 SVG stages in {os.path.relpath(target_path, REPO_ROOT)} ({len(text):,} bytes)")


def main():
    jobs = [
        (
            os.path.join(REPO_ROOT, "public", "kota-roasist-local.html"),
            os.path.join(REPO_ROOT, "public", "hizmetler", "performans-pazarlamasi", "instagram-reklamlari", "index.html"),
            False,
            False,
        ),
        (
            os.path.join(REPO_ROOT, "public", "kota-roasist-local.html"),
            os.path.join(REPO_ROOT, "public", "hizmetler", "instagram-reklamlari", "index.html"),
            False,
            False,
        ),
        (
            os.path.join(REPO_ROOT, "public", "en", "index.html"),
            os.path.join(REPO_ROOT, "public", "en", "instagram-ads", "index.html"),
            True,
            False,
        ),
        (
            os.path.join(REPO_ROOT, "dist", "index.html"),
            os.path.join(REPO_ROOT, "dist", "hizmetler", "performans-pazarlamasi", "instagram-reklamlari", "index.html"),
            False,
            True,
        ),
        (
            os.path.join(REPO_ROOT, "dist", "index.html"),
            os.path.join(REPO_ROOT, "dist", "hizmetler", "instagram-reklamlari", "index.html"),
            False,
            True,
        ),
        (
            os.path.join(REPO_ROOT, "dist", "en", "index.html"),
            os.path.join(REPO_ROOT, "dist", "en", "instagram-ads", "index.html"),
            True,
            True,
        ),
    ]

    for home_src, target, is_en, is_gh in jobs:
        if not os.path.exists(home_src) or not os.path.exists(target):
            print(f"[SKIP] Missing {os.path.relpath(target, REPO_ROOT)} or {os.path.relpath(home_src, REPO_ROOT)}")
            continue
        stats = get_homepage_statistics(home_src)
        sync_stats(target, stats, is_en=is_en, is_gh_pages=is_gh)
        update_process(target, EN_STEPS if is_en else TR_STEPS, is_en=is_en, is_gh_pages=is_gh)
        update_campaigns_and_stages(target, EN_META_CAMPAIGNS if is_en else TR_META_CAMPAIGNS, is_gh_pages=is_gh)


if __name__ == "__main__":
    main()
