"""Inject the 60 FPS HTML + CSS + Canvas animations for Slides 1, 2, 3, 4 & 5:
  - Slide 1 ('Önce veri ve strateji'): 3D Z-Axis Kinetic Typography (15 words)
  - Slide 2 ('Yaratıcı ve cesur fikir'): 3D Perspective Creative Bento & Particle Sphere
  - Slide 3 ('Kusursuz süreç yönetimi'): Agile Sprint Kanban Board & Real-Time ROAS Momentum Cockpit
  - Slide 4 ('Dönüşüm için tasarla'): 3D Exploded Isometric Web & UX Anatomy
  - Slide 5 ('Ölçeklenebilir büyüme'): 3D Rotating Global Expansion Globe, Great-Circle Arcs & Daylight Scale Card
and eliminate the MP4 video downloads for all 5 slides across public/ and dist/."""

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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@500;600;700;800&display=swap&subset=latin,latin-ext');

html body #carousel .swiper-slide:nth-child(1) .CarouselSlides_carouselMedia__aqYWx,
html body #carousel .swiper-slide:nth-child(2) .CarouselSlides_carouselMedia__aqYWx,
html body #carousel .swiper-slide:nth-child(3) .CarouselSlides_carouselMedia__aqYWx,
html body #carousel .swiper-slide:nth-child(4) .CarouselSlides_carouselMedia__aqYWx,
html body #carousel .swiper-slide:nth-child(5) .CarouselSlides_carouselMedia__aqYWx {
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

html body #carousel .swiper-slide:nth-child(1) .CarouselSlides_carouselMedia__aqYWx::after,
html body #carousel .swiper-slide:nth-child(2) .CarouselSlides_carouselMedia__aqYWx::after,
html body #carousel .swiper-slide:nth-child(3) .CarouselSlides_carouselMedia__aqYWx::after,
html body #carousel .swiper-slide:nth-child(4) .CarouselSlides_carouselMedia__aqYWx::after,
html body #carousel .swiper-slide:nth-child(5) .CarouselSlides_carouselMedia__aqYWx::after {
  display: none !important;
  content: none !important;
  background: none !important;
  opacity: 0 !important;
}

html body #carousel .swiper-slide:nth-child(1) .CarouselSlides_carouselMedia__aqYWx video,
html body #carousel .swiper-slide:nth-child(2) .CarouselSlides_carouselMedia__aqYWx video,
html body #carousel .swiper-slide:nth-child(3) .CarouselSlides_carouselMedia__aqYWx video,
html body #carousel .swiper-slide:nth-child(4) .CarouselSlides_carouselMedia__aqYWx video,
html body #carousel .swiper-slide:nth-child(5) .CarouselSlides_carouselMedia__aqYWx video {
  display: none !important;
}

html body .roasist-kinetic-3d-canvas,
html body .roasist-creative-bento-canvas,
html body .roasist-process-cockpit-canvas,
html body .roasist-convert-broll-canvas,
html body .roasist-scale-globe-canvas {
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
  // ==========================================================================
  // SLIDE 1: "Önce veri ve strateji" — 3D Z-Axis Kinetic Typography (15 Words)
  // ==========================================================================
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
  const LOOP_DURATION_S1 = 16.0;

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

  const s1Nodes = buildSceneNodes();
  const s1RenderList = new Array(TOTAL_NODES);

  // ==========================================================================
  // SLIDE 2: "Yaratıcı ve cesur fikir" — 3D Creative Bento & Particle Sphere
  // ==========================================================================
  const SPHERE_POINTS = [];
  const NUM_PTS = 340;
  const goldenAngle = Math.PI * (3 - Math.sqrt(5));
  for (let i = 0; i < NUM_PTS; i++) {
    const y = 1 - (i / (NUM_PTS - 1)) * 2;
    const radius = Math.sqrt(1 - y * y);
    const theta = goldenAngle * i;
    SPHERE_POINTS.push({
      x: Math.cos(theta) * radius,
      y: y,
      z: Math.sin(theta) * radius,
      size: (i % 5 === 0) ? 2.2 : 1.35,
      isAccent: (i % 7 === 0)
    });
  }

  function roundRectPath(c, x, y, w, h, r) {
    c.beginPath();
    c.roundRect(x, y, w, h, r);
  }

  function drawPill(c, x, y, text, bg, fg, fontSize = 13, padX = 14, padY = 7) {
    c.save();
    c.font = `600 ${fontSize}px 'Inter', sans-serif`;
    const tw = c.measureText(text).width;
    const pw = tw + padX * 2;
    const ph = fontSize + padY * 2;
    roundRectPath(c, x, y, pw, ph, 999);
    c.fillStyle = bg;
    c.fill();
    c.fillStyle = fg;
    c.textBaseline = 'middle';
    c.textAlign = 'left';
    c.fillText(text, x + padX, y + ph * 0.5 + 0.5);
    c.restore();
    return pw;
  }

  function drawIsoLayer(c, cx, cy, rx, ry, thickness, topGradColors, sideColorLeft, sideColorRight, drawStar = false) {
    c.save();
    c.beginPath();
    c.moveTo(cx - rx, cy);
    c.lineTo(cx, cy + ry);
    c.lineTo(cx, cy + ry + thickness);
    c.lineTo(cx - rx, cy + thickness);
    c.closePath();
    c.fillStyle = sideColorLeft;
    c.fill();

    c.beginPath();
    c.moveTo(cx + rx, cy);
    c.lineTo(cx, cy + ry);
    c.lineTo(cx, cy + ry + thickness);
    c.lineTo(cx + rx, cy + thickness);
    c.closePath();
    c.fillStyle = sideColorRight;
    c.fill();

    c.beginPath();
    c.moveTo(cx, cy - ry);
    c.lineTo(cx + rx, cy);
    c.lineTo(cx, cy + ry);
    c.lineTo(cx - rx, cy);
    c.closePath();
    const g = c.createLinearGradient(cx - rx, cy - ry, cx + rx, cy + ry);
    g.addColorStop(0, topGradColors[0]);
    g.addColorStop(1, topGradColors[1]);
    c.fillStyle = g;
    c.fill();

    c.strokeStyle = 'rgba(255, 255, 255, 0.24)';
    c.lineWidth = 1.2;
    c.stroke();

    if (drawStar) {
      c.save();
      c.translate(cx, cy);
      c.scale(1, 0.58);
      c.strokeStyle = '#FFFFFF';
      c.lineWidth = 2.6;
      c.lineCap = 'round';
      for (let a = 0; a < 4; a++) {
        const ang = (a * Math.PI) / 4;
        const len = (a % 2 === 0) ? 28 : 20;
        c.beginPath();
        c.moveTo(-Math.cos(ang) * len, -Math.sin(ang) * len);
        c.lineTo(Math.cos(ang) * len, Math.sin(ang) * len);
        c.stroke();
      }
      c.beginPath();
      c.arc(0, 0, 4, 0, Math.PI * 2);
      c.fillStyle = '#FFFFFF';
      c.fill();
      c.restore();
    }
    c.restore();
  }

  function renderSlide2Bento(ctx, width, height, dpr, elapsed) {
    const LOOP_SECONDS = 14.0;
    const phase = ((elapsed % LOOP_SECONDS) / LOOP_SECONDS) * Math.PI * 2;

    ctx.save();
    ctx.scale(dpr, dpr);

    ctx.fillStyle = '#0B0914';
    ctx.fillRect(0, 0, width, height);

    const scale = Math.min(width / 1020, height / 788);
    ctx.translate(width * 0.5, height * 0.5);
    ctx.scale(scale, scale);

    const camX = -15 + Math.sin(phase) * 52 + Math.cos(phase * 2) * 14;
    const camY = -65 + Math.cos(phase) * 44 + Math.sin(phase * 2) * 10;
    const zoom = 0.78 + Math.sin(phase) * 0.028;

    ctx.scale(zoom, zoom);
    ctx.rotate(-0.042 + Math.sin(phase) * 0.008);
    ctx.translate(-camX, -camY);

    // 1. ÜST SOL KART
    {
      const x = -740, y = -580, w = 470, h = 250;
      ctx.save();
      roundRectPath(ctx, x, y, w, h, 20);
      const g = ctx.createLinearGradient(x, y, x + w, y + h);
      g.addColorStop(0, '#FB7185');
      g.addColorStop(0.55, '#F43F5E');
      g.addColorStop(1, '#E11D48');
      ctx.fillStyle = g;
      ctx.fill();
      drawPill(ctx, x + w - 130, y + 24, 'Marka Dili', 'rgba(255,255,255,0.22)', '#FFFFFF', 12, 14, 6);
      ctx.fillStyle = 'rgba(255,255,255,0.88)';
      ctx.font = `700 11px 'Inter', sans-serif`;
      ctx.textAlign = 'left';
      ctx.fillText('KREATİF SİSTEM 01', x + 28, y + 40);
      ctx.fillStyle = '#FFFFFF';
      ctx.font = `700 30px 'Inter', sans-serif`;
      if ('letterSpacing' in ctx) ctx.letterSpacing = '-0.025em';
      ctx.fillText('Dönüşüm Odaklı', x + 28, y + 168);
      ctx.fillText('Kreatif Söylem', x + 28, y + 206);
      ctx.restore();
    }

    // 2. ÜST ORTA KART
    {
      const x = -245, y = -580, w = 470, h = 250;
      ctx.save();
      roundRectPath(ctx, x, y, w, h, 20);
      const g = ctx.createRadialGradient(x + w * 0.7, y + h * 0.4, 20, x + w * 0.5, y + h * 0.5, 340);
      g.addColorStop(0, '#0F766E');
      g.addColorStop(0.65, '#062C28');
      g.addColorStop(1, '#041513');
      ctx.fillStyle = g;
      ctx.fill();
      ctx.strokeStyle = 'rgba(94, 234, 212, 0.18)';
      ctx.lineWidth = 1.2;
      ctx.stroke();
      ctx.fillStyle = '#5EEAD4';
      ctx.font = `700 11px 'Inter', sans-serif`;
      ctx.textAlign = 'left';
      ctx.fillText('GÖRSEL KİMLİK MİMARİSİ', x + 28, y + 40);
      ctx.fillStyle = '#FFFFFF';
      ctx.font = `700 25px 'Inter', sans-serif`;
      if ('letterSpacing' in ctx) ctx.letterSpacing = '-0.02em';
      ctx.fillText('İlk 3 Saniyede Dikkat Çeken', x + 28, y + 98);
      ctx.fillText('Kanca Kurgusu', x + 28, y + 132);
      const pw1 = drawPill(ctx, x + 28, y + 190, '+%64 İzlenme', 'rgba(94, 234, 212, 0.16)', '#99F6E4', 12, 14, 6);
      drawPill(ctx, x + 28 + pw1 + 10, y + 190, 'UGC & Motion', 'rgba(255, 255, 255, 0.09)', '#E2E8F0', 12, 14, 6);
      ctx.restore();
    }

    // 3. ÜST SAĞ KART
    {
      const x = 250, y = -580, w = 440, h = 250;
      ctx.save();
      roundRectPath(ctx, x, y, w, h, 20);
      const g = ctx.createLinearGradient(x, y, x + w, y + h);
      g.addColorStop(0, '#1E1B4B');
      g.addColorStop(1, '#0F0D26');
      ctx.fillStyle = g;
      ctx.fill();
      ctx.strokeStyle = 'rgba(167, 139, 250, 0.22)';
      ctx.lineWidth = 1.2;
      ctx.stroke();
      ctx.fillStyle = '#A78BFA';
      ctx.font = `700 11px 'Inter', sans-serif`;
      ctx.textAlign = 'left';
      ctx.fillText('KREATİF PERFORMANS LAB', x + 28, y + 40);
      ctx.fillStyle = '#FFFFFF';
      ctx.font = `700 24px 'Inter', sans-serif`;
      if ('letterSpacing' in ctx) ctx.letterSpacing = '-0.02em';
      ctx.fillText('Yüksek Dönüşümlü', x + 28, y + 92);
      ctx.fillText('Reklam Kreatifleri', x + 28, y + 124);
      const barW = 240;
      const fillRatio = 0.76 + Math.sin(phase * 2) * 0.08;
      roundRectPath(ctx, x + 28, y + 196, barW, 8, 99);
      ctx.fillStyle = 'rgba(255,255,255,0.10)';
      ctx.fill();
      roundRectPath(ctx, x + 28, y + 196, barW * fillRatio, 8, 99);
      ctx.fillStyle = '#A78BFA';
      ctx.fill();
      ctx.fillStyle = '#C4B5FD';
      ctx.font = `600 12px 'Inter', sans-serif`;
      ctx.fillText('CTR Artışı: +2.8x', x + 28, y + 180);
      ctx.restore();
    }

    // 4. ORTA SOL KART
    {
      const x = -740, y = -305, w = 370, h = 460;
      ctx.save();
      roundRectPath(ctx, x, y, w, h, 20);
      const g = ctx.createLinearGradient(x, y, x + w, y + h);
      g.addColorStop(0, '#16132B');
      g.addColorStop(0.5, '#1D1836');
      g.addColorStop(1, '#0D0B18');
      ctx.fillStyle = g;
      ctx.fill();
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.12)';
      ctx.lineWidth = 1.2;
      ctx.stroke();

      ctx.save();
      ctx.beginPath();
      for (let i = 0; i <= 40; i++) {
        const px = x + 28 + (i / 40) * (w - 56);
        const py = y + 170 + Math.sin(i * 0.22 + phase * 2) * 28 - (i * 1.4);
        if (i === 0) ctx.moveTo(px, py);
        else ctx.lineTo(px, py);
      }
      ctx.strokeStyle = '#A78BFA';
      ctx.lineWidth = 3;
      ctx.stroke();
      ctx.restore();

      drawPill(ctx, x + 28, y + 28, 'WEB & KREATİF', 'rgba(167, 139, 250, 0.16)', '#C4B5FD', 11, 12, 5);
      ctx.fillStyle = '#FFFFFF';
      ctx.font = `700 26px 'Inter', sans-serif`;
      ctx.textAlign = 'left';
      if ('letterSpacing' in ctx) ctx.letterSpacing = '-0.02em';
      ctx.fillText('Estetik ve Veriyi', x + 28, y + 320);
      ctx.fillText('Birleştiren Deneyim', x + 28, y + 354);
      ctx.fillStyle = '#94A3B8';
      ctx.font = `500 13px 'Inter', sans-serif`;
      ctx.fillText('Kullanıcı psikolojisine uyumlu', x + 28, y + 392);
      ctx.fillText('görsel hikâye anlatımı.', x + 28, y + 412);
      ctx.restore();
    }

    // 5. MERKEZ ANA SAHNE KARTI
    {
      const x = -345, y = -305, w = 660, h = 460;
      ctx.save();
      roundRectPath(ctx, x, y, w, h, 22);
      const bgGrad = ctx.createRadialGradient(x + w * 0.52, y + h * 0.52, 10, x + w * 0.5, y + h * 0.5, 420);
      bgGrad.addColorStop(0, '#133836');
      bgGrad.addColorStop(0.55, '#0C1D24');
      bgGrad.addColorStop(1, '#080D16');
      ctx.fillStyle = bgGrad;
      ctx.fill();
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.18)';
      ctx.lineWidth = 1.5;
      ctx.stroke();

      ctx.fillStyle = '#FFFFFF';
      ctx.font = `800 15px 'Inter', sans-serif`;
      ctx.textAlign = 'left';
      if ('letterSpacing' in ctx) ctx.letterSpacing = '-0.03em';
      ctx.fillText('ROASİST', x + 28, y + 34);

      ctx.fillStyle = 'rgba(255, 255, 255, 0.72)';
      ctx.font = `500 11.5px 'Inter', sans-serif`;
      if ('letterSpacing' in ctx) ctx.letterSpacing = '0px';
      const navItems = ['Strateji', 'Kreatif Stüdyo', 'Web Deneyimi', 'Performans'];
      let navX = x + 150;
      for (const item of navItems) {
        ctx.fillText(item, navX, y + 33);
        navX += ctx.measureText(item).width + 20;
      }

      drawPill(ctx, x + w - 122, y + 18, 'Projeyi Başlat', '#FFFFFF', '#0B0914', 11, 14, 6);

      const sphereCx = x + w * 0.54;
      const sphereCy = y + h * 0.52;
      const sphereRadius = 148;
      const rotY = elapsed * 0.55;
      const rotX = 0.32 + Math.sin(phase) * 0.12;
      const cosY = Math.cos(rotY), sinY = Math.sin(rotY);
      const cosX = Math.cos(rotX), sinX = Math.sin(rotX);

      for (let i = 0; i < SPHERE_POINTS.length; i++) {
        const p = SPHERE_POINTS[i];
        const x1 = p.x * cosY - p.z * sinY;
        const z1 = p.z * cosY + p.x * sinY;
        const y2 = p.y * cosX - z1 * sinX;
        const z2 = z1 * cosX + p.y * sinX;

        const depthAlpha = 0.15 + 0.75 * ((z2 + 1) * 0.5);
        const sx = sphereCx + x1 * sphereRadius;
        const sy = sphereCy + y2 * sphereRadius;

        ctx.fillStyle = p.isAccent
          ? `rgba(167, 139, 250, ${depthAlpha.toFixed(2)})`
          : `rgba(204, 251, 241, ${(depthAlpha * 0.85).toFixed(2)})`;
        ctx.beginPath();
        ctx.arc(sx, sy, p.size * (0.75 + 0.35 * ((z2 + 1) * 0.5)), 0, Math.PI * 2);
        ctx.fill();
      }

      ctx.fillStyle = '#FFFFFF';
      ctx.font = `700 31px 'Inter', sans-serif`;
      ctx.textAlign = 'center';
      if ('letterSpacing' in ctx) ctx.letterSpacing = '-0.025em';
      ctx.shadowColor = 'rgba(0, 0, 0, 0.55)';
      ctx.shadowBlur = 16;
      ctx.fillText('Stratejiyle Güçlenen', sphereCx, y + 145);
      ctx.fillText('Kreatif Mimari', sphereCx, y + 183);
      ctx.shadowBlur = 0;

      const stackCx = sphereCx;
      const baseStackY = y + 345;
      const floatOffset = Math.sin(phase * 2) * 5;

      drawIsoLayer(ctx, stackCx, baseStackY + 36 - floatOffset * 0.4, 72, 38, 12, ['#8B5CF6', '#6D28D9'], '#5B21B6', '#4C1D95', false);
      drawIsoLayer(ctx, stackCx, baseStackY + 12 - floatOffset * 0.7, 72, 38, 12, ['#3B82F6', '#2563EB'], '#1D4ED8', '#1E40AF', false);
      drawIsoLayer(ctx, stackCx, baseStackY - 12 - floatOffset * 1.0, 72, 38, 12, ['#10B981', '#059669'], '#047857', '#065F46', false);
      drawIsoLayer(ctx, stackCx, baseStackY - 36 - floatOffset * 1.35, 72, 38, 12, ['#F59E0B', '#EA580C'], '#D97706', '#B45309', true);

      const bx = x + 26, by = y + 268, bw = 200, bh = 136;
      roundRectPath(ctx, bx, by, bw, bh, 14);
      ctx.fillStyle = 'rgba(15, 35, 38, 0.76)';
      ctx.fill();
      ctx.strokeStyle = 'rgba(94, 234, 212, 0.22)';
      ctx.lineWidth = 1;
      ctx.stroke();

      ctx.fillStyle = '#5EEAD4';
      ctx.font = `700 9.5px 'Inter', sans-serif`;
      ctx.textAlign = 'left';
      ctx.fillText('KREATİF METODOLOJİ', bx + 16, by + 26);

      ctx.fillStyle = 'rgba(255, 255, 255, 0.88)';
      ctx.font = `500 11.5px 'Inter', sans-serif`;
      ctx.fillText('Veri içgörülerini yüksek', bx + 16, by + 50);
      ctx.fillText('dönüşümlü görsel kimlik ve', bx + 16, by + 68);
      ctx.fillText('reklam kreatiflerine', bx + 16, by + 86);
      ctx.fillText('dönüştürüyoruz.', bx + 16, by + 104);

      roundRectPath(ctx, bx + 16, by + 118, bw - 32, 3, 99);
      ctx.fillStyle = 'rgba(255,255,255,0.14)';
      ctx.fill();
      roundRectPath(ctx, bx + 16, by + 118, (bw - 32) * (0.68 + 0.22 * Math.sin(phase * 2)), 3, 99);
      ctx.fillStyle = '#34D399';
      ctx.fill();

      ctx.restore();
    }

    // 6. ORTA SAĞ KART
    {
      const x = 340, y = -305, w = 350, h = 460;
      ctx.save();
      roundRectPath(ctx, x, y, w, h, 20);
      const g = ctx.createLinearGradient(x, y, x + w, y + h);
      g.addColorStop(0, '#A3E635');
      g.addColorStop(0.55, '#4ADE80');
      g.addColorStop(1, '#22C55E');
      ctx.fillStyle = g;
      ctx.fill();
      ctx.fillStyle = '#052E16';
      ctx.font = `700 11px 'Inter', sans-serif`;
      ctx.textAlign = 'left';
      ctx.fillText('PERFORMANS KREATİFİ', x + 28, y + 42);
      ctx.fillStyle = '#052E16';
      ctx.font = `800 32px 'Inter', sans-serif`;
      if ('letterSpacing' in ctx) ctx.letterSpacing = '-0.03em';
      ctx.fillText('Cesur Fikir.', x + 28, y + 186);
      ctx.fillText('Ölçülebilir', x + 28, y + 224);
      ctx.fillText('Dönüşüm.', x + 28, y + 262);
      ctx.fillStyle = 'rgba(5, 46, 22, 0.82)';
      ctx.font = `500 13px 'Inter', sans-serif`;
      if ('letterSpacing' in ctx) ctx.letterSpacing = '0px';
      ctx.fillText('Estetik tasarımı gerçek kullanıcı', x + 28, y + 304);
      ctx.fillText('psikolojisi ve verisiyle birleştiriyoruz.', x + 28, y + 324);
      ctx.fillStyle = '#052E16';
      ctx.font = `700 12px 'Inter', sans-serif`;
      ctx.fillText('roasist.com / kreatif', x + 28, y + 424);
      ctx.restore();
    }

    // 7. ALT SOL KART
    {
      const x = -740, y = 180, w = 370, h = 250;
      ctx.save();
      roundRectPath(ctx, x, y, w, h, 20);
      const g = ctx.createLinearGradient(x, y, x + w, y + h);
      g.addColorStop(0, '#FBBF24');
      g.addColorStop(1, '#F59E0B');
      ctx.fillStyle = g;
      ctx.fill();
      drawPill(ctx, x + w - 92, y + 22, 'UI / UX', '#FFFFFF', '#0B0914', 11, 14, 5);
      ctx.fillStyle = '#0B0914';
      ctx.font = `800 28px 'Inter', sans-serif`;
      ctx.textAlign = 'left';
      if ('letterSpacing' in ctx) ctx.letterSpacing = '-0.025em';
      ctx.fillText('Akılda Kalan', x + 28, y + 165);
      ctx.fillText('Marka Deneyimi', x + 28, y + 201);
      ctx.restore();
    }

    // 8. ALT ORTA KART
    {
      const x = -345, y = 180, w = 660, h = 250;
      ctx.save();
      roundRectPath(ctx, x, y, w, h, 20);
      const g = ctx.createLinearGradient(x, y, x + w, y + h);
      g.addColorStop(0, '#0F766E');
      g.addColorStop(0.6, '#0D524D');
      g.addColorStop(1, '#082F2C');
      ctx.fillStyle = g;
      ctx.fill();
      ctx.strokeStyle = 'rgba(94, 234, 212, 0.18)';
      ctx.lineWidth = 1.2;
      ctx.stroke();
      ctx.fillStyle = '#99F6E4';
      ctx.font = `700 11px 'Inter', sans-serif`;
      ctx.textAlign = 'left';
      ctx.fillText('HİKÂYE & DÖNÜŞÜM', x + 32, y + 135);
      ctx.fillStyle = '#FFFFFF';
      ctx.font = `700 29px 'Inter', sans-serif`;
      if ('letterSpacing' in ctx) ctx.letterSpacing = '-0.02em';
      ctx.fillText('Markanızın Hikâyesini Satışa', x + 32, y + 174);
      ctx.fillText('Dönüştüren Tasarım Sistemleri', x + 32, y + 210);
      ctx.restore();
    }

    // 9. ALT SAĞ KART
    {
      const x = 340, y = 180, w = 350, h = 250;
      ctx.save();
      roundRectPath(ctx, x, y, w, h, 20);
      const g = ctx.createLinearGradient(x, y, x + w, y + h);
      g.addColorStop(0, '#2E1065');
      g.addColorStop(1, '#170B3B');
      ctx.fillStyle = g;
      ctx.fill();
      ctx.strokeStyle = 'rgba(167, 139, 250, 0.24)';
      ctx.lineWidth = 1.2;
      ctx.stroke();
      drawPill(ctx, x + 28, y + 24, 'META · TIKTOK · YOUTUBE', 'rgba(167, 139, 250, 0.18)', '#DDD6FE', 10.5, 12, 5);
      ctx.fillStyle = '#FFFFFF';
      ctx.font = `700 24px 'Inter', sans-serif`;
      ctx.textAlign = 'left';
      if ('letterSpacing' in ctx) ctx.letterSpacing = '-0.02em';
      ctx.fillText('Çok Kanallı', x + 28, y + 158);
      ctx.fillText('Kreatif Ölçekleme', x + 28, y + 190);
      ctx.restore();
    }

    ctx.restore();

    ctx.save();
    ctx.scale(dpr, dpr);
    const vig = ctx.createRadialGradient(
      width * 0.5, height * 0.5, Math.min(width, height) * 0.35,
      width * 0.5, height * 0.5, Math.max(width, height) * 0.72
    );
    vig.addColorStop(0, 'rgba(11, 9, 20, 0)');
    vig.addColorStop(1, 'rgba(11, 9, 20, 0.55)');
    ctx.fillStyle = vig;
    ctx.fillRect(0, 0, width, height);
    ctx.restore();
  }

  // ==========================================================================
  // SLIDE 3: "Kusursuz süreç yönetimi" — Agile Sprint Kanban & ROAS Cockpit
  // ==========================================================================
  function smoothstepS3(edge0, edge1, x) {
    const t = Math.max(0, Math.min(1, (x - edge0) / (edge1 - edge0)));
    return t * t * (3 - 2 * t);
  }

  function lerpS3(a, b, t) {
    return a + (b - a) * t;
  }

  function drawBadgeS3(c, x, y, text, bg, fg, borderCol, fontSize = 11, padX = 12, padY = 5, dotColor = null) {
    c.save();
    c.font = `600 ${fontSize}px 'Inter', sans-serif`;
    const dotSpace = dotColor ? 14 : 0;
    const tw = c.measureText(text).width + dotSpace;
    const pw = tw + padX * 2;
    const ph = fontSize + padY * 2;
    roundRectPath(c, x, y, pw, ph, 999);
    c.fillStyle = bg;
    c.fill();
    if (borderCol) {
      c.strokeStyle = borderCol;
      c.lineWidth = 1;
      c.stroke();
    }
    if (dotColor) {
      c.beginPath();
      c.arc(x + padX + 4, y + ph * 0.5, 3.8, 0, Math.PI * 2);
      c.fillStyle = dotColor;
      c.shadowColor = dotColor;
      c.shadowBlur = 8;
      c.fill();
      c.shadowBlur = 0;
    }
    c.fillStyle = fg;
    c.textBaseline = 'middle';
    c.textAlign = 'left';
    c.fillText(text, x + padX + dotSpace, y + ph * 0.5 + 0.5);
    c.restore();
    return pw;
  }

  function drawTaskCardS3(c, x, y, w, h, tagText, tagBg, tagFg, rightLabel, rightColor, titleLines, footLeft, footRight, footRightColor, borderColor = 'rgba(255,255,255,0.08)', bgColor = '#131122', glowColor = null) {
    c.save();
    if (glowColor) {
      c.shadowColor = glowColor;
      c.shadowBlur = 24;
    }
    roundRectPath(c, x, y, w, h, 14);
    c.fillStyle = bgColor;
    c.fill();
    c.shadowBlur = 0;
    c.strokeStyle = borderColor;
    c.lineWidth = glowColor ? 1.8 : 1;
    c.stroke();

    c.font = `700 9.5px 'Inter', sans-serif`;
    const tw = c.measureText(tagText).width + 16;
    roundRectPath(c, x + 16, y + 14, tw, 20, 6);
    c.fillStyle = tagBg;
    c.fill();
    c.fillStyle = tagFg;
    c.textAlign = 'left';
    c.textBaseline = 'middle';
    c.fillText(tagText, x + 24, y + 24.5);

    c.fillStyle = rightColor;
    c.font = `600 10.5px 'Inter', sans-serif`;
    c.textAlign = 'right';
    c.fillText(rightLabel, x + w - 16, y + 24.5);

    c.fillStyle = '#FFFFFF';
    c.font = `600 14.5px 'Inter', sans-serif`;
    c.textAlign = 'left';
    if ('letterSpacing' in c) c.letterSpacing = '-0.015em';
    for (let i = 0; i < titleLines.length; i++) {
      c.fillText(titleLines[i], x + 16, y + 56 + i * 20);
    }

    c.fillStyle = '#94A3B8';
    c.font = `500 11px 'Inter', sans-serif`;
    if ('letterSpacing' in c) c.letterSpacing = '0px';
    c.fillText(footLeft, x + 16, y + h - 18);

    c.fillStyle = footRightColor;
    c.font = `700 11px 'Inter', sans-serif`;
    c.textAlign = 'right';
    c.fillText(footRight, x + w - 16, y + h - 18);
    c.restore();
  }

  function drawSprintBoardScene(c, progress, alpha) {
    if (alpha <= 0.005) return;
    c.save();
    c.globalAlpha = alpha;

    const zoom = lerpS3(0.96, 1.01, progress);
    const panX = lerpS3(-12, 12, progress);
    const panY = lerpS3(8, -8, progress);
    c.translate(510 + panX, 394 + panY);
    c.scale(zoom, zoom);
    c.translate(-510, -394);

    const px = 24, py = 22, pw = 972, ph = 744;
    roundRectPath(c, px, py, pw, ph, 22);
    c.fillStyle = '#0E0C1A';
    c.fill();
    c.strokeStyle = 'rgba(167, 139, 250, 0.18)';
    c.lineWidth = 1.4;
    c.stroke();

    c.fillStyle = '#A78BFA';
    c.font = `800 18px 'Inter', sans-serif`;
    c.textAlign = 'left';
    c.textBaseline = 'middle';
    if ('letterSpacing' in c) c.letterSpacing = '-0.03em';
    c.fillText('ROASİST', px + 32, py + 42);

    c.fillStyle = 'rgba(255,255,255,0.14)';
    c.fillRect(px + 124, py + 30, 1, 24);

    c.fillStyle = '#E2E8F0';
    c.font = `500 14.5px 'Inter', sans-serif`;
    if ('letterSpacing' in c) c.letterSpacing = '-0.01em';
    c.fillText('Şeffaf Süreç & Çevik Sprint Yönetimi', px + 140, py + 42);

    drawBadgeS3(
      c, px + pw - 365, py + 28,
      'Canlı Müşteri Paneli Aktif',
      'rgba(16, 185, 129, 0.11)', '#6EE7B7', 'rgba(16, 185, 129, 0.28)',
      11.5, 14, 7, '#10B981'
    );
    drawBadgeS3(
      c, px + pw - 160, py + 28,
      'Sprint #04 · Hafta 6',
      '#7601FF', '#FFFFFF', null,
      11.5, 14, 7, null
    );

    c.fillStyle = 'rgba(255,255,255,0.07)';
    c.fillRect(px + 32, py + 72, pw - 64, 1);

    const tx = px + 32, ty = py + 92, tw = pw - 64, th = 126;
    roundRectPath(c, tx, ty, tw, th, 16);
    c.fillStyle = '#131122';
    c.fill();
    c.strokeStyle = 'rgba(255,255,255,0.08)';
    c.lineWidth = 1;
    c.stroke();

    c.fillStyle = '#94A3B8';
    c.font = `700 11px 'Inter', sans-serif`;
    c.textAlign = 'left';
    c.fillText('PROJE İVME HATTI', tx + 22, ty + 26);

    c.textAlign = 'right';
    c.fillStyle = '#10B981';
    c.font = `600 12px 'Inter', sans-serif`;
    c.fillText('Teslimat Zamanlaması: %100 Planlanan Takvimde', tx + tw - 22, ty + 26);

    const barX = tx + 22, barY = ty + 52, barW = tw - 44, barH = 7;
    roundRectPath(c, barX, barY, barW, barH, 99);
    c.fillStyle = 'rgba(255,255,255,0.08)';
    c.fill();

    const fillProg = lerpS3(0.56, 0.88, smoothstepS3(0.05, 0.85, progress));
    const fillGrad = c.createLinearGradient(barX, 0, barX + barW * fillProg, 0);
    fillGrad.addColorStop(0, '#7601FF');
    fillGrad.addColorStop(1, '#A78BFA');
    roundRectPath(c, barX, barY, barW * fillProg, barH, 99);
    c.fillStyle = fillGrad;
    c.fill();

    const stages = [
      { code: '01 · GÜN 1–7', name: 'Veri & Takip Kurulumu', active: true },
      { code: '02 · HAFTA 2–3', name: 'Kreatif & Huni Üretimi', active: true },
      { code: '03 · HAFTA 4–6', name: 'Hızlı A/B Test & CRO', active: true },
      { code: '04 · SÜREKLİ İVME', name: 'Kârlı Ölçeklendirme', active: fillProg > 0.78 }
    ];
    const colW = (tw - 44) / 4;
    c.textAlign = 'left';
    for (let i = 0; i < 4; i++) {
      const sx = tx + 22 + i * colW;
      c.fillStyle = stages[i].active ? '#A78BFA' : '#64748B';
      c.font = `700 10px 'Inter', sans-serif`;
      c.fillText(stages[i].code, sx, ty + 82);

      c.fillStyle = stages[i].active ? '#FFFFFF' : '#94A3B8';
      c.font = `600 13.5px 'Inter', sans-serif`;
      c.fillText(stages[i].name, sx, ty + 102);
    }

    const ky = ty + th + 20;
    const kh = ph - (ky - py) - 28;
    const kw = (tw - 36) / 3;

    const cols = [
      { title: 'Sıradaki Adımlar', badge: '2 Görev', badgeBg: 'rgba(255,255,255,0.07)', badgeFg: '#94A3B8', border: 'rgba(255,255,255,0.07)', dot: null },
      { title: 'Aktif Sprint #04', badge: 'Devam Eden', badgeBg: 'rgba(118,1,255,0.20)', badgeFg: '#D8B4FE', border: 'rgba(167,139,250,0.28)', dot: '#A78BFA' },
      { title: 'Tamamlandı & Yayında', badge: 'Doğrulandı', badgeBg: 'rgba(16,185,129,0.14)', badgeFg: '#6EE7B7', border: 'rgba(16,185,129,0.24)', dot: '#10B981' }
    ];

    for (let i = 0; i < 3; i++) {
      const cx = tx + i * (kw + 18);
      roundRectPath(c, cx, ky, kw, kh, 18);
      c.fillStyle = '#110F1E';
      c.fill();
      c.strokeStyle = cols[i].border;
      c.lineWidth = 1.2;
      c.stroke();

      let titleX = cx + 18;
      if (cols[i].dot) {
        c.beginPath();
        c.arc(cx + 22, ky + 26, 4, 0, Math.PI * 2);
        c.fillStyle = cols[i].dot;
        c.fill();
        titleX += 14;
      }
      c.fillStyle = '#FFFFFF';
      c.font = `600 13px 'Inter', sans-serif`;
      c.textAlign = 'left';
      c.fillText(cols[i].title, titleX, ky + 26);

      drawBadgeS3(c, cx + kw - 92, ky + 15, cols[i].badge, cols[i].badgeBg, cols[i].badgeFg, null, 10, 10, 4);
    }

    const c1x = tx;
    const c2x = tx + (kw + 18);
    const c3x = tx + 2 * (kw + 18);
    const cardW = kw - 32;
    const cardH = 128;

    drawTaskCardS3(
      c, c1x + 16, ky + 52, cardW, cardH,
      'YENİ PAZAR', 'rgba(118,1,255,0.18)', '#C4B5FD', 'Sprint #05', '#94A3B8',
      ['Almanya & İngiltere Çok Dilli', 'Kampanya Genişlemesi'],
      'Medya Planlama', 'Hazır %85', '#E2E8F0'
    );
    drawTaskCardS3(
      c, c1x + 16, ky + 52 + cardH + 14, cardW, cardH,
      'AEO & SEO', 'rgba(255,255,255,0.08)', '#CBD5E1', 'Sprint #05', '#94A3B8',
      ['Yapay Zeka Arama Görünürlük', '& İçerik Kümeleri'],
      'Organik Büyüme', 'Planlandı', '#E2E8F0'
    );

    roundRectPath(c, c2x + 16, ky + 52, cardW, cardH, 14);
    c.fillStyle = 'rgba(118, 1, 255, 0.04)';
    c.fill();
    c.save();
    c.setLineDash([6, 5]);
    c.strokeStyle = 'rgba(167, 139, 250, 0.28)';
    c.lineWidth = 1.2;
    c.stroke();
    c.restore();
    c.fillStyle = 'rgba(216, 180, 254, 0.45)';
    c.font = `500 12px 'Inter', sans-serif`;
    c.textAlign = 'center';
    c.fillText('Canlı Yayına Aktarıldı', c2x + 16 + cardW * 0.5, ky + 52 + cardH * 0.5);

    drawTaskCardS3(
      c, c2x + 16, ky + 52 + cardH + 14, cardW, cardH,
      'KREATİF TEST', 'rgba(118,1,255,0.18)', '#D8B4FE', 'Canlı Test', '#C4B5FD',
      ['Video Kanca A/B Varyasyonları', '(İlk 3 Saniye Kurgusu)'],
      'Test İlerlemesi', '%78 Tamamlandı', '#A78BFA'
    );

    drawTaskCardS3(
      c, c3x + 16, ky + 52, cardW, cardH,
      'VERİ ALTYAPISI', 'rgba(16,185,129,0.15)', '#6EE7B7', '✓ Aktif', '#6EE7B7',
      ['GA4 + Server-Side GTM &', 'CRM Dönüşüm Eşleşmesi'],
      'Veri Doğruluğu', '%98.4 Eşleşme', '#6EE7B7',
      'rgba(16,185,129,0.24)'
    );

    const destX = c3x + 16;
    const destY = ky + 52 + cardH + 14;
    roundRectPath(c, destX, destY, cardW, cardH, 14);
    c.save();
    c.setLineDash([6, 5]);
    c.strokeStyle = 'rgba(255, 255, 255, 0.10)';
    c.stroke();
    c.restore();

    const moveT = smoothstepS3(0.18, 0.68, progress);
    const startX = c2x + 16;
    const startY = ky + 52;
    const curX = lerpS3(startX, destX, moveT);
    const curY = lerpS3(startY, destY, moveT) - Math.sin(moveT * Math.PI) * 18;
    const isDone = moveT > 0.75;

    drawTaskCardS3(
      c, curX, curY, cardW, cardH,
      'CRO & PERFORMANS',
      isDone ? 'rgba(16,185,129,0.20)' : '#7601FF',
      isDone ? '#6EE7B7' : '#FFFFFF',
      isDone ? '✓ Yayında' : 'Yayına Alınıyor...',
      isDone ? '#6EE7B7' : '#D8B4FE',
      ['Açılış Sayfası Hız & Teklif', 'Kurgusu Optimizasyonu'],
      'Sprint #04',
      '+%38 Dönüşüm Artışı',
      isDone ? '#6EE7B7' : '#FFFFFF',
      isDone ? '#10B981' : '#A78BFA',
      isDone ? '#111F1D' : '#1B1630',
      isDone ? 'rgba(16, 185, 129, 0.35)' : 'rgba(118, 1, 255, 0.42)'
    );

    c.restore();
  }

  function drawMomentumCockpitScene(c, progress, alpha) {
    if (alpha <= 0.005) return;
    c.save();
    c.globalAlpha = alpha;

    const zoom = lerpS3(0.97, 1.01, progress);
    c.translate(510, 394);
    c.scale(zoom, zoom);
    c.translate(-510, -394);

    const px = 24, py = 22, pw = 972, ph = 744;
    roundRectPath(c, px, py, pw, ph, 22);
    c.fillStyle = '#0E0C1A';
    c.fill();
    c.strokeStyle = 'rgba(167, 139, 250, 0.18)';
    c.lineWidth = 1.4;
    c.stroke();

    c.fillStyle = '#A78BFA';
    c.font = `800 18px 'Inter', sans-serif`;
    c.textAlign = 'left';
    c.textBaseline = 'middle';
    if ('letterSpacing' in c) c.letterSpacing = '-0.03em';
    c.fillText('ROASİST', px + 32, py + 42);

    c.fillStyle = 'rgba(255,255,255,0.14)';
    c.fillRect(px + 124, py + 30, 1, 24);

    c.fillStyle = '#E2E8F0';
    c.font = `500 14.5px 'Inter', sans-serif`;
    if ('letterSpacing' in c) c.letterSpacing = '-0.01em';
    c.fillText('Gerçek Zamanlı Performans & İvme Paneli', px + 140, py + 42);

    drawBadgeS3(
      c, px + pw - 365, py + 28,
      'Google Ads · Meta · TikTok · GA4',
      'rgba(255,255,255,0.06)', '#CBD5E1', null,
      11, 14, 7, null
    );
    drawBadgeS3(
      c, px + pw - 138, py + 28,
      'CANLI VERİ',
      'rgba(16, 185, 129, 0.12)', '#6EE7B7', 'rgba(16, 185, 129, 0.30)',
      11, 14, 7, '#10B981'
    );

    const curveT = smoothstepS3(0.06, 0.78, progress);
    const currentRoas = lerpS3(2.5, 6.4, curveT);
    const currentCpa = Math.round(lerpS3(12, 38, curveT));

    const kpiY = py + 82;
    const kpiH = 118;
    const kpiW = (pw - 64 - 32) / 3;

    {
      const kx = px + 32;
      roundRectPath(c, kx, kpiY, kpiW, kpiH, 16);
      const g = c.createLinearGradient(kx, kpiY, kx, kpiY + kpiH);
      g.addColorStop(0, '#1A1430');
      g.addColorStop(1, '#121020');
      c.fillStyle = g;
      c.fill();
      c.strokeStyle = 'rgba(167, 139, 250, 0.35)';
      c.lineWidth = 1.2;
      c.stroke();

      c.fillStyle = '#A1A1AA';
      c.font = `600 10.5px 'Inter', sans-serif`;
      c.textAlign = 'left';
      c.fillText('BİRLEŞİK KÂRLILIK (ROAS)', kx + 20, kpiY + 28);

      c.fillStyle = '#FFFFFF';
      c.font = `800 38px 'Inter', sans-serif`;
      if ('letterSpacing' in c) c.letterSpacing = '-0.03em';
      c.fillText(`${currentRoas.toFixed(1)}x`, kx + 20, kpiY + 76);

      drawBadgeS3(c, kx + 125, kpiY + 62, '+106% İvme', 'rgba(118, 1, 255, 0.26)', '#D8B4FE', null, 11, 10, 4);
    }

    {
      const kx = px + 32 + kpiW + 16;
      roundRectPath(c, kx, kpiY, kpiW, kpiH, 16);
      c.fillStyle = '#131122';
      c.fill();
      c.strokeStyle = 'rgba(255, 255, 255, 0.08)';
      c.lineWidth = 1;
      c.stroke();

      c.fillStyle = '#A1A1AA';
      c.font = `600 10.5px 'Inter', sans-serif`;
      c.textAlign = 'left';
      c.fillText('EDİNME MALİYETİ (CPA)', kx + 20, kpiY + 28);

      c.fillStyle = '#FFFFFF';
      c.font = `800 38px 'Inter', sans-serif`;
      if ('letterSpacing' in c) c.letterSpacing = '-0.03em';
      c.fillText(`-%${currentCpa}`, kx + 20, kpiY + 76);

      drawBadgeS3(c, kx + 135, kpiY + 62, 'Optimize', 'rgba(16, 185, 129, 0.16)', '#6EE7B7', null, 11, 10, 4);
    }

    {
      const kx = px + 32 + (kpiW + 16) * 2;
      roundRectPath(c, kx, kpiY, kpiW, kpiH, 16);
      c.fillStyle = '#131122';
      c.fill();
      c.strokeStyle = 'rgba(255, 255, 255, 0.08)';
      c.lineWidth = 1;
      c.stroke();

      c.fillStyle = '#A1A1AA';
      c.font = `600 10.5px 'Inter', sans-serif`;
      c.textAlign = 'left';
      c.fillText('SPRINT TESLİMAT HIZI', kx + 20, kpiY + 28);

      c.fillStyle = '#FFFFFF';
      c.font = `800 38px 'Inter', sans-serif`;
      if ('letterSpacing' in c) c.letterSpacing = '-0.03em';
      c.fillText('%98.2', kx + 20, kpiY + 76);

      c.fillStyle = '#94A3B8';
      c.font = `500 11.5px 'Inter', sans-serif`;
      if ('letterSpacing' in c) c.letterSpacing = '0px';
      c.fillText('Haftalık Hedef', kx + 148, kpiY + 78);
    }

    const cx = px + 32, cy = kpiY + kpiH + 20, cw = pw - 64, ch = ph - (cy - py) - 28;
    roundRectPath(c, cx, cy, cw, ch, 18);
    c.fillStyle = '#110F1E';
    c.fill();
    c.strokeStyle = 'rgba(255, 255, 255, 0.08)';
    c.lineWidth = 1;
    c.stroke();

    c.fillStyle = '#FFFFFF';
    c.font = `700 16px 'Inter', sans-serif`;
    c.textAlign = 'left';
    c.fillText('Sprint Bazlı Büyüme & ROAS İvmesi', cx + 24, cy + 32);

    c.fillStyle = '#94A3B8';
    c.font = `500 12px 'Inter', sans-serif`;
    c.fillText('Her iki haftalık sprint sonunda doğrulanan kümülatif reklam verimliliği', cx + 24, cy + 52);

    c.fillStyle = '#7601FF';
    roundRectPath(c, cx + cw - 260, cy + 28, 10, 10, 3);
    c.fill();
    c.fillStyle = '#CBD5E1';
    c.font = `500 11.5px 'Inter', sans-serif`;
    c.fillText('Gerçekleşen ROAS', cx + cw - 244, cy + 33.5);

    c.fillStyle = '#475569';
    c.fillRect(cx + cw - 120, cy + 32, 10, 2);
    c.fillStyle = '#94A3B8';
    c.fillText('Başlangıç Bazı', cx + cw - 104, cy + 33.5);

    const plotX0 = cx + 68, plotX1 = cx + cw - 36;
    const plotY0 = cy + 96, plotY1 = cy + ch - 58;
    const yLabels = ['7.0x', '5.5x', '4.0x', '2.5x'];

    for (let i = 0; i < 4; i++) {
      const gy = lerpS3(plotY0, plotY1, i / 3);
      c.fillStyle = '#64748B';
      c.font = `500 11px 'Inter', sans-serif`;
      c.textAlign = 'left';
      c.fillText(yLabels[i], cx + 24, gy);

      c.beginPath();
      c.moveTo(plotX0, gy);
      c.lineTo(plotX1, gy);
      c.strokeStyle = (i === 3) ? 'rgba(148, 163, 184, 0.22)' : 'rgba(255, 255, 255, 0.05)';
      c.lineWidth = 1;
      c.stroke();
    }

    const sprints = [
      'Sprint 01 · Kurulum',
      'Sprint 02 · Kreatif',
      'Sprint 03 · CRO',
      'Sprint 04 · Ölçek',
      'Sprint 05 · Otomasyon',
      'Sprint 06 · 6.4x ROAS'
    ];
    const pts = [];
    const roasValues = [2.5, 3.2, 4.1, 5.0, 5.8, 6.4];

    for (let i = 0; i < 6; i++) {
      const sx = lerpS3(plotX0, plotX1, i / 5);
      const normVal = (roasValues[i] - 2.5) / (7.0 - 2.5);
      const sy = lerpS3(plotY1, plotY0, normVal);
      pts.push({ x: sx, y: sy, val: roasValues[i] });

      c.fillStyle = (i === 5) ? '#D8B4FE' : '#94A3B8';
      c.font = `600 11px 'Inter', sans-serif`;
      c.textAlign = 'center';
      c.fillText(sprints[i], sx, cy + ch - 24);
    }

    const totalSegs = 5;
    const activeFloat = curveT * totalSegs;
    const activeIdx = Math.min(totalSegs - 1, Math.floor(activeFloat));
    const segFrac = activeFloat - activeIdx;

    const tipX = lerpS3(pts[activeIdx].x, pts[activeIdx + 1].x, segFrac);
    const tipY = lerpS3(pts[activeIdx].y, pts[activeIdx + 1].y, segFrac);

    c.save();
    c.beginPath();
    c.moveTo(pts[0].x, plotY1);
    for (let i = 0; i <= activeIdx; i++) {
      c.lineTo(pts[i].x, pts[i].y);
    }
    c.lineTo(tipX, tipY);
    c.lineTo(tipX, plotY1);
    c.closePath();
    const areaGrad = c.createLinearGradient(0, plotY0, 0, plotY1);
    areaGrad.addColorStop(0, 'rgba(118, 1, 255, 0.34)');
    areaGrad.addColorStop(1, 'rgba(118, 1, 255, 0.0)');
    c.fillStyle = areaGrad;
    c.fill();
    c.restore();

    c.save();
    c.beginPath();
    c.moveTo(pts[0].x, pts[0].y);
    for (let i = 1; i <= activeIdx; i++) {
      c.lineTo(pts[i].x, pts[i].y);
    }
    c.lineTo(tipX, tipY);
    c.strokeStyle = '#9333EA';
    c.lineWidth = 3.5;
    c.shadowColor = '#7601FF';
    c.shadowBlur = 16;
    c.stroke();
    c.restore();

    for (let i = 0; i <= activeIdx; i++) {
      c.beginPath();
      c.arc(pts[i].x, pts[i].y, 4.5, 0, Math.PI * 2);
      c.fillStyle = '#FFFFFF';
      c.fill();
      c.strokeStyle = '#7601FF';
      c.lineWidth = 2;
      c.stroke();
    }

    c.save();
    c.beginPath();
    c.arc(tipX, tipY, 6, 0, Math.PI * 2);
    c.fillStyle = '#FFFFFF';
    c.shadowColor = '#10B981';
    c.shadowBlur = 14;
    c.fill();
    c.strokeStyle = '#10B981';
    c.lineWidth = 2.5;
    c.stroke();
    c.restore();

    const badgeW = 190, badgeH = 64;
    const bx = Math.min(plotX1 - badgeW, Math.max(plotX0, tipX - badgeW * 0.75));
    const by = tipY - badgeH - 18;
    c.save();
    c.shadowColor = 'rgba(118, 1, 255, 0.45)';
    c.shadowBlur = 24;
    roundRectPath(c, bx, by, badgeW, badgeH, 14);
    c.fillStyle = '#7601FF';
    c.fill();
    c.shadowBlur = 0;
    c.strokeStyle = 'rgba(255, 255, 255, 0.35)';
    c.lineWidth = 1.2;
    c.stroke();

    c.fillStyle = 'rgba(255, 255, 255, 0.85)';
    c.font = `700 9.5px 'Inter', sans-serif`;
    c.textAlign = 'left';
    c.fillText('CANLI İVME', bx + 14, by + 20);

    c.fillStyle = '#FFFFFF';
    c.font = `800 19px 'Inter', sans-serif`;
    c.fillText(`${currentRoas.toFixed(1)}x ROAS`, bx + 14, by + 44);

    drawBadgeS3(c, bx + badgeW - 64, by + 22, '+106%', 'rgba(255,255,255,0.18)', '#FFFFFF', null, 11, 8, 4);
    c.restore();

    c.restore();
  }

  function renderSlide3ProcessCockpit(ctx, width, height, dpr, elapsed) {
    const CYCLE_SECONDS = 12.0;
    const cycleTime = elapsed % CYCLE_SECONDS;

    ctx.save();
    ctx.scale(dpr, dpr);

    ctx.fillStyle = '#0B0914';
    ctx.fillRect(0, 0, width, height);

    const scale = Math.min(width / 1020, height / 788);
    ctx.translate((width - 1020 * scale) * 0.5, (height - 788 * scale) * 0.5);
    ctx.scale(scale, scale);

    let alphaA = 0, alphaB = 0;
    const fadeDur = 0.85;
    if (cycleTime < 6.0 - fadeDur) {
      alphaA = cycleTime < fadeDur ? smoothstepS3(0, fadeDur, cycleTime) : 1;
      alphaB = cycleTime < fadeDur ? 1 - alphaA : 0;
    } else if (cycleTime < 6.0) {
      const t = (cycleTime - (6.0 - fadeDur)) / fadeDur;
      alphaA = 1 - smoothstepS3(0, 1, t);
      alphaB = smoothstepS3(0, 1, t);
    } else if (cycleTime < 12.0 - fadeDur) {
      alphaA = 0;
      alphaB = 1;
    } else {
      const t = (cycleTime - (12.0 - fadeDur)) / fadeDur;
      alphaB = 1 - smoothstepS3(0, 1, t);
      alphaA = smoothstepS3(0, 1, t);
    }

    const progA = Math.min(1, cycleTime / 6.0);
    const progB = cycleTime >= 6.0 ? Math.min(1, (cycleTime - 6.0) / 6.0) : 1.0;

    drawSprintBoardScene(ctx, progA, alphaA);
    drawMomentumCockpitScene(ctx, progB, alphaB);

    ctx.restore();
  }

  // ==========================================================================
  // SLIDE 4: "Dönüşüm için tasarla" — 3D Exploded Isometric Web & UX Anatomy
  // ==========================================================================
  function clamp01S4(x) {
    return Math.max(0, Math.min(1, x));
  }

  function easeOutQuintS4(x) {
    const t = clamp01S4(x);
    return 1 - Math.pow(1 - t, 4.2);
  }

  function easeInOutCubicS4(x) {
    const t = clamp01S4(x);
    return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
  }

  function projectPointS4(u, v, z, cam) {
    const x1 = u * cam.cosYaw - v * cam.sinYaw;
    const y1 = u * cam.sinYaw + v * cam.cosYaw;
    return {
      x: cam.cx + cam.scale * x1,
      y: cam.cy - cam.scale * cam.sinPitch * z + cam.scale * cam.cosPitch * y1
    };
  }

  function applyPlaneTransformS4(c, z, cam) {
    const a = cam.scale * cam.cosYaw;
    const b = cam.scale * cam.cosPitch * cam.sinYaw;
    const cc = -cam.scale * cam.sinYaw;
    const d = cam.scale * cam.cosPitch * cam.cosYaw;
    const e = cam.cx;
    const f = cam.cy - cam.scale * cam.sinPitch * z;
    c.transform(a, b, cc, d, e, f);
  }

  function drawExtrudedSlabS4(c, W, H, r, z, thickness, cam, topFill, rimStroke, sideFill, shadowAlpha = 0) {
    const hw = W * 0.5;
    const hh = H * 0.5;

    if (shadowAlpha > 0.005) {
      c.save();
      applyPlaneTransformS4(c, z - thickness - 6, cam);
      roundRectPath(c, -hw + 6, -hh + 10, W, H, r);
      c.fillStyle = `rgba(4, 3, 9, ${shadowAlpha.toFixed(3)})`;
      c.shadowColor = `rgba(0, 0, 0, ${(shadowAlpha * 0.9).toFixed(3)})`;
      c.shadowBlur = 32;
      c.fill();
      c.restore();
    }

    const steps = Math.max(2, Math.ceil(thickness));
    for (let s = steps; s >= 1; s--) {
      const zs = z - (s / steps) * thickness;
      c.save();
      applyPlaneTransformS4(c, zs, cam);
      roundRectPath(c, -hw, -hh, W, H, r);
      c.fillStyle = sideFill;
      c.fill();
      c.restore();
    }

    c.save();
    applyPlaneTransformS4(c, z, cam);
    roundRectPath(c, -hw, -hh, W, H, r);
    c.fillStyle = topFill;
    c.fill();
    if (rimStroke) {
      c.strokeStyle = rimStroke;
      c.lineWidth = 1.4;
      c.stroke();
    }
    c.restore();
  }

  function drawCursor2DS4(c, x, y, scale = 1, isClicking = false) {
    c.save();
    c.translate(x, y);
    c.scale(scale, scale);

    if (isClicking) {
      c.beginPath();
      c.arc(0, 0, 18, 0, Math.PI * 2);
      c.strokeStyle = 'rgba(118, 1, 255, 0.55)';
      c.lineWidth = 2;
      c.stroke();
    }

    c.shadowColor = 'rgba(15, 23, 42, 0.45)';
    c.shadowBlur = 10;
    c.beginPath();
    c.moveTo(0, 0);
    c.lineTo(0, 19);
    c.lineTo(5.2, 14.8);
    c.lineTo(9.5, 22.5);
    c.lineTo(13, 20.8);
    c.lineTo(8.6, 13);
    c.lineTo(15.5, 13);
    c.closePath();
    c.fillStyle = '#0F172A';
    c.fill();
    c.strokeStyle = '#FFFFFF';
    c.lineWidth = 1.5;
    c.stroke();
    c.restore();
  }

  function drawCheckIconS3(c, x, y, size, color) {
    c.save();
    c.strokeStyle = color;
    c.lineWidth = 1.8;
    c.lineCap = 'round';
    c.lineJoin = 'round';
    c.beginPath();
    c.moveTo(x - size * 0.45, y + size * 0.02);
    c.lineTo(x - size * 0.12, y + size * 0.36);
    c.lineTo(x + size * 0.48, y - size * 0.32);
    c.stroke();
    c.restore();
  }

  function drawLayer1TechnicalSEOS4(c, W, H, z1, cam, explode, elapsed) {
    if (explode <= 0.01) return;

    const alpha = smoothstepS3(0.01, 0.22, explode);
    c.save();
    c.globalAlpha = alpha;

    const hw = W * 0.5;
    const hh = H * 0.5;

    drawExtrudedSlabS4(
      c, W, H, 16, z1, 7, cam,
      '#0E1526',
      'rgba(148, 163, 184, 0.38)',
      '#070B14',
      0.65 * alpha
    );

    c.save();
    applyPlaneTransformS4(c, z1, cam);

    roundRectPath(c, -hw, -hh, W, H, 16);
    c.clip();

    c.strokeStyle = 'rgba(148, 163, 184, 0.08)';
    c.lineWidth = 1;
    for (let gx = -hw; gx <= hw; gx += 24) {
      c.beginPath();
      c.moveTo(gx, -hh);
      c.lineTo(gx, hh);
      c.stroke();
    }
    for (let gy = -hh; gy <= hh; gy += 24) {
      c.beginPath();
      c.moveTo(-hw, gy);
      c.lineTo(hw, gy);
      c.stroke();
    }

    const pad = 22;
    const ix = -hw + pad;
    const iy = -hh + pad;
    const iw = W - pad * 2;

    roundRectPath(c, ix, iy, iw, 36, 8);
    c.fillStyle = 'rgba(15, 23, 42, 0.85)';
    c.fill();
    c.strokeStyle = 'rgba(148, 163, 184, 0.28)';
    c.lineWidth = 1;
    c.stroke();

    c.fillStyle = '#94A3B8';
    c.font = "600 10.5px 'Inter', sans-serif";
    c.textAlign = 'left';
    c.textBaseline = 'middle';
    c.fillText('<header> · CANONICAL & HREFLANG MİMARİSİ', ix + 14, iy + 18);

    c.fillStyle = '#10B981';
    c.textAlign = 'right';
    c.fillText('TTFB: 0.08s · HTTP/3', ix + iw - 14, iy + 18);

    const leftW = 314;
    const bodyY = iy + 48;
    const bodyH = H - pad * 2 - 48;

    roundRectPath(c, ix, bodyY, leftW, bodyH, 10);
    c.fillStyle = 'rgba(15, 23, 42, 0.72)';
    c.fill();
    c.strokeStyle = 'rgba(167, 139, 250, 0.30)';
    c.setLineDash([5, 4]);
    c.stroke();
    c.setLineDash([]);

    c.fillStyle = '#A78BFA';
    c.font = "700 10px 'Inter', sans-serif";
    c.textAlign = 'left';
    c.fillText('<h1> SEMANTİK İSKELET & JSON-LD SCHEMA', ix + 16, bodyY + 22);

    const nodes = [
      { x: ix + 56, y: bodyY + 68, label: '@Organization' },
      { x: ix + 158, y: bodyY + 54, label: '@Product / Offer' },
      { x: ix + 158, y: bodyY + 92, label: '@AggregateRating' },
      { x: ix + 258, y: bodyY + 72, label: 'SERP & AEO' }
    ];

    const edges = [[0, 1], [0, 2], [1, 3], [2, 3]];
    c.strokeStyle = 'rgba(167, 139, 250, 0.38)';
    c.lineWidth = 1.3;
    edges.forEach(([a, b]) => {
      c.beginPath();
      c.moveTo(nodes[a].x, nodes[a].y);
      c.lineTo(nodes[b].x, nodes[b].y);
      c.stroke();
    });

    const pulseU = (elapsed * 0.65) % 1;
    edges.forEach(([a, b], idx) => {
      const localU = (pulseU + idx * 0.25) % 1;
      const px = lerpS3(nodes[a].x, nodes[b].x, localU);
      const py = lerpS3(nodes[a].y, nodes[b].y, localU);
      c.beginPath();
      c.arc(px, py, 2.8, 0, Math.PI * 2);
      c.fillStyle = '#A78BFA';
      c.fill();
    });

    nodes.forEach((n, idx) => {
      const nw = 84, nh = 24;
      roundRectPath(c, n.x - nw * 0.5, n.y - nh * 0.5, nw, nh, 6);
      c.fillStyle = idx === 3 ? 'rgba(16, 185, 129, 0.16)' : '#1E293B';
      c.fill();
      c.strokeStyle = idx === 3 ? 'rgba(16, 185, 129, 0.55)' : 'rgba(148, 163, 184, 0.35)';
      c.lineWidth = 1;
      c.stroke();

      c.fillStyle = idx === 3 ? '#6EE7B7' : '#E2E8F0';
      c.font = "600 9px 'Inter', sans-serif";
      c.textAlign = 'center';
      c.fillText(n.label, n.x, n.y + 0.5);
    });

    const specs = [
      { code: 'LCP (Largest Contentful Paint)', val: '0.4s' },
      { code: 'CLS (Görsel Sıfır Zıplama)', val: '0.00' },
      { code: 'Arama & AI Tarama Bütçesi', val: '%100' }
    ];
    specs.forEach((sp, i) => {
      const sy = bodyY + 132 + i * 38;
      roundRectPath(c, ix + 14, sy, leftW - 28, 30, 6);
      c.fillStyle = 'rgba(30, 41, 59, 0.65)';
      c.fill();

      c.fillStyle = '#CBD5E1';
      c.font = "500 10px 'Inter', sans-serif";
      c.textAlign = 'left';
      c.fillText(sp.code, ix + 24, sy + 15);

      c.fillStyle = '#10B981';
      c.font = "700 10.5px 'Inter', sans-serif";
      c.textAlign = 'right';
      c.fillText(sp.val, ix + leftW - 24, sy + 15);
    });

    const rx = ix + leftW + 14;
    const rw = iw - leftW - 14;
    roundRectPath(c, rx, bodyY, rw, bodyH, 10);
    c.fillStyle = 'rgba(15, 23, 42, 0.78)';
    c.fill();
    c.strokeStyle = 'rgba(16, 185, 129, 0.35)';
    c.lineWidth = 1;
    c.stroke();

    c.fillStyle = '#94A3B8';
    c.font = "700 10px 'Inter', sans-serif";
    c.textAlign = 'center';
    c.fillText('CORE WEB VITALS', rx + rw * 0.5, bodyY + 24);

    const gx = rx + rw * 0.5;
    const gy = bodyY + 106;
    const gr = 50;
    c.beginPath();
    c.arc(gx, gy, gr, 0, Math.PI * 2);
    c.strokeStyle = 'rgba(148, 163, 184, 0.16)';
    c.lineWidth = 6;
    c.stroke();

    c.beginPath();
    c.arc(gx, gy, gr, -Math.PI * 0.5, -Math.PI * 0.5 + Math.PI * 2 * smoothstepS3(0.05, 0.6, explode));
    c.strokeStyle = '#10B981';
    c.lineWidth = 6;
    c.lineCap = 'round';
    c.stroke();

    c.fillStyle = '#FFFFFF';
    c.font = "800 26px 'Inter', sans-serif";
    c.textAlign = 'center';
    if ('letterSpacing' in c) c.letterSpacing = '-0.03em';
    c.fillText('100', gx, gy - 2);

    c.fillStyle = '#10B981';
    c.font = "600 9px 'Inter', sans-serif";
    if ('letterSpacing' in c) c.letterSpacing = '0px';
    c.fillText('PERFORMANS', gx, gy + 17);

    roundRectPath(c, rx + 14, bodyY + 182, rw - 28, 56, 8);
    c.fillStyle = 'rgba(30, 41, 59, 0.72)';
    c.fill();
    c.fillStyle = '#94A3B8';
    c.font = "500 9.5px 'Inter', sans-serif";
    c.fillText('ORGANİK & AEO GÖRÜNÜRLÜK', rx + rw * 0.5, bodyY + 201);
    c.fillStyle = '#FFFFFF';
    c.font = "800 15.5px 'Inter', sans-serif";
    c.fillText('+214% Trafik Kalitesi', rx + rw * 0.5, bodyY + 223);

    c.restore();
    c.restore();
  }

  function drawLayer2UXWireframeS4(c, W, H, z2, cam, explode, elapsed) {
    if (explode <= 0.01) return;

    const alpha = smoothstepS3(0.01, 0.22, explode);
    c.save();
    c.globalAlpha = alpha;

    const hw = W * 0.5;
    const hh = H * 0.5;

    drawExtrudedSlabS4(
      c, W, H, 16, z2, 6, cam,
      'rgba(30, 27, 54, 0.76)',
      'rgba(167, 139, 250, 0.48)',
      'rgba(18, 16, 34, 0.88)',
      0.48 * alpha
    );

    c.save();
    applyPlaneTransformS4(c, z2, cam);

    roundRectPath(c, -hw, -hh, W, H, 16);
    c.clip();

    const pad = 22;
    const ix = -hw + pad;
    const iy = -hh + pad;
    const iw = W - pad * 2;
    const ih = H - pad * 2;
    const cols = 12;
    const gap = 8;
    const colW = (iw - gap * (cols - 1)) / cols;

    for (let i = 0; i < cols; i++) {
      const cx = ix + i * (colW + gap);
      c.fillStyle = 'rgba(167, 139, 250, 0.048)';
      c.fillRect(cx, iy, colW, ih);
    }

    roundRectPath(c, ix, iy, iw, 34, 8);
    c.strokeStyle = 'rgba(226, 232, 240, 0.30)';
    c.lineWidth = 1.2;
    c.stroke();

    c.fillStyle = '#E2E8F0';
    c.font = "600 10px 'Inter', sans-serif";
    c.textAlign = 'left';
    c.textBaseline = 'middle';
    c.fillText('UX NAVİGASYON · 12 SÜTUN SWISS GRID', ix + 14, iy + 17);

    c.fillStyle = '#A78BFA';
    c.textAlign = 'right';
    c.fillText('SÜRTÜNMESİZ AKIŞ (0.0s GECİKME)', ix + iw - 14, iy + 17);

    const bodyY = iy + 46;
    const bodyH = ih - 46;
    const leftW = 314;

    roundRectPath(c, ix, bodyY, leftW, bodyH, 10);
    c.fillStyle = 'rgba(15, 23, 42, 0.55)';
    c.fill();
    c.strokeStyle = 'rgba(226, 232, 240, 0.25)';
    c.stroke();

    c.fillStyle = 'rgba(167, 139, 250, 0.22)';
    roundRectPath(c, ix + 16, bodyY + 16, 128, 14, 4);
    c.fill();

    c.fillStyle = '#CBD5E1';
    c.font = "700 10.5px 'Inter', sans-serif";
    c.textAlign = 'left';
    c.fillText('ODAK 01 · DEĞER ÖNERİSİ & BAŞLIK HİYERARŞİSİ', ix + 16, bodyY + 48);

    roundRectPath(c, ix + 16, bodyY + 64, 260, 18, 5);
    c.fillStyle = 'rgba(255, 255, 255, 0.18)';
    c.fill();
    roundRectPath(c, ix + 16, bodyY + 88, 215, 18, 5);
    c.fill();

    roundRectPath(c, ix + 16, bodyY + 122, leftW - 32, 116, 8);
    c.fillStyle = 'rgba(118, 1, 255, 0.15)';
    c.fill();
    c.strokeStyle = 'rgba(167, 139, 250, 0.45)';
    c.setLineDash([4, 4]);
    c.stroke();
    c.setLineDash([]);

    c.fillStyle = '#E2E8F0';
    c.font = "600 10.5px 'Inter', sans-serif";
    c.textAlign = 'center';
    c.fillText('ODAK 02 · GÖRSEL KANCA & GÜVEN ALANI', ix + leftW * 0.5, bodyY + 170);
    c.fillStyle = '#A78BFA';
    c.font = "500 9.5px 'Inter', sans-serif";
    c.fillText('Göz Takibi (Eye-Tracking) Dikkat Oranı: %94', ix + leftW * 0.5, bodyY + 190);

    const rx = ix + leftW + 14;
    const rw = iw - leftW - 14;
    roundRectPath(c, rx, bodyY, rw, bodyH, 10);
    c.fillStyle = 'rgba(15, 23, 42, 0.62)';
    c.fill();
    c.strokeStyle = 'rgba(167, 139, 250, 0.45)';
    c.stroke();

    c.fillStyle = '#E2E8F0';
    c.font = "700 10.5px 'Inter', sans-serif";
    c.textAlign = 'left';
    c.fillText('ODAK 03 · TEK ADIM DÖNÜŞÜM', rx + 16, bodyY + 24);

    const steps = [
      '1. Mikro-Kopya & Güven Doğrulaması',
      '2. Sıfır Sürtünmeli Seçim Alanı',
      '3. Tek Birincil CTA Odak Noktası'
    ];
    steps.forEach((st, i) => {
      const sy = bodyY + 46 + i * 47;
      roundRectPath(c, rx + 14, sy, rw - 28, 37, 7);
      c.fillStyle = 'rgba(255, 255, 255, 0.07)';
      c.fill();
      c.strokeStyle = 'rgba(255, 255, 255, 0.16)';
      c.stroke();

      c.fillStyle = '#E2E8F0';
      c.font = "500 9.5px 'Inter', sans-serif";
      c.textAlign = 'left';
      c.fillText(st, rx + 22, sy + 18.5);
    });

    roundRectPath(c, rx + 14, bodyY + 192, rw - 28, 44, 9);
    c.fillStyle = 'rgba(118, 1, 255, 0.30)';
    c.fill();
    c.strokeStyle = '#A78BFA';
    c.lineWidth = 1.5;
    c.stroke();

    c.fillStyle = '#FFFFFF';
    c.font = "700 10.5px 'Inter', sans-serif";
    c.textAlign = 'center';
    c.fillText('HEDEF AKSİYON (CTA) KİLİDİ', rx + rw * 0.5, bodyY + 214);

    const p0 = { x: ix + 140, y: bodyY + 74 };
    const p1 = { x: ix + 160, y: bodyY + 180 };
    const p2 = { x: rx + rw * 0.5, y: bodyY + 214 };

    c.beginPath();
    c.moveTo(p0.x, p0.y);
    c.quadraticCurveTo(p1.x, p1.y, p2.x, p2.y);
    c.strokeStyle = 'rgba(167, 139, 250, 0.65)';
    c.lineWidth = 2;
    c.setLineDash([6, 4]);
    c.stroke();
    c.setLineDash([]);

    const flowT = (elapsed * 0.55) % 1;
    const qx = (1 - flowT) * (1 - flowT) * p0.x + 2 * (1 - flowT) * flowT * p1.x + flowT * flowT * p2.x;
    const qy = (1 - flowT) * (1 - flowT) * p0.y + 2 * (1 - flowT) * flowT * p1.y + flowT * flowT * p2.y;

    c.beginPath();
    c.arc(qx, qy, 5, 0, Math.PI * 2);
    c.fillStyle = '#FFFFFF';
    c.shadowColor = '#A78BFA';
    c.shadowBlur = 10;
    c.fill();
    c.shadowBlur = 0;

    c.restore();
    c.restore();
  }

  function drawLayer3FinishedUIS4(c, W, H, z3, cam, explode, clickProgress, roasVal, cvrVal) {
    const hw = W * 0.5;
    const hh = H * 0.5;
    const pad = 24;
    const leftX = -hw + pad;
    const bodyY = -hh + 64;
    const leftW = 308;
    const vcY = bodyY + 134;
    const vcH = 156;
    const rx = leftX + leftW + 18;
    const rw = W - pad * 2 - leftW - 18;
    const rh = 290;

    drawExtrudedSlabS4(
      c, W, H, 16, z3, 8, cam,
      '#F8FAFC',
      'rgba(255, 255, 255, 0.95)',
      '#CBD5E1',
      lerpS3(0.65, 0.42, explode)
    );

    c.save();
    applyPlaneTransformS4(c, z3, cam);

    roundRectPath(c, -hw, -hh, W, H, 16);
    c.clip();

    c.fillStyle = '#FFFFFF';
    c.fillRect(-hw, -hh, W, 46);
    c.fillStyle = 'rgba(15, 23, 42, 0.08)';
    c.fillRect(-hw, -hh + 46, W, 1);

    for (let i = 0; i < 3; i++) {
      c.beginPath();
      c.arc(-hw + 22 + i * 13, -hh + 23, 3.8, 0, Math.PI * 2);
      c.fillStyle = i === 0 ? '#94A3B8' : '#CBD5E1';
      c.fill();
    }

    c.fillStyle = '#0F172A';
    c.font = "800 12.5px 'Inter', sans-serif";
    c.textAlign = 'left';
    c.textBaseline = 'middle';
    if ('letterSpacing' in c) c.letterSpacing = '-0.03em';
    c.fillText('ROASİST', -hw + 76, -hh + 23);

    c.fillStyle = '#64748B';
    c.font = "500 10.5px 'Inter', sans-serif";
    if ('letterSpacing' in c) c.letterSpacing = '0px';
    c.fillText('Mimari   ·   Kullanıcı Deneyimi   ·   Performans', -hw + 154, -hh + 23);

    const spX = hw - 142;
    roundRectPath(c, spX, -hh + 11, 122, 24, 999);
    c.fillStyle = '#F1F5F9';
    c.fill();
    c.beginPath();
    c.arc(spX + 13, -hh + 23, 3.5, 0, Math.PI * 2);
    c.fillStyle = '#10B981';
    c.fill();
    c.fillStyle = '#0F172A';
    c.font = "600 9.5px 'Inter', sans-serif";
    c.textAlign = 'left';
    c.fillText('0.4s LCP · 100/100', spX + 22, -hh + 23.5);

    c.fillStyle = '#7601FF';
    c.font = "700 9.5px 'Inter', sans-serif";
    c.textAlign = 'left';
    if ('letterSpacing' in c) c.letterSpacing = '0.04em';
    c.fillText('DÖNÜŞÜM ODAKLI WEB MİMARİSİ', leftX, bodyY + 10);

    c.fillStyle = '#0F172A';
    c.font = "800 24.5px 'Inter', sans-serif";
    if ('letterSpacing' in c) c.letterSpacing = '-0.03em';
    c.fillText('Her Detay Satış ve', leftX, bodyY + 39);
    c.fillText('ROAS İçin Tasarlanır.', leftX, bodyY + 67);

    c.fillStyle = '#475569';
    c.font = "500 10.8px 'Inter', sans-serif";
    if ('letterSpacing' in c) c.letterSpacing = '0px';
    c.fillText('Kreatif görsel hiyerarşi, sürtünmesiz UX akışı ve', leftX, bodyY + 95);
    c.fillText('teknik SEO altyapısı tek bir büyüme motorunda.', leftX, bodyY + 112);

    c.save();
    roundRectPath(c, leftX, vcY, leftW, vcH, 12);
    c.fillStyle = '#0F172A';
    if (explode > 0.05) {
      c.shadowColor = `rgba(15, 23, 42, ${(0.18 * explode).toFixed(3)})`;
      c.shadowBlur = 18;
      c.shadowOffsetY = 6 * explode;
    }
    c.fill();
    c.restore();

    c.save();
    roundRectPath(c, leftX, vcY, leftW, vcH, 12);
    c.clip();

    c.strokeStyle = 'rgba(255, 255, 255, 0.08)';
    c.lineWidth = 1;
    for (let r = 36; r <= 144; r += 36) {
      c.beginPath();
      c.arc(leftX + leftW - 56, vcY + vcH * 0.5, r, 0, Math.PI * 2);
      c.stroke();
    }

    roundRectPath(c, leftX + 18, vcY + 18, 42, 4, 2);
    c.fillStyle = '#A78BFA';
    c.fill();

    c.fillStyle = '#FFFFFF';
    c.font = "700 14px 'Inter', sans-serif";
    if ('letterSpacing' in c) c.letterSpacing = '-0.02em';
    c.textAlign = 'left';
    c.textBaseline = 'middle';
    c.fillText('Kreatif Görsel & UX Uyumu', leftX + 18, vcY + 42);

    c.fillStyle = '#94A3B8';
    c.font = "500 10.2px 'Inter', sans-serif";
    if ('letterSpacing' in c) c.letterSpacing = '0px';
    c.fillText('İlk 3 saniyede dikkat yakalayan görsel kurgu', leftX + 18, vcY + 62);

    roundRectPath(c, leftX + 16, vcY + 90, leftW - 32, 50, 8);
    c.fillStyle = 'rgba(255, 255, 255, 0.06)';
    c.fill();
    c.strokeStyle = 'rgba(255, 255, 255, 0.10)';
    c.stroke();

    c.fillStyle = '#94A3B8';
    c.font = "500 9.2px 'Inter', sans-serif";
    c.fillText('ETKİLEŞİM & DİKKAT SKORU', leftX + 28, vcY + 107);

    c.fillStyle = '#FFFFFF';
    c.font = "800 15px 'Inter', sans-serif";
    c.fillText('%96.4', leftX + 28, vcY + 126);

    c.fillStyle = '#6EE7B7';
    c.font = "600 10px 'Inter', sans-serif";
    c.textAlign = 'right';
    c.fillText('+2.4x Etkileşim', leftX + leftW - 28, vcY + 118);
    c.restore();

    c.save();
    roundRectPath(c, rx, bodyY, rw, rh, 14);
    c.fillStyle = '#FFFFFF';
    c.shadowColor = `rgba(15, 23, 42, ${lerpS3(0.08, 0.24, explode).toFixed(3)})`;
    c.shadowBlur = lerpS3(22, 30, explode);
    c.shadowOffsetY = lerpS3(8, 14, explode);
    c.fill();
    c.restore();

    roundRectPath(c, rx, bodyY, rw, rh, 14);
    c.strokeStyle = 'rgba(15, 23, 42, 0.09)';
    c.lineWidth = 1;
    c.stroke();

    c.fillStyle = '#0F172A';
    c.font = "700 12.8px 'Inter', sans-serif";
    c.textAlign = 'left';
    c.textBaseline = 'middle';
    if ('letterSpacing' in c) c.letterSpacing = '-0.02em';
    c.fillText('Dönüşüm & Büyüme Etkisi', rx + 18, bodyY + 23);

    c.fillStyle = '#64748B';
    c.font = "500 9.8px 'Inter', sans-serif";
    if ('letterSpacing' in c) c.letterSpacing = '0px';
    c.fillText('Doğrulanmış Canlı Performans', rx + 18, bodyY + 40);

    c.fillStyle = '#F1F5F9';
    c.fillRect(rx + 18, bodyY + 53, rw - 36, 1);

    const m1Y = bodyY + 65;
    roundRectPath(c, rx + 16, m1Y, rw - 32, 60, 10);
    c.fillStyle = '#F8FAFC';
    c.fill();
    c.strokeStyle = 'rgba(15, 23, 42, 0.06)';
    c.stroke();

    c.fillStyle = '#64748B';
    c.font = "600 8.8px 'Inter', sans-serif";
    c.textAlign = 'left';
    c.fillText('DÖNÜŞÜM ORANI (CVR)', rx + 26, m1Y + 17);

    c.fillStyle = '#0F172A';
    c.font = "800 23px 'Inter', sans-serif";
    if ('letterSpacing' in c) c.letterSpacing = '-0.03em';
    c.fillText(`%${cvrVal.toFixed(2)}`, rx + 26, m1Y + 42);

    c.fillStyle = '#10B981';
    c.font = "700 10px 'Inter', sans-serif";
    c.textAlign = 'right';
    if ('letterSpacing' in c) c.letterSpacing = '0px';
    c.fillText('+148%', rx + rw - 26, m1Y + 41);

    const m2Y = bodyY + 133;
    roundRectPath(c, rx + 16, m2Y, rw - 32, 60, 10);
    c.fillStyle = '#F8FAFC';
    c.fill();
    c.strokeStyle = 'rgba(15, 23, 42, 0.06)';
    c.stroke();

    c.fillStyle = '#64748B';
    c.font = "600 8.8px 'Inter', sans-serif";
    c.textAlign = 'left';
    c.fillText('REKLAM GETİRİSİ (ROAS)', rx + 26, m2Y + 17);

    c.fillStyle = '#0F172A';
    c.font = "800 23px 'Inter', sans-serif";
    if ('letterSpacing' in c) c.letterSpacing = '-0.03em';
    c.fillText(`${roasVal.toFixed(1)}x`, rx + 26, m2Y + 42);

    c.fillStyle = '#7601FF';
    c.font = "700 10px 'Inter', sans-serif";
    c.textAlign = 'right';
    if ('letterSpacing' in c) c.letterSpacing = '0px';
    c.fillText('Birim Büyüme', rx + rw - 26, m2Y + 41);

    drawCheckIconS3(c, rx + 23, bodyY + 212, 9.5, '#10B981');
    c.fillStyle = '#475569';
    c.font = "500 9.6px 'Inter', sans-serif";
    c.textAlign = 'left';
    c.fillText('SEO · UX · CRO Tam Entegrasyon', rx + 35, bodyY + 212.5);

    const btnX = rx + 16;
    const btnY = bodyY + 231;
    const btnW = rw - 32;
    const btnH = 43;

    const isClicked = clickProgress > 0.35;
    const pressScale = clickProgress > 0.15 && clickProgress < 0.45 ? 0.975 : 1.0;

    c.save();
    c.translate(btnX + btnW * 0.5, btnY + btnH * 0.5);
    c.scale(pressScale, pressScale);
    roundRectPath(c, -btnW * 0.5, -btnH * 0.5, btnW, btnH, 10);
    c.fillStyle = isClicked ? '#7601FF' : '#0F172A';
    c.fill();

    c.fillStyle = '#FFFFFF';
    c.font = "700 11px 'Inter', sans-serif";
    c.textAlign = 'center';
    c.textBaseline = 'middle';
    if ('letterSpacing' in c) c.letterSpacing = '-0.01em';
    c.fillText(isClicked ? '✓ Dönüşüm Optimize Edildi' : 'Dönüşümü Başlat  →', 0, 0.5);
    c.restore();

    if (explode < 0.25) {
      const curAlpha = 1 - smoothstepS3(0.05, 0.22, explode);
      c.save();
      c.globalAlpha = curAlpha;
      const targetX = btnX + btnW * 0.62;
      const targetY = btnY + btnH * 0.58;
      const startX = leftX + 205;
      const startY = bodyY + 148;
      const moveT = easeOutQuintS4(clamp01S4(clickProgress * 1.8));
      const cx = lerpS3(startX, targetX, moveT);
      const cy = lerpS3(startY, targetY, moveT);
      const clicking = clickProgress > 0.22 && clickProgress < 0.52;
      drawCursor2DS4(c, cx, cy, clicking ? 0.92 : 1.0, clicking);
      c.restore();
    }

    c.restore();
  }

  function drawVerticalAxesAndPulsesS4(c, W, H, z1, z3, cam, explode, elapsed) {
    if (explode <= 0.08) return;
    const alpha = smoothstepS3(0.08, 0.35, explode);
    const hw = W * 0.5;
    const hh = H * 0.5;

    const corners = [
      [-hw, -hh],
      [hw, -hh],
      [hw, hh],
      [-hw, hh]
    ];

    c.save();
    c.globalAlpha = alpha;

    corners.forEach(([u, v], idx) => {
      const pBot = projectPointS4(u, v, z1, cam);
      const pTop = projectPointS4(u, v, z3, cam);

      c.beginPath();
      c.moveTo(pBot.x, pBot.y);
      c.lineTo(pTop.x, pTop.y);
      c.strokeStyle = 'rgba(167, 139, 250, 0.28)';
      c.lineWidth = 1.2;
      c.setLineDash([4, 4]);
      c.stroke();
      c.setLineDash([]);

      const pT = ((elapsed * 0.6) + idx * 0.25) % 1;
      const zPulse = lerpS3(z1, z3, pT);
      const pCur = projectPointS4(u, v, zPulse, cam);

      c.beginPath();
      c.arc(pCur.x, pCur.y, 3.2, 0, Math.PI * 2);
      c.fillStyle = '#A78BFA';
      c.shadowColor = '#A78BFA';
      c.shadowBlur = 8;
      c.fill();
      c.shadowBlur = 0;
    });

    c.restore();
  }

  function drawArchitecturalCalloutsS4(c, W, H, z1, z2, z3, cam, explode) {
    if (explode <= 0.22) return;
    const alpha = smoothstepS3(0.22, 0.52, explode);

    const hw = W * 0.5;
    const boxW = 204;
    const boxH = 58;

    const callouts = [
      {
        anchor: projectPointS4(-hw, -108, z3, cam),
        bx: 36,
        side: 'left',
        num: 'KATMAN 03',
        title: 'Kreatif & Dönüşüm (CRO)',
        sub: 'Görsel Kanca & Tek Birincil CTA',
        accent: '#FFFFFF',
        dot: '#7601FF'
      },
      {
        anchor: projectPointS4(hw, 62, z2, cam),
        bx: 1020 - 36 - boxW,
        side: 'right',
        num: 'KATMAN 02',
        title: 'UX Akışı & Hiyerarşi',
        sub: '12 Sütun Grid & Göz Takibi Yolu',
        accent: '#E2E8F0',
        dot: '#A78BFA'
      },
      {
        anchor: projectPointS4(-hw, 32, z1, cam),
        bx: 36,
        side: 'left',
        num: 'KATMAN 01',
        title: 'Teknik SEO & Hız İskeleti',
        sub: 'Semantik HTML · Schema · 0.4s LCP',
        accent: '#CBD5E1',
        dot: '#10B981'
      }
    ];

    c.save();
    c.globalAlpha = alpha;

    callouts.forEach((co) => {
      const isLeft = co.side === 'left';
      const y = co.anchor.y;
      const lineEndX = isLeft ? co.bx + boxW + 8 : co.bx - 8;

      c.beginPath();
      c.arc(co.anchor.x, y, 3.8, 0, Math.PI * 2);
      c.fillStyle = co.dot;
      c.fill();

      c.beginPath();
      c.moveTo(co.anchor.x, y);
      c.lineTo(lineEndX, y);
      c.strokeStyle = 'rgba(226, 232, 240, 0.35)';
      c.lineWidth = 1.2;
      c.stroke();

      const by = y - boxH * 0.5;

      roundRectPath(c, co.bx, by, boxW, boxH, 10);
      c.fillStyle = 'rgba(15, 13, 26, 0.90)';
      c.fill();
      c.strokeStyle = 'rgba(255, 255, 255, 0.11)';
      c.lineWidth = 1;
      c.stroke();

      c.beginPath();
      c.arc(co.bx + 14, by + 16, 3.2, 0, Math.PI * 2);
      c.fillStyle = co.dot;
      c.fill();

      c.fillStyle = '#94A3B8';
      c.font = "700 9px 'Inter', sans-serif";
      c.textAlign = 'left';
      c.textBaseline = 'middle';
      if ('letterSpacing' in c) c.letterSpacing = '0.05em';
      c.fillText(co.num, co.bx + 23, by + 16);

      c.fillStyle = co.accent;
      c.font = "700 12px 'Inter', sans-serif";
      if ('letterSpacing' in c) c.letterSpacing = '-0.02em';
      c.fillText(co.title, co.bx + 14, by + 33);

      c.fillStyle = '#94A3B8';
      c.font = "500 9.6px 'Inter', sans-serif";
      if ('letterSpacing' in c) c.letterSpacing = '0px';
      c.fillText(co.sub, co.bx + 14, by + 48);
    });

    c.restore();
  }

  function drawStudioBackdropAndHUDS4(c, explode, clickProgress, roasVal, cvrVal) {
    c.fillStyle = '#0B0914';
    c.fillRect(0, 0, 1020, 788);

    const grad = c.createRadialGradient(510, 394, 20, 510, 394, 460);
    grad.addColorStop(0, 'rgba(118, 1, 255, 0.11)');
    grad.addColorStop(0.55, 'rgba(30, 27, 75, 0.05)');
    grad.addColorStop(1, 'rgba(11, 9, 20, 0)');
    c.fillStyle = grad;
    c.fillRect(0, 0, 1020, 788);

    c.save();
    c.fillStyle = '#94A3B8';
    c.font = "600 11px 'Inter', sans-serif";
    c.textAlign = 'left';
    c.textBaseline = 'middle';
    if ('letterSpacing' in c) c.letterSpacing = '0.06em';
    c.fillText('04 // DÖNÜŞÜM İÇİN TASARLA', 42, 42);

    const stateText = explode > 0.35
      ? '3D MİMARİ ANATOMİ · 3 KATMAN'
      : (clickProgress > 0.3 ? 'CANLI DÖNÜŞÜM · AKTİF' : 'BİRLEŞİK WEB DENEYİMİ');
    const dotCol = explode > 0.35 ? '#A78BFA' : '#10B981';

    c.textAlign = 'right';
    c.fillStyle = '#E2E8F0';
    c.font = "600 11px 'Inter', sans-serif";
    if ('letterSpacing' in c) c.letterSpacing = '0.04em';
    c.fillText(stateText, 1020 - 42, 42);

    const tw = c.measureText(stateText).width;
    c.beginPath();
    c.arc(1020 - 42 - tw - 12, 42, 3.8, 0, Math.PI * 2);
    c.fillStyle = dotCol;
    c.fill();

    const botY = 788 - 38;
    c.fillStyle = 'rgba(255, 255, 255, 0.08)';
    c.fillRect(42, botY - 22, 1020 - 84, 1);

    const specs = [
      { label: 'TEKNİK SEO & HIZ', val: '100/100 · 0.4s LCP' },
      { label: 'KULLANICI DENEYİMİ (UX)', val: '12-Sütun Sürtünmesiz Akış' },
      { label: 'DÖNÜŞÜM ORANI (CVR)', val: `%${cvrVal.toFixed(2)} (+148%)` },
      { label: 'REKLAM GETİRİSİ (ROAS)', val: `${roasVal.toFixed(1)}x Çarpan` }
    ];

    const colW = (1020 - 84) / 4;
    specs.forEach((sp, i) => {
      const sx = 42 + i * colW;
      c.fillStyle = '#64748B';
      c.font = "600 9.5px 'Inter', sans-serif";
      c.textAlign = 'left';
      if ('letterSpacing' in c) c.letterSpacing = '0.04em';
      c.fillText(sp.label, sx, botY - 4);

      c.fillStyle = i >= 2 ? '#FFFFFF' : '#CBD5E1';
      c.font = "700 12.5px 'Inter', sans-serif";
      if ('letterSpacing' in c) c.letterSpacing = '-0.01em';
      c.fillText(sp.val, sx, botY + 13);
    });

    c.restore();
  }

  function renderSlide4ConvertBroll(ctx, width, height, dpr, elapsed) {
    const LOOP_DURATION_S4 = 11.0;
    const t = elapsed % LOOP_DURATION_S4;

    const explodeIn = easeOutQuintS4(smoothstepS3(1.3, 3.0, t));
    const explodeOut = easeInOutCubicS4(smoothstepS3(6.7, 8.2, t));
    const explode = explodeIn * (1 - explodeOut);

    const orbitSweep = smoothstepS3(2.0, 7.6, t);
    const yawDeg = lerpS3(-4, -29 + 9 * orbitSweep, explode);
    const pitchDeg = lerpS3(8, 50, explode);
    const yaw = (yawDeg * Math.PI) / 180;
    const pitch = (pitchDeg * Math.PI) / 180;

    const snapPulse = Math.sin(smoothstepS3(7.8, 8.5, t) * Math.PI) * (1 - smoothstepS3(8.2, 8.6, t));

    let clickProgress = 0;
    if (t >= 8.25 && t <= 10.6) {
      clickProgress = smoothstepS3(8.25, 9.1, t) * (1 - smoothstepS3(10.2, 10.6, t));
    }

    const boost = smoothstepS3(8.7, 9.3, t) * (1 - smoothstepS3(10.3, 10.8, t));
    const cvrVal = lerpS3(4.20, 4.85, boost);
    const roasVal = lerpS3(5.4, 6.4, boost);

    const cam = {
      cx: 510,
      cy: lerpS3(388, 398, explode),
      scale: lerpS3(1.16, 0.81, explode) + snapPulse * 0.015,
      cosYaw: Math.cos(yaw),
      sinYaw: Math.sin(yaw),
      cosPitch: Math.cos(pitch),
      sinPitch: Math.sin(pitch)
    };

    const W = 576;
    const H = 368;
    const sep = 154 * explode;
    const z1 = -sep;
    const z2 = 0;
    const z3 = +sep;

    ctx.save();
    ctx.scale(dpr, dpr);

    ctx.fillStyle = '#0B0914';
    ctx.fillRect(0, 0, width, height);

    const scale = Math.min(width / 1020, height / 788);
    ctx.translate((width - 1020 * scale) * 0.5, (height - 788 * scale) * 0.5);
    ctx.scale(scale, scale);

    drawStudioBackdropAndHUDS4(ctx, explode, clickProgress, roasVal, cvrVal);
    drawLayer1TechnicalSEOS4(ctx, W, H, z1, cam, explode, elapsed);
    drawLayer2UXWireframeS4(ctx, W, H, z2, cam, explode, elapsed);
    drawVerticalAxesAndPulsesS4(ctx, W, H, z1, z3, cam, explode, elapsed);
    drawLayer3FinishedUIS4(ctx, W, H, z3, cam, explode, clickProgress, roasVal, cvrVal);
    drawArchitecturalCalloutsS4(ctx, W, H, z1, z2, z3, cam, explode);

    ctx.restore();
  }

  // ==========================================================================
  // SLIDE 5: "Ölçeklenebilir büyüme" — 3D Global Expansion Globe & Scale Card
  // ==========================================================================
  const LOOP_DURATION_S5 = 12.0;
  const smoothstep = smoothstepS3;
  const lerp = lerpS3;

  function latLonToVec3S5(latDeg, lonDeg) {
    const lat = (latDeg * Math.PI) / 180;
    const lon = (lonDeg * Math.PI) / 180;
    const cosLat = Math.cos(lat);
    return {
      x: cosLat * Math.sin(lon),
      y: -Math.sin(lat),
      z: cosLat * Math.cos(lon)
    };
  }

  function projectGlobeVec3S5(v, radius, cam) {
    const x1 = v.x * cam.cosYaw + v.z * cam.sinYaw;
    const y1 = v.y;
    const z1 = -v.x * cam.sinYaw + v.z * cam.cosYaw;

    const x2 = x1;
    const y2 = y1 * cam.cosPitch - z1 * cam.sinPitch;
    const z2 = y1 * cam.sinPitch + z1 * cam.cosPitch;

    const x3 = x2 * cam.cosRoll - y2 * cam.sinRoll;
    const y3 = x2 * cam.sinRoll + y2 * cam.cosRoll;

    return {
      x: cam.cx + x3 * radius,
      y: cam.cy + y3 * radius,
      z: z2,
      nx: x3,
      ny: y3
    };
  }

  const CONTINENT_BOXES_S5 = [
    [36, 60, -10, 30],
    [50, 70, 4, 32],
    [51, 59, -8, 2],
    [36, 42.5, 26, 45],
    [13, 35, 34, 60],
    [5, 36, -17, 51],
    [-35, 5, 9, 42],
    [20, 66, 45, 142],
    [8, 25, 70, 108],
    [25, 52, -125, -66],
    [52, 68, -135, -60],
    [15, 25, -106, -77],
    [-24, 11, -80, -35],
    [-54, -24, -74, -48]
  ];

  function isLandmassS5(lat, lon) {
    if (lat > 31 && lat < 36.2 && lon > 11 && lon < 34.5) return false;
    if (lat > 41.5 && lat < 46.5 && lon > 28 && lon < 41.5) return false;
    for (let i = 0; i < CONTINENT_BOXES_S5.length; i++) {
      const b = CONTINENT_BOXES_S5[i];
      if (lat >= b[0] && lat <= b[1] && lon >= b[2] && lon <= b[3]) return true;
    }
    return false;
  }

  const GLOBE_DOTS_S5 = (() => {
    const N = 1450;
    const goldenAngle = Math.PI * (3 - Math.sqrt(5));
    const list = [];
    for (let i = 0; i < N; i++) {
      const y = 1 - (i / (N - 1)) * 2;
      const latDeg = Math.asin(-y) * (180 / Math.PI);
      const theta = goldenAngle * i;
      let lonDeg = ((theta * 180) / Math.PI) % 360;
      if (lonDeg > 180) lonDeg -= 360;
      if (lonDeg < -180) lonDeg += 360;

      const land = isLandmassS5(latDeg, lonDeg);
      const vec = latLonToVec3S5(latDeg, lonDeg);
      const isCoreRegion = land && latDeg > 20 && latDeg < 58 && lonDeg > -85 && lonDeg < 60;
      list.push({
        vec,
        land,
        isCoreRegion,
        size: land ? (isCoreRegion ? 1.85 : 1.45) : 0.85
      });
    }
    return list;
  })();

  const GRATICULE_LINES_S5 = (() => {
    const lines = [];
    for (let lat = -60; lat <= 60; lat += 20) {
      const pts = [];
      for (let lon = -180; lon <= 180; lon += 6) pts.push(latLonToVec3S5(lat, lon));
      lines.push(pts);
    }
    for (let lon = -180; lon < 180; lon += 20) {
      const pts = [];
      for (let lat = -80; lat <= 80; lat += 5) pts.push(latLonToVec3S5(lat, lon));
      lines.push(pts);
    }
    return lines;
  })();

  const ORIGIN_HUB_S5 = {
    name: 'İSTANBUL',
    tag: 'MERKEZ HUB',
    lat: 41.01,
    lon: 28.97,
    vec: latLonToVec3S5(41.01, 28.97)
  };

  const EXPANSION_MARKETS_S5 = [
    {
      id: 'berlin',
      name: 'BERLİN',
      region: 'DACH',
      metric: '5.1x ROAS',
      growth: '+210%',
      lat: 52.52,
      lon: 13.40,
      vec: latLonToVec3S5(52.52, 13.40),
      arcHeight: 0.16,
      phaseOffset: 0.0,
      showBadge: true,
      labelDx: 10,
      labelDy: -22
    },
    {
      id: 'amsterdam',
      name: 'AMSTERDAM',
      region: 'EU',
      metric: '5.1x ROAS',
      growth: '+172%',
      lat: 52.37,
      lon: 4.90,
      vec: latLonToVec3S5(52.37, 4.90),
      arcHeight: 0.18,
      phaseOffset: 0.34,
      showBadge: false,
      labelDx: 0,
      labelDy: 0
    },
    {
      id: 'london',
      name: 'LONDRA',
      region: 'UK',
      metric: '5.8x ROAS',
      growth: '+184%',
      lat: 51.51,
      lon: -0.13,
      vec: latLonToVec3S5(51.51, -0.13),
      arcHeight: 0.22,
      phaseOffset: 0.16,
      showBadge: true,
      labelDx: -108,
      labelDy: -16
    },
    {
      id: 'newyork',
      name: 'NEW YORK',
      region: 'US',
      metric: '5.8x ROAS',
      growth: '+195%',
      lat: 40.71,
      lon: -64.0,
      vec: latLonToVec3S5(40.71, -64.0),
      arcHeight: 0.34,
      phaseOffset: 0.68,
      showBadge: true,
      labelDx: -46,
      labelDy: 22
    },
    {
      id: 'dubai',
      name: 'DUBAİ',
      region: 'MENA',
      metric: '6.2x ROAS',
      growth: '+240%',
      lat: 25.20,
      lon: 55.27,
      vec: latLonToVec3S5(25.20, 55.27),
      arcHeight: 0.20,
      phaseOffset: 0.52,
      showBadge: true,
      labelDx: -32,
      labelDy: 22
    },
    {
      id: 'riyadh',
      name: 'RİYAD',
      region: 'MENA',
      metric: '6.2x ROAS',
      growth: '+225%',
      lat: 24.71,
      lon: 46.67,
      vec: latLonToVec3S5(24.71, 46.67),
      arcHeight: 0.17,
      phaseOffset: 0.82,
      showBadge: false,
      labelDx: 0,
      labelDy: 0
    }
  ];

  function sampleArcVec3S5(v0, v1, u, maxAltitude) {
    const x = lerp(v0.x, v1.x, u);
    const y = lerp(v0.y, v1.y, u);
    const z = lerp(v0.z, v1.z, u);
    const len = Math.hypot(x, y, z) || 1;
    const elev = 1 + maxAltitude * 4 * u * (1 - u);
    return {
      x: (x / len) * elev,
      y: (y / len) * elev,
      z: (z / len) * elev
    };
  }

  function drawStudioBackdropAndHUDS5(c) {
    c.fillStyle = '#0B0914';
    c.fillRect(0, 0, 1020, 788);

    const grad = c.createRadialGradient(365, 396, 30, 365, 396, 410);
    grad.addColorStop(0, 'rgba(118, 1, 255, 0.15)');
    grad.addColorStop(0.55, 'rgba(30, 27, 75, 0.06)');
    grad.addColorStop(1, 'rgba(11, 9, 20, 0)');
    c.fillStyle = grad;
    c.fillRect(0, 0, 1020, 788);
  }

  function drawOrbitalScaleRingHalfS5(c, radius, cam, elapsed, isFrontHalf) {
    const ringR = radius * 1.22;
    const segments = 90;

    c.save();
    c.beginPath();
    let started = false;

    for (let i = 0; i <= segments; i++) {
      const a = (i / segments) * Math.PI * 2;
      const v = {
        x: Math.cos(a),
        y: Math.sin(a) * 0.22,
        z: Math.sin(a)
      };
      const p = projectGlobeVec3S5(v, ringR, cam);
      const inFront = p.z >= 0;
      if (inFront === isFrontHalf) {
        if (!started) {
          c.moveTo(p.x, p.y);
          started = true;
        } else {
          c.lineTo(p.x, p.y);
        }
      } else {
        started = false;
      }
    }

    c.strokeStyle = isFrontHalf ? 'rgba(167, 139, 250, 0.34)' : 'rgba(148, 163, 184, 0.12)';
    c.lineWidth = isFrontHalf ? 1.4 : 1.0;
    c.setLineDash([5, 5]);
    c.stroke();
    c.setLineDash([]);

    for (let k = 0; k < 3; k++) {
      const angle = elapsed * 0.55 + k * ((Math.PI * 2) / 3);
      const v = {
        x: Math.cos(angle),
        y: Math.sin(angle) * 0.22,
        z: Math.sin(angle)
      };
      const p = projectGlobeVec3S5(v, ringR, cam);
      if ((p.z >= 0) === isFrontHalf) {
        c.beginPath();
        c.arc(p.x, p.y, isFrontHalf ? 3.4 : 2.2, 0, Math.PI * 2);
        c.fillStyle = k === 0 ? '#10B981' : '#A78BFA';
        if (isFrontHalf) {
          c.shadowColor = k === 0 ? '#10B981' : '#A78BFA';
          c.shadowBlur = 8;
        }
        c.fill();
        c.shadowBlur = 0;
      }
    }

    c.restore();
  }

  function draw3DGlobeAndArcsS5(c, radius, cam, elapsed) {
    drawOrbitalScaleRingHalfS5(c, radius, cam, elapsed, false);

    c.save();
    c.beginPath();
    c.arc(cam.cx, cam.cy, radius, 0, Math.PI * 2);
    const sphereGrad = c.createRadialGradient(
      cam.cx - radius * 0.28,
      cam.cy - radius * 0.28,
      radius * 0.1,
      cam.cx,
      cam.cy,
      radius
    );
    sphereGrad.addColorStop(0, '#17132B');
    sphereGrad.addColorStop(0.68, '#0D0B18');
    sphereGrad.addColorStop(1, '#080610');
    c.fillStyle = sphereGrad;
    c.fill();

    c.strokeStyle = 'rgba(167, 139, 250, 0.32)';
    c.lineWidth = 1.5;
    c.stroke();
    c.restore();

    c.save();
    c.beginPath();
    c.arc(cam.cx, cam.cy, radius - 1, 0, Math.PI * 2);
    c.clip();

    c.strokeStyle = 'rgba(148, 163, 184, 0.09)';
    c.lineWidth = 0.9;
    for (let l = 0; l < GRATICULE_LINES_S5.length; l++) {
      const pts = GRATICULE_LINES_S5[l];
      c.beginPath();
      let drawing = false;
      for (let i = 0; i < pts.length; i++) {
        const p = projectGlobeVec3S5(pts[i], radius, cam);
        if (p.z > 0.02) {
          if (!drawing) {
            c.moveTo(p.x, p.y);
            drawing = true;
          } else {
            c.lineTo(p.x, p.y);
          }
        } else {
          drawing = false;
        }
      }
      c.stroke();
    }

    for (let i = 0; i < GLOBE_DOTS_S5.length; i++) {
      const d = GLOBE_DOTS_S5[i];
      const p = projectGlobeVec3S5(d.vec, radius, cam);
      if (p.z <= 0.04) continue;

      const limbFade = smoothstep(0.04, 0.35, p.z);
      c.beginPath();
      c.arc(p.x, p.y, d.size, 0, Math.PI * 2);
      if (d.land) {
        const alpha = (d.isCoreRegion ? 0.82 : 0.48) * limbFade;
        c.fillStyle = d.isCoreRegion
          ? `rgba(226, 232, 240, ${alpha.toFixed(3)})`
          : `rgba(148, 163, 184, ${alpha.toFixed(3)})`;
      } else {
        c.fillStyle = `rgba(148, 163, 184, ${(0.07 * limbFade).toFixed(3)})`;
      }
      c.fill();
    }
    c.restore();

    const pOrigin = projectGlobeVec3S5(ORIGIN_HUB_S5.vec, radius, cam);

    EXPANSION_MARKETS_S5.forEach((mkt, idx) => {
      const steps = 36;
      const arcPts = [];
      for (let s = 0; s <= steps; s++) {
        const u = s / steps;
        const vArc = sampleArcVec3S5(ORIGIN_HUB_S5.vec, mkt.vec, u, mkt.arcHeight);
        arcPts.push(projectGlobeVec3S5(vArc, radius, cam));
      }

      c.save();
      c.beginPath();
      arcPts.forEach((pt, i) => {
        if (i === 0) c.moveTo(pt.x, pt.y);
        else c.lineTo(pt.x, pt.y);
      });
      c.strokeStyle = 'rgba(167, 139, 250, 0.24)';
      c.lineWidth = 1.2;
      c.setLineDash([4, 4]);
      c.stroke();
      c.setLineDash([]);

      const cycle = ((elapsed * 0.42) + mkt.phaseOffset) % 1.0;
      const headIdx = Math.min(steps, Math.floor(cycle * steps));
      const tailIdx = Math.max(0, headIdx - 11);

      if (headIdx > tailIdx) {
        c.beginPath();
        for (let i = tailIdx; i <= headIdx; i++) {
          if (i === tailIdx) c.moveTo(arcPts[i].x, arcPts[i].y);
          else c.lineTo(arcPts[i].x, arcPts[i].y);
        }
        c.strokeStyle = idx % 2 === 0 ? '#A78BFA' : '#10B981';
        c.lineWidth = 2.4;
        c.lineCap = 'round';
        c.stroke();

        const headPt = arcPts[headIdx];
        c.beginPath();
        c.arc(headPt.x, headPt.y, 3.6, 0, Math.PI * 2);
        c.fillStyle = '#FFFFFF';
        c.shadowColor = idx % 2 === 0 ? '#A78BFA' : '#10B981';
        c.shadowBlur = 10;
        c.fill();
        c.shadowBlur = 0;
      }
      c.restore();

      const pDest = projectGlobeVec3S5(mkt.vec, radius, cam);
      if (pDest.z > 0.08) {
        const vis = smoothstep(0.08, 0.28, pDest.z);
        c.save();
        c.globalAlpha = vis;

        const ringPhase = ((elapsed * 0.85) + mkt.phaseOffset) % 1.0;
        c.beginPath();
        c.arc(pDest.x, pDest.y, 4 + ringPhase * 14, 0, Math.PI * 2);
        c.strokeStyle = `rgba(16, 185, 129, ${(0.65 * (1 - ringPhase)).toFixed(3)})`;
        c.lineWidth = 1.4;
        c.stroke();

        c.beginPath();
        c.arc(pDest.x, pDest.y, 4.2, 0, Math.PI * 2);
        c.fillStyle = '#10B981';
        c.fill();
        c.lineWidth = 1.5;
        c.strokeStyle = '#FFFFFF';
        c.stroke();

        if (mkt.showBadge) {
          const lx = pDest.x + mkt.labelDx;
          const ly = pDest.y + mkt.labelDy;
          const tagText = `${mkt.name} · ${mkt.growth}`;
          c.font = `700 9.5px 'Inter', sans-serif`;
          const tw = c.measureText(tagText).width;
          const pw = tw + 16;
          const ph = 20;

          roundRectPath(c, lx, ly - ph * 0.5, pw, ph, 6);
          c.fillStyle = 'rgba(15, 13, 26, 0.90)';
          c.fill();
          c.strokeStyle = 'rgba(255, 255, 255, 0.15)';
          c.lineWidth = 1;
          c.stroke();

          c.fillStyle = '#FFFFFF';
          c.textAlign = 'left';
          c.textBaseline = 'middle';
          c.fillText(tagText, lx + 8, ly + 0.5);
        }

        c.restore();
      }
    });

    if (pOrigin.z > 0.1) {
      c.save();
      const pulseR = 6 + ((elapsed * 14) % 16);
      const pulseA = 1 - ((pulseR - 6) / 16);
      c.beginPath();
      c.arc(pOrigin.x, pOrigin.y, pulseR, 0, Math.PI * 2);
      c.strokeStyle = `rgba(118, 1, 255, ${(0.8 * pulseA).toFixed(3)})`;
      c.lineWidth = 2;
      c.stroke();

      c.beginPath();
      c.arc(pOrigin.x, pOrigin.y, 5.5, 0, Math.PI * 2);
      c.fillStyle = '#7601FF';
      c.fill();
      c.lineWidth = 2;
      c.strokeStyle = '#FFFFFF';
      c.stroke();
      c.restore();
    }

    drawOrbitalScaleRingHalfS5(c, radius, cam, elapsed, true);

    return pOrigin;
  }

  function drawLeftGlobeCalloutsS5(c, pOrigin, cam, radius) {
    const boxW = 192;
    const boxH = 58;
    const bx = 38;

    const by1 = 194;
    const anchor1X = pOrigin.x;
    const anchor1Y = pOrigin.y;
    const elbow1X = bx + boxW + 24;
    const start1Y = by1 + boxH * 0.5;

    c.save();
    c.beginPath();
    c.moveTo(bx + boxW + 6, start1Y);
    c.lineTo(elbow1X, start1Y);
    c.lineTo(anchor1X, anchor1Y);
    c.strokeStyle = 'rgba(167, 139, 250, 0.38)';
    c.lineWidth = 1.2;
    c.stroke();

    roundRectPath(c, bx, by1, boxW, boxH, 10);
    c.fillStyle = 'rgba(15, 13, 26, 0.90)';
    c.fill();
    c.strokeStyle = 'rgba(255, 255, 255, 0.11)';
    c.lineWidth = 1;
    c.stroke();

    c.beginPath();
    c.arc(bx + 14, by1 + 16, 3.2, 0, Math.PI * 2);
    c.fillStyle = '#7601FF';
    c.fill();

    c.fillStyle = '#94A3B8';
    c.font = `700 9px 'Inter', sans-serif`;
    c.textAlign = 'left';
    c.textBaseline = 'middle';
    if ('letterSpacing' in c) c.letterSpacing = '0.05em';
    c.fillText('MERKEZ // İSTANBUL HUB', bx + 23, by1 + 16);

    c.fillStyle = '#FFFFFF';
    c.font = `700 12px 'Inter', sans-serif`;
    if ('letterSpacing' in c) c.letterSpacing = '-0.02em';
    c.fillText('Global Kampanya Üssü', bx + 14, by1 + 33);

    c.fillStyle = '#94A3B8';
    c.font = `500 9.5px 'Inter', sans-serif`;
    if ('letterSpacing' in c) c.letterSpacing = '0px';
    c.fillText('Veri & Çok Dilli Reklam Kurgusu', bx + 14, by1 + 48);

    const by2 = 524;
    const start2Y = by2 + boxH * 0.5;
    const ringAnchorX = cam.cx - radius * 0.86;
    const ringAnchorY = cam.cy + radius * 0.52;

    c.beginPath();
    c.moveTo(bx + boxW + 6, start2Y);
    c.lineTo(ringAnchorX, ringAnchorY);
    c.strokeStyle = 'rgba(16, 185, 129, 0.35)';
    c.lineWidth = 1.2;
    c.stroke();

    c.beginPath();
    c.arc(ringAnchorX, ringAnchorY, 3.5, 0, Math.PI * 2);
    c.fillStyle = '#10B981';
    c.fill();

    roundRectPath(c, bx, by2, boxW, boxH, 10);
    c.fillStyle = 'rgba(15, 13, 26, 0.90)';
    c.fill();
    c.strokeStyle = 'rgba(255, 255, 255, 0.11)';
    c.lineWidth = 1;
    c.stroke();

    c.beginPath();
    c.arc(bx + 14, by2 + 16, 3.2, 0, Math.PI * 2);
    c.fillStyle = '#10B981';
    c.fill();

    c.fillStyle = '#94A3B8';
    c.font = `700 9px 'Inter', sans-serif`;
    if ('letterSpacing' in c) c.letterSpacing = '0.05em';
    c.fillText('ÖLÇEK // YENİ LANSMAN', bx + 23, by2 + 16);

    c.fillStyle = '#E2E8F0';
    c.font = `700 12px 'Inter', sans-serif`;
    if ('letterSpacing' in c) c.letterSpacing = '-0.02em';
    c.fillText('Sınır Ötesi Büyüme Ağı', bx + 14, by2 + 33);

    c.fillStyle = '#94A3B8';
    c.font = `500 9.5px 'Inter', sans-serif`;
    if ('letterSpacing' in c) c.letterSpacing = '0px';
    c.fillText('5 Global Bölge · Sıfır Kayıp', bx + 14, by2 + 48);

    c.restore();
  }

  function drawRightGlobalScaleCardS5(c, elapsed, compoundGrowth, globalRoas, activeCorridorIdx) {
    const cardX = 638;
    const cardY = 136;
    const cardW = 340;
    const cardH = 516;

    c.save();
    const floatY = Math.sin(elapsed * 1.4) * 3.5;
    c.translate(0, floatY);

    for (let s = 6; s >= 1; s--) {
      roundRectPath(c, cardX - s * 0.8, cardY + s * 1.1, cardW, cardH, 18);
      c.fillStyle = '#CBD5E1';
      c.fill();
    }

    c.save();
    roundRectPath(c, cardX, cardY, cardW, cardH, 18);
    c.fillStyle = '#F8FAFC';
    c.shadowColor = 'rgba(0, 0, 0, 0.65)';
    c.shadowBlur = 42;
    c.shadowOffsetX = -12;
    c.shadowOffsetY = 18;
    c.fill();
    c.restore();

    roundRectPath(c, cardX, cardY, cardW, cardH, 18);
    c.fillStyle = '#F8FAFC';
    c.fill();
    c.strokeStyle = '#FFFFFF';
    c.lineWidth = 1.5;
    c.stroke();

    c.save();
    roundRectPath(c, cardX, cardY, cardW, cardH, 18);
    c.clip();

    c.fillStyle = '#FFFFFF';
    c.fillRect(cardX, cardY, cardW, 48);
    c.fillStyle = 'rgba(15, 23, 42, 0.08)';
    c.fillRect(cardX, cardY + 48, cardW, 1);

    c.fillStyle = '#0F172A';
    c.font = `800 12px 'Inter', sans-serif`;
    c.textAlign = 'left';
    c.textBaseline = 'middle';
    if ('letterSpacing' in c) c.letterSpacing = '-0.03em';
    c.fillText('ROASİST SCALE', cardX + 22, cardY + 24);

    const pillW = 124;
    const pillX = cardX + cardW - pillW - 18;
    roundRectPath(c, pillX, cardY + 12, pillW, 24, 999);
    c.fillStyle = '#F1F5F9';
    c.fill();
    c.beginPath();
    c.arc(pillX + 13, cardY + 24, 3.5, 0, Math.PI * 2);
    c.fillStyle = '#10B981';
    c.fill();
    c.fillStyle = '#0F172A';
    c.font = `600 9.5px 'Inter', sans-serif`;
    if ('letterSpacing' in c) c.letterSpacing = '0px';
    c.fillText('14 Ülke · Aktif Ağ', pillX + 22, cardY + 24.5);

    const pad = 22;
    const ix = cardX + pad;
    let curY = cardY + 70;

    c.fillStyle = '#7601FF';
    c.font = `700 9.5px 'Inter', sans-serif`;
    if ('letterSpacing' in c) c.letterSpacing = '0.04em';
    c.fillText('SÜRDÜRÜLEBİLİR ÖLÇEKLENME', ix, curY);

    curY += 26;
    c.fillStyle = '#0F172A';
    c.font = `800 22px 'Inter', sans-serif`;
    if ('letterSpacing' in c) c.letterSpacing = '-0.03em';
    c.fillText('Yeni Lansmandan', ix, curY);
    curY += 26;
    c.fillText('Global Pazarlara.', ix, curY);

    curY += 24;
    const heroH = 92;
    const innerW = cardW - pad * 2;

    c.save();
    roundRectPath(c, ix, curY, innerW, heroH, 12);
    c.fillStyle = '#FFFFFF';
    c.shadowColor = 'rgba(15, 23, 42, 0.06)';
    c.shadowBlur = 16;
    c.shadowOffsetY = 5;
    c.fill();
    c.restore();

    roundRectPath(c, ix, curY, innerW, heroH, 12);
    c.strokeStyle = 'rgba(15, 23, 42, 0.08)';
    c.lineWidth = 1;
    c.stroke();

    c.fillStyle = '#64748B';
    c.font = `600 9px 'Inter', sans-serif`;
    if ('letterSpacing' in c) c.letterSpacing = '0.03em';
    c.fillText('BİLEŞİK GELİR & PAZAR ÖLÇEĞİ', ix + 18, curY + 20);

    c.fillStyle = '#0F172A';
    c.font = `800 31px 'Inter', sans-serif`;
    if ('letterSpacing' in c) c.letterSpacing = '-0.03em';
    c.fillText(`+%${Math.round(compoundGrowth)}`, ix + 18, curY + 54);

    c.fillStyle = '#10B981';
    c.font = `700 11px 'Inter', sans-serif`;
    c.textAlign = 'right';
    if ('letterSpacing' in c) c.letterSpacing = '0px';
    c.fillText(`${globalRoas.toFixed(1)}x Global ROAS`, ix + innerW - 18, curY + 46);

    c.fillStyle = '#64748B';
    c.font = `500 9.5px 'Inter', sans-serif`;
    c.fillText('Birim Ekonomi Korunarak', ix + innerW - 18, curY + 64);

    curY += heroH + 18;
    c.textAlign = 'left';
    c.fillStyle = '#475569';
    c.font = `700 9.5px 'Inter', sans-serif`;
    if ('letterSpacing' in c) c.letterSpacing = '0.03em';
    c.fillText('CANLI PAZAR AÇILIM KORİDORLARI', ix, curY);

    curY += 14;
    const corridors = [
      { region: 'AVRUPA & DACH', cities: 'Berlin · Amsterdam', roas: '5.1x ROAS', lift: '+210%' },
      { region: 'İNGİLTERE & ABD', cities: 'Londra · New York', roas: '5.8x ROAS', lift: '+195%' },
      { region: 'MENA & KÖRFEZ', cities: 'Dubai · Riyad', roas: '6.2x ROAS', lift: '+240%' }
    ];

    corridors.forEach((cor, i) => {
      const ry = curY + i * 54;
      const isActive = i === activeCorridorIdx;

      roundRectPath(c, ix, ry, innerW, 46, 10);
      c.fillStyle = isActive ? '#FFFFFF' : '#F1F5F9';
      c.fill();
      c.strokeStyle = isActive ? 'rgba(118, 1, 255, 0.35)' : 'rgba(15, 23, 42, 0.06)';
      c.lineWidth = isActive ? 1.4 : 1;
      c.stroke();

      c.beginPath();
      c.arc(ix + 15, ry + 23, 3.6, 0, Math.PI * 2);
      c.fillStyle = isActive ? '#7601FF' : '#10B981';
      c.fill();

      c.fillStyle = '#0F172A';
      c.font = `700 11px 'Inter', sans-serif`;
      c.textAlign = 'left';
      if ('letterSpacing' in c) c.letterSpacing = '-0.01em';
      c.fillText(cor.region, ix + 27, ry + 16);

      c.fillStyle = '#64748B';
      c.font = `500 9.5px 'Inter', sans-serif`;
      if ('letterSpacing' in c) c.letterSpacing = '0px';
      c.fillText(cor.cities, ix + 27, ry + 32);

      c.fillStyle = '#0F172A';
      c.font = `700 11px 'Inter', sans-serif`;
      c.textAlign = 'right';
      c.fillText(cor.lift, ix + innerW - 14, ry + 16);

      c.fillStyle = isActive ? '#7601FF' : '#10B981';
      c.font = `600 9.5px 'Inter', sans-serif`;
      c.fillText(cor.roas, ix + innerW - 14, ry + 32);
    });

    const btnY = cardY + cardH - 60;
    roundRectPath(c, ix, btnY, innerW, 42, 10);
    c.fillStyle = '#0F172A';
    c.fill();

    drawCheckIconS3(c, ix + 22, btnY + 21, 9.5, '#10B981');
    c.fillStyle = '#FFFFFF';
    c.font = `700 11px 'Inter', sans-serif`;
    c.textAlign = 'left';
    if ('letterSpacing' in c) c.letterSpacing = '-0.01em';
    c.fillText('Global Ölçekleme Altyapısı Hazır', ix + 36, btnY + 21.5);

    c.fillStyle = '#A78BFA';
    c.textAlign = 'right';
    c.fillText('→', ix + innerW - 18, btnY + 21.5);

    c.restore();
    c.restore();
  }

  function renderSlide5ScaleGlobe(ctx, width, height, dpr, elapsed) {
    const t = elapsed % LOOP_DURATION_S5;
    const phase = (t / LOOP_DURATION_S5) * Math.PI * 2;

    const yawDeg = -4 + Math.sin(phase) * 10;
    const pitchDeg = -32 + Math.cos(phase) * 3;
    const rollDeg = -5;

    const yaw = (yawDeg * Math.PI) / 180;
    const pitch = (pitchDeg * Math.PI) / 180;
    const roll = (rollDeg * Math.PI) / 180;

    const cam = {
      cx: 392,
      cy: 394,
      cosYaw: Math.cos(yaw),
      sinYaw: Math.sin(yaw),
      cosPitch: Math.cos(pitch),
      sinPitch: Math.sin(pitch),
      cosRoll: Math.cos(roll),
      sinRoll: Math.sin(roll)
    };

    const globeRadius = 212;
    const wave01 = 0.5 - 0.5 * Math.cos(phase);
    const compoundGrowth = lerp(285, 340, wave01);
    const globalRoas = lerp(5.2, 5.8, wave01);
    const activeMarketsCount = 14;
    const activeCorridorIdx = Math.floor((t / LOOP_DURATION_S5) * 3) % 3;

    ctx.save();
    ctx.scale(dpr, dpr);

    ctx.fillStyle = '#0B0914';
    ctx.fillRect(0, 0, width, height);

    const scale = Math.min(width / 1020, height / 788);
    ctx.translate((width - 1020 * scale) * 0.5, (height - 788 * scale) * 0.5);
    ctx.scale(scale, scale);

    drawStudioBackdropAndHUDS5(ctx, activeMarketsCount, compoundGrowth, globalRoas);
    const pOrigin = draw3DGlobeAndArcsS5(ctx, globeRadius, cam, elapsed);
    drawLeftGlobeCalloutsS5(ctx, pOrigin, cam, globeRadius);
    drawRightGlobalScaleCardS5(ctx, elapsed, compoundGrowth, globalRoas, activeCorridorIdx);

    ctx.restore();
  }

  // ==========================================================================
  // MOUNT & INTERSECTION OBSERVER LIFECYCLE
  // ==========================================================================
  let s1Canvas = null, s1Ctx = null, s1W = 562, s1H = 434, s1Dpr = 1;
  let s2Canvas = null, s2Ctx = null, s2W = 562, s2H = 434, s2Dpr = 1;
  let s3Canvas = null, s3Ctx = null, s3W = 562, s3H = 434, s3Dpr = 1;
  let s4Canvas = null, s4Ctx = null, s4W = 562, s4H = 434, s4Dpr = 1;
  let s5Canvas = null, s5Ctx = null, s5W = 562, s5H = 434, s5Dpr = 1;
  let isCarouselVisible = true;
  let observerAttached = false;
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
    const carouselEl = document.getElementById('carousel');
    if (carouselEl && !observerAttached && 'IntersectionObserver' in window) {
      observerAttached = true;
      const io = new IntersectionObserver((entries) => {
        for (const entry of entries) {
          isCarouselVisible = entry.isIntersecting;
        }
      }, { threshold: 0.02 });
      io.observe(carouselEl);
    }

    // Slide 1
    const c1 = document.querySelector('#carousel .swiper-slide:nth-child(1) .CarouselSlides_carouselMedia__aqYWx');
    if (c1) {
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
      const r1 = c1.getBoundingClientRect();
      if (r1.width > 40 && r1.height > 40) {
        const d = Math.min(window.devicePixelRatio || 1, 2);
        const tw = Math.floor(r1.width), th = Math.floor(r1.height);
        if (s1W !== tw || s1H !== th || s1Dpr !== d || cv1.width !== tw * d) {
          s1W = tw; s1H = th; s1Dpr = d;
          cv1.width = tw * d; cv1.height = th * d;
        }
      }
    }

    // Slide 2
    const c2 = document.querySelector('#carousel .swiper-slide:nth-child(2) .CarouselSlides_carouselMedia__aqYWx');
    if (c2) {
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
      const r2 = c2.getBoundingClientRect();
      if (r2.width > 40 && r2.height > 40) {
        const d = Math.min(window.devicePixelRatio || 1, 2);
        const tw = Math.floor(r2.width), th = Math.floor(r2.height);
        if (s2W !== tw || s2H !== th || s2Dpr !== d || cv2.width !== tw * d) {
          s2W = tw; s2H = th; s2Dpr = d;
          cv2.width = tw * d; cv2.height = th * d;
        }
      }
    }

    // Slide 3
    const c3 = document.querySelector('#carousel .swiper-slide:nth-child(3) .CarouselSlides_carouselMedia__aqYWx');
    if (c3) {
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
      const r3 = c3.getBoundingClientRect();
      if (r3.width > 40 && r3.height > 40) {
        const d = Math.min(window.devicePixelRatio || 1, 2);
        const tw = Math.floor(r3.width), th = Math.floor(r3.height);
        if (s3W !== tw || s3H !== th || s3Dpr !== d || cv3.width !== tw * d) {
          s3W = tw; s3H = th; s3Dpr = d;
          cv3.width = tw * d; cv3.height = th * d;
        }
      }
    }

    // Slide 4
    const c4 = document.querySelector('#carousel .swiper-slide:nth-child(4) .CarouselSlides_carouselMedia__aqYWx');
    if (c4) {
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
      const r4 = c4.getBoundingClientRect();
      if (r4.width > 40 && r4.height > 40) {
        const d = Math.min(window.devicePixelRatio || 1, 2);
        const tw = Math.floor(r4.width), th = Math.floor(r4.height);
        if (s4W !== tw || s4H !== th || s4Dpr !== d || cv4.width !== tw * d) {
          s4W = tw; s4H = th; s4Dpr = d;
          cv4.width = tw * d; cv4.height = th * d;
        }
      }
    }

    // Slide 5
    const c5 = document.querySelector('#carousel .swiper-slide:nth-child(5) .CarouselSlides_carouselMedia__aqYWx');
    if (c5) {
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
      const r5 = c5.getBoundingClientRect();
      if (r5.width > 40 && r5.height > 40) {
        const d = Math.min(window.devicePixelRatio || 1, 2);
        const tw = Math.floor(r5.width), th = Math.floor(r5.height);
        if (s5W !== tw || s5H !== th || s5Dpr !== d || cv5.width !== tw * d) {
          s5W = tw; s5H = th; s5Dpr = d;
          cv5.width = tw * d; cv5.height = th * d;
        }
      }
    }
  }

  function tick(now) {
    requestAnimationFrame(tick);
    try {
      ensureCanvasesMounted();
    } catch {}

    if (isCarouselVisible && !document.hidden) {
      const elapsedSeconds = (now - startTime) * 0.001;

      // Render Slide 1 ("Önce veri ve strateji")
      if (s1Ctx) {
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
      if (s2Ctx) {
        try { renderSlide2Bento(s2Ctx, s2W, s2H, s2Dpr, elapsedSeconds); } catch {}
      }

      // Render Slide 3 ("Kusursuz süreç yönetimi")
      if (s3Ctx) {
        try { renderSlide3ProcessCockpit(s3Ctx, s3W, s3H, s3Dpr, elapsedSeconds); } catch {}
      }

      // Render Slide 4 ("Dönüşüm için tasarla")
      if (s4Ctx) {
        try { renderSlide4ConvertBroll(s4Ctx, s4W, s4H, s4Dpr, elapsedSeconds); } catch {}
      }

      // Render Slide 5 ("Ölçeklenebilir büyüme")
      if (s5Ctx) {
        try { renderSlide5ScaleGlobe(s5Ctx, s5W, s5H, s5Dpr, elapsedSeconds); } catch {}
      }
    }
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

        # Eliminate the MP4 video downloads from RSC payload for all 5 slides
        # IMPORTANT: Keep a valid https:// URL so Next.js/React new URL(mediaItemUrl) never throws!
        html = re.sub(
            r'https://roasist\.github\.io/roasist-web/images/methodology/01-veri-ve-strateji\.mp4(\?v=\d+)?',
            "https://roasist.github.io/roasist-web/images/methodology/01-veri-ve-strateji.jpg",
            html,
        )
        html = re.sub(
            r'https://roasist\.github\.io/roasist-web/images/methodology/02-yaratici-ve-cesur-fikir\.mp4(\?v=\d+)?',
            "https://roasist.github.io/roasist-web/images/methodology/02-yaratici-ve-cesur-fikir.jpg",
            html,
        )
        html = re.sub(
            r'https://roasist\.github\.io/roasist-web/images/methodology/03-kusursuz-surec-yonetimi\.mp4(\?v=\d+)?',
            "https://roasist.github.io/roasist-web/images/methodology/03-kusursuz-surec-yonetimi.jpg",
            html,
        )
        html = re.sub(
            r'https://kota-content\.b-cdn\.net/app/uploads/2026/07/Create-To-Convert-compress\.mp4',
            "https://roasist.github.io/roasist-web/images/methodology/04-donusum-icin-tasarla.jpg",
            html,
        )
        html = re.sub(
            r'https://kota-content\.b-cdn\.net/app/uploads/2026/07/Build-For-Scale-V3-compressed\.mp4',
            "https://roasist.github.io/roasist-web/images/methodology/05-olceklenebilir-buyume.jpg",
            html,
        )
        # Also repair any already-emptied mediaItemUrl:"" in slides
        html = html.replace(
            r'\"media\":{\"mediaItemUrl\":\"\",\"mimeType\":\"video/mp4\"},\"image\":{\"mediaItemUrl\":\"https://roasist.github.io/roasist-web/images/methodology/01-veri-ve-strateji.jpg',
            r'\"media\":{\"mediaItemUrl\":\"https://roasist.github.io/roasist-web/images/methodology/01-veri-ve-strateji.jpg\",\"mimeType\":\"video/mp4\"},\"image\":{\"mediaItemUrl\":\"https://roasist.github.io/roasist-web/images/methodology/01-veri-ve-strateji.jpg',
        )
        html = html.replace(
            r'\"media\":{\"mediaItemUrl\":\"\",\"mimeType\":\"video/mp4\"},\"image\":{\"mediaItemUrl\":\"https://roasist.github.io/roasist-web/images/methodology/02-yaratici-ve-cesur-fikir.jpg',
            r'\"media\":{\"mediaItemUrl\":\"https://roasist.github.io/roasist-web/images/methodology/02-yaratici-ve-cesur-fikir.jpg\",\"mimeType\":\"video/mp4\"},\"image\":{\"mediaItemUrl\":\"https://roasist.github.io/roasist-web/images/methodology/02-yaratici-ve-cesur-fikir.jpg',
        )
        html = html.replace(
            r'\"media\":{\"mediaItemUrl\":\"\",\"mimeType\":\"video/mp4\"},\"image\":{\"mediaItemUrl\":\"https://roasist.github.io/roasist-web/images/methodology/03-kusursuz-surec-yonetimi.jpg',
            r'\"media\":{\"mediaItemUrl\":\"https://roasist.github.io/roasist-web/images/methodology/03-kusursuz-surec-yonetimi.jpg\",\"mimeType\":\"video/mp4\"},\"image\":{\"mediaItemUrl\":\"https://roasist.github.io/roasist-web/images/methodology/03-kusursuz-surec-yonetimi.jpg',
        )
        html = html.replace(
            r'\"media\":{\"mediaItemUrl\":\"\",\"mimeType\":\"video/mp4\"},\"image\":{\"mediaItemUrl\":\"https://roasist.github.io/roasist-web/images/methodology/04-donusum-icin-tasarla.jpg',
            r'\"media\":{\"mediaItemUrl\":\"https://roasist.github.io/roasist-web/images/methodology/04-donusum-icin-tasarla.jpg\",\"mimeType\":\"video/mp4\"},\"image\":{\"mediaItemUrl\":\"https://roasist.github.io/roasist-web/images/methodology/04-donusum-icin-tasarla.jpg',
        )
        html = re.sub(
            r'https://kota-content\.b-cdn\.net/app/uploads/2026/07/create-to-convert\.jpg',
            "https://roasist.github.io/roasist-web/images/methodology/04-donusum-icin-tasarla.jpg",
            html,
        )
        html = re.sub(
            r'https://kota-content\.b-cdn\.net/app/uploads/2026/07/build-for-scale-V3\.jpg',
            "https://roasist.github.io/roasist-web/images/methodology/05-olceklenebilir-buyume.jpg",
            html,
        )

        if "</body>" in html:
            html = html.replace("</body>", KINETIC_3D_BLOCK + "</body>", 1)

        if protected is not None:
            html = html.replace("__PROTECTED_T712_BLOCK__", protected)

        p.write_text(html, encoding="utf-8")
        print(f"Injected Slides 1, 2, 3, 4 & 5 Canvas + removed video loads in {rel}")


if __name__ == "__main__":
    main()



