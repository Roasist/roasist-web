#!/usr/bin/env python3
"""
Mobile CTA Cleanup & Rock-Solid Floating 'Teklif Al' Button:
  1. Removes 'Teklif Al' / 'Projeye Başla' buttons from both the mobile top Header
     (`.Header_button__yG4_K`) and mobile Hamburger Menu (`.PrimaryNavigation_buttonContainer__iiKTy`)
     below `769px`.
  2. Eliminates the mobile scroll flicker/disappearing bug on `.FloatingStartButton_linkContainer__eZz7z`
     (caused by `roasist-arrow-rotator` calling `flt.style.removeProperty('opacity')` on every scroll tick
     and fighting GSAP's broken `#kotaverceCta` ScrollTrigger), replacing it with a deterministic,
     zero-flicker `body.roasist-show-floating-cta` controller (`scrollY > 180`, hidden in menu & footer,
     lifted cleanly above cookie bar if open).
  3. Renames the floating button from 'Projeye Başla' / 'Projeye Başlayın' to 'Teklif Al' (TR)
     and 'Get a Quote' (EN) across SSR HTML, Flight AST, post-hydration scripts, and all JS chunks,
     and cache-busts modified JS/CSS assets so mobile Safari updates immediately on refresh.
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

MOBILE_CTA_CSS = """
/* === MOBILE CTA HIERARCHY & STABLE FLOATING 'TEKLİF AL' BUTTON === */
@media (max-width: 768px) {
  .Header_header__KwdYD .Header_button__yG4_K,
  header[class*="Header_header"] a[class*="Header_button"],
  .PrimaryNavigation_buttonContainer__iiKTy,
  nav[class*="PrimaryNavigation_navigation"] [class*="PrimaryNavigation_buttonContainer"] {
    display: none !important;
  }
}

.FloatingStartButton_linkContainer__eZz7z {
  z-index: 88 !important;
  opacity: 0 !important;
  visibility: hidden !important;
  transform: translate3d(0, 12px, 0) !important;
  pointer-events: none !important;
  transition:
    opacity 180ms cubic-bezier(0.22, 1, 0.36, 1),
    transform 180ms cubic-bezier(0.22, 1, 0.36, 1),
    bottom 180ms cubic-bezier(0.22, 1, 0.36, 1),
    visibility 180ms !important;
}

@media (max-width: 640px) {
  .FloatingStartButton_linkContainer__eZz7z {
    padding: 1rem 1.125rem !important;
  }
  body.roasist-cookie-open .FloatingStartButton_linkContainer__eZz7z {
    bottom: 132px !important;
  }
}

body.roasist-show-floating-cta:not(.roasist-footer-in-view):not(.roasist-menu-open) .FloatingStartButton_linkContainer__eZz7z {
  opacity: 1 !important;
  visibility: visible !important;
  transform: translate3d(0, 0, 0) !important;
}

body.roasist-show-floating-cta:not(.roasist-footer-in-view):not(.roasist-menu-open) .FloatingStartButton_button__Ncnrf {
  pointer-events: auto !important;
}

.FloatingStartButton_button__Ncnrf {
  background-color: #0f172a !important;
  color: #ffffff !important;
  border: 1px solid rgba(255, 255, 255, 0.16) !important;
  box-shadow: 0 10px 28px -6px rgba(15, 23, 42, 0.42) !important;
  font-weight: 600 !important;
  transition: background-color 170ms cubic-bezier(0.22, 1, 0.36, 1), transform 170ms cubic-bezier(0.22, 1, 0.36, 1) !important;
}

.FloatingStartButton_button__Ncnrf:hover {
  background-color: #7602FF !important;
  color: #ffffff !important;
}

.FloatingStartButton_button__Ncnrf .FloatingStartButton_buttonArrow__re1eN {
  color: #ffffff !important;
}
"""

FLOATING_CONTROLLER_JS = """<script id="roasist-floating-cta-ctrl">
(function() {
  var isEn = document.documentElement.lang === 'en' || window.location.pathname.indexOf('/en/') === 0 || window.location.pathname === '/en';
  var targetLabel = isEn ? 'Get a Quote' : 'Teklif Al';
  var targetHref = isEn ? '/en/contact-us/' : '/iletisim/';

  function syncFloatingLabel() {
    var btn = document.querySelector('.FloatingStartButton_button__Ncnrf');
    if (!btn) return;
    if (btn.getAttribute('href') !== targetHref) {
      btn.setAttribute('href', targetHref);
    }
    var txtWrap = btn.querySelector('.FloatingStartButton_text__70x9M');
    if (txtWrap) {
      var sp = txtWrap.querySelector('span');
      if (sp && sp.textContent !== targetLabel) {
        sp.textContent = targetLabel;
      }
    }
  }

  function updateFloatingState() {
    syncFloatingLabel();
    var sy = window.scrollY || window.pageYOffset || 0;
    var vh = window.innerHeight || 844;
    var ftr = document.querySelector('footer[class*="Footer_footer"]');
    var ftrInView = false;
    if (ftr) {
      var fr = ftr.getBoundingClientRect();
      ftrInView = fr.top < vh * 0.94;
    }
    var menuOpen = !!document.querySelector('[class*="PrimaryNavigation_active"]');
    var cookieOpen = !!document.querySelector('.roasist-cookie-bar.is-visible');

    document.body.classList.toggle('roasist-footer-in-view', ftrInView);
    document.body.classList.toggle('roasist-menu-open', menuOpen);
    document.body.classList.toggle('roasist-cookie-open', cookieOpen);
    document.body.classList.toggle('roasist-show-floating-cta', sy > 180 && !ftrInView && !menuOpen);
  }

  var rafPending = false;
  function requestUpdate() {
    if (rafPending) return;
    rafPending = true;
    requestAnimationFrame(function() {
      rafPending = false;
      updateFloatingState();
    });
  }

  window.addEventListener('scroll', requestUpdate, { passive: true });
  window.addEventListener('resize', requestUpdate, { passive: true });
  document.addEventListener('click', function() { setTimeout(requestUpdate, 60); setTimeout(requestUpdate, 350); }, { passive: true });

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      updateFloatingState();
      setTimeout(updateFloatingState, 600);
      setTimeout(updateFloatingState, 1500);
    });
  } else {
    updateFloatingState();
    setTimeout(updateFloatingState, 600);
    setTimeout(updateFloatingState, 1500);
  }

  if ('MutationObserver' in window) {
    var startObs = function() {
      if (!document.body) return;
      new MutationObserver(function() {
        syncFloatingLabel();
        var cookieOpen = !!document.querySelector('.roasist-cookie-bar.is-visible');
        var menuOpen = !!document.querySelector('[class*="PrimaryNavigation_active"]');
        document.body.classList.toggle('roasist-cookie-open', cookieOpen);
        document.body.classList.toggle('roasist-menu-open', menuOpen);
      }).observe(document.body, { childList: true, subtree: true, attributes: true, attributeFilter: ['class'] });
    };
    if (document.body) startObs();
    else document.addEventListener('DOMContentLoaded', startObs);
  }
})();
</script>"""


def step1_patch_floating_button_js_chunks() -> list:
    chunks_dir = os.path.join(PUBLIC_DIR, "_next", "static", "chunks")
    label_expr = '("undefined"!=typeof document&&"en"===document.documentElement.lang?"Get a Quote":"Teklif Al")'
    href_expr = '("undefined"!=typeof document&&"en"===document.documentElement.lang?"/en/contact-us/":"/iletisim/")'

    modified_chunks = []
    for fp in sorted(glob.glob(os.path.join(chunks_dir, "**", "*.js"), recursive=True)):
        orig = open(fp, "r", encoding="utf-8", errors="ignore").read()
        if "FloatingStartButton_linkContainer__eZz7z" not in orig and "86802:function" not in orig:
            continue
        upd = orig
        # Replace href:"/start-your-project" inside FloatingStartButton
        upd = upd.replace('href:"/start-your-project",children:', f"href:{href_expr},children:")
        for old_lbl in ('"Projeye Başlayın"', '"Projeye Başla"', '"Start your project"'):
            upd = re.sub(
                r'(\.textInner,children:)' + re.escape(old_lbl),
                lambda m: m.group(1) + label_expr,
                upd,
            )
        if upd != orig:
            open(fp, "w", encoding="utf-8").write(upd)
            modified_chunks.append(fp)

    print(f"[1/4] Updated FloatingStartButton label ('Teklif Al' / 'Get a Quote') & href in {len(modified_chunks)} JS chunks")
    return modified_chunks


def step2_update_html_pages():
    # Remove old inline opacity-wiping block inside roasist-arrow-rotator
    arrow_flt_re = re.compile(
        r"var flt = document\.querySelector\('\.FloatingStartButton_linkContainer__eZz7z'\);\s*"
        r"if \(ftr\) \{.*?\n    \}",
        re.S,
    )
    arrow_flt_clean = """if (ftr) {
      var fr = ftr.getBoundingClientRect();
      document.body.classList.toggle('roasist-footer-in-view', fr.top < vh * 0.94);
    }"""

    # Remove old 550px mobile Header_button inline-flex override from inline UX style
    old_550_re = re.compile(
        r"@media\s*\(max-width:\s*550px\)\s*\{\s*\.Header_header__KwdYD\s+\.Header_button__yG4_K\s*\{[^}]*\}\s*\}",
        re.S,
    )
    ctrl_re = re.compile(r'<script id="roasist-floating-cta-ctrl">.*?</script>', re.S)

    updated = 0
    for fp in sorted(glob.glob(os.path.join(PUBLIC_DIR, "**", "*.html"), recursive=True)):
        rel = os.path.relpath(fp, PUBLIC_DIR).replace(os.sep, "/")
        if rel == "404.html" or rel.endswith("-3d.html") or "api/" in rel:
            continue
        is_en = rel.startswith("en/")
        btn_lbl = "Get a Quote" if is_en else "Teklif Al"
        btn_href = "/en/contact-us/" if is_en else "/iletisim/"

        orig = open(fp, "r", encoding="utf-8").read()

        # Transform SSR + Flight safely for FloatingStartButton SSR & Flight text
        matches, _, full = extract_flight_chunks(orig)

        def transform_non_flight(seg: str) -> str:
            seg = old_550_re.sub("", seg)
            seg = arrow_flt_re.sub(arrow_flt_clean, seg)
            # Update SSR FloatingStartButton markup
            seg = re.sub(
                r'(<div class="FloatingStartButton_linkContainer__eZz7z"><a class="FloatingStartButton_button__Ncnrf" href=")[^"]+(".*?<span class="FloatingStartButton_text__70x9M"><span>)[^<]+(</span>)',
                rf"\g<1>{btn_href}\g<2>{btn_lbl}\g<3>",
                seg,
                flags=re.S,
            )
            # Update data-roasist-ui EN enhancer so FloatingStartButton gets 'Get a Quote'
            seg = seg.replace(
                "if (sp.children.length === 0 && (sp.textContent === 'Projeye Başla' || sp.textContent === 'Projeye Başlayın')) {\n            sp.textContent = 'Start a Project';",
                "if (sp.children.length === 0 && (sp.textContent === 'Projeye Başla' || sp.textContent === 'Projeye Başlayın' || sp.textContent === 'Teklif Al')) {\n            sp.textContent = 'Get a Quote';",
            )
            return seg

        if matches:
            recs = parse_flight_stream(full)
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

        # Inject / update FLOATING_CONTROLLER_JS right before </body> (skip contact pages where user is already on the form)
        is_contact_page = rel in (
            "iletisim/index.html",
            "start-your-project/index.html",
            "en/contact-us/index.html",
            "en/start-your-project/index.html",
        )
        if not is_contact_page:
            if ctrl_re.search(upd):
                upd = ctrl_re.sub(lambda _: FLOATING_CONTROLLER_JS, upd, count=1)
            else:
                body_end = upd.rfind("</body>")
                if body_end != -1:
                    upd = upd[:body_end] + FLOATING_CONTROLLER_JS + upd[body_end:]
        else:
            upd = ctrl_re.sub("", upd)

        if upd != orig:
            open(fp, "w", encoding="utf-8").write(upd)
            updated += 1

    print(f"[2/4] Updated HTML markup & deterministic floating CTA controller across {updated} pages")


def step3_update_css_and_bundles():
    css_dir = os.path.join(PUBLIC_DIR, "_next", "static", "css")
    old_block_re = re.compile(
        r"\n/\* === MOBILE CTA HIERARCHY & STABLE FLOATING 'TEKLİF AL' BUTTON === \*/.*?(?=\n/\* ===|\Z)",
        re.S,
    )

    targets = [
        os.path.join(css_dir, "84191844b30595bc.css"),
        os.path.join(css_dir, "053ade63481ccabc.css"),
        os.path.join(css_dir, "e36a1a112c1c5ec8.css"),
    ] + sorted(glob.glob(os.path.join(css_dir, "roasist-bundle-*.css")))

    count = 0
    for fp in targets:
        if not os.path.exists(fp):
            continue
        orig = open(fp, "r", encoding="utf-8").read()
        upd = old_block_re.sub("", orig) + "\n" + MOBILE_CTA_CSS
        if upd != orig:
            open(fp, "w", encoding="utf-8").write(upd)
            count += 1
    print(f"[3/4] Applied mobile header/menu CTA hide & floating CTA styles across {count} CSS files/bundles")


def step4_cache_bust_assets():
    css_dir = os.path.join(PUBLIC_DIR, "_next", "static", "css")
    chunks_dir = os.path.join(PUBLIC_DIR, "_next", "static", "chunks")
    pairs = []

    # Cache-bust CSS bundles (*m3.css -> *m5.css)
    for fp in sorted(glob.glob(os.path.join(css_dir, "roasist-bundle-*m3.css"))):
        old_base = os.path.basename(fp)
        new_base = old_base[:-6] + "m5.css"
        assert len(old_base) == len(new_base)
        shutil.copy2(fp, os.path.join(css_dir, new_base))
        pairs.append((old_base, new_base))

    # Cache-bust active page chunks with same-byte-length aliases
    chunk_bumps = [
        ("app/(home)/page-b58f77e3dc47742c.js", "app/(home)/page-b58f77e3dc47742d.js", "app/(home)/page-b58f77e3dc47742e.js"),
        ("app/blog/page-227af4ac752ea4f7.js", "app/blog/page-227af4ac752ea4f8.js", "app/blog/page-227af4ac752ea4f9.js"),
        ("app/agency/page-4ecdeefc9091d461.js", "app/agency/page-4ecdeefc9091d461.js", "app/agency/page-4ecdeefc9091d462.js"),
        ("app/work/page-5b3919766e28ce0e.js", "app/work/page-5b3919766e28ce0e.js", "app/work/page-5b3919766e28ce0f.js"),
    ]
    for base_rel, prev_rel, next_rel in chunk_bumps:
        src = os.path.join(chunks_dir, prev_rel)
        if not os.path.exists(src):
            src = os.path.join(chunks_dir, base_rel)
        dst = os.path.join(chunks_dir, next_rel)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            old_b = os.path.basename(prev_rel)
            new_b = os.path.basename(next_rel)
            assert len(old_b) == len(new_b)
            pairs.append((old_b, new_b))

    # For dynamic route chunks ([slug] & %5Bslug%5D), keep URL-encoded & decoded copies synced + bump last hex char
    dyn_bumps = [
        ("app/service/[slug]/page-53d2604786d625db.js", "app/service/[slug]/page-53d2604786d625dc.js",
         "app/service/%5Bslug%5D/page-53d2604786d625dc.js"),
        ("app/[slug]/page-476cfeca3f4b50d2.js", "app/[slug]/page-476cfeca3f4b50d3.js",
         "app/%5Bslug%5D/page-476cfeca3f4b50d3.js"),
        ("app/blog/[slug]/page-d99a465d7f04c801.js", "app/blog/[slug]/page-d99a465d7f04c802.js",
         "app/blog/%5Bslug%5D/page-d99a465d7f04c802.js"),
        ("app/work/[slug]/page-52a6fe0f49fb5a18.js", "app/work/[slug]/page-52a6fe0f49fb5a19.js",
         "app/work/%5Bslug%5D/page-52a6fe0f49fb5a19.js"),
    ]
    for src_rel, dst_rel1, dst_rel2 in dyn_bumps:
        src = os.path.join(chunks_dir, src_rel)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(chunks_dir, dst_rel1))
            shutil.copy2(src, os.path.join(chunks_dir, dst_rel2))
            old_b = os.path.basename(src_rel)
            new_b = os.path.basename(dst_rel1)
            assert len(old_b) == len(new_b)
            pairs.append((old_b, new_b))

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
    print(f"[4/4] Cache-busted {len(pairs)} CSS/JS assets across {touched} files")


def main():
    step1_patch_floating_button_js_chunks()
    step2_update_html_pages()
    step3_update_css_and_bundles()
    step4_cache_bust_assets()


if __name__ == "__main__":
    main()
