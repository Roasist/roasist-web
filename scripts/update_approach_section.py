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

# New authentic Roasist copy for Approach section (SSR + Flight JSON synchronized, zero \n\n gaps)
NEW_APPROACH_H2 = "Trafiği yüksek dönüşüme, reklam yatırımını kârlı ciroya dönüştürüyoruz."
NEW_APPROACH_P = (
    "Büyümek isteyen markaların tahmine değil, ölçülebilir performansa ihtiyacı vardır. "
    "Roasist; reklam yönetimi, SEO ve dönüşüm odaklı tasarımı tek stratejide birleştirir."
)

CARD_1_H3 = "Veri Stratejisi"
CARD_1_P = "Pazar, rakip ve arama niyeti analizleriyle bütçenizi en kârlı kanallara odaklayan büyüme planı."

CARD_2_H3 = "Dönüşüm Tasarımı"
CARD_2_P = "Dikkat çeken reklam kreatifleri ve ziyaretçiyi müşteriye dönüştüren hızlı, ikna edici web deneyimi."

CARD_3_H3 = "Yüksek ROAS"
CARD_3_P = "Google, Meta, TikTok, Yandex ve SEO’da sürdürülebilir ciro üreten performans sistemleri."

REPLACEMENTS = [
    # 1. Approach Top Row: Heading (SSR + Flight JSON)
    (
        "İddialı markaların \n\nnasıl görüldüğünü, güvenildiğini \n\nve büyüdüğünü şekillendiriyoruz.",
        NEW_APPROACH_H2,
    ),
    (
        r"Shaping how global \\r\\nbrands are seen, trusted, \\r\\nand remembered.",
        NEW_APPROACH_H2,
    ),
    # 2. Approach Top Row: Right Paragraph (SSR + Flight JSON)
    (
        "Her marka için hızlı ölçeklenme, yeni pazarlar veya yüksek ROAS hedefleri gibi kırılma anları vardır. Bizim işimiz tam orada başlar.",
        NEW_APPROACH_P,
    ),
    # 3. Card 01 (SSR + Flight JSON)
    (">Stratejik Netlik<", f">{CARD_1_H3}<"),
    (r'\"children\":\"Stratejik Netlik\"', rf'\"children\":\"{CARD_1_H3}\"'),
    (
        "Veri ve pazar analizleriyle markanızı doğru konumlandıran net kararlar.",
        CARD_1_P,
    ),
    # 4. Card 02 (SSR + Flight JSON)
    (">Kreatif Ustalık<", f">{CARD_2_H3}<"),
    (r'\"children\":\"Kreatif Ustalık\"', rf'\"children\":\"{CARD_2_H3}\"'),
    (
        "Fark yaratan, dönüşüm odaklı ve estetik açıdan kusursuz dijital tasarım.",
        CARD_2_P,
    ),
    # 5. Card 03 (SSR + Flight JSON)
    (">Ticari İvme &amp; ROAS<", f">{CARD_3_H3}<"),
    (">Ticari İvme & ROAS<", f">{CARD_3_H3}<"),
    (r'\"children\":\"Ticari İvme \u0026 ROAS\"', rf'\"children\":\"{CARD_3_H3}\"'),
    (r'\"children\":\"Ticari İvme & ROAS\"', rf'\"children\":\"{CARD_3_H3}\"'),
    (
        "Sürdürülebilir ciro ve \n\nölçeklenebilir büyüme sistemleri.",
        CARD_3_P,
    ),
    (
        r"Scalable systems with \\r\\ngrowth in mind.",
        CARD_3_P,
    ),
    (
        "Google, Meta, TikTok, Yandex ve SEO’da sürdürülebilir ciro üreten ölçeklenebilir performans yönetimi.",
        CARD_3_P,
    ),
    # 6. Fix Services heading Turkish dotted İ & Flight JSON sync
    (
        'ServicesHeading_bottom__K8yXu">Hizmetler<',
        'ServicesHeading_bottom__K8yXu">HİZMETLER<',
    ),
    (
        r'ServicesHeading_bottom__K8yXu\",\"children\":\"Services\"',
        r'ServicesHeading_bottom__K8yXu\",\"children\":\"HİZMETLER\"',
    ),
    # 7. Fix Carousel \n\n double-newline blank gaps in SSR + English \r\n remnants in Flight JSON
    (
        "Adım adım büyüme \n\nmetodolojimiz.",
        "Adım adım büyüme metodolojimiz.",
    ),
    (
        r"Our brand-to-build \\r\\nframework.",
        "Adım adım büyüme metodolojimiz.",
    ),
    ("Önce veri ve \n\nstrateji.", "Önce veri ve strateji."),
    ("Önce veri ve \n\nstrateji", "Önce veri ve strateji"),
    (r"Strategy first. \\r\\nAlways.", "Önce veri ve strateji."),
    ("Yaratıcı ve \n\ncesur fikir.", "Yaratıcı ve cesur fikir."),
    ("Yaratıcı ve \n\ncesur fikir", "Yaratıcı ve cesur fikir"),
    (r"Find the \\r\\nbold idea.", "Yaratıcı ve cesur fikir."),
    ("Kusursuz \n\nsüreç yönetimi.", "Kusursuz süreç yönetimi."),
    ("Kusursuz \n\nsüreç yönetimi", "Kusursuz süreç yönetimi"),
    (r"Nail the \\r\\nprocess.", "Kusursuz süreç yönetimi."),
    ("Dönüşüm için \n\ntasarla.", "Dönüşüm için tasarla."),
    ("Dönüşüm için \n\ntasarla", "Dönüşüm için tasarla"),
    (r"Create to \\r\\nconvert.", "Dönüşüm için tasarla."),
    ("Ölçeklenebilir \n\nbüyüme.", "Ölçeklenebilir büyüme."),
    ("Ölçeklenebilir \n\nbüyüme", "Ölçeklenebilir büyüme"),
    (r"Build for \\r\\nscale.", "Ölçeklenebilir büyüme."),
]


def main():
    for rel in TARGET_FILES:
        p = ROOT / rel
        if not p.exists():
            print(f"SKIP (not found): {rel}")
            continue
        html = p.read_text(encoding="utf-8")

        # Protect byte-counted T712 JSON-LD block so byte length never shifts
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
