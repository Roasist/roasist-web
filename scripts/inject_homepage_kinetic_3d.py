"""Inject the 60 FPS HTML + CSS + Canvas animations for Slides 1, 2, 3 & 4:
  - Slide 1 ('Önce veri ve strateji'): 3D Z-Axis Kinetic Typography (15 words)
  - Slide 2 ('Yaratıcı ve cesur fikir'): 3D Perspective Creative Bento & Particle Sphere
  - Slide 3 ('Kusursuz süreç yönetimi'): Agile Sprint Kanban Board & Real-Time ROAS Momentum Cockpit
  - Slide 4 ('Dönüşüm için tasarla'): 3-Shot Dynamic B-Roll (UX & CRO + Technical SEO 100/100 + 3D Funnel ROAS Multiplier)
and eliminate the MP4 video downloads for Slides 1, 2, 3 & 4 across public/ and dist/."""

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
html body #carousel .swiper-slide:nth-child(4) .CarouselSlides_carouselMedia__aqYWx {
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

html body #carousel .swiper-slide:nth-child(1) .CarouselSlides_carouselMedia__aqYWx video,
html body #carousel .swiper-slide:nth-child(2) .CarouselSlides_carouselMedia__aqYWx video,
html body #carousel .swiper-slide:nth-child(3) .CarouselSlides_carouselMedia__aqYWx video,
html body #carousel .swiper-slide:nth-child(4) .CarouselSlides_carouselMedia__aqYWx video {
  display: none !important;
}

html body .roasist-kinetic-3d-canvas,
html body .roasist-creative-bento-canvas,
html body .roasist-process-cockpit-canvas,
html body .roasist-convert-broll-canvas {
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
  // SLIDE 4: "Dönüşüm için tasarla" — 3-Shot Dynamic B-Roll (UX, SEO & Funnel)
  // ==========================================================================
  function drawCursorS4(c, x, y, scale = 1, isClicking = false) {
    c.save();
    c.translate(x, y);
    c.scale(scale, scale);

    if (isClicking) {
      c.beginPath();
      c.arc(0, 0, 22, 0, Math.PI * 2);
      c.strokeStyle = 'rgba(16, 185, 129, 0.75)';
      c.lineWidth = 2.2;
      c.stroke();
    }

    c.shadowColor = 'rgba(0, 0, 0, 0.65)';
    c.shadowBlur = 12;
    c.beginPath();
    c.moveTo(0, 0);
    c.lineTo(0, 22);
    c.lineTo(6, 17);
    c.lineTo(11, 26);
    c.lineTo(15, 24);
    c.lineTo(10, 15);
    c.lineTo(18, 15);
    c.closePath();
    c.fillStyle = '#FFFFFF';
    c.fill();
    c.strokeStyle = '#0B0914';
    c.lineWidth = 1.6;
    c.stroke();
    c.restore();
  }

  const bokehNodesS4 = Array.from({ length: 28 }, (_, i) => ({
    x: ((i * 197) % 1020),
    y: ((i * 313) % 788),
    r: 2 + (i % 4) * 1.4,
    vx: (i % 2 === 0 ? 1 : -1) * (10 + (i % 5) * 4),
    vy: -12 - (i % 6) * 4,
    color: i % 3 === 0 ? '#A78BFA' : (i % 3 === 1 ? '#7601FF' : '#10B981'),
    alpha: 0.12 + (i % 4) * 0.06
  }));

  function drawAmbientBrollBackdropS4(c, elapsed) {
    const g = c.createRadialGradient(510, 394, 40, 510, 394, 580);
    g.addColorStop(0, 'rgba(118, 1, 255, 0.14)');
    g.addColorStop(0.55, 'rgba(16, 185, 129, 0.04)');
    g.addColorStop(1, 'rgba(11, 9, 20, 0)');
    c.fillStyle = g;
    c.fillRect(0, 0, 1020, 788);

    c.save();
    c.strokeStyle = 'rgba(167, 139, 250, 0.045)';
    c.lineWidth = 1;
    const shift = (elapsed * 24) % 60;
    for (let x = -60 + shift; x < 1080; x += 60) {
      c.beginPath();
      c.moveTo(x, 0);
      c.lineTo(x, 788);
      c.stroke();
    }
    for (let y = -60 + shift; y < 840; y += 60) {
      c.beginPath();
      c.moveTo(0, y);
      c.lineTo(1020, y);
      c.stroke();
    }
    c.restore();

    c.save();
    for (const b of bokehNodesS4) {
      const px = (b.x + elapsed * b.vx + 10200) % 1020;
      const py = (b.y + elapsed * b.vy + 7880) % 788;
      c.beginPath();
      c.arc(px, py, b.r, 0, Math.PI * 2);
      c.fillStyle = b.color;
      c.globalAlpha = b.alpha;
      c.fill();
    }
    c.restore();
  }

  function drawBrollShot1UX(c, p, alpha, elapsed) {
    if (alpha <= 0.005) return;
    c.save();
    c.globalAlpha = alpha;

    const camScale = lerpS3(1.06, 0.99, smoothstepS3(0, 1, p));
    const camX = lerpS3(-18, 12, p);
    const camY = lerpS3(14, -8, p);
    c.translate(510 + camX, 394 + camY);
    c.scale(camScale, camScale);
    c.translate(-510, -394);

    const px = 28, py = 24, pw = 964, ph = 684;
    roundRectPath(c, px, py, pw, ph, 22);
    c.fillStyle = '#0E0C1A';
    c.fill();
    c.strokeStyle = 'rgba(167, 139, 250, 0.20)';
    c.lineWidth = 1.4;
    c.stroke();

    drawBadgeS3(c, px + 28, py + 24, 'B-ROLL 01 / UX & CRO MİMARİSİ', 'rgba(118, 1, 255, 0.22)', '#D8B4FE', 'rgba(167, 139, 250, 0.35)', 10.5, 12, 5, '#A78BFA');

    c.fillStyle = '#E2E8F0';
    c.font = `600 14px 'Inter', sans-serif`;
    c.textAlign = 'left';
    c.textBaseline = 'middle';
    c.fillText('Mikro-Etkileşim, Isı Haritası & Dönüşüm Optimizasyonu', px + 246, py + 35);

    const scanT = smoothstepS3(0.16, 0.58, p);
    const isOptimized = scanT > 0.52;
    const cvrVal = lerpS3(1.82, 4.94, scanT);
    const roasVal = lerpS3(2.4, 6.4, scanT);

    drawBadgeS3(
      c, px + pw - 210, py + 22,
      isOptimized ? 'VARYASYON B · KAZANAN' : 'VARYASYON A · ANALİZ',
      isOptimized ? 'rgba(16, 185, 129, 0.16)' : 'rgba(255, 255, 255, 0.07)',
      isOptimized ? '#6EE7B7' : '#94A3B8',
      isOptimized ? 'rgba(16, 185, 129, 0.35)' : null,
      10.5, 12, 6,
      isOptimized ? '#10B981' : '#94A3B8'
    );

    const uxX = px + 28, uxY = py + 68, uxW = 576, uxH = 588;
    roundRectPath(c, uxX, uxY, uxW, uxH, 18);
    c.fillStyle = '#131122';
    c.fill();
    c.strokeStyle = isOptimized ? 'rgba(167, 139, 250, 0.32)' : 'rgba(255, 255, 255, 0.08)';
    c.lineWidth = 1.2;
    c.stroke();

    c.fillStyle = 'rgba(255,255,255,0.04)';
    roundRectPath(c, uxX + 14, uxY + 14, uxW - 28, 34, 10);
    c.fill();
    const dots = ['#EF4444', '#F59E0B', '#10B981'];
    for (let i = 0; i < 3; i++) {
      c.beginPath();
      c.arc(uxX + 30 + i * 14, uxY + 31, 4, 0, Math.PI * 2);
      c.fillStyle = dots[i];
      c.globalAlpha = alpha * 0.7;
      c.fill();
    }
    c.globalAlpha = alpha;
    c.fillStyle = '#94A3B8';
    c.font = `500 11px 'Inter', sans-serif`;
    c.textAlign = 'left';
    c.fillText('store.markaniz.com/premium-seri — Hız: 0.6sn LCP', uxX + 82, uxY + 31.5);

    const imgX = uxX + 22, imgY = uxY + 64, imgW = 240, imgH = 290;
    roundRectPath(c, imgX, imgY, imgW, imgH, 14);
    const prodGrad = c.createLinearGradient(imgX, imgY, imgX + imgW, imgY + imgH);
    prodGrad.addColorStop(0, '#231742');
    prodGrad.addColorStop(0.5, '#17122B');
    prodGrad.addColorStop(1, '#101E24');
    c.fillStyle = prodGrad;
    c.fill();
    c.strokeStyle = 'rgba(167, 139, 250, 0.24)';
    c.stroke();

    c.save();
    c.beginPath();
    c.arc(imgX + imgW * 0.5, imgY + imgH * 0.46, 62, 0, Math.PI * 2);
    const orbG = c.createRadialGradient(imgX + imgW * 0.42, imgY + imgH * 0.38, 8, imgX + imgW * 0.5, imgY + imgH * 0.46, 66);
    orbG.addColorStop(0, '#DDD6FE');
    orbG.addColorStop(0.45, '#7601FF');
    orbG.addColorStop(1, 'rgba(19, 17, 34, 0.1)');
    c.fillStyle = orbG;
    c.shadowColor = '#7601FF';
    c.shadowBlur = 28;
    c.fill();
    c.restore();

    if (scanT > 0.25) {
      c.save();
      c.globalAlpha = alpha * smoothstepS3(0.25, 0.55, scanT);
      drawBadgeS3(c, imgX + 14, imgY + 14, 'ÇOK SATAN · %98 MEMNUNİYET', 'rgba(11, 9, 20, 0.82)', '#6EE7B7', 'rgba(16, 185, 129, 0.4)', 9.5, 10, 4, '#10B981');
      c.restore();
    }

    c.fillStyle = '#E2E8F0';
    c.font = `700 12px 'Inter', sans-serif`;
    c.textAlign = 'center';
    c.fillText('Kreatif Görsel Optimizasyonu', imgX + imgW * 0.5, imgY + imgH - 36);
    c.fillStyle = '#A78BFA';
    c.font = `600 11px 'Inter', sans-serif`;
    c.fillText('Görsel Dikkat Skoru: 96/100', imgX + imgW * 0.5, imgY + imgH - 18);

    const dx = imgX + imgW + 24;
    const dw = uxW - (dx - uxX) - 22;

    c.textAlign = 'left';
    c.fillStyle = isOptimized ? '#10B981' : '#64748B';
    c.font = `700 11.5px 'Inter', sans-serif`;
    c.fillText(isOptimized ? '★★★★★  4.9/5 · 2.480+ Doğrulanmış Deneyim' : '★★★☆☆  Standart Ürün Görünümü', dx, imgY + 18);

    c.fillStyle = '#FFFFFF';
    c.font = `800 20px 'Inter', sans-serif`;
    if ('letterSpacing' in c) c.letterSpacing = '-0.025em';
    c.fillText('Dönüşüm Odaklı UX', dx, imgY + 50);
    c.fillText('& Satın Alma Akışı', dx, imgY + 76);

    const bullets = [
      { text: 'Sürtünmesiz Tek Sayfa Checkout', active: scanT > 0.30 },
      { text: 'Dinamik Teslimat & Güven Rozetleri', active: scanT > 0.45 },
      { text: 'Kişiselleştirilmiş Teklif Kurgusu', active: scanT > 0.60 }
    ];
    for (let i = 0; i < bullets.length; i++) {
      const by = imgY + 112 + i * 32;
      roundRectPath(c, dx, by - 11, dw, 24, 7);
      c.fillStyle = bullets[i].active ? 'rgba(118, 1, 255, 0.14)' : 'rgba(255, 255, 255, 0.04)';
      c.fill();

      c.beginPath();
      c.arc(dx + 12, by + 1, 4, 0, Math.PI * 2);
      c.fillStyle = bullets[i].active ? '#10B981' : '#475569';
      c.fill();

      c.fillStyle = bullets[i].active ? '#F8FAFC' : '#94A3B8';
      c.font = `600 11.5px 'Inter', sans-serif`;
      if ('letterSpacing' in c) c.letterSpacing = '0px';
      c.fillText(bullets[i].text, dx + 24, by + 1.5);
    }

    const clickPhase = smoothstepS3(0.56, 0.72, p);
    const isClickMoment = p > 0.64 && p < 0.84;
    const btnPulse = isClickMoment ? 1 + Math.sin((p - 0.64) * Math.PI * 5) * 0.028 : 1;

    const btnX = dx, btnY = imgY + 224, btnW = dw, btnH = 54;
    c.save();
    c.translate(btnX + btnW * 0.5, btnY + btnH * 0.5);
    c.scale(btnPulse, btnPulse);
    c.translate(-(btnX + btnW * 0.5), -(btnY + btnH * 0.5));

    if (isOptimized) {
      c.shadowColor = isClickMoment ? 'rgba(16, 185, 129, 0.65)' : 'rgba(118, 1, 255, 0.55)';
      c.shadowBlur = isClickMoment ? 28 : 18;
    }
    roundRectPath(c, btnX, btnY, btnW, btnH, 14);
    const btnGrad = c.createLinearGradient(btnX, btnY, btnX + btnW, btnY);
    if (isClickMoment) {
      btnGrad.addColorStop(0, '#059669');
      btnGrad.addColorStop(1, '#10B981');
    } else if (isOptimized) {
      btnGrad.addColorStop(0, '#7601FF');
      btnGrad.addColorStop(1, '#9333EA');
    } else {
      btnGrad.addColorStop(0, '#334155');
      btnGrad.addColorStop(1, '#1E293B');
    }
    c.fillStyle = btnGrad;
    c.fill();
    c.shadowBlur = 0;

    c.fillStyle = '#FFFFFF';
    c.font = `800 13.5px 'Inter', sans-serif`;
    c.textAlign = 'center';
    c.fillText(
      isClickMoment ? '✓ DÖNÜŞÜM GERÇEKLEŞTİ (+%172 CVR)' : 'HEMEN SEPETE EKLE · HIZLI TESLİMAT',
      btnX + btnW * 0.5,
      btnY + btnH * 0.5 + 0.5
    );
    c.restore();

    const hmX = uxX + 22, hmY = imgY + imgH + 18, hmW = uxW - 44, hmH = 194;
    roundRectPath(c, hmX, hmY, hmW, hmH, 14);
    c.fillStyle = '#0F0D1C';
    c.fill();
    c.strokeStyle = 'rgba(255, 255, 255, 0.07)';
    c.stroke();

    c.fillStyle = '#94A3B8';
    c.font = `700 10.5px 'Inter', sans-serif`;
    c.textAlign = 'left';
    c.fillText('CANLI KULLANICI DENEYİMİ (UX) & DİKKAT ISI HARİTASI', hmX + 18, hmY + 24);

    c.textAlign = 'right';
    c.fillStyle = '#6EE7B7';
    c.font = `600 11px 'Inter', sans-serif`;
    c.fillText('Form Terk Oranı: -%48 Düşürüldü', hmX + hmW - 18, hmY + 24);

    const steps = [
      { label: '1. Görsel Kanca Dikkat', val: 96, col: '#A78BFA' },
      { label: '2. Ürün Değer Önerisi', val: 88, col: '#8B5CF6' },
      { label: '3. Sepet Mikro-Etkileşim', val: Math.round(lerpS3(42, 82, scanT)), col: '#7601FF' },
      { label: '4. Satın Alma Tamamlama', val: Math.round(lerpS3(31, 76, scanT)), col: '#10B981' }
    ];
    for (let i = 0; i < 4; i++) {
      const sy = hmY + 52 + i * 34;
      c.fillStyle = '#CBD5E1';
      c.font = `500 11.5px 'Inter', sans-serif`;
      c.textAlign = 'left';
      c.fillText(steps[i].label, hmX + 18, sy);

      const bx = hmX + 190, bw = hmW - 260, bh = 9;
      roundRectPath(c, bx, sy - 5, bw, bh, 99);
      c.fillStyle = 'rgba(255,255,255,0.07)';
      c.fill();

      roundRectPath(c, bx, sy - 5, bw * (steps[i].val / 100), bh, 99);
      c.fillStyle = steps[i].col;
      c.fill();

      c.fillStyle = '#FFFFFF';
      c.font = `700 11.5px 'Inter', sans-serif`;
      c.textAlign = 'right';
      c.fillText(`%${steps[i].val}`, hmX + hmW - 18, sy);
    }

    const heatSpots = [
      { x: btnX + btnW * 0.55, y: btnY + btnH * 0.5, r: 48 },
      { x: imgX + imgW * 0.5, y: imgY + imgH * 0.45, r: 54 }
    ];
    for (const hs of heatSpots) {
      c.save();
      const hg = c.createRadialGradient(hs.x, hs.y, 4, hs.x, hs.y, hs.r);
      hg.addColorStop(0, 'rgba(16, 185, 129, 0.38)');
      hg.addColorStop(0.5, 'rgba(118, 1, 255, 0.22)');
      hg.addColorStop(1, 'rgba(118, 1, 255, 0)');
      c.fillStyle = hg;
      c.beginPath();
      c.arc(hs.x, hs.y, hs.r, 0, Math.PI * 2);
      c.fill();
      c.restore();
    }

    if (p > 0.14 && p < 0.60) {
      const scanY = lerpS3(uxY + 10, uxY + uxH - 10, smoothstepS3(0.14, 0.60, p));
      c.save();
      c.strokeStyle = '#A78BFA';
      c.lineWidth = 2.2;
      c.shadowColor = '#7601FF';
      c.shadowBlur = 18;
      c.beginPath();
      c.moveTo(uxX + 8, scanY);
      c.lineTo(uxX + uxW - 8, scanY);
      c.stroke();
      c.restore();
    }

    const curX = lerpS3(uxX + 140, btnX + btnW * 0.62, clickPhase);
    const curY = lerpS3(uxY + 180, btnY + btnH * 0.58, clickPhase);
    drawCursorS4(c, curX, curY, 1.05, isClickMoment);

    const rx = uxX + uxW + 20, rw = pw - (rx - px) - 28;

    {
      const ky = uxY, kh = 184;
      roundRectPath(c, rx, ky, rw, kh, 18);
      const g = c.createLinearGradient(rx, ky, rx, ky + kh);
      g.addColorStop(0, '#1B1433');
      g.addColorStop(1, '#121020');
      c.fillStyle = g;
      c.fill();
      c.strokeStyle = 'rgba(167, 139, 250, 0.38)';
      c.lineWidth = 1.3;
      c.stroke();

      c.fillStyle = '#A78BFA';
      c.font = `700 10.5px 'Inter', sans-serif`;
      c.textAlign = 'left';
      c.fillText('DÖNÜŞÜM ORANI (CVR)', rx + 22, ky + 30);

      c.fillStyle = '#FFFFFF';
      c.font = `800 46px 'Inter', sans-serif`;
      if ('letterSpacing' in c) c.letterSpacing = '-0.03em';
      c.fillText(`%${cvrVal.toFixed(2)}`, rx + 22, ky + 88);

      drawBadgeS3(c, rx + 22, ky + 126, '+172% CRO Artışı', 'rgba(16, 185, 129, 0.16)', '#6EE7B7', 'rgba(16, 185, 129, 0.32)', 11, 12, 5, '#10B981');
    }

    {
      const ky = uxY + 202, kh = 184;
      roundRectPath(c, rx, ky, rw, kh, 18);
      c.fillStyle = '#131122';
      c.fill();
      c.strokeStyle = 'rgba(255, 255, 255, 0.08)';
      c.lineWidth = 1;
      c.stroke();

      c.fillStyle = '#94A3B8';
      c.font = `700 10.5px 'Inter', sans-serif`;
      c.textAlign = 'left';
      c.fillText('REKLAM VERİMLİLİĞİ (ROAS)', rx + 22, ky + 30);

      c.fillStyle = '#FFFFFF';
      c.font = `800 46px 'Inter', sans-serif`;
      if ('letterSpacing' in c) c.letterSpacing = '-0.03em';
      c.fillText(`${roasVal.toFixed(1)}x`, rx + 22, ky + 88);

      drawBadgeS3(c, rx + 22, ky + 126, 'Aynı Bütçeyle 2.6x Gelir', 'rgba(118, 1, 255, 0.24)', '#D8B4FE', null, 11, 12, 5);
    }

    {
      const ky = uxY + 404, kh = 184;
      roundRectPath(c, rx, ky, rw, kh, 18);
      c.fillStyle = '#131122';
      c.fill();
      c.strokeStyle = 'rgba(255, 255, 255, 0.08)';
      c.lineWidth = 1;
      c.stroke();

      c.fillStyle = '#94A3B8';
      c.font = `700 10.5px 'Inter', sans-serif`;
      c.textAlign = 'left';
      c.fillText('OPTİMİZE EDİLEN DETAYLAR', rx + 22, ky + 30);

      const checks = [
        'Görsel Hiyerarşi & Kontrast',
        'Mobil Başparmak Ergonomisi',
        'Mikro-Kopya & CTA Psikolojisi',
        'Anlık Hız & Sıfır Zıplama (CLS)'
      ];
      for (let i = 0; i < 4; i++) {
        const cy = ky + 62 + i * 28;
        c.fillStyle = '#10B981';
        c.font = `700 12px 'Inter', sans-serif`;
        c.fillText('✓', rx + 22, cy);
        c.fillStyle = '#E2E8F0';
        c.font = `500 12px 'Inter', sans-serif`;
        c.fillText(checks[i], rx + 40, cy);
      }
    }

    c.restore();
  }

  function drawBrollShot2SEO(c, p, alpha, elapsed) {
    if (alpha <= 0.005) return;
    c.save();
    c.globalAlpha = alpha;

    const camScale = lerpS3(0.96, 1.01, smoothstepS3(0, 1, p));
    const camX = lerpS3(14, -10, p);
    c.translate(510 + camX, 394);
    c.scale(camScale, camScale);
    c.translate(-510, -394);

    const px = 28, py = 24, pw = 964, ph = 684;
    roundRectPath(c, px, py, pw, ph, 22);
    c.fillStyle = '#0E0C1A';
    c.fill();
    c.strokeStyle = 'rgba(167, 139, 250, 0.20)';
    c.lineWidth = 1.4;
    c.stroke();

    drawBadgeS3(c, px + 28, py + 24, 'B-ROLL 02 / TEKNİK SEO & HIZ MİMARİSİ', 'rgba(16, 185, 129, 0.16)', '#6EE7B7', 'rgba(16, 185, 129, 0.35)', 10.5, 12, 5, '#10B981');

    c.fillStyle = '#E2E8F0';
    c.font = `600 14px 'Inter', sans-serif`;
    c.textAlign = 'left';
    c.textBaseline = 'middle';
    c.fillText('Core Web Vitals, Yapısal Veri (Schema) & Semantik Otorite', px + 286, py + 35);

    const dialProg = smoothstepS3(0.05, 0.72, p);

    const gauges = [
      { title: 'PERFORMANS & HIZ', score: Math.round(lerpS3(64, 100, dialProg)), sub: 'LCP: 0.6sn · Anında Açılış', col: '#10B981' },
      { title: 'TEKNİK SEO SKORU', score: Math.round(lerpS3(72, 100, dialProg)), sub: 'Sıfır Tarama Hatası', col: '#10B981' },
      { title: 'YAPISAL VERİ & AEO', score: Math.round(lerpS3(58, 99, dialProg)), sub: 'JSON-LD Product Schema', col: '#A78BFA' },
      { title: 'KULLANICI DENEYİMİ', score: Math.round(lerpS3(68, 100, dialProg)), sub: 'CLS: 0.00 · INP: 24ms', col: '#7601FF' }
    ];

    const gw = (pw - 56 - 48) / 4;
    const gh = 166;
    const gy = py + 68;

    for (let i = 0; i < 4; i++) {
      const gx = px + 28 + i * (gw + 16);
      roundRectPath(c, gx, gy, gw, gh, 16);
      c.fillStyle = '#131122';
      c.fill();
      c.strokeStyle = 'rgba(255, 255, 255, 0.08)';
      c.lineWidth = 1;
      c.stroke();

      const cx = gx + 54, cy = gy + 74, r = 34;
      c.beginPath();
      c.arc(cx, cy, r, 0, Math.PI * 2);
      c.strokeStyle = 'rgba(255, 255, 255, 0.08)';
      c.lineWidth = 6;
      c.stroke();

      const endAngle = -Math.PI * 0.5 + (Math.PI * 2) * (gauges[i].score / 100);
      c.save();
      c.beginPath();
      c.arc(cx, cy, r, -Math.PI * 0.5, endAngle);
      c.strokeStyle = gauges[i].col;
      c.lineWidth = 6;
      c.lineCap = 'round';
      c.shadowColor = gauges[i].col;
      c.shadowBlur = 12;
      c.stroke();
      c.restore();

      c.fillStyle = '#FFFFFF';
      c.font = `800 18px 'Inter', sans-serif`;
      c.textAlign = 'center';
      c.fillText(`${gauges[i].score}`, cx, cy + 1);

      c.textAlign = 'left';
      c.fillStyle = '#94A3B8';
      c.font = `700 9.5px 'Inter', sans-serif`;
      c.fillText(gauges[i].title, gx + 102, gy + 54);

      c.fillStyle = '#FFFFFF';
      c.font = `700 13px 'Inter', sans-serif`;
      c.fillText('Mükemmel', gx + 102, gy + 76);

      c.fillStyle = '#CBD5E1';
      c.font = `500 11px 'Inter', sans-serif`;
      c.fillText(gauges[i].sub, gx + 18, gy + 140);
    }

    const ax = px + 28, ay = gy + gh + 20, aw = 496, ah = 402;
    roundRectPath(c, ax, ay, aw, ah, 18);
    c.fillStyle = '#110F1E';
    c.fill();
    c.strokeStyle = 'rgba(167, 139, 250, 0.22)';
    c.stroke();

    c.fillStyle = '#FFFFFF';
    c.font = `700 15px 'Inter', sans-serif`;
    c.textAlign = 'left';
    c.fillText('Teknik SEO & Semantik İçerik Mimarisi', ax + 22, ay + 30);

    c.fillStyle = '#94A3B8';
    c.font = `500 11.5px 'Inter', sans-serif`;
    c.fillText('Arama motoru botları ve AI yanıt motorları (AEO) için kusursuz hiyerarşi', ax + 22, ay + 50);

    const rootNode = { x: ax + aw * 0.5, y: ay + 102, label: 'ANA OTORİTE DOMAİN (SSR · 0.6sn)' };
    const midNodes = [
      { x: ax + 90, y: ay + 206, label: 'Kümelenmiş Kategori' },
      { x: ax + aw * 0.5, y: ay + 206, label: 'JSON-LD Schema.org' },
      { x: ax + aw - 90, y: ay + 206, label: 'AI Arama (AEO) Özeti' }
    ];
    const leafNodes = [
      { x: ax + 90, y: ay + 322, label: 'Yüksek Niyetli Kelime', stat: '#1 Sıra' },
      { x: ax + aw * 0.5, y: ay + 322, label: 'Rich Snippet Sonuç', stat: '+%84 CTR' },
      { x: ax + aw - 90, y: ay + 322, label: 'Organik Büyüme', stat: 'Sürekli ROAS' }
    ];

    c.save();
    for (let i = 0; i < 3; i++) {
      c.beginPath();
      c.moveTo(rootNode.x, rootNode.y + 20);
      c.lineTo(midNodes[i].x, midNodes[i].y - 18);
      c.lineTo(leafNodes[i].x, leafNodes[i].y - 24);
      c.strokeStyle = 'rgba(167, 139, 250, 0.28)';
      c.lineWidth = 1.6;
      c.stroke();

      const pulseT = ((elapsed * 0.9) + i * 0.33) % 1.0;
      const px1 = pulseT < 0.5
        ? lerpS3(rootNode.x, midNodes[i].x, pulseT * 2)
        : lerpS3(midNodes[i].x, leafNodes[i].x, (pulseT - 0.5) * 2);
      const py1 = pulseT < 0.5
        ? lerpS3(rootNode.y + 20, midNodes[i].y - 18, pulseT * 2)
        : lerpS3(midNodes[i].y - 18, leafNodes[i].y - 24, (pulseT - 0.5) * 2);

      c.beginPath();
      c.arc(px1, py1, 4.5, 0, Math.PI * 2);
      c.fillStyle = '#10B981';
      c.shadowColor = '#10B981';
      c.shadowBlur = 10;
      c.fill();
      c.shadowBlur = 0;
    }
    c.restore();

    roundRectPath(c, rootNode.x - 135, rootNode.y - 20, 270, 40, 12);
    c.fillStyle = '#7601FF';
    c.fill();
    c.fillStyle = '#FFFFFF';
    c.font = `700 11.5px 'Inter', sans-serif`;
    c.textAlign = 'center';
    c.fillText(rootNode.label, rootNode.x, rootNode.y + 0.5);

    for (let i = 0; i < 3; i++) {
      roundRectPath(c, midNodes[i].x - 68, midNodes[i].y - 18, 136, 36, 10);
      c.fillStyle = '#19152E';
      c.fill();
      c.strokeStyle = 'rgba(167, 139, 250, 0.4)';
      c.stroke();
      c.fillStyle = '#E2E8F0';
      c.font = `600 10.5px 'Inter', sans-serif`;
      c.fillText(midNodes[i].label, midNodes[i].x, midNodes[i].y + 0.5);

      roundRectPath(c, leafNodes[i].x - 68, leafNodes[i].y - 24, 136, 56, 12);
      c.fillStyle = '#131D22';
      c.fill();
      c.strokeStyle = 'rgba(16, 185, 129, 0.38)';
      c.stroke();
      c.fillStyle = '#FFFFFF';
      c.font = `600 10.5px 'Inter', sans-serif`;
      c.fillText(leafNodes[i].label, leafNodes[i].x, leafNodes[i].y - 6);
      c.fillStyle = '#6EE7B7';
      c.font = `800 12px 'Inter', sans-serif`;
      c.fillText(leafNodes[i].stat, leafNodes[i].x, leafNodes[i].y + 14);
    }

    const sx = ax + aw + 16, sw = pw - (sx - px) - 28, sh = ah;
    roundRectPath(c, sx, ay, sw, sh, 18);
    c.fillStyle = '#110F1E';
    c.fill();
    c.strokeStyle = 'rgba(255, 255, 255, 0.08)';
    c.stroke();

    c.fillStyle = '#FFFFFF';
    c.font = `700 14.5px 'Inter', sans-serif`;
    c.textAlign = 'left';
    c.fillText('Arama Sonucu (SERP) & Zengin Kart', sx + 20, ay + 30);

    const cardX = sx + 18, cardY = ay + 56, cardW = sw - 36, cardH = 194;
    roundRectPath(c, cardX, cardY, cardW, cardH, 14);
    c.fillStyle = '#171429';
    c.fill();
    c.strokeStyle = 'rgba(167, 139, 250, 0.35)';
    c.stroke();

    drawBadgeS3(c, cardX + 14, cardY + 14, '#1 ORGANİK SIRALAMA · ZENGİN SONUÇ', 'rgba(16, 185, 129, 0.16)', '#6EE7B7', null, 9.5, 10, 4, '#10B981');

    c.fillStyle = '#C4B5FD';
    c.font = `700 13.5px 'Inter', sans-serif`;
    c.textAlign = 'left';
    c.fillText('Markanız — Yüksek Dönüşümlü Çözümler', cardX + 14, cardY + 58);

    c.fillStyle = '#10B981';
    c.font = `600 10.5px 'Inter', sans-serif`;
    c.fillText('★★★★★ 4.9/5 · 2.480 Yorum · Stokta · Hızlı Kargo', cardX + 14, cardY + 82);

    c.fillStyle = '#94A3B8';
    c.font = `500 10.5px 'Inter', sans-serif`;
    c.fillText('Teknik SEO ve yapısal veri mimarisiyle arama sonuçlarında', cardX + 14, cardY + 108);
    c.fillText('rakiplerden 2 kat fazla alan kaplayan yüksek CTR görünümü.', cardX + 14, cardY + 126);

    const links = ['Hızlı Teklif Al', 'Birim Ekonomisi', 'Vaka Analizi'];
    for (let i = 0; i < 3; i++) {
      drawBadgeS3(c, cardX + 14 + i * 106, cardY + 148, links[i], 'rgba(118, 1, 255, 0.22)', '#DDD6FE', null, 9.5, 9, 4);
    }

    const metY = cardY + cardH + 18;
    roundRectPath(c, cardX, metY, cardW, 114, 14);
    c.fillStyle = '#141125';
    c.fill();
    c.strokeStyle = 'rgba(16, 185, 129, 0.25)';
    c.stroke();

    const ctrVal = lerpS3(3.4, 8.9, dialProg);
    c.fillStyle = '#94A3B8';
    c.font = `700 10px 'Inter', sans-serif`;
    c.fillText('ORGANİK TIKLAMA ORANI (CTR)', cardX + 18, metY + 28);

    c.fillStyle = '#FFFFFF';
    c.font = `800 34px 'Inter', sans-serif`;
    c.fillText(`%${ctrVal.toFixed(1)}`, cardX + 18, metY + 72);

    drawBadgeS3(c, cardX + 136, metY + 56, '+%162 Organik Trafik', 'rgba(16, 185, 129, 0.16)', '#6EE7B7', null, 10.5, 10, 5, '#10B981');

    c.restore();
  }

  function drawBrollShot3Funnel(c, p, alpha, elapsed) {
    if (alpha <= 0.005) return;
    c.save();
    c.globalAlpha = alpha;

    const camScale = lerpS3(1.04, 0.99, smoothstepS3(0, 1, p));
    c.translate(510, 394);
    c.scale(camScale, camScale);
    c.translate(-510, -394);

    const px = 28, py = 24, pw = 964, ph = 684;
    roundRectPath(c, px, py, pw, ph, 22);
    c.fillStyle = '#0E0C1A';
    c.fill();
    c.strokeStyle = 'rgba(167, 139, 250, 0.20)';
    c.lineWidth = 1.4;
    c.stroke();

    drawBadgeS3(c, px + 28, py + 24, 'B-ROLL 03 / TAM HUNİ DÖNÜŞÜM ÇARPANI', 'rgba(118, 1, 255, 0.24)', '#DDD6FE', 'rgba(167, 139, 250, 0.4)', 10.5, 12, 5, '#10B981');

    c.fillStyle = '#E2E8F0';
    c.font = `600 14px 'Inter', sans-serif`;
    c.textAlign = 'left';
    c.textBaseline = 'middle';
    c.fillText('Kreatif + Teknik SEO + UX Akışı = Maksimum ROAS & Kârlı Büyüme', px + 306, py + 35);

    const flowT = smoothstepS3(0.05, 0.80, p);

    const sources = [
      { y: py + 150, tag: '01 · KREATİF GÖRSELLER', title: 'Yüksek Dikkat Çeken Reklam & Video Kancaları', metric: '+%64 Tıklama Oranı', col: '#A78BFA' },
      { y: py + 340, tag: '02 · TEKNİK SEO MİMARİSİ', title: '0.6sn Açılış Hızı & #1 Organik Arama Görünürlüğü', metric: '100/100 Core Web Vitals', col: '#8B5CF6' },
      { y: py + 530, tag: '03 · KULLANICI DENEYİMİ (UX)', title: 'Sürtünmesiz Akış, Isı Haritası & Checkout CRO', metric: '+%172 Dönüşüm Oranı', col: '#10B981' }
    ];

    const centerHubX = px + 560, centerHubY = py + 375;

    for (let i = 0; i < 3; i++) {
      const sy = sources[i].y + 38;
      const sx = px + 380;

      c.save();
      c.beginPath();
      c.moveTo(sx, sy);
      c.bezierCurveTo(sx + 90, sy, centerHubX - 90, centerHubY, centerHubX, centerHubY);
      c.strokeStyle = sources[i].col;
      c.globalAlpha = alpha * 0.35;
      c.lineWidth = 3;
      c.stroke();
      c.restore();

      for (let k = 0; k < 4; k++) {
        const t = ((elapsed * 0.75) + k * 0.25 + i * 0.15) % 1.0;
        const inv = 1 - t;
        const c1x = sx + 90, c1y = sy;
        const c2x = centerHubX - 90, c2y = centerHubY;
        const bx = inv * inv * inv * sx + 3 * inv * inv * t * c1x + 3 * inv * t * t * c2x + t * t * t * centerHubX;
        const by = inv * inv * inv * sy + 3 * inv * inv * t * c1y + 3 * inv * t * t * c2y + t * t * t * centerHubY;

        c.save();
        c.beginPath();
        c.arc(bx, by, 5, 0, Math.PI * 2);
        c.fillStyle = '#FFFFFF';
        c.shadowColor = sources[i].col;
        c.shadowBlur = 14;
        c.fill();
        c.restore();
      }

      roundRectPath(c, px + 28, sources[i].y - 24, 356, 124, 16);
      c.fillStyle = '#131122';
      c.fill();
      c.strokeStyle = 'rgba(167, 139, 250, 0.22)';
      c.lineWidth = 1.2;
      c.stroke();

      c.fillStyle = sources[i].col;
      c.font = `700 10.5px 'Inter', sans-serif`;
      c.textAlign = 'left';
      c.fillText(sources[i].tag, px + 48, sources[i].y + 4);

      c.fillStyle = '#FFFFFF';
      c.font = `600 13.5px 'Inter', sans-serif`;
      c.fillText(sources[i].title, px + 48, sources[i].y + 34);

      drawBadgeS3(c, px + 48, sources[i].y + 56, sources[i].metric, 'rgba(255, 255, 255, 0.06)', '#E2E8F0', null, 10.5, 10, 4, sources[i].col);
    }

    const rx = px + 468, ry = py + 112, rw = 468, rh = 526;
    roundRectPath(c, rx, ry, rw, rh, 22);
    const hubGrad = c.createLinearGradient(rx, ry, rx + rw, ry + rh);
    hubGrad.addColorStop(0, '#1C1338');
    hubGrad.addColorStop(0.6, '#120F24');
    hubGrad.addColorStop(1, '#0F1E22');
    c.fillStyle = hubGrad;
    c.fill();
    c.strokeStyle = 'rgba(167, 139, 250, 0.42)';
    c.lineWidth = 1.6;
    c.stroke();

    const ringX = rx + rw * 0.5, ringY = ry + 168, ringR = 88;
    c.save();
    for (let r = 0; r < 3; r++) {
      c.beginPath();
      c.arc(ringX, ringY, ringR + r * 18, 0, Math.PI * 2);
      c.strokeStyle = `rgba(167, 139, 250, ${0.18 - r * 0.05})`;
      c.lineWidth = 1.2;
      c.stroke();
    }

    c.beginPath();
    c.arc(ringX, ringY, ringR, 0, Math.PI * 2);
    const coreG = c.createRadialGradient(ringX, ringY, 10, ringX, ringY, ringR);
    coreG.addColorStop(0, 'rgba(118, 1, 255, 0.55)');
    coreG.addColorStop(1, 'rgba(19, 17, 34, 0.85)');
    c.fillStyle = coreG;
    c.shadowColor = '#7601FF';
    c.shadowBlur = 32;
    c.fill();
    c.shadowBlur = 0;
    c.strokeStyle = '#A78BFA';
    c.lineWidth = 2.5;
    c.stroke();

    const finalRoas = lerpS3(3.8, 6.8, flowT);
    c.fillStyle = '#D8B4FE';
    c.font = `700 10.5px 'Inter', sans-serif`;
    c.textAlign = 'center';
    c.fillText('BİRLEŞİK ETKİ', ringX, ringY - 32);

    c.fillStyle = '#FFFFFF';
    c.font = `800 44px 'Inter', sans-serif`;
    if ('letterSpacing' in c) c.letterSpacing = '-0.03em';
    c.fillText(`${finalRoas.toFixed(1)}x`, ringX, ringY + 8);

    c.fillStyle = '#6EE7B7';
    c.font = `700 12px 'Inter', sans-serif`;
    c.fillText('ORTALAMA ROAS', ringX, ringY + 38);
    c.restore();

    const b1x = rx + 26, b2x = rx + rw * 0.5 + 10, bw = rw * 0.5 - 36, by = ry + 306, bh = 116;

    roundRectPath(c, b1x, by, bw, bh, 14);
    c.fillStyle = 'rgba(255, 255, 255, 0.04)';
    c.fill();
    c.strokeStyle = 'rgba(255, 255, 255, 0.08)';
    c.stroke();

    c.fillStyle = '#94A3B8';
    c.font = `700 10px 'Inter', sans-serif`;
    c.textAlign = 'left';
    c.fillText('ETKİLEŞİM ARTIŞI', b1x + 18, by + 28);
    c.fillStyle = '#FFFFFF';
    c.font = `800 32px 'Inter', sans-serif`;
    c.fillText(`+%${Math.round(lerpS3(64, 148, flowT))}`, b1x + 18, by + 68);
    c.fillStyle = '#A78BFA';
    c.font = `600 11px 'Inter', sans-serif`;
    c.fillText('Nitelikli Oturum Süresi', b1x + 18, by + 96);

    roundRectPath(c, b2x, by, bw, bh, 14);
    c.fillStyle = 'rgba(16, 185, 129, 0.08)';
    c.fill();
    c.strokeStyle = 'rgba(16, 185, 129, 0.28)';
    c.stroke();

    c.fillStyle = '#6EE7B7';
    c.font = `700 10px 'Inter', sans-serif`;
    c.fillText('MÜŞTERİ EDİNME (CPA)', b2x + 18, by + 28);
    c.fillStyle = '#FFFFFF';
    c.font = `800 32px 'Inter', sans-serif`;
    c.fillText(`-%${Math.round(lerpS3(18, 42, flowT))}`, b2x + 18, by + 68);
    c.fillStyle = '#6EE7B7';
    c.font = `600 11px 'Inter', sans-serif`;
    c.fillText('Daha Düşük Maliyet', b2x + 18, by + 96);

    roundRectPath(c, rx + 26, ry + 442, rw - 52, 58, 12);
    c.fillStyle = 'rgba(118, 1, 255, 0.18)';
    c.fill();
    c.fillStyle = '#FFFFFF';
    c.font = `600 11.5px 'Inter', sans-serif`;
    c.textAlign = 'center';
    c.fillText('Her görsel, her kod satırı ve her UX adımı dönüşüm için tasarlanır.', rx + rw * 0.5, ry + 471);

    c.restore();
  }

  function drawBrollTimelineBar(c, cycleTime) {
    c.save();
    const barW = 964, barH = 38, bx = 28, by = 724;
    roundRectPath(c, bx, by, barW, barH, 12);
    c.fillStyle = 'rgba(14, 12, 26, 0.9)';
    c.fill();
    c.strokeStyle = 'rgba(255, 255, 255, 0.08)';
    c.lineWidth = 1;
    c.stroke();

    const labels = [
      '01 · UX & CRO MİKRO-ETKİLEŞİM',
      '02 · TEKNİK SEO & 100/100 HIZ',
      '03 · TAM HUNİ ROAS ÇARPANI'
    ];
    const activeShot = Math.floor(cycleTime / 4.0);
    const segW = (barW - 24) / 3;

    for (let i = 0; i < 3; i++) {
      const sx = bx + 12 + i * segW;
      const isCurrent = i === activeShot;
      const shotProg = isCurrent ? (cycleTime - i * 4.0) / 4.0 : (i < activeShot ? 1 : 0);

      roundRectPath(c, sx + 4, by + 27, segW - 12, 4, 99);
      c.fillStyle = 'rgba(255, 255, 255, 0.08)';
      c.fill();

      if (shotProg > 0) {
        roundRectPath(c, sx + 4, by + 27, (segW - 12) * shotProg, 4, 99);
        c.fillStyle = isCurrent ? '#A78BFA' : '#10B981';
        c.fill();
      }

      c.fillStyle = isCurrent ? '#FFFFFF' : '#94A3B8';
      c.font = `${isCurrent ? 700 : 500} 10.5px 'Inter', sans-serif`;
      c.textAlign = 'left';
      c.textBaseline = 'middle';
      c.fillText(labels[i], sx + 6, by + 15);
    }
    c.restore();
  }

  function renderSlide4ConvertBroll(ctx, width, height, dpr, elapsed) {
    const CYCLE_SECONDS = 12.0;
    const cycleTime = elapsed % CYCLE_SECONDS;

    ctx.save();
    ctx.scale(dpr, dpr);

    ctx.fillStyle = '#0B0914';
    ctx.fillRect(0, 0, width, height);

    const scale = Math.min(width / 1020, height / 788);
    ctx.translate((width - 1020 * scale) * 0.5, (height - 788 * scale) * 0.5);
    ctx.scale(scale, scale);

    drawAmbientBrollBackdropS4(ctx, elapsed);

    const fade = 0.65;
    let a1 = 0, a2 = 0, a3 = 0;

    if (cycleTime < 4.0 - fade) {
      a1 = cycleTime < fade ? smoothstepS3(0, fade, cycleTime) : 1;
      a3 = cycleTime < fade ? 1 - a1 : 0;
    } else if (cycleTime < 4.0) {
      const t = (cycleTime - (4.0 - fade)) / fade;
      a1 = 1 - smoothstepS3(0, 1, t);
      a2 = smoothstepS3(0, 1, t);
    } else if (cycleTime < 8.0 - fade) {
      a2 = 1;
    } else if (cycleTime < 8.0) {
      const t = (cycleTime - (8.0 - fade)) / fade;
      a2 = 1 - smoothstepS3(0, 1, t);
      a3 = smoothstepS3(0, 1, t);
    } else if (cycleTime < 12.0 - fade) {
      a3 = 1;
    } else {
      const t = (cycleTime - (12.0 - fade)) / fade;
      a3 = 1 - smoothstepS3(0, 1, t);
      a1 = smoothstepS3(0, 1, t);
    }

    const p1 = cycleTime < 4.0 ? cycleTime / 4.0 : 0.0;
    const p2 = cycleTime >= 3.35 && cycleTime < 8.0 ? Math.max(0, Math.min(1, (cycleTime - 4.0) / 4.0)) : 1.0;
    const p3 = cycleTime >= 7.35 ? Math.max(0, Math.min(1, (cycleTime - 8.0) / 4.0)) : 1.0;

    drawBrollShot1UX(ctx, p1, a1, elapsed);
    drawBrollShot2SEO(ctx, p2, a2, elapsed);
    drawBrollShot3Funnel(ctx, p3, a3, elapsed);
    drawBrollTimelineBar(ctx, cycleTime);

    ctx.restore();
  }

  // ==========================================================================
  // MOUNT & INTERSECTION OBSERVER LIFECYCLE
  // ==========================================================================
  let s1Canvas = null, s1Ctx = null, s1W = 562, s1H = 434, s1Dpr = 1;
  let s2Canvas = null, s2Ctx = null, s2W = 562, s2H = 434, s2Dpr = 1;
  let s3Canvas = null, s3Ctx = null, s3W = 562, s3H = 434, s3Dpr = 1;
  let s4Canvas = null, s4Ctx = null, s4W = 562, s4H = 434, s4Dpr = 1;
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
  }

  function tick(now) {
    ensureCanvasesMounted();

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
        renderSlide2Bento(s2Ctx, s2W, s2H, s2Dpr, elapsedSeconds);
      }

      // Render Slide 3 ("Kusursuz süreç yönetimi")
      if (s3Ctx) {
        renderSlide3ProcessCockpit(s3Ctx, s3W, s3H, s3Dpr, elapsedSeconds);
      }

      // Render Slide 4 ("Dönüşüm için tasarla")
      if (s4Ctx) {
        renderSlide4ConvertBroll(s4Ctx, s4W, s4H, s4Dpr, elapsedSeconds);
      }
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

        # Eliminate the MP4 video downloads from RSC payload for Slides 1, 2, 3 & 4
        html = re.sub(
            r'https://roasist\.github\.io/roasist-web/images/methodology/01-veri-ve-strateji\.mp4(\?v=\d+)?',
            "",
            html,
        )
        html = re.sub(
            r'https://roasist\.github\.io/roasist-web/images/methodology/02-yaratici-ve-cesur-fikir\.mp4(\?v=\d+)?',
            "",
            html,
        )
        html = re.sub(
            r'https://roasist\.github\.io/roasist-web/images/methodology/03-kusursuz-surec-yonetimi\.mp4(\?v=\d+)?',
            "",
            html,
        )
        html = re.sub(
            r'https://kota-content\.b-cdn\.net/app/uploads/2026/07/Create-To-Convert-compress\.mp4',
            "",
            html,
        )
        html = re.sub(
            r'https://kota-content\.b-cdn\.net/app/uploads/2026/07/create-to-convert\.jpg',
            "https://roasist.github.io/roasist-web/images/methodology/04-donusum-icin-tasarla.jpg",
            html,
        )

        if "</body>" in html:
            html = html.replace("</body>", KINETIC_3D_BLOCK + "</body>", 1)

        if protected is not None:
            html = html.replace("__PROTECTED_T712_BLOCK__", protected)

        p.write_text(html, encoding="utf-8")
        print(f"Injected Slides 1, 2, 3 & 4 Canvas + removed video loads in {rel}")


if __name__ == "__main__":
    main()


