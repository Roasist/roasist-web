import glob
import os
import re

PUBLIC_DIR = "/home/antigravity/Roasist/roasist-web/public"

html = open(f"{PUBLIC_DIR}/kota-roasist-local.html", "r", encoding="utf-8").read()
t712_start = html.find("28:T712,")
t712_end = html.find("2b:T8f6,", t712_start)
protected_t712 = html[t712_start:t712_end]
html = html[:t712_start] + "__PROTECTED_T712_BLOCK__" + html[t712_end:]

# 1. A1: Remove text next to logo & update Hero subtitle to match www.roasist.com
html = html.replace(
    "ROASIST DIGITAL — 360° BÜYÜME &amp; KREATİF AJANS : 2026",
    ""
)
html = html.replace(
    "ROASIST DIGITAL — 360° BÜYÜME \\u0026 KREATİF AJANS : 2026",
    ""
)
html = html.replace(
    "ROASIST DIGITAL — 360° BÜYÜME & KREATİF AJANS : 2026",
    ""
)

old_intro_ssr = "İstanbul merkezli 360° dijital pazarlama, performans ve kreatif web tasarım stüdyosu; <strong>veri odaklı stratejilerle iddialı markalara rekabet üstünlüğü kazandırıyoruz.</strong>"
new_intro_ssr = "Büyüyen işletmeler için dijital pazarlama çözümleri; <strong>kapsamlı ve özelleştirilmiş dijital pazarlama hizmetlerimizle işinizi bir sonraki seviyeye taşımanıza yardımcı olalım.</strong>"
html = html.replace(old_intro_ssr, new_intro_ssr)

old_intro_rsc = "İstanbul merkezli 360° dijital pazarlama, performans ve kreatif web tasarım stüdyosu; \\u003cstrong\\u003everi odaklı stratejilerle iddialı markalara rekabet üstünlüğü kazandırıyoruz.\\u003c/strong\\u003e"
new_intro_rsc = "Büyüyen işletmeler için dijital pazarlama çözümleri; \\u003cstrong\\u003ekapsamlı ve özelleştirilmiş dijital pazarlama hizmetlerimizle işinizi bir sonraki seviyeye taşımanıza yardımcı olalım.\\u003c/strong\\u003e"
html = html.replace(old_intro_rsc, new_intro_rsc)

# 2. Fix "SEÇİLMİŞ Work" -> "SEÇİLMİŞ PROJELER" and 5 ProjectCard titles
html = html.replace('Work_bottom__rzrzH">Work<', 'Work_bottom__rzrzH">PROJELER<')
html = html.replace('Work_bottom__rzrzH\\",\\"children\\":\\"Work\\"', 'Work_bottom__rzrzH\\",\\"children\\":\\"PROJELER\\"')

project_title_replacements = [
    ('></svg>UPP</h3>', '></svg>Medistate Hospital</h3>'),
    ('\\"],\\"UPP\\"]}', '\\"],\\"Medistate Hospital\\"]}'),
    ('></svg>Copper</h3>', '></svg>DermaDerm Laboratories</h3>'),
    ('\\"],\\"Copper\\"]}', '\\"],\\"DermaDerm Laboratories\\"]}'),
    ('></svg>Bucher + Suter</h3>', '></svg>Summer Home</h3>'),
    ('\\"],\\"Bucher + Suter\\"]}', '\\"],\\"Summer Home\\"]}'),
    ('></svg>Finura</h3>', '></svg>Mobile Game Factory</h3>'),
    ('\\"],\\"Finura\\"]}', '\\"],\\"Mobile Game Factory\\"]}'),
    ('></svg>The Goat Agency</h3>', '></svg>İstanbul Medya Akademisi</h3>'),
    ('\\"],\\"The Goat Agency\\"]}', '\\"],\\"İstanbul Medya Akademisi\\"]}'),
]
for old_t, new_t in project_title_replacements:
    html = html.replace(old_t, new_t)

# 3. A2: Replace foreign logos in ÖLÇÜLEBİLİR SONUÇLAR (Statistics) and MARKA ORTAKLARIMIZ (Partners)
# with Roasist's real reference logos from www.roasist.com/referanslar/
logo_replacements = [
    # StatisticsCarousel (4 cards)
    ("https://kota-content.b-cdn.net/app/uploads/2025/04/Pison-Logo-White.svg", "/images/clients-white/ref-29.png"),
    ("https://kota-content.b-cdn.net/app/uploads/2025/04/DKA-Logo-White.svg", "/images/clients-white/ref-04.png"),
    ("https://kota-content.b-cdn.net/app/uploads/2025/04/Wogan-Logo-White.svg", "/images/clients-white/ref-11.png"),
    ("https://kota-content.b-cdn.net/app/uploads/2025/04/ISI-Logo-White.svg", "/images/clients-white/ref-14.png"),
    # Partners grid (15 slots -> 15 real Roasist reference logos)
    ("https://kota-content.b-cdn.net/app/uploads/2023/10/Jamie-oliver.svg", "/images/clients-white/ref-29.png"),
    ("https://kota-content.b-cdn.net/app/uploads/2023/10/comptoir-libanais-1.svg", "/images/clients-white/ref-14.png"),
    ("https://kota-content.b-cdn.net/app/uploads/2023/10/british-red-cross.svg", "/images/clients-white/ref-04.png"),
    ("https://kota-content.b-cdn.net/app/uploads/2023/10/sym.svg", "/images/clients-white/ref-11.png"),
    ("https://kota-content.b-cdn.net/app/uploads/2023/10/penguin.svg", "/images/clients-white/ref-12.png"),
    ("https://kota-content.b-cdn.net/app/uploads/2023/10/raw.svg", "/images/clients-white/ref-23.png"),
    ("https://kota-content.b-cdn.net/app/uploads/2023/10/penhaligons.svg", "/images/clients-white/ref-10.png"),
    ("https://kota-content.b-cdn.net/app/uploads/2023/10/stoli.svg", "/images/clients-white/ref-06.png"),
    ("https://kota-content.b-cdn.net/app/uploads/2023/10/bounce.svg", "/images/clients-white/ref-08.png"),
    ("https://kota-content.b-cdn.net/app/uploads/2023/10/tangerine.svg", "/images/clients-white/ref-20.png"),
    ("https://kota-content.b-cdn.net/app/uploads/2023/10/tribepad.svg", "/images/clients-white/ref-27.png"),
    ("https://kota-content.b-cdn.net/app/uploads/2023/10/matchroom.svg", "/images/clients-white/ref-28.png"),
    ("https://kota-content.b-cdn.net/app/uploads/2023/10/diageo.svg", "/images/clients-white/ref-09.png"),
    ("https://kota-content.b-cdn.net/app/uploads/2023/10/sonovate.svg", "/images/clients-white/ref-22.png"),
    ("https://kota-content.b-cdn.net/app/uploads/2023/10/saatchi.svg", "/images/clients-white/ref-16.png"),
    # Testimonials logos
    ("https://kota-content.b-cdn.net/app/uploads/2025/05/Florence-Logo-White.svg", "/images/clients-white/ref-01.png"),
    ("https://kota-content.b-cdn.net/app/uploads/2025/08/UPP-logo.svg", "/images/clients-white/ref-24.png"),
    ("https://kota-content.b-cdn.net/app/uploads/2023/11/tangerine-logo.svg", "/images/clients-white/ref-25.png"),
    ("https://kota-content.b-cdn.net/app/uploads/2023/11/Floan-Logo-Black.svg", "/images/clients-white/ref-26.png"),
]

for old_url, new_url in logo_replacements:
    html = html.replace(old_url, new_url)

html = html.replace("__PROTECTED_T712_BLOCK__", protected_t712)
open(f"{PUBLIC_DIR}/kota-roasist-local.html", "w", encoding="utf-8").write(html)

# 4. Update CSS in f9cbc29e5dcba8c4.css and 84191844b30595bc.css
css_f9 = f"{PUBLIC_DIR}/_next/static/css/f9cbc29e5dcba8c4.css"
txt_f9 = open(css_f9, "r", encoding="utf-8").read()
if ".Celebrating_celebrating__MdmnM{display:none!important;}" not in txt_f9:
    txt_f9 += "\n.Celebrating_celebrating__MdmnM{display:none!important;}\n"
open(css_f9, "w", encoding="utf-8").write(txt_f9)

css_8419 = f"{PUBLIC_DIR}/_next/static/css/84191844b30595bc.css"
txt_8419 = open(css_8419, "r", encoding="utf-8").read()
marker3 = "/* ROASIST_SECTION_3_CUSTOM */"
if marker3 in txt_8419:
    txt_8419 = txt_8419[:txt_8419.find(marker3)]

section3_css = f"""{marker3}
/* Hide header tagline next to logo */
.Celebrating_celebrating__MdmnM {{
  display: none !important;
}}

/* Section 3A: SEÇİLMİŞ PROJELER (ProjectCard) -> Roasist Violet (#7602FF) Filter & Glass Tags */
.ProjectCard_projectText__o770X {{
  border-color: rgba(118, 2, 255, 0.45) !important;
  background: linear-gradient(90deg, rgba(118, 2, 255, 0.12) 0%, rgba(30, 27, 75, 0.18) 100%) !important;
  backdrop-filter: blur(12px) !important;
  -webkit-backdrop-filter: blur(12px) !important;
}}
.ProjectCard_projectImage__Nfx9I {{
  position: relative !important;
  overflow: hidden !important;
  border-radius: 1.125rem !important;
  border: 1px solid rgba(118, 2, 255, 0.32) !important;
  box-shadow: 0 24px 60px -18px rgba(118, 2, 255, 0.25) !important;
}}
.ProjectCard_projectImage__Nfx9I img,
.ProjectCard_video__AheFz {{
  filter: hue-rotate(-25deg) saturate(1.22) contrast(1.06) !important;
  transition: transform 0.6s cubic-bezier(0.22, 1, 0.36, 1), filter 0.4s ease !important;
}}
.ProjectCard_project__d1wbY:hover .ProjectCard_projectImage__Nfx9I img,
.ProjectCard_project__d1wbY:hover .ProjectCard_video__AheFz {{
  transform: scale(1.03) !important;
}}
.ProjectCard_projectImage__Nfx9I::after {{
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(145deg, rgba(118, 2, 255, 0.30) 0%, rgba(49, 46, 129, 0.38) 55%, rgba(12, 6, 28, 0.65) 100%);
  mix-blend-mode: color;
  pointer-events: none;
  z-index: 3;
}}
/* Keep glassmorphic tags visible at bottom of ProjectCard and intensify overlay on hover */
.ProjectCard_imageOverlay__OCawr {{
  opacity: 1 !important;
  background: linear-gradient(180deg, rgba(10, 5, 24, 0.05) 0%, rgba(18, 8, 42, 0.35) 55%, rgba(10, 4, 26, 0.86) 100%) !important;
  transition: background 0.35s ease !important;
  z-index: 6 !important;
}}
.ProjectCard_project__d1wbY:hover .ProjectCard_imageOverlay__OCawr {{
  background: linear-gradient(180deg, rgba(118, 2, 255, 0.28) 0%, rgba(18, 8, 46, 0.82) 55%, rgba(8, 3, 22, 0.94) 100%) !important;
}}
.ProjectCard_tags__XdVcf li {{
  background: rgba(118, 2, 255, 0.28) !important;
  backdrop-filter: blur(14px) saturate(150%) !important;
  -webkit-backdrop-filter: blur(14px) saturate(150%) !important;
  border: 1px solid rgba(168, 85, 247, 0.65) !important;
  color: #ffffff !important;
  box-shadow: 0 6px 18px rgba(118, 2, 255, 0.28) !important;
}}

/* Section 3B: ÖLÇÜLEBİLİR SONUÇLAR (StatisticsCarousel) & MARKA ORTAKLARIMIZ (Partners) */
.StatisticsPanel_panel__5YHtR {{
  border-color: rgba(118, 2, 255, 0.45) !important;
  box-shadow: 0 24px 64px -18px rgba(118, 2, 255, 0.25) !important;
}}
.StatisticsPanel_heading__UrLlt {{
  background: linear-gradient(90deg, #7602FF, #00D2FF, #A855F7, #7602FF) !important;
  background-size: 200% 200% !important;
  -webkit-background-clip: text !important;
  background-clip: text !important;
}}
.StatisticsPanel_logo__Y5wQT img {{
  height: 68px !important;
  max-width: 210px !important;
  object-fit: contain !important;
}}
.Partners_logo__eDI8e {{
  opacity: 1 !important;
}}
.Partners_logo__eDI8e img {{
  max-height: 3.4rem !important;
  max-width: 82% !important;
  object-fit: contain !important;
  filter: drop-shadow(0 2px 10px rgba(118, 2, 255, 0.18)) !important;
  transition: transform 0.3s ease, opacity 0.3s ease !important;
}}
.Partners_logo__eDI8e:hover img {{
  transform: scale(1.08) !important;
}}
"""

open(css_8419, "w", encoding="utf-8").write(txt_8419 + section3_css)
print("Successfully applied A1 (removed logo text + original Roasist subtitle), A2 (Roasist reference logos), and A3 (#7602FF project filters & glass tags)!")
