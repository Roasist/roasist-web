#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Inject 60 FPS 3D HTML5 Canvas B-Roll animations for all 6 Performance Marketing channels
on /hizmetler/performans-pazarlamasi/ and /en/performance-marketing/ (in both public/ and dist/):

  1. Google Ads (Search, Shopping, PMax, YouTube) — 3D Isometric Search Intent, Shopping Feed & YouTube Video Slab
  2. Instagram & Facebook (Meta Ads) — 3D Isometric Reels/Stories Mobile Frame, Dynamic Product Catalog (DPA) & CAPI Signal Pulse
  3. TikTok Ads — 3D Isometric Vertical Video Studio, Audio Waveizer & Spark Creator Engagement Motion
  4. Yandex Ads — 3D Eurasia & CIS Geodesic Sphere, Yandex Direct Search Slab & YAN Ad Network Nodes
  5. Bing Ads — 3D Enterprise Desktop Browser Slab, Multi-Engine (Bing/Yahoo/DuckDuckGo) Routing Prism & Low-CPC Efficiency Gauge
  6. LinkedIn Ads — 3D Executive Decision-Maker Hierarchy Pyramid (C-Suite Radar) & Enterprise B2B Account Pipeline

Preserves 100% React Flight hydration parity and eliminates external KOTA MP4/PNG/JPG downloads for all 6 channel rows.
"""

import json
import os
import pathlib
import re
import sys

ROOT = pathlib.Path("/home/antigravity/Roasist/roasist-web")
sys.path.insert(0, str(ROOT / "scripts"))
from update_about_page import parse_flight_stream, serialize_flight_stream  # noqa: E402

TARGET_FILES = [
    "public/hizmetler/performans-pazarlamasi/index.html",
    "public/en/performance-marketing/index.html",
    "dist/hizmetler/performans-pazarlamasi/index.html",
    "dist/en/performance-marketing/index.html",
]

PERF_CHANNELS_3D_BLOCK = r"""<style data-roasist-perf-channels-3d-style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap&subset=latin,latin-ext');

html body .TextImageRows_row__PPlpB .TextImageRows_media__twu3R {
  position: relative !important;
  overflow: hidden !important;
  isolation: isolate !important;
}

html body .TextImageRows_row__PPlpB .TextImageRows_media__twu3R .ImageEnter_image__FSEP_ {
  background-color: #090812 !important;
  overflow: hidden !important;
  opacity: 1 !important;
  border: 1px solid rgba(255, 255, 255, 0.09) !important;
  box-shadow:
    0 28px 70px -18px rgba(6, 5, 12, 0.85),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.08) !important;
  isolation: isolate !important;
}

/* Preserve KOTA asymmetric architectural corner radii on container & canvas */
html body .TextImageRows_row__PPlpB:nth-child(odd) .TextImageRows_media__twu3R .ImageEnter_image__FSEP_,
html body .TextImageRows_row__PPlpB:nth-child(odd) .TextImageRows_media__twu3R canvas.roasist-perf-channel-canvas {
  border-radius: 28px 7.5rem 28px 28px !important;
}
@media (min-width: 850px) {
  html body .TextImageRows_row__PPlpB:nth-child(odd) .TextImageRows_media__twu3R .ImageEnter_image__FSEP_,
  html body .TextImageRows_row__PPlpB:nth-child(odd) .TextImageRows_media__twu3R canvas.roasist-perf-channel-canvas {
    border-radius: 32px 12.5rem 32px 32px !important;
  }
}

html body .TextImageRows_row__PPlpB:nth-child(2n) .TextImageRows_media__twu3R .ImageEnter_image__FSEP_,
html body .TextImageRows_row__PPlpB:nth-child(2n) .TextImageRows_media__twu3R canvas.roasist-perf-channel-canvas {
  border-radius: 28px 7.5rem 28px 28px !important;
}
@media (min-width: 769px) and (max-width: 849px) {
  html body .TextImageRows_row__PPlpB:nth-child(2n) .TextImageRows_media__twu3R .ImageEnter_image__FSEP_,
  html body .TextImageRows_row__PPlpB:nth-child(2n) .TextImageRows_media__twu3R canvas.roasist-perf-channel-canvas {
    border-radius: 7.5rem 28px 28px 28px !important;
  }
}
@media (min-width: 850px) {
  html body .TextImageRows_row__PPlpB:nth-child(2n) .TextImageRows_media__twu3R .ImageEnter_image__FSEP_,
  html body .TextImageRows_row__PPlpB:nth-child(2n) .TextImageRows_media__twu3R canvas.roasist-perf-channel-canvas {
    border-radius: 12.5rem 32px 32px 32px !important;
  }
}

html body .TextImageRows_row__PPlpB .TextImageRows_media__twu3R video,
html body .TextImageRows_row__PPlpB .TextImageRows_media__twu3R img {
  opacity: 0 !important;
  pointer-events: none !important;
}

html body canvas.roasist-perf-channel-canvas {
  position: absolute !important;
  inset: 0 !important;
  width: 100% !important;
  height: 100% !important;
  display: block !important;
  z-index: 3 !important;
  pointer-events: none !important;
}

/* Row 1: Google Ads Official Brand Motion SVG Stage */
html body .TextImageRows_row__PPlpB:nth-child(1) .TextImageRows_media__twu3R .ImageEnter_image__FSEP_ {
  background-color: #FFFFFF !important;
  border: 1px solid rgba(15, 23, 42, 0.08) !important;
  box-shadow: 0 24px 60px -18px rgba(15, 23, 42, 0.12) !important;
}

html body .TextImageRows_row__PPlpB:nth-child(1) .gads-anim-stage {
  position: absolute !important;
  inset: 0 !important;
  width: 100% !important;
  height: 100% !important;
  max-width: none !important;
  margin: 0 !important;
  background: #FFFFFF !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  overflow: hidden !important;
  z-index: 4 !important;
  pointer-events: none !important;
}

html body .TextImageRows_row__PPlpB:nth-child(1) .gads-svg {
  width: 96% !important;
  height: auto !important;
  display: block !important;
}

.gads-anim-stage .grid-lines {
  opacity: 0;
  transform-origin: 300px 150px;
  animation: gadsGridFade 7s ease-in-out infinite;
}

.gads-anim-stage .col-green {
  transform-origin: 200px 220px;
  animation: gadsBarRiseLeft 7s cubic-bezier(0.22, 1, 0.36, 1) infinite;
}
.gads-anim-stage .col-yellow {
  transform-origin: 300px 220px;
  animation: gadsBarRiseMid 7s cubic-bezier(0.22, 1, 0.36, 1) infinite;
}
.gads-anim-stage .col-blue {
  transform-origin: 400px 220px;
  animation: gadsBarRiseRight 7s cubic-bezier(0.22, 1, 0.36, 1) infinite;
}

.gads-anim-stage .logo-assembly {
  transform-origin: 300px 160px;
  animation: gadsLogoSequence 7s cubic-bezier(0.25, 1, 0.5, 1) infinite;
}

.gads-anim-stage .pill-blue-wrap {
  transform-origin: 300px 151px;
  animation: gadsBlueFlip 7s cubic-bezier(0.34, 1.56, 0.64, 1) infinite;
}

.gads-anim-stage .brand-text {
  animation: gadsTextReveal 7s cubic-bezier(0.22, 1, 0.36, 1) infinite;
}

@keyframes gadsGridFade {
  0%, 6%   { opacity: 0; transform: scaleX(0.6); }
  14%, 30% { opacity: 1; transform: scaleX(1); }
  38%, 100%{ opacity: 0; transform: scaleX(0.8); }
}

@keyframes gadsBarRiseLeft {
  0%        { opacity: 0; transform: translateY(80px) scaleY(0.3); }
  10%, 28%  { opacity: 1; transform: translateY(0) scaleY(1); }
  36%, 100% { opacity: 0; transform: translateX(75px) translateY(50px) scale(0.4); }
}

@keyframes gadsBarRiseMid {
  0%, 3%    { opacity: 0; transform: translateY(80px) scaleY(0.3); }
  13%, 28%  { opacity: 1; transform: translateY(0) scaleY(1); }
  36%, 100% { opacity: 0; transform: translateY(40px) scale(0.4); }
}

@keyframes gadsBarRiseRight {
  0%, 6%    { opacity: 0; transform: translateY(80px) scaleY(0.3); }
  16%, 27%  { opacity: 1; transform: translateY(0) scaleY(1); }
  35%, 100% { opacity: 0; transform: translateX(-75px) translateY(-30px) scale(0.4); }
}

@keyframes gadsLogoSequence {
  0%, 33%   { opacity: 0; transform: translateX(0) scale(1.15); }
  38%       { opacity: 1; transform: translateX(0) scale(1.15); }
  52%       { opacity: 1; transform: translateX(0) scale(0.72); }
  62%, 92%  { opacity: 1; transform: translateX(-135px) scale(0.72); }
  98%, 100% { opacity: 0; transform: translateX(-135px) scale(0.72); }
}

@keyframes gadsBlueFlip {
  0%, 33%   { transform: rotate(-110deg) translateY(-30px); }
  44%, 100% { transform: rotate(0deg) translateY(0); }
}

@keyframes gadsTextReveal {
  0%, 58%   { opacity: 0; transform: translateX(-18px); }
  68%, 92%  { opacity: 1; transform: translateX(0); }
  98%, 100% { opacity: 0; transform: translateX(0); }
}
</style>
<script data-roasist-perf-channels-3d-script>
(() => {
  const clamp01 = (x) => Math.max(0, Math.min(1, x));
  const lerp = (a, b, t) => a + (b - a) * t;
  const smoothstep = (e0, e1, x) => {
    const t = clamp01((x - e0) / (e1 - e0));
    return t * t * (3 - 2 * t);
  };
  const springOut = (x) => {
    const t = clamp01(x);
    return 1 - Math.pow(1 - t, 3.2) * Math.cos(t * Math.PI * 0.65);
  };

  function roundRectPath(c, x, y, w, h, r) {
    c.beginPath();
    c.roundRect(x, y, w, h, r);
  }

  // Isometric / 3D Plane Projection Engine (Reference coordinate space 900x900)
  function createCam(cx, cy, scale, pitch, yaw, roll = 0) {
    return {
      cx,
      cy,
      scale,
      pitch,
      yaw,
      roll,
      cosP: Math.cos(pitch),
      sinP: Math.sin(pitch),
      cosY: Math.cos(yaw),
      sinY: Math.sin(yaw),
      cosR: Math.cos(roll),
      sinR: Math.sin(roll)
    };
  }

  function project3D(u, v, z, cam) {
    const x1 = u * cam.cosY - v * cam.sinY;
    const y1 = u * cam.sinY + v * cam.cosY;
    const sx = cam.scale * x1;
    const sy = -cam.scale * cam.sinP * z + cam.scale * cam.cosP * y1;
    const rx = sx * cam.cosR - sy * cam.sinR;
    const ry = sx * cam.sinR + sy * cam.cosR;
    return { x: cam.cx + rx, y: cam.cy + ry };
  }

  function applyIsoPlane(c, z, cam, offsetX = 0, offsetY = 0) {
    const p0 = project3D(offsetX, offsetY, z, cam);
    const px = project3D(offsetX + 100, offsetY, z, cam);
    const py = project3D(offsetX, offsetY + 100, z, cam);
    c.transform(
      (px.x - p0.x) / 100,
      (px.y - p0.y) / 100,
      (py.x - p0.x) / 100,
      (py.y - p0.y) / 100,
      p0.x,
      p0.y
    );
  }

  function drawExtrudedSlab(c, x, y, w, h, r, zTop, thickness, cam, topFill, sideFill, rimStroke, shadowAlpha = 0.42) {
    if (shadowAlpha > 0.01) {
      c.save();
      applyIsoPlane(c, zTop - thickness - 12, cam);
      roundRectPath(c, x + 8, y + 12, w, h, r);
      c.fillStyle = `rgba(3, 3, 8, ${shadowAlpha.toFixed(3)})`;
      c.shadowColor = `rgba(0, 0, 0, ${(shadowAlpha * 0.9).toFixed(3)})`;
      c.shadowBlur = 34;
      c.fill();
      c.restore();
    }

    const steps = Math.max(2, Math.min(10, Math.ceil(thickness / 2.2)));
    for (let s = steps; s >= 1; s--) {
      const zs = zTop - (s / steps) * thickness;
      c.save();
      applyIsoPlane(c, zs, cam);
      roundRectPath(c, x, y, w, h, r);
      c.fillStyle = sideFill;
      c.fill();
      c.restore();
    }

    c.save();
    applyIsoPlane(c, zTop, cam);
    roundRectPath(c, x, y, w, h, r);
    c.fillStyle = topFill;
    c.fill();
    if (rimStroke) {
      c.strokeStyle = rimStroke;
      c.lineWidth = 1.4;
      c.stroke();
    }
    c.restore();
  }

  function drawStudioBackground(c, W, H, accentRgb, pulse = 0) {
    c.fillStyle = '#090812';
    c.fillRect(0, 0, W, H);

    const g1 = c.createRadialGradient(W * 0.48, H * 0.48, 20, W * 0.5, H * 0.5, W * 0.62);
    g1.addColorStop(0, `rgba(${accentRgb}, ${(0.18 + pulse * 0.04).toFixed(3)})`);
    g1.addColorStop(0.55, 'rgba(18, 16, 32, 0.35)');
    g1.addColorStop(1, 'rgba(9, 8, 18, 0)');
    c.fillStyle = g1;
    c.fillRect(0, 0, W, H);

    // Subtle vignettes for depth
    const vig = c.createRadialGradient(W * 0.5, H * 0.5, W * 0.32, W * 0.5, H * 0.5, W * 0.75);
    vig.addColorStop(0, 'rgba(9, 8, 18, 0)');
    vig.addColorStop(1, 'rgba(5, 4, 11, 0.72)');
    c.fillStyle = vig;
    c.fillRect(0, 0, W, H);
  }

  function drawBaseGridSlab(c, cam, zBase, w, h, accentRgba) {
    drawExtrudedSlab(
      c, -w * 0.5, -h * 0.5, w, h, 26, zBase, 14, cam,
      '#111320', '#090A12', 'rgba(255, 255, 255, 0.11)', 0.55
    );
    c.save();
    applyIsoPlane(c, zBase + 0.5, cam);
    roundRectPath(c, -w * 0.5, -h * 0.5, w, h, 26);
    c.clip();
    c.strokeStyle = 'rgba(148, 163, 184, 0.08)';
    c.lineWidth = 1;
    const step = 36;
    for (let x = -w * 0.5; x <= w * 0.5; x += step) {
      c.beginPath(); c.moveTo(x, -h * 0.5); c.lineTo(x, h * 0.5); c.stroke();
    }
    for (let y = -h * 0.5; y <= h * 0.5; y += step) {
      c.beginPath(); c.moveTo(-w * 0.5, y); c.lineTo(w * 0.5, y); c.stroke();
    }
    // Corner architectural registration ticks
    c.strokeStyle = accentRgba;
    c.lineWidth = 1.6;
    const pad = 20, tk = 12;
    const corners = [
      [-w * 0.5 + pad, -h * 0.5 + pad, 1, 1],
      [w * 0.5 - pad, -h * 0.5 + pad, -1, 1],
      [-w * 0.5 + pad, h * 0.5 - pad, 1, -1],
      [w * 0.5 - pad, h * 0.5 - pad, -1, -1]
    ];
    for (const [cx, cy, dx, dy] of corners) {
      c.beginPath();
      c.moveTo(cx + dx * tk, cy);
      c.lineTo(cx, cy);
      c.lineTo(cx, cy + dy * tk);
      c.stroke();
    }
    c.restore();
  }

  function drawCheck(c, x, y, r, color) {
    c.save();
    c.strokeStyle = color;
    c.lineWidth = 2.1;
    c.lineCap = 'round';
    c.lineJoin = 'round';
    c.beginPath();
    c.moveTo(x - r * 0.45, y + r * 0.05);
    c.lineTo(x - r * 0.1, y + r * 0.4);
    c.lineTo(x + r * 0.5, y - r * 0.35);
    c.stroke();
    c.restore();
  }

  // ============================================================================
  // CHANNEL 1: GOOGLE ADS (Search SERP, Shopping Carousel, YouTube & PMax Engine)
  // ============================================================================
  function renderGoogleAds(c, w, h, dpr, elapsed) {
    const W = 900, H = 900;
    const sc = Math.min(w / W, h / H);
    const loop = 12.0;
    const t = elapsed % loop;
    const phase = (t / loop) * Math.PI * 2;

    c.save();
    c.scale(dpr, dpr);
    drawStudioBackground(c, w, h, '124, 58, 237', Math.sin(phase) * 0.5 + 0.5);
    c.translate(w * 0.5, h * 0.5);
    c.scale(sc, sc);
    c.translate(-W * 0.5, -H * 0.5);

    const lift = smoothstep(0.0, 1.8, t) * (1 - 0.18 * smoothstep(10.2, 12.0, t));
    const cam = createCam(
      450 + Math.sin(phase) * 10,
      478 + Math.cos(phase) * 8,
      0.86 + Math.sin(phase) * 0.015,
      0.56 + Math.sin(phase) * 0.03,
      -0.46 + Math.cos(phase * 0.5) * 0.05
    );

    const z0 = -45 * lift;
    const z1 = 16 * lift;
    const z2 = 76 * lift;
    const z3 = 132 * lift;

    // Layer 0: PMax Algorithmic Signal Routing Base Grid
    drawBaseGridSlab(c, cam, z0, 560, 440, 'rgba(167, 139, 250, 0.45)');

    // Glowing PMax Auction Bid Pulse Rings on Base
    c.save();
    applyIsoPlane(c, z0 + 1.2, cam);
    for (let i = 0; i < 3; i++) {
      const rp = ((elapsed * 0.45 + i * 0.33) % 1.0);
      c.beginPath();
      c.arc(0, 0, 60 + rp * 190, 0, Math.PI * 2);
      c.strokeStyle = `rgba(167, 139, 250, ${((1 - rp) * 0.28).toFixed(3)})`;
      c.lineWidth = 1.8;
      c.stroke();
    }
    c.restore();

    // Vertical laser guide pillars connecting layers
    const pillars = [[-220, -165], [220, -165], [-220, 165], [220, 165]];
    for (const [px, py] of pillars) {
      const pBot = project3D(px, py, z0, cam);
      const pTop = project3D(px, py, z2, cam);
      c.save();
      c.strokeStyle = 'rgba(167, 139, 250, 0.22)';
      c.lineWidth = 1.3;
      c.setLineDash([4, 5]);
      c.beginPath(); c.moveTo(pBot.x, pBot.y); c.lineTo(pTop.x, pTop.y); c.stroke();
      c.restore();
    }

    // Layer 1: Porcelain SERP & Search Intent Architecture Slab
    drawExtrudedSlab(
      c, -250, -185, 500, 370, 22, z1, 14, cam,
      '#F8FAFC', '#CBD5E1', 'rgba(255, 255, 255, 0.95)', 0.5
    );

    c.save();
    applyIsoPlane(c, z1 + 0.6, cam);
    // Search Bar inside Porcelain Slab
    roundRectPath(c, -222, -158, 444, 48, 24);
    c.fillStyle = '#FFFFFF';
    c.fill();
    c.strokeStyle = '#7C3AED';
    c.lineWidth = 2;
    c.stroke();

    // Magnifying glass vector icon
    c.strokeStyle = '#7C3AED';
    c.lineWidth = 2.4;
    c.beginPath(); c.arc(-192, -134, 8.5, 0, Math.PI * 2); c.stroke();
    c.beginPath(); c.moveTo(-185, -127); c.lineTo(-179, -121); c.stroke();

    // Animated search intent progress skeleton bar (minimal, zero text clutter)
    const searchFill = 120 + 180 * (0.5 + 0.5 * Math.sin(phase * 1.5));
    roundRectPath(c, -164, -140, searchFill, 12, 6);
    c.fillStyle = '#0F172A';
    c.fill();
    // Blinking caret
    if (Math.sin(elapsed * 7) > -0.2) {
      c.fillStyle = '#7C3AED';
      c.fillRect(-164 + searchFill + 6, -143, 2.5, 18);
    }

    // Top Sponsored Search Ad Result Card
    roundRectPath(c, -222, -94, 260, 112, 14);
    c.fillStyle = '#F1F5F9';
    c.fill();
    c.strokeStyle = 'rgba(15, 23, 42, 0.08)';
    c.lineWidth = 1.2;
    c.stroke();

    // "AD" minimal pill + quality score stars
    roundRectPath(c, -206, -78, 34, 18, 5);
    c.fillStyle = '#0F172A';
    c.fill();
    c.fillStyle = '#FFFFFF';
    c.font = "700 9.5px 'Inter', sans-serif";
    c.textAlign = 'center';
    c.textBaseline = 'middle';
    c.fillText('AD', -189, -68.5);

    // Architectural headline & sitelink bars
    roundRectPath(c, -162, -75, 140, 12, 6);
    c.fillStyle = '#7C3AED';
    c.fill();
    roundRectPath(c, -206, -50, 210, 9, 4.5);
    c.fillStyle = '#64748B';
    c.fill();
    roundRectPath(c, -206, -33, 165, 9, 4.5);
    c.fillStyle = '#94A3B8';
    c.fill();
    // 2 Sitelink mini pills
    roundRectPath(c, -206, -12, 84, 18, 6);
    c.fillStyle = '#E2E8F0';
    c.fill();
    roundRectPath(c, -114, -12, 84, 18, 6);
    c.fillStyle = '#E2E8F0';
    c.fill();

    // Bottom Organic / Extension Bars
    roundRectPath(c, -222, 32, 260, 124, 14);
    c.fillStyle = '#F1F5F9';
    c.fill();
    // Conversion value sparkline inside card
    c.beginPath();
    const pts = [[-202, 128], [-162, 114], [-122, 118], [-82, 92], [-42, 74], [14, 54]];
    pts.forEach(([x, y], idx) => idx === 0 ? c.moveTo(x, y) : c.lineTo(x, y));
    c.strokeStyle = '#10B981';
    c.lineWidth = 3;
    c.lineCap = 'round';
    c.lineJoin = 'round';
    c.stroke();
    c.restore();

    // Layer 2: 3D Floating Google Shopping Product Cards (Trio on Right)
    const shopOffsets = [-95, 20, 135];
    for (let i = 0; i < 3; i++) {
      const hoverZ = z2 + Math.sin(phase * 1.5 + i * 1.1) * 10;
      const cardX = 56;
      const cardY = -140 + i * 102;
      drawExtrudedSlab(
        c, cardX, cardY, 174, 88, 14, hoverZ, 10, cam,
        '#FFFFFF', '#CBD5E1', i === 0 ? '#7C3AED' : 'rgba(15, 23, 42, 0.12)', 0.32
      );
      c.save();
      applyIsoPlane(c, hoverZ + 0.6, cam);
      // Product thumbnail square
      roundRectPath(c, cardX + 12, cardY + 12, 64, 64, 10);
      c.fillStyle = i === 0 ? 'rgba(124, 58, 237, 0.12)' : '#F1F5F9';
      c.fill();
      // 3D Isometric Product Cube icon inside thumbnail
      const cx = cardX + 44, cy = cardY + 44;
      c.fillStyle = i === 0 ? '#7C3AED' : '#475569';
      c.beginPath();
      c.moveTo(cx, cy - 16); c.lineTo(cx + 15, cy - 7); c.lineTo(cx, cy + 2); c.lineTo(cx - 15, cy - 7);
      c.closePath(); c.fill();
      c.fillStyle = i === 0 ? '#5B21B6' : '#334155';
      c.beginPath();
      c.moveTo(cx - 15, cy - 7); c.lineTo(cx, cy + 2); c.lineTo(cx, cy + 17); c.lineTo(cx - 15, cy + 8);
      c.closePath(); c.fill();
      c.fillStyle = i === 0 ? '#8B5CF6' : '#64748B';
      c.beginPath();
      c.moveTo(cx + 15, cy - 7); c.lineTo(cx, cy + 2); c.lineTo(cx, cy + 17); c.lineTo(cx + 15, cy + 8);
      c.closePath(); c.fill();

      // Product bars & star rating dots
      roundRectPath(c, cardX + 88, cardY + 18, 68, 10, 5);
      c.fillStyle = '#0F172A';
      c.fill();
      for (let s = 0; s < 5; s++) {
        c.beginPath();
        c.arc(cardX + 92 + s * 10, cardY + 42, 3.2, 0, Math.PI * 2);
        c.fillStyle = '#F59E0B';
        c.fill();
      }
      roundRectPath(c, cardX + 88, cardY + 56, 48, 14, 7);
      c.fillStyle = 'rgba(16, 185, 129, 0.14)';
      c.fill();
      c.restore();
    }

    // Layer 3: Top Floating YouTube Video & ROAS Badge Slab
    const ytZ = z3 + Math.cos(phase) * 8;
    drawExtrudedSlab(
      c, -210, 20, 225, 132, 18, ytZ, 12, cam,
      '#0F172A', '#020617', 'rgba(167, 139, 250, 0.55)', 0.45
    );
    c.save();
    applyIsoPlane(c, ytZ + 0.6, cam);
    // Video player screen
    roundRectPath(c, -196, 34, 197, 82, 11);
    const vg = c.createLinearGradient(-196, 34, 0, 116);
    vg.addColorStop(0, '#1E1B4B');
    vg.addColorStop(1, '#31104F');
    c.fillStyle = vg;
    c.fill();

    // Glowing Play Button with pulse ring
    const playPulse = (elapsed * 0.9) % 1.0;
    c.beginPath();
    c.arc(-97, 75, 18 + playPulse * 16, 0, Math.PI * 2);
    c.strokeStyle = `rgba(167, 139, 250, ${(1 - playPulse) * 0.55})`;
    c.lineWidth = 1.8;
    c.stroke();

    c.beginPath();
    c.arc(-97, 75, 19, 0, Math.PI * 2);
    c.fillStyle = '#7C3AED';
    c.fill();
    c.fillStyle = '#FFFFFF';
    c.beginPath();
    c.moveTo(-102, 67); c.lineTo(-88, 75); c.lineTo(-102, 83);
    c.closePath();
    c.fill();

    // Video timeline scrubber at bottom of video frame
    roundRectPath(c, -186, 128, 177, 6, 3);
    c.fillStyle = 'rgba(255, 255, 255, 0.15)';
    c.fill();
    const scrubW = 45 + 120 * ((elapsed % 6.0) / 6.0);
    roundRectPath(c, -186, 128, scrubW, 6, 3);
    c.fillStyle = '#A78BFA';
    c.fill();
    c.beginPath();
    c.arc(-186 + scrubW, 131, 5.5, 0, Math.PI * 2);
    c.fillStyle = '#FFFFFF';
    c.fill();
    c.restore();

    c.restore();
  }

  // ============================================================================
  // CHANNEL 2: INSTAGRAM & FACEBOOK (Meta Ads, Reels/Stories, DPA Catalog & CAPI)
  // ============================================================================
  function renderMetaAds(c, w, h, dpr, elapsed) {
    const W = 900, H = 900;
    const sc = Math.min(w / W, h / H);
    const loop = 12.0;
    const t = elapsed % loop;
    const phase = (t / loop) * Math.PI * 2;

    c.save();
    c.scale(dpr, dpr);
    drawStudioBackground(c, w, h, '217, 70, 239', Math.sin(phase) * 0.5 + 0.5);
    c.translate(w * 0.5, h * 0.5);
    c.scale(sc, sc);
    c.translate(-W * 0.5, -H * 0.5);

    const cam = createCam(
      450 + Math.cos(phase) * 9,
      482 + Math.sin(phase) * 8,
      0.86 + Math.sin(phase) * 0.014,
      0.54 + Math.cos(phase) * 0.028,
      0.42 + Math.sin(phase * 0.5) * 0.05
    );

    const z0 = -50;
    const zPhone = 22 + Math.sin(phase) * 8;
    const zCatalog = 86 + Math.cos(phase) * 10;

    // Layer 0: Conversions API (CAPI) Server-to-Meta Signal Grid
    drawBaseGridSlab(c, cam, z0, 540, 440, 'rgba(232, 121, 249, 0.42)');

    // Animated CAPI Server Event Stream Arcs on Base Plane
    c.save();
    applyIsoPlane(c, z0 + 1.5, cam);
    for (let i = 0; i < 4; i++) {
      const yLine = -120 + i * 80;
      c.strokeStyle = 'rgba(232, 121, 249, 0.16)';
      c.lineWidth = 1.6;
      c.beginPath();
      c.moveTo(-230, yLine);
      c.bezierCurveTo(-80, yLine - 35, 80, yLine + 35, 230, yLine);
      c.stroke();

      // Traveling data photon
      const prog = (elapsed * 0.38 + i * 0.25) % 1.0;
      const px = lerp(-230, 230, prog);
      const py = yLine + Math.sin(prog * Math.PI * 2) * 18;
      c.beginPath();
      c.arc(px, py, 5, 0, Math.PI * 2);
      c.fillStyle = '#F0ABFC';
      c.shadowColor = '#E879F9';
      c.shadowBlur = 14;
      c.fill();
    }
    c.restore();

    // Layer 1: 3D Isometric Smartphone Frame (Instagram Reels / Story Ad)
    drawExtrudedSlab(
      c, -145, -210, 250, 420, 34, zPhone, 16, cam,
      '#0F172A', '#020617', 'rgba(255, 255, 255, 0.25)', 0.55
    );
    // Inner Screen Porcelain Canvas
    drawExtrudedSlab(
      c, -131, -194, 222, 388, 24, zPhone + 2, 2, cam,
      '#F8FAFC', '#E2E8F0', null, 0
    );

    c.save();
    applyIsoPlane(c, zPhone + 3.2, cam);
    // Dynamic Island / Speaker Notch
    roundRectPath(c, -52, -182, 64, 14, 7);
    c.fillStyle = '#0F172A';
    c.fill();

    // Story Progress Bars at Top
    for (let s = 0; s < 3; s++) {
      const bx = -114 + s * 66;
      roundRectPath(c, bx, -158, 60, 4, 2);
      c.fillStyle = '#E2E8F0';
      c.fill();
      const fillRatio = s === 0 ? 1 : (s === 1 ? (elapsed % 4.0) / 4.0 : 0);
      if (fillRatio > 0) {
        roundRectPath(c, bx, -158, 60 * fillRatio, 4, 2);
        c.fillStyle = '#D946EF';
        c.fill();
      }
    }

    // Reel Visual Showcase Window inside Phone
    roundRectPath(c, -115, -138, 190, 226, 18);
    const rg = c.createLinearGradient(-115, -138, 75, 88);
    rg.addColorStop(0, '#1E1B4B');
    rg.addColorStop(0.55, '#4C1D95');
    rg.addColorStop(1, '#86198F');
    c.fillStyle = rg;
    c.fill();

    // Abstract 3D Sculptural Sphere / Product Spotlight inside Reel
    const orbY = -25 + Math.sin(phase * 2) * 10;
    const orbG = c.createRadialGradient(-32, orbY - 14, 6, -20, orbY, 54);
    orbG.addColorStop(0, '#F5D0FE');
    orbG.addColorStop(0.45, '#C026D3');
    orbG.addColorStop(1, 'rgba(88, 28, 135, 0)');
    c.fillStyle = orbG;
    c.beginPath();
    c.arc(-20, orbY, 54, 0, Math.PI * 2);
    c.fill();

    // Floating heart/like & conversion particles rising on right edge of Reel
    for (let p = 0; p < 4; p++) {
      const pt = (elapsed * 0.55 + p * 0.25) % 1.0;
      const hx = 45 + Math.sin(pt * 6 + p) * 10;
      const hy = lerp(65, -95, pt);
      const alpha = Math.sin(pt * Math.PI);
      c.beginPath();
      c.arc(hx, hy, 7 * (0.7 + 0.3 * alpha), 0, Math.PI * 2);
      c.fillStyle = `rgba(244, 114, 182, ${(alpha * 0.85).toFixed(3)})`;
      c.fill();
    }

    // Conversion CTA Button at bottom of phone
    const ctaPulse = 0.5 + 0.5 * Math.sin(phase * 2);
    roundRectPath(c, -115, 112, 190, 46, 14);
    c.fillStyle = '#0F172A';
    c.fill();
    // Glowing indicator dot & bar on CTA
    c.beginPath();
    c.arc(-88, 135, 6, 0, Math.PI * 2);
    c.fillStyle = '#10B981';
    c.fill();
    roundRectPath(c, -70, 130, 86, 10, 5);
    c.fillStyle = '#FFFFFF';
    c.fill();
    // Arrow icon on CTA
    c.strokeStyle = '#E879F9';
    c.lineWidth = 2.4;
    c.lineCap = 'round';
    c.beginPath();
    c.moveTo(42, 135); c.lineTo(54, 135);
    c.moveTo(49, 129); c.lineTo(55, 135); c.lineTo(49, 141);
    c.stroke();
    c.restore();

    // Layer 2: Orbiting Dynamic Product Catalog (DPA) Cards (Sliding in 3D depth)
    const dpaPositions = [
      { x: -275, y: -95, zOff: 12, accent: '#D946EF' },
      { x: 115, y: -135, zOff: 28, accent: '#8B5CF6' },
      { x: 125, y: 25, zOff: -4, accent: '#10B981' }
    ];
    dpaPositions.forEach((card, idx) => {
      const cz = zCatalog + card.zOff + Math.sin(phase * 1.5 + idx * 1.4) * 10;
      drawExtrudedSlab(
        c, card.x, card.y, 156, 118, 16, cz, 10, cam,
        '#FFFFFF', '#CBD5E1', 'rgba(15, 23, 42, 0.14)', 0.42
      );
      c.save();
      applyIsoPlane(c, cz + 0.6, cam);
      roundRectPath(c, card.x + 12, card.y + 12, 132, 62, 10);
      c.fillStyle = '#F1F5F9';
      c.fill();

      // Verified CAPI match checkmark badge
      c.beginPath();
      c.arc(card.x + 126, card.y + 30, 11, 0, Math.PI * 2);
      c.fillStyle = card.accent;
      c.fill();
      drawCheck(c, card.x + 126, card.y + 30, 9, '#FFFFFF');

      // Minimal product geometry bar
      roundRectPath(c, card.x + 22, card.y + 34, 68, 10, 5);
      c.fillStyle = '#334155';
      c.fill();
      roundRectPath(c, card.x + 22, card.y + 50, 44, 8, 4);
      c.fillStyle = '#94A3B8';
      c.fill();

      // Bottom price/ROAS indicator bar
      roundRectPath(c, card.x + 14, card.y + 88, 76, 14, 7);
      c.fillStyle = '#0F172A';
      c.fill();
      roundRectPath(c, card.x + 100, card.y + 88, 42, 14, 7);
      c.fillStyle = 'rgba(16, 185, 129, 0.16)';
      c.fill();
      c.restore();
    });

    c.restore();
  }

  // ============================================================================
  // CHANNEL 3: TIKTOK ADS (3D Vertical Motion Stage, Soundwave Equalizer & Spark Pulse)
  // ============================================================================
  function renderTikTokAds(c, w, h, dpr, elapsed) {
    const W = 900, H = 900;
    const sc = Math.min(w / W, h / H);
    const loop = 10.0;
    const t = elapsed % loop;
    const phase = (t / loop) * Math.PI * 2;

    c.save();
    c.scale(dpr, dpr);
    drawStudioBackground(c, w, h, '20, 184, 166', Math.sin(phase) * 0.5 + 0.5);
    c.translate(w * 0.5, h * 0.5);
    c.scale(sc, sc);
    c.translate(-W * 0.5, -H * 0.5);

    const cam = createCam(
      450 + Math.sin(phase) * 10,
      480 + Math.cos(phase) * 8,
      0.86 + Math.sin(phase) * 0.015,
      0.56 + Math.sin(phase) * 0.025,
      -0.44 + Math.cos(phase * 0.5) * 0.05
    );

    const zBase = -48;
    const zBackCard = 6;
    const zMainCard = 48 + Math.sin(phase) * 7;
    const zFrontWidget = 104 + Math.cos(phase) * 9;

    // Layer 0: Base Studio Deck
    drawBaseGridSlab(c, cam, zBase, 540, 440, 'rgba(45, 212, 191, 0.42)');

    // Layer 1: Secondary Stacked Vertical Video Slab (Offset in 3D Depth)
    drawExtrudedSlab(
      c, -70, -195, 240, 380, 28, zBackCard, 12, cam,
      '#1E293B', '#0F172A', 'rgba(45, 212, 191, 0.35)', 0.4
    );

    // Layer 2: Primary Vertical Video Slab (Porcelain & Slate High-Contrast Stage)
    drawExtrudedSlab(
      c, -145, -185, 240, 380, 28, zMainCard, 16, cam,
      '#F8FAFC', '#CBD5E1', '#FFFFFF', 0.55
    );

    c.save();
    applyIsoPlane(c, zMainCard + 0.8, cam);
    // Dark cinema viewport inside vertical frame
    roundRectPath(c, -131, -171, 212, 352, 20);
    c.fillStyle = '#090D16';
    c.fill();

    // 3D Kinetic Play Prism / Hook Ring in Center of Vertical Screen
    const pulse = 0.5 + 0.5 * Math.sin(phase * 3);
    c.beginPath();
    c.arc(-25, -24, 54 + pulse * 10, 0, Math.PI * 2);
    c.strokeStyle = 'rgba(45, 212, 191, 0.32)';
    c.lineWidth = 2;
    c.stroke();

    c.beginPath();
    c.arc(-25, -24, 44, 0, Math.PI * 2);
    c.strokeStyle = 'rgba(244, 63, 94, 0.45)';
    c.lineWidth = 2.5;
    c.stroke();

    // Dual-chromatic offset play disc (subtle nod to short-form video optics without clichés)
    c.beginPath();
    c.arc(-28, -26, 30, 0, Math.PI * 2);
    c.fillStyle = 'rgba(45, 212, 191, 0.85)';
    c.fill();
    c.beginPath();
    c.arc(-22, -22, 30, 0, Math.PI * 2);
    c.fillStyle = 'rgba(244, 63, 94, 0.85)';
    c.fill();
    c.beginPath();
    c.arc(-25, -24, 28, 0, Math.PI * 2);
    c.fillStyle = '#FFFFFF';
    c.fill();

    // Crisp Dark Play Triangle
    c.fillStyle = '#0F172A';
    c.beginPath();
    c.moveTo(-31, -35); c.lineTo(-13, -24); c.lineTo(-31, -13);
    c.closePath();
    c.fill();

    // Right-Side Vertical Engagement Action Stack (3 minimalist circles)
    for (let a = 0; a < 3; a++) {
      const ay = -55 + a * 44;
      c.beginPath();
      c.arc(54, ay, 13, 0, Math.PI * 2);
      c.fillStyle = a === 0 ? '#F43F5E' : 'rgba(255, 255, 255, 0.14)';
      c.fill();
    }

    // Bottom Spark Ads Native Creator Bar & Progress Fill
    roundRectPath(c, -113, 114, 176, 46, 12);
    c.fillStyle = 'rgba(255, 255, 255, 0.1)';
    c.fill();
    c.beginPath();
    c.arc(-90, 137, 12, 0, Math.PI * 2);
    c.fillStyle = '#2DD4BF';
    c.fill();
    roundRectPath(c, -70, 129, 95, 8, 4);
    c.fillStyle = '#FFFFFF';
    c.fill();
    roundRectPath(c, -70, 143, 62, 6, 3);
    c.fillStyle = '#94A3B8';
    c.fill();
    c.restore();

    // Layer 3: 3D Extruded Spatial Audio Wave / Hook Retention Equalizer Bars
    // Positioned alongside the vertical video slab, rising in true 3D Z-space
    const numBars = 9;
    for (let b = 0; b < numBars; b++) {
      const bx = 130;
      const by = -140 + b * 34;
      const wave = 0.5 + 0.5 * Math.sin(elapsed * 5.2 - b * 0.55);
      const barW = 45 + wave * 95;
      const barZ = zMainCard + 15 + wave * 28;
      const isHighlight = b === 3 || b === 4 || b === 5;
      drawExtrudedSlab(
        c, bx, by, barW, 20, 8, barZ, 10, cam,
        isHighlight ? '#2DD4BF' : '#F8FAFC',
        isHighlight ? '#0D9488' : '#CBD5E1',
        null, 0.25
      );
    }

    // Layer 4: Top Left Floating Spark Ads Retention Curve Slab
    drawExtrudedSlab(
      c, -280, -130, 165, 112, 16, zFrontWidget, 10, cam,
      '#FFFFFF', '#CBD5E1', 'rgba(15, 23, 42, 0.12)', 0.45
    );
    c.save();
    applyIsoPlane(c, zFrontWidget + 0.6, cam);
    // Green live dot + header bar
    c.beginPath();
    c.arc(-256, -104, 5.5, 0, Math.PI * 2);
    c.fillStyle = '#10B981';
    c.fill();
    roundRectPath(c, -242, -108, 78, 8, 4);
    c.fillStyle = '#0F172A';
    c.fill();

    // Smooth rising hook retention curve
    c.beginPath();
    c.moveTo(-260, -45);
    c.bezierCurveTo(-230, -48, -215, -82, -185, -80);
    c.bezierCurveTo(-160, -78, -150, -94, -135, -96);
    c.strokeStyle = '#F43F5E';
    c.lineWidth = 3.2;
    c.lineCap = 'round';
    c.stroke();

    c.beginPath();
    c.arc(-135, -96, 5, 0, Math.PI * 2);
    c.fillStyle = '#F43F5E';
    c.fill();
    c.restore();

    c.restore();
  }

  // ============================================================================
  // CHANNEL 4: YANDEX ADS (3D Eurasia/CIS Geodesic Globe, Yandex Direct & YAN Network)
  // ============================================================================
  const YANDEX_LAND_BOXES = [
    [35, 62, -9, 32],   // Europe
    [36, 42.5, 26, 45], // Türkiye & Anatolia
    [41, 71, 28, 145],  // Russia / Siberia / CIS North
    [36, 55, 46, 87],   // Central Asia (Kazakhstan, Uzbekistan, Azerbaijan)
    [15, 36, 34, 60],   // MENA
    [18, 45, 70, 122]   // East & South Asia
  ];

  function isYandexLand(lat, lon) {
    if (lat > 31 && lat < 36.2 && lon > 11 && lon < 34.5) return false;
    if (lat > 41.5 && lat < 46.5 && lon > 28 && lon < 41.5) return false;
    for (let i = 0; i < YANDEX_LAND_BOXES.length; i++) {
      const b = YANDEX_LAND_BOXES[i];
      if (lat >= b[0] && lat <= b[1] && lon >= b[2] && lon <= b[3]) return true;
    }
    return false;
  }

  const YANDEX_GLOBE_DOTS = (() => {
    const pts = [];
    const N = 1150;
    const ga = Math.PI * (3 - Math.sqrt(5));
    for (let i = 0; i < N; i++) {
      const y = 1 - (i / (N - 1)) * 2;
      const r = Math.sqrt(1 - y * y);
      const th = ga * i;
      const lat = Math.asin(-y) * (180 / Math.PI);
      let lon = ((th * 180) / Math.PI) % 360;
      if (lon > 180) lon -= 360;
      const land = isYandexLand(lat, lon);
      const isCoreCIS = land && lat > 36 && lat < 64 && lon > 25 && lon < 92;
      pts.push({
        x: Math.cos(th) * r,
        y,
        z: Math.sin(th) * r,
        land,
        isCoreCIS
      });
    }
    return pts;
  })();

  const YANDEX_GRATICULES = (() => {
    const lines = [];
    for (let lat = -45; lat <= 65; lat += 22) {
      const pts = [];
      for (let lon = -180; lon <= 180; lon += 8) {
        const la = (lat * Math.PI) / 180, lo = (lon * Math.PI) / 180;
        pts.push({ vx: Math.cos(la) * Math.sin(lo), vy: -Math.sin(la), vz: Math.cos(la) * Math.cos(lo) });
      }
      lines.push(pts);
    }
    for (let lon = -180; lon < 180; lon += 24) {
      const pts = [];
      for (let lat = -70; lat <= 75; lat += 6) {
        const la = (lat * Math.PI) / 180, lo = (lon * Math.PI) / 180;
        pts.push({ vx: Math.cos(la) * Math.sin(lo), vy: -Math.sin(la), vz: Math.cos(la) * Math.cos(lo) });
      }
      lines.push(pts);
    }
    return lines;
  })();

  const YANDEX_HUBS = [
    { lat: 41.01, lon: 28.97, isOrigin: true },  // Istanbul
    { lat: 55.75, lon: 37.61, isOrigin: false }, // Moscow
    { lat: 59.93, lon: 30.33, isOrigin: false }, // St. Petersburg
    { lat: 43.23, lon: 76.88, isOrigin: false }, // Almaty
    { lat: 51.16, lon: 71.47, isOrigin: false }, // Astana
    { lat: 41.29, lon: 69.24, isOrigin: false }, // Tashkent
    { lat: 40.40, lon: 49.86, isOrigin: false }, // Baku
    { lat: 53.90, lon: 27.56, isOrigin: false }  // Minsk
  ].map(h => {
    const la = (h.lat * Math.PI) / 180;
    const lo = (h.lon * Math.PI) / 180;
    return {
      ...h,
      vx: Math.cos(la) * Math.sin(lo),
      vy: -Math.sin(la),
      vz: Math.cos(la) * Math.cos(lo)
    };
  });

  function projSpherePt(vx, vy, vz, radius, cx, cy, yaw, pitch) {
    // 1. Rotate around Y by yaw (center lon ~48E facing viewer at yaw = -0.84)
    const x1 = vx * Math.cos(yaw) + vz * Math.sin(yaw);
    const y1 = vy;
    const z1 = -vx * Math.sin(yaw) + vz * Math.cos(yaw);
    // 2. Tilt northern hemisphere toward viewer (negative pitch tilts +Z up and -Y forward)
    const y2 = y1 * Math.cos(pitch) + z1 * Math.sin(pitch);
    const z2 = -y1 * Math.sin(pitch) + z1 * Math.cos(pitch);
    return { x: cx + x1 * radius, y: cy + y2 * radius, z: z2 };
  }

  function renderYandexAds(c, w, h, dpr, elapsed) {
    const W = 900, H = 900;
    const sc = Math.min(w / W, h / H);
    const loop = 14.0;
    const phase = ((elapsed % loop) / loop) * Math.PI * 2;

    c.save();
    c.scale(dpr, dpr);
    drawStudioBackground(c, w, h, '245, 158, 11', Math.sin(phase) * 0.5 + 0.5);
    c.translate(w * 0.5, h * 0.5);
    c.scale(sc, sc);
    c.translate(-W * 0.5, -H * 0.5);

    const gCx = 490, gCy = 415, gR = 242;
    const yaw = -0.86 + Math.sin(phase) * 0.24;
    const pitch = 0.52 + Math.cos(phase) * 0.05;

    // Outer Orbital Ring
    c.save();
    c.translate(gCx, gCy);
    c.rotate(-0.18);
    c.scale(1, 0.36);
    c.beginPath();
    c.arc(0, 0, gR * 1.25, 0, Math.PI * 2);
    c.strokeStyle = 'rgba(245, 158, 11, 0.26)';
    c.lineWidth = 2;
    c.setLineDash([8, 8]);
    c.stroke();
    c.restore();

    // 3D Obsidian Sphere Body with Atmospheric Rim
    const sg = c.createRadialGradient(gCx - 75, gCy - 75, 20, gCx, gCy, gR);
    sg.addColorStop(0, '#1E293B');
    sg.addColorStop(0.62, '#0F172A');
    sg.addColorStop(1, '#060911');
    c.fillStyle = sg;
    c.beginPath();
    c.arc(gCx, gCy, gR, 0, Math.PI * 2);
    c.fill();
    c.strokeStyle = 'rgba(251, 191, 36, 0.38)';
    c.lineWidth = 1.8;
    c.stroke();

    // Subtle Graticule Lat/Lon Mesh on Front Hemisphere
    c.save();
    c.strokeStyle = 'rgba(148, 163, 184, 0.09)';
    c.lineWidth = 1;
    for (const line of YANDEX_GRATICULES) {
      c.beginPath();
      let penDown = false;
      for (const pt of line) {
        const p = projSpherePt(pt.vx, pt.vy, pt.vz, gR, gCx, gCy, yaw, pitch);
        if (p.z > 0.02) {
          if (!penDown) { c.moveTo(p.x, p.y); penDown = true; }
          else c.lineTo(p.x, p.y);
        } else {
          penDown = false;
        }
      }
      c.stroke();
    }
    c.restore();

    // Fibonacci Eurasia & CIS Landmass Nodes
    for (let i = 0; i < YANDEX_GLOBE_DOTS.length; i++) {
      const d = YANDEX_GLOBE_DOTS[i];
      const p = projSpherePt(d.x, d.y, d.z, gR, gCx, gCy, yaw, pitch);
      if (p.z < -0.05) continue;
      const alpha = clamp01((p.z + 0.05) / 0.95);
      c.beginPath();
      const rad = d.isCoreCIS ? 2.6 : (d.land ? 1.9 : 0.95);
      c.arc(p.x, p.y, rad, 0, Math.PI * 2);
      if (d.isCoreCIS) {
        c.fillStyle = `rgba(251, 191, 36, ${(alpha * 0.92).toFixed(3)})`;
      } else if (d.land) {
        c.fillStyle = `rgba(226, 232, 240, ${(alpha * 0.55).toFixed(3)})`;
      } else {
        c.fillStyle = `rgba(148, 163, 184, ${(alpha * 0.16).toFixed(3)})`;
      }
      c.fill();
    }

    // Geodesic Arcs from Origin Hub to CIS / International Markets
    const origin = YANDEX_HUBS[0];
    const pOrigin = projSpherePt(origin.vx, origin.vy, origin.vz, gR, gCx, gCy, yaw, pitch);

    for (let i = 1; i < YANDEX_HUBS.length; i++) {
      const target = YANDEX_HUBS[i];
      const pTarget = projSpherePt(target.vx, target.vy, target.vz, gR, gCx, gCy, yaw, pitch);
      if (pTarget.z < 0.05) continue;

      const mx = (origin.vx + target.vx) * 0.5;
      const my = (origin.vy + target.vy) * 0.5;
      const mz = (origin.vz + target.vz) * 0.5;
      const mLen = Math.hypot(mx, my, mz) || 1;
      const pMid = projSpherePt(mx / mLen, my / mLen, mz / mLen, gR * 1.24, gCx, gCy, yaw, pitch);

      c.save();
      c.beginPath();
      c.moveTo(pOrigin.x, pOrigin.y);
      c.quadraticCurveTo(pMid.x, pMid.y, pTarget.x, pTarget.y);
      c.strokeStyle = 'rgba(251, 191, 36, 0.62)';
      c.lineWidth = 2.2;
      c.stroke();

      // Traveling photon packet along Bezier curve
      const u = (elapsed * 0.48 + i * 0.17) % 1.0;
      const inv = 1 - u;
      const bx = inv * inv * pOrigin.x + 2 * inv * u * pMid.x + u * u * pTarget.x;
      const by = inv * inv * pOrigin.y + 2 * inv * u * pMid.y + u * u * pTarget.y;
      c.beginPath();
      c.arc(bx, by, 5, 0, Math.PI * 2);
      c.fillStyle = '#FEF08A';
      c.shadowColor = '#F59E0B';
      c.shadowBlur = 14;
      c.fill();
      c.restore();

      // Target Hub Pulsing Beacon
      const pulse = (elapsed * 0.8 + i * 0.25) % 1.0;
      c.beginPath();
      c.arc(pTarget.x, pTarget.y, 5 + pulse * 16, 0, Math.PI * 2);
      c.strokeStyle = `rgba(251, 191, 36, ${(1 - pulse) * 0.7})`;
      c.lineWidth = 1.8;
      c.stroke();

      c.beginPath();
      c.arc(pTarget.x, pTarget.y, 5.5, 0, Math.PI * 2);
      c.fillStyle = '#FFFFFF';
      c.fill();
      c.strokeStyle = '#F59E0B';
      c.lineWidth = 2;
      c.stroke();
    }

    // Origin Hub Beacon (Istanbul)
    if (pOrigin.z > 0) {
      c.beginPath();
      c.arc(pOrigin.x, pOrigin.y, 8, 0, Math.PI * 2);
      c.fillStyle = '#EF4444';
      c.fill();
      c.strokeStyle = '#FFFFFF';
      c.lineWidth = 2.2;
      c.stroke();
    }

    // Foreground 3D Isometric Yandex Direct Search & YAN Ad Slab (Bottom-Left)
    const cam = createCam(265, 620, 0.86, 0.52, -0.35);
    const zSlab = 22 + Math.sin(phase) * 8;
    drawExtrudedSlab(
      c, -155, -95, 310, 175, 18, zSlab, 13, cam,
      '#F8FAFC', '#CBD5E1', '#FFFFFF', 0.58
    );
    c.save();
    applyIsoPlane(c, zSlab + 0.6, cam);
    roundRectPath(c, -135, -75, 270, 38, 10);
    c.fillStyle = '#FFFFFF';
    c.fill();
    c.strokeStyle = '#F59E0B';
    c.lineWidth = 2.2;
    c.stroke();

    roundRectPath(c, 82, -71, 49, 30, 7);
    c.fillStyle = '#EF4444';
    c.fill();

    roundRectPath(c, -120, -61, 130, 10, 5);
    c.fillStyle = '#0F172A';
    c.fill();

    for (let k = 0; k < 2; k++) {
      const tx = -135 + k * 140;
      roundRectPath(c, tx, -22, 130, 82, 12);
      c.fillStyle = '#F1F5F9';
      c.fill();
      roundRectPath(c, tx + 12, -10, 42, 42, 8);
      c.fillStyle = k === 0 ? 'rgba(245, 158, 11, 0.22)' : 'rgba(15, 23, 42, 0.08)';
      c.fill();
      roundRectPath(c, tx + 64, -4, 52, 9, 4.5);
      c.fillStyle = '#0F172A';
      c.fill();
      roundRectPath(c, tx + 64, 12, 38, 8, 4);
      c.fillStyle = '#64748B';
      c.fill();
      roundRectPath(c, tx + 12, 42, 106, 8, 4);
      c.fillStyle = '#10B981';
      c.fill();
    }
    c.restore();

    c.restore();
  }

  // ============================================================================
  // CHANNEL 5: BING ADS (3D Enterprise Desktop Browser, Multi-Engine Prism & Low-CPC Gauge)
  // ============================================================================
  function renderBingAds(c, w, h, dpr, elapsed) {
    const W = 900, H = 900;
    const sc = Math.min(w / W, h / H);
    const loop = 12.0;
    const t = elapsed % loop;
    const phase = (t / loop) * Math.PI * 2;

    c.save();
    c.scale(dpr, dpr);
    drawStudioBackground(c, w, h, '56, 189, 248', Math.sin(phase) * 0.5 + 0.5);
    c.translate(w * 0.5, h * 0.5);
    c.scale(sc, sc);
    c.translate(-W * 0.5, -H * 0.5);

    const cam = createCam(
      450 + Math.sin(phase) * 9,
      475 + Math.cos(phase) * 8,
      0.86 + Math.sin(phase) * 0.014,
      0.55 + Math.cos(phase) * 0.025,
      -0.42 + Math.sin(phase * 0.5) * 0.045
    );

    const z0 = -45;
    const zDesktop = 20 + Math.sin(phase) * 6;
    const zCards = 80 + Math.cos(phase) * 9;

    // Layer 0: Microsoft Search Network Architectural Base
    drawBaseGridSlab(c, cam, z0, 560, 440, 'rgba(56, 189, 248, 0.42)');

    // Layer 1: 3D Isometric Enterprise Widescreen Desktop Browser Slab
    drawExtrudedSlab(
      c, -255, -185, 510, 350, 22, zDesktop, 15, cam,
      '#F8FAFC', '#CBD5E1', '#FFFFFF', 0.55
    );

    c.save();
    applyIsoPlane(c, zDesktop + 0.8, cam);
    // Desktop Browser Top Chrome Header
    roundRectPath(c, -255, -185, 510, 44, [22, 22, 0, 0]);
    c.fillStyle = '#0F172A';
    c.fill();
    // Window controls
    const dotColors = ['#64748B', '#475569', '#38BDF8'];
    for (let d = 0; d < 3; d++) {
      c.beginPath();
      c.arc(-228 + d * 16, -163, 4.5, 0, Math.PI * 2);
      c.fillStyle = dotColors[d];
      c.fill();
    }
    // Omnibox Search Bar in Browser Header
    roundRectPath(c, -155, -175, 310, 24, 12);
    c.fillStyle = 'rgba(255, 255, 255, 0.12)';
    c.fill();
    roundRectPath(c, -138, -167, 140, 8, 4);
    c.fillStyle = '#38BDF8';
    c.fill();

    // Multi-Engine Routing Hub inside Desktop Canvas (Bing + Yahoo + DuckDuckGo)
    const colXs = [-165, 0, 165];
    const colAccents = ['#0284C7', '#6366F1', '#10B981'];

    for (let i = 0; i < 3; i++) {
      const cx = colXs[i];
      c.beginPath();
      c.moveTo(0, -132);
      c.bezierCurveTo(0, -108, cx, -112, cx, -88);
      c.strokeStyle = 'rgba(2, 132, 199, 0.35)';
      c.lineWidth = 2;
      c.stroke();

      const sp = (elapsed * 0.55 + i * 0.33) % 1.0;
      const sx = lerp(0, cx, smoothstep(0, 1, sp));
      const sy = lerp(-132, -88, sp);
      c.beginPath();
      c.arc(sx, sy, 4.5, 0, Math.PI * 2);
      c.fillStyle = colAccents[i];
      c.fill();

      roundRectPath(c, cx - 72, -86, 144, 224, 14);
      c.fillStyle = '#F1F5F9';
      c.fill();
      c.strokeStyle = 'rgba(15, 23, 42, 0.08)';
      c.lineWidth = 1.2;
      c.stroke();

      c.beginPath();
      c.arc(cx - 42, -56, 14, 0, Math.PI * 2);
      c.fillStyle = colAccents[i];
      c.fill();
      drawCheck(c, cx - 42, -56, 10, '#FFFFFF');

      roundRectPath(c, cx - 18, -62, 74, 10, 5);
      c.fillStyle = '#0F172A';
      c.fill();

      for (let r = 0; r < 3; r++) {
        const ry = -22 + r * 48;
        roundRectPath(c, cx - 58, ry, 116, 36, 8);
        c.fillStyle = '#FFFFFF';
        c.fill();
        roundRectPath(c, cx - 48, ry + 10, 72, 7, 3.5);
        c.fillStyle = r === 0 ? colAccents[i] : '#475569';
        c.fill();
        roundRectPath(c, cx - 48, ry + 22, 92, 5, 2.5);
        c.fillStyle = '#CBD5E1';
        c.fill();
      }
    }
    c.restore();

    // Layer 2: Floating 3D CPC vs ROAS Efficiency Balance Slab (Front Right)
    drawExtrudedSlab(
      c, 45, 35, 235, 145, 18, zCards, 12, cam,
      '#0F172A', '#020617', 'rgba(56, 189, 248, 0.55)', 0.48
    );
    c.save();
    applyIsoPlane(c, zCards + 0.6, cam);
    roundRectPath(c, 75, 118, 44, 38, 8);
    c.fillStyle = '#334155';
    c.fill();
    c.strokeStyle = '#38BDF8';
    c.lineWidth = 2.4;
    c.lineCap = 'round';
    c.beginPath();
    c.moveTo(97, 86); c.lineTo(97, 106);
    c.moveTo(90, 99); c.lineTo(97, 106); c.lineTo(104, 99);
    c.stroke();

    const roasH = 88 + Math.sin(phase * 2) * 8;
    roundRectPath(c, 145, 156 - roasH, 48, roasH, 8);
    const bg = c.createLinearGradient(145, 156 - roasH, 145, 156);
    bg.addColorStop(0, '#38BDF8');
    bg.addColorStop(1, '#10B981');
    c.fillStyle = bg;
    c.fill();

    c.strokeStyle = '#10B981';
    c.lineWidth = 2.6;
    c.beginPath();
    c.moveTo(216, 136); c.lineTo(216, 76);
    c.moveTo(208, 84); c.lineTo(216, 76); c.lineTo(224, 84);
    c.stroke();
    c.restore();

    c.restore();
  }

  // ============================================================================
  // CHANNEL 6: LINKEDIN ADS (3D Executive Decision-Maker Pyramid & ABM B2B Pipeline)
  // ============================================================================
  function renderLinkedInAds(c, w, h, dpr, elapsed) {
    const W = 900, H = 900;
    const sc = Math.min(w / W, h / H);
    const loop = 13.0;
    const t = elapsed % loop;
    const phase = (t / loop) * Math.PI * 2;

    c.save();
    c.scale(dpr, dpr);
    drawStudioBackground(c, w, h, '37, 99, 235', Math.sin(phase) * 0.5 + 0.5);
    c.translate(w * 0.5, h * 0.5);
    c.scale(sc, sc);
    c.translate(-W * 0.5, -H * 0.5);

    const cam = createCam(
      450 + Math.cos(phase) * 9,
      500 + Math.sin(phase) * 8,
      0.86 + Math.sin(phase) * 0.015,
      0.58 + Math.sin(phase) * 0.025,
      0.44 + Math.cos(phase * 0.5) * 0.045
    );

    const spread = 0.88 + 0.16 * Math.sin(phase);
    const zTier1 = -62 * spread;  // Industry & Enterprise Firmographics Foundation
    const zTier2 = 24 * spread;   // Department & Seniority Qualification Matrix
    const zTier3 = 122 * spread;  // C-Suite Decision Maker Target Lock (Apex)

    // Tier 1: Enterprise Firmographics Base Slab
    drawExtrudedSlab(
      c, -255, -195, 510, 390, 24, zTier1, 16, cam,
      '#111827', '#090D16', 'rgba(96, 165, 250, 0.32)', 0.55
    );
    c.save();
    applyIsoPlane(c, zTier1 + 0.8, cam);
    for (let r = 1; r <= 3; r++) {
      c.beginPath();
      c.arc(0, 0, r * 60, 0, Math.PI * 2);
      c.strokeStyle = 'rgba(96, 165, 250, 0.18)';
      c.lineWidth = 1.5;
      c.stroke();
    }
    const baseNodes = [[-185, -125], [185, -125], [-185, 125], [185, 125], [-205, 0], [205, 0]];
    for (const [nx, ny] of baseNodes) {
      c.beginPath();
      c.arc(nx, ny, 7.5, 0, Math.PI * 2);
      c.fillStyle = '#3B82F6';
      c.fill();
      c.beginPath();
      c.moveTo(nx, ny); c.lineTo(0, 0);
      c.strokeStyle = 'rgba(59, 130, 246, 0.22)';
      c.lineWidth = 1.3;
      c.stroke();
    }
    c.restore();

    // Vertical Optical Alignment Beams through all 3 Pyramid Tiers
    const beamPts = [[-145, -105], [145, -105], [-145, 105], [145, 105], [0, 0]];
    for (const [bx, by] of beamPts) {
      const p1 = project3D(bx, by, zTier1, cam);
      const p2 = project3D(bx * 0.5, by * 0.5, zTier3, cam);
      c.save();
      c.strokeStyle = bx === 0 ? 'rgba(96, 165, 250, 0.6)' : 'rgba(96, 165, 250, 0.25)';
      c.lineWidth = bx === 0 ? 2.4 : 1.3;
      if (bx !== 0) c.setLineDash([4, 5]);
      c.beginPath(); c.moveTo(p1.x, p1.y); c.lineTo(p2.x, p2.y); c.stroke();
      c.restore();
    }

    // Tier 2: Porcelain Mid-Tier Slab (Account & Role Qualification Matrix)
    drawExtrudedSlab(
      c, -185, -138, 370, 276, 20, zTier2, 14, cam,
      '#F8FAFC', '#CBD5E1', '#FFFFFF', 0.48
    );
    c.save();
    applyIsoPlane(c, zTier2 + 0.8, cam);
    const tileCoords = [[-162, -114], [12, -114], [-162, 12], [12, 12]];
    tileCoords.forEach(([tx, ty], idx) => {
      const isTarget = idx === 0 || idx === 3;
      roundRectPath(c, tx, ty, 150, 102, 12);
      c.fillStyle = isTarget ? '#FFFFFF' : '#F1F5F9';
      c.fill();
      c.strokeStyle = isTarget ? '#2563EB' : 'rgba(15, 23, 42, 0.08)';
      c.lineWidth = isTarget ? 1.8 : 1;
      c.stroke();

      c.beginPath();
      c.arc(tx + 28, ty + 32, 13, 0, Math.PI * 2);
      c.fillStyle = isTarget ? '#2563EB' : '#94A3B8';
      c.fill();
      c.fillStyle = '#FFFFFF';
      c.beginPath(); c.arc(tx + 28, ty + 28, 4.2, 0, Math.PI * 2); c.fill();
      c.beginPath(); c.arc(tx + 28, ty + 40, 7.5, Math.PI * 1.15, Math.PI * 1.85); c.fill();

      roundRectPath(c, tx + 50, ty + 22, 78, 9, 4.5);
      c.fillStyle = '#0F172A';
      c.fill();
      roundRectPath(c, tx + 50, ty + 37, 56, 7, 3.5);
      c.fillStyle = '#64748B';
      c.fill();

      roundRectPath(c, tx + 16, ty + 74, 118, 8, 4);
      c.fillStyle = '#E2E8F0';
      c.fill();
      roundRectPath(c, tx + 16, ty + 74, isTarget ? 102 : 52, 8, 4);
      c.fillStyle = isTarget ? '#10B981' : '#94A3B8';
      c.fill();
    });
    c.restore();

    // Tier 3 (Apex): C-Suite Decision-Maker Target Lock Vault Slab
    drawExtrudedSlab(
      c, -108, -80, 216, 160, 18, zTier3, 14, cam,
      '#0F172A', '#020617', '#60A5FA', 0.54
    );
    c.save();
    applyIsoPlane(c, zTier3 + 0.8, cam);
    const lockPulse = 0.5 + 0.5 * Math.sin(phase * 2.5);
    c.beginPath();
    c.arc(0, -10, 42 + lockPulse * 6, 0, Math.PI * 2);
    c.strokeStyle = 'rgba(96, 165, 250, 0.48)';
    c.lineWidth = 1.8;
    c.stroke();

    c.beginPath();
    c.arc(0, -10, 30, 0, Math.PI * 2);
    const ag = c.createLinearGradient(-30, -40, 30, 20);
    ag.addColorStop(0, '#3B82F6');
    ag.addColorStop(1, '#1D4ED8');
    c.fillStyle = ag;
    c.fill();

    drawCheck(c, 0, -10, 22, '#FFFFFF');

    roundRectPath(c, -72, 42, 144, 22, 11);
    c.fillStyle = 'rgba(16, 185, 129, 0.18)';
    c.fill();
    c.strokeStyle = 'rgba(16, 185, 129, 0.5)';
    c.lineWidth = 1.2;
    c.stroke();
    c.beginPath();
    c.arc(-52, 53, 5, 0, Math.PI * 2);
    c.fillStyle = '#10B981';
    c.fill();
    roundRectPath(c, -38, 49, 92, 8, 4);
    c.fillStyle = '#FFFFFF';
    c.fill();
    c.restore();

    c.restore();
  }

  // ============================================================================
  // MOUNTING & 60 FPS ANIMATION LOOP ACROSS ALL 6 PERFORMANCE MARKETING ROWS
  // ============================================================================
  const RENDERERS = [
    renderGoogleAds,
    renderMetaAds,
    renderTikTokAds,
    renderYandexAds,
    renderBingAds,
    renderLinkedInAds
  ];

  const rowStates = RENDERERS.map(() => ({
    canvas: null,
    ctx: null,
    w: 580,
    h: 580,
    dpr: 1,
    visible: true
  }));

  let ioAttached = false;
  const startTime = performance.now();

  function disableNativeMedia(container) {
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
    const imgs = container.querySelectorAll('img');
    imgs.forEach(img => {
      if (!img.dataset.roasistDisabled) {
        img.dataset.roasistDisabled = 'true';
        img.removeAttribute('data-src');
        img.removeAttribute('data-srcset');
      }
    });
  }

  const GADS_SVG_HTML = `<div class="gads-anim-stage" aria-hidden="true">
  <svg viewBox="0 0 600 320" class="gads-svg" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="gradGreen" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#34A853" stop-opacity="0.95"/>
        <stop offset="100%" stop-color="#34A853" stop-opacity="0"/>
      </linearGradient>
      <linearGradient id="gradYellow" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#FBBC05" stop-opacity="0.95"/>
        <stop offset="100%" stop-color="#FBBC05" stop-opacity="0"/>
      </linearGradient>
      <linearGradient id="gradBlue" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#4285F4" stop-opacity="0.95"/>
        <stop offset="100%" stop-color="#4285F4" stop-opacity="0"/>
      </linearGradient>
    </defs>

    <g class="grid-lines">
      <line x1="120" y1="95"  x2="480" y2="95"  stroke="#CBD5E1" stroke-width="1.5"/>
      <line x1="120" y1="130" x2="480" y2="130" stroke="#CBD5E1" stroke-width="1.5"/>
      <line x1="120" y1="165" x2="480" y2="165" stroke="#CBD5E1" stroke-width="1.5"/>
      <line x1="120" y1="200" x2="480" y2="200" stroke="#CBD5E1" stroke-width="1.5"/>
    </g>

    <g class="bars-phase">
      <g class="col-group col-green">
        <rect x="172" y="100" width="56" height="145" fill="url(#gradGreen)" class="bar-tail"/>
        <circle cx="200" cy="100" r="28" fill="#34A853"/>
        <text x="200" y="109" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="25">$</text>
      </g>

      <g class="col-group col-yellow">
        <rect x="272" y="100" width="56" height="145" fill="url(#gradYellow)" class="bar-tail"/>
        <circle cx="300" cy="100" r="28" fill="#FBBC05"/>
        <path d="M289 95h22l2 5h-26l2-5zm1 6h20v11h-6v-6h-8v6h-6v-11z" fill="#FFFFFF"/>
      </g>

      <g class="col-group col-blue">
        <rect x="372" y="100" width="56" height="145" fill="url(#gradBlue)" class="bar-tail"/>
        <circle cx="400" cy="100" r="28" fill="#4285F4"/>
        <circle cx="400" cy="94" r="4.5" fill="#FFFFFF"/>
        <path d="M391 107c0-4 4-6 9-6s9 2 9 6" fill="#FFFFFF"/>
        <circle cx="390" cy="96" r="3.2" fill="#FFFFFF" opacity="0.85"/>
        <circle cx="410" cy="96" r="3.2" fill="#FFFFFF" opacity="0.85"/>
      </g>
    </g>

    <g class="logo-assembly">
      <g class="pill-yellow-wrap">
        <rect x="282" y="95" width="36" height="112" rx="18" fill="#FBBC05" transform="rotate(30 300 151)"/>
      </g>
      <g class="dot-green-wrap">
        <circle cx="272" cy="199" r="18" fill="#34A853"/>
      </g>
      <g class="pill-blue-wrap">
        <rect x="282" y="95" width="36" height="112" rx="18" fill="#4285F4" transform="rotate(-30 300 151)"/>
      </g>
    </g>

    <g class="brand-text">
      <text x="235" y="175" font-family="'Product Sans', 'Inter', Arial, sans-serif" font-size="44" font-weight="500" fill="#5F6368" letter-spacing="-0.5">
        Google Ads
      </text>
    </g>
  </svg>
</div>`;

  function ensureMounted() {
    const rows = document.querySelectorAll('.TextImageRows_row__PPlpB');
    if (!rows || rows.length === 0) return;

    if (!ioAttached && 'IntersectionObserver' in window) {
      ioAttached = true;
      const io = new IntersectionObserver((entries) => {
        for (const entry of entries) {
          const idx = Number(entry.target.dataset.roasistChannelIdx);
          if (!Number.isNaN(idx) && rowStates[idx]) {
            rowStates[idx].visible = entry.isIntersecting;
          }
        }
      }, { rootMargin: '180px 0px', threshold: 0.01 });

      rows.forEach((row, idx) => {
        if (idx < rowStates.length) {
          row.dataset.roasistChannelIdx = String(idx);
          io.observe(row);
        }
      });
    }

    rows.forEach((row, idx) => {
      if (idx >= rowStates.length) return;
      const mediaBox = row.querySelector('.TextImageRows_media__twu3R .ImageEnter_image__FSEP_')
                    || row.querySelector('.TextImageRows_media__twu3R');
      if (!mediaBox) return;

      disableNativeMedia(mediaBox);

      // Row 1 (Google Ads): Mount official SVG brand-motion stage
      if (idx === 0) {
        const oldCv = mediaBox.querySelector('canvas.roasist-perf-channel-canvas');
        if (oldCv) oldCv.remove();
        rowStates[0].canvas = null;
        rowStates[0].ctx = null;
        if (!mediaBox.querySelector('.gads-anim-stage')) {
          mediaBox.insertAdjacentHTML('beforeend', GADS_SVG_HTML);
        }
        return;
      }

      let cv = mediaBox.querySelector('canvas.roasist-perf-channel-canvas');
      const st = rowStates[idx];
      if (!cv) {
        cv = document.createElement('canvas');
        cv.className = 'roasist-perf-channel-canvas';
        cv.setAttribute('aria-hidden', 'true');
        mediaBox.appendChild(cv);
        st.canvas = cv;
        st.ctx = cv.getContext('2d', { alpha: false });
      }
      const rect = mediaBox.getBoundingClientRect();
      if (rect.width > 40 && rect.height > 40) {
        const d = Math.min(window.devicePixelRatio || 1, 2);
        const tw = Math.floor(rect.width);
        const th = Math.floor(rect.height);
        if (st.w !== tw || st.h !== th || st.dpr !== d || cv.width !== tw * d) {
          st.w = tw;
          st.h = th;
          st.dpr = d;
          cv.width = tw * d;
          cv.height = th * d;
        }
      }
    });
  }

  function tick(now) {
    requestAnimationFrame(tick);
    try {
      ensureMounted();
    } catch {}

    if (document.hidden) return;
    const elapsed = (now - startTime) * 0.001;

    for (let i = 0; i < rowStates.length; i++) {
      const st = rowStates[i];
      if (st.ctx && st.visible) {
        try {
          RENDERERS[i](st.ctx, st.w, st.h, st.dpr, elapsed);
        } catch {}
      }
    }
  }

  requestAnimationFrame(tick);
})();
</script>"""

# Neutral local SVG placeholder so Next.js/lazysizes never downloads external KOTA MP4s/PNGs/JPGs
NEUTRAL_PLACEHOLDER = "/roasist-logo.svg"

EXTERNAL_MEDIA_REPLACEMENTS = [
    ("/images/roasist-logo.svg", NEUTRAL_PLACEHOLDER),
    ("https://kota-content.b-cdn.net/app/uploads/2023/11/Animation-1-Bipsync-1.mp4", NEUTRAL_PLACEHOLDER),
    ("https://kota-content.b-cdn.net/app/uploads/2023/11/seo-geo-V2.mp4", NEUTRAL_PLACEHOLDER),
    (
        "https://kota-content.b-cdn.net/app/uploads/2023/11/Web-Development-backrate-2.png 1224w, "
        "https://kota-content.b-cdn.net/app/uploads/2023/11/Web-Development-backrate-2-500x500.png 500w, "
        "https://kota-content.b-cdn.net/app/uploads/2023/11/Web-Development-backrate-2-768x768.png 768w",
        "",
    ),
    ("https://kota-content.b-cdn.net/app/uploads/2023/11/Web-Development-backrate-2.png", NEUTRAL_PLACEHOLDER),
    (
        "https://kota-content.b-cdn.net/app/uploads/2023/11/Wordpress-and-cms-mealeo.png 1224w, "
        "https://kota-content.b-cdn.net/app/uploads/2023/11/Wordpress-and-cms-mealeo-500x500.png 500w, "
        "https://kota-content.b-cdn.net/app/uploads/2023/11/Wordpress-and-cms-mealeo-768x768.png 768w",
        "",
    ),
    ("https://kota-content.b-cdn.net/app/uploads/2023/11/Wordpress-and-cms-mealeo.png", NEUTRAL_PLACEHOLDER),
    (
        "https://kota-content.b-cdn.net/app/uploads/2023/11/copywriting-2-1.jpg 1224w, "
        "https://kota-content.b-cdn.net/app/uploads/2023/11/copywriting-2-1-500x500.jpg 500w, "
        "https://kota-content.b-cdn.net/app/uploads/2023/11/copywriting-2-1-768x768.jpg 768w",
        "",
    ),
    ("https://kota-content.b-cdn.net/app/uploads/2023/11/copywriting-2-1.jpg", NEUTRAL_PLACEHOLDER),
    (
        "https://kota-content.b-cdn.net/app/uploads/2023/11/sitecare.jpg 1224w, "
        "https://kota-content.b-cdn.net/app/uploads/2023/11/sitecare-500x500.jpg 500w, "
        "https://kota-content.b-cdn.net/app/uploads/2023/11/sitecare-768x768.jpg 768w",
        "",
    ),
    ("https://kota-content.b-cdn.net/app/uploads/2023/11/sitecare.jpg", NEUTRAL_PLACEHOLDER),
]


def inject_file(rel_path: str):
    p = ROOT / rel_path
    if not p.exists():
        print(f"[SKIP] {rel_path} does not exist")
        return

    html = p.read_text(encoding="utf-8")

    # Remove any previous injection
    html = re.sub(
        r"<style data-roasist-perf-channels-3d-style>.*?</style>\s*<script data-roasist-perf-channels-3d-script>.*?</script>",
        "",
        html,
        flags=re.DOTALL,
    )

    # Update Flight push stream safely via parse_flight_stream + serialize_flight_stream
    push_re = re.compile(r"self\.__next_f\.push\(\[1,\s*(\"(?:\\.|[^\"\\])*\")\]\)")
    pushes = list(push_re.finditer(html))
    if len(pushes) == 1:
        pm = pushes[0]
        flight_str = json.loads(pm.group(1))
        records = parse_flight_stream(flight_str)
        for rec in records:
            if rec[0] == "line" and rec[1] == "34":
                for old_val, new_val in EXTERNAL_MEDIA_REPLACEMENTS:
                    rec[2] = rec[2].replace(old_val, new_val)
        new_flight_str = serialize_flight_stream(records)
        assert serialize_flight_stream(parse_flight_stream(new_flight_str)) == new_flight_str
        encoded_flight = json.dumps(new_flight_str, ensure_ascii=False).replace("</script>", "<\\/script>")
        new_push = f"self.__next_f.push([1,{encoded_flight}])"

        before_push = html[: pm.start()]
        after_push = html[pm.end() :]
        for old_val, new_val in EXTERNAL_MEDIA_REPLACEMENTS:
            before_push = before_push.replace(old_val, new_val)
            after_push = after_push.replace(old_val, new_val)
        html = before_push + new_push + after_push
    else:
        for old_val, new_val in EXTERNAL_MEDIA_REPLACEMENTS:
            html = html.replace(old_val, new_val)

    if "</body>" in html:
        html = html.replace("</body>", PERF_CHANNELS_3D_BLOCK + "</body>", 1)

    p.write_text(html, encoding="utf-8")
    print(f"[OK] Injected 6x 3D Channel Canvases into {rel_path} ({len(html):,} bytes)")


def main():
    for rel in TARGET_FILES:
        inject_file(rel)


if __name__ == "__main__":
    main()
