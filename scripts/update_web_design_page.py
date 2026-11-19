#!/usr/bin/env python3
"""
Upgrades Web Design pages (TR: /hizmetler/web-tasarim/, EN: /en/web-design/)
in both public/ and dist/:
  1. 6 bespoke Web Design & Development service cards (UI/UX, E-Commerce, Responsive,
     Core Web Vitals & SEO, CRO Landing Pages, Custom Engineering & CMS) with 6 bespoke
     white-stage SVG + CSS brand-motion animations (no 'Detaylı İncele' buttons).
  2. Synced 5 Homepage 'ÖLÇÜLEBİLİR SONUÇLAR' / 'MEASURABLE RESULTS' dark case-study
     cards + heading + Turkish diacritic top-clearance fix.
  3. Upgraded 6-step Web Design-specific 'Hizmet Sürecimiz' cards (zero duplicate sections).
"""
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

from sync_performans_statistics_cards import get_homepage_statistics, update_target_page as sync_stats
from update_performans_process import update_page as update_process
from update_tiktok_yandex_pages import update_channel_campaigns

# ---------------------------------------------------------------------------
# 6 Web Design & Development Service Cards (TR & EN)
# ---------------------------------------------------------------------------

TR_WEB_SERVICES = [
    {
        "title": "Kurumsal Web Tasarım & UI/UX",
        "desc": "Hazır şablonlardan uzak, markanızın karakterini yansıtan modern tipografi, güçlü görsel hiyerarşi ve sezgisel kullanıcı deneyimiyle güven veren kurumsal web siteleri tasarlıyoruz.",
    },
    {
        "title": "E-Ticaret & Yüksek Dönüşümlü Mağaza",
        "desc": "Hızlı ürün keşfi, sürtünmesiz ödeme adımları ve mobil alışveriş deneyimiyle sepet terk oranlarını düşüren, ROAS ve satış odaklı e-ticaret altyapıları kuruyoruz.",
    },
    {
        "title": "Mobil Öncelikli & Responsive Mimari",
        "desc": "Masaüstü, tablet ve tüm mobil ekranlarda piksel hassasiyetinde kusursuz çalışan, dokunmatik ergonomiye sahip akıcı arayüzler geliştiriyoruz.",
    },
    {
        "title": "Hız, Core Web Vitals & Teknik SEO",
        "desc": "Milisaniyeler içinde açılan, 95+ Core Web Vitals skorlarına sahip, temiz semantik HTML ve yapısal veri (Schema) uyumlu arama motoru dostu siteler kodluyoruz.",
    },
    {
        "title": "Dönüşüm Odaklı Landing Page (CRO)",
        "desc": "Google, Meta ve performans reklamlarınızdan gelen trafiği maksimum düzeyde form, arama ve satışa dönüştüren A/B testine hazır yüksek performanslı iniş sayfaları üretiyoruz.",
    },
    {
        "title": "Özel Yazılım, CMS & Entegrasyonlar",
        "desc": "Kolay içerik yönetimi, CRM, ödeme sistemleri, çoklu dil desteği ve API entegrasyonlarıyla iş süreçlerinize tam uyum sağlayan ölçeklenebilir web çözümleri geliştiriyoruz.",
    },
]

EN_WEB_SERVICES = [
    {
        "title": "Bespoke UI/UX & Brand Websites",
        "desc": "We craft template-free, brand-defining digital experiences with crisp typography, deliberate visual hierarchy, and intuitive user journeys that build instant authority.",
    },
    {
        "title": "High-Converting E-Commerce Stores",
        "desc": "We engineer fast, frictionless online stores designed for effortless product discovery, streamlined checkout flows, and higher average order value.",
    },
    {
        "title": "Mobile-First & Responsive Architecture",
        "desc": "Every layout is engineered mobile-first for fluid, pixel-sharp responsiveness and effortless thumb ergonomics across phones, tablets, and widescreen displays.",
    },
    {
        "title": "Speed, Core Web Vitals & Technical SEO",
        "desc": "Sub-second load times, 95+ Core Web Vitals scores, clean semantic markup, and structured Schema data built in from line one so Google and AI engines love your site.",
    },
    {
        "title": "Conversion-Engineered Landing Pages (CRO)",
        "desc": "Purpose-built landing pages for paid search and social campaigns—structured for maximum lead capture, rapid A/B testing, and lower acquisition costs.",
    },
    {
        "title": "Custom Engineering, CMS & Integrations",
        "desc": "Scalable modern stacks with intuitive CMS workflows, multi-language support, CRM pipelines, payment gateways, and custom API integrations.",
    },
]

# ---------------------------------------------------------------------------
# 6 Bespoke Web Design Process Steps (TR & EN)
# ---------------------------------------------------------------------------

WEB_TR_STEPS = [
    {
        "num": "01",
        "heading": "Keşif & UX Araştırması",
        "text": "Markanızı, hedef kitlenizi, rakiplerinizi ve kullanıcı yolculuklarını analiz eder; bilgi mimarisini (site haritası) ve dönüşüm hedeflerini netleştiririz.",
    },
    {
        "num": "02",
        "heading": "Wireframe & Prototipleme",
        "text": "Görsel tasarıma geçmeden önce sayfa hiyerarşisini, içerik akışını ve etkileşimli prototipleri oluşturarak kusursuz kullanıcı deneyimi kurgularız.",
    },
    {
        "num": "03",
        "heading": "Özel UI & Marka Tasarımı",
        "text": "Şablonlardan uzak, markanızın kimliğine özgü tipografi, renk sistemi ve mikro-etkileşimlerle mobil öncelikli modern arayüzler tasarlarız.",
    },
    {
        "num": "04",
        "heading": "Temiz Kod & CMS Geliştirme",
        "text": "Modern web teknolojileri ve esnek CMS altyapılarıyla yüksek hızlı, güvenli, kolay yönetilebilir ve ölçeklenebilir web yazılımı geliştiririz.",
    },
    {
        "num": "05",
        "heading": "Hız, SEO & QA Testleri",
        "text": "Core Web Vitals performansını, teknik SEO/schema yapısını, tüm cihaz ve tarayıcı uyumluluğunu titizlikle test edip optimize ederiz.",
    },
    {
        "num": "06",
        "heading": "Yayın, Analitik & Sürekli Destek",
        "text": "GA4, dönüşüm takibi ve ısı haritası entegrasyonlarıyla sitenizi yayına alır; canlı verilerle sürekli CRO iyileştirmeleri yaparız.",
    },
]

WEB_EN_STEPS = [
    {
        "num": "01",
        "heading": "Discovery & UX Research",
        "text": "We analyze your brand, audience, competitors, and user journeys to define clear information architecture, sitemaps, and conversion goals.",
    },
    {
        "num": "02",
        "heading": "Wireframing & Prototyping",
        "text": "Before visual styling begins, we map page hierarchy, content flow, and interactive prototypes to validate effortless usability.",
    },
    {
        "num": "03",
        "heading": "Bespoke UI & Brand Craft",
        "text": "We design mobile-first interfaces with custom typography, refined color systems, and natural micro-interactions tailored strictly to your brand.",
    },
    {
        "num": "04",
        "heading": "Clean Code & CMS Build",
        "text": "We engineer fast, secure, maintainable websites and flexible CMS setups built on modern frameworks for long-term scalability.",
    },
    {
        "num": "05",
        "heading": "Speed, SEO & QA Testing",
        "text": "We audit Core Web Vitals, technical SEO/Schema markup, accessibility, and cross-device compatibility before launch.",
    },
    {
        "num": "06",
        "heading": "Launch, Analytics & CRO",
        "text": "We deploy with GA4, conversion tracking, and heatmaps—continuously optimizing conversion rates using real user data.",
    },
]

# ---------------------------------------------------------------------------
# 6 Bespoke White-Stage Brand-Motion SVG Animations for Web Design
# ---------------------------------------------------------------------------

SVG_WEB_UIUX = """
<div class="roasist-brand-stage wd-sub-stage">
  <svg viewBox="0 0 600 320" class="sub-brand-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="UI/UX Web Design">
    <defs><filter id="wdSh1" x="-15%" y="-15%" width="130%" height="140%"><feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#0F172A" flood-opacity="0.08"/></filter></defs>
    <g class="sub-p1-slide" filter="url(#wdSh1)">
      <rect x="136" y="64" width="328" height="192" rx="18" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <rect x="136" y="64" width="328" height="32" rx="18" fill="#F8FAFC"/>
      <circle cx="158" cy="80" r="4.5" fill="#F87171"/>
      <circle cx="172" cy="80" r="4.5" fill="#FBBF24"/>
      <circle cx="186" cy="80" r="4.5" fill="#34D399"/>
      <!-- Hero Wireframe Layout -->
      <rect x="156" y="114" width="132" height="14" rx="7" fill="#0F172A"/>
      <rect x="156" y="136" width="106" height="8" rx="4" fill="#CBD5E1"/>
      <rect x="156" y="152" width="84" height="8" rx="4" fill="#CBD5E1"/>
      <rect x="156" y="176" width="76" height="24" rx="12" fill="#7602FF"/>
      <!-- Visual Canvas Card with Selection Handles -->
      <rect x="312" y="112" width="132" height="122" rx="14" fill="#F5F3FF" stroke="#7602FF" stroke-width="1.6" stroke-dasharray="5 4"/>
      <circle cx="378" cy="173" r="28" fill="#7602FF" opacity="0.16"/>
      <circle cx="378" cy="173" r="14" fill="#7602FF"/>
      <rect x="308" y="108" width="8" height="8" rx="2" fill="#FFFFFF" stroke="#7602FF" stroke-width="1.8"/>
      <rect x="440" y="108" width="8" height="8" rx="2" fill="#FFFFFF" stroke="#7602FF" stroke-width="1.8"/>
      <rect x="308" y="230" width="8" height="8" rx="2" fill="#FFFFFF" stroke="#7602FF" stroke-width="1.8"/>
      <rect x="440" y="230" width="8" height="8" rx="2" fill="#FFFFFF" stroke="#7602FF" stroke-width="1.8"/>
    </g>
    <g class="sub-emblem-144">
      <rect x="262" y="122" width="76" height="76" rx="20" fill="#0F172A"/>
      <rect x="276" y="136" width="22" height="48" rx="6" fill="#7602FF"/>
      <rect x="304" y="136" width="20" height="20" rx="6" fill="#FFFFFF"/>
      <rect x="304" y="162" width="20" height="22" rx="6" fill="#38BDF8"/>
    </g>
    <g class="sub-wordmark"><text x="220" y="174" font-family="'Inter', Arial, sans-serif" font-size="40" font-weight="700" fill="#0F172A" letter-spacing="-0.8">UI/UX Design</text></g>
  </svg>
</div>
""".strip()

SVG_WEB_ECOM = """
<div class="roasist-brand-stage wd-sub-stage">
  <svg viewBox="0 0 600 320" class="sub-brand-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="E-Commerce Web Design">
    <defs><filter id="wdSh2" x="-15%" y="-15%" width="130%" height="140%"><feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#0F172A" flood-opacity="0.08"/></filter></defs>
    <g class="sub-card-1" filter="url(#wdSh2)">
      <rect x="128" y="94" width="104" height="134" rx="16" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <rect x="142" y="108" width="76" height="62" rx="10" fill="#F1F5F9"/>
      <circle cx="180" cy="139" r="14" fill="#0F172A"/>
      <rect x="142" y="182" width="54" height="8" rx="4" fill="#CBD5E1"/>
      <rect x="142" y="198" width="48" height="18" rx="9" fill="#ECFDF5"/>
      <text x="166" y="211" text-anchor="middle" fill="#059669" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="10">CART</text>
    </g>
    <g class="sub-card-2" filter="url(#wdSh2)">
      <rect x="248" y="76" width="104" height="152" rx="18" fill="#FFFFFF" stroke="#7602FF" stroke-width="1.8"/>
      <rect x="262" y="90" width="76" height="68" rx="10" fill="#F5F3FF"/>
      <path d="M285 112 h30 l4 28 h-38 z" fill="#7602FF"/>
      <path d="M292 112 a8 8 0 0 1 16 0" fill="none" stroke="#7602FF" stroke-width="2.8"/>
      <rect x="262" y="170" width="64" height="9" rx="4.5" fill="#0F172A"/>
      <rect x="262" y="186" width="46" height="7" rx="3.5" fill="#CBD5E1"/>
      <rect x="262" y="200" width="66" height="18" rx="9" fill="#10B981"/>
      <text x="295" y="213" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="10">CHECKOUT</text>
    </g>
    <g class="sub-card-3" filter="url(#wdSh2)">
      <rect x="368" y="94" width="104" height="134" rx="16" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <rect x="382" y="108" width="76" height="62" rx="10" fill="#EFF6FF"/>
      <circle cx="420" cy="139" r="14" fill="#0EA5E9"/>
      <path d="M414 139 L418.5 143.5 L427 135" fill="none" stroke="#FFFFFF" stroke-width="2.6" stroke-linecap="round"/>
      <rect x="382" y="182" width="56" height="8" rx="4" fill="#CBD5E1"/>
      <rect x="382" y="198" width="48" height="18" rx="9" fill="#F5F3FF"/>
      <text x="406" y="211" text-anchor="middle" fill="#7602FF" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="10">PAY</text>
    </g>
    <g class="sub-emblem-144">
      <rect x="262" y="122" width="76" height="76" rx="22" fill="#7602FF"/>
      <path d="M284 148 h32 l4 32 h-40 z" fill="#FFFFFF"/>
      <path d="M291 148 a9 9 0 0 1 18 0" fill="none" stroke="#FFFFFF" stroke-width="3.2"/>
    </g>
    <g class="sub-wordmark"><text x="220" y="174" font-family="'Inter', Arial, sans-serif" font-size="40" font-weight="700" fill="#0F172A" letter-spacing="-0.8">E-Commerce</text></g>
  </svg>
</div>
""".strip()

SVG_WEB_RESPONSIVE = """
<div class="roasist-brand-stage wd-sub-stage">
  <svg viewBox="0 0 600 320" class="sub-brand-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Responsive Mobile-First Design">
    <defs><filter id="wdSh3" x="-15%" y="-15%" width="130%" height="140%"><feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#0F172A" flood-opacity="0.08"/></filter></defs>
    <g class="sub-p1-pop" filter="url(#wdSh3)">
      <!-- Desktop Viewport -->
      <rect x="132" y="76" width="246" height="164" rx="16" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.8"/>
      <rect x="148" y="96" width="104" height="12" rx="6" fill="#0F172A"/>
      <rect x="148" y="118" width="84" height="8" rx="4" fill="#CBD5E1"/>
      <rect x="148" y="138" width="214" height="82" rx="10" fill="#F8FAFC"/>
      <rect x="162" y="152" width="88" height="54" rx="8" fill="#EFF6FF"/>
      <rect x="262" y="152" width="86" height="54" rx="8" fill="#F5F3FF"/>
      <!-- Overlapping Mobile Viewport -->
      <rect x="356" y="106" width="112" height="154" rx="22" fill="#0F172A"/>
      <rect x="364" y="118" width="96" height="130" rx="14" fill="#FFFFFF"/>
      <rect x="374" y="130" width="54" height="8" rx="4" fill="#0F172A"/>
      <rect x="374" y="146" width="76" height="44" rx="8" fill="#F5F3FF"/>
      <rect x="374" y="198" width="76" height="36" rx="8" fill="#EFF6FF"/>
      <rect x="398" y="240" width="28" height="3.5" rx="1.75" fill="#CBD5E1"/>
    </g>
    <g class="sub-emblem-152">
      <rect x="256" y="128" width="66" height="54" rx="12" fill="#0F172A"/>
      <rect x="264" y="136" width="50" height="38" rx="6" fill="#38BDF8"/>
      <rect x="304" y="144" width="38" height="54" rx="10" fill="#7602FF" stroke="#FFFFFF" stroke-width="3"/>
      <rect x="313" y="154" width="20" height="28" rx="4" fill="#FFFFFF" opacity="0.9"/>
    </g>
    <g class="sub-wordmark"><text x="206" y="174" font-family="'Inter', Arial, sans-serif" font-size="38" font-weight="700" fill="#0F172A" letter-spacing="-0.8">Responsive UI</text></g>
  </svg>
</div>
""".strip()

SVG_WEB_SPEED = """
<div class="roasist-brand-stage wd-sub-stage">
  <svg viewBox="0 0 600 320" class="sub-brand-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Core Web Vitals 100 Speed">
    <defs><filter id="wdSh4" x="-15%" y="-15%" width="130%" height="140%"><feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#0F172A" flood-opacity="0.07"/></filter></defs>
    <g class="sub-p1-pop" filter="url(#wdSh4)">
      <rect x="132" y="84" width="336" height="152" rx="22" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <!-- 3 Lighthouse 100 Gauges -->
      <circle cx="204" cy="152" r="34" fill="#ECFDF5" stroke="#10B981" stroke-width="7"/>
      <text x="204" y="160" text-anchor="middle" fill="#059669" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="22">99</text>
      <text x="204" y="208" text-anchor="middle" fill="#475569" font-family="Inter, Arial, sans-serif" font-weight="600" font-size="11">SPEED</text>

      <circle cx="300" cy="152" r="34" fill="#ECFDF5" stroke="#10B981" stroke-width="7"/>
      <text x="300" y="160" text-anchor="middle" fill="#059669" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="22">100</text>
      <text x="300" y="208" text-anchor="middle" fill="#475569" font-family="Inter, Arial, sans-serif" font-weight="600" font-size="11">SEO</text>

      <circle cx="396" cy="152" r="34" fill="#ECFDF5" stroke="#10B981" stroke-width="7"/>
      <text x="396" y="160" text-anchor="middle" fill="#059669" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="22">100</text>
      <text x="396" y="208" text-anchor="middle" fill="#475569" font-family="Inter, Arial, sans-serif" font-weight="600" font-size="11">VITALS</text>
    </g>
    <g class="sub-emblem-156">
      <circle cx="300" cy="160" r="38" fill="#ECFDF5" stroke="#10B981" stroke-width="8"/>
      <text x="300" y="170" text-anchor="middle" fill="#059669" font-family="Inter, Arial, sans-serif" font-weight="800" font-size="28">100</text>
    </g>
    <g class="sub-wordmark"><text x="202" y="174" font-family="'Inter', Arial, sans-serif" font-size="38" font-weight="700" fill="#0F172A" letter-spacing="-0.8">Core Web Vitals</text></g>
  </svg>
</div>
""".strip()

SVG_WEB_CRO = """
<div class="roasist-brand-stage wd-sub-stage">
  <svg viewBox="0 0 600 320" class="sub-brand-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Conversion Rate Optimization CRO">
    <defs><filter id="wdSh5" x="-15%" y="-15%" width="130%" height="140%"><feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#0F172A" flood-opacity="0.07"/></filter></defs>
    <g class="sub-p1-slide" filter="url(#wdSh5)">
      <rect x="148" y="72" width="304" height="176" rx="22" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <!-- Funnel Tiers -->
      <rect x="180" y="96"  width="240" height="28" rx="14" fill="#F1F5F9"/>
      <rect x="208" y="134" width="184" height="28" rx="14" fill="#DDD6FE"/>
      <rect x="236" y="172" width="128" height="28" rx="14" fill="#7602FF"/>
      <text x="300" y="191" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="12">CONVERT ↑</text>
      <circle cx="424" cy="110" r="18" fill="#10B981"/>
      <path d="M416 110 L421.5 115.5 L433 104" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
    </g>
    <g class="sub-emblem-144">
      <rect x="262" y="122" width="76" height="76" rx="22" fill="#10B981"/>
      <path d="M282 174 L296 158 L306 166 L320 146" fill="none" stroke="#FFFFFF" stroke-width="5.5" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M308 146 L320 146 L320 158" fill="none" stroke="#FFFFFF" stroke-width="5.5" stroke-linecap="round" stroke-linejoin="round"/>
    </g>
    <g class="sub-wordmark"><text x="218" y="174" font-family="'Inter', Arial, sans-serif" font-size="38" font-weight="700" fill="#0F172A" letter-spacing="-0.8">CRO &amp; Funnels</text></g>
  </svg>
</div>
""".strip()

SVG_WEB_STACK = """
<div class="roasist-brand-stage wd-sub-stage">
  <svg viewBox="0 0 600 320" class="sub-brand-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Custom Engineering and CMS">
    <defs><filter id="wdSh6" x="-15%" y="-15%" width="130%" height="140%"><feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#0F172A" flood-opacity="0.09"/></filter></defs>
    <g class="sub-p1-slide" filter="url(#wdSh6)">
      <rect x="148" y="72" width="304" height="176" rx="20" fill="#0F172A"/>
      <circle cx="172" cy="92" r="4.5" fill="#F87171"/>
      <circle cx="186" cy="92" r="4.5" fill="#FBBF24"/>
      <circle cx="200" cy="92" r="4.5" fill="#34D399"/>
      <!-- Clean syntax bars -->
      <rect x="172" y="116" width="68" height="10" rx="5" fill="#7602FF"/>
      <rect x="250" y="116" width="112" height="10" rx="5" fill="#38BDF8"/>
      <rect x="192" y="140" width="96" height="10" rx="5" fill="#34D399"/>
      <rect x="298" y="140" width="76" height="10" rx="5" fill="#94A3B8"/>
      <rect x="192" y="164" width="136" height="10" rx="5" fill="#FBBF24"/>
      <rect x="172" y="188" width="54" height="10" rx="5" fill="#7602FF"/>
      <rect x="372" y="196" width="58" height="26" rx="13" fill="#10B981"/>
      <text x="401" y="213" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="11">API ✓</text>
    </g>
    <g class="sub-emblem-144">
      <rect x="262" y="122" width="76" height="76" rx="22" fill="#0F172A"/>
      <path d="M288 148 L276 160 L288 172 M312 148 L324 160 L312 172" fill="none" stroke="#38BDF8" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
      <line x1="304" y1="144" x2="296" y2="176" stroke="#7602FF" stroke-width="4.5" stroke-linecap="round"/>
    </g>
    <g class="sub-wordmark"><text x="218" y="174" font-family="'Inter', Arial, sans-serif" font-size="38" font-weight="700" fill="#0F172A" letter-spacing="-0.8">Custom Stack</text></g>
  </svg>
</div>
""".strip()

WEB_STAGES = [
    SVG_WEB_UIUX,
    SVG_WEB_ECOM,
    SVG_WEB_RESPONSIVE,
    SVG_WEB_SPEED,
    SVG_WEB_CRO,
    SVG_WEB_STACK,
]


def main():
    jobs = [
        ("public/kota-roasist-local.html", "public/hizmetler/web-tasarim/index.html", False, False),
        ("public/en/index.html", "public/en/web-design/index.html", True, False),
        ("dist/index.html", "dist/hizmetler/web-tasarim/index.html", False, True),
        ("dist/en/index.html", "dist/en/web-design/index.html", True, True),
    ]
    for home_rel, target_rel, is_en, is_gh in jobs:
        home_src = os.path.join(REPO_ROOT, home_rel)
        target = os.path.join(REPO_ROOT, target_rel)
        if not os.path.exists(home_src) or not os.path.exists(target):
            print(f"[SKIP] Missing {target_rel} or {home_rel}")
            continue
        stats = get_homepage_statistics(home_src)
        sync_stats(target, stats, is_en=is_en, is_gh_pages=is_gh)
        update_process(target, WEB_EN_STEPS if is_en else WEB_TR_STEPS, is_en=is_en, is_gh_pages=is_gh)
        update_channel_campaigns(target, "wd", EN_WEB_SERVICES if is_en else TR_WEB_SERVICES, WEB_STAGES, is_gh_pages=is_gh)


if __name__ == "__main__":
    main()
