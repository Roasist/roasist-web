#!/usr/bin/env python3
"""
Fixes mobile video playback across iOS Safari, Android Chrome, and tablets:
  1. `app/(home)/page-b58f77e3dc47742c.js`:
     - Removes KOTA's `window.innerWidth < 769` video-disabler in `ServicesPanel` (`17891`, `360° HİZMETLER`)
       that replaced `<AutoplayVideo>` with broken/static `<Image>` on mobile.
     - Passes `poster={service.image.sourceUrl}` into `<AutoplayVideo>` for instant zero-blank framing.
     - Fixes client-hydrated `"service/<slug>"` hrefs to `"/hizmetler/<slug>/"` (TR) and `"/en/<slug>/"` (EN),
       eliminating 7 RSC prefetch 404s.
     - Removes `window.innerWidth < 769` static-image swap in `CarouselSlides` (`84024`, Methodology 3D section).
  2. `988-86d1af1c6c90b59b.js`:
     - Upgrades `AutoplayVideo` (`30013`) to bind `src` & `poster` directly on `<video>` (ignoring non-video
       placeholder URLs like `.svg`/`.jpg`), with WebKit-required `muted`, `defaultMuted`, `playsinline`,
       `webkit-playsinline`, `.load()`, and `.play()` inside `useEffect` + `320px` `IntersectionObserver` rootMargin.
  3. Stylesheets (`84191844b30595bc.css`, `33a276ed7bd6abf4.css`, and all `roasist-bundle-*.css`):
     - Enables `.ProjectCard_video__AheFz { display: block !important; }` across mobile/tablet (`< 1024px`).
     - Enforces `.ServiceMedia_mediaContainer__WGgZa` & `.ProjectCard_projectImage__Nfx9I` positioning/clipping.
     - Fixes `.Hero_video__rzcbe > span` (`0x0` collapsed circular hero video on `/referanslar/` & `/en/references/`
       below `769px`) and `.CarouselSlides_carouselMedia__aqYWx` aspect-ratio on mobile.
  4. HTML pages:
     - Upgrades `<script id="roasist-lazy-video">` with iOS Safari attributes, `.Hero_video__rzcbe video` support,
       and passive `touchstart` unlock fallback.
     - Adds matching `poster` attributes on SSR `ServicesPanel` `<video>` tags and rewrites SSR `href="service/..."`
       links on `/` and `/en/`.
  5. Cache-busts modified immutable (`max-age=31536000`) JS/CSS assets using identical-byte-length filenames.
"""
import glob
import os
import re
import shutil

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
PUBLIC_DIR = os.path.join(REPO_ROOT, "public")

LAZY_VIDEO_SCRIPT_ID = "roasist-lazy-video"
IOS_LAZY_VIDEO_SCRIPT = f"""<script id="{LAZY_VIDEO_SCRIPT_ID}">
(function() {{
  function ensureInlineAttrs(v) {{
    if (!v) return;
    v.muted = true;
    v.defaultMuted = true;
    v.playsInline = true;
    v.loop = true;
    v.setAttribute('muted', '');
    v.setAttribute('playsinline', '');
    v.setAttribute('webkit-playsinline', '');
  }}

  function primeAndPlay(v) {{
    if (!v) return;
    ensureInlineAttrs(v);
    var ds = v.getAttribute('data-src');
    if (ds && !v.getAttribute('src')) {{
      v.setAttribute('src', ds);
      try {{ v.load(); }} catch (e) {{}}
    }}
    if (v.getAttribute('src')) {{
      var p = v.play();
      if (p && typeof p.catch === 'function') p.catch(function() {{}});
    }}
  }}

  function initHeroVideos() {{
    document.querySelectorAll('video[class*="Hero_video__"]').forEach(function(v) {{
      if (window.getComputedStyle && window.getComputedStyle(v).display === 'none') return;
      primeAndPlay(v);
    }});
  }}

  var SELECTOR = 'video.ProjectCard_video__AheFz[data-src], .ServiceMedia_mediaContainer__WGgZa video[data-src]';

  if (!('IntersectionObserver' in window)) {{
    initHeroVideos();
    document.querySelectorAll(SELECTOR).forEach(primeAndPlay);
    return;
  }}

  var visibleSet = new Set();
  var io = new IntersectionObserver(function(entries) {{
    entries.forEach(function(entry) {{
      var v = entry.target;
      if (entry.isIntersecting) {{
        visibleSet.add(v);
        primeAndPlay(v);
      }} else {{
        visibleSet.delete(v);
        if (v.getAttribute('src') && !v.paused) {{
          try {{ v.pause(); }} catch (e) {{}}
        }}
      }}
    }});
  }}, {{ rootMargin: '320px 0px', threshold: 0.01 }});

  function observeVideos(root) {{
    initHeroVideos();
    (root || document).querySelectorAll(SELECTOR).forEach(function(v) {{
      if (!v.dataset.roasistObserved) {{
        v.dataset.roasistObserved = '1';
        io.observe(v);
      }}
    }});
  }}

  // iOS Safari touch unlock fallback (e.g. Low Power Mode or strict gesture gate)
  function resumeVisible() {{
    visibleSet.forEach(function(v) {{
      if (v.paused) primeAndPlay(v);
    }});
    document.querySelectorAll('.ServiceMedia_mediaContainer__WGgZa video, .AutoplayVideo_video__zckWy video, video[class*="Hero_video__"]').forEach(function(v) {{
      if (window.getComputedStyle && window.getComputedStyle(v).display === 'none') return;
      if ((v.getAttribute('src') || v.getAttribute('data-src')) && v.paused) {{
        primeAndPlay(v);
      }}
    }});
  }}
  window.addEventListener('touchstart', resumeVisible, {{ passive: true, once: false }});

  if (document.readyState === 'loading') {{
    document.addEventListener('DOMContentLoaded', function() {{ observeVideos(document); }});
  }} else {{
    observeVideos(document);
  }}

  if ('MutationObserver' in window && document.body) {{
    var mo = new MutationObserver(function(muts) {{
      for (var i = 0; i < muts.length; i++) {{
        if (muts[i].addedNodes && muts[i].addedNodes.length) {{
          observeVideos(document);
          break;
        }}
      }}
    }});
    mo.observe(document.body, {{ childList: true, subtree: true }});
  }}
}})();
</script>"""

MOBILE_VIDEO_CSS = """
/* === MOBILE VIDEO PLAYBACK & CONTAINER FIX v2 (iOS Safari & Android) === */
.ServiceMedia_mediaContainer__WGgZa {
  position: relative !important;
  overflow: hidden !important;
}
.ServiceMedia_mediaContainer__WGgZa .AutoplayVideo_video__zckWy,
.ServiceMedia_mediaContainer__WGgZa video {
  position: absolute !important;
  top: 0 !important;
  left: 0 !important;
  width: 100% !important;
  height: 100% !important;
  object-fit: cover !important;
  display: block !important;
}
.ProjectCard_projectImage__Nfx9I {
  position: relative !important;
  overflow: hidden !important;
}
.ProjectCard_video__AheFz {
  display: block !important;
  z-index: 2 !important;
}
@media (max-width: 849px) {
  .ProjectCard_projectImage__Nfx9I,
  .ProjectCard_projectImage__Nfx9I img,
  .ProjectCard_video__AheFz {
    border-radius: 0.75rem !important;
  }
}
#carousel .CarouselSlides_carouselMedia__aqYWx {
  width: 100% !important;
  aspect-ratio: 562 / 434 !important;
}
#carousel .CarouselSlides_carouselMedia__aqYWx img,
#carousel .CarouselSlides_carouselMedia__aqYWx .AutoplayVideo_video__zckWy {
  display: none !important;
}
"""


def fix_home_services_panel_js():
    p = os.path.join(PUBLIC_DIR, "_next", "static", "chunks", "app", "(home)", "page-b58f77e3dc47742c.js")
    s = open(p, "r", encoding="utf-8").read()

    # 1. Disable mobile image-swap in CarouselSlides (84024)
    s = s.replace("let e=()=>{y(window.innerWidth<769)}", "let e=()=>{y(!1)}")

    # 2. Disable mobile image-swap in ServiceMedia (17891), pass poster, and fix /service/<slug> -> /hizmetler/<slug>/ or /en/<slug>/
    mod_17891_re = re.compile(
        r'17891:function\(e,t,n\)\{"use strict";n\.d\(t,\{default:function\(\)\{return y\}\}\);'
        r'var r=n\(57437\),i=n\(25523\),s=n\(2265\),a=n\(23610\),o=n\(30013\),l=n\(28406\),c=n\.n\(l\);'
        r'function d\(e\)\{.*?var h=n\(45909\)',
        re.S,
    )
    new_17891_prefix = (
        '17891:function(e,t,n){"use strict";n.d(t,{default:function(){return y}});'
        'var r=n(57437),i=n(25523),s=n(2265),a=n(23610),o=n(30013),l=n(28406),c=n.n(l);'
        'function d(e){var t,n,p;let{service:i}=e;'
        'return(0,r.jsx)("div",{className:c().mediaContainer,children:(null==i?void 0:null===(t=i.video)||void 0===t?void 0:t.mediaItemUrl)'
        '?(0,r.jsx)(o.default,{layout:"fill",src:null==i?void 0:null===(n=i.video)||void 0===n?void 0:n.mediaItemUrl,poster:null==i?void 0:null===(p=i.image)||void 0===p?void 0:p.sourceUrl})'
        ':(0,r.jsx)(a.default,{image:null==i?void 0:i.image})})}'
        'var u=n(47899),_=n(66284),p=n.n(_),v=n(36869);'
        'function m(e){var t,n;let{service:s}=e,'
        'k="undefined"!=typeof document&&("en"===document.documentElement.lang||window.location.pathname.startsWith("/en")),'
        'b=e=>k?"/en/".concat(e,"/"):("yapay-zeka-seo"===e?"/hizmetler/aeo-geo/":"/hizmetler/".concat(e,"/"));'
        'return(0,r.jsxs)("div",{className:(0,v.cn)(p().panel,"servicePanel"),children:['
        '(0,r.jsxs)("div",{className:p().panelText,children:['
        '(0,r.jsx)("h3",{className:p().panelHeading,children:null==s?void 0:s.heading}),'
        '(0,r.jsx)("div",{className:p().tags,children:(null==s?void 0:s.tags)&&(null==s?void 0:s.tags.map(e=>(0,r.jsx)("a",{href:b(null==e?void 0:e.slug),className:p().tag,children:null==e?void 0:e.title},null==e?void 0:e.id)))}),'
        '(0,r.jsx)("p",{className:p().panelMainText,children:null==s?void 0:s.mainText}),'
        '(null==s?void 0:null===(t=s.link)||void 0===t?void 0:t.slug)&&(0,r.jsx)(i.default,{text:k?"Explore Service":"Detaylı İncele",type:"a",href:b(null==s?void 0:null===(n=s.link)||void 0===n?void 0:n.slug)})'
        ']}),'
        '(0,r.jsx)(d,{service:s}),'
        '(0,r.jsx)("div",{className:p().panelBackground})'
        ']},null==s?void 0:s.heading)}var h=n(45909)'
    )
    if not mod_17891_re.search(s):
        raise RuntimeError("Could not match module 17891 in page-b58f77e3dc47742c.js")
    s = mod_17891_re.sub(lambda _: new_17891_prefix, s, count=1)
    open(p, "w", encoding="utf-8").write(s)
    print("[OK] Upgraded ServicesPanel (17891) & CarouselSlides (84024) in page-b58f77e3dc47742c.js")


def fix_autoplay_video_chunk():
    p = os.path.join(PUBLIC_DIR, "_next", "static", "chunks", "988-86d1af1c6c90b59b.js")
    s = open(p, "r", encoding="utf-8").read()

    old_fn_re = re.compile(
        r'30013:function\(e,t,n\)\{"use strict";n\.r\(t\),n\.d\(t,\{default:function\(\)\{return a\}\}\);'
        r'var r=n\(57437\),i=n\(2265\),o=n\(36869\),s=n\(95394\),u=n\.n\(s\);'
        r'function a\(e\)\{.*?\}\},25523:function',
        re.S,
    )

    new_fn = (
        '30013:function(e,t,n){"use strict";n.r(t),n.d(t,{default:function(){return a}});'
        'var r=n(57437),i=n(2265),o=n(36869),s=n(95394),u=n.n(s);'
        'function a(e){let{src:t,poster:p,layout:n="fill",onLoadedMetadata:s}=e,a=(0,i.useRef)(null),[c,l]=(0,i.useState)(!1),d=u()[n],m=!!t&&/\\.(mp4|webm|mov)(\\?|$)/i.test(t);'
        'return(0,i.useEffect)(()=>{let v=a.current;if(!v||!m)return;'
        'let e=new IntersectionObserver(e=>{if(e[0].isIntersecting){c||l(!0);v.muted=!0;v.defaultMuted=!0;let q=v.play();q&&q.catch&&q.catch(()=>{})}else{v.pause()}},{root:null,rootMargin:"320px 0px",threshold:.01});'
        'return e.observe(v),()=>e.unobserve(v)},[c,m]),'
        '(0,i.useEffect)(()=>{let v=a.current;if(c&&m&&v){v.muted=!0;v.defaultMuted=!0;v.playsInline=!0;v.setAttribute("muted","");v.setAttribute("playsinline","");v.setAttribute("webkit-playsinline","");try{v.load()}catch(e){}let q=v.play();q&&q.catch&&q.catch(()=>{})}},[c,t,m]),'
        '(0,r.jsx)("span",{className:(0,o.cn)(u().video,d),children:(0,r.jsx)("video",{ref:a,"data-src":m?t:void 0,src:c&&m?t:void 0,poster:p||void 0,autoPlay:c&&m?!0:void 0,loop:!0,muted:!0,playsInline:!0,preload:c&&m?"auto":"none",controls:!1,onLoadedMetadata:s})})}},25523:function'
    )

    if not old_fn_re.search(s):
        raise RuntimeError("Could not match module 30013 in 988-86d1af1c6c90b59b.js")
    s2 = old_fn_re.sub(lambda _: new_fn, s, count=1)
    open(p, "w", encoding="utf-8").write(s2)
    print("[OK] Upgraded AutoplayVideo (module 30013) with poster & iOS Safari lifecycle in 988-86d1af1c6c90b59b.js")


def fix_css_files_and_bundles():
    css_dir = os.path.join(PUBLIC_DIR, "_next", "static", "css")
    targets = [
        os.path.join(css_dir, "84191844b30595bc.css"),
        os.path.join(css_dir, "33a276ed7bd6abf4.css"),
    ] + sorted(glob.glob(os.path.join(css_dir, "roasist-bundle-*.css")))

    old_block_re = re.compile(
        r"\n/\* === MOBILE VIDEO PLAYBACK & CONTAINER FIX(?: v2)? \(iOS Safari & Android\) === \*/.*\Z",
        re.S,
    )

    changed = 0
    for fp in targets:
        if not os.path.exists(fp):
            continue
        orig = open(fp, "r", encoding="utf-8").read()
        upd = orig.replace(
            ".ProjectCard_video__AheFz{position:absolute;width:100%;height:100%;top:0;left:0;object-fit:cover;border-radius:1.125rem;display:none}",
            ".ProjectCard_video__AheFz{position:absolute;width:100%;height:100%;top:0;left:0;object-fit:cover;border-radius:1.125rem;display:block}",
        )
        upd = old_block_re.sub("", upd) + "\n" + MOBILE_VIDEO_CSS
        if upd != orig:
            open(fp, "w", encoding="utf-8").write(upd)
            changed += 1
    print(f"[OK] Updated mobile video CSS rules across {changed} stylesheet files/bundles")


def fix_homepage_ssr_posters_and_links():
    panel_media = [
        ("/images/services/performans-pazarlamasi.mp4", "/images/services/performans-pazarlamasi.jpg"),
        ("/images/services/web-tasarim.mp4", "/images/services/web-tasarim.jpg"),
        ("/images/services/seo-aeo-buyume.mp4", "/images/services/seo-aeo-buyume.jpg"),
    ]
    ssr_vid_re = re.compile(
        r'(<div class="ServiceMedia_mediaContainer__WGgZa"><span class="AutoplayVideo_video__zckWy AutoplayVideo_fill__ZPgCR">)'
        r'<video\b[^>]*></video>'
    )

    for rel, is_en in (("kota-roasist-local.html", False), ("en/index.html", True)):
        fp = os.path.join(PUBLIC_DIR, rel)
        if not os.path.exists(fp):
            continue
        orig = open(fp, "r", encoding="utf-8").read()
        flight_idx = orig.find("self.__next_f.push")
        head_ssr = orig[:flight_idx] if flight_idx != -1 else orig
        tail_flight = orig[flight_idx:] if flight_idx != -1 else ""

        idx_counter = [0]

        def _vid_repl(m):
            i = idx_counter[0]
            idx_counter[0] += 1
            v_url, p_url = panel_media[i] if i < len(panel_media) else panel_media[0]
            return f'{m.group(1)}<video data-src="{v_url}" poster="{p_url}" loop="" muted="" playsInline="" preload="none"></video>'

        head_ssr = ssr_vid_re.sub(_vid_repl, head_ssr)

        # Fix SSR href="service/<slug>" in non-Flight markup
        def _href_repl(m):
            slug = m.group(1)
            if is_en:
                return f'href="/en/{slug}/"'
            if slug == "yapay-zeka-seo":
                return 'href="/hizmetler/aeo-geo/"'
            return f'href="/hizmetler/{slug}/"'

        head_ssr = re.sub(r'href="service/([^"]+)"', _href_repl, head_ssr)
        if is_en:
            head_ssr = head_ssr.replace(">Detaylı İncele<", ">Explore Service<")

        upd = head_ssr + tail_flight
        if upd != orig:
            open(fp, "w", encoding="utf-8").write(upd)
            print(f"[OK] Updated SSR posters & service links in {rel} (panels={idx_counter[0]})")


def fix_html_lazy_video_scripts():
    script_re = re.compile(rf'<script id="{LAZY_VIDEO_SCRIPT_ID}">.*?</script>', re.S)
    updated = 0
    for fp in sorted(glob.glob(os.path.join(PUBLIC_DIR, "**", "*.html"), recursive=True)):
        rel = os.path.relpath(fp, PUBLIC_DIR)
        if rel == "404.html" or rel.endswith("-3d.html"):
            continue
        orig = open(fp, "r", encoding="utf-8").read()
        upd = orig
        if script_re.search(upd):
            upd = script_re.sub(lambda _: IOS_LAZY_VIDEO_SCRIPT, upd, count=1)
        elif 'Hero_video__' in upd or 'ServiceMedia_mediaContainer__WGgZa' in upd:
            body_end = upd.rfind("</body>")
            if body_end != -1:
                upd = upd[:body_end] + IOS_LAZY_VIDEO_SCRIPT + upd[body_end:]
        if upd != orig:
            open(fp, "w", encoding="utf-8").write(upd)
            updated += 1
    print(f"[OK] Upgraded iOS-safe lazy video observer in {updated} HTML pages")


def cache_bust_modified_assets():
    """
    Syncs modified JS chunks & CSS bundles to their same-byte-length cache-busted
    filenames so mobile browsers with 1-year max-age cache fetch fresh code immediately.
    """
    pairs = []
    chunks_dir = os.path.join(PUBLIC_DIR, "_next", "static", "chunks")
    js_targets = [
        ("988-86d1af1c6c90b59b.js", "988-86d1af1c6c90b59c.js"),
        ("app/(home)/page-b58f77e3dc47742c.js", "app/(home)/page-b58f77e3dc47742d.js"),
        ("2827-f8fce45e8c1f0443.js", "2827-f8fce45e8c1f0444.js"),
    ]
    for old_rel, new_rel in js_targets:
        src = os.path.join(chunks_dir, old_rel)
        dst = os.path.join(chunks_dir, new_rel)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            old_base = os.path.basename(old_rel)
            new_base = os.path.basename(new_rel)
            assert len(old_base) == len(new_base)
            pairs.append((old_base, new_base))

    css_dir = os.path.join(PUBLIC_DIR, "_next", "static", "css")
    for fp in sorted(glob.glob(os.path.join(css_dir, "roasist-bundle-*.css"))):
        base = os.path.basename(fp)
        if base.endswith("m2.css"):
            continue
        stem = base[:-4]
        new_base = stem[:-2] + "m2.css"
        assert len(base) == len(new_base)
        shutil.copy2(fp, os.path.join(css_dir, new_base))
        pairs.append((base, new_base))

    touched = 0
    for ext in ("*.html", "*.js"):
        for fp in sorted(glob.glob(os.path.join(PUBLIC_DIR, "**", ext), recursive=True)):
            orig = open(fp, "r", encoding="utf-8", errors="ignore").read()
            upd = orig
            for old_s, new_s in pairs:
                upd = upd.replace(old_s, new_s)
            if upd != orig:
                open(fp, "w", encoding="utf-8").write(upd)
                touched += 1
    print(f"[OK] Synced {len(pairs)} cache-busted JS/CSS assets (updated references in {touched} files)")


def main():
    fix_home_services_panel_js()
    fix_autoplay_video_chunk()
    fix_css_files_and_bundles()
    fix_homepage_ssr_posters_and_links()
    fix_html_lazy_video_scripts()
    cache_bust_modified_assets()


if __name__ == "__main__":
    main()
