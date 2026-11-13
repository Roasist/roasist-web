"""Roasist reference list for the /referanslar page.

Single source of truth. Add `video` (file name inside public/images/references/)
to a reference to give its card a short loop video; the poster is generated from
the logo until then. Featured projects (those that already have a video on the
homepage) are pulled from scripts/update_work_section.py PROJECTS.
"""

# sector slug -> label (a filter only appears for sectors that have >= 1 reference)
SECTORS = {
    "saglik": "Sağlık",
    "egitim": "Eğitim",
    "gayrimenkul-turizm": "Gayrimenkul ve Turizm",
    "cagri-merkezi": "Çağrı Merkezi",
    "yeme-icme": "Yeme İçme",
    "oyun": "Oyun",
}

# Sector of the featured homepage projects (keyed by PROJECTS["name"]).
FEATURED_SECTORS = {
    "23 Projects": "gayrimenkul-turizm",
    "Summer Homes": "gayrimenkul-turizm",
    "Dental Art": "saglik",
    "Medistate": "saglik",
    "Bonus Vip": "cagri-merkezi",
}

# (slug, title, logo file in public/images/clients, sector slug or None, video or None)
# Sector is only set where the brand's sector is clear; None = shown under "Tümü" only.
REFERENCES = [
    ("op-dr-ozgur-demirtas", "Op. Dr. Özgür Demirtaş", "Calisma-Yuzeyi-28-kopya-21.webp", "saglik", "op-dr-ozgur-demirtas.mp4"),
    ("center-of-surgeons", "Center of Surgeons", "Calisma-Yuzeyi-28-kopya-19_4x.webp", "saglik", "center-of-surgeons.mp4"),
    ("doctor-bircan", "Doctor Bircan", "Calisma-Yuzeyi-28-kopya-17_4x.webp", "saglik", "doctor-bircan.mp4"),
    ("dermaderm", "DermaDerm", "Calisma-Yuzeyi-28-kopya-14_4x.webp", "saglik", "dermaderm.mp4"),
    ("turkey-hair-academy", "Turkey Hair Academy", "Calisma-Yuzeyi-28-kopya-22.webp", "saglik", "turkey-hair-academy.mp4"),
    ("autarke-call-center", "Autarke Call Center", "Calisma-Yuzeyi-28-kopya-9_4x.webp", "cagri-merkezi", "autarke-call-center.mp4"),
    ("bbg-call-center", "BBG Call Center", "bbg-call-center.png", "cagri-merkezi", "bbg-call-center.mp4"),
    ("loyalcall", "LoyalCall", "loyalcall.png", "cagri-merkezi", "loyalcall.mp4"),
    ("turkey-house", "Turkey House", "Website-Reference-Logo-5.png", "gayrimenkul-turizm", "turkey-house.mp4"),
    ("livaneli-group", "Livaneli Group", "livaneli.png", "gayrimenkul-turizm", "livaneli-group.mp4"),
    ("hyundai", "Hyundai", "Calisma-Yuzeyi-28-kopya-8_4x.webp", None, "hyundai.mp4"),
    ("mobile-game-factory", "Mobile Game Factory", "Calisma-Yuzeyi-28-kopya-15_4x.webp", "oyun", "mobile-game-factory.mp4"),
    ("istanbul-medya-akademisi", "İstanbul Medya Akademisi", "Calisma-Yuzeyi-28-kopya_4x.webp", "egitim", "istanbul-medya-akademisi.mp4"),
    ("kodlab", "Kodlab", "Calisma-Yuzeyi-28-kopya-2_4x.webp", None, "kodlab.mp4"),
    ("dus-bahcesi-okullari", "Düş Bahçesi Okulları", "Website-Reference-Logo-2.png", "egitim", "dus-bahcesi-okullari.mp4"),
    ("marmara-kurs", "Marmara Kurs", "Website-Reference-Logo-3.png", "egitim", "marmara-kurs.mp4"),
    ("bessekiz-ortaokullari", "Beşsekiz Ortaokulları", "besseKiz.png", "egitim", "bessekiz-ortaokullari.mp4"),
    ("urla-balik", "Urla Balık", "Calisma-Yuzeyi-28-kopya-10_4x.webp", "yeme-icme", "urla-balik.mp4"),
    ("izmir-balik-restaurant", "İzmir Balık Restaurant", "izmir-balik.png", "yeme-icme", "izmir-balik-restaurant.mp4"),
    ("kitapbilgini", "Kitapbilgini", "Calisma-Yuzeyi-28_4x.webp", None, "kitapbilgini.mp4"),
    ("sfk", "SFK", "Calisma-Yuzeyi-28-kopya-20_4x.webp", None, "sfk.mp4"),
    ("cosy-life-consulting", "Cosy Life Consulting", "Calisma-Yuzeyi-28-kopya-18_4x.webp", None, "cosy-life-consulting.mp4"),
    ("lefior", "Lefior", "Calisma-Yuzeyi-28-kopya-16_4x.webp", None, "lefior.mp4"),
    ("elose-laboratories", "Elose Laboratories", "Calisma-Yuzeyi-28-kopya-13_4x.webp", None, "elose-laboratories.mp4"),
    ("yoloo", "Yoloo", "Calisma-Yuzeyi-28-kopya-7_4x.webp", None, "yoloo.mp4"),
    ("natural-dukkan", "Natural Dukkan", "Calisma-Yuzeyi-28-kopya-11_4x.webp", None, "natural-dukkan.mp4"),
    ("3e-ilaclama", "3E İlaçlama", "Calisma-Yuzeyi-28-kopya-12_4x.webp", None, "3e-ilaclama.mp4"),
    ("yengec", "Yengeç", "Calisma-Yuzeyi-28-kopya-6_4x.webp", None, "yengec.mp4"),
    ("pedalbox", "Pedalbox", "Calisma-Yuzeyi-28-kopya-5_4x.webp", None, "pedalbox.mp4"),
    ("gekoo", "GekoO", "Calisma-Yuzeyi-28-kopya-4_4x.webp", None, "gekoo.mp4"),
    ("decorevi", "DecorEvi", "Calisma-Yuzeyi-28-kopya-3_4x.webp", None, "decorevi.mp4"),
    ("sekiz-oniki", "Sekiz Oniki", "Website-Reference-Logo-1.png", "egitim", "sekiz-oniki.mp4"),
    ("cordelia", "Cordelia", "cordelia.webp", "gayrimenkul-turizm", "cordelia.mp4"),
]

# Card details per reference slug: year of work, services we delivered, optional hover heading.
DETAILS = {
    "pedalbox": {"year": "2020", "services": ["Performans Pazarlaması", "Web Analitiği"]},
    "op-dr-ozgur-demirtas": {
        "year": "2022",
        "services": ["Performans Pazarlaması", "Web Analitik", "Büyüme Stratejisi", "Grafik Tasarım"],
    },
    "doctor-bircan": {
        "year": "2022",
        "services": ["Performans Pazarlaması", "Web Analitiği", "Büyüme Stratejisi"],
    },
    "center-of-surgeons": {
        "year": "2022",
        "services": ["Performans Pazarlaması", "Web Analitiği", "Büyüme Stratejisi"],
    },
    "turkey-house": {
        "year": "2025",
        "services": ["Performans Pazarlaması", "Web Analitiği", "Büyüme Stratejisi"],
    },
    "livaneli-group": {
        "year": "2025",
        "services": ["Performans Pazarlaması", "Web Analitiği", "Büyüme Stratejisi", "Grafik Tasarım", "Web Tasarım"],
    },
    "istanbul-medya-akademisi": {
        "services": ["Performans Pazarlaması", "Web Analitiği", "Büyüme Stratejisi", "Grafik Tasarım", "Web Tasarım"],
    },
    "izmir-balik-restaurant": {
        "services": ["Performans Pazarlaması", "Web Analitiği", "Büyüme Stratejisi", "Grafik Tasarım", "Web Tasarım", "Kreatif İletişim"],
    },
    "dus-bahcesi-okullari": {
        "services": ["Performans Pazarlaması", "Web Analitiği"],
    },
    "yengec": {
        "services": ["Performans Pazarlaması", "Web Analitiği"],
    },
    "gekoo": {
        "services": ["Performans Pazarlaması", "Web Analitiği", "Kreatif İletişim"],
    },
    "sekiz-oniki": {
        "services": ["Performans Pazarlaması", "Web Analitiği"],
    },
    "cordelia": {
        "services": ["Performans Pazarlaması", "Web Analitiği", "Kreatif İletişim"],
    },
    "dermaderm": {
        "services": ["Performans Pazarlaması"],
    },
}
