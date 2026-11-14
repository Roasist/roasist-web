import fs from 'node:fs';
import path from 'node:path';
import { spawn } from 'node:child_process';

const ROOT = '/home/antigravity/Roasist/roasist-web';
const OUT_DIR = path.join(ROOT, 'scripts/assets/methodology/s3');
fs.mkdirSync(OUT_DIR, { recursive: true });

const logoSvgRaw = fs.readFileSync(path.join(ROOT, 'public/roasist-logo.svg'), 'utf8');
const fullPaths = [...logoSvgRaw.matchAll(/<path class="cls-1" d="([^"]+)"><\/path>/g)].map(m => m[1]);

const bin = fs.existsSync('/usr/bin/chromium') ? '/usr/bin/chromium' : '/usr/bin/google-chrome';
const dbgPort = 9892;
const chrome = spawn(bin, [
  '--headless=new', '--no-sandbox', '--disable-gpu', '--hide-scrollbars',
  `--proxy-server=${process.env.HTTPS_PROXY || process.env.HTTP_PROXY}`,
  '--ignore-certificate-errors',
  `--user-data-dir=/tmp/chr-m3-${Date.now()}`, `--remote-debugging-port=${dbgPort}`,
  '--window-size=2000,1600', 'about:blank'
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
    color: transparent ? { r: 0, g: 0, b: 0, a: 0 } : { r: 9, g: 9, b: 13, a: 1 }
  });
  const doc = `<!doctype html><html><head><meta charset="utf-8">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600;9..40,700&display=swap" rel="stylesheet">
    <style>
      * { box-sizing: border-box; margin: 0; padding: 0; }
      body {
        width: ${width}px; height: ${height}px; overflow: hidden;
        background: ${transparent ? 'transparent' : '#09090d'};
        font-family: 'DM Sans', sans-serif;
        font-variant-numeric: tabular-nums;
        -webkit-font-smoothing: antialiased;
        color: #f8fafc;
      }
      .card {
        background: #13131a;
        border: 1px solid rgba(255,255,255,0.09);
        border-radius: 18px;
      }
    </style></head><body>${bodyHtml}</body></html>`;
  await send('Page.setDocumentContent', { frameId, html: doc });
  await send('Runtime.evaluate', { expression: 'document.fonts.ready', awaitPromise: true });
  await sleep(160);
  const shot = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(OUT_DIR, name), Buffer.from(shot.data, 'base64'));
  console.log('Rendered', name);
}

const checkIcon = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>`;
const pulseDot = `<span style="display:inline-block;width:9px;height:9px;border-radius:50%;background:#10b981;box-shadow:0 0 12px #10b981;"></span>`;
const purpleDot = `<span style="display:inline-block;width:9px;height:9px;border-radius:50%;background:#7601ff;box-shadow:0 0 12px #7601ff;"></span>`;

// 1. Agile Sprint Workspace Window (1680 x 1140 RGBA)
// Note: Slot 2 in Column 2 (x=592, y=566, w=496, h=188) and Slot 2 in Column 3 (x=1120, y=566, w=496, h=188)
// are left empty/dashed so Python animates the live Sprint Card gliding from Active Sprint -> Completed!
await renderPng('sprint-workspace.png', 1680, 1140, `
  <div style="width:1680px;height:1140px;padding:30px;">
    <div style="width:100%;height:100%;border-radius:30px;background:#0d0d13;border:1.5px solid rgba(255,255,255,0.12);
      box-shadow:0 40px 100px rgba(0,0,0,0.72);padding:40px 46px;display:flex;flex-direction:column;gap:30px;">

      <!-- Top Header Bar -->
      <div style="display:flex;align-items:center;justify-content:space-between;padding-bottom:26px;border-bottom:1px solid rgba(255,255,255,0.08);">
        <div style="display:flex;align-items:center;gap:22px;">
          <svg viewBox="0 0 819.98 200" style="height:34px;width:auto;">
            ${fullPaths.map(d => `<path d="${d}" fill="#7601ff"/>`).join('')}
          </svg>
          <span style="width:1px;height:24px;background:rgba(255,255,255,0.14);"></span>
          <span style="font-size:19px;font-weight:500;color:#cbd5e1;letter-spacing:-0.01em;">Şeffaf Süreç &amp; Çevik Sprint Yönetimi</span>
        </div>
        <div style="display:flex;align-items:center;gap:16px;">
          <div style="display:flex;align-items:center;gap:10px;padding:10px 18px;border-radius:999px;background:rgba(16,185,129,0.10);border:1px solid rgba(16,185,129,0.28);font-size:15px;font-weight:600;color:#6ee7b7;">
            ${pulseDot}
            <span>Canlı Müşteri Paneli Aktif</span>
          </div>
          <div style="padding:10px 20px;border-radius:999px;background:#7601ff;color:#ffffff;font-size:15px;font-weight:600;">
            Sprint #04 · Hafta 6
          </div>
        </div>
      </div>

      <!-- 4-Stage Sprint Progress Track (Python animates the #7601ff progress fill along y=224!) -->
      <div class="card" style="padding:26px 34px;display:flex;flex-direction:column;gap:20px;background:#12121a;">
        <div style="display:flex;justify-content:space-between;align-items:center;">
          <div style="display:flex;gap:8px;align-items:center;font-size:15px;font-weight:600;color:#a1a1aa;text-transform:uppercase;letter-spacing:0.05em;">
            <span>PROJE İVME HATTI</span>
          </div>
          <div style="font-size:16px;font-weight:600;color:#e2e8f0;">
            Teslimat Zamanlaması: <span style="color:#10b981;">%100 Planlanan Takvimde</span>
          </div>
        </div>
        <!-- Track labels -->
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:20px;padding-top:18px;">
          <div>
            <div style="font-size:13px;font-weight:700;color:#7601ff;letter-spacing:0.05em;">01 · GÜN 1–7</div>
            <div style="font-size:18px;font-weight:600;margin-top:4px;">Veri &amp; Takip Kurulumu</div>
          </div>
          <div>
            <div style="font-size:13px;font-weight:700;color:#7601ff;letter-spacing:0.05em;">02 · HAFTA 2–3</div>
            <div style="font-size:18px;font-weight:600;margin-top:4px;">Kreatif &amp; Huni Üretimi</div>
          </div>
          <div>
            <div style="font-size:13px;font-weight:700;color:#e2e8f0;letter-spacing:0.05em;">03 · HAFTA 4–6</div>
            <div style="font-size:18px;font-weight:600;margin-top:4px;">Hızlı A/B Test &amp; CRO</div>
          </div>
          <div>
            <div style="font-size:13px;font-weight:700;color:#94a3b8;letter-spacing:0.05em;">04 · SÜREKLİ İVME</div>
            <div style="font-size:18px;font-weight:600;margin-top:4px;color:#cbd5e1;">Kârlı Ölçeklendirme</div>
          </div>
        </div>
      </div>

      <!-- 3-Column Agile Kanban Sprint Board -->
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:26px;flex:1;">

        <!-- Column 1: Planlanan Sprint -->
        <div style="background:#111118;border:1px solid rgba(255,255,255,0.07);border-radius:22px;padding:24px;display:flex;flex-direction:column;gap:18px;">
          <div style="display:flex;justify-content:space-between;align-items:center;padding-bottom:8px;">
            <span style="font-size:16px;font-weight:600;color:#cbd5e1;">Sıradaki Adımlar</span>
            <span style="padding:4px 12px;border-radius:999px;background:rgba(255,255,255,0.07);font-size:13px;font-weight:600;color:#94a3b8;">2 Görev</span>
          </div>

          <div class="card" style="padding:22px;display:flex;flex-direction:column;gap:14px;">
            <div style="display:flex;justify-content:space-between;align-items:center;">
              <span style="padding:5px 12px;border-radius:8px;background:rgba(118,1,255,0.16);color:#c4b5fd;font-size:12px;font-weight:700;letter-spacing:0.04em;">YENİ PAZAR</span>
              <span style="font-size:13px;color:#94a3b8;">Sprint #05</span>
            </div>
            <div style="font-size:20px;font-weight:600;line-height:1.28;letter-spacing:-0.015em;">
              Almanya &amp; İngiltere Çok Dilli Kampanya Genişlemesi
            </div>
            <div style="display:flex;justify-content:space-between;align-items:center;padding-top:6px;font-size:14px;color:#94a3b8;">
              <span>Medya Planlama</span>
              <span style="color:#e2e8f0;font-weight:600;">Hazır %85</span>
            </div>
          </div>

          <div class="card" style="padding:22px;display:flex;flex-direction:column;gap:14px;">
            <div style="display:flex;justify-content:space-between;align-items:center;">
              <span style="padding:5px 12px;border-radius:8px;background:rgba(255,255,255,0.08);color:#cbd5e1;font-size:12px;font-weight:700;letter-spacing:0.04em;">AEO &amp; SEO</span>
              <span style="font-size:13px;color:#94a3b8;">Sprint #05</span>
            </div>
            <div style="font-size:20px;font-weight:600;line-height:1.28;letter-spacing:-0.015em;">
              Yapay Zeka Arama Görünürlük &amp; İçerik Kümeleri
            </div>
            <div style="display:flex;justify-content:space-between;align-items:center;padding-top:6px;font-size:14px;color:#94a3b8;">
              <span>Organik Büyüme</span>
              <span style="color:#e2e8f0;font-weight:600;">Planlandı</span>
            </div>
          </div>
        </div>

        <!-- Column 2: Aktif Sprint #04 -->
        <div style="background:#111118;border:1px solid rgba(118,1,255,0.28);border-radius:22px;padding:24px;display:flex;flex-direction:column;gap:18px;">
          <div style="display:flex;justify-content:space-between;align-items:center;padding-bottom:8px;">
            <div style="display:flex;align-items:center;gap:10px;">
              ${purpleDot}
              <span style="font-size:16px;font-weight:600;color:#ffffff;">Aktif Sprint #04</span>
            </div>
            <span style="padding:4px 12px;border-radius:999px;background:rgba(118,1,255,0.20);font-size:13px;font-weight:700;color:#d8b4fe;">Devam Eden</span>
          </div>

          <!-- Placeholder slot where the animated card starts! -->
          <div style="height:192px;border-radius:18px;border:1.5px dashed rgba(118,1,255,0.28);background:rgba(118,1,255,0.04);
            display:flex;align-items:center;justify-content:center;color:rgba(216,180,254,0.45);font-size:15px;font-weight:500;">
            Canlı Yayına Aktarıldı
          </div>

          <div class="card" style="padding:22px;display:flex;flex-direction:column;gap:14px;">
            <div style="display:flex;justify-content:space-between;align-items:center;">
              <span style="padding:5px 12px;border-radius:8px;background:rgba(118,1,255,0.18);color:#d8b4fe;font-size:12px;font-weight:700;letter-spacing:0.04em;">KREATİF TEST</span>
              <span style="font-size:13px;color:#c4b5fd;font-weight:600;">Canlı Test</span>
            </div>
            <div style="font-size:20px;font-weight:600;line-height:1.28;letter-spacing:-0.015em;">
              Video Kanca A/B Varyasyonları (İlk 3 Saniye Kurgusu)
            </div>
            <div style="width:100%;height:6px;border-radius:999px;background:rgba(255,255,255,0.08);overflow:hidden;margin-top:4px;">
              <div style="width:78%;height:100%;background:#7601ff;border-radius:999px;"></div>
            </div>
          </div>
        </div>

        <!-- Column 3: Tamamlandı & Yayında -->
        <div style="background:#111118;border:1px solid rgba(16,185,129,0.22);border-radius:22px;padding:24px;display:flex;flex-direction:column;gap:18px;">
          <div style="display:flex;justify-content:space-between;align-items:center;padding-bottom:8px;">
            <div style="display:flex;align-items:center;gap:10px;">
              ${pulseDot}
              <span style="font-size:16px;font-weight:600;color:#ffffff;">Tamamlandı &amp; Yayında</span>
            </div>
            <span style="padding:4px 12px;border-radius:999px;background:rgba(16,185,129,0.14);font-size:13px;font-weight:700;color:#6ee7b7;">Doğrulandı</span>
          </div>

          <div class="card" style="padding:22px;display:flex;flex-direction:column;gap:14px;border-color:rgba(16,185,129,0.22);">
            <div style="display:flex;justify-content:space-between;align-items:center;">
              <span style="padding:5px 12px;border-radius:8px;background:rgba(16,185,129,0.14);color:#6ee7b7;font-size:12px;font-weight:700;">VERİ ALTYAPISI</span>
              <span style="display:flex;align-items:center;gap:6px;font-size:13px;font-weight:700;color:#6ee7b7;">${checkIcon} Aktif</span>
            </div>
            <div style="font-size:20px;font-weight:600;line-height:1.28;letter-spacing:-0.015em;">
              GA4 + Server-Side GTM &amp; CRM Dönüşüm Eşleşmesi
            </div>
            <div style="display:flex;justify-content:space-between;align-items:center;padding-top:4px;font-size:14px;color:#94a3b8;">
              <span>Veri Doğruluğu</span>
              <span style="color:#6ee7b7;font-weight:700;">%98.4 Eşleşme</span>
            </div>
          </div>

          <!-- Destination slot where the animated Sprint Card lands! -->
          <div style="height:192px;border-radius:18px;border:1.5px dashed rgba(255,255,255,0.08);background:rgba(255,255,255,0.015);"></div>
        </div>

      </div>
    </div>
  </div>
`, true);

// 2. Animated Moving Sprint Card (480 x 210 RGBA) — State A (Active #7601FF) & State B (Completed Emerald)
await renderPng('moving-card-active.png', 510, 224, `
  <div style="width:510px;height:224px;padding:16px;">
    <div style="width:100%;height:100%;border-radius:18px;background:#191627;border:2px solid #7601ff;
      box-shadow:0 22px 48px rgba(0,0,0,0.65), 0 0 28px rgba(118,1,255,0.28);padding:22px;display:flex;flex-direction:column;justify-content:space-between;">
      <div style="display:flex;justify-content:space-between;align-items:center;">
        <span style="padding:5px 12px;border-radius:8px;background:#7601ff;color:#ffffff;font-size:12px;font-weight:700;letter-spacing:0.04em;">CRO &amp; PERFORMANS</span>
        <span style="font-size:13px;font-weight:600;color:#d8b4fe;">Yayına Alınıyor...</span>
      </div>
      <div style="font-size:20px;font-weight:600;line-height:1.26;letter-spacing:-0.015em;color:#ffffff;">
        Açılış Sayfası Hız &amp; Teklif Kurgusu Optimizasyonu
      </div>
      <div style="display:flex;justify-content:space-between;align-items:center;font-size:14px;color:#cbd5e1;">
        <span>Sprint #04 Teslimatı</span>
        <span style="font-weight:700;color:#ffffff;">+%38 Dönüşüm</span>
      </div>
    </div>
  </div>
`, true);

await renderPng('moving-card-done.png', 510, 224, `
  <div style="width:510px;height:224px;padding:16px;">
    <div style="width:100%;height:100%;border-radius:18px;background:#111d1a;border:2px solid #10b981;
      box-shadow:0 22px 48px rgba(0,0,0,0.65), 0 0 26px rgba(16,185,129,0.24);padding:22px;display:flex;flex-direction:column;justify-content:space-between;">
      <div style="display:flex;justify-content:space-between;align-items:center;">
        <span style="padding:5px 12px;border-radius:8px;background:rgba(16,185,129,0.20);color:#6ee7b7;font-size:12px;font-weight:700;letter-spacing:0.04em;">CRO &amp; PERFORMANS</span>
        <span style="display:flex;align-items:center;gap:6px;font-size:13px;font-weight:700;color:#6ee7b7;">${checkIcon} Yayında</span>
      </div>
      <div style="font-size:20px;font-weight:600;line-height:1.26;letter-spacing:-0.015em;color:#ffffff;">
        Açılış Sayfası Hız &amp; Teklif Kurgusu Optimizasyonu
      </div>
      <div style="display:flex;justify-content:space-between;align-items:center;font-size:14px;color:#cbd5e1;">
        <span>Sprint #04 Teslimatı</span>
        <span style="font-weight:700;color:#6ee7b7;">+%38 Dönüşüm Artışı</span>
      </div>
    </div>
  </div>
`, true);

// 3. Real-Time Data & Momentum Panel (1560 x 1060 RGBA) — Chart plot area left clean so Python draws 60fps live #7601FF spline!
await renderPng('realtime-cockpit.png', 1560, 1060, `
  <div style="width:1560px;height:1060px;padding:30px;">
    <div style="width:100%;height:100%;border-radius:30px;background:#0d0d13;border:1.5px solid rgba(255,255,255,0.12);
      box-shadow:0 40px 100px rgba(0,0,0,0.75);padding:42px 48px;display:flex;flex-direction:column;justify-content:space-between;">

      <!-- Header -->
      <div style="display:flex;justify-content:space-between;align-items:center;">
        <div style="display:flex;align-items:center;gap:20px;">
          <svg viewBox="0 0 819.98 200" style="height:32px;width:auto;">
            ${fullPaths.map(d => `<path d="${d}" fill="#7601ff"/>`).join('')}
          </svg>
          <span style="width:1px;height:24px;background:rgba(255,255,255,0.14);"></span>
          <span style="font-size:19px;font-weight:500;color:#cbd5e1;">Gerçek Zamanlı Performans &amp; İvme Paneli</span>
        </div>
        <div style="display:flex;align-items:center;gap:14px;">
          <span style="padding:9px 16px;border-radius:999px;background:rgba(255,255,255,0.06);font-size:14px;color:#cbd5e1;font-weight:500;">Google Ads · Meta · TikTok · GA4</span>
          <div style="display:flex;align-items:center;gap:9px;padding:9px 18px;border-radius:999px;background:rgba(16,185,129,0.12);border:1px solid rgba(16,185,129,0.3);font-size:14px;font-weight:700;color:#6ee7b7;">
            ${pulseDot} CANLI VERİ
          </div>
        </div>
      </div>

      <!-- Top KPI Strip -->
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:24px;margin-top:24px;">
        <div class="card" style="padding:24px 28px;border-color:rgba(118,1,255,0.35);background:linear-gradient(180deg,#171326 0%,#12121a 100%);">
          <div style="font-size:14px;font-weight:600;color:#a1a1aa;text-transform:uppercase;letter-spacing:0.05em;">BİRLEŞİK KÂRLILIK (ROAS)</div>
          <div style="display:flex;align-items:baseline;gap:14px;margin-top:10px;">
            <span style="font-size:52px;font-weight:700;letter-spacing:-0.03em;color:#ffffff;">6.4x</span>
            <span style="padding:5px 12px;border-radius:999px;background:rgba(118,1,255,0.24);color:#d8b4fe;font-size:15px;font-weight:700;">+106% İvme</span>
          </div>
        </div>

        <div class="card" style="padding:24px 28px;">
          <div style="font-size:14px;font-weight:600;color:#a1a1aa;text-transform:uppercase;letter-spacing:0.05em;">EDİNME MALİYETİ (CPA)</div>
          <div style="display:flex;align-items:baseline;gap:14px;margin-top:10px;">
            <span style="font-size:52px;font-weight:700;letter-spacing:-0.03em;color:#ffffff;">-%38</span>
            <span style="padding:5px 12px;border-radius:999px;background:rgba(16,185,129,0.15);color:#6ee7b7;font-size:15px;font-weight:700;">Optimize</span>
          </div>
        </div>

        <div class="card" style="padding:24px 28px;">
          <div style="font-size:14px;font-weight:600;color:#a1a1aa;text-transform:uppercase;letter-spacing:0.05em;">SPRINT TESLİMAT HIZI</div>
          <div style="display:flex;align-items:baseline;gap:14px;margin-top:10px;">
            <span style="font-size:52px;font-weight:700;letter-spacing:-0.03em;color:#ffffff;">%98.2</span>
            <span style="font-size:15px;font-weight:600;color:#94a3b8;">Haftalık Hedef Uyumu</span>
          </div>
        </div>
      </div>

      <!-- Main Chart Container (Plot region: x=120..1440, y=430..885 in 1560x1060 coordinates) -->
      <div class="card" style="flex:1;margin-top:24px;padding:28px 34px;display:flex;flex-direction:column;justify-content:space-between;background:#101017;">
        <div style="display:flex;justify-content:space-between;align-items:center;">
          <div>
            <div style="font-size:21px;font-weight:600;letter-spacing:-0.015em;">Sprint Bazlı Büyüme &amp; ROAS İvmesi</div>
            <div style="font-size:15px;color:#94a3b8;margin-top:4px;">Her iki haftalık sprint sonunda doğrulanan kümülatif reklam verimliliği</div>
          </div>
          <div style="display:flex;align-items:center;gap:20px;font-size:14px;color:#cbd5e1;">
            <span style="display:flex;align-items:center;gap:8px;"><span style="width:12px;height:12px;border-radius:3px;background:#7601ff;display:inline-block;"></span> Gerçekleşen ROAS</span>
            <span style="display:flex;align-items:center;gap:8px;"><span style="width:12px;height:3px;background:#475569;display:inline-block;"></span> Başlangıç Bazı</span>
          </div>
        </div>

        <!-- Subtle horizontal gridlines -->
        <div style="display:flex;flex-direction:column;justify-content:space-between;height:360px;padding:16px 0;border-bottom:1px solid rgba(255,255,255,0.08);">
          <div style="display:flex;align-items:center;gap:16px;"><span style="width:44px;font-size:13px;color:#64748b;">7.0x</span><div style="flex:1;height:1px;background:rgba(255,255,255,0.05);"></div></div>
          <div style="display:flex;align-items:center;gap:16px;"><span style="width:44px;font-size:13px;color:#64748b;">5.5x</span><div style="flex:1;height:1px;background:rgba(255,255,255,0.05);"></div></div>
          <div style="display:flex;align-items:center;gap:16px;"><span style="width:44px;font-size:13px;color:#64748b;">4.0x</span><div style="flex:1;height:1px;background:rgba(255,255,255,0.05);"></div></div>
          <div style="display:flex;align-items:center;gap:16px;"><span style="width:44px;font-size:13px;color:#64748b;">2.5x</span><div style="flex:1;height:1px;border-top:1px dashed rgba(148,163,184,0.22);"></div></div>
        </div>

        <!-- X-axis Sprint Labels -->
        <div style="display:grid;grid-template-columns:repeat(6,1fr);padding-left:60px;padding-top:12px;font-size:14px;font-weight:600;color:#94a3b8;">
          <span>Sprint 01 · Kurulum</span>
          <span>Sprint 02 · Kreatif</span>
          <span>Sprint 03 · CRO</span>
          <span>Sprint 04 · Ölçek</span>
          <span>Sprint 05 · Otomasyon</span>
          <span style="color:#d8b4fe;">Sprint 06 · 6.4x ROAS</span>
        </div>
      </div>

    </div>
  </div>
`, true);

// 4. Floating Live Tooltip Badge (270 x 96 RGBA) that rides the tip of the live 60fps #7601ff growth curve!
await renderPng('curve-live-badge.png', 290, 108, `
  <div style="width:290px;height:108px;padding:12px;">
    <div style="width:100%;height:100%;border-radius:16px;background:#7601ff;color:#ffffff;
      box-shadow:0 16px 36px rgba(118,1,255,0.48);border:1.5px solid rgba(255,255,255,0.35);
      padding:14px 20px;display:flex;align-items:center;justify-content:space-between;">
      <div>
        <div style="font-size:11px;font-weight:700;letter-spacing:0.06em;opacity:0.88;text-transform:uppercase;">CANLI İVME</div>
        <div style="font-size:26px;font-weight:700;letter-spacing:-0.02em;margin-top:2px;">6.4x ROAS</div>
      </div>
      <div style="padding:6px 11px;border-radius:10px;background:rgba(255,255,255,0.18);font-size:14px;font-weight:700;">
        +106%
      </div>
    </div>
  </div>
`, true);

ws.close();
chrome.kill();
process.exit(0);
