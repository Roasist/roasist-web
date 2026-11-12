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
    # 3. Panel 1 Description with "Bing" added (SSR + Flight JSON)
    (OLD_MAIN_TEXT, NEW_MAIN_TEXT),
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
