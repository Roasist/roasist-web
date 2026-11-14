#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hydration-safe updater for all 'Başarı Hikayelerimiz' (RelatedProjects) sections across the site:
  - Replaces KOTA placeholder projects (UPP, Incentive Games, The Goat Agency, Bipsync, Wogan Coffee, DK&A)
    with Roasist's 5 featured homepage references from scripts/update_work_section.py:
      1. 23 Projects (ProjectCard_large__JOQbv)
      2. Summer Homes (ProjectCard_small__xsL92)
      3. Dental Art (ProjectCard_small__xsL92)
      4. Medistate (ProjectCard_small__xsL92)
      5. Bonus Vip (ProjectCard_small__xsL92)
  - Updates 'Tüm Referansları Gör' button links inside RelatedProjects from /work to /referanslar/
  - Updates both SSR HTML and Next.js React Flight AST (preserving exact per-page $L module IDs
    and recomputing UTF-8 byte lengths for any T<hex>, chunks) across all 21 public/ and 21 dist/ pages.
"""

import json
import os
import re
import sys

ROOT = "/home/antigravity/Roasist/roasist-web"
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from update_about_page import parse_flight_stream, serialize_flight_stream  # noqa: E402
from update_work_section import PROJECTS, SVG_ARROW_OBJ, build_ssr_cards  # noqa: E402


def build_flight_project_cards(card_link_id: str, image_comp_id: str) -> list:
    cards = []
    for p in PROJECTS:
        tag_items = [["$", "li", t, {"children": t}] for t in p["tags"]]
        cards.append(
            [
                "$",
                card_link_id,
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
                                                        "dangerouslySetInnerHTML": {
                                                            "__html": p["heading"]
                                                        },
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
                                        image_comp_id,
                                        None,
                                        {
                                            "image": {
                                                "altText": "",
                                                "srcSet": p["img_srcset"],
                                                "sourceUrl": p["img_src"],
                                                "mediaDetails": {
                                                    "width": p["img_w"],
                                                    "height": p["img_h"],
                                                },
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
        )
    return cards


def find_related_projects_node(node):
    if isinstance(node, list):
        if (
            len(node) == 4
            and node[0] == "$"
            and isinstance(node[3], dict)
            and node[3].get("className") == "RelatedProjects_relatedProjects__opNhl"
        ):
            return node
        for item in node:
            res = find_related_projects_node(item)
            if res is not None:
                return res
    elif isinstance(node, dict):
        for val in node.values():
            res = find_related_projects_node(val)
            if res is not None:
                return res
    return None


def update_view_all_hrefs(node):
    if isinstance(node, list):
        if (
            len(node) == 4
            and node[0] == "$"
            and isinstance(node[3], dict)
            and node[3].get("text") == "Tüm Referansları Gör"
            and node[3].get("href") in ("/work", "/work/", "/referanslar")
        ):
            node[3]["href"] = "/referanslar/"
        for item in node:
            update_view_all_hrefs(item)
    elif isinstance(node, dict):
        for val in node.values():
            update_view_all_hrefs(val)


def update_file(abs_path: str) -> bool:
    with open(abs_path, "r", encoding="utf-8") as f:
        orig_html = f.read()

    if "RelatedProjects_relatedProjects__opNhl" not in orig_html:
        return False

    html = orig_html

    # 1. Update SSR HTML inside <section class="RelatedProjects_relatedProjects__opNhl">...</section>
    sec_re = re.compile(
        r'<section class="RelatedProjects_relatedProjects__opNhl">.*?</section>', re.S
    )
    m_sec = sec_re.search(html)
    if not m_sec:
        raise RuntimeError(f"SSR RelatedProjects section not found in {abs_path}")

    sec_html = m_sec.group(0)
    grid_re = re.compile(
        r'(<div class="AnimatedGrid_grid__otAMD"><div class="container">)'
        r".*?"
        r'(</div></div><div class="container"><div class="RelatedProjects_viewAllLinkMobile__pDKQH">)',
        re.S,
    )
    new_cards_ssr = build_ssr_cards()
    sec_html, n_grid = grid_re.subn(
        lambda m: m.group(1) + new_cards_ssr + m.group(2), sec_html, count=1
    )
    if n_grid != 1:
        raise RuntimeError(f"Failed to replace SSR AnimatedGrid in {abs_path}")

    # Update 'Tüm Referansları Gör' button href in SSR RelatedProjects section
    sec_html = sec_html.replace(
        '<a class="Button_inner__fnyH6" href="/work"><span class="Button_border__hirH2"></span><span class="Button_text__IZaCD"><span class="Button_textInner__JTTHe">Tüm Referansları Gör</span>',
        '<a class="Button_inner__fnyH6" href="/referanslar/"><span class="Button_border__hirH2"></span><span class="Button_text__IZaCD"><span class="Button_textInner__JTTHe">Tüm Referansları Gör</span>',
    )

    html = html[: m_sec.start()] + sec_html + html[m_sec.end() :]

    # 2. Update React Flight AST
    push_re = re.compile(r"self\.__next_f\.push\(\[1,\s*(\"(?:\\.|[^\"\\])*\")\]\)")
    pushes = list(push_re.finditer(html))
    patched_flight = False

    for pm in reversed(pushes):
        flight_str = json.loads(pm.group(1))
        if "RelatedProjects_relatedProjects__opNhl" not in flight_str:
            continue

        records = parse_flight_stream(flight_str)
        for rec in records:
            kind, key, val = rec
            if kind == "line" and "RelatedProjects_relatedProjects__opNhl" in val:
                ast = json.loads(val)
                rp_node = find_related_projects_node(ast)
                if rp_node is None:
                    raise RuntimeError(f"RP AST node not found in {abs_path}")

                # Extract exact per-page module IDs ($L26/$L47 on hizmetler, $L23/$L2a on blog)
                grid_container = rp_node[3]["children"][2][3]["children"]
                existing_cards = grid_container[3]["children"]
                first_card = existing_cards[0]
                card_link_id = first_card[1]
                # Find image component ID inside first_card's ProjectCard_projectImage__Nfx9I children
                img_children = first_card[3]["children"][1][3]["children"]
                image_comp_id = img_children[1][1]

                if not (card_link_id.startswith("$L") and image_comp_id.startswith("$L")):
                    raise RuntimeError(
                        f"Unexpected module IDs ({card_link_id}, {image_comp_id}) in {abs_path}"
                    )

                grid_container[3]["children"] = build_flight_project_cards(
                    card_link_id, image_comp_id
                )
                update_view_all_hrefs(rp_node)

                rec[2] = json.dumps(ast, ensure_ascii=False, separators=(",", ":"))
                patched_flight = True

        new_flight_str = serialize_flight_stream(records)
        assert serialize_flight_stream(parse_flight_stream(new_flight_str)) == new_flight_str
        encoded_flight = json.dumps(new_flight_str, ensure_ascii=False).replace(
            "</script>", "<\\/script>"
        )
        new_push = f"self.__next_f.push([1,{encoded_flight}])"
        html = html[: pm.start()] + new_push + html[pm.end() :]

    if not patched_flight:
        raise RuntimeError(f"Failed to patch Flight RelatedProjects in {abs_path}")

    with open(abs_path, "w", encoding="utf-8") as f:
        f.write(html)
    return True


def main():
    updated_public = 0
    updated_dist = 0
    for base_name in ("public", "dist"):
        base_dir = os.path.join(ROOT, base_name)
        for root, _, files in os.walk(base_dir):
            for fn in sorted(files):
                if not fn.endswith(".html") or fn == "kota-exact.html":
                    continue
                fp = os.path.join(root, fn)
                if update_file(fp):
                    if base_name == "public":
                        updated_public += 1
                    else:
                        updated_dist += 1
                    print(f"[OK] {os.path.relpath(fp, ROOT)}")

    print(
        f"\nCompleted: updated {updated_public} public/ files and {updated_dist} dist/ files."
    )


if __name__ == "__main__":
    main()
