#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Removes the 4-panel Bento video grid (<section class="Bento_bento__aFMAt">...</section>)
from all Turkish (/hizmetler/*) and English (/en/services/ + /en/<service-slug>/) service pages
across both public/ and dist/, keeping SSR HTML and Next.js Flight AST 100% synchronized
for zero React hydration mismatch.
"""

import glob
import json
import os
import re
import sys

ROOT = "/home/antigravity/Roasist/roasist-web"
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from apply_phase1_cleanup import PUSH_RE, rewrite_flight_in_html  # noqa: E402

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

SECTION_TAG_RE = re.compile(r"<section(?:\s[^>]*)?>|</section>")


def replace_exact_section(html_str: str, open_tag_exact: str, replacement: str) -> str:
    """Replaces the exact balanced <section>...</section> block starting at `open_tag_exact`."""
    start = html_str.find(open_tag_exact)
    if start == -1:
        raise RuntimeError(f"Could not find {open_tag_exact!r} in HTML")
    depth = 0
    for m in SECTION_TAG_RE.finditer(html_str, start):
        tok = m.group(0)
        if tok.startswith("</section"):
            depth -= 1
            if depth == 0:
                end = m.end()
                return html_str[:start] + replacement + html_str[end:]
        else:
            depth += 1
    raise RuntimeError(f"Unbalanced <section> starting at {open_tag_exact!r}")


def is_bento_section_node(item) -> bool:
    return (
        isinstance(item, list)
        and len(item) >= 4
        and item[0] == "$"
        and item[1] == "section"
        and isinstance(item[3], dict)
        and str(item[3].get("className", "")).startswith("Bento_bento__")
    )


def strip_bento_from_ast(node) -> int:
    removed = 0
    if isinstance(node, list):
        new_items = []
        for item in node:
            if is_bento_section_node(item):
                removed += 1
            else:
                removed += strip_bento_from_ast(item)
                new_items.append(item)
        if removed > 0 and len(new_items) != len(node):
            node[:] = new_items
    elif isinstance(node, dict):
        for v in node.values():
            removed += strip_bento_from_ast(v)
    return removed


def process_file(fp: str) -> bool:
    with open(fp, "r", encoding="utf-8") as f:
        html = f.read()

    if "Bento_bento__" not in html:
        return False

    pushes = list(PUSH_RE.finditer(html))
    if not pushes:
        return False

    ssr = html[: pushes[0].start()]
    tail = html[pushes[0].start() :]

    open_m = re.search(r'<section class="Bento_bento__[^"]*">', ssr)
    if not open_m:
        raise RuntimeError(f"Missing SSR Bento section tag in {fp}")

    ssr_clean = replace_exact_section(ssr, open_m.group(0), "")
    if 'Intro_intro__' not in ssr_clean:
        raise RuntimeError(f"Safety check failed: Intro_intro__ missing after Bento removal in {fp}")

    flight_removed = 0

    def mut(records):
        nonlocal flight_removed
        any_changed = False
        for rec in records:
            if rec[0] != "line":
                continue
            payload = rec[2]
            if not payload or payload[0] not in "[{" or "Bento_bento__" not in payload:
                continue
            ast = json.loads(payload)
            n = strip_bento_from_ast(ast)
            if n > 0:
                rec[2] = json.dumps(ast, ensure_ascii=False, separators=(",", ":"))
                flight_removed += n
                any_changed = True
        return any_changed

    new_html = ssr_clean + rewrite_flight_in_html(tail, mut)
    if flight_removed != 1:
        raise RuntimeError(f"Expected flight_removed=1 in {fp}, got {flight_removed}")
    if "Bento_bento__" in new_html:
        raise RuntimeError(f"Bento_bento__ still present in {fp}")

    with open(fp, "w", encoding="utf-8") as f:
        f.write(new_html)
    return True


def remove_bento_from_all_service_pages() -> int:
    updated = 0
    for base_name in ("public", "dist"):
        targets = sorted(glob.glob(os.path.join(ROOT, base_name, "hizmetler", "**", "index.html"), recursive=True))
        for slug in EN_SERVICE_SLUGS:
            targets.append(os.path.join(ROOT, base_name, "en", slug, "index.html"))

        for fp in targets:
            if os.path.exists(fp) and process_file(fp):
                updated += 1

    print(f"[BENTO VIDEOS REMOVED] Updated {updated} service HTML files across public/ and dist/")
    return updated


if __name__ == "__main__":
    remove_bento_from_all_service_pages()
