#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Replaces the `Vizyon Misyon` heading and circular `mission.jpg` image inside
`<section class="Mission_mission__8wC67">` on the Hakkımızda (`/hakkimizda/`) page
with the Sigmund Freud quote block (matching legacy roasist.com/hakkimizda/ layout),
and removes the duplicate inline quote sentence from `Mission_mainText__ejHIS`.

Maintains 100% parity between SSR HTML and Next.js React Flight AST (`self.__next_f.push`).
"""

import json
import os
import re
import sys

ROOT = "/home/antigravity/Roasist/roasist-web"
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from apply_phase1_cleanup import PUSH_RE, find_node_by_class, rewrite_flight_in_html  # noqa: E402

QUOTE_ICON_PATH_D = (
    "M23.6 5.2C14.8 9.4 9.6 15.8 8.8 23.4c1.5-.8 3.3-1.2 5.2-1.2 6.4 0 11.4 5 11.4 11.6 "
    "0 6.7-5.3 12-12 12C6 45.8.8 40 .8 31.4.8 17.8 9.2 6.8 21.4 1.2l2.2 4zm34 0C48.8 9.4 "
    "43.6 15.8 42.8 23.4c1.5-.8 3.3-1.2 5.2-1.2 6.4 0 11.4 5 11.4 11.6 0 6.7-5.3 12-12 "
    "12-7.4 0-12.6-5.8-12.6-14.4 0-13.6 8.4-24.6 20.6-30.2l2.2 4z"
)

FREUD_QUOTE_TR = (
    "Çoğu insan gerçekte özgürlük istemez, çünkü özgürlük sorumluluk gerektirir ve "
    "çoğu insan sorumluluktan korkar."
)
FREUD_AUTHOR = "Sigmund Freud"

NEW_MISSION_MAIN_HTML_TR = (
    "<p>Özgürlüğü ve sorumluluğu bir arada benimsiyor; çalıştığımız her markanın "
    "dijital büyüme hedeflerini kendi işimiz gibi sahipleniyoruz.</p>\n"
    "<p>Roasist, dijital pazarlama sektöründe özelleştirilmiş ve yenilikçi yaklaşımıyla "
    "öne çıkan bir dijital pazarlama ajansıdır. Müşterilerimize en güçlü sonuçları sunmak "
    "için kanıtlanmış pazarlama prensiplerini modern fikirler ve veri analitiğiyle "
    "birleştiriyor; hızla değişen dijital dünyayı yakından takip ederek araştırmaya ve "
    "kendimizi geliştirmeye sürekli yatırım yapıyoruz.</p>\n"
)


def build_ssr_quote_block() -> str:
    return (
        '<blockquote class="roasist-mission-quote">'
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 48" aria-hidden="true" class="roasist-mission-quote__icon">'
        f'<path fill="currentColor" d="{QUOTE_ICON_PATH_D}"></path></svg>'
        f'<p class="roasist-mission-quote__text">{FREUD_QUOTE_TR}</p>'
        f'<cite class="roasist-mission-quote__author">{FREUD_AUTHOR}</cite>'
        "</blockquote>"
    )


def build_flight_quote_node() -> list:
    return [
        "$",
        "blockquote",
        None,
        {
            "className": "roasist-mission-quote",
            "children": [
                [
                    "$",
                    "svg",
                    None,
                    {
                        "xmlns": "http://www.w3.org/2000/svg",
                        "viewBox": "0 0 60 48",
                        "aria-hidden": "true",
                        "className": "roasist-mission-quote__icon",
                        "children": [
                            "$",
                            "path",
                            None,
                            {
                                "fill": "currentColor",
                                "d": QUOTE_ICON_PATH_D,
                            },
                        ],
                    },
                ],
                [
                    "$",
                    "p",
                    None,
                    {
                        "className": "roasist-mission-quote__text",
                        "children": FREUD_QUOTE_TR,
                    },
                ],
                [
                    "$",
                    "cite",
                    None,
                    {
                        "className": "roasist-mission-quote__author",
                        "children": FREUD_AUTHOR,
                    },
                ],
            ],
        },
    ]


def update_single_about_tr(fp: str) -> bool:
    with open(fp, "r", encoding="utf-8") as f:
        html = f.read()

    pushes = list(PUSH_RE.finditer(html))
    if not pushes:
        raise RuntimeError(f"No Flight stream found in {fp}")

    ssr = html[: pushes[0].start()]
    tail = html[pushes[0].start() :]

    # Remove any preload tag referencing mission.jpg in <head>
    ssr = re.sub(r'<link[^>]+mission[^>]*/?>', "", ssr)

    # Replace Mission_heading + Mission_image (or existing roasist-mission-quote) inside Mission_mission__8wC67
    quote_ssr = build_ssr_quote_block()
    ssr_updated, n_top = re.subn(
        r'(<section class="Mission_mission__8wC67"><div class="container">)'
        r'(?:<h2 class="Mission_heading__Z0yjM">.*?</h2><figure class="Mission_image__gbyeM">.*?</figure>|<blockquote class="roasist-mission-quote">.*?</blockquote>)',
        lambda m: m.group(1) + quote_ssr,
        ssr,
        count=1,
        flags=re.S,
    )
    if n_top != 1:
        raise RuntimeError(f"Failed to replace Mission top block in SSR of {fp}")

    # Update Mission_mainText__ejHIS inner HTML in SSR
    ssr_updated, n_body = re.subn(
        r'(<div class="Mission_mainText__ejHIS"><span class="FadeInUp_container___uxva" data-fill="false"><div>).*?(</div></span></div>)',
        lambda m: m.group(1) + NEW_MISSION_MAIN_HTML_TR + m.group(2),
        ssr_updated,
        count=1,
        flags=re.S,
    )
    if n_body != 1:
        raise RuntimeError(f"Failed to update Mission_mainText__ejHIS in SSR of {fp}")

    flight_updated_ok = False

    def mut(records):
        nonlocal flight_updated_ok
        changed = False
        for rec in records:
            if rec[0] != "line":
                continue
            payload = rec[2]
            if not payload or payload[0] not in "[{" or "Mission_mission__8wC67" not in payload:
                continue
            ast = json.loads(payload)
            mission_sec = find_node_by_class(ast, "Mission_mission__8wC67")
            if not mission_sec:
                continue
            container_node = mission_sec[3]["children"]
            c_children = container_node[3]["children"]

            # Filter out Mission_heading__Z0yjM, Mission_image__gbyeM, or previous roasist-mission-quote
            kept = []
            for item in c_children:
                if (
                    isinstance(item, list)
                    and len(item) >= 4
                    and isinstance(item[3], dict)
                    and item[3].get("className") in ("Mission_heading__Z0yjM", "Mission_image__gbyeM", "roasist-mission-quote")
                ):
                    continue
                kept.append(item)

            # Update Mission_mainText__ejHIS in kept
            main_text_node = find_node_by_class(kept, "Mission_mainText__ejHIS")
            if not main_text_node:
                raise RuntimeError(f"Could not find Mission_mainText__ejHIS in Flight AST of {fp}")
            main_text_node[3]["children"][3]["children"][3]["dangerouslySetInnerHTML"]["__html"] = NEW_MISSION_MAIN_HTML_TR

            container_node[3]["children"] = [build_flight_quote_node(), *kept]
            rec[2] = json.dumps(ast, ensure_ascii=False, separators=(",", ":"))
            flight_updated_ok = True
            changed = True
        return changed

    new_html = ssr_updated + rewrite_flight_in_html(tail, mut)
    if not flight_updated_ok:
        raise RuntimeError(f"Failed to update Flight AST Mission_mission__8wC67 in {fp}")
    if "Mission_heading__Z0yjM" in new_html or "Mission_image__gbyeM" in new_html:
        raise RuntimeError(f"Leftover Mission heading/image in {fp}")

    if new_html != html:
        with open(fp, "w", encoding="utf-8") as f:
            f.write(new_html)
        return True
    return False


def update_about_mission_quote_tr() -> int:
    count = 0
    for base_name in ("public", "dist"):
        fp = os.path.join(ROOT, base_name, "hakkimizda", "index.html")
        if update_single_about_tr(fp):
            count += 1
    print(f"[ABOUT MISSION QUOTE] Updated {count} TR Hakkımızda files (public + dist)")
    return count


if __name__ == "__main__":
    update_about_mission_quote_tr()
