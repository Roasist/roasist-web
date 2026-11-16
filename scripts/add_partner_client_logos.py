#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Adds 23Projects (https://www.23projects.net/) and Dental Art (https://www.dentalartalanya.com/)
white reference logos to the black-background reference logos component (`Partners_partners__jBo8y` ->
`Partners_logosInner__Aoq5_`) across Homepage (TR & EN) and About Us (TR & EN) in both `public/` and `dist/`.

Maintains 100% parity between SSR HTML and React Flight JSON (`self.__next_f.push`).
Idempotent: safe to re-run repeatedly.
"""

import argparse
import json
import os
import re
import subprocess
import sys

ROOT = "/home/antigravity/Roasist/roasist-web"
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from apply_phase1_cleanup import (  # noqa: E402
    PUSH_RE,
    find_node_by_class,
    rewrite_flight_in_html,
)

NEW_LOGOS = [
    ("23projects.png", "23Projects"),
    ("dental-art.png", "Dental Art"),
]

TARGET_FILES = [
    ("public/kota-roasist-local.html", False),
    ("public/en/index.html", False),
    ("public/hakkimizda/index.html", False),
    ("public/en/who-we-are/index.html", False),
    ("dist/index.html", True),
    ("dist/en/index.html", True),
    ("dist/hakkimizda/index.html", True),
    ("dist/en/who-we-are/index.html", True),
]

DIV_TAG_RE = re.compile(r"<div(?:\s[^>]*)?>|</div>")


def replace_logos_inner_ssr(ssr_html: str, prefix: str) -> str:
    open_tag = '<div class="Partners_logosInner__Aoq5_">'
    start = ssr_html.find(open_tag)
    if start == -1:
        raise RuntimeError("Could not find Partners_logosInner__Aoq5_ in SSR HTML")

    depth = 0
    end = -1
    for m in DIV_TAG_RE.finditer(ssr_html, start):
        tok = m.group(0)
        if tok.startswith("</div"):
            depth -= 1
            if depth == 0:
                end = m.end()
                break
        else:
            depth += 1

    if end == -1:
        raise RuntimeError("Unbalanced div for Partners_logosInner__Aoq5_")

    inner_html = ssr_html[start + len(open_tag) : end - len("</div>")]
    item_re = re.compile(
        r'<div class="Partners_logo__eDI8e" data-animation="grid-item"><img src="([^"]+)" alt="([^"]*)"/></div>'
    )
    items = item_re.findall(inner_html)
    if not items:
        raise RuntimeError("No Partners_logo__eDI8e items found in SSR HTML")

    new_filenames = {fn for fn, _ in NEW_LOGOS}
    filtered_items = [
        (src, alt)
        for src, alt in items
        if not any(src.endswith("/" + fn) for fn in new_filenames)
    ]

    for fn, alt in NEW_LOGOS:
        filtered_items.append((f"{prefix}/{fn}", alt))

    rebuilt_inner = "".join(
        f'<div class="Partners_logo__eDI8e" data-animation="grid-item"><img src="{src}" alt="{alt}"/></div>'
        for src, alt in filtered_items
    )
    return ssr_html[:start] + open_tag + rebuilt_inner + "</div>" + ssr_html[end:]


def update_file(rel_path: str, is_dist: bool, cdn_sha: str) -> bool:
    fp = os.path.join(ROOT, rel_path)
    with open(fp, "r", encoding="utf-8") as f:
        html = f.read()

    pushes = list(PUSH_RE.finditer(html))
    if not pushes:
        raise RuntimeError(f"No Flight stream found in {rel_path}")

    ssr = html[: pushes[0].start()]
    tail = html[pushes[0].start() :]

    if is_dist:
        prefix = f"https://cdn.jsdelivr.net/gh/Roasist/roasist-web@{cdn_sha}/public/images/clients-white"
    else:
        prefix = "/images/clients-white"

    ssr_updated = replace_logos_inner_ssr(ssr, prefix)

    flight_ok = False
    new_filenames = {fn for fn, _ in NEW_LOGOS}

    def mut(records):
        nonlocal flight_ok
        changed = False
        for rec in records:
            if rec[0] != "line":
                continue
            payload = rec[2]
            if not payload or payload[0] not in "[{" or "Partners_logosInner__Aoq5_" not in payload:
                continue
            ast = json.loads(payload)
            logos_inner = find_node_by_class(ast, "Partners_logosInner__Aoq5_")
            if not logos_inner:
                continue
            children = logos_inner[3].get("children", [])
            filtered_children = []
            for child in children:
                try:
                    img_src = child[3]["children"][3]["src"]
                except (IndexError, KeyError, TypeError):
                    img_src = ""
                if any(img_src.endswith("/" + fn) for fn in new_filenames):
                    continue
                filtered_children.append(child)

            for fn, alt in NEW_LOGOS:
                filtered_children.append(
                    [
                        "$",
                        "div",
                        str(len(filtered_children)),
                        {
                            "className": "Partners_logo__eDI8e",
                            "data-animation": "grid-item",
                            "children": [
                                "$",
                                "img",
                                None,
                                {
                                    "src": f"{prefix}/{fn}",
                                    "alt": alt,
                                },
                            ],
                        },
                    ]
                )

            for idx, child in enumerate(filtered_children):
                child[2] = str(idx)

            logos_inner[3]["children"] = filtered_children
            rec[2] = json.dumps(ast, ensure_ascii=False, separators=(",", ":"))
            flight_ok = True
            changed = True
        return changed

    new_html = ssr_updated + rewrite_flight_in_html(tail, mut)
    if not flight_ok:
        raise RuntimeError(f"Failed to update Partners_logosInner__Aoq5_ in Flight AST of {rel_path}")

    if new_html != html:
        with open(fp, "w", encoding="utf-8") as f:
            f.write(new_html)
        return True
    return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cdn-sha", default=None, help="Git commit SHA on main for jsDelivr URLs in dist/")
    args = parser.parse_args()

    cdn_sha = args.cdn_sha
    if not cdn_sha:
        cdn_sha = (
            subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT)
            .decode("utf-8")
            .strip()
        )

    updated = 0
    for rel_path, is_dist in TARGET_FILES:
        if update_file(rel_path, is_dist, cdn_sha):
            updated += 1
            print(f"  [OK] {rel_path}")
        else:
            print(f"  [NO-OP] {rel_path}")
    print(f"Done. Updated {updated}/{len(TARGET_FILES)} files (cdn_sha={cdn_sha}).")


if __name__ == "__main__":
    main()
