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

CANER_NAME = "Caner"
CANER_TITLE = "Performance Marketing Manager"

CANER_BIO_TR = (
    "<p>Roasist’te Performance Marketing Manager olarak Google, Meta, TikTok ve LinkedIn ekosistemlerinde "
    "veri odaklı ücretli medya stratejilerini ve çok kanallı büyüme kampanyalarını uçtan uca yönetiyor.</p>\n"
    "<p>Bütçe optimizasyonu, dönüşüm odaklı ölçümleme ve sürekli test yaklaşımıyla reklam yatırımlarını "
    "ölçülebilir ciroya ve sürdürülebilir ROAS artışına dönüştürmeye odaklanıyor.</p>\n"
)

CANER_BIO_EN = (
    "<p>As Performance Marketing Manager at Roasist, Caner leads data-driven paid media strategies and "
    "multi-channel growth campaigns end-to-end across Google, Meta, TikTok, and LinkedIn.</p>\n"
    "<p>Through disciplined budget allocation, conversion tracking, and continuous creative testing, "
    "he turns ad spend into measurable revenue and sustainable ROAS growth.</p>\n"
)

EBRU_NAME = "Ebru"
EBRU_TITLE = "Lead Generation Executive"

EBRU_BIO_TR = (
    "<p>Roasist’te Lead Generation Executive olarak potansiyel müşteri kazanımı süreçlerini yönetiyor, "
    "doğru hedef kitle analiziyle yüksek dönüşüm potansiyelli iş fırsatlarını markalarla buluşturuyor.</p>\n"
    "<p>Çok kanallı erişim stratejileri, nitelikli talep oluşturma ve sistematik aday takibiyle satış "
    "hunisini besleyerek sürdürülebilir müşteri büyümesine doğrudan katkı sağlıyor.</p>\n"
)

EBRU_BIO_EN = (
    "<p>As Lead Generation Executive at Roasist, Ebru drives B2B and B2C client acquisition pipelines, "
    "connecting ambitious brands with high-intent growth opportunities through precise audience targeting.</p>\n"
    "<p>Through multi-channel outreach, qualified demand generation, and structured pipeline management, "
    "she fuels the sales funnel and accelerates sustainable revenue growth.</p>\n"
)


def build_member_obj(name: str, title: str, bio_tr: str, slug: str, is_dist: bool) -> dict:
    img_base = "/roasist-web/images/team" if is_dist else "/images/team"
    portrait_url = f"{img_base}/{slug}-portrait.jpg"
    circle_url = f"{img_base}/{slug}-circle.jpg"
    return {
        "bio": bio_tr,
        "name": name,
        "photo": {
            "altText": name,
            "srcSet": f"{portrait_url} 705w",
            "sourceUrl": portrait_url,
            "mediaDetails": {"width": 705, "height": 960},
        },
        "title": title,
        "secondaryPhoto": {
            "altText": name,
            "srcSet": f"{circle_url} 500w",
            "sourceUrl": circle_url,
            "mediaDetails": {"width": 500, "height": 500},
        },
    }


def build_team_members(is_dist: bool) -> list[dict]:
    return [
        build_member_obj(LEYLA_NAME, LEYLA_TITLE, LEYLA_BIO_TR, "leyla", is_dist),
        build_member_obj(CANER_NAME, CANER_TITLE, CANER_BIO_TR, "caner", is_dist),
        build_member_obj(EBRU_NAME, EBRU_TITLE, EBRU_BIO_TR, "ebru", is_dist),
    ]


def build_simple_slide_html(member: dict) -> str:
    portrait_url = member["photo"]["sourceUrl"]
    name = member["name"]
    return (
        '<div class="swiper-slide">'
        f'<img src="{portrait_url}" srcSet="{portrait_url} 705w" alt="{name}" '
        'fetchPriority="low" height="960" width="705" sizes="50vw" loading="lazy"/>'
        "</div>"
    )


def build_active_slide_html(member: dict) -> str:
    portrait_url = member["photo"]["sourceUrl"]
    name = member["name"]
    title = member["title"]
    return (
        '<div class="swiper-slide">'
        '<span class="Team_imageContainer__Gef7v">'
        '<div class="Team_panelText__BQVSn" data-swiper-parallax="100%" data-swiper-parallax-duration="600">'
        f'<span class="Team_name__q_itV">{name}</span>'
        f'<span class="Team_title__oEVRD">{title}</span>'
        "</div>"
        '<div class="Team_imageOuter__lgtFv" data-swiper-parallax="90%" data-swiper-parallax-duration="600">'
        f'<img src="{portrait_url}" srcSet="{portrait_url} 705w" alt="{name}" '
        'fetchPriority="low" height="960" width="705" sizes="50vw" loading="lazy"/>'
        "</div></span></div>"
    )


def strip_single_team_style(ssr: str) -> str:
    return re.sub(r"<style data-roasist-single-team>.*?</style>", "", ssr, flags=re.S)


OFFICIAL_PARTNERS_TR = [
    ("badge-google-partner-w.svg", "Google Partner"),
    ("badge-meta-partner-w.svg", "Meta Business Partner"),
    ("badge-tiktok-partner-w.svg", "TikTok Marketing Partner"),
    ("badge-ai-seo-w.svg", "Yandex Ads Partner"),
]


def build_ssr_bigups_section(is_dist: bool) -> str:
    partner_base = "/roasist-web/images" if is_dist else "/images"
    rows_html = []
    for svg_file, name in OFFICIAL_PARTNERS_TR:
        logo_url = f"{partner_base}/{svg_file}"
        rows_html.append(
            '<span class="FadeIn_container__bjQVL" data-fill="false">'
            '<div class="BigUps_award__D7Yq2">'
            f'<figure class="BigUps_logo__sSEo5"><img src="{logo_url}" alt="{name}"/></figure>'
            "</div></span>"
        )
    return (
        '<div class="BigUps_partners__xRCBU">'
        '<div class="DarkThemeSwitch_cover__hn_xc"></div>'
        '<div class="container">'
        '<h2 class="BigUps_heading__zYN_v"><span class="BigUps_heading__zYN_v">Resmi Partnerlikler</span></h2>'
        f'<div class="BigUps_awards__JQZ1R">{"".join(rows_html)}</div>'
        "</div></div>"
    )


def build_flight_bigups_node(is_dist: bool) -> list:
    partner_base = "/roasist-web/images" if is_dist else "/images"
    award_nodes = []
    for idx, (svg_file, name) in enumerate(OFFICIAL_PARTNERS_TR):
        logo_url = f"{partner_base}/{svg_file}"
        award_nodes.append(
            [
                "$",
                "$L39",
                str(idx),
                {
                    "children": [
                        "$",
                        "div",
                        str(idx),
                        {
                            "className": "BigUps_award__D7Yq2",
                            "children": [
                                [
                                    "$",
                                    "figure",
                                    None,
                                    {
                                        "className": "BigUps_logo__sSEo5",
                                        "children": ["$", "img", None, {"src": logo_url, "alt": name}],
                                    },
                                ],
                            ],
                        },
                    ]
                },
            ]
        )
    return [
        "$",
        "div",
        None,
        {
            "className": "BigUps_partners__xRCBU",
            "children": [
                ["$", "$L1f", None, {}],
                [
                    "$",
                    "div",
                    None,
                    {
                        "className": "container",
                        "children": [
                            [
                                "$",
                                "h2",
                                None,
                                {
                                    "className": "BigUps_heading__zYN_v",
                                    "children": [
                                        "$",
                                        "span",
                                        None,
                                        {"className": "BigUps_heading__zYN_v", "children": "Resmi Partnerlikler"},
                                    ],
                                },
                            ],
                            [
                                "$",
                                "div",
                                None,
                                {
                                    "className": "BigUps_awards__JQZ1R",
                                    "children": award_nodes,
                                },
                            ],
                        ],
                    },
                ],
            ],
        },
    ]


def build_about_cta_subheading_tr(is_dist: bool) -> str:
    contact_href = "/roasist-web/iletisim/" if is_dist else "/iletisim/"
    return f'<p>Bize hemen ulaşın:<br />\n<a href="{contact_href}">İletişim Formunu Doldurun</a></p>\n'


def update_ssr_team_section(ssr: str, is_dist: bool) -> str:
    ssr = strip_single_team_style(ssr)
    members = build_team_members(is_dist=is_dist)
    first = members[0]
    circle_url = first["secondaryPhoto"]["sourceUrl"]

    # 0A. Replace BigUps_partners__xRCBU block right before Team_team__Z__z1
    bigups_ssr = build_ssr_bigups_section(is_dist=is_dist)
    ssr, n_bigups = re.subn(
        r'<div class="BigUps_partners__xRCBU">.*?(?=<section class="Team_team__Z__z1">)',
        lambda _m: bigups_ssr,
        ssr,
        count=1,
        flags=re.S,
    )
    if n_bigups != 1:
        raise RuntimeError("Failed to update BigUps_partners__xRCBU in SSR HTML")

    # 0B. Replace LargeCta_subHeading__Cs6d8 mailto link with contact form link
    cta_sub_html = build_about_cta_subheading_tr(is_dist=is_dist)
    ssr, n_cta = re.subn(
        r'(<div class="LargeCta_subHeading__Cs6d8">).*?(</div><p class="LargeCta_mainText__6MrpN">)',
        lambda m: m.group(1) + cta_sub_html + m.group(2),
        ssr,
        count=1,
        flags=re.S,
    )
    if n_cta != 1:
        raise RuntimeError("Failed to update LargeCta_subHeading__Cs6d8 in SSR HTML")

    sec_m = re.search(r'<section class="Team_team__Z__z1">.*?</section>', ssr, re.S)
    if not sec_m:
        raise RuntimeError("Could not locate Team_team__Z__z1 section in SSR HTML")

    team_html = sec_m.group(0)

    # 1. Update initial popover secondaryPhoto + bio (index 0)
    new_secondary = (
        '<figure class="Team_secondaryPhoto__4zx1f">'
        '<span class="Image_image__RAAdZ Image_fill__EiIzS">'
        f'<img data-srcset="{circle_url} 500w" data-src="{circle_url}" '
        f'alt="{first["name"]}" fetchPriority="low" height="500" width="500" sizes="auto" class="lazyload"/>'
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
        lambda m: m.group(1) + first["bio"] + m.group(2),
        team_html,
        count=1,
        flags=re.S,
    )
    if n_bio != 1:
        raise RuntimeError("Failed to update Team_bio__EVTbV in SSR")

    # 2. Replace slides in Left, Active, and Right Swiper wrappers with [Leyla, Caner, Ebru]
    simple_slides = "".join(build_simple_slide_html(m) for m in members)
    active_slides = "".join(build_active_slide_html(m) for m in members)

    team_html, n_l = re.subn(
        r'(<div class="Team_swiperLeft__7m5ib">.*?<div class="swiper-wrapper">).*?(</div></div></span></span></div>)(?=<div class="Team_swiperActive__7qyzg">)',
        lambda m: m.group(1) + simple_slides + m.group(2),
        team_html,
        count=1,
        flags=re.S,
    )
    team_html, n_a = re.subn(
        r'(<div class="Team_swiperActive__7qyzg"><div class="swiper"><div class="swiper-wrapper">).*?(</div></div></div>)(?=<div class="Team_swiperRight__N2hNV">)',
        lambda m: m.group(1) + active_slides + m.group(2),
        team_html,
        count=1,
        flags=re.S,
    )
    team_html, n_r = re.subn(
        r'(<div class="Team_swiperRight__N2hNV">.*?<div class="swiper-wrapper">).*?(</div></div></span></span></div></div></section>)',
        lambda m: m.group(1) + simple_slides + m.group(2),
        team_html,
        count=1,
        flags=re.S,
    )
    if n_l != 1 or n_a != 1 or n_r != 1:
        raise RuntimeError(f"Failed to replace Swipers with [Leyla, Caner, Ebru] ({n_l}, {n_a}, {n_r})")

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
    members = build_team_members(is_dist=is_dist)
    bigups_node = build_flight_bigups_node(is_dist=is_dist)
    cta_sub_html = build_about_cta_subheading_tr(is_dist=is_dist)
    out_parts = []
    pos = 0
    rec12_ok = False
    rec3c_ok = False
    rec92_ok = False

    for match in PUSH_RE.finditer(tail):
        out_parts.append(tail[pos : match.start()])
        raw_str = json.loads(match.group(1))
        if "$L3b" in raw_str or "3c:" in raw_str or "92:" in raw_str:
            records = parse_flight_stream(raw_str)
            changed = False
            for rec in records:
                kind, key, val = rec
                if kind == "line" and key == "12":
                    ast = json.loads(val)
                    sections = ast[2][3]["children"]
                    sections[6] = bigups_node
                    team_sec = sections[7]
                    team_sec[3]["data"]["team"] = members
                    rec[2] = json.dumps(ast, ensure_ascii=False, separators=(",", ":"))
                    rec12_ok = True
                    changed = True
                elif kind == "line" and key == "3c":
                    rec[2] = json.dumps(members, ensure_ascii=False, separators=(",", ":"))
                    rec3c_ok = True
                    changed = True
                elif kind == "line" and key == "92":
                    ast92 = json.loads(val)
                    right_children = ast92[3]["children"][1][3]["children"][3]["children"][1][3]["children"][3]["children"]
                    right_children[0][3]["dangerouslySetInnerHTML"]["__html"] = cta_sub_html
                    rec[2] = json.dumps(ast92, ensure_ascii=False, separators=(",", ":"))
                    rec92_ok = True
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
    if not rec12_ok or not rec3c_ok or not rec92_ok:
        raise RuntimeError(
            f"Failed to update Flight records in {fp}: rec12={rec12_ok}, rec3c={rec3c_ok}, rec92={rec92_ok}"
        )

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
    print(f"[ABOUT TEAM] Updated {count} TR Hakkımızda files with Leyla, Caner & Ebru")
    return count


if __name__ == "__main__":
    update_about_team_leyla_tr()
