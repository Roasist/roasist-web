import fs from 'node:fs';
import path from 'node:path';
import { spawn } from 'node:child_process';

const ROOT = '/home/antigravity/Roasist/roasist-web';
const PUB_CS_DIR = path.join(ROOT, 'public/images/case-studies');
const DIST_CS_DIR = path.join(ROOT, 'dist/images/case-studies');
const WEB_SCREENS_DIR = path.join(ROOT, 'scripts/assets/web-screens');

fs.mkdirSync(PUB_CS_DIR, { recursive: true });
fs.mkdirSync(DIST_CS_DIR, { recursive: true });
fs.mkdirSync(WEB_SCREENS_DIR, { recursive: true });

function b64File(absPath) {
  return fs.readFileSync(absPath).toString('base64');
}

// Assets for the 5 websites
const medLogoB64 = b64File('/tmp/medistate_logo_crop.png');
const medJciB64 = b64File('/tmp/medistate_jci_crop.png');
const medBldgB64 = b64File('/tmp/medistate_bldg_crop.jpg');
const medInteriorB64 = b64File('/tmp/med_cur_5.0.jpg');

const summerScreenB64 = b64File(path.join(WEB_SCREENS_DIR, 'summerhomes.jpg'));

const accLogoB64 = b64File(path.join(ROOT, 'public/images/clients/Calisma-Yuzeyi-28-kopya-9_4x.webp'));
const bessekizLogoB64 = b64File(path.join(ROOT, 'public/images/clients/besseKiz.png'));
const gekooLogoB64 = b64File(path.join(ROOT, 'public/images/clients/Calisma-Yuzeyi-28-kopya-4_4x.webp'));
const gekooSnacksB64 = b64File(path.join(ROOT, 'public/images/references/gekoo.jpg'));
const gekooFreshB64 = b64File('/tmp/gekoo_50.jpg');
const officeBgB64 = b64File(path.join(ROOT, 'public/images/projects/bonus-vip-office.jpg'));
const schoolBgB64 = b64File(path.join(ROOT, 'public/images/references/istanbul-medya-akademisi.jpg'));

// 1. Medistate Official Website (medistateinternational.com)
const medistateSiteHtml = `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 1440px; height: 940px; overflow: hidden;
    font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
    background: #f4f6f9; color: #1e293b;
  }
  .top-header {
    height: 82px; background: #ffffff;
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 56px;
    border-bottom: 1px solid #e5e7eb;
  }
  .logo-img { height: 50px; width: auto; display: block; }
  .jci-img { height: 52px; width: auto; display: block; }
  .nav-bar {
    height: 54px; background: #ffffff;
    display: flex; align-items: center; gap: 34px;
    padding: 0 56px;
    border-bottom: 1px solid #e2e8f0;
    font-size: 14.5px; font-weight: 500; color: #334155;
  }
  .nav-item { display: flex; align-items: center; gap: 6px; white-space: nowrap; }
  .nav-caret { font-size: 11px; color: #64748b; }
  .hero {
    position: relative;
    width: 1440px; height: 560px;
    background-image: url('data:image/jpeg;base64,${medBldgB64}');
    background-size: cover; background-position: center 28%;
  }
  .hero-overlay {
    position: absolute; inset: 0;
    background: linear-gradient(180deg, rgba(15,23,42,0.08) 0%, rgba(15,23,42,0.38) 65%, rgba(15,23,42,0.58) 100%);
  }
  .right-quick-tabs {
    position: absolute; right: 0; top: 88px;
    display: flex; flex-direction: column; gap: 4px; z-index: 10;
  }
  .q-tab {
    width: 44px; padding: 18px 0;
    border-radius: 10px 0 0 10px;
    color: #ffffff; font-size: 12px; font-weight: 600;
    writing-mode: vertical-rl; transform: rotate(180deg);
    display: flex; align-items: center; justify-content: center; gap: 8px;
    letter-spacing: 0.02em;
    box-shadow: -4px 4px 16px rgba(0,0,0,0.18);
  }
  .cards-row {
    position: relative; z-index: 5;
    margin-top: -86px;
    padding: 0 56px;
    display: grid; grid-template-columns: 1fr 1fr; gap: 28px;
  }
  .hosp-card {
    background: #ffffff;
    border-radius: 20px;
    padding: 32px 38px;
    box-shadow: 0 18px 40px rgba(15, 23, 42, 0.09);
    text-align: center;
    border: 1px solid rgba(226, 232, 240, 0.9);
  }
  .hosp-sub {
    font-size: 16px; font-weight: 500; color: #475569; margin-bottom: 4px;
  }
  .hosp-title {
    font-size: 24px; font-weight: 700; color: #1e293b; margin-bottom: 14px;
    letter-spacing: -0.02em;
  }
  .hosp-desc {
    font-size: 14px; line-height: 1.6; color: #64748b;
    max-width: 520px; margin: 0 auto 18px;
  }
  .hosp-btn {
    display: inline-flex; align-items: center; gap: 8px;
    padding: 9px 24px; border-radius: 999px;
    border: 1.5px solid #0284c7; color: #0284c7;
    font-size: 13.5px; font-weight: 600;
  }
</style>
</head>
<body>
  <header class="top-header">
    <img class="logo-img" src="data:image/png;base64,${medLogoB64}" alt="Medistate">
    <img class="jci-img" src="data:image/png;base64,${medJciB64}" alt="JCI Accredited">
  </header>
  <nav class="nav-bar">
    <div class="nav-item">Hospitals <span class="nav-caret">⌄</span></div>
    <div class="nav-item">Doctors</div>
    <div class="nav-item">Medical Units</div>
    <div class="nav-item">Technologies</div>
    <div class="nav-item">Health Guide <span class="nav-caret">⌄</span></div>
    <div class="nav-item">Check-Up</div>
    <div class="nav-item">Patients and Visitors <span class="nav-caret">⌄</span></div>
    <div class="nav-item">Corporate <span class="nav-caret">⌄</span></div>
    <div class="nav-item">Communication <span class="nav-caret">⌄</span></div>
  </nav>
  <section class="hero">
    <div class="right-quick-tabs">
      <div class="q-tab" style="background:#0284c7;">444 44 13 · 7/24</div>
      <div class="q-tab" style="background:#00b4d8;">Book an Appointment</div>
      <div class="q-tab" style="background:#334155;">Contact Us</div>
    </div>
  </section>
  <section class="cards-row">
    <div class="hosp-card">
      <div class="hosp-sub">Medistate</div>
      <div class="hosp-title">Çekmeköy Hospital</div>
      <div class="hosp-desc">
        Medistate Çekmeköy Private Hospital, operating under the principle of "Your Health is Valuable", provides world-class healthcare services by combining modern medicine with a patient-centered approach.
      </div>
      <div class="hosp-btn">Detailed Information →</div>
    </div>
    <div class="hosp-card">
      <div class="hosp-sub">Medistate</div>
      <div class="hosp-title">Kavacık Hospital</div>
      <div class="hosp-desc">
        Medistate Kavacık Private Hospital provides JCI-accredited, preventive, and curative healthcare services across 41 specialized medical units with internationally experienced physicians.
      </div>
      <div class="hosp-btn">Detailed Information →</div>
    </div>
  </section>
</body>
</html>`;

// 2. Summer Homes Official Website (summerhomes.com) -> uses the real 1920x1080 screenshot at full width (no left/right clipping)
const summerBldgB64 = b64File(path.join(ROOT, 'public/images/projects/summer-homes.jpg'));
const summerPoolB64 = b64File(path.join(WEB_SCREENS_DIR, 'cordelia.jpg'));
const summerSiteHtml = `<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700&display=swap" rel="stylesheet">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 1440px; height: 940px; overflow: hidden;
    background: #ffffff;
    font-family: 'Plus Jakarta Sans', sans-serif;
  }
  .top-ss {
    width: 1440px; height: 798px;
    overflow: hidden;
  }
  .top-ss img {
    width: 1440px; height: 810px;
    display: block;
  }
  .dest-row {
    padding: 10px 180px 0;
    display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px;
    background: #ffffff;
  }
  .dest-card {
    height: 120px; border-radius: 14px; overflow: hidden;
    position: relative;
    display: flex; flex-direction: column; justify-content: flex-end;
    padding: 16px 20px; color: #ffffff;
    box-shadow: 0 8px 20px rgba(15, 23, 42, 0.08);
  }
  .dest-title { font-size: 16px; font-weight: 700; margin-bottom: 2px; }
  .dest-sub { font-size: 12px; color: rgba(255,255,255,0.88); font-weight: 600; }
</style>
</head>
<body>
  <div class="top-ss">
    <img src="data:image/jpeg;base64,${summerScreenB64}" alt="Summer Homes">
  </div>
  <div class="dest-row">
    <div class="dest-card" style="background:linear-gradient(180deg,rgba(12,74,110,0.25),rgba(12,74,110,0.88)),url('data:image/jpeg;base64,${summerBldgB64}') center/cover;">
      <div class="dest-title">Türkiye'deki Mülkler</div>
      <div class="dest-sub">Alanya · Antalya · İstanbul · Bodrum →</div>
    </div>
    <div class="dest-card" style="background:linear-gradient(180deg,rgba(6,78,59,0.25),rgba(6,78,59,0.88)),url('data:image/jpeg;base64,${summerPoolB64}') left bottom/cover;">
      <div class="dest-title">Kıbrıs'taki Mülkler</div>
      <div class="dest-sub">Girne · İskele · Gazimağusa →</div>
    </div>
    <div class="dest-card" style="background:linear-gradient(180deg,rgba(30,41,59,0.25),rgba(30,41,59,0.88)),url('data:image/jpeg;base64,${summerBldgB64}') right top/cover;">
      <div class="dest-title">Dubai'deki Mülkler</div>
      <div class="dest-sub">Yüksek Kira Getirili Yatırım Projeleri →</div>
    </div>
  </div>
</body>
</html>`;

// 3. ACC — Autarke Call Center Official Website (autarkecallcenter.com)
const accSiteHtml = `<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 1440px; height: 940px; overflow: hidden;
    font-family: 'Plus Jakarta Sans', sans-serif;
    background: #faf9f6; color: #18181b;
    font-variant-numeric: tabular-nums;
  }
  .top-bar {
    height: 40px; background: #18181b; color: #d4d4d8;
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 64px; font-size: 13px; font-weight: 500;
  }
  .top-bar span.gold { color: #d4af37; font-weight: 600; }
  .navbar {
    height: 86px; background: #ffffff;
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 64px;
    border-bottom: 1px solid #e4e4e7;
  }
  .logo-wrap {
    height: 62px; width: 220px; overflow: hidden;
    display: flex; align-items: center;
  }
  .logo-wrap img {
    width: 240px; height: auto;
    margin-left: -10px;
  }
  .nav-links {
    display: flex; align-items: center; gap: 32px;
    font-size: 14.5px; font-weight: 600; color: #27272a;
  }
  .nav-links .active { color: #856b38; }
  .nav-cta {
    background: #18181b; color: #ffffff;
    padding: 12px 24px; border-radius: 8px;
    font-size: 14px; font-weight: 600;
    border: 1px solid #9a7b3e;
  }
  .hero {
    position: relative;
    height: 555px;
    background: linear-gradient(95deg, #121316 0%, #1c1d22 52%, rgba(24,24,27,0.72) 100%),
                url('data:image/jpeg;base64,${officeBgB64}') center/cover no-repeat;
    padding: 58px 64px;
    display: grid; grid-template-columns: 1.18fr 0.82fr; gap: 48px; align-items: center;
  }
  .badge {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(197, 168, 105, 0.16);
    border: 1px solid rgba(197, 168, 105, 0.45);
    color: #e5c985;
    padding: 7px 16px; border-radius: 999px;
    font-size: 12.5px; font-weight: 700; letter-spacing: 0.05em;
    text-transform: uppercase; margin-bottom: 20px;
  }
  .hero h1 {
    font-size: 44px; font-weight: 800; color: #ffffff;
    line-height: 1.14; letter-spacing: -0.025em; margin-bottom: 18px;
  }
  .hero h1 em {
    font-style: normal; color: #dfbe77;
  }
  .hero p {
    font-size: 16.5px; line-height: 1.6; color: #d4d4d8;
    max-width: 620px; margin-bottom: 28px;
  }
  .perks {
    display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px;
  }
  .perk {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 10px; padding: 14px 16px;
  }
  .perk-val { font-size: 19px; font-weight: 700; color: #dfbe77; margin-bottom: 4px; }
  .perk-lbl { font-size: 12.5px; color: #e4e4e7; line-height: 1.35; }
  .apply-card {
    background: #ffffff; border-radius: 16px;
    padding: 28px 30px;
    box-shadow: 0 24px 48px rgba(0,0,0,0.35);
    border-top: 4px solid #b0914f;
  }
  .apply-title {
    font-size: 20px; font-weight: 700; color: #18181b;
    letter-spacing: -0.02em; margin-bottom: 4px;
  }
  .apply-sub {
    font-size: 13px; color: #71717a; margin-bottom: 18px;
  }
  .field {
    margin-bottom: 12px;
  }
  .field-lbl {
    font-size: 12px; font-weight: 600; color: #3f3f46; margin-bottom: 5px;
  }
  .field-box {
    height: 40px; border: 1px solid #d4d4d8; border-radius: 8px;
    background: #fafafa; padding: 0 14px;
    display: flex; align-items: center; justify-content: space-between;
    font-size: 13.5px; color: #52525b;
  }
  .submit-btn {
    margin-top: 14px; height: 46px; width: 100%;
    background: #8f7236; color: #ffffff;
    border-radius: 8px; display: flex; align-items: center; justify-content: center;
    font-size: 14.5px; font-weight: 700; letter-spacing: 0.01em;
  }
  .bottom-strip {
    height: 259px; background: #ffffff;
    padding: 32px 64px;
    display: grid; grid-template-columns: repeat(3, 1fr); gap: 28px;
  }
  .b-card {
    background: #faf9f5; border: 1px solid #e7e2d3;
    border-radius: 14px; padding: 22px 24px;
  }
  .b-tag {
    font-size: 11.5px; font-weight: 700; color: #8f7236;
    text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px;
  }
  .b-title {
    font-size: 18px; font-weight: 700; color: #18181b; margin-bottom: 8px;
    letter-spacing: -0.015em;
  }
  .b-desc {
    font-size: 13.5px; line-height: 1.5; color: #52525b;
  }
</style>
</head>
<body>
  <div class="top-bar">
    <div>Standorte in der Türkei: <span class="gold">İstanbul · İzmir · Antalya · Ankara · Homeoffice</span></div>
    <div>Karriere-Hotline: <span class="gold">+90 (212) 909 00 49</span> &nbsp;|&nbsp; karriere@autarkecallcenter.com &nbsp;|&nbsp; DE / TR</div>
  </div>
  <header class="navbar">
    <div class="logo-wrap">
      <img src="data:image/webp;base64,${accLogoB64}" alt="ACC Autarke Call Center">
    </div>
    <div class="nav-links">
      <span class="active">Startseite</span>
      <span>Über ACC</span>
      <span>Kundenservice &amp; BPO</span>
      <span>Karriere (Deutsch C1/C2)</span>
      <span>Standorte</span>
      <span>Kontakt</span>
    </div>
    <div class="nav-cta">Jetzt Bewerben →</div>
  </header>
  <section class="hero">
    <div>
      <div class="badge">AUTARKE CALL CENTER · DEUTSCHSPRACHIGE KARRIERE IN DER TÜRKEI</div>
      <h1>Du sprichst fließend <em>Deutsch?</em> Starte deine Karriere bei ACC!</h1>
      <p>
        Als führendes deutschsprachiges Customer-Care-Center in der Türkei bieten wir Muttersprachlern (C1/C2) erstklassige Karrierechancen, Top-Vergütung auf europäischem Niveau und flexible Arbeitsmodelle.
      </p>
      <div class="perks">
        <div class="perk">
          <div class="perk-val">EUR / TRY</div>
          <div class="perk-lbl">Überdurchschnittliches Fixgehalt + Leistungsbonus</div>
        </div>
        <div class="perk">
          <div class="perk-val">100% DACH</div>
          <div class="perk-lbl">Exklusive Projekte aus Deutschland, Österreich &amp; Schweiz</div>
        </div>
        <div class="perk">
          <div class="perk-val">Homeoffice</div>
          <div class="perk-lbl">Moderne Büros oder Türkeiweit im Homeoffice arbeiten</div>
        </div>
      </div>
    </div>
    <div class="apply-card">
      <div class="apply-title">Schnellbewerbung in 60 Sekunden</div>
      <div class="apply-sub">Kundenberater (m/w/d) Inbound &amp; Outbound — Deutsch C1/C2</div>
      <div class="field">
        <div class="field-lbl">Vor- und Nachname *</div>
        <div class="field-box">Max Mustermann</div>
      </div>
      <div class="field">
        <div class="field-lbl">Telefonnummer (WhatsApp erreichbar) *</div>
        <div class="field-box">+90 (532) 000 00 00</div>
      </div>
      <div class="field">
        <div class="field-lbl">Deutsch-Sprachniveau *</div>
        <div class="field-box"><span>Muttersprachler / C2 Niveau</span><span>⌄</span></div>
      </div>
      <div class="field">
        <div class="field-lbl">Bevorzugtes Arbeitsmodell *</div>
        <div class="field-box"><span>Homeoffice (Türkeiweit) / Büro</span><span>⌄</span></div>
      </div>
      <div class="submit-btn">Bewerbung Jetzt Absenden →</div>
    </div>
  </section>
  <section class="bottom-strip">
    <div class="b-card">
      <div class="b-tag">01 · KUNDENBETREUUNG AUF HÖCHSTEM NIVEAU</div>
      <div class="b-title">Inbound &amp; Qualitäts-Support</div>
      <div class="b-desc">Professionelle Beratung für renommierte Unternehmen aus Telekommunikation, Energie und E-Commerce im DACH-Raum.</div>
    </div>
    <div class="b-card">
      <div class="b-tag">02 · MITARBEITERVORTEILE</div>
      <div class="b-title">SGK, Privatversicherung &amp; Prämien</div>
      <div class="b-desc">Pünktliche Gehaltszahlung, ungedeckelte Provisionsmodelle, bezahlte Schulungen und langfristige Aufstiegschancen.</div>
    </div>
    <div class="b-card">
      <div class="b-tag">03 · ARBEITEN BEI ACC</div>
      <div class="b-title">Starkes Team &amp; Moderne Kultur</div>
      <div class="b-desc">Familiäres Arbeitsklima mit deutschsprachigen Teamleitern, modernem Equipment und direktem Onboarding.</div>
    </div>
  </section>
</body>
</html>`;

// 4. Beşsekiz Ortaokulları Official Website (bessekizortaokullari.com)
const bessekizSiteHtml = `<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 1440px; height: 940px; overflow: hidden;
    font-family: 'Plus Jakarta Sans', sans-serif;
    background: #f8faf8; color: #14261c;
    font-variant-numeric: tabular-nums;
  }
  .top-exam-bar {
    height: 42px; background: #17562b; color: #ffffff;
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 56px; font-size: 13px; font-weight: 600;
  }
  .exam-pill {
    background: #f59e0b; color: #14261c;
    padding: 5px 16px; border-radius: 999px;
    font-size: 12.5px; font-weight: 800; letter-spacing: 0.02em;
  }
  .navbar {
    height: 88px; background: #ffffff;
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 56px; gap: 24px;
    border-bottom: 1px solid #e2e8f0;
    box-shadow: 0 4px 16px rgba(23, 86, 43, 0.05);
  }
  .logo-box {
    height: 64px; width: 175px; flex-shrink: 0; overflow: hidden;
    display: flex; align-items: center;
  }
  .logo-box img {
    width: 170px; height: auto;
  }
  .nav-menu {
    display: flex; align-items: center; gap: 15px;
    font-size: 12px; font-weight: 700; color: #1e293b;
    text-transform: uppercase; letter-spacing: 0.005em;
    white-space: nowrap;
  }
  .nav-menu .active { color: #17562b; }
  .nav-cta {
    background: #17562b; color: #ffffff;
    padding: 12px 20px; border-radius: 10px;
    font-size: 12.5px; font-weight: 700;
    white-space: nowrap; flex-shrink: 0;
  }
  .hero {
    height: 530px;
    background: linear-gradient(95deg, #0f391d 0%, #17562b 54%, rgba(23,86,43,0.82) 100%),
                url('data:image/jpeg;base64,${schoolBgB64}') center/cover no-repeat;
    padding: 52px 60px;
    display: grid; grid-template-columns: 1.18fr 0.82fr; gap: 46px; align-items: center;
    color: #ffffff;
  }
  .hero-badge {
    display: inline-block;
    background: rgba(255,255,255,0.14);
    border: 1px solid rgba(255,255,255,0.28);
    padding: 7px 16px; border-radius: 999px;
    font-size: 12.5px; font-weight: 700; letter-spacing: 0.04em;
    margin-bottom: 18px; color: #dcfce7;
  }
  .hero h1 {
    font-size: 46px; font-weight: 800; line-height: 1.12;
    letter-spacing: -0.025em; margin-bottom: 16px;
  }
  .hero h1 span { color: #fde047; }
  .hero p {
    font-size: 16px; line-height: 1.62; color: #ecfdf5;
    margin-bottom: 28px; max-width: 630px;
  }
  .hero-btns {
    display: flex; align-items: center; gap: 16px;
  }
  .btn-primary {
    background: #f59e0b; color: #14261c;
    padding: 14px 28px; border-radius: 10px;
    font-size: 14.5px; font-weight: 800;
  }
  .btn-outline {
    background: rgba(255,255,255,0.1); color: #ffffff;
    border: 1.5px solid rgba(255,255,255,0.45);
    padding: 13px 24px; border-radius: 10px;
    font-size: 14px; font-weight: 700;
  }
  .form-card {
    background: #ffffff; color: #1e293b;
    border-radius: 18px; padding: 28px 30px;
    box-shadow: 0 22px 45px rgba(0,0,0,0.25);
  }
  .form-title {
    font-size: 19px; font-weight: 800; color: #17562b;
    letter-spacing: -0.02em; margin-bottom: 4px;
  }
  .form-sub {
    font-size: 13px; color: #64748b; margin-bottom: 16px;
  }
  .f-row { margin-bottom: 11px; }
  .f-lbl { font-size: 12px; font-weight: 700; color: #334155; margin-bottom: 4px; }
  .f-inp {
    height: 39px; border: 1px solid #cbd5e1; border-radius: 8px;
    background: #f8fafc; padding: 0 13px;
    display: flex; align-items: center; justify-content: space-between;
    font-size: 13px; color: #475569;
  }
  .f-btn {
    margin-top: 14px; height: 45px; background: #17562b; color: #ffffff;
    border-radius: 8px; display: flex; align-items: center; justify-content: center;
    font-size: 14px; font-weight: 800;
  }
  .concepts {
    height: 280px; background: #ffffff;
    padding: 30px 60px;
    display: grid; grid-template-columns: repeat(3, 1fr); gap: 26px;
  }
  .c-card {
    background: #f4f9f5; border: 1px solid #d1fae5;
    border-radius: 16px; padding: 22px 24px;
    display: flex; flex-direction: column; justify-content: space-between;
  }
  .c-head {
    font-size: 17px; font-weight: 800; color: #17562b;
    letter-spacing: -0.015em; margin-bottom: 8px;
  }
  .c-body {
    font-size: 13.5px; line-height: 1.52; color: #334155; margin-bottom: 12px;
  }
  .c-link {
    font-size: 12.5px; font-weight: 800; color: #17562b;
    text-transform: uppercase; letter-spacing: 0.04em;
  }
</style>
</head>
<body>
  <div class="top-exam-bar">
    <div class="exam-pill">BEŞSEKİZ'E GİRİŞ SINAVI BAŞVURU İÇİN TIKLAYIN →</div>
    <div>Sakarya Kampüsü: 0 264 373 72 00 &nbsp;|&nbsp; İzmit Kampüsü: 0 262 331 05 08 &nbsp;|&nbsp; info@bessekizortaokullari.com</div>
  </div>
  <header class="navbar">
    <div class="logo-box">
      <img src="data:image/png;base64,${bessekizLogoB64}" alt="Beşsekiz Ortaokulları">
    </div>
    <div class="nav-menu">
      <span class="active">Anasayfa</span>
      <span>Kurumsal ⌄</span>
      <span>Sakarya Kampüsü ⌄</span>
      <span>İzmit Kampüsü ⌄</span>
      <span>Beşsekiz'de Eğitim ⌄</span>
      <span>Beşsekiz'de Yaşam ⌄</span>
      <span>Veli Görüşleri</span>
      <span>İletişim</span>
    </div>
    <div class="nav-cta">ONLINE KAYIT RANDEVUSU</div>
  </header>
  <section class="hero">
    <div>
      <div class="hero-badge">BOYUT EĞİTİM KURUMLARI · YENİ ORTAOKUL KONSEPTİ</div>
      <h1>Öğrenmenin Sınırı Yok!<br><span>İşimiz Gücümüz Ortaokul.</span></h1>
      <p>
        Nitelikli bir ortaokul eğitimi iyi bir lisenin, iyi bir lise eğitimi de iyi bir üniversitenin kapılarını açar. 5. sınıfı haftada 20 saat İngilizce hazırlık sınıfı olarak tasarladık; doğru lise kazandırmanın çalışmalarını birlikte gerçekleştiriyoruz.
      </p>
      <div class="hero-btns">
        <div class="btn-primary">BİZİ YAKINDAN TANIYIN →</div>
        <div class="btn-outline">KAMPÜSLERİMİZİ İNCELEYİN</div>
      </div>
    </div>
    <div class="form-card">
      <div class="form-title">Kayıt &amp; Bursluluk Sınavı Başvuru Formu</div>
      <div class="form-sub">Eğitim danışmanlarımız 24 saat içinde sizinle iletişime geçsin.</div>
      <div class="f-row">
        <div class="f-lbl">Veli Adı Soyadı *</div>
        <div class="f-inp">Ahmet Yılmaz</div>
      </div>
      <div class="f-row">
        <div class="f-lbl">Veli Cep Telefonu *</div>
        <div class="f-inp">0 (532) 000 00 00</div>
      </div>
      <div class="f-row">
        <div class="f-lbl">Kampüs &amp; Sınıf Seçimi *</div>
        <div class="f-inp"><span>İzmit Kampüsü · 5. Sınıf (İngilizce Hazırlık)</span><span>⌄</span></div>
      </div>
      <div class="f-btn">BAŞVURUYU TAMAMLA →</div>
    </div>
  </section>
  <section class="concepts">
    <div class="c-card">
      <div>
        <div class="c-head">İŞİMİZ GÜCÜMÜZ ORTAOKUL</div>
        <div class="c-body">Beşsekiz Ortaokulları, yalnızca ortaokul kademesine odaklanan uzmanlaşmış akademik kadrosuyla yeni bir ortaokul projesidir.</div>
      </div>
      <div class="c-link">DETAYLI İNCELE →</div>
    </div>
    <div class="c-card">
      <div>
        <div class="c-head">HAFTADA 20 SAAT İNGİLİZCE</div>
        <div class="c-body">5. sınıf hazırlık programımızla öğrencilerimizin İngilizce'yi anadili gibi konuşabilen, tam donanımlı bireyler olmasını amaçlıyoruz.</div>
      </div>
      <div class="c-link">DETAYLI İNCELE →</div>
    </div>
    <div class="c-card">
      <div>
        <div class="c-head">LGS &amp; AKADEMİK TAM DONANIM</div>
        <div class="c-body">Matematik, Fen Bilimleri ve Türkçe derslerinde bireysel farklılıkları gözeten etüt ve rehberlik sistemiyle nitelikli liselere hazırlık.</div>
      </div>
      <div class="c-link">DAHA FAZLA BİLGİ →</div>
    </div>
  </section>
</body>
</html>`;

// 5. Gekoo Official E-Commerce Website (gekoo.com.tr — Doğayla Organik Bağınız)
const gekooSiteHtml = `<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 1440px; height: 940px; overflow: hidden;
    font-family: 'Plus Jakarta Sans', sans-serif;
    background: #fdfefb; color: #1e293b;
    font-variant-numeric: tabular-nums;
  }
  .promo-bar {
    height: 38px; background: #56217a; color: #ffffff;
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 56px; font-size: 12.5px; font-weight: 600;
  }
  .promo-bar span.hl { color: #b7e868; font-weight: 700; }
  .header-main {
    height: 84px; background: #ffffff;
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 56px;
    border-bottom: 1px solid #e5e7eb;
  }
  .gekoo-logo {
    height: 68px; width: 225px; overflow: hidden;
    display: flex; align-items: center;
  }
  .gekoo-logo img {
    width: 225px; height: auto;
  }
  .search-bar {
    width: 520px; height: 44px;
    background: #f4f7f2; border: 1.5px solid #d5e6c3;
    border-radius: 999px; padding: 0 20px;
    display: flex; align-items: center; justify-content: space-between;
    font-size: 13.5px; color: #64748b;
  }
  .search-btn {
    background: #65a30d; color: #ffffff;
    padding: 6px 16px; border-radius: 999px;
    font-size: 12.5px; font-weight: 700;
  }
  .header-actions {
    display: flex; align-items: center; gap: 18px;
    font-size: 13.5px; font-weight: 600; color: #334155;
  }
  .cart-pill {
    background: #56217a; color: #ffffff;
    padding: 10px 20px; border-radius: 999px;
    font-size: 13px; font-weight: 700;
    display: flex; align-items: center; gap: 8px;
  }
  .cat-bar {
    height: 46px; background: #f4f9ef;
    border-bottom: 1px solid #e2eed8;
    padding: 0 56px;
    display: flex; align-items: center; gap: 30px;
    font-size: 13.5px; font-weight: 700; color: #2e471d;
  }
  .cat-bar .active { color: #56217a; }
  .hero-banner {
    margin: 22px 56px;
    height: 330px;
    border-radius: 22px; overflow: hidden;
    background: linear-gradient(95deg, #2d1242 0%, #56217a 48%, #4d7c0f 100%);
    display: grid; grid-template-columns: 1.15fr 0.85fr;
    box-shadow: 0 16px 36px rgba(86, 33, 122, 0.14);
  }
  .hero-left {
    padding: 36px 46px; color: #ffffff;
    display: flex; flex-direction: column; justify-content: center;
  }
  .cert-pill {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(163, 230, 53, 0.2);
    border: 1px solid rgba(163, 230, 53, 0.5);
    color: #d9f99d;
    padding: 6px 14px; border-radius: 999px;
    font-size: 12px; font-weight: 700; width: fit-content;
    margin-bottom: 14px; letter-spacing: 0.03em;
  }
  .hero-left h1 {
    font-size: 34px; font-weight: 800; line-height: 1.16;
    letter-spacing: -0.02em; margin-bottom: 12px;
  }
  .hero-left h1 span { color: #bef264; }
  .hero-left p {
    font-size: 14.5px; line-height: 1.58; color: #f3e8ff;
    margin-bottom: 22px; max-width: 580px;
  }
  .hero-cta-row {
    display: flex; align-items: center; gap: 14px;
  }
  .btn-shop {
    background: #84cc16; color: #1a2e05;
    padding: 12px 26px; border-radius: 999px;
    font-size: 14px; font-weight: 800;
  }
  .btn-cert {
    background: rgba(255,255,255,0.12); color: #ffffff;
    border: 1px solid rgba(255,255,255,0.35);
    padding: 11px 22px; border-radius: 999px;
    font-size: 13.5px; font-weight: 700;
  }
  .hero-right {
    position: relative;
    background-image: url('data:image/jpeg;base64,${gekooSnacksB64}');
    background-size: cover; background-position: center;
  }
  .hero-right-badge {
    position: absolute; bottom: 20px; left: 20px;
    background: rgba(255,255,255,0.95); color: #1e293b;
    padding: 12px 18px; border-radius: 14px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    font-size: 12.5px; font-weight: 700;
  }
  .products-sec {
    padding: 6px 56px 0;
  }
  .sec-head {
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 16px;
  }
  .sec-title {
    font-size: 21px; font-weight: 800; color: #1e293b;
    letter-spacing: -0.02em;
  }
  .sec-sub {
    font-size: 13.5px; font-weight: 700; color: #56217a;
  }
  .prod-grid {
    display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px;
  }
  .prod-card {
    background: #ffffff; border: 1px solid #e2e8f0;
    border-radius: 16px; padding: 16px;
    box-shadow: 0 8px 20px rgba(15,23,42,0.04);
    display: flex; flex-direction: column; justify-content: space-between;
  }
  .p-top {
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 10px;
  }
  .p-badge {
    background: #ecfccb; color: #3f6212;
    font-size: 11px; font-weight: 800; padding: 4px 10px; border-radius: 999px;
  }
  .p-rate { font-size: 12px; font-weight: 700; color: #f59e0b; }
  .p-img {
    height: 112px; border-radius: 12px; margin-bottom: 12px;
    display: flex; align-items: center; justify-content: center;
    padding: 12px; text-align: center;
    font-weight: 800; font-size: 14px;
    position: relative; overflow: hidden;
  }
  .p-name {
    font-size: 14px; font-weight: 700; color: #1e293b;
    line-height: 1.38; margin-bottom: 6px;
  }
  .p-meta {
    font-size: 12px; color: #64748b; margin-bottom: 12px;
  }
  .p-foot {
    display: flex; align-items: center; justify-content: space-between;
  }
  .p-price {
    font-size: 18px; font-weight: 800; color: #56217a;
  }
  .p-add {
    background: #65a30d; color: #ffffff;
    padding: 8px 16px; border-radius: 8px;
    font-size: 12.5px; font-weight: 700;
  }
</style>
</head>
<body>
  <div class="promo-bar">
    <div>T.C. Tarım Bakanlığı &amp; CERES Organik Sertifikalı &nbsp;·&nbsp; <span class="hl">%100 Katkısız &amp; İlave Şekersiz Doğal Gıdalar</span></div>
    <div>Aynı Gün Kargo &nbsp;|&nbsp; 750 TL Üzeri Ücretsiz Teslimat &nbsp;|&nbsp; Müşteri Hizmetleri: 0850 304 43 56</div>
  </div>
  <header class="header-main">
    <div class="gekoo-logo">
      <img src="data:image/webp;base64,${gekooLogoB64}" alt="GekoO Organik">
    </div>
    <div class="search-bar">
      <span>Organik bebek bisküvisi, fırınlanmış sebze cipsi, keçiboynuzu unu...</span>
      <span class="search-btn">ARA</span>
    </div>
    <div class="header-actions">
      <span>Organik Sertifikalar</span>
      <span>Hesabım</span>
      <div class="cart-pill">Sepetim (3) · 428,00 TL</div>
    </div>
  </header>
  <nav class="cat-bar">
    <span class="active">Tüm Organik Ürünler</span>
    <span>Organik Bebek &amp; Çocuk Bisküvisi</span>
    <span>Fırınlanmış Sebze Cipsi</span>
    <span>Organik Müsli &amp; Ezme</span>
    <span>Organik Bakliyat &amp; Un</span>
    <span>Kuru Meyve</span>
    <span>Avantajlı Aile Paketleri</span>
  </nav>
  <section class="hero-banner">
    <div class="hero-left">
      <div class="cert-pill">DOĞAYLA ORGANİK BAĞINIZ · SERTİFİKALI ORGANİK ÜRETİM</div>
      <h1>Kendiniz ve Aileniz İçin<br><span>%100 Organik ve Sağlıklı Gıdalar</span></h1>
      <p>
        Gekoo e-ticaret mağazasında bebek ve çocuklarınız için katkısız organik bisküviler, düşük ısıda fırınlanmış taze sebze cipsleri ve organik tahıllar doğrudan sofranızda.
      </p>
      <div class="hero-cta-row">
        <div class="btn-shop">Alışverişe Başla →</div>
        <div class="btn-cert">Aile Paketlerini İncele</div>
      </div>
    </div>
    <div class="hero-right">
      <div class="hero-right-badge">
        %100 Organik Sertifikalı · Koruyucu &amp; İlave Şeker İçermez
      </div>
    </div>
  </section>
  <section class="products-sec">
    <div class="sec-head">
      <div class="sec-title">Çok Satan Organik Aile &amp; Çocuk Ürünleri</div>
      <div class="sec-sub">Tüm Ürünleri Gör (48 Ürün) →</div>
    </div>
    <div class="prod-grid">
      <div class="prod-card">
        <div>
          <div class="p-top"><span class="p-badge">ORGANİK SERTİFİKALI</span><span class="p-rate">★ 4.9 (214)</span></div>
          <div class="p-img" style="background:linear-gradient(135deg,#f3e8ff,#e9d5ff);color:#56217a;">
            GekoO Organik<br>Yulaflı Bebek Bisküvisi<br><span style="font-size:12px;font-weight:600;color:#6b21a8;">+8 Ay · Sütsüz Vegan · 250g</span>
          </div>
          <div class="p-name">Gekoo Organik Yulaflı Bebek Bisküvisi +8 Ay 250g</div>
          <div class="p-meta">Elma suyu konsantreli, ilave şekersiz</div>
        </div>
        <div class="p-foot"><span class="p-price">145,00 TL</span><span class="p-add">Sepete Ekle</span></div>
      </div>
      <div class="prod-card">
        <div>
          <div class="p-top"><span class="p-badge">ORGANİK SERTİFİKALI</span><span class="p-rate">★ 5.0 (178)</span></div>
          <div class="p-img" style="background:linear-gradient(135deg,#ecfccb,#d9f99d);color:#365314;">
            GekoO Organik<br>Sütlü Keçiboynuzlu<br><span style="font-size:12px;font-weight:600;color:#3f6212;">Şekilli Çocuk Bisküvisi · 150g</span>
          </div>
          <div class="p-name">Gekoo Organik Sütlü Keçiboynuzlu Çocuk Bisküvisi 150g</div>
          <div class="p-meta">Organik tam buğday unu &amp; keçiboynuzu</div>
        </div>
        <div class="p-foot"><span class="p-price">115,00 TL</span><span class="p-add">Sepete Ekle</span></div>
      </div>
      <div class="prod-card">
        <div>
          <div class="p-top"><span class="p-badge">FIRINLANMIŞ CİPS</span><span class="p-rate">★ 4.9 (132)</span></div>
          <div class="p-img" style="background:linear-gradient(135deg,#fce7f3,#fbcfe8);color:#831843;">
            GekoO Organik<br>Sebzeli Fırınlanmış Cips<br><span style="font-size:12px;font-weight:600;color:#9d174d;">Pancar, Soğan &amp; Zeytinyağı · 115g</span>
          </div>
          <div class="p-name">Gekoo Organik Sebzeli Fırınlanmış Cips (Pancar &amp; Soğan) 115g</div>
          <div class="p-meta">Kızartılmamış, taze sebze ve sızma zeytinyağlı</div>
        </div>
        <div class="p-foot"><span class="p-price">98,00 TL</span><span class="p-add">Sepete Ekle</span></div>
      </div>
      <div class="prod-card">
        <div>
          <div class="p-top"><span class="p-badge">AİLE BOYU KAHVALTI</span><span class="p-rate">★ 4.9 (95)</span></div>
          <div class="p-img" style="background:linear-gradient(135deg,#fef3c7,#fde68a);color:#78350f;">
            GekoO Organik<br>Ekomüsli 3 Tahıl<br><span style="font-size:12px;font-weight:600;color:#92400e;">Fındıklı &amp; Cevizli Müsli · 400g</span>
          </div>
          <div class="p-name">Gekoo Organik Ekomüsli 3 Tahıl Fındıklı Cevizli 400g</div>
          <div class="p-meta">Yüksek lifli, diyabetik &amp; katkısız tahıl karışımı</div>
        </div>
        <div class="p-foot"><span class="p-price">165,00 TL</span><span class="p-add">Sepete Ekle</span></div>
      </div>
    </div>
  </section>
</body>
</html>`;

const SITES = [
  { slug: 'medistate', domain: 'medistateinternational.com', html: medistateSiteHtml },
  { slug: 'summer-homes', domain: 'summerhomes.com', html: summerSiteHtml },
  { slug: 'acc', domain: 'autarkecallcenter.com', html: accSiteHtml },
  { slug: 'bessekiz-ortaokullari', domain: 'bessekizortaokullari.com', html: bessekizSiteHtml },
  { slug: 'gekoo', domain: 'gekoo.com.tr', html: gekooSiteHtml },
];

function buildVisualCardHtml(siteShotB64, domain) {
  return `<!doctype html>
<html>
<head>
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600&display=swap" rel="stylesheet">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 1354px; height: 1080px;
    background: transparent;
    display: flex; align-items: center; justify-content: center;
    font-family: 'Plus Jakarta Sans', sans-serif;
    overflow: hidden;
  }
  .browser-win {
    width: 1216px; height: 836px;
    border-radius: 22px;
    background: #14141d;
    border: 1.5px solid rgba(255, 255, 255, 0.18);
    box-shadow: 0 36px 80px rgba(0, 0, 0, 0.65), 0 0 0 1px rgba(118, 2, 255, 0.22);
    overflow: hidden;
    display: flex; flex-direction: column;
  }
  .browser-bar {
    height: 44px;
    background: #181824;
    border-bottom: 1px solid rgba(255, 255, 255, 0.09);
    padding: 0 20px;
    display: flex; align-items: center; justify-content: space-between;
  }
  .dots {
    display: flex; align-items: center; gap: 8px; width: 80px;
  }
  .dot {
    width: 11px; height: 11px; border-radius: 50%;
  }
  .dot.r { background: #ff5f56; }
  .dot.y { background: #ffbd2e; }
  .dot.g { background: #27c93f; }
  .url-pill {
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.09);
    border-radius: 8px;
    padding: 5px 28px;
    color: rgba(248, 250, 252, 0.82);
    font-size: 13px; font-weight: 500;
    display: flex; align-items: center; gap: 7px;
    letter-spacing: 0.01em;
  }
  .viewport {
    width: 1216px; height: 792px;
    overflow: hidden;
    background: #ffffff;
  }
  .viewport img {
    width: 100%; height: 100%;
    object-fit: cover; object-position: top center;
    display: block;
  }
</style>
</head>
<body>
  <div class="browser-win">
    <div class="browser-bar">
      <div class="dots">
        <span class="dot r"></span>
        <span class="dot y"></span>
        <span class="dot g"></span>
      </div>
      <div class="url-pill">
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
        <span>${domain}</span>
      </div>
      <div style="width:80px;"></div>
    </div>
    <div class="viewport">
      <img src="data:image/png;base64,${siteShotB64}" alt="${domain}">
    </div>
  </div>
</body>
</html>`;
}

function buildHeroBannerHtml(siteShotB64, domain) {
  return `<!doctype html>
<html>
<head>
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600&display=swap" rel="stylesheet">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 1400px; height: 787px;
    background: radial-gradient(circle at 50% 45%, #241346 0%, #0d0b14 72%);
    display: flex; align-items: center; justify-content: center;
    font-family: 'Plus Jakarta Sans', sans-serif;
    overflow: hidden;
  }
  .browser-win {
    width: 1120px; height: 696px;
    border-radius: 18px;
    background: #14141d;
    border: 1.5px solid rgba(255, 255, 255, 0.18);
    box-shadow: 0 32px 70px rgba(0, 0, 0, 0.65);
    overflow: hidden;
    display: flex; flex-direction: column;
  }
  .browser-bar {
    height: 40px;
    background: #181824;
    border-bottom: 1px solid rgba(255, 255, 255, 0.09);
    padding: 0 18px;
    display: flex; align-items: center; justify-content: space-between;
  }
  .dots {
    display: flex; align-items: center; gap: 7px; width: 70px;
  }
  .dot {
    width: 10px; height: 10px; border-radius: 50%;
  }
  .dot.r { background: #ff5f56; }
  .dot.y { background: #ffbd2e; }
  .dot.g { background: #27c93f; }
  .url-pill {
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.09);
    border-radius: 7px;
    padding: 4px 24px;
    color: rgba(248, 250, 252, 0.82);
    font-size: 12.5px; font-weight: 500;
    display: flex; align-items: center; gap: 6px;
  }
  .viewport {
    width: 1120px; height: 656px;
    overflow: hidden;
    background: #ffffff;
  }
  .viewport img {
    width: 100%; height: 100%;
    object-fit: cover; object-position: top center;
    display: block;
  }
</style>
</head>
<body>
  <div class="browser-win">
    <div class="browser-bar">
      <div class="dots">
        <span class="dot r"></span>
        <span class="dot y"></span>
        <span class="dot g"></span>
      </div>
      <div class="url-pill">
        <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
        <span>${domain}</span>
      </div>
      <div style="width:70px;"></div>
    </div>
    <div class="viewport">
      <img src="data:image/png;base64,${siteShotB64}" alt="${domain}">
    </div>
  </div>
</body>
</html>`;
}

const bin = fs.existsSync('/usr/bin/chromium') ? '/usr/bin/chromium' : '/usr/bin/google-chrome';
const dbgPort = 9894;
const chrome = spawn(bin, [
  '--headless=new', '--no-sandbox', '--disable-gpu', '--hide-scrollbars',
  `--proxy-server=${process.env.HTTPS_PROXY || process.env.HTTP_PROXY}`,
  '--ignore-certificate-errors',
  `--user-data-dir=/tmp/chr-cs-ss-${Date.now()}`, `--remote-debugging-port=${dbgPort}`,
  '--window-size=1440,940', 'about:blank'
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

for (const site of SITES) {
  // Step 1: Capture 1440x940 raw website screenshot
  await send('Emulation.setDeviceMetricsOverride', { width: 1440, height: 940, deviceScaleFactor: 1, mobile: false });
  await send('Emulation.setDefaultBackgroundColorOverride', { color: { r: 255, g: 255, b: 255, a: 1 } });
  await send('Page.setDocumentContent', { frameId, html: site.html });
  await send('Runtime.evaluate', { expression: 'document.fonts.ready', awaitPromise: true });
  await sleep(300);
  const rawShot = await send('Page.captureScreenshot', { format: 'png' });
  const rawB64 = rawShot.data;
  fs.writeFileSync(path.join(WEB_SCREENS_DIR, `${site.slug}-site.png`), Buffer.from(rawB64, 'base64'));

  // Step 2: Render 1354x1080 transparent *-visual.png for homepage "Ölçülebilir Sonuçlar" cards
  await send('Emulation.setDeviceMetricsOverride', { width: 1354, height: 1080, deviceScaleFactor: 1, mobile: false });
  await send('Emulation.setDefaultBackgroundColorOverride', { color: { r: 0, g: 0, b: 0, a: 0 } });
  await send('Page.setDocumentContent', { frameId, html: buildVisualCardHtml(rawB64, site.domain) });
  await send('Runtime.evaluate', { expression: 'document.fonts.ready', awaitPromise: true });
  await sleep(200);
  const visShot = await send('Page.captureScreenshot', { format: 'png' });
  const visBuf = Buffer.from(visShot.data, 'base64');
  fs.writeFileSync(path.join(PUB_CS_DIR, `${site.slug}-visual.png`), visBuf);
  fs.writeFileSync(path.join(DIST_CS_DIR, `${site.slug}-visual.png`), visBuf);

  // Step 3: Render 1400x787 *-hero.jpg for Case Study detail pages
  await send('Emulation.setDeviceMetricsOverride', { width: 1400, height: 787, deviceScaleFactor: 1, mobile: false });
  await send('Emulation.setDefaultBackgroundColorOverride', { color: { r: 13, g: 11, b: 20, a: 1 } });
  await send('Page.setDocumentContent', { frameId, html: buildHeroBannerHtml(rawB64, site.domain) });
  await send('Runtime.evaluate', { expression: 'document.fonts.ready', awaitPromise: true });
  await sleep(200);
  const heroShot = await send('Page.captureScreenshot', { format: 'jpeg', quality: 92 });
  const heroBuf = Buffer.from(heroShot.data, 'base64');
  fs.writeFileSync(path.join(PUB_CS_DIR, `${site.slug}-hero.jpg`), heroBuf);
  fs.writeFileSync(path.join(DIST_CS_DIR, `${site.slug}-hero.jpg`), heroBuf);

  console.log(`Rendered website SS visual & hero for: ${site.slug} (${site.domain})`);
}

ws.close();
chrome.kill();
process.exit(0);
