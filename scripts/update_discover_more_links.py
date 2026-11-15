#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Updates all `DiscoverMore` ("Diğer Hizmetlerimiz" / "Explore Our Services") sections
(both Hero top bar and pre-footer dark bar) across all 33 TR + EN service pages
in `public/` and `dist/`:
  - First pill (active / black `.DiscoverMoreLink_active__6IF37`): the current service page.
  - Remaining pills next to it: the other services from the Hizmetler / Services navigation menu.
  - Updates both SSR HTML and Next.js React Flight AST (`self.__next_f.push`) with 100% parity.
"""

import glob
import html as html_mod
import json
import os
import re
import sys

ROOT = "/home/antigravity/Roasist/roasist-web"
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from apply_phase1_cleanup import PUSH_RE, rewrite_flight_in_html  # noqa: E402
from apply_phase3_seo_gtm import get_route_for_file  # noqa: E402

TR_MENU_SERVICES: list[tuple[str, str]] = [
    ("Performans Pazarlaması", "/hizmetler/performans-pazarlamasi/"),
    ("SEO", "/hizmetler/seo/"),
    ("Grafik Tasarım", "/hizmetler/grafik-tasarim/"),
    ("Web Tasarım", "/hizmetler/web-tasarim/"),
    ("360° Dijital Pazarlama Yönetimi", "/hizmetler/360-derece-dijital-pazarlama-yonetimi/"),
]

EN_MENU_SERVICES: list[tuple[str, str]] = [
    ("Performance Marketing", "/en/performance-marketing/"),
    ("SEO", "/en/seo/"),
    ("Graphic Design", "/en/graphic-design/"),
    ("Web Design", "/en/web-design/"),
    ("360° Digital Marketing", "/en/360-digital-marketing-management/"),
]

TR_PAGE_LABELS: dict[str, str] = {
    "/hizmetler/": "Tüm Hizmetler",
    "/hizmetler/performans-pazarlamasi/": "Performans Pazarlaması",
    "/hizmetler/seo/": "SEO",
    "/hizmetler/grafik-tasarim/": "Grafik Tasarım",
    "/hizmetler/web-tasarim/": "Web Tasarım",
    "/hizmetler/360-derece-dijital-pazarlama-yonetimi/": "360° Dijital Pazarlama Yönetimi",
    "/hizmetler/google-reklamlari/": "Google Reklamları",
    "/hizmetler/performans-pazarlamasi/google-reklamlari/": "Google Reklamları",
    "/hizmetler/facebook-reklamlari/": "Facebook Reklamları",
    "/hizmetler/performans-pazarlamasi/facebook-reklamlari/": "Facebook Reklamları",
    "/hizmetler/instagram-reklamlari/": "Instagram Reklamları",
    "/hizmetler/performans-pazarlamasi/instagram-reklamlari/": "Instagram Reklamları",
    "/hizmetler/tiktok-reklamlari/": "TikTok Reklamları",
    "/hizmetler/performans-pazarlamasi/tiktok-reklamlari/": "TikTok Reklamları",
    "/hizmetler/yandex-reklamlari/": "Yandex Reklamları",
    "/hizmetler/performans-pazarlamasi/yandex-reklamlari/": "Yandex Reklamları",
    "/hizmetler/bing-reklamlari/": "Bing Reklamları",
    "/hizmetler/performans-pazarlamasi/bing-reklamlari/": "Bing Reklamları",
    "/hizmetler/linkedin-reklamlari/": "LinkedIn Reklamları",
    "/hizmetler/performans-pazarlamasi/linkedin-reklamlari/": "LinkedIn Reklamları",
}

EN_PAGE_LABELS: dict[str, str] = {
    "/en/services/": "All Services",
    "/en/performance-marketing/": "Performance Marketing",
    "/en/seo/": "SEO",
    "/en/graphic-design/": "Graphic Design",
    "/en/web-design/": "Web Design",
    "/en/360-digital-marketing-management/": "360° Digital Marketing",
    "/en/google-ads/": "Google Ads",
    "/en/facebook-ads/": "Facebook Ads",
    "/en/instagram-ads/": "Instagram Ads",
    "/en/tiktok-ads/": "TikTok Ads",
    "/en/yandex-ads/": "Yandex Ads",
    "/en/bing-ads/": "Bing Ads",
    "/en/linkedin-ads/": "LinkedIn Ads",
}


def resolve_discover_more_for_route(route: str) -> tuple[str, tuple[str, str], list[tuple[str, str]]] | None:
    """Returns `(heading_text, (active_label, active_href), other_items)` for a service route."""
    norm = route if route.endswith("/") else route + "/"
    if norm.startswith("/en/"):
        if norm not in EN_PAGE_LABELS:
            return None
        active = (EN_PAGE_LABELS[norm], norm)
        others = [(lbl, href) for (lbl, href) in EN_MENU_SERVICES if href != norm]
        return ("Other Services", active, others)
    else:
        if norm not in TR_PAGE_LABELS:
            return None
        active = (TR_PAGE_LABELS[norm], norm)
        others = [(lbl, href) for (lbl, href) in TR_MENU_SERVICES if href != norm]
        return ("Diğer Hizmetlerimiz", active, others)


def build_ssr_links_inner(heading: str, active: tuple[str, str], others: list[tuple[str, str]]) -> str:
    act_lbl, act_href = active
    parts = [
        '<div class="DiscoverMore_linksInner__Vgx11">',
        f'<p class="DiscoverMore_heading__fBuVc">{html_mod.escape(heading)}</p>',
        f'<a class="DiscoverMoreLink_active__6IF37" href="{act_href}" aria-current="page">{html_mod.escape(act_lbl)}</a>',
    ]
    for lbl, href in others:
        parts.append(f'<a class="" href="{href}">{html_mod.escape(lbl)}</a>')
    parts.append("</div>")
    return "".join(parts)


def build_flight_links_children(heading: str, active: tuple[str, str], others: list[tuple[str, str]]) -> list:
    act_lbl, act_href = active
    return [
        ["$", "p", None, {"className": "DiscoverMore_heading__fBuVc", "children": heading}],
        [
            "$",
            "a",
            None,
            {
                "className": "DiscoverMoreLink_active__6IF37",
                "href": act_href,
                "aria-current": "page",
                "children": act_lbl,
            },
        ],
        [
            None,
            *[
                [
                    "$",
                    "a",
                    str(idx),
                    {
                        "className": "",
                        "href": href,
                        "children": lbl,
                    },
                ]
                for idx, (lbl, href) in enumerate(others)
            ],
        ],
    ]


def mutate_ast_discover_more(node, new_children: list) -> int:
    replaced = 0
    if isinstance(node, dict):
        if node.get("className") == "DiscoverMore_linksInner__Vgx11":
            node["children"] = json.loads(json.dumps(new_children, ensure_ascii=False))
            replaced += 1
        else:
            for v in node.values():
                replaced += mutate_ast_discover_more(v, new_children)
    elif isinstance(node, list):
        for item in node:
            replaced += mutate_ast_discover_more(item, new_children)
    return replaced


def update_single_file(fp: str, base_dir: str) -> bool:
    route = get_route_for_file(fp, base_dir)
    spec = resolve_discover_more_for_route(route)
    if spec is None:
        return False

    with open(fp, "r", encoding="utf-8") as f:
        html = f.read()

    if "DiscoverMore_linksInner__Vgx11" not in html:
        return False

    heading, active, others = spec
    ssr_block = build_ssr_links_inner(heading, active, others)
    flight_children = build_flight_links_children(heading, active, others)

    pushes = list(PUSH_RE.finditer(html))
    if not pushes:
        return False

    ssr = html[: pushes[0].start()]
    tail = html[pushes[0].start() :]

    ssr_new, ssr_n = re.subn(
        r'<div class="DiscoverMore_linksInner__Vgx11">.*?</div>',
        lambda _m: ssr_block,
        ssr,
        flags=re.S,
    )
    if ssr_n == 0:
        raise RuntimeError(f"Expected SSR DiscoverMore_linksInner__Vgx11 in {fp}")

    html_combined = ssr_new + tail

    flight_hits = 0

    def _mutator(records):
        nonlocal flight_hits
        changed = False
        for rec in records:
            if rec[0] != "line":
                continue
            payload = rec[2]
            if not payload or payload[0] not in "[{":
                continue
            if "DiscoverMore_linksInner__Vgx11" not in payload:
                continue
            ast = json.loads(payload)
            n = mutate_ast_discover_more(ast, flight_children)
            if n > 0:
                rec[2] = json.dumps(ast, ensure_ascii=False, separators=(",", ":"))
                flight_hits += n
                changed = True
        return changed

    updated_html = rewrite_flight_in_html(html_combined, _mutator)
    if flight_hits != ssr_n:
        raise RuntimeError(f"Mismatch in {fp}: ssr_n={ssr_n}, flight_hits={flight_hits}")

    if updated_html != html:
        with open(fp, "w", encoding="utf-8") as f:
            f.write(updated_html)
        return True
    return False


def update_discover_more_all_pages() -> int:
    total = 0
    for base_name in ("public", "dist"):
        base_dir = os.path.join(ROOT, base_name)
        for fp in sorted(glob.glob(os.path.join(base_dir, "**", "index.html"), recursive=True)):
            if update_single_file(fp, base_dir):
                total += 1
    print(f"[DISCOVER MORE] Updated active & menu sibling service pills in {total} HTML files (public + dist)")
    return total


if __name__ == "__main__":
    update_discover_more_all_pages()
