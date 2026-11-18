#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Inject 6 bespoke, lightweight SVG + CSS brand-motion animations for all 6 Performance Marketing channels
on /hizmetler/performans-pazarlamasi/ and /en/performance-marketing/ (in both public/ and dist/):

  1. Google Ads    — Rising metric columns ($, Store, Audience) -> Official Google Ads A-frame logo & wordmark
  2. Meta Ads      — Rising social columns (Instagram, Facebook, Shop) -> Official Meta Infinity ribbon & wordmark
  3. TikTok Ads    — 5-bar rhythmic audio equalizer + 9:16 frame -> Chromatic split-snap TikTok note & wordmark
  4. Yandex Ads    — Concentric Eurasia/CIS radar + orbiting market beacons -> Official Yandex Red Я mark & wordmark
  5. Bing Ads      — Multi-engine desktop search ribbons (Bing/Yahoo/DDG) -> Official folded Bing ribbon & wordmark
  6. LinkedIn Ads  — B2B executive decision-maker hierarchy graph -> Official LinkedIn 'in' badge & wordmark

Preserves 100% React Flight hydration parity and eliminates external KOTA MP4/PNG/JPG downloads for all 6 channel rows.
"""

import json
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
  background-color: #FFFFFF !important;
  overflow: hidden !important;
  opacity: 1 !important;
  border: 1px solid rgba(15, 23, 42, 0.08) !important;
  box-shadow: 0 24px 60px -18px rgba(15, 23, 42, 0.12) !important;
  isolation: isolate !important;
}

/* Preserve KOTA asymmetric architectural corner radii on all 6 stages */
html body .TextImageRows_row__PPlpB:nth-child(odd) .TextImageRows_media__twu3R .ImageEnter_image__FSEP_,
html body .TextImageRows_row__PPlpB:nth-child(odd) .TextImageRows_media__twu3R .roasist-brand-stage {
  border-radius: 28px 7.5rem 28px 28px !important;
}
@media (min-width: 850px) {
  html body .TextImageRows_row__PPlpB:nth-child(odd) .TextImageRows_media__twu3R .ImageEnter_image__FSEP_,
  html body .TextImageRows_row__PPlpB:nth-child(odd) .TextImageRows_media__twu3R .roasist-brand-stage {
    border-radius: 32px 12.5rem 32px 32px !important;
  }
}

html body .TextImageRows_row__PPlpB:nth-child(2n) .TextImageRows_media__twu3R .ImageEnter_image__FSEP_,
html body .TextImageRows_row__PPlpB:nth-child(2n) .TextImageRows_media__twu3R .roasist-brand-stage {
  border-radius: 28px 7.5rem 28px 28px !important;
}
@media (min-width: 769px) and (max-width: 849px) {
  html body .TextImageRows_row__PPlpB:nth-child(2n) .TextImageRows_media__twu3R .ImageEnter_image__FSEP_,
  html body .TextImageRows_row__PPlpB:nth-child(2n) .TextImageRows_media__twu3R .roasist-brand-stage {
    border-radius: 7.5rem 28px 28px 28px !important;
  }
}
@media (min-width: 850px) {
  html body .TextImageRows_row__PPlpB:nth-child(2n) .TextImageRows_media__twu3R .ImageEnter_image__FSEP_,
  html body .TextImageRows_row__PPlpB:nth-child(2n) .TextImageRows_media__twu3R .roasist-brand-stage {
    border-radius: 12.5rem 32px 32px 32px !important;
  }
}

html body .TextImageRows_row__PPlpB .TextImageRows_media__twu3R video,
html body .TextImageRows_row__PPlpB .TextImageRows_media__twu3R img {
  opacity: 0 !important;
  pointer-events: none !important;
}

html body .roasist-brand-stage {
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

html body .roasist-brand-svg {
  width: 96% !important;
  height: auto !important;
  display: block !important;
}

/* ============================================================================
   1. GOOGLE ADS ANIMATION (7s loop)
   ============================================================================ */
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
  transform-origin: 300px 125px;
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
  0%, 33%   { transform: rotate(60deg); }
  46%, 100% { transform: rotate(0deg); }
}
@keyframes gadsTextReveal {
  0%, 58%   { opacity: 0; transform: translateX(-18px); }
  68%, 92%  { opacity: 1; transform: translateX(0); }
  98%, 100% { opacity: 0; transform: translateX(0); }
}

/* ============================================================================
   2. META ADS (INSTAGRAM & FACEBOOK) ANIMATION (7s loop)
   ============================================================================ */
.meta-anim-stage .meta-grid-lines {
  opacity: 0;
  transform-origin: 300px 150px;
  animation: metaGridFade 7s ease-in-out infinite;
}
.meta-anim-stage .meta-col-ig {
  transform-origin: 200px 220px;
  animation: metaBarLeft 7s cubic-bezier(0.22, 1, 0.36, 1) infinite;
}
.meta-anim-stage .meta-col-fb {
  transform-origin: 300px 220px;
  animation: metaBarMid 7s cubic-bezier(0.22, 1, 0.36, 1) infinite;
}
.meta-anim-stage .meta-col-conv {
  transform-origin: 400px 220px;
  animation: metaBarRight 7s cubic-bezier(0.22, 1, 0.36, 1) infinite;
}
.meta-anim-stage .meta-logo-assembly {
  transform-origin: 300px 160px;
  animation: metaLogoSeq 7s cubic-bezier(0.25, 1, 0.5, 1) infinite;
}
.meta-anim-stage .meta-infinity-ribbon {
  stroke-dasharray: 560;
  stroke-dashoffset: 560;
  animation: metaRibbonDraw 7s cubic-bezier(0.22, 1, 0.36, 1) infinite;
}
.meta-anim-stage .meta-ribbon-crossover {
  animation: metaCrossFade 7s ease-out infinite;
}
.meta-anim-stage .meta-brand-text {
  animation: metaTextReveal 7s cubic-bezier(0.22, 1, 0.36, 1) infinite;
}

@keyframes metaGridFade {
  0%, 6%   { opacity: 0; transform: scaleX(0.6); }
  14%, 30% { opacity: 1; transform: scaleX(1); }
  38%, 100%{ opacity: 0; transform: scaleX(0.8); }
}
@keyframes metaBarLeft {
  0%        { opacity: 0; transform: translateY(80px) scaleY(0.3); }
  10%, 28%  { opacity: 1; transform: translateY(0) scaleY(1); }
  36%, 100% { opacity: 0; transform: translateX(75px) translateY(45px) scale(0.4); }
}
@keyframes metaBarMid {
  0%, 3%    { opacity: 0; transform: translateY(80px) scaleY(0.3); }
  13%, 28%  { opacity: 1; transform: translateY(0) scaleY(1); }
  36%, 100% { opacity: 0; transform: translateY(35px) scale(0.4); }
}
@keyframes metaBarRight {
  0%, 6%    { opacity: 0; transform: translateY(80px) scaleY(0.3); }
  16%, 27%  { opacity: 1; transform: translateY(0) scaleY(1); }
  35%, 100% { opacity: 0; transform: translateX(-75px) translateY(45px) scale(0.4); }
}
@keyframes metaLogoSeq {
  0%, 32%   { opacity: 0; transform: translateX(0) scale(1.08); }
  37%       { opacity: 1; transform: translateX(0) scale(1.08); }
  52%       { opacity: 1; transform: translateX(0) scale(0.76); }
  62%, 92%  { opacity: 1; transform: translateX(-118px) scale(0.76); }
  98%, 100% { opacity: 0; transform: translateX(-118px) scale(0.76); }
}
@keyframes metaRibbonDraw {
  0%, 32%   { stroke-dashoffset: 560; }
  49%, 100% { stroke-dashoffset: 0; }
}
@keyframes metaCrossFade {
  0%, 44%   { opacity: 0; }
  52%, 100% { opacity: 1; }
}
@keyframes metaTextReveal {
  0%, 58%   { opacity: 0; transform: translateX(-18px); }
  68%, 92%  { opacity: 1; transform: translateX(0); }
  98%, 100% { opacity: 0; transform: translateX(0); }
}

/* ============================================================================
   3. TIKTOK ADS — AUDIO EQUALIZER + VERTICAL FRAME -> CHROMATIC NOTE SNAP (7s)
   ============================================================================ */
.tiktok-anim-stage .tt-frame {
  transform-origin: 300px 160px;
  animation: ttFramePhase 7s cubic-bezier(0.22, 1, 0.36, 1) infinite;
}
.tiktok-anim-stage .tt-eq-1 { transform-origin: 224px 160px; animation: ttEqPulseA 7s ease-in-out infinite; }
.tiktok-anim-stage .tt-eq-2 { transform-origin: 262px 160px; animation: ttEqPulseB 7s ease-in-out infinite; }
.tiktok-anim-stage .tt-eq-3 { transform-origin: 300px 160px; animation: ttEqPulseC 7s ease-in-out infinite; }
.tiktok-anim-stage .tt-eq-4 { transform-origin: 338px 160px; animation: ttEqPulseB 7s ease-in-out infinite; }
.tiktok-anim-stage .tt-eq-5 { transform-origin: 376px 160px; animation: ttEqPulseA 7s ease-in-out infinite; }

.tiktok-anim-stage .tt-logo-assembly {
  transform-origin: 300px 160px;
  animation: ttLogoSeq 7s cubic-bezier(0.25, 1, 0.5, 1) infinite;
}
.tiktok-anim-stage .tt-note-cyan {
  animation: ttCyanSnap 7s cubic-bezier(0.22, 1, 0.36, 1) infinite;
}
.tiktok-anim-stage .tt-note-red {
  animation: ttRedSnap 7s cubic-bezier(0.22, 1, 0.36, 1) infinite;
}
.tiktok-anim-stage .tt-brand-text {
  animation: ttTextReveal 7s cubic-bezier(0.22, 1, 0.36, 1) infinite;
}

@keyframes ttFramePhase {
  0%, 4%    { opacity: 0; transform: scale(0.75); }
  12%, 28%  { opacity: 1; transform: scale(1); }
  36%, 100% { opacity: 0; transform: scale(0.55); }
}
@keyframes ttEqPulseA {
  0%, 4%    { opacity: 0; transform: scaleY(0.2); }
  12%       { opacity: 1; transform: scaleY(0.85); }
  18%       { opacity: 1; transform: scaleY(1.2); }
  25%       { opacity: 1; transform: scaleY(0.7); }
  34%, 100% { opacity: 0; transform: scaleY(0.15) translateX(0); }
}
@keyframes ttEqPulseB {
  0%, 6%    { opacity: 0; transform: scaleY(0.2); }
  14%       { opacity: 1; transform: scaleY(1.25); }
  20%       { opacity: 1; transform: scaleY(0.72); }
  27%       { opacity: 1; transform: scaleY(1.1); }
  35%, 100% { opacity: 0; transform: scaleY(0.15); }
}
@keyframes ttEqPulseC {
  0%, 8%    { opacity: 0; transform: scaleY(0.2); }
  15%       { opacity: 1; transform: scaleY(1.0); }
  22%       { opacity: 1; transform: scaleY(1.32); }
  28%       { opacity: 1; transform: scaleY(0.85); }
  36%, 100% { opacity: 0; transform: scaleY(0.15); }
}
@keyframes ttLogoSeq {
  0%, 32%   { opacity: 0; transform: translateX(0) scale(1.12); }
  38%       { opacity: 1; transform: translateX(0) scale(1.12); }
  52%       { opacity: 1; transform: translateX(0) scale(0.84); }
  62%, 92%  { opacity: 1; transform: translateX(-118px) scale(0.84); }
  98%, 100% { opacity: 0; transform: translateX(-118px) scale(0.84); }
}
@keyframes ttCyanSnap {
  0%, 32%   { transform: translate(-22px, -16px); }
  45%, 100% { transform: translate(-4.5px, -4px); }
}
@keyframes ttRedSnap {
  0%, 32%   { transform: translate(22px, 16px); }
  45%, 100% { transform: translate(4.5px, 4px); }
}
@keyframes ttTextReveal {
  0%, 58%   { opacity: 0; transform: translateX(-18px); }
  68%, 92%  { opacity: 1; transform: translateX(0); }
  98%, 100% { opacity: 0; transform: translateX(0); }
}

/* ============================================================================
   4. YANDEX ADS — EURASIA RADAR & ORBITING MARKET BEACONS -> YANDEX MARK (7s)
   ============================================================================ */
.yandex-anim-stage .yd-radar-ring-1 {
  transform-origin: 300px 160px;
  animation: ydRingExpand 7s cubic-bezier(0.22, 1, 0.36, 1) infinite;
}
.yandex-anim-stage .yd-radar-ring-2 {
  transform-origin: 300px 160px;
  animation: ydRingExpand2 7s cubic-bezier(0.22, 1, 0.36, 1) infinite;
}
.yandex-anim-stage .yd-beacons {
  transform-origin: 300px 160px;
  animation: ydBeaconsOrbit 7s cubic-bezier(0.22, 1, 0.36, 1) infinite;
}
.yandex-anim-stage .yd-logo-assembly {
  transform-origin: 300px 160px;
  animation: ydLogoSeq 7s cubic-bezier(0.25, 1, 0.5, 1) infinite;
}
.yandex-anim-stage .yd-glyph {
  transform-origin: 300px 160px;
  animation: ydGlyphPop 7s cubic-bezier(0.34, 1.56, 0.64, 1) infinite;
}
.yandex-anim-stage .yd-brand-text {
  animation: ydTextReveal 7s cubic-bezier(0.22, 1, 0.36, 1) infinite;
}

@keyframes ydRingExpand {
  0%, 3%    { opacity: 0; transform: scale(0.35); }
  14%, 28%  { opacity: 1; transform: scale(1); }
  36%, 100% { opacity: 0; transform: scale(0.45); }
}
@keyframes ydRingExpand2 {
  0%, 7%    { opacity: 0; transform: scale(0.45); }
  18%, 28%  { opacity: 0.75; transform: scale(1); }
  36%, 100% { opacity: 0; transform: scale(0.45); }
}
@keyframes ydBeaconsOrbit {
  0%, 4%    { opacity: 0; transform: rotate(-28deg) scale(0.6); }
  16%, 27%  { opacity: 1; transform: rotate(8deg) scale(1); }
  36%, 100% { opacity: 0; transform: rotate(35deg) scale(0.3); }
}
@keyframes ydLogoSeq {
  0%, 32%   { opacity: 0; transform: translateX(0) scale(1.1); }
  38%       { opacity: 1; transform: translateX(0) scale(1.1); }
  52%       { opacity: 1; transform: translateX(0) scale(0.82); }
  62%, 92%  { opacity: 1; transform: translateX(-124px) scale(0.82); }
  98%, 100% { opacity: 0; transform: translateX(-124px) scale(0.82); }
}
@keyframes ydGlyphPop {
  0%, 34%   { opacity: 0; transform: scale(0.5); }
  45%, 100% { opacity: 1; transform: scale(1); }
}
@keyframes ydTextReveal {
  0%, 58%   { opacity: 0; transform: translateX(-18px); }
  68%, 92%  { opacity: 1; transform: translateX(0); }
  98%, 100% { opacity: 0; transform: translateX(0); }
}

/* ============================================================================
   5. BING ADS — MULTI-ENGINE SEARCH RIBBONS -> OFFICIAL BING RIBBON MARK (7s)
   ============================================================================ */
.bing-anim-stage .bing-row-1 { animation: bingRowL 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }
.bing-anim-stage .bing-row-2 { animation: bingRowR 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }
.bing-anim-stage .bing-row-3 { animation: bingRowL2 7s cubic-bezier(0.22, 1, 0.36, 1) infinite; }
.bing-anim-stage .bing-logo-assembly {
  transform-origin: 300px 160px;
  animation: bingLogoSeq 7s cubic-bezier(0.25, 1, 0.5, 1) infinite;
}
.bing-anim-stage .bing-wing {
  transform-origin: 284px 160px;
  animation: bingWingFold 7s cubic-bezier(0.34, 1.45, 0.64, 1) infinite;
}
.bing-anim-stage .bing-brand-text {
  animation: bingTextReveal 7s cubic-bezier(0.22, 1, 0.36, 1) infinite;
}

@keyframes bingRowL {
  0%, 2%    { opacity: 0; transform: translateX(-70px); }
  12%, 28%  { opacity: 1; transform: translateX(0); }
  36%, 100% { opacity: 0; transform: translateX(40px) scale(0.5); }
}
@keyframes bingRowR {
  0%, 5%    { opacity: 0; transform: translateX(70px); }
  15%, 28%  { opacity: 1; transform: translateX(0); }
  36%, 100% { opacity: 0; transform: translateX(-40px) scale(0.5); }
}
@keyframes bingRowL2 {
  0%, 8%    { opacity: 0; transform: translateX(-70px); }
  18%, 28%  { opacity: 1; transform: translateX(0); }
  36%, 100% { opacity: 0; transform: translateX(40px) scale(0.5); }
}
@keyframes bingLogoSeq {
  0%, 32%   { opacity: 0; transform: translateX(0) scale(1.1); }
  38%       { opacity: 1; transform: translateX(0) scale(1.1); }
  52%       { opacity: 1; transform: translateX(0) scale(0.84); }
  62%, 92%  { opacity: 1; transform: translateX(-108px) scale(0.84); }
  98%, 100% { opacity: 0; transform: translateX(-108px) scale(0.84); }
}
@keyframes bingWingFold {
  0%, 34%   { opacity: 0; transform: scaleX(0.25) translateX(-16px); }
  47%, 100% { opacity: 1; transform: scaleX(1) translateX(0); }
}
@keyframes bingTextReveal {
  0%, 58%   { opacity: 0; transform: translateX(-18px); }
  68%, 92%  { opacity: 1; transform: translateX(0); }
  98%, 100% { opacity: 0; transform: translateX(0); }
}

/* ============================================================================
   6. LINKEDIN ADS — B2B DECISION-MAKER HIERARCHY GRAPH -> 'in' BADGE (7s)
   ============================================================================ */
.linkedin-anim-stage .li-graph-links {
  stroke-dasharray: 120;
  stroke-dashoffset: 120;
  animation: liLinksDraw 7s ease-out infinite;
}
.linkedin-anim-stage .li-tier-bot {
  transform-origin: 300px 212px;
  animation: liTierBot 7s cubic-bezier(0.22, 1, 0.36, 1) infinite;
}
.linkedin-anim-stage .li-tier-mid {
  transform-origin: 300px 158px;
  animation: liTierMid 7s cubic-bezier(0.22, 1, 0.36, 1) infinite;
}
.linkedin-anim-stage .li-tier-top {
  transform-origin: 300px 102px;
  animation: liTierTop 7s cubic-bezier(0.34, 1.56, 0.64, 1) infinite;
}
.linkedin-anim-stage .li-logo-assembly {
  transform-origin: 300px 160px;
  animation: liLogoSeq 7s cubic-bezier(0.25, 1, 0.5, 1) infinite;
}
.linkedin-anim-stage .li-in-letters {
  transform-origin: 300px 160px;
  animation: liLettersPop 7s cubic-bezier(0.34, 1.56, 0.64, 1) infinite;
}
.linkedin-anim-stage .li-brand-text {
  animation: liTextReveal 7s cubic-bezier(0.22, 1, 0.36, 1) infinite;
}

@keyframes liLinksDraw {
  0%, 6%    { opacity: 0; stroke-dashoffset: 120; }
  16%, 28%  { opacity: 1; stroke-dashoffset: 0; }
  35%, 100% { opacity: 0; stroke-dashoffset: 0; }
}
@keyframes liTierBot {
  0%, 2%    { opacity: 0; transform: translateY(18px) scale(0.6); }
  11%, 28%  { opacity: 1; transform: translateY(0) scale(1); }
  36%, 100% { opacity: 0; transform: translateY(-48px) scale(0.35); }
}
@keyframes liTierMid {
  0%, 7%    { opacity: 0; transform: translateY(14px) scale(0.6); }
  16%, 28%  { opacity: 1; transform: translateY(0) scale(1); }
  36%, 100% { opacity: 0; transform: scale(0.35); }
}
@keyframes liTierTop {
  0%, 12%   { opacity: 0; transform: scale(0.4); }
  21%, 28%  { opacity: 1; transform: scale(1); }
  36%, 100% { opacity: 0; transform: translateY(55px) scale(0.35); }
}
@keyframes liLogoSeq {
  0%, 32%   { opacity: 0; transform: translateX(0) scale(1.1); }
  38%       { opacity: 1; transform: translateX(0) scale(1.1); }
  52%       { opacity: 1; transform: translateX(0) scale(0.82); }
  62%, 92%  { opacity: 1; transform: translateX(-132px) scale(0.82); }
  98%, 100% { opacity: 0; transform: translateX(-132px) scale(0.82); }
}
@keyframes liLettersPop {
  0%, 35%   { opacity: 0; transform: scale(0.6); }
  46%, 100% { opacity: 1; transform: scale(1); }
}
@keyframes liTextReveal {
  0%, 58%   { opacity: 0; transform: translateX(-18px); }
  68%, 92%  { opacity: 1; transform: translateX(0); }
  98%, 100% { opacity: 0; transform: translateX(0); }
}
</style>
<script data-roasist-perf-channels-3d-script>
(() => {
  // 1. GOOGLE ADS
  const GADS_SVG_HTML = `<div class="roasist-brand-stage gads-anim-stage" aria-hidden="true">
  <svg viewBox="0 0 600 320" class="roasist-brand-svg gads-svg" xmlns="http://www.w3.org/2000/svg">
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
        <rect x="172" y="100" width="56" height="145" fill="url(#gradGreen)"/>
        <circle cx="200" cy="100" r="28" fill="#34A853"/>
        <text x="200" y="109" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="25">$</text>
      </g>
      <g class="col-group col-yellow">
        <rect x="272" y="100" width="56" height="145" fill="url(#gradYellow)"/>
        <circle cx="300" cy="100" r="28" fill="#FBBC05"/>
        <path d="M289 95h22l2 5h-26l2-5zm1 6h20v11h-6v-6h-8v6h-6v-11z" fill="#FFFFFF"/>
      </g>
      <g class="col-group col-blue">
        <rect x="372" y="100" width="56" height="145" fill="url(#gradBlue)"/>
        <circle cx="400" cy="100" r="28" fill="#4285F4"/>
        <circle cx="400" cy="94" r="4.5" fill="#FFFFFF"/>
        <path d="M391 107c0-4 4-6 9-6s9 2 9 6" fill="#FFFFFF"/>
        <circle cx="390" cy="96" r="3.2" fill="#FFFFFF" opacity="0.85"/>
        <circle cx="410" cy="96" r="3.2" fill="#FFFFFF" opacity="0.85"/>
      </g>
    </g>

    <g class="logo-assembly">
      <g class="pill-yellow-wrap">
        <rect x="282" y="107" width="36" height="116" rx="18" fill="#FBBC05" transform="rotate(30 300 125)"/>
      </g>
      <g class="dot-green-wrap">
        <circle cx="260" cy="194.28" r="18" fill="#34A853"/>
      </g>
      <g class="pill-blue-wrap">
        <rect x="282" y="107" width="36" height="116" rx="18" fill="#4285F4" transform="rotate(-30 300 125)"/>
      </g>
    </g>

    <g class="brand-text">
      <text x="235" y="175" font-family="'Product Sans', 'Inter', Arial, sans-serif" font-size="44" font-weight="500" fill="#5F6368" letter-spacing="-0.5">
        Google Ads
      </text>
    </g>
  </svg>
</div>`;

  // 2. INSTAGRAM & FACEBOOK (META ADS)
  const META_SVG_HTML = `<div class="roasist-brand-stage meta-anim-stage" aria-hidden="true">
  <svg viewBox="0 0 600 320" class="roasist-brand-svg meta-svg" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="metaGradIg" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#E1306C" stop-opacity="0.92"/>
        <stop offset="100%" stop-color="#E1306C" stop-opacity="0"/>
      </linearGradient>
      <linearGradient id="metaGradIgCircle" x1="0" y1="1" x2="1" y2="0">
        <stop offset="0%" stop-color="#F58529"/>
        <stop offset="48%" stop-color="#DD2A7B"/>
        <stop offset="100%" stop-color="#8134AF"/>
      </linearGradient>
      <linearGradient id="metaGradFb" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#0081FB" stop-opacity="0.95"/>
        <stop offset="100%" stop-color="#0081FB" stop-opacity="0"/>
      </linearGradient>
      <linearGradient id="metaGradConv" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#0064E0" stop-opacity="0.95"/>
        <stop offset="100%" stop-color="#0064E0" stop-opacity="0"/>
      </linearGradient>
      <linearGradient id="metaInfinityGrad" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="#0064E0"/>
        <stop offset="50%" stop-color="#0081FB"/>
        <stop offset="100%" stop-color="#0064E0"/>
      </linearGradient>
      <linearGradient id="metaCrossShadow" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="#004BB5"/>
        <stop offset="100%" stop-color="#0081FB"/>
      </linearGradient>
    </defs>

    <g class="meta-grid-lines">
      <line x1="120" y1="95"  x2="480" y2="95"  stroke="#CBD5E1" stroke-width="1.5"/>
      <line x1="120" y1="130" x2="480" y2="130" stroke="#CBD5E1" stroke-width="1.5"/>
      <line x1="120" y1="165" x2="480" y2="165" stroke="#CBD5E1" stroke-width="1.5"/>
      <line x1="120" y1="200" x2="480" y2="200" stroke="#CBD5E1" stroke-width="1.5"/>
    </g>

    <g class="meta-bars-phase">
      <g class="meta-col-ig">
        <rect x="172" y="100" width="56" height="145" fill="url(#metaGradIg)"/>
        <circle cx="200" cy="100" r="28" fill="url(#metaGradIgCircle)"/>
        <rect x="188" y="88" width="24" height="24" rx="6.5" fill="none" stroke="#FFFFFF" stroke-width="2.4"/>
        <circle cx="200" cy="100" r="5.5" fill="none" stroke="#FFFFFF" stroke-width="2.3"/>
        <circle cx="206.8" cy="93.2" r="1.6" fill="#FFFFFF"/>
      </g>
      <g class="meta-col-fb">
        <rect x="272" y="100" width="56" height="145" fill="url(#metaGradFb)"/>
        <circle cx="300" cy="100" r="28" fill="#0081FB"/>
        <path d="M303.5 114v-12.2h4.1l.6-4.7h-4.7v-3c0-1.4.4-2.3 2.4-2.3h2.5v-4.2c-.4-.1-1.9-.2-3.6-.2-3.6 0-6.1 2.2-6.1 6.2v3.5h-4.1v4.7h4.1V114h4.8z" fill="#FFFFFF"/>
      </g>
      <g class="meta-col-conv">
        <rect x="372" y="100" width="56" height="145" fill="url(#metaGradConv)"/>
        <circle cx="400" cy="100" r="28" fill="#0064E0"/>
        <path d="M390 95h20l-1.6 15.5a2 2 0 0 1-2 1.8h-12.8a2 2 0 0 1-2-1.8L390 95z" fill="none" stroke="#FFFFFF" stroke-width="2.3" stroke-linejoin="round"/>
        <path d="M395.5 95v-2.5a4.5 4.5 0 0 1 9 0V95" fill="none" stroke="#FFFFFF" stroke-width="2.3" stroke-linecap="round"/>
      </g>
    </g>

    <g class="meta-logo-assembly">
      <path
        class="meta-infinity-ribbon"
        d="M 300 156 C 282 126, 268 116, 250 116 C 228 116, 216 140, 216 168 C 216 192, 229 204, 246 204 C 265 204, 281 186, 300 156 C 319 126, 332 116, 350 116 C 372 116, 384 140, 384 168 C 384 192, 371 204, 354 204 C 335 204, 319 186, 300 156 Z"
        fill="none"
        stroke="url(#metaInfinityGrad)"
        stroke-width="17"
        stroke-linecap="round"
        stroke-linejoin="round"
      />
      <path
        class="meta-ribbon-crossover"
        d="M 284 130 C 292 142, 300 156, 316 182"
        fill="none"
        stroke="url(#metaCrossShadow)"
        stroke-width="17.2"
        stroke-linecap="round"
      />
    </g>

    <g class="meta-brand-text">
      <text x="268" y="175" font-family="'Inter', -apple-system, BlinkMacSystemFont, Arial, sans-serif" font-size="44" font-weight="600" fill="#1C2B33" letter-spacing="-0.8">
        Meta Ads
      </text>
    </g>
  </svg>
</div>`;

  // 3. TIKTOK ADS (Rhythmic Vertical Soundwave + 9:16 Frame -> Chromatic Split-Snap Note)
  const TIKTOK_SVG_HTML = `<div class="roasist-brand-stage tiktok-anim-stage" aria-hidden="true">
  <svg viewBox="0 0 600 320" class="roasist-brand-svg" xmlns="http://www.w3.org/2000/svg">
    <!-- 1. Dikey 9:16 Kısa Video Çerçevesi ve Ses Ekolayzeri -->
    <g class="tt-frame">
      <rect x="242" y="68" width="116" height="184" rx="22" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="2"/>
      <rect x="282" y="79" width="36" height="5" rx="2.5" fill="#CBD5E1"/>
      <polygon points="292,146 316,160 292,174" fill="#0F172A" opacity="0.12"/>
    </g>

    <g class="tt-eq-group">
      <rect class="tt-eq-1" x="215" y="128" width="18" height="64" rx="9" fill="#25F4EE"/>
      <rect class="tt-eq-2" x="253" y="106" width="18" height="108" rx="9" fill="#010101"/>
      <rect class="tt-eq-3" x="291" y="96"  width="18" height="128" rx="9" fill="#FE2C55"/>
      <rect class="tt-eq-4" x="329" y="106" width="18" height="108" rx="9" fill="#010101"/>
      <rect class="tt-eq-5" x="367" y="128" width="18" height="64" rx="9" fill="#25F4EE"/>
    </g>

    <!-- 2. Resmi TikTok Nota Sembolü (Cyan + Crimson + Black 3 Katmanlı Kilitlenme) -->
    <g class="tt-logo-assembly">
      <!-- Cyan Offset Layer -->
      <path class="tt-note-cyan" fill="#25F4EE"
        d="M316 98h18c1.5 14 11 25 25 27v18c-10 0-19-3.2-26-8.6v42.6c0 22.8-18.4 41-41 41s-41-18.2-41-41 18.4-41 41-41c2.8 0 5.5.3 8 .9v19.2c-2.5-.8-5.2-1.3-8-1.3-12.2 0-22 9.8-22 22s9.8 22 22 22 24-9.5 24-23.5V98z"/>
      <!-- Crimson Offset Layer -->
      <path class="tt-note-red" fill="#FE2C55"
        d="M316 98h18c1.5 14 11 25 25 27v18c-10 0-19-3.2-26-8.6v42.6c0 22.8-18.4 41-41 41s-41-18.2-41-41 18.4-41 41-41c2.8 0 5.5.3 8 .9v19.2c-2.5-.8-5.2-1.3-8-1.3-12.2 0-22 9.8-22 22s9.8 22 22 22 24-9.5 24-23.5V98z"/>
      <!-- Crisp Black Core Layer -->
      <path class="tt-note-core" fill="#010101"
        d="M316 98h18c1.5 14 11 25 25 27v18c-10 0-19-3.2-26-8.6v42.6c0 22.8-18.4 41-41 41s-41-18.2-41-41 18.4-41 41-41c2.8 0 5.5.3 8 .9v19.2c-2.5-.8-5.2-1.3-8-1.3-12.2 0-22 9.8-22 22s9.8 22 22 22 24-9.5 24-23.5V98z"/>
    </g>

    <!-- 3. TikTok Ads Metni -->
    <g class="tt-brand-text">
      <text x="255" y="175" font-family="'Inter', -apple-system, BlinkMacSystemFont, Arial, sans-serif" font-size="44" font-weight="700" fill="#010101" letter-spacing="-1">
        TikTok Ads
      </text>
    </g>
  </svg>
</div>`;

  // 4. YANDEX ADS (Concentric Eurasia/CIS Radar & Market Beacons -> Official Yandex Red Я Mark)
  const YANDEX_SVG_HTML = `<div class="roasist-brand-stage yandex-anim-stage" aria-hidden="true">
  <svg viewBox="0 0 600 320" class="roasist-brand-svg" xmlns="http://www.w3.org/2000/svg">
    <!-- 1. Uluslararası / Avrasya Pazar Radarı & Yörünge Sinyalleri -->
    <g class="yd-radar-ring-2">
      <circle cx="300" cy="160" r="108" fill="none" stroke="#E2E8F0" stroke-width="1.6" stroke-dasharray="6 6"/>
      <line x1="176" y1="160" x2="424" y2="160" stroke="#F1F5F9" stroke-width="1.4"/>
      <line x1="300" y1="42"  x2="300" y2="278" stroke="#F1F5F9" stroke-width="1.4"/>
    </g>
    <g class="yd-radar-ring-1">
      <circle cx="300" cy="160" r="68" fill="#FEF2F2" stroke="#FCA5A5" stroke-width="1.8"/>
    </g>

    <g class="yd-beacons">
      <!-- Connecting Direct Signal Rays -->
      <line x1="300" y1="160" x2="210" y2="108" stroke="#FC3F1D" stroke-width="2" stroke-opacity="0.45"/>
      <line x1="300" y1="160" x2="392" y2="118" stroke="#FFCC00" stroke-width="2.2" stroke-opacity="0.75"/>
      <line x1="300" y1="160" x2="348" y2="236" stroke="#FC3F1D" stroke-width="2" stroke-opacity="0.45"/>
      <line x1="300" y1="160" x2="226" y2="224" stroke="#94A3B8" stroke-width="1.8" stroke-opacity="0.45"/>
      <!-- Orbiting Market Nodes -->
      <circle cx="210" cy="108" r="12" fill="#FC3F1D"/>
      <circle cx="392" cy="118" r="14" fill="#FFCC00"/>
      <circle cx="348" cy="236" r="11" fill="#FC3F1D"/>
      <circle cx="226" cy="224" r="9"  fill="#0F172A"/>
      <circle cx="300" cy="160" r="15" fill="#FC3F1D"/>
    </g>

    <!-- 2. Resmi Yandex Kırmızı Daire & Beyaz Я Logosu -->
    <g class="yd-logo-assembly">
      <circle cx="300" cy="160" r="54" fill="#FC3F1D"/>
      <g class="yd-glyph">
        <path fill="#FFFFFF"
          d="M312.5 123h-12.2c-15.6 0-25.8 9.2-25.8 23.2 0 11 5.6 17.8 14.8 22.1l-17 28.7h14.4l15.4-26.6h6.4v26.6h12V123h-8zm-4 36.8h-5.8c-8.2 0-14-4.5-14-13.2 0-8.6 5.4-13.2 13.5-13.2h6.3v26.4z"/>
      </g>
    </g>

    <!-- 3. Yandex Ads Metni -->
    <g class="yd-brand-text">
      <text x="242" y="175" font-family="'Inter', -apple-system, BlinkMacSystemFont, Arial, sans-serif" font-size="44" font-weight="600" fill="#111827" letter-spacing="-0.8">
        Yandex Ads
      </text>
    </g>
  </svg>
</div>`;

  // 5. BING ADS (Multi-Engine Desktop Search Ribbons -> Official Folded Bing Ribbon Mark)
  const BING_SVG_HTML = `<div class="roasist-brand-stage bing-anim-stage" aria-hidden="true">
  <svg viewBox="0 0 600 320" class="roasist-brand-svg" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="bingStemGrad" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#00B294"/>
        <stop offset="100%" stop-color="#008373"/>
      </linearGradient>
      <linearGradient id="bingWingGrad" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="#00A4EF"/>
        <stop offset="100%" stop-color="#0078D4"/>
      </linearGradient>
    </defs>

    <!-- 1. Çoklu Masaüstü Arama Ağı Şeritleri (Bing, Yahoo, DuckDuckGo) -->
    <g class="bing-rows-phase">
      <g class="bing-row-1">
        <rect x="175" y="92" width="250" height="36" rx="18" fill="#F0FDFA" stroke="#99F6E4" stroke-width="1.5"/>
        <circle cx="195" cy="110" r="10" fill="#008373"/>
        <rect x="216" y="105" width="124" height="10" rx="5" fill="#0F172A" opacity="0.8"/>
        <rect x="358" y="105" width="46"  height="10" rx="5" fill="#00B294"/>
      </g>
      <g class="bing-row-2">
        <rect x="155" y="142" width="290" height="36" rx="18" fill="#EFF6FF" stroke="#BFDBFE" stroke-width="1.5"/>
        <circle cx="175" cy="160" r="10" fill="#0078D4"/>
        <rect x="196" y="155" width="156" height="10" rx="5" fill="#0F172A" opacity="0.85"/>
        <rect x="368" y="155" width="56"  height="10" rx="5" fill="#00A4EF"/>
      </g>
      <g class="bing-row-3">
        <rect x="185" y="192" width="230" height="36" rx="18" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.5"/>
        <circle cx="205" cy="210" r="10" fill="#00B294"/>
        <rect x="226" y="205" width="108" height="10" rx="5" fill="#475569" opacity="0.75"/>
        <rect x="348" y="205" width="46"  height="10" rx="5" fill="#10B981"/>
      </g>
    </g>

    <!-- 2. Resmi Bing Katlanan Şerit Logosu -->
    <g class="bing-logo-assembly">
      <!-- Sol Dikey Şerit -->
      <path fill="url(#bingStemGrad)"
        d="M266 98l26 9.5v88.5l-26 14.5V98z"/>
      <!-- Sağ Katlanan Ok/Kanat Şeridi -->
      <g class="bing-wing">
        <path fill="url(#bingWingGrad)"
          d="M292 146.5l48 17.5c6 2.2 8.5 9.2 5.2 14.6l-11.2 18.4-68 24.5 26-25.5 26.5-10.2-26.5-11.8v-27.5z"/>
      </g>
    </g>

    <!-- 3. Bing Ads Metni -->
    <g class="bing-brand-text">
      <text x="260" y="175" font-family="'Inter', -apple-system, BlinkMacSystemFont, Arial, sans-serif" font-size="44" font-weight="600" fill="#1E293B" letter-spacing="-0.8">
        Bing Ads
      </text>
    </g>
  </svg>
</div>`;

  // 6. LINKEDIN ADS (B2B Executive Decision-Maker Network Graph -> Official LinkedIn 'in' Badge)
  const LINKEDIN_SVG_HTML = `<div class="roasist-brand-stage linkedin-anim-stage" aria-hidden="true">
  <svg viewBox="0 0 600 320" class="roasist-brand-svg" xmlns="http://www.w3.org/2000/svg">
    <!-- 1. Kurumsal B2B Karar Verici Ağı (Şirketler -> Direktörler -> C-Suite) -->
    <g class="li-graph-links" stroke="#93C5FD" stroke-width="2.2" fill="none" stroke-linecap="round">
      <line x1="216" y1="212" x2="258" y2="158"/>
      <line x1="300" y1="212" x2="258" y2="158"/>
      <line x1="300" y1="212" x2="342" y2="158"/>
      <line x1="384" y1="212" x2="342" y2="158"/>
      <line x1="258" y1="158" x2="300" y2="102"/>
      <line x1="342" y1="158" x2="300" y2="102"/>
    </g>

    <g class="li-tier-bot">
      <circle cx="216" cy="212" r="14" fill="#E2E8F0"/>
      <circle cx="300" cy="212" r="14" fill="#CBD5E1"/>
      <circle cx="384" cy="212" r="14" fill="#E2E8F0"/>
    </g>

    <g class="li-tier-mid">
      <circle cx="258" cy="158" r="17" fill="#60A5FA"/>
      <circle cx="342" cy="158" r="17" fill="#60A5FA"/>
    </g>

    <g class="li-tier-top">
      <circle cx="300" cy="102" r="24" fill="#0A66C2"/>
      <circle cx="300" cy="96" r="5" fill="#FFFFFF"/>
      <path d="M290 111c0-5 4.5-7.5 10-7.5s10 2.5 10 7.5" fill="#FFFFFF"/>
    </g>

    <!-- 2. Resmi LinkedIn 'in' Rozeti -->
    <g class="li-logo-assembly">
      <rect x="248" y="108" width="104" height="104" rx="18" fill="#0A66C2"/>
      <g class="li-in-letters" fill="#FFFFFF">
        <circle cx="275" cy="136" r="7.5"/>
        <rect x="268.5" y="150" width="13" height="43" rx="2"/>
        <path d="M294 150h12.5v6h.2c1.8-3.4 6.2-7 13-7 13.8 0 16.3 9 16.3 20.8V193h-13v-20.5c0-4.9-.1-11.2-6.8-11.2-6.8 0-7.9 5.3-7.9 10.8V193h-14.3v-43z"/>
      </g>
    </g>

    <!-- 3. LinkedIn Ads Metni -->
    <g class="li-brand-text">
      <text x="232" y="175" font-family="'Inter', -apple-system, BlinkMacSystemFont, Arial, sans-serif" font-size="44" font-weight="600" fill="#1D2226" letter-spacing="-0.8">
        LinkedIn Ads
      </text>
    </g>
  </svg>
</div>`;

  const CHANNEL_STAGES = [
    { cls: 'gads-anim-stage',     html: GADS_SVG_HTML },
    { cls: 'meta-anim-stage',     html: META_SVG_HTML },
    { cls: 'tiktok-anim-stage',   html: TIKTOK_SVG_HTML },
    { cls: 'yandex-anim-stage',   html: YANDEX_SVG_HTML },
    { cls: 'bing-anim-stage',     html: BING_SVG_HTML },
    { cls: 'linkedin-anim-stage', html: LINKEDIN_SVG_HTML }
  ];

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
    container.querySelectorAll('img').forEach(img => {
      if (!img.dataset.roasistDisabled) {
        img.dataset.roasistDisabled = 'true';
        img.removeAttribute('data-src');
        img.removeAttribute('data-srcset');
      }
    });
  }

  function mountAllChannels() {
    const rows = document.querySelectorAll('.TextImageRows_row__PPlpB');
    if (!rows || rows.length === 0) return;

    rows.forEach((row, idx) => {
      if (idx >= CHANNEL_STAGES.length) return;
      const mediaBox = row.querySelector('.TextImageRows_media__twu3R .ImageEnter_image__FSEP_')
                    || row.querySelector('.TextImageRows_media__twu3R');
      if (!mediaBox) return;

      disableNativeMedia(mediaBox);

      const oldCv = mediaBox.querySelector('canvas.roasist-perf-channel-canvas');
      if (oldCv) oldCv.remove();

      const spec = CHANNEL_STAGES[idx];
      if (!mediaBox.querySelector('.' + spec.cls)) {
        mediaBox.insertAdjacentHTML('beforeend', spec.html);
      }
    });
  }

  // Mount immediately and re-verify after React hydration settles
  mountAllChannels();
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mountAllChannels);
  }
  const mo = new MutationObserver(() => mountAllChannels());
  if (document.body) {
    mo.observe(document.body, { childList: true, subtree: true });
  }
  setTimeout(mountAllChannels, 400);
  setTimeout(mountAllChannels, 1400);
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

    html = re.sub(
        r"<style data-roasist-perf-channels-3d-style>.*?</style>\s*<script data-roasist-perf-channels-3d-script>.*?</script>",
        "",
        html,
        flags=re.DOTALL,
    )

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
    print(f"[OK] Injected 6x Brand Motion SVG Stages into {rel_path} ({len(html):,} bytes)")


def main():
    for rel in TARGET_FILES:
        inject_file(rel)


if __name__ == "__main__":
    main()
