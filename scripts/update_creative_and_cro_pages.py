#!/usr/bin/env python3
"""
Upgrades the remaining two sub-services under 'Web Tasarım & Kreatif Stüdyo':
  1. Grafik & Kreatif Tasarım (/hizmetler/grafik-tasarim/ & /en/graphic-design/)
  2. Dönüşüm Optimizasyonu (CRO) — creates dedicated /hizmetler/donusum-optimizasyonu/
     & /en/conversion-optimization/ pages (cloned from web-tasarim/web-design) and wires
     the Homepage 'Dönüşüm Optimizasyonu (CRO)' pill & route map straight to them.

Both TR & EN, in both public/ and dist/:
  - 5 bespoke service cards + 5 white-stage SVG/CSS brand-motion animations (no buttons).
  - Synced 5 Homepage 'ÖLÇÜLEBİLİR SONUÇLAR' / 'MEASURABLE RESULTS' dark cards + heading.
  - Bespoke 6-step elevated white Process cards (zero duplicate sections).
"""
import os
import re
import shutil
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

from sync_performans_statistics_cards import get_homepage_statistics, update_target_page as sync_stats
from update_performans_process import update_page as update_process
from update_tiktok_yandex_pages import update_channel_campaigns

# ===========================================================================
# 1. GRAFIK & KREATIF TASARIM — 5 Services + 6 Process Steps + 5 SVG Stages
# ===========================================================================

TR_GD_SERVICES = [
    {
        "title": "Performans Reklam Kreatifleri (Meta, TikTok, Google)",
        "desc": "Tıklama oranını (CTR) artıran, ilk 3 saniyede dikkat yakalayan ve A/B testlerine göre sürekli optimize edilen yüksek dönüşümlü performans reklam görselleri üretiyoruz.",
    },
    {
        "title": "Motion Design & Kısa Video Kreatifleri",
        "desc": "Instagram Reels, TikTok, YouTube Shorts ve Display ağları için dinamik hareketli grafikler, ürün animasyonları ve hikaye anlatımı güçlü kısa reklam videoları hazırlıyoruz.",
    },
    {
        "title": "Kurumsal Kimlik & Marka Tasarımı",
        "desc": "Logo, tipografi hiyerarşisi, renk sistemi ve kapsamlı marka kullanım kılavuzuyla (Brandbook) markanıza tüm dijital ve fiziksel kanallarda unutulmaz bir kimlik kazandırıyoruz.",
    },
    {
        "title": "Sosyal Medya Görsel & Grid Yönetimi",
        "desc": "Markanızın ses tonuna ve estetik diline tam uyumlu post, carousel, hikaye ve kapak şablonlarıyla profesyonel, tutarlı ve etkileşimi yüksek bir sosyal medya vitrini kuruyoruz.",
    },
    {
        "title": "Sunum, Katalog & Kurumsal Materyaller",
        "desc": "Yatırımcı sunumları (Pitch Deck), dijital ürün katalogları, broşürler ve kurumsal satış dokümanlarıyla markanızın profesyonel algısını her temas noktasında güçlendiriyoruz.",
    },
]

EN_GD_SERVICES = [
    {
        "title": "Performance Ad Creatives (Meta, TikTok, Google)",
        "desc": "Scroll-stopping static and multi-ratio ad creatives engineered for higher CTR, lower CPA, and systematic A/B creative testing across every paid channel.",
    },
    {
        "title": "Motion Design & Short-Form Video",
        "desc": "Dynamic motion graphics, product showcases, and hook-driven vertical videos crafted specifically for Reels, TikTok, YouTube Shorts, and Display networks.",
    },
    {
        "title": "Brand Identity & Visual Systems",
        "desc": "Distinctive logos, typography systems, color palettes, and comprehensive brand guidelines that establish immediate authority across digital and print.",
    },
    {
        "title": "Social Media Visual & Grid Systems",
        "desc": "Cohesive post templates, editorial carousels, and story frameworks designed to keep your brand feed sharp, recognizable, and high-engagement.",
    },
    {
        "title": "Pitch Decks, Catalogs & Brand Collateral",
        "desc": "High-craft investor pitch decks, digital product catalogs, and sales collateral that elevate your brand perception at every touchpoint.",
    },
]

GD_TR_STEPS = [
    {"num": "01", "heading": "Marka & Brief Analizi", "text": "Markanızın konumlandırmasını, hedef kitlesini, rakiplerini ve kampanya hedeflerini analiz ederek net bir kreatif brief oluştururuz."},
    {"num": "02", "heading": "Konsept & Moodboard", "text": "Görsel dil, tipografi, renk paleti ve sanat yönetimi yönünü belirleyen moodboard ve konsept eskizlerini onayınıza sunarız."},
    {"num": "03", "heading": "Kreatif Tasarım & Varyasyon", "text": "Performans ve estetiği dengeleyen özgün tasarımlar ile A/B testlerine uygun mesaj ve görsel varyasyonları üretiriz."},
    {"num": "04", "heading": "Motion & Format Uyarlama", "text": "Onaylanan konseptleri 9:16, 4:5, 1:1 ve 16:9 reklam formatlarına ve akıcı motion grafiklere kusursuz biçimde uyarlarız."},
    {"num": "05", "heading": "A/B Test & Veri İterasyonu", "text": "Canlı reklamlardan gelen CTR, izlenme ve dönüşüm verilerini okuyarak en çok kazandıran kreatif açıları ölçekleriz."},
    {"num": "06", "heading": "Marka Kılavuzu & Teslim", "text": "Tüm kaynak dosyaları, yeniden kullanılabilir şablonları ve marka kılavuzunu düzenli bir kütüphane halinde teslim ederiz."},
]

GD_EN_STEPS = [
    {"num": "01", "heading": "Brand & Brief Discovery", "text": "We analyze your brand positioning, audience psychology, competitors, and campaign goals to build a sharp creative brief."},
    {"num": "02", "heading": "Concept & Moodboarding", "text": "We align on visual direction, typography, color hierarchy, and art direction through focused moodboards before production."},
    {"num": "03", "heading": "Creative Design & Variants", "text": "We craft distinctive visuals and multiple hook/message variants engineered for real-world A/B testing."},
    {"num": "04", "heading": "Motion & Multi-Ratio Sizing", "text": "We adapt approved concepts seamlessly into 9:16, 4:5, 1:1, and 16:9 placements with crisp motion design."},
    {"num": "05", "heading": "Performance Data Iteration", "text": "We review live CTR, thumbstop rate, and ROAS metrics to double down on winning creative angles."},
    {"num": "06", "heading": "System & Asset Handover", "text": "We deliver organized source files, scalable templates, and brand guidelines ready for your team."},
]

SVG_GD_ADS = """
<div class="roasist-brand-stage gd-sub-stage">
  <svg viewBox="0 0 600 320" class="sub-brand-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Performance Ad Creatives">
    <defs><filter id="gdF1" x="-15%" y="-15%" width="130%" height="140%"><feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#0F172A" flood-opacity="0.08"/></filter></defs>
    <g class="sub-card-1" filter="url(#gdF1)">
      <rect x="128" y="90" width="96" height="144" rx="16" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <rect x="140" y="102" width="72" height="92" rx="10" fill="#F5F3FF"/>
      <circle cx="176" cy="148" r="18" fill="#7602FF"/>
      <rect x="140" y="204" width="46" height="16" rx="8" fill="#0F172A"/>
      <text x="163" y="216" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="9">9:16</text>
    </g>
    <g class="sub-card-2" filter="url(#gdF1)">
      <rect x="242" y="76" width="116" height="158" rx="18" fill="#FFFFFF" stroke="#7602FF" stroke-width="1.8"/>
      <rect x="256" y="90" width="88" height="94" rx="12" fill="#EC4899" opacity="0.14"/>
      <path d="M300 112 l6 18 l18 6 l-18 6 l-6 18 l-6 -18 l-18 -6 l18 -6 z" fill="#EC4899"/>
      <rect x="256" y="196" width="88" height="22" rx="11" fill="#7602FF"/>
      <text x="300" y="211" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="10.5">CTR +42%</text>
    </g>
    <g class="sub-card-3" filter="url(#gdF1)">
      <rect x="376" y="98" width="96" height="128" rx="16" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <rect x="388" y="110" width="72" height="72" rx="10" fill="#EFF6FF"/>
      <rect x="408" y="130" width="32" height="32" rx="8" fill="#0EA5E9"/>
      <rect x="388" y="194" width="44" height="16" rx="8" fill="#E0F2FE"/>
      <text x="410" y="206" text-anchor="middle" fill="#0369A1" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="9">1:1</text>
    </g>
    <g class="sub-emblem-144">
      <rect x="262" y="122" width="76" height="76" rx="22" fill="#7602FF"/>
      <path d="M300 138 l5 15 l15 5 l-15 5 l-5 15 l-5 -15 l-15 -5 l15 -5 z" fill="#FFFFFF"/>
    </g>
    <g class="sub-wordmark"><text x="218" y="174" font-family="'Inter', Arial, sans-serif" font-size="38" font-weight="700" fill="#0F172A" letter-spacing="-0.8">Ad Creatives</text></g>
  </svg>
</div>
""".strip()

SVG_GD_MOTION = """
<div class="roasist-brand-stage gd-sub-stage">
  <svg viewBox="0 0 600 320" class="sub-brand-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Motion Design">
    <defs><filter id="gdF2" x="-15%" y="-15%" width="130%" height="140%"><feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#0F172A" flood-opacity="0.09"/></filter></defs>
    <g class="sub-p1-slide" filter="url(#gdF2)">
      <rect x="142" y="72" width="316" height="176" rx="20" fill="#0F172A"/>
      <path d="M174 178 C224 178 242 104 300 104 C358 104 376 178 426 178" fill="none" stroke="#7602FF" stroke-width="4" stroke-linecap="round"/>
      <circle cx="174" cy="178" r="7" fill="#38BDF8"/>
      <circle cx="300" cy="104" r="9" fill="#EC4899"/>
      <circle cx="426" cy="178" r="7" fill="#38BDF8"/>
      <!-- Timeline track -->
      <rect x="166" y="212" width="268" height="14" rx="7" fill="#1E293B"/>
      <rect x="166" y="212" width="154" height="14" rx="7" fill="#7602FF"/>
      <circle cx="320" cy="219" r="9" fill="#FFFFFF"/>
    </g>
    <g class="sub-emblem-152">
      <rect x="262" y="122" width="76" height="76" rx="22" fill="#EC4899"/>
      <polygon points="290,144 290,176 318,160" fill="#FFFFFF"/>
    </g>
    <g class="sub-wordmark"><text x="208" y="174" font-family="'Inter', Arial, sans-serif" font-size="38" font-weight="700" fill="#0F172A" letter-spacing="-0.8">Motion Design</text></g>
  </svg>
</div>
""".strip()

SVG_GD_BRAND = """
<div class="roasist-brand-stage gd-sub-stage">
  <svg viewBox="0 0 600 320" class="sub-brand-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Brand Identity">
    <defs><filter id="gdF3" x="-15%" y="-15%" width="130%" height="140%"><feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#0F172A" flood-opacity="0.08"/></filter></defs>
    <g class="sub-p1-pop" filter="url(#gdF3)">
      <rect x="142" y="74" width="316" height="172" rx="20" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <!-- Typography Aa Tile -->
      <rect x="160" y="92" width="124" height="136" rx="14" fill="#0F172A"/>
      <text x="222" y="176" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="52">Aa</text>
      <!-- Color Swatches -->
      <rect x="300" y="92"  width="140" height="38" rx="10" fill="#7602FF"/>
      <rect x="300" y="140" width="140" height="38" rx="10" fill="#0EA5E9"/>
      <rect x="300" y="188" width="140" height="38" rx="10" fill="#EC4899"/>
    </g>
    <g class="sub-emblem-152">
      <rect x="262" y="122" width="76" height="76" rx="22" fill="#0F172A"/>
      <circle cx="288" cy="148" r="12" fill="#7602FF"/>
      <circle cx="312" cy="148" r="12" fill="#0EA5E9" opacity="0.9"/>
      <circle cx="300" cy="170" r="12" fill="#EC4899" opacity="0.9"/>
    </g>
    <g class="sub-wordmark"><text x="208" y="174" font-family="'Inter', Arial, sans-serif" font-size="38" font-weight="700" fill="#0F172A" letter-spacing="-0.8">Brand Identity</text></g>
  </svg>
</div>
""".strip()

SVG_GD_SOCIAL = """
<div class="roasist-brand-stage gd-sub-stage">
  <svg viewBox="0 0 600 320" class="sub-brand-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Social Media Visuals">
    <defs><filter id="gdF4" x="-15%" y="-15%" width="130%" height="140%"><feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#0F172A" flood-opacity="0.08"/></filter></defs>
    <g class="sub-p1-pop" filter="url(#gdF4)">
      <rect x="172" y="66" width="256" height="188" rx="20" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <rect x="190" y="84"  width="66" height="68" rx="12" fill="#7602FF"/>
      <rect x="267" y="84"  width="66" height="68" rx="12" fill="#F5F3FF"/>
      <rect x="344" y="84"  width="66" height="68" rx="12" fill="#0F172A"/>
      <rect x="190" y="164" width="66" height="68" rx="12" fill="#EFF6FF"/>
      <rect x="267" y="164" width="66" height="68" rx="12" fill="#EC4899"/>
      <rect x="344" y="164" width="66" height="68" rx="12" fill="#E0F2FE"/>
    </g>
    <g class="sub-emblem-152">
      <rect x="262" y="122" width="76" height="76" rx="20" fill="#0EA5E9"/>
      <rect x="276" y="136" width="20" height="20" rx="5" fill="#FFFFFF"/>
      <rect x="302" y="136" width="20" height="20" rx="5" fill="#FFFFFF" opacity="0.7"/>
      <rect x="276" y="162" width="20" height="20" rx="5" fill="#FFFFFF" opacity="0.7"/>
      <rect x="302" y="162" width="20" height="20" rx="5" fill="#FFFFFF"/>
    </g>
    <g class="sub-wordmark"><text x="206" y="174" font-family="'Inter', Arial, sans-serif" font-size="38" font-weight="700" fill="#0F172A" letter-spacing="-0.8">Social Visuals</text></g>
  </svg>
</div>
""".strip()

SVG_GD_DECK = """
<div class="roasist-brand-stage gd-sub-stage">
  <svg viewBox="0 0 600 320" class="sub-brand-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Brand Collateral and Pitch Decks">
    <defs><filter id="gdF5" x="-15%" y="-15%" width="130%" height="140%"><feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#0F172A" flood-opacity="0.08"/></filter></defs>
    <g class="sub-p1-slide" filter="url(#gdF5)">
      <rect x="166" y="96" width="268" height="154" rx="18" fill="#E2E8F0" transform="rotate(-4 300 173)"/>
      <rect x="156" y="80" width="288" height="162" rx="18" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5"/>
      <rect x="178" y="104" width="118" height="14" rx="7" fill="#0F172A"/>
      <rect x="178" y="128" width="88" height="8" rx="4" fill="#94A3B8"/>
      <rect x="178" y="146" width="102" height="8" rx="4" fill="#CBD5E1"/>
      <rect x="178" y="182" width="76" height="28" rx="14" fill="#7602FF"/>
      <rect x="322" y="104" width="98" height="114" rx="12" fill="#F5F3FF"/>
      <circle cx="371" cy="161" r="24" fill="#7602FF"/>
    </g>
    <g class="sub-emblem-162">
      <rect x="262" y="122" width="76" height="76" rx="20" fill="#0F172A"/>
      <rect x="278" y="138" width="44" height="10" rx="5" fill="#FFFFFF"/>
      <rect x="278" y="156" width="28" height="8" rx="4" fill="#7602FF"/>
      <rect x="278" y="172" width="36" height="8" rx="4" fill="#38BDF8"/>
    </g>
    <g class="sub-wordmark"><text x="192" y="174" font-family="'Inter', Arial, sans-serif" font-size="36" font-weight="700" fill="#0F172A" letter-spacing="-0.8">Brand Collateral</text></g>
  </svg>
</div>
""".strip()

GD_STAGES = [SVG_GD_ADS, SVG_GD_MOTION, SVG_GD_BRAND, SVG_GD_SOCIAL, SVG_GD_DECK]

# ===========================================================================
# 2. DONUSUM OPTIMIZASYONU (CRO) — 5 Services + 6 Process Steps + 5 SVG Stages
# ===========================================================================

TR_CRO_SERVICES = [
    {
        "title": "UX & Dönüşüm Hunisi (Funnel) Denetimi",
        "desc": "Ziyaretçilerin sitenizde hangi adımda ayrıldığını analitik verilerle tespit eder, satın alma ve form doldurma önündeki tüm sürtünme noktalarını ortadan kaldırırız.",
    },
    {
        "title": "Isı Haritası & Kullanıcı Davranış Analizi",
        "desc": "Tıklama haritaları, kaydırma derinliği ve anonim oturum kayıtlarıyla kullanıcıların gerçek davranışlarını izleyip veri temelli tasarım kararları alırız.",
    },
    {
        "title": "A/B & Çok Değişkenli (Multivariate) Testler",
        "desc": "Başlık, değer önerisi, CTA butonu, görsel ve sayfa düzeni varyasyonlarını istatistiksel anlamlılıkla test ederek dönüşüm oranınızı ölçülebilir biçimde yükseltiriz.",
    },
    {
        "title": "Açılış Sayfası (Landing Page) Optimizasyonu",
        "desc": "Google Ads ve Meta reklamlarından gelen ücretli trafiği boşa harcamadan maksimum lead ve satışa çeviren yüksek ikna gücüne sahip iniş sayfaları kurgularız.",
    },
    {
        "title": "Sepet & Ödeme Adımı (Checkout) İyileştirme",
        "desc": "Form alanlarını sadeleştirerek, güven unsurlarını güçlendirerek ve mobil ödeme akışını hızlandırarak sepet terk oranlarını düşürür, gelirinizi artırırız.",
    },
]

EN_CRO_SERVICES = [
    {
        "title": "UX & Conversion Funnel Audit",
        "desc": "We pinpoint exact drop-off stages across your analytics funnel and eliminate friction barriers standing between visitors and completed conversions.",
    },
    {
        "title": "Heatmaps & Session Behavior Analytics",
        "desc": "We analyze click maps, scroll depth, and anonymized session recordings to ground every UX improvement in real user behavior.",
    },
    {
        "title": "A/B & Multivariate Experimentation",
        "desc": "We run statistically rigorous split tests across headlines, value propositions, CTAs, and layouts to compound conversion gains month after month.",
    },
    {
        "title": "Landing Page Optimization",
        "desc": "We align paid search and social ad messaging with persuasive, fast-loading landing pages engineered to maximize ROAS and lower CPA.",
    },
    {
        "title": "Checkout & Form Flow Optimization",
        "desc": "We streamline form fields, reinforce trust signals, and accelerate mobile checkout steps to slash cart abandonment and lift revenue per session.",
    },
]

CRO_TR_STEPS = [
    {"num": "01", "heading": "Veri & Huni Analizi", "text": "GA4, dönüşüm hunisi ve cihaz kırılımlarıyla en yüksek gelir potansiyeline sahip kayıp noktalarını tespit ederiz."},
    {"num": "02", "heading": "Isı Haritası & Kullanıcı Testi", "text": "Tıklama haritaları, kaydırma analizi ve oturum kayıtlarıyla ziyaretçilerin neden dönüşmediğini net biçimde ortaya çıkarırız."},
    {"num": "03", "heading": "Hipotez & Önceliklendirme", "text": "Etki/efor matrisine göre en hızlı ve en yüksek dönüşüm artışı getirecek A/B test yol haritasını oluştururuz."},
    {"num": "04", "heading": "Varyant Tasarımı & Kurulum", "text": "Hipotezlere uygun temiz UI/UX varyantlarını tasarlar ve sıfır hız kaybıyla test altyapısında yayına alırız."},
    {"num": "05", "heading": "İstatistiksel Doğrulama", "text": "Yeterli örneklem büyüklüğüne ulaşana kadar testleri izler, gerçek dönüşüm ve gelir artışını bilimsel olarak doğrularız."},
    {"num": "06", "heading": "Kazanan Varyant & Ölçekleme", "text": "Kazanan tasarımı kalıcı olarak yayına alır, elde edilen içgörülerle yeni optimizasyon döngüsünü başlatırız."},
]

CRO_EN_STEPS = [
    {"num": "01", "heading": "Analytics & Funnel Diagnostics", "text": "We audit GA4 funnels and device breakdowns to locate the highest-leverage conversion leaks."},
    {"num": "02", "heading": "Heatmaps & Qualitative Research", "text": "We combine click heatmaps, scroll data, and session replays to uncover exactly why visitors hesitate."},
    {"num": "03", "heading": "Hypothesis & Prioritization", "text": "We score every opportunity on impact vs. effort to build a disciplined experimentation roadmap."},
    {"num": "04", "heading": "Variant Design & Launch", "text": "We craft clean UI/UX test variants and deploy them with zero flicker or Core Web Vitals penalty."},
    {"num": "05", "heading": "Statistical Validation", "text": "We monitor experiments to statistical significance, measuring real revenue and conversion uplift."},
    {"num": "06", "heading": "Rollout & Continuous Scaling", "text": "We ship winning variants permanently and feed every learning into the next optimization sprint."},
]

SVG_CRO_FUNNEL = """
<div class="roasist-brand-stage cro-sub-stage">
  <svg viewBox="0 0 600 320" class="sub-brand-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Conversion Funnel Audit">
    <defs><filter id="crF1" x="-15%" y="-15%" width="130%" height="140%"><feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#0F172A" flood-opacity="0.08"/></filter></defs>
    <g class="sub-p1-slide" filter="url(#crF1)">
      <rect x="148" y="68" width="304" height="184" rx="22" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <rect x="176" y="90"  width="248" height="26" rx="13" fill="#F1F5F9"/>
      <rect x="200" y="126" width="200" height="26" rx="13" fill="#E0E7FF"/>
      <rect x="224" y="162" width="152" height="26" rx="13" fill="#C4B5FD"/>
      <rect x="248" y="198" width="104" height="26" rx="13" fill="#7602FF"/>
      <text x="300" y="216" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="11">CVR ↑</text>
    </g>
    <g class="sub-emblem-144">
      <rect x="262" y="122" width="76" height="76" rx="22" fill="#7602FF"/>
      <polygon points="278,142 322,142 306,162 306,180 294,174 294,162" fill="#FFFFFF"/>
    </g>
    <g class="sub-wordmark"><text x="218" y="174" font-family="'Inter', Arial, sans-serif" font-size="38" font-weight="700" fill="#0F172A" letter-spacing="-0.8">Funnel Audit</text></g>
  </svg>
</div>
""".strip()

SVG_CRO_HEATMAP = """
<div class="roasist-brand-stage cro-sub-stage">
  <svg viewBox="0 0 600 320" class="sub-brand-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Heatmaps and UX Analytics">
    <defs>
      <radialGradient id="hmHot"><stop offset="0%" stop-color="#EF4444" stop-opacity="0.9"/><stop offset="55%" stop-color="#F59E0B" stop-opacity="0.5"/><stop offset="100%" stop-color="#F59E0B" stop-opacity="0"/></radialGradient>
      <filter id="crF2" x="-15%" y="-15%" width="130%" height="140%"><feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#0F172A" flood-opacity="0.08"/></filter>
    </defs>
    <g class="sub-p1-pop" filter="url(#crF2)">
      <rect x="148" y="70" width="304" height="180" rx="20" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <rect x="172" y="96"  width="132" height="12" rx="6" fill="#CBD5E1"/>
      <rect x="172" y="118" width="96"  height="8"  rx="4" fill="#E2E8F0"/>
      <rect x="172" y="142" width="88"  height="28" rx="14" fill="#0F172A"/>
      <rect x="316" y="96"  width="112" height="124" rx="14" fill="#F8FAFC" stroke="#E2E8F0"/>
      <!-- Heatmap Hotspots -->
      <circle cx="216" cy="156" r="36" fill="url(#hmHot)"/>
      <circle cx="372" cy="144" r="30" fill="url(#hmHot)"/>
    </g>
    <g class="sub-emblem-152">
      <rect x="262" y="122" width="76" height="76" rx="22" fill="#0F172A"/>
      <circle cx="300" cy="160" r="24" fill="#F59E0B" opacity="0.35"/>
      <circle cx="300" cy="160" r="14" fill="#EF4444"/>
      <circle cx="300" cy="160" r="5"  fill="#FFFFFF"/>
    </g>
    <g class="sub-wordmark"><text x="206" y="174" font-family="'Inter', Arial, sans-serif" font-size="38" font-weight="700" fill="#0F172A" letter-spacing="-0.8">Heatmaps &amp; UX</text></g>
  </svg>
</div>
""".strip()

SVG_CRO_AB = """
<div class="roasist-brand-stage cro-sub-stage">
  <svg viewBox="0 0 600 320" class="sub-brand-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="A/B Split Testing">
    <defs><filter id="crF3" x="-15%" y="-15%" width="130%" height="140%"><feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#0F172A" flood-opacity="0.08"/></filter></defs>
    <g class="sub-p1-slide" filter="url(#crF3)">
      <!-- Variant A -->
      <rect x="142" y="84" width="144" height="152" rx="18" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <rect x="160" y="102" width="32" height="24" rx="8" fill="#F1F5F9"/>
      <text x="176" y="119" text-anchor="middle" fill="#64748B" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="13">A</text>
      <rect x="160" y="142" width="104" height="10" rx="5" fill="#CBD5E1"/>
      <rect x="160" y="162" width="76"  height="10" rx="5" fill="#E2E8F0"/>
      <rect x="160" y="192" width="84"  height="24" rx="12" fill="#CBD5E1"/>
      <!-- Winning Variant B -->
      <rect x="314" y="76" width="144" height="164" rx="18" fill="#FFFFFF" stroke="#10B981" stroke-width="2"/>
      <rect x="332" y="94" width="32" height="24" rx="8" fill="#ECFDF5"/>
      <text x="348" y="111" text-anchor="middle" fill="#059669" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="13">B</text>
      <rect x="372" y="94" width="68" height="24" rx="12" fill="#10B981"/>
      <text x="406" y="110" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="11">+38%</text>
      <rect x="332" y="138" width="108" height="10" rx="5" fill="#0F172A"/>
      <rect x="332" y="158" width="80"  height="10" rx="5" fill="#94A3B8"/>
      <rect x="332" y="192" width="108" height="26" rx="13" fill="#7602FF"/>
    </g>
    <g class="sub-emblem-138">
      <rect x="262" y="122" width="76" height="76" rx="22" fill="#10B981"/>
      <text x="300" y="170" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Arial, sans-serif" font-weight="800" font-size="26">A/B</text>
    </g>
    <g class="sub-wordmark"><text x="226" y="174" font-family="'Inter', Arial, sans-serif" font-size="40" font-weight="700" fill="#0F172A" letter-spacing="-0.8">A/B Testing</text></g>
  </svg>
</div>
""".strip()

SVG_CRO_LANDING = """
<div class="roasist-brand-stage cro-sub-stage">
  <svg viewBox="0 0 600 320" class="sub-brand-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Landing Page CRO">
    <defs><filter id="crF4" x="-15%" y="-15%" width="130%" height="140%"><feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#0F172A" flood-opacity="0.08"/></filter></defs>
    <g class="sub-p1-slide" filter="url(#crF4)">
      <rect x="148" y="68" width="304" height="184" rx="20" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <rect x="224" y="96"  width="152" height="14" rx="7" fill="#0F172A"/>
      <rect x="200" y="120" width="200" height="9"  rx="4.5" fill="#94A3B8"/>
      <rect x="236" y="148" width="128" height="36" rx="18" fill="#7602FF"/>
      <text x="300" y="171" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="12">GET STARTED</text>
      <!-- Trust bar -->
      <rect x="184" y="206" width="66" height="18" rx="9" fill="#F1F5F9"/>
      <rect x="267" y="206" width="66" height="18" rx="9" fill="#F1F5F9"/>
      <rect x="350" y="206" width="66" height="18" rx="9" fill="#F1F5F9"/>
    </g>
    <g class="sub-emblem-144">
      <rect x="262" y="122" width="76" height="76" rx="22" fill="#0EA5E9"/>
      <path d="M282 174 L296 158 L306 166 L320 146" fill="none" stroke="#FFFFFF" stroke-width="5.5" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M308 146 L320 146 L320 158" fill="none" stroke="#FFFFFF" stroke-width="5.5" stroke-linecap="round" stroke-linejoin="round"/>
    </g>
    <g class="sub-wordmark"><text x="218" y="174" font-family="'Inter', Arial, sans-serif" font-size="38" font-weight="700" fill="#0F172A" letter-spacing="-0.8">Landing CRO</text></g>
  </svg>
</div>
""".strip()

SVG_CRO_CHECKOUT = """
<div class="roasist-brand-stage cro-sub-stage">
  <svg viewBox="0 0 600 320" class="sub-brand-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Checkout Optimization">
    <defs><filter id="crF5" x="-15%" y="-15%" width="130%" height="140%"><feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#0F172A" flood-opacity="0.08"/></filter></defs>
    <g class="sub-p1-pop" filter="url(#crF5)">
      <rect x="164" y="70" width="272" height="180" rx="22" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <!-- 3-step checkout progress -->
      <line x1="214" y1="106" x2="386" y2="106" stroke="#10B981" stroke-width="3"/>
      <circle cx="214" cy="106" r="11" fill="#10B981"/>
      <circle cx="300" cy="106" r="11" fill="#10B981"/>
      <circle cx="386" cy="106" r="11" fill="#10B981"/>
      <rect x="194" y="138" width="212" height="24" rx="8" fill="#F8FAFC" stroke="#CBD5E1"/>
      <rect x="194" y="178" width="212" height="40" rx="20" fill="#10B981"/>
      <text x="300" y="203" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="13">ORDER COMPLETE ✓</text>
    </g>
    <g class="sub-emblem-152">
      <rect x="262" y="122" width="76" height="76" rx="22" fill="#10B981"/>
      <path d="M284 160 L295 171 L318 148" fill="none" stroke="#FFFFFF" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round"/>
    </g>
    <g class="sub-wordmark"><text x="206" y="174" font-family="'Inter', Arial, sans-serif" font-size="38" font-weight="700" fill="#0F172A" letter-spacing="-0.8">Checkout CRO</text></g>
  </svg>
</div>
""".strip()

CRO_STAGES = [SVG_CRO_FUNNEL, SVG_CRO_HEATMAP, SVG_CRO_AB, SVG_CRO_LANDING, SVG_CRO_CHECKOUT]


def create_cro_page_from_web_design(src_path, dst_path, is_en=False):
    from update_about_page import parse_flight_stream, serialize_flight_stream
    from update_tiktok_yandex_pages import extract_flight_chunks
    import json

    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    text = open(src_path, "r", encoding="utf-8").read()

    # Remove old wd-sub-stage CSS & JS if cloning from already-updated web-tasarim
    text = re.sub(r'<style id="roasist-wd-brand-stages-css">.*?</style>', '', text, flags=re.S)
    text = re.sub(r'<script id="roasist-wd-brand-stages-js">.*?</script>', '', text, flags=re.S)

    if is_en:
        replacements = [
            ("Web Design &amp; Development Agency | Roasist", "Conversion Rate Optimization (CRO) Agency | Roasist"),
            ("Web Design & Development Agency | Roasist", "Conversion Rate Optimization (CRO) Agency | Roasist"),
            ("Web Design &amp; Development", "Conversion Optimization (CRO)"),
            ("Web Design & Development", "Conversion Optimization (CRO)"),
            ("Our Web Design &amp; Development Process.", "Our Conversion Optimization (CRO) Process."),
            ("Our Web Design & Development Process.", "Our Conversion Optimization (CRO) Process."),
            ("/en/web-design/", "/en/conversion-optimization/"),
            ("/hizmetler/web-tasarim/", "/hizmetler/donusum-optimizasyonu/"),
        ]
    else:
        replacements = [
            ("Web Tasarım Ajansı | Roasist", "Dönüşüm Optimizasyonu (CRO) Ajansı | Roasist"),
            ("Web Tasarım Hizmet Sürecimiz", "Dönüşüm Optimizasyonu (CRO) Sürecimiz"),
            ("web tasarım", "dönüşüm optimizasyonu (CRO)"),
            ("Web Tasarım", "Dönüşüm Optimizasyonu (CRO)"),
            ("/hizmetler/web-tasarim/", "/hizmetler/donusum-optimizasyonu/"),
            ("/en/web-design/", "/en/conversion-optimization/"),
        ]

    # 1. Extract Flight chunks FIRST, apply replacements inside parsed records, then re-serialize
    matches, _, full = extract_flight_chunks(text)
    recs = parse_flight_stream(full)
    for rec in recs:
        val = rec[2]
        for old, new in replacements:
            val = val.replace(old, new)
        rec[2] = val
    new_full = serialize_flight_stream(recs)

    # 2. Apply replacements ONLY to non-Flight parts of HTML
    out_parts = []
    last_end = 0
    for idx, m in enumerate(matches):
        seg = text[last_end : m.start()]
        for old, new in replacements:
            seg = seg.replace(old, new)
        out_parts.append(seg)
        if idx == 0:
            encoded = json.dumps(new_full, ensure_ascii=False)[1:-1].replace("</", "\\u003c/")
            out_parts.append(m.group(1) + encoded + m.group(3))
        else:
            out_parts.append("")
        last_end = m.end()
    tail = text[last_end:]
    for old, new in replacements:
        tail = tail.replace(old, new)
    out_parts.append(tail)
    text = "".join(out_parts)

    with open(dst_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"[OK] Created CRO page {os.path.relpath(dst_path, REPO_ROOT)}")


def wire_cro_link_on_homepage(home_path, is_en=False):
    text = open(home_path, "r", encoding="utf-8").read()
    changed = False
    if is_en:
        old_ssr = '<a class="ServicesPanel_tag__JYwRk" href="service/web-design">Conversion Optimization (CRO)</a>'
        new_ssr = '<a class="ServicesPanel_tag__JYwRk" href="service/conversion-optimization">Conversion Optimization (CRO)</a>'
        if old_ssr in text:
            text = text.replace(old_ssr, new_ssr, 1)
            changed = True
        old_fl = '\\"slug\\":\\"web-design\\",\\"title\\":\\"Conversion Optimization (CRO)\\"'
        new_fl = '\\"slug\\":\\"conversion-optimization\\",\\"title\\":\\"Conversion Optimization (CRO)\\"'
        if old_fl in text:
            text = text.replace(old_fl, new_fl, 1)
            changed = True
        if "'conversion-optimization':" not in text and "'web-design':" in text:
            text = text.replace("'web-design': '/en/web-design/',", "'web-design': '/en/web-design/',\n    'conversion-optimization': '/en/conversion-optimization/',")
            changed = True
    else:
        old_ssr = '<a class="ServicesPanel_tag__JYwRk" href="service/web-tasarim">Dönüşüm Optimizasyonu (CRO)</a>'
        new_ssr = '<a class="ServicesPanel_tag__JYwRk" href="service/donusum-optimizasyonu">Dönüşüm Optimizasyonu (CRO)</a>'
        if old_ssr in text:
            text = text.replace(old_ssr, new_ssr, 1)
            changed = True
        old_fl = '\\"slug\\":\\"web-tasarim\\",\\"title\\":\\"Dönüşüm Optimizasyonu (CRO)\\"'
        new_fl = '\\"slug\\":\\"donusum-optimizasyonu\\",\\"title\\":\\"Dönüşüm Optimizasyonu (CRO)\\"'
        if old_fl in text:
            text = text.replace(old_fl, new_fl, 1)
            changed = True
        if "'donusum-optimizasyonu':" not in text and "'web-tasarim':" in text:
            text = text.replace("'web-tasarim': '/hizmetler/web-tasarim/',", "'web-tasarim': '/hizmetler/web-tasarim/',\n    'donusum-optimizasyonu': '/hizmetler/donusum-optimizasyonu/',")
            changed = True

    if changed:
        with open(home_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"[OK] Wired CRO pill link in {os.path.relpath(home_path, REPO_ROOT)}")
    else:
        print(f"[OK] CRO pill link already wired in {os.path.relpath(home_path, REPO_ROOT)}")


def main():
    # 1. Wire CRO pill link on Homepages
    for rel, is_en in [
        ("public/kota-roasist-local.html", False),
        ("public/en/index.html", True),
        ("dist/index.html", False),
        ("dist/en/index.html", True),
    ]:
        p = os.path.join(REPO_ROOT, rel)
        if os.path.exists(p):
            wire_cro_link_on_homepage(p, is_en=is_en)

    # 2. Upgrade Grafik Tasarım (TR & EN, public + dist)
    gd_jobs = [
        ("public/kota-roasist-local.html", "public/hizmetler/grafik-tasarim/index.html", False, False),
        ("public/en/index.html", "public/en/graphic-design/index.html", True, False),
        ("dist/index.html", "dist/hizmetler/grafik-tasarim/index.html", False, True),
        ("dist/en/index.html", "dist/en/graphic-design/index.html", True, True),
    ]
    for home_rel, target_rel, is_en, is_gh in gd_jobs:
        home_src = os.path.join(REPO_ROOT, home_rel)
        target = os.path.join(REPO_ROOT, target_rel)
        if not os.path.exists(home_src) or not os.path.exists(target):
            print(f"[SKIP] Missing {target_rel} or {home_rel}")
            continue
        stats = get_homepage_statistics(home_src)
        sync_stats(target, stats, is_en=is_en, is_gh_pages=is_gh)
        update_process(target, GD_EN_STEPS if is_en else GD_TR_STEPS, is_en=is_en, is_gh_pages=is_gh)
        update_channel_campaigns(target, "gd", EN_GD_SERVICES if is_en else TR_GD_SERVICES, GD_STAGES, is_gh_pages=is_gh)

    # 3. Create & upgrade dedicated CRO pages (TR & EN, public + dist)
    cro_jobs = [
        ("public/kota-roasist-local.html", "public/hizmetler/web-tasarim/index.html", "public/hizmetler/donusum-optimizasyonu/index.html", False, False),
        ("public/en/index.html", "public/en/web-design/index.html", "public/en/conversion-optimization/index.html", True, False),
        ("dist/index.html", "dist/hizmetler/web-tasarim/index.html", "dist/hizmetler/donusum-optimizasyonu/index.html", False, True),
        ("dist/en/index.html", "dist/en/web-design/index.html", "dist/en/conversion-optimization/index.html", True, True),
    ]
    for home_rel, src_rel, dst_rel, is_en, is_gh in cro_jobs:
        home_src = os.path.join(REPO_ROOT, home_rel)
        src = os.path.join(REPO_ROOT, src_rel)
        dst = os.path.join(REPO_ROOT, dst_rel)
        if not os.path.exists(home_src) or not os.path.exists(src):
            print(f"[SKIP] Missing {src_rel} or {home_rel}")
            continue
        create_cro_page_from_web_design(src, dst, is_en=is_en)
        stats = get_homepage_statistics(home_src)
        sync_stats(dst, stats, is_en=is_en, is_gh_pages=is_gh)
        update_process(dst, CRO_EN_STEPS if is_en else CRO_TR_STEPS, is_en=is_en, is_gh_pages=is_gh)
        update_channel_campaigns(dst, "cro", EN_CRO_SERVICES if is_en else TR_CRO_SERVICES, CRO_STAGES, is_gh_pages=is_gh)


if __name__ == "__main__":
    main()
