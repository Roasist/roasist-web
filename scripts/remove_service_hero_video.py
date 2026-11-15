#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Removes the circular Hero video (<div class="Hero_video__IHL3y">...</div>) from all
Turkish (/hizmetler/*) and English (/en/services/ + /en/<service-slug>/) service pages
across both public/ and dist/, keeping SSR HTML and Next.js Flight AST 100% synchronized
for zero React hydration mismatch.
"""

import glob
import json
import os
import sys

ROOT = "/home/antigravity/Roasist/roasist-web"
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from apply_phase1_cleanup import PUSH_RE, find_node_by_class, rewrite_flight_in_html  # noqa: E402
from build_english_site_and_switcher import replace_exact_div  # noqa: E402

EN_SERVICE_SLUGS = (
    "services",
    "performance-marketing",
    "google-ads",
    "instagram-ads",
    "facebook-ads",
    "tiktok-ads",
    "linkedin-ads",
    "yandex-ads",
    "bing-ads",
    "seo",
    "graphic-design",
    "web-design",
    "360-digital-marketing-management",
)


def strip_hero_video_from_ast(node) -> bool:
    changed = False
    hero_top = find_node_by_class(node, "Hero_top__fPz2U")
    if hero_top and isinstance(hero_top[3], dict):
        ch = hero_top[3].get("children")
        if isinstance(ch, list):
            filtered = [
                item
                for item in ch
                if not (
                    isinstance(item, list)
                    and len(item) >= 4
                    and isinstance(item[3], dict)
                    and item[3].get("className") == "Hero_video__IHL3y"
                )
            ]
            if len(filtered) != len(ch):
                hero_top[3]["children"] = filtered
                changed = True
    return changed


def process_file(fp: str) -> bool:
    html = open(fp, "r", encoding="utf-8").read()
    if "Hero_video__IHL3y" not in html:
        return False

    pushes = list(PUSH_RE.finditer(html))
    ssr = html[: pushes[0].start()]
    tail = html[pushes[0].start() :]

    if '<div class="Hero_video__IHL3y">' in ssr:
        ssr = replace_exact_div(ssr, '<div class="Hero_video__IHL3y">', "")

    def mut(records):
        any_changed = False
        for rec in records:
            if rec[0] == "line" and "Hero_video__IHL3y" in rec[2]:
                ast = json.loads(rec[2])
                if strip_hero_video_from_ast(ast):
                    rec[2] = json.dumps(ast, ensure_ascii=False, separators=(",", ":"))
                    any_changed = True
        return any_changed

    new_html = ssr + rewrite_flight_in_html(tail, mut)
    if "Hero_video__IHL3y" in new_html:
        raise RuntimeError(f"Hero_video__IHL3y still present in {fp}")

    with open(fp, "w", encoding="utf-8") as f:
        f.write(new_html)
    return True


def main():
    updated = 0
    for base_name in ("public", "dist"):
        targets = sorted(glob.glob(os.path.join(ROOT, base_name, "hizmetler", "**", "index.html"), recursive=True))
        for slug in EN_SERVICE_SLUGS:
            targets.append(os.path.join(ROOT, base_name, "en", slug, "index.html"))

        for fp in targets:
            if os.path.exists(fp) and process_file(fp):
                updated += 1

    print(f"[HERO VIDEO REMOVED] Updated {updated} service HTML files across public/ and dist/")


if __name__ == "__main__":
    main()
