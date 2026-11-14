import pathlib
import re

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

TRUE_COLOR_STYLE = """<style data-roasist-true-video-colors>
/* Disable legacy KOTA pink->purple hue-rotate & color-wash overlays on custom Roasist videos */
html body .ServiceMedia_mediaContainer__WGgZa video,
html body .ServiceMedia_mediaContainer__WGgZa img,
html body section .ServiceMedia_mediaContainer__WGgZa video,
html body .CarouselSlides_carouselMedia__aqYWx video[src*="roasist"],
html body .CarouselSlides_carouselMedia__aqYWx video:has(source[src*="roasist"]),
html body .CarouselSlides_carouselMedia__aqYWx img[src*="roasist"],
html body section .CarouselSlides_carouselMedia__aqYWx video:has(source[src*="roasist"]),
html body #carousel .swiper-slide:nth-child(1) .CarouselSlides_carouselMedia__aqYWx video,
html body #carousel .swiper-slide:nth-child(2) .CarouselSlides_carouselMedia__aqYWx video {
  filter: none !important;
  -webkit-filter: none !important;
}
html body .ServiceMedia_mediaContainer__WGgZa::after,
html body .CarouselSlides_carouselMedia__aqYWx:has(source[src*="roasist"])::after,
html body .CarouselSlides_carouselMedia__aqYWx:has(video[src*="roasist"])::after,
html body .CarouselSlides_carouselMedia__aqYWx:has(img[src*="roasist"])::after,
html body #carousel .swiper-slide:nth-child(1) .CarouselSlides_carouselMedia__aqYWx::after,
html body #carousel .swiper-slide:nth-child(2) .CarouselSlides_carouselMedia__aqYWx::after {
  display: none !important;
  content: none !important;
  background: none !important;
  opacity: 0 !important;
}
</style>"""

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
    # Slide 2 ("Yaratıcı ve cesur fikir.") — Custom 3D Particle Sphere, Tilted Bento Grid, Roasist Identity (#7601FF) & Client Creative Deck
    (
        r'\"media\":{\"mediaItemUrl\":\"https://kota-content.b-cdn.net/app/uploads/2026/07/Find-The-Bold-Idea-compressed.mp4\",\"mimeType\":\"video/mp4\"},\"image\":{\"mediaItemUrl\":\"https://kota-content.b-cdn.net/app/uploads/2026/07/find-the-bold-idea.jpg\"},\"title\":\"Yaratıcı ve cesur fikir.\"',
        rf'\"media\":{{\"mediaItemUrl\":\"{PAGES_BASE}/02-yaratici-ve-cesur-fikir.mp4?v=2\",\"mimeType\":\"video/mp4\"}},\"image\":{{\"mediaItemUrl\":\"{PAGES_BASE}/02-yaratici-ve-cesur-fikir.jpg?v=2\"}},\"title\":\"Yaratıcı ve cesur fikir.\"',
    ),
    (
        rf'\"media\":{{\"mediaItemUrl\":\"{PAGES_BASE}/02-yaratici-ve-cesur-fikir.mp4\",\"mimeType\":\"video/mp4\"}},\"image\":{{\"mediaItemUrl\":\"{PAGES_BASE}/02-yaratici-ve-cesur-fikir.jpg\"}},\"title\":\"Yaratıcı ve cesur fikir.\"',
        rf'\"media\":{{\"mediaItemUrl\":\"{PAGES_BASE}/02-yaratici-ve-cesur-fikir.mp4?v=2\",\"mimeType\":\"video/mp4\"}},\"image\":{{\"mediaItemUrl\":\"{PAGES_BASE}/02-yaratici-ve-cesur-fikir.jpg?v=2\"}},\"title\":\"Yaratıcı ve cesur fikir.\"',
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

        # Inject or update <style data-roasist-true-video-colors> right before </head>
        html_no_old_style = re.sub(
            r"<style data-roasist-true-video-colors>.*?</style>",
            "",
            html,
            flags=re.DOTALL,
        )
        if "</head>" in html_no_old_style:
            html = html_no_old_style.replace("</head>", TRUE_COLOR_STYLE + "</head>", 1)
            changed += 1

        if protected is not None:
            html = html.replace("__PROTECTED_T712_BLOCK__", protected)

        p.write_text(html, encoding="utf-8")
        print(f"Updated {rel} ({changed} replacement groups applied)")


if __name__ == "__main__":
    main()
