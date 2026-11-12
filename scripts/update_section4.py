import os
import re

PUBLIC_DIR = "/home/antigravity/Roasist/roasist-web/public"

html = open(f"{PUBLIC_DIR}/kota-roasist-local.html", "r", encoding="utf-8").read()
t712_start = html.find("28:T712,")
t712_end = html.find("2b:T8f6,", t712_start)
protected_t712 = html[t712_start:t712_end]
html = html[:t712_start] + "__PROTECTED_T712_BLOCK__" + html[t712_end:]

# 1. A2: Testimonial Card Background Colors -> Roasist Lavender, Periwinkle & Soft Indigo Palette
color_map = [
    ("#a8e1ec", "#EDE9FE"),
    ("#f8e5cb", "#E0E7FF"),
    ("#efb2d9", "#F3E8FF"),
    ("#d7e1d3", "#DDD6FE"),
    ("#c4b5f3", "#C7D2FE"),
]
for old_c, new_c in color_map:
    html = html.replace(old_c, new_c)

# Replace 2nd testimonial logo (incentive-games.png) with Roasist ref-04.png
html = html.replace(
    "https://kota-content.b-cdn.net/app/uploads/2024/06/incentive-games.png 640w, https://kota-content.b-cdn.net/app/uploads/2024/06/incentive-games-500x303.png 500w",
    "/images/clients-white/ref-04.png"
)
html = html.replace(
    "https://kota-content.b-cdn.net/app/uploads/2024/06/incentive-games.png",
    "/images/clients-white/ref-04.png"
)

# Replace Testimonial quotes, names, and roles with real Roasist testimonials from www.roasist.com
testimonial_replacements = [
    # Quote 1 -> Burak Özhan (www.roasist.com)
    (
        "Marka konumlandırma ve performans stratejimiz her şeyin yerine oturmasını sağladı. Roasist ekibi hızlı, esnek ve dijital büyüme ile görsel kimlik konusunda olağanüstü yetenekli. Şimdiden iki iş ortağımıza tavsiye ettik!",
        "Reklam sürecinde projeye yaklaşımları, anlaşmamızın ötesinde sorumluluk alarak grafik tasarım katkısı sunmaları ve 7/24 destekleriyle işimiz için en az bizim kadar dertlenen bir ekiple çalıştığımız için şanslıyız. Roasist ile gönül rahatlığıyla çalışabilirsiniz."
    ),
    ("Shanice Daeche", "Burak Özhan"),
    (">CMO<", ">Project Program Coordinator<"),
    ('\\"CMO\\"', '\\"Project Program Coordinator\\"'),
    # Quote 2 -> Gaye Tukar (www.roasist.com)
    (
        "Estetiğin ötesinde, yeni web sitemiz inanılmaz derecede işlevsel ve hızlı. İçerik yönetim sistemi bize tam esneklik sağlarken kullanıcı deneyimini (UX) ve dönüşüm oranlarımızı zirveye taşıdı.",
        "Roasist ile yaklaşık iki senedir çalışıyoruz. Her sorumuza dürüstlükle yanıt alıyor, tüm sorunlarımızı efektif bir şekilde çözüyorlar. Öncesi-sonrası değerlendirmesi yaptığımda kazanç konusunda bize çok büyük katkıları oldu. Profesyonel yaklaşımları için çok teşekkür ederim."
    ),
    ("Jenny Frame", "Gaye Tukar"),
    ("Marketing Manager", "Girişimci & Kurucu"),
    # Quote 3 -> Celal Kandemir (www.roasist.com)
    (
        "Web, teknoloji ve kreatif tasarımı birleştiren üst düzey bir dijital yapıya ihtiyacımız vardı. İlk görüşmeden itibaren Roasist vizyonumuzu anladı ve beklentilerimizin çok ötesinde bir dijital deneyim ortaya koydu.",
        "Mesai kavramı olmaksızın sizin için çalışıyorlar. İşinde profesyonel, şeffaf ve doğrudan sonuç odaklı bir dijital pazarlama ajansı arıyorsanız Roasist'i kesinlikle tavsiye ederim."
    ),
    ("Shaun Obanion", "Celal Kandemir"),
    ("PR Manager of Universal Production Partners", "İşletme Sahibi"),
    # Quote 4 -> Medistate
    ("Bianca Cristescu  ", "Medistate Dijital Ekibi"),
    ("Bianca Cristescu", "Medistate Dijital Ekibi"),
    ("Key Account Director, ISI Global", "Kurumsal İletişim & Büyüme"),
    # Quote 5 -> DermaDerm
    ("Laurie Bushe", "DermaDerm E-Ticaret"),
    ("Head of Marketing", "Pazarlama & E-Ticaret Yönetimi"),
    # Quote 6 -> Sekiz Oniki
    ("Finn Bruce", "Sekiz Oniki Kurumsal"),
    (">Floan<", ">Yönetim Kurulu<"),
    ('\\"Floan\\"', '\\"Yönetim Kurulu\\"'),
]
for old_t, new_t in testimonial_replacements:
    html = html.replace(old_t, new_t)

# 2. A3: Update S.S.S. (FAQs 1-4) to match www.roasist.com FAQs
faq_replacements = [
    (
        "Dijital pazarlama ve web tasarım projelerinde bütçelendirme nasıl yapılıyor?",
        "Roasist hangi dijital pazarlama hizmetlerini sunuyor?"
    ),
    (
        "Projelerimizin kapsamı markanızın hedeflerine, ihtiyaç duyulan hizmet kanallarına (Performans Pazarlaması, SEO, Web Tasarım veya 360° Yönetim) ve rekabet düzeyine göre özel olarak planlanır. Şeffaf fiyatlandırma ve net kilometre taşlarıyla çalışıyoruz.",
        "Roasist; 360° Dijital Pazarlama Yönetimi, Performans Pazarlaması (Google Ads, Instagram, Facebook, TikTok, LinkedIn ve Yandex Reklamları), Arama Motoru Optimizasyonu (SEO & AEO), Dönüşüm Odaklı Web Tasarım ve Kreatif Grafik Tasarım hizmetlerini veri odaklı bir yaklaşımla sunar."
    ),
    (
        "Bir web tasarım veya dijital dönüşüm projesi ortalama ne kadar sürer?",
        "Çalışma süreciniz nasıl başlıyor?"
    ),
    (
        "Kurumsal web tasarım ve geliştirme projeleri kapsamına göre ortalama 4 ila 8 hafta sürerken, 360° dijital pazarlama, SEO ve performans büyüme programları sürekli optimizasyon döngüsüyle yürütülür. Acil lansman hedefleriniz için fazlandırılmış hızlı teslimat planları da uyguluyoruz.",
        "Sürecimiz ücretsiz ön analiz ve strateji görüşmesiyle başlar. Mevcut dijital varlıklarınızı, reklam hesaplarınızı ve sektörünüzdeki gerçek arama hacimlerini inceler; işletmenize özel KPI ve büyüme yol haritasını çıkarırız."
    ),
    (
        "Kısa süreli ve acil lansman takvimlerine uyum sağlayabiliyor musunuz?",
        "Reklam hesapları ve veriler kimin mülkiyetinde oluyor?"
    ),
    (
        "Kesinlikle! Tasarım, yazılım ve performans ekiplerimizi hızla mobilize ederek en kritik önceliklere odaklanıyor, kaliteden ödün vermeden projenizi hedeflenen lansman tarihinde yayına alıyoruz.",
        "Şeffaflık ilkemiz gereği tüm reklam hesapları (Google Ads, Meta, TikTok, LinkedIn, Yandex) ve analitik mülkleri doğrudan sizin adınıza açılır ve %100 sizin mülkiyetinizde kalır. Tüm performans verilerini 7/24 canlı olarak takip edebilirsiniz."
    ),
    (
        "Yayın sonrasında sürekli teknik destek, bakım ve optimizasyon sunuyor musunuz?",
        "Sadece tek bir hizmet (örneğin SEO veya Google Ads) alabilir miyiz?"
    ),
    (
        "Roasist olarak web sitenizi ve kampanyalarınızı yayına aldıktan sonra da yalnız bırakmıyoruz. Düzenli performans takibi, hız optimizasyonu, güvenlik güncellemeleri ve dönüşüm oranı (CRO) iyileştirmeleriyle dijital varlığınızı sürekli geliştiriyoruz.<!-- notionvc: 1e6bfa10-99db-4f7d-99c4-5fc804c8ad99 -->",
        "Evet. İhtiyacınıza göre yalnızca Google Reklamları, SEO veya Web Tasarım gibi tekil uzmanlık hizmetlerimizden faydalanabileceğiniz gibi, tüm dijital kanallarınızı kapsayan 360° Dijital Pazarlama Yönetimi modelimizle de çalışabilirsiniz."
    ),
]
for old_f, new_f in faq_replacements:
    html = html.replace(old_f, new_f)

# 3. A3: Synchronize Footer & Navigation links, phone (+90 541 507 53 50), and social links with www.roasist.com
link_replacements = [
    ("https://bsky.app/profile/kotacreative.bsky.social", "https://www.youtube.com/channel/UCY3G_IU2YJ326zGwU3_YlyA"),
    (">Bluesky<", ">YouTube<"),
    ('\\"Bluesky\\"', '\\"YouTube\\"'),
    ("https://www.facebook.com/roasist\"", "https://www.facebook.com/roasistt\""),
    ("https://www.facebook.com/roasist\\", "https://www.facebook.com/roasistt\\"),
    ("https://x.com/kotacreative", "https://twitter.com/Roasistt"),
    # Replace KOTA Cyber Essentials badge in Footer with Roasist direct phone & Istanbul location
    (
        '<a target="_blank" href="https://registry.blockmarktech.com/certificates/f2732cc3-b4f0-4dd3-85ce-fa6ee589e132/" class="Footer_cyberEssestials__2qh89"><img src="/images/cyber-essentials.svg" alt="cyber-essentials"/></a>',
        '<a href="tel:+905415075350" class="Footer_cyberEssestials__2qh89" style="color:#fff;text-decoration:none;font-size:0.95rem;opacity:0.85">+90 541 507 53 50 • İstanbul</a>'
    ),
    ("https://registry.blockmarktech.com/certificates/f2732cc3-b4f0-4dd3-85ce-fa6ee589e132/", "tel:+905415075350"),
    # Replace all remaining kota.co.uk work/service/agency links with Roasist routes
    ("https://kota.co.uk/work/pison/", "/referanslar"),
    ("https://kota.co.uk/work/dka/", "/referanslar"),
    ("https://kota.co.uk/work/wogan-coffee/", "/referanslar"),
    ("https://kota.co.uk/work/isi-global/", "/referanslar"),
    ("https://kota.co.uk/work/florence/", "/referanslar"),
    ("https://kota.co.uk/work/incentive-games/", "/referanslar"),
    ("https://kota.co.uk/work/upp/", "/referanslar"),
    ("https://kota.co.uk/work/tangerine/", "/referanslar"),
    ("https://kota.co.uk/work/floan/", "/referanslar"),
    ("https://kota.co.uk/work/", "/referanslar"),
    ("https://kota.co.uk/agency/", "/hakkimizda"),
    ("https://kota.co.uk/service/brand-strategy-and-identity/", "/hizmetler/performans-pazarlamasi"),
    ("https://kota.co.uk/service/web-design-development/", "/hizmetler/web-tasarim"),
    ("https://kota.co.uk/service/growth-marketing/", "/hizmetler/seo"),
    ("https://kota.co.uk/blog/sitecare-management-website-maintenance", "/blog"),
    ("https://kota.co.uk/blog/", "/blog"),
    ("https://kota.co.uk/culture/", "/referanslar"),
    ("https://kota.co.uk/contact/", "/iletisim"),
    ("https://kota.co.uk/agencies/", "/hizmetler/performans-pazarlamasi"),
    ("https://kota.co.uk/b2b-tech-software-saas/", "/hizmetler/performans-pazarlamasi/google-reklamlari"),
    ("https://kota.co.uk/b2b-transformation/", "/hizmetler/performans-pazarlamasi/instagram-reklamlari"),
    ("https://kota.co.uk/healthcare/", "/hizmetler/seo"),
    ("https://kota.co.uk/media-entertainment/", "/hizmetler/web-tasarim"),
    ("https://kota.co.uk/retail/", "/hizmetler/360-derece-dijital-pazarlama-yonetimi"),
    # Update Blog article links to /blog
    ("/blog/branding-inspiration-brand-design-trends-for-2026", "/blog"),
    ("/blog/design-with-guts-kotas-manifesto-for-creative-bravery", "/blog"),
    ("/blog/kota-wins-a-lovie-award-for-best-web-design-aesthetic", "/blog"),
    ("/blog/brand-first-vs-dev-first-what-actually-sets-kota-apart-and-why-it-matters", "/blog"),
    ("/blog/10-creative-websites-to-inspire-your-next-web-design-2025-update", "/blog"),
    ("/blog/web-design-inspiration-50-sites-to-bookmark", "/blog"),
    ("/blog/clutch-names-kota-a-2024-global-winner-clutch-champion-and-top-branding-company", "/blog"),
    ("/blog/kota-earns-2025-great-place-to-work-certification", "/blog"),
    ("/blog/what-your-2026-website-brief-should-include", "/blog"),
]
for old_l, new_l in link_replacements:
    html = html.replace(old_l, new_l)

html = html.replace("__PROTECTED_T712_BLOCK__", protected_t712)
open(f"{PUBLIC_DIR}/kota-roasist-local.html", "w", encoding="utf-8").write(html)

# 4. Add Section 4 CSS customizations in 84191844b30595bc.css
css_8419 = f"{PUBLIC_DIR}/_next/static/css/84191844b30595bc.css"
txt_8419 = open(css_8419, "r", encoding="utf-8").read()
marker4 = "/* ROASIST_SECTION_4_CUSTOM */"
if marker4 in txt_8419:
    txt_8419 = txt_8419[:txt_8419.find(marker4)]

section4_css = f"""{marker4}
/* Section 4A: Testimonials (Müşterilerimiz ne diyor?) -> Dark logos on Roasist Lavender cards + #7602FF border accent */
.TestimonialsPanel_panel__QSk4x {{
  border: 1.5px solid rgba(118, 2, 255, 0.22) !important;
  box-shadow: 0 24px 60px -18px rgba(118, 2, 255, 0.25) !important;
}}
.TestimonialsPanel_logo__m6tmz img {{
  filter: brightness(0) !important;
  height: 56px !important;
  width: auto !important;
  max-width: 190px !important;
  object-fit: contain !important;
}}

/* Section 4B: Güncel yazılar (Articles / Blog) -> #7602FF Filter + Glass Category Pills */
.Articles_article__3ZS4Y {{
  border-radius: 0.75rem 5rem 0.75rem 0.75rem !important;
  overflow: hidden !important;
  border: 1px solid rgba(118, 2, 255, 0.32) !important;
  box-shadow: 0 20px 50px -16px rgba(118, 2, 255, 0.22) !important;
  transition: transform 0.35s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.35s ease !important;
}}
.Articles_article__3ZS4Y:hover {{
  transform: translateY(-6px) !important;
  box-shadow: 0 28px 64px -14px rgba(118, 2, 255, 0.38) !important;
}}
.Articles_article__3ZS4Y .Articles_image__Cvgsi {{
  position: relative !important;
  overflow: hidden !important;
}}
.Articles_article__3ZS4Y .Articles_image__Cvgsi img {{
  filter: hue-rotate(-28deg) saturate(1.25) contrast(1.06) !important;
  transition: transform 0.5s cubic-bezier(0.22, 1, 0.36, 1) !important;
}}
.Articles_article__3ZS4Y:hover .Articles_image__Cvgsi img {{
  transform: scale(1.04) !important;
}}
.Articles_article__3ZS4Y .Articles_image__Cvgsi::after {{
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(118, 2, 255, 0.32) 0%, rgba(49, 46, 129, 0.38) 100%);
  mix-blend-mode: color;
  pointer-events: none;
  z-index: 2;
}}
.Articles_filterNames__mCWt8 {{
  display: inline-block !important;
  background: rgba(118, 2, 255, 0.10) !important;
  border: 1px solid rgba(118, 2, 255, 0.32) !important;
  color: #7602FF !important;
  font-weight: 600 !important;
  border-radius: 2rem !important;
  padding: 5px 12px !important;
  margin-bottom: 0.9rem !important;
}}

/* Section 4C: S.S.S. (FaqsList) & Showreel -> #7602FF accents */
.FaqsList_question__6fKon:hover .FaqsList_icon__54ODy svg path,
.FaqsList_question__6fKon:has(:checked) .FaqsList_icon__54ODy svg path {{
  fill: #7602FF !important;
}}
.Showreel_showreel__abc12 video,
section video {{
  filter: hue-rotate(-28deg) saturate(1.2) !important;
}}
"""

open(css_8419, "w", encoding="utf-8").write(txt_8419 + section4_css)
print("Successfully applied Section 4 customizations (Real Roasist testimonials + Lavender cards + Blog #7602FF filter/glass pills + S.S.S. & Footer contact sync)!")
