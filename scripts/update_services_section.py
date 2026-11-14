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

OLD_MAIN_TEXT = (
    "Reklam bütçenizi sadece harcamıyor, kârlı yatırıma dönüştürüyoruz. "
    "Google, Meta, TikTok, LinkedIn ve Yandex’te veri odaklı ROAS mimarisiyle satışlarınızı ölçeklendiriyoruz."
)
NEW_MAIN_TEXT = (
    "Reklam bütçenizi sadece harcamıyor, kârlı yatırıma dönüştürüyoruz. "
    "Google, Meta, TikTok, LinkedIn, Yandex ve Bing’de veri odaklı ROAS mimarisiyle satışlarınızı ölçeklendiriyoruz."
)

REPLACEMENTS = [
    # 1. Panel 1 Heading (SSR + Flight JSON)
    (
        '<h3 class="ServicesPanel_panelHeading__5Sy4s">Performans Pazarlaması &amp; ROAS</h3>',
        '<h3 class="ServicesPanel_panelHeading__5Sy4s">Performans Pazarlaması</h3>',
    ),
    (
        '<h3 class="ServicesPanel_panelHeading__5Sy4s">Performans Pazarlaması & ROAS</h3>',
        '<h3 class="ServicesPanel_panelHeading__5Sy4s">Performans Pazarlaması</h3>',
    ),
    (
        r'\"heading\":\"Büyüme Stratejisi \u0026 identity\"',
        r'\"heading\":\"Performans Pazarlaması\"',
    ),
    (
        r'\"heading\":\"Performans Pazarlaması \u0026 ROAS\"',
        r'\"heading\":\"Performans Pazarlaması\"',
    ),
    # 2. Panel 1 Tag Buttons (SSR + Flight JSON)
    (
        '<a class="ServicesPanel_tag__JYwRk" href="/hizmetler/performans-pazarlamasi/instagram-reklamlari">Meta &amp; Instagram Ads</a>',
        '<a class="ServicesPanel_tag__JYwRk" href="/hizmetler/performans-pazarlamasi/instagram-reklamlari">Meta Ads</a>',
    ),
    (
        '<a class="ServicesPanel_tag__JYwRk" href="/hizmetler/performans-pazarlamasi/instagram-reklamlari">Meta & Instagram Ads</a>',
        '<a class="ServicesPanel_tag__JYwRk" href="/hizmetler/performans-pazarlamasi/instagram-reklamlari">Meta Ads</a>',
    ),
    (
        '<a class="ServicesPanel_tag__JYwRk" href="/hizmetler/performans-pazarlamasi/tiktok-reklamlari">TikTok &amp; LinkedIn Ads</a>',
        '<a class="ServicesPanel_tag__JYwRk" href="/hizmetler/performans-pazarlamasi/tiktok-reklamlari">TikTok Ads</a>',
    ),
    (
        '<a class="ServicesPanel_tag__JYwRk" href="/hizmetler/performans-pazarlamasi/tiktok-reklamlari">TikTok & LinkedIn Ads</a>',
        '<a class="ServicesPanel_tag__JYwRk" href="/hizmetler/performans-pazarlamasi/tiktok-reklamlari">TikTok Ads</a>',
    ),
    (
        r'{\"id\":\"cG9zdDo4ODQ=\",\"slug\":\"brand-strategy\",\"title\":\"Büyüme Stratejisi\"}',
        r'{\"id\":\"cG9zdDo4ODQ=\",\"slug\":\"brand-strategy\",\"title\":\"Google Ads Yönetimi\"}',
    ),
    (
        r'{\"id\":\"cG9zdDo4ODg=\",\"slug\":\"brand-identity-design\",\"title\":\"Görsel Kimlik design\"}',
        r'{\"id\":\"cG9zdDo4ODg=\",\"slug\":\"brand-identity-design\",\"title\":\"Meta Ads\"}',
    ),
    (
        r'{\"id\":\"cG9zdDo4ODY=\",\"slug\":\"tone-of-voice\",\"title\":\"Kreatif İletişim\"}',
        r'{\"id\":\"cG9zdDo4ODY=\",\"slug\":\"tone-of-voice\",\"title\":\"TikTok Ads\"}',
    ),
    # 2b. Append "Yandex Ads" tag button right after "TikTok Ads" (SSR + Flight JSON)
    (
        '<a class="ServicesPanel_tag__JYwRk" href="/hizmetler/performans-pazarlamasi/tiktok-reklamlari">TikTok Ads</a></div>',
        '<a class="ServicesPanel_tag__JYwRk" href="/hizmetler/performans-pazarlamasi/tiktok-reklamlari">TikTok Ads</a>'
        '<a class="ServicesPanel_tag__JYwRk" href="/hizmetler/performans-pazarlamasi/yandex-reklamlari">Yandex Ads</a></div>',
    ),
    (
        r'{\"id\":\"cG9zdDo4ODY=\",\"slug\":\"tone-of-voice\",\"title\":\"TikTok Ads\"}]',
        r'{\"id\":\"cG9zdDo4ODY=\",\"slug\":\"tone-of-voice\",\"title\":\"TikTok Ads\"},'
        r'{\"id\":\"cG9zdDo4ODc=\",\"slug\":\"yandex-reklamlari\",\"title\":\"Yandex Ads\"}]',
    ),
    # 3. Panel 1 Description with "Bing" added (SSR + Flight JSON)
    (OLD_MAIN_TEXT, NEW_MAIN_TEXT),
    # 4. Panel 1 Custom Orbital Client Video & Poster (Flight JSON)
    (
        r'\"image\":{\"altText\":\"\",\"srcSet\":\"https://kota-content.b-cdn.net/app/uploads/2023/10/wogan-1.jpg 1086w, https://kota-content.b-cdn.net/app/uploads/2023/10/wogan-1-479x500.jpg 479w, https://kota-content.b-cdn.net/app/uploads/2023/10/wogan-1-768x802.jpg 768w\",\"sourceUrl\":\"https://kota-content.b-cdn.net/app/uploads/2023/10/wogan-1.jpg\",\"mediaDetails\":{\"width\":1086,\"height\":1134}},\"video\":{\"mediaItemUrl\":\"https://kota-content.b-cdn.net/app/uploads/2026/07/Branding-1.mp4\"}',
        r'\"image\":{\"altText\":\"Performans Pazarlaması\",\"srcSet\":\"https://cdn.jsdelivr.net/gh/Roasist/roasist-web@eb064304d8b3f3053263e5f79b3b5a3da883d011/public/images/services/performans-pazarlamasi.jpg 1080w\",\"sourceUrl\":\"https://cdn.jsdelivr.net/gh/Roasist/roasist-web@eb064304d8b3f3053263e5f79b3b5a3da883d011/public/images/services/performans-pazarlamasi.jpg\",\"mediaDetails\":{\"width\":1080,\"height\":1080}},\"video\":{\"mediaItemUrl\":\"https://cdn.jsdelivr.net/gh/Roasist/roasist-web@eb064304d8b3f3053263e5f79b3b5a3da883d011/public/images/services/performans-pazarlamasi.mp4\"}',
    ),
    # 5. Panel 2 Custom 3D Website Gallery Video & Poster (Flight JSON)
    (
        r'\"image\":{\"altText\":\"\",\"srcSet\":\"https://kota-content.b-cdn.net/app/uploads/2023/10/Web-design-Development.jpg 1086w, https://kota-content.b-cdn.net/app/uploads/2023/10/Web-design-Development-479x500.jpg 479w, https://kota-content.b-cdn.net/app/uploads/2023/10/Web-design-Development-768x802.jpg 768w\",\"sourceUrl\":\"https://kota-content.b-cdn.net/app/uploads/2023/10/Web-design-Development.jpg\",\"mediaDetails\":{\"width\":1086,\"height\":1134}},\"video\":{\"mediaItemUrl\":\"https://kota-content.b-cdn.net/app/uploads/2026/07/Websites-2026-1.mp4\"}',
        r'\"image\":{\"altText\":\"Web Tasarım ve Kreatif Stüdyo\",\"srcSet\":\"https://cdn.jsdelivr.net/gh/Roasist/roasist-web@097860ece7c2d31384c3b8ca3013b147c8dbb1f7/public/images/services/web-tasarim.jpg 1080w\",\"sourceUrl\":\"https://cdn.jsdelivr.net/gh/Roasist/roasist-web@097860ece7c2d31384c3b8ca3013b147c8dbb1f7/public/images/services/web-tasarim.jpg\",\"mediaDetails\":{\"width\":1080,\"height\":1080}},\"video\":{\"mediaItemUrl\":\"https://cdn.jsdelivr.net/gh/Roasist/roasist-web@097860ece7c2d31384c3b8ca3013b147c8dbb1f7/public/images/services/web-tasarim.mp4\"}',
    ),
    # 6. Panel 3 Custom 3D SEO & AEO Ecosystem Video & Poster (Flight JSON)
    (
        r'\"image\":{\"altText\":\"\",\"srcSet\":\"https://kota-content.b-cdn.net/app/uploads/2023/10/floan.jpg 1086w, https://kota-content.b-cdn.net/app/uploads/2023/10/floan-479x500.jpg 479w, https://kota-content.b-cdn.net/app/uploads/2023/10/floan-768x802.jpg 768w\",\"sourceUrl\":\"https://kota-content.b-cdn.net/app/uploads/2023/10/floan.jpg\",\"mediaDetails\":{\"width\":1086,\"height\":1134}},\"video\":{\"mediaItemUrl\":\"https://kota-content.b-cdn.net/app/uploads/2023/11/Growth-Marketing.mp4\"}',
        r'\"image\":{\"altText\":\"SEO, AEO ve 360 Dijital Büyüme\",\"srcSet\":\"https://cdn.jsdelivr.net/gh/Roasist/roasist-web@c2b0d79ee14a72f519427282ff0d82ee15ea68a1/public/images/services/seo-aeo-buyume.jpg 1080w\",\"sourceUrl\":\"https://cdn.jsdelivr.net/gh/Roasist/roasist-web@c2b0d79ee14a72f519427282ff0d82ee15ea68a1/public/images/services/seo-aeo-buyume.jpg\",\"mediaDetails\":{\"width\":1080,\"height\":1080}},\"video\":{\"mediaItemUrl\":\"https://cdn.jsdelivr.net/gh/Roasist/roasist-web@c2b0d79ee14a72f519427282ff0d82ee15ea68a1/public/images/services/seo-aeo-buyume.mp4\"}',
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
