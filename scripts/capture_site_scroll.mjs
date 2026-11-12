// Usage: node capture_site_scroll.mjs <slug> <url> <outDir> [frames=132] [maxScroll=2600]
// Captures desktop (1440x900) and mobile (390x844) viewport frames while easing the page scroll.
import fs from 'node:fs';
import path from 'node:path';
import { spawn } from 'node:child_process';

const [slug, url, outDir, framesArg, maxScrollArg] = process.argv.slice(2);
const FRAMES = Number(framesArg || 132);
const MAX_SCROLL = Number(maxScrollArg || 2600);
fs.mkdirSync(outDir, { recursive: true });

const dbgPort = 9800 + Math.floor(Math.random() * 150);
const chrome = spawn('/usr/bin/chromium', [
  '--headless=new', '--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage', '--hide-scrollbars',
  `--user-data-dir=/tmp/chr-cap-${slug}-${Date.now()}`, '--no-first-run', '--mute-audio',
  `--proxy-server=${process.env.HTTPS_PROXY || process.env.HTTP_PROXY}`, '--ignore-certificate-errors',
  '--autoplay-policy=no-user-gesture-required',
  `--remote-debugging-port=${dbgPort}`, '--window-size=1440,900', 'about:blank'
], { stdio: 'ignore' });

const sleep = ms => new Promise(r => setTimeout(r, ms));
let targets;
for (let i = 0; i < 40; i++) {
  try { targets = await fetch(`http://127.0.0.1:${dbgPort}/json`).then(r => r.json()); if (targets?.length) break; } catch {}
  await sleep(250);
}
const ws = new WebSocket(targets.find(t => t.type === 'page').webSocketDebuggerUrl);
await new Promise(r => ws.addEventListener('open', r));
let id = 0; const pending = new Map();
ws.addEventListener('message', ev => { const m = JSON.parse(ev.data); if (m.id && pending.has(m.id)) { pending.get(m.id)(m.result || m.error); pending.delete(m.id); } });
const send = (method, params = {}) => new Promise(res => { const c = ++id; pending.set(c, res); ws.send(JSON.stringify({ id: c, method, params })); });
const ev = async expr => (await send('Runtime.evaluate', { expression: expr, returnByValue: true, awaitPromise: true }))?.result?.value;

const DISMISS = `(() => {
  const words = ['kabul', 'accept', 'tümünü', 'allow', 'agree', 'anladım', 'tamam', 'got it', 'ok', 'onayla', 'izin ver', 'kapat', 'close'];
  let n = 0;
  document.querySelectorAll('button, a, [role=button], div[class*=cookie] span').forEach(b => {
    const t = (b.innerText || b.getAttribute('aria-label') || '').trim().toLowerCase();
    if (t && t.length < 40 && words.some(w => t === w || t.startsWith(w))) { const r = b.getBoundingClientRect(); if (r.width && r.height) { try { b.click(); n++; } catch {} } }
  });
  document.querySelectorAll('[id*=cookie i], [class*=cookie i], [id*=consent i], [class*=consent i], [class*=gdpr i], [id*=CybotCookiebot], .cky-consent-container, #onetrust-banner-sdk, [class*=popup i][class*=newsletter i]').forEach(e => { const cs = getComputedStyle(e); if (cs.position === 'fixed' || cs.position === 'sticky' || cs.position === 'absolute') e.style.setProperty('display', 'none', 'important'); });
  // Floating chat / whatsapp widgets
  document.querySelectorAll('[class*=whatsapp i], [id*=whatsapp i], [class*=chat-widget i], iframe[title*=chat i], #tidio-chat, [class*=tawk i]').forEach(e => e.style.setProperty('display', 'none', 'important'));
  // Generic: fixed/sticky overlays mentioning cookies, and small floating widgets near the bottom edge
  document.querySelectorAll('body *').forEach(e => {
    const cs = getComputedStyle(e);
    if (cs.position !== 'fixed') return;
    const r = e.getBoundingClientRect();
    const txt = (e.innerText || '').toLowerCase();
    const isCookie = /cookie|çerez|gdpr|datenschutz/.test(txt) && r.height < innerHeight * 0.9;
    const isFloating = r.width > 0 && r.width < 440 && r.height < 360 && r.bottom > innerHeight - 380 && r.top > innerHeight * 0.3;
    if (isCookie || isFloating || e.tagName === 'IFRAME') e.style.setProperty('display', 'none', 'important');
  });
  document.documentElement.style.overflow = ''; document.body.style.overflow = '';
  const overlayRoot = el => {
    let best = null;
    for (let e = el; e && e !== document.body && e !== document.documentElement; e = e.parentElement) {
      const cs = getComputedStyle(e);
      if (cs.position === 'fixed' || cs.position === 'sticky' || (cs.position === 'absolute' && Number(cs.zIndex) >= 50)) best = e;
    }
    return best;
  };
  const hide = e => { if (!e) return; const r = e.getBoundingClientRect(); if (r.height < innerHeight * 0.92 || r.width < innerWidth * 0.9) e.style.setProperty('display', 'none', 'important'); };
  // Text-anchored overlays (cookie banners, push-notification prompts, chat bubbles)
  const re = /(cookie|çerez|personal data|kişisel veri|stay informed|enable notification|we're offline|leave a message|hello! let us|chat with us|online now)/i;
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const hits = new Set();
  for (let t; (t = walker.nextNode());) { if (re.test(t.textContent) && t.parentElement) hits.add(t.parentElement); }
  hits.forEach(p => hide(overlayRoot(p)));
  // Shadow-DOM consent managers (Efilli, Usercentrics, etc.)
  document.querySelectorAll('*').forEach(e => {
    if (e.shadowRoot && (/efilli|usercentrics|consent|cookie/i.test(e.tagName + ' ' + e.id) || /cookie|personal data|çerez/i.test(e.shadowRoot.textContent || ''))) e.style.setProperty('display', 'none', 'important');
  });
  // Corner-anchored floating widgets
  [[innerWidth - 40, innerHeight - 40], [innerWidth - 90, innerHeight - 90], [40, innerHeight - 40], [90, innerHeight - 90], [innerWidth - 40, innerHeight - 160], [60, innerHeight - 160]].forEach(([x, y]) => {
    const el = document.elementFromPoint(x, y); const root = el && overlayRoot(el);
    if (root) { const r = root.getBoundingClientRect(); if (r.width < 460 && r.height < 520) root.style.setProperty('display', 'none', 'important'); }
  });
  return n;
})()`;

async function capture(mode) {
  const mobile = mode === 'm';
  const W = mobile ? 390 : 1440, H = mobile ? 844 : 900;
  await send('Emulation.setDeviceMetricsOverride', { width: W, height: H, deviceScaleFactor: mobile ? 2 : 1, mobile });
  await send('Emulation.setUserAgentOverride', { userAgent: mobile
    ? 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1'
    : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36' });
  await send('Page.navigate', { url });
  await sleep(6500);
  await ev(DISMISS); await sleep(800); await ev(DISMISS);
  // Pre-scroll to trigger lazy loading & reveal animations
  const docH = await ev('Math.max(document.documentElement.scrollHeight, document.body.scrollHeight)');
  const maxS = Math.min(mobile ? MAX_SCROLL * 1.15 : MAX_SCROLL, Math.max(0, docH - H));
  for (let y = 0; y <= maxS; y += 250) { await ev(`window.scrollTo(0, ${y})`); await sleep(120); }
  await ev('window.scrollTo(0, 0)'); await sleep(1800); await ev(DISMISS); await sleep(400);
  // Disable smooth scrolling libs so scrollTo is immediate
  await ev(`document.documentElement.style.scrollBehavior='auto'; document.body.style.scrollBehavior='auto'; 1`);
  const ease = t => t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
  const HOLD_START = Math.round(FRAMES * 0.12), HOLD_END = Math.round(FRAMES * 0.08);
  for (let f = 0; f < FRAMES; f++) {
    let t = (f - HOLD_START) / (FRAMES - HOLD_START - HOLD_END);
    t = Math.min(1, Math.max(0, t));
    const y = Math.round(ease(t) * maxS);
    await ev(`window.scrollTo(0, ${y}); new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)))`);
    if (f % 8 === 0) await ev(DISMISS);
    await sleep(45);
    const shot = await send('Page.captureScreenshot', { format: 'jpeg', quality: 92 });
    fs.writeFileSync(path.join(outDir, `${mode}_${String(f).padStart(3, '0')}.jpg`), Buffer.from(shot.data, 'base64'));
  }
  return { docH, maxS };
}

await send('Page.enable'); await send('Runtime.enable');
const d = await capture('d');
const m = await capture('m');
console.log(JSON.stringify({ slug, d, m }));
ws.close(); chrome.kill();
process.exit(0);
