#!/usr/bin/env python3
"""
Prunes blog posts down to a single flagship article (TR + EN counterpart) while keeping
the entire blog infrastructure ready for future articles:
  - Kept TR Post: /blog/Performans-Pazarlamasi-Nedir/
  - Kept EN Post: /en/blog/what-is-performance-marketing/
  1. Removes the 5 extra TR blog post directories, 2 extra EN blog post directories,
     and unused /blog/etiket/* & /blog/kategori/* archive directories.
  2. Removes self-referential/dead RelatedPosts section from the single active blog detail
     pages (/blog/Performans-Pazarlamasi-Nedir/ & /en/blog/what-is-performance-marketing/)
     in both SSR HTML and Flight stream.
  3. Updates /blog/index.html, /blog/kategori/performans-pazarlamasi/index.html, and
     /en/blog/index.html Flight stream (posts + categories) to contain only the 1 active post.
  4. Updates Homepage Articles section (public/kota-roasist-local.html & public/en/index.html)
     in SSR HTML and Flight stream to show only the 1 active post.
  5. Updates RelatedPosts section across all TR & EN service pages (SSR + Flight) to show
     only the 1 active post (leaving /referanslar/* & /en/references/* case-study cards untouched).
  6. Updates mapKotaHref runtime router across all HTML pages and cleans public/sitemap.xml.
  7. Adds responsive :only-of-type editorial layout rules (which automatically step aside as
     soon as a 2nd post is added later), patches /en/blog/ card hrefs in blog/page.js, and
     cache-busts CSS/JS bundles.
"""
import glob
import json
import os
import re
import shutil
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
PUBLIC_DIR = os.path.join(REPO_ROOT, "public")
sys.path.insert(0, SCRIPT_DIR)

from apply_phase1_cleanup import PUSH_RE, find_node_by_class, rewrite_flight_in_html

KEEP_TR_SLUG = "Performans-Pazarlamasi-Nedir"
KEEP_EN_SLUG = "what-is-performance-marketing"

REMOVED_TR_SLUGS = [
    "performans-pazarlamasinda-roas-optimizasyonu",
    "kurumsal-seo-ve-yapay-zeka-aramalari-aeo-rehberi",
    "360-dijital-pazarlama-kanallar-arasi-sinerji",
    "Veriye-Dayali-Dijital-Pazarlama-Stratejisi-Nedir",
    "Reklam-Harcamalarinin-Geri-Donusu-ROAS-Nasil-Hesaplanir",
]
REMOVED_EN_SLUGS = [
    "how-to-calculate-and-optimize-roas",
    "enterprise-seo-and-ai-search-aeo-guide",
]

SINGLE_BLOG_CSS = """
/* === SINGLE BLOG POST EDITORIAL LAYOUT (:only-of-type — auto-reverts when 2+ posts exist) === */
.Blog_postsWithFilters__aXNNs:has(.PostsList_postsList__U9F5T > a:only-of-type) {
  display: none !important;
}
.FeaturedBlogPost_featuredPost__aRcs9 {
  padding-bottom: 4.5rem;
}
@media (min-width: 769px) {
  .Articles_articlesList__CXW8a:has(> a:only-of-type) {
    grid-template-columns: minmax(0, 1fr) !important;
  }
  .Articles_articlesList__CXW8a > a:only-of-type .Articles_article__3ZS4Y {
    display: grid !important;
    grid-template-columns: 1.15fr 1fr !important;
    align-items: stretch !important;
  }
  .Articles_articlesList__CXW8a > a:only-of-type .Articles_article__3ZS4Y .Articles_image__Cvgsi {
    aspect-ratio: 16 / 10 !important;
    min-height: 21rem !important;
    height: 100% !important;
  }
  .Articles_articlesList__CXW8a > a:only-of-type .Articles_article__3ZS4Y img {
    border-top-right-radius: 0 !important;
  }
  .Articles_articlesList__CXW8a > a:only-of-type .Articles_article__3ZS4Y .Articles_text__HhO2L {
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
    align-items: flex-start !important;
    padding: 2.5rem 3rem !important;
  }
  .Articles_articlesList__CXW8a > a:only-of-type .Articles_title__h86PB {
    font-size: clamp(1.5rem, 2.2vw, 2.125rem) !important;
    line-height: 1.25 !important;
  }
  .RelatedPosts_relatedPosts__xfLkb .AnimatedGrid_grid__otAMD .container > a.BlogPostCard_post__fNGbL:only-of-type {
    grid-column: 1 / span 7 !important;
  }
}
"""


def step1_remove_extra_blog_directories():
    removed = []
    for base_name in ("public", "dist"):
        base_dir = os.path.join(REPO_ROOT, base_name)
        if not os.path.isdir(base_dir):
            continue
        for sl in REMOVED_TR_SLUGS:
            p = os.path.join(base_dir, "blog", sl)
            if os.path.isdir(p):
                shutil.rmtree(p)
                removed.append(os.path.relpath(p, REPO_ROOT))
        for sl in REMOVED_EN_SLUGS:
            p = os.path.join(base_dir, "en", "blog", sl)
            if os.path.isdir(p):
                shutil.rmtree(p)
                removed.append(os.path.relpath(p, REPO_ROOT))
        # Remove /blog/etiket/ completely and unused /blog/kategori/*
        etiket_dir = os.path.join(base_dir, "blog", "etiket")
        if os.path.isdir(etiket_dir):
            shutil.rmtree(etiket_dir)
            removed.append(os.path.relpath(etiket_dir, REPO_ROOT))
        kat_dir = os.path.join(base_dir, "blog", "kategori")
        if os.path.isdir(kat_dir):
            for entry in sorted(os.listdir(kat_dir)):
                if entry != "performans-pazarlamasi":
                    kp = os.path.join(kat_dir, entry)
                    if os.path.isdir(kp):
                        shutil.rmtree(kp)
                        removed.append(os.path.relpath(kp, REPO_ROOT))
    print(f"[1/7] Removed {len(removed)} obsolete blog post & archive directories")


def step2_clean_active_blog_detail_pages():
    targets = [
        os.path.join(PUBLIC_DIR, "blog", KEEP_TR_SLUG, "index.html"),
        os.path.join(PUBLIC_DIR, "en", "blog", KEEP_EN_SLUG, "index.html"),
    ]
    for fp in targets:
        if not os.path.exists(fp):
            continue
        html = open(fp, "r", encoding="utf-8").read()
        pushes = list(PUSH_RE.finditer(html))
        ssr = html[: pushes[0].start()]
        tail = html[pushes[0].start() :]

        ssr = re.sub(
            r'<section class="RelatedPosts_relatedPosts__xfLkb">.*?</section>',
            "",
            ssr,
            count=1,
            flags=re.S,
        )

        def detail_mutator(records):
            changed = False
            for rec in records:
                if rec[0] == "line" and rec[1] == "f" and "RelatedPosts_relatedPosts__xfLkb" in rec[2]:
                    ast = json.loads(rec[2])
                    art_ch = ast[2][3]["children"]
                    ast[2][3]["children"] = [
                        ch
                        for ch in art_ch
                        if not (
                            isinstance(ch, list)
                            and len(ch) >= 4
                            and isinstance(ch[3], dict)
                            and ch[3].get("className") == "RelatedPosts_relatedPosts__xfLkb"
                        )
                    ]
                    rec[2] = json.dumps(ast, ensure_ascii=False, separators=(",", ":"))
                    changed = True
            return changed

        new_tail = rewrite_flight_in_html(tail, detail_mutator)
        open(fp, "w", encoding="utf-8").write(ssr + new_tail)
        print(f"[2/7] Cleaned RelatedPosts from single active post: {os.path.relpath(fp, REPO_ROOT)}")


def step3_update_blog_index_pages():
    targets = [
        (os.path.join(PUBLIC_DIR, "blog", "index.html"), KEEP_TR_SLUG, "performans-pazarlamasi"),
        (os.path.join(PUBLIC_DIR, "blog", "kategori", "performans-pazarlamasi", "index.html"), KEEP_TR_SLUG, "performans-pazarlamasi"),
        (os.path.join(PUBLIC_DIR, "en", "blog", "index.html"), KEEP_EN_SLUG, "performance-marketing"),
    ]
    for fp, keep_slug, keep_cat in targets:
        if not os.path.exists(fp):
            continue
        html = open(fp, "r", encoding="utf-8").read()
        pushes = list(PUSH_RE.finditer(html))
        ssr = html[: pushes[0].start()]
        tail = html[pushes[0].start() :]

        def idx_mutator(records):
            changed = False
            for rec in records:
                if rec[0] == "line" and rec[1] == "d":
                    ast = json.loads(rec[2])
                    pwf = ast[2][3]["children"][2]
                    inner_pair = pwf[3]["children"][3]["children"][3]["children"][3]["children"]
                    cats = inner_pair[0][3]["children"][3]["categories"]
                    kept_cats = [c for c in cats if c.get("node", {}).get("slug") == keep_cat]
                    for c in kept_cats:
                        c["node"]["count"] = 1
                    inner_pair[0][3]["children"][3]["categories"] = kept_cats

                    posts = inner_pair[1][3]["posts"]
                    inner_pair[1][3]["posts"] = [
                        p for p in posts if p.get("node", {}).get("slug") == keep_slug
                    ]
                    rec[2] = json.dumps(ast, ensure_ascii=False, separators=(",", ":"))
                    changed = True
            return changed

        new_tail = rewrite_flight_in_html(tail, idx_mutator)
        open(fp, "w", encoding="utf-8").write(ssr + new_tail)
        print(f"[3/7] Updated blog index Flight posts/categories (1 post): {os.path.relpath(fp, REPO_ROOT)}")


def step4_update_homepage_articles():
    targets = [
        (os.path.join(PUBLIC_DIR, "kota-roasist-local.html"), KEEP_TR_SLUG),
        (os.path.join(PUBLIC_DIR, "en", "index.html"), KEEP_EN_SLUG),
    ]
    for fp, keep_slug in targets:
        html = open(fp, "r", encoding="utf-8").read()
        pushes = list(PUSH_RE.finditer(html))
        ssr = html[: pushes[0].start()]
        tail = html[pushes[0].start() :]

        def repl_ssr_articles(m):
            inner = m.group(2)
            cards = re.findall(r'<a\b[^>]*data-animation="grid-item"[^>]*>.*?</article></a>', inner, re.S)
            kept = [c for c in cards if keep_slug in c] or cards[:1]
            # Promote data-src -> src for reliable immediate rendering
            kept = [
                re.sub(
                    r'<img\s+data-srcset="([^"]*)"\s+data-src="([^"]+)"([^>]*)\s+class="lazyload"\s*/>',
                    r'<img srcSet="\1" src="\2"\3 loading="lazy" decoding="async"/>',
                    c,
                )
                for c in kept
            ]
            return m.group(1) + "".join(kept) + m.group(3)

        ssr, n = re.subn(
            r'(<div class="Articles_articlesList__CXW8a">)(.*?)(<div class="Articles_mobileButton__Df7CF">)',
            repl_ssr_articles,
            ssr,
            count=1,
            flags=re.S,
        )
        if n != 1:
            raise RuntimeError(f"Could not update SSR Articles_articlesList in {fp}")

        def home_mutator(records):
            changed = False
            for rec in records:
                if rec[0] == "line" and "Articles_articlesList__CXW8a" in rec[2]:
                    ast = json.loads(rec[2])
                    alist = find_node_by_class(ast, "Articles_articlesList__CXW8a")
                    cards_list = alist[3]["children"][0]
                    kept_ast = [
                        c
                        for c in cards_list
                        if isinstance(c, list)
                        and len(c) >= 4
                        and isinstance(c[3], dict)
                        and keep_slug in str(c[3].get("href", ""))
                    ] or cards_list[:1]
                    for c in kept_ast:
                        try:
                            c[3]["children"][3]["children"][0][3]["children"][3]["lazy"] = False
                        except Exception:
                            pass
                    alist[3]["children"][0] = kept_ast
                    rec[2] = json.dumps(ast, ensure_ascii=False, separators=(",", ":"))
                    changed = True
            return changed

        new_tail = rewrite_flight_in_html(tail, home_mutator)
        open(fp, "w", encoding="utf-8").write(ssr + new_tail)
        print(f"[4/7] Updated Homepage Articles to 1 post: {os.path.relpath(fp, REPO_ROOT)}")


def step5_update_service_related_posts():
    updated = 0
    for fp in sorted(glob.glob(os.path.join(PUBLIC_DIR, "**", "*.html"), recursive=True)):
        rel = os.path.relpath(fp, PUBLIC_DIR)
        if rel.startswith("referanslar/") or rel.startswith("en/references/"):
            continue
        if rel.startswith("blog/") or rel.startswith("en/blog/"):
            continue
        html = open(fp, "r", encoding="utf-8").read()
        if "RelatedPosts_relatedPosts__xfLkb" not in html:
            continue

        is_en = rel.startswith("en/")
        keep_slug = KEEP_EN_SLUG if is_en else KEEP_TR_SLUG

        pushes = list(PUSH_RE.finditer(html))
        ssr = html[: pushes[0].start()]
        tail = html[pushes[0].start() :]

        sec_match = re.search(r'<section class="RelatedPosts_relatedPosts__xfLkb">.*?</section>', ssr, re.S)
        if not sec_match or ("/blog/" not in sec_match.group(0)):
            continue

        def repl_rp_ssr(m):
            sec = m.group(0)
            cards = re.findall(r'<a\b[^>]*class="BlogPostCard_post__fNGbL[^"]*"[^>]*>.*?</a>', sec, re.S)
            kept = [c for c in cards if keep_slug in c] or cards[:1]
            return re.sub(
                r'(<div class="AnimatedGrid_grid__otAMD"><div class="container">).*?(</div></div><div class="container"><div class="RelatedPosts_viewAllLinkMobile__joii8">)',
                lambda gm: gm.group(1) + "".join(kept) + gm.group(2),
                sec,
                count=1,
                flags=re.S,
            )

        ssr = re.sub(
            r'<section class="RelatedPosts_relatedPosts__xfLkb">.*?</section>',
            repl_rp_ssr,
            ssr,
            count=1,
            flags=re.S,
        )

        def rp_mutator(records):
            changed = False
            for rec in records:
                if rec[0] == "line" and "RelatedPosts_relatedPosts__xfLkb" in rec[2]:
                    ast = json.loads(rec[2])
                    rp = find_node_by_class(ast, "RelatedPosts_relatedPosts__xfLkb")
                    if not rp:
                        continue
                    grid_c = rp[3]["children"][2][3]["children"]
                    cards_ast = grid_c[3]["children"]
                    kept_ast = [
                        c
                        for c in cards_ast
                        if isinstance(c, list)
                        and len(c) >= 4
                        and isinstance(c[3], dict)
                        and keep_slug in str(c[3].get("href", ""))
                    ] or cards_ast[:1]
                    grid_c[3]["children"] = kept_ast
                    rec[2] = json.dumps(ast, ensure_ascii=False, separators=(",", ":"))
                    changed = True
            return changed

        new_tail = rewrite_flight_in_html(tail, rp_mutator)
        open(fp, "w", encoding="utf-8").write(ssr + new_tail)
        updated += 1
    print(f"[5/7] Updated RelatedPosts to 1 post across {updated} TR & EN service pages")


def step6_update_runtime_router_and_sitemap():
    router_re = re.compile(
        r"else if \(h === '/blog/Performans-Pazarlamasi-Nedir'.*?else if \(h\.startsWith\('/blog/'\) && !h\.endsWith\('/'\)\) h = h \+ '/';",
        re.S,
    )
    new_router_rules = (
        "else if (h === '/blog/Performans-Pazarlamasi-Nedir' || h.indexOf('inspire-your-next-design') !== -1) h = '/blog/Performans-Pazarlamasi-Nedir/';\n"
        "    else if (h.startsWith('/blog/') && h !== '/blog/' && !h.startsWith('/blog/Performans-Pazarlamasi-Nedir') && !h.startsWith('/blog/kategori/performans-pazarlamasi')) h = '/blog/';\n"
        "    else if (h.startsWith('/en/blog/') && h !== '/en/blog/' && !h.startsWith('/en/blog/what-is-performance-marketing')) h = '/en/blog/';\n"
        "    else if ((h.startsWith('/blog/') || h.startsWith('/en/blog/')) && !h.endsWith('/')) h = h + '/';"
    )

    r_count = 0
    for fp in sorted(glob.glob(os.path.join(PUBLIC_DIR, "**", "*.html"), recursive=True)):
        orig = open(fp, "r", encoding="utf-8").read()
        if "mapKotaHref" not in orig:
            continue
        upd = router_re.sub(lambda _: new_router_rules, orig)
        if upd != orig:
            open(fp, "w", encoding="utf-8").write(upd)
            r_count += 1

    # Clean public/sitemap.xml
    sm_path = os.path.join(PUBLIC_DIR, "sitemap.xml")
    sm = open(sm_path, "r", encoding="utf-8").read()
    drop_patterns = (
        REMOVED_TR_SLUGS
        + REMOVED_EN_SLUGS
        + [
            "/blog/etiket/",
            "/blog/kategori/dijital-pazarlama/",
            "/blog/kategori/reklam-yonetimi/",
            "/blog/kategori/performans-pazarlamasi/",
        ]
    )

    def keep_url_block(m):
        blk = m.group(0)
        return "" if any(dp in blk for dp in drop_patterns) else blk

    sm_new = re.sub(r"\s*<url>.*?</url>", keep_url_block, sm, flags=re.S)
    open(sm_path, "w", encoding="utf-8").write(sm_new.strip() + "\n")

    # Fix inherited blog JSON-LD schema on /referanslar/<slug>/ and /en/references/<slug>/ case study pages
    cs_fixed = 0
    for fp in sorted(
        glob.glob(os.path.join(PUBLIC_DIR, "referanslar", "*", "index.html"))
        + glob.glob(os.path.join(PUBLIC_DIR, "en", "references", "*", "index.html"))
    ):
        rel_dir = os.path.dirname(os.path.relpath(fp, PUBLIC_DIR)).replace(os.sep, "/")
        is_en = rel_dir.startswith("en/")
        canon = f"https://www.roasist.com/{rel_dir}/"
        html = open(fp, "r", encoding="utf-8").read()
        t_m = re.search(r"<title>([^<]+)</title>", html)
        d_m = re.search(r'<meta name="description" content="([^"]*)"', html)
        page_title = (t_m.group(1) if t_m else "Roasist").replace("&amp;", "&")
        short_name = page_title.split("|")[0].strip()
        page_desc = (d_m.group(1) if d_m else "").replace("&amp;", "&")

        def _fix_yoast(m):
            data = json.loads(m.group(2))
            for node in data.get("@graph", []):
                if node.get("@type") == "WebPage":
                    node["@id"] = canon
                    node["url"] = canon
                    node["name"] = page_title
                    node["description"] = page_desc
                    node["breadcrumb"] = {"@id": f"{canon}#breadcrumb"}
                    node["potentialAction"] = [{"@type": "ReadAction", "target": [canon]}]
                elif node.get("@type") == "BreadcrumbList":
                    node["@id"] = f"{canon}#breadcrumb"
                    node["itemListElement"] = (
                        [
                            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.roasist.com/en/"},
                            {"@type": "ListItem", "position": 2, "name": "Case Studies", "item": "https://www.roasist.com/en/references/"},
                            {"@type": "ListItem", "position": 3, "name": short_name, "item": canon},
                        ]
                        if is_en
                        else [
                            {"@type": "ListItem", "position": 1, "name": "Ana Sayfa", "item": "https://www.roasist.com/"},
                            {"@type": "ListItem", "position": 2, "name": "Referanslar", "item": "https://www.roasist.com/referanslar/"},
                            {"@type": "ListItem", "position": 3, "name": short_name, "item": canon},
                        ]
                    )
            return m.group(1) + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + m.group(3)

        html2 = re.sub(
            r'(<script[^>]*class="yoast-schema-graph"[^>]*>)(.*?)(</script>)',
            _fix_yoast,
            html,
            flags=re.S,
        )
        if html2 != html:
            open(fp, "w", encoding="utf-8").write(html2)
            cs_fixed += 1

    print(f"[6/7] Updated mapKotaHref in {r_count} HTML files, fixed {cs_fixed} case-study schemas & cleaned public/sitemap.xml")


def step7_update_css_js_and_cache_bust():
    # 1. Patch /en/blog/ card href in app/blog/page-227af4ac752ea4f7.js -> page-227af4ac752ea4f8.js
    chunks_dir = os.path.join(PUBLIC_DIR, "_next", "static", "chunks")
    blog_js_old = os.path.join(chunks_dir, "app", "blog", "page-227af4ac752ea4f7.js")
    blog_js_new = os.path.join(chunks_dir, "app", "blog", "page-227af4ac752ea4f8.js")
    if os.path.exists(blog_js_old):
        js = open(blog_js_old, "r", encoding="utf-8").read()
        js = js.replace(
            'href:"/blog/".concat(null==s?void 0:s.slug)',
            'href:("undefined"!=typeof document&&"en"===document.documentElement.lang?"/en/blog/":"/blog/").concat(null==s?void 0:s.slug,"/")',
        )
        open(blog_js_old, "w", encoding="utf-8").write(js)
        shutil.copy2(blog_js_old, blog_js_new)

    # 2. Add :only-of-type single-blog editorial rules to CSS & bundles + cache-bust (*m2.css -> *m3.css)
    css_dir = os.path.join(PUBLIC_DIR, "_next", "static", "css")
    old_css_re = re.compile(
        r"\n/\* === SINGLE BLOG POST EDITORIAL LAYOUT.*?\Z",
        re.S,
    )
    css_targets = [
        os.path.join(css_dir, "84191844b30595bc.css"),
        os.path.join(css_dir, "c8ac051173e41d45.css"),
    ] + sorted(glob.glob(os.path.join(css_dir, "roasist-bundle-*.css")))

    for fp in css_targets:
        if not os.path.exists(fp):
            continue
        orig = open(fp, "r", encoding="utf-8").read()
        upd = old_css_re.sub("", orig) + "\n" + SINGLE_BLOG_CSS
        if upd != orig:
            open(fp, "w", encoding="utf-8").write(upd)

    pairs = [("page-227af4ac752ea4f7.js", "page-227af4ac752ea4f8.js")]
    for fp in sorted(glob.glob(os.path.join(css_dir, "roasist-bundle-*m2.css"))):
        old_base = os.path.basename(fp)
        new_base = old_base[:-6] + "m3.css"
        assert len(old_base) == len(new_base)
        shutil.copy2(fp, os.path.join(css_dir, new_base))
        pairs.append((old_base, new_base))

    touched = 0
    for ext in ("*.html", "*.js"):
        for fp in sorted(glob.glob(os.path.join(PUBLIC_DIR, "**", ext), recursive=True)):
            orig = open(fp, "r", encoding="utf-8", errors="ignore").read()
            upd = orig
            for old_s, new_s in pairs:
                upd = upd.replace(old_s, new_s)
            if upd != orig:
                open(fp, "w", encoding="utf-8").write(upd)
                touched += 1
    print(f"[7/7] Added single-post editorial CSS & cache-busted {len(pairs)} assets across {touched} files")


def main():
    step1_remove_extra_blog_directories()
    step2_clean_active_blog_detail_pages()
    step3_update_blog_index_pages()
    step4_update_homepage_articles()
    step5_update_service_related_posts()
    step6_update_runtime_router_and_sitemap()
    step7_update_css_js_and_cache_bust()


if __name__ == "__main__":
    main()
