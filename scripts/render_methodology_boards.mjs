import fs from 'node:fs';
import path from 'node:path';
import { spawn } from 'node:child_process';

const ROOT = '/home/antigravity/Roasist/roasist-web';
const OUT_DIR = path.join(ROOT, 'scripts/assets/methodology');
fs.mkdirSync(OUT_DIR, { recursive: true });

const roasistWhiteSvg = fs.readFileSync(path.join(ROOT, 'public/roasist-logo.svg'), 'utf8')
  .replace('.cls-1{fill:#7601ff;}', '.cls-1{fill:#ffffff;}')
  .replace(/<\?xml[^>]*\?>/, '')
  .replace('<svg ', '<svg style="width:210px;height:auto;display:block;" ');

const b64 = slug => fs.readFileSync(path.join(ROOT, `scripts/assets/web-screens/${slug}.jpg`)).toString('base64');
const imgTalent = b64('talentfinder');
const imgSummer = b64('summerhomes');
const imgHr = b64('hrshortlist');
const imgCordelia = b64('cordelia');

const html = `<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600;9..40,700&display=swap" rel="stylesheet">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 3400px;
    height: 2600px;
    overflow: hidden;
    background-color: #f5e6d0;
    background-image: radial-gradient(rgba(24, 24, 27, 0.11) 1.5px, transparent 1.5px);
    background-size: 36px 36px;
    font-family: 'DM Sans', sans-serif;
    font-variant-numeric: tabular-nums;
    color: #141417;
    position: relative;
  }
  .frame {
    position: absolute;
    border: 2px solid #18181b;
    background: #ffffff;
    overflow: hidden;
  }
  .frame-bar {
    height: 44px;
    border-bottom: 1.5px solid rgba(24,24,27,0.12);
    padding: 0 22px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 14px;
    font-weight: 600;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: #52525b;
    background: #fafafa;
  }
  .sticky {
    position: absolute;
    background: #fde49b;
    padding: 30px 34px;
    box-shadow: 0 18px 38px rgba(24, 24, 27, 0.12), 0 2px 6px rgba(24, 24, 27, 0.06);
    font-size: 25px;
    font-weight: 500;
    line-height: 1.34;
    letter-spacing: -0.02em;
    color: #1c1917;
    z-index: 20;
  }
  .pill {
    display: inline-flex;
    align-items: center;
    padding: 6px 14px;
    border-radius: 999px;
    font-size: 14px;
    font-weight: 600;
    letter-spacing: -0.01em;
  }
  .connector {
    position: absolute;
    inset: 0;
    pointer-events: none;
    z-index: 5;
  }
</style>
</head>
<body>

  <svg class="connector" width="3400" height="2600" viewBox="0 0 3400 2600" fill="none">
    <path d="M 980 480 C 1010 480, 1005 460, 1030 460" stroke="#18181b" stroke-width="2.5" stroke-dasharray="7 7"/>
    <path d="M 1610 460 C 1640 460, 1640 500, 1670 500" stroke="#18181b" stroke-width="2.5"/>
    <path d="M 2430 510 L 2480 510" stroke="#18181b" stroke-width="2.5"/>
    <path d="M 2050 1270 L 2050 1340" stroke="#18181b" stroke-width="2.5" stroke-dasharray="7 7"/>
    <path d="M 1660 1550 L 1600 1550" stroke="#18181b" stroke-width="2.5" stroke-dasharray="7 7"/>
  </svg>

  <!-- ==================== CLUSTER 1 (TOP-LEFT) ==================== -->
  <div class="frame" style="left:280px;top:240px;width:700px;height:490px;">
    <div class="frame-bar">
      <span>01 · Birim Ekonomisi &amp; ROAS Mimarisi</span>
      <span style="color:#16a34a;">DOĞRULANDI</span>
    </div>
    <div style="padding:34px 40px;">
      <div style="font-size:34px;font-weight:700;letter-spacing:-0.03em;margin-bottom:26px;">Kârlılık Odaklı Büyüme Modeli</div>
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-bottom:30px;">
        <div style="background:#f8fafc;border:1px solid #e2e8f0;padding:20px 22px;border-radius:12px;">
          <div style="font-size:15px;color:#64748b;margin-bottom:6px;">Hedef ROAS</div>
          <div style="font-size:46px;font-weight:700;letter-spacing:-0.03em;color:#0f172a;">6.4x</div>
          <div style="font-size:14px;font-weight:600;color:#16a34a;margin-top:4px;">+142% Ölçek</div>
        </div>
        <div style="background:#f8fafc;border:1px solid #e2e8f0;padding:20px 22px;border-radius:12px;">
          <div style="font-size:15px;color:#64748b;margin-bottom:6px;">Başabaş ROAS</div>
          <div style="font-size:46px;font-weight:700;letter-spacing:-0.03em;color:#0f172a;">2.3x</div>
          <div style="font-size:14px;font-weight:500;color:#64748b;margin-top:4px;">Alt Sınır</div>
        </div>
        <div style="background:#f8fafc;border:1px solid #e2e8f0;padding:20px 22px;border-radius:12px;">
          <div style="font-size:15px;color:#64748b;margin-bottom:6px;">LTV / CAC</div>
          <div style="font-size:46px;font-weight:700;letter-spacing:-0.03em;color:#0f172a;">4.8x</div>
          <div style="font-size:14px;font-weight:500;color:#64748b;margin-top:4px;">12 Aylık Değer</div>
        </div>
      </div>
      <div style="font-size:15px;font-weight:600;color:#475569;margin-bottom:10px;display:flex;justify-content:space-between;">
        <span>Gelir Dağılımı &amp; Net Katkı Payı</span>
        <span>Brüt Marj %62.0</span>
      </div>
      <div style="height:24px;width:100%;background:#f1f5f9;border-radius:8px;overflow:hidden;display:flex;">
        <div style="width:46.4%;background:#0f172a;"></div>
        <div style="width:15.6%;background:#7601ff;"></div>
        <div style="width:38.0%;background:#cbd5e1;"></div>
      </div>
      <div style="display:flex;gap:22px;margin-top:12px;font-size:13px;color:#475569;font-weight:500;">
        <span><b style="color:#0f172a;">■ %46.4</b> Net Kâr Katkısı</span>
        <span><b style="color:#7601ff;">■ %15.6</b> Reklam Yatırımı</span>
      </div>
    </div>
  </div>

  <div class="frame" style="left:1030px;top:240px;width:580px;height:460px;background:#1424e8;color:#ffffff;padding:42px 44px;display:flex;flex-direction:column;justify-content:space-between;">
    <div style="display:flex;justify-content:space-between;align-items:center;">
      ${roasistWhiteSvg}
      <span class="pill" style="background:rgba(255,255,255,0.16);color:#fff;">STRATEJİ FAZI</span>
    </div>
    <div>
      <div style="font-size:56px;font-weight:700;line-height:1.06;letter-spacing:-0.035em;margin-bottom:18px;">
        Veri olmadan<br>tek kuruş bütçe<br>harcanmaz.
      </div>
      <div style="font-size:19px;color:rgba(255,255,255,0.84);line-height:1.42;">
        Pazar hacmi, rakip açıkları ve birim ekonomisi doğrulanmadan kampanya başlatılmaz.
      </div>
    </div>
  </div>

  <div class="frame" style="left:320px;top:810px;width:760px;height:450px;">
    <div class="frame-bar">
      <span>Rakip &amp; Değer Önerisi Analizi · B2B</span>
      <span>talentfinder.consulting</span>
    </div>
    <img src="data:image/jpeg;base64,${imgTalent}" style="width:100%;height:406px;object-fit:cover;object-position:top center;"/>
  </div>

  <div class="frame" style="left:1130px;top:760px;width:480px;height:500px;padding:34px;">
    <div style="font-size:14px;font-weight:700;letter-spacing:0.05em;color:#64748b;text-transform:uppercase;margin-bottom:12px;">RAKİP BOŞLUK MATRİSİ</div>
    <div style="font-size:28px;font-weight:700;letter-spacing:-0.025em;margin-bottom:22px;">Yüksek Niyetli Kelime Fırsatı</div>
    <svg width="410" height="295" viewBox="0 0 410 295">
      <rect x="25" y="10" width="365" height="240" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
      <line x1="208" y1="10" x2="208" y2="250" stroke="#cbd5e1" stroke-dasharray="5 5"/>
      <line x1="25" y1="130" x2="390" y2="130" stroke="#cbd5e1" stroke-dasharray="5 5"/>
      <rect x="214" y="16" width="170" height="108" rx="10" fill="rgba(118,1,255,0.09)" stroke="#7601ff" stroke-width="1.5"/>
      <circle cx="299" cy="64" r="16" fill="#7601ff"/>
      <text x="299" y="102" text-anchor="middle" font-size="13" font-weight="700" fill="#7601ff">ROASİST HEDEF ALANI</text>
      <circle cx="110" cy="185" r="11" fill="#94a3b8"/>
      <text x="110" y="212" text-anchor="middle" font-size="13" fill="#64748b">Rakip A</text>
      <circle cx="150" cy="95" r="13" fill="#94a3b8"/>
      <text x="150" y="120" text-anchor="middle" font-size="13" fill="#64748b">Rakip B</text>
      <circle cx="275" cy="190" r="12" fill="#94a3b8"/>
      <text x="275" y="216" text-anchor="middle" font-size="13" fill="#64748b">Rakip C</text>
      <text x="208" y="278" text-anchor="middle" font-size="13" font-weight="600" fill="#475569">Arama Niyeti &amp; Dönüşüm Potansiyeli →</text>
    </svg>
  </div>

  <!-- Sticky 1 positioned cleanly in the gap between A1/A3 without overlapping A2 text -->
  <div class="sticky" style="left:695px;top:668px;width:355px;">
    Birim ekonomisi doğrulandı: Başabaş ROAS 2.3x, ölçeklenme eşiği 5.0x+.
  </div>


  <!-- ==================== CLUSTER 2 (TOP-RIGHT) ==================== -->
  <div class="frame" style="left:1670px;top:240px;width:760px;height:500px;background:#111318;color:#ffffff;padding:42px;">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:26px;">
      <span style="font-size:14px;font-weight:700;letter-spacing:0.05em;color:#94a3b8;text-transform:uppercase;">02 · PAZAR &amp; KANAL HARİTASI</span>
      <span class="pill" style="background:rgba(16,185,129,0.16);color:#34d399;">TAM HUNİ KURGUSU</span>
    </div>
    <div style="font-size:36px;font-weight:700;letter-spacing:-0.03em;margin-bottom:32px;">Çok Kanallı Talep &amp; Arama Dağılımı</div>
    <div style="display:flex;flex-direction:column;gap:22px;">
      <div>
        <div style="display:flex;justify-content:space-between;font-size:18px;font-weight:500;margin-bottom:8px;">
          <span>Google Arama &amp; Alışveriş (Sıcak Talep)</span><span style="color:#a78bfa;font-weight:700;">%42</span>
        </div>
        <div style="height:14px;background:#27272a;border-radius:99px;"><div style="width:84%;height:100%;background:#8b5cf6;border-radius:99px;"></div></div>
      </div>
      <div>
        <div style="display:flex;justify-content:space-between;font-size:18px;font-weight:500;margin-bottom:8px;">
          <span>Meta &amp; Instagram Ads (Talep Yaratma &amp; Retargeting)</span><span style="color:#38bdf8;font-weight:700;">%31</span>
        </div>
        <div style="height:14px;background:#27272a;border-radius:99px;"><div style="width:62%;height:100%;background:#38bdf8;border-radius:99px;"></div></div>
      </div>
      <div>
        <div style="display:flex;justify-content:space-between;font-size:18px;font-weight:500;margin-bottom:8px;">
          <span>Organik SEO &amp; Yapay Zeka Aramaları (AEO / GEO)</span><span style="color:#34d399;font-weight:700;">%16</span>
        </div>
        <div style="height:14px;background:#27272a;border-radius:99px;"><div style="width:36%;height:100%;background:#34d399;border-radius:99px;"></div></div>
      </div>
      <div>
        <div style="display:flex;justify-content:space-between;font-size:18px;font-weight:500;margin-bottom:8px;">
          <span>TikTok, LinkedIn, Yandex &amp; Bing (Yeni Pazar Erişimi)</span><span style="color:#fbbf24;font-weight:700;">%11</span>
        </div>
        <div style="height:14px;background:#27272a;border-radius:99px;"><div style="width:25%;height:100%;background:#fbbf24;border-radius:99px;"></div></div>
      </div>
    </div>
  </div>

  <div class="frame" style="left:2480px;top:240px;width:620px;height:480px;background:#d2f800;color:#111315;padding:44px 46px;display:flex;flex-direction:column;justify-content:space-between;">
    <div style="display:flex;justify-content:space-between;align-items:center;">
      <span style="font-size:15px;font-weight:700;letter-spacing:0.05em;text-transform:uppercase;">ÖN DENETİM PROTOKOLÜ</span>
      <span style="background:#111315;color:#d2f800;padding:6px 14px;border-radius:8px;font-weight:700;font-size:15px;">42 KRİTER</span>
    </div>
    <div style="font-size:74px;font-weight:700;line-height:0.98;letter-spacing:-0.04em;">
      Önce Veri.<br>Sonra<br>Kampanya.
    </div>
    <div style="font-size:19px;font-weight:600;color:#27272a;">
      GA4, GTM Server-Side ve CRM sinyalleri doğrulanır.
    </div>
  </div>

  <div class="frame" style="left:1720px;top:810px;width:800px;height:460px;">
    <div class="frame-bar">
      <span>Çok Dilli Pazar &amp; Arama Hacmi İncelemesi</span>
      <span>TR · EN · DE · RU</span>
    </div>
    <img src="data:image/jpeg;base64,${imgSummer}" style="width:100%;height:416px;object-fit:cover;object-position:top center;"/>
  </div>

  <div class="frame" style="left:2570px;top:790px;width:530px;height:480px;background:#ffffff;padding:38px;display:flex;flex-direction:column;justify-content:space-between;">
    <div>
      <div style="font-size:14px;font-weight:700;color:#64748b;letter-spacing:0.05em;text-transform:uppercase;margin-bottom:12px;">HEDEF KİTLE SEGMENTLERİ</div>
      <div style="font-size:32px;font-weight:700;letter-spacing:-0.03em;margin-bottom:24px;">Satın Alma Motivasyonu</div>
      <div style="display:flex;flex-direction:column;gap:14px;">
        <div style="padding:16px 20px;background:#f8fafc;border-radius:10px;border:1px solid #e2e8f0;display:flex;justify-content:space-between;align-items:center;">
          <span style="font-weight:600;font-size:18px;">Yatırım &amp; ROI Odaklı</span>
          <span class="pill" style="background:#ede9fe;color:#6d28d9;">CPA -%34</span>
        </div>
        <div style="padding:16px 20px;background:#f8fafc;border-radius:10px;border:1px solid #e2e8f0;display:flex;justify-content:space-between;align-items:center;">
          <span style="font-weight:600;font-size:18px;">Kurumsal Karar Verici</span>
          <span class="pill" style="background:#dcfce7;color:#15803d;">LTV 3.2x</span>
        </div>
        <div style="padding:16px 20px;background:#f8fafc;border-radius:10px;border:1px solid #e2e8f0;display:flex;justify-content:space-between;align-items:center;">
          <span style="font-weight:600;font-size:18px;">Acil Çözüm Arayan Niyet</span>
          <span class="pill" style="background:#dbeafe;color:#1d4ed8;">TO %8.4</span>
        </div>
      </div>
    </div>
  </div>

  <div class="sticky" style="left:2145px;top:695px;width:360px;">
    Yüksek niyetli aramalarda rakip bütçe boşluğu var — ilk 30 günde odaklan.
  </div>


  <!-- ==================== CLUSTER 3 (BOTTOM-RIGHT) ==================== -->
  <div class="frame" style="left:1660px;top:1340px;width:750px;height:480px;padding:36px 40px;">
    <div style="font-size:14px;font-weight:700;color:#64748b;letter-spacing:0.05em;text-transform:uppercase;margin-bottom:10px;">03 · DÖNÜŞÜM HUNİSİ TASARIMI</div>
    <div style="font-size:32px;font-weight:700;letter-spacing:-0.03em;margin-bottom:22px;">Tam Huni (Full-Funnel) Akışı</div>
    <div style="display:flex;flex-direction:column;gap:12px;">
      <div style="background:#0f172a;color:#fff;padding:15px 24px;border-radius:10px;width:100%;display:flex;justify-content:space-between;font-size:18px;font-weight:600;">
        <span>1 · Farkındalık &amp; Video Kancası</span><span>İzlenme %48</span>
      </div>
      <div style="background:#1e293b;color:#fff;padding:15px 24px;border-radius:10px;width:88%;display:flex;justify-content:space-between;font-size:18px;font-weight:600;">
        <span>2 · Arama &amp; Yapay Zeka Yanıtı (SEO / AEO)</span><span>TO %6.4</span>
      </div>
      <div style="background:#4c1d95;color:#fff;padding:15px 24px;border-radius:10px;width:76%;display:flex;justify-content:space-between;font-size:18px;font-weight:600;">
        <span>3 · Dinamik Yeniden Pazarlama</span><span>ROAS 7.8x</span>
      </div>
      <div style="background:#7601ff;color:#fff;padding:15px 24px;border-radius:10px;width:64%;display:flex;justify-content:space-between;font-size:18px;font-weight:600;">
        <span>4 · Satış, Teklif &amp; CRM Kapanışı</span><span>Dönüşüm %5.9</span>
      </div>
    </div>
  </div>

  <div class="frame" style="left:2460px;top:1340px;width:640px;height:480px;background:#3b0764;color:#ffffff;padding:42px 44px;display:flex;flex-direction:column;justify-content:space-between;">
    <div style="display:flex;justify-content:space-between;align-items:center;">
      <span style="font-size:14px;font-weight:700;letter-spacing:0.06em;color:#e9d5ff;text-transform:uppercase;">04 · BÜYÜME YOL HARİTASI</span>
      <span class="pill" style="background:rgba(255,255,255,0.14);color:#fde047;">90 GÜN</span>
    </div>
    <div style="font-size:52px;font-weight:700;line-height:1.06;letter-spacing:-0.03em;color:#fde047;">
      Adım Adım<br>Ölçeklenme Planı
    </div>
    <div style="display:flex;flex-direction:column;gap:12px;font-size:19px;color:#f3e8ff;">
      <div><b>Gün 1–30:</b> Veri Denetimi, Huni &amp; Hızlı Kazanımlar</div>
      <div><b>Gün 31–60:</b> Kreatif Varyasyon &amp; Açılış Sayfası CRO</div>
      <div><b>Gün 61–90:</b> Kârlı Kampanya &amp; Yeni Pazar Ölçeklendirme</div>
    </div>
  </div>

  <div class="frame" style="left:1760px;top:1885px;width:820px;height:455px;">
    <div class="frame-bar">
      <span>Açılış Sayfası Mesaj &amp; Teklif Kurgusu</span>
      <span>hrshortlist.com</span>
    </div>
    <img src="data:image/jpeg;base64,${imgHr}" style="width:100%;height:411px;object-fit:cover;object-position:top center;"/>
  </div>

  <div class="sticky" style="left:1355px;top:1765px;width:365px;">
    Karar verici kitlede masaüstü dönüşüm oranı %68 daha yüksek — teklif kurgusunu ayır.
  </div>


  <!-- ==================== CLUSTER 4 (BOTTOM-LEFT) ==================== -->
  <div class="frame" style="left:290px;top:1310px;width:760px;height:480px;">
    <div class="frame-bar">
      <span>Kreatif Öncesi Değer Önerisi &amp; Görsel Ton</span>
      <span>cordeliacyprus.com</span>
    </div>
    <img src="data:image/jpeg;base64,${imgCordelia}" style="width:100%;height:436px;object-fit:cover;object-position:center 35%;"/>
  </div>

  <div class="frame" style="left:1100px;top:1310px;width:500px;height:435px;background:#ff008c;color:#ffffff;padding:38px 42px;display:flex;flex-direction:column;justify-content:space-between;">
    <span style="font-size:14px;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;opacity:0.9;">VERİ DOĞRULUĞU</span>
    <div>
      <div style="font-size:104px;font-weight:700;line-height:0.95;letter-spacing:-0.04em;">%98.4</div>
      <div style="font-size:27px;font-weight:600;margin-top:12px;letter-spacing:-0.02em;">Dönüşüm Eşleşmesi</div>
    </div>
    <div style="font-size:17px;opacity:0.94;">Server-Side GTM + Meta CAPI + CRM</div>
  </div>

  <div class="frame" style="left:330px;top:1855px;width:960px;height:485px;background:#141418;color:#ffffff;padding:40px 46px;display:flex;align-items:center;justify-content:space-between;">
    <div style="max-width:440px;">
      <div style="font-size:14px;font-weight:700;color:#a78bfa;letter-spacing:0.05em;text-transform:uppercase;margin-bottom:14px;">STRATEJİ ÇIKTISI</div>
      <div style="font-size:40px;font-weight:700;line-height:1.12;letter-spacing:-0.03em;margin-bottom:18px;">Netleşmiş Büyüme Yol Haritası</div>
      <div style="font-size:19px;color:#a1a1aa;line-height:1.5;">
        Hedef CPA, kanal bazlı bütçe ağırlıkları ve ilk 90 günlük test takvimi tek tabloda onaylanır.
      </div>
    </div>
    <svg width="400" height="360" viewBox="0 0 400 360">
      <circle cx="255" cy="195" r="112" fill="#c4b5fd"/>
      <text x="255" y="190" text-anchor="middle" font-size="58" font-weight="700" fill="#141418">6.4x</text>
      <text x="255" y="222" text-anchor="middle" font-size="17" font-weight="600" fill="#1e1b4b">HEDEF ROAS</text>
      <circle cx="115" cy="115" r="68" fill="#7601ff"/>
      <text x="115" y="112" text-anchor="middle" font-size="32" font-weight="700" fill="#ffffff">-38%</text>
      <text x="115" y="136" text-anchor="middle" font-size="14" font-weight="600" fill="#ede9fe">HEDEF CPA</text>
      <circle cx="115" cy="272" r="54" fill="#d2f800"/>
      <text x="115" y="270" text-anchor="middle" font-size="26" font-weight="700" fill="#141418">+3.2x</text>
      <text x="115" y="292" text-anchor="middle" font-size="13" font-weight="700" fill="#141418">LTV / CAC</text>
    </svg>
  </div>

  <div class="sticky" style="left:820px;top:1690px;width:355px;">
    Görsel üretime geçmeden önce her kanalın kârlılık çerçevesi netleştirildi.
  </div>

</body>
</html>`;

const bin = fs.existsSync('/usr/bin/chromium') ? '/usr/bin/chromium' : '/usr/bin/google-chrome';
const dbgPort = 9889;
const chrome = spawn(bin, [
  '--headless=new', '--no-sandbox', '--disable-gpu', '--hide-scrollbars',
  `--proxy-server=${process.env.HTTPS_PROXY || process.env.HTTP_PROXY}`,
  '--ignore-certificate-errors',
  `--user-data-dir=/tmp/chr-m1b-${Date.now()}`, `--remote-debugging-port=${dbgPort}`,
  '--window-size=3400,2600', 'about:blank'
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
await send('Emulation.setDeviceMetricsOverride', { width: 3400, height: 2600, deviceScaleFactor: 1, mobile: false });

const frameId = (await send('Page.getFrameTree')).frameTree.frame.id;
await send('Page.setDocumentContent', { frameId, html });
await send('Runtime.evaluate', { expression: 'document.fonts.ready', awaitPromise: true });
await sleep(400);

const shot = await send('Page.captureScreenshot', { format: 'png' });
fs.writeFileSync(path.join(OUT_DIR, 'board-01-strategy.png'), Buffer.from(shot.data, 'base64'));
console.log('Saved board-01-strategy.png');

// Now render 3 transparent Figma multiplayer cursor sprites (2x supersampled -> 440x160)
await send('Emulation.setDeviceMetricsOverride', { width: 440, height: 160, deviceScaleFactor: 1, mobile: false });
await send('Emulation.setDefaultBackgroundColorOverride', { color: { r: 0, g: 0, b: 0, a: 0 } });

const CURSORS = [
  { slug: 'cursor-veri', label: 'Veri & Analitik', color: '#10b981' },
  { slug: 'cursor-strateji', label: 'Büyüme Stratejisi', color: '#7601ff' },
  { slug: 'cursor-medya', label: 'Medya Planlama', color: '#f43f5e' },
];

for (const cur of CURSORS) {
  const curHtml = `<!doctype html><html><head><meta charset="utf-8">
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,600&display=swap" rel="stylesheet">
    <style>*{box-sizing:border-box;margin:0;padding:0;}body{background:transparent;overflow:hidden;font-family:'DM Sans',sans-serif;}</style></head>
    <body>
      <div style="position:relative;width:440px;height:160px;padding:10px;">
        <!-- Figma cursor pointer arrow at top-left -->
        <svg width="46" height="48" viewBox="0 0 36 38" style="filter:drop-shadow(0 4px 10px rgba(0,0,0,0.22));display:block;">
          <path d="M4 3 L32 15 L19 20 L14 34 Z" fill="${cur.color}" stroke="#ffffff" stroke-width="3.2" stroke-linejoin="round"/>
        </svg>
        <!-- Pill label -->
        <div style="display:inline-block;margin-left:26px;margin-top:-6px;background:${cur.color};color:#ffffff;
          padding:11px 22px;border-radius:12px;font-size:25px;font-weight:600;letter-spacing:-0.015em;
          box-shadow:0 8px 20px rgba(0,0,0,0.20);border:2px solid rgba(255,255,255,0.92);white-space:nowrap;">
          ${cur.label}
        </div>
      </div>
    </body></html>`;
  await send('Page.setDocumentContent', { frameId, html: curHtml });
  await send('Runtime.evaluate', { expression: 'document.fonts.ready', awaitPromise: true });
  await sleep(120);
  const cShot = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(OUT_DIR, `${cur.slug}.png`), Buffer.from(cShot.data, 'base64'));
  console.log('Saved', cur.slug);
}

ws.close();
chrome.kill();
process.exit(0);
