"""Rebuild the Roasist reference grid on /referanslar.

The page is a KOTA-clone (Next.js app router) whose project list is rendered
client side from the flight payload. This script:

  posters : generate a 1440x810 poster per reference from its logo
            -> public/images/references/<slug>.jpg   (commit these first)
  patch   : replace sectors / services / projects in dist/referanslar/index.html
            and tweak the work-page chunk (no /work/<slug> links, TR filter labels)

Usage:
  python3 scripts/build_references_page.py posters
  python3 scripts/build_references_page.py patch [<git sha serving public/images/references>]
"""
import glob
import json
import pathlib
import re
import subprocess
import sys

from PIL import Image, ImageChops

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import references_data as R  # noqa: E402
import update_work_section as W  # noqa: E402

CLIENTS = ROOT / "public/images/clients"
POSTERS = ROOT / "public/images/references"
PAGE = ROOT / "dist/referanslar/index.html"
CHUNK_GLOB = str(ROOT / "dist/_next/static/chunks/app/work/page-*.js")
CDN = "https://cdn.jsdelivr.net/gh/Roasist/roasist-web@{sha}/public/images/references"

W_, H_ = 1440, 810
BG = (243, 242, 247)


def make_poster(logo_path: pathlib.Path, out: pathlib.Path):
    logo = Image.open(logo_path).convert("RGBA")
    bbox = logo.getchannel("A").point(lambda a: 255 if a > 8 else 0).getbbox()
    if bbox:
        logo = logo.crop(bbox)
    max_w, max_h = int(W_ * 0.5), int(H_ * 0.34)
    scale = min(max_w / logo.width, max_h / logo.height)
    logo = logo.resize((max(1, int(logo.width * scale)), max(1, int(logo.height * scale))), Image.LANCZOS)
    canvas = Image.new("RGB", (W_, H_), BG)
    canvas.paste(logo, ((W_ - logo.width) // 2, (H_ - logo.height) // 2), logo)
    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out, quality=88, optimize=True)


def cmd_posters():
    for slug, title, logo, _sector, video in R.REFERENCES:
        if video:  # poster is a frame of the video, keep it
            continue
        make_poster(CLIENTS / logo, POSTERS / f"{slug}.jpg")
    print(f"posters: {len(R.REFERENCES)} -> {POSTERS}")


def edge(slug, name):
    return {"node": {"slug": slug, "name": name}}


def project_node(db_id, title, slug, year, img, video, heading, services, sector):
    return {
        "node": {
            "title": title,
            "slug": slug,
            "databaseId": db_id,
            "singleProject": {
                "projectDetails": {
                    "showOnlyOnFilter": None,
                    "yearCompleted": year,
                    "featuredImage": {
                        "altText": title,
                        "srcSet": f"{img} 1440w",
                        "sourceUrl": img,
                        "mediaDetails": {"width": 1440, "height": 810},
                    },
                    "featuredVideo": {"mediaItemUrl": video} if video else None,
                },
                "hero": {"heading": heading},
            },
            "taxonomyServices": {"edges": [edge(re.sub(r"\W+", "-", s.lower()), s) for s in services]},
            "taxonomySectors": {"edges": [edge(sector, R.SECTORS[sector])] if sector else []},
        }
    }


def build_payload(sha):
    base = CDN.format(sha=sha)
    projects = []
    db_id = 9000
    # 1) featured projects with videos (same data as the homepage cards)
    for p in W.PROJECTS:
        db_id += 1
        projects.append(
            project_node(
                db_id, p["name"], re.sub(r"\W+", "-", p["name"].lower()), p["year"],
                p["img_src"], p.get("video"), p["heading"], p["tags"],
                R.FEATURED_SECTORS.get(p["name"]),
            )
        )
    # 2) the rest of the references; curated order (max 2 video-less cards consecutively)
    refs = R.REFERENCES
    for slug, title, _logo, sector, video in refs:
        db_id += 1
        d = R.DETAILS.get(slug, {})
        vid = f"{base}/{video}" if video else None
        projects.append(project_node(
            db_id, title, slug, d.get("year"), f"{base}/{slug}.jpg", vid,
            d.get("heading"), d.get("services", []), sector,
        ))

    counts = {}
    for pr in projects:
        for e in pr["node"]["taxonomySectors"]["edges"]:
            counts[e["node"]["slug"]] = counts.get(e["node"]["slug"], 0) + 1
    sectors = [
        {"node": {"name": label, "slug": s, "count": counts[s]}}
        for s, label in R.SECTORS.items() if counts.get(s)
    ]
    return sectors, projects


def esc(obj):
    """JSON -> text as it appears inside the flight JS string literal."""
    s = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
    return s.replace("\\", "\\\\").replace('"', '\\"')


def array_end(s, start):
    depth, i, instr = 0, start, False
    while i < len(s):
        if s.startswith('\\"', i):
            instr = not instr
            i += 2
            continue
        if not instr:
            if s[i] == "[":
                depth += 1
            elif s[i] == "]":
                depth -= 1
                if depth == 0:
                    return i
        i += 1
    raise RuntimeError("unbalanced array")


def replace_array(html, key, value):
    marker = f'\\"{key}\\":['
    a = html.find(marker)
    if a < 0:
        raise RuntimeError(f"{key} not found")
    start = a + len(marker) - 1
    end = array_end(html, start)
    return html[:start] + esc(value) + html[end + 1:], end - start


def patch_chunk():
    files = glob.glob(CHUNK_GLOB)
    if not files:
        raise RuntimeError("work chunk not found")
    p = pathlib.Path(files[0])
    t = p.read_text(encoding="utf-8")
    o = t
    # reference cards have no detail page: render a plain element instead of a /work/<slug> link
    t = t.replace(
        's.default,{className:(0,a.cn)(l().project,l()[w]),href:"/work/".concat(null==j?void 0:j.slug),"data-animation"',
        '"div",{className:(0,a.cn)(l().project,l()[w]),"data-animation"',
    )
    t = t.replace('children:["Sectors",', 'children:["Sektörler",')
    # drop the Services filter button (we only have sector data)
    m = re.search(r'\(0,n\.jsxs\)\("button",\{className:\(0,a\.cn\)\(s\(\)\.trigger,u\?s\(\)\.active:""\),onClick:\(\)=>\{d\(!u\),o&&c\(!1\)\},children:\["Services",', t)
    if m:
        i, depth = m.start(), 0
        j = i + len("(0,n.jsxs)")  # match the call's argument list, not the callee parens
        while True:
            c = t[j]
            if c == "(":
                depth += 1
            elif c == ")":
                depth -= 1
                if depth == 0:
                    break
            elif c in "\"'":
                q = c
                j += 1
                while t[j] != q:
                    j += 2 if t[j] == "\\" else 1
            j += 1
        t = t[:i] + "null" + t[j + 1:]
    if t != o:
        p.write_text(t, encoding="utf-8")
    print("chunk patched:", p.name, "changed" if t != o else "already patched")


def strip_hero_video(html: str) -> str:
    # Safely hide the hero video element and reduce excessive vertical spacing
    # caused by removing the video (which previously stretched the hero to 100svh).
    style = (
        '<style id="hide-hero-video">'
        '.Hero_video__rzcbe{display:none!important;visibility:hidden!important;width:0!important;height:0!important;pointer-events:none!important;}'
        '.Hero_hero__Oyf4n{height:auto!important;min-height:0!important;max-height:none!important;padding-bottom:3.5rem!important;}'
        '.Hero_top__RRkYH{align-self:auto!important;}'
        '.Hero_hero__Oyf4n h2{margin-top:0.5rem!important;margin-bottom:2.5rem!important;}'
        '.Hero_bottom__ktiOH{align-self:auto!important;margin-top:1rem!important;}'
        '@media (max-width:768px){'
        '.Hero_hero__Oyf4n .container{height:auto!important;padding-top:6rem!important;padding-bottom:2rem!important;}'
        '.Hero_bottom__ktiOH{flex:none!important;margin-top:1.5rem!important;}'
        '}'
        '</style>'
    )
    if '<style id="hide-hero-video">' in html:
        html = re.sub(r'<style id="hide-hero-video">.*?</style>', style, html, flags=re.DOTALL)
    else:
        html = html.replace("</head>", style + "</head>")
    return html


def cmd_patch(sha):
    html = PAGE.read_text(encoding="utf-8")
    sectors, projects = build_payload(sha)
    html, _ = replace_array(html, "projects", projects)
    html, _ = replace_array(html, "sectors", sectors)
    html, _ = replace_array(html, "services", [])
    html = strip_hero_video(html)
    PAGE.write_text(html, encoding="utf-8")
    patch_chunk()
    print(f"patched {PAGE.relative_to(ROOT)}: {len(projects)} projects, {len(sectors)} sectors (hero video stripped)")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "posters":
        cmd_posters()
    elif mode == "patch":
        sha = sys.argv[2] if len(sys.argv) > 2 else subprocess.check_output(
            ["git", "log", "-1", "--format=%H", "--", "public/images/references"], cwd=ROOT, text=True).strip()
        cmd_patch(sha)
    else:
        print(__doc__)
