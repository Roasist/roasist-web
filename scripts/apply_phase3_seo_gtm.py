#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Faz 3 — Analytics (GTM-TRVG2SF + Consent Mode v2), Technical SEO, Schema.org & Draft Cleanup:
  1. Removes leftover development draft HTML files from dist/ and public/.
  2. Across all 88 Turkish KOTA HTML files (44 in public/ + 44 in dist/):
     - Sets <html lang="tr"> in both SSR and Flight record 0.
     - Removes foreign KOTA GA4 (G-XNWXS5PNXY) and Hotjar (1373482) from SSR & Flight record 0,
       disables KOTA's hardcoded English CookieBanner in Flight record 0, and localizes the
       inline 404 fallback in Flight record 0.
     - Replaces https://10-years.kota.co.uk/ Celebrating bar with clean static Roasist AST in SSR & Flight,
       and syncs Homepage Header CTA ("Teklif Al" -> /iletisim/) in Flight.
     - Fixes remaining English meta descriptions (iletisim, start-your-project, referanslar, gizlilik).
     - Updates canonical, og:locale (tr_TR), og:url, og:site_name (Roasist), article:publisher,
       og:image, and twitter:site (@Roasistt) in both SSR <head> and Flight metadata record.
     - Replaces Yoast JSON-LD schema in both SSR and Flight T<hex>, record with valid Roasist
       WebPage + BreadcrumbList + WebSite + Organization schema (+90 540 507 53 50, info@roasist.com, 5 socials).
     - Injects official Google Tag Manager (GTM-TRVG2SF) + Consent Mode v2 in <head>.
  3. Updates dist/404.html with GTM-TRVG2SF and clean canonical/meta.
"""

import glob
import html as html_mod
import json
import os
import re
import sys

ROOT = "/home/antigravity/Roasist/roasist-web"
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from apply_phase1_cleanup import PUSH_RE, parse_flight_stream, serialize_flight_stream  # noqa: E402

SITE_ORIGIN = "https://www.roasist.com"
DEFAULT_OG_IMAGE = (
    "https://cdn.jsdelivr.net/gh/Roasist/roasist-web@5c1d9cff2d8430e51c27f11555dd13bd040c5c55"
    "/public/images/projects/23-projects.jpg"
)
ROASIST_LOGO_PNG = (
    "https://cdn.jsdelivr.net/gh/Roasist/roasist-web@189b2e0aee16a196d88d8895fb3795810c6d17f9"
    "/icon.png"
)

ROASIST_SAME_AS = [
    "https://www.instagram.com/roasist",
    "https://www.linkedin.com/company/roasist",
    "https://twitter.com/Roasistt",
    "https://www.facebook.com/roasistt",
    "https://www.youtube.com/channel/UCY3G_IU2YJ326zGwU3_YlyA",
]

DRAFT_FILES_DIST = [
    "kota-exact.html",
    "kota.html",
    "onizleme.html",
    "partner.html",
    "roasist.html",
    "ust-bolum.html",
    "bolum-2.html",
    "bolum-3.html",
    "bolum-4.html",
]

DRAFT_FILES_PUBLIC = [
    "onizleme.html",
]

DESC_OVERRIDES_TR = {
    "/gizlilik-politikasi-ve-kullanim-sartlari/": (
        "Roasist gizlilik politikası, çerez aydınlatma metni, KVKK kapsamındaki kişisel veri işleme "
        "ilkeleri ve web sitesi kullanım şartları."
    ),
    "/iletisim/": (
        "Markanızın dijital büyüme hedefleri, performans pazarlaması, kurumsal SEO ve web tasarım "
        "projeleri için Roasist uzman ekibiyle iletişime geçin."
    ),
    "/start-your-project/": (
        "Ücretsiz dijital ön analiz ve markanıza özel büyüme stratejisi için Roasist ile projenize "
        "hemen başlayın."
    ),
    "/referanslar/": (
        "Roasist olarak birlikte büyüdüğümüz markaların performans pazarlaması, kurumsal SEO, web tasarım "
        "ve 360° dijital pazarlama başarı hikayelerini inceleyin."
    ),
}

GTM_HEAD_SNIPPET = (
    '<script data-roasist-gtm>'
    'window.dataLayer=window.dataLayer||[];'
    'function gtag(){dataLayer.push(arguments);}'
    '(function(){'
    'var saved=null;try{saved=localStorage.getItem("roasist_cookie_consent");}catch(e){}'
    'var st=saved==="granted"?"granted":"denied";'
    'gtag("consent","default",{'
    'analytics_storage:st,ad_storage:st,ad_user_data:st,ad_personalization:st,wait_for_update:500'
    '});'
    '})();'
    '(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({"gtm.start":new Date().getTime(),event:"gtm.js"});'
    'var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!="dataLayer"?"&l="+l:"";'
    'j.async=true;j.src="https://www.googletagmanager.com/gtm.js?id="+i+dl;f.parentNode.insertBefore(j,f);'
    '})(window,document,"script","dataLayer","GTM-TRVG2SF");'
    '</script>'
)


def rewrite_flight(html_text: str, mutator_fn) -> str:
    matches = list(PUSH_RE.finditer(html_text))
    if not matches:
        return html_text
    joined = "".join(json.loads(m.group(1)) for m in matches)
    records = parse_flight_stream(joined)
    mutator_fn(records)
    new_raw = serialize_flight_stream(records)
    encoded = json.dumps(new_raw, ensure_ascii=False)
    replacement = f"<script>self.__next_f.push([1,{encoded}])</script>"
    first_start = matches[0].start()
    last_end = matches[-1].end()
    return html_text[:first_start] + replacement + html_text[last_end:]


def find_node_by_tag(node, tag: str):
    if isinstance(node, list):
        if len(node) >= 4 and node[0] == "$" and node[1] == tag and isinstance(node[3], dict):
            return node
        for item in node:
            res = find_node_by_tag(item, tag)
            if res is not None:
                return res
    elif isinstance(node, dict):
        for v in node.values():
            res = find_node_by_tag(v, tag)
            if res is not None:
                return res
    return None


def get_route_for_file(fp: str, base_dir: str) -> str:
    rel = os.path.relpath(fp, base_dir).replace("\\", "/")
    if rel in ("index.html", "kota-roasist-local.html"):
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


def build_roasist_schema(
    canonical_url: str,
    route: str,
    title: str,
    description: str,
    lang_code: str = "tr-TR",
    home_label: str = "Ana Sayfa",
    home_url: str = "https://www.roasist.com/",
) -> str:
    crumbs = [{"@type": "ListItem", "position": 1, "name": home_label, "item": home_url}]
    if route not in ("/", "/en/"):
        clean_title = title.split("|")[0].split(" - Roasist")[0].replace("Roasist - ", "").strip()
        crumbs.append({"@type": "ListItem", "position": 2, "name": clean_title, "item": canonical_url})

    graph = [
        {
            "@type": "WebPage",
            "@id": canonical_url,
            "url": canonical_url,
            "name": title,
            "isPartOf": {"@id": f"{SITE_ORIGIN}/#website"},
            "about": {"@id": f"{SITE_ORIGIN}/#organization"},
            "description": description,
            "breadcrumb": {"@id": f"{canonical_url}#breadcrumb"},
            "inLanguage": lang_code,
            "potentialAction": [{"@type": "ReadAction", "target": [canonical_url]}],
        },
        {
            "@type": "BreadcrumbList",
            "@id": f"{canonical_url}#breadcrumb",
            "itemListElement": crumbs,
        },
        {
            "@type": "WebSite",
            "@id": f"{SITE_ORIGIN}/#website",
            "url": f"{SITE_ORIGIN}/",
            "name": "Roasist",
            "description": "Veri Odaklı 360° Dijital Pazarlama, Performans ve Büyüme Ajansı",
            "publisher": {"@id": f"{SITE_ORIGIN}/#organization"},
            "inLanguage": lang_code,
        },
        {
            "@type": "Organization",
            "@id": f"{SITE_ORIGIN}/#organization",
            "name": "Roasist",
            "alternateName": "Roasist Dijital Pazarlama Ajansı",
            "url": f"{SITE_ORIGIN}/",
            "email": "info@roasist.com",
            "telephone": "+90 540 507 53 50",
            "address": {
                "@type": "PostalAddress",
                "addressLocality": "İstanbul",
                "addressCountry": "TR",
            },
            "logo": {
                "@type": "ImageObject",
                "@id": f"{SITE_ORIGIN}/#/schema/logo/image/",
                "url": ROASIST_LOGO_PNG,
                "contentUrl": ROASIST_LOGO_PNG,
                "width": 512,
                "height": 512,
                "caption": "Roasist",
            },
            "sameAs": ROASIST_SAME_AS,
        },
    ]
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))


def clean_draft_files():
    removed = []
    for fn in DRAFT_FILES_DIST:
        p = os.path.join(ROOT, "dist", fn)
        if os.path.exists(p):
            os.remove(p)
            removed.append(f"dist/{fn}")
    for fn in DRAFT_FILES_PUBLIC:
        p = os.path.join(ROOT, "public", fn)
        if os.path.exists(p):
            os.remove(p)
            removed.append(f"public/{fn}")
    print(f"[DRAFTS] Removed {len(removed)} leftover draft files: {removed}")


def update_meta_ast(node, meta_updates: dict):
    """Recursively update <title>, <meta>, and <link rel='canonical'> inside Next.js Flight head array."""
    if isinstance(node, list):
        if len(node) >= 4 and node[0] == "$" and isinstance(node[3], dict):
            tag = node[1]
            props = node[3]
            if tag == "title" and "title" in meta_updates:
                props["children"] = meta_updates["title"]
            elif tag == "link" and props.get("rel") == "canonical" and "canonical" in meta_updates:
                props["href"] = meta_updates["canonical"]
            elif tag == "meta":
                name = props.get("name")
                prop = props.get("property")
                if name == "description" and "description" in meta_updates:
                    props["content"] = meta_updates["description"]
                elif name == "twitter:site":
                    props["content"] = meta_updates["twitter:site"]
                elif name == "twitter:title" and "title" in meta_updates:
                    props["content"] = meta_updates["title"]
                elif name == "twitter:description" and "description" in meta_updates:
                    props["content"] = meta_updates["description"]
                elif name == "twitter:image" and "og:image" in meta_updates:
                    if "kota" in str(props.get("content", "")):
                        props["content"] = meta_updates["og:image"]
                elif prop == "og:locale":
                    props["content"] = meta_updates["og:locale"]
                elif prop == "og:title" and "title" in meta_updates:
                    props["content"] = meta_updates["title"]
                elif prop == "og:description" and "description" in meta_updates:
                    props["content"] = meta_updates["description"]
                elif prop == "og:url":
                    props["content"] = meta_updates["canonical"]
                elif prop == "og:site_name":
                    props["content"] = "Roasist"
                elif prop == "article:publisher":
                    props["content"] = "https://www.facebook.com/roasistt"
                elif prop == "og:image":
                    cur = str(props.get("content", ""))
                    if not cur or "kota" in cur:
                        props["content"] = meta_updates["og:image"]
        for item in node:
            update_meta_ast(item, meta_updates)
    elif isinstance(node, dict):
        for v in node.values():
            update_meta_ast(v, meta_updates)


def sanitize_ast0(node, lang: str = "tr"):
    """Clean foreign GA4/Hotjar, disable English CookieBanner, and localize 404 fallback in Flight record 0."""
    html_node = find_node_by_tag(node, "html")
    if html_node is not None:
        html_node[3]["lang"] = lang
        ch = html_node[3].get("children")
        if isinstance(ch, list):
            for idx in range(len(ch)):
                item_str = json.dumps(ch[idx], ensure_ascii=False)
                if "GA_MEASUREMENT_ID" in item_str or "G-XNWXS5PNXY" in item_str or "hotjar" in item_str or "1373482" in item_str:
                    ch[idx] = False

    def walk(n):
        if isinstance(n, dict):
            if "cookieBanner" in n:
                n["cookieBanner"] = False
            if "notFound" in n and isinstance(n["notFound"], list):
                nf = n["notFound"]
                h1 = find_node_by_tag(nf, "h1")
                if h1 is not None:
                    if lang == "tr":
                        h1[3]["children"] = ["Aradığınız sayfa", ["$", "br", None, {}], "bulunamadı..."]
                    else:
                        h1[3]["children"] = ["Hello there.", ["$", "br", None, {}], "Looks like you're a bit lost..."]
                # Update button inside NotFound_buttonContainer__YCunx
                def fix_nf_btn(sub):
                    if isinstance(sub, dict) and sub.get("type") == "a-internal" and "href" in sub and "text" in sub:
                        sub["href"] = "/" if lang == "tr" else "/en/"
                        sub["text"] = "Ana Sayfaya Dön" if lang == "tr" else "Back to Homepage"
                    elif isinstance(sub, list):
                        for x in sub:
                            fix_nf_btn(x)
                    elif isinstance(sub, dict):
                        for x in sub.values():
                            fix_nf_btn(x)

                fix_nf_btn(nf)
            for v in n.values():
                walk(v)
        elif isinstance(n, list):
            for x in n:
                walk(x)

    walk(node)


def process_kota_tr_file(fp: str, base_dir: str) -> bool:
    html = open(fp, "r", encoding="utf-8").read()
    if "self.__next_f.push" not in html:
        return False

    route = get_route_for_file(fp, base_dir)
    canonical = f"{SITE_ORIGIN}{route}"
    is_home = route == "/"

    # Split SSR vs Flight tail
    matches = list(PUSH_RE.finditer(html))
    if not matches:
        return False
    first_push = matches[0].start()
    ssr = html[:first_push]
    tail = html[first_push:]

    # Extract current title & description from SSR
    t_m = re.search(r"<title>(.*?)</title>", ssr, flags=re.S)
    cur_title = html_mod.unescape(t_m.group(1)).strip() if t_m else "Roasist"

    d_m = re.search(r'<meta name="description" content="(.*?)"', ssr, flags=re.S)
    cur_desc = html_mod.unescape(d_m.group(1)).strip() if d_m else ""
    if route in DESC_OVERRIDES_TR:
        cur_desc = DESC_OVERRIDES_TR[route]

    # Check if SSR has an existing custom og:image (e.g. blog article cover)
    og_img_m = re.search(r'<meta property="og:image" content="(.*?)"', ssr)
    cur_og_img = og_img_m.group(1) if og_img_m else DEFAULT_OG_IMAGE
    if not cur_og_img or "kota" in cur_og_img:
        cur_og_img = DEFAULT_OG_IMAGE

    # 1. SSR <html lang="tr">
    ssr = re.sub(r'<html\s+lang="[^"]*"', '<html lang="tr"', ssr, count=1)

    # 2. Remove foreign GA4 preload / script tags from SSR
    ssr = re.sub(
        r'<link[^>]+href="https://www\.googletagmanager\.com/gtag/js\?id=G-XNWXS5PNXY"[^>]*/>',
        "",
        ssr,
    )
    ssr = re.sub(r'<script[^>]*G-XNWXS5PNXY[^>]*>.*?</script>', "", ssr, flags=re.S)

    # 3. Update SSR <meta> & <link rel="canonical">
    esc_title = html_mod.escape(cur_title, quote=True)
    esc_desc = html_mod.escape(cur_desc, quote=True)

    ssr = re.sub(r'<meta name="description" content="[^"]*"\s*/>', f'<meta name="description" content="{esc_desc}"/>', ssr)
    if '<link rel="canonical"' in ssr:
        ssr = re.sub(r'<link rel="canonical" href="[^"]*"\s*/>', f'<link rel="canonical" href="{canonical}"/>', ssr)
    else:
        ssr = ssr.replace("</title>", f'</title><link rel="canonical" href="{canonical}"/>', 1)

    ssr = re.sub(r'<meta property="og:locale" content="[^"]*"\s*/>', '<meta property="og:locale" content="tr_TR"/>', ssr)
    ssr = re.sub(r'<meta property="og:title" content="[^"]*"\s*/>', f'<meta property="og:title" content="{esc_title}"/>', ssr)
    ssr = re.sub(
        r'<meta property="og:description" content="[^"]*"\s*/>',
        f'<meta property="og:description" content="{esc_desc}"/>',
        ssr,
    )
    ssr = re.sub(r'<meta property="og:url" content="[^"]*"\s*/>', f'<meta property="og:url" content="{canonical}"/>', ssr)
    ssr = re.sub(r'<meta property="og:site_name" content="[^"]*"\s*/>', '<meta property="og:site_name" content="Roasist"/>', ssr)
    ssr = re.sub(
        r'<meta property="article:publisher" content="[^"]*"\s*/>',
        '<meta property="article:publisher" content="https://www.facebook.com/roasistt"/>',
        ssr,
    )
    ssr = re.sub(
        r'<meta property="og:image" content="[^"]*kota[^"]*"\s*/>',
        f'<meta property="og:image" content="{cur_og_img}"/>',
        ssr,
    )
    ssr = re.sub(r'<meta name="twitter:site" content="[^"]*"\s*/>', '<meta name="twitter:site" content="@Roasistt"/>', ssr)

    # 4. Standardize Celebrating_celebrating__MdmnM in SSR (remove 10-years.kota.co.uk)
    has_celebrating_ssr = "Celebrating_celebrating__MdmnM" in ssr
    celebrating_text_tr = "ROASIST DIGITAL — 360° BÜYÜME & KREATİF AJANS : "
    if has_celebrating_ssr:
        ssr = re.sub(
            r'<p class="Celebrating_celebrating__MdmnM"[^>]*>.*?</p>',
            (
                '<p class="Celebrating_celebrating__MdmnM" data-modal-hide="true">'
                f'<a href="/hakkimizda/">{html_mod.escape(celebrating_text_tr)}<!-- -->2026</a></p>'
            ),
            ssr,
            flags=re.S,
        )

    # Normalize Homepage Header CTA href to /iletisim/ in SSR too so SSR and Flight match cleanly
    if is_home:
        ssr = ssr.replace(
            '<a class="Header_button__yG4_K" href="/iletisim">',
            '<a class="Header_button__yG4_K" href="/iletisim/">',
        )

    # 5. Build clean Roasist JSON-LD and replace in SSR
    schema_json = build_roasist_schema(
        canonical_url=canonical,
        route=route,
        title=cur_title,
        description=cur_desc,
        lang_code="tr-TR",
        home_label="Ana Sayfa",
        home_url=f"{SITE_ORIGIN}/",
    )
    ssr = re.sub(
        r'<script type="application/ld\+json" class="yoast-schema-graph">.*?</script>',
        f'<script type="application/ld+json" class="yoast-schema-graph">{schema_json}</script>',
        ssr,
        flags=re.S,
    )

    # 6. Inject GTM-TRVG2SF + Consent Mode v2 in <head> (idempotent)
    ssr = re.sub(r"<script data-roasist-gtm>.*?</script>", "", ssr, flags=re.S)
    ssr = ssr.replace("</head>", f"{GTM_HEAD_SNIPPET}</head>", 1)

    # 7. Mutate Flight records to match SSR 100%
    meta_updates = {
        "title": cur_title,
        "description": cur_desc,
        "canonical": canonical,
        "og:locale": "tr_TR",
        "og:image": cur_og_img,
        "twitter:site": "@Roasistt",
    }

    def flight_mutator(records):
        for rec in records:
            kind, rid, val = rec[0], rec[1], rec[2]
            if kind == "line" and rid == "0":
                ast0 = json.loads(val)
                sanitize_ast0(ast0, lang="tr")
                # Some pages inline metadata inside ast0 as well — update any meta tags inside ast0 safely
                update_meta_ast(ast0, meta_updates)
                rec[2] = json.dumps(ast0, ensure_ascii=False, separators=(",", ":"))
            elif kind == "line" and "Header_header__KwdYD" in val:
                hdr_ast = json.loads(val)
                if isinstance(hdr_ast, list) and len(hdr_ast) >= 2:
                    # Sync Header CTA button on Homepage ("Hire us" -> "Teklif Al", "/iletisim/")
                    def fix_hdr_btn(n):
                        if isinstance(n, list):
                            if len(n) >= 4 and n[0] == "$" and isinstance(n[3], dict):
                                cls = str(n[3].get("className", ""))
                                if "Header_button__yG4_K" in cls:
                                    n[3]["href"] = "/iletisim/" if is_home else "/iletisim/"
                                    # Keep SSR text ("Teklif Al" on home, "Bize Ulaşın" on inner pages)
                                    btn_label = "Teklif Al" if is_home else "Bize Ulaşın"
                                    txt_span = n[3].get("children")
                                    if isinstance(txt_span, list) and len(txt_span) >= 4 and isinstance(txt_span[3], dict):
                                        ch_list = txt_span[3].get("children")
                                        if isinstance(ch_list, list) and len(ch_list) >= 1 and isinstance(ch_list[0], list):
                                            ch_list[0][3]["children"] = btn_label
                            for item in n:
                                fix_hdr_btn(item)
                        elif isinstance(n, dict):
                            for v in n.values():
                                fix_hdr_btn(v)

                    fix_hdr_btn(hdr_ast[0])

                    if has_celebrating_ssr:
                        hdr_ast[1] = [
                            "$",
                            "p",
                            None,
                            {
                                "className": "Celebrating_celebrating__MdmnM",
                                "data-modal-hide": True,
                                "children": [
                                    "$",
                                    "a",
                                    None,
                                    {
                                        "href": "/hakkimizda/",
                                        "children": [celebrating_text_tr, 2026],
                                    },
                                ],
                            },
                        ]
                    else:
                        hdr_ast[1] = None
                    rec[2] = json.dumps(hdr_ast, ensure_ascii=False, separators=(",", ":"))
            elif kind == "line" and ('"rel":"canonical"' in val or '"og:locale"' in val or val.startswith('[[["$","title"')):
                meta_ast = json.loads(val)
                update_meta_ast(meta_ast, meta_updates)
                rec[2] = json.dumps(meta_ast, ensure_ascii=False, separators=(",", ":"))
            elif kind == "text" and '"@context":"https://schema.org"' in val:
                rec[2] = schema_json
            elif kind == "line" and "yoast-schema-graph" in val and '"__html":"{' in val:
                # If schema is inline inside dangerouslySetInnerHTML instead of $xx T-ref
                try:
                    line_ast = json.loads(val)

                    def fix_inline_schema(n):
                        if isinstance(n, dict):
                            if n.get("className") == "yoast-schema-graph" and isinstance(n.get("dangerouslySetInnerHTML"), dict):
                                inner = n["dangerouslySetInnerHTML"].get("__html", "")
                                if isinstance(inner, str) and not inner.startswith("$"):
                                    n["dangerouslySetInnerHTML"]["__html"] = schema_json
                            for v in n.values():
                                fix_inline_schema(v)
                        elif isinstance(n, list):
                            for x in n:
                                fix_inline_schema(x)

                    fix_inline_schema(line_ast)
                    rec[2] = json.dumps(line_ast, ensure_ascii=False, separators=(",", ":"))
                except Exception:
                    pass

    # Also sync inner-page SSR Header_button__yG4_K href="/iletisim/" so SSR and Flight match 1:1
    if not is_home:
        ssr = re.sub(
            r'(<a class="Header_button__yG4_K" href=")[^"]*(")',
            r"\1/iletisim/\2",
            ssr,
        )

    new_tail = rewrite_flight(tail, flight_mutator)
    with open(fp, "w", encoding="utf-8") as f:
        f.write(ssr + new_tail)
    return True


def update_404_page():
    p = os.path.join(ROOT, "dist", "404.html")
    if not os.path.exists(p):
        return
    txt = open(p, "r", encoding="utf-8").read()
    txt = re.sub(r'<html\s+lang="[^"]*"', '<html lang="tr"', txt, count=1)
    txt = re.sub(r"<script data-roasist-gtm>.*?</script>", "", txt, flags=re.S)
    txt = txt.replace("</head>", f"{GTM_HEAD_SNIPPET}</head>", 1)
    with open(p, "w", encoding="utf-8") as f:
        f.write(txt)
    print("[404] Updated dist/404.html with GTM-TRVG2SF and lang='tr'")


def main():
    clean_draft_files()
    total = 0
    for base_name in ("public", "dist"):
        base_dir = os.path.join(ROOT, base_name)
        for fp in sorted(glob.glob(os.path.join(base_dir, "**", "*.html"), recursive=True)):
            if os.path.basename(fp) == "404.html":
                continue
            if "/en/" in fp.replace("\\", "/"):
                continue
            if process_kota_tr_file(fp, base_dir):
                total += 1
    update_404_page()
    print(f"[FAZ 3] Processed {total} Turkish KOTA HTML files across public/ and dist/")


if __name__ == "__main__":
    main()
