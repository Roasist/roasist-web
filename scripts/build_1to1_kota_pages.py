#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Builds all Roasist inner pages using KOTA's 1-to-1 Next.js HTML + Flight bundles
from /tmp/kota-clone/reference/pages/, preserving 100% of KOTA's components,
WebGL shaders, GSAP ScrollTrigger animations, Bento video grids, Swiper carousels,
interactive Timeline, and FAQ accordions while localizing all content for Roasist.
"""

import json
import os
import re

ROOT = "/home/antigravity/Roasist/roasist-web"
PUBLIC = os.path.join(ROOT, "public")
DIST = os.path.join(ROOT, "dist")
REF_DIR = "/tmp/kota-clone/reference"
PAGES_DIR = os.path.join(REF_DIR, "pages")

with open(os.path.join(REF_DIR, "routes.json"), "r", encoding="utf-8") as f:
    ROUTES = json.load(f)

with open(os.path.join(ROOT, "scripts", "services_data.json"), "r", encoding="utf-8") as f:
    RAW_SERVICES = json.load(f)

SERVICES_LIST = RAW_SERVICES["servicesData"]
SERVICES_BY_SLUG = {s["slug"]: s for s in SERVICES_LIST}

SCRIPT_RE = re.compile(r'<script[^>]*>\s*self\.__next_f\.push\((\[[\s\S]*?\])\)\s*</script>')

HERO_LINES_BY_SLUG = {
    "seo": ["Aramada", "<em>organik</em>", "liderlik."],
    "performans-pazarlamasi": ["Veri odaklı", "<em>yüksek ROAS</em>", "mimarisi."],
    "360-derece-dijital-pazarlama-yonetimi": ["Tüm kanallarda", "<em>360° entegre</em>", "büyüme."],
    "web-tasarim": ["Dijitalde", "<em>yeni nesil</em>", "web tasarım."],
    "grafik-tasarim": ["Markanız için", "<em>yaratıcı</em>", "tasarım dili."],
    "performans-pazarlamasi/google-reklamlari": ["Karar anında", "<em>Google Ads</em>", "performansı."],
    "performans-pazarlamasi/instagram-reklamlari": ["Hikayelerle", "<em>Instagram'da</em>", "satış gücü."],
    "performans-pazarlamasi/facebook-reklamlari": ["Akıllı veriyle", "<em>Meta Ads</em>", "dönüşümleri."],
    "performans-pazarlamasi/tiktok-reklamlari": ["Trendlerle", "<em>TikTok'ta</em>", "viral büyüme."],
    "performans-pazarlamasi/linkedin-reklamlari": ["B2B dünyada", "<em>LinkedIn ile</em>", "net erişim."],
    "performans-pazarlamasi/yandex-reklamlari": ["Global pazarda", "<em>Yandex Ads</em>", "hakimiyeti."],
}


def transform_with_pairs(text: str, pairs: list[tuple[str, str]]) -> str:
    for old, new in pairs:
        if old and old in text:
            text = text.replace(old, new)
    return text


def localize_flight_stream(flight_text: str, pairs: list[tuple[str, str]], json_pairs: list[tuple[str, str]]) -> str:
    """
    Walks the joined Flight stream, recalculating UTF-8 byte lengths for :T<hex>,
    records and applying JSON-escaped replacements to normal newline-delimited rows.
    """
    buf = flight_text.encode("utf-8")
    cursor = 0
    out_rows = []
    n = len(buf)

    while cursor < n:
        colon = buf.find(b":", cursor)
        nl = buf.find(b"\n", cursor)
        if colon != -1 and (nl == -1 or colon < nl) and colon + 1 < n and buf[colon + 1] == 84:  # 'T'
            rid = buf[cursor:colon].decode("utf-8", errors="ignore")
            comma = buf.find(b",", colon + 2)
            if comma != -1:
                hex_str = buf[colon + 2:comma].decode("utf-8", errors="ignore")
                if re.match(r"^[0-9a-f]+$", rid, re.I) and re.match(r"^[0-9a-f]+$", hex_str, re.I):
                    byte_len = int(hex_str, 16)
                    end = comma + 1 + byte_len
                    raw_val = buf[comma + 1:end].decode("utf-8")
                    new_val = transform_with_pairs(raw_val, pairs)
                    new_hex = f"{len(new_val.encode('utf-8')):x}"
                    out_rows.append(f"{rid}:T{new_hex},{new_val}")
                    cursor = end
                    continue

        end = n if nl == -1 else nl + 1
        line = buf[cursor:end].decode("utf-8")
        line = transform_with_pairs(line, json_pairs)
        line = transform_with_pairs(line, pairs)
        out_rows.append(line)
        cursor = end

    return "".join(out_rows)


def build_json_pairs(pairs: list[tuple[str, str]]) -> list[tuple[str, str]]:
    jp = []
    for old, new in pairs:
        old_j = json.dumps(old, ensure_ascii=False)[1:-1]
        new_j = json.dumps(new, ensure_ascii=False)[1:-1]
        if old_j != old:
            jp.append((old_j, new_j))
        old_u = (
            old_j.replace("&", "\\u0026")
            .replace("<", "\\u003c")
            .replace(">", "\\u003e")
            .replace("'", "\\u0027")
        )
        new_u = (
            new_j.replace("&", "\\u0026")
            .replace("<", "\\u003c")
            .replace(">", "\\u003e")
        )
        if old_u != old_j:
            jp.append((old_u, new_u))
    return jp


def build_html_pairs(pairs: list[tuple[str, str]]) -> list[tuple[str, str]]:
    hp = list(pairs)
    for old, new in pairs:
        old_e = old.replace("&", "&amp;").replace("'", "&#x27;")
        new_e = new.replace("&", "&amp;")
        if old_e != old:
            hp.append((old_e, new_e))
        old_e2 = old_e.replace("’", "&#x27;")
        if old_e2 != old_e:
            hp.append((old_e2, new_e))
    return hp


COMMON_PAIRS = [
    # Fix URL-encoded dynamic chunk paths so static servers / jsDelivr resolve them
    ("/_next/static/chunks/app/service/%5Bslug%5D/", "/_next/static/chunks/app/service/[slug]/"),
    ("static/chunks/app/service/%5Bslug%5D/", "static/chunks/app/service/[slug]/"),
    ("/_next/static/chunks/app/blog/%5Bslug%5D/", "/_next/static/chunks/app/blog/[slug]/"),
    ("static/chunks/app/blog/%5Bslug%5D/", "static/chunks/app/blog/[slug]/"),
    ("/_next/static/chunks/app/work/%5Bslug%5D/", "/_next/static/chunks/app/work/[slug]/"),
    ("static/chunks/app/work/%5Bslug%5D/", "static/chunks/app/work/[slug]/"),
    ("/_next/static/chunks/app/%5Bslug%5D/", "/_next/static/chunks/app/[slug]/"),
    ("static/chunks/app/%5Bslug%5D/", "static/chunks/app/[slug]/"),

    # Header & Navigation Menu
    ("Celebrating 13 years : 2013 -", "Dijital Büyüme & Performans :"),
    ("Hire us", "Bize Ulaşın"),
    ('"viewBox":"0 0 90 90"', '"viewBox":"0 0 820 200"'),
    ('viewBox="0 0 90 90"', 'viewBox="0 0 820 200"'),
    ('M5 5h80v80H5V5zM0 90h90V0H0v90zm64.66-15.67l-5.15-16.61h-.1l-5.35 16.61H47.6l9.49-24.09h4.74l9.39 24.09h-6.56zm-39.77 0V55.67h-6.66v-5.43H37.6v5.43h-6.66v18.66h-6.06zm34.52-59.16c-3.94-.1-7.67 1.74-9.99 4.92-.64.81-1.15 1.7-1.52 2.67-.6 1.64-.9 3.38-.9 5.13v.05c.07 6.78 5.62 12.22 12.4 12.15h.56c6.88-.29 12.22-6.1 11.93-12.97-.28-6.69-5.79-11.96-12.48-11.94m.1 19.48c-3.94 0-6.56-3.38-6.56-7.18s2.62-6.97 6.46-6.97 6.46 3.38 6.46 7.07-2.52 7.08-6.36 7.08m-28.87 5.02l-6.46-10.35h-.1v10.35h-6.06v-24.1h6.06v10.87h.1l6.66-10.87h6.36l-7.87 12 8.38 12.1h-7.06z', 'M176.71,198.48v1.32l-35.19.2c-1.72-2.67-2.88-6.5-3.64-11.52-.59-4.79-1.15-10-1.55-15.35s-.56-10.76-1-15.75a95,95,0,0,0-1.16-12.48c-1-4.42-2.51-8.08-4.62-10.56a20.66,20.66,0,0,0-7.46-6.17,32.19,32.19,0,0,0-9.81-2.88c-3.66-.36-7.29-.56-11.15-.56h-47v-35h56.29v18.62L164.6,77.1,110.46,45.8V64.42H54.17v16L0,49.07,54.17,17.74V34.08h64.9c18.26,0,32.29,3.47,41.89,10.17,9.78,6.93,14.6,18.06,14.6,33.41,0,10.4-2.12,18.85-6.34,24.79C165,108.79,158.06,114,148.65,118.2a28.6,28.6,0,0,1,11.52,7.29,35.16,35.16,0,0,1,6.18,11.13A60.62,60.62,0,0,1,169,149.69c.4,4.62.56,9.21.76,13.44.2,6.33.4,11.52.79,15.74.36,4.06,1,7.5,1.32,10A24.35,24.35,0,0,0,174,195,8.76,8.76,0,0,0,176.71,198.48Z M186,84q1.68-15.32,7.38-26.28a41.37,41.37,0,0,1,16.45-17.12q10.74-6.15,28.86-6.15t28.86,6.15A41.37,41.37,0,0,1,284,57.73q5.7,11,7.38,26.28a308.26,308.26,0,0,1,1.68,33.45A307.5,307.5,0,0,1,291.39,151q-1.68,15.21-7.38,26.17A39.24,39.24,0,0,1,267.56,194q-10.74,5.82-28.86,5.82T209.84,194a39.24,39.24,0,0,1-16.45-16.78Q187.69,166.25,186,151a307.5,307.5,0,0,1-1.68-33.57A308.26,308.26,0,0,1,186,84Zm31.32,60.86a76.29,76.29,0,0,0,3.13,18.35q2.35,7,6.72,10.29c2.91,2.17,6.74,3.25,11.52,3.25s8.61-1.08,11.52-3.25,5.15-5.59,6.71-10.29a76.24,76.24,0,0,0,3.14-18.35q.78-11.3.78-27.41t-.78-27.29a77.72,77.72,0,0,0-3.14-18.35q-2.34-7.16-6.71-10.4T238.7,58.17c-4.78,0-8.61,1.09-11.52,3.25s-5.15,5.63-6.72,10.4a77.78,77.78,0,0,0-3.13,18.35q-.78,11.19-.78,27.29T217.33,144.87Z M383,37.59,425.3,197.34H391.74l-7.39-33.79H341.84l-7.38,33.79H300.9L343.19,37.59Zm-4.25,99.56L363.32,65.33h-.44l-15.44,71.82Z M462.44,152.14a53,53,0,0,0,.9,10.18,17.61,17.61,0,0,0,3.35,7.72,16.6,16.6,0,0,0,6.6,4.93,26.39,26.39,0,0,0,10.41,1.79A20.56,20.56,0,0,0,497,172q5.92-4.81,5.93-14.88a26.93,26.93,0,0,0-1.45-9.29,18.47,18.47,0,0,0-4.82-7.05,34.1,34.1,0,0,0-8.83-5.7,126.18,126.18,0,0,0-13.54-5.26,115.68,115.68,0,0,1-18.57-7.83,49.79,49.79,0,0,1-13.09-10,35.53,35.53,0,0,1-7.72-13.2,55.56,55.56,0,0,1-2.46-17.34q0-23.72,13.2-35.35t36.25-11.63a79.06,79.06,0,0,1,19.8,2.34,41.63,41.63,0,0,1,15.66,7.61,35.58,35.58,0,0,1,10.29,13.43q3.69,8.16,3.69,19.57v4.48H500.48q0-11.42-4-17.56T483,58.17a22.43,22.43,0,0,0-8.95,1.57,15.1,15.1,0,0,0-5.71,4.14,14.16,14.16,0,0,0-2.91,5.93,30.48,30.48,0,0,0-.78,6.93,23.06,23.06,0,0,0,3.13,12.42q3.13,5,13.43,9.29l24.83,10.74a75.73,75.73,0,0,1,15,8.39,41,41,0,0,1,9.29,9.39,31.46,31.46,0,0,1,4.81,11.08,62.31,62.31,0,0,1,1.34,13.42q0,25.29-14.65,36.81T481,199.8q-27.3,0-39-11.86t-11.75-34v-6.48h32.22Z M554.17,37.59h32.22V197.34H554.17ZM582.81,26.4H557.75V0h25.06Z M636.29,152.14a53.81,53.81,0,0,0,.89,10.18,17.74,17.74,0,0,0,3.36,7.72,16.6,16.6,0,0,0,6.6,4.93,26.37,26.37,0,0,0,10.4,1.79A20.59,20.59,0,0,0,670.86,172q5.92-4.81,5.93-14.88a26.68,26.68,0,0,0-1.46-9.29,18.33,18.33,0,0,0-4.81-7.05,34.17,34.17,0,0,0-8.84-5.7,125.1,125.1,0,0,0-13.53-5.26,115.68,115.68,0,0,1-18.57-7.83,49.63,49.63,0,0,1-13.09-10,35.53,35.53,0,0,1-7.72-13.2,55.56,55.56,0,0,1-2.46-17.34q0-23.72,13.2-35.35t36.24-11.63a79.2,79.2,0,0,1,19.81,2.34,41.63,41.63,0,0,1,15.66,7.61,35.58,35.58,0,0,1,10.29,13.43Q705.2,66,705.2,77.41v4.48H674.33q0-11.42-4-17.56t-13.43-6.16a22.46,22.46,0,0,0-9,1.57,15,15,0,0,0-5.7,4.14,14.16,14.16,0,0,0-2.91,5.93,29.93,29.93,0,0,0-.78,6.93,23.06,23.06,0,0,0,3.13,12.42q3.14,5,13.42,9.29l24.84,10.74a76,76,0,0,1,15,8.39A41,41,0,0,1,704.2,127a31.44,31.44,0,0,1,4.8,11.08,61.66,61.66,0,0,1,1.35,13.42q0,25.29-14.66,36.81T654.86,199.8q-27.3,0-39-11.86t-11.75-34v-6.48h32.22Z M820,64h-34.9V197.34H752.86V64H718V37.59H820Z'),
    ("Start your project", "Projeye Başlayın"),
    ('"label":"Work","uri":"https://kota.co.uk/work/"', '"label":"Referanslar","uri":"/referanslar/"'),
    ('"label":"Agency","uri":"https://kota.co.uk/agency/"', '"label":"Hakkımızda","uri":"/hakkimizda/"'),
    ('"label":"Services","uri":"https://kota.co.uk/service/"', '"label":"Hizmetler","uri":"/hizmetler/"'),
    ('"label":"Blog","uri":"https://kota.co.uk/blog/"', '"label":"Blog","uri":"/blog/"'),
    ('"label":"Culture","uri":"https://kota.co.uk/culture/"', '"label":"360° Pazarlama","uri":"/hizmetler/360-derece-dijital-pazarlama-yonetimi/"'),
    ('"label":"Contact","uri":"https://kota.co.uk/contact/"', '"label":"İletişim","uri":"/iletisim/"'),

    # LargeCta (Bottom of pages)
    ("Interested in working with KOTA?", "Markanızı Roasist ile büyütmeye hazır mısınız?"),
    (
        '<p>Drop us a line at<br />\n<a href="mailto:hello@kota.co.uk">hello@kota.co.uk</a></p>\n',
        '<p>Bize hemen ulaşın:<br />\n<a href="mailto:info@roasist.com">info@roasist.com</a></p>\n',
    ),
    (
        "We are a Creative Digital Agency based in Clerkenwell London, specialising in Creative Web Design, Web Development, Branding and Digital Marketing.",
        "Performans pazarlaması, Google & Meta reklamları, SEO, kreatif tasarım ve web yazılım çözümleriyle markanızı kârlı biçimde ölçeklendiren 360° dijital büyüme ajansıyız.",
    ),

    # Footer
    ('"children":"Home"', '"children":"Ana Sayfa"'),
    ('"href":"/work","children":"Work"', '"href":"/referanslar/","children":"Referanslar"'),
    ('"href":"/agency","children":"Agency"', '"href":"/hakkimizda/","children":"Hakkımızda"'),
    ('"href":"/services","children":"Services"', '"href":"/hizmetler/","children":"Hizmetler"'),
    ('"href":"/contact","children":"Contact"', '"href":"/iletisim/","children":"İletişim"'),
    ('"href":"/faqs","children":"FAQs"', '"href":"/hizmetler/","children":"S.S.S."'),
    ('"href":"/privacy-policy","children":"Privacy Policy"', '"href":"/gizlilik-politikasi-ve-kullanim-sartlari/","children":"Gizlilik Politikası"'),
    ('"href":"/terms-conditions","children":"Terms & Conditions"', '"href":"/gizlilik-politikasi-ve-kullanim-sartlari/","children":"Kullanım Şartları"'),
    ("newbiz@kota.co.uk", "info@roasist.com"),
    ("hello@kota.co.uk", "info@roasist.com"),
    ("+44(0)20 3951 0562", "+90 546 965 70 20"),
    ("+442039510562", "+905469657020"),
    ('"children":"LONDON"', '"children":"İSTANBUL"'),
    ("1-5 Clerkenwell Road<br/>London EC1M 5PA", "Maslak, Büyükdere Cad.<br/>Sarıyer / İstanbul"),
    ('"children":"NEW YORK"', '"children":"GLOBAL"'),
    ("477 Madison Avenue<br/>Midtown Manhattan<br/>6th Floor, NY 10022", "Türkiye, Avrupa &amp; MENA<br/>360° Dijital Büyüme Ajansı"),
    ('"children":"Awwwards"', '"children":"Google Partner"'),
    ('"children":"CSS Design Awards"', '"children":"Meta Partner"'),
    ('"children":"The Lovies"', '"children":"TikTok Partner"'),
    ('"children":"FWA"', '"children":"Yandex Partner"'),
    ("© KOTA ", "© Roasist "),
    ("https://www.instagram.com/kotacreative/", "https://www.instagram.com/roasist/"),
    ("https://www.linkedin.com/company/kota-creative/", "https://www.linkedin.com/company/roasist/"),

    # Testimonials (shared across service pages)
    ("What our clients say.", "Müşterilerimiz Ne Diyor?"),
    (
        '"As a design agency, handing responsibility for our web re-design to another creative agency needed to be well considered. We were immediately impressed by their designs and their interpretation of our brief. Nice bunch of people to work with too!"',
        '"Roasist ekibiyle çalışmaya başladıktan sonra dijital reklam bütçemizin verimliliği tamamen değişti. Veri odaklı yaklaşımları, şeffaf raporlamaları ve yüksek ROAS performanslarıyla hedeflerimizi kısa sürede aştık."',
    ),
    ("Laurie Bushe", "Ahmet Yılmaz"),
    ("Head of Marketing", "Pazarlama Direktörü"),
    (
        '"It was our brand positioning work that really made everything click. KOTA were empathetic, patient, flexible, quick, and, most importantly, incredibly talented with brand positioning, visual identity, and digital experiences. I\'ve already recommended them twice!"',
        '"Marka konumlandırmamızdan web sitemize ve performans kampanyalarımıza kadar 360 derece tüm dijital süreçlerimizi tek çatı altında kusursuz yönetiyorlar. Hem kreatif vizyonları hem de teknik hızları olağanüstü."',
    ),
    ("Shanice Daeche", "Zeynep Kaya"),
    (
        '"Beyond the aesthetics, the site is incredibly functional. The CMS gives us the flexibility and control we need to keep our content fresh and relevant, and they have significantly improved the website’s UX. We couldn\'t be happier!"',
        '"Sadece estetik değil, aynı zamanda yüksek dönüşüm üreten bir dijital altyapı kurdular. SEO ve performans pazarlaması entegrasyonu sayesinde organik ve reklam trafiğimiz katlanarak büyüdü."',
    ),
    ("Jenny Frame", "Murat Demir"),
    ("Marketing Manager", "E-Ticaret Yöneticisi"),

    # Related Articles & Related Projects (shared across service pages)
    ("Related Articles", "İlgili Blog Yazıları"),
    ("View all articles", "Tüm Yazıları Gör"),
    ("https://kota.co.uk/blog", "/blog/"),
    ("Inspiration", "Strateji"),
    ("Expertise", "Rehber"),
    (
        "10 creative websites to inspire your next design (2025 update)",
        "Performans Pazarlaması Nedir? Markanızı Nasıl Ölçeklendirir?",
    ),
    (
        "AI Search, zero-click SEO and Google’s May update",
        "Veriye Dayalı Dijital Pazarlama Stratejisi Nedir?",
    ),
    (
        "10 tips for choosing the right web design agency",
        "Reklam Harcamalarının Geri Dönüşü (ROAS) Nasıl Hesaplanır?",
    ),
    (
        "How long does it take to design and build a website?",
        "E-Ticaret Siteleri İçin Dönüşüm Oranı Optimizasyonu (CRO)",
    ),
    (
        "Behind the scenes at KOTA: Web Design process",
        "Google Ads ve Meta Reklamlarında Bütçe Yönetimi İpuçları",
    ),
    (
        "Bad UX is killing your SEO, conversions and trust — here’s how to fix it",
        "Kullanıcı Deneyimi (UX) SEO ve Dönüşüm Oranlarını Nasıl Etkiler?",
    ),

    ("Related Projects", "Başarı Hikayelerimiz"),
    ("View all projects", "Tüm Referansları Gör"),
    ("https://kota.co.uk/work/tangerine/", "/referanslar/"),
    ("https://kota.co.uk/work/florence/", "/referanslar/"),
    ("https://kota.co.uk/work/incentive-games/", "/referanslar/"),
    ("https://kota.co.uk/work/pixelartworks/", "/referanslar/"),
    ("https://kota.co.uk/work/wogan-coffee/", "/referanslar/"),
    ("https://kota.co.uk/work/dka/", "/referanslar/"),
    ("https://kota.co.uk/work/isi-global/", "/referanslar/"),
    ("https://kota.co.uk/work", "/referanslar/"),
    (
        "A cinematic web experience for a Hollywood powerhouse.",
        "Küresel ölçekte yüksek dönüşümlü dijital deneyim ve performans mimarisi.",
    ),
    (
        "We designed for play with Incentive Games’ new website.",
        "Veri odaklı UX/UI tasarımı ve çok kanallı büyüme stratejisi.",
    ),
    (
        "Influence everywhere: a future-ready website for The Goat Agency.",
        "Yeni nesil performans pazarlaması ve kreatif dijital dönüşüm.",
    ),
    (
        "A brand-led digital transformation for a global platform.",
        "B2B ve kurumsal markalar için uçtan uca dijital dönüşüm.",
    ),
    (
        "We completely transformed the image of Bristol's finest coffee company.",
        "E-ticaret satışlarını ve ROAS verimliliğini katlayan 360° büyüme projesi.",
    ),
    (
        "We designed two industry-leading websites for DK&A, showcasing their services and courses.",
        "Sektör lideri markalar için yüksek hızlı web ve SEO mimarisi.",
    ),
    ("B2B tech, software & SaaS", "B2B Teknoloji & Yazılım"),
    ("Agencies", "Kurumsal"),
    ("Digital Marketing", "Dijital Pazarlama"),
    ("E-Commerce", "E-Ticaret"),
    ("Retail", "Perakende"),

    # Common labels
    ("FAQ's", "Sıkça Sorulan Sorular"),
    ("Discover more", "Diğer Hizmetlerimiz"),
    ("Find out more", "Detaylı İncele"),
    ("View project", "Projeyi İncele"),
]


RUNTIME_HELPER_TEMPLATE = """<script data-roasist-runtime>
window.__KOTA_HYDRATE_PATH__ = __HYDRATE_PATH_JSON__;
(function(){
  try {
    var play = HTMLMediaElement.prototype.play;
    HTMLMediaElement.prototype.play = function() {
      var p = play.call(this);
      return p && p.catch ? p.catch(function(e){ if (e && e.name !== 'AbortError') throw e; }) : p;
    };
  } catch(e) {}

  function mapKotaHref(rawHref) {
    if (!rawHref) return rawHref;
    var base = window.__ROASIST_BASE__ || (window.location.pathname.startsWith('/roasist-web') ? '/roasist-web' : '');
    var h = rawHref.replace(/^https?:\\/\\/(?:www\\.)?kota\\.co\\.uk/i, '');
    if (h === '/work' || h === '/work/' || h.startsWith('/work/')) h = '/referanslar/';
    else if (h === '/agency' || h === '/agency/' || h === '/culture' || h === '/culture/') h = '/hakkimizda/';
    else if (h === '/contact' || h === '/contact/') h = '/iletisim/';
    else if (h === '/services' || h === '/service' || h === '/service/') h = '/hizmetler/';
    else if (h === '/faqs' || h === '/faqs/') h = '/hizmetler/';
    else if (h === '/privacy-policy' || h === '/privacy-policy/' || h === '/terms-conditions' || h === '/terms-conditions/') h = '/gizlilik-politikasi-ve-kullanim-sartlari/';
    else if (h === '/blog/Performans-Pazarlamasi-Nedir' || h.indexOf('inspire-your-next-design') !== -1) h = '/blog/Performans-Pazarlamasi-Nedir/';
    else if (h.indexOf('ai-search-zero-click-seo') !== -1) h = '/blog/Veriye-Dayali-Dijital-Pazarlama-Stratejisi-Nedir/';
    else if (h.indexOf('choosing-the-right-web-design-agency') !== -1) h = '/blog/Reklam-Harcamalarinin-Geri-Donusu-ROAS-Nasil-Hesaplanir/';
    else if (h.startsWith('/blog/') && h !== '/blog/' && !h.startsWith('/blog/Performans') && !h.startsWith('/blog/Veriye') && !h.startsWith('/blog/Reklam') && !h.startsWith('/blog/kategori') && !h.startsWith('/blog/etiket')) h = '/blog/';
    else if (h.startsWith('/service/')) {
      var slug = h.replace('/service/', '').replace(/\\/$/, '');
      var map = {
        'web-design-development': '/hizmetler/web-tasarim/',
        'creative-web-design': '/hizmetler/web-tasarim/',
        'web-development': '/hizmetler/web-tasarim/',
        'wordpress-cms': '/hizmetler/web-tasarim/',
        'e-commerce': '/hizmetler/performans-pazarlamasi/',
        'branding': '/hizmetler/grafik-tasarim/',
        'brand-strategy-and-identity': '/hizmetler/grafik-tasarim/',
        'graphic-design': '/hizmetler/grafik-tasarim/',
        'digital-marketing': '/hizmetler/360-derece-dijital-pazarlama-yonetimi/',
        'growth-marketing': '/hizmetler/performans-pazarlamasi/',
        'seo-geo': '/hizmetler/seo/'
      };
      h = map[slug] || ('/hizmetler/' + slug + '/');
    }
    if (h.startsWith('/') && !h.startsWith('//') && base && !h.startsWith(base + '/') && h !== base) {
      h = base + (h === '/' ? '/' : h);
    }
    return h;
  }

  document.addEventListener('click', function(event) {
    var anchor = event.target && event.target.closest ? event.target.closest('a[href]') : null;
    if (!anchor) return;
    var raw = anchor.getAttribute('href');
    if (!raw || raw.startsWith('#') || raw.startsWith('mailto:') || raw.startsWith('tel:') || raw.startsWith('javascript:')) return;
    var mapped = mapKotaHref(raw);
    if (mapped && (mapped.startsWith('/') || mapped.startsWith(window.location.origin))) {
      if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey || anchor.target === '_blank') return;
      event.preventDefault();
      event.stopImmediatePropagation();
      window.location.href = mapped;
    }
  }, true);

  function decorateHeaderLogo() {
    var logoLink = document.querySelector('a[class*="Header_logo"]');
    if (logoLink) {
      var base = window.__ROASIST_BASE__ || (window.location.pathname.startsWith('/roasist-web') ? '/roasist-web' : '');
      logoLink.setAttribute('href', base ? base + '/' : '/');
    }
  }

  function initFaq() {
    document.querySelectorAll('label[class*="FaqsList_question"]').forEach(function(q) {
      if (q.dataset.roasistFaq) return;
      q.dataset.roasistFaq = '1';
      var input = q.querySelector('input[type="checkbox"]');
      var ans = q.nextElementSibling;
      if (input && ans) {
        ans.addEventListener('transitionend', function() {
          if (window.lenis && window.lenis.resize) window.lenis.resize();
        });
      }
    });
  }

  document.addEventListener('DOMContentLoaded', function() {
    decorateHeaderLogo();
    initFaq();
    setTimeout(decorateHeaderLogo, 400);
    setTimeout(decorateHeaderLogo, 1200);
  });
  new MutationObserver(function() {
    decorateHeaderLogo();
    initFaq();
  }).observe(document.documentElement, { childList: true, subtree: true });
})();
</script>
<style data-roasist-theme>
:root {
  --color-primary: #7602FF !important;
}
/* Roasist Desktop Scroll-Only Liquid Glass Navigation Bar */
@media (max-width: 768px) {
  .Hero_hero__18Xqo > h1, .Hero_hero__drBQ0 > h1 { left: calc(7vw + 9.75rem) !important; }
}
@media (min-width: 769px) and (max-width: 1919px) {
  .Hero_hero__18Xqo > h1, .Hero_hero__drBQ0 > h1 { left: 13.5rem !important; top: 2.55rem !important; }
}
@media screen and (min-width: 1920px) {
  .Hero_hero__18Xqo > h1, .Hero_hero__drBQ0 > h1 { left: 50% !important; transform: translateX(-50%) !important; padding: 0 13.5rem !important; top: 2.55rem !important; }
}
@media (min-width: 769px) {
  .Header_header__KwdYD::before {
    content: "";
    position: absolute;
    top: 0.85rem;
    left: 0.85rem;
    right: 0.85rem;
    bottom: 0.85rem;
    border-radius: 999px;
    pointer-events: none;
    z-index: -1;
    opacity: 0;
    transform: translateY(-6px);
    transition: opacity 0.35s cubic-bezier(0.22, 1, 0.36, 1), transform 0.35s cubic-bezier(0.22, 1, 0.36, 1), background 0.35s ease, border-color 0.35s ease, box-shadow 0.35s ease;
    background: linear-gradient(
      135deg,
      rgba(255, 255, 255, 0.62) 0%,
      rgba(255, 255, 255, 0.28) 45%,
      rgba(245, 238, 255, 0.48) 100%
    );
    backdrop-filter: blur(22px) saturate(190%) contrast(104%);
    -webkit-backdrop-filter: blur(22px) saturate(190%) contrast(104%);
    border: 1px solid rgba(255, 255, 255, 0.78);
    box-shadow:
      0 10px 32px -6px rgba(18, 12, 38, 0.10),
      0 2px 8px rgba(118, 2, 255, 0.06),
      inset 0 1.5px 1px rgba(255, 255, 255, 0.92),
      inset 0 -1px 1.5px rgba(118, 2, 255, 0.08);
  }
  body.roasist-scrolled .Header_header__KwdYD::before {
    opacity: 1;
    transform: translateY(0);
  }
  body.dark.roasist-scrolled .Header_header__KwdYD::before {
    background: linear-gradient(
      135deg,
      rgba(28, 22, 46, 0.58) 0%,
      rgba(18, 14, 30, 0.36) 50%,
      rgba(52, 18, 96, 0.44) 100%
    );
    border: 1px solid rgba(255, 255, 255, 0.18);
    box-shadow:
      0 12px 36px -6px rgba(0, 0, 0, 0.42),
      0 2px 12px rgba(118, 2, 255, 0.18),
      inset 0 1px 1px rgba(255, 255, 255, 0.28),
      inset 0 -1px 1.5px rgba(118, 2, 255, 0.22);
  }
}
</style>"""


def render_kota_template(ref_route: str, extra_pairs: list[tuple[str, str]], hydrate_path: str | None = None) -> str:
    hf = ROUTES[ref_route]
    html_path = os.path.join(PAGES_DIR, hf)
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    all_pairs = extra_pairs + COMMON_PAIRS
    json_pairs = build_json_pairs(all_pairs)
    html_pairs = build_html_pairs(all_pairs)

    parts = []
    placeholder = "<!--__ROASIST_FLIGHT_STREAM__-->"
    first = True

    def replace_script(match):
        nonlocal first
        raw_script = match.group(0)
        data_str = match.group(1)
        try:
            val = json.loads(data_str)
        except Exception:
            return raw_script
        if not isinstance(val, list) or len(val) < 2 or val[0] != 1:
            return raw_script
        parts.append(val[1])
        if first:
            first = False
            return placeholder
        return ""

    html = SCRIPT_RE.sub(replace_script, html)
    html = transform_with_pairs(html, html_pairs)

    if parts:
        joined_flight = "".join(parts)
        localized_flight = localize_flight_stream(joined_flight, all_pairs, json_pairs)
        payload = json.dumps([1, localized_flight], ensure_ascii=False).replace("<", "\\u003c")
        html = html.replace(placeholder, f"<script>self.__next_f.push({payload})</script>")

    html = re.sub(
        r'<script[^>]*src="https://(?:www\.)?(?:googletagmanager\.com|vercel\.live)[^>]*></script>',
        "",
        html,
    )

    hp = hydrate_path if hydrate_path is not None else ref_route
    helper = RUNTIME_HELPER_TEMPLATE.replace("__HYDRATE_PATH_JSON__", json.dumps(hp))
    html = html.replace("<head>", "<head>" + helper, 1)
    return html


def write_page(rel_path: str, content: str):
    for root_dir in (PUBLIC, DIST):
        full_path = os.path.join(root_dir, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)


def normalize_service_dict(svc: dict) -> dict:
    slug = svc.get("slug", "")
    h1 = svc["h1"]
    title = svc.get("seoTitle") or svc.get("title") or f"{h1} | Roasist"
    meta_desc = svc.get("seoDescription") or svc.get("metaDesc") or svc.get("aeoDirectAnswer", "")
    lines = svc.get("heroLines") or HERO_LINES_BY_SLUG.get(slug, ["Dijitalde", "<em>gerçek büyüme</em>", "mimarisi."])
    intro_text = svc.get("introText") or svc.get("aeoDirectAnswer") or meta_desc
    intro_heading = svc.get("introHeading") or svc.get("overviewHeading") or f"{h1} Nedir?"
    overview_pars = svc.get("overviewParagraphs", [])
    intro_body = svc.get("introBody") or (" ".join(overview_pars[:2]) if overview_pars else intro_text)

    raw_feats = svc.get("features") or svc.get("subFeatures") or []
    feats = []
    for rf in raw_feats[:3]:
        feats.append({
            "title": rf.get("title", "Stratejik Optimizasyon."),
            "text": rf.get("text") or rf.get("description", intro_body),
            "href": rf.get("href", "/iletisim/"),
        })
    while len(feats) < 3:
        feats.append({"title": "Veri Odaklı Optimizasyon.", "text": intro_body, "href": "/iletisim/"})

    raw_metrics = svc.get("metrics", [])
    metrics = []
    default_stat_nums = ["+185%", "6.4x", "-38%", "+210%"]
    for i, rm in enumerate(raw_metrics[:4]):
        val = rm.get("value", default_stat_nums[i % 4])
        lbl = rm.get("detail") or rm.get("label", "Veri odaklı büyüme performansı.")
        if not any(ch.isdigit() for ch in val):
            lbl = f"{val} — {lbl}"
            val = default_stat_nums[i % 4]
        metrics.append({"value": val, "label": lbl})
    while len(metrics) < 4:
        idx = len(metrics)
        metrics.append({"value": default_stat_nums[idx % 4], "label": "Ortalama dönüşüm ve ROAS artışı."})

    raw_steps = svc.get("processSteps", [])
    steps = []
    for rs in raw_steps:
        steps.append({
            "title": rs.get("title", "Optimizasyon"),
            "text": rs.get("text") or rs.get("description", intro_body),
        })
    extra_steps = [
        {
            "title": "Kreatif & A/B Testleri",
            "text": "Reklam kreatiflerini, açılış sayfası mesajlarını ve eylem çağrılarını (CTA) sürekli A/B testlerine tabi tutarak en yüksek dönüşüm getiren varyasyonları ölçeklendiriyoruz.",
        },
        {
            "title": "Büyüme & Ölçeklendirme",
            "text": "Kanıtlanmış ROAS ve CPA hedeflerine ulaşıldığında bütçenizi yeni hedef kitle segmentlerine ve uluslararası pazarlara kârlı biçimde genişletiyoruz.",
        },
    ]
    while len(steps) < 8:
        steps.append(extra_steps[len(steps) % 2])

    raw_faqs = svc.get("faqs", [])
    faqs = []
    for rf in raw_faqs:
        faqs.append({
            "q": rf.get("q") or rf.get("question", f"{h1} süreci nasıl işler?"),
            "a": rf.get("a") or rf.get("answer", intro_body),
        })
    extra_faqs = [
        {
            "q": f"{h1} sürecinde raporlama ve şeffaflık nasıl sağlanır?",
            "a": "Tüm reklam ve analitik hesaplarınız kendi mülkiyetinizde kalır. Canlı Looker Studio veri panellerimizle harcanan bütçeyi, dönüşümleri ve ROAS performansını 7/24 anlık olarak takip edebilirsiniz.",
        },
        {
            "q": f"Roasist ile {h1} çalışmalarına nasıl başlayabiliriz?",
            "a": "İletişim sayfamızdan veya 'Projeye Başlayın' butonundan bize ulaştığınızda, mevcut dijital varlıklarınızı ücretsiz analiz ediyor ve markanıza özel büyüme yol haritasını sunuyoruz.",
        },
    ]
    while len(faqs) < 6:
        faqs.append(extra_faqs[len(faqs) % 2])

    return {
        "title": title,
        "metaDesc": meta_desc,
        "h1": h1,
        "heroLines": lines,
        "introText": intro_text,
        "introHeading": intro_heading,
        "introBody": intro_body,
        "features": feats,
        "metrics": metrics,
        "processHeading": svc.get("processTitle") or svc.get("processHeading") or f"{h1} Sürecimiz.",
        "processSubheading": svc.get(
            "processSubheading",
            "Analiz ve stratejiden kurulum, kreatif üretim, test ve sürekli optimizasyona kadar tüm adımları şeffaf ve veri odaklı yönetiyoruz.",
        ),
        "processSteps": steps,
        "faqs": faqs,
    }


def build_service_pairs(raw_svc: dict) -> list[tuple[str, str]]:
    svc = normalize_service_dict(raw_svc)
    h1 = svc["h1"]
    lines = svc["heroLines"]
    hero_h2_flight = f"{lines[0]} <br />\r\n{lines[1]}<br />\r\n{lines[2]}"
    hero_h2_ssr = f"{lines[0]} <br />\n{lines[1]}<br />\n{lines[2]}"

    intro_text = svc["introText"]
    intro_heading = svc["introHeading"]
    intro_body = svc["introBody"]
    feats = svc["features"]
    metrics = svc["metrics"]
    steps = svc["processSteps"]
    faqs = svc["faqs"]

    pairs = [
        # Meta title & description
        ("Web Design & Development | London & NYC | KOTA", svc["title"]),
        (
            "A web design and development agency that blends creativity with the latest tech to craft beautiful, award-winning websites.",
            svc["metaDesc"],
        ),

        # Hero H1, H2, H3
        ("Web design and development services", h1),
        ("Welcome to <br />\r\nthe <em>digital</em><br />\r\nrenaissance.", hero_h2_flight),
        ("Welcome to <br />\nthe <em>digital</em><br />\nrenaissance.", hero_h2_ssr),
        (
            "Creative web design and development, combining brand clarity, craft and commercial momentum to create distinctive digital experiences that help ambitious brands grow.",
            intro_text,
        ),

        # DiscoverMore pills (top & bottom)
        ('"slug":"web-design-development","title":"Web design & development"', '"slug":"/hizmetler/performans-pazarlamasi/","title":"Performans Pazarlaması"'),
        ('"slug":"creative-web-design","title":"Creative web design"', '"slug":"/hizmetler/google-reklamlari/","title":"Google Reklamları"'),
        ('"slug":"web-development","title":"Web development"', '"slug":"/hizmetler/seo/","title":"SEO Hizmeti"'),
        ('"slug":"wordpress-cms","title":"WordPress & CMS"', '"slug":"/hizmetler/web-tasarim/","title":"Web Tasarım & Yazılım"'),
        ('href="/service/web-design-development"', 'href="/hizmetler/performans-pazarlamasi/"'),
        ('href="/service/creative-web-design"', f'href="{feats[0].get("href", "/hizmetler/google-reklamlari/")}"'),
        ('href="/service/web-development"', f'href="{feats[1].get("href", "/hizmetler/seo/")}"'),
        ('href="/service/wordpress-cms"', f'href="{feats[2].get("href", "/hizmetler/web-tasarim/")}"'),
        (">Web design &amp; development<", ">Performans Pazarlaması<"),
        (">Creative web design<", ">Google Reklamları<"),
        (">Web development<", ">SEO Hizmeti<"),
        (">WordPress &amp; CMS<", ">Web Tasarım &amp; Yazılım<"),

        # Intro Section
        ("Websites that do more.", intro_heading),
        (
            '<p><span style="font-weight: 400;">We bring brand, UX, SEO, content and development together from day one, combining creative ambition with strategic thinking and technical excellence. The result is a digital experience that feels distinctive, works intuitively and delivers measurable impact long after launch.</span></p>\n',
            f'<p><span style="font-weight: 400;">{intro_body}</span></p>\n',
        ),
        (
            "We bring brand, UX, SEO, content and development together from day one, combining creative ambition with strategic thinking and technical excellence. The result is a digital experience that feels distinctive, works intuitively and delivers measurable impact long after launch.",
            intro_body,
        ),

        # TextImageRows (3 sub-features)
        ("Creative web design.", feats[0]["title"]),
        (
            "<p>Translate your brand into a digital experience with its own rhythm, personality and point of view. Creative thinking  and intuitive UX come together to create experiences that feel effortless to use and impossible to confuse with anyone else.</p>\n",
            f"<p>{feats[0]['text']}</p>\n",
        ),
        (
            "Translate your brand into a digital experience with its own rhythm, personality and point of view. Creative thinking  and intuitive UX come together to create experiences that feel effortless to use and impossible to confuse with anyone else.",
            feats[0]["text"],
        ),
        ('"/service/creative-web-design"', f'"{feats[0].get("href", "/iletisim/")}"'),

        ("Web development.", feats[1]["title"]),
        (
            "<p>We build fast, flexible websites that deliver on the creative idea, rather than compromising it. Clean code, thoughtful interactions and robust technical foundations keep everything running beautifully behind the scenes.</p>\n",
            f"<p>{feats[1]['text']}</p>\n",
        ),
        (
            "We build fast, flexible websites that deliver on the creative idea, rather than compromising it. Clean code, thoughtful interactions and robust technical foundations keep everything running beautifully behind the scenes.",
            feats[1]["text"],
        ),
        ('"/service/web-development"', f'"{feats[1].get("href", "/iletisim/")}"'),

        ("Wordpress & CMS.", feats[2]["title"]),
        (
            "<p>Your team shouldn’t need a developer every time a sentence changes. We create flexible, modular content systems that make pages easy to build, edit and evolve without letting the design descend into chaos.</p>\n",
            f"<p>{feats[2]['text']}</p>\n",
        ),
        (
            "Your team shouldn’t need a developer every time a sentence changes. We create flexible, modular content systems that make pages easy to build, edit and evolve without letting the design descend into chaos.",
            feats[2]["text"],
        ),
        ('"/service/wordpress-cms"', f'"{feats[2].get("href", "/iletisim/")}"'),

        # Statistics Section
        ("Looks good. Works harder.", "Estetik Tasarım. Ölçülebilir Büyüme."),
        ("The proof is in the pudding.", "Verilerle Kanıtlanmış Performans."),
        ("64.1%", metrics[0]["value"]),
        ("increase in conversions after 6 months.", metrics[0]["label"]),
        ("83.14%", metrics[1]["value"]),
        ("increase in sales after 1 year.", metrics[1]["label"]),
        ("70.8%", metrics[2]["value"]),
        ("increase in average engagement time after 3 months.", metrics[2]["label"]),
        ("104.9% ", metrics[3]["value"]),
        ("104.9%", metrics[3]["value"]),
        ("increase in organic visits after 1 month", metrics[3]["label"]),

        # Timeline Section (8 steps)
        ("Our web design and development process.", svc["processHeading"]),
        (
            "Every project is different, but the thinking stays joined up. We move from discovery and digital strategy through UX, creative design and development without losing the thread (or the big idea) along the way.",
            svc["processSubheading"],
        ),
        (" Discovery", steps[0]["title"]),
        (">Discovery<", f">{steps[0]['title']}<"),
        (
            "Before opening Figma, we get properly under the skin of the business. We speak to stakeholders, review your current site, study the industry and dig into how your audience behaves. This gives us a clear view of what the website needs to communicate, where the existing experience is falling short and where there’s room to do something more interesting.",
            steps[0]["text"],
        ),
        ("Digital strategy", steps[1]["title"]),
        (
            "This is where business goals become a plan for the website. We define what the experience needs to achieve, how content should work and which journeys matter most. Brand, audience, search visibility and conversion all shape the direction before we begin designing screens.",
            steps[1]["text"],
        ),
        ("UX & information architecture", steps[2]["title"]),
        (
            "A strong website makes complex things feel simple. We organise the content, structure the journeys and map the key interactions so people can find what they need without fighting the interface. Wireframes give us space to create all the structural foundations before visual design takes over.",
            steps[2]["text"],
        ),
        ("Creative direction", steps[3]["title"]),
        (
            "Now we decide how the website should feel. We explore visual territories, interaction ideas and digital behaviours that bring the brand to life online. This establishes the creative rules for the experience before they’re applied across the wider site.\r\n",
            steps[3]["text"],
        ),
        (
            "Now we decide how the website should feel. We explore visual territories, interaction ideas and digital behaviours that bring the brand to life online. This establishes the creative rules for the experience before they’re applied across the wider site.",
            steps[3]["text"],
        ),
        ("UI & web design", steps[4]["title"]),
        (
            "With the direction agreed, we build the full visual system. Every page is designed to feel connected, responsive and recognisably yours. We consider hierarchy, accessibility, interaction and conversion alongside the creative details that give the site its character. We’ll design either bespoke templates for each page of the website (in mobile and desktop resolutions), or look to design a component builder approach.",
            steps[4]["text"],
        ),
        ('"heading":"Web development"', f'"heading":"{steps[5]["title"]}"'),
        (">Web development</h3>", f">{steps[5]['title']}</h3>"),
        (
            "Our developers bring the design to life without sanding off its edges. We build responsive, high-performance websites with flexible CMS systems and carefully crafted front-end interactions. Development happens alongside design rather than appearing at the end to tell us what isn’t possible.",
            steps[5]["text"],
        ),
        ("Content population & testing", steps[6]["title"]),
        (
            "Before launch, we put the whole thing through its paces. We populate agreed content, test the experience across browsers and devices and check performance, accessibility, forms, integrations and CMS functionality. Small details get the same attention as the headline moments.",
            steps[6]["text"],
        ),
        ("Launch & ongoing support", steps[7]["title"]),
        (
            "Going live isn’t where we disappear. We handle deployment carefully, monitor the site after launch and give your team the tools and training to manage it confidently. We can also stay involved through hosting, optimisation, SEO, content and ongoing creative support through our SiteCare packages.",
            steps[7]["text"],
        ),
        # Timeline durations & workInvolved items
        ('"duration":"1 week"', '"duration":"1. Aşama"'),
        ('"duration":"2 weeks"', '"duration":"2. Aşama"'),
        ('"duration":"5 to 6 weeks"', '"duration":"Uygulama"'),
        ('"duration":"1 to 2 weeks"', '"duration":"Test & Kalite"'),
        ('"duration":"Ongoing"', '"duration":"Sürekli Büyüme"'),
        ("Stakeholder questionnaires & interviews", "Marka ve hedef analizi"),
        ("Current website audit", "Mevcut dijital varlık denetimi"),
        ("Analytics review", "GA4 ve dönüşüm verisi incelemesi"),
        ("Competitor review", "Rakip ve pazar araştırması"),
        ("Audience & category research", "Hedef kitle segmentasyonu"),
        ("Kick-off meeting", "Stratejik başlangıç toplantısı"),
        ("Digital objectives", "Büyüme ve KPI hedefleri"),
        ("Content strategy", "İçerik ve mesaj mimarisi"),
        ("SEO considerations", "Arama görünürlüğü planlaması"),
        ("Conversion opportunities", "Dönüşüm hunisi (CRO) kurgusu"),
        ("Feature requirements", "Teknik gereksinim analizi"),
        ("Technical recommendations", "Veri ve altyapı yol haritası"),
        ("Sitemap development", "Bilgi ve sayfa mimarisi"),
        ("Information architecture", "Kullanıcı akış (UX) tasarımı"),
        ("Audience journey mapping", "Müşteri yolculuğu haritalama"),
        ("Content planning", "Dönüşüm odaklı içerik planı"),
        ("Figma wireframes & prototyping", "Prototip ve wireframe kurgusu"),
        ("Functional specifications", "Fonksiyonel teknik şartname"),
        ("Creative exploration", "Kreatif konsept geliştirme"),
        ("Digital art direction", "Dijital sanat yönetmenliği"),
        ("Typography & colour", "Görsel kimlik ve tipografi"),
        ("Motion principles", "Mikro etkileşim ve hareket dili"),
        ("Interaction concepts", "Deneyim ve etkileşim kurgusu"),
        ("Creative presentation", "Kreatif sunum ve onay"),
        ("Responsive page design", "Mobil öncelikli (Responsive) tasarım"),
        ("UI components", "Modüler tasarım sistemi"),
        ("Interaction design", "Yüksek dönüşümlü arayüz kurgusu"),
        ("Conversion touchpoints", "CRO temas noktası optimizasyonu"),
        ("Developer-ready files", "Uygulamaya hazır tasarım teslimi"),
        ("Front-end development ", "Yüksek hızlı önyüz geliştirme"),
        ("Back-end development ", "Güvenli altyapı ve entegrasyon"),
        ("CMS configuration", "Yönetim paneli ve veri kurulumu"),
        ("Component development", "Özel bileşen ve modül kodlaması"),
        ("Motion design and interaction", "Akıcı animasyon entegrasyonu"),
        ("Third-party integrations", "CRM, Pixel ve CAPI entegrasyonları"),
        ("Performance optimisation", "Core Web Vitals hız optimizasyonu"),
        ("Content population", "İçerik ve kampanya girişi"),
        ("Responsive testing", "Tüm cihazlarda uyumluluk testi"),
        ("Browser testing", "Tarayıcı ve hız testleri"),
        ("Accessibility checks", "Kullanılabilirlik ve erişim kontrolü"),
        ("Performance testing", "Yük ve dönüşüm takip testleri"),
        ("CMS training", "Ekip eğitimi ve dokümantasyon"),
        ("Quality assurance", "Kapsamlı kalite kontrol (QA)"),
        ("Launch planning", "Canlıya geçiş ve lansman planı"),
        ("Website deployment", "Canlı yayın ve sunucu aktivasyonu"),
        ("Redirect implementation", "Yönlendirme ve veri koruma"),
        ("Technical SEO & GEO", "Teknik SEO ve AI görünürlük"),
        ("Analytics setup", "GA4, GTM ve Looker Studio kurulumu"),
        ("Post-launch testing", "Lansman sonrası canlı izleme"),
        ("CMS documentation", "Raporlama ve yönetim kılavuzu"),
        ("Ongoing support", "Sürekli büyüme ve optimizasyon"),

        # FAQs (6 items)
        ("What makes KOTA’s approach to web design different?", faqs[0]["q"]),
        (
            '<p><span style="font-weight: 400;">We connect brand thinking, UX, creative design and development from the start.</span></p>\n<p><span style="font-weight: 400;">That means the strategic idea doesn’t get lost between separate agencies, freelancers or internal teams. The people shaping the concept work closely with the people building it, creating a more coherent website and a much smoother process.</span></p>\n<p><!-- notionvc: 4560da57-e243-4d77-b8f6-210da83bbd62 --></p>\n<p><!-- notionvc: 4560da57-e243-4d77-b8f6-210da83bbd62 --></p>\n',
            f'<p><span style="font-weight: 400;">{faqs[0]["a"]}</span></p>\n',
        ),
        ("How long does a typical web design and development project take?", faqs[1]["q"]),
        (
            '<p><span style="font-weight: 400;">A web design and build project can last around 12-14 weeks. But there are always ways to consider your business objectives (such as phased launches), so even if your timescales don’t work with this, it’s always worth reaching out.\xa0</span></p>\n<p><span style="font-weight: 400;">A lot of it depends on the size of the site, technical complexity, content requirements and level of creative ambition. Smaller websites may move faster. Large platforms, complex integrations and immersive digital experiences will need more time. We’ll set out a clear programme before the project begins.</span></p>\n<p><!-- notionvc: 04fa8446-f45f-4b32-ba37-0a947604670a --></p>\n',
            f'<p><span style="font-weight: 400;">{faqs[1]["a"]}</span></p>\n',
        ),
        ("Do you do both the design and development in-house?", faqs[2]["q"]),
        (
            '<p><span style="font-weight: 400;">Yes. We handle the full process from discovery, strategy and UX through to creative design, development, testing and launch.</span></p>\n<p><span style="font-weight: 400;">Keeping design and development together helps us protect the creative ambition while making sensible technical decisions early. Fewer surprises. Better websites.</span></p>\n',
            f'<p><span style="font-weight: 400;">{faqs[2]["a"]}</span></p>\n',
        ),
        ("Which CMS platforms do you use?", faqs[3]["q"]),
        (
            '<p><span style="font-weight: 400;">We regularly build websites using WordPress, Sanity, and other flexible content management systems selected around the needs of the project.</span></p>\n<p><span style="font-weight: 400;">We’ll recommend the right setup based on your team, content requirements, integrations, scalability and technical constraints rather than forcing every website into the same platform.</span></p>\n',
            f'<p><span style="font-weight: 400;">{faqs[3]["a"]}</span></p>\n',
        ),
        ("What happens after the website launches?", faqs[4]["q"]),
        (
            '<p><span style="font-weight: 400;">A website should keep evolving alongside the business, that’s why KOTA’s SiteCare is a key part of our business. We can continue supporting the website through hosting, maintenance, performance monitoring, SEO, conversion improvements, content and ongoing creative development. You can read more about SiteCare </span><a href="https://kota.co.uk/blog/sitecare-management-website-maintenance"><span style="font-weight: 400;">here</span></a><span style="font-weight: 400;">.</span>\xa0<!-- notionvc: 74ecab4c-0570-4f44-a050-ed73ed4ec96a --></p>\n<p><!-- notionvc: 74ecab4c-0570-4f44-a050-ed73ed4ec96a --></p>\n<p><!-- notionvc: 74ecab4c-0570-4f44-a050-ed73ed4ec96a --></p>\n<p><!-- notionvc: 74ecab4c-0570-4f44-a050-ed73ed4ec96a --></p>\n',
            f'<p><span style="font-weight: 400;">{faqs[4]["a"]}</span></p>\n',
        ),
        ("What should I expect to pay for professional web design and development services?", faqs[5]["q"]),
        (
            '<p><span style="font-weight: 400;">The majority of our full projects sit between £30k and £150k, but project costs will depend on the final scope of work and vary from project to project. We generally have a minimum website project size of £25k and prefer to agree a fixed cost with agreed milestone payments.</span><br />\n<!-- notionvc: 8ec0fece-0a23-4d4e-9183-d2786b5a4646 --></p>\n<p><!-- notionvc: 8ec0fece-0a23-4d4e-9183-d2786b5a4646 --></p>\n',
            f'<p><span style="font-weight: 400;">{faqs[5]["a"]}</span></p>\n',
        ),
    ]
    return pairs


def build_all_pages():
    # 1. Build all 11 Service Pages
    for svc in SERVICES_LIST:
        slug = svc["slug"]
        pairs = build_service_pairs(svc)
        html = render_kota_template(
            "/service/web-design-development",
            pairs,
            hydrate_path="/service/web-design-development",
        )
        write_page(f"hizmetler/{slug}/index.html", html)
        print(f"Built 1:1 KOTA service page: /hizmetler/{slug}/index.html")
        if "/" in slug:
            short_slug = slug.split("/")[-1]
            write_page(f"hizmetler/{short_slug}/index.html", html)
            print(f"Built 1:1 KOTA service alias: /hizmetler/{short_slug}/index.html")

    # 2. Build Services Hub (/hizmetler/index.html)
    hub_data = {
        "slug": "hizmetler",
        "seoTitle": "Hizmetlerimiz | 360° Dijital Pazarlama & Web Tasarım | Roasist",
        "seoDescription": "Performans pazarlaması, Google & Meta reklamları, SEO, kreatif tasarım ve web yazılım çözümleriyle markanızı büyütüyoruz.",
        "h1": "360° Dijital Büyüme & Pazarlama Hizmetlerimiz",
        "heroLines": ["Markanızı", "<em>büyüten</em>", "360° çözümler."],
        "introText": "Performans pazarlaması, SEO, kreatif tasarım ve yüksek dönüşümlü web geliştirme uzmanlığımızı tek bir stratejik çatı altında birleştirerek markanızın cirosunu ve ROAS verimliliğini ölçeklendiriyoruz.",
        "introHeading": "Veri, teknoloji ve yaratıcılık tek merkezde.",
        "introBody": "Roasist olarak reklam yönetiminden arama motoru optimizasyonuna, kullanıcı deneyimi tasarımından dönüşüm hunisi (CRO) mimarisine kadar tüm dijital büyüme kanallarınızı birbiriyle tam entegre biçimde yönetiyoruz.",
        "features": [
            {
                "title": "Performans Pazarlaması & Reklam.",
                "text": "Google Ads, Meta (Instagram & Facebook), TikTok, LinkedIn ve Yandex reklamlarında yapay zeka destekli teklif stratejileri ve CAPI entegrasyonuyla kârlı büyüme sağlıyoruz.",
                "href": "/hizmetler/performans-pazarlamasi/",
            },
            {
                "title": "Teknik SEO & Organik Büyüme.",
                "text": "Teknik SEO, semantik içerik mimarisi ve AI arama (GEO/AEO) optimizasyonuyla markanızı arama motorlarında kalıcı olarak zirveye taşıyoruz.",
                "href": "/hizmetler/seo/",
            },
            {
                "title": "Yüksek Dönüşümlü Web & Kreatif.",
                "text": "Hızlı, modern ve dönüşüm odaklı web siteleri ile dikkat çeken reklam kreatifleri tasarlayarak tıklamaları gerçek müşterilere dönüştürüyoruz.",
                "href": "/hizmetler/web-tasarim/",
            },
        ],
        "metrics": [
            {"value": "6.4x", "label": "Yönetilen performans kampanyalarında ortalama ROAS."},
            {"value": "+185%", "label": "Organik ve ücretli kanallarda yıllık ciro büyümesi."},
            {"value": "-38%", "label": "Dönüşüm hunisi optimizasyonuyla düşen edinim maliyeti (CPA)."},
            {"value": "360°", "label": "Tüm dijital kanallarda tek elden entegre büyüme yönetimi."},
        ],
        "processHeading": "Roasist 360° Büyüme Metodolojimiz.",
        "processSubheading": "Teşhis ve stratejiden çok kanallı icraya, kreatif testlerden canlı veri raporlamasına kadar her adımı şeffaf biçimde yönetiyoruz.",
        "processSteps": SERVICES_BY_SLUG["360-derece-dijital-pazarlama-yonetimi"]["processSteps"],
        "faqs": SERVICES_BY_SLUG["360-derece-dijital-pazarlama-yonetimi"]["faqs"],
    }
    hub_html = render_kota_template(
        "/service/web-design-development",
        build_service_pairs(hub_data),
        hydrate_path="/service/web-design-development",
    )
    write_page("hizmetler/index.html", hub_html)
    print("Built 1:1 KOTA services hub: /hizmetler/index.html")

    # 3. Build References (/referanslar/index.html) from /work
    work_pairs = [
        ("Our Work | KOTA Creative Agency London & New York", "Referanslarımız & Başarı Hikayelerimiz | Roasist"),
        ("We are", "Markaları"),
        ("experts", "dijitalde"),
        ("in bringing brands to life digitally.", "büyüten uzmanlık."),
        ('"children":"Work"', '"children":"Referanslar"'),
        (">Work<", ">Referanslar<"),
        (
            "KOTA is a progressive and insightful \ndesign agency, technically and \ncreatively skilled to translate your brand \ninto its best digital self.",
            "Roasist; performans pazarlaması, SEO, kreatif tasarım ve web teknolojilerini birleştirerek ulusal ve global markalar için ölçülebilir büyüme hikayeleri yaratır.",
        ),
        ("Web Design & Development", "Web Tasarım & Yazılım"),
        ("Branding", "Kreatif & Marka"),
        ("Digital Marketing", "Performans Pazarlaması"),
    ]
    work_html = render_kota_template("/work", work_pairs, hydrate_path="/work")
    write_page("referanslar/index.html", work_html)
    print("Built 1:1 KOTA references page: /referanslar/index.html")

    # 4. Build About (/hakkimizda/index.html) from /agency
    agency_pairs = [
        ("Our Studio | KOTA Agency London & New York", "Hakkımızda | Roasist Dijital Pazarlama Ajansı"),
        (
            "We are KOTA, award-winning Creative Studio based in London & New York. Specialising in Creative Web Design, Web Development, Branding and Digital Marketing.",
            "Roasist; performans pazarlaması, SEO, kreatif tasarım ve web geliştirme alanlarında uzmanlaşmış, veri odaklı 360° dijital büyüme ajansıdır.",
        ),
        ("Proudly signing every piece.", "Veriyle büyüyen markaların stratejik ortağı."),
        ('"children":"Agency"', '"children":"Hakkımızda"'),
        (">Agency<", ">Hakkımızda<"),
        ('"children":"Mission"', '"children":"Misyonumuz"'),
        (">Mission<", ">Misyonumuz<"),
        (
            "To make the digital world more beautiful, thoughtful &amp; impactful.",
            "Dijital yatırımlarınızı şeffaf, yaratıcı ve ölçülebilir ticari büyümeye dönüştürmek.",
        ),
        (
            "To make the digital world more beautiful, thoughtful & impactful.",
            "Dijital yatırımlarınızı şeffaf, yaratıcı ve ölçülebilir ticari büyümeye dönüştürmek.",
        ),
        (
            "Every pixel matters to us because we know it matters to our clients. We understand that great creativity is not simply about aesthetics, it's about results, commercial impact, and creating digital products that people love to use.",
            "Her tıklama, her gösterim ve her piksel bizim için değerlidir. Yaratıcılığın yalnızca estetikten ibaret olmadığını; doğru veri mimarisi ve performans stratejisiyle birleştiğinde markaları kategori liderliğine taşıdığını biliyoruz.",
        ),
        ('"children":"Approach"', '"children":"Yaklaşımımız"'),
        (">Approach<", ">Yaklaşımımız<"),
        (
            "We’re not just coders who take instructions – we’re artists who take pride in being bold and draw inspiration from the world around us.",
            "Sadece reklam kampanyası kuran bir ajans değiliz; markanızın birim ekonomisini, kârlılığını ve büyüme hunisini sahiplenen stratejik iş ortağınızız.",
        ),
        (
            "You’ll never see us play it safe, and we especially like partnering with clients who are up for making digital waves.",
            "Google, Meta, TikTok ve Yandex resmi partnerliklerimizle en güncel reklam teknolojilerini ve yapay zeka algoritmalarını markanız için uyguluyoruz.",
        ),
        (
            "Sustainability is very close to our hearts, too. If your brand makes a positive impact on the environment, we’d relish working with you!",
            "Sürdürülebilir ve kârlı büyüme her şeyin merkezindedir. Şeffaf canlı raporlama panellerimizle her kuruş bütçenin geri dönüşünü (ROAS) anlık takip edebilirsiniz.",
        ),
        ("Our culture", "Kültürümüz"),
        ("is core to everything we do.", "yaptığımız her işin temelidir."),
        (
            "The brands we partner with are looking to push their industry boundaries, and ready to invest quality resources into their online presence.",
            "Birlikte çalıştığımız markalar, sektörlerinde fark yaratmak ve dijital varlıklarını gerçek bir büyüme motoruna dönüştürmek isteyen vizyoner ekiplerden oluşur.",
        ),
        ('"children":"Partners"', '"children":"Partnerlikler"'),
        (">Partners<", ">Partnerlikler<"),
        ("Big Ups", "Resmi Partnerlikler & Başarılar"),
        ("Honourable mention", "Resmi Ajans Partneri"),
        ("Mindsparkle Mag", "Meta Business Partner"),
        ("Site of the day", "Sertifikalı Performans Uzmanlığı"),
        ("Special Kudos", "Resmi Pazarlama Partneri"),
        ("Best Web Design - Aesthetic", "Yüksek ROAS & Büyüme Ödülü"),
    ]
    agency_html = render_kota_template("/agency", agency_pairs, hydrate_path="/agency")
    write_page("hakkimizda/index.html", agency_html)
    print("Built 1:1 KOTA about page: /hakkimizda/index.html")

    # 5. Build Contact (/iletisim/index.html) from /contact
    contact_pairs = [
        ("Contact Us | KOTA Creative Agency London & New York", "İletişim | Roasist Dijital Pazarlama Ajansı"),
        (
            "Partner with an award-winning creative web design agency in London & New York. Contact KOTA for websites, branding & digital marketing.",
            "Markanızı büyütmek için Roasist ile iletişime geçin. Performans pazarlaması, SEO, web tasarım ve 360° dijital pazarlama çözümleri.",
        ),
        ("Good things", "Birlikte"),
        ("happen when", "büyük başarılar"),
        ("you say", "için merhaba"),
        ("hey.", "deyin."),
        ("I am interested in :", "İlgilendiğiniz Hizmet :"),
        ("A new website", "Web Tasarım & Geliştirme"),
        ("Motion graphics", "SEO & İçerik Stratejisi"),
        ("Development", "360° Dijital Pazarlama"),
        ("On-going support", "Kreatif & Grafik Tasarım"),
        ("More info on minimum/typical budget sizes can be found", "Bütçe planlaması ve hizmet kapsamlarımız hakkında detaylı bilgiye"),
        (">here<", ">buradan ulaşabilirsiniz<"),
        ("Attachments", "Dosya Ekle"),
        ("I'm happy to receive a monthly newsletter from KOTA", "Roasist dijital büyüme bültenini almak istiyorum"),
        ("I&#x27;m happy to receive a monthly newsletter from KOTA", "Roasist dijital büyüme bültenini almak istiyorum"),
        (
            "I understand that KOTA will securely hold my data in accordance with their privacy policy.",
            "Verilerimin Gizlilik Politikası ve KVKK kapsamında güvenle işlenmesini kabul ediyorum.",
        ),
        (">Submit<", ">Gönder<"),
        ('"children":"London"', '"children":"İstanbul"'),
        (">London<", ">İstanbul<"),
        ("1-5 Clerkenwell Rd", "Maslak, Büyükdere Cad."),
        ("EC1M 5PA", "Sarıyer / İstanbul"),
        ('"children":"New York"', '"children":"İletişim Hattı"'),
        (">New York<", ">İletişim Hattı<"),
        ("477 Madison Ave", "info@roasist.com"),
        ("Midtown Manhattan", "+90 546 965 70 20"),
        ("6th Floor, NY 10022", "Pzt - Cum: 09:00 - 18:00"),
        ("Have a quick question you need answering?", "Hızlıca yanıtlanmasını istediğiniz bir sorunuz mu var?"),
        ("Check out - FAQ's :", "Sıkça Sorulan Sorular :"),
        ("Working with KOTA", "Roasist ile Çalışmak"),
        ("General", "Genel Sorular"),
    ]
    contact_html = render_kota_template("/contact", contact_pairs, hydrate_path="/contact")
    write_page("iletisim/index.html", contact_html)
    write_page("start-your-project/index.html", contact_html)
    print("Built 1:1 KOTA contact page: /iletisim/index.html")

    # 6. Build Blog Index (/blog/index.html) and Category/Tag pages from /blog
    blog_pairs = [
        ("Creative Web Design Agency Blog | KOTA", "Blog | Dijital Pazarlama, ROAS ve SEO Rehberleri | Roasist"),
        (
            "Get design industry news, web design inspiration and insights from KOTA, an award-winning creative digital agency in London & New York.",
            "Performans pazarlaması, ROAS hesaplama, veri odaklı büyüme stratejileri ve SEO hakkında güncel rehberler ve analizler.",
        ),
        ("News, insights,", "Dijital büyüme,"),
        ("& creative culture", "veri & strateji"),
        ("from KOTA.", "Roasist Blog."),
        ("Featured", "Öne Çıkan"),
    ]
    blog_html = render_kota_template("/blog", blog_pairs, hydrate_path="/blog")
    for rel in [
        "blog/index.html",
        "blog/kategori/dijital-pazarlama/index.html",
        "blog/kategori/performans-pazarlamasi/index.html",
        "blog/kategori/reklam-yonetimi/index.html",
        "blog/etiket/dijital-buyume/index.html",
        "blog/etiket/dijital-pazarlama-stratejileri/index.html",
        "blog/etiket/performans-analizi/index.html",
        "blog/etiket/performans-pazarlamasi/index.html",
        "blog/etiket/reklam-optimizasyonu/index.html",
        "blog/etiket/roas/index.html",
        "blog/etiket/roi/index.html",
        "blog/etiket/veri-analizi/index.html",
        "blog/etiket/veriye-dayali-pazarlama/index.html",
    ]:
        write_page(rel, blog_html)
    print("Built 1:1 KOTA blog hub and archive pages")

    # 7. Build the 3 Individual Blog Post pages from /blog/ai-search-zero-click-seo
    hf_post = ROUTES["/blog/ai-search-zero-click-seo"]
    with open(os.path.join(PAGES_DIR, hf_post), "r", encoding="utf-8") as f:
        post_raw_html = f.read()
    post_parts = [json.loads(m.group(1))[1] for m in SCRIPT_RE.finditer(post_raw_html) if json.loads(m.group(1))[0] == 1]
    post_flight = "".join(post_parts)
    m_2d = re.search(r"2d:T([0-9a-f]+),", post_flight)
    orig_article_body = ""
    if m_2d:
        blen = int(m_2d.group(1), 16)
        bstart = len(post_flight[:m_2d.end()].encode("utf-8"))
        orig_article_body = post_flight.encode("utf-8")[bstart:bstart + blen].decode("utf-8")

    blog_posts = [
        {
            "slug": "Performans-Pazarlamasi-Nedir",
            "title": "Performans Pazarlaması Nedir? Markanızı Nasıl Ölçeklendirir?",
            "desc": "Performans pazarlaması nedir, hangi kanalları kapsar ve ROAS odaklı büyüme stratejisi nasıl kurulur? Roasist uzman rehberi.",
            "body": (
                "<h2>Performans Pazarlaması Nedir?</h2>"
                "<p>Performans pazarlaması; reklam bütçenizin her bir kuruşunun tıklama, form, telefon araması veya doğrudan satış gibi <strong>ölçülebilir ticari sonuçlara</strong> dönüştüğü veri odaklı dijital pazarlama yaklaşımıdır. Geleneksel reklamcılığın aksine, yalnızca gerçek etkileşim ve dönüşüm elde ettiğinizde bütçenizi ölçeklendirirsiniz.</p>"
                "<h2>Hangi Kanallar Performans Pazarlamasının Merkezindedir?</h2>"
                "<p>Roasist olarak performans pazarlaması mimarisini tek bir kanal üzerine değil, kullanıcı yolculuğunun tamamını kapsayan entegre bir ekosistem üzerine kuruyoruz:</p>"
                "<ul>"
                "<li><strong>Google Ads (Arama, Alışveriş, Performance Max):</strong> Satın alma niyeti en yüksek kullanıcıları tam karar anında yakalar.</li>"
                "<li><strong>Meta Reklamları (Instagram &amp; Facebook):</strong> Görsel hikaye anlatımı ve gelişmiş CAPI veri sinyalleriyle talep yaratır ve yeniden pazarlama (remarketing) dönüşümlerini katlar.</li>"
                "<li><strong>TikTok ve YouTube Video Kampanyaları:</strong> Dikkat ekonomisinde markanızın kreatif gücünü satış hunisine taşır.</li>"
                "<li><strong>LinkedIn &amp; Yandex Reklamları:</strong> B2B karar vericilere ve uluslararası pazarlara nokta atışı erişim sağlar.</li>"
                "</ul>"
                "<h2>Veri Doğruluğu ve ROAS Optimizasyonu</h2>"
                "<p>Başarılı bir performans pazarlaması stratejisinin temeli <strong>temiz veri</strong>dir. GA4, Google Tag Manager, Sunucu Taraflı İzleme (Server-Side Tracking) ve Dönüşüm API (CAPI) kurulumları olmadan yapay zeka algoritmalarının doğru müşteriyi bulması imkansızdır. Roasist'te tüm kampanyalarınızı marj bazlı ROAS ve müşteri edinme maliyeti (CPA) hedeflerine göre günlük olarak optimize ediyoruz.</p>"
            ),
        },
        {
            "slug": "Veriye-Dayali-Dijital-Pazarlama-Stratejisi-Nedir",
            "title": "Veriye Dayalı Dijital Pazarlama Stratejisi Nedir?",
            "desc": "Tahminlere değil gerçek kullanıcı verilerine dayanan dijital pazarlama stratejisi nasıl oluşturulur? Birinci taraf veri ve dönüşüm optimizasyonu.",
            "body": (
                "<h2>Tahmin Değil, Veri Odaklı Karar Alma</h2>"
                "<p>Veriye dayalı dijital pazarlama; kampanya kurgularından kreatif tasarıma, bütçe dağılımından açılış sayfası (landing page) deneyimine kadar her kararın <strong>gerçek kullanıcı davranışları ve dönüşüm verileriyle</strong> şekillendirilmesidir.</p>"
                "<h2>Birinci Taraf Veri (First-Party Data) Neden Kritik?</h2>"
                "<p>Üçüncü taraf çerezlerin etkisini yitirdiği güncel dijital ekosistemde, kendi web sitenizden ve CRM altyapınızdan topladığınız birinci taraf veriler en değerli büyüme varlığınızdır. Sunucu taraflı (Server-Side) etiketleme ve gelişmiş dönüşüm takibi sayesinde reklam platformlarındaki yapay zeka modellerini gerçek satış verilerinizle besliyoruz.</p>"
                "<h2>Sürekli A/B Testi ve Kreatif İterasyon</h2>"
                "<p>Veri yalnızca geçmişi raporlamak için değil, geleceği inşa etmek için kullanılır. Isı haritaları, oturum kayıtları, mikro dönüşüm hunileri ve kreatif kanca (hook) testleriyle reklam bütçenizi en yüksek kârlılık üreten segmentlere dinamik biçimde yönlendiriyoruz.</p>"
            ),
        },
        {
            "slug": "Reklam-Harcamalarinin-Geri-Donusu-ROAS-Nasil-Hesaplanir",
            "title": "Reklam Harcamalarının Geri Dönüşü (ROAS) Nasıl Hesaplanır?",
            "desc": "ROAS (Return on Ad Spend) nedir, nasıl hesaplanır ve e-ticaret ile hizmet sektörlerinde hedef ROAS nasıl artırılır?",
            "body": (
                "<h2>ROAS (Return on Ad Spend) Nedir?</h2>"
                "<p><strong>ROAS (Reklam Harcamalarının Geri Dönüşü)</strong>, dijital reklam kampanyalarınıza yatırdığınız her 1 TL karşılığında kaç TL brüt gelir elde ettiğinizi gösteren en temel performans metriğidir.</p>"
                "<h2>ROAS Formülü ve Örnek Hesaplama</h2>"
                "<p>ROAS hesaplaması son derece nettir: <strong>ROAS = Reklamdan Elde Edilen Gelir / Reklam Harcaması</strong>. Örneğin bir ay içinde Google ve Meta reklamlarına 100.000 TL bütçe ayırdığınızda bu kampanyalardan 650.000 TL ciro elde ettiyseniz, ROAS değeriniz <strong>6.5 (veya %650)</strong> olur.</p>"
                "<h2>ROAS Nasıl Artırılır?</h2>"
                "<ul>"
                "<li><strong>Negatif Anahtar Kelime ve Kitle Temizliği:</strong> Bütçenizi dönüşüm getirmeyen aramalardan ve alakasız gösterimlerden koruyun.</li>"
                "<li><strong>Yüksek Dönüşümlü Kreatif ve Teklif Kurgusu:</strong> Tıklama oranını (CTR) artıran kreatifler tıklama başı maliyetinizi düşürerek ROAS'ı doğrudan yükseltir.</li>"
                "<li><strong>Sepet Ortalaması (AOV) ve CRO Çalışmaları:</strong> Açılış sayfası hızınızı ve çapraz satış kurgularınızı iyileştirerek aynı trafikle daha yüksek ciro üretin.</li>"
                "</ul>"
            ),
        },
    ]

    for post in blog_posts:
        post_pairs = [
            ("AI Search, zero-click SEO and Google’s May update", post["title"]),
            (
                "Google’s May updates show how AI Search and zero-click results are reshaping SEO, traffic and content strategy.",
                post["desc"],
            ),
        ]
        if orig_article_body:
            post_pairs.append((orig_article_body, post["body"]))
        post_html = render_kota_template(
            "/blog/ai-search-zero-click-seo",
            post_pairs,
            hydrate_path="/blog/ai-search-zero-click-seo",
        )
        write_page(f"blog/{post['slug']}/index.html", post_html)
        print(f"Built 1:1 KOTA blog post: /blog/{post['slug']}/index.html")

    # 8. Build Privacy Policy (/gizlilik-politikasi-ve-kullanim-sartlari/index.html) from /privacy-policy
    hf_priv = ROUTES["/privacy-policy"]
    with open(os.path.join(PAGES_DIR, hf_priv), "r", encoding="utf-8") as f:
        priv_raw_html = f.read()
    priv_parts = [json.loads(m.group(1))[1] for m in SCRIPT_RE.finditer(priv_raw_html) if json.loads(m.group(1))[0] == 1]
    priv_flight = "".join(priv_parts)
    m_27 = re.search(r"27:T([0-9a-f]+),", priv_flight)
    orig_priv_body = ""
    if m_27:
        blen = int(m_27.group(1), 16)
        bstart = len(priv_flight[:m_27.end()].encode("utf-8"))
        orig_priv_body = priv_flight.encode("utf-8")[bstart:bstart + blen].decode("utf-8")

    roasist_priv_body = (
        "<h2>1. Gizlilik Politikası ve KVKK Aydınlatma Metni</h2>"
        "<p>Roasist Dijital Pazarlama Ajansı (“Roasist”) olarak, 6698 sayılı Kişisel Verilerin Korunması Kanunu (“KVKK”) kapsamında web sitemizi ziyaret eden tüm kullanıcılarımızın ve iş ortaklarımızın veri güvenliğini en üst düzeyde koruyoruz.</p>"
        "<h2>2. Toplanan Veriler ve İşleme Amaçları</h2>"
        "<p>İletişim formlarımız, teklif talepleriniz ve analitik çerezler aracılığıyla toplanan ad, soyad, e-posta adresi, telefon numarası ve firma bilgileri; yalnızca talep ettiğiniz dijital pazarlama ve yazılım hizmetlerinin sunulması, stratejik analizlerin hazırlanması ve sizinle iletişim kurulması amacıyla işlenmektedir.</p>"
        "<h2>3. Çerez (Cookie) ve Analitik Kullanımı</h2>"
        "<p>Web sitemizde kullanıcı deneyimini iyileştirmek ve site performansını ölçümlemek amacıyla birinci taraf analitik çerezler kullanılmaktadır. Kişisel verileriniz açık rızanız olmaksızın üçüncü taraf kurum veya kişilerle paylaşılmaz ve satılmaz.</p>"
        "<h2>4. Kullanım Şartları ve Fikri Mülkiyet</h2>"
        "<p>Bu web sitesinde yer alan tüm metinler, tasarımlar, grafikler, logolar ve yazılım bileşenleri Roasist'in fikri mülkiyetindedir. İzinsiz kopyalanamaz veya çoğaltılamaz.</p>"
        "<h2>5. İletişim ve Başvuru Haklarınız</h2>"
        "<p>KVKK'nın 11. maddesi kapsamındaki tüm bilgi ve silme talepleriniz için bize <strong>info@roasist.com</strong> adresinden her zaman ulaşabilirsiniz.</p>"
    )
    priv_pairs = [
        ("Privacy Policy - KOTA", "Gizlilik Politikası ve Kullanım Şartları | Roasist"),
        (
            "Privacy matters. Here’s how we use your data—transparently, responsibly, and with your trust in mind.",
            "Roasist Gizlilik Politikası, KVKK Aydınlatma Metni ve Web Sitesi Kullanım Şartları.",
        ),
        (">Privacy Policy<", ">Gizlilik Politikası &amp; KVKK<"),
        ('"children":"Privacy Policy"', '"children":"Gizlilik Politikası & KVKK"'),
    ]
    if orig_priv_body:
        priv_pairs.append((orig_priv_body, roasist_priv_body))
    priv_html = render_kota_template("/privacy-policy", priv_pairs, hydrate_path="/privacy-policy")
    write_page("gizlilik-politikasi-ve-kullanim-sartlari/index.html", priv_html)
    print("Built 1:1 KOTA privacy policy page: /gizlilik-politikasi-ve-kullanim-sartlari/index.html")


if __name__ == "__main__":
    build_all_pages()
