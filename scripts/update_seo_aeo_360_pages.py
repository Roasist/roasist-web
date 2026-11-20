#!/usr/bin/env python3
"""
Upgrades all 3 services under 'SEO, AEO & 360° Dijital Büyüme' (TR & EN, public/ and dist/):
  1. Teknik & Kurumsal SEO (/hizmetler/seo/ & /en/seo/)
  2. Yapay Zeka Aramaları (AEO & GEO) — creates dedicated /hizmetler/aeo-geo/
     & /en/aeo-geo/ pages and wires the Homepage pill straight to them.
  3. 360° Dijital Pazarlama Yönetimi (/hizmetler/360-derece-dijital-pazarlama-yonetimi/
     & /en/360-digital-marketing-management/)

Each page gets:
  - 5 bespoke service modules + 5 white-stage SVG/CSS brand-motion animations (no buttons).
  - Synced 5 Homepage 'ÖLÇÜLEBİLİR SONUÇLAR' / 'MEASURABLE RESULTS' dark cards + heading.
  - Bespoke 6-step elevated white Process cards (zero duplicate sections).
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
from update_performans_process import update_page as update_process
from update_tiktok_yandex_pages import extract_flight_chunks, update_channel_campaigns

# ===========================================================================
# 1. TEKNIK & KURUMSAL SEO
# ===========================================================================

TR_SEO_SERVICES = [
    {"title": "Teknik SEO & Core Web Vitals", "desc": "Tarama bütçesi, indeksleme mimarisi, site hızı, Core Web Vitals ve teknik hata temizliğiyle arama motorlarının sitenizi kusursuz taramasını sağlıyoruz."},
    {"title": "Anahtar Kelime & Arama Niyeti Mimarisi", "desc": "Ticari ve bilgi odaklı arama niyetlerini haritalayarak yalnızca trafik değil, gerçek müşteri ve satış getiren konu kümeleri (Topic Clusters) kurguluyoruz."},
    {"title": "Site İçi (On-Page) & Semantik İçerik", "desc": "E-E-A-T standartlarına uygun, güçlü iç linkleme ve yapısal veri (Schema) destekli semantik içeriklerle organik sıralamalarınızı kalıcı olarak yükseltiyoruz."},
    {"title": "Dijital PR & Otorite (Backlink) İnşası", "desc": "Sektörünüzle yüksek alakalı, güvenilir yayınlardan doğal otorite bağlantıları ve marka bahsedilmeleri kazanarak alan adı gücünüzü (DR) artırıyoruz."},
    {"title": "Yerel & Global (Çok Dilli) SEO", "desc": "Hreflang mimarisi, uluslararası pazar yerelleştirmesi ve Google İşletme Profili optimizasyonuyla hem lokal hem global aramalarda ilk sayfada yer alın."},
]

EN_SEO_SERVICES = [
    {"title": "Technical SEO & Core Web Vitals", "desc": "We optimize crawl budget, indexation architecture, site speed, and Core Web Vitals so search engines render and rank your pages effortlessly."},
    {"title": "Keyword & Search Intent Architecture", "desc": "We map commercial and informational search intent into structured topic clusters engineered to capture high-value organic pipeline."},
    {"title": "On-Page & Semantic Content Systems", "desc": "We build E-E-A-T aligned editorial content, precision internal linking, and rich Schema markup for compounding organic visibility."},
    {"title": "Digital PR & Domain Authority", "desc": "We earn high-trust editorial backlinks and brand mentions across authoritative publications to strengthen domain equity."},
    {"title": "Local & International (Multi-Region) SEO", "desc": "We implement clean hreflang architecture, localized keyword research, and local search signals to scale across global markets."},
]

SEO_TR_STEPS = [
    {"num": "01", "heading": "Teknik & Rakip Denetimi", "text": "Tarama hatalarını, hız darboğazlarını, indeksleme yapısını ve sektör rakiplerinizin organik stratejilerini derinlemesine analiz ederiz."},
    {"num": "02", "heading": "Arama Niyeti & Kelime Haritası", "text": "Gelir potansiyeli en yüksek ticari anahtar kelimeleri ve konu kümelerini sayfa mimarisiyle eşleştiririz."},
    {"num": "03", "heading": "Teknik & Schema İyileştirmeleri", "text": "Core Web Vitals, site mimarisi, canonical/hreflang ve JSON-LD yapısal verilerini hatasız biçimde uygularız."},
    {"num": "04", "heading": "Semantik İçerik & On-Page", "text": "Arama niyetine tam yanıt veren, dönüşüm odaklı ve E-E-A-T uyumlu içerikleri düzenli olarak yayına alırız."},
    {"num": "05", "heading": "Otorite & Dijital PR", "text": "Yüksek güvenilirliğe sahip sektör yayınlarından doğal backlink ve marka otoritesi sinyalleri oluştururuz."},
    {"num": "06", "heading": "Ölçümleme & Sürekli Büyüme", "text": "Search Console ve GA4 üzerinden organik görünürlük, sıralama ve dönüşüm gelirini şeffaf biçimde raporlayıp ölçekleriz."},
]

SEO_EN_STEPS = [
    {"num": "01", "heading": "Technical & Competitor Audit", "text": "We diagnose crawl errors, speed bottlenecks, indexation gaps, and competitor organic moats."},
    {"num": "02", "heading": "Search Intent & Keyword Map", "text": "We align high-intent commercial keywords and topic clusters directly with your revenue pages."},
    {"num": "03", "heading": "Technical & Schema Engineering", "text": "We resolve Core Web Vitals, internal architecture, hreflang, and JSON-LD structured data cleanly."},
    {"num": "04", "heading": "Semantic Content & On-Page", "text": "We publish E-E-A-T aligned, conversion-ready content built to win top organic positions."},
    {"num": "05", "heading": "Authority & Digital PR", "text": "We build clean editorial authority signals and high-relevance brand mentions across your niche."},
    {"num": "06", "heading": "Tracking & Compounding Scale", "text": "We track rankings, organic pipeline, and revenue transparently via Search Console and GA4."},
]

SVG_SEO_TECH = """
<div class="roasist-brand-stage seo-sub-stage">
  <svg viewBox="0 0 600 320" class="sub-brand-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Technical SEO">
    <defs><filter id="seF1" x="-15%" y="-15%" width="130%" height="140%"><feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#0F172A" flood-opacity="0.07"/></filter></defs>
    <g class="sub-p1-pop" filter="url(#seF1)">
      <rect x="132" y="84" width="336" height="152" rx="22" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <circle cx="204" cy="152" r="34" fill="#ECFDF5" stroke="#10B981" stroke-width="7"/>
      <text x="204" y="160" text-anchor="middle" fill="#059669" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="22">100</text>
      <text x="204" y="208" text-anchor="middle" fill="#475569" font-family="Inter, Arial, sans-serif" font-weight="600" font-size="11">CRAWL</text>
      <circle cx="300" cy="152" r="34" fill="#ECFDF5" stroke="#10B981" stroke-width="7"/>
      <text x="300" y="160" text-anchor="middle" fill="#059669" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="22">100</text>
      <text x="300" y="208" text-anchor="middle" fill="#475569" font-family="Inter, Arial, sans-serif" font-weight="600" font-size="11">SEO</text>
      <circle cx="396" cy="152" r="34" fill="#ECFDF5" stroke="#10B981" stroke-width="7"/>
      <text x="396" y="160" text-anchor="middle" fill="#059669" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="22">99</text>
      <text x="396" y="208" text-anchor="middle" fill="#475569" font-family="Inter, Arial, sans-serif" font-weight="600" font-size="11">SPEED</text>
    </g>
    <g class="sub-emblem-152">
      <rect x="262" y="122" width="76" height="76" rx="22" fill="#10B981"/>
      <path d="M286 148 L274 160 L286 172 M314 148 L326 160 L314 172" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
      <line x1="304" y1="144" x2="296" y2="176" stroke="#FFFFFF" stroke-width="4.5" stroke-linecap="round"/>
    </g>
    <g class="sub-wordmark"><text x="206" y="174" font-family="'Inter', Arial, sans-serif" font-size="38" font-weight="700" fill="#0F172A" letter-spacing="-0.8">Technical SEO</text></g>
  </svg>
</div>
""".strip()

SVG_SEO_KW = """
<div class="roasist-brand-stage seo-sub-stage">
  <svg viewBox="0 0 600 320" class="sub-brand-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Keyword Strategy">
    <defs><filter id="seF2" x="-15%" y="-15%" width="130%" height="140%"><feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#0F172A" flood-opacity="0.07"/></filter></defs>
    <g class="sub-p1-slide" filter="url(#seF2)">
      <rect x="136" y="76" width="328" height="46" rx="23" fill="#FFFFFF" stroke="#7602FF" stroke-width="1.8"/>
      <circle cx="164" cy="99" r="8" fill="none" stroke="#7602FF" stroke-width="2.5"/>
      <line x1="170" y1="105" x2="176" y2="111" stroke="#7602FF" stroke-width="2.5" stroke-linecap="round"/>
      <rect x="188" y="94" width="166" height="10" rx="5" fill="#0F172A"/>
      <!-- Rank #1 Organic Card -->
      <rect x="136" y="140" width="328" height="102" rx="18" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <rect x="156" y="158" width="44" height="22" rx="11" fill="#ECFDF5"/>
      <text x="178" y="173" text-anchor="middle" fill="#059669" font-family="Inter, Arial, sans-serif" font-weight="800" font-size="11">#1</text>
      <rect x="210" y="164" width="144" height="10" rx="5" fill="#0EA5E9"/>
      <rect x="156" y="194" width="248" height="9" rx="4.5" fill="#CBD5E1"/>
      <rect x="156" y="212" width="186" height="9" rx="4.5" fill="#E2E8F0"/>
    </g>
    <g class="sub-emblem-162">
      <circle cx="300" cy="160" r="38" fill="#7602FF"/>
      <text x="300" y="174" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Arial, sans-serif" font-weight="800" font-size="34">#1</text>
    </g>
    <g class="sub-wordmark"><text x="192" y="174" font-family="'Inter', Arial, sans-serif" font-size="36" font-weight="700" fill="#0F172A" letter-spacing="-0.8">Keyword Strategy</text></g>
  </svg>
</div>
""".strip()

SVG_SEO_CONTENT = """
<div class="roasist-brand-stage seo-sub-stage">
  <svg viewBox="0 0 600 320" class="sub-brand-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Semantic Content">
    <defs><filter id="seF3" x="-15%" y="-15%" width="130%" height="140%"><feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#0F172A" flood-opacity="0.07"/></filter></defs>
    <g class="sub-p1-slide" filter="url(#seF3)">
      <rect x="164" y="66" width="272" height="188" rx="20" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <rect x="188" y="92"  width="34" height="22" rx="6" fill="#F5F3FF"/>
      <text x="205" y="107" text-anchor="middle" fill="#7602FF" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="11">H1</text>
      <rect x="232" y="96"  width="174" height="12" rx="6" fill="#0F172A"/>
      <rect x="188" y="132" width="34" height="20" rx="6" fill="#EFF6FF"/>
      <text x="205" y="146" text-anchor="middle" fill="#0284C7" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="10">H2</text>
      <rect x="232" y="137" width="142" height="9" rx="4.5" fill="#475569"/>
      <rect x="188" y="168" width="218" height="8" rx="4" fill="#CBD5E1"/>
      <rect x="188" y="186" width="186" height="8" rx="4" fill="#CBD5E1"/>
      <rect x="188" y="212" width="84" height="22" rx="11" fill="#ECFDF5"/>
      <text x="230" y="227" text-anchor="middle" fill="#059669" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="10">E-E-A-T ✓</text>
    </g>
    <g class="sub-emblem-162">
      <rect x="262" y="122" width="76" height="76" rx="20" fill="#0F172A"/>
      <rect x="278" y="140" width="44" height="8" rx="4" fill="#FFFFFF"/>
      <rect x="278" y="156" width="32" height="8" rx="4" fill="#7602FF"/>
      <rect x="278" y="172" width="40" height="8" rx="4" fill="#10B981"/>
    </g>
    <g class="sub-wordmark"><text x="192" y="174" font-family="'Inter', Arial, sans-serif" font-size="35" font-weight="700" fill="#0F172A" letter-spacing="-0.8">Semantic Content</text></g>
  </svg>
</div>
""".strip()

SVG_SEO_AUTH = """
<div class="roasist-brand-stage seo-sub-stage">
  <svg viewBox="0 0 600 320" class="sub-brand-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Domain Authority">
    <g class="sub-p1-pop">
      <line x1="300" y1="160" x2="210" y2="104" stroke="#CBD5E1" stroke-width="2.5"/>
      <line x1="300" y1="160" x2="390" y2="104" stroke="#CBD5E1" stroke-width="2.5"/>
      <line x1="300" y1="160" x2="210" y2="216" stroke="#CBD5E1" stroke-width="2.5"/>
      <line x1="300" y1="160" x2="390" y2="216" stroke="#CBD5E1" stroke-width="2.5"/>
      <circle cx="210" cy="104" r="16" fill="#0EA5E9"/>
      <circle cx="390" cy="104" r="16" fill="#10B981"/>
      <circle cx="210" cy="216" r="16" fill="#7602FF"/>
      <circle cx="390" cy="216" r="16" fill="#0EA5E9"/>
      <circle cx="300" cy="160" r="34" fill="#0F172A"/>
      <text x="300" y="168" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Arial, sans-serif" font-weight="800" font-size="22">DR↑</text>
    </g>
    <g class="sub-emblem-162">
      <circle cx="300" cy="160" r="38" fill="#0EA5E9"/>
      <path d="M286 160 L296 170 L316 148" fill="none" stroke="#FFFFFF" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round"/>
    </g>
    <g class="sub-wordmark"><text x="192" y="174" font-family="'Inter', Arial, sans-serif" font-size="35" font-weight="700" fill="#0F172A" letter-spacing="-0.8">Domain Authority</text></g>
  </svg>
</div>
""".strip()

SVG_SEO_GLOBAL = """
<div class="roasist-brand-stage seo-sub-stage">
  <svg viewBox="0 0 600 320" class="sub-brand-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Global and Local SEO">
    <g class="sub-p1-pop">
      <circle cx="300" cy="160" r="76" fill="#F8FAFC" stroke="#0EA5E9" stroke-width="2.2"/>
      <ellipse cx="300" cy="160" rx="36" ry="76" fill="none" stroke="#CBD5E1" stroke-width="1.6"/>
      <line x1="224" y1="160" x2="376" y2="160" stroke="#CBD5E1" stroke-width="1.6"/>
      <line x1="234" y1="124" x2="366" y2="124" stroke="#E2E8F0" stroke-width="1.4"/>
      <line x1="234" y1="196" x2="366" y2="196" stroke="#E2E8F0" stroke-width="1.4"/>
      <circle cx="268" cy="134" r="9" fill="#7602FF"/>
      <circle cx="338" cy="146" r="9" fill="#10B981"/>
      <circle cx="304" cy="192" r="9" fill="#0EA5E9"/>
    </g>
    <g class="sub-emblem-144">
      <circle cx="300" cy="160" r="38" fill="#0F172A"/>
      <ellipse cx="300" cy="160" rx="18" ry="36" fill="none" stroke="#38BDF8" stroke-width="3"/>
      <line x1="264" y1="160" x2="336" y2="160" stroke="#38BDF8" stroke-width="3"/>
    </g>
    <g class="sub-wordmark"><text x="216" y="174" font-family="'Inter', Arial, sans-serif" font-size="38" font-weight="700" fill="#0F172A" letter-spacing="-0.8">Global SEO</text></g>
  </svg>
</div>
""".strip()

SEO_STAGES = [SVG_SEO_TECH, SVG_SEO_KW, SVG_SEO_CONTENT, SVG_SEO_AUTH, SVG_SEO_GLOBAL]

# ===========================================================================
# 2. YAPAY ZEKA ARAMALARI (AEO & GEO)
# ===========================================================================

TR_AEO_SERVICES = [
    {"title": "ChatGPT, Gemini & Perplexity Görünürlüğü", "desc": "Kullanıcılar yapay zeka asistanlarına sektörünüzle ilgili sorular sorduğunda markanızın güvenilir birincil kaynak olarak önerilmesini ve alıntılanmasını sağlıyoruz."},
    {"title": "Google AI Overviews (SGE) Optimizasyonu", "desc": "Google'ın yapay zeka özet kutularında (AI Overviews) en üstte yer almanız için doğrudan yanıt mimarisi, özet blokları ve yüksek otoriteli kaynak yapısı kuruyoruz."},
    {"title": "Entity, Knowledge Graph & Schema Mimarisi", "desc": "Markanızı, ürünlerinizi ve uzmanlığınızı makine tarafından eksiksiz okunabilen JSON-LD Schema ve varlık (Entity) grafiklerine dönüştürüyoruz."},
    {"title": "Yanıt Motoru Odaklı İçerik (AEO)", "desc": "Konuşma dilindeki uzun kuyruklu sorulara net, doğrulanabilir ve yapılandırılmış yanıtlar veren yeni nesil AEO içerik ekosistemleri üretiyoruz."},
    {"title": "LLM Marka Otoritesi & Dijital Alıntılar", "desc": "Büyük dil modellerinin (LLM) eğitim ve canlı arama katmanlarında güvendiği dijital yayınlarda marka tutarlılığınızı ve alıntı payınızı (Share of Model) büyütüyoruz."},
]

EN_AEO_SERVICES = [
    {"title": "ChatGPT, Gemini & Perplexity Visibility", "desc": "Position your brand as the primary cited and recommended answer when buyers ask AI assistants for solutions in your category."},
    {"title": "Google AI Overviews Optimization", "desc": "Engineer direct-answer blocks, authoritative citations, and structured summaries designed to capture Google AI Overview placements."},
    {"title": "Entity, Knowledge Graph & Schema Systems", "desc": "Translate your brand, services, and proof points into machine-readable JSON-LD Schema and connected Knowledge Graph entities."},
    {"title": "Answer-Engine Content Architecture (AEO)", "desc": "Build conversational, fact-dense, citation-ready content tailored to how modern answer engines retrieve and synthesize information."},
    {"title": "LLM Brand Authority & Citation Share", "desc": "Expand your Share of Model across trusted third-party sources, reviews, and authoritative publications relied on by AI retrieval pipelines."},
]

AEO_TR_STEPS = [
    {"num": "01", "heading": "AI Görünürlük Denetimi", "text": "ChatGPT, Gemini, Perplexity ve Google AI Overviews üzerinde markanızın ve rakiplerinizin mevcut alıntı payını (Share of Model) ölçeriz."},
    {"num": "02", "heading": "Soru & Niyet Haritalama", "text": "Hedef kitlenizin yapay zeka motorlarına sorduğu gerçek karar aşaması sorularını ve bilgi boşluklarını tespit ederiz."},
    {"num": "03", "heading": "Entity & Schema Kurulumu", "text": "Organization, Service, FAQ, Product ve Author varlıklarını birbirine bağlayan kapsamlı JSON-LD grafiklerini kurarız."},
    {"num": "04", "heading": "AEO İçerik Mimarisi", "text": "Yapay zekaların doğrudan alıntılayabileceği net, veriye dayalı ve yapılandırılmış yanıt sayfaları yayınlarız."},
    {"num": "05", "heading": "Otorite & Alıntı İnşası", "text": "LLM'lerin kaynak olarak güvendiği sektörel yayınlarda ve bilgi tabanlarında marka bahsedilmelerinizi güçlendiririz."},
    {"num": "06", "heading": "AI Payı Takibi & İterasyon", "text": "Yapay zeka yanıtlarındaki marka görünürlüğünüzü ve AI kaynaklı yönlendirme trafiğini düzenli takip edip büyütürüz."},
]

AEO_EN_STEPS = [
    {"num": "01", "heading": "AI Visibility Baseline Audit", "text": "We benchmark your brand's Share of Model across ChatGPT, Gemini, Perplexity, and Google AI Overviews."},
    {"num": "02", "heading": "Prompt & Question Mapping", "text": "We uncover the exact high-intent prompts buyers ask AI engines during vendor evaluation."},
    {"num": "03", "heading": "Entity & Schema Engineering", "text": "We deploy interconnected JSON-LD Schema graphs defining your brand, services, and domain expertise."},
    {"num": "04", "heading": "Citation-Ready AEO Content", "text": "We craft structured, verifiable direct-answer pages engineered for effortless LLM retrieval."},
    {"num": "05", "heading": "Authority & Citation Signals", "text": "We strengthen consistent brand mentions across high-trust publications and knowledge bases."},
    {"num": "06", "heading": "Share of Model Tracking", "text": "We monitor AI citation growth and AI-referred conversions continuously to compound visibility."},
]

SVG_AEO_CITE = """
<div class="roasist-brand-stage aeo-sub-stage">
  <svg viewBox="0 0 600 320" class="sub-brand-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="AI Answer Citations">
    <defs><filter id="aeF1" x="-15%" y="-15%" width="130%" height="140%"><feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#0F172A" flood-opacity="0.08"/></filter></defs>
    <g class="sub-p1-slide" filter="url(#aeF1)">
      <rect x="136" y="72" width="328" height="176" rx="22" fill="#FFFFFF" stroke="#7602FF" stroke-width="1.8"/>
      <circle cx="168" cy="104" r="14" fill="#7602FF"/>
      <path d="M168 95 l2.5 6.5 l6.5 2.5 l-6.5 2.5 l-2.5 6.5 l-2.5 -6.5 l-6.5 -2.5 l6.5 -2.5 z" fill="#FFFFFF"/>
      <rect x="194" y="96" width="152" height="10" rx="5" fill="#0F172A"/>
      <rect x="160" y="134" width="280" height="9" rx="4.5" fill="#CBD5E1"/>
      <rect x="160" y="152" width="242" height="9" rx="4.5" fill="#CBD5E1"/>
      <rect x="160" y="170" width="196" height="9" rx="4.5" fill="#CBD5E1"/>
      <!-- Cited Brand Source Pill -->
      <rect x="160" y="198" width="124" height="28" rx="14" fill="#F5F3FF" stroke="#7602FF" stroke-width="1.4"/>
      <text x="222" y="216" text-anchor="middle" fill="#7602FF" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="11">CITED #1 ✓</text>
    </g>
    <g class="sub-emblem-144">
      <rect x="262" y="122" width="76" height="76" rx="22" fill="#7602FF"/>
      <path d="M300 138 l5 15 l15 5 l-15 5 l-5 15 l-5 -15 l-15 -5 l15 -5 z" fill="#FFFFFF"/>
    </g>
    <g class="sub-wordmark"><text x="218" y="174" font-family="'Inter', Arial, sans-serif" font-size="38" font-weight="700" fill="#0F172A" letter-spacing="-0.8">AI Citations</text></g>
  </svg>
</div>
""".strip()

SVG_AEO_OVERVIEW = """
<div class="roasist-brand-stage aeo-sub-stage">
  <svg viewBox="0 0 600 320" class="sub-brand-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Google AI Overviews">
    <defs><filter id="aeF2" x="-15%" y="-15%" width="130%" height="140%"><feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#0F172A" flood-opacity="0.08"/></filter></defs>
    <g class="sub-p1-pop" filter="url(#aeF2)">
      <rect x="136" y="72" width="328" height="176" rx="22" fill="#F5F3FF" stroke="#C4B5FD" stroke-width="1.5"/>
      <rect x="156" y="92" width="112" height="24" rx="12" fill="#7602FF"/>
      <text x="212" y="108" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="10.5">AI OVERVIEW</text>
      <rect x="156" y="132" width="176" height="10" rx="5" fill="#0F172A"/>
      <rect x="156" y="152" width="154" height="8" rx="4" fill="#64748B"/>
      <rect x="156" y="170" width="168" height="8" rx="4" fill="#64748B"/>
      <!-- Featured Source Card on Right -->
      <rect x="350" y="96" width="96" height="128" rx="14" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.4"/>
      <circle cx="398" cy="134" r="18" fill="#0EA5E9"/>
      <rect x="364" y="166" width="68" height="8" rx="4" fill="#0F172A"/>
      <rect x="364" y="182" width="48" height="7" rx="3.5" fill="#10B981"/>
    </g>
    <g class="sub-emblem-152">
      <rect x="262" y="122" width="76" height="76" rx="22" fill="#0EA5E9"/>
      <path d="M300 138 l5 15 l15 5 l-15 5 l-5 15 l-5 -15 l-15 -5 l15 -5 z" fill="#FFFFFF"/>
    </g>
    <g class="sub-wordmark"><text x="206" y="174" font-family="'Inter', Arial, sans-serif" font-size="38" font-weight="700" fill="#0F172A" letter-spacing="-0.8">AI Overviews</text></g>
  </svg>
</div>
""".strip()

SVG_AEO_SCHEMA = """
<div class="roasist-brand-stage aeo-sub-stage">
  <svg viewBox="0 0 600 320" class="sub-brand-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Entity and Schema Graph">
    <g class="sub-p1-pop">
      <line x1="300" y1="160" x2="210" y2="104" stroke="#7602FF" stroke-width="2.2" opacity="0.5"/>
      <line x1="300" y1="160" x2="390" y2="104" stroke="#0EA5E9" stroke-width="2.2" opacity="0.5"/>
      <line x1="300" y1="160" x2="210" y2="216" stroke="#10B981" stroke-width="2.2" opacity="0.5"/>
      <line x1="300" y1="160" x2="390" y2="216" stroke="#EC4899" stroke-width="2.2" opacity="0.5"/>
      <rect x="176" y="88"  width="68" height="32" rx="16" fill="#F5F3FF" stroke="#7602FF"/>
      <text x="210" y="108" text-anchor="middle" fill="#7602FF" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="10">ORG</text>
      <rect x="356" y="88"  width="68" height="32" rx="16" fill="#EFF6FF" stroke="#0EA5E9"/>
      <text x="390" y="108" text-anchor="middle" fill="#0284C7" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="10">FAQ</text>
      <rect x="176" y="200" width="68" height="32" rx="16" fill="#ECFDF5" stroke="#10B981"/>
      <text x="210" y="220" text-anchor="middle" fill="#059669" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="10">ENTITY</text>
      <rect x="356" y="200" width="68" height="32" rx="16" fill="#FCE7F3" stroke="#EC4899"/>
      <text x="390" y="220" text-anchor="middle" fill="#DB2777" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="10">SCHEMA</text>
      <circle cx="300" cy="160" r="30" fill="#0F172A"/>
      <text x="300" y="166" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Arial, sans-serif" font-weight="800" font-size="14">{JSON}</text>
    </g>
    <g class="sub-emblem-156">
      <rect x="262" y="122" width="76" height="76" rx="22" fill="#0F172A"/>
      <text x="300" y="168" text-anchor="middle" fill="#38BDF8" font-family="Inter, Arial, sans-serif" font-weight="800" font-size="24">{ }</text>
    </g>
    <g class="sub-wordmark"><text x="198" y="174" font-family="'Inter', Arial, sans-serif" font-size="36" font-weight="700" fill="#0F172A" letter-spacing="-0.8">Entity &amp; Schema</text></g>
  </svg>
</div>
""".strip()

SVG_AEO_QA = """
<div class="roasist-brand-stage aeo-sub-stage">
  <svg viewBox="0 0 600 320" class="sub-brand-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Answer Engine Optimization">
    <defs><filter id="aeF4" x="-15%" y="-15%" width="130%" height="140%"><feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#0F172A" flood-opacity="0.07"/></filter></defs>
    <g class="sub-p1-slide" filter="url(#aeF4)">
      <rect x="148" y="76" width="248" height="58" rx="20" fill="#F1F5F9"/>
      <rect x="170" y="98" width="168" height="12" rx="6" fill="#475569"/>
      <rect x="204" y="152" width="248" height="92" rx="20" fill="#0F172A"/>
      <rect x="226" y="176" width="184" height="10" rx="5" fill="#FFFFFF"/>
      <rect x="226" y="196" width="142" height="8" rx="4" fill="#94A3B8"/>
      <rect x="226" y="214" width="76" height="16" rx="8" fill="#10B981"/>
    </g>
    <g class="sub-emblem-156">
      <rect x="262" y="122" width="76" height="76" rx="22" fill="#10B981"/>
      <text x="300" y="170" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Arial, sans-serif" font-weight="800" font-size="26">AEO</text>
    </g>
    <g class="sub-wordmark"><text x="198" y="174" font-family="'Inter', Arial, sans-serif" font-size="36" font-weight="700" fill="#0F172A" letter-spacing="-0.8">Answer Engine</text></g>
  </svg>
</div>
""".strip()

SVG_AEO_LLM = """
<div class="roasist-brand-stage aeo-sub-stage">
  <svg viewBox="0 0 600 320" class="sub-brand-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="LLM Brand Authority">
    <g class="sub-p1-pop">
      <circle cx="300" cy="160" r="88" fill="none" stroke="#E2E8F0" stroke-width="1.6" stroke-dasharray="6 6"/>
      <circle cx="300" cy="160" r="58" fill="none" stroke="#7602FF" stroke-width="1.6" opacity="0.35"/>
      <circle cx="300" cy="72"  r="14" fill="#7602FF"/>
      <circle cx="388" cy="160" r="14" fill="#0EA5E9"/>
      <circle cx="300" cy="248" r="14" fill="#10B981"/>
      <circle cx="212" cy="160" r="14" fill="#EC4899"/>
      <circle cx="300" cy="160" r="32" fill="#7602FF"/>
      <text x="300" y="167" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Arial, sans-serif" font-weight="800" font-size="18">GEO</text>
    </g>
    <g class="sub-emblem-152">
      <circle cx="300" cy="160" r="38" fill="#7602FF"/>
      <text x="300" y="169" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Arial, sans-serif" font-weight="800" font-size="22">GEO</text>
    </g>
    <g class="sub-wordmark"><text x="206" y="174" font-family="'Inter', Arial, sans-serif" font-size="38" font-weight="700" fill="#0F172A" letter-spacing="-0.8">LLM Authority</text></g>
  </svg>
</div>
""".strip()

AEO_STAGES = [SVG_AEO_CITE, SVG_AEO_OVERVIEW, SVG_AEO_SCHEMA, SVG_AEO_QA, SVG_AEO_LLM]

# ===========================================================================
# 3. 360 DERECE DIJITAL PAZARLAMA YONETIMI
# ===========================================================================

TR_360_SERVICES = [
    {"title": "Çok Kanallı Performans Pazarlaması", "desc": "Google Ads, Meta, TikTok, Yandex, Bing ve LinkedIn reklamlarını tek bir kârlılık ve ROAS hedefi etrafında bütünsel olarak yönetiyoruz."},
    {"title": "Organik Büyüme: SEO, AEO & İçerik", "desc": "Reklam bütçesine bağımlılığı azaltan, Google ve yapay zeka yanıt motorlarında (ChatGPT, Gemini) bileşik büyüme üreten kalıcı organik trafik kuruyoruz."},
    {"title": "Kreatif Stüdyo, Web & CRO Sinerjisi", "desc": "Yüksek performanslı reklam kreatifleri, hızlı açılış sayfaları ve sürekli A/B testleriyle reklam tıklamalarının her birini maksimum ciroya dönüştürüyoruz."},
    {"title": "Kanallar Arası Attribution & Veri Mimarisi", "desc": "GA4, Server-Side CAPI, CRM ve canlı kârlılık panelleriyle hangi kanalın gerçek ciroya ne kadar katkı sağladığını şeffaf biçimde ölçüyoruz."},
    {"title": "Özel Büyüme Ekibi & Haftalık Sprintler", "desc": "Tek bir iletişim noktasından performans, SEO, kreatif ve yazılım uzmanlarını markanız için haftalık büyüme sprintleriyle senkronize ediyoruz."},
]

EN_360_SERVICES = [
    {"title": "Omnichannel Paid Acquisition", "desc": "We orchestrate Google, Meta, TikTok, Yandex, Bing, and LinkedIn campaigns under one unified ROAS and profit growth architecture."},
    {"title": "Compounding Organic: SEO & AI Search", "desc": "We build durable organic visibility across Google and AI answer engines (ChatGPT, Gemini, Perplexity) to lower blended CAC over time."},
    {"title": "Creative Studio, Web & CRO Synergy", "desc": "High-converting ad creatives, fast landing pages, and disciplined A/B testing ensure every paid and organic visit converts at peak efficiency."},
    {"title": "Cross-Channel Attribution & Analytics", "desc": "Server-side CAPI, GA4, CRM integration, and real-time profit dashboards give you crystal-clear visibility into true revenue impact."},
    {"title": "Dedicated Growth Pod & Weekly Sprints", "desc": "A unified team of paid media, SEO, creative, and engineering specialists operating on weekly growth sprints aligned to your commercial KPIs."},
]

G360_TR_STEPS = [
    {"num": "01", "heading": "360° Dijital Büyüme Denetimi", "text": "Tüm reklam hesaplarınızı, organik görünürlüğünüzü, web sitenizi ve birim ekonominizi tek bir stratejik bakışla denetleriz."},
    {"num": "02", "heading": "Bütünsel Büyüme Yol Haritası", "text": "90 günlük kanal dağılımını, kreatif üretim takvimini, SEO/AEO hedeflerini ve CRO test planını netleştiririz."},
    {"num": "03", "heading": "Ölçümleme & Veri Altyapısı", "text": "GA4, GTM, Conversions API (CAPI) ve CRM bağlantılarıyla kanallar arası kusursuz attribution kurarız."},
    {"num": "04", "heading": "Çok Kanallı İcra & Kreatif Üretim", "text": "Performans kampanyaları, SEO içerikleri ve yeni reklam kreatiflerini eş zamanlı olarak yayına alırız."},
    {"num": "05", "heading": "Haftalık Büyüme Sprintleri", "text": "Her hafta verileri analiz eder; bütçe kaydırmaları, A/B testleri ve kreatif yenilemeleriyle ROAS'ı maksimize ederiz."},
    {"num": "06", "heading": "Şeffaf Raporlama & Ölçekleme", "text": "Canlı kârlılık panelleriyle tüm kanalların net katkısını raporlar, yeni pazarlara güvenle ölçekleriz."},
]

G360_EN_STEPS = [
    {"num": "01", "heading": "360° Digital Growth Audit", "text": "We audit paid channels, organic/AI search visibility, web conversion funnels, and unit economics holistically."},
    {"num": "02", "heading": "Unified 90-Day Roadmap", "text": "We align channel budgets, creative sprints, SEO/AEO priorities, and CRO tests around clear revenue KPIs."},
    {"num": "03", "heading": "Measurement & Attribution Stack", "text": "We engineer GA4, GTM, server-side CAPI, and CRM pipelines for airtight cross-channel attribution."},
    {"num": "04", "heading": "Omnichannel Execution", "text": "We launch coordinated paid campaigns, semantic SEO/AEO assets, and fresh ad creatives simultaneously."},
    {"num": "05", "heading": "Weekly Growth Sprints", "text": "Every week we optimize bids, ship A/B tests, and refresh creatives to compound blended ROAS."},
    {"num": "06", "heading": "Executive Reporting & Scale", "text": "We report net profit contribution transparently via live dashboards and scale winning channels globally."},
]

SVG_360_OMNI = """
<div class="roasist-brand-stage g360-sub-stage">
  <svg viewBox="0 0 600 320" class="sub-brand-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Omnichannel Ads">
    <g class="sub-p1-pop">
      <circle cx="300" cy="160" r="88" fill="none" stroke="#E2E8F0" stroke-width="1.6" stroke-dasharray="5 6"/>
      <circle cx="300" cy="72"  r="16" fill="#4285F4"/>
      <circle cx="376" cy="116" r="16" fill="#0081FB"/>
      <circle cx="376" cy="204" r="16" fill="#010101"/>
      <circle cx="300" cy="248" r="16" fill="#FC3F1D"/>
      <circle cx="224" cy="204" r="16" fill="#00809D"/>
      <circle cx="224" cy="116" r="16" fill="#0A66C2"/>
      <circle cx="300" cy="160" r="34" fill="#7602FF"/>
      <text x="300" y="168" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Arial, sans-serif" font-weight="800" font-size="20">360°</text>
    </g>
    <g class="sub-emblem-162">
      <circle cx="300" cy="160" r="38" fill="#7602FF"/>
      <text x="300" y="169" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Arial, sans-serif" font-weight="800" font-size="22">360°</text>
    </g>
    <g class="sub-wordmark"><text x="192" y="174" font-family="'Inter', Arial, sans-serif" font-size="35" font-weight="700" fill="#0F172A" letter-spacing="-0.8">Omnichannel Ads</text></g>
  </svg>
</div>
""".strip()

SVG_360_ORG = """
<div class="roasist-brand-stage g360-sub-stage">
  <svg viewBox="0 0 600 320" class="sub-brand-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Organic and AI Growth">
    <defs><filter id="g3F2" x="-15%" y="-15%" width="130%" height="140%"><feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#0F172A" flood-opacity="0.07"/></filter></defs>
    <g class="sub-p1-slide" filter="url(#g3F2)">
      <rect x="148" y="74" width="304" height="172" rx="22" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <path d="M180 212 Q240 202 288 164 T416 102" fill="none" stroke="#10B981" stroke-width="5" stroke-linecap="round"/>
      <circle cx="416" cy="102" r="10" fill="#10B981" stroke="#FFFFFF" stroke-width="3"/>
      <rect x="180" y="96" width="84" height="24" rx="12" fill="#ECFDF5"/>
      <text x="222" y="112" text-anchor="middle" fill="#059669" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="10.5">SEO + AEO</text>
    </g>
    <g class="sub-emblem-144">
      <rect x="262" y="122" width="76" height="76" rx="22" fill="#10B981"/>
      <path d="M282 174 L296 158 L306 166 L320 146" fill="none" stroke="#FFFFFF" stroke-width="5.5" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M308 146 L320 146 L320 158" fill="none" stroke="#FFFFFF" stroke-width="5.5" stroke-linecap="round" stroke-linejoin="round"/>
    </g>
    <g class="sub-wordmark"><text x="218" y="174" font-family="'Inter', Arial, sans-serif" font-size="38" font-weight="700" fill="#0F172A" letter-spacing="-0.8">Organic &amp; AI</text></g>
  </svg>
</div>
""".strip()

SVG_360_CRO = """
<div class="roasist-brand-stage g360-sub-stage">
  <svg viewBox="0 0 600 320" class="sub-brand-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Creative and CRO Synergy">
    <defs><filter id="g3F3" x="-15%" y="-15%" width="130%" height="140%"><feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#0F172A" flood-opacity="0.08"/></filter></defs>
    <g class="sub-card-1" filter="url(#g3F3)">
      <rect x="128" y="94" width="104" height="134" rx="16" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <rect x="142" y="108" width="76" height="62" rx="10" fill="#FCE7F3"/>
      <circle cx="180" cy="139" r="14" fill="#EC4899"/>
      <rect x="142" y="198" width="60" height="18" rx="9" fill="#0F172A"/>
      <text x="172" y="211" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="9.5">CREATIVE</text>
    </g>
    <g class="sub-card-2" filter="url(#g3F3)">
      <rect x="248" y="76" width="104" height="152" rx="18" fill="#FFFFFF" stroke="#7602FF" stroke-width="1.8"/>
      <rect x="262" y="90" width="76" height="68" rx="10" fill="#F5F3FF"/>
      <rect x="282" y="108" width="36" height="32" rx="8" fill="#7602FF"/>
      <rect x="262" y="200" width="60" height="18" rx="9" fill="#7602FF"/>
      <text x="292" y="213" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="10">WEB UI</text>
    </g>
    <g class="sub-card-3" filter="url(#g3F3)">
      <rect x="368" y="94" width="104" height="134" rx="16" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <rect x="382" y="108" width="76" height="62" rx="10" fill="#ECFDF5"/>
      <circle cx="420" cy="139" r="14" fill="#10B981"/>
      <rect x="382" y="198" width="52" height="18" rx="9" fill="#10B981"/>
      <text x="408" y="211" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="10">CRO ↑</text>
    </g>
    <g class="sub-emblem-152">
      <rect x="262" y="122" width="76" height="76" rx="22" fill="#EC4899"/>
      <path d="M300 138 l5 15 l15 5 l-15 5 l-5 15 l-5 -15 l-15 -5 l15 -5 z" fill="#FFFFFF"/>
    </g>
    <g class="sub-wordmark"><text x="204" y="174" font-family="'Inter', Arial, sans-serif" font-size="37" font-weight="700" fill="#0F172A" letter-spacing="-0.8">Creative &amp; CRO</text></g>
  </svg>
</div>
""".strip()

SVG_360_DATA = """
<div class="roasist-brand-stage g360-sub-stage">
  <svg viewBox="0 0 600 320" class="sub-brand-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Full-Funnel Attribution">
    <defs><filter id="g3F4" x="-15%" y="-15%" width="130%" height="140%"><feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#0F172A" flood-opacity="0.07"/></filter></defs>
    <g class="sub-p1-slide" filter="url(#g3F4)">
      <rect x="148" y="74" width="304" height="172" rx="20" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <rect x="184" y="170" width="34" height="46" rx="8" fill="#CBD5E1"/>
      <rect x="236" y="144" width="34" height="72" rx="8" fill="#0EA5E9"/>
      <rect x="288" y="122" width="34" height="94" rx="8" fill="#7602FF"/>
      <rect x="340" y="98"  width="34" height="118" rx="8" fill="#10B981"/>
      <rect x="392" y="114" width="34" height="102" rx="8" fill="#0F172A"/>
    </g>
    <g class="sub-emblem-156">
      <rect x="262" y="122" width="76" height="76" rx="22" fill="#0F172A"/>
      <rect x="278" y="162" width="12" height="22" rx="4" fill="#0EA5E9"/>
      <rect x="294" y="148" width="12" height="36" rx="4" fill="#7602FF"/>
      <rect x="310" y="136" width="12" height="48" rx="4" fill="#10B981"/>
    </g>
    <g class="sub-wordmark"><text x="198" y="174" font-family="'Inter', Arial, sans-serif" font-size="36" font-weight="700" fill="#0F172A" letter-spacing="-0.8">Full Attribution</text></g>
  </svg>
</div>
""".strip()

SVG_360_POD = """
<div class="roasist-brand-stage g360-sub-stage">
  <svg viewBox="0 0 600 320" class="sub-brand-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="360 Growth Team">
    <g class="sub-p1-pop">
      <circle cx="236" cy="144" r="24" fill="#0EA5E9"/>
      <circle cx="364" cy="144" r="24" fill="#10B981"/>
      <circle cx="300" cy="126" r="30" fill="#7602FF" stroke="#FFFFFF" stroke-width="4"/>
      <circle cx="300" cy="118" r="8" fill="#FFFFFF"/>
      <path d="M286 138 c0-7 6-11 14-11 s14 4 14 11" fill="#FFFFFF"/>
      <rect x="216" y="196" width="168" height="32" rx="16" fill="#0F172A"/>
      <text x="300" y="216" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="11">WEEKLY SPRINTS ✓</text>
    </g>
    <g class="sub-emblem-162">
      <rect x="262" y="122" width="76" height="76" rx="22" fill="#0EA5E9"/>
      <circle cx="300" cy="148" r="10" fill="#FFFFFF"/>
      <path d="M282 178 c0-9 8-14 18-14 s18 5 18 14" fill="#FFFFFF"/>
    </g>
    <g class="sub-wordmark"><text x="192" y="174" font-family="'Inter', Arial, sans-serif" font-size="35" font-weight="700" fill="#0F172A" letter-spacing="-0.8">360° Growth Team</text></g>
  </svg>
</div>
""".strip()

G360_STAGES = [SVG_360_OMNI, SVG_360_ORG, SVG_360_CRO, SVG_360_DATA, SVG_360_POD]


def create_aeo_page_from_seo(src_path, dst_path, is_en=False):
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    text = open(src_path, "r", encoding="utf-8").read()
    text = re.sub(r'<style id="roasist-seo-brand-stages-css">.*?</style>', '', text, flags=re.S)
    text = re.sub(r'<script id="roasist-seo-brand-stages-js">.*?</script>', '', text, flags=re.S)

    if is_en:
        replacements = [
            ("SEO Agency | Roasist", "AI Search Optimization (AEO & GEO) | Roasist"),
            ("Enterprise SEO &amp; AEO Agency | Roasist", "AI Search Optimization (AEO & GEO) | Roasist"),
            ("Our Enterprise SEO &amp; AEO Process.", "Our AI Search (AEO & GEO) Process."),
            ("Our Enterprise SEO & AEO Process.", "Our AI Search (AEO & GEO) Process."),
            ("Organic <br />\n<em>search</em><br />\nleadership.", "AI search <br />\n<em>citation</em><br />\nleadership."),
            ("Organic <br />\\n<em>search</em><br />\\nleadership.", "AI search <br />\\n<em>citation</em><br />\\nleadership."),
            ("Dominate Google rankings and AI answer engines (ChatGPT, Gemini, Perplexity) with technical precision and commercial-intent content.",
             "Become the primary cited brand across ChatGPT, Google Gemini, Perplexity, and Google AI Overviews with structured entities, answer-engine content, and authoritative signals."),
            ("What Is Modern SEO &amp; How Do We Execute It?", "What Are AEO &amp; GEO and How Do We Execute Them?"),
            ("What Is Modern SEO & How Do We Execute It?", "What Are AEO & GEO and How Do We Execute Them?"),
            ("Search visibility is no longer about stuffing keywords—it is about technical speed, semantic authority, and capturing buyers with real commercial intent across both Google SERPs and AI answer engines (AEO &amp; GEO). We build compounding organic revenue assets.",
             "Search behavior has shifted permanently—buyers now ask ChatGPT, Gemini, Perplexity, and Google AI Overviews for direct recommendations. Answer Engine Optimization (AEO) and Generative Engine Optimization (GEO) structure your brand's entities, JSON-LD schema, citation-ready content, and third-party authority so AI engines cite and recommend you first."),
            ("Search visibility is no longer about stuffing keywords—it is about technical speed, semantic authority, and capturing buyers with real commercial intent across both Google SERPs and AI answer engines (AEO & GEO). We build compounding organic revenue assets.",
             "Search behavior has shifted permanently—buyers now ask ChatGPT, Gemini, Perplexity, and Google AI Overviews for direct recommendations. Answer Engine Optimization (AEO) and Generative Engine Optimization (GEO) structure your brand's entities, JSON-LD schema, citation-ready content, and third-party authority so AI engines cite and recommend you first."),
            ("How long does SEO take to deliver measurable results?", "How do AEO & GEO differ from traditional SEO?"),
            ("Technical fixes improve crawling within weeks, while competitive commercial rankings and compounding organic revenue typically accelerate across months 3 to 6.",
             "Traditional SEO focuses on ranking web pages in Google's blue links, whereas AEO & GEO optimize your entities, schema, and verifiable facts so AI assistants (ChatGPT, Gemini, Perplexity) synthesize and cite your brand directly in generated answers."),
            ("Should we run SEO and Google Ads together?", "How long does AEO & GEO take to show measurable AI citations?"),
            ("Yes. Paid search query conversion data sharpens your SEO priorities, while stronger SEO landing pages boost Google Ads Quality Scores and lower CPCs.",
             "Live web-retrieval engines like Perplexity, ChatGPT Search, and Google AI Overviews often reflect structured schema and direct-answer content updates within 2 to 6 weeks, while broader LLM brand authority compounds over 3 to 6 months."),
            ("Do you ever use risky automated backlinks?", "Should we run AEO & GEO alongside traditional SEO?"),
            ("Never. Every technical and off-page initiative adheres strictly to Google's official Search Essentials and E-E-A-T standards.",
             "Yes. Strong technical SEO, fast crawlable pages, and domain authority provide the exact retrieval foundation that AI answer engines rely on to trust and cite your brand."),
            ("How do you report SEO progress?", "How do you measure and report AI Search visibility?"),
            ("Via live Looker Studio dashboards integrating Google Search Console and GA4—tracking impressions, clicks, rankings, and organic conversions.",
             "We track Share of Model across target buyer prompts on ChatGPT, Gemini, Perplexity, and Google AI Overviews alongside GA4 AI-referral traffic and conversions."),
            ("Contact us for a complimentary technical SEO &amp; AI visibility audit.", "Contact us for a complimentary AI Search (AEO &amp; GEO) visibility audit."),
            ("Contact us for a complimentary technical SEO & AI visibility audit.", "Contact us for a complimentary AI Search (AEO & GEO) visibility audit."),
            ("/en/seo/", "/en/aeo-geo/"),
            ("/hizmetler/seo/", "/hizmetler/aeo-geo/"),
        ]
    else:
        replacements = [
            ("SEO Ajansı | Roasist", "Yapay Zeka Aramaları (AEO & GEO) | Roasist"),
            ("SEO Sürecimiz", "AEO & GEO Sürecimiz"),
            (">seo<", ">yapay zeka aramaları (aeo &amp; geo)<"),
            ('"children":"seo"', '"children":"yapay zeka aramaları (aeo & geo)"'),
            ("Aramada <br />\n<em>organik</em><br />\nliderlik.", "Yapay zeka <br />\n<em>yanıtlarında</em><br />\nliderlik."),
            ("Aramada <br />\\n<em>organik</em><br />\\nliderlik.", "Yapay zeka <br />\\n<em>yanıtlarında</em><br />\\nliderlik."),
            ("SEO (Arama Motoru Optimizasyonu), bir web sitesinin Google ve yapay zeka arama motorlarında (ChatGPT, Perplexity, Google AI) hedef anahtar kelimelerde üst sıralarda yer alarak reklamsız, sürdürülebilir ve yüksek dönüşümlü organik trafik kazanmasını sağlayan teknik, içeriksel ve otorite odaklı büyüme disiplinidir.",
             "AEO (Yanıt Motoru Optimizasyonu) ve GEO (Üretken Motor Optimizasyonu), markanızın ChatGPT, Google Gemini, Perplexity ve Google AI Overviews yanıtlarında güvenilir birincil kaynak olarak önerilmesini ve alıntılanmasını sağlayan yeni nesil yapay zeka görünürlük disiplinidir."),
            ("SEO Nedir ve Nasıl Yapılır?", "AEO & GEO Nedir ve Nasıl Yapılır?"),
            ("Roasist, kalite ve performans odaklı çalışma prensibini gözetir, doğru ölçümleme için gerekli entegrasyonları ve teknolojileri kullanır, detaylı analizler sonucu SEO stratejinizi inşa eder, verilerin ışığında süreçleri daha iyi hale getirir ve anlamlı raporlar ile sürece sizi de dahil eder. SEO (Search Engine Optimization), online pazarlama dünyasında oldukça önemli bir konudur. Bir web sitesinin arama motorları tarafından daha yüksek sıralarda görünmesi, potansiyel müşteriler tarafından daha kolay bulunması anlamına gelir. Fakat SEO’nun ne olduğunu tam olarak anlamak için bu tanımın ötesine bakmak gerekmektedir.",
             "Arama alışkanlıkları kökten değişiyor: kullanıcılar artık yalnızca mavi bağlantılara tıklamak yerine ChatGPT, Gemini, Perplexity ve Google AI Overviews üzerinden doğrudan yanıt ve marka önerisi alıyor. AEO (Answer Engine Optimization) ve GEO (Generative Engine Optimization), markanızın bu yapay zeka yanıtlarında birincil kaynak olarak alıntılanmasını ve önerilmesini sağlar. Roasist olarak varlık (Entity) mimarisi, JSON-LD Schema, yanıt odaklı içerik ve dijital otorite sinyalleriyle markanızı yapay zeka çağının lideri konumuna taşıyoruz."),
            ("SEO nedir ve işletmem için neden önemlidir?", "AEO ve GEO nedir, klasik SEO'dan farkı nedir?"),
            ("SEO, “Arama Motoru Optimizasyonu”nun kısaltılmış halidir. Google ve diğer küresel arama motorlarında bir web sitesinin görünürlüğünü ve organik arama sonuçlarını iyileştirmek için kullanılan uzun vadeli bir pazarlama stratejisidir. Artan web sitesi trafiği, nitelikli potansiyel müşteri kazanımı, marka bilinirliği ve reklama bağımlı kalmadan sürdürülebilir satış sağlar.",
             "Klasik SEO web sitenizi Google arama sonuçlarında sıralamaya odaklanırken; AEO (Yanıt Motoru Optimizasyonu) ve GEO (Üretken Motor Optimizasyonu) markanızın ChatGPT, Gemini, Perplexity ve Google AI Overviews tarafından doğrudan önerilen ve alıntılanan kaynak olmasını sağlar."),
            ("SEO çalışmalarından ne kadar sürede sonuç alınır?", "AEO & GEO çalışmalarından ne kadar sürede sonuç alınır?"),
            ("SEO çalışması için zaman çerçevesi web sitenizin mevcut teknik durumuna, sektör rekabetine ve içerik derinliğine göre değişebilir. Teknik düzeltmeler ilk haftalarda indekslemeye yansırken, rekabetçi kelimelerde kalıcı ve güçlü organik büyüme sonuçlarının görülmesi ortalama 3 ile 6 ay arasında gerçekleşir.",
             "Canlı web taraması yapan Perplexity, ChatGPT Search ve Google AI Overviews gibi motorlarda teknik Schema ve yanıt odaklı içerik iyileştirmeleri 2–6 hafta içinde görünürlük üretmeye başlar; genel LLM marka otoritesi ise 3–6 ayda kalıcı biçimde güçlenir."),
            ("En sık yapılan SEO hataları nelerdir?", "ChatGPT, Gemini ve Perplexity'de markamız nasıl önerilir?"),
            ("En yaygın SEO hataları arasında anahtar kelime doldurma (keyword stuffing), kopya veya zayıf içerik kullanımı, bozuk/404 iç linkler, yavaş açılan mobil sayfalar, eksik H1/meta etiketleri ve kalitesiz backlink alımları yer alır. Roasist olarak tüm süreci Google’ın resmi kalite yönergelerine %100 uyumlu yürütüyoruz.",
             "Yapay zeka modelleri net yapılandırılmış JSON-LD Schema verilerine, doğrudan soruya yanıt veren yüksek bilgi yoğunluklu içeriklere, tutarlı varlık (Entity) sinyallerine ve güvenilir üçüncü parti yayınlardaki marka alıntılarına dayanarak öneri üretir."),
            ("SEO ve Google Ads (SEM) birlikte yürütülmeli mi?", "Klasik SEO ile AEO & GEO birlikte yürütülmeli mi?"),
            ("Kesinlikle evet. Google Ads kampanyalarından elde edilen yüksek dönüşümlü arama terimi verileri SEO içerik stratejisini beslerken, SEO ile güçlenen açılış sayfası kalitesi Google Ads Kalite Puanınızı (Quality Score) artırarak tıklama başı maliyetlerinizi (CPC) düşürür.",
             "Kesinlikle evet. Güçlü bir teknik SEO ve alan adı otoritesi, yapay zeka yanıt motorlarının web sitenizi güvenilir kaynak olarak taraması ve alıntılaması için temel omurgayı oluşturur."),
            ("SEO (Arama Motoru Optimizasyonu) sürecinde raporlama ve şeffaflık nasıl sağlanır?", "Yapay zeka görünürlüğü (Share of Model) nasıl ölçülür ve raporlanır?"),
            ("Tüm reklam ve analitik hesaplarınız kendi mülkiyetinizde kalır. Canlı Looker Studio veri panellerimizle harcanan bütçeyi, dönüşümleri ve ROAS performansını 7/24 anlık olarak takip edebilirsiniz.",
             "Sektörünüzdeki kritik kullanıcı sorularında ChatGPT, Gemini, Perplexity ve AI Overviews üzerindeki marka alıntı payınızı (Share of Model) ve GA4 yapay zeka yönlendirme trafiğini canlı panellerle şeffaf biçimde raporluyoruz."),
            ("Roasist ile SEO (Arama Motoru Optimizasyonu) çalışmalarına nasıl başlayabiliriz?", "Roasist ile AEO & GEO çalışmalarına nasıl başlayabiliriz?"),
            ("İletişim sayfamızdan veya 'Projeye Başlayın' butonundan bize ulaştığınızda, mevcut dijital varlıklarınızı ücretsiz analiz ediyor ve markanıza özel büyüme yol haritasını sunuyoruz.",
             "İletişim sayfamızdan bize ulaştığınızda markanızın ChatGPT, Gemini ve Google AI Overviews üzerindeki mevcut görünürlüğünü ücretsiz analiz edip size özel AEO & GEO yol haritasını sunuyoruz."),
            ("/hizmetler/seo/", "/hizmetler/aeo-geo/"),
            ("/en/seo/", "/en/aeo-geo/"),
        ]

    matches, _, full = extract_flight_chunks(text)
    recs = parse_flight_stream(full)
    for rec in recs:
        val = rec[2]
        for old, new in replacements:
            val = val.replace(old, new)
        rec[2] = val
    new_full = serialize_flight_stream(recs)

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
    print(f"[OK] Created AEO & GEO page {os.path.relpath(dst_path, REPO_ROOT)}")


def wire_aeo_link_on_homepage(home_path, is_en=False):
    text = open(home_path, "r", encoding="utf-8").read()
    changed = False
    if is_en:
        old_ssr = '<a class="ServicesPanel_tag__JYwRk" href="service/seo">AI Search (AEO &amp; GEO)</a>'
        new_ssr = '<a class="ServicesPanel_tag__JYwRk" href="service/ai-search-aeo-geo">AI Search (AEO &amp; GEO)</a>'
        if old_ssr in text:
            text = text.replace(old_ssr, new_ssr, 1)
            changed = True
        old_fl = '\\"slug\\":\\"seo\\",\\"title\\":\\"AI Search (AEO \\u0026 GEO)\\"'
        old_fl2 = '\\"slug\\":\\"seo\\",\\"title\\":\\"AI Search (AEO & GEO)\\"'
        if old_fl in text:
            text = text.replace(old_fl, '\\"slug\\":\\"ai-search-aeo-geo\\",\\"title\\":\\"AI Search (AEO \\u0026 GEO)\\"', 1)
            changed = True
        elif old_fl2 in text:
            text = text.replace(old_fl2, '\\"slug\\":\\"ai-search-aeo-geo\\",\\"title\\":\\"AI Search (AEO & GEO)\\"', 1)
            changed = True
        if "'ai-search-aeo-geo':" not in text and "'seo':" in text:
            text = text.replace("'seo': '/en/seo/',", "'seo': '/en/seo/',\n    'ai-search-aeo-geo': '/en/aeo-geo/',")
            changed = True
    else:
        old_ssr = '<a class="ServicesPanel_tag__JYwRk" href="service/seo">Yapay Zeka Aramaları (AEO &amp; GEO)</a>'
        new_ssr = '<a class="ServicesPanel_tag__JYwRk" href="service/yapay-zeka-seo">Yapay Zeka Aramaları (AEO &amp; GEO)</a>'
        if old_ssr in text:
            text = text.replace(old_ssr, new_ssr, 1)
            changed = True
        old_fl = '\\"slug\\":\\"seo\\",\\"title\\":\\"Yapay Zeka Aramaları (AEO \\u0026 GEO)\\"'
        old_fl2 = '\\"slug\\":\\"seo\\",\\"title\\":\\"Yapay Zeka Aramaları (AEO & GEO)\\"'
        if old_fl in text:
            text = text.replace(old_fl, '\\"slug\\":\\"yapay-zeka-seo\\",\\"title\\":\\"Yapay Zeka Aramaları (AEO \\u0026 GEO)\\"', 1)
            changed = True
        elif old_fl2 in text:
            text = text.replace(old_fl2, '\\"slug\\":\\"yapay-zeka-seo\\",\\"title\\":\\"Yapay Zeka Aramaları (AEO & GEO)\\"', 1)
            changed = True
        if "'yapay-zeka-seo':" not in text and "'seo':" in text:
            text = text.replace("'seo': '/hizmetler/seo/',", "'seo': '/hizmetler/seo/',\n    'yapay-zeka-seo': '/hizmetler/aeo-geo/',")
            changed = True

    if changed:
        with open(home_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"[OK] Wired AEO & GEO pill link in {os.path.relpath(home_path, REPO_ROOT)}")
    else:
        print(f"[OK] AEO & GEO pill link already wired in {os.path.relpath(home_path, REPO_ROOT)}")


def main():
    # 1. Wire AEO pill on Homepages
    for rel, is_en in [
        ("public/kota-roasist-local.html", False),
        ("public/en/index.html", True),
        ("dist/index.html", False),
        ("dist/en/index.html", True),
    ]:
        p = os.path.join(REPO_ROOT, rel)
        if os.path.exists(p):
            wire_aeo_link_on_homepage(p, is_en=is_en)

    # 2. Upgrade SEO & 360 pages
    direct_jobs = [
        ("public/kota-roasist-local.html", "public/hizmetler/seo/index.html", "seo", TR_SEO_SERVICES, SEO_STAGES, SEO_TR_STEPS, False, False),
        ("public/en/index.html", "public/en/seo/index.html", "seo", EN_SEO_SERVICES, SEO_STAGES, SEO_EN_STEPS, True, False),
        ("dist/index.html", "dist/hizmetler/seo/index.html", "seo", TR_SEO_SERVICES, SEO_STAGES, SEO_TR_STEPS, False, True),
        ("dist/en/index.html", "dist/en/seo/index.html", "seo", EN_SEO_SERVICES, SEO_STAGES, SEO_EN_STEPS, True, True),
        ("public/kota-roasist-local.html", "public/hizmetler/360-derece-dijital-pazarlama-yonetimi/index.html", "g360", TR_360_SERVICES, G360_STAGES, G360_TR_STEPS, False, False),
        ("public/en/index.html", "public/en/360-digital-marketing-management/index.html", "g360", EN_360_SERVICES, G360_STAGES, G360_EN_STEPS, True, False),
        ("dist/index.html", "dist/hizmetler/360-derece-dijital-pazarlama-yonetimi/index.html", "g360", TR_360_SERVICES, G360_STAGES, G360_TR_STEPS, False, True),
        ("dist/en/index.html", "dist/en/360-digital-marketing-management/index.html", "g360", EN_360_SERVICES, G360_STAGES, G360_EN_STEPS, True, True),
    ]
    for home_rel, target_rel, key, svcs, stages, steps, is_en, is_gh in direct_jobs:
        home_src = os.path.join(REPO_ROOT, home_rel)
        target = os.path.join(REPO_ROOT, target_rel)
        if not os.path.exists(home_src) or not os.path.exists(target):
            print(f"[SKIP] Missing {target_rel} or {home_rel}")
            continue
        stats = get_homepage_statistics(home_src)
        sync_stats(target, stats, is_en=is_en, is_gh_pages=is_gh)
        update_process(target, steps, is_en=is_en, is_gh_pages=is_gh)
        update_channel_campaigns(target, key, svcs, stages, is_gh_pages=is_gh)

    # 3. Create & upgrade dedicated AEO & GEO pages
    aeo_jobs = [
        ("public/kota-roasist-local.html", "public/hizmetler/seo/index.html", "public/hizmetler/aeo-geo/index.html", False, False),
        ("public/en/index.html", "public/en/seo/index.html", "public/en/aeo-geo/index.html", True, False),
        ("dist/index.html", "dist/hizmetler/seo/index.html", "dist/hizmetler/aeo-geo/index.html", False, True),
        ("dist/en/index.html", "dist/en/seo/index.html", "dist/en/aeo-geo/index.html", True, True),
    ]
    for home_rel, src_rel, dst_rel, is_en, is_gh in aeo_jobs:
        home_src = os.path.join(REPO_ROOT, home_rel)
        src = os.path.join(REPO_ROOT, src_rel)
        dst = os.path.join(REPO_ROOT, dst_rel)
        if not os.path.exists(home_src) or not os.path.exists(src):
            print(f"[SKIP] Missing {src_rel} or {home_rel}")
            continue
        create_aeo_page_from_seo(src, dst, is_en=is_en)
        stats = get_homepage_statistics(home_src)
        sync_stats(dst, stats, is_en=is_en, is_gh_pages=is_gh)
        update_process(dst, AEO_EN_STEPS if is_en else AEO_TR_STEPS, is_en=is_en, is_gh_pages=is_gh)
        update_channel_campaigns(dst, "aeo", EN_AEO_SERVICES if is_en else TR_AEO_SERVICES, AEO_STAGES, is_gh_pages=is_gh)


if __name__ == "__main__":
    main()
