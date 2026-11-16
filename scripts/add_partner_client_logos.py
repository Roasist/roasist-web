#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Replaces Mobile Game Factory (`ref-10.png`) with 23Projects (`23projects.png`)
and Urla Balık (`ref-16.png`, or 15th slot `ref-15.png` on About Us) with Dental Art (`dental-art.png`)
inside the black-background reference logos component (`Partners_partners__jBo8y` ->
`Partners_logosInner__Aoq5_`) across Homepage (TR & EN) and About Us (TR & EN) in both `public/` and `dist/`.

Maintains 15 logos (3x5 grid) and 100% parity between SSR HTML and React Flight JSON (`self.__next_f.push`).
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

HOME_LOGOS = [
    ("ref-29.png", ""),
    ("ref-14.png", ""),
    ("ref-04.png", ""),
    ("ref-11.png", ""),
    ("ref-12.png", ""),
    ("ref-23.png", ""),
    ("23projects.png", "23Projects"),   # Replaces Mobile Game Factory (ref-10.png)
    ("ref-06.png", ""),
    ("ref-08.png", ""),
    ("ref-20.png", ""),
    ("ref-27.png", ""),
    ("ref-28.png", ""),
    ("ref-09.png", ""),
    ("ref-22.png", ""),
    ("dental-art.png", "Dental Art"),   # Replaces Urla Balık (ref-16.png)
]

ABOUT_LOGOS = [
    ("ref-01.png", ""),
    ("ref-02.png", ""),
    ("ref-03.png", ""),
    ("ref-04.png", ""),
    ("ref-05.png", ""),
    ("ref-06.png", ""),
    ("ref-07.png", ""),
    ("ref-08.png", ""),
    ("ref-09.png", ""),
    ("23projects.png", "23Projects"),   # Replaces Mobile Game Factory (ref-10.png)
    ("ref-11.png", ""),
    ("ref-12.png", ""),
    ("ref-13.png", ""),
    ("ref-14.png", ""),
    ("dental-art.png", "Dental Art"),   # Replaces 15th slot (ref-15.png)
]

OLD_REF_SHA = "189b2e0aee16a196d88d8895fb3795810c6d17f9"

TARGET_FILES = [
    ("public/kota-roasist-local.html", False, HOME_LOGOS),
    ("public/en/index.html", False, HOME_LOGOS),
    ("public/hakkimizda/index.html", False, ABOUT_LOGOS),
    ("public/en/who-we-are/index.html", False, ABOUT_LOGOS),
    ("dist/index.html", True, HOME_LOGOS),
    ("dist/en/index.html", True, HOME_LOGOS),
    ("dist/hakkimizda/index.html", True, ABOUT_LOGOS),
    ("dist/en/who-we-are/index.html", True, ABOUT_LOGOS),
]

DIV_TAG_RE = re.compile(r"<div(?:\s[^>]*)?>|</div>")


def logo_url_for(fn: str, is_dist: bool, cdn_sha: str) -> str:
    if not is_dist:
        return f"/images/clients-white/{fn}"
    if fn.startswith("ref-"):
        return f"https://cdn.jsdelivr.net/gh/Roasist/roasist-web@{OLD_REF_SHA}/images/clients-white/{fn}"
    return f"https://cdn.jsdelivr.net/gh/Roasist/roasist-web@{cdn_sha}/public/images/clients-white/{fn}"


def replace_logos_inner_ssr(ssr_html: str, logos_spec: list, is_dist: bool, cdn_sha: str) -> str:
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

    rebuilt_inner = "".join(
        f'<div class="Partners_logo__eDI8e" data-animation="grid-item"><img src="{logo_url_for(fn, is_dist, cdn_sha)}" alt="{alt}"/></div>'
        for fn, alt in logos_spec
    )
    return ssr_html[:start] + open_tag + rebuilt_inner + "</div>" + ssr_html[end:]


def update_file(rel_path: str, is_dist: bool, logos_spec: list, cdn_sha: str) -> bool:
    fp = os.path.join(ROOT, rel_path)
    with open(fp, "r", encoding="utf-8") as f:
        html = f.read()

    pushes = list(PUSH_RE.finditer(html))
    if not pushes:
        raise RuntimeError(f"No Flight stream found in {rel_path}")

    ssr = html[: pushes[0].start()]
    tail = html[pushes[0].start() :]

    ssr_updated = replace_logos_inner_ssr(ssr, logos_spec, is_dist, cdn_sha)

    flight_ok = False

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

            rebuilt_children = [
                [
                    "$",
                    "div",
                    str(idx),
                    {
                        "className": "Partners_logo__eDI8e",
                        "data-animation": "grid-item",
                        "children": [
                            "$",
                            "img",
                            None,
                            {
                                "src": logo_url_for(fn, is_dist, cdn_sha),
                                "alt": alt,
                            },
                        ],
                    },
                ]
                for idx, (fn, alt) in enumerate(logos_spec)
            ]

            logos_inner[3]["children"] = rebuilt_children
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
    for rel_path, is_dist, logos_spec in TARGET_FILES:
        if update_file(rel_path, is_dist, logos_spec, cdn_sha):
            updated += 1
            print(f"  [OK] {rel_path}")
        else:
            print(f"  [NO-OP] {rel_path}")
    print(f"Done. Updated {updated}/{len(TARGET_FILES)} files (cdn_sha={cdn_sha}).")


if __name__ == "__main__":
    main()
