#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prepends Roasist Brand Partner "Leyla" to the `Our Team` (`Team_team__Z__z1`)
section on `/hakkimizda/` (and `/en/who-we-are/` via `build_en_about`),
updating both SSR HTML (initial popover + all 3 Swipers) and React Flight AST
(`data.team` in record `12` and `teamMembers` in record `3c`) with 100% parity.

Idempotent: safe to re-run repeatedly across `public/` and `dist/`.
"""

import json
import os
import re
import sys

ROOT = "/home/antigravity/Roasist/roasist-web"
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from apply_phase1_cleanup import (  # noqa: E402
    PUSH_RE,
    parse_flight_stream,
    serialize_flight_stream,
)

LEYLA_NAME = "Leyla"
LEYLA_TITLE = "Brand Partner"

LEYLA_BIO_TR = (
    "<p>Roasist’te Brand Partner olarak stratejik iş ortaklıkları kuruyor, yeni büyüme fırsatları "
    "geliştiriyor ve markaları hedeflerine özel dijital pazarlama çözümleriyle buluşturuyor.</p>\n"
    "<p>İş stratejisi, müşteri danışmanlığı ve uzman ekipleri tek köprüde birleştirerek, hizmet "
    "sunumunun ötesine geçen kalıcı değer ve sürdürülebilir marka ortaklıkları inşa etmeye odaklanıyor.</p>\n"
)

LEYLA_BIO_EN = (
    "<p>As a Brand Partner at Roasist, Leyla focuses on building strategic partnerships, developing "
    "business opportunities, and connecting brands with tailored digital marketing solutions.</p>\n"
    "<p>Bridging business strategy, client advisory, and cross-functional digital expertise, she "
    "builds trusted relationships and long-term partnerships that deliver lasting value beyond service delivery.</p>\n"
)


def build_leyla_obj(is_dist: bool) -> dict:
    img_base = "/roasist-web/images/team" if is_dist else "/images/team"
    portrait_url = f"{img_base}/leyla-portrait.jpg"
    circle_url = f"{img_base}/leyla-circle.jpg"
    return {
        "bio": LEYLA_BIO_TR,
        "name": LEYLA_NAME,
        "photo": {
            "altText": LEYLA_NAME,
            "srcSet": f"{portrait_url} 705w",
            "sourceUrl": portrait_url,
            "mediaDetails": {"width": 705, "height": 960},
        },
        "title": LEYLA_TITLE,
        "secondaryPhoto": {
            "altText": LEYLA_NAME,
            "srcSet": f"{circle_url} 500w",
            "sourceUrl": circle_url,
            "mediaDetails": {"width": 500, "height": 500},
        },
    }


def build_simple_slide_html(portrait_url: str) -> str:
    return (
        '<div class="swiper-slide" data-roasist-team-leyla="1">'
        f'<img src="{portrait_url}" srcSet="{portrait_url} 705w" alt="{LEYLA_NAME}" '
        'fetchPriority="low" height="960" width="705" sizes="50vw" loading="lazy"/>'
        "</div>"
    )


def build_active_slide_html(portrait_url: str) -> str:
    return (
        '<div class="swiper-slide" data-roasist-team-leyla="1">'
        '<span class="Team_imageContainer__Gef7v">'
        '<div class="Team_panelText__BQVSn" data-swiper-parallax="100%" data-swiper-parallax-duration="600">'
        f'<span class="Team_name__q_itV">{LEYLA_NAME}</span>'
        f'<span class="Team_title__oEVRD">{LEYLA_TITLE}</span>'
        "</div>"
        '<div class="Team_imageOuter__lgtFv" data-swiper-parallax="90%" data-swiper-parallax-duration="600">'
        f'<img src="{portrait_url}" srcSet="{portrait_url} 705w" alt="{LEYLA_NAME}" '
        'fetchPriority="low" height="960" width="705" sizes="50vw" loading="lazy"/>'
        "</div></span></div>"
    )


SINGLE_TEAM_STYLE = (
    "<style data-roasist-single-team>"
    ".Team_swiperLeft__7m5ib,.Team_swiperRight__N2hNV,.Team_arrows__KD1Ad{display:none!important;pointer-events:none!important;}"
    ".Team_swiperActive__7qyzg .swiper-slide .Team_name__q_itV,.Team_swiperActive__7qyzg .swiper-slide .Team_title__oEVRD{opacity:1!important;}"
    "</style>"
)


def upsert_single_team_style(ssr: str) -> str:
    ssr = re.sub(r"<style data-roasist-single-team>.*?</style>", "", ssr, flags=re.S)
    if "</head>" not in ssr:
        raise RuntimeError("Could not locate </head> in SSR HTML")
    return ssr.replace("</head>", SINGLE_TEAM_STYLE + "</head>", 1)


def update_ssr_team_section(ssr: str, is_dist: bool) -> str:
    ssr = upsert_single_team_style(ssr)
    img_base = "/roasist-web/images/team" if is_dist else "/images/team"
    portrait_url = f"{img_base}/leyla-portrait.jpg"
    circle_url = f"{img_base}/leyla-circle.jpg"

    sec_m = re.search(r'<section class="Team_team__Z__z1">.*?</section>', ssr, re.S)
    if not sec_m:
        raise RuntimeError("Could not locate Team_team__Z__z1 section in SSR HTML")

    team_html = sec_m.group(0)

    # 1. Update initial popover secondaryPhoto + bio (index 0)
    new_secondary = (
        '<figure class="Team_secondaryPhoto__4zx1f">'
        '<span class="Image_image__RAAdZ Image_fill__EiIzS">'
        f'<img data-srcset="{circle_url} 500w" data-src="{circle_url}" '
        f'alt="{LEYLA_NAME}" fetchPriority="low" height="500" width="500" sizes="auto" class="lazyload"/>'
        "</span></figure>"
    )
    team_html, n_sec_ph = re.subn(
        r'<figure class="Team_secondaryPhoto__4zx1f">.*?</figure>',
        lambda _m: new_secondary,
        team_html,
        count=1,
        flags=re.S,
    )
    if n_sec_ph != 1:
        raise RuntimeError("Failed to update Team_secondaryPhoto__4zx1f in SSR")

    team_html, n_bio = re.subn(
        r'(<div class="Team_bio__EVTbV">).*?(</div><svg xmlns="http://www\.w3\.org/2000/svg" viewBox="0 0 52 52" class="Team_close__vp9VK">)',
        lambda m: m.group(1) + LEYLA_BIO_TR + m.group(2),
        team_html,
        count=1,
        flags=re.S,
    )
    if n_bio != 1:
        raise RuntimeError("Failed to update Team_bio__EVTbV in SSR")

    # 2. Replace all slides in Left, Active, and Right Swiper wrappers with ONLY Leyla
    simple_slide = build_simple_slide_html(portrait_url)
    active_slide = build_active_slide_html(portrait_url)

    team_html, n_l = re.subn(
        r'(<div class="Team_swiperLeft__7m5ib">.*?<div class="swiper-wrapper">).*?(</div></div></span></span></div>)(?=<div class="Team_swiperActive__7qyzg">)',
        lambda m: m.group(1) + simple_slide + m.group(2),
        team_html,
        count=1,
        flags=re.S,
    )
    team_html, n_a = re.subn(
        r'(<div class="Team_swiperActive__7qyzg"><div class="swiper"><div class="swiper-wrapper">).*?(</div></div></div>)(?=<div class="Team_swiperRight__N2hNV">)',
        lambda m: m.group(1) + active_slide + m.group(2),
        team_html,
        count=1,
        flags=re.S,
    )
    team_html, n_r = re.subn(
        r'(<div class="Team_swiperRight__N2hNV">.*?<div class="swiper-wrapper">).*?(</div></div></span></span></div></div></section>)',
        lambda m: m.group(1) + simple_slide + m.group(2),
        team_html,
        count=1,
        flags=re.S,
    )
    if n_l != 1 or n_a != 1 or n_r != 1:
        raise RuntimeError(f"Failed to replace Swipers with Leyla ({n_l}, {n_a}, {n_r})")

    return ssr[: sec_m.start()] + team_html + ssr[sec_m.end() :]


def update_single_about_team_tr(fp: str, is_dist: bool) -> bool:
    with open(fp, "r", encoding="utf-8") as f:
        html = f.read()

    pushes = list(PUSH_RE.finditer(html))
    if not pushes:
        raise RuntimeError(f"No Flight stream found in {fp}")

    ssr = html[: pushes[0].start()]
    tail = html[pushes[0].start() :]

    ssr_updated = update_ssr_team_section(ssr, is_dist=is_dist)

    # Locate the main Flight chunk containing "Team_team__Z__z1" or "$L3b"
    leyla_obj = build_leyla_obj(is_dist=is_dist)
    out_parts = []
    pos = 0
    rec12_ok = False
    rec3c_ok = False

    for match in PUSH_RE.finditer(tail):
        out_parts.append(tail[pos : match.start()])
        raw_str = json.loads(match.group(1))
        if "$L3b" in raw_str or "3c:" in raw_str:
            records = parse_flight_stream(raw_str)
            changed = False
            for rec in records:
                kind, key, val = rec
                if kind == "line" and key == "12":
                    ast = json.loads(val)
                    sections = ast[2][3]["children"]
                    team_sec = sections[7]
                    team_sec[3]["data"]["team"] = [leyla_obj]
                    rec[2] = json.dumps(ast, ensure_ascii=False, separators=(",", ":"))
                    rec12_ok = True
                    changed = True
                elif kind == "line" and key == "3c":
                    rec[2] = json.dumps([leyla_obj], ensure_ascii=False, separators=(",", ":"))
                    rec3c_ok = True
                    changed = True
            if changed:
                new_stream = serialize_flight_stream(records)
                new_lit = json.dumps(new_stream, ensure_ascii=False).replace("<", "\\u003c")
                out_parts.append(f"<script>self.__next_f.push([1,{new_lit}])</script>")
            else:
                out_parts.append(match.group(0))
        else:
            out_parts.append(match.group(0))
        pos = match.end()

    out_parts.append(tail[pos:])
    if not rec12_ok or not rec3c_ok:
        raise RuntimeError(f"Failed to update Flight records in {fp}: rec12={rec12_ok}, rec3c={rec3c_ok}")

    new_html = ssr_updated + "".join(out_parts)
    if new_html != html:
        with open(fp, "w", encoding="utf-8") as f:
            f.write(new_html)
        return True
    return False


def update_about_team_leyla_tr() -> int:
    count = 0
    for base_name, is_dist in (("public", False), ("dist", True)):
        fp = os.path.join(ROOT, base_name, "hakkimizda", "index.html")
        if update_single_about_team_tr(fp, is_dist=is_dist):
            count += 1
    print(f"[ABOUT TEAM] Updated {count} TR Hakkımızda files with Brand Partner Leyla (solo)")
    return count


if __name__ == "__main__":
    update_about_team_leyla_tr()
