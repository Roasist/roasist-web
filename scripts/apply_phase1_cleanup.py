#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Faz 1 Comprehensive Cleanup & Synchronization for Roasist Web:
  1. Creates /hizmetler/performans-pazarlamasi/bing-reklamlari/index.html and
     /hizmetler/bing-reklamlari/index.html in both public/ and dist/, plus adds
     Bing Reklamları to scripts/services_data.json.
  2. Updates Testimonials_testimonials__J0bdm across all /hizmetler/... pages (SSR + Flight 12 + Flight 38..44)
     with Roasist's 3 real customer testimonials (Burak Özhan, Gaye Tukar, Celal Kandemir) & Roasist client logos.
  3. Updates /iletisim/ and /start-your-project/ (SSR + Flight 10) with +90 540 507 53 50,
     WhatsApp (https://wa.me/905405075350), Roasist's 5 social channels, and removes KOTA/London/careers@kota.co.uk
     while keeping <section class="Form_contactForm__X6bdS"> SSR 100% intact.
  4. Synchronizes Footer_footer__pQtti (SSR + Flight) across ALL KOTA pages in public/ and dist/
     (including dist/index.html and public/kota-roasist-local.html) with 5 Roasist social accounts,
     4 official Partner Badges, Turkish footer links, © Roasist 2026, and +90 540 507 53 50 • İstanbul.
  5. Updates all remaining phone occurrences (541 507 53 50 / 546 965 70 20) to +90 540 507 53 50 across src/, public/, dist/.
  6. Fixes /referanslar/ <title> (SSR + Flight) to "Referanslar & Başarı Hikayeleri | Roasist".
"""

import glob
import html as html_mod
import json
import os
import re
import sys

ROOT = "/home/antigravity/Roasist/roasist-web"
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from update_about_page import parse_flight_stream, serialize_flight_stream  # noqa: E402

CDN_BASE = "https://cdn.jsdelivr.net/gh/Roasist/roasist-web@189b2e0aee16a196d88d8895fb3795810c6d17f9"
BADGE_CDN = "https://cdn.jsdelivr.net/gh/Roasist/roasist-web@c766063e6a19824bf5e1a598d275bf05cbf2226f/public"

OFFICIAL_PHONE_DISPLAY = "+90 540 507 53 50"
OFFICIAL_PHONE_TEL = "tel:+905405075350"
OFFICIAL_WHATSAPP_URL = "https://wa.me/905405075350"

ROASIST_SOCIALS = [
    ("Instagram", "https://www.instagram.com/roasist"),
    ("LinkedIn", "https://www.linkedin.com/company/roasist"),
    ("X", "https://twitter.com/Roasistt"),
    ("Facebook", "https://www.facebook.com/roasistt"),
    ("YouTube", "https://www.youtube.com/channel/UCY3G_IU2YJ326zGwU3_YlyA"),
]

FOOTER_NAV_TR = [
    ("İletişim", "/iletisim/"),
    ("Hakkımızda", "/hakkimizda/"),
    ("Gizlilik Politikası", "/gizlilik-politikasi-ve-kullanim-sartlari/"),
]

FOOTER_SERVICES_TR = [
    ("Performans Pazarlaması", "/hizmetler/performans-pazarlamasi/"),
    ("SEO", "/hizmetler/seo/"),
    ("Grafik Tasarım", "/hizmetler/grafik-tasarim/"),
    ("Web Tasarım", "/hizmetler/web-tasarim/"),
    ("360° Dijital Pazarlama", "/hizmetler/360-derece-dijital-pazarlama-yonetimi/"),
]

ROASIST_TESTIMONIALS_TR = [
    {
        "text": (
            '"Reklam sürecinde projeye yaklaşımları, anlaşmamızın ötesinde sorumluluk alarak '
            "grafik tasarım katkısı sunmaları ve 7/24 destekleriyle işimiz için en az bizim kadar "
            "dertlenen bir ekiple çalıştığımız için şanslıyız. Roasist ile gönül rahatlığıyla "
            'çalışabilirsiniz."'
        ),
        "backgroundColor": "#EDE9FE",
        "name": "Burak Özhan",
        "speciality": "Project Program Coordinator",
        "button": {"title": "Projeyi İncele", "url": "/referanslar/", "target": ""},
        "logo_rel": "ref-14.png",
        "width": 241,
        "height": 34,
    },
    {
        "text": (
            '"Roasist ile yaklaşık iki senedir çalışıyoruz. Her sorumuza dürüstlükle yanıt alıyor, '
            "tüm sorunlarımızı efektif bir şekilde çözüyorlar. Öncesi-sonrası değerlendirmesi "
            "yaptığımda kazanç konusunda bize çok büyük katkıları oldu. Profesyonel yaklaşımları "
            'için çok teşekkür ederim."'
        ),
        "backgroundColor": "#E0E7FF",
        "name": "Gaye Tukar",
        "speciality": "Girişimci & Kurucu",
        "button": {"title": "Projeyi İncele", "url": "/referanslar/", "target": ""},
        "logo_rel": "ref-04.png",
        "width": 640,
        "height": 388,
    },
    {
        "text": (
            '"Mesai kavramı olmaksızın sizin için çalışıyorlar. İşinde profesyonel, şeffaf ve '
            "doğrudan sonuç odaklı bir dijital pazarlama ajansı arıyorsanız Roasist'i kesinlikle "
            'tavsiye ederim."'
        ),
        "backgroundColor": "#F3E8FF",
        "name": "Celal Kandemir",
        "speciality": "İşletme Sahibi",
        "button": {"title": "Projeyi İncele", "url": "/referanslar/", "target": ""},
        "logo_rel": "ref-25.png",
        "width": 233,
        "height": 53,
    },
]

PUSH_RE = re.compile(r'(?:<script>)+self\.__next_f\.push\(\[1,\s*("(?:\\.|[^"\\])*")\]\)(?:</script>)+')

ROASIST_LOGO_PATH_D = (
    "M176.71,198.48v1.32l-35.19.2c-1.72-2.67-2.88-6.5-3.64-11.52-.59-4.79-1.15-10-1.55-15.35"
    "s-.56-10.76-1-15.75a95,95,0,0,0-1.16-12.48c-1-4.42-2.51-8.08-4.62-10.56a20.66,20.66,0,0,0-7.46-6.17,"
    "32.19,32.19,0,0,0-9.81-2.88c-3.66-.36-7.29-.56-11.15-.56h-47v-35h56.29v18.62L164.6,77.1,110.46,45.8"
    "V64.42H54.17v16L0,49.07,54.17,17.74V34.08h64.9c18.26,0,32.29,3.47,41.89,10.17,9.78,6.93,14.6,18.06,"
    "14.6,33.41,0,10.4-2.12,18.85-6.34,24.79C165,108.79,158.06,114,148.65,118.2a28.6,28.6,0,0,1,11.52,7.29,"
    "35.16,35.16,0,0,1,6.18,11.13A60.62,60.62,0,0,1,169,149.69c.4,4.62.56,9.21.76,13.44.2,6.33.4,11.52.79,"
    "15.74.36,4.06,1,7.5,1.32,10A24.35,24.35,0,0,0,174,195,8.76,8.76,0,0,0,176.71,198.48Z M186,84q1.68-15.32,"
    "7.38-26.28a41.37,41.37,0,0,1,16.45-17.12q10.74-6.15,28.86-6.15t28.86,6.15A41.37,41.37,0,0,1,284,57.73"
    "q5.7,11,7.38,26.28a308.26,308.26,0,0,1,1.68,33.45A307.5,307.5,0,0,1,291.39,151q-1.68,15.21-7.38,26.17"
    "A39.24,39.24,0,0,1,267.56,194q-10.74,5.82-28.86,5.82T209.84,194a39.24,39.24,0,0,1-16.45-16.78"
    "Q187.69,166.25,186,151a307.5,307.5,0,0,1-1.68-33.57A308.26,308.26,0,0,1,186,84Zm31.32,60.86"
    "a76.29,76.29,0,0,0,3.13,18.35q2.35,7,6.72,10.29c2.91,2.17,6.74,3.25,11.52,3.25s8.61-1.08,11.52-3.25,"
    "5.15-5.59,6.71-10.29a76.24,76.24,0,0,0,3.14-18.35q.78-11.3.78-27.41t-.78-27.29a77.72,77.72,0,0,0-3.14-18.35"
    "q-2.34-7.16-6.71-10.4T238.7,58.17c-4.78,0-8.61,1.09-11.52,3.25s-5.15,5.63-6.72,10.4a77.78,77.78,0,0,0-3.13,18.35"
    "q-.78,11.19-.78,27.29T217.33,144.87Z M383,37.59,425.3,197.34H391.74l-7.39-33.79H341.84l-7.38,33.79H300.9"
    "L343.19,37.59Zm-4.25,99.56L363.32,65.33h-.44l-15.44,71.82Z M462.44,152.14a53,53,0,0,0,.9,10.18,"
    "17.61,17.61,0,0,0,3.35,7.72,16.6,16.6,0,0,0,6.6,4.93,26.39,26.39,0,0,0,10.41,1.79A20.56,20.56,0,0,0,497,172"
    "q5.92-4.81,5.93-14.88a26.93,26.93,0,0,0-1.45-9.29,18.47,18.47,0,0,0-4.82-7.05,34.1,34.1,0,0,0-8.83-5.7,"
    "126.18,126.18,0,0,0-13.54-5.26,115.68,115.68,0,0,1-18.57-7.83,49.79,49.79,0,0,1-13.09-10,"
    "35.53,35.53,0,0,1-7.72-13.2,55.56,55.56,0,0,1-2.46-17.34q0-23.72,13.2-35.35t36.25-11.63"
    "a79.06,79.06,0,0,1,19.8,2.34,41.63,41.63,0,0,1,15.66,7.61,35.58,35.58,0,0,1,10.29,13.43"
    "q3.69,8.16,3.69,19.57v4.48H500.48q0-11.42-4-17.56T483,58.17a22.43,22.43,0,0,0-8.95,1.57,"
    "15.1,15.1,0,0,0-5.71,4.14,14.16,14.16,0,0,0-2.91,5.93,30.48,30.48,0,0,0-.78,6.93,23.06,23.06,0,0,0,3.13,12.42"
    "q3.13,5,13.43,9.29l24.83,10.74a75.73,75.73,0,0,1,15,8.39,41,41,0,0,1,9.29,9.39,31.46,31.46,0,0,1,4.81,11.08,"
    "62.31,62.31,0,0,1,1.34,13.42q0,25.29-14.65,36.81T481,199.8q-27.3,0-39-11.86t-11.75-34v-6.48h32.22Z "
    "M554.17,37.59h32.22V197.34H554.17ZM582.81,26.4H557.75V0h25.06Z M636.29,152.14a53.81,53.81,0,0,0,.89,10.18,"
    "17.74,17.74,0,0,0,3.36,7.72,16.6,16.6,0,0,0,6.6,4.93,26.37,26.37,0,0,0,10.4,1.79A20.59,20.59,0,0,0,670.86,172"
    "q5.92-4.81,5.93-14.88a26.68,26.68,0,0,0-1.46-9.29,18.33,18.33,0,0,0-4.81-7.05,34.17,34.17,0,0,0-8.84-5.7,"
    "125.1,125.1,0,0,0-13.53-5.26,115.68,115.68,0,0,1-18.57-7.83,49.63,49.63,0,0,1-13.09-10,"
    "35.53,35.53,0,0,1-7.72-13.2,55.56,55.56,0,0,1-2.46-17.34q0-23.72,13.2-35.35t36.24-11.63"
    "a79.2,79.2,0,0,1,19.81,2.34,41.63,41.63,0,0,1,15.66,7.61,35.58,35.58,0,0,1,10.29,13.43"
    "Q705.2,66,705.2,77.41v4.48H674.33q0-11.42-4-17.56t-13.43-6.16a22.46,22.46,0,0,0-9,1.57,"
    "15,15,0,0,0-5.7,4.14,14.16,14.16,0,0,0-2.91,5.93,29.93,29.93,0,0,0-.78,6.93,23.06,23.06,0,0,0,3.13,12.42"
    "q3.14,5,13.42,9.29l24.84,10.74a76,76,0,0,1,15,8.39A41,41,0,0,1,704.2,127a31.44,31.44,0,0,1,4.8,11.08,"
    "61.66,61.66,0,0,1,1.35,13.42q0,25.29-14.66,36.81T654.86,199.8q-27.3,0-39-11.86t-11.75-34v-6.48h32.22Z "
    "M820,64h-34.9V197.34H752.86V64H718V37.59H820Z"
)

SOCIAL_ARROW_PATH_D = (
    "M12.65.31a.504.504 0 00-.46-.31H.5C.22 0 0 .22 0 .5s.22.5.5.5h10.49L.55 11.43"
    "c-.2.2-.2.51 0 .71a.485.485 0 00.7 0L11.69 1.71v10.47c0 .28.22.5.5.5s.5-.22.5-.5V.52c0-.07 0-.14-.04-.21z"
)

BUTTON_ARROW_PATH_D = (
    "m17.1,7.58s-.01-.04-.01-.06c.01-.22-.06-.45-.24-.61L9.23.19c-.31-.27-.78-.24-1.06.07"
    "-.27.31-.24.78.07,1.06l6.26,5.52H.75c-.41,0-.75.34-.75.75s.34.75.75.75h13.74l-6.26,5.52"
    "c-.31.27-.34.75-.07,1.06.15.17.35.25.56.25.18,0,.35-.06.5-.19l7.62-6.72c.18-.16.25-.39.24-.61,0-.02.01-.04.01-.06Z"
)


def rewrite_flight_in_html(html: str, mutator_fn) -> str:
    """
    Joins all contiguous <script>self.__next_f.push([1, "..."])</script> tags into a single
    React Flight stream, runs mutator_fn(records), and re-encodes with exact T<hex>, byte lengths.
    """
    pushes = list(PUSH_RE.finditer(html))
    if not pushes:
        return html
    joined_flight = "".join(json.loads(pm.group(1)) for pm in pushes)
    records = parse_flight_stream(joined_flight)
    changed = mutator_fn(records)
    if changed:
        new_flight_str = serialize_flight_stream(records)
        assert serialize_flight_stream(parse_flight_stream(new_flight_str)) == new_flight_str
        encoded = json.dumps(new_flight_str, ensure_ascii=False).replace("</script>", "<\\/script>")
        new_tag = f"<script>self.__next_f.push([1,{encoded}])</script>"
        html = html[: pushes[0].start()] + new_tag + html[pushes[-1].end() :]
    return html


# ==============================================================================
# STEP 1: CREATE BING REKLAMLARI PAGES & ADD TO services_data.json
# ==============================================================================
BING_SERVICE_JSON = {
    "slug": "performans-pazarlamasi/bing-reklamlari",
    "permalink": "/hizmetler/performans-pazarlamasi/bing-reklamlari/",
    "category": "Performans Kanalı",
    "icon": "tabler:brand-windows",
    "seoTitle": "Bing Reklamları (Microsoft Advertising) - Roasist",
    "seoDescription": (
        "Bing reklamları (Microsoft Advertising) ile masaüstü ve kurumsal aramalarda yüksek satın alma "
        "gücüne sahip kitlelere düşük tıklama maliyetleriyle (CPC) ulaşın."
    ),
    "h1": "Bing Reklamları",
    "heroQuestion": "Microsoft Advertising ve Bing reklamlarıyla yüksek ROAS yakalamaya hazır mısınız?",
    "aeoDirectAnswer": (
        "Bing Reklamları (Microsoft Advertising); Windows, Microsoft Edge, Bing, Yahoo ve DuckDuckGo arama ağında "
        "masaüstü ve kurumsal karar vericilere daha düşük tıklama maliyetleriyle (CPC) ulaşarak ihracat, B2B, "
        "turizm ve e-ticaret markalarına yüksek yatırım getirisi (ROAS) sağlayan performans reklam platformudur."
    ),
    "metrics": [
        {
            "value": "Microsoft Ağı",
            "label": "Bing, Yahoo & DuckDuckGo",
            "detail": "Masaüstü ve kurumsal aramalarda yüksek satın alma gücü",
        },
        {
            "value": "Düşük CPC",
            "label": "Yüksek ROAS Verimliliği",
            "detail": "Daha düşük rekabet ve birim tıklama maliyetiyle kârlı dönüşüm",
        },
        {
            "value": "LinkedIn Verisi",
            "label": "Profil Bazlı Hedefleme",
            "detail": "Microsoft ekosistemi üzerinden şirket, sektör ve unvan hedeflemesi",
        },
    ],
    "overviewHeading": "İşletmeler İçin Bing Reklamlarının Önemi Nedir?",
    "overviewParagraphs": [
        (
            "Roasist, kalite ve performans odaklı çalışma prensibini gözetir, doğru ölçümleme için gerekli "
            "entegrasyonları ve teknolojileri kullanır, detaylı analizler sonucu reklam stratejinizi inşa eder, "
            "verilerin ışığında kampanya süreçlerini daha iyi hale getirir ve anlamlı raporlar ile sürece sizi de dahil eder."
        ),
        (
            "Bing Reklamları (Microsoft Advertising), başta Kuzey Amerika, İngiltere ve Avrupa olmak üzere küresel "
            "pazarlarda Windows işletim sistemi ve Microsoft Edge tarayıcısını varsayılan olarak kullanan yüksek gelir "
            "grubundaki masaüstü kullanıcılarına ve kurumsal profesyonellere ulaşmanın en kârlı yoludur."
        ),
        (
            "Daha düşük tıklama başı maliyetler (CPC), Google Ads kampanya senkronizasyonu ve Microsoft’a özel "
            "LinkedIn profil hedefleme yetenekleriyle hem B2B hem de uluslararası B2C satışlarınızı ölçeklendiriyoruz."
        ),
    ],
    "subFeaturesTitle": "Bing Ads & Microsoft Advertising Çözümlerimiz",
    "subFeaturesSubtitle": "Küresel arama ağında daha düşük maliyetle daha nitelikli müşteriler kazandırıyoruz.",
    "subFeatures": [
        {
            "title": "Microsoft Arama Ağı (Bing, Yahoo, DuckDuckGo)",
            "description": (
                "Bing, Yahoo, DuckDuckGo ve Ecosia arama sonuçlarında ürün veya hizmetinizi arayan yüksek satın alma "
                "niyetli kullanıcılara tam karar anında en üst sırada görünür olun."
            ),
            "icon": "tabler:search",
        },
        {
            "title": "Microsoft Audience Network & Alışveriş Reklamları",
            "description": (
                "MSN, Outlook ve Microsoft iş ortağı premium yayıncılarda görsel reklamlar ve ürün katalog (Shopping) "
                "kampanyalarıyla e-ticaret ve ihracat dönüşümlerinizi katlayın."
            ),
            "icon": "tabler:shopping-cart",
        },
        {
            "title": "LinkedIn Profil Tabanlı Kurumsal Hedefleme",
            "description": (
                "Arama reklamlarında yalnızca Microsoft Advertising’in sunduğu LinkedIn şirket, sektör ve iş unvanı "
                "katmanlarını kullanarak B2B karar vericilere nokta atışı ulaşın."
            ),
            "icon": "tabler:briefcase",
        },
    ],
    "processTitle": "Bing Reklamları Hizmet Sürecimiz",
    "faqs": [
        {
            "question": "Bing Reklamları (Microsoft Advertising) nedir ve nerelerde yayınlanır?",
            "answer": (
                "Bing Reklamları; Microsoft Bing, Yahoo, DuckDuckGo arama motorlarında ve MSN, Microsoft Edge, "
                "Outlook gibi Microsoft Audience Network platformlarında yayınlanan arama, alışveriş ve görüntülü "
                "performans reklamlarıdır."
            ),
        },
        {
            "question": "Hangi işletmeler mutlaka Bing Reklamları kullanmalıdır?",
            "answer": (
                "ABD, İngiltere, Almanya ve Avrupa pazarlarına ihracat, yazılım/SaaS, sağlık turizmi, turizm veya "
                "e-ticaret satışı yapan markalar ile masaüstü kullanan kurumsal B2B karar vericilere düşük CPC "
                "maliyetleriyle ulaşmak isteyen tüm işletmeler için yüksek ROAS sağlayan bir kanaldır."
            ),
        },
    ],
}

YANDEX_TO_BING_PAIRS = [
    ("Yandex Reklamları - Roasist", BING_SERVICE_JSON["seoTitle"]),
    (
        "Yandex reklamlarıyla Rusya, BDT ülkeleri ve küresel pazarlarda hedef kitlenize ulaşın. Yandex Direct arama ve görüntülü reklam ağı yönetimi.",
        BING_SERVICE_JSON["seoDescription"],
    ),
    ("Global pazarda", "Küresel aramada"),
    ("<em>Yandex Ads</em>", "<em>Bing Ads</em>"),
    ("hakimiyeti.", "verimliliği."),
    ("Yandex Ads", "Bing Ads"),
    ("Yandex Reklamları Hizmet Sürecimiz", "Bing Reklamları Hizmet Sürecimiz"),
    (
        "Yandex Reklamları (Yandex Direct); Rusya, BDT (Bağımsız Devletler Topluluğu) ülkeleri ve Rusça konuşan pazarlarda lider arama motoru olan Yandex’in Arama Sonuçları ve Yandex Reklam Ağı (YAN) üzerinden ihracat, turizm, sağlık turizmi ve gayrimenkul markalarını doğrudan potansiyel müşterilerle buluşturan reklam platformudur.",
        BING_SERVICE_JSON["aeoDirectAnswer"],
    ),
    (
        "İşletmeler İçin Yandex Reklamlarının Önemi Nedir?",
        BING_SERVICE_JSON["overviewHeading"],
    ),
    (
        "Yandex Reklamları, Rusya ve BDT ülkelerinin önde gelen arama motoru ve dijital ekosistemi olan Yandex üzerinde markaların ürün veya hizmetlerini tanıtmak için kullanılan en güçlü reklam kanalıdır.",
        BING_SERVICE_JSON["overviewParagraphs"][1],
    ),
    (
        "Özellikle sağlık turizmi, gayrimenkul, turizm/otelcilik, tekstil ve ihracat yapan işletmeler için Yandex Direct üzerinden bölgesel, demografik ve arama niyetine dayalı hedefleme yaparak yüksek dönüşümlü uluslararası müşteriler kazandırıyoruz.",
        BING_SERVICE_JSON["overviewParagraphs"][2],
    ),
    (
        "Yandex Arama (Search) Reklamları",
        BING_SERVICE_JSON["subFeatures"][0]["title"],
    ),
    (
        "Yandex arama motorunda ürün veya hizmetinizi Rusça veya yerel dilde arayan kullanıcılara en üst sırada reklamlarınızı gösterin.",
        BING_SERVICE_JSON["subFeatures"][0]["description"],
    ),
    (
        "Yandex Reklam Ağı (YAN) Gösterim Reklamları",
        BING_SERVICE_JSON["subFeatures"][1]["title"],
    ),
    (
        "Yandex’in ortaklık ağındaki binlerce popüler web sitesi ve mobil uygulamada görsel, metin ve video reklamlarla erişiminizi katlayın.",
        BING_SERVICE_JSON["subFeatures"][1]["description"],
    ),
    (
        "Sağlık Turizmi &amp; Gayrimenkul Uzmanlığı",
        "LinkedIn Profil Tabanlı Kurumsal Hedefleme",
    ),
    (
        "Sağlık Turizmi & Gayrimenkul Uzmanlığı",
        "LinkedIn Profil Tabanlı Kurumsal Hedefleme",
    ),
    (
        "Türkiye’ye gelen uluslararası hasta ve gayrimenkul yatırımcılarının arama alışkanlıklarına özel yüksek dönüşümlü kampanya kurguları.",
        BING_SERVICE_JSON["subFeatures"][2]["description"],
    ),
    (
        "Yandex Reklamları nedir ve nerelerde görüntülenir?",
        BING_SERVICE_JSON["faqs"][0]["question"],
    ),
    (
        "Yandex Reklamları (Yandex Direct), Rusya ve BDT ülkelerinin lider arama motoru Yandex’in arama sonuçları sayfalarında, Yandex Haritalar’da ve Yandex Reklam Ağı (YAN) bünyesindeki binlerce web sitesi ile mobil uygulamada görüntülenen performans reklamlarıdır.",
        BING_SERVICE_JSON["faqs"][0]["answer"],
    ),
    (
        "Hangi sektörler mutlaka Yandex Reklamları kullanmalıdır?",
        BING_SERVICE_JSON["faqs"][1]["question"],
    ),
    (
        "Başta sağlık turizmi (saç ekimi, diş, estetik, hastane), gayrimenkul/inşaat, turizm ve otelcilik, e-ihracat, lojistik ve B2B üretim sektörleri olmak üzere Rusya ve BDT coğrafyasından müşteri kazanmak isteyen tüm işletmeler için vazgeçilmez bir kanaldır.",
        BING_SERVICE_JSON["faqs"][1]["answer"],
    ),
    (
        "Yandex Reklamları sürecinde raporlama ve şeffaflık nasıl sağlanır?",
        "Bing Reklamları sürecinde raporlama ve şeffaflık nasıl sağlanır?",
    ),
    (
        "Roasist ile Yandex Reklamları çalışmalarına nasıl başlayabiliriz?",
        "Roasist ile Bing Reklamları çalışmalarına nasıl başlayabiliriz?",
    ),
    (
        "#1 Arama — Rusça konuşulan coğrafyada en yüksek arama ve erişim payı",
        "Microsoft Ağı — Masaüstü ve kurumsal aramalarda yüksek satın alma gücü",
    ),
    (
        "Rusça konuşulan coğrafyada en yüksek arama ve erişim payı",
        "Masaüstü ve kurumsal aramalarda yüksek satın alma gücü",
    ),
    ("#1 Arama", "Microsoft Ağı"),
    ("Rusya &amp; BDT Pazar Lideri", "Bing, Yahoo &amp; DuckDuckGo"),
    ("Rusya & BDT Pazar Lideri", "Bing, Yahoo & DuckDuckGo"),
    (
        "Yandex Direct — Arama sonuçları ve binlerce iş ortağı sitede görsel reklamlar",
        "Düşük CPC — Daha düşük rekabet ve birim tıklama maliyetiyle kârlı dönüşüm",
    ),
    ("Yandex Direct", "Düşük CPC"),
    ("Arama + YAN Ağı", "Yüksek ROAS Verimliliği"),
    (
        "Metrica — Yandex Metrica ve Webvisor ile kullanıcı davranış analizi",
        "LinkedIn Verisi — Microsoft ekosistemi üzerinden şirket, sektör ve unvan hedeflemesi",
    ),
    ("Metrica", "LinkedIn Verisi"),
    ("Isı Haritası &amp; Analitik", "Profil Bazlı Hedefleme"),
    ("Isı Haritası & Analitik", "Profil Bazlı Hedefleme"),
    ("yandex-reklamlari", "bing-reklamlari"),
    ("Yandex Reklamları", "Bing Reklamları"),
]


def create_bing_ads_pages():
    sd_path = os.path.join(ROOT, "scripts", "services_data.json")
    sd = json.load(open(sd_path, "r", encoding="utf-8"))
    slugs = [s["slug"] for s in sd["servicesData"]]
    if BING_SERVICE_JSON["slug"] not in slugs:
        sd["servicesData"].append(BING_SERVICE_JSON)
        with open(sd_path, "w", encoding="utf-8") as f:
            json.dump(sd, f, ensure_ascii=False, indent=2)
            f.write("\n")

    for base_name in ("public", "dist"):
        src_path = os.path.join(
            ROOT, base_name, "hizmetler", "performans-pazarlamasi", "yandex-reklamlari", "index.html"
        )
        raw = open(src_path, "r", encoding="utf-8").read()

        # Split SSR and Flight pushes so we transform SSR cleanly and Flight records with byte-accurate T<hex>,
        pushes = list(PUSH_RE.finditer(raw))
        first_push_start = pushes[0].start()
        ssr = raw[:first_push_start]
        tail = raw[first_push_start:]

        for old_s, new_s in YANDEX_TO_BING_PAIRS:
            ssr = ssr.replace(old_s, new_s)

        def bing_mutator(records):
            for rec in records:
                kind, key, val = rec
                if kind == "text":
                    for old_s, new_s in YANDEX_TO_BING_PAIRS:
                        val = val.replace(old_s, new_s)
                    rec[2] = val
                else:
                    for old_s, new_s in YANDEX_TO_BING_PAIRS:
                        old_j = json.dumps(old_s, ensure_ascii=False)[1:-1]
                        new_j = json.dumps(new_s, ensure_ascii=False)[1:-1]
                        val = val.replace(old_j, new_j).replace(old_s, new_s)
                    rec[2] = val
            return True

        tail = rewrite_flight_in_html(tail, bing_mutator)
        bing_html = ssr + tail

        for rel_target in (
            os.path.join("hizmetler", "performans-pazarlamasi", "bing-reklamlari", "index.html"),
            os.path.join("hizmetler", "bing-reklamlari", "index.html"),
        ):
            out_path = os.path.join(ROOT, base_name, rel_target)
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(bing_html)
            print(f"[BING] Created {base_name}/{rel_target}")


# ==============================================================================
# STEP 2: UPDATE TESTIMONIALS ON ALL /hizmetler/... PAGES
# ==============================================================================
def build_ssr_testimonials_section(heading_text: str, items: list, is_dist: bool) -> str:
    logo_prefix = f"{CDN_BASE}/images/clients-white" if is_dist else "/images/clients-white"
    slides_html = []
    for it in items:
        logo_url = f"{logo_prefix}/{it['logo_rel']}"
        desc_esc = html_mod.escape(it["text"], quote=True)
        name_esc = html_mod.escape(it["name"], quote=True)
        spec_esc = html_mod.escape(it["speciality"], quote=True)
        btn_title = html_mod.escape(it["button"]["title"], quote=True)
        btn_url = html_mod.escape(it["button"]["url"], quote=True)
        slides_html.append(
            f'<div class="TestimonialsCarousel_swiperSlide__xzlOt swiper-slide">'
            f'<div class="TestimonialsPanel_panel__82Pbr testimonialPanel" style="background-color:{it["backgroundColor"]}">'
            f'<div class="TestimonialsPanel_panelWrap__IAqAF">'
            f'<figure class="TestimonialsPanel_logo__rFOvF">'
            f'<span class="Image_image__RAAdZ Image_intrinsic__JRoea">'
            f'<img data-srcset="" data-src="{logo_url}" alt="" fetchPriority="low" height="{it["height"]}" width="{it["width"]}" sizes="auto" class="lazyload"/>'
            f"</span></figure>"
            f'<p class="TestimonialsPanel_description__WA6g_">{desc_esc}</p>'
            f'<div class="TestimonialsPanel_details__JWR2H">'
            f'<span class="TestimonialsPanel_name__bD4Ek">{name_esc}</span>'
            f'<span class="TestimonialsPanel_name__bD4Ek">{spec_esc}</span>'
            f"</div>"
            f'<div class="TestimonialsPanel_buttons__gZnG1">'
            f'<div class="Magnetic_magnetic__LncOy" data-fill="false">'
            f'<div class="Button_button__JJiqJ" data-direction="forwards">'
            f'<a class="Button_inner__fnyH6" href="{btn_url}">'
            f'<span class="Button_border__hirH2"></span>'
            f'<span class="Button_text__IZaCD"><span class="Button_textInner__JTTHe">{btn_title}</span>'
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 17.1 15.17" class="Button_buttonArrow__0W9XI">'
            f'<path d="{BUTTON_ARROW_PATH_D}" fill="currentColor"></path></svg>'
            f"</span></a></div></div></div></div></div></div>"
        )
    carousel_inner = (
        '<div class="TestimonialsCarousel_panels__OhfPy">'
        '<div class="TestimonialsCarousel_container__sBMji">'
        '<div class="TestimonialsCarousel_swiper__OcQHM swiper">'
        f'<div class="swiper-wrapper">{"".join(slides_html)}</div>'
        '<div class="TestimonialsCarousel_swiperNav__zD7PI">'
        '<div class="TestimonialsCarousel_swiperNavNext__jvv3x swiper-panel-next"></div>'
        "</div></div></div></div>"
    )
    return (
        '<section class="Testimonials_testimonials__J0bdm">'
        '<div class="DarkThemeSwitch_cover__hn_xc"></div>'
        '<div class="container">'
        f'<h2 class="Testimonials_heading__q4vc3"><span class="LineByLine_headingOuter__JmusT"><span>{html_mod.escape(heading_text)}</span></span></h2>'
        f'<div class="Testimonials_testimonialDesktop__XClcG">{carousel_inner}</div>'
        "</div>"
        f'<div class="Testimonials_testimonialMobile__B0_Aa">{carousel_inner}</div>'
        "</section>"
    )


def find_node_by_class(node, cls_substr: str):
    if isinstance(node, list):
        if (
            len(node) >= 4
            and node[0] == "$"
            and isinstance(node[3], dict)
            and cls_substr in str(node[3].get("className", ""))
        ):
            return node
        for item in node:
            res = find_node_by_class(item, cls_substr)
            if res is not None:
                return res
    elif isinstance(node, dict):
        for v in node.values():
            res = find_node_by_class(v, cls_substr)
            if res is not None:
                return res
    return None


def update_service_testimonials(fp: str, is_dist: bool):
    html = open(fp, "r", encoding="utf-8").read()
    if "Testimonials_testimonials__J0bdm" not in html:
        return False

    logo_prefix = f"{CDN_BASE}/images/clients-white" if is_dist else "/images/clients-white"
    new_ssr_sec = build_ssr_testimonials_section("Müşterilerimiz Ne Diyor?", ROASIST_TESTIMONIALS_TR, is_dist)
    html, n_sub = re.subn(
        r'<section class="Testimonials_testimonials__J0bdm">.*?</section>',
        lambda _: new_ssr_sec,
        html,
        count=1,
        flags=re.S,
    )
    if n_sub != 1:
        raise RuntimeError(f"Expected 1 SSR Testimonials section in {fp}, found {n_sub}")

    desktop_items = [
        {
            "text": it["text"],
            "backgroundColor": it["backgroundColor"],
            "name": it["name"],
            "speciality": it["speciality"],
            "button": dict(it["button"]),
            "logo": {
                "altText": "",
                "srcSet": None,
                "sourceUrl": f"{logo_prefix}/{it['logo_rel']}",
                "mediaDetails": {"width": it["width"], "height": it["height"]},
            },
        }
        for it in ROASIST_TESTIMONIALS_TR
    ]

    def mutator(records):
        changed = False
        rec_map = {r[1]: r for r in records if r[0] == "line"}
        mobile_ref_key = None

        for rec in records:
            if rec[0] == "line" and "Testimonials_testimonials__J0bdm" in rec[2]:
                ast = json.loads(rec[2])
                t_sec = find_node_by_class(ast, "Testimonials_testimonials__J0bdm")
                if t_sec is None:
                    raise RuntimeError(f"Flight Testimonials AST not found in {fp}")
                desk = find_node_by_class(t_sec, "Testimonials_testimonialDesktop__XClcG")
                mob = find_node_by_class(t_sec, "Testimonials_testimonialMobile__B0_Aa")
                desk[3]["children"][3]["testimonials"] = desktop_items
                mob_val = mob[3]["children"][3]["testimonials"]
                if isinstance(mob_val, str) and mob_val.startswith("$"):
                    mobile_ref_key = mob_val[1:]
                else:
                    mob[3]["children"][3]["testimonials"] = desktop_items
                rec[2] = json.dumps(ast, ensure_ascii=False, separators=(",", ":"))
                changed = True

        if mobile_ref_key and mobile_ref_key in rec_map:
            # Replace mobile_ref_key directly with inline array of the 3 testimonials (valid Flight JSON!)
            rec_map[mobile_ref_key][2] = json.dumps(desktop_items, ensure_ascii=False, separators=(",", ":"))
            changed = True

        return changed

    html = rewrite_flight_in_html(html, mutator)

    # Ensure dark client logo filter on pastel lavender cards in <style data-roasist-theme>
    testi_css = (
        "/* ROASIST_SERVICE_TESTIMONIALS_CSS */"
        ".TestimonialsPanel_panel__82Pbr{border:1.5px solid rgba(118,2,255,0.22)!important;"
        "box-shadow:0 24px 60px -18px rgba(118,2,255,0.20)!important;}"
        ".TestimonialsPanel_logo__rFOvF img{filter:brightness(0)!important;height:48px!important;"
        "width:auto!important;max-width:180px!important;object-fit:contain!important;}"
    )
    if "ROASIST_SERVICE_TESTIMONIALS_CSS" not in html:
        if "</style>" in html:
            html = html.replace("</style>", testi_css + "</style>", 1)

    with open(fp, "w", encoding="utf-8") as f:
        f.write(html)
    return True


# ==============================================================================
# STEP 3: UPDATE CONTACT PAGES (/iletisim/ and /start-your-project/)
# ==============================================================================
def build_contact_details_ssr() -> str:
    addr1 = "Roasist Dijital Pazarlama Ajansı<br />\nİstanbul, Türkiye"
    addr2 = f"info@roasist.com<br />\n{OFFICIAL_PHONE_DISPLAY}<br />\nPzt - Cum: 09:00 - 18:00"
    email_blocks = [
        ("Genel Sorular", "info@roasist.com"),
        ("Yeni Proje &amp; Teklif", "info@roasist.com"),
        ("Kariyer &amp; İş Birliği", "info@roasist.com"),
    ]
    emails_ssr = "".join(
        f'<div class="ContactDetails_email__X5toE"><span class="FadeIn_container__bjQVL" data-fill="false">'
        f'<p class="ContactDetails_heading__kxcCU">{label}</p>'
        f'<a class="undefined CopyText_copyText__OtWNq">{addr}'
        f'<div class="CopyText_tooltip__HuxWa ">Copy email address</div></a></span></div>'
        for label, addr in email_blocks
    )
    follow_links = [("WhatsApp", OFFICIAL_WHATSAPP_URL)] + ROASIST_SOCIALS
    follows_ssr = "".join(
        f'<span class="FadeIn_container__bjQVL" data-fill="false">'
        f'<a class="ContactDetails_follow__WB_uR" href="{url}" target="_blank" rel="noopener noreferrer">{name}</a></span>'
        for name, url in follow_links
    )
    return (
        '<section class="ContactDetails_contactDetails__KiaCK">'
        '<div class="DarkThemeSwitch_cover__hn_xc"></div>'
        '<div class="container">'
        '<div class="ContactDetails_left__gBJ4h">'
        '<span class="FadeIn_container__bjQVL" data-fill="false">'
        '<div class="ContactDetails_leftInner__c_hen">'
        '<div class="ContactDetails_addresses__lHCN1">'
        f'<div class="ContactDetails_address__kG_2k"><h3 class="ContactDetails_heading__kxcCU">İstanbul</h3><p>{addr1}</p></div>'
        f'<div class="ContactDetails_address__kG_2k"><h3 class="ContactDetails_heading__kxcCU">İletişim Hattı</h3><p>{addr2}</p></div>'
        "</div>"
        f'<p class="ContactDetails_phone__juaYl"><a href="{OFFICIAL_PHONE_TEL}">{OFFICIAL_PHONE_DISPLAY}</a></p>'
        '<p class="ContactDetails_moreInfo__zOfvU">'
        '<span class="ContactDetails_moreInfo__zOfvU">Hızlıca yanıtlanmasını istediğiniz bir sorunuz mu var?<br />\nHizmetlerimiz :</span> '
        '<a href="/hizmetler/">Roasist ile Çalışmak</a></p>'
        "</div></span></div>"
        '<div class="ContactDetails_right__D3SFA">'
        f"<div>{emails_ssr}</div>"
        '<div class="ContactDetails_follows__KzlYU">'
        '<p class="ContactDetails_heading__kxcCU"><span class="FadeIn_container__bjQVL" data-fill="false">Bizi Takip Edin</span></p>'
        f"{follows_ssr}"
        "</div></div></div></section>"
    )


def update_contact_page(fp: str, is_dist: bool):
    html = open(fp, "r", encoding="utf-8").read()
    new_cd_ssr = build_contact_details_ssr()
    html, n_sub = re.subn(
        r'<section class="ContactDetails_contactDetails__KiaCK">.*?</section>',
        lambda _: new_cd_ssr,
        html,
        count=1,
        flags=re.S,
    )
    if n_sub != 1:
        raise RuntimeError(f"Expected ContactDetails section in {fp}, found {n_sub}")

    img_prefix = f"{CDN_BASE}/images/work" if is_dist else "/images/work"

    def mutator(records):
        changed = False
        for rec in records:
            if rec[0] == "line" and "ContactDetails_contactDetails__KiaCK" in rec[2]:
                ast = json.loads(rec[2])
                # Update $L2a form post-submit thank you data
                main_children = ast[1][3]["children"]
                for child in main_children:
                    if isinstance(child, list) and len(child) >= 4 and isinstance(child[3], dict) and "data" in child[3]:
                        d = child[3]["data"]
                        if "heading" in d and "relatedProjects" in d:
                            d["heading"] = "Mesajınız için teşekkür ederiz!"
                            d["text"] = (
                                "Roasist ekibimiz en kısa sürede sizinle iletişime geçecek. "
                                "Bu sırada öne çıkan başarı hikayelerimizi inceleyebilirsiniz :"
                            )
                            d["relatedProjects"] = [
                                {
                                    "title": "23 Projects",
                                    "slug": "23-projects",
                                    "databaseId": 9001,
                                    "singleProject": {
                                        "projectDetails": {
                                            "yearCompleted": "2025",
                                            "featuredImage": {
                                                "altText": "23 Projects",
                                                "srcSet": None,
                                                "sourceUrl": f"{img_prefix}/23projects.jpg",
                                                "mediaDetails": {"width": 1600, "height": 1000},
                                            },
                                            "featuredVideo": None,
                                        },
                                        "hero": {
                                            "heading": "Küresel gayrimenkul yatırımlarında çok kanallı performans mimarisi."
                                        },
                                    },
                                    "taxonomyServices": {
                                        "edges": [{"node": {"slug": "performans-pazarlamasi", "name": "Performans Pazarlaması"}}]
                                    },
                                    "taxonomySectors": {
                                        "edges": [{"node": {"slug": "gayrimenkul", "name": "Gayrimenkul"}}]
                                    },
                                },
                                {
                                    "title": "Summer Homes",
                                    "slug": "summer-homes",
                                    "databaseId": 9002,
                                    "singleProject": {
                                        "projectDetails": {
                                            "yearCompleted": "2025",
                                            "featuredImage": {
                                                "altText": "Summer Homes",
                                                "srcSet": None,
                                                "sourceUrl": f"{img_prefix}/summerhomes.jpg",
                                                "mediaDetails": {"width": 1600, "height": 1000},
                                            },
                                            "featuredVideo": None,
                                        },
                                        "hero": {
                                            "heading": "Uluslararası yatırımcı kazanımında Google, Meta ve Yandex büyüme stratejisi."
                                        },
                                    },
                                    "taxonomyServices": {
                                        "edges": [{"node": {"slug": "seo", "name": "SEO & Performans"}}]
                                    },
                                    "taxonomySectors": {
                                        "edges": [{"node": {"slug": "gayrimenkul", "name": "Uluslararası Satış"}}]
                                    },
                                },
                            ]

                cd = find_node_by_class(ast, "ContactDetails_contactDetails__KiaCK")
                cd_str = json.dumps(cd, ensure_ascii=False, separators=(",", ":"))
                dark_switch_id = cd[3]["children"][0][1]
                fade_id = re.search(r'"(\$L[0-9a-f]+)",null,\{"delay":0\.25,', cd_str).group(1)
                link_id = re.search(r'"(\$L[0-9a-f]+)",null,\{"href":"/[^"]*"', cd_str).group(1)
                copy_id = re.search(r'"(\$L[0-9a-f]+)",null,\{"text":"info@roasist\.com"', cd_str).group(1)

                email_blocks_fl = [
                    ("0", "Genel Sorular", "info@roasist.com"),
                    ("1", "Yeni Proje & Teklif", "info@roasist.com"),
                    ("2", "Kariyer & İş Birliği", "info@roasist.com"),
                ]
                follow_links = [("WhatsApp", OFFICIAL_WHATSAPP_URL)] + ROASIST_SOCIALS

                new_cd_ast = [
                    "$",
                    "section",
                    None,
                    {
                        "className": "ContactDetails_contactDetails__KiaCK",
                        "children": [
                            ["$", dark_switch_id, None, {}],
                            [
                                "$",
                                "div",
                                None,
                                {
                                    "className": "container",
                                    "children": [
                                        [
                                            "$",
                                            "div",
                                            None,
                                            {
                                                "className": "ContactDetails_left__gBJ4h",
                                                "children": [
                                                    "$",
                                                    fade_id,
                                                    None,
                                                    {
                                                        "children": [
                                                            "$",
                                                            "div",
                                                            None,
                                                            {
                                                                "className": "ContactDetails_leftInner__c_hen",
                                                                "children": [
                                                                    [
                                                                        "$",
                                                                        "div",
                                                                        None,
                                                                        {
                                                                            "className": "ContactDetails_addresses__lHCN1",
                                                                            "children": [
                                                                                [
                                                                                    "$",
                                                                                    "div",
                                                                                    None,
                                                                                    {
                                                                                        "className": "ContactDetails_address__kG_2k",
                                                                                        "children": [
                                                                                            [
                                                                                                "$",
                                                                                                "h3",
                                                                                                None,
                                                                                                {
                                                                                                    "className": "ContactDetails_heading__kxcCU",
                                                                                                    "children": "İstanbul",
                                                                                                },
                                                                                            ],
                                                                                            [
                                                                                                "$",
                                                                                                "p",
                                                                                                None,
                                                                                                {
                                                                                                    "dangerouslySetInnerHTML": {
                                                                                                        "__html": "Roasist Dijital Pazarlama Ajansı<br />\nİstanbul, Türkiye"
                                                                                                    }
                                                                                                },
                                                                                            ],
                                                                                        ],
                                                                                    },
                                                                                ],
                                                                                [
                                                                                    "$",
                                                                                    "div",
                                                                                    None,
                                                                                    {
                                                                                        "className": "ContactDetails_address__kG_2k",
                                                                                        "children": [
                                                                                            [
                                                                                                "$",
                                                                                                "h3",
                                                                                                None,
                                                                                                {
                                                                                                    "className": "ContactDetails_heading__kxcCU",
                                                                                                    "children": "İletişim Hattı",
                                                                                                },
                                                                                            ],
                                                                                            [
                                                                                                "$",
                                                                                                "p",
                                                                                                None,
                                                                                                {
                                                                                                    "dangerouslySetInnerHTML": {
                                                                                                        "__html": f"info@roasist.com<br />\n{OFFICIAL_PHONE_DISPLAY}<br />\nPzt - Cum: 09:00 - 18:00"
                                                                                                    }
                                                                                                },
                                                                                            ],
                                                                                        ],
                                                                                    },
                                                                                ],
                                                                            ],
                                                                        },
                                                                    ],
                                                                    [
                                                                        "$",
                                                                        "p",
                                                                        None,
                                                                        {
                                                                            "className": "ContactDetails_phone__juaYl",
                                                                            "children": [
                                                                                "$",
                                                                                "a",
                                                                                None,
                                                                                {
                                                                                    "href": OFFICIAL_PHONE_TEL,
                                                                                    "children": OFFICIAL_PHONE_DISPLAY,
                                                                                },
                                                                            ],
                                                                        },
                                                                    ],
                                                                    [
                                                                        "$",
                                                                        "p",
                                                                        None,
                                                                        {
                                                                            "className": "ContactDetails_moreInfo__zOfvU",
                                                                            "children": [
                                                                                [
                                                                                    "$",
                                                                                    "span",
                                                                                    None,
                                                                                    {
                                                                                        "className": "ContactDetails_moreInfo__zOfvU",
                                                                                        "dangerouslySetInnerHTML": {
                                                                                            "__html": "Hızlıca yanıtlanmasını istediğiniz bir sorunuz mu var?<br />\nHizmetlerimiz :"
                                                                                        },
                                                                                    },
                                                                                ],
                                                                                [
                                                                                    " ",
                                                                                    [
                                                                                        "$",
                                                                                        link_id,
                                                                                        None,
                                                                                        {
                                                                                            "href": "/hizmetler/",
                                                                                            "children": "Roasist ile Çalışmak",
                                                                                        },
                                                                                    ],
                                                                                ],
                                                                            ],
                                                                        },
                                                                    ],
                                                                ],
                                                            },
                                                        ]
                                                    },
                                                ],
                                            },
                                        ],
                                        [
                                            "$",
                                            "div",
                                            None,
                                            {
                                                "className": "ContactDetails_right__D3SFA",
                                                "children": [
                                                    [
                                                        "$",
                                                        "div",
                                                        None,
                                                        {
                                                            "className": "$undefined",
                                                            "children": [
                                                                [
                                                                    "$",
                                                                    "div",
                                                                    k_idx,
                                                                    {
                                                                        "className": "ContactDetails_email__X5toE",
                                                                        "children": [
                                                                            "$",
                                                                            fade_id,
                                                                            None,
                                                                            {
                                                                                "delay": 0.25,
                                                                                "children": [
                                                                                    [
                                                                                        "$",
                                                                                        "p",
                                                                                        None,
                                                                                        {
                                                                                            "className": "ContactDetails_heading__kxcCU",
                                                                                            "children": lbl,
                                                                                        },
                                                                                    ],
                                                                                    [
                                                                                        "$",
                                                                                        copy_id,
                                                                                        None,
                                                                                        {
                                                                                            "text": addr,
                                                                                            "className": "$undefined",
                                                                                        },
                                                                                    ],
                                                                                ],
                                                                            },
                                                                        ],
                                                                    },
                                                                ]
                                                                for k_idx, lbl, addr in email_blocks_fl
                                                            ],
                                                        },
                                                    ],
                                                    [
                                                        "$",
                                                        "div",
                                                        None,
                                                        {
                                                            "className": "ContactDetails_follows__KzlYU",
                                                            "children": [
                                                                [
                                                                    "$",
                                                                    "p",
                                                                    None,
                                                                    {
                                                                        "className": "ContactDetails_heading__kxcCU",
                                                                        "children": [
                                                                            "$",
                                                                            fade_id,
                                                                            None,
                                                                            {"delay": 0.25, "children": "Bizi Takip Edin"},
                                                                        ],
                                                                    },
                                                                ],
                                                                [
                                                                    [
                                                                        "$",
                                                                        fade_id,
                                                                        None,
                                                                        {
                                                                            "delay": 0.25,
                                                                            "children": [
                                                                                "$",
                                                                                "a",
                                                                                str(idx_f),
                                                                                {
                                                                                    "className": "ContactDetails_follow__WB_uR",
                                                                                    "href": f_url,
                                                                                    "target": "_blank",
                                                                                    "rel": "noopener noreferrer",
                                                                                    "children": f_name,
                                                                                },
                                                                            ],
                                                                        },
                                                                    ]
                                                                    for idx_f, (f_name, f_url) in enumerate(follow_links)
                                                                ],
                                                            ],
                                                        },
                                                    ],
                                                ],
                                            },
                                        ],
                                    ],
                                },
                            ],
                        ],
                    },
                ]
                cd[:] = new_cd_ast
                rec[2] = json.dumps(ast, ensure_ascii=False, separators=(",", ":"))
                changed = True
        return changed

    html = rewrite_flight_in_html(html, mutator)
    with open(fp, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[CONTACT] Updated {os.path.relpath(fp, ROOT)}")


# ==============================================================================
# STEP 4: UNIVERSAL FOOTER SYNCHRONIZER (SSR + FLIGHT) ACROSS ALL KOTA PAGES
# ==============================================================================
def build_footer_ssr(is_dist: bool) -> str:
    badge_prefix = f"{BADGE_CDN}/images" if is_dist else "/images"
    socials_html = "".join(
        f'<a href="{url}" target="_blank" rel="noopener noreferrer">{name}'
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 12.69 12.69">'
        f'<path fill="#fff" stroke-width="0" d="{SOCIAL_ARROW_PATH_D}"></path></svg></a>'
        for name, url in ROASIST_SOCIALS
    )
    last_nav_items = "".join(f'<li><a href="{href}">{lbl}</a></li>' for lbl, href in FOOTER_NAV_TR)
    sector_items = "".join(
        f'<a class="Footer_sectorItem__0Cx14" href="{href}">{lbl}</a>' for lbl, href in FOOTER_SERVICES_TR
    )
    badges = [
        f"{badge_prefix}/badge-google-partner-w.svg",
        f"{badge_prefix}/badge-meta-partner-w.svg",
        f"{badge_prefix}/badge-tiktok-partner-w.svg",
        f"{badge_prefix}/badge-ai-seo-w.svg",
    ]
    badges_html = "".join(f'<img src="{b}" alt=""/>' for b in badges)

    return (
        '<footer class="Footer_footer__pQtti" data-theme="dark">'
        '<div class="container">'
        '<div class="Footer_top__623B4">'
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 820 200" class="Footer_logo__b602f">'
        f'<path fill="#fff" stroke-width="0" d="{ROASIST_LOGO_PATH_D}"></path></svg>'
        '<a class="Footer_email__nLajh CopyText_copyText__OtWNq">info@roasist.com'
        '<div class="CopyText_tooltip__HuxWa ">Copy email address</div></a></div>'
        '<div class="Footer_bottom__wxP7Z">'
        f'<div class="Footer_socialLinks__tA7gt">{socials_html}</div>'
        f'<ul class="Footer_lastNav__at6Kh" data-type="mobile">{last_nav_items}</ul>'
        '<div class="Footer_sectorsWrap__UM4Zx" data-type="mobile">'
        '<span class="Footer_sectorTitle__yEZhb">Hizmetlerimiz :</span>'
        f'<ul class="Footer_sectorMenu__GX7QZ">{sector_items}</ul></div>'
        f'<div class="Footer_logos__jFNys">{badges_html}</div></div>'
        '<div class="Footer_last__auU9C">'
        f'<ul class="Footer_lastNav__at6Kh" data-type="desktop">{last_nav_items}</ul>'
        '<a class="Footer_newsletterButton__wp2hz" href="/iletisim/">Ücretsiz Dijital Analiz Alın</a></div>'
        '<div class="Footer_copyright__j4atB">'
        '<div class="Footer_sectorsWrap__UM4Zx" data-type="desktop">'
        '<span class="Footer_sectorTitle__yEZhb">Hizmetlerimiz :</span>'
        f'<ul class="Footer_sectorMenu__GX7QZ">{sector_items}</ul></div>'
        '<div class="Footer_copyrightTextWrap__uhQWh">'
        '<span class="Footer_copyrightText__f_Lte">© Roasist <!-- -->2026</span>'
        f'<a href="{OFFICIAL_PHONE_TEL}" class="Footer_cyberEssestials__2qh89">{OFFICIAL_PHONE_DISPLAY} • İstanbul</a>'
        "</div></div></div></footer>"
    )


def build_footer_flight_ast(copy_id: str, link_id: str, is_dist: bool) -> list:
    badge_prefix = f"{BADGE_CDN}/images" if is_dist else "/images"
    social_arrow = [
        "$",
        "svg",
        None,
        {
            "xmlns": "http://www.w3.org/2000/svg",
            "viewBox": "0 0 12.69 12.69",
            "children": ["$", "path", None, {"fill": "#fff", "strokeWidth": "0", "d": SOCIAL_ARROW_PATH_D}],
        },
    ]
    social_nodes = [
        [
            "$",
            "a",
            str(idx),
            {
                "href": url,
                "target": "_blank",
                "rel": "noopener noreferrer",
                "children": [name, social_arrow],
            },
        ]
        for idx, (name, url) in enumerate(ROASIST_SOCIALS)
    ]

    def make_last_nav(dtype: str):
        return [
            "$",
            "ul",
            None,
            {
                "className": "Footer_lastNav__at6Kh",
                "data-type": dtype,
                "children": [
                    [
                        "$",
                        "li",
                        None,
                        {"className": "$undefined", "children": ["$", link_id, None, {"href": href, "children": lbl}]},
                    ]
                    for lbl, href in FOOTER_NAV_TR
                ],
            },
        ]

    def make_sectors_wrap(dtype: str):
        return [
            "$",
            "div",
            None,
            {
                "className": "Footer_sectorsWrap__UM4Zx",
                "data-type": dtype,
                "children": [
                    ["$", "span", None, {"className": "Footer_sectorTitle__yEZhb", "children": "Hizmetlerimiz :"}],
                    [
                        "$",
                        "ul",
                        None,
                        {
                            "className": "Footer_sectorMenu__GX7QZ",
                            "children": [
                                [
                                    "$",
                                    link_id,
                                    str(idx),
                                    {"className": "Footer_sectorItem__0Cx14", "href": href, "children": lbl},
                                ]
                                for idx, (lbl, href) in enumerate(FOOTER_SERVICES_TR)
                            ],
                        },
                    ],
                ],
            },
        ]

    badge_nodes = [
        ["$", "img", "4739", {"src": f"{badge_prefix}/badge-google-partner-w.svg", "alt": ""}],
        ["$", "img", "154", {"src": f"{badge_prefix}/badge-meta-partner-w.svg", "alt": ""}],
        ["$", "img", "155", {"src": f"{badge_prefix}/badge-tiktok-partner-w.svg", "alt": ""}],
        ["$", "img", "153", {"src": f"{badge_prefix}/badge-ai-seo-w.svg", "alt": ""}],
    ]

    return [
        "$",
        "footer",
        None,
        {
            "className": "Footer_footer__pQtti",
            "data-theme": "dark",
            "children": [
                "$",
                "div",
                None,
                {
                    "className": "container",
                    "children": [
                        [
                            "$",
                            "div",
                            None,
                            {
                                "className": "Footer_top__623B4",
                                "children": [
                                    [
                                        "$",
                                        "svg",
                                        None,
                                        {
                                            "xmlns": "http://www.w3.org/2000/svg",
                                            "viewBox": "0 0 820 200",
                                            "className": "Footer_logo__b602f",
                                            "children": [
                                                "$",
                                                "path",
                                                None,
                                                {"fill": "#fff", "strokeWidth": "0", "d": ROASIST_LOGO_PATH_D},
                                            ],
                                        },
                                    ],
                                    ["$", copy_id, None, {"text": "info@roasist.com", "className": "Footer_email__nLajh"}],
                                ],
                            },
                        ],
                        [
                            "$",
                            "div",
                            None,
                            {
                                "className": "Footer_bottom__wxP7Z",
                                "children": [
                                    ["$", "div", None, {"className": "Footer_socialLinks__tA7gt", "children": social_nodes}],
                                    make_last_nav("mobile"),
                                    make_sectors_wrap("mobile"),
                                    ["$", "div", None, {"className": "Footer_logos__jFNys", "children": badge_nodes}],
                                ],
                            },
                        ],
                        [
                            "$",
                            "div",
                            None,
                            {
                                "className": "Footer_last__auU9C",
                                "children": [
                                    make_last_nav("desktop"),
                                    [
                                        "$",
                                        link_id,
                                        None,
                                        {
                                            "className": "Footer_newsletterButton__wp2hz",
                                            "href": "/iletisim/",
                                            "children": "Ücretsiz Dijital Analiz Alın",
                                        },
                                    ],
                                ],
                            },
                        ],
                        [
                            "$",
                            "div",
                            None,
                            {
                                "className": "Footer_copyright__j4atB",
                                "children": [
                                    make_sectors_wrap("desktop"),
                                    [
                                        "$",
                                        "div",
                                        None,
                                        {
                                            "className": "Footer_copyrightTextWrap__uhQWh",
                                            "children": [
                                                [
                                                    "$",
                                                    "span",
                                                    None,
                                                    {
                                                        "className": "Footer_copyrightText__f_Lte",
                                                        "children": ["© Roasist ", 2026],
                                                    },
                                                ],
                                                [
                                                    "$",
                                                    "a",
                                                    None,
                                                    {
                                                        "href": OFFICIAL_PHONE_TEL,
                                                        "className": "Footer_cyberEssestials__2qh89",
                                                        "children": f"{OFFICIAL_PHONE_DISPLAY} • İstanbul",
                                                    },
                                                ],
                                            ],
                                        },
                                    ],
                                ],
                            },
                        ],
                    ],
                },
            ],
        },
    ]


def sync_footer_on_kota_page(fp: str, is_dist: bool) -> bool:
    html = open(fp, "r", encoding="utf-8").read()
    if "Footer_footer__pQtti" not in html or "self.__next_f.push" not in html:
        return False

    # Replace preload links in <head> for old KOTA footer badges if present
    badge_prefix = f"{BADGE_CDN}/images" if is_dist else "/images"
    for old_b, new_b in [
        ("https://kota-content.b-cdn.net/app/uploads/2024/06/DAN-1-500x167.png", f"{badge_prefix}/badge-google-partner-w.svg"),
        ("https://kota-content.b-cdn.net/app/uploads/2023/10/clutch.svg", f"{badge_prefix}/badge-meta-partner-w.svg"),
        ("https://kota-content.b-cdn.net/app/uploads/2023/10/awwwards.svg", f"{badge_prefix}/badge-tiktok-partner-w.svg"),
        ("https://kota-content.b-cdn.net/app/uploads/2023/10/cssda.svg", f"{badge_prefix}/badge-ai-seo-w.svg"),
    ]:
        html = html.replace(old_b, new_b)

    new_footer_ssr = build_footer_ssr(is_dist)
    html, n_sub = re.subn(
        r'<footer class="Footer_footer__pQtti".*?</footer>',
        lambda _: new_footer_ssr,
        html,
        count=1,
        flags=re.S,
    )
    if n_sub != 1:
        return False

    def footer_mutator(records):
        changed = False
        for rec in records:
            if rec[0] == "line" and "Footer_footer__pQtti" in rec[2]:
                m_ids = re.search(
                    r'"(\$L[0-9a-f]+)",null,\{"text":"[^"]+","className":"Footer_email__nLajh".*?"(\$L[0-9a-f]+)",null,\{(?:"className":"[^"]+",)?"href":',
                    rec[2],
                )
                if not m_ids:
                    raise RuntimeError(f"Could not extract Footer $L IDs in {fp}")
                copy_id, link_id = m_ids.group(1), m_ids.group(2)
                new_ast = build_footer_flight_ast(copy_id, link_id, is_dist)
                rec[2] = json.dumps(new_ast, ensure_ascii=False, separators=(",", ":"))
                changed = True
        return changed

    html = rewrite_flight_in_html(html, footer_mutator)

    footer_phone_css = (
        "/* ROASIST_FOOTER_PHONE_CSS */"
        ".Footer_cyberEssestials__2qh89{color:rgba(255,255,255,0.86)!important;"
        "text-decoration:none!important;font-size:0.95rem!important;"
        "font-variant-numeric:tabular-nums!important;transition:opacity 0.18s cubic-bezier(0.22,1,0.36,1)!important;}"
        ".Footer_cyberEssestials__2qh89:hover{opacity:1!important;color:#fff!important;}"
        ".Footer_logos__jFNys img{height:38px!important;width:auto!important;max-height:38px!important;object-fit:contain!important;}"
    )
    if "ROASIST_FOOTER_PHONE_CSS" not in html:
        if "</style>" in html:
            html = html.replace("</style>", footer_phone_css + "</style>", 1)
        elif "</head>" in html:
            html = html.replace("</head>", f"<style data-roasist-footer>{footer_phone_css}</style></head>", 1)

    with open(fp, "w", encoding="utf-8") as f:
        f.write(html)
    return True


# ==============================================================================
# STEP 5: PHONE NUMBERS + REFERANSLAR TITLE
# ==============================================================================
def replace_legacy_phones_everywhere():
    phone_pairs = [
        ("541 507 53 50", "540 507 53 50"),
        ("5415075350", "5405075350"),
        ("546 965 70 20", "540 507 53 50"),
        ("5469657020", "5405075350"),
    ]
    count = 0
    for root_name in ("src", "public", "dist"):
        for fp in sorted(glob.glob(os.path.join(ROOT, root_name, "**", "*"), recursive=True)):
            if not os.path.isfile(fp) or not fp.endswith(
                (".html", ".astro", ".ts", ".tsx", ".js", ".json", ".md", ".mdx", ".yaml")
            ):
                continue
            if os.path.basename(fp) == "kota-exact.html":
                continue
            txt = open(fp, "r", encoding="utf-8", errors="ignore").read()
            if not any(old_p in txt for old_p, _ in phone_pairs):
                continue

            if fp.endswith(".html") and "self.__next_f.push" in txt:
                pushes = list(PUSH_RE.finditer(txt))
                first_start = pushes[0].start()
                ssr = txt[:first_start]
                tail = txt[first_start:]
                for old_p, new_p in phone_pairs:
                    ssr = ssr.replace(old_p, new_p)

                def phone_mutator(records):
                    c = False
                    for rec in records:
                        orig = rec[2]
                        val = orig
                        for old_p, new_p in phone_pairs:
                            val = val.replace(old_p, new_p)
                        if val != orig:
                            rec[2] = val
                            c = True
                    return c

                tail = rewrite_flight_in_html(tail, phone_mutator)
                new_txt = ssr + tail
            else:
                new_txt = txt
                for old_p, new_p in phone_pairs:
                    new_txt = new_txt.replace(old_p, new_p)

            if new_txt != txt:
                with open(fp, "w", encoding="utf-8") as f:
                    f.write(new_txt)
                count += 1
                print(f"[PHONE] Updated {os.path.relpath(fp, ROOT)}")
    print(f"[PHONE] Total files updated: {count}")


def fix_referanslar_title():
    old_t = "Our Work | Web Design Portfolio | KOTA Creative Agency"
    new_t = "Referanslar & Başarı Hikayeleri | Roasist"
    for base_name in ("public", "dist"):
        fp = os.path.join(ROOT, base_name, "referanslar", "index.html")
        html = open(fp, "r", encoding="utf-8").read()
        html = html.replace(
            f"<title>{old_t}</title>",
            "<title>Referanslar &amp; Başarı Hikayeleri | Roasist</title>",
        )

        def title_mutator(records):
            c = False
            for rec in records:
                if old_t in rec[2]:
                    rec[2] = rec[2].replace(old_t, new_t)
                    c = True
            return c

        html = rewrite_flight_in_html(html, title_mutator)
        with open(fp, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"[REFERANSLAR] Fixed <title> in {base_name}/referanslar/index.html")


def main():
    # 1. Create Bing Ads detail pages
    create_bing_ads_pages()

    # 2. Update Testimonials on all /hizmetler/... pages (including newly created bing-reklamlari)
    t_count = 0
    for base_name in ("public", "dist"):
        is_dist = base_name == "dist"
        for fp in sorted(glob.glob(os.path.join(ROOT, base_name, "hizmetler", "**", "*.html"), recursive=True)):
            if update_service_testimonials(fp, is_dist):
                t_count += 1
    print(f"[TESTIMONIALS] Updated {t_count} service HTML files (public + dist)")

    # 3. Update Contact & Start-Your-Project pages
    for base_name in ("public", "dist"):
        is_dist = base_name == "dist"
        for slug in ("iletisim", "start-your-project"):
            fp = os.path.join(ROOT, base_name, slug, "index.html")
            if os.path.exists(fp):
                update_contact_page(fp, is_dist)

    # 4. Sync Footer across all KOTA pages in public/ and dist/
    skip_drafts = {
        "kota-exact.html",
        "kota.html",
        "onizleme.html",
        "partner.html",
        "roasist.html",
        "ust-bolum.html",
        "bolum-2.html",
        "bolum-3.html",
        "bolum-4.html",
        "404.html",
    }
    f_count = 0
    for base_name in ("public", "dist"):
        is_dist = base_name == "dist"
        for fp in sorted(glob.glob(os.path.join(ROOT, base_name, "**", "*.html"), recursive=True)):
            if os.path.basename(fp) in skip_drafts:
                continue
            if sync_footer_on_kota_page(fp, is_dist):
                f_count += 1
    print(f"[FOOTER] Synchronized {f_count} KOTA HTML files (public + dist)")

    # 5. Replace any remaining legacy phone numbers across src/, public/, dist/
    replace_legacy_phones_everywhere()

    # 6. Fix Referanslar <title>
    fix_referanslar_title()


if __name__ == "__main__":
    main()
