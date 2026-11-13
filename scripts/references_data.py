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
    ("turkey-hair-academy", "Turkey Hair Academy", "Calisma-Yuzeyi-28-kopya-22.webp", "saglik", "turkey-hair-academy.mp4"),
    ("autarke-call-center", "Autarke Call Center", "Calisma-Yuzeyi-28-kopya-9_4x.webp", "cagri-merkezi", "autarke-call-center.mp4"),
    ("izmir-balik-restaurant", "İzmir Balık Restaurant", "izmir-balik.png", "yeme-icme", "izmir-balik-restaurant.mp4"),
    ("bbg-call-center", "BBG Call Center", "bbg-call-center.png", "cagri-merkezi", "bbg-call-center.mp4"),
    ("loyalcall", "LoyalCall", "loyalcall.png", "cagri-merkezi", "loyalcall.mp4"),
    ("doctor-bircan", "Doctor Bircan", "Calisma-Yuzeyi-28-kopya-17_4x.webp", "saglik", "doctor-bircan.mp4"),
    ("hyundai", "Hyundai", "Calisma-Yuzeyi-28-kopya-8_4x.webp", None, "hyundai.mp4"),
    ("mobile-game-factory", "Mobile Game Factory", "Calisma-Yuzeyi-28-kopya-15_4x.webp", "oyun", "mobile-game-factory.mp4"),
    ("yengec", "Yengeç", "Calisma-Yuzeyi-28-kopya-6_4x.webp", None, "yengec.mp4"),
    ("kodlab", "Kodlab", "Calisma-Yuzeyi-28-kopya-2_4x.webp", None, "kodlab.mp4"),
    ("marmara-kurs", "Marmara Kurs", "Website-Reference-Logo-3.png", "egitim", "marmara-kurs.mp4"),
    ("turkey-house", "Turkey House", "Website-Reference-Logo-5.png", "gayrimenkul-turizm", "turkey-house.mp4"),
    ("bessekiz-ortaokullari", "Beşsekiz Ortaokulları", "besseKiz.png", "egitim", "bessekiz-ortaokullari.mp4"),
    ("urla-balik", "Urla Balık", "Calisma-Yuzeyi-28-kopya-10_4x.webp", "yeme-icme", "urla-balik.mp4"),
    ("livaneli-group", "Livaneli Group", "livaneli.png", "gayrimenkul-turizm", "livaneli-group.mp4"),
    ("kitapbilgini", "Kitapbilgini", "Calisma-Yuzeyi-28_4x.webp", None, "kitapbilgini.mp4"),
    ("sfk", "SFK", "Calisma-Yuzeyi-28-kopya-20_4x.webp", None, "sfk.mp4"),
    ("istanbul-medya-akademisi", "İstanbul Medya Akademisi", "Calisma-Yuzeyi-28-kopya_4x.webp", "egitim", "istanbul-medya-akademisi.mp4"),
    ("cosy-life-consulting", "Cosy Life Consulting", "Calisma-Yuzeyi-28-kopya-18_4x.webp", None, "cosy-life-consulting.mp4"),
    ("dus-bahcesi-okullari", "Düş Bahçesi Okulları", "Website-Reference-Logo-2.png", "egitim", "dus-bahcesi-okullari.mp4"),
    ("lefior", "Lefior", "Calisma-Yuzeyi-28-kopya-16_4x.webp", None, "lefior.mp4"),
    ("center-of-surgeons", "Center of Surgeons", "Calisma-Yuzeyi-28-kopya-19_4x.webp", "saglik", "center-of-surgeons.mp4"),
    ("elose-laboratories", "Elose Laboratories", "Calisma-Yuzeyi-28-kopya-13_4x.webp", None, "elose-laboratories.mp4"),
    ("dermaderm", "DermaDerm", "Calisma-Yuzeyi-28-kopya-14_4x.webp", "saglik", "dermaderm.mp4"),
    ("yoloo", "Yoloo", "Calisma-Yuzeyi-28-kopya-7_4x.webp", None, "yoloo.mp4"),
    ("pedalbox", "Pedalbox", "Calisma-Yuzeyi-28-kopya-5_4x.webp", None, "pedalbox.mp4"),
    ("natural-dukkan", "Natural Dukkan", "Calisma-Yuzeyi-28-kopya-11_4x.webp", None, "natural-dukkan.mp4"),
    ("gekoo", "GekoO", "Calisma-Yuzeyi-28-kopya-4_4x.webp", None, "gekoo.mp4"),
    ("3e-ilaclama", "3E İlaçlama", "Calisma-Yuzeyi-28-kopya-12_4x.webp", None, "3e-ilaclama.mp4"),
    ("sekiz-oniki", "Sekiz Oniki", "Website-Reference-Logo-1.png", "egitim", "sekiz-oniki.mp4"),
    ("decorevi", "DecorEvi", "Calisma-Yuzeyi-28-kopya-3_4x.webp", None, "decorevi.mp4"),
    ("cordelia", "Cordelia", "cordelia.webp", "gayrimenkul-turizm", "cordelia.mp4"),
]

# Card details per reference slug: hover heading and delivered services.
DETAILS = {
    "op-dr-ozgur-demirtas": {
        "heading": "Estetik ve cerrahide hasta odaklı dijital büyüme.",
        "services": ["Performans Pazarlaması", "Web Analitik", "Büyüme Stratejisi", "Grafik Tasarım"],
    },
    "turkey-hair-academy": {
        "heading": "Sağlık turizminde global hasta kazanımı ve ölçekleme.",
        "services": ["Performans Pazarlaması", "Büyüme Stratejisi"],
    },
    "autarke-call-center": {
        "heading": "Çok dilli çağrı merkezleri için kurumsal müşteri edinimi.",
        "services": ["Performans Pazarlaması", "Dijital Strateji"],
    },
    "izmir-balik-restaurant": {
        "heading": "Gastronomide yerel marka bilinirliği ve masa rezervasyonu.",
        "services": ["Performans Pazarlaması", "Web Analitiği", "Büyüme Stratejisi", "Grafik Tasarım", "Web Tasarım", "Kreatif İletişim"],
    },
    "bbg-call-center": {
        "heading": "Çağrı merkezi sektöründe nitelikli lead ve yetenek kazanımı.",
        "services": ["Performans Pazarlaması", "Büyüme Stratejisi"],
    },
    "loyalcall": {
        "heading": "Müşteri iletişim merkezleri için veri odaklı büyüme stratejisi.",
        "services": ["Performans Pazarlaması", "Web Analitiği"],
    },
    "doctor-bircan": {
        "heading": "Uluslararası saç ekimi ve estetikte yüksek dönüşümlü hasta edinimi.",
        "services": ["Performans Pazarlaması", "Web Analitiği", "Büyüme Stratejisi"],
    },
    "hyundai": {
        "heading": "Otomotiv dünyasında test sürüşü ve satış odaklı kampanyalar.",
        "services": ["Performans Pazarlaması", "Kampanya Yönetimi"],
    },
    "mobile-game-factory": {
        "heading": "Mobil oyun ekosisteminde kullanıcı edinimi ve küresel ölçeklenme.",
        "services": ["Performans Pazarlaması", "Büyüme Stratejisi"],
    },
    "yengec": {
        "heading": "E-ticaret entegrasyonu yazılımında SaaS büyüme ve müşteri edinimi.",
        "services": ["Performans Pazarlaması", "Web Analitiği"],
    },
    "kodlab": {
        "heading": "Yazılım ve teknoloji yayıncılığında e-ticaret odaklı satış artışı.",
        "services": ["Performans Pazarlaması", "E-Ticaret Büyüme"],
    },
    "marmara-kurs": {
        "heading": "Eğitim sektöründe hedef kitle odaklı öğrenci kayıt dönüşümü.",
        "services": ["Performans Pazarlaması", "Kayıt Stratejisi"],
    },
    "turkey-house": {
        "heading": "Yabancı yatırımcı odaklı lüks gayrimenkul portföy pazarlaması.",
        "services": ["Performans Pazarlaması", "Web Analitiği", "Büyüme Stratejisi"],
    },
    "bessekiz-ortaokullari": {
        "heading": "Özel okul eğitiminde veli etkileşimi ve yeni dönem kayıt başarısı.",
        "services": ["Performans Pazarlaması", "Kurumsal İletişim"],
    },
    "urla-balik": {
        "heading": "Ege gastronomisinde marka konumlandırma ve ziyaretçi trafiği.",
        "services": ["Performans Pazarlaması", "Kreatif İletişim"],
    },
    "livaneli-group": {
        "heading": "Prestijli gayrimenkul ve turizm yatırımlarında küresel büyüme.",
        "services": ["Performans Pazarlaması", "Web Analitiği", "Büyüme Stratejisi", "Grafik Tasarım", "Web Tasarım"],
    },
    "kitapbilgini": {
        "heading": "Online kitap satışında sepet dönüşüm oranı ve ROAS optimizasyonu.",
        "services": ["Performans Pazarlaması", "E-Ticaret Büyüme"],
    },
    "sfk": {
        "heading": "B2B sektöründe uluslararası pazar payı ve nitelikli talep oluşturma.",
        "services": ["Performans Pazarlaması", "B2B Strateji"],
    },
    "istanbul-medya-akademisi": {
        "heading": "Medya ve iletişim eğitimlerinde sektör profesyonellerine erişim.",
        "services": ["Performans Pazarlaması", "Web Analitiği", "Büyüme Stratejisi", "Grafik Tasarım", "Web Tasarım"],
    },
    "cosy-life-consulting": {
        "heading": "Yatırım ve yaşam danışmanlığında nitelikli müşteri portföyü.",
        "services": ["Performans Pazarlaması", "Büyüme Stratejisi"],
    },
    "dus-bahcesi-okullari": {
        "heading": "Erken çocukluk eğitiminde güven ve veli odaklı kayıt stratejisi.",
        "services": ["Performans Pazarlaması", "Web Analitiği"],
    },
    "lefior": {
        "heading": "Premium dermokozmetikte e-ticaret satış hacmi ve marka sadakati.",
        "services": ["Performans Pazarlaması", "E-Ticaret Büyüme"],
    },
    "center-of-surgeons": {
        "heading": "Cerrahi uzmanlık alanlarında küresel hasta iletişimi ve randevu hacmi.",
        "services": ["Performans Pazarlaması", "Web Analitiği", "Büyüme Stratejisi"],
    },
    "elose-laboratories": {
        "heading": "Dermokozmetik laboratuvar ürünlerinde pazaryeri ve web satışı.",
        "services": ["Performans Pazarlaması", "E-Ticaret Stratejisi"],
    },
    "dermaderm": {
        "heading": "Bitkisel cilt ve saç bakımında doğrudan tüketiciye satış ölçekleme.",
        "services": ["Performans Pazarlaması"],
    },
    "yoloo": {
        "heading": "Mobil ulaşım teknolojisinde aktif kullanıcı edinimi ve büyüme.",
        "services": ["Performans Pazarlaması", "Uygulama Büyüme"],
    },
    "pedalbox": {
        "heading": "Otomotiv performans teknolojisinde e-ticaret satış ve lead artışı.",
        "services": ["Performans Pazarlaması", "Web Analitiği"],
    },
    "natural-dukkan": {
        "heading": "Organik ve doğal yaşam ürünlerinde sürdürülebilir e-ticaret geliri.",
        "services": ["Performans Pazarlaması", "E-Ticaret Büyüme"],
    },
    "gekoo": {
        "heading": "Organik bebek ve çocuk beslenmesinde güven odaklı satış dönüşümü.",
        "services": ["Performans Pazarlaması", "Web Analitiği", "Kreatif İletişim"],
    },
    "3e-ilaclama": {
        "heading": "Kurumsal ve bireysel çevre sağlığında hızlı yerel çağrı dönüşümü.",
        "services": ["Performans Pazarlaması", "Yerel Reklamlar"],
    },
    "sekiz-oniki": {
        "heading": "Sınav hazırlık eğitiminde hedefli veli iletişimi ve şube kayıtları.",
        "services": ["Performans Pazarlaması", "Web Analitiği"],
    },
    "decorevi": {
        "heading": "Ev dekorasyonunda ortalama sepet tutarı ve e-ticaret ROAS artışı.",
        "services": ["Performans Pazarlaması", "E-Ticaret Reklamları"],
    },
    "cordelia": {
        "heading": "Butik tatil ve gayrimenkul konseptinde yüksek etkileşimli doluluk.",
        "services": ["Performans Pazarlaması", "Web Analitiği", "Kreatif İletişim"],
    },
}
