#!/usr/bin/env python3
"""
Pre-Launch Step 2:
1. Removes all remaining KOTA / foreign client text leftovers across SSR & Flight streams
   (Hakkımızda 'Our Team' -> 'Ekibimiz', KOTA bios, Wogan/Penhaligon/Jamie Oliver, etc.).
2. Replaces all remaining `https://kota-content.b-cdn.net/...` external CDN URLs across
   every HTML page (in both public/ and dist/) with fast, local Roasist assets in
   `/images/...` using Flight-stream-safe record serialization (`T<hex>,` byte exact).
"""
import glob
import json
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

from update_about_page import parse_flight_stream, serialize_flight_stream
from update_tiktok_yandex_pages import extract_flight_chunks


def map_kota_cdn_url(url: str, prefix: str = "") -> str:
    low = url.lower()
    if "logo" in low or "tangerine" in low or "florence" in low or "dka" in low or "wogan" in low or "isi" in low or "pixelartworks" in low:
        rel = "/images/clients-white/ref-02.png"
    elif "geo-ai" in low or "ai-search" in low or "zero-click" in low:
        rel = "/images/kota/kota-case-seo-aeo.webp"
    elif "creative" in low or "design-with-guts" in low or "brand-trend" in low or "lovie" in low:
        rel = "/images/kota/kota-case-creative.webp"
    elif "10-tips" in low or "doelb0q" in low or "ecommerce" in low:
        rel = "/images/kota/kota-case-ecommerce.webp"
    elif "incentive" in low or "b2b" in low or "upp" in low:
        rel = "/images/kota/kota-case-b2b.webp"
    elif "results-" in low or "bg" in low:
        rel = "/images/case-studies/statistics-bg-black.jpg"
    elif ".mp4" in low:
        rel = "/images/services/performans-pazarlamasi.mp4"
    else:
        rel = "/images/kota/kota-case-creative.webp"
    return prefix + rel


KOTA_URL_RE = re.compile(r'https://kota-content\.b-cdn\.net/[^"\'\\\s),]+')

TEXT_CLEANUPS = [
    # Hakkımızda TR heading
    (">Our Team<", ">Ekibimiz<"),
    # Residual KOTA text inside unrendered Flight records
    ("setting up KOTA with Jonny Bradford in 2012", "building data-driven digital growth systems at Roasist"),
    ("Co-Founder of KOTA", "Growth Strategist at Roasist"),
    ("glue that holds KOTA together", "bridge across performance, creative, and engineering at Roasist"),
    ("smoothly in the KOTA studio", "smoothly across Roasist growth sprints"),
    ("At KOTA, he focuses", "At Roasist, the team focuses"),
    ("KOTA director and ex-rock and roll star", "Creative Director at Roasist"),
    ("KOTA’s ideas were fresh and exciting", "Roasist’s strategies were sharp and measurable"),
    ("what we offer here at KOTA", "what we deliver at Roasist"),
    ("new strategy with KOTA", "new growth strategy with Roasist"),
    ("Wogan Coffee", "Gekoo"),
    ("Penhaligon's", "Medistate"),
    ("Penhaligons", "Medistate"),
    ("Jamie Oliver", "Summer Homes"),
]


def clean_html_file(path: str, is_gh_pages: bool = False) -> bool:
    orig = open(path, "r", encoding="utf-8").read()
    prefix = "/roasist-web" if is_gh_pages else ""
    is_tr_about = path.endswith("hakkimizda/index.html")

    def clean_segment(seg: str, in_flight: bool = False) -> str:
        out = KOTA_URL_RE.sub(lambda m: map_kota_cdn_url(m.group(0), prefix), seg)
        for old, new in TEXT_CLEANUPS:
            if old == ">Our Team<" and not is_tr_about:
                continue
            out = out.replace(old, new)
        if is_tr_about and in_flight:
            out = out.replace('"children":"Our Team"', '"children":"Ekibimiz"')
        return out

    matches, _, full = extract_flight_chunks(orig)
    if matches and full:
        try:
            recs = parse_flight_stream(full)
            flight_dirty = False
            for rec in recs:
                new_val = clean_segment(rec[2], in_flight=True)
                if new_val != rec[2]:
                    rec[2] = new_val
                    flight_dirty = True

            out_parts = []
            last_end = 0
            new_full = serialize_flight_stream(recs) if flight_dirty else full
            for idx, m in enumerate(matches):
                out_parts.append(clean_segment(orig[last_end : m.start()], in_flight=False))
                if flight_dirty:
                    if idx == 0:
                        encoded = json.dumps(new_full, ensure_ascii=False)[1:-1].replace("</", "\\u003c/")
                        out_parts.append(m.group(1) + encoded + m.group(3))
                    else:
                        out_parts.append("")
                else:
                    out_parts.append(m.group(0))
                last_end = m.end()
            out_parts.append(clean_segment(orig[last_end:], in_flight=False))
            updated = "".join(out_parts)
        except Exception:
            # Fallback for non-Next standalone 3D HTML files
            updated = clean_segment(orig, in_flight=False)
    else:
        updated = clean_segment(orig, in_flight=False)

    if updated != orig:
        open(path, "w", encoding="utf-8").write(updated)
        return True
    return False


def main():
    for root_name, is_gh in [("public", False), ("dist", True)]:
        root_dir = os.path.join(REPO_ROOT, root_name)
        if not os.path.exists(root_dir):
            continue
        html_files = sorted(glob.glob(os.path.join(root_dir, "**", "*.html"), recursive=True))
        changed = 0
        for f in html_files:
            # Skip git internal if any
            if "/.git/" in f:
                continue
            if clean_html_file(f, is_gh_pages=is_gh):
                changed += 1
        print(f"[OK] Step 2 cleaned KOTA leftovers & localized CDN URLs across {changed}/{len(html_files)} files in {root_name}/")


if __name__ == "__main__":
    main()
