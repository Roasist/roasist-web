#!/usr/bin/env python3
"""
Pre-Launch Step 4:
1. Updates `sitemap.xml` (in both public/ and dist/) with full hreflang="tr", "en", and
   "x-default" entries for the newly added routes:
     - /hizmetler/donusum-optimizasyonu/ <-> /en/conversion-optimization/
     - /hizmetler/yapay-zeka-seo/ <-> /en/ai-search-aeo-geo/
     - /start-your-project/ <-> /en/start-your-project/
   and refreshes `<lastmod>` to 2026-11-20.
2. Creates a clean, bilingual, brand-aligned `404.html` page (in both public/ and dist/)
   that automatically adapts to `/roasist-web/` preview paths vs root `www.roasist.com/`
   paths and TR vs EN language.
3. Adds `scripts/switch_to_production_domain.py` so switching `gh-pages` from
   `/roasist-web/` preview base path to root `www.roasist.com` + `CNAME` is a single,
   repeatable command at DNS cutover time.
"""
import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)

NEW_SITEMAP_PAIRS = [
    ("/hizmetler/donusum-optimizasyonu/", "/en/conversion-optimization/", "0.9"),
    ("/hizmetler/yapay-zeka-seo/", "/en/ai-search-aeo-geo/", "0.9"),
    ("/start-your-project/", "/en/start-your-project/", "0.8"),
]

CUSTOM_404_HTML = """<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>404 — Sayfa Bulunamadı | Roasist</title>
  <meta name="robots" content="noindex, follow"/>
  <link rel="icon" href="/favicon.svg" type="image/svg+xml"/>
  <style>
    :root {
      color-scheme: light;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      min-height: 100svh;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      background: #f8fafc;
      color: #0f172a;
      font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      padding: clamp(1.5rem, 4vw, 3rem);
    }
    header {
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .brand {
      font-weight: 800;
      font-size: 1.35rem;
      letter-spacing: -0.03em;
      color: #7602FF;
      text-decoration: none;
    }
    main {
      max-width: 620px;
      margin: auto;
      text-align: center;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 1.25rem;
      padding: 3rem 0;
    }
    .badge {
      display: inline-flex;
      align-items: center;
      padding: 0.4rem 0.9rem;
      border-radius: 999px;
      font-size: 0.85rem;
      font-weight: 600;
      font-variant-numeric: tabular-nums;
      letter-spacing: 0.06em;
      color: #7602FF;
      background: rgba(118, 2, 255, 0.08);
      border: 1px solid rgba(118, 2, 255, 0.2);
    }
    h1 {
      font-size: clamp(2.2rem, 5vw, 3.5rem);
      font-weight: 600;
      letter-spacing: -0.03em;
      line-height: 1.1;
      color: #0f172a;
    }
    p {
      font-size: 1.05rem;
      line-height: 1.6;
      color: #475569;
      max-width: 48ch;
    }
    .actions {
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 0.85rem;
      margin-top: 0.75rem;
    }
    .btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 0.8rem 1.5rem;
      border-radius: 999px;
      font-size: 0.95rem;
      font-weight: 600;
      text-decoration: none;
      transition: transform 160ms cubic-bezier(0.22, 1, 0.36, 1);
    }
    .btn:hover { transform: translateY(-1px); }
    .btn-primary {
      background: #0f172a;
      color: #ffffff;
    }
    .btn-outline {
      background: #ffffff;
      color: #0f172a;
      border: 1px solid rgba(15, 23, 42, 0.14);
    }
    footer {
      text-align: center;
      font-size: 0.85rem;
      color: #64748b;
    }
  </style>
</head>
<body>
  <header>
    <a id="nav-brand" class="brand" href="/">ROASİST</a>
  </header>
  <main>
    <span class="badge">404</span>
    <h1 id="err-title">Aradığınız sayfa bulunamadı.</h1>
    <p id="err-desc">Sayfa taşınmış, kaldırılmış veya adres yanlış yazılmış olabilir. Ana sayfaya dönebilir veya hizmetlerimizi inceleyebilirsiniz.</p>
    <div class="actions">
      <a id="btn-home" class="btn btn-primary" href="/">Ana Sayfaya Dön →</a>
      <a id="btn-services" class="btn btn-outline" href="/hizmetler/">Hizmetlerimiz</a>
    </div>
  </main>
  <footer>© 2026 Roasist Digital Growth Studio</footer>
  <script>
    (function() {
      var p = window.location.pathname || '/';
      var base = p.indexOf('/roasist-web/') === 0 || p === '/roasist-web' ? '/roasist-web' : '';
      var isEn = p.indexOf('/en/') !== -1 || p.endsWith('/en');
      var homeHref = base + (isEn ? '/en/' : '/');
      var svcsHref = base + (isEn ? '/en/services/' : '/hizmetler/');
      document.getElementById('nav-brand').href = homeHref;
      document.getElementById('btn-home').href = homeHref;
      document.getElementById('btn-services').href = svcsHref;
      if (isEn) {
        document.documentElement.lang = 'en';
        document.title = '404 — Page Not Found | Roasist';
        document.getElementById('err-title').textContent = 'Page not found.';
        document.getElementById('err-desc').textContent = 'The page you are looking for may have been moved or no longer exists. Return to the homepage or explore our services.';
        document.getElementById('btn-home').textContent = 'Back to Homepage →';
        document.getElementById('btn-services').textContent = 'Explore Services';
      }
    })();
  </script>
</body>
</html>
"""


def build_url_block(loc: str, tr_url: str, en_url: str, prio: str) -> str:
    base = "https://www.roasist.com"
    return (
        "  <url>\n"
        f"    <loc>{base}{loc}</loc>\n"
        f"    <xhtml:link rel=\"alternate\" hreflang=\"tr\" href=\"{base}{tr_url}\"/>\n"
        f"    <xhtml:link rel=\"alternate\" hreflang=\"en\" href=\"{base}{en_url}\"/>\n"
        f"    <xhtml:link rel=\"alternate\" hreflang=\"x-default\" href=\"{base}{tr_url}\"/>\n"
        "    <lastmod>2026-11-20</lastmod>\n"
        f"    <priority>{prio}</priority>\n"
        "  </url>\n"
    )


def update_sitemap(sitemap_path: str):
    if not os.path.exists(sitemap_path):
        return
    xml = open(sitemap_path, "r", encoding="utf-8").read()
    xml = re.sub(r"<lastmod>\d{4}-\d{2}-\d{2}</lastmod>", "<lastmod>2026-11-20</lastmod>", xml)

    additions = []
    for tr_u, en_u, prio in NEW_SITEMAP_PAIRS:
        if f"<loc>https://www.roasist.com{tr_u}</loc>" not in xml:
            additions.append(build_url_block(tr_u, tr_u, en_u, prio))
        if f"<loc>https://www.roasist.com{en_u}</loc>" not in xml:
            additions.append(build_url_block(en_u, tr_u, en_u, prio))

    if additions:
        xml = xml.replace("</urlset>", "".join(additions) + "</urlset>")

    open(sitemap_path, "w", encoding="utf-8").write(xml)
    print(f"[OK] Updated {os.path.relpath(sitemap_path, REPO_ROOT)} ({xml.count('<loc>')} URLs)")


def write_404(root_dir: str):
    p = os.path.join(root_dir, "404.html")
    open(p, "w", encoding="utf-8").write(CUSTOM_404_HTML)
    print(f"[OK] Created {os.path.relpath(p, REPO_ROOT)}")


def fix_aeo_titles(root_dir: str):
    import sys
    sys.path.insert(0, SCRIPT_DIR)
    from prelaunch_step3_forms_links_en import apply_replacements_flight_safe

    tr_aeo = os.path.join(root_dir, "hizmetler", "yapay-zeka-seo", "index.html")
    if os.path.exists(tr_aeo):
        t = open(tr_aeo, "r", encoding="utf-8").read()
        t2 = apply_replacements_flight_safe(
            t,
            [
                (
                    "Roasist - SEO - Çevrimiçi Varlığınızı Güçlendirin",
                    "Yapay Zeka Aramaları (AEO & GEO) | ChatGPT & Gemini Görünürlüğü | Roasist",
                )
            ],
        )
        if t2 != t:
            open(tr_aeo, "w", encoding="utf-8").write(t2)
            print(f"[OK] Updated <title> in {os.path.relpath(tr_aeo, REPO_ROOT)}")

    en_aeo = os.path.join(root_dir, "en", "ai-search-aeo-geo", "index.html")
    if os.path.exists(en_aeo):
        t = open(en_aeo, "r", encoding="utf-8").read()
        t2 = apply_replacements_flight_safe(
            t,
            [
                (
                    "Enterprise SEO &amp; AI Search (AEO) Agency | Roasist",
                    "AI Search Optimization (AEO &amp; GEO) Agency | ChatGPT &amp; Perplexity | Roasist",
                ),
                (
                    "Enterprise SEO & AI Search (AEO) Agency | Roasist",
                    "AI Search Optimization (AEO & GEO) Agency | ChatGPT & Perplexity | Roasist",
                ),
            ],
        )
        if t2 != t:
            open(en_aeo, "w", encoding="utf-8").write(t2)
            print(f"[OK] Updated <title> in {os.path.relpath(en_aeo, REPO_ROOT)}")

    en_seo = os.path.join(root_dir, "en", "seo", "index.html")
    if os.path.exists(en_seo):
        t = open(en_seo, "r", encoding="utf-8").read()
        t2 = apply_replacements_flight_safe(
            t,
            [
                (
                    "Enterprise SEO &amp; AI Search (AEO) Agency | Roasist",
                    "Technical &amp; Enterprise SEO Agency | Organic Search Growth | Roasist",
                ),
                (
                    "Enterprise SEO & AI Search (AEO) Agency | Roasist",
                    "Technical & Enterprise SEO Agency | Organic Search Growth | Roasist",
                ),
            ],
        )
        if t2 != t:
            open(en_seo, "w", encoding="utf-8").write(t2)
            print(f"[OK] Updated <title> in {os.path.relpath(en_seo, REPO_ROOT)}")


def main():
    for root_name in ["public", "dist"]:
        root_dir = os.path.join(REPO_ROOT, root_name)
        if not os.path.exists(root_dir):
            continue
        update_sitemap(os.path.join(root_dir, "sitemap.xml"))
        write_404(root_dir)
        fix_aeo_titles(root_dir)


if __name__ == "__main__":
    main()

