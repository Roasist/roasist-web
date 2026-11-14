#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Surgical, hydration-safe updater for Roasist's Hakkımızda page:
  - Updates both public/hakkimizda/index.html and dist/hakkimizda/index.html
  - Preserves 100% of the KOTA layout, design, CSS, and animations
  - Removes Hero mouse-move background image trail ($L30 / HeroTrail)
  - Removes full-width Video section ($L34 / Video_video__ODG2u)
  - Applies elevated Turkish copy based on https://www.roasist.com/hakkimizda/
  - Recomputes exact UTF-8 hex byte lengths for React Flight T-chunks (e.g. 29:T<hex>,)
    so Next.js hydration succeeds with zero errors.
"""

import json
import os
import re

ROOT = "/home/antigravity/Roasist/roasist-web"

CDN_BASE = "https://cdn.jsdelivr.net/gh/Roasist/roasist-web@189b2e0aee16a196d88d8895fb3795810c6d17f9"
BADGE_CDN = "https://cdn.jsdelivr.net/gh/Roasist/roasist-web@c766063e6a19824bf5e1a598d275bf05cbf2226f/public"

ROASIST_DESC = (
    "Roasist, dijital pazarlama sektöründe özelleştirilmiş, kalite, süreç ve hız odaklı "
    "yaklaşımıyla öne çıkan yeni nesil dijital büyüme ve performans ajansıdır."
)

MISSION_SUBHEADING = (
    "Özelleştirilmiş ve veri odaklı stratejilerle markanızın büyüme sorumluluğunu üstleniyoruz."
)

MISSION_HTML = (
    "<p>“Çoğu insan gerçekte özgürlük istemez, çünkü özgürlük sorumluluk gerektirir ve çoğu insan sorumluluktan korkar.” "
    "— Sigmund Freud’un bu sözü, Roasist’in kuruluş felsefesini yansıtır. Biz özgürlüğü ve sorumluluğu bir arada benimsiyor; "
    "çalıştığımız her markanın dijital büyüme hedeflerini kendi işimiz gibi sahipleniyoruz.</p>\n"
    "<p>Roasist, dijital pazarlama sektöründe özelleştirilmiş ve yenilikçi yaklaşımıyla öne çıkan bir dijital pazarlama ajansıdır. "
    "Müşterilerimize en güçlü sonuçları sunmak için kanıtlanmış pazarlama prensiplerini modern fikirler ve veri analitiğiyle birleştiriyor; "
    "hızla değişen dijital dünyayı yakından takip ederek araştırmaya ve kendimizi geliştirmeye sürekli yatırım yapıyoruz.</p>\n"
)

APPROACH_HTML = (
    "<p>Kalite ve süreç odaklı bir yaklaşım benimsiyoruz. Her bir müşterimizin hedefleri ve ihtiyaçları farklı olduğundan, "
    "standart kalıplar yerine markanıza özel kurgulanmış bütünsel dijital pazarlama çözümleri sunuyoruz.</p>\n"
    "<p>Esnekliği, çeşitliliği ve yakın işbirliği kültürünü değerli buluyoruz. Markalarımızla güçlü ve şeffaf ilişkiler kuruyor; "
    "Google, Meta, TikTok ve Yandex resmi partnerliklerimizle en güncel reklam teknolojilerini işiniz için uyguluyoruz.</p>\n"
    "<p>Dijital dünyada hızın belirleyici olduğunun bilinciyle hareket ediyoruz. Acil ihtiyaçları çevik bir şekilde ele alıyor; "
    "kalite, esneklik ve hızı koruyarak markanıza daha fazla müşteri, satış ve sürdürülebilir büyüme kazandırıyoruz.</p>\n"
)

CULTURE_HTML = "<em>Özgürlük ve sorumluluk</em> yaptığımız her işin temelidir."
CULTURE_BTN_TEXT = "Randevu Planlayın"
CULTURE_BTN_HREF = "/iletisim/"

PARTNERS_INTRO_HTML = (
    "<p>Roasist’in özelleştirilmiş pazarlama yaklaşımlarıyla markanızın gerçek potansiyelini ortaya çıkarıyoruz. "
    "Bize güvenen iş ortaklarımızın dijital varlıklarını güçlendiriyor, pazarlama güçlerini ölçülebilir sonuçlarla artırıyoruz.</p>\n"
)

TEAM_INTRO_HTML = (
    "<p>Performans pazarlaması, kurumsal SEO, kreatif tasarım ve web geliştirme disiplinlerinde uzman ekibimizle "
    "dijital varlıklarınızı güçlendiriyor ve işinizi büyütüyoruz.</p>\n"
)


def parse_flight_stream(flight_str: str):
    """
    Parse a Next.js React Flight string into an ordered list of records:
      ('line', key, raw_value)  -> serialized as f"{key}:{raw_value}\\n"
      ('text', key, raw_text)   -> serialized as f"{key}:T{len(utf8_bytes):x},{raw_text}" (NO trailing newline!)
    """
    records = []
    pos = 0
    n = len(flight_str)
    header_re = re.compile(r"([0-9a-f]+):")

    while pos < n:
        if flight_str[pos] == "\n":
            pos += 1
            continue
        m = header_re.match(flight_str, pos)
        if not m:
            raise ValueError(f"Unexpected Flight token at pos {pos}: {flight_str[pos:pos+60]!r}")
        key = m.group(1)
        val_start = m.end()

        # Check if length-prefixed text chunk: T<hex>,
        tm = re.match(r"T([0-9a-f]+),", flight_str[val_start:])
        if tm:
            byte_len = int(tm.group(1), 16)
            text_start = val_start + tm.end()
            # Slice exact UTF-8 byte_len starting from text_start
            rem_bytes = flight_str[text_start:].encode("utf-8")
            chunk_text = rem_bytes[:byte_len].decode("utf-8")
            records.append(["text", key, chunk_text])
            pos = text_start + len(chunk_text)
        else:
            nl = flight_str.find("\n", val_start)
            if nl == -1:
                raw_val = flight_str[val_start:]
                pos = n
            else:
                raw_val = flight_str[val_start:nl]
                pos = nl + 1
            records.append(["line", key, raw_val])

    return records


def serialize_flight_stream(records) -> str:
    out = []
    for i, (kind, key, val) in enumerate(records):
        if kind == "text":
            b_len = len(val.encode("utf-8"))
            out.append(f"{key}:T{b_len:x},{val}")
        else:
            out.append(f"{key}:{val}\n")
    return "".join(out)


def must_replace(text: str, old: str, new: str, label: str, count: int = 1) -> str:
    actual = text.count(old)
    if actual < count:
        raise RuntimeError(f"[{label}] Expected at least {count} occurrence(s) of {old[:80]!r}, found {actual}")
    return text.replace(old, new, count) if count > 0 else text.replace(old, new)


def update_file(html_path: str, is_dist: bool):
    with open(html_path, "r", encoding="utf-8") as f:
        full_html = f.read()

    start_marker = "self.__next_f.push([1, "
    end_marker = "])</script></body></html>"
    s_idx = full_html.find(start_marker)
    e_idx = full_html.find(end_marker)
    if s_idx == -1 or e_idx == -1:
        raise RuntimeError(f"Could not find Flight markers in {html_path}")

    ssr = full_html[:s_idx]
    flight_json_literal = full_html[s_idx + len(start_marker):e_idx]
    flight_str = json.loads(flight_json_literal)

    # Verify lossless roundtrip BEFORE edits
    records = parse_flight_stream(flight_str)

    logo_prefix = f"{CDN_BASE}/images/clients-white" if is_dist else "/images/clients-white"
    badge_prefix = f"{BADGE_CDN}/images" if is_dist else "/images"

    # =========================================================================
    # 1. SSR HTML UPDATES
    # =========================================================================
    ssr = ssr.replace('<html lang="en"', '<html lang="tr"', 1)

    # 1a. Head Meta descriptions & OpenGraph
    old_meta_desc_amp = "We are KOTA, award-winning Creative Studio based in London &amp; New York. Meet our expert team of creative designers, developers and strategists."
    ssr = ssr.replace(old_meta_desc_amp, ROASIST_DESC)
    ssr = ssr.replace('href="https://kota.co.uk/agency"', 'href="https://www.roasist.com/hakkimizda/"')
    ssr = ssr.replace('content="https://kota.co.uk/agency/"', 'content="https://www.roasist.com/hakkimizda/"')
    ssr = ssr.replace('content="KOTA"', 'content="Roasist"')
    ssr = ssr.replace('content="en_US"', 'content="tr_TR"')
    ssr = ssr.replace('content="https://www.facebook.com/kotacreative/"', 'content="https://www.facebook.com/roasistt"')
    ssr = ssr.replace('content="@kotacreative"', 'content="@roasist"')

    # Preload client logos in <head>
    old_kota_logos = [
        "https://kota-content.b-cdn.net/app/uploads/2023/10/Jamie-oliver.svg",
        "https://kota-content.b-cdn.net/app/uploads/2023/10/comptoir-libanais-1.svg",
        "https://kota-content.b-cdn.net/app/uploads/2023/10/british-red-cross.svg",
        "https://kota-content.b-cdn.net/app/uploads/2023/10/sym.svg",
        "https://kota-content.b-cdn.net/app/uploads/2023/10/penguin.svg",
        "https://kota-content.b-cdn.net/app/uploads/2023/10/raw.svg",
        "https://kota-content.b-cdn.net/app/uploads/2023/10/penhaligons.svg",
        "https://kota-content.b-cdn.net/app/uploads/2023/10/stoli.svg",
        "https://kota-content.b-cdn.net/app/uploads/2023/10/bounce.svg",
        "https://kota-content.b-cdn.net/app/uploads/2023/10/tangerine.svg",
        "https://kota-content.b-cdn.net/app/uploads/2023/10/tribepad.svg",
        "https://kota-content.b-cdn.net/app/uploads/2023/10/matchroom.svg",
        "https://kota-content.b-cdn.net/app/uploads/2023/10/diageo.svg",
        "https://kota-content.b-cdn.net/app/uploads/2023/10/sonovate.svg",
        "https://kota-content.b-cdn.net/app/uploads/2023/10/saatchi.svg",
    ]
    for idx_logo, old_logo_url in enumerate(old_kota_logos, 1):
        new_logo_url = f"{logo_prefix}/ref-{idx_logo:02d}.png"
        ssr = ssr.replace(old_logo_url, new_logo_url)

    # Preload footer partner badges in <head> & SSR Footer
    footer_badge_map = [
        ("https://kota-content.b-cdn.net/app/uploads/2024/06/DAN-1-500x167.png", f"{badge_prefix}/badge-google-partner-w.svg"),
        ("https://kota-content.b-cdn.net/app/uploads/2023/10/clutch.svg", f"{badge_prefix}/badge-meta-partner-w.svg"),
        ("https://kota-content.b-cdn.net/app/uploads/2023/10/awwwards.svg", f"{badge_prefix}/badge-tiktok-partner-w.svg"),
        ("https://kota-content.b-cdn.net/app/uploads/2023/10/cssda.svg", f"{badge_prefix}/badge-ai-seo-w.svg"),
    ]
    for old_b, new_b in footer_badge_map:
        ssr = ssr.replace(old_b, new_b)

    # 1b. SSR Navigation Menu (matches Flight 1c 100%)
    old_ssr_nav = (
        '<nav class="PrimaryNavigation_navigation__l8Jgb"><ul>'
        '<li><a href="/referanslar//">Work</a></li>'
        '<li><a href="https://kota.co.uk/agency/">Hakkımızda</a></li>'
        '<li><div class="PrimaryNavigation_parent__bfX37">Services'
        '<figure class="PrimaryNavigation_toggleSign__XESvT "><span class="PrimaryNavigation_toggleInner__Lz3QB">'
        '<span class="PrimaryNavigation_toggleLine__QUlfd"></span><span class="PrimaryNavigation_toggleLine__QUlfd"></span>'
        '</span></figure></div>'
        '<ul class="PrimaryNavigation_submenu__ryGWu ">'
        '<li><a href="https://kota.co.uk/service/brand-strategy-and-identity/">Brand strategy &amp; identity</a></li>'
        '<li><a href="https://kota.co.uk/service/web-design-development/">Web design &amp; development</a></li>'
        '<li><a href="https://kota.co.uk/service/growth-marketing/">Growth marketing</a></li>'
        '</ul></li>'
        '<li><a href="/blog//">Blog</a></li>'
        '<li><a href="https://kota.co.uk/culture/">Culture</a></li>'
        '<li><a href="https://kota.co.uk/contact/">Contact</a></li>'
        '</ul>'
    )
    new_ssr_nav = (
        '<nav class="PrimaryNavigation_navigation__l8Jgb"><ul>'
        '<li><a href="/referanslar/">Referanslar</a></li>'
        '<li><a href="/hakkimizda/">Hakkımızda</a></li>'
        '<li><div class="PrimaryNavigation_parent__bfX37">Hizmetler'
        '<figure class="PrimaryNavigation_toggleSign__XESvT "><span class="PrimaryNavigation_toggleInner__Lz3QB">'
        '<span class="PrimaryNavigation_toggleLine__QUlfd"></span><span class="PrimaryNavigation_toggleLine__QUlfd"></span>'
        '</span></figure></div>'
        '<ul class="PrimaryNavigation_submenu__ryGWu ">'
        '<li><a href="/hizmetler/performans-pazarlamasi/">Performans Pazarlaması</a></li>'
        '<li><a href="/hizmetler/web-tasarim/">Web Tasarım &amp; Geliştirme</a></li>'
        '<li><a href="/hizmetler/360-derece-dijital-pazarlama-yonetimi/">360° Dijital Pazarlama</a></li>'
        '</ul></li>'
        '<li><a href="/blog/">Blog</a></li>'
        '<li><a href="/hizmetler/seo/">Kurumsal SEO</a></li>'
        '<li><a href="/iletisim/">İletişim</a></li>'
        '</ul>'
    )
    ssr = must_replace(ssr, old_ssr_nav, new_ssr_nav, "SSR Navigation")

    # 1c. REMOVE Hero mouse-move background image trail bailout in SSR
    old_hero_tail = '<!--$!--><template data-dgst="BAILOUT_TO_CLIENT_SIDE_RENDERING"></template><!--/$--></section><section class="Mission_mission__8wC67">'
    new_hero_tail = '</section><section class="Mission_mission__8wC67">'
    ssr = must_replace(ssr, old_hero_tail, new_hero_tail, "SSR Hero Mouse Trail Removal")

    # 1d. Mission Section SSR
    ssr = must_replace(
        ssr,
        '<span class="Mission_heading__Z0yjM">Our</span><span class="Mission_heading__Z0yjM Mission_bottom__FzQ0F">Misyonumuz</span>',
        '<span class="Mission_heading__Z0yjM">Vizyon</span><span class="Mission_heading__Z0yjM Mission_bottom__FzQ0F">Misyon</span>',
        "SSR Mission Heading",
    )
    ssr = must_replace(
        ssr,
        'Dijital yatırımlarınızı şeffaf, yaratıcı ve ölçülebilir ticari büyümeye dönüştürmek.',
        MISSION_SUBHEADING,
        "SSR Mission Subheading",
    )
    old_ssr_mission_body = (
        "<p>Every pixel matters to us because we know it matters to our clients. "
        "We understand that great creativity is not simply about big ideas; it’s also about the smallest details. "
        "Our focus on the minutiae is not just an obsession, it&#8217;s a reflection of our commitment to providing "
        "the highest quality service, and we’re really proud of that.</p>\n"
    )
    ssr = must_replace(ssr, old_ssr_mission_body, MISSION_HTML, "SSR Mission Body")

    # 1e. REMOVE Video Section completely in SSR
    vid_re = re.compile(r'<section class="Video_video__ODG2u">.*?</section>', re.S)
    if not vid_re.search(ssr):
        raise RuntimeError("[SSR Video Removal] Could not find Video_video__ODG2u section!")
    ssr = vid_re.sub("", ssr, count=1)

    # 1f. Approach Section SSR
    ssr = must_replace(
        ssr,
        '<span class="Approach_heading__mbcS_">Our</span><span class="Approach_heading__mbcS_ Approach_bottom__o3s1M">Yaklaşımımız</span>',
        '<span class="Approach_heading__mbcS_">Özgün</span><span class="Approach_heading__mbcS_ Approach_bottom__o3s1M">Yaklaşım</span>',
        "SSR Approach Heading",
    )
    old_ssr_approach_body = (
        "<p>We’re not just coders who take instructions – we’re artists who take pride in being bold and draw inspiration "
        "from the wider creative world of music, film and the arts.</p>\n"
        "<p>Google, Meta, TikTok ve Yandex resmi partnerliklerimizle en güncel reklam teknolojilerini ve yapay zeka algoritmalarını "
        "markanız için uyguluyoruz.</p>\n"
        "<p>Sustainability is very close to our hearts, too. If your brand makes a positive impact on the environment, "
        "we’d relish in making it even bigger.</p>\n"
    )
    ssr = must_replace(ssr, old_ssr_approach_body, APPROACH_HTML, "SSR Approach Body")

    # 1g. Culture Section SSR
    ssr = must_replace(
        ssr,
        '<span><em>Kültürümüz</em> yaptığımız her işin temelidir.</span>',
        f'<span>{CULTURE_HTML}</span>',
        "SSR Culture Text",
    )
    ssr = must_replace(
        ssr,
        '<a class="Button_inner__fnyH6" href="culture"><span class="Button_border__hirH2"></span><span class="Button_text__IZaCD"><span class="Button_textInner__JTTHe">Detaylı İncele</span>',
        f'<a class="Button_inner__fnyH6" href="{CULTURE_BTN_HREF}"><span class="Button_border__hirH2"></span><span class="Button_text__IZaCD"><span class="Button_textInner__JTTHe">{CULTURE_BTN_TEXT}</span>',
        "SSR Culture Button",
    )

    # 1h. Partners Section SSR
    old_ssr_partners_intro = (
        "<p>The brands we partner with are looking to push their industry boundaries, and ready to invest quality resources "
        "into their digital. They want to work with a close, more specialist team they click with – and who they trust to "
        "take them outside of their creative comfort zone.</p>\n"
    )
    ssr = must_replace(ssr, old_ssr_partners_intro, PARTNERS_INTRO_HTML, "SSR Partners Intro")
    ssr = must_replace(
        ssr,
        '<span class="Partners_heading__AOTNV">Our</span><span class="Partners_heading__AOTNV Partners_bottom__5DSXe">Partnerlikler</span>',
        '<span class="Partners_heading__AOTNV">Güçlü</span><span class="Partners_heading__AOTNV Partners_bottom__5DSXe">Markalar</span>',
        "SSR Partners Heading",
    )

    # 1i. Team Intro SSR (appears twice: desktop & mobile)
    old_ssr_team_intro = (
        "<p>We're proud to be a Certified Great Place to Work®! You'll find us working across Creative Web Design, "
        "Web Development, Branding, and Dijital Pazarlama. </p>\n"
    )
    if ssr.count(old_ssr_team_intro) != 2:
        raise RuntimeError(f"Expected 2 Team intros in SSR, found {ssr.count(old_ssr_team_intro)}")
    ssr = ssr.replace(old_ssr_team_intro, TEAM_INTRO_HTML)

    # 1j. SSR Footer localization (matching Flight 1e 100%)
    ssr = ssr.replace(
        '<li><a href="/contact/">Contact</a></li><li><a href="/faqs/">FAQs</a></li><li><a href="/privacy-policy/">Privacy Policy</a></li>',
        '<li><a href="/iletisim/">İletişim</a></li><li><a href="/hizmetler/">S.S.S.</a></li><li><a href="/gizlilik-politikasi-ve-kullanim-sartlari/">Gizlilik Politikası</a></li>',
    )
    ssr = ssr.replace('>Our sectors :</span>', '>Hizmetlerimiz :</span>')
    old_ssr_sectors = (
        '<a class="Footer_sectorItem__0Cx14" href="https://kota.co.uk/agencies/">Kurumsal</a>'
        '<a class="Footer_sectorItem__0Cx14" href="https://kota.co.uk/b2b-tech-software-saas/">SaaS and Tech</a>'
        '<a class="Footer_sectorItem__0Cx14" href="https://kota.co.uk/b2b-transformation/">B2B Transformation</a>'
        '<a class="Footer_sectorItem__0Cx14" href="https://kota.co.uk/healthcare/">Healthcare</a>'
        '<a class="Footer_sectorItem__0Cx14" href="https://kota.co.uk/media-entertainment/">Media &amp; Entertainment</a>'
        '<a class="Footer_sectorItem__0Cx14" href="https://kota.co.uk/retail/">Perakende</a>'
    )
    new_ssr_sectors = (
        '<a class="Footer_sectorItem__0Cx14" href="/hizmetler/performans-pazarlamasi/">Performans Pazarlaması</a>'
        '<a class="Footer_sectorItem__0Cx14" href="/hizmetler/performans-pazarlamasi/google-reklamlari/">Google Ads</a>'
        '<a class="Footer_sectorItem__0Cx14" href="/hizmetler/performans-pazarlamasi/instagram-reklamlari/">Meta &amp; Instagram Ads</a>'
        '<a class="Footer_sectorItem__0Cx14" href="/hizmetler/seo/">Kurumsal SEO &amp; AEO</a>'
        '<a class="Footer_sectorItem__0Cx14" href="/hizmetler/web-tasarim/">Web Tasarım</a>'
        '<a class="Footer_sectorItem__0Cx14" href="/hizmetler/360-derece-dijital-pazarlama-yonetimi/">360° Dijital Yönetim</a>'
    )
    ssr = must_replace(ssr, old_ssr_sectors, new_ssr_sectors, "SSR Footer Sectors", count=2)
    ssr = must_replace(
        ssr,
        '<a class="Footer_newsletterButton__wp2hz" href="/newsletter">Sign up to our newsletter</a>',
        '<a class="Footer_newsletterButton__wp2hz" href="/iletisim/">Ücretsiz Dijital Analiz Alın</a>',
        "SSR Footer Newsletter Button",
    )
    ssr = ssr.replace("https://www.facebook.com/kotacreative/", "https://www.facebook.com/roasistt")
    ssr = ssr.replace("https://www.instagram.com/kotalondon/", "https://www.instagram.com/roasist")
    ssr = ssr.replace(
        '<a href="https://bsky.app/profile/kotacreative.bsky.social" target="_blank" rel="noopener noreferrer">Bluesky',
        '<a href="https://www.youtube.com/channel/UCY3G_IU2YJ326zGwU3_YlyA" target="_blank" rel="noopener noreferrer">YouTube',
    )

    # Defensive CSS hiding .HeroTrail and .Video_video + preventing Turkish uppercase diacritic clipping in SplitText
    extra_css = (
        "<style data-roasist-about>"
        ".HeroTrail_container__LDdco,.Video_video__ODG2u{display:none!important;pointer-events:none!important;}"
        ".LargeHeading_headingOuter__i9qcd .split-word{padding-top:0.16em;margin-top:-0.16em;padding-bottom:0.16em;margin-bottom:-0.16em;}"
        "</style></head>"
    )
    if "data-roasist-about" not in ssr:
        ssr = ssr.replace("</head>", extra_css, 1)

    # =========================================================================
    # 2. REACT FLIGHT PAYLOAD UPDATES (STRUCTURAL JSON + BYTE-EXACT T-CHUNKS)
    # =========================================================================
    for rec in records:
        kind, key, val = rec

        if kind == "text" and key == "29":
            schema_obj = json.loads(val)
            for node in schema_obj.get("@graph", []):
                t = node.get("@type")
                if t == "WebPage":
                    node["@id"] = "https://www.roasist.com/hakkimizda/"
                    node["url"] = "https://www.roasist.com/hakkimizda/"
                    node["name"] = "Hakkımızda | Roasist Dijital Pazarlama Ajansı"
                    node["isPartOf"] = {"@id": "https://www.roasist.com/#website"}
                    node["description"] = ROASIST_DESC
                    node["breadcrumb"] = {"@id": "https://www.roasist.com/hakkimizda/#breadcrumb"}
                    node["inLanguage"] = "tr-TR"
                    node["potentialAction"] = [{"@type": "ReadAction", "target": ["https://www.roasist.com/hakkimizda/"]}]
                elif t == "BreadcrumbList":
                    node["@id"] = "https://www.roasist.com/hakkimizda/#breadcrumb"
                    node["itemListElement"] = [
                        {"@type": "ListItem", "position": 1, "name": "Anasayfa", "item": "https://www.roasist.com/"},
                        {"@type": "ListItem", "position": 2, "name": "Hakkımızda"},
                    ]
                elif t == "WebSite":
                    node["@id"] = "https://www.roasist.com/#website"
                    node["url"] = "https://www.roasist.com/"
                    node["name"] = "Roasist"
                    node["publisher"] = {"@id": "https://www.roasist.com/#organization"}
                    node["inLanguage"] = "tr-TR"
                elif t == "Organization":
                    node["@id"] = "https://www.roasist.com/#organization"
                    node["name"] = "Roasist"
                    node["alternateName"] = "Roasist Dijital Pazarlama Ajansı"
                    node["url"] = "https://www.roasist.com/"
                    node["sameAs"] = [
                        "https://www.linkedin.com/company/roasist",
                        "https://www.instagram.com/roasist",
                        "https://www.facebook.com/roasistt",
                    ]
            # serialize_flight_stream will automatically compute exact hex UTF-8 byte length!
            rec[2] = json.dumps(schema_obj, ensure_ascii=False, separators=(",", ":"))

        elif kind == "line" and key == "1c":
            nav_obj = json.loads(val)
            nav_obj[3]["data"]["menu"]["menuItems"]["nodes"] = [
                {"databaseId": 936, "label": "Referanslar", "uri": "/referanslar/", "childItems": {"nodes": []}},
                {"databaseId": 946, "label": "Hakkımızda", "uri": "/hakkimizda/", "childItems": {"nodes": []}},
                {
                    "databaseId": 937,
                    "label": "Hizmetler",
                    "uri": "#",
                    "childItems": {
                        "nodes": [
                            {"databaseId": 942, "label": "Performans Pazarlaması", "uri": "/hizmetler/performans-pazarlamasi/"},
                            {"databaseId": 943, "label": "Web Tasarım & Geliştirme", "uri": "/hizmetler/web-tasarim/"},
                            {"databaseId": 941, "label": "360° Dijital Pazarlama", "uri": "/hizmetler/360-derece-dijital-pazarlama-yonetimi/"},
                        ]
                    },
                },
                {"databaseId": 938, "label": "Blog", "uri": "/blog/", "childItems": {"nodes": []}},
                {"databaseId": 939, "label": "Kurumsal SEO", "uri": "/hizmetler/seo/", "childItems": {"nodes": []}},
                {"databaseId": 940, "label": "İletişim", "uri": "/iletisim/", "childItems": {"nodes": []}},
            ]
            rec[2] = json.dumps(nav_obj, ensure_ascii=False, separators=(",", ":"))

        elif kind == "line" and key == "1e":
            foot_str = val
            foot_str = foot_str.replace("https://www.linkedin.com/company/roasist/", "https://www.linkedin.com/company/roasist")
            foot_str = foot_str.replace("https://www.facebook.com/kotacreative/", "https://www.facebook.com/roasistt")
            foot_str = foot_str.replace("https://www.instagram.com/kotalondon/", "https://www.instagram.com/roasist")
            foot_str = foot_str.replace("https://bsky.app/profile/kotacreative.bsky.social", "https://www.youtube.com/channel/UCY3G_IU2YJ326zGwU3_YlyA")
            foot_str = foot_str.replace('"Bluesky"', '"YouTube"')
            foot_str = foot_str.replace('"Our sectors :"', '"Hizmetlerimiz :"')
            foot_str = foot_str.replace(
                '[["$","$L25","0",{"className":"Footer_sectorItem__0Cx14","href":"https://kota.co.uk/agencies/","children":"Kurumsal"}],'
                '["$","$L25","1",{"className":"Footer_sectorItem__0Cx14","href":"https://kota.co.uk/b2b-tech-software-saas/","children":"SaaS and Tech"}],'
                '["$","$L25","2",{"className":"Footer_sectorItem__0Cx14","href":"https://kota.co.uk/b2b-transformation/","children":"B2B Transformation"}],'
                '["$","$L25","3",{"className":"Footer_sectorItem__0Cx14","href":"https://kota.co.uk/healthcare/","children":"Healthcare"}],'
                '["$","$L25","4",{"className":"Footer_sectorItem__0Cx14","href":"https://kota.co.uk/media-entertainment/","children":"Media & Entertainment"}],'
                '["$","$L25","5",{"className":"Footer_sectorItem__0Cx14","href":"https://kota.co.uk/retail/","children":"Perakende"}]]',
                '[["$","$L25","0",{"className":"Footer_sectorItem__0Cx14","href":"/hizmetler/performans-pazarlamasi/","children":"Performans Pazarlaması"}],'
                '["$","$L25","1",{"className":"Footer_sectorItem__0Cx14","href":"/hizmetler/performans-pazarlamasi/google-reklamlari/","children":"Google Ads"}],'
                '["$","$L25","2",{"className":"Footer_sectorItem__0Cx14","href":"/hizmetler/performans-pazarlamasi/instagram-reklamlari/","children":"Meta & Instagram Ads"}],'
                '["$","$L25","3",{"className":"Footer_sectorItem__0Cx14","href":"/hizmetler/seo/","children":"Kurumsal SEO & AEO"}],'
                '["$","$L25","4",{"className":"Footer_sectorItem__0Cx14","href":"/hizmetler/web-tasarim/","children":"Web Tasarım"}],'
                '["$","$L25","5",{"className":"Footer_sectorItem__0Cx14","href":"/hizmetler/360-derece-dijital-pazarlama-yonetimi/","children":"360° Dijital Yönetim"}]]',
            )
            for old_b, new_b in footer_badge_map:
                foot_str = foot_str.replace(old_b, new_b)
            foot_str = foot_str.replace(
                '{"className":"Footer_newsletterButton__wp2hz","href":"/newsletter","children":"Sign up to our newsletter"}',
                '{"className":"Footer_newsletterButton__wp2hz","href":"/iletisim/","children":"Ücretsiz Dijital Analiz Alın"}',
            )
            # Validate JSON
            json.loads(foot_str)
            rec[2] = foot_str

        elif kind == "line" and key == "12":
            data12 = json.loads(val)

            # 2a. Head meta array in data12[0]
            head_str = json.dumps(data12[0], ensure_ascii=False, separators=(",", ":"))
            head_str = head_str.replace(
                "We are KOTA, award-winning Creative Studio based in London & New York. Meet our expert team of creative designers, developers and strategists.",
                ROASIST_DESC,
            )
            head_str = head_str.replace('"href":"https://kota.co.uk/agency"', '"href":"https://www.roasist.com/hakkimizda/"')
            head_str = head_str.replace('"content":"https://kota.co.uk/agency/"', '"content":"https://www.roasist.com/hakkimizda/"')
            head_str = head_str.replace('"content":"KOTA"', '"content":"Roasist"')
            head_str = head_str.replace('"content":"en_US"', '"content":"tr_TR"')
            head_str = head_str.replace('"content":"https://www.facebook.com/kotacreative/"', '"content":"https://www.facebook.com/roasistt"')
            head_str = head_str.replace('"content":"@kotacreative"', '"content":"@roasist"')
            data12[0] = json.loads(head_str)

            # 2b. Page sections in data12[2]
            sections = data12[2][3]["children"]

            # Section 0: Hero -> fix h1 ("<i></i>Hakkımızda") & REMOVE mouse-hover image trail!
            hero_sec = sections[0]
            assert hero_sec[3]["className"] == "Hero_hero__zbooM"
            hero_container = hero_sec[3]["children"][0]
            hero_bottom = hero_container[3]["children"][1]
            hero_h1 = hero_bottom[3]["children"][0]
            hero_h1[3]["children"][3]["children"][3]["dangerouslySetInnerHTML"]["__html"] = "<i></i>Hakkımızda"
            # Replace second child ($2e -> $L30 HeroTrail mouse-hover images) with False!
            hero_sec[3]["children"][1] = False

            # Section 1: Mission
            mission_sec = sections[1]
            assert mission_sec[3]["className"] == "Mission_mission__8wC67"
            m_children = mission_sec[3]["children"][3]["children"]
            # Heading spans: "Vizyon" / "Misyon"
            m_spans = m_children[0][3]["children"][3]["children"]
            m_spans[0][3]["children"] = "Vizyon"
            m_spans[1][3]["children"] = "Misyon"
            # Subheading
            m_children[2][3]["children"][3]["children"] = MISSION_SUBHEADING
            # Main text (Freud quote + Roasist story)
            m_children[3][3]["children"][3]["children"][3]["dangerouslySetInnerHTML"]["__html"] = MISSION_HTML

            # Section 2: Video ($L34) -> REMOVE COMPLETELY!
            assert sections[2][1] == "$L34"
            sections[2] = False

            # Section 3: Approach
            approach_sec = sections[3]
            assert approach_sec[3]["className"] == "Approach_approach__l9ADx"
            a_children = approach_sec[3]["children"][3]["children"]
            a_spans = a_children[0][3]["children"][3]["children"]
            a_spans[0][3]["children"] = "Özgün"
            a_spans[1][3]["children"] = "Yaklaşım"
            a_children[3][3]["children"][3]["children"][3]["dangerouslySetInnerHTML"]["__html"] = APPROACH_HTML

            # Section 4: Culture
            culture_sec = sections[4]
            assert culture_sec[3]["className"] == "Culture_culture__lmpEt"
            c_container_children = culture_sec[3]["children"][1][3]["children"]
            c_container_children[0][3]["children"][3]["children"][3]["dangerouslySetInnerHTML"]["__html"] = CULTURE_HTML
            c_btn = c_container_children[1][3]["children"]
            c_btn[3]["text"] = CULTURE_BTN_TEXT
            c_btn[3]["href"] = CULTURE_BTN_HREF

            # Section 5: Partners
            partners_sec = sections[5]
            assert partners_sec[3]["className"] == "Partners_partners__jBo8y"
            p_container_children = partners_sec[3]["children"][1][3]["children"]
            p_container_children[0][3]["children"][3]["children"][3]["dangerouslySetInnerHTML"]["__html"] = PARTNERS_INTRO_HTML
            p_spans = p_container_children[1][3]["children"][0][3]["children"][3]["children"]
            p_spans[0][3]["children"] = "Güçlü"
            p_spans[1][3]["children"] = "Markalar"
            logo_items = p_container_children[2][3]["children"][3]["children"][3]["children"]
            assert len(logo_items) == 15
            for idx_logo, item in enumerate(logo_items, 1):
                item[3]["children"][3]["src"] = f"{logo_prefix}/ref-{idx_logo:02d}.png"

            # Section 7: Team intro
            team_sec = sections[7]
            assert team_sec[1] == "$L3b"
            team_sec[3]["data"]["intro"] = TEAM_INTRO_HTML

            rec[2] = json.dumps(data12, ensure_ascii=False, separators=(",", ":"))

        elif kind == "line" and key == "0":
            # In RootLayout HTML element, lang="en" -> lang="tr"
            rec[2] = val.replace('"lang":"en"', '"lang":"tr"')

    new_flight_str = serialize_flight_stream(records)

    # Verify serialized Flight stream re-parses cleanly with 0 errors and all JSON lines valid!
    verify_records = parse_flight_stream(new_flight_str)
    assert len(verify_records) == len(records), f"Record count mismatch: {len(verify_records)} != {len(records)}"
    for kind, key, val in verify_records:
        if kind == "text" and key == "29":
            json.loads(val)  # Must be 100% valid JSON!

    new_flight_literal = json.dumps(new_flight_str, ensure_ascii=False).replace("<", "\\u003c")
    out_html = ssr + start_marker + new_flight_literal + end_marker

    # Sanity checks: zero double-https, zero agency-header-hover, zero Kota-Showreel
    doubles = re.findall(r'https?://[^\s"\'<>]+https?://[^\s"\'<>]+', out_html)
    if doubles:
        raise RuntimeError(f"Malformed double URL detected in {html_path}: {doubles}")
    assert "agency-header-hover" not in out_html, "Hero hover images still present!"
    assert "Kota-Showreel" not in out_html, "Showreel video still present!"
    assert "Short-Preview-Agency" not in out_html, "Preview video still present!"
    assert "Video_video__ODG2u></section>" not in out_html
    assert '<section class="Video_video__ODG2u">' not in out_html

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(out_html)

    print(f"OK -> {html_path} ({len(out_html)} bytes, {len(verify_records)} Flight records verified)")


if __name__ == "__main__":
    update_file(os.path.join(ROOT, "public", "hakkimizda", "index.html"), is_dist=False)
    update_file(os.path.join(ROOT, "dist", "hakkimizda", "index.html"), is_dist=True)
