import fs from 'node:fs';
import path from 'node:path';
import { spawn } from 'node:child_process';

const ROOT = '/home/antigravity/Roasist/roasist-web';
const OUT_DIR = path.join(ROOT, 'scripts/assets/methodology/s2');
fs.mkdirSync(OUT_DIR, { recursive: true });

const b64File = rel => fs.readFileSync(path.join(ROOT, rel)).toString('base64');

const webCordelia = b64File('scripts/assets/web-screens/cordelia.jpg');
const webLivaneli = b64File('scripts/assets/web-screens/livaneli.jpg');
const webSummer = b64File('scripts/assets/web-screens/summerhomes.jpg');
const webTalent = b64File('scripts/assets/web-screens/talentfinder.jpg');
const webHr = b64File('scripts/assets/web-screens/hrshortlist.jpg');

const refBircan = b64File('public/images/references/doctor-bircan.jpg');
const refDus = b64File('public/images/references/dus-bahcesi-okullari.jpg');
const refSurgeons = b64File('public/images/references/center-of-surgeons.jpg');
const refAutarke = b64File('public/images/references/autarke-call-center.jpg');

const logoSvgRaw = fs.readFileSync(path.join(ROOT, 'public/roasist-logo.svg'), 'utf8');
const iconMatch = logoSvgRaw.match(/<path class="cls-1" d="([^"]+)"><\/path>/);
const rIconPath = iconMatch ? iconMatch[1] : '';
const fullPaths = [...logoSvgRaw.matchAll(/<path class="cls-1" d="([^"]+)"><\/path>/g)].map(m => m[1]);

const bin = fs.existsSync('/usr/bin/chromium') ? '/usr/bin/chromium' : '/usr/bin/google-chrome';
const dbgPort = 9896;
const chrome = spawn(bin, [
  '--headless=new', '--no-sandbox', '--disable-gpu', '--hide-scrollbars',
  `--proxy-server=${process.env.HTTPS_PROXY || process.env.HTTP_PROXY}`,
  '--ignore-certificate-errors',
  `--user-data-dir=/tmp/chr-m2-${Date.now()}`, `--remote-debugging-port=${dbgPort}`,
  '--window-size=2800,2100', 'about:blank'
], { stdio: 'ignore' });

const sleep = ms => new Promise(r => setTimeout(r, ms));
let targets;
for (let i = 0; i < 30; i++) {
  try { targets = await fetch(`http://127.0.0.1:${dbgPort}/json`).then(r => r.json()); if (targets?.length) break; } catch {}
  await sleep(200);
}
const ws = new WebSocket(targets.find(t => t.type === 'page').webSocketDebuggerUrl);
await new Promise(r => ws.addEventListener('open', r));
let id = 0; const pending = new Map();
ws.addEventListener('message', ev => {
  const m = JSON.parse(ev.data);
  if (m.id && pending.has(m.id)) { pending.get(m.id)(m.result || m.error); pending.delete(m.id); }
});
const send = (method, params = {}) => new Promise(res => { const c = ++id; pending.set(c, res); ws.send(JSON.stringify({ id: c, method, params })); });

await send('Page.enable');
await send('Runtime.enable');
const frameId = (await send('Page.getFrameTree')).frameTree.frame.id;

async function renderPng(name, width, height, bodyHtml, transparent = true) {
  await send('Emulation.setDeviceMetricsOverride', { width, height, deviceScaleFactor: 1, mobile: false });
  await send('Emulation.setDefaultBackgroundColorOverride', {
    color: transparent ? { r: 0, g: 0, b: 0, a: 0 } : { r: 5, g: 5, b: 8, a: 1 }
  });
  const doc = `<!doctype html><html><head><meta charset="utf-8">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&display=swap" rel="stylesheet">
    <style>
      * { box-sizing: border-box; margin: 0; padding: 0; }
      body {
        width: ${width}px; height: ${height}px; overflow: hidden;
        background: ${transparent ? 'transparent' : '#050508'};
        font-family: 'DM Sans', sans-serif;
        font-variant-numeric: tabular-nums;
        -webkit-font-smoothing: antialiased;
      }
    </style></head><body>${bodyHtml}</body></html>`;
  await send('Page.setDocumentContent', { frameId, html: doc });
  await send('Runtime.evaluate', { expression: 'document.fonts.ready', awaitPromise: true });
  await sleep(160);
  const shot = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(OUT_DIR, name), Buffer.from(shot.data, 'base64'));
  console.log('Rendered', name);
}

// 1. Bento Grid Surroundings (2800 x 2100)
// Center screen sits at x=800, y=610, w=1200, h=820 (with transparent interior so Python draws live 3D particles inside!)
await renderPng('bento-grid-overlay.png', 2800, 2100, `
  <div style="position:relative;width:2800px;height:2100px;">
    <!-- Top Row Left: Coral Brand Messaging Tile -->
    <div style="position:absolute;left:120px;top:70px;width:960px;height:490px;border-radius:26px;
      background:linear-gradient(135deg,#fb7185 0%,#f43f5e 55%,#e11d48 100%);padding:48px 54px;color:#fff;
      display:flex;flex-direction:column;justify-content:space-between;box-shadow:0 24px 60px rgba(0,0,0,0.45);">
      <div style="display:flex;justify-content:space-between;align-items:center;">
        <span style="font-size:16px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;opacity:0.9;">KREATİF SİSTEM 01</span>
        <span style="padding:8px 18px;border-radius:999px;background:rgba(255,255,255,0.2);font-size:15px;font-weight:600;">Marka Dili</span>
      </div>
      <div style="font-size:56px;font-weight:600;line-height:1.08;letter-spacing:-0.025em;">
        Dönüşüm Odaklı<br>Kreatif Söylem
      </div>
    </div>

    <!-- Top Row Center: Dark Emerald Mini Showcase -->
    <div style="position:absolute;left:1130px;top:70px;width:820px;height:490px;border-radius:26px;
      background:radial-gradient(circle at 65% 45%,#0f766e 0%,#062c28 65%,#041312 100%);padding:42px 48px;color:#fff;
      border:1px solid rgba(255,255,255,0.10);display:flex;flex-direction:column;justify-content:space-between;">
      <div style="font-size:15px;font-weight:600;color:#5eead4;letter-spacing:0.06em;text-transform:uppercase;">GÖRSEL KİMLİK MİMARİSİ</div>
      <div style="font-size:42px;font-weight:600;line-height:1.14;letter-spacing:-0.02em;max-width:520px;">
        İlk 3 Saniyede Dikkat Çeken Kanca Kurgusu
      </div>
      <div style="display:flex;gap:14px;">
        <span style="padding:8px 16px;border-radius:999px;background:rgba(94,234,212,0.14);color:#99f6e4;font-size:15px;font-weight:600;">+%64 İzlenme</span>
        <span style="padding:8px 16px;border-radius:999px;background:rgba(255,255,255,0.08);color:#e2e8f0;font-size:15px;font-weight:500;">UGC &amp; Motion</span>
      </div>
    </div>

    <!-- Top Row Right: Livaneli Hotels Screen -->
    <div style="position:absolute;left:2000px;top:70px;width:680px;height:490px;border-radius:26px;overflow:hidden;
      background:#0f172a;border:1px solid rgba(255,255,255,0.12);box-shadow:0 24px 60px rgba(0,0,0,0.45);">
      <img src="data:image/jpeg;base64,${webLivaneli}" style="width:100%;height:100%;object-fit:cover;object-position:top center;"/>
    </div>

    <!-- Middle Row Left: Cordelia Screen -->
    <div style="position:absolute;left:60px;top:610px;width:690px;height:820px;border-radius:26px;overflow:hidden;
      background:#0b1120;border:1px solid rgba(255,255,255,0.12);box-shadow:0 24px 60px rgba(0,0,0,0.45);">
      <img src="data:image/jpeg;base64,${webCordelia}" style="width:100%;height:100%;object-fit:cover;object-position:center top;"/>
      <div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(5,5,8,0.10) 0%,rgba(5,5,8,0.72) 100%);"></div>
      <div style="position:absolute;left:36px;bottom:36px;color:#fff;">
        <div style="font-size:14px;font-weight:700;letter-spacing:0.06em;color:#a78bfa;text-transform:uppercase;margin-bottom:8px;">WEB &amp; KREATİF</div>
        <div style="font-size:32px;font-weight:600;letter-spacing:-0.02em;">Cordelia Cyprus</div>
      </div>
    </div>

    <!-- CENTER HERO SCREEN FRAME (800, 610, 1200x820) - Transparent interior, crisp top navigation bar! -->
    <div style="position:absolute;left:800px;top:610px;width:1200px;height:820px;border-radius:26px;
      border:1.5px solid rgba(255,255,255,0.16);box-shadow:0 30px 90px rgba(0,0,0,0.65);pointer-events:none;">
      <div style="display:flex;align-items:center;justify-content:space-between;padding:28px 42px;">
        <svg viewBox="0 0 819.98 200" style="height:28px;width:auto;">
          ${fullPaths.map(d => `<path d="${d}" fill="#ffffff"/>`).join('')}
        </svg>
        <div style="display:flex;align-items:center;gap:28px;font-size:15px;font-weight:500;color:rgba(255,255,255,0.78);">
          <span>Strateji</span>
          <span>Kreatif Stüdyo</span>
          <span>Web Deneyimi</span>
          <span>Performans</span>
        </div>
        <div style="padding:10px 24px;border-radius:999px;background:#ffffff;color:#050508;font-size:15px;font-weight:700;">
          Projeyi Başlat
        </div>
      </div>
    </div>

    <!-- Middle Row Right: Vibrant Lime Strategy-to-Creative Card -->
    <div style="position:absolute;left:2050px;top:610px;width:690px;height:820px;border-radius:26px;
      background:linear-gradient(160deg,#bef264 0%,#4ade80 55%,#22c55e 100%);padding:48px;color:#052e16;
      display:flex;flex-direction:column;justify-content:space-between;box-shadow:0 24px 60px rgba(0,0,0,0.45);">
      <div style="display:flex;justify-content:space-between;align-items:center;">
        <span style="font-size:16px;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;">PERFORMANS KREATİFİ</span>
        <span style="padding:8px 16px;border-radius:999px;background:rgba(5,46,22,0.12);font-size:15px;font-weight:700;">ROAS Odaklı</span>
      </div>
      <div>
        <div style="font-size:60px;font-weight:700;line-height:1.04;letter-spacing:-0.03em;margin-bottom:22px;">
          Cesur Fikir.<br>Ölçülebilir<br>Dönüşüm.
        </div>
        <div style="font-size:22px;font-weight:500;line-height:1.45;opacity:0.88;">
          Estetik tasarımı gerçek kullanıcı psikolojisi ve dönüşüm verisiyle birleştiriyoruz.
        </div>
      </div>
      <div style="font-size:18px;font-weight:700;letter-spacing:-0.01em;">roasist.com / kreatif</div>
    </div>

    <!-- Bottom Row Left: Warm Amber Card -->
    <div style="position:absolute;left:120px;top:1480px;width:630px;height:520px;border-radius:26px;
      background:linear-gradient(135deg,#fde047 0%,#fb923c 100%);padding:44px 48px;color:#1c1917;
      display:flex;flex-direction:column;justify-content:space-between;">
      <div style="display:flex;justify-content:space-between;align-items:center;">
        <span style="font-size:15px;font-weight:700;text-transform:uppercase;letter-spacing:0.06em;">ETKİLEŞİM TASARIMI</span>
        <span style="padding:8px 18px;border-radius:999px;background:#ffffff;font-size:14px;font-weight:700;">UI / UX</span>
      </div>
      <div style="font-size:48px;font-weight:700;line-height:1.08;letter-spacing:-0.025em;">
        Akılda Kalan<br>Web Deneyimleri
      </div>
    </div>

    <!-- Bottom Row Center: Teal Editorial Feature -->
    <div style="position:absolute;left:800px;top:1480px;width:1200px;height:520px;border-radius:26px;
      background:linear-gradient(125deg,#0d9488 0%,#115e59 55%,#042f2e 100%);padding:46px 56px;color:#ffffff;
      border:1px solid rgba(255,255,255,0.12);display:flex;justify-content:space-between;align-items:flex-end;">
      <div style="max-width:640px;">
        <div style="font-size:15px;font-weight:700;color:#99f6e4;letter-spacing:0.06em;text-transform:uppercase;margin-bottom:16px;">HİKÂYE &amp; DÖNÜŞÜM</div>
        <div style="font-size:52px;font-weight:600;line-height:1.08;letter-spacing:-0.025em;">
          Markanızın Hikâyesini Satışa Dönüştüren Mimari
        </div>
      </div>
      <div style="padding:14px 28px;border-radius:999px;background:#ffffff;color:#042f2e;font-size:17px;font-weight:700;">
        Portfolyoyu İncele
      </div>
    </div>

    <!-- Bottom Row Right: Summer Homes Screen -->
    <div style="position:absolute;left:2050px;top:1480px;width:630px;height:520px;border-radius:26px;overflow:hidden;
      background:#0f172a;border:1px solid rgba(255,255,255,0.12);">
      <img src="data:image/jpeg;base64,${webSummer}" style="width:100%;height:100%;object-fit:cover;object-position:top center;"/>
    </div>
  </div>
`, true);

// 2. Center Screen Isometric Stack + Callout Overlay (1200 x 820 transparent)
await renderPng('center-iso-overlay.png', 1200, 820, `
  <div style="position:relative;width:1200px;height:820px;color:#ffffff;">
    <!-- Left info card inside center screen -->
    <div style="position:absolute;left:64px;top:375px;width:300px;padding:24px 26px;border-radius:18px;
      background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.12);backdrop-filter:blur(8px);">
      <div style="font-size:13px;font-weight:700;color:#5eead4;letter-spacing:0.06em;text-transform:uppercase;margin-bottom:10px;">KREATİF METODOLOJİ</div>
      <div style="font-size:18px;font-weight:500;line-height:1.45;color:rgba(255,255,255,0.9);">
        Veri içgörülerini yüksek dönüşümlü görsel kimlik ve reklam kreatiflerine dönüştürüyoruz.
      </div>
      <div style="margin-top:16px;height:3px;width:100%;background:rgba(255,255,255,0.12);border-radius:4px;overflow:hidden;">
        <div style="width:74%;height:100%;background:#34d399;"></div>
      </div>
    </div>

    <!-- Isometric 4-Layer Stack in lower-center -->
    <svg viewBox="0 0 420 340" style="position:absolute;left:390px;top:385px;width:420px;height:340px;filter:drop-shadow(0 20px 36px rgba(0,0,0,0.55));">
      <!-- Layer 4 (Bottom - Violet Strategy) -->
      <polygon points="210,296 78,224 210,152 342,224" fill="#7c3aed" opacity="0.92"/>
      <polygon points="78,224 210,296 210,312 78,240" fill="#5b21b6"/>
      <polygon points="342,224 210,296 210,312 342,240" fill="#6d28d9"/>
      <!-- Layer 3 (Cobalt UX & Funnel) -->
      <polygon points="210,254 78,182 210,110 342,182" fill="#2563eb" opacity="0.94"/>
      <polygon points="78,182 210,254 210,268 78,196" fill="#1d4ed8"/>
      <polygon points="342,182 210,254 210,268 342,196" fill="#1e40af"/>
      <!-- Layer 2 (Emerald Conversion Copy) -->
      <polygon points="210,212 78,140 210,68 342,140" fill="#10b981" opacity="0.95"/>
      <polygon points="78,140 210,212 210,226 78,154" fill="#059669"/>
      <polygon points="342,140 210,212 210,226 342,154" fill="#047857"/>
      <!-- Layer 1 (Top - Warm Amber Bold Idea) -->
      <polygon points="210,170 78,98 210,26 342,98" fill="#f59e0b"/>
      <polygon points="78,98 210,170 210,184 78,112" fill="#d97706"/>
      <polygon points="342,98 210,170 210,184 342,112" fill="#b45309"/>
      <!-- Crisp radial spark lines on top plate -->
      <g stroke="#ffffff" stroke-width="2.5" stroke-linecap="round" opacity="0.92">
        <line x1="210" y1="62" x2="210" y2="134"/>
        <line x1="146" y1="98" x2="274" y2="98"/>
        <line x1="166" y1="74" x2="254" y2="122"/>
        <line x1="254" y1="74" x2="166" y2="122"/>
      </g>
      <circle cx="210" cy="98" r="10" fill="#ffffff"/>
    </svg>
  </div>
`, true);

// 3. Decoded Kinetic Headlines (1200 x 260 transparent)
await renderPng('headline-1.png', 1200, 260, `
  <div style="width:1200px;height:260px;display:flex;align-items:center;justify-content:center;text-align:center;">
    <div style="font-size:74px;font-weight:500;line-height:1.08;letter-spacing:-0.03em;color:#ffffff;text-shadow:0 8px 36px rgba(0,0,0,0.65);">
      Veriden Doğan<br>Cesur Fikir
    </div>
  </div>
`, true);

await renderPng('headline-2.png', 1200, 260, `
  <div style="width:1200px;height:260px;display:flex;align-items:center;justify-content:center;text-align:center;">
    <div style="font-size:56px;font-weight:500;line-height:1.12;letter-spacing:-0.025em;color:#ffffff;text-shadow:0 8px 32px rgba(0,0,0,0.65);">
      Stratejiyle Güçlenen<br>Kreatif Mimari
    </div>
  </div>
`, true);

// 4. Beat 3 Brand Reveal Assets (1020 x 788)
await renderPng('brand-icon.png', 1020, 788, `
  <div style="width:1020px;height:788px;display:flex;align-items:center;justify-content:center;">
    <svg viewBox="0 0 185 210" style="width:230px;height:auto;filter:drop-shadow(0 20px 50px rgba(118,1,255,0.45));">
      <defs>
        <linearGradient id="rg" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stop-color="#9333ea"/>
          <stop offset="50%" stop-color="#7601ff"/>
          <stop offset="100%" stop-color="#2563eb"/>
        </linearGradient>
      </defs>
      <path d="${rIconPath}" fill="url(#rg)"/>
    </svg>
  </div>
`, true);

await renderPng('brand-lockup.png', 1020, 788, `
  <div style="width:1020px;height:788px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:28px;">
    <svg viewBox="0 0 819.98 200" style="width:500px;height:auto;filter:drop-shadow(0 20px 50px rgba(37,99,235,0.38));">
      <defs>
        <linearGradient id="rg2" x1="0" y1="0" x2="1" y2="0.6">
          <stop offset="0%" stop-color="#a855f7"/>
          <stop offset="45%" stop-color="#7601ff"/>
          <stop offset="100%" stop-color="#3b82f6"/>
        </linearGradient>
      </defs>
      ${fullPaths.map(d => `<path d="${d}" fill="url(#rg2)"/>`).join('')}
    </svg>
    <div style="font-size:24px;font-weight:500;letter-spacing:0.06em;text-transform:uppercase;color:#94a3b8;">
      Kreatif &amp; Performans Stüdyosu
    </div>
  </div>
`, true);

// 5. Beat 4 — 9 Real Roasist Client Creative Ad Cards (560 x 360 RGBA)
const CARDS = [
  {
    slug: 'card-01.png', bg: '#7601ff', text: '#ffffff', tag: 'LÜKS KONAKLAMA', metric: '7.4x ROAS',
    title: 'Akdeniz’de Butik Tatil Deneyimi', brand: 'Livaneli Hotels', img: webLivaneli
  },
  {
    slug: 'card-02.png', bg: '#1d4ed8', text: '#ffffff', tag: 'GAYRİMENKUL LANSMAN', metric: '+186% Talep',
    title: 'Kıbrıs’ta Prestijli Yaşam Projesi', brand: 'Cordelia Cyprus', img: webCordelia
  },
  {
    slug: 'card-03.png', bg: '#0f172a', text: '#ffffff', tag: 'GLOBAL YATIRIM', metric: '6.2x ROAS',
    title: 'Avrupa’dan Doğrudan Yatırımcı Hunisi', brand: 'Summer Homes', img: webSummer
  },
  {
    slug: 'card-04.png', bg: '#6d28d9', text: '#ffffff', tag: 'YETENEK KAZANIMI', metric: '-%44 Başvuru Maliyeti',
    title: 'Doğru Adaya Veriyle Ulaşın', brand: 'TalentFinder', img: webTalent
  },
  {
    slug: 'card-05.png', bg: '#2563eb', text: '#ffffff', tag: 'SAĞLIK TURİZMİ', metric: '+210% Lead',
    title: 'Uluslararası Hasta Kazanım Kreatifi', brand: 'Doctor Bircan', img: refBircan
  },
  {
    slug: 'card-06.png', bg: '#111827', text: '#ffffff', tag: 'B2B PLATFORM', metric: '%5.4 CTR',
    title: 'İK Karar Vericilerine Özel Kanca', brand: 'HRShortlist', img: webHr
  },
  {
    slug: 'card-07.png', bg: '#4f46e5', text: '#ffffff', tag: 'EĞİTİM KAMPANYASI', metric: '4.9x Kayıt',
    title: 'Erken Kayıt Dönemi Kreatif Serisi', brand: 'Düş Bahçesi', img: refDus
  },
  {
    slug: 'card-08.png', bg: '#0f172a', text: '#ffffff', tag: 'KLİNİK BÜYÜME', metric: '6.8x ROAS',
    title: 'Güven Odaklı Video & Web Kurgusu', brand: 'Center of Surgeons', img: refSurgeons
  },
  {
    slug: 'card-09.png', bg: '#7c3aed', text: '#ffffff', tag: 'İK & İŞVEREN MARKASI', metric: '+165% Başvuru',
    title: 'Almanca Bilen Yetenek Kampanyası', brand: 'Autarke', img: refAutarke
  },
];

for (const c of CARDS) {
  await renderPng(c.slug, 580, 380, `
    <div style="width:580px;height:380px;padding:18px;">
      <div style="width:100%;height:100%;border-radius:20px;overflow:hidden;background:${c.bg};color:${c.text};
        display:grid;grid-template-columns:1.05fr 0.95fr;border:3px solid #ffffff;
        box-shadow:0 18px 38px rgba(15,23,42,0.22);">
        <div style="padding:26px 24px 24px 28px;display:flex;flex-direction:column;justify-content:space-between;">
          <div>
            <span style="display:inline-block;padding:5px 11px;border-radius:999px;background:rgba(255,255,255,0.18);
              font-size:11px;font-weight:700;letter-spacing:0.06em;">${c.tag}</span>
            <div style="font-size:25px;font-weight:700;line-height:1.15;letter-spacing:-0.02em;margin-top:16px;">
              ${c.title}
            </div>
          </div>
          <div style="display:flex;align-items:center;justify-content:space-between;gap:8px;">
            <span style="font-size:14px;font-weight:600;opacity:0.88;">${c.brand}</span>
            <span style="padding:6px 12px;border-radius:8px;background:#ffffff;color:#0f172a;font-size:13px;font-weight:700;">
              ${c.metric}
            </span>
          </div>
        </div>
        <div style="position:relative;height:100%;overflow:hidden;background:#0f172a;">
          <img src="data:image/jpeg;base64,${c.img}" style="width:100%;height:100%;object-fit:cover;object-position:center top;"/>
        </div>
      </div>
    </div>
  `, true);
}

ws.close();
chrome.kill();
process.exit(0);
