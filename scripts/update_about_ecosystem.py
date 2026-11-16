#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Replaces KOTA's broken `/matter/*.png` BailoutToCSR placeholder inside
`<section class="Culture_culture__lmpEt">` on `/hakkimizda/` (and `/en/who-we-are/` via build_en_about)
with Concept A: "Manyetik Büyüme Ekosistemi" (Magnetic Growth Ecosystem — Orbital Physics Stage).

Maintains 100% parity between SSR HTML and Next.js React Flight AST (`self.__next_f.push`),
eliminates all `/matter/*.png` 404 requests, and renders a crisp HiDPI 2D Canvas ecosystem
with interactive principle capsules, monochrome channel/tech discs, magnetic orbital pull,
and zero-layout-shift live commitment details.
"""

import json
import os
import re
import sys

ROOT = "/home/antigravity/Roasist/roasist-web"
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from apply_phase1_cleanup import PUSH_RE, find_node_by_class, rewrite_flight_in_html  # noqa: E402

DEFAULT_HINT_TR = "Keşfetmek için ilkeleri ve kanalları sürükleyin veya bir düğüme tıklayın."
DEFAULT_HINT_EN = "Drag or click any principle or channel node to explore."

ROASIST_ECOSYSTEM_CSS = """
/* Hakkımızda / Who We Are — Concept A: Magnetic Growth Ecosystem */
.Culture_culture__lmpEt{
  margin:0 0 clamp(4rem,8vh,6.5rem)!important;
  padding:clamp(1rem,2vw,2rem) 0 0;
  position:relative;
  overflow:hidden;
  z-index:2;
}
.roasist-ecosystem{
  width:100%;
  max-width:1680px;
  margin:0 auto clamp(1.5rem,2.8vw,2.5rem);
  padding:0 clamp(1rem,3vw,2.5rem);
  display:flex;
  flex-direction:column;
  align-items:center;
}
.roasist-ecosystem__stage{
  position:relative;
  width:100%;
  height:clamp(390px,42vw,560px);
  border-radius:28px;
  overflow:hidden;
  user-select:none;
  -webkit-user-select:none;
}
@media (max-width:768px){
  .roasist-ecosystem{
    padding:0 0.75rem;
    margin-bottom:1.25rem;
  }
  .roasist-ecosystem__stage{
    height:clamp(370px,96vw,430px);
    border-radius:22px;
  }
}
.roasist-ecosystem__stage canvas{
  display:block;
  width:100%;
  height:100%;
  touch-action:pan-y;
}
.roasist-ecosystem__detail{
  min-height:48px;
  max-width:1080px;
  width:fit-content;
  margin:0.5rem auto 0;
  padding:0.55rem 1.35rem;
  border-radius:999px;
  background:rgba(255,255,255,0.74);
  border:1px solid rgba(15,23,42,0.09);
  backdrop-filter:blur(10px);
  -webkit-backdrop-filter:blur(10px);
  display:flex;
  align-items:center;
  justify-content:center;
  gap:0.625rem;
  text-align:center;
  font-size:clamp(0.84rem,0.95vw,0.93rem);
  line-height:1.4;
  color:#475569;
  font-variant-numeric:tabular-nums;
  transition:border-color 170ms cubic-bezier(0.22,1,0.36,1),background-color 170ms cubic-bezier(0.22,1,0.36,1),box-shadow 170ms cubic-bezier(0.22,1,0.36,1);
}
@media (min-width:1024px){
  .roasist-ecosystem__detail{
    height:48px;
    white-space:nowrap;
  }
}
.roasist-ecosystem__detail.is-active{
  background:rgba(255,255,255,0.93);
  border-color:rgba(124,58,237,0.28);
  box-shadow:0 8px 24px rgba(15,23,42,0.06);
}
@media (max-width:768px){
  .roasist-ecosystem__detail{
    width:100%;
    height:76px;
    min-height:76px;
    border-radius:16px;
    flex-direction:column;
    justify-content:center;
    padding:0.55rem 1rem;
    gap:0.25rem;
  }
  .roasist-ecosystem__dot{
    display:none;
  }
  .roasist-ecosystem__label:not(:empty)::after{
    display:none;
  }
}
.roasist-ecosystem__dot{
  width:7px;
  height:7px;
  border-radius:999px;
  background:#7c3aed;
  box-shadow:0 0 0 4px rgba(124,58,237,0.14);
  flex-shrink:0;
}
.roasist-ecosystem__label{
  font-weight:600;
  color:#0f172a;
  letter-spacing:-0.01em;
  white-space:nowrap;
}
.roasist-ecosystem__label:empty{
  display:none;
}
.roasist-ecosystem__label:not(:empty)::after{
  content:"—";
  margin-left:0.55rem;
  color:#94a3b8;
  font-weight:400;
}
.roasist-ecosystem__desc{
  color:#334155;
}
body.dark .roasist-ecosystem__detail{
  background:rgba(15,23,42,0.72);
  border-color:rgba(255,255,255,0.14);
  color:rgba(255,255,255,0.78);
}
body.dark .roasist-ecosystem__label{
  color:#ffffff;
}
body.dark .roasist-ecosystem__desc{
  color:rgba(255,255,255,0.82);
}
"""

ROASIST_ECOSYSTEM_SCRIPT = r"""<script data-roasist-ecosystem-js>
(function(){
  function initEcosystem(root) {
    if (!root) return;
    var stage = root.querySelector('.roasist-ecosystem__stage');
    if (!stage || stage.querySelector('canvas')) return;

    var isEn = (document.documentElement.lang || '').toLowerCase().indexOf('en') === 0 ||
               window.location.pathname.indexOf('/en/') !== -1;
    var reducedMotion = false;
    try { reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) {}

    var detailWrap = root.querySelector('.roasist-ecosystem__detail');
    var labelEl = root.querySelector('.roasist-ecosystem__label');
    var descEl = root.querySelector('.roasist-ecosystem__desc');
    var defaultHint = isEn
      ? 'Drag or click any principle or channel node to explore.'
      : 'Keşfetmek için ilkeleri ve kanalları sürükleyin veya bir düğüme tıklayın.';

    var CORE_SPEC = isEn
      ? {
          id: 'core', kind: 'core', label: 'ROASIST',
          title: 'ROASIST Core',
          desc: 'Unified growth architecture uniting paid media, enterprise SEO/AEO, creative, and web engineering.'
        }
      : {
          id: 'core', kind: 'core', label: 'ROASİST',
          title: 'ROASİST Çekirdek',
          desc: 'Performans pazarlaması, kurumsal SEO/AEO, kreatif ve web mühendisliğini tek merkezde birleştiren büyüme mimarisi.'
        };

    var PILL_SPECS = isEn
      ? [
          { id: 'p1', kind: 'pill', theme: 'dark',  ax: -0.30, ay: -0.29, tilt: -0.08, label: 'Data-First Decisions',    desc: 'Every strategy is built on verified conversion signals and real search demand—never guesswork.' },
          { id: 'p2', kind: 'pill', theme: 'light', ax:  0.30, ay: -0.28, tilt:  0.07, label: '100% Account Ownership',  desc: 'Every ad account, pixel, and analytics property belongs 100% to your company from day one.' },
          { id: 'p3', kind: 'pill', theme: 'dark',  ax: -0.34, ay:  0.05, tilt:  0.05, label: '24/7 Live Reporting',     desc: 'Track spend, CPA, pipeline quality, and net ROAS anytime via live Looker Studio dashboards.' },
          { id: 'p4', kind: 'pill', theme: 'light', ax:  0.34, ay:  0.06, tilt: -0.06, label: 'Full Accountability',     desc: 'We own your commercial revenue and growth targets with the same discipline as our own business.' },
          { id: 'p5', kind: 'pill', theme: 'dark',  ax: -0.26, ay:  0.32, tilt: -0.05, label: 'Agile Optimization',      desc: 'Weekly creative A/B testing and bid refinements systematically lower your acquisition costs.' },
          { id: 'p6', kind: 'pill', theme: 'light', ax:  0.26, ay:  0.32, tilt:  0.06, label: 'Measurable ROAS',         desc: 'Every impression and click is engineered around net revenue, qualified leads, and profitable return.' }
        ]
      : [
          { id: 'p1', kind: 'pill', theme: 'dark',  ax: -0.30, ay: -0.29, tilt: -0.08, label: 'Veriyle Karar',           desc: 'Tahminlerle değil, gerçek arama hacimleri ve doğrulanmış dönüşüm verileriyle strateji kurarız.' },
          { id: 'p2', kind: 'pill', theme: 'light', ax:  0.30, ay: -0.28, tilt:  0.07, label: '%100 Hesap Mülkiyeti',    desc: 'Tüm reklam ve analitik hesapları doğrudan sizin adınıza açılır ve daima %100 sizin mülkiyetinizde kalır.' },
          { id: 'p3', kind: 'pill', theme: 'dark',  ax: -0.34, ay:  0.05, tilt:  0.05, label: '7/24 Canlı Raporlama',    desc: 'Canlı Looker Studio panelleriyle harcama, CPA ve net ROAS metriklerini her an şeffafça izlersiniz.' },
          { id: 'p4', kind: 'pill', theme: 'light', ax:  0.34, ay:  0.06, tilt: -0.06, label: 'Sorumluluk Bilinci',      desc: 'Bütçenizi sadece harcamaz; ticari büyüme hedeflerinizi kendi işimiz gibi uçtan uca sahipleniriz.' },
          { id: 'p5', kind: 'pill', theme: 'dark',  ax: -0.26, ay:  0.32, tilt: -0.05, label: 'Çevik Optimizasyon',      desc: 'Haftalık kreatif A/B testleri ve teklif optimizasyonlarıyla edinim maliyetlerini sürekli düşürürüz.' },
          { id: 'p6', kind: 'pill', theme: 'light', ax:  0.26, ay:  0.32, tilt:  0.06, label: 'Ölçülebilir ROAS',        desc: 'Her tıklamayı ve gösterimi net ciro, nitelikli talep ve kârlı yatırım getirisine bağlarız.' }
        ];

    var DISC_SPECS = isEn
      ? [
          { id: 'd1', kind: 'disc', icon: 'google',   ax:  0.00, ay: -0.35, label: 'Google',    title: 'Google Ads',        desc: 'High-intent demand capture across Google Search, Shopping, Performance Max, and YouTube.' },
          { id: 'd2', kind: 'disc', icon: 'meta',     ax: -0.17, ay: -0.16, label: 'Meta',      title: 'Meta Ads',          desc: 'Server-Side CAPI-powered full-funnel customer acquisition across Instagram and Facebook.' },
          { id: 'd3', kind: 'disc', icon: 'tiktok',   ax:  0.17, ay: -0.16, label: 'TikTok',    title: 'TikTok Ads',        desc: 'Scroll-stopping creative video hooks engineered for rapid customer acquisition on TikTok.' },
          { id: 'd4', kind: 'disc', icon: 'linkedin', ax: -0.18, ay:  0.18, label: 'LinkedIn',  title: 'LinkedIn Ads',      desc: 'Precision B2B pipeline targeting decision-makers by role, industry, and company scale.' },
          { id: 'd5', kind: 'disc', icon: 'yandex',   ax:  0.18, ay:  0.18, label: 'Yandex',    title: 'Yandex Ads',        desc: 'High-converting cross-border acquisition across CIS and global export markets via Yandex Direct.' },
          { id: 'd6', kind: 'disc', icon: 'ga4',      ax:  0.00, ay:  0.36, label: 'GA4 · GTM', title: 'GA4 & Server GTM',  desc: 'First-party Server-Side GTM, GA4, and Enhanced Conversions measurement infrastructure.' },
          { id: 'd7', kind: 'disc', icon: 'aeo',      ax:  0.42, ay: -0.12, label: 'SEO · AEO', title: 'Enterprise SEO & AEO', desc: 'Compounding authority across Google Search and AI answer engines like ChatGPT and Perplexity.' },
          { id: 'd8', kind: 'disc', icon: 'bing',     ax: -0.42, ay: -0.12, label: 'Bing',      title: 'Microsoft Bing Ads', desc: 'High-purchasing-power desktop and enterprise search reach across US, UK, and European markets.' }
        ]
      : [
          { id: 'd1', kind: 'disc', icon: 'google',   ax:  0.00, ay: -0.35, label: 'Google',    title: 'Google Ads',        desc: 'Google Arama, Alışveriş, Performance Max ve YouTube’da yüksek niyetli talep yakalama.' },
          { id: 'd2', kind: 'disc', icon: 'meta',     ax: -0.17, ay: -0.16, label: 'Meta',      title: 'Meta Ads',          desc: 'Instagram ve Facebook’ta CAPI destekli tam huni dönüşüm ve ölçekleme mimarisi.' },
          { id: 'd3', kind: 'disc', icon: 'tiktok',   ax:  0.17, ay: -0.16, label: 'TikTok',    title: 'TikTok Ads',        desc: 'Dikkat yakalayan kreatif video kurgularıyla hızlı ölçeklenen yeni nesil müşteri edinimi.' },
          { id: 'd4', kind: 'disc', icon: 'linkedin', ax: -0.18, ay:  0.18, label: 'LinkedIn',  title: 'LinkedIn Ads',      desc: 'Karar vericileri unvan, sektör ve şirket ölçeğine göre hedefleyen B2B talep üretimi.' },
          { id: 'd5', kind: 'disc', icon: 'yandex',   ax:  0.18, ay:  0.18, label: 'Yandex',    title: 'Yandex Ads',        desc: 'BDT ve uluslararası pazarlarda Yandex Direct ile yüksek dönüşümlü ihracat ve turizm erişimi.' },
          { id: 'd6', kind: 'disc', icon: 'ga4',      ax:  0.00, ay:  0.36, label: 'GA4 · GTM', title: 'GA4 & Server GTM',  desc: 'Sunucu taraflı (Server-Side) GTM, GA4 ve gelişmiş dönüşüm ölçümleme altyapısı.' },
          { id: 'd7', kind: 'disc', icon: 'aeo',      ax:  0.42, ay: -0.12, label: 'SEO · AEO', title: 'Kurumsal SEO & AEO', desc: 'Google organik aramalarda ve ChatGPT, Gemini, Perplexity yanıt motorlarında kalıcı otorite.' },
          { id: 'd8', kind: 'disc', icon: 'bing',     ax: -0.42, ay: -0.12, label: 'Bing',      title: 'Microsoft Bing Ads', desc: 'ABD, İngiltere ve Avrupa pazarlarında yüksek alım güçlü masaüstü ve kurumsal arama erişimi.' }
        ];

    var canvas = document.createElement('canvas');
    stage.innerHTML = '';
    stage.appendChild(canvas);
    var ctx = canvas.getContext('2d');

    var W = 0, H = 0, DPR = 1;
    var bodies = [];
    var hoveredBody = null;
    var pinnedBody = null;
    var draggedBody = null;
    var dragOffsetX = 0, dragOffsetY = 0;
    var pointerDownPos = null;
    var pointerMoved = false;
    var pointer = { x: -9999, y: -9999, vx: 0, vy: 0, active: false };
    var pulseRing = { active: false, r: 0, alpha: 0 };
    var orbitPhase = 0;
    var isVisible = true;
    var rafId = 0;
    var fontFamily = 'system-ui, -apple-system, sans-serif';

    function updateDetailBar(b) {
      var target = b || pinnedBody;
      if (!labelEl || !descEl || !detailWrap) return;
      if (target) {
        labelEl.textContent = target.title || target.label;
        descEl.textContent = target.desc;
        detailWrap.classList.add('is-active');
      } else {
        labelEl.textContent = '';
        descEl.textContent = defaultHint;
        detailWrap.classList.remove('is-active');
      }
    }

    function clamp(v, lo, hi) { return v < lo ? lo : (v > hi ? hi : v); }

    function closestPointsOnSegments(a1x, a1y, b1x, b1y, a2x, a2y, b2x, b2y) {
      var d1x = b1x - a1x, d1y = b1y - a1y;
      var d2x = b2x - a2x, d2y = b2y - a2y;
      var rx = a1x - a2x, ry = a1y - a2y;
      var a = d1x * d1x + d1y * d1y;
      var e = d2x * d2x + d2y * d2y;
      var f = d2x * rx + d2y * ry;
      var s = 0, t = 0;

      if (a <= 1e-6 && e <= 1e-6) {
        return { q1x: a1x, q1y: a1y, q2x: a2x, q2y: a2y };
      }
      if (a <= 1e-6) {
        t = clamp(f / e, 0, 1);
      } else {
        var c = d1x * rx + d1y * ry;
        if (e <= 1e-6) {
          s = clamp(-c / a, 0, 1);
        } else {
          var b = d1x * d2x + d1y * d2y;
          var denom = a * e - b * b;
          if (denom !== 0) {
            s = clamp((b * f - c * e) / denom, 0, 1);
          } else {
            s = 0;
          }
          t = (b * s + f) / e;
          if (t < 0) {
            t = 0;
            s = clamp(-c / a, 0, 1);
          } else if (t > 1) {
            t = 1;
            s = clamp((b - c) / a, 0, 1);
          }
        }
      }
      return {
        q1x: a1x + d1x * s,
        q1y: a1y + d1y * s,
        q2x: a2x + d2x * t,
        q2y: a2y + d2y * t
      };
    }

    function buildScene() {
      var rect = stage.getBoundingClientRect();
      W = Math.max(300, Math.round(rect.width || stage.clientWidth || 1200));
      H = Math.max(320, Math.round(rect.height || stage.clientHeight || 500));
      DPR = Math.min(window.devicePixelRatio || 1, 2);
      canvas.width = W * DPR;
      canvas.height = H * DPR;
      ctx.setTransform(DPR, 0, 0, DPR, 0, 0);

      try {
        var cs = window.getComputedStyle(document.body);
        if (cs && cs.fontFamily) fontFamily = cs.fontFamily;
      } catch (e) {}

      var mobile = W < 700;
      var tablet = W >= 700 && W < 1024;
      var cx = W * 0.5;
      var cy = H * 0.5;

      var coreH = mobile ? 46 : (tablet ? 54 : 62);
      var coreW = mobile ? 136 : (tablet ? 162 : 186);
      var pillH = mobile ? 34 : (tablet ? 42 : 48);
      var pillFont = mobile ? 12 : (tablet ? 13.5 : 15);
      var pillPadX = mobile ? 15 : (tablet ? 20 : 24);
      var discR = mobile ? 24 : (tablet ? 30 : 35);

      bodies = [];

      // 0: Center Core
      bodies.push({
        id: CORE_SPEC.id,
        kind: 'core',
        label: CORE_SPEC.label,
        title: CORE_SPEC.title,
        desc: CORE_SPEC.desc,
        x: cx, y: cy, vx: 0, vy: 0,
        angle: 0, omega: 0, restAngle: 0,
        w: coreW, h: coreH,
        halfSeg: (coreW - coreH) * 0.5,
        r: coreH * 0.5,
        mass: 16,
        invMass: 1 / 16,
        inertia: 48000,
        scale: 1,
        ax: 0, ay: 0
      });

      ctx.font = '500 ' + pillFont + 'px ' + fontFamily;
      PILL_SPECS.forEach(function(sp, idx) {
        var tw = ctx.measureText(sp.label).width;
        var pw = Math.round(tw + pillPadX * 2);
        var spreadX = mobile ? sp.ax * 1.08 : sp.ax;
        var spreadY = mobile ? sp.ay * 1.12 : sp.ay;
        var px = cx + spreadX * W;
        var py = cy + spreadY * H;
        var m = 2.0;
        bodies.push({
          id: sp.id,
          kind: 'pill',
          theme: sp.theme,
          label: sp.label,
          title: sp.label,
          desc: sp.desc,
          fontSize: pillFont,
          x: px, y: py, vx: 0, vy: 0,
          angle: sp.tilt, omega: 0, restAngle: sp.tilt * 0.5,
          w: pw, h: pillH,
          halfSeg: Math.max(0, (pw - pillH) * 0.5),
          r: pillH * 0.5,
          mass: m,
          invMass: 1 / m,
          inertia: Math.max(900, (m * (pw * pw + pillH * pillH)) / 12),
          scale: 1,
          ax: spreadX, ay: spreadY,
          orbitDir: idx % 2 === 0 ? 1 : -1
        });
      });

      DISC_SPECS.forEach(function(sp, idx) {
        if (mobile && sp.id === 'd8') return;
        // On compact mobile, reposition the far-right AEO disc neatly into upper-center balance
        var ax = (mobile && sp.id === 'd7') ? 0.0 : sp.ax;
        var ay = (mobile && sp.id === 'd7') ? -0.18 : sp.ay;
        var px = cx + ax * W;
        var py = cy + ay * H;
        var m = 1.25;
        var d = discR * 2;
        bodies.push({
          id: sp.id,
          kind: 'disc',
          icon: sp.icon,
          label: sp.label,
          title: sp.title,
          desc: sp.desc,
          x: px, y: py, vx: 0, vy: 0,
          angle: 0, omega: 0, restAngle: 0,
          w: d, h: d,
          halfSeg: 0,
          r: discR,
          mass: m,
          invMass: 1 / m,
          inertia: Math.max(600, 0.5 * m * discR * discR),
          scale: 1,
          ax: ax, ay: ay,
          orbitDir: idx % 2 === 0 ? -1 : 1
        });
      });

      // Warm-up 45 physics steps so initial layout has zero overlaps at any screen size
      for (var wStep = 0; wStep < 45; wStep++) {
        stepPhysics(true);
      }
    }

    function stepPhysics(isWarmup) {
      var cx = W * 0.5;
      var cy = H * 0.5;
      var padWall = W < 700 ? 10 : 18;

      for (var i = 0; i < bodies.length; i++) {
        var b = bodies[i];
        if (b === draggedBody) {
          b.vx = 0;
          b.vy = 0;
          b.omega *= 0.7;
          b.angle += (0 - b.angle) * 0.14;
          continue;
        }

        if (b.kind === 'core') {
          b.vx += (cx - b.x) * 0.055;
          b.vy += (cy - b.y) * 0.055;
          b.vx *= 0.80;
          b.vy *= 0.80;
          b.omega += (0 - b.angle) * 0.12;
          b.omega *= 0.78;
        } else {
          // Soft magnetic attraction toward each body's home orbital zone around core
          var tx = cx + b.ax * W;
          var ty = cy + b.ay * H;
          var dxHome = tx - b.x;
          var dyHome = ty - b.y;
          b.vx += dxHome * 0.0038;
          b.vy += dyHome * 0.0038;

          // Gentle ambient breathing motion when not reduced-motion
          if (!reducedMotion && !isWarmup) {
            var dxC = b.x - cx;
            var dyC = b.y - cy;
            var distC = Math.hypot(dxC, dyC) || 1;
            b.vx += (-dyC / distC) * 0.012 * b.orbitDir;
            b.vy += ( dxC / distC) * 0.012 * b.orbitDir;
          }

          // Cursor sweep wake (only when sweeping briskly and not hovering slowly to click)
          if (!isWarmup && pointer.active && !draggedBody) {
            var pSpeed = Math.hypot(pointer.vx, pointer.vy);
            if (pSpeed > 4.2) {
              var mdx = b.x - pointer.x;
              var mdy = b.y - pointer.y;
              var mDist = Math.hypot(mdx, mdy);
              var wakeR = b.r + 42;
              if (mDist > 0.1 && mDist < wakeR) {
                var push = (1 - mDist / wakeR) * Math.min(pSpeed * 0.09, 2.4);
                b.vx += (mdx / mDist) * push + pointer.vx * 0.04;
                b.vy += (mdy / mDist) * push + pointer.vy * 0.04;
                if (b.kind === 'pill') {
                  b.omega += ((mdx * pointer.vy - mdy * pointer.vx) / (wakeR * wakeR)) * 0.05;
                }
              }
            }
          }

          b.vx *= 0.945;
          b.vy *= 0.945;

          if (b.kind === 'pill') {
            b.omega += (b.restAngle - b.angle) * 0.016;
            b.omega *= 0.88;
          } else {
            b.omega *= 0.85;
            b.angle = 0;
          }
        }

        b.x += b.vx;
        b.y += b.vy;
        b.angle = clamp(b.angle + b.omega, -0.58, 0.58);

        // Soft stage boundary containment
        var cosA = Math.cos(b.angle), sinA = Math.sin(b.angle);
        var extX = Math.abs(cosA) * b.halfSeg + b.r;
        var extY = Math.abs(sinA) * b.halfSeg + b.r;

        if (b.x - extX < padWall) {
          b.x = padWall + extX;
          b.vx = Math.abs(b.vx) * 0.55;
        } else if (b.x + extX > W - padWall) {
          b.x = W - padWall - extX;
          b.vx = -Math.abs(b.vx) * 0.55;
        }
        if (b.y - extY < padWall) {
          b.y = padWall + extY;
          b.vy = Math.abs(b.vy) * 0.55;
        } else if (b.y + extY > H - padWall) {
          b.y = H - padWall - extY;
          b.vy = -Math.abs(b.vy) * 0.55;
        }

        var targetScale = (b === draggedBody || b === hoveredBody) ? 1.05 : 1.0;
        b.scale += (targetScale - b.scale) * 0.22;
      }

      // Multi-pass capsule-to-capsule collision resolution
      var gap = W < 700 ? 5 : 8;
      for (var iter = 0; iter < 3; iter++) {
        for (var i = 0; i < bodies.length; i++) {
          var bi = bodies[i];
          var ci = Math.cos(bi.angle), si = Math.sin(bi.angle);
          var a1x = bi.x - ci * bi.halfSeg, a1y = bi.y - si * bi.halfSeg;
          var b1x = bi.x + ci * bi.halfSeg, b1y = bi.y + si * bi.halfSeg;

          for (var j = i + 1; j < bodies.length; j++) {
            var bj = bodies[j];
            var cj = Math.cos(bj.angle), sj = Math.sin(bj.angle);
            var a2x = bj.x - cj * bj.halfSeg, a2y = bj.y - sj * bj.halfSeg;
            var b2x = bj.x + cj * bj.halfSeg, b2y = bj.y + sj * bj.halfSeg;

            var cp = closestPointsOnSegments(a1x, a1y, b1x, b1y, a2x, a2y, b2x, b2y);
            var dx = cp.q2x - cp.q1x;
            var dy = cp.q2y - cp.q1y;
            var dist = Math.hypot(dx, dy);
            var minDist = bi.r + bj.r + gap;

            if (dist < minDist) {
              var nx = dist > 1e-4 ? dx / dist : 1;
              var ny = dist > 1e-4 ? dy / dist : 0;
              var overlap = minDist - dist;

              var wi = bi === draggedBody ? 0 : bi.invMass;
              var wj = bj === draggedBody ? 0 : bj.invMass;
              var wSum = wi + wj;
              if (wSum > 0) {
                var corr = (overlap / wSum) * 0.85;
                bi.x -= nx * corr * wi;
                bi.y -= ny * corr * wi;
                bj.x += nx * corr * wj;
                bj.y += ny * corr * wj;
              }

              var kx = cp.q1x + nx * bi.r;
              var ky = cp.q1y + ny * bi.r;
              var rix = kx - bi.x, riy = ky - bi.y;
              var rjx = kx - bj.x, rjy = ky - bj.y;

              var vix = bi.vx - bi.omega * riy;
              var viy = bi.vy + bi.omega * rix;
              var vjx = bj.vx - bj.omega * rjy;
              var vjy = bj.vy + bj.omega * rjx;

              var relVn = (vjx - vix) * nx + (vjy - viy) * ny;
              if (relVn < 0 && wSum > 0) {
                var rni = rix * ny - riy * nx;
                var rnj = rjx * ny - rjy * nx;
                var denom = wSum + (rni * rni) / bi.inertia + (rnj * rnj) / bj.inertia;
                var jImp = -(1 + 0.48) * relVn / denom;

                if (bi !== draggedBody) {
                  bi.vx -= jImp * nx * wi;
                  bi.vy -= jImp * ny * wi;
                  if (bi.kind === 'pill') bi.omega -= (jImp * rni) / bi.inertia;
                }
                if (bj !== draggedBody) {
                  bj.vx += jImp * nx * wj;
                  bj.vy += jImp * ny * wj;
                  if (bj.kind === 'pill') bj.omega += (jImp * rnj) / bj.inertia;
                }
              }
            }
          }
        }
      }
    }

    function hitTest(px, py) {
      for (var i = bodies.length - 1; i >= 0; i--) {
        var b = bodies[i];
        var dx = px - b.x, dy = py - b.y;
        var c = Math.cos(-b.angle), s = Math.sin(-b.angle);
        var lx = dx * c - dy * s;
        var ly = dx * s + dy * c;
        var cxClamped = clamp(lx, -b.halfSeg, b.halfSeg);
        if (Math.hypot(lx - cxClamped, ly) <= b.r + 4) {
          return b;
        }
      }
      return null;
    }

    function drawRoundedPill(w, h) {
      var r = h * 0.5;
      var hw = w * 0.5;
      var hh = h * 0.5;
      ctx.beginPath();
      ctx.moveTo(-hw + r, -hh);
      ctx.lineTo(hw - r, -hh);
      ctx.arc(hw - r, 0, r, -Math.PI * 0.5, Math.PI * 0.5);
      ctx.lineTo(-hw + r, hh);
      ctx.arc(-hw + r, 0, r, Math.PI * 0.5, Math.PI * 1.5);
      ctx.closePath();
    }

    var BRAND_PATHS = (typeof Path2D !== 'undefined') ? {
      google: [new Path2D('M12.48 10.92v3.28h7.84c-.24 1.84-.853 3.187-1.787 4.133-1.147 1.147-2.933 2.4-6.053 2.4-4.827 0-8.6-3.893-8.6-8.72s3.773-8.72 8.6-8.72c2.6 0 4.507 1.027 5.907 2.347l2.307-2.307C18.747 1.44 16.133 0 12.48 0 5.867 0 .307 5.387.307 12s5.56 12 12.173 12c3.573 0 6.267-1.173 8.373-3.36 2.16-2.16 2.84-5.213 2.84-7.667 0-.76-.053-1.467-.173-2.053H12.48z')],
      bing: [
        new Path2D('M8.35 5.046a.615.615 0 0 0-.54.575c-.009.13-.006.14.289.899.67 1.727.833 2.142.86 2.2q.101.215.277.395c.089.092.148.141.247.208.176.117.262.15.944.351.664.197 1.026.327 1.338.482.405.201.688.43.866.7.128.195.242.544.291.896.02.137.02.44 0 .564-.041.27-.124.495-.252.684-.067.1-.044.084.055-.039.278-.346.562-.938.707-1.475a4.42 4.42 0 0 0-2.14-5.028 70 70 0 0 0-.888-.465l-.53-.277-.353-.184c-.16-.082-.266-.138-.345-.18-.368-.192-.523-.27-.568-.283a1 1 0 0 0-.194-.03z'),
        new Path2D('M9.152 11.493a3 3 0 0 0-.135.083 320 320 0 0 0-1.513.934l-.8.496c-.012.01-.587.367-.876.543a1.9 1.9 0 0 1-.732.257c-.12.017-.349.017-.47 0a1.9 1.9 0 0 1-.884-.358 2.5 2.5 0 0 1-.365-.364 1.9 1.9 0 0 1-.34-.76 1 1 0 0 0-.027-.121c-.005-.006.004.092.022.22.018.132.057.324.098.489a4.1 4.1 0 0 0 2.487 2.796c.359.142.72.23 1.114.275.147.016.566.023.72.011a4.1 4.1 0 0 0 1.956-.661l.235-.149.394-.248.258-.163 1.164-.736c.51-.32.663-.433.9-.665.099-.097.248-.262.255-.283.002-.005.028-.046.059-.091a1.64 1.64 0 0 0 .25-.682c.02-.124.02-.427 0-.565a3 3 0 0 0-.213-.758c-.15-.314-.47-.6-.928-.83a2 2 0 0 0-.273-.12c-.006 0-.433.26-.948.58l-1.113.687z'),
        new Path2D('m3.004 12.184.03.129c.089.402.245.693.515.963a1.82 1.82 0 0 0 1.312.543c.361 0 .673-.09.994-.287l.472-.29.373-.23V5.334c0-1.537-.003-2.45-.008-2.521a1.82 1.82 0 0 0-.535-1.177c-.097-.096-.18-.16-.427-.33L4.183.24c-.239-.163-.258-.175-.33-.2a.63.63 0 0 0-.842.464c-.009.042-.01.603-.01 3.646l.003 8.035Z')
      ],
      meta: [new Path2D('M6.915 4.03c-1.968 0-3.683 1.28-4.871 3.113C.704 9.208 0 11.883 0 14.449c0 .706.07 1.369.21 1.973a6.624 6.624 0 0 0 .265.86 5.297 5.297 0 0 0 .371.761c.696 1.159 1.818 1.927 3.593 1.927 1.497 0 2.633-.671 3.965-2.444.76-1.012 1.144-1.626 2.663-4.32l.756-1.339.186-.325c.061.1.121.196.183.3l2.152 3.595c.724 1.21 1.665 2.556 2.47 3.314 1.046.987 1.992 1.22 3.06 1.22 1.075 0 1.876-.355 2.455-.843a3.743 3.743 0 0 0 .81-.973c.542-.939.861-2.127.861-3.745 0-2.72-.681-5.357-2.084-7.45-1.282-1.912-2.957-2.93-4.716-2.93-1.047 0-2.088.467-3.053 1.308-.652.57-1.257 1.29-1.82 2.05-.69-.875-1.335-1.547-1.958-2.056-1.182-.966-2.315-1.303-3.454-1.303zm10.16 2.053c1.147 0 2.188.758 2.992 1.999 1.132 1.748 1.647 4.195 1.647 6.4 0 1.548-.368 2.9-1.839 2.9-.58 0-1.027-.23-1.664-1.004-.496-.601-1.343-1.878-2.832-4.358l-.617-1.028a44.908 44.908 0 0 0-1.255-1.98c.07-.109.141-.224.211-.327 1.12-1.667 2.118-2.602 3.358-2.602zm-10.201.553c1.265 0 2.058.791 2.675 1.446.307.327.737.871 1.234 1.579l-1.02 1.566c-.757 1.163-1.882 3.017-2.837 4.338-1.191 1.649-1.81 1.817-2.486 1.817-.524 0-1.038-.237-1.383-.794-.263-.426-.464-1.13-.464-2.046 0-2.221.63-4.535 1.66-6.088.454-.687.964-1.226 1.533-1.533a2.264 2.264 0 0 1 1.088-.285z')],
      tiktok: [new Path2D('M12.525.02c1.31-.02 2.61-.01 3.91-.02.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.15 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z')]
    } : null;

    function drawChannelIcon(icon, size, strokeColor) {
      ctx.save();
      ctx.strokeStyle = strokeColor;
      ctx.fillStyle = strokeColor;
      ctx.lineWidth = 1.75;
      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';
      var s = size;

      if (icon === 'google' && BRAND_PATHS) {
        var gs = (s * 0.94) / 24;
        ctx.scale(gs, gs);
        ctx.translate(-12, -12);
        ctx.fill(BRAND_PATHS.google[0]);
      } else if (icon === 'bing' && BRAND_PATHS) {
        var bs = (s * 1.04) / 16;
        ctx.scale(bs, bs);
        ctx.translate(-8.2, -8.1);
        for (var bi = 0; bi < BRAND_PATHS.bing.length; bi++) {
          ctx.fill(BRAND_PATHS.bing[bi]);
        }
      } else if (icon === 'meta' && BRAND_PATHS) {
        var ms = (s * 1.10) / 24;
        ctx.scale(ms, ms);
        ctx.translate(-12, -12);
        ctx.fill(BRAND_PATHS.meta[0]);
      } else if (icon === 'tiktok' && BRAND_PATHS) {
        var ts = (s * 0.95) / 24;
        ctx.scale(ts, ts);
        ctx.translate(-12, -12);
        ctx.fill(BRAND_PATHS.tiktok[0]);
      } else if (icon === 'linkedin') {
        ctx.font = '700 ' + Math.round(s * 1.02) + 'px ' + fontFamily;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('in', 0, 1);
      } else if (icon === 'yandex') {
        ctx.font = '700 ' + Math.round(s * 1.02) + 'px ' + fontFamily;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('Я', 0, 1);
      } else if (icon === 'ga4') {
        var bw = s * 0.18;
        ctx.beginPath();
        ctx.moveTo(-s * 0.36, s * 0.40); ctx.lineTo(-s * 0.36, s * 0.12);
        ctx.moveTo(0, s * 0.40);         ctx.lineTo(0, -s * 0.12);
        ctx.moveTo(s * 0.36, s * 0.40);  ctx.lineTo(s * 0.36, -s * 0.40);
        ctx.lineWidth = Math.max(2.2, bw);
        ctx.stroke();
      } else if (icon === 'aeo') {
        var rOuter = s * 0.50, rInner = s * 0.16;
        ctx.beginPath();
        for (var k = 0; k < 8; k++) {
          var ang = (k * Math.PI) / 4 - Math.PI / 2;
          var rad = k % 2 === 0 ? rOuter : rInner;
          var vx = Math.cos(ang) * rad, vy = Math.sin(ang) * rad;
          if (k === 0) ctx.moveTo(vx, vy); else ctx.lineTo(vx, vy);
        }
        ctx.closePath();
        ctx.stroke();
      }
      ctx.restore();
    }

    function render() {
      ctx.clearRect(0, 0, W, H);
      var isDarkPage = document.body.classList.contains('dark');
      var core = bodies[0];
      if (!core) return;

      var cx = W * 0.5, cy = H * 0.5;
      orbitPhase += reducedMotion ? 0 : 0.0025;

      // 1. Subtle orbital field rings
      ctx.save();
      ctx.translate(cx, cy);
      ctx.strokeStyle = isDarkPage ? 'rgba(255,255,255,0.10)' : 'rgba(15,23,42,0.08)';
      ctx.lineWidth = 1;
      ctx.setLineDash([5, 7]);
      ctx.save();
      ctx.rotate(orbitPhase);
      ctx.beginPath();
      ctx.ellipse(0, 0, W * 0.22, H * 0.26, 0, 0, Math.PI * 2);
      ctx.stroke();
      ctx.restore();

      ctx.setLineDash([]);
      ctx.strokeStyle = isDarkPage ? 'rgba(255,255,255,0.06)' : 'rgba(15,23,42,0.05)';
      ctx.beginPath();
      ctx.ellipse(0, 0, W * 0.38, H * 0.40, 0, 0, Math.PI * 2);
      ctx.stroke();
      ctx.restore();

      // Optional pulse wave when clicking core or nodes
      if (pulseRing.active) {
        pulseRing.r += 4.5;
        pulseRing.alpha *= 0.93;
        if (pulseRing.alpha < 0.02) {
          pulseRing.active = false;
        } else {
          ctx.save();
          ctx.strokeStyle = 'rgba(124,58,237,' + pulseRing.alpha.toFixed(3) + ')';
          ctx.lineWidth = 1.5;
          ctx.beginPath();
          ctx.arc(core.x, core.y, pulseRing.r, 0, Math.PI * 2);
          ctx.stroke();
          ctx.restore();
        }
      }

      // 2. Subtle magnetic tether lines from core to nodes
      var activeNode = hoveredBody || pinnedBody;
      ctx.save();
      for (var i = 1; i < bodies.length; i++) {
        var nb = bodies[i];
        var isFocus = (nb === activeNode || nb === draggedBody);
        ctx.beginPath();
        ctx.moveTo(core.x, core.y);
        ctx.lineTo(nb.x, nb.y);
        if (isFocus) {
          ctx.strokeStyle = 'rgba(124,58,237,0.38)';
          ctx.lineWidth = 1.5;
        } else {
          ctx.strokeStyle = isDarkPage ? 'rgba(255,255,255,0.05)' : 'rgba(15,23,42,0.045)';
          ctx.lineWidth = 1;
        }
        ctx.stroke();
      }
      ctx.restore();

      // 3. Render Discs & Capsules (Core rendered last so it stays crisp at center)
      var renderOrder = bodies.slice(1).concat([core]);
      for (var rIdx = 0; rIdx < renderOrder.length; rIdx++) {
        var b = renderOrder[rIdx];
        var isSel = (b === hoveredBody || b === pinnedBody || b === draggedBody);

        ctx.save();
        ctx.translate(b.x, b.y);
        ctx.rotate(b.angle);
        ctx.scale(b.scale, b.scale);

        if (b.kind === 'core') {
          // Outer soft magnetic aura
          ctx.save();
          drawRoundedPill(b.w + 14, b.h + 14);
          ctx.strokeStyle = isSel ? 'rgba(124,58,237,0.34)' : (isDarkPage ? 'rgba(255,255,255,0.12)' : 'rgba(15,23,42,0.09)');
          ctx.lineWidth = 1.25;
          ctx.stroke();
          ctx.restore();

          ctx.shadowColor = 'rgba(15,23,42,0.20)';
          ctx.shadowBlur = 24;
          ctx.shadowOffsetY = 8;
          drawRoundedPill(b.w, b.h);
          ctx.fillStyle = '#0f172a';
          ctx.fill();
          ctx.shadowColor = 'transparent';

          ctx.lineWidth = isSel ? 1.75 : 1;
          ctx.strokeStyle = isSel ? '#7c3aed' : 'rgba(255,255,255,0.18)';
          ctx.stroke();

          // Live accent dot + ROASIST wordmark
          var coreFont = W < 700 ? 13.5 : 16;
          ctx.font = '700 ' + coreFont + 'px ' + fontFamily;
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';
          ctx.fillStyle = '#7c3aed';
          ctx.beginPath();
          ctx.arc(-b.w * 0.30, 0, 4, 0, Math.PI * 2);
          ctx.fill();

          ctx.fillStyle = '#ffffff';
          ctx.fillText(b.label, 7, 0.5);
        } else if (b.kind === 'pill') {
          var darkPill = (b.theme === 'dark');
          ctx.shadowColor = darkPill ? 'rgba(15,23,42,0.15)' : 'rgba(15,23,42,0.08)';
          ctx.shadowBlur = isSel ? 22 : 16;
          ctx.shadowOffsetY = 6;

          drawRoundedPill(b.w, b.h);
          ctx.fillStyle = darkPill ? '#0f172a' : 'rgba(255,255,255,0.95)';
          ctx.fill();
          ctx.shadowColor = 'transparent';

          ctx.lineWidth = isSel ? 1.75 : 1;
          ctx.strokeStyle = isSel
            ? '#7c3aed'
            : (darkPill ? 'rgba(255,255,255,0.14)' : 'rgba(15,23,42,0.13)');
          ctx.stroke();

          ctx.font = '500 ' + b.fontSize + 'px ' + fontFamily;
          ctx.fillStyle = darkPill ? '#ffffff' : '#0f172a';
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';
          ctx.fillText(b.label, 0, 0.5);
        } else if (b.kind === 'disc') {
          ctx.shadowColor = 'rgba(15,23,42,0.09)';
          ctx.shadowBlur = isSel ? 20 : 14;
          ctx.shadowOffsetY = 5;

          ctx.beginPath();
          ctx.arc(0, 0, b.r, 0, Math.PI * 2);
          ctx.fillStyle = 'rgba(255,255,255,0.96)';
          ctx.fill();
          ctx.shadowColor = 'transparent';

          ctx.lineWidth = isSel ? 1.75 : 1;
          ctx.strokeStyle = isSel ? '#7c3aed' : 'rgba(15,23,42,0.14)';
          ctx.stroke();

          var iconSz = W < 700 ? 12.5 : 16;
          var lblSz = W < 700 ? 8.5 : 10;
          ctx.save();
          ctx.translate(0, -b.r * 0.20);
          drawChannelIcon(b.icon, iconSz, isSel ? '#7c3aed' : '#0f172a');
          ctx.restore();

          ctx.font = '600 ' + lblSz + 'px ' + fontFamily;
          ctx.fillStyle = '#334155';
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';
          ctx.fillText(b.label, 0, b.r * 0.44);
        }

        ctx.restore();
      }
    }

    function tick() {
      if (isVisible) {
        stepPhysics(false);
        render();
      }
      rafId = window.requestAnimationFrame(tick);
    }

    function getLocalCoords(ev) {
      var r = canvas.getBoundingClientRect();
      return { x: ev.clientX - r.left, y: ev.clientY - r.top };
    }

    function triggerPulse(originBody) {
      pulseRing.active = true;
      pulseRing.r = (originBody ? originBody.r : 30);
      pulseRing.alpha = 0.42;
      if (originBody && originBody.kind === 'core') {
        for (var i = 1; i < bodies.length; i++) {
          var nb = bodies[i];
          var dx = nb.x - originBody.x, dy = nb.y - originBody.y;
          var d = Math.hypot(dx, dy) || 1;
          nb.vx += (dx / d) * 2.6;
          nb.vy += (dy / d) * 2.6;
        }
      }
    }

    canvas.addEventListener('pointerdown', function(ev) {
      var pt = getLocalCoords(ev);
      pointer.x = pt.x; pointer.y = pt.y;
      pointer.vx = 0; pointer.vy = 0;
      pointer.active = true;
      pointerDownPos = pt;
      pointerMoved = false;

      var hit = hitTest(pt.x, pt.y);
      if (hit) {
        draggedBody = hit;
        dragOffsetX = hit.x - pt.x;
        dragOffsetY = hit.y - pt.y;
        hoveredBody = hit;
        canvas.style.cursor = 'grabbing';
        updateDetailBar(hit);
        if (ev.pointerType === 'mouse' && canvas.setPointerCapture) {
          try { canvas.setPointerCapture(ev.pointerId); } catch (e) {}
        }
      }
    });

    canvas.addEventListener('pointermove', function(ev) {
      var pt = getLocalCoords(ev);
      pointer.vx = pt.x - pointer.x;
      pointer.vy = pt.y - pointer.y;
      pointer.x = pt.x;
      pointer.y = pt.y;
      pointer.active = true;

      if (pointerDownPos && Math.hypot(pt.x - pointerDownPos.x, pt.y - pointerDownPos.y) > 7) {
        pointerMoved = true;
      }

      if (draggedBody) {
        if (draggedBody.kind !== 'core') {
          var nx = pt.x + dragOffsetX;
          var ny = pt.y + dragOffsetY;
          draggedBody.vx = (nx - draggedBody.x) * 0.45;
          draggedBody.vy = (ny - draggedBody.y) * 0.45;
          draggedBody.x = nx;
          draggedBody.y = ny;
        }
        return;
      }

      var hit = hitTest(pt.x, pt.y);
      if (hit !== hoveredBody) {
        hoveredBody = hit;
        canvas.style.cursor = hit ? 'grab' : 'default';
        updateDetailBar(hit);
      }
    });

    function releasePointer(ev) {
      if (draggedBody) {
        if (!pointerMoved) {
          pinnedBody = (pinnedBody === draggedBody) ? null : draggedBody;
          triggerPulse(draggedBody);
          updateDetailBar(hoveredBody || pinnedBody);
        } else if (draggedBody.kind !== 'core') {
          draggedBody.vx = clamp(pointer.vx * 0.55, -9, 9);
          draggedBody.vy = clamp(pointer.vy * 0.55, -9, 9);
        }
        draggedBody = null;
      } else if (ev && ev.type === 'pointerup' && !pointerMoved) {
        pinnedBody = null;
        updateDetailBar(hoveredBody);
      }
      pointerDownPos = null;
      canvas.style.cursor = hoveredBody ? 'grab' : 'default';
    }

    canvas.addEventListener('pointerup', releasePointer);
    canvas.addEventListener('pointercancel', function() {
      draggedBody = null;
      pointerDownPos = null;
      pointer.active = false;
    });
    canvas.addEventListener('pointerleave', function() {
      pointer.active = false;
      if (!draggedBody) {
        hoveredBody = null;
        canvas.style.cursor = 'default';
        updateDetailBar(null);
      }
    });

    var resizeTimer = null;
    window.addEventListener('resize', function() {
      if (resizeTimer) clearTimeout(resizeTimer);
      resizeTimer = setTimeout(function() {
        var newRect = stage.getBoundingClientRect();
        if (Math.abs(newRect.width - W) > 8) {
          buildScene();
          render();
        }
      }, 150);
    });

    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function(entries) {
        entries.forEach(function(en) { isVisible = en.isIntersecting; });
      }, { rootMargin: '180px' }).observe(stage);
    }

    buildScene();
    updateDetailBar(null);
    render();
    rafId = window.requestAnimationFrame(tick);

    if (document.fonts && document.fonts.ready) {
      document.fonts.ready.then(function() {
        buildScene();
        render();
      });
    }
  }

  function mountAll() {
    document.querySelectorAll('[data-roasist-ecosystem="1"]').forEach(initEcosystem);
  }

  function scheduleMount() {
    setTimeout(mountAll, 350);
    setTimeout(mountAll, 900);
    setTimeout(mountAll, 1600);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', scheduleMount);
  } else {
    scheduleMount();
  }
})();
</script>"""


def build_ssr_ecosystem_block() -> str:
    return (
        '<div class="roasist-ecosystem" data-roasist-ecosystem="1">'
        '<div class="roasist-ecosystem__stage"></div>'
        '<div class="roasist-ecosystem__detail" aria-live="polite">'
        '<span class="roasist-ecosystem__dot" aria-hidden="true"></span>'
        '<strong class="roasist-ecosystem__label"></strong>'
        f'<span class="roasist-ecosystem__desc">{DEFAULT_HINT_TR}</span>'
        "</div></div>"
    )


def build_flight_ecosystem_node() -> list:
    return [
        "$",
        "div",
        None,
        {
            "className": "roasist-ecosystem",
            "data-roasist-ecosystem": "1",
            "children": [
                ["$", "div", None, {"className": "roasist-ecosystem__stage"}],
                [
                    "$",
                    "div",
                    None,
                    {
                        "className": "roasist-ecosystem__detail",
                        "aria-live": "polite",
                        "children": [
                            ["$", "span", None, {"className": "roasist-ecosystem__dot", "aria-hidden": "true"}],
                            ["$", "strong", None, {"className": "roasist-ecosystem__label"}],
                            [
                                "$",
                                "span",
                                None,
                                {
                                    "className": "roasist-ecosystem__desc",
                                    "children": DEFAULT_HINT_TR,
                                },
                            ],
                        ],
                    },
                ],
            ],
        },
    ]


def update_single_about_ecosystem_tr(fp: str) -> bool:
    with open(fp, "r", encoding="utf-8") as f:
        html = f.read()

    pushes = list(PUSH_RE.finditer(html))
    if not pushes:
        raise RuntimeError(f"No Flight stream found in {fp}")

    ssr = html[: pushes[0].start()]
    tail = html[pushes[0].start() :]

    eco_ssr = build_ssr_ecosystem_block()
    ssr_updated, n_sec = re.subn(
        r'(<section class="Culture_culture__lmpEt">)'
        r'(?:<!--\$!--><template data-dgst="BAILOUT_TO_CLIENT_SIDE_RENDERING"></template><!--/\$-->|<div class="roasist-ecosystem" data-roasist-ecosystem="1">.*?</div></div>)'
        r'(<div class="container">)',
        lambda m: m.group(1) + eco_ssr + m.group(2),
        ssr,
        count=1,
        flags=re.S,
    )
    if n_sec != 1:
        raise RuntimeError(f"Failed to update Culture_culture__lmpEt in SSR of {fp}")

    flight_ok = False

    def mut(records):
        nonlocal flight_ok
        changed = False
        for rec in records:
            if rec[0] != "line":
                continue
            payload = rec[2]
            if not payload or payload[0] not in "[{" or "Culture_culture__lmpEt" not in payload:
                continue
            ast = json.loads(payload)
            culture_sec = find_node_by_class(ast, "Culture_culture__lmpEt")
            if not culture_sec:
                continue
            c_children = culture_sec[3]["children"]
            if not isinstance(c_children, list) or len(c_children) < 2:
                raise RuntimeError(f"Unexpected Culture_culture__lmpEt children in {fp}")
            c_children[0] = build_flight_ecosystem_node()
            rec[2] = json.dumps(ast, ensure_ascii=False, separators=(",", ":"))
            flight_ok = True
            changed = True
        return changed

    new_html = ssr_updated + rewrite_flight_in_html(tail, mut)
    if not flight_ok:
        raise RuntimeError(f"Failed to update Culture_culture__lmpEt in Flight AST of {fp}")

    if new_html != html:
        with open(fp, "w", encoding="utf-8") as f:
            f.write(new_html)
        return True
    return False


def update_about_ecosystem_tr() -> int:
    count = 0
    for base_name in ("public", "dist"):
        fp = os.path.join(ROOT, base_name, "hakkimizda", "index.html")
        if update_single_about_ecosystem_tr(fp):
            count += 1
    print(f"[ABOUT ECOSYSTEM] Updated {count} TR Hakkımızda files with Concept A orbital ecosystem")
    return count


if __name__ == "__main__":
    update_about_ecosystem_tr()
