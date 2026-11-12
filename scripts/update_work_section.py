import json
import pathlib
import re

ROOT = pathlib.Path("/home/antigravity/Roasist/roasist-web")

HOMEPAGE_FILES = [
    "public/kota-roasist-local.html",
    "public/onizleme.html",
    "dist/index.html",
    "dist/partner.html",
    "dist/onizleme.html",
    "dist/roasist.html",
    "dist/kota.html",
    "dist/ust-bolum.html",
    "dist/bolum-2.html",
    "dist/bolum-3.html",
    "dist/bolum-4.html",
]

SVG_ARROW_SSR = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 14.78 14.78">'
    '<defs><linearGradient id="d" x1="3.54" x2="13.98" y1="3.54" y2="13.99" gradientUnits="userSpaceOnUse">'
    '<stop offset="0" stop-color="#7c41f3"></stop><stop offset="1" stop-color="#ff6eff"></stop>'
    '</linearGradient></defs>'
    '<path fill="url(#d)" stroke-width="0" d="M13.25 12.18L13.25 0.23 14.78 0.23 14.78 14.76 14.74 14.76 14.74 14.78 0.21 14.78 0.21 13.25 12.18 13.25 0 1.08 1.08 0 13.25 12.18z"></path>'
    '</svg>'
)

SVG_ARROW_OBJ = [
    "$",
    "svg",
    None,
    {
        "xmlns": "http://www.w3.org/2000/svg",
        "viewBox": "0 0 14.78 14.78",
        "children": [
            [
                "$",
                "defs",
                None,
                {
                    "children": [
                        "$",
                        "linearGradient",
                        None,
                        {
                            "id": "d",
                            "x1": "3.54",
                            "x2": "13.98",
                            "y1": "3.54",
                            "y2": "13.99",
                            "gradientUnits": "userSpaceOnUse",
                            "children": [
                                ["$", "stop", None, {"offset": "0", "stopColor": "#7c41f3"}],
                                ["$", "stop", None, {"offset": "1", "stopColor": "#ff6eff"}],
                            ],
                        },
                    ]
                },
            ],
            [
                "$",
                "path",
                None,
                {
                    "fill": "url(#d)",
                    "strokeWidth": "0",
                    "d": "M13.25 12.18L13.25 0.23 14.78 0.23 14.78 14.76 14.74 14.76 14.74 14.78 0.21 14.78 0.21 13.25 12.18 13.25 0 1.08 1.08 0 13.25 12.18z",
                },
            ],
        ],
    },
]

CDN_PROJECTS = "https://cdn.jsdelivr.net/gh/Roasist/roasist-web@2339d60b705457a08a0f8ea860be260e0d57d83b/public/images/projects"

# 5 Featured Roasist Client Brands with custom sector-specific loop MP4 videos & poster images
PROJECTS = [
    {
        "key": "6084",
        "size_cls": "ProjectCard_large__JOQbv",
        "name": "23 Projects",
        "href": "https://www.23projects.net/",
        "year": "2026",
        "heading": "Prestijli gayrimenkul ve yaşam projeleri için uluslararası yatırımcı odaklı dijital büyüme ve performans mimarisi.",
        "tags": [
            "Performans Pazarlaması",
            "Büyüme Stratejisi",
            "Web Analitik",
        ],
        "img_srcset": f"{CDN_PROJECTS}/23-projects.jpg 1440w",
        "img_src": f"{CDN_PROJECTS}/23-projects.jpg",
        "img_w": 1440,
        "img_h": 810,
        "video": f"{CDN_PROJECTS}/23-projects.mp4",
    },
    {
        "key": "8692",
        "size_cls": "ProjectCard_small__xsL92",
        "name": "Summer Homes",
        "href": "https://www.summerhomes.com/",
        "year": "2025",
        "heading": "Uluslararası gayrimenkul lideri için çok dilli performans pazarlaması, kreatif tasarım ve 360° dijital yönetim.",
        "tags": [
            "Performans Pazarlaması",
            "360° Dijital Pazarlama",
            "Web Tasarım",
            "Grafik Tasarım",
            "Büyüme Stratejisi",
            "Web Analitik",
        ],
        "img_srcset": f"{CDN_PROJECTS}/summer-homes.jpg 1440w",
        "img_src": f"{CDN_PROJECTS}/summer-homes.jpg",
        "img_w": 1440,
        "img_h": 810,
        "video": f"{CDN_PROJECTS}/summer-homes.mp4",
    },
    {
        "key": "8166",
        "size_cls": "ProjectCard_small__xsL92",
        "name": "Dental Art",
        "href": "https://www.dentalartalanya.com/",
        "year": "2026",
        "heading": "Avrupa sağlık turizmi pazarında hasta edinimini ölçekleyen çok kanallı performans ve kreatif iletişim stratejisi.",
        "tags": [
            "Performans Pazarlaması",
            "Büyüme Stratejisi",
            "Kreatif İletişim",
        ],
        "img_srcset": f"{CDN_PROJECTS}/dental-art.jpg 1440w",
        "img_src": f"{CDN_PROJECTS}/dental-art.jpg",
        "img_w": 1440,
        "img_h": 810,
        "video": f"{CDN_PROJECTS}/dental-art.mp4",
    },
    {
        "key": "7814",
        "size_cls": "ProjectCard_small__xsL92",
        "name": "Medistate",
        "href": "https://www.medistateinternational.com/",
        "year": "2024",
        "heading": "Uluslararası sağlık grubu için veri odaklı hasta edinimi, web analitik altyapısı ve kreatif iletişim yönetimi.",
        "tags": [
            "Performans Pazarlaması",
            "Büyüme Stratejisi",
            "Web Analitik",
            "Kreatif İletişim",
        ],
        "img_srcset": f"{CDN_PROJECTS}/medistate.jpg 1440w",
        "img_src": f"{CDN_PROJECTS}/medistate.jpg",
        "img_w": 1440,
        "img_h": 810,
        "video": f"{CDN_PROJECTS}/medistate.mp4",
    },
    {
        "key": "7018",
        "size_cls": "ProjectCard_small__xsL92",
        "name": "Bonus Vip",
        "href": "https://bonus-vip.com/",
        "year": "2026",
        "heading": "Türkiye genelinde 13 şubeli sektör lideri için yetenek kazanımı ve kurumsal büyümeyi hızlandıran performans stratejisi.",
        "tags": [
            "Performans Pazarlaması",
            "Büyüme Stratejisi",
            "Web Analitik",
            "Kreatif İletişim",
        ],
        "img_srcset": f"{CDN_PROJECTS}/bonus-vip.jpg 1440w",
        "img_src": f"{CDN_PROJECTS}/bonus-vip.jpg",
        "img_w": 1440,
        "img_h": 810,
        "video": f"{CDN_PROJECTS}/bonus-vip.mp4",
    },
]


def build_ssr_cards() -> str:
    parts = []
    for p in PROJECTS:
        tags_html = "".join(f"<li>{t}</li>" for t in p["tags"])
        card = (
            f'<a class="ProjectCard_project__d1wbY {p["size_cls"]}" data-animation="grid-item" '
            f'href="{p["href"]}" target="_blank" rel="noopener noreferrer">'
            f'<div class="ProjectCard_projectText__o770X">'
            f'<h3>{SVG_ARROW_SSR}{p["name"]}</h3><p>{p["year"]}</p>'
            f'</div>'
            f'<div class="ProjectCard_projectImage__Nfx9I">'
            f'<div class="ProjectCard_imageOverlay__OCawr">'
            f'<p class="ProjectCard_heading__1csIW">{p["heading"]}</p>'
            f'<ul class="ProjectCard_tags__XdVcf">{tags_html}</ul>'
            f'</div>'
            f'<span class="Image_image__RAAdZ Image_fill__EiIzS">'
            f'<img data-srcset="{p["img_srcset"]}" data-src="{p["img_src"]}" alt="" '
            f'fetchPriority="low" height="{p["img_h"]}" width="{p["img_w"]}" sizes="auto" class="lazyload"/>'
            f'</span>'
            f'<video src="{p["video"]}" class="ProjectCard_video__AheFz" autoPlay="" muted="" loop="" preload="none" playsInline=""></video>'
            f'</div></a>'
        )
        parts.append(card)
    return "".join(parts)


def build_flight_cards_escaped() -> str:
    cards_obj = []
    for p in PROJECTS:
        tag_items = [["$", "li", t, {"children": t}] for t in p["tags"]]
        card_obj = [
            "$",
            "$L24",
            p["key"],
            {
                "className": f'ProjectCard_project__d1wbY {p["size_cls"]}',
                "href": p["href"],
                "target": "_blank",
                "rel": "noopener noreferrer",
                "data-animation": "grid-item",
                "children": [
                    [
                        "$",
                        "div",
                        None,
                        {
                            "className": "ProjectCard_projectText__o770X",
                            "children": [
                                [
                                    "$",
                                    "h3",
                                    None,
                                    {"children": [SVG_ARROW_OBJ, p["name"]]},
                                ],
                                ["$", "p", None, {"children": p["year"]}],
                            ],
                        },
                    ],
                    [
                        "$",
                        "div",
                        None,
                        {
                            "className": "ProjectCard_projectImage__Nfx9I",
                            "children": [
                                [
                                    "$",
                                    "div",
                                    None,
                                    {
                                        "className": "ProjectCard_imageOverlay__OCawr",
                                        "children": [
                                            [
                                                "$",
                                                "p",
                                                None,
                                                {
                                                    "className": "ProjectCard_heading__1csIW",
                                                    "dangerouslySetInnerHTML": {"__html": p["heading"]},
                                                },
                                            ],
                                            [
                                                "$",
                                                "ul",
                                                None,
                                                {
                                                    "className": "ProjectCard_tags__XdVcf",
                                                    "children": [tag_items, []],
                                                },
                                            ],
                                        ],
                                    },
                                ],
                                [
                                    "$",
                                    "$L38",
                                    None,
                                    {
                                        "image": {
                                            "altText": "",
                                            "srcSet": p["img_srcset"],
                                            "sourceUrl": p["img_src"],
                                            "mediaDetails": {"width": p["img_w"], "height": p["img_h"]},
                                        },
                                        "layout": "fill",
                                    },
                                ],
                                [
                                    "$",
                                    "video",
                                    None,
                                    {
                                        "src": p["video"],
                                        "className": "ProjectCard_video__AheFz",
                                        "autoPlay": True,
                                        "muted": True,
                                        "loop": True,
                                        "preload": "none",
                                        "playsInline": True,
                                    },
                                ],
                            ],
                        },
                    ],
                ],
            },
        ]
        cards_obj.append(card_obj)

    raw_json = json.dumps(cards_obj, ensure_ascii=False, separators=(",", ":"))
    # Escape for inside JS double-quoted string self.__next_f.push([1, "..."])
    escaped = raw_json.replace("\\", "\\\\").replace('"', '\\"')
    return escaped


def update_homepage(p: pathlib.Path):
    html = p.read_text(encoding="utf-8")

    t712_start = html.find("28:T712,")
    t712_end = html.find("2b:T8f6,", t712_start) if t712_start != -1 else -1
    protected = None
    if t712_start != -1 and t712_end != -1:
        protected = html[t712_start:t712_end]
        html = html[:t712_start] + "__PROTECTED_T712_BLOCK__" + html[t712_end:]

    # 1. Fix "OUR PROJELER" -> "SEÇİLMİŞ PROJELER" (and "Our Results" -> "ÖLÇÜLEBİLİR SONUÇLAR")
    html = html.replace(
        '<span class="Work_heading__pbv4g">Our</span><span class="Work_heading__pbv4g Work_bottom__rzrzH">PROJELER</span>',
        '<span class="Work_heading__pbv4g">SEÇİLMİŞ</span><span class="Work_heading__pbv4g Work_bottom__rzrzH">PROJELER</span>',
    )
    html = html.replace(
        '<span class="StatisticsHeading_heading__3C_3F">Our</span><span class="StatisticsHeading_heading__3C_3F StatisticsHeading_bottom__WtLQC">Results</span>',
        '<span class="StatisticsHeading_heading__3C_3F">ÖLÇÜLEBİLİR</span><span class="StatisticsHeading_heading__3C_3F StatisticsHeading_bottom__WtLQC">SONUÇLAR</span>',
    )
    html = html.replace(
        r'StatisticsHeading_bottom__WtLQC\",\"children\":\"Results\"',
        r'StatisticsHeading_bottom__WtLQC\",\"children\":\"SONUÇLAR\"',
    )

    # 2. Replace SSR 5 ProjectCards inside <div class="Work_projects__A5q77">
    ssr_pat = re.compile(
        r'(<div class="Work_projects__A5q77"><div class="AnimatedGrid_grid__otAMD"><div class="container">)'
        r'.*?'
        r'(<div class="Work_buttonContainer__Owbmu">)',
        re.S,
    )
    new_ssr_cards = build_ssr_cards()
    html, n_ssr = ssr_pat.subn(lambda m: m.group(1) + new_ssr_cards + m.group(2), html, count=1)

    # 3. Update "Tüm Referansları Gör" button href (/work -> /referanslar)
    html = html.replace(
        '<a class="Button_inner__fnyH6" href="/work"><span class="Button_border__hirH2"></span><span class="Button_text__IZaCD"><span class="Button_textInner__JTTHe">Tüm Referansları Gör</span>',
        '<a class="Button_inner__fnyH6" href="/referanslar"><span class="Button_border__hirH2"></span><span class="Button_text__IZaCD"><span class="Button_textInner__JTTHe">Tüm Referansları Gör</span>',
    )
    html = html.replace(
        r'\"href\":\"/work\",\"text\":\"Tüm Referansları Gör\"',
        r'\"href\":\"/referanslar\",\"text\":\"Tüm Referansları Gör\"',
    )

    # 4. Replace Flight JSON 5 ProjectCards inside Work_projects__A5q77
    flight_prefix = r'Work_projects__A5q77\",\"children\":[\"$\",\"$L37\",null,{\"children\":[\"$\",\"div\",null,{\"className\":\"container\",\"children\":['
    flight_suffix = r',[\"$\",\"div\",null,{\"className\":\"Work_buttonContainer__Owbmu\"'
    f_start = html.find(flight_prefix)
    f_end = html.find(flight_suffix, f_start) if f_start != -1 else -1
    n_flight = 0
    if f_start != -1 and f_end != -1:
        cards_escaped = build_flight_cards_escaped()
        html = html[: f_start + len(flight_prefix)] + cards_escaped + html[f_end:]
        n_flight = 1

    # 5. Clean up any remaining SaaS and Tech in Footer Flight JSON
    html = html.replace(r'\"children\":\"SaaS and Tech\"', r'\"children\":\"Google Ads\"')

    if protected is not None:
        html = html.replace("__PROTECTED_T712_BLOCK__", protected)

    p.write_text(html, encoding="utf-8")
    print(f"Homepage updated: {p.relative_to(ROOT)} (ssr={n_ssr}, flight={n_flight})")


def clean_inner_pages():
    cleaned = 0
    for sub in ["public", "dist"]:
        for p in sorted((ROOT / sub).rglob("*.html")):
            if p.name == "kota-exact.html":
                continue
            rel = str(p.relative_to(ROOT))
            if rel in HOMEPAGE_FILES:
                continue
            orig = p.read_text(encoding="utf-8")
            txt = orig
            # Remove Finans & Fintech and B2B Teknoloji & SaaS / Yazılım tags from any ProjectCards on inner pages
            txt = txt.replace("<li>Finans &amp; Fintech</li>", "")
            txt = txt.replace("<li>Finans & Fintech</li>", "")
            txt = txt.replace("<li>B2B Teknoloji &amp; SaaS</li>", "")
            txt = txt.replace("<li>B2B Teknoloji & SaaS</li>", "")
            txt = txt.replace("<li>B2B Teknoloji &amp; Yazılım</li>", "")
            txt = txt.replace("<li>B2B Teknoloji & Yazılım</li>", "")
            txt = txt.replace(
                r',[[\"$\",\"li\",\"B2B Teknoloji & Yazılım\",{\"children\":\"B2B Teknoloji & Yazılım\"}]]',
                ",[]",
            )
            txt = txt.replace(
                r',[[\"$\",\"li\",\"B2B Teknoloji \u0026 SaaS\",{\"children\":\"B2B Teknoloji \u0026 SaaS\"}]]',
                ",[]",
            )
            txt = txt.replace(
                r',[[\"$\",\"li\",\"Finance\",{\"children\":\"Finance\"}]]',
                ",[]",
            )
            if txt != orig:
                p.write_text(txt, encoding="utf-8")
                cleaned += 1
    print(f"Cleaned banned sector tags from {cleaned} inner HTML files")


def main():
    for rel in HOMEPAGE_FILES:
        p = ROOT / rel
        if p.exists():
            update_homepage(p)
    clean_inner_pages()


if __name__ == "__main__":
    main()
