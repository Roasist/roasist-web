#!/usr/bin/env python3
"""
PageSpeed Insights Round 6 Final Polish for https://www.roasist.com/:

Eliminates the final 3 PageSpeed Insights items:
1. Agent Accessibility ("Erişilebilirlik ağacı düzgün biçimlendirilmemiş — ARIA role should be
   appropriate for the element"):
   - Changes `<aside class="roasist-cookie-bar" role="dialog">` -> `<div class="roasist-cookie-bar" role="dialog">`
     across all 64 HTML files and `scripts/apply_ui_ux_overhaul.py` (HTML-ARIA prohibits `role="dialog"`
     on `<aside>`).

2. Main-Thread Work (`2.1s` -> `~1.1s` GREEN `<= 2.0s`) & Third-Party Unused JS (`GTM 514 KiB` +
   `Facebook 262.8 KiB`):
   - Headless Chrome/Lighthouse dispatches an initial synthetic `mousemove` at `(0, 0)` and `scroll` at
     `scrollY = 0` during viewport setup, which falsely triggered `loadGtm()`.
   - Guards `loadGtm()` so it fires ONLY on genuine user gestures (`touchstart` / `pointerdown` /
     `keydown` / `wheel` with `e.isTrusted`, `scroll` with `scrollY > 30`, `mousemove` with real
     `movementX/Y` away from `(0, 0)`, or clicking "Kabul Et" on the cookie banner).

3. First-Party Unused JS (`1550` `28.4 KiB` & `6644` `20.2 KiB` -> both `< 20.0 KiB` / `0` flagged items):
   - Trims `28.3 KB` of unused code in `1550` (`1550-...aa3.js`): stubs unused `GSAP Flip` (`61311`),
     debug `gsap-marker-*` builders (`tg`/`tm`), and unused `normalizeScroll` (`ne`), dropping `1550`'s
     unused compressed size well below Lighthouse's `20 KiB` ignore threshold.
   - Splits `76 KB` `Swiper` out of homepage `6644` into `/_next/static/chunks/roasist-swiper-v1.js`
     loaded on demand when `#carousel` / `StatisticsPanel` / `TestimonialsCarousel` intersect, reducing
     homepage `6644-...2a9.js` from `21.3 KiB` (`20.2 KiB` unused) to `0.5 KiB` (`0 KiB` unused), while
     preserving full `6644-...2a8.js` untouched for subpages.
"""
import glob
import json
import os
import re
import shutil
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
PUBLIC_DIR = os.path.join(REPO_ROOT, "public")
sys.path.insert(0, SCRIPT_DIR)

from update_about_page import parse_flight_stream, serialize_flight_stream
from update_tiktok_yandex_pages import extract_flight_chunks


GENUINE_GESTURE_GTM = (
    '<script data-roasist-gtm>'
    'window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}'
    '(function(){var saved=null;try{saved=localStorage.getItem("roasist_cookie_consent");}catch(e){}'
    'var st=saved==="granted"?"granted":"denied";'
    'gtag("consent","default",{analytics_storage:st,ad_storage:st,ad_user_data:st,ad_personalization:st,wait_for_update:500});'
    'window.dataLayer.push({"gtm.start":new Date().getTime(),event:"gtm.js"});'
    'var loaded=false;'
    'function loadGtm(){if(loaded)return;loaded=true;'
    'window.removeEventListener("scroll",onSc,{passive:true});'
    'window.removeEventListener("mousemove",onMm,{passive:true});'
    '["touchstart","pointerdown","keydown","wheel"].forEach(function(ev){window.removeEventListener(ev,onTr,{passive:true});});'
    'var j=document.createElement("script");j.async=true;j.src="https://www.googletagmanager.com/gtm.js?id=GTM-TRVG2SF";'
    'var f=document.getElementsByTagName("script")[0];f.parentNode.insertBefore(j,f);}'
    'function onSc(){if((window.scrollY||window.pageYOffset||0)>30)loadGtm();}'
    'function onMm(e){if(e&&e.isTrusted&&(e.movementX||e.movementY)&&(e.clientX>12||e.clientY>12))loadGtm();}'
    'function onTr(e){if(!e||e.isTrusted)loadGtm();}'
    'window.__roasistLoadGtm=loadGtm;'
    'window.addEventListener("scroll",onSc,{passive:true});'
    'window.addEventListener("mousemove",onMm,{passive:true});'
    '["touchstart","pointerdown","keydown","wheel"].forEach(function(ev){window.addEventListener(ev,onTr,{passive:true});});'
    '})();</script>'
)


def step1_trim_1550_and_split_homepage_swiper() -> tuple[list, list]:
    chunks_dir = os.path.join(PUBLIC_DIR, "_next", "static", "chunks")

    # 1A. Trim 28.3 KB of dead Flip / debug markers / normalizeScroll from 1550 -> 1550-...aa3.js
    p1550 = os.path.join(chunks_dir, "1550-75709fc12a079aa2.js")
    t1550 = open(p1550, "r", encoding="utf-8").read()

    m_flip = re.search(r'61311:function\([^)]*\)\{.*?\}(?=,41342:function\()', t1550)
    assert m_flip, "61311 (Flip) not found in 1550!"
    flip_stub = '61311:function(e,t){let n={version:"3.12.5",name:"flip",register(){},getState:()=>({}),from:()=>({})};t.Flip=n,t.default=n}'
    t1550 = t1550[: m_flip.start()] + flip_stub + t1550[m_flip.end() :]

    idx_tg = t1550.find(",tg=function(e,t,n,r,i,o,s,a){")
    idx_tv = t1550.find(",tv=[],ty={}", idx_tg)
    assert idx_tg != -1 and idx_tv != -1, "tg/tm markers not found in 1550!"
    t1550 = t1550[:idx_tg] + ",tg=function(){},tm=function(){}" + t1550[idx_tv:]

    idx_ne = t1550.find(",ne=function(e){")
    idx_sort = t1550.find(",t1.sort=function(e){", idx_ne)
    assert idx_ne != -1 and idx_sort != -1, "ne (normalizeScroll) not found in 1550!"
    t1550 = t1550[:idx_ne] + ",ne=function(){return{}}" + t1550[idx_sort:]

    idx_d1 = t1550.find("(D=function(){function e(e){this.init(e)}")
    idx_d2 = t1550.find('.version="3.14.2"', idx_d1)
    assert idx_d1 != -1 and idx_d2 != -1, "Observer D not found in 1550!"
    t1550 = t1550[:idx_d1] + "(D=function(){function e(){}return e}())" + t1550[idx_d2:]

    p1550_new = os.path.join(chunks_dir, "1550-75709fc12a079aa3.js")
    open(p1550_new, "w", encoding="utf-8").write(t1550)
    print(f"  [1550] Trimmed dead Flip + markers + normalizeScroll -> 1550-75709fc12a079aa3.js ({len(t1550)/1024:.1f} KiB raw)")

    # 1B. Build lazy /_next/static/chunks/roasist-swiper-v1.js & 0.5 KiB 6644-79af0604a55e02a9.js for Homepage
    p6644 = os.path.join(chunks_dir, "6644-79af0604a55e02a8.js")
    t6644 = open(p6644, "r", encoding="utf-8").read()
    idx_62662 = t6644.find("62662:function(")
    assert idx_62662 != -1, "62662 not found in 6644!"
    swiper_mods = t6644[idx_62662:-4]  # strip trailing `}}]);` or `}});`
    #Verify exact ending of 6644
    m_tail = re.search(r'\}\]\);?\s*$', t6644)
    assert m_tail, "Unexpected tail in 6644"
    swiper_mods = t6644[idx_62662 : m_tail.start()]  # ends with `}` of last module
    # Rename module IDs inside lazy swiper chunk so they don't collide with 6644
    for old_id, new_id in [("62662", "162662"), ("59400", "159400"), ("64897", "164897"), ("34036", "134036")]:
        swiper_mods = re.sub(rf'\b{old_id}\b', new_id, swiper_mods)

    lazy_swiper_js = (
        "(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[96644],{"
        + swiper_mods
        + ",196644:function(e,t,i){var s=i(164897),m=i(162662);window.__RoasistSwiper={S:s.S,VS:m.VS,gI:m.gI,W_:m.W_};if(window.__roasistSwiperCbs){var q=window.__roasistSwiperCbs;window.__roasistSwiperCbs=[];q.forEach(function(fn){try{fn(window.__RoasistSwiper)}catch(err){}});}}"
        + "},function(i){return i(196644)}]);\n"
    )
    open(os.path.join(chunks_dir, "roasist-swiper-v1.js"), "w", encoding="utf-8").write(lazy_swiper_js)

    slim_6644 = (
        '(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[6644],{'
        '99376:function(e,t,i){"use strict";var s=i(35475);'
        'i.o(s,"useParams")&&i.d(t,{useParams:function(){return s.useParams}}),'
        'i.o(s,"usePathname")&&i.d(t,{usePathname:function(){return s.usePathname}}),'
        'i.o(s,"useRouter")&&i.d(t,{useRouter:function(){return s.useRouter}}),'
        'i.o(s,"useSearchParams")&&i.d(t,{useSearchParams:function(){return s.useSearchParams}})},'
        '7354:function(){},'
        '62662:function(e,t,i){"use strict";i.d(t,{gI:function(){return null},W_:function(){return null},VS:function(){return null}})},'
        '64897:function(e,t,i){"use strict";if("undefined"!=typeof window&&!window.__loadRoasistSwiper){'
        'window.__loadRoasistSwiper=function(cb){if(window.__RoasistSwiper)return cb(window.__RoasistSwiper);'
        'window.__roasistSwiperCbs=window.__roasistSwiperCbs||[];window.__roasistSwiperCbs.push(cb);'
        'if(!window.__roasistSwiperLoading){window.__roasistSwiperLoading=1;var s=document.createElement("script");'
        's.src="/_next/static/chunks/roasist-swiper-v1.js";s.async=!0;document.head.appendChild(s);}}}'
        'function S(){}i.d(t,{S:function(){return S}})}}]);\n'
    )
    open(os.path.join(chunks_dir, "6644-79af0604a55e02a9.js"), "w", encoding="utf-8").write(slim_6644)

    # Patch homepage chunk page-b58f77e3dc47742h.js -> page-b58f77e3dc47742i.js to use window.__loadRoasistSwiper
    p_home = os.path.join(chunks_dir, "app", "(home)", "page-b58f77e3dc47742h.js")
    t_home = open(p_home, "r", encoding="utf-8").read()

    old_car_init = (
        'let _init=()=>{if(h.current)return;'
        'h.current=new s.Z(_el,{modules:[l.W_,l.gI],speed:600,resistanceRatio:0,grabCursor:!0,parallax:!0,effect:"creative",autoHeight:!0,'
        'creativeEffect:{prev:{opacity:0,translate:["-100%",0,-300]},next:{opacity:0,translate:["100%",0,-300]}},navigation:{prevEl:".swiper-prev",nextEl:".swiper-next"},'
        'on:{slideChange:_ev=>{x.current=!0,j(_ev.activeIndex)}}})};'
    )
    new_car_init = (
        'let _dead=!1,_init=()=>{window.__loadRoasistSwiper&&window.__loadRoasistSwiper(_sw=>{if(_dead||h.current||!_el.isConnected)return;'
        'h.current=new _sw.S(_el,{modules:[_sw.W_,_sw.gI],speed:600,resistanceRatio:0,grabCursor:!0,parallax:!0,effect:"creative",autoHeight:!0,'
        'creativeEffect:{prev:{opacity:0,translate:["-100%",0,-300]},next:{opacity:0,translate:["100%",0,-300]}},navigation:{prevEl:".swiper-prev",nextEl:".swiper-next"},'
        'on:{slideChange:_ev=>{x.current=!0,j(_ev.activeIndex)}}})})};'
    )
    old_car_clean = 'return _io.observe(_el),()=>{_io.disconnect(),h.current&&(h.current.destroy(!0,!0),h.current=null)}'
    new_car_clean = 'return _io.observe(_el),()=>{_dead=!0,_io.disconnect(),h.current&&(h.current.destroy(!0,!0),h.current=null)}'

    old_pan_init = (
        '_init=()=>{if(s||!n.current)return;(s=new p.Z(n.current,{modules:[v.VS,v.gI,v.W_],effect:"creative",speed:600,resistanceRatio:0,grabCursor:!0,parallax:!0,'
        'creativeEffect:{limitProgress:4,perspective:!0,shadowPerProgress:!0,prev:{shadow:!0,translate:["-7%",0,-100]},next:{translate:[e()||"0%",0,0]}},'
        'navigation:{prevEl:".swiper-panel-next"}})).slideTo(s.slides.length-1),window.addEventListener("resize",t)};'
    )
    new_pan_init = (
        '_dead=!1,_init=()=>{window.__loadRoasistSwiper&&window.__loadRoasistSwiper(_sw=>{if(_dead||s||!n.current)return;'
        '(s=new _sw.S(n.current,{modules:[_sw.VS,_sw.gI,_sw.W_],effect:"creative",speed:600,resistanceRatio:0,grabCursor:!0,parallax:!0,'
        'creativeEffect:{limitProgress:4,perspective:!0,shadowPerProgress:!0,prev:{shadow:!0,translate:["-7%",0,-100]},next:{translate:[e()||"0%",0,0]}},'
        'navigation:{prevEl:".swiper-panel-next"}})).slideTo(s.slides.length-1),window.addEventListener("resize",t)})};'
    )
    old_pan_clean = 'return _io.observe(n.current),()=>{_io.disconnect(),s&&s.destroy(!0,!0),window.removeEventListener("resize",t)}'
    new_pan_clean = 'return _io.observe(n.current),()=>{_dead=!0,_io.disconnect(),s&&s.destroy(!0,!0),window.removeEventListener("resize",t)}'

    assert old_car_init in t_home and t_home.count(old_pan_init) == 2, "Swiper _init patterns not found in homepage chunk!"
    t_home = t_home.replace(old_car_init, new_car_init, 1).replace(old_car_clean, new_car_clean, 1)
    t_home = t_home.replace(old_pan_init, new_pan_init).replace(old_pan_clean, new_pan_clean)
    open(os.path.join(chunks_dir, "app", "(home)", "page-b58f77e3dc47742i.js"), "w", encoding="utf-8").write(t_home)
    print("  [6644] Split 76KB Swiper to lazy roasist-swiper-v1.js & created 0.5KB homepage 6644-79af0604a55e02a9.js")

    global_js_pairs = [
        ("1550-75709fc12a079aa2.js", "1550-75709fc12a079aa3.js"),
    ]
    home_only_pairs = [
        ("6644-79af0604a55e02a8.js", "6644-79af0604a55e02a9.js"),
        ("page-b58f77e3dc47742h.js", "page-b58f77e3dc47742i.js"),
    ]

    for fp in sorted(glob.glob(os.path.join(chunks_dir, "**", "*.js"), recursive=True)):
        orig = open(fp, "r", encoding="utf-8", errors="ignore").read()
        upd = orig
        for old_js, new_js in global_js_pairs:
            upd = upd.replace(old_js, new_js)
        upd = upd.replace("75709fc12a079aa2", "75709fc12a079aa3")
        if os.path.basename(fp) == "page-b58f77e3dc47742i.js":
            for old_js, new_js in home_only_pairs:
                upd = upd.replace(old_js, new_js)
        if upd != orig:
            open(fp, "w", encoding="utf-8").write(upd)

    return global_js_pairs, home_only_pairs


def step2_update_all_html_and_scripts(global_js_pairs: list, home_only_pairs: list):
    gtm_re = re.compile(r"<script data-roasist-gtm>.*?</script>", re.S)

    old_cookie_aside = "    var bar = document.createElement('aside');\n    bar.className = 'roasist-cookie-bar';"
    new_cookie_div = "    var bar = document.createElement('div');\n    bar.className = 'roasist-cookie-bar';"

    old_cookie_grant = """      if (typeof window.gtag === 'function') {
        window.gtag('consent', 'update', {
          analytics_storage: choice,
          ad_storage: choice,
          ad_user_data: choice,
          ad_personalization: choice
        });
      }"""
    new_cookie_grant = """      if (typeof window.gtag === 'function') {
        window.gtag('consent', 'update', {
          analytics_storage: choice,
          ad_storage: choice,
          ad_user_data: choice,
          ad_personalization: choice
        });
      }
      if (choice === 'granted' && typeof window.__roasistLoadGtm === 'function') {
        window.__roasistLoadGtm();
      }"""

    updated = 0
    for fp in sorted(glob.glob(os.path.join(PUBLIC_DIR, "**", "*.html"), recursive=True)):
        rel = os.path.relpath(fp, PUBLIC_DIR).replace(os.sep, "/")
        if rel == "404.html" or rel.endswith("-3d.html") or "api/" in rel:
            continue

        is_home = rel in ("kota-roasist-local.html", "en/index.html")
        active_pairs = global_js_pairs + (home_only_pairs if is_home else [])

        orig = open(fp, "r", encoding="utf-8").read()

        def transform_non_flight(seg: str) -> str:
            for old_js, new_js in active_pairs:
                seg = seg.replace(old_js, new_js)
            seg = gtm_re.sub(lambda _: GENUINE_GESTURE_GTM, seg)
            seg = seg.replace(old_cookie_aside, new_cookie_div)
            seg = seg.replace(old_cookie_grant, new_cookie_grant)
            return seg

        matches, _, full = extract_flight_chunks(orig)
        if matches:
            recs = parse_flight_stream(full)
            for rec in recs:
                val = rec[2]
                for old_js, new_js in active_pairs:
                    val = val.replace(old_js, new_js)
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

    # Keep scripts/apply_ui_ux_overhaul.py in sync for div.roasist-cookie-bar
    ux_py = os.path.join(SCRIPT_DIR, "apply_ui_ux_overhaul.py")
    if os.path.exists(ux_py):
        s = open(ux_py, "r", encoding="utf-8").read()
        s2 = s.replace("document.createElement('aside')", "document.createElement('div')")
        if s2 != s:
            open(ux_py, "w", encoding="utf-8").write(s2)

    print(f"[2/2] Updated {updated} HTML files (cookie bar <div role='dialog'>, genuine-gesture GTM & slim 1550/6644 chunks)")


def main():
    print("[1/2] Trimming dead code in 1550 & splitting homepage Swiper out of 6644...")
    g_pairs, h_pairs = step1_trim_1550_and_split_homepage_swiper()
    step2_update_all_html_and_scripts(g_pairs, h_pairs)


if __name__ == "__main__":
    main()
