import glob
import json
import os
import re

ROOT_DIR = "/home/antigravity/Roasist/roasist-web"
PUBLIC_DIR = f"{ROOT_DIR}/public"
DIST_DIR = f"{ROOT_DIR}/dist"

# 1. Patch webpack and layout chunks so homepage links preserve /roasist-web on GitHub Pages
wp_file = f"{PUBLIC_DIR}/_next/static/chunks/webpack-1b6a5d5ee0c4d44d.js"
wp_txt = open(wp_file, "r", encoding="utf-8").read()
wp_old = 'try{if(window.location.pathname!=="/"||window.location.search)window.history.replaceState(null,"","/")}catch(e){};'
wp_new = 'try{if(window.__ROASIST_BASE__===void 0)window.__ROASIST_BASE__=window.location.pathname.startsWith("/roasist-web")?"/roasist-web":"";if(window.location.pathname!=="/"||window.location.search)window.history.replaceState(null,"","/")}catch(e){};'
if wp_old in wp_txt:
    wp_txt = wp_txt.replace(wp_old, wp_new)
    open(wp_file, "w", encoding="utf-8").write(wp_txt)

layout_file = f"{PUBLIC_DIR}/_next/static/chunks/app/layout-69eda66b9da6597e.js"
layout_txt = open(layout_file, "r", encoding="utf-8").read()
layout_old = 'window.location.href=e}'
layout_new = 'window.location.href=(e.startsWith("/")&&window.__ROASIST_BASE__&&!e.startsWith(window.__ROASIST_BASE__))?(window.__ROASIST_BASE__+e):e}'
if layout_old in layout_txt:
    layout_txt = layout_txt.replace(layout_old, layout_new)
    open(layout_file, "w", encoding="utf-8").write(layout_txt)

# 2. Extract exact Header, PrimaryNavigation, and Footer from public/kota-roasist-local.html
home_html = open(f"{PUBLIC_DIR}/kota-roasist-local.html", "r", encoding="utf-8").read()
h_start = home_html.find('<nav class="PrimaryNavigation_navigation__l8Jgb">')
h_end = home_html.find('<main>', h_start)
kota_header_and_nav = home_html[h_start:h_end]

f_start = home_html.find('<footer class="Footer_footer__pQtti"')
f_end = home_html.find('</footer>', f_start) + 9
kota_footer = home_html[f_start:f_end]

# Load services and clients data
services_bundle = json.load(open(f"{ROOT_DIR}/scripts/services_data.json", "r", encoding="utf-8"))
services_data = services_bundle["servicesData"]
default_why_us = services_bundle["defaultWhyUs"]
default_process_steps = services_bundle["defaultProcessSteps"]
clients_data = json.load(open(f"{ROOT_DIR}/src/data/clients.json", "r", encoding="utf-8"))

all_service_pills = [
    ("360° Dijital Pazarlama", "/hizmetler/360-derece-dijital-pazarlama-yonetimi/"),
    ("Performans Pazarlaması", "/hizmetler/performans-pazarlamasi/"),
    ("Google Ads", "/hizmetler/performans-pazarlamasi/google-reklamlari/"),
    ("Instagram Reklamları", "/hizmetler/performans-pazarlamasi/instagram-reklamlari/"),
    ("Facebook Reklamları", "/hizmetler/performans-pazarlamasi/facebook-reklamlari/"),
    ("TikTok Reklamları", "/hizmetler/performans-pazarlamasi/tiktok-reklamlari/"),
    ("LinkedIn Reklamları", "/hizmetler/performans-pazarlamasi/linkedin-reklamlari/"),
    ("Yandex Reklamları", "/hizmetler/performans-pazarlamasi/yandex-reklamlari/"),
    ("Kurumsal SEO & AEO", "/hizmetler/seo/"),
    ("Web Tasarım & CRO", "/hizmetler/web-tasarim/"),
    ("Grafik & Kreatif Tasarım", "/hizmetler/grafik-tasarim/"),
]

# Shared KOTA Inner Page Design System CSS & Interactive JS
KOTA_INNER_HEAD_ASSETS = """
<link rel="stylesheet" href="/_next/static/css/f9cbc29e5dcba8c4.css"/>
<link rel="stylesheet" href="/_next/static/css/84191844b30595bc.css"/>
<link rel="stylesheet" href="/_next/static/css/053ade63481ccabc.css"/>
<link rel="stylesheet" href="/_next/static/css/e36a1a112c1c5ec8.css"/>
<link rel="stylesheet" href="/_next/static/css/13f753c524b3db20.css"/>
<style>
  :root {
    --roasist-violet: #7602FF;
    --roasist-indigo: #4F46E5;
    --roasist-cyan: #00D2FF;
    --montreal: "__montreal_a78db3", "__montreal_Fallback_a78db3", -apple-system, BlinkMacSystemFont, sans-serif;
    --syne: "__syne_ab8453", "__syne_Fallback_ab8453", sans-serif;
  }
  body.kota-inner-body {
    margin: 0;
    background-color: #EFEDF4;
    color: #0F0A1C;
    font-family: var(--montreal), -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    overflow-x: hidden;
  }
  /* Ambient KOTA Aurora Shader Background */
  .kota-aurora-bg {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    z-index: 0;
    pointer-events: none;
    background:
      radial-gradient(circle at 82% 22%, rgba(0, 210, 255, 0.34) 0%, rgba(118, 2, 255, 0.42) 28%, rgba(79, 70, 229, 0.25) 52%, transparent 74%),
      radial-gradient(circle at 65% 78%, rgba(168, 85, 247, 0.30) 0%, rgba(118, 2, 255, 0.22) 38%, transparent 70%),
      #EFEDF4;
    filter: saturate(1.15);
  }
  .kota-inner-main {
    position: relative;
    z-index: 2;
  }
  .kota-inner-main section:not(.Partners_partners__jBo8y):not(.FaqsList_faqsList__3yyiS) > .container > *,
  .kota-inner-main .kota-dark-zone > .container > * {
    grid-column: 1 / -1 !important;
    width: 100%;
  }
  /* KOTA Inner Hero */
  .kota-inner-hero {
    min-height: auto;
    padding: 8.5rem 0 3.5rem;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    position: relative;
  }
  .kota-breadcrumb {
    display: inline-flex;
    width: fit-content !important;
    justify-self: start;
    align-items: center;
    gap: 0.5rem;
    padding: 0.45rem 1rem;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.72);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(118, 2, 255, 0.24);
    font-size: 0.85rem;
    color: #1E1035;
    margin-bottom: 2rem;
    text-decoration: none;
  }
  .kota-breadcrumb a {
    color: #5B4B7A;
    text-decoration: none;
    transition: color 0.2s ease;
  }
  .kota-breadcrumb a:hover {
    color: #7602FF;
  }
  .kota-breadcrumb strong {
    color: #7602FF;
    font-weight: 600;
  }
  .kota-hero-grid {
    display: grid;
    grid-template-columns: repeat(12, 1fr);
    gap: 2rem;
    align-items: end;
  }
  .kota-hero-title-col {
    grid-column: span 12;
  }
  .kota-hero-side-col {
    grid-column: span 12;
  }
  @media (min-width: 960px) {
    .kota-hero-title-col {
      grid-column: span 8;
    }
    .kota-hero-side-col {
      grid-column: span 4;
    }
  }
  .kota-display-h1 {
    font-family: var(--montreal), -apple-system, BlinkMacSystemFont, sans-serif;
    font-weight: 400;
    font-size: clamp(2.8rem, 6.8vw, 6.2rem);
    line-height: 0.96;
    letter-spacing: -0.04em;
    margin: 0;
    color: #0B0616;
  }
  .kota-display-h1 .indent-line {
    display: block;
    padding-left: clamp(1.5rem, 7vw, 6.5rem);
    color: #7602FF;
  }
  .kota-hero-lead {
    font-size: clamp(1.08rem, 1.35vw, 1.28rem);
    line-height: 1.42;
    color: #1A102E;
    margin: 0 0 1.75rem;
  }
  .kota-hero-badges-bar {
    margin-top: 4rem;
    padding-top: 1.75rem;
    border-top: 1px solid rgba(118, 2, 255, 0.14);
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 2.25rem;
  }
  .kota-hero-badges-bar img {
    height: 36px;
    width: auto;
    object-fit: contain;
  }
  /* KOTA Glassmorphic Section Cards */
  .kota-section {
    padding: 5.5rem 0;
    position: relative;
  }
  .kota-section-header {
    display: grid;
    grid-template-columns: repeat(12, 1fr);
    gap: 2rem;
    align-items: end;
    margin-bottom: 3.5rem;
  }
  .kota-section-header h2 {
    grid-column: span 12;
    font-size: clamp(2.2rem, 4.8vw, 4.4rem);
    font-weight: 400;
    line-height: 1;
    letter-spacing: -0.03em;
    margin: 0;
  }
  .kota-section-header p {
    grid-column: span 12;
    font-size: 1.15rem;
    line-height: 1.45;
    color: #3B2D54;
    margin: 0;
  }
  @media (min-width: 900px) {
    .kota-section-header h2 { grid-column: span 7; }
    .kota-section-header p { grid-column: span 5; }
  }
  /* KOTA 12.5rem Curved Panel */
  .kota-curved-panel {
    background: rgba(255, 255, 255, 0.86);
    backdrop-filter: blur(24px) saturate(150%);
    -webkit-backdrop-filter: blur(24px) saturate(150%);
    border: 1.5px solid rgba(118, 2, 255, 0.24);
    box-shadow: 0 28px 64px -16px rgba(118, 2, 255, 0.12), inset 0 1px 0 rgba(255, 255, 255, 0.95);
    border-radius: 2rem 8rem 2rem 2rem;
    padding: clamp(2rem, 4.5vw, 4.25rem);
    margin-bottom: 3.5rem;
  }
  @media (min-width: 960px) {
    .kota-curved-panel {
      border-radius: 3rem 12.5rem 3rem 3rem;
    }
  }
  /* KOTA Asymmetric Approach Cards (10px 100px 10px 10px) */
  .kota-cards-grid-3 {
    display: grid;
    grid-template-columns: repeat(1, 1fr);
    gap: 2rem;
  }
  @media (min-width: 850px) {
    .kota-cards-grid-3 {
      grid-template-columns: repeat(3, 1fr);
      gap: 2.25rem;
    }
  }
  .kota-asym-card {
    background: rgba(255, 255, 255, 0.74);
    backdrop-filter: blur(20px) saturate(140%);
    -webkit-backdrop-filter: blur(20px) saturate(140%);
    border: 1.5px solid rgba(118, 2, 255, 0.22);
    box-shadow: 0 20px 48px -14px rgba(118, 2, 255, 0.10);
    border-radius: 14px 96px 14px 14px;
    padding: 2.25rem 2rem;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: transform 0.3s cubic-bezier(0.22, 1, 0.36, 1), border-color 0.3s ease;
  }
  .kota-asym-card:hover {
    transform: translateY(-6px);
    border-color: #7602FF;
  }
  .kota-step-num {
    font-size: 1.1rem;
    font-weight: 700;
    color: #7602FF;
    margin-bottom: 1.5rem;
    display: inline-block;
  }
  .kota-metric-val {
    font-size: clamp(2.1rem, 3.4vw, 3.1rem);
    font-weight: 400;
    letter-spacing: -0.03em;
    line-height: 1.05;
    background: linear-gradient(135deg, #7602FF 0%, #4F46E5 60%, #00D2FF 100%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    margin: 0 0 0.75rem;
  }
  .kota-asym-card h3 {
    font-size: 1.55rem;
    font-weight: 500;
    line-height: 1.15;
    margin: 0 0 0.85rem;
    color: #0F0A1C;
  }
  .kota-asym-card p {
    font-size: 1.02rem;
    line-height: 1.48;
    color: #3B2D54;
    margin: 0;
  }
  /* KOTA Comparison Table */
  .kota-comp-row {
    display: grid;
    grid-template-columns: 1fr;
    gap: 1rem;
    padding: 1.4rem 1.5rem;
    border-bottom: 1px solid rgba(118, 2, 255, 0.14);
    align-items: center;
  }
  @media (min-width: 850px) {
    .kota-comp-row {
      grid-template-columns: 1.1fr 1.2fr 1.4fr;
      gap: 2rem;
    }
  }
  .kota-comp-row:last-child { border-bottom: none; }
  .kota-comp-crit { font-weight: 600; color: #0F0A1C; font-size: 1.08rem; }
  .kota-comp-trad { color: #64748B; font-size: 0.98rem; }
  .kota-comp-roas {
    color: #160933;
    font-weight: 500;
    background: rgba(118, 2, 255, 0.08);
    border: 1px solid rgba(118, 2, 255, 0.26);
    padding: 0.75rem 1.1rem;
    border-radius: 1rem;
  }
  /* Dark Section (#000) */
  .kota-dark-zone {
    background-color: #000000;
    color: #FFFFFF;
    padding: 6rem 0 2rem;
    position: relative;
    z-index: 3;
  }
  /* Reference Logo Card in /referanslar/ */
  .kota-ref-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1.25rem;
  }
  @media (min-width: 640px) {
    .kota-ref-grid { grid-template-columns: repeat(3, 1fr); }
  }
  @media (min-width: 1024px) {
    .kota-ref-grid { grid-template-columns: repeat(5, 1fr); gap: 1.5rem; }
  }
  .kota-ref-card {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(118, 2, 255, 0.28);
    border-radius: 1rem 2.5rem 1rem 1rem;
    padding: 1.6rem 1.2rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 0.85rem;
    transition: transform 0.3s ease, border-color 0.3s ease, background 0.3s ease;
  }
  .kota-ref-card:hover {
    transform: translateY(-4px);
    border-color: #7602FF;
    background: rgba(118, 2, 255, 0.12);
  }
  .kota-ref-card img {
    height: 52px;
    width: auto;
    max-width: 85%;
    object-fit: contain;
  }
  .kota-ref-card span {
    font-size: 0.78rem;
    color: rgba(255, 255, 255, 0.65);
    letter-spacing: 0.02em;
    text-align: center;
  }
  /* Contact Form Inputs */
  .kota-input {
    width: 100%;
    padding: 1rem 1.25rem;
    border-radius: 1rem;
    border: 1.5px solid rgba(118, 2, 255, 0.24);
    background: rgba(255, 255, 255, 0.9);
    font-family: inherit;
    font-size: 1rem;
    color: #0F0A1C;
    outline: none;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
    box-sizing: border-box;
  }
  .kota-input:focus {
    border-color: #7602FF;
    box-shadow: 0 0 0 4px rgba(118, 2, 255, 0.12);
  }
  .kota-submit-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.75rem;
    padding: 1.1rem 2.2rem;
    border-radius: 999px;
    border: none;
    background: linear-gradient(135deg, #7602FF 0%, #4F46E5 100%);
    color: #FFFFFF;
    font-family: inherit;
    font-size: 1.08rem;
    font-weight: 600;
    cursor: pointer;
    box-shadow: 0 12px 30px -6px rgba(118, 2, 255, 0.45);
    transition: transform 0.25s ease, box-shadow 0.25s ease;
    text-decoration: none;
  }
  .kota-submit-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 18px 38px -6px rgba(118, 2, 255, 0.6);
  }
  /* Make sure FadeIn/FadeInUp elements are visible without waiting on GSAP */
  .kota-inner-body .FadeIn_container__bjQVL,
  .kota-inner-body .FadeInUp_container___uxva,
  .kota-inner-body .FadeInRotate_container__QE9u9 {
    opacity: 1 !important;
    transform: none !important;
  }
</style>
"""

KOTA_INNER_SCRIPT = """
<script>
document.addEventListener("DOMContentLoaded", function() {
  // 1. Auto-prefix internal links when hosted under /roasist-web on GitHub Pages
  var base = window.location.pathname.startsWith("/roasist-web") ? "/roasist-web" : "";
  if (base) {
    document.querySelectorAll("a[href^='/']").forEach(function(a) {
      var href = a.getAttribute("href");
      if (href && !href.startsWith(base) && !href.startsWith("//")) {
        a.setAttribute("href", base + href);
      }
    });
  }

  // 2. Interactive KOTA Full-Screen Menu Drawer Toggle
  var toggleBtn = document.querySelector(".MenuToggle_toggle__22284");
  var navDrawer = document.querySelector(".PrimaryNavigation_navigation__22284");
  var headerEl = document.querySelector(".Header_header__KwdYD");
  var menuOpen = false;
  if (toggleBtn && navDrawer) {
    toggleBtn.style.pointerEvents = "all";
    toggleBtn.style.cursor = "pointer";
    toggleBtn.addEventListener("click", function() {
      menuOpen = !menuOpen;
      if (menuOpen) {
        navDrawer.style.opacity = "1";
        navDrawer.style.pointerEvents = "all";
        navDrawer.setAttribute("data-lenis-prevent", "true");
        document.body.classList.add("dark");
        navDrawer.querySelectorAll("li").forEach(function(li) {
          li.style.opacity = "1";
          li.style.transform = "translate(0, 0)";
        });
      } else {
        navDrawer.style.opacity = "0";
        navDrawer.style.pointerEvents = "none";
        document.body.classList.remove("dark");
      }
    });
  }

  // 3. Copy email tooltip in Footer
  var emailBtn = document.querySelector(".Footer_email__nLajh");
  var tooltip = emailBtn ? emailBtn.querySelector(".CopyText_tooltip__HuxWa") : null;
  if (emailBtn) {
    emailBtn.addEventListener("click", function() {
      if (navigator.clipboard) {
        navigator.clipboard.writeText("info@roasist.com");
      }
      if (tooltip) {
        var orig = tooltip.textContent;
        tooltip.textContent = "Kopyalandı! ✓";
        tooltip.style.opacity = "1";
        setTimeout(function() {
          tooltip.textContent = orig;
          tooltip.style.opacity = "";
        }, 2200);
      }
    });
  }

  // 4. Switch header theme when scrolled into dark zone
  var darkZone = document.querySelector(".kota-dark-zone");
  if (darkZone && headerEl) {
    window.addEventListener("scroll", function() {
      if (menuOpen) return;
      var rect = darkZone.getBoundingClientRect();
      if (rect.top <= 80) {
        document.body.classList.add("dark");
      } else {
        document.body.classList.remove("dark");
      }
    }, { passive: true });
  }
});
</script>
"""

def extract_head_seo(existing_html_path, fallback_title, fallback_desc):
    if os.path.exists(existing_html_path):
        raw = open(existing_html_path, "r", encoding="utf-8").read()
        head_m = re.search(r"<head[^>]*>(.*?)</head>", raw, re.S | re.I)
        if head_m:
            head_inner = head_m.group(1)
            # Keep meta, title, link rel="canonical", link rel="sitemap", and application/ld+json scripts
            kept = []
            for tag in re.findall(r"<title>.*?</title>|<meta[^>]+>|<link[^>]+rel=[\"'](?:canonical|icon|sitemap)[^\"']*[\"'][^>]*>|<script[^>]+application/ld\+json[^>]*>.*?</script>", head_inner, re.S | re.I):
                kept.append(tag)
            if kept:
                return "\n".join(kept)
    return f'<meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/><title>{fallback_title}</title><meta name="description" content="{fallback_desc}"/>'

def render_partner_badges_bar():
    return """
    <div class="kota-hero-badges-bar">
      <img src="/images/badge-google-partner.svg" alt="Google Partner"/>
      <img src="/images/badge-meta-partner.svg" alt="Meta Business Partner"/>
      <img src="/images/badge-tiktok-partner.svg" alt="TikTok Marketing Partner"/>
      <img src="/images/badge-ai-seo.svg" alt="Yandex Ads Partner"/>
    </div>
    """

def render_service_tags_nav(active_permalink=""):
    pills = []
    for label, href in all_service_pills:
        active_style = ' style="background:linear-gradient(135deg,#7602FF 0%,#4F46E5 100%)!important;color:#fff!important;border-color:#7602FF!important;"' if href.rstrip("/") == active_permalink.rstrip("/") else ""
        pills.append(f'<a class="ServicesPanel_tag__JYwRk" href="{href}"{active_style}>{label}</a>')
    return '<div class="ServicesPanel_tags__6NQOl" style="margin-top:1.5rem">' + "".join(pills) + '</div>'

def render_faqs_accordion(faqs):
    items = []
    for f in faqs:
        items.append(f"""
        <div class="FaqsList_faq__US_6Y">
          <span class="FadeInUp_container___uxva" data-fill="false">
            <label class="FaqsList_question__6fKon">
              <span class="FaqsList_icon__54ODy">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40"><path fill="#fff" d="M17.5 40V22.5H0v-5h17.5V0h5v17.5H40v5H22.5V40h-5z"></path></svg>
              </span>
              {f["question"]}
              <input type="checkbox"/>
            </label>
            <div class="FaqsList_answer__XAnT2 prose">
              <div><p>{f["answer"]}</p></div>
            </div>
          </span>
        </div>
        """)
    return f"""
    <section class="FaqsList_faqsList__3yyiS" style="padding:4rem 0">
      <div class="container">
        <div class="FaqsList_heading__kirHR"><p>S.S.S.</p></div>
        {"".join(items)}
      </div>
    </section>
    """

def render_clients_strip(limit=15):
    logos = []
    selected_indices = [29, 14, 4, 11, 12, 23, 10, 6, 8, 20, 27, 28, 9, 22, 16]
    for idx in selected_indices[:limit]:
        c = clients_data[idx - 1]
        logos.append(f'<div class="Partners_logo__eDI8e"><img src="/images/clients-white/ref-{idx:02d}.png" alt="{c["name"]}" loading="lazy"/></div>')
    return f"""
    <section class="Partners_partners__jBo8y" style="padding-top:3rem;padding-bottom:3rem">
      <div class="container">
        <div class="Partners_headingInner__vdhDe">
          <h2 class="Partners_heading__AOTNV">
            <span>MARKA</span>
            <span class="Partners_heading__AOTNV Partners_bottom__5DSXe">ORTAKLARIMIZ</span>
          </h2>
        </div>
        <div class="Partners_logos__7QiB4">
          <div class="Partners_logosInner__Aoq5_">
            {"".join(logos)}
          </div>
        </div>
      </div>
    </section>
    """

def build_full_page(seo_head, main_inner_html):
    return f"""<!DOCTYPE html>
<html lang="tr" class="__variable_a78db3 __variable_ab8453">
<head>
{seo_head}
{KOTA_INNER_HEAD_ASSETS}
</head>
<body class="kota-inner-body">
<div class="kota-aurora-bg"></div>
{kota_header_and_nav}
<main class="kota-inner-main">
{main_inner_html}
</main>
{kota_footer}
{KOTA_INNER_SCRIPT}
</body>
</html>"""

# ==============================================================================
# A. Generate All 11 Service Pages (/hizmetler/.../index.html)
# ==============================================================================
for svc in services_data:
    permalink = svc["permalink"].strip("/")
    out_file = f"{DIST_DIR}/{permalink}/index.html"
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    seo_head = extract_head_seo(out_file, svc["seoTitle"], svc["seoDescription"])

    # Split H1 into 2 lines for KOTA display styling
    words = svc["h1"].split(" ")
    mid = max(1, len(words) // 2)
    line1 = " ".join(words[:mid])
    line2 = " ".join(words[mid:])

    metrics_cards = []
    for i, m in enumerate(svc["metrics"], 1):
        metrics_cards.append(f"""
        <div class="kota-asym-card">
          <div>
            <span class="kota-step-num">0{i}</span>
            <div class="kota-metric-val">{m["value"]}</div>
            <h3>{m["label"]}</h3>
          </div>
          <p>{m["detail"]}</p>
        </div>
        """)

    overview_paras = "".join(f'<p style="font-size:1.12rem;line-height:1.55;color:#271B3D;margin:0 0 1.25rem">{p}</p>' for p in svc["overviewParagraphs"])

    sub_features_cards = []
    for i, sf in enumerate(svc["subFeatures"], 1):
        sub_features_cards.append(f"""
        <div class="kota-asym-card">
          <div>
            <span class="kota-step-num">0{i}</span>
            <h3>{sf["title"]}</h3>
          </div>
          <p>{sf["description"]}</p>
        </div>
        """)

    process_cards = []
    for ps in svc["processSteps"]:
        process_cards.append(f"""
        <div class="kota-asym-card">
          <div>
            <span class="kota-step-num">{ps["step"]}</span>
            <h3>{ps["title"]}</h3>
          </div>
          <p>{ps["description"]}</p>
        </div>
        """)

    comp_rows = []
    for cr in svc.get("comparisonRows", []):
        comp_rows.append(f"""
        <div class="kota-comp-row">
          <div class="kota-comp-crit">{cr["criteria"]}</div>
          <div class="kota-comp-trad">{cr["traditional"]}</div>
          <div class="kota-comp-roas">✓ {cr["roasist"]}</div>
        </div>
        """)

    main_html = f"""
    <section class="kota-inner-hero">
      <div class="container">
        <div>
          <nav class="kota-breadcrumb" aria-label="Breadcrumb">
            <a href="/">Ana Sayfa</a> <span>/</span>
            <a href="/hizmetler/">Hizmetler</a> <span>/</span>
            <strong>{svc["h1"]}</strong>
          </nav>
        </div>
        <div class="kota-hero-grid">
          <div class="kota-hero-title-col">
            <h1 class="kota-display-h1">
              <span>{line1}</span>
              <span class="indent-line">{line2}</span>
            </h1>
          </div>
          <div class="kota-hero-side-col">
            <p class="kota-hero-lead"><strong>{svc["heroQuestion"]}</strong><br/><br/>{svc["aeoDirectAnswer"]}</p>
            <a href="/iletisim/" class="kota-submit-btn">Ücretsiz Strateji Analizi Al →</a>
          </div>
        </div>
        {render_partner_badges_bar()}
      </div>
    </section>

    <section class="kota-section">
      <div class="container">
        <div class="kota-cards-grid-3">
          {"".join(metrics_cards)}
        </div>
      </div>
    </section>

    <section class="kota-section" style="padding-top:1rem">
      <div class="container">
        <div class="kota-curved-panel">
          <span class="kota-step-num">360° ROASIST MİMARİSİ</span>
          <h2 style="font-size:clamp(2rem,4vw,3.5rem);font-weight:400;line-height:1.05;letter-spacing:-0.03em;margin:0 0 1.75rem">{svc["overviewHeading"]}</h2>
          {overview_paras}
          {render_service_tags_nav(svc["permalink"])}
        </div>
      </div>
    </section>

    <section class="kota-section">
      <div class="container">
        <div class="kota-section-header">
          <h2>{svc["subFeaturesTitle"]}</h2>
          <p>{svc["subFeaturesSubtitle"]}</p>
        </div>
        <div class="kota-cards-grid-3">
          {"".join(sub_features_cards)}
        </div>
      </div>
    </section>

    <section class="kota-section">
      <div class="container">
        <div class="kota-section-header">
          <h2>{svc["processTitle"]}</h2>
          <p>Veri berraklığı, şeffaf hesap mülkiyeti ve ölçülebilir büyüme adımlarımız.</p>
        </div>
        <div class="kota-cards-grid-3">
          {"".join(process_cards)}
        </div>
      </div>
    </section>

    <section class="kota-section">
      <div class="container">
        <div class="kota-curved-panel">
          <span class="kota-step-num">NEDEN ROASIST?</span>
          <h2 style="font-size:clamp(1.9rem,3.6vw,3.1rem);font-weight:400;margin:0 0 2rem">Geleneksel Ajans Yaklaşımı vs Roasist Büyüme Modeli</h2>
          {"".join(comp_rows)}
        </div>
      </div>
    </section>

    <div class="kota-dark-zone">
      {render_clients_strip(15)}
      {render_faqs_accordion(svc["faqs"])}
    </div>
    """
    open(out_file, "w", encoding="utf-8").write(build_full_page(seo_head, main_html))
    print("Built KOTA service page:", out_file)

# Also build /hizmetler/index.html hub page
os.makedirs(f"{DIST_DIR}/hizmetler", exist_ok=True)
hub_cards = []
for i, svc in enumerate(services_data, 1):
    hub_cards.append(f"""
    <a href="{svc["permalink"]}" class="kota-asym-card" style="text-decoration:none;color:inherit">
      <div>
        <span class="kota-step-num">{i:02d} — {svc["category"]}</span>
        <h3>{svc["h1"]}</h3>
        <p style="margin-bottom:1.5rem">{svc["seoDescription"]}</p>
      </div>
      <span style="color:#7602FF;font-weight:600">Hizmeti İncele →</span>
    </a>
    """)
hub_main = f"""
<section class="kota-inner-hero">
  <div class="container">
    <nav class="kota-breadcrumb"><a href="/">Ana Sayfa</a> <span>/</span> <strong>360° Hizmetlerimiz</strong></nav>
    <div class="kota-hero-grid">
      <div class="kota-hero-title-col">
        <h1 class="kota-display-h1"><span>360° dijital</span><span class="indent-line">hizmetlerimiz.</span></h1>
      </div>
      <div class="kota-hero-side-col">
        <p class="kota-hero-lead">Performans pazarlaması, kurumsal SEO & AEO, dönüşüm odaklı web tasarım ve kreatif prodüksiyon çözümlerimizle reklam bütçenizi ölçülebilir ciroya dönüştürüyoruz.</p>
        <a href="/iletisim/" class="kota-submit-btn">Teklif & Analiz Al →</a>
      </div>
    </div>
    {render_partner_badges_bar()}
  </div>
</section>
<section class="kota-section">
  <div class="container">
    <div class="kota-cards-grid-3">
      {"".join(hub_cards)}
    </div>
  </div>
</section>
<div class="kota-dark-zone">
  {render_clients_strip(15)}
</div>
"""
open(f"{DIST_DIR}/hizmetler/index.html", "w", encoding="utf-8").write(
    build_full_page(extract_head_seo(f"{DIST_DIR}/hizmetler/performans-pazarlamasi/index.html", "Roasist — 360° Dijital Pazarlama Hizmetlerimiz", "Performans pazarlaması, Google Ads, Meta reklamları, SEO, AEO ve web tasarım hizmetleri."), hub_main)
)

# ==============================================================================
# B. Generate /referanslar/index.html (All 29 Real Roasist Reference Brands + Case Studies + Testimonials)
# ==============================================================================
ref_out = f"{DIST_DIR}/referanslar/index.html"
ref_seo = extract_head_seo(ref_out, "Roasist — Referanslarımız & Seçilmiş Başarı Hikayeleri", "Roasist dijital pazarlama, performans yönetimi, SEO ve web tasarım referanslarımız.")

all_29_cards = []
for idx, c in enumerate(clients_data, 1):
    all_29_cards.append(f"""
    <div class="kota-ref-card">
      <img src="/images/clients-white/ref-{idx:02d}.png" alt="{c["alt"]}" loading="lazy"/>
      <span>{c["name"]}</span>
    </div>
    """)

ref_main = f"""
<section class="kota-inner-hero">
  <div class="container">
    <nav class="kota-breadcrumb"><a href="/">Ana Sayfa</a> <span>/</span> <strong>Referanslarımız</strong></nav>
    <div class="kota-hero-grid">
      <div class="kota-hero-title-col">
        <h1 class="kota-display-h1">
          <span>ölçülebilir</span>
          <span class="indent-line">referanslar.</span>
        </h1>
      </div>
      <div class="kota-hero-side-col">
        <p class="kota-hero-lead">Sağlıktan e-ticarete, eğitimden gayrimenkul ve teknolojiye kadar <strong>30'dan fazla ulusal ve uluslararası markanın</strong> dijital büyüme ortağıyız.</p>
        <a href="/iletisim/" class="kota-submit-btn">Markanızı Büyütelim →</a>
      </div>
    </div>
    {render_partner_badges_bar()}
  </div>
</section>

<section class="kota-section">
  <div class="container">
    <div class="kota-section-header">
      <h2>Ölçülebilir Büyüme Metriklerimiz</h2>
      <p>Veri odaklı strateji, dönüşüm mimarisi ve tam şeffaflıkla ürettiğimiz gerçek ticari sonuçlar.</p>
    </div>
    <div class="kota-cards-grid-3">
      <div class="kota-asym-card">
        <div>
          <span class="kota-step-num">01 — PERFORMANS & ROAS</span>
          <div class="kota-metric-val">4.8x</div>
          <h3>Ortalama ROAS Büyümesi</h3>
        </div>
        <p>Google Ads, Meta CAPI ve çok kanallı dönüşüm hunileriyle reklam harcaması geri dönüşünde sürdürülebilir artış.</p>
      </div>
      <div class="kota-asym-card">
        <div>
          <span class="kota-step-num">02 — ORGANİK & AEO</span>
          <div class="kota-metric-val">%310</div>
          <h3>Organik Trafik & Görünürlük</h3>
        </div>
        <p>Teknik SEO, Core Web Vitals ve yapay zeka arama motoru (AEO) optimizasyonuyla reklamsız nitelikli müşteri akışı.</p>
      </div>
      <div class="kota-asym-card">
        <div>
          <span class="kota-step-num">03 — DÖNÜŞÜM (CRO)</span>
          <div class="kota-metric-val">-%42</div>
          <h3>Müşteri Edinme Maliyeti (CPA)</h3>
        </div>
        <p>Veri odaklı açılış sayfaları, negatif kelime optimizasyonu ve kreatif testlerle birim maliyetlerde kalıcı düşüş.</p>
      </div>
    </div>
  </div>
</section>

<div class="kota-dark-zone" style="padding-top:5rem;padding-bottom:5rem">
  <div class="container">
    <div class="kota-section-header" style="margin-bottom:3rem">
      <h2 style="color:#fff">Birlikte Büyüdüğümüz Markalar (29+ Referans)</h2>
      <p style="color:rgba(255,255,255,0.75)">Farklı sektörlerde dijital dönüşümünü, performans pazarlamasını ve SEO süreçlerini yönettiğimiz iş ortaklarımız.</p>
    </div>
    <div class="kota-ref-grid">
      {"".join(all_29_cards)}
    </div>

    <div class="kota-section-header" style="margin-top:6rem;margin-bottom:3rem">
      <h2 style="color:#fff">Müşterilerimiz Ne Diyor?</h2>
      <p style="color:rgba(255,255,255,0.75)">Uzun vadeli iş ortaklarımızın Roasist deneyimi hakkındaki görüşleri.</p>
    </div>
    <div class="kota-cards-grid-3">
      <div class="kota-asym-card" style="background:#EDE9FE;color:#0F0A1C">
        <p style="font-size:1.05rem;line-height:1.55;margin-bottom:1.5rem;color:#160933">"Reklam sürecinde projeye yaklaşımları, anlaşmamızın ötesinde sorumluluk alarak grafik tasarım katkısı sunmaları ve 7/24 destekleriyle işimiz için en az bizim kadar dertlenen bir ekiple çalıştığımız için şanslıyız."</p>
        <div><strong>Burak Özhan</strong><br/><span style="font-size:0.88rem;color:#4C1D95">Project Program Coordinator</span></div>
      </div>
      <div class="kota-asym-card" style="background:#E0E7FF;color:#0F0A1C">
        <p style="font-size:1.05rem;line-height:1.55;margin-bottom:1.5rem;color:#160933">"Roasist ile yaklaşık iki senedir çalışıyoruz. Her sorumuza dürüstlükle yanıt alıyor, tüm sorunlarımızı efektif bir şekilde çözüyorlar. Öncesi-sonrası değerlendirmesi yaptığımda kazanç konusunda bize çok büyük katkıları oldu."</p>
        <div><strong>Gaye Tukar</strong><br/><span style="font-size:0.88rem;color:#3730A3">Girişimci & Kurucu</span></div>
      </div>
      <div class="kota-asym-card" style="background:#F3E8FF;color:#0F0A1C">
        <p style="font-size:1.05rem;line-height:1.55;margin-bottom:1.5rem;color:#160933">"Mesai kavramı olmaksızın sizin için çalışıyorlar. İşinde profesyonel, şeffaf ve doğrudan sonuç odaklı bir dijital pazarlama ajansı arıyorsanız Roasist'i kesinlikle tavsiye ederim."</p>
        <div><strong>Celal Kandemir</strong><br/><span style="font-size:0.88rem;color:#581C87">İşletme Sahibi</span></div>
      </div>
    </div>
  </div>
</div>
"""
open(ref_out, "w", encoding="utf-8").write(build_full_page(ref_seo, ref_main))
print("Built KOTA references page:", ref_out)

# ==============================================================================
# C. Generate /hakkimizda/index.html (Hakkımızda & Ajans Kültürü)
# ==============================================================================
about_out = f"{DIST_DIR}/hakkimizda/index.html"
about_seo = extract_head_seo(about_out, "Roasist — Hakkımızda | Veri Odaklı 360° Dijital Büyüme Ajansı", "Roasist hakkında: veri analitiği, performans pazarlaması, SEO ve kreatif web tasarım uzmanlığımız.")

why_cards = []
for i, w in enumerate(default_why_us, 1):
    why_cards.append(f"""
    <div class="kota-asym-card">
      <div>
        <span class="kota-step-num">0{i}</span>
        <h3>{w["title"]}</h3>
      </div>
      <p>{w["description"]}</p>
    </div>
    """)

proc_cards = []
for p in default_process_steps:
    proc_cards.append(f"""
    <div class="kota-asym-card">
      <div>
        <span class="kota-step-num">{p["step"]}</span>
        <h3>{p["title"]}</h3>
      </div>
      <p>{p["description"]}</p>
    </div>
    """)

about_main = f"""
<section class="kota-inner-hero">
  <div class="container">
    <nav class="kota-breadcrumb"><a href="/">Ana Sayfa</a> <span>/</span> <strong>Hakkımızda</strong></nav>
    <div class="kota-hero-grid">
      <div class="kota-hero-title-col">
        <h1 class="kota-display-h1">
          <span>veriden beslenen</span>
          <span class="indent-line">kreatif güç.</span>
        </h1>
      </div>
      <div class="kota-hero-side-col">
        <p class="kota-hero-lead">Roasist; <strong>veri analitiği, performans pazarlaması, kurumsal SEO/AEO ve yüksek dönüşümlü web tasarımı</strong> tek bir stratejik merkezde buluşturan yeni nesil dijital büyüme ajansıdır.</p>
        <a href="/iletisim/" class="kota-submit-btn">Ekibimizle Tanışın →</a>
      </div>
    </div>
    {render_partner_badges_bar()}
  </div>
</section>

<section class="kota-section">
  <div class="container">
    <div class="kota-curved-panel">
      <span class="kota-step-num">VİZYONUMUZ & FELSEFEMİZ</span>
      <h2 style="font-size:clamp(2rem,4vw,3.5rem);font-weight:400;line-height:1.05;margin:0 0 1.5rem">Tahminlerle Değil, Gerçek Verilerle Büyüyoruz</h2>
      <p style="font-size:1.15rem;line-height:1.58;color:#271B3D;margin:0 0 1.25rem">Dijital pazarlamada başarının tesadüflere bırakılamayacağına inanıyoruz. Google, Meta, TikTok, LinkedIn ve Yandex ekosistemlerindeki resmi verileri, kendi geliştirdiğimiz analiz metodolojileriyle birleştirerek her reklam kuruşunun izini sürüyoruz.</p>
      <p style="font-size:1.15rem;line-height:1.58;color:#271B3D;margin:0">Tüm reklam ve analitik hesaplarınız %100 sizin mülkiyetinizde kalır; 7/24 şeffaf raporlama ve proaktif iletişimle markanızın kendi iç büyüme ekibi gibi çalışırız.</p>
      {render_service_tags_nav()}
    </div>
  </div>
</section>

<section class="kota-section">
  <div class="container">
    <div class="kota-section-header">
      <h2>Neden Roasist?</h2>
      <p>Markaların bizi uzun vadeli dijital büyüme ortağı olarak seçmesinin 6 temel nedeni.</p>
    </div>
    <div class="kota-cards-grid-3">
      {"".join(why_cards)}
    </div>
  </div>
</section>

<section class="kota-section">
  <div class="container">
    <div class="kota-section-header">
      <h2>6 Adımlı Büyüme Metodolojimiz</h2>
      <p>İlk denetimden ölçeklemeye kadar tüm projelerimizde uyguladığımız disiplinli süreç.</p>
    </div>
    <div class="kota-cards-grid-3">
      {"".join(proc_cards)}
    </div>
  </div>
</section>

<div class="kota-dark-zone">
  {render_clients_strip(15)}
</div>
"""
open(about_out, "w", encoding="utf-8").write(build_full_page(about_seo, about_main))
print("Built KOTA about page:", about_out)

# ==============================================================================
# D. Generate /iletisim/index.html (İletişim & Ücretsiz Strateji Görüşmesi Formu)
# ==============================================================================
contact_out = f"{DIST_DIR}/iletisim/index.html"
contact_seo = extract_head_seo(contact_out, "Roasist — İletişim & Ücretsiz Dijital Strateji Analizi", "Roasist ile iletişime geçin: ücretsiz dijital pazarlama, Google Ads, SEO ve web tasarım ön analizi.")

contact_main = f"""
<section class="kota-inner-hero">
  <div class="container">
    <nav class="kota-breadcrumb"><a href="/">Ana Sayfa</a> <span>/</span> <strong>İletişim</strong></nav>
    <div class="kota-hero-grid">
      <div class="kota-hero-title-col">
        <h1 class="kota-display-h1">
          <span>büyüme zamanı</span>
          <span class="indent-line">başlayalım.</span>
        </h1>
      </div>
      <div class="kota-hero-side-col">
        <p class="kota-hero-lead">Mevcut reklam hesaplarınızı, SEO görünürlüğünüzü ve web sitenizin dönüşüm potansiyelini <strong>ücretsiz ön analiz görüşmesinde</strong> birlikte inceleyelim.</p>
      </div>
    </div>
    {render_partner_badges_bar()}
  </div>
</section>

<section class="kota-section" id="analiz-formu" style="padding-top:1rem">
  <div class="container">
    <div class="kota-hero-grid" style="align-items:start">
      <div class="kota-hero-title-col" style="grid-column:span 12">
        <div class="kota-curved-panel">
          <div class="kota-hero-grid" style="align-items:start">
            <div style="grid-column:span 12;margin-bottom:2rem">
              <span class="kota-step-num">ÜCRETSİZ ÖN ANALİZ & TEKLİF FORMU</span>
              <h2 style="font-size:clamp(1.8rem,3.4vw,2.8rem);font-weight:400;margin:0 0 0.75rem">Projenizi Dinlemeye Hazırız</h2>
              <p style="color:#3B2D54;font-size:1.08rem;margin:0">Formu doldurduğunuzda uzman ekibimiz dijital varlıklarınızı inceleyerek aynı gün içinde sizinle iletişime geçer.</p>
            </div>
          </div>
          <form id="roasist-kota-contact-form" style="display:grid;grid-template-columns:repeat(12,1fr);gap:1.25rem">
            <div style="grid-column:span 12">
              <label style="display:block;font-weight:600;margin-bottom:0.45rem;font-size:0.92rem">Adınız Soyadınız *</label>
              <input class="kota-input" type="text" name="name" required placeholder="Örn: Ahmet Yılmaz"/>
            </div>
            <div style="grid-column:span 12">
              <label style="display:block;font-weight:600;margin-bottom:0.45rem;font-size:0.92rem">Telefon Numaranız *</label>
              <input class="kota-input" type="tel" name="phone" required placeholder="Örn: 05XX XXX XX XX"/>
            </div>
            <div style="grid-column:span 12">
              <label style="display:block;font-weight:600;margin-bottom:0.45rem;font-size:0.92rem">Web Siteniz veya Marka Adınız</label>
              <input class="kota-input" type="text" name="website" placeholder="Örn: www.markaniz.com"/>
            </div>
            <div style="grid-column:span 12">
              <label style="display:block;font-weight:600;margin-bottom:0.45rem;font-size:0.92rem">İlgilendiğiniz Hizmet *</label>
              <select class="kota-input" name="service">
                <option value="360° Dijital Pazarlama Yönetimi">360° Dijital Pazarlama Yönetimi</option>
                <option value="Performans Pazarlaması (Google, Meta, TikTok, Yandex)">Performans Pazarlaması (Google, Meta, TikTok, Yandex)</option>
                <option value="Kurumsal SEO & Yapay Zeka Aramaları (AEO)">Kurumsal SEO & Yapay Zeka Aramaları (AEO)</option>
                <option value="Web Tasarım & Dönüşüm Optimizasyonu (CRO)">Web Tasarım & Dönüşüm Optimizasyonu (CRO)</option>
                <option value="Grafik Tasarım & Reklam Kreatifi">Grafik Tasarım & Reklam Kreatifi</option>
              </select>
            </div>
            <div style="grid-column:span 12">
              <label style="display:block;font-weight:600;margin-bottom:0.45rem;font-size:0.92rem">Hedefleriniz veya Notunuz</label>
              <textarea class="kota-input" name="message" rows="4" placeholder="Aylık hedef bütçeniz, mevcut durumunuz veya beklentilerinizden kısaca bahsedebilirsiniz..."></textarea>
            </div>
            <div style="grid-column:span 12;display:flex;flex-wrap:wrap;gap:1rem;align-items:center;margin-top:0.5rem">
              <button type="submit" class="kota-submit-btn">Strateji Görüşmesi Planla (WhatsApp & E-Posta) →</button>
              <a href="mailto:info@roasist.com" class="ServicesPanel_tag__JYwRk" style="padding:0.95rem 1.5rem">info@roasist.com</a>
              <a href="tel:+905415075350" class="ServicesPanel_tag__JYwRk" style="padding:0.95rem 1.5rem">+90 541 507 53 50</a>
            </div>
          </form>
        </div>
      </div>
    </div>

    <div class="kota-cards-grid-3">
      <div class="kota-asym-card">
        <div>
          <span class="kota-step-num">01 — DOĞRUDAN HAT & WHATSAPP</span>
          <h3>+90 541 507 53 50</h3>
        </div>
        <p><a href="https://wa.me/+905415075350" target="_blank" rel="noopener noreferrer" style="color:#7602FF;font-weight:600;text-decoration:none">WhatsApp üzerinden hemen yazın →</a></p>
      </div>
      <div class="kota-asym-card">
        <div>
          <span class="kota-step-num">02 — KURUMSAL E-POSTA</span>
          <h3>info@roasist.com</h3>
        </div>
        <p><a href="mailto:info@roasist.com" style="color:#7602FF;font-weight:600;text-decoration:none">Proje brief'inizi e-posta ile gönderin →</a></p>
      </div>
      <div class="kota-asym-card">
        <div>
          <span class="kota-step-num">03 — MERKEZ OFİS</span>
          <h3>İstanbul, Türkiye</h3>
        </div>
        <p>Ulusal ve global markalar için 360° uzaktan ve yüz yüze büyüme yönetimi.</p>
      </div>
    </div>
  </div>
</section>
<script>
document.addEventListener("DOMContentLoaded", function() {{
  var f = document.getElementById("roasist-kota-contact-form");
  if (f) {{
    f.addEventListener("submit", function(e) {{
      e.preventDefault();
      var fd = new FormData(f);
      var msg = "Merhaba Roasist, web sitenizden strateji görüşmesi talep ediyorum.%0A%0A" +
        "*Ad Soyad:* " + encodeURIComponent(fd.get("name") || "") + "%0A" +
        "*Telefon:* " + encodeURIComponent(fd.get("phone") || "") + "%0A" +
        "*Web Sitesi/Marka:* " + encodeURIComponent(fd.get("website") || "") + "%0A" +
        "*Hizmet:* " + encodeURIComponent(fd.get("service") || "") + "%0A" +
        "*Not:* " + encodeURIComponent(fd.get("message") || "");
      window.open("https://wa.me/+905415075350?text=" + msg, "_blank", "noopener,noreferrer");
    }});
  }}
}});
</script>
"""
open(contact_out, "w", encoding="utf-8").write(build_full_page(contact_seo, contact_main))
print("Built KOTA contact page:", contact_out)

# ==============================================================================
# E. Generate /blog/index.html, 3 Blog Posts, Categories, Tags, and Privacy Policy
# ==============================================================================
blog_posts = [
    {
        "slug": "kurumsal-seo-ve-yapay-zeka-aramalari-aeo-rehberi",
        "permalink": "/blog/kurumsal-seo-ve-yapay-zeka-aramalari-aeo-rehberi/",
        "category": "SEO & AEO",
        "title": "Kurumsal SEO ve Yapay Zeka Aramaları (AEO & GEO) Rehberi",
        "excerpt": "Google Arama ile birlikte ChatGPT, Perplexity ve Gemini gibi yapay zeka yanıt motorlarında markanızın birincil kaynak olarak önerilmesini sağlayan teknik ve içeriksel mimari.",
        "image": "https://kota-content.b-cdn.net/app/uploads/2025/12/Design-with-guts.png",
        "body": [
            "Arama alışkanlıkları hızla dönüşüyor. Kullanıcılar artık yalnızca klasik mavi bağlantıları tıklamakla kalmıyor; doğrudan ChatGPT, Google AI Overviews, Perplexity ve Gemini üzerinden karşılaştırmalı yanıtlar arıyor.",
            "Roasist olarak kurumsal SEO stratejimizi yalnızca anahtar kelime sıralamaları üzerine değil, Varlık (Entity) Otoritesi, zenginleştirilmiş Schema.org yapısal verileri (Service, FAQPage, Organization) ve doğrudan yanıt mimarisi (AEO — Answer Engine Optimization) üzerine inşa ediyoruz.",
            "Sıfır SEO kaybı protokolümüz, Core Web Vitals hız optimizasyonumuz ve resmi Google arama hacmi verilerine dayanan içerik kümelerimizle markanızı hem geleneksel aramada hem de yapay zeka motorlarında sektör lideri konumuna taşıyoruz."
        ]
    },
    {
        "slug": "performans-pazarlamasinda-roas-optimizasyonu",
        "permalink": "/blog/performans-pazarlamasinda-roas-optimizasyonu/",
        "category": "Performans & ROAS",
        "title": "Performans Pazarlamasında ROAS Optimizasyonu: Bütçenizi Ciroya Dönüştürün",
        "excerpt": "Google Ads, Meta CAPI, TikTok ve Yandex kampanyalarında tıklama maliyetine değil, gerçek ciroya ve nitelikli müşteri edinme maliyetine (CPA) odaklanan büyüme stratejileri.",
        "image": "https://kota-content.b-cdn.net/app/uploads/2025/11/brand-trend-2026.png",
        "body": [
            "Performans pazarlamasında en sık yapılan hata, kampanyaları yalnızca tıklama başı maliyet (CPC) veya gösterim metrikleriyle değerlendirmektir. Gerçek büyüme, reklam harcamasının ürettiği net ciro (ROAS) ve karlı müşteri edinme maliyeti (CPA) ile ölçülür.",
            "Sunucu taraflı dönüşüm takibi (Server-Side GTM, Meta Conversions API, Enhanced Conversions) sayesinde algoritmalara en temiz dönüşüm sinyallerini iletiyor, bütçe kaçaklarını negatif kelime ve kitle hariç tutma protokolleriyle ilk günden kesiyoruz.",
            "Kreatif varyasyon testleri ve açılış sayfası dönüşüm optimizasyonu (CRO) ile aynı reklam bütçesinden çok daha yüksek satış hacmi üretiyoruz."
        ]
    },
    {
        "slug": "360-dijital-pazarlama-kanallar-arasi-sinerji",
        "permalink": "/blog/360-dijital-pazarlama-kanallar-arasi-sinerji/",
        "category": "Dijital Strateji",
        "title": "360° Dijital Pazarlama: Kanallar Arası Sinerji Nasıl Kurulur?",
        "excerpt": "SEO, Google Ads, sosyal medya reklamları ve web tasarım süreçleri birbirinden kopuk yönetildiğinde oluşan bütçe kaybını 360° entegre büyüme mimarisiyle nasıl önlüyoruz?",
        "image": "https://kota-content.b-cdn.net/app/uploads/2025/11/Lovie-awards.png",
        "body": [
            "Birçok markada SEO ajansı, reklam ajansı ve web yazılım ekibi birbirinden bağımsız çalışır. Bu kopukluk, reklamla gelen yüksek niyetli kullanıcının yavaş veya dönüşüm kurgusu zayıf bir sayfada kaybedilmesine yol açar.",
            "Roasist'in 360° Dijital Pazarlama Yönetimi modelinde; arama terimi verileri SEO içerik stratejisini besler, yüksek dönüşümlü organik sayfalar yeniden pazarlama (remarketing) kitlelerini büyütür ve kreatif stüdyomuz her kanalın algoritmasına özel görsel/video varlıklar üretir.",
            "Tüm kanalların tek bir ortak KPI ve şeffaf veri paneli etrafında birleşmesi, büyüme hızınızı katlayan gerçek çarpan etkisini yaratır."
        ]
    }
]

def render_blog_cards_grid():
    cards = []
    for bp in blog_posts:
        cards.append(f"""
        <a href="{bp["permalink"]}" style="text-decoration:none;color:inherit">
          <article class="Articles_article__3ZS4Y">
            <figure class="Articles_image__Cvgsi" style="margin:0">
              <span class="Image_image__RAAdZ Image_fill__EiIzS">
                <img src="{bp["image"]}" alt="{bp["title"]}" loading="lazy"/>
              </span>
            </figure>
            <div class="Articles_text__HhO2L">
              <p class="Articles_filterNames__mCWt8">{bp["category"]}</p>
              <h3 class="Articles_title__h86PB">{bp["title"]}</h3>
            </div>
          </article>
        </a>
        """)
    return f'<div class="Articles_articlesList__CXW8a">{"".join(cards)}</div>'

# Build /blog/index.html and all category/tag hub pages
blog_hub_Paths = [
    f"{DIST_DIR}/blog/index.html",
    f"{DIST_DIR}/kategori/dijital-strateji/index.html",
    f"{DIST_DIR}/kategori/performans-pazarlamasi/index.html",
    f"{DIST_DIR}/kategori/seo/index.html",
] + glob.glob(f"{DIST_DIR}/etiket/*/index.html")

for bpath in blog_hub_Paths:
    os.makedirs(os.path.dirname(bpath), exist_ok=True)
    b_seo = extract_head_seo(bpath, "Roasist Blog — Dijital Pazarlama, SEO, AEO & Performans İçgörüleri", "Performans pazarlaması, Google Ads, Meta reklamları, kurumsal SEO ve AEO rehberleri.")
    b_main = f"""
    <section class="kota-inner-hero" style="min-height:60svh">
      <div class="container">
        <nav class="kota-breadcrumb"><a href="/">Ana Sayfa</a> <span>/</span> <strong>İçgörüler & Blog</strong></nav>
        <div class="kota-hero-grid">
          <div class="kota-hero-title-col">
            <h1 class="kota-display-h1"><span>güncel yazılar</span><span class="indent-line">& içgörüler.</span></h1>
          </div>
          <div class="kota-hero-side-col">
            <p class="kota-hero-lead">Performans pazarlaması, ROAS optimizasyonu, kurumsal SEO, yapay zeka aramaları (AEO) ve dönüşüm odaklı web tasarım üzerine stratejik rehberler.</p>
          </div>
        </div>
        {render_partner_badges_bar()}
      </div>
    </section>
    <div class="kota-dark-zone" style="padding-top:5rem;padding-bottom:6rem">
      <div class="container">
        {render_blog_cards_grid()}
      </div>
    </div>
    """
    open(bpath, "w", encoding="utf-8").write(build_full_page(b_seo, b_main))

# Build the 3 individual blog post pages
for bp in blog_posts:
    p_file = f"{DIST_DIR}/blog/{bp['slug']}/index.html"
    os.makedirs(os.path.dirname(p_file), exist_ok=True)
    p_seo = extract_head_seo(p_file, f"{bp['title']} | Roasist Blog", bp["excerpt"])
    paras = "".join(f'<p style="font-size:1.18rem;line-height:1.65;color:#231738;margin:0 0 1.5rem">{p}</p>' for p in bp["body"])
    p_main = f"""
    <section class="kota-inner-hero" style="min-height:60svh">
      <div class="container">
        <nav class="kota-breadcrumb"><a href="/">Ana Sayfa</a> <span>/</span> <a href="/blog/">Blog</a> <span>/</span> <strong>{bp["category"]}</strong></nav>
        <div class="kota-hero-grid">
          <div class="kota-hero-title-col" style="grid-column:span 12">
            <h1 class="kota-display-h1" style="font-size:clamp(2.4rem,5vw,4.6rem)">{bp["title"]}</h1>
          </div>
        </div>
        {render_partner_badges_bar()}
      </div>
    </section>
    <section class="kota-section" style="padding-top:1rem">
      <div class="container">
        <div class="kota-curved-panel">
          <span class="kota-step-num">{bp["category"]}</span>
          <p style="font-size:1.35rem;font-weight:500;line-height:1.45;color:#0F0A1C;margin:0 0 2rem">{bp["excerpt"]}</p>
          {paras}
          {render_service_tags_nav()}
        </div>
      </div>
    </section>
    <div class="kota-dark-zone" style="padding-top:5rem;padding-bottom:5rem">
      <div class="container">
        <h2 style="color:#fff;font-size:clamp(2rem,4vw,3.5rem);font-weight:400;margin:0 0 2.5rem">Diğer Güncel Yazılar</h2>
        {render_blog_cards_grid()}
      </div>
    </div>
    """
    open(p_file, "w", encoding="utf-8").write(build_full_page(p_seo, p_main))
    print("Built KOTA blog post:", p_file)

# Build /gizlilik-politikasi-ve-kullanim-sartlari/index.html
priv_file = f"{DIST_DIR}/gizlilik-politikasi-ve-kullanim-sartlari/index.html"
priv_seo = extract_head_seo(priv_file, "Roasist — Gizlilik Politikası ve Kullanım Şartları", "Roasist gizlilik politikası, KVKK aydınlatma metni ve web sitesi kullanım şartları.")
priv_main = f"""
<section class="kota-inner-hero" style="min-height:50svh">
  <div class="container">
    <nav class="kota-breadcrumb"><a href="/">Ana Sayfa</a> <span>/</span> <strong>Gizlilik Politikası</strong></nav>
    <h1 class="kota-display-h1" style="font-size:clamp(2.4rem,5vw,4.5rem)">Gizlilik Politikası & Kullanım Şartları</h1>
  </div>
</section>
<section class="kota-section" style="padding-top:1rem">
  <div class="container">
    <div class="kota-curved-panel">
      <h2 style="font-size:1.8rem;font-weight:500;margin:0 0 1rem">1. Veri Güvenliği ve KVKK Aydınlatma İlkemiz</h2>
      <p style="font-size:1.1rem;line-height:1.6;color:#271B3D;margin:0 0 1.5rem">Roasist Dijital Pazarlama ve Büyüme Ajansı ("Roasist") olarak, ziyaretçilerimizin ve iş ortaklarımızın kişisel verilerinin güvenliğine 6698 sayılı Kişisel Verilerin Korunması Kanunu (KVKK) kapsamında en üst düzeyde özen gösteriyoruz. İletişim formlarımız üzerinden paylaştığınız bilgiler yalnızca talep ettiğiniz dijital analiz ve teklif süreçlerinin yürütülmesi amacıyla kullanılır ve üçüncü taraflarla paylaşılmaz.</p>
      <h2 style="font-size:1.8rem;font-weight:500;margin:0 0 1rem">2. Çerezler (Cookies) ve Analitik</h2>
      <p style="font-size:1.1rem;line-height:1.6;color:#271B3D;margin:0 0 1.5rem">Web sitemizde kullanıcı deneyimini iyileştirmek ve site performansını ölçümlemek amacıyla anonim analitik çerezleri kullanılmaktadır. Tarayıcı ayarlarınızdan çerez tercihlerinizi dilediğiniz zaman yönetebilirsiniz.</p>
      <h2 style="font-size:1.8rem;font-weight:500;margin:0 0 1rem">3. İletişim</h2>
      <p style="font-size:1.1rem;line-height:1.6;color:#271B3D;margin:0">Gizlilik politikamız ve veri güvenliği uygulamalarımız hakkındaki tüm sorularınız için <a href="mailto:info@roasist.com" style="color:#7602FF;font-weight:600">info@roasist.com</a> adresinden bize ulaşabilirsiniz.</p>
    </div>
  </div>
</section>
"""
open(priv_file, "w", encoding="utf-8").write(build_full_page(priv_seo, priv_main))
print("Successfully built all KOTA inner pages!")
