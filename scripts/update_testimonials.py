#!/usr/bin/env python3
"""
Updates the "Müşterilerimiz ne diyor?" / "What Our Clients Say" (Testimonials_testimonials)
section across all TR & EN pages (Homepage and Service pages) in both public/ and dist/
to feature only the 4 requested client testimonials:
1. Burak Özhan — İstanbul Medya Akademisi
2. Alireza Hajiali — Summer Homes
3. Özlem Açıkyürek Atabaş — Gekoo
4. Özgür Demirtaş — Op. Dr. Özgür Demirtaş
"""

import argparse
import glob
import html as html_mod
import json
import os
import re
import subprocess

ROOT = "/home/antigravity/Roasist/roasist-web"

TESTIMONIALS = [
    {
        "name_tr": "Burak Özhan",
        "name_en": "Burak Özhan",
        "speciality_tr": "İstanbul Medya Akademisi",
        "speciality_en": "Istanbul Media Academy",
        "logo": "/images/clients-white/ref-04.png",
        "logo_w": 440,
        "logo_h": 160,
        "bg": "#EDE9FE",
        "url_tr": "/referanslar/",
        "url_en": "/en/references/",
        "text_tr": (
            '"Reklam sürecinde projeye yaklaşımları, anlaşmamızın ötesinde sorumluluk alarak aynı zamanda '
            'bir grafik tasarımcı katkısı sunmaları, mesai kavramından uzak 7/24 destek ve hassasiyet ile '
            'bizim işimiz için en az bizim kadar dertlenen bir dijital pazarlama uzmanıyla çalışma fırsatı '
            'yakaladığımız için şanslıyız. Roasist ile teknik konuları dert etmeden dijital dünyada '
            'şirketinizi büyütmek için gönül rahatlığıyla çalışabilirsiniz. Yeni kampanya dönemlerinde '
            'tekrar çalışma dileğiyle, emekleriniz için teşekkür ederim."'
        ),
        "text_en": (
            '"We are fortunate to work with a digital marketing team that cares about our business as much '
            'as we do—taking ownership beyond our agreement by contributing graphic design support and '
            'providing 24/7 dedication. With Roasist, you can confidently scale your company in the digital '
            'world without worrying about technical complexities. Thank you for all your hard work and '
            'commitment."'
        ),
    },
    {
        "name_tr": "Alireza Hajiali",
        "name_en": "Alireza Hajiali",
        "speciality_tr": "Summer Homes",
        "speciality_en": "Summer Homes",
        "logo": "/images/clients-white/ref-27.png",
        "logo_w": 440,
        "logo_h": 160,
        "bg": "#E0E7FF",
        "url_tr": "/referanslar/summer-homes/",
        "url_en": "/en/references/summer-homes/",
        "text_tr": (
            '"Yurtdışında gayrimenkul yatırımı ve yatırım yoluyla Türk vatandaşlığı arayan uluslararası '
            'yatırımcılara yönelik yürüttüğümüz global reklam kampanyalarında Roasist ekibi hedef pazarlarımızı '
            'çok doğru analiz etti. Veri odaklı hedefleme ve optimizasyon süreçleri sayesinde farklı ülkelerden '
            'gelen nitelikli yatırımcı başvurularımızda (lead) ve satış dönüşümlerimizde istikrarlı bir büyüme '
            'yakaladık. Global pazardaki büyüme sürecimizde güvenilir bir iş ortağı oldukları için teşekkür ederiz."'
        ),
        "text_en": (
            '"Across our global ad campaigns targeting international buyers seeking real estate investment '
            'opportunities and Turkish citizenship by investment, the Roasist team analyzed our target markets '
            'with exceptional precision. Their data-driven optimization delivered consistent growth in qualified '
            'international investor leads and sales conversions."'
        ),
    },
    {
        "name_tr": "Özlem Açıkyürek Atabaş",
        "name_en": "Özlem Açıkyürek Atabaş",
        "speciality_tr": "Gekoo",
        "speciality_en": "Gekoo",
        "logo": "/images/clients-white/ref-21.png",
        "logo_w": 440,
        "logo_h": 160,
        "bg": "#F3E8FF",
        "url_tr": "/referanslar/gekoo/",
        "url_en": "/en/references/gekoo/",
        "text_tr": (
            '"Gekoo olarak organik ve sağlıklı beslenme farkındalığı olan kullanıcıların kendileri ve aileleri '
            'için güvenle alışveriş yapmasını sağlama hedefimizde Roasist ile çalışmak e-ticaret performansımızı '
            'çok güçlü bir noktaya taşıdı. Doğru hedef kitle ve katalog stratejileriyle hem e-ticaret sitemiz '
            'üzerinden gerçekleşen organik gıda satışlarımızda hem de tekrar sipariş veren aile oranımızda '
            'yüksek bir artış elde ettik. Markamıza gösterdikleri özen için tüm ekibe teşekkür ediyorum."'
        ),
        "text_en": (
            '"Partnering with Roasist to connect health-conscious families with certified organic foods '
            'elevated our e-commerce performance at Gekoo. Their precision ad strategies drove strong growth '
            'in online organic food orders and repeat family purchases through our store. Thank you to the '
            'entire team for their dedication and transparency."'
        ),
    },
    {
        "name_tr": "Özgür Demirtaş",
        "name_en": "Özgür Demirtaş",
        "speciality_tr": "Op. Dr. Özgür Demirtaş",
        "speciality_en": "Op. Dr. Özgür Demirtaş",
        "logo": "/images/clients-white/ref-02.png",
        "logo_w": 440,
        "logo_h": 160,
        "bg": "#E8ECFF",
        "url_tr": "/referanslar/",
        "url_en": "/en/references/",
        "text_tr": (
            '"Sağlık ve cerrahi alanında dijital iletişimin hem mesleki etik sınırlar içinde hem de yüksek '
            'güven duygusuyla yürütülmesi bizim için çok kritikti. Roasist ekibi, doğru hasta kitlesine '
            'ulaşmamızı sağlayan stratejik reklam yönetimiyle kliniğimizin dijital görünürlüğünü ve nitelikli '
            'hasta başvuru süreçlerini büyük bir titizlikle yönetti. Profesyonel yaklaşımları, şeffaf '
            'raporlamaları ve kesintisiz destekleri için teşekkür ederim."'
        ),
        "text_en": (
            '"In the medical and surgical field, conducting digital communication with both ethical care '
            'and strong patient trust is paramount. The Roasist team meticulously managed our clinic\'s '
            'digital visibility and patient inquiry campaigns with strategic precision, transparent reporting, '
            'and continuous support."'
        ),
    },
]


def build_testimonial_slide_ssr(item: dict, lang: str, is_dist: bool, cdn_sha: str, is_home_variant: bool) -> str:
    text = item["text_tr"] if lang == "tr" else item["text_en"]
    text_escaped = html_mod.escape(text, quote=True)
    name = item["name_tr"] if lang == "tr" else item["name_en"]
    spec = item["speciality_tr"] if lang == "tr" else item["speciality_en"]
    btn_title = "Projeyi İncele" if lang == "tr" else "View Case Study"
    raw_url = item["url_tr"] if lang == "tr" else item["url_en"]
    btn_href = f"/roasist-web{raw_url}" if is_dist else raw_url

    if is_dist:
        logo_url = f"https://cdn.jsdelivr.net/gh/Roasist/roasist-web@{cdn_sha}/public{item['logo']}"
    else:
        logo_url = item["logo"]

    if is_home_variant:
        cls_slide = "TestimonialsCarousel_swiperSlide__lovqP"
        cls_panel = "TestimonialsPanel_panel__QSk4x"
        cls_wrap = "TestimonialsPanel_panelWrap__Lm7Hv"
        cls_logo = "TestimonialsPanel_logo__m6tmz"
        cls_desc = "TestimonialsPanel_description__njfi8"
        cls_details = "TestimonialsPanel_details__ijkyr"
        cls_name = "TestimonialsPanel_name__Spm5c"
        cls_btns = "TestimonialsPanel_buttons__fOECn"
    else:
        cls_slide = "TestimonialsCarousel_swiperSlide__xzlOt"
        cls_panel = "TestimonialsPanel_panel__82Pbr"
        cls_wrap = "TestimonialsPanel_panelWrap__IAqAF"
        cls_logo = "TestimonialsPanel_logo__rFOvF"
        cls_desc = "TestimonialsPanel_description__WA6g_"
        cls_details = "TestimonialsPanel_details__JWR2H"
        cls_name = "TestimonialsPanel_name__bD4Ek"
        cls_btns = "TestimonialsPanel_buttons__gZnG1"

    return (
        f'<div class="{cls_slide} swiper-slide">'
        f'<div class="{cls_panel} testimonialPanel" style="background-color:{item["bg"]}">'
        f'<div class="{cls_wrap}">'
        f'<figure class="{cls_logo}">'
        '<span class="Image_image__RAAdZ Image_intrinsic__JRoea">'
        f'<img src="{logo_url}" alt="{spec}" loading="eager" fetchPriority="low" height="{item["logo_h"]}" width="{item["logo_w"]}" sizes="100vw"/>'
        '</span></figure>'
        f'<p class="{cls_desc}">{text_escaped}</p>'
        f'<div class="{cls_details}">'
        f'<span class="{cls_name}">{name}</span>'
        f'<span class="{cls_name}">{spec}</span>'
        '</div>'
        f'<div class="{cls_btns}">'
        '<div class="Magnetic_magnetic__LncOy" data-fill="false">'
        '<div class="Button_button__JJiqJ" data-direction="forwards">'
        f'<a class="Button_inner__fnyH6" href="{btn_href}">'
        '<span class="Button_border__hirH2"></span>'
        '<span class="Button_text__IZaCD">'
        f'<span class="Button_textInner__JTTHe">{btn_title}</span>'
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 17.1 15.17" class="Button_buttonArrow__0W9XI">'
        '<path d="m17.1,7.58s-.01-.04-.01-.06c.01-.22-.06-.45-.24-.61L9.23.19c-.31-.27-.78-.24-1.06.07-.27.31-.24.78.07,1.06l6.26,5.52H.75c-.41,0-.75.34-.75.75s.34.75.75.75h13.74l-6.26,5.52c-.31.27-.34.75-.07,1.06.15.17.35.25.56.25.18,0,.35-.06.5-.19l7.62-6.72c.18-.16.25-.39.24-.61,0-.02.01-.04.01-.06Z" fill="currentColor"></path>'
        '</svg></span></a></div></div></div></div></div></div>'
    )


def build_testimonial_flight_item(item: dict, lang: str, is_dist: bool, cdn_sha: str) -> dict:
    text = item["text_tr"] if lang == "tr" else item["text_en"]
    name = item["name_tr"] if lang == "tr" else item["name_en"]
    spec = item["speciality_tr"] if lang == "tr" else item["speciality_en"]
    btn_title = "Projeyi İncele" if lang == "tr" else "View Case Study"
    btn_url = item["url_tr"] if lang == "tr" else item["url_en"]
    if is_dist:
        logo_url = f"https://cdn.jsdelivr.net/gh/Roasist/roasist-web@{cdn_sha}/public{item['logo']}"
    else:
        logo_url = item["logo"]

    return {
        "text": text,
        "backgroundColor": item["bg"],
        "name": name,
        "speciality": spec,
        "button": {
            "title": btn_title,
            "url": btn_url,
            "target": "",
        },
        "logo": {
            "altText": spec,
            "srcSet": None,
            "sourceUrl": logo_url,
            "mediaDetails": {
                "width": item["logo_w"],
                "height": item["logo_h"],
            },
        },
    }


def update_file_testimonials(file_path: str, is_dist: bool, cdn_sha: str) -> bool:
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()

    if "Testimonials_testimonials" not in html:
        return False

    lang = "en" if ('lang="en"' in html[:1000] or "/en/" in file_path.replace("\\", "/")) else "tr"
    is_home_variant = "Testimonials_testimonials__AMUEx" in html

    # Reverse order so Burak Özhan (last item in array) is the first card displayed on top of the stack
    ordered_items = list(reversed(TESTIMONIALS))
    slides_ssr = "".join(
        build_testimonial_slide_ssr(it, lang, is_dist, cdn_sha, is_home_variant) for it in ordered_items
    )
    flight_items = [build_testimonial_flight_item(it, lang, is_dist, cdn_sha) for it in ordered_items]

    # 1. Replace SSR <div class="swiper-wrapper">...</div> inside <section class="Testimonials_testimonials__...">
    sec_pattern = re.compile(
        r'(<section class="Testimonials_testimonials__[^"]*">)(.*?)(</section>)',
        re.DOTALL,
    )
    m_sec = sec_pattern.search(html)
    if not m_sec:
        raise RuntimeError(f"Testimonials section SSR not found in {file_path}")

    sec_inner = m_sec.group(2)
    nav_cls = "TestimonialsCarousel_swiperNav__hRE1L" if is_home_variant else "TestimonialsCarousel_swiperNav__zD7PI"
    wrapper_pattern = re.compile(
        r'(<div class="swiper-wrapper">).*?(</div><div class="' + re.escape(nav_cls) + r'">)',
        re.DOTALL,
    )
    new_sec_inner, count_w = wrapper_pattern.subn(
        lambda m: m.group(1) + slides_ssr + m.group(2),
        sec_inner,
    )
    if count_w == 0:
        raise RuntimeError(f"No swiper-wrapper replaced inside Testimonials section in {file_path}")

    html = html[: m_sec.start(2)] + new_sec_inner + html[m_sec.end(2) :]

    # 2. Replace Flight payload testimonials arrays
    flight_updated = False
    for fm in re.finditer(r'self\.__next_f\.push\(\[1,"(.*?)"\]\)</script>', html, re.DOTALL):
        s = fm.group(1)
        if "Testimonials_testimonials" not in s:
            continue
        decoded = json.loads('"' + s + '"')
        lines = decoded.split("\n")
        new_lines = []
        for line in lines:
            if ":" in line:
                colon = line.find(":")
                rkey = line[:colon]
                rval = line[colon + 1 :]
                if rkey in ("3e", "38") and rval.startswith("["):
                    new_lines.append(f"{rkey}:" + json.dumps(flight_items, ensure_ascii=False, separators=(",", ":")))
                    continue
                if "Testimonials_testimonials" in rval and not rval.startswith("T"):
                    try:
                        robj = json.loads(rval)

                        def patch_tnode(node):
                            changed = False
                            if isinstance(node, dict):
                                cname = str(node.get("className", ""))
                                if cname.startswith("Testimonials_testimonials"):
                                    for ch in node.get("children", []):
                                        if isinstance(ch, list):
                                            if patch_tnode(ch):
                                                changed = True
                                if "testimonials" in node:
                                    node["testimonials"] = flight_items
                                    changed = True
                                for v in node.values():
                                    if isinstance(v, (list, dict)) and patch_tnode(v):
                                        changed = True
                            elif isinstance(node, list):
                                for elem in node:
                                    if isinstance(elem, (list, dict)) and patch_tnode(elem):
                                        changed = True
                            return changed

                        if patch_tnode(robj):
                            flight_updated = True
                            new_lines.append(
                                f"{rkey}:" + json.dumps(robj, ensure_ascii=False, separators=(",", ":"))
                            )
                            continue
                    except Exception:
                        pass
            new_lines.append(line)

        if flight_updated:
            new_decoded = "\n".join(new_lines)
            new_encoded = json.dumps(new_decoded, ensure_ascii=False)[1:-1]
            html = html[: fm.start(1)] + new_encoded + html[fm.end(1) :]
            break

    if not flight_updated:
        raise RuntimeError(f"Flight testimonials array not updated in {file_path}")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html)
    return True


def patch_testimonials_js_chunks() -> None:
    patterns = [
        "public/_next/static/chunks/app/(home)/page-b58f77e3dc47742c.js",
        "public/_next/static/chunks/app/[slug]/page-476cfeca3f4b50d2.js",
        "public/_next/static/chunks/app/%5Bslug%5D/page-476cfeca3f4b50d2.js",
        "public/_next/static/chunks/app/service/[slug]/page-53d2604786d625db.js",
        "public/_next/static/chunks/app/service/%5Bslug%5D/page-53d2604786d625db.js",
        "dist/_next/static/chunks/app/(home)/page-b58f77e3dc47742c.js",
        "dist/_next/static/chunks/app/[slug]/page-476cfeca3f4b50d2.js",
        "dist/_next/static/chunks/app/%5Bslug%5D/page-476cfeca3f4b50d2.js",
        "dist/_next/static/chunks/app/service/[slug]/page-53d2604786d625db.js",
        "dist/_next/static/chunks/app/service/%5Bslug%5D/page-53d2604786d625db.js",
    ]
    for rel in patterns:
        p = os.path.join(ROOT, rel)
        if not os.path.exists(p):
            continue
        with open(p, "r", encoding="utf-8") as f:
            js = f.read()
        new_js = (
            js.replace(
                '{image:null==i?void 0:i.logo,layout:"intrinsic"}',
                '{image:null==i?void 0:i.logo,layout:"intrinsic",lazy:!1}',
            )
            .replace(
                '{image:null==r?void 0:r.logo,layout:"intrinsic"}',
                '{image:null==r?void 0:r.logo,layout:"intrinsic",lazy:!1}',
            )
        )
        if new_js != js:
            with open(p, "w", encoding="utf-8") as f:
                f.write(new_js)
            print(f"Patched TestimonialsPanel lazy:!1 in {rel}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cdn-sha", default="", help="Git commit SHA on main for jsDelivr CDN URLs in dist/")
    args = parser.parse_args()

    cdn_sha = args.cdn_sha.strip()
    if not cdn_sha:
        cdn_sha = (
            subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT)
            .decode("utf-8")
            .strip()
        )
    print(f"Using CDN SHA: {cdn_sha}")

    patch_testimonials_js_chunks()

    pub_count = 0
    for path in sorted(glob.glob(os.path.join(ROOT, "public/**/*.html"), recursive=True)):
        if update_file_testimonials(path, False, cdn_sha):
            pub_count += 1

    dist_count = 0
    for path in sorted(glob.glob(os.path.join(ROOT, "dist/**/*.html"), recursive=True)):
        if update_file_testimonials(path, True, cdn_sha):
            dist_count += 1

    print(f"Updated Testimonials in {pub_count} public HTML files and {dist_count} dist HTML files.")


if __name__ == "__main__":
    main()
