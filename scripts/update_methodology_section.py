import pathlib

ROOT = pathlib.Path("/home/antigravity/Roasist/roasist-web")

TARGET_FILES = [
    "public/kota-roasist-local.html",
    "public/onizleme.html",
    "dist/index.html",
    "dist/partner.html",
    "dist/onizleme.html",
    "dist/roasist.html",
    "dist/kota.html",
    "dist/ust-bolum.html",
    "dist/bolum-2.html",
    "dist/bolum-3.html",
    "dist/bolum-4.html",
]

PAGES_BASE = "https://roasist.github.io/roasist-web/images/methodology"

REPLACEMENTS = [
    # Slide 1 ("Önce veri ve strateji.") — Custom Interactive FigJam Strategy Board Video & Poster
    (
        r'\"media\":{\"mediaItemUrl\":\"https://kota-content.b-cdn.net/app/uploads/2026/07/Strategy-Firstv2-compressed.mp4\",\"mimeType\":\"video/mp4\"},\"image\":{\"mediaItemUrl\":\"https://kota-content.b-cdn.net/app/uploads/2026/07/strategy-first.jpg\"},\"title\":\"Önce veri ve strateji.\"',
        rf'\"media\":{{\"mediaItemUrl\":\"{PAGES_BASE}/01-veri-ve-strateji.mp4\",\"mimeType\":\"video/mp4\"}},\"image\":{{\"mediaItemUrl\":\"{PAGES_BASE}/01-veri-ve-strateji.jpg\"}},\"title\":\"Önce veri ve strateji.\"',
    ),
    (
        r'\"media\":{\"mediaItemUrl\":\"https://cdn.jsdelivr.net/gh/Roasist/roasist-web@7ed44a2dd6acce892090ef487c9b1d9e76008128/public/images/methodology/01-veri-ve-strateji.mp4\",\"mimeType\":\"video/mp4\"},\"image\":{\"mediaItemUrl\":\"https://cdn.jsdelivr.net/gh/Roasist/roasist-web@7ed44a2dd6acce892090ef487c9b1d9e76008128/public/images/methodology/01-veri-ve-strateji.jpg\"},\"title\":\"Önce veri ve strateji.\"',
        rf'\"media\":{{\"mediaItemUrl\":\"{PAGES_BASE}/01-veri-ve-strateji.mp4\",\"mimeType\":\"video/mp4\"}},\"image\":{{\"mediaItemUrl\":\"{PAGES_BASE}/01-veri-ve-strateji.jpg\"}},\"title\":\"Önce veri ve strateji.\"',
    ),
]


def main():
    for rel in TARGET_FILES:
        p = ROOT / rel
        if not p.exists():
            print(f"SKIP (not found): {rel}")
            continue
        html = p.read_text(encoding="utf-8")

        # Protect byte-counted T712 JSON-LD block
        t712_start = html.find("28:T712,")
        t712_end = html.find("2b:T8f6,", t712_start) if t712_start != -1 else -1
        protected = None
        if t712_start != -1 and t712_end != -1:
            protected = html[t712_start:t712_end]
            html = html[:t712_start] + "__PROTECTED_T712_BLOCK__" + html[t712_end:]

        changed = 0
        for old, new in REPLACEMENTS:
            if old in html:
                html = html.replace(old, new)
                changed += 1

        if protected is not None:
            html = html.replace("__PROTECTED_T712_BLOCK__", protected)

        p.write_text(html, encoding="utf-8")
        print(f"Updated {rel} ({changed} replacement groups applied)")


if __name__ == "__main__":
    main()
