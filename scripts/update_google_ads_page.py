#!/usr/bin/env python3
"""
Updates all Google Ads detail pages (TR: /hizmetler/performans-pazarlamasi/google-reklamlari/
and /hizmetler/google-reklamlari/, EN: /en/google-ads/) in both public/ and dist/:

  1. Replaces the 3 TextImageRows media blocks (Search, Shopping & PMax, GDN/Display)
     with bespoke, lightweight white-stage SVG + CSS brand-motion animations matching
     the Performance Marketing page style.
  2. Syncs the 5 Homepage 'ÖLÇÜLEBİLİR SONUÇLAR' / 'MEASURABLE RESULTS' dark case-study
     cards + heading + Turkish diacritic top-clearance fix.
  3. Upgrades 'Hizmet Sürecimiz' (Timeline_timeline__KvsOC) to the elevated 6-step
     architectural white card design.
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

STYLE_ID = "roasist-gads-brand-stages-css"
SCRIPT_ID = "roasist-gads-brand-stages-js"

# ---------------------------------------------------------------------------
# 3 Bespoke White-Stage Brand-Motion SVG + CSS Animations for Google Ads
# ---------------------------------------------------------------------------

SVG_SEARCH_ADS = """
<div class="roasist-brand-stage gads-sub-stage gads-search-stage">
  <svg viewBox="0 0 600 320" class="gads-sub-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Google Search Ads">
    <defs>
      <filter id="gsSoftShadow" x="-15%" y="-15%" width="130%" height="140%">
        <feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#0F172A" flood-opacity="0.07"/>
      </filter>
    </defs>

    <!-- Phase 1: Clean Search Bar + Top Sponsored Result + Click Ripple (0% - 36%) -->
    <g class="gs-phase1">
      <!-- Search Pill -->
      <g class="gs-searchbar" filter="url(#gsSoftShadow)">
        <rect x="132" y="76" width="336" height="52" rx="26" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
        <!-- Magnifier inside search bar -->
        <circle cx="164" cy="102" r="9" fill="none" stroke="#4285F4" stroke-width="2.6"/>
        <line x1="170.5" y1="108.5" x2="177" y2="115" stroke="#4285F4" stroke-width="2.6" stroke-linecap="round"/>
        <!-- Animated typing query bar -->
        <rect x="190" y="97" width="168" height="10" rx="5" fill="#CBD5E1" class="gs-query-bar"/>
        <rect x="364" y="91" width="2.5" height="22" rx="1.25" fill="#4285F4" class="gs-cursor"/>
        <!-- 4-color mini dots on right -->
        <circle cx="426" cy="102" r="4" fill="#4285F4"/>
        <circle cx="438" cy="102" r="4" fill="#EA4335"/>
        <circle cx="450" cy="102" r="4" fill="#FBBC05"/>
      </g>

      <!-- Sponsored Top Result Card -->
      <g class="gs-adcard" filter="url(#gsSoftShadow)">
        <rect x="132" y="146" width="336" height="96" rx="18" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
        <!-- Sponsored green badge -->
        <rect x="154" y="164" width="38" height="20" rx="6" fill="#E6F4EA"/>
        <text x="173" y="178" text-anchor="middle" fill="#1E8E3E" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="11">Ad</text>
        <!-- URL line -->
        <rect x="202" y="170" width="112" height="8" rx="4" fill="#E2E8F0"/>
        <!-- Blue Headline Bar -->
        <rect x="154" y="194" width="218" height="12" rx="6" fill="#4285F4"/>
        <!-- Subcopy lines -->
        <rect x="154" y="216" width="176" height="8" rx="4" fill="#CBD5E1"/>
        <!-- High-Intent Conversion Check Badge -->
        <circle cx="430" cy="194" r="20" fill="#34A853" class="gs-check-bg"/>
        <path d="M421 194 L427.5 200.5 L440 187.5" fill="none" stroke="#FFFFFF" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>
        <circle cx="430" cy="194" r="20" fill="none" stroke="#34A853" stroke-width="2" class="gs-ripple"/>
      </g>
    </g>

    <!-- Phase 2: 4-Color Search Emblem + Wordmark (38% - 96%) -->
    <g class="gs-emblem">
      <!-- 4-segment Google ring lens -->
      <path d="M300 108 A38 38 0 0 1 338 146" fill="none" stroke="#4285F4" stroke-width="13" stroke-linecap="round"/>
      <path d="M338 146 A38 38 0 0 1 300 184" fill="none" stroke="#34A853" stroke-width="13" stroke-linecap="round"/>
      <path d="M300 184 A38 38 0 0 1 262 146" fill="none" stroke="#FBBC05" stroke-width="13" stroke-linecap="round"/>
      <path d="M262 146 A38 38 0 0 1 300 108" fill="none" stroke="#EA4335" stroke-width="13" stroke-linecap="round"/>
      <!-- Handle -->
      <line x1="328" y1="174" x2="354" y2="200" stroke="#4285F4" stroke-width="14" stroke-linecap="round"/>
    </g>

    <g class="gs-wordmark">
      <text x="228" y="174" font-family="'Product Sans', 'Inter', Arial, sans-serif" font-size="42" font-weight="600" fill="#202124" letter-spacing="-0.8">
        Search Ads
      </text>
    </g>
  </svg>
</div>
""".strip()

SVG_SHOPPING_PMAX = """
<div class="roasist-brand-stage gads-sub-stage gads-shop-stage">
  <svg viewBox="0 0 600 320" class="gads-sub-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Google Shopping and Performance Max">
    <defs>
      <filter id="shShadow" x="-15%" y="-15%" width="130%" height="140%">
        <feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#0F172A" flood-opacity="0.07"/>
      </filter>
    </defs>

    <!-- Phase 1: 3 E-Commerce Shopping Cards Fanning Upward (0% - 36%) -->
    <g class="sh-phase1">
      <!-- Left Product Card -->
      <g class="sh-card sh-card-1" filter="url(#shShadow)">
        <rect x="128" y="92" width="104" height="136" rx="16" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
        <rect x="142" y="106" width="76" height="62" rx="10" fill="#EFF6FF"/>
        <!-- Bag silhouette -->
        <path d="M167 129 h26 l3 26 h-32 z" fill="#4285F4"/>
        <path d="M173 129 a7 7 0 0 1 14 0" fill="none" stroke="#4285F4" stroke-width="2.5"/>
        <rect x="142" y="180" width="52" height="8" rx="4" fill="#CBD5E1"/>
        <rect x="142" y="196" width="44" height="18" rx="9" fill="#E6F4EA"/>
        <text x="164" y="209" text-anchor="middle" fill="#1E8E3E" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="11">4.9 ★</text>
      </g>

      <!-- Center Featured Product Card -->
      <g class="sh-card sh-card-2" filter="url(#shShadow)">
        <rect x="248" y="76" width="104" height="152" rx="16" fill="#FFFFFF" stroke="#4285F4" stroke-width="1.8"/>
        <rect x="262" y="90" width="76" height="68" rx="10" fill="#FEF3C7"/>
        <!-- Tag icon -->
        <path d="M284 110 h18 l14 14 l-18 18 l-14 -14 z" fill="#FBBC05"/>
        <circle cx="292" cy="118" r="3" fill="#FFFFFF"/>
        <rect x="262" y="170" width="64" height="9" rx="4.5" fill="#1E293B"/>
        <rect x="262" y="186" width="46" height="7" rx="3.5" fill="#CBD5E1"/>
        <rect x="262" y="200" width="56" height="18" rx="9" fill="#34A853"/>
        <text x="290" y="213" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="10.5">ROAS ↑</text>
      </g>

      <!-- Right Product Card -->
      <g class="sh-card sh-card-3" filter="url(#shShadow)">
        <rect x="368" y="92" width="104" height="136" rx="16" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
        <rect x="382" y="106" width="76" height="62" rx="10" fill="#FEE2E2"/>
        <!-- Spark / PMax icon -->
        <path d="M420 120 l4 12 l12 4 l-12 4 l-4 12 l-4 -12 l-12 -4 l12 -4 z" fill="#EA4335"/>
        <rect x="382" y="180" width="58" height="8" rx="4" fill="#CBD5E1"/>
        <rect x="382" y="196" width="48" height="18" rx="9" fill="#DBEAFE"/>
        <text x="406" y="209" text-anchor="middle" fill="#1D4ED8" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="10.5">PMax</text>
      </g>
    </g>

    <!-- Phase 2: Google Shopping Tag + 4-Color PMax Spark + Wordmark (38% - 96%) -->
    <g class="sh-emblem">
      <!-- Price Tag Body -->
      <path d="M264 114 L306 114 L348 156 L306 198 L264 156 Z" fill="#4285F4"/>
      <path d="M264 114 L306 114 L306 156 L264 156 Z" fill="#34A853" opacity="0.92"/>
      <path d="M306 114 L348 156 L306 156 Z" fill="#FBBC05"/>
      <path d="M264 156 L306 156 L306 198 Z" fill="#EA4335"/>
      <!-- Tag Hole -->
      <circle cx="282" cy="132" r="7" fill="#FFFFFF"/>
    </g>

    <g class="sh-wordmark">
      <text x="206" y="173" font-family="'Product Sans', 'Inter', Arial, sans-serif" font-size="38" font-weight="600" fill="#202124" letter-spacing="-0.8">
        Shopping &amp; PMax
      </text>
    </g>
  </svg>
</div>
""".strip()

SVG_DISPLAY_GDN = """
<div class="roasist-brand-stage gads-sub-stage gads-gdn-stage">
  <svg viewBox="0 0 600 320" class="gads-sub-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Google Display Network and Video Ads">
    <defs>
      <filter id="gdShadow" x="-15%" y="-15%" width="130%" height="140%">
        <feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#0F172A" flood-opacity="0.07"/>
      </filter>
    </defs>

    <!-- Phase 1: Multi-Format Responsive Display & Video Grid (0% - 36%) -->
    <g class="gd-phase1">
      <!-- Top Leaderboard Banner -->
      <g class="gd-tile gd-tile-1" filter="url(#gdShadow)">
        <rect x="136" y="76" width="328" height="58" rx="14" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
        <rect x="150" y="90" width="30" height="30" rx="8" fill="#4285F4"/>
        <circle cx="165" cy="105" r="7" fill="#FFFFFF" opacity="0.9"/>
        <rect x="194" y="95" width="132" height="9" rx="4.5" fill="#1E293B"/>
        <rect x="194" y="110" width="88" height="7" rx="3.5" fill="#CBD5E1"/>
        <rect x="394" y="92" width="56" height="26" rx="13" fill="#4285F4"/>
      </g>

      <!-- Bottom-Left Square Visual Ad -->
      <g class="gd-tile gd-tile-2" filter="url(#gdShadow)">
        <rect x="136" y="148" width="152" height="98" rx="16" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
        <rect x="150" y="162" width="124" height="50" rx="10" fill="#FEF3C7"/>
        <circle cx="176" cy="182" r="9" fill="#FBBC05"/>
        <path d="M158 212 L196 184 L222 204 L244 188 L266 212 Z" fill="#34A853" opacity="0.85"/>
        <rect x="150" y="222" width="80" height="8" rx="4" fill="#CBD5E1"/>
      </g>

      <!-- Bottom-Right Video / YouTube Ad Frame -->
      <g class="gd-tile gd-tile-3" filter="url(#gdShadow)">
        <rect x="304" y="148" width="160" height="98" rx="16" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
        <rect x="318" y="162" width="132" height="70" rx="10" fill="#FEF2F2"/>
        <!-- Red Play Pill -->
        <rect x="360" y="180" width="48" height="34" rx="10" fill="#EA4335"/>
        <polygon points="379,189 379,205 393,197" fill="#FFFFFF"/>
      </g>
    </g>

    <!-- Phase 2: Layered Display + Video Emblem + Wordmark (38% - 96%) -->
    <g class="gd-emblem">
      <!-- Back Yellow Frame -->
      <rect x="260" y="114" width="84" height="62" rx="14" fill="#FBBC05" opacity="0.92" transform="rotate(-7 302 145)"/>
      <!-- Mid Blue Frame -->
      <rect x="266" y="124" width="84" height="62" rx="14" fill="#4285F4"/>
      <!-- Front Red Video Badge -->
      <rect x="292" y="144" width="52" height="38" rx="11" fill="#EA4335" stroke="#FFFFFF" stroke-width="3"/>
      <polygon points="313,155 313,171 327,163" fill="#FFFFFF"/>
    </g>

    <g class="gd-wordmark">
      <text x="218" y="173" font-family="'Product Sans', 'Inter', Arial, sans-serif" font-size="38" font-weight="600" fill="#202124" letter-spacing="-0.8">
        Display &amp; Video
      </text>
    </g>
  </svg>
</div>
""".strip()

GADS_STAGES_CSS = f"""<style id="{STYLE_ID}">
/* Bespoke White-Stage Brand-Motion SVG Animations for Google Ads Sub-Page */
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

/* ---- ROW 1: SEARCH ADS ---- */
.gs-searchbar {{ transform-origin: 300px 102px; animation: gsBar 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }}
.gs-query-bar {{ transform-origin: 190px 102px; animation: gsType 7s ease-in-out infinite; }}
.gs-cursor {{ animation: gsBlink 7s steps(2, start) infinite; }}
.gs-adcard {{ transform-origin: 300px 194px; animation: gsCard 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }}
.gs-ripple {{ transform-origin: 430px 194px; animation: gsRipple 7s ease-out infinite; }}
.gs-emblem {{ transform-origin: 300px 154px; animation: gsEmblem 7s cubic-bezier(0.25, 1, 0.5, 1) infinite; }}
.gs-wordmark {{ animation: gsWord 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }}

@keyframes gsBar {{
  0%        {{ opacity: 0; transform: translateY(18px) scale(0.92); }}
  10%, 30%  {{ opacity: 1; transform: translateY(0) scale(1); }}
  38%, 100% {{ opacity: 0; transform: translateY(-16px) scale(0.86); }}
}}
@keyframes gsType {{
  0%, 6%    {{ transform: scaleX(0.15); }}
  18%, 32%  {{ transform: scaleX(1); }}
  40%, 100% {{ transform: scaleX(1); }}
}}
@keyframes gsBlink {{
  0%, 100% {{ opacity: 1; }}
  12%, 22% {{ opacity: 0; }}
}}
@keyframes gsCard {{
  0%, 9%    {{ opacity: 0; transform: translateY(28px) scale(0.94); }}
  19%, 30%  {{ opacity: 1; transform: translateY(0) scale(1); }}
  38%, 100% {{ opacity: 0; transform: translateY(-10px) scale(0.84); }}
}}
@keyframes gsRipple {{
  0%, 18%   {{ opacity: 0; transform: scale(0.9); }}
  22%       {{ opacity: 0.7; transform: scale(1.05); }}
  31%, 100% {{ opacity: 0; transform: scale(1.65); }}
}}
@keyframes gsEmblem {{
  0%, 35%   {{ opacity: 0; transform: translateX(0) scale(0.65) rotate(-24deg); }}
  44%       {{ opacity: 1; transform: translateX(0) scale(1.06) rotate(0deg); }}
  53%       {{ opacity: 1; transform: translateX(0) scale(0.74) rotate(0deg); }}
  62%, 92%  {{ opacity: 1; transform: translateX(-142px) scale(0.74) rotate(0deg); }}
  98%, 100% {{ opacity: 0; transform: translateX(-142px) scale(0.74) rotate(0deg); }}
}}
@keyframes gsWord {{
  0%, 58%   {{ opacity: 0; transform: translateX(-16px); }}
  67%, 92%  {{ opacity: 1; transform: translateX(0); }}
  98%, 100% {{ opacity: 0; transform: translateX(0); }}
}}

/* ---- ROW 2: SHOPPING & PMAX ---- */
.sh-card-1 {{ transform-origin: 180px 160px; animation: shCard1 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }}
.sh-card-2 {{ transform-origin: 300px 152px; animation: shCard2 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }}
.sh-card-3 {{ transform-origin: 420px 160px; animation: shCard3 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }}
.sh-emblem {{ transform-origin: 300px 156px; animation: shEmblem 7s cubic-bezier(0.25, 1, 0.5, 1) infinite; }}
.sh-wordmark {{ animation: shWord 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }}

@keyframes shCard1 {{
  0%        {{ opacity: 0; transform: translateY(36px) rotate(-6deg) scale(0.88); }}
  12%, 29%  {{ opacity: 1; transform: translateY(0) rotate(-3deg) scale(1); }}
  37%, 100% {{ opacity: 0; transform: translateX(90px) scale(0.5); }}
}}
@keyframes shCard2 {{
  0%, 4%    {{ opacity: 0; transform: translateY(42px) scale(0.88); }}
  15%, 29%  {{ opacity: 1; transform: translateY(0) scale(1); }}
  37%, 100% {{ opacity: 0; transform: scale(0.5); }}
}}
@keyframes shCard3 {{
  0%, 8%    {{ opacity: 0; transform: translateY(36px) rotate(6deg) scale(0.88); }}
  18%, 29%  {{ opacity: 1; transform: translateY(0) rotate(3deg) scale(1); }}
  37%, 100% {{ opacity: 0; transform: translateX(-90px) scale(0.5); }}
}}
@keyframes shEmblem {{
  0%, 35%   {{ opacity: 0; transform: translateX(0) scale(0.6) rotate(22deg); }}
  44%       {{ opacity: 1; transform: translateX(0) scale(1.1) rotate(0deg); }}
  53%       {{ opacity: 1; transform: translateX(0) scale(0.76) rotate(0deg); }}
  62%, 92%  {{ opacity: 1; transform: translateX(-162px) scale(0.76) rotate(0deg); }}
  98%, 100% {{ opacity: 0; transform: translateX(-162px) scale(0.76) rotate(0deg); }}
}}
@keyframes shWord {{
  0%, 58%   {{ opacity: 0; transform: translateX(-16px); }}
  67%, 92%  {{ opacity: 1; transform: translateX(0); }}
  98%, 100% {{ opacity: 0; transform: translateX(0); }}
}}

/* ---- ROW 3: DISPLAY & VIDEO (GDN) ---- */
.gd-tile-1 {{ transform-origin: 300px 105px; animation: gdTile1 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }}
.gd-tile-2 {{ transform-origin: 212px 197px; animation: gdTile2 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }}
.gd-tile-3 {{ transform-origin: 384px 197px; animation: gdTile3 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }}
.gd-emblem {{ transform-origin: 304px 154px; animation: gdEmblem 7s cubic-bezier(0.25, 1, 0.5, 1) infinite; }}
.gd-wordmark {{ animation: gdWord 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }}

@keyframes gdTile1 {{
  0%        {{ opacity: 0; transform: translateY(-20px) scale(0.92); }}
  11%, 29%  {{ opacity: 1; transform: translateY(0) scale(1); }}
  37%, 100% {{ opacity: 0; transform: translateY(28px) scale(0.6); }}
}}
@keyframes gdTile2 {{
  0%, 5%    {{ opacity: 0; transform: translateX(-24px) scale(0.9); }}
  15%, 29%  {{ opacity: 1; transform: translateX(0) scale(1); }}
  37%, 100% {{ opacity: 0; transform: translateX(48px) scale(0.55); }}
}}
@keyframes gdTile3 {{
  0%, 9%    {{ opacity: 0; transform: translateX(24px) scale(0.9); }}
  19%, 29%  {{ opacity: 1; transform: translateX(0) scale(1); }}
  37%, 100% {{ opacity: 0; transform: translateX(-48px) scale(0.55); }}
}}
@keyframes gdEmblem {{
  0%, 35%   {{ opacity: 0; transform: translateX(0) scale(0.62); }}
  44%       {{ opacity: 1; transform: translateX(0) scale(1.08); }}
  53%       {{ opacity: 1; transform: translateX(0) scale(0.78); }}
  62%, 92%  {{ opacity: 1; transform: translateX(-156px) scale(0.78); }}
  98%, 100% {{ opacity: 0; transform: translateX(-156px) scale(0.78); }}
}}
@keyframes gdWord {{
  0%, 58%   {{ opacity: 0; transform: translateX(-16px); }}
  67%, 92%  {{ opacity: 1; transform: translateX(0); }}
  98%, 100% {{ opacity: 0; transform: translateX(0); }}
}}
</style>"""

STAGES_HTML = [SVG_SEARCH_ADS, SVG_SHOPPING_PMAX, SVG_DISPLAY_GDN]

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


def inject_gads_stages(target_path, is_gh_pages=False):
    text = open(target_path, "r", encoding="utf-8").read()

    # 1. Inject / replace CSS in <head>
    style_re = re.compile(rf'<style id="{STYLE_ID}">.*?</style>', re.S)
    if style_re.search(text):
        text = style_re.sub(GADS_STAGES_CSS, text, count=1)
    else:
        head_end = text.find("</head>")
        if head_end == -1:
            raise RuntimeError(f"No </head> in {target_path}")
        text = text[:head_end] + GADS_STAGES_CSS + text[head_end:]

    # 2. Replace old KOTA media URLs in TextImageRows with neutral placeholder so zero KOTA videos/images fetch
    placeholder = "/roasist-web/roasist-logo.svg" if is_gh_pages else "/roasist-logo.svg"
    for old_media in [
        "https://kota-content.b-cdn.net/app/uploads/2023/11/Animation-1-Bipsync-1.mp4",
        "https://kota-content.b-cdn.net/app/uploads/2023/11/Web-Development-backrate-2.png",
        "https://kota-content.b-cdn.net/app/uploads/2023/11/Web-Development-backrate-2-500x500.png",
        "https://kota-content.b-cdn.net/app/uploads/2023/11/Web-Development-backrate-2-768x768.png",
        "https://kota-content.b-cdn.net/app/uploads/2023/11/Wordpress-and-cms-mealeo.png",
        "https://kota-content.b-cdn.net/app/uploads/2023/11/Wordpress-and-cms-mealeo-500x500.png",
        "https://kota-content.b-cdn.net/app/uploads/2023/11/Wordpress-and-cms-mealeo-768x768.png",
    ]:
        text = text.replace(old_media, placeholder)

    # 3. Inject / replace mount script before </body>
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
    print(f"[OK] Injected 3x Google Ads SVG stages into {os.path.relpath(target_path, REPO_ROOT)} ({len(text):,} bytes)")


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
        # 2. Update 6-step Process cards
        update_process(target, EN_STEPS if is_en else TR_STEPS, is_en=is_en, is_gh_pages=is_gh)
        # 3. Inject 3x bespoke Google Ads brand-motion SVG stages
        inject_gads_stages(target, is_gh_pages=is_gh)


if __name__ == "__main__":
    main()
