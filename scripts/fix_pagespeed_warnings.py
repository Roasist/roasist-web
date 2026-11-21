#!/usr/bin/env python3
"""
Resolves all 3 Google PageSpeed Insights diagnostics on https://www.roasist.com/:
  1. Network Dependency Tree (885 ms Google Fonts + CSS chain):
     - Removes blocking `@import url('https://fonts.googleapis.com/...')` from inline styles
       (site already uses self-hosted local woff2 fonts).
  2. Render-Blocking Requests (roasist-bundle-*.css — 30.7 KiB, 220 ms):
     - Rewrites relative `url(../media/...)` & `url(../../../images/...)` paths to root-relative
       `/_next/static/media/...` & `/images/...`, minifies comments/newlines, and inlines the
       bundle as `<style id="roasist-bundle-inline" data-precedence="next">` in `<head>`,
       removing external CSS `<link>` tags from both SSR HTML and Flight stream.
  3. Forced Reflow / Layout Thrashing (Zorunlu yeniden düzenleme):
     - Rewrites `roasist-arrow-rotator` with strict Read-All-First -> Write-Changed-Only batching
       and removes synchronous parse-time / mid-hydration execution (`44 ms` -> `0 ms`).
     - Replaces `ftr.getBoundingClientRect()` in `roasist-floating-cta-ctrl` with a zero-reflow
       `IntersectionObserver`.
     - Defers `data-roasist-ui` & `roasist-ux-overhaul-js` post-hydration passes until after
       `load` / `requestIdleCallback` so React hydration (`2117-*.js`) runs on a clean style tree.
     - Defers GSAP `SplitText.create` in `LineByLine` (`15098`) into `ScrollTrigger` `onEnter` (`once: true`)
       and removes redundant `ScrollTrigger` layout measurement in `FloatingStartButton` (`86802`).
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

ZERO_REFLOW_ARROW_SCRIPT = """<script id="roasist-arrow-rotator">(function(){
  function clamp(v, min, max) { return v < min ? min : (v > max ? max : v); }
  function updateArrows() {
    // PHASE 1: READ ALL GEOMETRY FIRST (0 DOM writes beforehand -> 0 forced reflow!)
    var sy = window.scrollY || window.pageYOffset || 0;
    var vh = window.innerHeight || 900;
    var heroArrows = document.querySelectorAll('.roasist-hero-title-arrow svg');
    var secArrows = document.querySelectorAll(
      '.AnimatedArrow_innerArrow__6mwTB svg, svg.ServicesHeading_arrow__L7E0F, .Partners_arrowWrapper__Xq8Wc svg, .Approach_arrow__3EkCM svg'
    );
    var tops = new Array(secArrows.length);
    for (var i = 0; i < secArrows.length; i++) {
      tops[i] = secArrows[i].getBoundingClientRect().top;
    }

    // PHASE 2: WRITE ONLY CHANGED VALUES
    var heroAngle = 45 - 45 * clamp((sy - 2) / 105, 0, 1);
    var heroStr = heroAngle.toFixed(1) + 'deg';
    for (var h = 0; h < heroArrows.length; h++) {
      if (heroArrows[h]._rRot !== heroStr) {
        heroArrows[h]._rRot = heroStr;
        heroArrows[h].style.setProperty('--roasist-arrow-rot', heroStr);
      }
    }

    var startY = vh * 0.85;
    var span = Math.max(1, startY - vh * 0.46);
    for (var j = 0; j < secArrows.length; j++) {
      var angle = 45 - 45 * clamp((startY - tops[j]) / span, 0, 1);
      var rotStr = angle.toFixed(1) + 'deg';
      var el = secArrows[j];
      if (el._rRot !== rotStr) {
        el._rRot = rotStr;
        el.style.setProperty('--roasist-arrow-rot', rotStr);
      }
    }
  }

  var ticking = false;
  function onScroll() {
    if (!ticking) {
      ticking = true;
      window.requestAnimationFrame(function() {
        ticking = false;
        updateArrows();
      });
    }
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll, { passive: true });
  window.addEventListener('load', function() {
    if ((window.scrollY || 0) > 0) onScroll();
  }, { once: true });
})();</script>"""

ZERO_REFLOW_FLOATING_CTRL = """<script id="roasist-floating-cta-ctrl">
(function() {
  var isEn = document.documentElement.lang === 'en' || window.location.pathname.indexOf('/en/') === 0 || window.location.pathname === '/en';
  var targetLabel = isEn ? 'Get a Quote' : 'Teklif Al';
  var targetHref = isEn ? '/en/contact-us/' : '/iletisim/';
  var ftrInView = false;

  function syncFloatingLabel() {
    var btn = document.querySelector('.FloatingStartButton_button__Ncnrf');
    if (!btn) return;
    if (btn.getAttribute('href') !== targetHref) btn.setAttribute('href', targetHref);
    var txtWrap = btn.querySelector('.FloatingStartButton_text__70x9M');
    if (txtWrap) {
      var sp = txtWrap.querySelector('span');
      if (sp && sp.textContent !== targetLabel) sp.textContent = targetLabel;
    }
  }

  function applyClasses() {
    var sy = window.scrollY || window.pageYOffset || 0;
    var menuOpen = !!document.querySelector('[class*="PrimaryNavigation_active"]');
    var cookieOpen = !!document.querySelector('.roasist-cookie-bar.is-visible');
    document.body.classList.toggle('roasist-footer-in-view', ftrInView);
    document.body.classList.toggle('roasist-menu-open', menuOpen);
    document.body.classList.toggle('roasist-cookie-open', cookieOpen);
    document.body.classList.toggle('roasist-show-floating-cta', sy > 180 && !ftrInView && !menuOpen);
  }

  function observeFooter() {
    var ftr = document.querySelector('footer[class*="Footer_footer"]');
    if (!ftr || ftr.dataset.roasistFtrObs || !('IntersectionObserver' in window)) return;
    ftr.dataset.roasistFtrObs = '1';
    new IntersectionObserver(function(entries) {
      ftrInView = !!entries[0].isIntersecting;
      applyClasses();
    }, { rootMargin: '0px 0px -6% 0px', threshold: 0 }).observe(ftr);
  }

  var rafPending = false;
  function requestUpdate() {
    if (rafPending) return;
    rafPending = true;
    requestAnimationFrame(function() {
      rafPending = false;
      applyClasses();
    });
  }

  window.addEventListener('scroll', requestUpdate, { passive: true });
  window.addEventListener('resize', requestUpdate, { passive: true });
  document.addEventListener('click', function() { setTimeout(requestUpdate, 80); setTimeout(requestUpdate, 360); }, { passive: true });

  function init() {
    syncFloatingLabel();
    observeFooter();
    applyClasses();
  }

  if (document.readyState === 'complete') {
    setTimeout(init, 100);
  } else {
    window.addEventListener('load', function() { setTimeout(init, 100); }, { once: true });
  }

  if ('MutationObserver' in window) {
    var attachObs = function() {
      if (!document.body) return;
      new MutationObserver(function() {
        syncFloatingLabel();
        observeFooter();
        var cookieOpen = !!document.querySelector('.roasist-cookie-bar.is-visible');
        var menuOpen = !!document.querySelector('[class*="PrimaryNavigation_active"]');
        document.body.classList.toggle('roasist-cookie-open', cookieOpen);
        document.body.classList.toggle('roasist-menu-open', menuOpen);
      }).observe(document.body, { childList: true, subtree: true, attributes: true, attributeFilter: ['class'] });
    };
    if (document.readyState === 'complete') attachObs();
    else window.addEventListener('load', attachObs, { once: true });
  }
})();
</script>"""


def prepare_inline_css(css_path: str, cache: dict) -> str:
    if css_path in cache:
        return cache[css_path]
    raw = open(css_path, "r", encoding="utf-8").read()
    # Rewrite relative asset paths inside CSS so inlined <style> resolves from any route depth
    raw = raw.replace("url(../../../images/", "url(/images/")
    raw = raw.replace('url("../../../images/', 'url("/images/')
    raw = raw.replace("url('../../../images/", "url('/images/")
    raw = raw.replace("url(../media/", "url(/_next/static/media/")
    raw = raw.replace('url("../media/', 'url("/_next/static/media/')
    raw = raw.replace("url('../media/", "url('/_next/static/media/")
    # Strip block comments & compact line breaks safely (preserving calc() spaces and SVG data URIs)
    raw = re.sub(r"/\*.*?\*/", "", raw, flags=re.S)
    raw = re.sub(r"[ \t]*\n+[ \t]*", "", raw)
    raw = re.sub(r" {2,}", " ", raw)
    raw = raw.replace("</style", "\\3c /style")
    cache[css_path] = raw.strip()
    return cache[css_path]


def step1_patch_js_forced_reflows() -> list:
    chunks_dir = os.path.join(PUBLIC_DIR, "_next", "static", "chunks")
    line_by_line_re = re.compile(
        r'return\(0,([a-zA-Z_$]+)\.V\)\(\(\)=>\{let e=([a-zA-Z_$]+)\.p8\.matchMedia\(\),'
        r't=\2\.C2\.create\("span",\{type:"lines",linesClass:"split-line",autoSplit:!0,mask:"lines"\}\);'
        r'return \2\.ic\.create\(\{trigger:([a-zA-Z_$]+)\.current,start:"top bottom",end:"bottom top",'
        r'onEnter:\(\)=>\{\2\.p8\.fromTo\(t\.lines,\{y:"100%"\},\{y:"-7%",opacity:1,duration:1,ease:"power3\.out",stagger:\{each:\.25,amount:\.45\}\}\)\}\}\),'
        r'\(\)=>\{e\.revert\(\)\}\},\{scope:\3\}\)'
    )

    def _lbl_repl(m):
        v_hook, gs, ref_v = m.group(1), m.group(2), m.group(3)
        return (
            f'return(0,{v_hook}.V)(()=>{{let e={gs}.p8.matchMedia(),t;'
            f'return {gs}.ic.create({{trigger:{ref_v}.current,start:"top bottom",once:!0,'
            f'onEnter:()=>{{let el={ref_v}.current&&{ref_v}.current.querySelector("span");if(!el)return;'
            f't={gs}.C2.create(el,{{type:"lines",linesClass:"split-line",autoSplit:!0,mask:"lines"}});'
            f'{gs}.p8.fromTo(t.lines,{{y:"100%"}},{{y:"-7%",opacity:1,duration:1,ease:"power3.out",stagger:{{each:.25,amount:.45}}}})}}}}),'
            f'()=>{{t&&t.revert(),e.revert()}}}},{{scope:{ref_v}}})'
        )

    flt_st_re = re.compile(
        r'return\(0,[a-zA-Z_$]+\.V\)\(\(\)=>\{let t=window\.innerHeight,[a-zA-Z_$]+=document\.querySelector\("#kotaverceCta"\);'
        r'[a-zA-Z_$]+\.p8\.to\([a-zA-Z_$]+\.current,\{opacity:1,scrollTrigger:\{[^}]+\},ease:"power3\.out",duration:\.3\}\)\}\),',
    )

    modified = []
    for fp in sorted(glob.glob(os.path.join(chunks_dir, "**", "*.js"), recursive=True)):
        orig = open(fp, "r", encoding="utf-8", errors="ignore").read()
        upd = line_by_line_re.sub(_lbl_repl, orig)
        upd = flt_st_re.sub("return ", upd)
        if upd != orig:
            open(fp, "w", encoding="utf-8").write(upd)
            modified.append(fp)

    # Cache-bust 988...59d.js -> 988...59e.js and homepage 42e.js -> 42f.js
    pairs = []
    bumps = [
        ("988-86d1af1c6c90b59d.js", "988-86d1af1c6c90b59e.js"),
        ("app/(home)/page-b58f77e3dc47742e.js", "app/(home)/page-b58f77e3dc47742f.js"),
    ]
    for old_rel, new_rel in bumps:
        src = os.path.join(chunks_dir, old_rel)
        dst = os.path.join(chunks_dir, new_rel)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            pairs.append((os.path.basename(old_rel), os.path.basename(new_rel)))

    print(f"[1/3] Deferred offscreen SplitText & stripped redundant ScrollTrigger across {len(modified)} JS chunks")
    return pairs


def step2_inline_css_strip_gfonts_and_fix_scripts(js_pairs: list):
    css_cache = {}
    gfonts_import_re = re.compile(
        r"@import\s+url\(['\"]https://fonts\.googleapis\.com/[^'\"]+['\"]\)\s*;?\s*",
        re.I,
    )
    css_link_re = re.compile(
        r'<link rel="stylesheet" href="(/_next/static/css/roasist-bundle-[^"]+\.css)" data-precedence="next"/>'
    )
    arrow_re = re.compile(r'<script id="roasist-arrow-rotator">.*?</script>', re.S)
    flt_ctrl_re = re.compile(r'<script id="roasist-floating-cta-ctrl">.*?</script>', re.S)

    old_sched_re = re.compile(
        r"function scheduleEnhancements\(\) \{\s*"
        r"setTimeout\(applyPostHydrationEnhancements, 450\);\s*"
        r"setTimeout\(applyPostHydrationEnhancements, 1200\);\s*"
        r"setTimeout\(mountCookieBanner, 1300\);\s*"
        r"var timer = null;\s*"
        r"new MutationObserver\(function\(\) \{\s*"
        r"if \(timer\) return;\s*"
        r"timer = setTimeout\(function\(\) \{\s*"
        r"timer = null;\s*"
        r"applyPostHydrationEnhancements\(\);\s*"
        r"\}, 250\);\s*"
        r"\}\)\.observe\(document\.documentElement, \{ childList: true, subtree: true \}\);\s*"
        r"\}",
        re.S,
    )
    new_sched = """function scheduleEnhancements() {
    var runIdle = window.requestIdleCallback || function(cb) { return setTimeout(cb, 200); };
    function startAfterHydration() {
      runIdle(function() { applyPostHydrationEnhancements(); });
      setTimeout(mountCookieBanner, 900);
      var timer = null;
      new MutationObserver(function() {
        if (timer) return;
        timer = setTimeout(function() {
          timer = null;
          runIdle(function() { applyPostHydrationEnhancements(); });
        }, 500);
      }).observe(document.documentElement, { childList: true, subtree: true });
    }
    if (document.readyState === 'complete') {
      setTimeout(startAfterHydration, 120);
    } else {
      window.addEventListener('load', function() { setTimeout(startAfterHydration, 120); }, { once: true });
    }
  }"""

    flight_css_arr_re = re.compile(
        r'\[\["\$","link","0",\{"rel":"stylesheet","href":"/_next/static/css/roasist-bundle-[^"]+\.css","precedence":"next","crossOrigin":"\$undefined"\}\]\]'
    )

    # Also strip @import from scripts/inject_homepage_kinetic_3d.py so future runs never re-add Google Fonts
    kin_py = os.path.join(SCRIPT_DIR, "inject_homepage_kinetic_3d.py")
    if os.path.exists(kin_py):
        ks = open(kin_py, "r", encoding="utf-8").read()
        ks2 = gfonts_import_re.sub("", ks)
        if ks2 != ks:
            open(kin_py, "w", encoding="utf-8").write(ks2)

    updated = 0
    inlined_pages = 0
    for fp in sorted(glob.glob(os.path.join(PUBLIC_DIR, "**", "*.html"), recursive=True)):
        rel = os.path.relpath(fp, PUBLIC_DIR).replace(os.sep, "/")
        if rel == "404.html" or rel.endswith("-3d.html") or "api/" in rel:
            continue

        orig = open(fp, "r", encoding="utf-8").read()

        def transform_non_flight(seg: str) -> str:
            nonlocal inlined_pages
            seg = gfonts_import_re.sub("", seg)
            seg = arrow_re.sub(lambda _: ZERO_REFLOW_ARROW_SCRIPT, seg)
            seg = flt_ctrl_re.sub(lambda _: ZERO_REFLOW_FLOATING_CTRL, seg)
            seg = old_sched_re.sub(lambda _: new_sched, seg)
            for old_js, new_js in js_pairs:
                seg = seg.replace(old_js, new_js)

            def _inline_css_match(m):
                href = m.group(1)
                abs_css = os.path.join(PUBLIC_DIR, href.lstrip("/"))
                if not os.path.exists(abs_css):
                    return m.group(0)
                inlined = prepare_inline_css(abs_css, css_cache)
                return f'<style id="roasist-bundle-inline" data-precedence="next">{inlined}</style>'

            if css_link_re.search(seg):
                seg = css_link_re.sub(_inline_css_match, seg, count=1)
                # Remove any duplicate link tags if present
                seg = css_link_re.sub("", seg)
                inlined_pages += 1
            return seg

        matches, _, full = extract_flight_chunks(orig)
        if matches:
            recs = parse_flight_stream(full)
            kept_recs = []
            for rec in recs:
                val = rec[2]
                if val.startswith('HL["/_next/static/css/') and val.endswith('","style"]'):
                    continue
                val = flight_css_arr_re.sub("[]", val)
                for old_js, new_js in js_pairs:
                    val = val.replace(old_js, new_js)
                rec[2] = val
                kept_recs.append(rec)
            new_full = serialize_flight_stream(kept_recs)

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

    # Also update chunk cross-references in JS files
    for fp in sorted(glob.glob(os.path.join(PUBLIC_DIR, "_next", "static", "chunks", "**", "*.js"), recursive=True)):
        orig = open(fp, "r", encoding="utf-8", errors="ignore").read()
        upd = orig
        for old_js, new_js in js_pairs:
            upd = upd.replace(old_js, new_js)
        if upd != orig:
            open(fp, "w", encoding="utf-8").write(upd)

    print(
        f"[2/3] Inlined render-blocking CSS ({len(css_cache)} unique bundles across {inlined_pages} pages), "
        f"removed Google Fonts @import & fixed forced-reflow scripts in {updated} HTML files"
    )


def step3_prune_superseded_bundle_versions():
    # Remove intermediate superseded bundle copies (*m2, *m3) to keep package lean
    removed = 0
    for pat in ("roasist-bundle-*m2.css", "roasist-bundle-*m3.css"):
        for fp in glob.glob(os.path.join(PUBLIC_DIR, "_next", "static", "css", pat)):
            os.remove(fp)
            removed += 1
    print(f"[3/3] Cleaned {removed} superseded intermediate CSS bundle files")


def main():
    js_pairs = step1_patch_js_forced_reflows()
    step2_inline_css_strip_gfonts_and_fix_scripts(js_pairs)
    step3_prune_superseded_bundle_versions()


if __name__ == "__main__":
    main()
