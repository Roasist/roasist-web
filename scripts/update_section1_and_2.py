import glob
import os
import re

PUBLIC_DIR = "/home/antigravity/Roasist/roasist-web/public"

# 1. Refine Section 1 HeroSplitTextDesktop (75103) in page-b58f77e3dc47742c.js and SSR HTML
# Using KOTA's authentic Neue Montreal (--montreal) 400 weight with balanced staggered alignment
# so 'beslenen' and 'büyüme.' never overlap with the right-hand intro paragraph.
for pf in glob.glob(f"{PUBLIC_DIR}/_next/static/chunks/app/(home)/page-*.js"):
    txt = open(pf, "r", encoding="utf-8").read()
    idx_start = txt.find('75103:function(e,t,n){')
    idx_end = txt.find('},73259:function', idx_start)
    assert idx_start != -1 and idx_end != -1
    new_75103 = '''75103:function(e,t,n){"use strict";n.d(t,{default:function(){return c}});var r=n(57437),i=n(2265),s=n(45909),a=n(23897),o=n(13253),l=n.n(o);function c(){let e=(0,i.useRef)(null);return(0,a.V)(()=>{s.p8.matchMedia().add("(min-width: 850px)",()=>{let e=s.p8.timeline({duration:1,ease:"power3.out"}),t=190,n=200,r=200;e.set(".rebelLetters",{y:"".concat(t,"px")}).set(".rebelMask",{y:"-".concat(t,"px")}).set(".rebelLetters",{opacity:1}).set(".againstLetters",{y:"".concat(n,"px")}).set(".againstMask",{y:"-".concat(n,"px")}).set(".againstLetters",{opacity:1}).set(".boringLetters",{y:"".concat(r,"px")}).set(".boringMask",{y:"-".concat(r,"px")}).set(".boringLetters",{opacity:1}).to(".rebelLetters",{y:0}).to(".rebelMask",{y:0},"<").to(".againstLetters",{y:0},"<+=0.125").to(".againstMask",{y:0},"<").to(".boringLetters",{y:0},"<+=0.125").to(".boringMask",{y:0},"<")})},{scope:e}),(0,r.jsxs)("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 1143.9 590.2",className:l().desktop,ref:e,children:[(0,r.jsxs)("defs",{children:[(0,r.jsx)("mask",{id:"rebel-mask",children:(0,r.jsx)("rect",{className:"rebelMask",x:"0",y:"0",width:"1143.9",height:"198",style:{fill:"#fff"}})}),(0,r.jsx)("mask",{id:"against-mask",children:(0,r.jsx)("rect",{className:"againstMask",x:"0",y:"175",width:"1143.9",height:"220",style:{fill:"#fff"}})}),(0,r.jsx)("mask",{id:"boring-mask",children:(0,r.jsx)("rect",{className:"boringMask",x:"0",y:"365",width:"1143.9",height:"225",style:{fill:"#fff"}})})]}),(0,r.jsxs)("g",{className:"rebelLetters",mask:"url(#rebel-mask)",style:{opacity:"1"},children:[(0,r.jsx)("rect",{x:"0",y:"0",width:"10",height:"190",fill:"transparent"}),(0,r.jsx)("text",{x:"0",y:"156",fontFamily:"var(--montreal), -apple-system, BlinkMacSystemFont, sans-serif",fontWeight:"400",fontSize:"192",letterSpacing:"-0.04em",fill:"currentColor",children:"veriden"})]}),(0,r.jsxs)("g",{className:"againstLetters",mask:"url(#against-mask)",style:{opacity:"1"},children:[(0,r.jsx)("rect",{x:"195",y:"180",width:"10",height:"200",fill:"transparent"}),(0,r.jsx)("text",{x:"195",y:"344",fontFamily:"var(--montreal), -apple-system, BlinkMacSystemFont, sans-serif",fontWeight:"400",fontSize:"192",letterSpacing:"-0.04em",fill:"currentColor",children:"beslenen"})]}),(0,r.jsxs)("g",{className:"boringLetters",mask:"url(#boring-mask)",style:{opacity:"1"},children:[(0,r.jsx)("rect",{x:"35",y:"370",width:"10",height:"200",fill:"transparent"}),(0,r.jsx)("text",{x:"35",y:"526",fontFamily:"var(--montreal), -apple-system, BlinkMacSystemFont, sans-serif",fontWeight:"400",fontSize:"192",letterSpacing:"-0.04em",fill:"currentColor",children:"büyüme."})]})]})}'''
    txt = txt[:idx_start] + new_75103 + txt[idx_end:]
    open(pf, "w", encoding="utf-8").write(txt)

# Update SSR Hero SVG in kota-roasist-local.html
html = open(f"{PUBLIC_DIR}/kota-roasist-local.html", "r", encoding="utf-8").read()
t712_start = html.find("28:T712,")
t712_end = html.find("2b:T8f6,", t712_start)
protected_t712 = html[t712_start:t712_end]
html = html[:t712_start] + "__PROTECTED_T712_BLOCK__" + html[t712_end:]

ssr_svg_start = html.find('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1143.9 590.2" class="HeroSplitTextDesktop_desktop__Bey7n">')
ssr_svg_end = html.find('</svg><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 345 226.9"', ssr_svg_start)
assert ssr_svg_start != -1 and ssr_svg_end != -1
new_ssr_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1143.9 590.2" class="HeroSplitTextDesktop_desktop__Bey7n"><defs><mask id="rebel-mask"><rect class="rebelMask" x="0" y="0" width="1143.9" height="198" style="fill:#fff"></rect></mask><mask id="against-mask"><rect class="againstMask" x="0" y="175" width="1143.9" height="220" style="fill:#fff"></rect></mask><mask id="boring-mask"><rect class="boringMask" x="0" y="365" width="1143.9" height="225" style="fill:#fff"></rect></mask></defs><g class="rebelLetters" mask="url(#rebel-mask)" style="opacity:1"><rect x="0" y="0" width="10" height="190" fill="transparent"></rect><text x="0" y="156" font-family="var(--montreal), -apple-system, BlinkMacSystemFont, sans-serif" font-weight="400" font-size="192" letter-spacing="-0.04em" fill="currentColor">veriden</text></g><g class="againstLetters" mask="url(#against-mask)" style="opacity:1"><rect x="195" y="180" width="10" height="200" fill="transparent"></rect><text x="195" y="344" font-family="var(--montreal), -apple-system, BlinkMacSystemFont, sans-serif" font-weight="400" font-size="192" letter-spacing="-0.04em" fill="currentColor">beslenen</text></g><g class="boringLetters" mask="url(#boring-mask)" style="opacity:1"><rect x="35" y="370" width="10" height="200" fill="transparent"></rect><text x="35" y="526" font-family="var(--montreal), -apple-system, BlinkMacSystemFont, sans-serif" font-weight="400" font-size="192" letter-spacing="-0.04em" fill="currentColor">büyüme.</text></g>'''
html = html[:ssr_svg_start] + new_ssr_svg + html[ssr_svg_end:]

html = html.replace("__PROTECTED_T712_BLOCK__", protected_t712)
open(f"{PUBLIC_DIR}/kota-roasist-local.html", "w", encoding="utf-8").write(html)

# 2. Apply Section 2 CSS Customizations in 84191844b30595bc.css:
# - Shift video hues from KOTA magenta/pink to Roasist Electric Violet (#7602FF) & Deep Indigo (#4F46E5)
# - Glassmorphic cards with #7602FF border/glow while preserving the 12.5rem top-right curve
# - Service tags (/hizmetler/...) with #7602FF border and hover states
css_8419 = f"{PUBLIC_DIR}/_next/static/css/84191844b30595bc.css"
txt = open(css_8419, "r", encoding="utf-8").read()
marker = "/* ROASIST_SECTION_2_CUSTOM */"
if marker in txt:
    txt = txt[:txt.find(marker)]

section2_css = f"""{marker}
/* Hero intro paragraph clean alignment on desktop */
@media (min-width:1100px){{
  .Hero_introText__wboFn{{
    right:-2%!important;
    width:28%!important;
    max-width:27ch!important;
  }}
}}

/* Section 2: Video Color Grading -> Roasist Electric Violet (#7602FF) & Deep Indigo */
.ServiceMedia_mediaContainer__WGgZa,
.CarouselSlides_carouselMedia__aqYWx {{
  position: relative !important;
  box-shadow: 0 20px 45px -15px rgba(118, 2, 255, 0.22) !important;
}}
.ServiceMedia_mediaContainer__WGgZa video,
.CarouselSlides_carouselMedia__aqYWx video,
.Sphere_particle__E2OB8 canvas,
.Sphere_lottie__kYkK_ {{
  filter: hue-rotate(-34deg) saturate(1.3) contrast(1.06) !important;
}}
.ServiceMedia_mediaContainer__WGgZa::after,
.CarouselSlides_carouselMedia__aqYWx::after {{
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(118, 2, 255, 0.24) 0%, rgba(49, 46, 129, 0.30) 100%);
  mix-blend-mode: color;
  pointer-events: none;
  z-index: 3;
}}

/* Section 2: 360 Hizmetler Glassmorphic Cards with 12.5rem top-right curve & #7602FF accents */
.ServicesPanel_panelBackground__O9mDV {{
  background: rgba(255, 255, 255, 0.84) !important;
  backdrop-filter: blur(24px) saturate(150%) !important;
  -webkit-backdrop-filter: blur(24px) saturate(150%) !important;
  border: 1.5px solid rgba(118, 2, 255, 0.24) !important;
  box-shadow: 0 28px 64px -16px rgba(118, 2, 255, 0.12), inset 0 1px 0 rgba(255, 255, 255, 0.95) !important;
}}

/* Service Tag Pills (/hizmetler/...) with Roasist Violet Glassmorphism */
.ServicesPanel_tag__JYwRk {{
  border: 1.5px solid rgba(118, 2, 255, 0.26) !important;
  background: rgba(118, 2, 255, 0.045) !important;
  color: #160933 !important;
  font-weight: 500 !important;
  transition: all 0.25s cubic-bezier(0.22, 1, 0.36, 1) !important;
}}
.ServicesPanel_tag__JYwRk:hover {{
  border-color: #7602FF !important;
  background: linear-gradient(135deg, #7602FF 0%, #4F46E5 100%) !important;
  color: #ffffff !important;
  box-shadow: 0 8px 22px -4px rgba(118, 2, 255, 0.40) !important;
  transform: translateY(-2px) !important;
}}

/* Service Card CTA Button (#7602FF accent) */
.ServicesPanel_panelText__iyjwZ .Button_border__hirH2 {{
  border-color: #7602FF !important;
}}
.ServicesPanel_panelText__iyjwZ .Button_inner__fnyH6,
.ServicesPanel_panelText__iyjwZ .Button_buttonArrow__0W9XI {{
  color: #7602FF !important;
}}

/* Approach Cards (01 / 02 / 03) & 5-Stage Methodology Carousel Glassmorphism */
.Approach_item__5N2E6 {{
  background: rgba(255, 255, 255, 0.68) !important;
  backdrop-filter: blur(20px) saturate(140%) !important;
  -webkit-backdrop-filter: blur(20px) saturate(140%) !important;
  border: 1.5px solid rgba(118, 2, 255, 0.22) !important;
  box-shadow: 0 20px 48px -14px rgba(118, 2, 255, 0.10) !important;
}}
.Approach_step__HEa5K {{
  color: #7602FF !important;
  font-weight: 600 !important;
}}
.CarouselSlides_carouselSlide__gJ_Hz {{
  background: rgba(255, 255, 255, 0.76) !important;
  backdrop-filter: blur(22px) saturate(140%) !important;
  -webkit-backdrop-filter: blur(22px) saturate(140%) !important;
  border: 1.5px solid rgba(118, 2, 255, 0.24) !important;
  box-shadow: 0 24px 56px -16px rgba(118, 2, 255, 0.12) !important;
}}
.CarouselSlides_carouselNavigationButton__PEeuA {{
  border: 1.5px solid rgba(118, 2, 255, 0.22) !important;
  background: rgba(255, 255, 255, 0.70) !important;
  color: #160933 !important;
  transition: all 0.25s ease !important;
}}
.CarouselSlides_carouselNavigationButton__PEeuA:hover {{
  border-color: #7602FF !important;
  background: rgba(118, 2, 255, 0.10) !important;
}}
.CarouselSlides_carouselNavigationButton__PEeuA.active {{
  background: linear-gradient(135deg, #7602FF 0%, #4F46E5 100%) !important;
  border-color: #7602FF !important;
  color: #ffffff !important;
  box-shadow: 0 8px 20px -4px rgba(118, 2, 255, 0.38) !important;
}}
"""

open(css_8419, "w", encoding="utf-8").write(txt + section2_css)
print("Successfully updated Section 1 (Hero typography/alignment) and Section 2 (Violet/Indigo videos & Glassmorphic cards)!")
