#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Converts the black-background reference logos section (`Partners_partners__jBo8y` ->
`Partners_logosInner__Aoq5_`) into a two-row opposite-direction continuous marquee
containing all 37 Roasist reference brand logos across Homepage (TR & EN) and
About Us (TR & EN) in both `public/` and `dist/`.

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

# Row 1 (19 logos): flows smoothly right-to-left
ROW_1_LOGOS = [
    ("23projects.png", "23Projects"),
    ("dental-art.png", "Dental Art"),
    ("ref-29.png", "Medistate Hospital İstanbul"),
    ("ref-27.png", "Summer Home"),
    ("ref-14.png", "Hyundai Su Arıtma Sistemleri"),
    ("ref-04.png", "İstanbul Medya Akademisi"),
    ("ref-11.png", "DermaDerm Laboratories"),
    ("ref-12.png", "Elosé Laboratories"),
    ("ref-23.png", "Kodlab"),
    ("ref-06.png", "Center of Surgeons"),
    ("ref-08.png", "Doctor Bircan"),
    ("ref-20.png", "PedalBox"),
    ("ref-28.png", "Turkey House"),
    ("ref-09.png", "Le Fior"),
    ("ref-22.png", "DecorEvi"),
    ("cordelia.png", "Cordelia"),
    ("loyalcall.png", "LoyalCall"),
    ("bbg-call-center.png", "BBG Call Center"),
    ("ref-01.png", "Turkey Hair Academy"),
]

# Row 2 (18 logos): flows smoothly left-to-right (opposite direction)
ROW_2_LOGOS = [
    ("bessekiz.png", "Beşsekiz Ortaokulları"),
    ("izmir-balik.png", "İzmir Balık Restaurant"),
    ("livaneli.png", "Livaneli Group"),
    ("ref-02.png", "Op. Dr. Özgür Demirtaş"),
    ("ref-03.png", "Kitapbilgini"),
    ("ref-05.png", "Schutz für Kinder (SFK)"),
    ("ref-07.png", "Cos'y Life Consulting"),
    ("ref-10.png", "Mobile Game Factory"),
    ("ref-13.png", "Yoloo"),
    ("ref-15.png", "Autarke Call Center"),
    ("ref-16.png", "Urla Balık"),
    ("ref-17.png", "Natural Dükkan"),
    ("ref-18.png", "3E İlaçlama"),
    ("ref-19.png", "Yengeç"),
    ("ref-21.png", "GekoO"),
    ("ref-24.png", "Sekiz Oniki Kurs"),
    ("ref-25.png", "Düş Bahçesi İlkokulu"),
    ("ref-26.png", "Marmara Kurs"),
]

OLD_REF_SHA = "189b2e0aee16a196d88d8895fb3795810c6d17f9"

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

MARQUEE_STYLE_TAG = """<style data-roasist-logo-marquee>
.Partners_logosInner__Aoq5_{
  display:flex!important;
  flex-direction:column!important;
  gap:clamp(2.5rem,4.2vw,3.75rem)!important;
  width:100%!important;
  overflow:hidden!important;
  position:relative!important;
  padding:clamp(1.25rem,2.5vw,2.25rem) 0!important;
  -webkit-mask-image:linear-gradient(to right,transparent 0%,rgba(0,0,0,1) 10%,rgba(0,0,0,1) 90%,transparent 100%)!important;
  mask-image:linear-gradient(to right,transparent 0%,rgba(0,0,0,1) 10%,rgba(0,0,0,1) 90%,transparent 100%)!important;
}
.roasist-logo-marquee__row{
  display:flex!important;
  width:100%!important;
  overflow:hidden!important;
}
.roasist-logo-marquee__track{
  display:flex!important;
  align-items:center!important;
  width:max-content!important;
  will-change:transform;
}
.roasist-logo-marquee__row--left .roasist-logo-marquee__track{
  animation:roasist-marquee-left 62s linear infinite!important;
}
.roasist-logo-marquee__row--right .roasist-logo-marquee__track{
  animation:roasist-marquee-right 62s linear infinite!important;
}
.roasist-logo-marquee__row:hover .roasist-logo-marquee__track{
  animation-play-state:paused!important;
}
@keyframes roasist-marquee-left{
  0%{transform:translate3d(0,0,0)}
  100%{transform:translate3d(-50%,0,0)}
}
@keyframes roasist-marquee-right{
  0%{transform:translate3d(-50%,0,0)}
  100%{transform:translate3d(0,0,0)}
}
.roasist-logo-marquee__track .Partners_logo__eDI8e{
  flex:0 0 auto!important;
  width:clamp(145px,13.5vw,205px)!important;
  height:clamp(52px,4.8vw,68px)!important;
  margin:0 clamp(1.6rem,2.8vw,2.85rem)!important;
  display:flex!important;
  align-items:center!important;
  justify-content:center!important;
  opacity:0.78!important;
  transition:opacity 180ms cubic-bezier(0.22,1,0.36,1),transform 180ms cubic-bezier(0.22,1,0.36,1)!important;
}
.roasist-logo-marquee__track .Partners_logo__eDI8e:hover{
  opacity:1!important;
  transform:scale(1.06)!important;
}
.roasist-logo-marquee__track .Partners_logo__eDI8e img{
  max-width:100%!important;
  max-height:100%!important;
  width:auto!important;
  height:auto!important;
  object-fit:contain!important;
  margin:0!important;
}
@media (prefers-reduced-motion:reduce){
  .roasist-logo-marquee__row--left .roasist-logo-marquee__track,
  .roasist-logo-marquee__row--right .roasist-logo-marquee__track{
    animation-duration:140s!important;
  }
}
</style>"""

DIV_TAG_RE = re.compile(r"<div(?:\s[^>]*)?>|</div>")


def logo_url_for(fn: str, is_dist: bool, cdn_sha: str) -> str:
    if not is_dist:
        return f"/images/clients-white/{fn}"
    if fn.startswith("ref-"):
        return f"https://cdn.jsdelivr.net/gh/Roasist/roasist-web@{OLD_REF_SHA}/images/clients-white/{fn}"
    return f"https://cdn.jsdelivr.net/gh/Roasist/roasist-web@{cdn_sha}/public/images/clients-white/{fn}"


def build_row_ssr(row_logos: list, direction: str, is_dist: bool, cdn_sha: str) -> str:
    doubled = list(row_logos) + list(row_logos)
    items_html = "".join(
        f'<div class="Partners_logo__eDI8e"><img src="{logo_url_for(fn, is_dist, cdn_sha)}" alt="{alt}" loading="eager" decoding="async"/></div>'
        for fn, alt in doubled
    )
    return (
        f'<div class="roasist-logo-marquee__row roasist-logo-marquee__row--{direction}">'
        f'<div class="roasist-logo-marquee__track">{items_html}</div>'
        f"</div>"
    )


def build_row_flight(row_logos: list, direction: str, row_key: str, is_dist: bool, cdn_sha: str) -> list:
    doubled = list(row_logos) + list(row_logos)
    children = [
        [
            "$",
            "div",
            str(idx),
            {
                "className": "Partners_logo__eDI8e",
                "children": [
                    "$",
                    "img",
                    None,
                    {
                        "src": logo_url_for(fn, is_dist, cdn_sha),
                        "alt": alt,
                        "loading": "eager",
                        "decoding": "async",
                    },
                ],
            },
        ]
        for idx, (fn, alt) in enumerate(doubled)
    ]
    return [
        "$",
        "div",
        row_key,
        {
            "className": f"roasist-logo-marquee__row roasist-logo-marquee__row--{direction}",
            "children": [
                "$",
                "div",
                None,
                {
                    "className": "roasist-logo-marquee__track",
                    "children": children,
                },
            ],
        },
    ]


def replace_logos_inner_ssr(ssr_html: str, is_dist: bool, cdn_sha: str) -> str:
    # 1. Inject or update <style data-roasist-logo-marquee> in <head>
    ssr_html = re.sub(
        r"<style data-roasist-logo-marquee>.*?</style>",
        "",
        ssr_html,
        flags=re.S,
    )
    if "</head>" not in ssr_html:
        raise RuntimeError("Could not find </head> in SSR HTML")
    ssr_html = ssr_html.replace("</head>", f"{MARQUEE_STYLE_TAG}</head>", 1)

    # 2. Replace <div class="Partners_logosInner__Aoq5_">...</div>
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

    row1_ssr = build_row_ssr(ROW_1_LOGOS, "left", is_dist, cdn_sha)
    row2_ssr = build_row_ssr(ROW_2_LOGOS, "right", is_dist, cdn_sha)
    return ssr_html[:start] + open_tag + row1_ssr + row2_ssr + "</div>" + ssr_html[end:]


def update_file(rel_path: str, is_dist: bool, cdn_sha: str) -> bool:
    fp = os.path.join(ROOT, rel_path)
    with open(fp, "r", encoding="utf-8") as f:
        html = f.read()

    pushes = list(PUSH_RE.finditer(html))
    if not pushes:
        raise RuntimeError(f"No Flight stream found in {rel_path}")

    ssr = html[: pushes[0].start()]
    tail = html[pushes[0].start() :]

    ssr_updated = replace_logos_inner_ssr(ssr, is_dist, cdn_sha)

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

            logos_inner[3]["children"] = [
                build_row_flight(ROW_1_LOGOS, "left", "row-left", is_dist, cdn_sha),
                build_row_flight(ROW_2_LOGOS, "right", "row-right", is_dist, cdn_sha),
            ]
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
