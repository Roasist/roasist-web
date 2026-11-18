"""Inject the 60 FPS 3D Z-Axis Kinetic Typography (Word Cloud Fly-Through)
canvas and updated video/poster URLs into the homepage 'Önce veri ve strateji'
methodology card across public/ and dist/."""

import pathlib
import re

ROOT = pathlib.Path("/home/antigravity/Roasist/roasist-web")

TARGET_FILES = [
    "public/kota-roasist-local.html",
    "public/en/index.html",
    "dist/index.html",
    "dist/en/index.html",
]

KINETIC_3D_BLOCK = """<style data-roasist-kinetic-3d-style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@800&display=swap&subset=latin,latin-ext');

html body #carousel .swiper-slide:nth-child(1) .CarouselSlides_carouselMedia__aqYWx {
  background-color: #0B0914 !important;
  border-radius: 24px !important;
  overflow: hidden !important;
  border: 1px solid rgba(167, 139, 250, 0.16) !important;
  box-shadow: 0 24px 60px -15px rgba(11, 9, 20, 0.85), inset 0 1px 0 0 rgba(255, 255, 255, 0.06) !important;
  position: relative !important;
  isolation: isolate !important;
}

html body #carousel .swiper-slide:nth-child(1) .CarouselSlides_carouselMedia__aqYWx::before {
  content: "" !important;
  position: absolute !important;
  inset: 0 !important;
  background:
    radial-gradient(circle at 50% 50%, rgba(124, 58, 237, 0.08) 0%, rgba(11, 9, 20, 0) 64%),
    radial-gradient(circle at 50% 50%, rgba(11, 9, 20, 0) 58%, rgba(11, 9, 20, 0.84) 100%) !important;
  pointer-events: none !important;
  z-index: 3 !important;
}

html body .roasist-kinetic-3d-canvas {
  position: absolute !important;
  inset: 0 !important;
  width: 100% !important;
  height: 100% !important;
  display: block !important;
  z-index: 2 !important;
  border-radius: 24px !important;
  pointer-events: none !important;
}
</style>
<script data-roasist-kinetic-3d-script>
(() => {
  const WORD_LIST = [
    'VERİ',
    'STRATEJİ',
    'ANALİZ',
    'BİRİM EKONOMİSİ',
    'BÜYÜME',
    'YOL HARİTASI',
    'PAZAR ANALİZİ',
    'RAKİP İSTİHBARATI',
    'HEDEF KİTLE',
    'KONUMLANDIRMA',
    'DÖNÜŞÜM HUNİSİ',
    'PLANLAMA',
    'TALEP ANALİZİ',
    'SEGMENTASYON',
    'KOHORT'
  ];

  const HIGHLIGHT_SET = new Set([
    'VERİ',
    'STRATEJİ',
    'BİRİM EKONOMİSİ',
    'YOL HARİTASI'
  ]);

  const COLOR_BG = '#0B0914';
  const COLOR_HIGHLIGHT = '#A78BFA';
  const COLOR_WHITE = '#FFFFFF';
  const COLOR_SLATE = '#94A3B8';

  const CYCLES = 3;
  const TOTAL_NODES = WORD_LIST.length * CYCLES;
  const LOOP_DURATION = 16.0;

  function createSeededRandom(seed) {
    let s = seed >>> 0;
    return () => {
      s = (s * 1664525 + 1013904223) >>> 0;
      return s / 4294967296;
    };
  }

  function getScaleAtZ(z, sizeMultiplier) {
    const approach = 1 - z;
    return (0.24 + 1.18 * Math.pow(approach, 2.05)) * sizeMultiplier;
  }

  function getParallaxAtZ(z) {
    const approach = 1 - z;
    return 0.72 + 0.36 * Math.pow(approach, 1.35);
  }

  function computeOpacity(z) {
    if (z > 0.92) {
      const t = Math.max(0, Math.min(1, (1.0 - z) / 0.08));
      return 0.15 * (t * t * (3 - 2 * t));
    }
    if (z > 0.66) {
      const t = (0.92 - z) / (0.92 - 0.66);
      return 0.15 + 0.10 * t;
    }
    if (z > 0.26) {
      const t = (0.66 - z) / (0.66 - 0.26);
      const smooth = t * t * (3 - 2 * t);
      return 0.25 + 0.75 * smooth;
    }
    if (z > 0.13) return 1.0;
    const t = Math.max(0, Math.min(1, z / 0.13));
    return t * t * (3 - 2 * t);
  }

  function buildSceneNodes() {
    const rand = createSeededRandom(20261128);
    const placed = [];
    const zStep = 1.0 / TOTAL_NODES;
    const REF_BASE_FONT = 38;

    const sequence = [];
    for (let c = 0; c < CYCLES; c++) {
      const cycleWords = [...WORD_LIST];
      for (let i = cycleWords.length - 1; i > 0; i--) {
        const j = Math.floor(rand() * (i + 1));
        const tmp = cycleWords[i];
        cycleWords[i] = cycleWords[j];
        cycleWords[j] = tmp;
      }
      sequence.push(...cycleWords);
    }

    const ROWS = 9;
    const COLS = 3;
    const TOTAL_SLOTS = ROWS * COLS;

    for (let i = 0; i < TOTAL_NODES; i++) {
      const text = sequence[i];
      const isHighlight = HIGHLIGHT_SET.has(text);
      const zBase = i * zStep;
      const sizeMultiplier = isHighlight ? 1.15 : (i % 3 === 0 ? 1.02 : 0.90);

      const peakScale = getScaleAtZ(0.18, sizeMultiplier);
      const peakFontSize = REF_BASE_FONT * peakScale;
      const peakHalfW = (text.length * peakFontSize * 0.34) + 22;
      const peakHalfH = (peakFontSize * 0.65) + 16;

      const maxSafeX = Math.max(120, 465 - peakHalfW * 0.85);
      const maxSafeY = Math.max(80, 340 - peakHalfH);

      let bestX = 0;
      let bestY = 0;
      let bestScore = -Infinity;

      for (let attempt = 0; attempt < 60; attempt++) {
        const slotIdx = (i * 13 + attempt * 5) % TOTAL_SLOTS;
        const row = slotIdx % ROWS;
        const col = Math.floor(slotIdx / ROWS);

        const rowOffset = (row % 2 === 0) ? -0.14 : 0.14;
        const baseNormX = ((col + 0.5) / COLS) * 2 - 1 + rowOffset + (rand() - 0.5) * 0.36;
        const baseNormY = ((row + 0.5) / ROWS) * 2 - 1 + (rand() - 0.5) * 0.22;

        const candX = Math.max(-maxSafeX, Math.min(maxSafeX, baseNormX * maxSafeX));
        const candY = Math.max(-maxSafeY, Math.min(maxSafeY, baseNormY * maxSafeY));

        let minClearance = Infinity;

        for (let j = 0; j < placed.length; j++) {
          const other = placed[j];
          let rawDz = zBase - other.zBase;
          if (rawDz > 0.5) rawDz -= 1.0;
          if (rawDz < -0.5) rawDz += 1.0;
          const absDz = Math.abs(rawDz);

          if (absDz < 0.52) {
            const testZs = [0.20, 0.36, 0.54, 0.72];
            for (let k = 0; k < testZs.length; k++) {
              const z1 = testZs[k];
              const z2 = z1 - rawDz;
              if (z2 < 0.06 || z2 > 0.92) continue;

              const p1 = getParallaxAtZ(z1);
              const p2 = getParallaxAtZ(z2);
              const sc1 = getScaleAtZ(z1, sizeMultiplier);
              const sc2 = getScaleAtZ(z2, other.sizeMultiplier);

              const sx1 = candX * p1;
              const sy1 = candY * p1;
              const sx2 = other.x * p2;
              const sy2 = other.y * p2;

              const w1 = (text.length * 34 * sc1 * 0.35) + 18;
              const h1 = (34 * sc1 * 0.72) + 14;
              const w2 = (other.text.length * 34 * sc2 * 0.35) + 18;
              const h2 = (34 * sc2 * 0.72) + 14;

              const dxNorm = Math.abs(sx1 - sx2) / (w1 + w2);
              const dyNorm = Math.abs(sy1 - sy2) / (h1 + h2);

              const boxClearance = Math.max(dxNorm * 0.92, dyNorm * 1.08);
              const score = boxClearance * (0.72 + 0.28 * (absDz / 0.52));

              if (score < minClearance) {
                minClearance = score;
              }
            }
          }
        }

        if (placed.length === 0) minClearance = 10;

        if (minClearance > bestScore) {
          bestScore = minClearance;
          bestX = candX;
          bestY = candY;
        }
      }

      placed.push({
        text,
        isHighlight,
        color: isHighlight ? COLOR_HIGHLIGHT : ((i % 2 === 0) ? COLOR_WHITE : COLOR_SLATE),
        x: bestX,
        y: bestY,
        zBase,
        sizeMultiplier
      });
    }

    return placed;
  }

  const nodes = buildSceneNodes();
  const renderList = new Array(TOTAL_NODES);
  let activeCanvas = null;
  let activeCtx = null;
  let cWidth = 562;
  let cHeight = 434;
  let dpr = 1;
  const startTime = performance.now();

  function ensureCanvasMounted() {
    const mediaContainer = document.querySelector('#carousel .swiper-slide:nth-child(1) .CarouselSlides_carouselMedia__aqYWx');
    if (!mediaContainer) return false;

    let canvas = mediaContainer.querySelector('canvas.roasist-kinetic-3d-canvas');
    if (!canvas) {
      canvas = document.createElement('canvas');
      canvas.className = 'roasist-kinetic-3d-canvas';
      canvas.setAttribute('aria-hidden', 'true');
      mediaContainer.appendChild(canvas);
      activeCanvas = canvas;
      activeCtx = canvas.getContext('2d', { alpha: false });
    }

    const rect = mediaContainer.getBoundingClientRect();
    if (rect.width > 40 && rect.height > 40) {
      const newDpr = Math.min(window.devicePixelRatio || 1, 2);
      const targetW = Math.floor(rect.width);
      const targetH = Math.floor(rect.height);
      if (cWidth !== targetW || cHeight !== targetH || dpr !== newDpr || canvas.width !== targetW * newDpr) {
        cWidth = targetW;
        cHeight = targetH;
        dpr = newDpr;
        canvas.width = cWidth * dpr;
        canvas.height = cHeight * dpr;
      }
    }
    return true;
  }

  function tick(now) {
    if (ensureCanvasMounted() && activeCtx) {
      const elapsedSeconds = (now - startTime) * 0.001;
      const cameraProgress = (elapsedSeconds / LOOP_DURATION) % 1.0;

      activeCtx.save();
      activeCtx.scale(dpr, dpr);

      activeCtx.fillStyle = COLOR_BG;
      activeCtx.fillRect(0, 0, cWidth, cHeight);

      const centerX = cWidth * 0.5;
      const centerY = cHeight * 0.5;
      const viewportScale = Math.min(cWidth / 1020, cHeight / 788);
      const refBaseFont = 34 * viewportScale;

      for (let i = 0; i < TOTAL_NODES; i++) {
        const node = nodes[i];
        let z = (node.zBase - cameraProgress) % 1.0;
        if (z < 0) z += 1.0;
        renderList[i] = { node, z };
      }

      renderList.sort((a, b) => b.z - a.z);

      activeCtx.textAlign = 'center';
      activeCtx.textBaseline = 'middle';

      for (let i = 0; i < TOTAL_NODES; i++) {
        const { node, z } = renderList[i];
        const alpha = computeOpacity(z);
        if (alpha <= 0.005) continue;

        const scale = getScaleAtZ(z, node.sizeMultiplier);
        const parallax = getParallaxAtZ(z);

        const screenX = centerX + node.x * parallax * viewportScale;
        const screenY = centerY + node.y * parallax * viewportScale;
        const fontSize = refBaseFont * scale;

        activeCtx.save();
        activeCtx.font = `800 ${fontSize.toFixed(2)}px 'Inter', -apple-system, BlinkMacSystemFont, sans-serif`;
        if ('letterSpacing' in activeCtx) {
          activeCtx.letterSpacing = `${(-0.03 * fontSize).toFixed(2)}px`;
        }

        activeCtx.globalAlpha = alpha;
        activeCtx.fillStyle = node.color;

        if (node.isHighlight) {
          activeCtx.shadowColor = 'rgba(167, 139, 250, 0.72)';
          activeCtx.shadowBlur = Math.min(26, Math.max(4, 15 * scale * viewportScale));
        } else {
          activeCtx.shadowBlur = 0;
        }

        activeCtx.fillText(node.text, screenX, screenY);
        activeCtx.restore();
      }

      activeCtx.restore();
    }
    requestAnimationFrame(tick);
  }

  requestAnimationFrame(tick);
})();
</script>"""


def main():
    for rel in TARGET_FILES:
        p = ROOT / rel
        if not p.exists():
            continue
        html = p.read_text(encoding="utf-8")

        # Protect byte-counted T712 JSON-LD block
        t712_start = html.find("28:T712,")
        t712_end = html.find("2b:T8f6,", t712_start) if t712_start != -1 else -1
        protected = None
        if t712_start != -1 and t712_end != -1:
            protected = html[t712_start:t712_end]
            html = html[:t712_start] + "__PROTECTED_T712_BLOCK__" + html[t712_end:]

        # Remove any existing kinetic 3d blocks
        html = re.sub(
            r"<style data-roasist-kinetic-3d-style>.*?</style>\s*<script data-roasist-kinetic-3d-script>.*?</script>",
            "",
            html,
            flags=re.DOTALL,
        )

        # Bump cache version on 01-veri-ve-strateji.mp4 and .jpg
        html = html.replace(
            "01-veri-ve-strateji.mp4?v=3", "01-veri-ve-strateji.mp4"
        ).replace(
            "01-veri-ve-strateji.jpg?v=3", "01-veri-ve-strateji.jpg"
        )
        html = html.replace(
            "01-veri-ve-strateji.mp4", "01-veri-ve-strateji.mp4?v=3"
        ).replace(
            "01-veri-ve-strateji.jpg", "01-veri-ve-strateji.jpg?v=3"
        )

        if "</body>" in html:
            html = html.replace("</body>", KINETIC_3D_BLOCK + "</body>", 1)

        if protected is not None:
            html = html.replace("__PROTECTED_T712_BLOCK__", protected)

        p.write_text(html, encoding="utf-8")
        print(f"Injected 3D Kinetic Typography into {rel}")


if __name__ == "__main__":
    main()
