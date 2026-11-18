"""Inject the 60 FPS HTML + CSS + Canvas animations for BOTH:
  - Slide 1 ('Önce veri ve strateji'): 3D Z-Axis Kinetic Typography (15 words)
  - Slide 2 ('Yaratıcı ve cesur fikir'): 3D Perspective Creative Bento & Particle Sphere
and eliminate the 9.5 MB MP4 video downloads for Slides 1 & 2 across public/ and dist/."""

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
html body #carousel .swiper-slide:nth-child(2) .CarouselSlides_carouselMedia__aqYWx {
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
html body #carousel .swiper-slide:nth-child(2) .CarouselSlides_carouselMedia__aqYWx video {
  display: none !important;
}

html body .roasist-kinetic-3d-canvas,
html body .roasist-creative-bento-canvas {
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
  // MOUNT & INTERSECTION OBSERVER LIFECYCLE
  // ==========================================================================
  let s1Canvas = null, s1Ctx = null, s1W = 562, s1H = 434, s1Dpr = 1;
  let s2Canvas = null, s2Ctx = null, s2W = 562, s2H = 434, s2Dpr = 1;
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

        # Eliminate the 3.9 MB + 5.6 MB MP4 video downloads from RSC payload for Slide 1 & Slide 2
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

        if "</body>" in html:
            html = html.replace("</body>", KINETIC_3D_BLOCK + "</body>", 1)

        if protected is not None:
            html = html.replace("__PROTECTED_T712_BLOCK__", protected)

        p.write_text(html, encoding="utf-8")
        print(f"Injected Slide 1 & Slide 2 Canvas + removed 9.5 MB video loads in {rel}")


if __name__ == "__main__":
    main()
