#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Updates the site-wide PrimaryNavigation menu across all HTML files in public/ and dist/:
  - Sets Hizmetler submenu items to the 5 requested services:
      1. Performans Pazarlaması (/hizmetler/performans-pazarlamasi/)
      2. SEO (/hizmetler/seo/)
      3. Grafik Tasarım (/hizmetler/grafik-tasarim/)
      4. Web Tasarım (/hizmetler/web-tasarim/)
      5. 360° Dijital Pazarlama Yönetimi (/hizmetler/360-derece-dijital-pazarlama-yonetimi/)
  - Removes "Kreatif Stüdyo" and "Kurumsal SEO" from the top-level list
  - Sets Top-Level items:
      1. Referanslar (/referanslar/)
      2. Hakkımızda (/hakkimizda/)
      3. Hizmetler (# with 5 sub-items)
      4. Blog (/blog/)
      5. İletişim (/iletisim/)
  - CTA Button: Projeye Başla (/iletisim/)
  - Updates both SSR HTML markup and Next.js React Flight push chunks
  - Injects submenu max-height fix to ensure smooth animation without clipping
"""

import glob
import json
import os
import re

ROOT = "/home/antigravity/Roasist/roasist-web"

NEW_NODES = [
    {"databaseId": 936, "label": "Referanslar", "uri": "/referanslar/", "childItems": {"nodes": []}},
    {"databaseId": 946, "label": "Hakkımızda", "uri": "/hakkimizda/", "childItems": {"nodes": []}},
    {
        "databaseId": 937,
        "label": "Hizmetler",
        "uri": "#",
        "childItems": {
            "nodes": [
                {"databaseId": 942, "label": "Performans Pazarlaması", "uri": "/hizmetler/performans-pazarlamasi/"},
                {"databaseId": 944, "label": "SEO", "uri": "/hizmetler/seo/"},
                {"databaseId": 945, "label": "Grafik Tasarım", "uri": "/hizmetler/grafik-tasarim/"},
                {"databaseId": 943, "label": "Web Tasarım", "uri": "/hizmetler/web-tasarim/"},
                {"databaseId": 941, "label": "360° Dijital Pazarlama Yönetimi", "uri": "/hizmetler/360-derece-dijital-pazarlama-yonetimi/"},
            ]
        },
    },
    {"databaseId": 938, "label": "Blog", "uri": "/blog/", "childItems": {"nodes": []}},
    {"databaseId": 940, "label": "İletişim", "uri": "/iletisim/", "childItems": {"nodes": []}},
]

NEW_SSR_NAV = (
    '<nav class="PrimaryNavigation_navigation__l8Jgb"><ul>'
    '<li><a href="/referanslar/">Referanslar</a></li>'
    '<li><a href="/hakkimizda/">Hakkımızda</a></li>'
    '<li><div class="PrimaryNavigation_parent__bfX37">Hizmetler'
    '<figure class="PrimaryNavigation_toggleSign__XESvT "><span class="PrimaryNavigation_toggleInner__Lz3QB">'
    '<span class="PrimaryNavigation_toggleLine__QUlfd"></span><span class="PrimaryNavigation_toggleLine__QUlfd"></span>'
    '</span></figure></div>'
    '<ul class="PrimaryNavigation_submenu__ryGWu ">'
    '<li><a href="/hizmetler/performans-pazarlamasi/">Performans Pazarlaması</a></li>'
    '<li><a href="/hizmetler/seo/">SEO</a></li>'
    '<li><a href="/hizmetler/grafik-tasarim/">Grafik Tasarım</a></li>'
    '<li><a href="/hizmetler/web-tasarim/">Web Tasarım</a></li>'
    '<li><a href="/hizmetler/360-derece-dijital-pazarlama-yonetimi/">360° Dijital Pazarlama Yönetimi</a></li>'
    '</ul></li>'
    '<li><a href="/blog/">Blog</a></li>'
    '<li><a href="/iletisim/">İletişim</a></li>'
    '</ul>'
    '<div class="PrimaryNavigation_buttonContainer__iiKTy"><div class="Magnetic_magnetic__LncOy" data-fill="false">'
    '<div class="Button_button__JJiqJ" data-direction="forwards"><a class="Button_inner__fnyH6" href="/iletisim/">'
    '<span class="Button_border__hirH2"></span><span class="Button_text__IZaCD">'
    '<span class="Button_textInner__JTTHe">Projeye Başla</span>'
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 17.1 15.17" class="Button_buttonArrow__0W9XI">'
    '<path d="m17.1,7.58s-.01-.04-.01-.06c.01-.22-.06-.45-.24-.61L9.23.19c-.31-.27-.78-.24-1.06.07-.27.31-.24.78.07,1.06l6.26,5.52H.75c-.41,0-.75.34-.75.75s.34.75.75.75h13.74l-6.26,5.52c-.31.27-.34.75-.07,1.06.15.17.35.25.56.25.18,0,.35-.06.5-.19l7.62-6.72c.18-.16.25-.39.24-.61,0-.02.01-.04.01-.06Z" fill="currentColor"></path>'
    '</svg></span></a></div></div></div></nav>'
)

MENU_STYLE = '<style id="roasist-menu-fix">.PrimaryNavigation_submenuOpen__uJhU7{max-height:280px!important;}</style>'


def update_file(fp: str) -> bool:
    # Skip hakkimizda pages here if handled separately by update_about_page.py, but update if needed
    with open(fp, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    orig = content

    # 1. Update SSR Navigation
    if '<nav class="PrimaryNavigation_navigation__l8Jgb">' in content:
        content = re.sub(
            r'<nav class="PrimaryNavigation_navigation__l8Jgb">.*?</nav>',
            NEW_SSR_NAV,
            content,
            count=1,
            flags=re.S,
        )

    # 2. Update React Flight chunks
    def repl_push(m):
        raw = m.group(1)
        try:
            s = json.loads(raw)
        except Exception:
            return m.group(0)

        lines = s.split("\n")
        new_lines = []
        changed = False
        for line in lines:
            if "menuItems" in line and "nodes" in line:
                idx = line.find(":[")
                if idx != -1:
                    key = line[:idx]
                    try:
                        arr = json.loads(line[idx + 1:])
                        target = None
                        if isinstance(arr, list) and len(arr) >= 4 and isinstance(arr[3], dict):
                            target = arr[3]
                        elif isinstance(arr, list) and len(arr) >= 2 and isinstance(arr[1], dict):
                            target = arr[1]
                        if target and "data" in target and "menu" in target["data"] and "menuItems" in target["data"]["menu"]:
                            target["data"]["menu"]["menuItems"]["nodes"] = NEW_NODES
                            new_line = key + ":" + json.dumps(arr, ensure_ascii=False, separators=(",", ":"))
                            new_lines.append(new_line)
                            changed = True
                            continue
                    except Exception:
                        pass
            new_lines.append(line)

        if changed:
            new_s = "\n".join(new_lines)
            return "self.__next_f.push([1, " + json.dumps(new_s, ensure_ascii=False).replace("<", "\\u003c") + "])"
        return m.group(0)

    if "self.__next_f.push" in content:
        content = re.sub(r"self\.__next_f\.push\(\[1,\s*(\".*?\")\]\)", repl_push, content)

    # 3. Add MENU_STYLE in <head> if not present
    if "roasist-menu-fix" not in content and "</head>" in content:
        content = content.replace("</head>", f"{MENU_STYLE}</head>", 1)

    if content != orig:
        with open(fp, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False


def main():
    total_updated = 0
    for folder in [os.path.join(ROOT, "public"), os.path.join(ROOT, "dist")]:
        files = sorted(glob.glob(f"{folder}/**/*.html", recursive=True))
        updated = 0
        for fp in files:
            # Special case for hakkimizda: let update_about_page.py handle it to keep T-chunk length exact
            if fp.endswith("hakkimizda/index.html"):
                continue
            if update_file(fp):
                updated += 1
        print(f"Updated {updated} files in {folder}")
        total_updated += updated

    # Now run update_about_page.py for hakkimizda files
    print("Running update_about_page.py for hakkimizda...")
    os.system(f"python3 {os.path.join(ROOT, 'scripts', 'update_about_page.py')}")
    print(f"Done! Total files updated: {total_updated + 2}")


if __name__ == "__main__":
    main()
