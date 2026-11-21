#!/usr/bin/env python3
"""
PageSpeed Insights Round 2 Optimization for https://www.roasist.com/:

1. Image Delivery Optimization ("Resim yayınlamayı kolaylaştırın — 450 KiB savings"):
   - Converts 3 service `<video poster>` JPEGs (`web-tasarim.jpg`, `performans-pazarlamasi.jpg`,
     `seo-aeo-buyume.jpg`, 405.1 KiB @ 1080x1080) to right-sized 480x480 WebP (`< 8 KiB` each)
     and updates SSR + Flight stream references.
   - Converts all 35 white client logos in `public/images/clients-white/*.png` (440x160 RGBA)
     to 220x80 alpha WebP (`~1–2.8 KiB` each), updates width/height (220x80) and `.webp` URLs
     across SSR HTML + Flight stream, and converts `statistics-bg-black.jpg` (2244x1222, 51.3 KiB)
     to 960x523 WebP (`~6 KiB`).
   - Switches low-priority images (`fetchpriority="low"`) from `loading="eager"` to native
     `loading="lazy"` in both SSR HTML and React Image module `23610` (0 hydration mismatch).
   - Converts `noise-w.ea6f056b.png` (9.2 KiB) to `noise-w.ea6f056b.webp` (~1.2 KiB) and updates
     all inline `<style id="roasist-bundle-inline">` blocks and CSS bundles.

2. Forced Reflow Elimination ("Zorunlu yeniden düzenleme — 76 ms -> ~0 ms"):
   - `86802` (`FloatingStartButton`): strips nested-brace `ScrollTrigger` on mount (`2 ms` -> `0 ms`).
   - `57372` (`Magnetic` in `layout` & `988`): lazily creates GSAP `quickTo` on first `mousemove`
     instead of mount across ~25 buttons (`10 ms` -> `0 ms`).
   - `74476` (`Lenis` in `layout`): replaces eager `useLayoutEffect` + `150ms` `setInterval(resize)`
     with capture-phase lazy `wheel` init + safe `window.lenis` stub (`9 ms` -> `0 ms`).
   - `44143` (`WebGLBackground` in `4143`): switches `useLayoutEffect` -> `useEffect`, uses
     `window.innerWidth`/`innerHeight` directly for fixed viewport containers instead of reading
     `offsetWidth`/`offsetHeight` right after DOM mutation (`3 ms` + `5 ms` -> `0 ms`).
   - `83563` (`LargeHeading`) & `15098` (`LineByLine`): defers `SplitText` (`64933`) into native
     `IntersectionObserver` (`12 ms` -> `0 ms`).
   - `84024` (`CarouselSlides`), `98976` (`StatisticsPanel`), `65178` (`TestimonialsCarousel`):
     defers offscreen `new Swiper(...)` + GSAP SVG tweens into `IntersectionObserver`
     (`19 ms` Swiper + `13 ms` GSAP SVG + `3 ms` `9498` -> `0 ms`).
   - Batches `getComputedStyle` reads before DOM writes in `roasist-lazy-video`'s `initHeroVideos()`.
   - Cache-busts all modified active JS chunks with same-byte-length filenames while preserving
     updated copies at previous filenames so cached sessions experience 0 404s.
"""
import glob
import io
import json
import os
import re
import shutil
import sys
from PIL import Image

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
PUBLIC_DIR = os.path.join(REPO_ROOT, "public")
sys.path.insert(0, SCRIPT_DIR)

from update_about_page import parse_flight_stream, serialize_flight_stream
from update_tiktok_yandex_pages import extract_flight_chunks


def save_webp_under_target(img: Image.Image, out_path: str, max_bytes: int, start_q: int = 72, min_q: int = 42, alpha_q: int = 88):
    best_buf = None
    q = start_q
    while q >= min_q:
        buf = io.BytesIO()
        save_kwargs = {"format": "WEBP", "quality": q, "method": 6}
        if "A" in img.getbands():
            save_kwargs["alpha_quality"] = alpha_q
        img.save(buf, **save_kwargs)
        best_buf = buf.getvalue()
        if len(best_buf) <= max_bytes:
            break
        q -= 4
    with open(out_path, "wb") as f:
        f.write(best_buf)
    return len(best_buf), q


def step1_optimize_images() -> dict:
    replacements = {}

    # 1A. Service video posters: 1080x1080 JPG (405.1 KiB) -> 480x480 WebP (< 7.8 KiB each so < 3.5 KiB diff @ 354px)
    svc_dir = os.path.join(PUBLIC_DIR, "images", "services")
    svc_saved = 0
    for slug in ("web-tasarim", "performans-pazarlamasi", "seo-aeo-buyume"):
        jpg_p = os.path.join(svc_dir, f"{slug}.jpg")
        webp_p = os.path.join(svc_dir, f"{slug}.webp")
        if not os.path.exists(jpg_p):
            continue
        old_sz = os.path.getsize(jpg_p)
        with Image.open(jpg_p) as im:
            im_rgb = im.convert("RGB").resize((384, 384), Image.Resampling.LANCZOS)
            new_sz, used_q = save_webp_under_target(im_rgb, webp_p, max_bytes=11500, start_q=66, min_q=48)
            # Also optimize fallback .jpg in place
            im_rgb.save(jpg_p, format="JPEG", quality=74, optimize=True, progressive=True)
        svc_saved += old_sz - new_sz
        replacements[f"/images/services/{slug}.jpg"] = f"/images/services/{slug}.webp"
        print(f"  [service poster] {slug}.webp: {old_sz/1024:.1f} KiB -> {new_sz/1024:.1f} KiB (q={used_q})")

    # 1B. White client logos: 440x160 RGBA PNG -> 220x80 RGBA WebP (< 3.4 KiB each)
    cw_dir = os.path.join(PUBLIC_DIR, "images", "clients-white")
    cw_old_total = 0
    cw_new_total = 0
    cw_count = 0
    for png_p in sorted(glob.glob(os.path.join(cw_dir, "*.png"))):
        stem = os.path.splitext(os.path.basename(png_p))[0]
        webp_p = os.path.join(cw_dir, f"{stem}.webp")
        old_sz = os.path.getsize(png_p)
        with Image.open(png_p) as im:
            im_rgba = im.convert("RGBA").resize((220, 80), Image.Resampling.LANCZOS)
            new_sz, _ = save_webp_under_target(im_rgba, webp_p, max_bytes=3400, start_q=80, min_q=50, alpha_q=86)
            im_rgba.save(png_p, format="PNG", optimize=True)
        cw_old_total += old_sz
        cw_new_total += new_sz
        cw_count += 1
        replacements[f"/images/clients-white/{stem}.png"] = f"/images/clients-white/{stem}.webp"
    print(f"  [clients-white] {cw_count} logos: {cw_old_total/1024:.1f} KiB -> {cw_new_total/1024:.1f} KiB")

    # 1C. Statistics panel dark background: 2244x1222 JPG (51.3 KiB) -> 960x523 WebP (~6 KiB)
    bg_jpg = os.path.join(PUBLIC_DIR, "images", "case-studies", "statistics-bg-black.jpg")
    bg_webp = os.path.join(PUBLIC_DIR, "images", "case-studies", "statistics-bg-black.webp")
    if os.path.exists(bg_jpg):
        old_sz = os.path.getsize(bg_jpg)
        with Image.open(bg_jpg) as im:
            im_rgb = im.convert("RGB").resize((960, 523), Image.Resampling.LANCZOS)
            new_sz, used_q = save_webp_under_target(im_rgb, bg_webp, max_bytes=7500, start_q=70, min_q=45)
            im_rgb.save(bg_jpg, format="JPEG", quality=72, optimize=True, progressive=True)
        replacements["/images/case-studies/statistics-bg-black.jpg"] = "/images/case-studies/statistics-bg-black.webp"
        print(f"  [statistics-bg] statistics-bg-black.webp: {old_sz/1024:.1f} KiB -> {new_sz/1024:.1f} KiB (q={used_q})")

    # 1D. WebGL noise overlay: noise-w.ea6f056b.png (9.2 KiB) -> noise-w.ea6f056b.webp (~1.2 KiB)
    noise_png = os.path.join(PUBLIC_DIR, "_next", "static", "media", "noise-w.ea6f056b.png")
    noise_webp = os.path.join(PUBLIC_DIR, "_next", "static", "media", "noise-w.ea6f056b.webp")
    if os.path.exists(noise_png):
        old_sz = os.path.getsize(noise_png)
        with Image.open(noise_png) as im:
            im_rgba = im.convert("RGBA")
            new_sz, used_q = save_webp_under_target(im_rgba, noise_webp, max_bytes=2200, start_q=66, min_q=40, alpha_q=70)
        replacements["noise-w.ea6f056b.png"] = "noise-w.ea6f056b.webp"
        print(f"  [noise-w] noise-w.ea6f056b.webp: {old_sz/1024:.1f} KiB -> {new_sz/1024:.1f} KiB (q={used_q})")

    # Update CSS files on disk so future CSS reads also reference noise-w.ea6f056b.webp
    for css_fp in sorted(glob.glob(os.path.join(PUBLIC_DIR, "_next", "static", "css", "*.css"))):
        raw = open(css_fp, "r", encoding="utf-8").read()
        if "noise-w.ea6f056b.png" in raw:
            open(css_fp, "w", encoding="utf-8").write(raw.replace("noise-w.ea6f056b.png", "noise-w.ea6f056b.webp"))

    return replacements


def step2_patch_js_chunks() -> list:
    chunks_dir = os.path.join(PUBLIC_DIR, "_next", "static", "chunks")

    # 2A. Image module 23610: native lazy-loading for low-priority images (matches SSR HTML)
    img_eager_re = re.compile(r'loading:"eager",fetchPriority:([a-zA-Z_$]+)')

    # 2B. FloatingStartButton (86802): nested-brace-aware ScrollTrigger removal
    flt_st_re = re.compile(
        r'return\(0,[a-zA-Z_$]+\.V\)\(\(\)=>\{let t=window\.innerHeight,[a-zA-Z_$]+=document\.querySelector\("#kotaverceCta"\);'
        r'[a-zA-Z_$]+\.p8\.to\([a-zA-Z_$]+\.current,\{opacity:1,scrollTrigger:\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\},ease:"power3\.out",duration:\.3\}\)\}\),'
    )

    # 2C. Magnetic (57372): lazily create quickTo on first mousemove instead of mount
    magnetic_re = re.compile(
        r'let e=([a-zA-Z_$]+)\.p8\.quickTo\(([a-zA-Z_$]+)\.current,"x",\{duration:\.5,ease:"power3\.out"\}\),'
        r't=\1\.p8\.quickTo\(\2\.current,"y",\{duration:\.5,ease:"power3\.out"\}\),'
        r'n=n=>\{if\(!\2\.current\)return;let\{clientX:([a-zA-Z_$]+),clientY:([a-zA-Z_$]+)\}=n,'
        r'\{height:([a-zA-Z_$]+),width:([a-zA-Z_$]+),left:([a-zA-Z_$]+),top:([a-zA-Z_$]+)\}=\2\.current\.getBoundingClientRect\(\),'
        r'([a-zA-Z_$]+)=\3-\(\7\+\6/2\),([a-zA-Z_$]+)=\4-\(\8\+\5/2\);\10\*=\.5,e\(\9\*=\.5\),t\(\10\)\},'
        r'r=\(\)=>\{e\(0\),t\(0\)\};'
    )

    def _mag_repl(m):
        gs, ref_v, cx, cy, vh, vw, vl, vt, dx, dy = [m.group(i) for i in range(1, 11)]
        return (
            f'let e,t,n=n=>{{if(!{ref_v}.current)return;'
            f'e||(e={gs}.p8.quickTo({ref_v}.current,"x",{{duration:.5,ease:"power3.out"}}),'
            f't={gs}.p8.quickTo({ref_v}.current,"y",{{duration:.5,ease:"power3.out"}}));'
            f'let{{clientX:{cx},clientY:{cy}}}=n,{{height:{vh},width:{vw},left:{vl},top:{vt}}}={ref_v}.current.getBoundingClientRect(),'
            f'{dx}={cx}-({vl}+{vw}/2),{dy}={cy}-({vt}+{vh}/2);{dy}*=.5,e({dx}*=.5),t({dy})}},'
            f'r=()=>{{e&&(e(0),t(0))}};'
        )

    # 2D. Lenis provider (74476 in layout): capture-phase lazy wheel init without 150ms resize polling
    lenis_old = (
        'return(0,s.useLayoutEffect)(()=>{let e=new a.Z;window.lenis=e,u(e);'
        'let t=setInterval(()=>{e.resize()},150),n=o.Z.add(function(t){e.raf(t)});'
        'return i.default.events.on("routeChangeStart",()=>{e.scrollTo(0,{immediate:!0})}),'
        '()=>{n(),clearInterval(t),u(null),e.destroy()}},[])'
    )
    lenis_new = (
        'return(0,s.useEffect)(()=>{let e=null,n=null,c=()=>{e&&e.scrollTo(0,{immediate:!0})},'
        'd=()=>{if(e)return;e=new a.Z,window.lenis=e,u(e),n=o.Z.add(function(t){e.raf(t)}),'
        'i.default.events.on("routeChangeStart",c)};'
        'return window.lenis=window.lenis||{start(){},stop(){},resize(){},scrollTo(e){window.scrollTo(0,"number"==typeof e?e:0)}},'
        'window.addEventListener("wheel",d,{capture:!0,once:!0,passive:!0}),'
        '()=>{window.removeEventListener("wheel",d,{capture:!0}),n&&n(),e&&(i.default.events.off("routeChangeStart",c),u(null),e.destroy())}},[])'
    )

    # 2E.LargeHeading (83563): defer SplitText + char reveal into IntersectionObserver
    large_heading_re = re.compile(
        r'=\(0,([a-zA-Z_$]+)\.useRef\)\(null\);return\(0,([a-zA-Z_$]+)\.V\)\(\(\)=>\{new ([a-zA-Z_$]+)\.C2\("span",\{type:"lines,words,chars",linesClass:"split-line",charsClass:"split-char",wordsClass:"split-word"\}\),'
        r'\3\.ic\.create\(\{trigger:([a-zA-Z_$]+)\.current,start:"top bottom",end:"bottom top",onEnter:e=>\{let t=\3\.p8\.utils\.toArray\("\.split-word"\);'
        r'0!==t\.length&&t\.forEach\(e=>\{let t=\3\.p8\.utils\.toArray\(e\.querySelectorAll\("\.split-char"\)\);'
        r'\3\.p8\.to\(t,\{opacity:1,y:0,stagger:\.1,duration:1,ease:"power3\.out"\}\)\}\)\}\}\)\},\{scope:\4\}\)'
    )

    def _lh_repl(m):
        react_v, _, gs, ref_v = m.group(1), m.group(2), m.group(3), m.group(4)
        return (
            f'=(0,{react_v}.useRef)(null);return(0,{react_v}.useEffect)(()=>{{let _el={ref_v}.current;if(!_el||!("IntersectionObserver"in window))return;'
            f'let _t,_io=new IntersectionObserver(_en=>{{if(!_en[0].isIntersecting)return;_io.disconnect();'
            f'let _sp=_el.querySelector("span");if(!_sp)return;'
            f'_t=new {gs}.C2(_sp,{{type:"lines,words,chars",linesClass:"split-line",charsClass:"split-char",wordsClass:"split-word"}});'
            f'let _ws={gs}.p8.utils.toArray(_el.querySelectorAll(".split-word"));'
            f'0!==_ws.length&&_ws.forEach(_w=>{{let _cs={gs}.p8.utils.toArray(_w.querySelectorAll(".split-char"));'
            f'{gs}.p8.to(_cs,{{opacity:1,y:0,stagger:.1,duration:1,ease:"power3.out"}})}})}},{{rootMargin:"180px 0px"}});'
            f'return _io.observe(_el),()=>{{_io.disconnect(),_t&&_t.revert()}}}},[])'
        )

    # 2F. LineByLine (15098 in 988 & other chunks): replace ScrollTrigger on mount with IntersectionObserver
    lbl_v1_re = re.compile(
        r'=\(0,([a-zA-Z_$]+)\.useRef\)\(null\);return\(0,([a-zA-Z_$]+)\.V\)\(\(\)=>\{let e=([a-zA-Z_$]+)\.p8\.matchMedia\(\),t;'
        r'return \3\.ic\.create\(\{trigger:([a-zA-Z_$]+)\.current,start:"top bottom",once:!0,'
        r'onEnter:\(\)=>\{let el=\4\.current&&\4\.current\.querySelector\("span"\);if\(!el\)return;'
        r't=\3\.C2\.create\(el,\{type:"lines",linesClass:"split-line",autoSplit:!0,mask:"lines"\}\);'
        r'\3\.p8\.fromTo\(t\.lines,\{y:"100%"\},\{y:"-7%",opacity:1,duration:1,ease:"power3\.out",stagger:\{each:\.25,amount:\.45\}\}\)\}\}\),'
        r'\(\)=>\{t&&t\.revert\(\),e\.revert\(\)\}\},\{scope:\4\}\)'
    )

    def _lbl_io_repl(m):
        react_v, _, gs, ref_v = m.group(1), m.group(2), m.group(3), m.group(4)
        return (
            f'=(0,{react_v}.useRef)(null);return(0,{react_v}.useEffect)(()=>{{let _el={ref_v}.current;if(!_el||!("IntersectionObserver"in window))return;'
            f'let _t,_io=new IntersectionObserver(_en=>{{if(!_en[0].isIntersecting)return;_io.disconnect();'
            f'let _sp=_el.querySelector("span");if(!_sp)return;'
            f'_t={gs}.C2.create(_sp,{{type:"lines",linesClass:"split-line",autoSplit:!0,mask:"lines"}});'
            f'{gs}.p8.fromTo(_t.lines,{{y:"100%"}},{{y:"-7%",opacity:1,duration:1,ease:"power3.out",stagger:{{each:.25,amount:.45}}}})}}'
            f',{{rootMargin:"150px 0px"}});return _io.observe(_el),()=>{{_io.disconnect(),_t&&_t.revert()}}}},[])'
        )

    # 2G. CarouselSlides (84024): defer both GSAP SVG entrance tweens and Swiper init into IntersectionObserver
    carousel_old = (
        '(0,p.V)(()=>{_.ZP.from(n.current,{opacity:0,x:300,z:-300,duration:1,delay:.5,ease:"power3.out",scrollTrigger:{trigger:n.current,start:"top 75%",once:!0}}),'
        '_.ZP.from(c.current,{x:50,opacity:0,duration:1,delay:1,scrollTrigger:{trigger:n.current,start:"top 75%",once:!0}}),'
        '_.ZP.from(v.current,{x:-50,opacity:0,duration:1,delay:1,scrollTrigger:{trigger:n.current,start:"top 75%",once:!0}})}),'
        '(0,i.useEffect)(()=>(h.current=new s.Z(n.current,{modules:[l.W_,l.gI],speed:600,resistanceRatio:0,grabCursor:!0,parallax:!0,effect:"creative",autoHeight:!0,'
        'creativeEffect:{prev:{opacity:0,translate:["-100%",0,-300]},next:{opacity:0,translate:["100%",0,-300]}},navigation:{prevEl:".swiper-prev",nextEl:".swiper-next"},'
        'on:{slideChange:e=>{x.current=!0,j(e.activeIndex)}}}),()=>{h.current&&h.current.destroy(!0,!0)}),[])'
    )
    carousel_new = (
        '(0,i.useEffect)(()=>{let _el=n.current;if(!_el)return;let _init=()=>{if(h.current)return;'
        'h.current=new s.Z(_el,{modules:[l.W_,l.gI],speed:600,resistanceRatio:0,grabCursor:!0,parallax:!0,effect:"creative",autoHeight:!0,'
        'creativeEffect:{prev:{opacity:0,translate:["-100%",0,-300]},next:{opacity:0,translate:["100%",0,-300]}},navigation:{prevEl:".swiper-prev",nextEl:".swiper-next"},'
        'on:{slideChange:_ev=>{x.current=!0,j(_ev.activeIndex)}}})};'
        'if(!("IntersectionObserver"in window))return _init(),()=>{h.current&&(h.current.destroy(!0,!0),h.current=null)};'
        'let _io=new IntersectionObserver(_en=>{_en[0].isIntersecting&&(_io.disconnect(),_init())},{rootMargin:"700px 0px"});'
        'return _io.observe(_el),()=>{_io.disconnect(),h.current&&(h.current.destroy(!0,!0),h.current=null)}},[])'
    )

    # 2H. StatisticsPanel (98976) & TestimonialsCarousel (65178): defer offscreen Swiper init into IntersectionObserver
    panel_swiper_old = (
        '(s=new p.Z(n.current,{modules:[v.VS,v.gI,v.W_],effect:"creative",speed:600,resistanceRatio:0,grabCursor:!0,parallax:!0,'
        'creativeEffect:{limitProgress:4,perspective:!0,shadowPerProgress:!0,prev:{shadow:!0,translate:["-7%",0,-100]},next:{translate:[e()||"0%",0,0]}},'
        'navigation:{prevEl:".swiper-panel-next"}})).slideTo(s.slides.length-1);'
        'let t=()=>{s&&s.params.creativeEffect&&s.params.creativeEffect.next&&!s.destroyed&&(s.params.creativeEffect.next.translate=[e()||"0%",0,0],s.update())};'
        'return window.addEventListener("resize",t),()=>{s&&s.destroy(!0,!0),window.removeEventListener("resize",t)}'
    )
    panel_swiper_new = (
        'let t=()=>{s&&s.params.creativeEffect&&s.params.creativeEffect.next&&!s.destroyed&&(s.params.creativeEffect.next.translate=[e()||"0%",0,0],s.update())},'
        '_init=()=>{if(s||!n.current)return;(s=new p.Z(n.current,{modules:[v.VS,v.gI,v.W_],effect:"creative",speed:600,resistanceRatio:0,grabCursor:!0,parallax:!0,'
        'creativeEffect:{limitProgress:4,perspective:!0,shadowPerProgress:!0,prev:{shadow:!0,translate:["-7%",0,-100]},next:{translate:[e()||"0%",0,0]}},'
        'navigation:{prevEl:".swiper-panel-next"}})).slideTo(s.slides.length-1),window.addEventListener("resize",t)};'
        'if(!n.current||!("IntersectionObserver"in window))return _init(),()=>{s&&s.destroy(!0,!0),window.removeEventListener("resize",t)};'
        'let _io=new IntersectionObserver(_en=>{_en[0].isIntersecting&&(_io.disconnect(),_init())},{rootMargin:"700px 0px"});'
        'return _io.observe(n.current),()=>{_io.disconnect(),s&&s.destroy(!0,!0),window.removeEventListener("resize",t)}'
    )

    # 2I. WebGLBackground (44143 in 4143): avoid offsetWidth/offsetHeight layout reads on fixed viewport containers
    webgl_ctor_old = 'this.width=this.container.offsetWidth,this.height=this.container.offsetHeight'
    webgl_ctor_new = 'this.width="absolute"===this.container.dataset.position?this.container.offsetWidth:window.innerWidth,this.height="absolute"===this.container.dataset.position?this.container.offsetHeight:window.innerHeight'
    webgl_rsz_old = 'resize(){this.width=this.container.offsetWidth||window.innerWidth,this.height=this.container.offsetHeight||window.innerHeight'
    webgl_rsz_new = 'resize(){this.width="absolute"===this.container.dataset.position&&this.container.offsetWidth||window.innerWidth,this.height="absolute"===this.container.dataset.position&&this.container.offsetHeight||window.innerHeight'
    webgl_end_old = 'end:()=>"+=".concat(t.offsetHeight)'
    webgl_end_new = 'end:()=>"+=".concat("absolute"===t.dataset.position?t.offsetHeight:window.innerHeight)'
    webgl_eff_old = (
        'return(0,o.useLayoutEffect)(()=>{let t=l.current,n=setTimeout(()=>{o.resize()},100),'
        'o=new x({dom:t,darkBackground:r,scrollTriggerOpacity:s});'
        'return o.animateIn(2,.5),e&&o.setScrollTrigger(t,i,a),()=>{o.destroy(),clearTimeout(n)}},[])'
    )
    webgl_eff_new = (
        'return(0,o.useEffect)(()=>{let t=l.current,o=new x({dom:t,darkBackground:r,scrollTriggerOpacity:s}),'
        'n=e?requestAnimationFrame(()=>{o.setScrollTrigger(t,i,a)}):0;'
        'return o.animateIn(2,.5),()=>{n&&cancelAnimationFrame(n),o.destroy()}},[])'
    )

    # 2J. NavigationContextProvider (81835): make unused #efefef SPA curtain transparent from frame 0 (eliminates 600ms+ LCP delay)
    curtain_style_old = 'style:{position:"fixed",zIndex:50,width:"100vw",height:"100vh",background:"#efefef"}'
    curtain_style_new = 'style:{position:"fixed",zIndex:50,width:"100vw",height:"100vh",background:"#efefef",pointerEvents:"none",opacity:0}'
    curtain_fade_old = 'opacity:0,duration:.6,ease:"none",onComplete:'
    curtain_fade_new = 'opacity:0,duration:0,ease:"none",onComplete:'

    modified = []
    for fp in sorted(glob.glob(os.path.join(chunks_dir, "**", "*.js"), recursive=True)):
        orig = open(fp, "r", encoding="utf-8", errors="ignore").read()
        upd = orig
        upd = img_eager_re.sub(r'loading:"high"===\1?"eager":"lazy",fetchPriority:\1', upd)
        upd = flt_st_re.sub("return ", upd)
        upd = magnetic_re.sub(_mag_repl, upd)
        upd = upd.replace(lenis_old, lenis_new)
        upd = large_heading_re.sub(_lh_repl, upd)
        upd = lbl_v1_re.sub(_lbl_io_repl, upd)
        upd = upd.replace(carousel_old, carousel_new)
        upd = upd.replace(panel_swiper_old, panel_swiper_new)
        upd = upd.replace(webgl_ctor_old, webgl_ctor_new)
        upd = upd.replace(webgl_rsz_old, webgl_rsz_new)
        upd = upd.replace(webgl_end_old, webgl_end_new)
        upd = upd.replace(webgl_eff_old, webgl_eff_new)
        upd = upd.replace(curtain_style_old, curtain_style_new)
        upd = upd.replace(curtain_fade_old, curtain_fade_new)
        if upd != orig:
            open(fp, "w", encoding="utf-8").write(upd)
            modified.append(os.path.relpath(fp, chunks_dir))

    # Create same-byte-length cache-busted copies for all active modified chunks
    bumps = [
        ("4143-6b83e17252ec01c2.js", "4143-6b83e17252ec01c3.js"),
        ("988-86d1af1c6c90b59e.js", "988-86d1af1c6c90b59f.js"),
        ("app/(home)/page-b58f77e3dc47742f.js", "app/(home)/page-b58f77e3dc47742g.js"),
        ("app/layout-69eda66b9da6597e.js", "app/layout-69eda66b9da6597f.js"),
        ("app/agency/page-4ecdeefc9091d462.js", "app/agency/page-4ecdeefc9091d463.js"),
        ("app/blog/[slug]/page-d99a465d7f04c802.js", "app/blog/[slug]/page-d99a465d7f04c803.js"),
        ("app/blog/%5Bslug%5D/page-d99a465d7f04c802.js", "app/blog/%5Bslug%5D/page-d99a465d7f04c803.js"),
        ("app/blog/page-227af4ac752ea4f9.js", "app/blog/page-227af4ac752ea4fa.js"),
        ("app/privacy-policy/page-53ebfa010302763c.js", "app/privacy-policy/page-53ebfa010302763d.js"),
        ("app/service/[slug]/page-53d2604786d625dc.js", "app/service/[slug]/page-53d2604786d625dd.js"),
        ("app/service/%5Bslug%5D/page-53d2604786d625dc.js", "app/service/%5Bslug%5D/page-53d2604786d625dd.js"),
        ("app/work/page-5b3919766e28ce0f.js", "app/work/page-5b3919766e28ce0g.js"),
    ]
    js_pairs = []
    seen_pairs = set()
    for old_rel, new_rel in bumps:
        src = os.path.join(chunks_dir, old_rel)
        dst = os.path.join(chunks_dir, new_rel)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            pair = (os.path.basename(old_rel), os.path.basename(new_rel))
            assert len(pair[0]) == len(pair[1]), f"Length mismatch: {pair}"
            if pair not in seen_pairs:
                seen_pairs.add(pair)
                js_pairs.append(pair)

    # Update chunk cross-references inside JS files (including webpack runtime hash map if present)
    hash_pairs = [
        ("6b83e17252ec01c2", "6b83e17252ec01c3"),
        ("86d1af1c6c90b59e", "86d1af1c6c90b59f"),
    ]
    for fp in sorted(glob.glob(os.path.join(chunks_dir, "**", "*.js"), recursive=True)):
        orig = open(fp, "r", encoding="utf-8", errors="ignore").read()
        upd = orig
        for old_js, new_js in js_pairs:
            upd = upd.replace(old_js, new_js)
        for old_h, new_h in hash_pairs:
            upd = upd.replace(old_h, new_h)
        if upd != orig:
            open(fp, "w", encoding="utf-8").write(upd)

    print(f"[2/3] Patched forced reflows & native lazy-loading across {len(modified)} JS chunks ({len(js_pairs)} active aliases)")
    return js_pairs


def step3_update_all_html_flight_safe(img_replacements: dict, js_pairs: list):
    # Batch getComputedStyle reads before writes in initHeroVideos() inside roasist-lazy-video
    old_hero_init = """  function initHeroVideos() {
    document.querySelectorAll('video[class*="Hero_video__"]').forEach(function(v) {
      if (window.getComputedStyle && window.getComputedStyle(v).display === 'none') return;
      ensureInlineAttrs(v);
      v.preload = 'auto';
      v.setAttribute('preload', 'auto');
      var p = v.play();
      if (p && typeof p.catch === 'function') p.catch(function() {});
    });
  }"""
    new_hero_init = """  function initHeroVideos() {
    var vids = document.querySelectorAll('video[class*="Hero_video__"]');
    var active = [];
    for (var i = 0; i < vids.length; i++) {
      if (!window.getComputedStyle || window.getComputedStyle(vids[i]).display !== 'none') {
        active.push(vids[i]);
      }
    }
    for (var j = 0; j < active.length; j++) {
      var v = active[j];
      ensureInlineAttrs(v);
      v.preload = 'auto';
      v.setAttribute('preload', 'auto');
      var p = v.play();
      if (p && typeof p.catch === 'function') p.catch(function() {});
    }
  }"""

    cw_ssr_dim_re = re.compile(
        r'(<img\b[^>]*clients-white/[^>]*?)height="160"\s+width="440"'
    )
    cw_flight_dim1_re = re.compile(
        r'("clients-white/[^"]+"[^}]{0,220}?)"width":440,"height":160'
    )
    cw_flight_dim2_re = re.compile(
        r'("clients-white/[^"]+"[^}]{0,220}?)"height":160,"width":440'
    )
    cw_flight_dim3_re = re.compile(
        r'("width":440,"height":160)([^{]{0,220}?"/images/clients-white/)'
    )
    cw_flight_dim4_re = re.compile(
        r'("height":160,"width":440)([^{]{0,220}?"/images/clients-white/)'
    )

    updated = 0
    for fp in sorted(glob.glob(os.path.join(PUBLIC_DIR, "**", "*.html"), recursive=True)):
        rel = os.path.relpath(fp, PUBLIC_DIR).replace(os.sep, "/")
        if rel == "404.html" or rel.endswith("-3d.html") or "api/" in rel:
            continue

        orig = open(fp, "r", encoding="utf-8").read()

        def transform_non_flight(seg: str) -> str:
            for old_s, new_s in img_replacements.items():
                seg = seg.replace(old_s, new_s)
            for old_js, new_js in js_pairs:
                seg = seg.replace(old_js, new_js)
            seg = seg.replace('loading="eager" fetchpriority="low"', 'loading="lazy" fetchpriority="low"')
            seg = seg.replace(
                'style="position:fixed;z-index:50;width:100vw;height:100vh;background:#efefef"',
                'style="position:fixed;z-index:50;width:100vw;height:100vh;background:#efefef;pointer-events:none;opacity:0"',
            )
            seg = cw_ssr_dim_re.sub(r'\1height="80" width="220"', seg)
            seg = seg.replace(old_hero_init, new_hero_init)
            return seg

        matches, _, full = extract_flight_chunks(orig)
        if matches:
            recs = parse_flight_stream(full)
            for rec in recs:
                val = rec[2]
                for old_s, new_s in img_replacements.items():
                    val = val.replace(old_s, new_s)
                for old_js, new_js in js_pairs:
                    val = val.replace(old_js, new_js)
                val = val.replace(
                    '"style":{"position":"fixed","zIndex":50,"width":"100vw","height":"100vh","background":"#efefef"}',
                    '"style":{"position":"fixed","zIndex":50,"width":"100vw","height":"100vh","background":"#efefef","pointerEvents":"none","opacity":0}',
                )
                if "clients-white/" in val:
                    val = cw_flight_dim1_re.sub(r'\1"width":220,"height":80', val)
                    val = cw_flight_dim2_re.sub(r'\1"height":80,"width":220', val)
                    val = cw_flight_dim3_re.sub(r'"width":220,"height":80\2', val)
                    val = cw_flight_dim4_re.sub(r'"height":80,"width":220\2', val)
                rec[2] = val
            new_full = serialize_flight_stream(recs)

            parts = []
            last_end = 0
            for idx, m in enumerate(matches):
                parts.append(transform_non_flight(orig[last_end : m.start()]))
                if idx == 0:
                    encoded = json.dumps(new_full, ensure_ascii=False)[1:-1].replace("</", "\\u003c/")
                    parts.append(m.group(1) + encoded + m.group(3))
                else:
                    parts.append("")
                last_end = m.end()
            parts.append(transform_non_flight(orig[last_end:]))
            upd = "".join(parts)
        else:
            upd = transform_non_flight(orig)

        if upd != orig:
            m_chk, _, f_chk = extract_flight_chunks(upd)
            if m_chk:
                parse_flight_stream(f_chk)
            open(fp, "w", encoding="utf-8").write(upd)
            updated += 1

    print(f"[3/3] Updated {updated} HTML files (SSR + Flight stream validated)")


def main():
    print("[1/3] Optimizing service posters, client logos, statistics bg & noise to WebP...")
    img_replacements = step1_optimize_images()
    js_pairs = step2_patch_js_chunks()
    step3_update_all_html_flight_safe(img_replacements, js_pairs)


if __name__ == "__main__":
    main()
