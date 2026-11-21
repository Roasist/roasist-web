#!/usr/bin/env python3
"""
Eliminates mobile startup delay on 'Seçilmiş Projeler' (ProjectCard) & ServicesPanel videos:
  1. Re-encodes `public/images/projects/*.mp4` with Low-Latency H.264 (`-bf 0` zero B-frames
     to eliminate hardware decoder frame-reordering delay on iOS Safari, `-g 45` 1.5s GOPs,
     `854x480` 16:9, `-maxrate 550k -bufsize 950k`, `+faststart`, `-an`).
  2. Upgrades `<script id="roasist-lazy-video">` across all HTML pages with:
     - Explicit `preload="auto"` promotion (fixing the `preload="none"` buffering block on WebKit)
     - Two-tier IntersectionObservers:
       * `prewarmIO` (`rootMargin: '2600px 0px'`) + post-load sequential background queue (`maxActive = 2`)
         so project videos are already buffered in RAM (`readyState >= 3`) well before scrolling to them
       * `playIO` (`rootMargin: '750px 0px'`) so playback is already rolling before cards enter the screen
     - `?v=2` MP4 cache-busting so mobile Safari fetches the fast-startup zero-B-frame streams immediately
     - React hydration attribute guard + passive momentum-scroll / touch resume
  3. Widens `AutoplayVideo` (`30013`) observer `rootMargin` to `1200px 0px` and cache-busts JS/CSS bundles.
"""
import glob
import os
import re
import shutil
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
PUBLIC_DIR = os.path.join(REPO_ROOT, "public")

LAZY_VIDEO_SCRIPT_ID = "roasist-lazy-video"
INSTANT_LAZY_VIDEO_SCRIPT = f"""<script id="{LAZY_VIDEO_SCRIPT_ID}">
(function() {{
  var MP4_VER = 'v=2';
  var SELECTOR = 'video.ProjectCard_video__AheFz[data-src], .ServiceMedia_mediaContainer__WGgZa video[data-src]';
  var conn = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
  var saveData = !!(conn && conn.saveData);

  function withVer(url) {{
    if (!url) return url;
    if (url.indexOf('/projects/') !== -1 && url.indexOf('?') === -1) {{
      return url + '?' + MP4_VER;
    }}
    return url;
  }}

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

  function markReady(v) {{
    if (v && !v.classList.contains('is-ready')) {{
      v.classList.add('is-ready');
    }}
  }}

  function bindReadyEvents(v) {{
    if (!v || v.dataset.roasistBound) return;
    v.dataset.roasistBound = '1';
    ['loadeddata', 'canplay', 'playing'].forEach(function(ev) {{
      v.addEventListener(ev, function() {{ markReady(v); }}, {{ passive: true }});
    }});
    v.addEventListener('timeupdate', function() {{
      if (v.currentTime > 0.02) markReady(v);
    }}, {{ passive: true }});
  }}

  function attachAndBuffer(v, onDone) {{
    if (!v) {{ if (onDone) onDone(); return; }}
    ensureInlineAttrs(v);
    bindReadyEvents(v);
    var ds = v.getAttribute('data-src');
    var targetSrc = withVer(ds);
    v.preload = 'auto';
    v.setAttribute('preload', 'auto');
    v.dataset.roasistWarmed = '1';

    if (targetSrc && v.getAttribute('src') !== targetSrc) {{
      var finished = false;
      var finish = function() {{
        if (finished) return;
        finished = true;
        if (onDone) onDone();
      }};
      v.addEventListener('canplay', finish, {{ once: true, passive: true }});
      v.addEventListener('loadeddata', finish, {{ once: true, passive: true }});
      v.addEventListener('error', finish, {{ once: true, passive: true }});
      setTimeout(finish, 650);
      v.setAttribute('src', targetSrc);
      try {{ v.load(); }} catch (e) {{ finish(); }}
    }} else {{
      if (v.readyState >= 2) markReady(v);
      if (onDone) onDone();
    }}
  }}

  function playNow(v) {{
    if (!v) return;
    attachAndBuffer(v);
    if (v.readyState >= 2) markReady(v);
    var p = v.play();
    if (p && typeof p.then === 'function') {{
      p.then(function() {{ markReady(v); }}).catch(function() {{}});
    }}
  }}

  // Sequential Prewarm Queue (prevents 5 simultaneous MP4 downloads fighting for mobile bandwidth)
  var queue = [];
  var activeLoads = 0;
  var MAX_CONCURRENT = 3;

  function pumpQueue() {{
    while (activeLoads < MAX_CONCURRENT && queue.length > 0) {{
      var nextVid = queue.shift();
      if (!nextVid || nextVid.dataset.roasistWarmed === '1') continue;
      activeLoads++;
      attachAndBuffer(nextVid, function() {{
        activeLoads = Math.max(0, activeLoads - 1);
        pumpQueue();
      }});
    }}
  }}

  function enqueuePrewarm(v, urgent) {{
    if (!v || v.dataset.roasistWarmed === '1') return;
    var idx = queue.indexOf(v);
    if (urgent) {{
      if (idx !== -1) queue.splice(idx, 1);
      queue.unshift(v);
    }} else if (idx === -1) {{
      queue.push(v);
    }}
    pumpQueue();
  }}

  function initHeroVideos() {{
    document.querySelectorAll('video[class*="Hero_video__"]').forEach(function(v) {{
      if (window.getComputedStyle && window.getComputedStyle(v).display === 'none') return;
      ensureInlineAttrs(v);
      v.preload = 'auto';
      v.setAttribute('preload', 'auto');
      var p = v.play();
      if (p && typeof p.catch === 'function') p.catch(function() {{}});
    }});
  }}

  if (!('IntersectionObserver' in window)) {{
    initHeroVideos();
    document.querySelectorAll(SELECTOR).forEach(playNow);
    return;
  }}

  var visibleSet = new Set();

  // Tier 1: Wide Prewarm Observer (3600px ~ 4 mobile screens ahead)
  var prewarmIO = new IntersectionObserver(function(entries) {{
    entries.forEach(function(entry) {{
      if (entry.isIntersecting) {{
        enqueuePrewarm(entry.target, true);
        prewarmIO.unobserve(entry.target);
      }}
    }});
  }}, {{ rootMargin: '3600px 0px', threshold: 0.01 }});

  // Tier 2: Early Play Observer (800px ~ 1 mobile screen ahead so video is already rolling on entry)
  var playIO = new IntersectionObserver(function(entries) {{
    entries.forEach(function(entry) {{
      var v = entry.target;
      if (entry.isIntersecting) {{
        visibleSet.add(v);
        playNow(v);
      }} else {{
        visibleSet.delete(v);
        if (v.getAttribute('src') && !v.paused) {{
          try {{ v.pause(); }} catch (e) {{}}
        }}
      }}
    }});
  }}, {{ rootMargin: '800px 0px', threshold: 0.01 }});

  function observeVideos(root) {{
    initHeroVideos();
    (root || document).querySelectorAll(SELECTOR).forEach(function(v) {{
      bindReadyEvents(v);
      if (!v.dataset.roasistObserved) {{
        v.dataset.roasistObserved = '1';
        prewarmIO.observe(v);
        playIO.observe(v);
      }}
    }});
  }}

  // Background sequential warmup 750ms after DOMContentLoaded (does not block on external GTM load)
  function startIdleWarmup() {{
    if (saveData) return;
    document.querySelectorAll('video.ProjectCard_video__AheFz[data-src]').forEach(function(v) {{
      enqueuePrewarm(v, false);
    }});
    document.querySelectorAll('.ServiceMedia_mediaContainer__WGgZa video[data-src]').forEach(function(v) {{
      enqueuePrewarm(v, false);
    }});
  }}

  if (document.readyState === 'loading') {{
    document.addEventListener('DOMContentLoaded', function() {{ setTimeout(startIdleWarmup, 750); }}, {{ once: true }});
  }} else {{
    setTimeout(startIdleWarmup, 750);
  }}

  // Resume helper for iOS Safari momentum scroll & touch unlock
  function resumeVisible() {{
    visibleSet.forEach(function(v) {{
      if (v.paused) playNow(v);
    }});
    document.querySelectorAll('.ServiceMedia_mediaContainer__WGgZa video, .AutoplayVideo_video__zckWy video, video[class*="Hero_video__"]').forEach(function(v) {{
      if (window.getComputedStyle && window.getComputedStyle(v).display === 'none') return;
      if ((v.getAttribute('src') || v.getAttribute('data-src')) && v.paused) {{
        var r = v.getBoundingClientRect();
        if (r.bottom > -400 && r.top < (window.innerHeight || 900) + 400) {{
          playNow(v);
        }}
      }}
    }});
  }}
  window.addEventListener('touchstart', resumeVisible, {{ passive: true }});
  window.addEventListener('touchend', resumeVisible, {{ passive: true }});

  var scrollTick = false;
  window.addEventListener('scroll', function() {{
    if (scrollTick) return;
    scrollTick = true;
    setTimeout(function() {{
      scrollTick = false;
      visibleSet.forEach(function(v) {{
        if (v.paused) playNow(v);
      }});
    }}, 180);
  }}, {{ passive: true }});

  if (document.readyState === 'loading') {{
    document.addEventListener('DOMContentLoaded', function() {{ observeVideos(document); }});
  }} else {{
    observeVideos(document);
  }}

  // Guard against React hydration resetting preload="none" or stripping src on warmed <video> elements
  if ('MutationObserver' in window) {{
    var mo = new MutationObserver(function(muts) {{
      var added = false;
      for (var i = 0; i < muts.length; i++) {{
        var m = muts[i];
        if (m.type === 'childList' && m.addedNodes && m.addedNodes.length) {{
          added = true;
        }} else if (m.type === 'attributes' && m.target && m.target.tagName === 'VIDEO' && m.target.dataset && m.target.dataset.roasistWarmed === '1') {{
          var v = m.target;
          if (v.getAttribute('preload') !== 'auto') {{
            v.preload = 'auto';
            v.setAttribute('preload', 'auto');
          }}
          var ds = v.getAttribute('data-src');
          if (ds && !v.getAttribute('src')) {{
            v.setAttribute('src', withVer(ds));
            try {{ v.load(); }} catch (e) {{}}
            if (visibleSet.has(v)) playNow(v);
          }}
        }}
      }}
      if (added) observeVideos(document);
    }});
    var startMo = function() {{
      if (document.body) {{
        mo.observe(document.body, {{ childList: true, subtree: true, attributes: true, attributeFilter: ['preload', 'src'] }});
      }}
    }};
    if (document.body) startMo();
    else document.addEventListener('DOMContentLoaded', startMo);
  }}
}})();
</script>"""

def step1_reencode_project_mp4s_zero_bframe():
    mp4s = sorted(glob.glob(os.path.join(PUBLIC_DIR, "images", "projects", "*.mp4")))
    before_total = 0
    after_total = 0
    reencoded = 0
    for mp4 in mp4s:
        orig_sz = os.path.getsize(mp4)
        before_total += orig_sz
        bf_chk = subprocess.check_output(
            ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=has_b_frames,width", "-of", "csv=p=0", mp4]
        ).decode().strip()
        if bf_chk == "854,0" or bf_chk == "0,854":
            after_total += orig_sz
            continue
        tmp_out = mp4 + ".lowlat.mp4"
        cmd = ["ffmpeg", "-y", "-loglevel", "error"]
        if os.path.basename(mp4) == "23-projects.mp4":
            cmd += ["-ss", "0.30"]
        cmd += [
            "-i", mp4,
            "-an",
            "-c:v", "libx264",
            "-profile:v", "main",
            "-pix_fmt", "yuv420p",
            "-bf", "0",
            "-g", "45",
            "-keyint_min", "24",
            "-crf", "26",
            "-maxrate", "550k",
            "-bufsize", "950k",
            "-vf", "scale='min(854,iw)':-2",
            "-movflags", "+faststart",
            tmp_out,
        ]
        subprocess.run(cmd, check=True)
        new_sz = os.path.getsize(tmp_out)
        os.replace(tmp_out, mp4)
        after_total += new_sz
        reencoded += 1
        print(f"  [MP4] {os.path.basename(mp4)}: {orig_sz / 1024:.0f} KB -> {new_sz / 1024:.0f} KB (0 B-frames, +faststart)")
    print(f"[1/4] Project MP4s ready ({reencoded} re-encoded): {after_total / 1024 / 1024:.2f} MB total")


def step2_widen_autoplay_video_rootmargin():
    for fname in ("988-86d1af1c6c90b59b.js", "988-86d1af1c6c90b59c.js"):
        fp = os.path.join(PUBLIC_DIR, "_next", "static", "chunks", fname)
        if not os.path.exists(fp):
            continue
        s = open(fp, "r", encoding="utf-8").read()
        s2 = s.replace('rootMargin:"320px 0px"', 'rootMargin:"1200px 0px"')
        if s2 != s:
            open(fp, "w", encoding="utf-8").write(s2)
    print("[2/4] Widened AutoplayVideo (ServicesPanel) rootMargin to 1200px")


def step3_update_html_lazy_video_scripts():
    script_re = re.compile(rf'<script id="{LAZY_VIDEO_SCRIPT_ID}">.*?</script>', re.S)
    updated = 0
    for fp in sorted(glob.glob(os.path.join(PUBLIC_DIR, "**", "*.html"), recursive=True)):
        rel = os.path.relpath(fp, PUBLIC_DIR)
        if rel == "404.html" or rel.endswith("-3d.html") or "api/" in rel:
            continue
        orig = open(fp, "r", encoding="utf-8").read()
        if script_re.search(orig):
            upd = script_re.sub(lambda _: INSTANT_LAZY_VIDEO_SCRIPT, orig, count=1)
            if upd != orig:
                open(fp, "w", encoding="utf-8").write(upd)
                updated += 1
    print(f"[3/4] Upgraded instant two-tier prewarm video engine across {updated} HTML pages")


def step4_update_css_and_cache_bust():
    chunks_dir = os.path.join(PUBLIC_DIR, "_next", "static", "chunks")
    pairs = []
    src_988 = os.path.join(chunks_dir, "988-86d1af1c6c90b59b.js")
    dst_988 = os.path.join(chunks_dir, "988-86d1af1c6c90b59d.js")
    if os.path.exists(src_988):
        shutil.copy2(src_988, dst_988)
        pairs.append(("988-86d1af1c6c90b59c.js", "988-86d1af1c6c90b59d.js"))

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
    print(f"[4/4] Cache-busted {len(pairs)} JS chunk(s) across {touched} files")


def main():
    step1_reencode_project_mp4s_zero_bframe()
    step2_widen_autoplay_video_rootmargin()
    step3_update_html_lazy_video_scripts()
    step4_update_css_and_cache_bust()


if __name__ == "__main__":
    main()
