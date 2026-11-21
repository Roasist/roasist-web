#!/usr/bin/env python3
"""
PageSpeed Insights Round 3 Optimization for https://www.roasist.com/:

1. Eliminates Main-Thread & CPU Thrashing (`41.6s` Main Thread / `39.0s` Other / `40.4s` JS CPU):
   - `2553` (`11856` `@studio-freight/tempus` — `29,409 ms`): stops the unconditional 60fps
     `requestAnimationFrame` loop when `this.callbacks.length === 0`, starting RAF only when
     active callbacks exist (`0` idle frames during page load).
   - `4143` (`44143` `WebGLBackground` + `c15bf2b0` `EffectComposer` — `39,052 ms` SwiftShader `Other`):
     * Sets `renderer.setPixelRatio(1)` (75% fewer fragment shader pixels on Retina/mobile).
     * Removes redundant `this.renderer.render(this.scene, this.camera)` before `this.composer.render()`
       (cuts WebGL passes in half).
     * Pre-binds `_boundRender` once instead of allocating `this.render.bind(this)` every frame.
     * Detects mobile (`< 850px`), `prefers-reduced-motion`, or software WebGL (`SwiftShader`,
       `llvmpipe`, `Software`, `Basic Render`) and renders 1 crisp static frame at full target
       uniforms (`uPow=1.5, uAlpha=1, rayMouse=-0.4`) instead of running a 60fps shader loop +
       2.5s GSAP tweens on CPU software rasterizers; throttles desktop hardware GPU loop to 30fps.
   - Homepage `#carousel` 5-canvas `kinetic-3d` script (`kota-roasist-local.html`, `en/index.html`,
     `scripts/inject_homepage_kinetic_3d.py`):
     * Defaults `isCarouselVisible = false` instead of `true` and runs `requestAnimationFrame(tick)`
       ONLY while `#carousel` is intersecting the viewport (`0` idle frames when offscreen).
     * Renders only the active/visible slide instead of drawing all 5 2D canvases every frame.

2. Eliminates Remaining Inline Forced Reflows (`https://www.roasist.com:320:28` `50 ms` & `:5238` `1 ms`):
   - Header Logo Ink WebGL script (`roasist-ink` across all 64 HTML files):
     * Reads `header.getBoundingClientRect()` & `svg.getBoundingClientRect()` BEFORE `appendChild(canvas)`.
     * Defers `initEngine()` (`buildTexture` 5-canvas blur + WebGL shader compile) until first `scroll`
       event when `window.scrollY <= 5` (since `.roasist-ink-canvas` is `visibility: hidden` at `scrollY=0`),
       eliminating both the `50 ms` forced reflow and `~290 ms` initial main-thread script evaluation.
   - Homepage `#carousel` `ensureCanvasesMounted()`:
     * Batch-reads all 5 `getBoundingClientRect()` calls BEFORE any `appendChild` DOM writes (`0 ms` reflow).
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


def step1_patch_2553_and_4143() -> tuple[list, list]:
    chunks_dir = os.path.join(PUBLIC_DIR, "_next", "static", "chunks")

    # 1A. Patch 2553-48f52e8f75360017.js (module 11856 tempus idle 60fps RAF loop)
    p2553 = os.path.join(chunks_dir, "2553-48f52e8f75360017.js")
    t2553 = open(p2553, "r", encoding="utf-8").read()
    old_tempus = (
        '11856:function(e,t,r){"use strict";r.d(t,{Z:function(){return i}});'
        'var i="undefined"!=typeof window&&new class{constructor(){'
        'this.raf=e=>{requestAnimationFrame(this.raf);let t=e-this.now;this.now=e;'
        'for(let r=0;r<this.callbacks.length;r++)this.callbacks[r].callback(e,t)},'
        'this.callbacks=[],this.now=performance.now(),requestAnimationFrame(this.raf)}'
        'add(e,t=0){return this.callbacks.push({callback:e,priority:t}),'
        'this.callbacks.sort((e,t)=>e.priority-t.priority),()=>this.remove(e)}'
        'remove(e){this.callbacks=this.callbacks.filter(({callback:t})=>e!==t)}}}'
    )
    new_tempus = (
        '11856:function(e,t,r){"use strict";r.d(t,{Z:function(){return i}});'
        'var i="undefined"!=typeof window&&new class{constructor(){'
        'this.running=!1,this.raf=e=>{if(!this.callbacks.length){this.running=!1;return}'
        'requestAnimationFrame(this.raf);let t=e-this.now;this.now=e;'
        'for(let r=0;r<this.callbacks.length;r++)this.callbacks[r].callback(e,t)},'
        'this.callbacks=[],this.now=performance.now()}'
        'add(e,t=0){return this.callbacks.push({callback:e,priority:t}),'
        'this.callbacks.sort((e,t)=>e.priority-t.priority),'
        'this.running||(this.running=!0,this.now=performance.now(),requestAnimationFrame(this.raf)),'
        '()=>this.remove(e)}'
        'remove(e){this.callbacks=this.callbacks.filter(({callback:t})=>e!==t)}}}'
    )
    assert old_tempus in t2553, "old_tempus not found in 2553!"
    t2553_upd = t2553.replace(old_tempus, new_tempus, 1)
    open(p2553, "w", encoding="utf-8").write(t2553_upd)
    p2553_new = os.path.join(chunks_dir, "2553-48f52e8f75360018.js")
    shutil.copy2(p2553, p2553_new)
    print("  [2553] Stopped idle 60fps tempus RAF loop -> 2553-48f52e8f75360018.js")

    # 1B. Patch 4143 (WebGLBackground: 1x DPR, single-pass composer, static single-frame on mobile & SwiftShader)
    old_anim_in = (
        'animateIn(t,e){a.p8.to(this.material.uniforms.uPow,{value:1.5,duration:t,delay:e,ease:"power4.out"}),'
        'a.p8.to(this.material.uniforms.uAlpha,{value:1,duration:t,delay:e,ease:"power4.out"}),'
        'this.allowRayMouse=!1,a.p8.to(this.rayMouse,{x:-.4,y:-.4,duration:t,ease:"power1.out",immediateRender:!1,onComplete:()=>{this.allowRayMouse=!0}})}'
    )
    new_anim_in = (
        'animateIn(t,e){if(this.isStatic){this.material.uniforms.uPow.value=1.5,this.material.uniforms.uAlpha.value=1,'
        'this.rayMouse.x=-.4,this.rayMouse.y=-.4,this.uTime=.25,this.renderFrame();return}'
        'a.p8.to(this.material.uniforms.uPow,{value:1.5,duration:t,delay:e,ease:"power4.out"}),'
        'a.p8.to(this.material.uniforms.uAlpha,{value:1,duration:t,delay:e,ease:"power4.out"}),'
        'this.allowRayMouse=!1,a.p8.to(this.rayMouse,{x:-.4,y:-.4,duration:t,ease:"power1.out",immediateRender:!1,onComplete:()=>{this.allowRayMouse=!0}})}'
    )

    old_render = (
        'render(){if(!1===this.isPlaying)return;this.time+=.026,'
    )
    new_render = (
        'render(e){if(!1===this.isPlaying)return;if(this.isStatic){this.renderFrame();return}'
        'if(document.hidden){requestAnimationFrame(this._boundRender);return}'
        'if(e&&this._lt&&e-this._lt<30){requestAnimationFrame(this._boundRender);return}'
        'this._lt=e||0,this.renderFrame(),requestAnimationFrame(this._boundRender)}'
        'renderFrame(){this.time+=.026,'
    )

    old_render_tail = 'this.renderer.render(this.scene,this.camera),this.composer.render(),requestAnimationFrame(this.render.bind(this))}'
    new_render_tail = 'this.composer.render()}'

    old_dpr = 'this.renderer.setPixelRatio(Math.min(window.devicePixelRatio,2))'
    new_dpr = (
        'this.renderer.setPixelRatio(1),'
        'this._boundRender=this.render.bind(this),'
        'this.isStatic=(()=>{try{if(window.innerWidth<850||window.matchMedia&&window.matchMedia("(prefers-reduced-motion: reduce)").matches)return!0;'
        'let e=this.renderer.getContext(),t=e&&e.getExtension("WEBGL_debug_renderer_info"),i=t&&e.getParameter(t.UNMASKED_RENDERER_WEBGL)||"";'
        'return/SwiftShader|Software|llvmpipe|Basic Render/i.test(i)}catch(e){return!0}})()'
    )

    old_boot_tail = 'this.initPostProcessing(),this.addObjects(),this.resize(),this.render(),this.setupResize(),this.followMouse()'
    new_boot_tail = 'this.initPostProcessing(),this.addObjects(),this.resize(),!this.isStatic&&this.render(),this.setupResize(),!this.isStatic&&this.followMouse()'

    old_resize_tail = 'this.plane.material.uniforms.uRatio=this.plane.scale.x/this.plane.scale.y}'
    new_resize_tail = 'this.plane.material.uniforms.uRatio=this.plane.scale.x/this.plane.scale.y,this.isStatic&&this.composer&&this.renderFrame()}'

    for fn in ("4143-6b83e17252ec01c2.js", "4143-6b83e17252ec01c3.js"):
        p4 = os.path.join(chunks_dir, fn)
        if not os.path.exists(p4):
            continue
        t4 = open(p4, "r", encoding="utf-8").read()
        assert old_anim_in in t4 and old_render in t4 and old_render_tail in t4 and old_dpr in t4, f"4143 pattern missing in {fn}"
        t4 = t4.replace(old_anim_in, new_anim_in, 1)
        t4 = t4.replace(old_render, new_render, 1)
        t4 = t4.replace(old_render_tail, new_render_tail, 1)
        t4 = t4.replace(old_dpr, new_dpr, 1)
        t4 = t4.replace(old_boot_tail, new_boot_tail, 1)
        t4 = t4.replace(old_resize_tail, new_resize_tail, 1)
        open(p4, "w", encoding="utf-8").write(t4)

    p4_src = os.path.join(chunks_dir, "4143-6b83e17252ec01c3.js")
    p4_new = os.path.join(chunks_dir, "4143-6b83e17252ec01c4.js")
    shutil.copy2(p4_src, p4_new)
    print("  [4143] Eliminated duplicate WebGL pass & SwiftShader/mobile 60fps loop -> 4143-6b83e17252ec01c4.js")

    js_pairs = [
        ("2553-48f52e8f75360017.js", "2553-48f52e8f75360018.js"),
        ("4143-6b83e17252ec01c3.js", "4143-6b83e17252ec01c4.js"),
    ]
    hash_pairs = [
        ("48f52e8f75360017", "48f52e8f75360018"),
        ("6b83e17252ec01c3", "6b83e17252ec01c4"),
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

    return js_pairs, hash_pairs


NEW_KINETIC_LIFECYCLE = """  // ==========================================================================
  // MOUNT & INTERSECTION OBSERVER LIFECYCLE (Zero-Reflow & Zero-Idle-RAF)
  // ==========================================================================
  let s1Canvas = null, s1Ctx = null, s1W = 562, s1H = 434, s1Dpr = 1;
  let s2Canvas = null, s2Ctx = null, s2W = 562, s2H = 434, s2Dpr = 1;
  let s3Canvas = null, s3Ctx = null, s3W = 562, s3H = 434, s3Dpr = 1;
  let s4Canvas = null, s4Ctx = null, s4W = 562, s4H = 434, s4Dpr = 1;
  let s5Canvas = null, s5Ctx = null, s5W = 562, s5H = 434, s5Dpr = 1;
  let isCarouselVisible = false;
  let rafHandle = 0;
  let lastMountCheck = -1000;
  const startTime = performance.now();

  function stopSlideVideo(container) {
    const vid = container.querySelector('video');
    if (vid && !vid.dataset.roasistDisabled) {
      vid.dataset.roasistDisabled = 'true';
      try {
        vid.pause();
        vid.removeAttribute('src');
        vid.querySelectorAll('source').forEach(s => s.remove());
        vid.load();
      } catch {}
    }
  }

  function ensureCanvasesMounted() {
    // PHASE 1: Batch-read all slide container geometries BEFORE any DOM writes (0 forced reflow!)
    const sel = (n) => document.querySelector(`#carousel .swiper-slide:nth-child(${n}) .CarouselSlides_carouselMedia__aqYWx`);
    const c1 = sel(1), c2 = sel(2), c3 = sel(3), c4 = sel(4), c5 = sel(5);
    const r1 = c1 ? c1.getBoundingClientRect() : null;
    const r2 = c2 ? c2.getBoundingClientRect() : null;
    const r3 = c3 ? c3.getBoundingClientRect() : null;
    const r4 = c4 ? c4.getBoundingClientRect() : null;
    const r5 = c5 ? c5.getBoundingClientRect() : null;
    const d = Math.min(window.devicePixelRatio || 1, 2);

    // PHASE 2: Perform DOM mutations & canvas sizing
    if (c1 && r1) {
      stopSlideVideo(c1);
      let cv1 = c1.querySelector('canvas.roasist-kinetic-3d-canvas');
      if (!cv1) {
        cv1 = document.createElement('canvas');
        cv1.className = 'roasist-kinetic-3d-canvas';
        cv1.setAttribute('aria-hidden', 'true');
        c1.appendChild(cv1);
        s1Canvas = cv1;
        s1Ctx = cv1.getContext('2d', { alpha: false });
      }
      if (r1.width > 40 && r1.height > 40) {
        const tw = Math.floor(r1.width), th = Math.floor(r1.height);
        if (s1W !== tw || s1H !== th || s1Dpr !== d || cv1.width !== tw * d) {
          s1W = tw; s1H = th; s1Dpr = d;
          cv1.width = tw * d; cv1.height = th * d;
        }
      }
    }

    if (c2 && r2) {
      stopSlideVideo(c2);
      let cv2 = c2.querySelector('canvas.roasist-creative-bento-canvas');
      if (!cv2) {
        cv2 = document.createElement('canvas');
        cv2.className = 'roasist-creative-bento-canvas';
        cv2.setAttribute('aria-hidden', 'true');
        c2.appendChild(cv2);
        s2Canvas = cv2;
        s2Ctx = cv2.getContext('2d', { alpha: false });
      }
      if (r2.width > 40 && r2.height > 40) {
        const tw = Math.floor(r2.width), th = Math.floor(r2.height);
        if (s2W !== tw || s2H !== th || s2Dpr !== d || cv2.width !== tw * d) {
          s2W = tw; s2H = th; s2Dpr = d;
          cv2.width = tw * d; cv2.height = th * d;
        }
      }
    }

    if (c3 && r3) {
      stopSlideVideo(c3);
      let cv3 = c3.querySelector('canvas.roasist-process-cockpit-canvas');
      if (!cv3) {
        cv3 = document.createElement('canvas');
        cv3.className = 'roasist-process-cockpit-canvas';
        cv3.setAttribute('aria-hidden', 'true');
        c3.appendChild(cv3);
        s3Canvas = cv3;
        s3Ctx = cv3.getContext('2d', { alpha: false });
      }
      if (r3.width > 40 && r3.height > 40) {
        const tw = Math.floor(r3.width), th = Math.floor(r3.height);
        if (s3W !== tw || s3H !== th || s3Dpr !== d || cv3.width !== tw * d) {
          s3W = tw; s3H = th; s3Dpr = d;
          cv3.width = tw * d; cv3.height = th * d;
        }
      }
    }

    if (c4 && r4) {
      stopSlideVideo(c4);
      let cv4 = c4.querySelector('canvas.roasist-convert-broll-canvas');
      if (!cv4) {
        cv4 = document.createElement('canvas');
        cv4.className = 'roasist-convert-broll-canvas';
        cv4.setAttribute('aria-hidden', 'true');
        c4.appendChild(cv4);
        s4Canvas = cv4;
        s4Ctx = cv4.getContext('2d', { alpha: false });
      }
      if (r4.width > 40 && r4.height > 40) {
        const tw = Math.floor(r4.width), th = Math.floor(r4.height);
        if (s4W !== tw || s4H !== th || s4Dpr !== d || cv4.width !== tw * d) {
          s4W = tw; s4H = th; s4Dpr = d;
          cv4.width = tw * d; cv4.height = th * d;
        }
      }
    }

    if (c5 && r5) {
      stopSlideVideo(c5);
      let cv5 = c5.querySelector('canvas.roasist-scale-globe-canvas');
      if (!cv5) {
        cv5 = document.createElement('canvas');
        cv5.className = 'roasist-scale-globe-canvas';
        cv5.setAttribute('aria-hidden', 'true');
        c5.appendChild(cv5);
        s5Canvas = cv5;
        s5Ctx = cv5.getContext('2d', { alpha: false });
      }
      if (r5.width > 40 && r5.height > 40) {
        const tw = Math.floor(r5.width), th = Math.floor(r5.height);
        if (s5W !== tw || s5H !== th || s5Dpr !== d || cv5.width !== tw * d) {
          s5W = tw; s5H = th; s5Dpr = d;
          cv5.width = tw * d; cv5.height = th * d;
        }
      }
    }
  }

  function isSlideActiveOrNear(cv, fallbackFirst) {
    if (!cv) return false;
    const slide = cv.closest('.swiper-slide');
    if (!slide) return fallbackFirst;
    const sw = slide.parentElement && slide.parentElement.parentElement;
    if (!sw || !sw.classList.contains('swiper-initialized')) return fallbackFirst;
    return (
      slide.classList.contains('swiper-slide-active') ||
      slide.classList.contains('swiper-slide-next') ||
      slide.classList.contains('swiper-slide-prev')
    );
  }

  function tick(now) {
    if (!isCarouselVisible) {
      rafHandle = 0;
      return;
    }
    rafHandle = requestAnimationFrame(tick);
    if (document.hidden) return;

    if (now - lastMountCheck > 800) {
      lastMountCheck = now;
      try { ensureCanvasesMounted(); } catch {}
    }

    const elapsedSeconds = (now - startTime) * 0.001;

    // Render Slide 1 ("Önce veri ve strateji")
    if (s1Ctx && isSlideActiveOrNear(s1Canvas, true)) {
      const cameraProgress = (elapsedSeconds / LOOP_DURATION_S1) % 1.0;
      s1Ctx.save();
      s1Ctx.scale(s1Dpr, s1Dpr);
      s1Ctx.fillStyle = COLOR_BG;
      s1Ctx.fillRect(0, 0, s1W, s1H);

      const centerX = s1W * 0.5;
      const centerY = s1H * 0.5;
      const viewportScale = Math.min(s1W / 1020, s1H / 788);
      const refBaseFont = 34 * viewportScale;

      for (let i = 0; i < TOTAL_NODES; i++) {
        const node = s1Nodes[i];
        let z = (node.zBase - cameraProgress) % 1.0;
        if (z < 0) z += 1.0;
        s1RenderList[i] = { node, z };
      }

      s1RenderList.sort((a, b) => b.z - a.z);
      s1Ctx.textAlign = 'center';
      s1Ctx.textBaseline = 'middle';

      for (let i = 0; i < TOTAL_NODES; i++) {
        const { node, z } = s1RenderList[i];
        const alpha = computeOpacity(z);
        if (alpha <= 0.005) continue;

        const scale = getScaleAtZ(z, node.sizeMultiplier);
        const parallax = getParallaxAtZ(z);

        const screenX = centerX + node.x * parallax * viewportScale;
        const screenY = centerY + node.y * parallax * viewportScale;
        const fontSize = refBaseFont * scale;

        s1Ctx.save();
        s1Ctx.font = `800 ${fontSize.toFixed(2)}px 'Inter', -apple-system, BlinkMacSystemFont, sans-serif`;
        if ('letterSpacing' in s1Ctx) {
          s1Ctx.letterSpacing = `${(-0.03 * fontSize).toFixed(2)}px`;
        }

        s1Ctx.globalAlpha = alpha;
        s1Ctx.fillStyle = node.color;

        if (node.isHighlight) {
          s1Ctx.shadowColor = 'rgba(167, 139, 250, 0.72)';
          s1Ctx.shadowBlur = Math.min(26, Math.max(4, 15 * scale * viewportScale));
        } else {
          s1Ctx.shadowBlur = 0;
        }

        s1Ctx.fillText(node.text, screenX, screenY);
        s1Ctx.restore();
      }
      s1Ctx.restore();
    }

    // Render Slide 2 ("Yaratıcı ve cesur fikir")
    if (s2Ctx && isSlideActiveOrNear(s2Canvas, false)) {
      try { renderSlide2Bento(s2Ctx, s2W, s2H, s2Dpr, elapsedSeconds); } catch {}
    }

    // Render Slide 3 ("Kusursuz süreç yönetimi")
    if (s3Ctx && isSlideActiveOrNear(s3Canvas, false)) {
      try { renderSlide3ProcessCockpit(s3Ctx, s3W, s3H, s3Dpr, elapsedSeconds); } catch {}
    }

    // Render Slide 4 ("Dönüşüm için tasarla")
    if (s4Ctx && isSlideActiveOrNear(s4Canvas, false)) {
      try { renderSlide4ConvertBroll(s4Ctx, s4W, s4H, s4Dpr, elapsedSeconds); } catch {}
    }

    // Render Slide 5 ("Ölçeklenebilir büyüme")
    if (s5Ctx && isSlideActiveOrNear(s5Canvas, false)) {
      try { renderSlide5ScaleGlobe(s5Ctx, s5W, s5H, s5Dpr, elapsedSeconds); } catch {}
    }
  }

  function bindCarouselObserver() {
    const carouselEl = document.getElementById('carousel');
    if (!carouselEl) return;
    if (!('IntersectionObserver' in window)) {
      isCarouselVisible = true;
      ensureCanvasesMounted();
      if (!rafHandle) rafHandle = requestAnimationFrame(tick);
      return;
    }
    const io = new IntersectionObserver((entries) => {
      const vis = !!entries[0].isIntersecting;
      isCarouselVisible = vis;
      if (vis) {
        try { ensureCanvasesMounted(); } catch {}
        if (!rafHandle) rafHandle = requestAnimationFrame(tick);
      } else if (rafHandle) {
        cancelAnimationFrame(rafHandle);
        rafHandle = 0;
      }
    }, { rootMargin: '250px 0px', threshold: 0.01 });
    io.observe(carouselEl);
  }

  if (document.readyState === 'complete') {
    bindCarouselObserver();
  } else {
    window.addEventListener('load', bindCarouselObserver, { once: true });
  }
})();
"""


def step2_patch_html_and_generator_scripts(js_pairs: list):
    old_sync_layout = """      function syncLayout(refs) {
        if (!refs.header || !refs.svg) return false;
        if (!mounted || canvas.parentNode !== refs.header) {
          refs.header.appendChild(canvas);
          mounted = true;
        }
        var hRect = refs.header.getBoundingClientRect();
        var sRect = refs.svg.getBoundingClientRect();
        if (sRect.width < 10) return false;"""

    new_sync_layout = """      function syncLayout(refs) {
        if (!refs.header || !refs.svg) return false;
        var hRect = refs.header.getBoundingClientRect();
        var sRect = refs.svg.getBoundingClientRect();
        if (sRect.width < 10) return false;
        if (!mounted || canvas.parentNode !== refs.header) {
          refs.header.appendChild(canvas);
          mounted = true;
        }"""

    old_ink_boot = """      if (document.readyState === "complete") {
        setTimeout(safeBoot, 320);
      } else {
        window.addEventListener("load", function () {
          setTimeout(safeBoot, 320);
        });
      }

      window.addEventListener("scroll", updateTarget, { passive: true });
      window.addEventListener(
        "resize",
        function () {
          var refs = getRefs();
          syncLayout(refs);
          if (progress > 0.002 && progress < 0.998) drawFrame(progress, refs);
        },
        { passive: true }
      );
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initEngine);
  } else {
    initEngine();
  }"""

    new_ink_boot = """      safeBoot();
      updateTarget();

      window.addEventListener("scroll", updateTarget, { passive: true });
      window.addEventListener(
        "resize",
        function () {
          var refs = getRefs();
          syncLayout(refs);
          if (progress > 0.002 && progress < 0.998) drawFrame(progress, refs);
        },
        { passive: true }
      );
    });
  }

  var _inkBooted = false;
  function bootInkOnScroll() {
    if (_inkBooted) return;
    _inkBooted = true;
    initEngine();
  }
  if ((window.scrollY || window.pageYOffset || 0) > 5) {
    bootInkOnScroll();
  } else {
    window.addEventListener("scroll", bootInkOnScroll, { once: true, passive: true });
  }"""

    kinetic_re = re.compile(
        r"  // ==========================================================================\n"
        r"  // MOUNT & INTERSECTION OBSERVER LIFECYCLE.*?\}\)\(\);\n(?=</script>)",
        re.S,
    )

    updated = 0
    kinetic_updated = 0
    for fp in sorted(glob.glob(os.path.join(PUBLIC_DIR, "**", "*.html"), recursive=True)):
        rel = os.path.relpath(fp, PUBLIC_DIR).replace(os.sep, "/")
        if rel == "404.html" or rel.endswith("-3d.html") or "api/" in rel:
            continue

        orig = open(fp, "r", encoding="utf-8").read()

        def transform_non_flight(seg: str) -> str:
            nonlocal kinetic_updated
            for old_js, new_js in js_pairs:
                seg = seg.replace(old_js, new_js)
            seg = seg.replace(old_sync_layout, new_sync_layout)
            seg = seg.replace(old_ink_boot, new_ink_boot)
            if kinetic_re.search(seg):
                seg = kinetic_re.sub(lambda _: NEW_KINETIC_LIFECYCLE, seg, count=1)
                kinetic_updated += 1
            return seg

        matches, _, full = extract_flight_chunks(orig)
        if matches:
            recs = parse_flight_stream(full)
            for rec in recs:
                val = rec[2]
                for old_js, new_js in js_pairs:
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

    # Also update scripts/inject_homepage_kinetic_3d.py so source script stays in sync
    kin_script = os.path.join(SCRIPT_DIR, "inject_homepage_kinetic_3d.py")
    if os.path.exists(kin_script):
        ks = open(kin_script, "r", encoding="utf-8").read()
        ks2 = re.sub(
            r"  // ==========================================================================\n"
            r"  // MOUNT & INTERSECTION OBSERVER LIFECYCLE.*?\}\)\(\);\n",
            lambda _: NEW_KINETIC_LIFECYCLE,
            ks,
            count=1,
            flags=re.S,
        )
        if ks2 != ks:
            open(kin_script, "w", encoding="utf-8").write(ks2)

    print(
        f"[2/2] Updated {updated} HTML files (zero-reflow roasist-ink lazy scroll boot + "
        f"{kinetic_updated} kinetic-3d IntersectionObserver lifecycles + cache-busted JS refs)"
    )


def main():
    print("[1/2] Stopping idle 60fps RAF loops in 2553 (tempus) and 4143 (WebGLBackground)...")
    js_pairs, _ = step1_patch_2553_and_4143()
    step2_patch_html_and_generator_scripts(js_pairs)


if __name__ == "__main__":
    main()
