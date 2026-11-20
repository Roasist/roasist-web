#!/usr/bin/env python3
"""
Pre-Launch Step 3:
1. Fixes Contact & Start-Your-Project forms (TR & EN):
   - Removes 'Lorem Ipsum' & 'Branding' -> replaces with 'Yapay Zeka Aramaları (AEO & GEO)'
     & 'Performans Pazarlaması (Ads)' (and English equivalents).
   - Fixes 'Budget (£)' & untranslated form labels/placeholders in TR and EN.
   - Fixes broken '/faqs' link -> '/hizmetler/' (TR) and '/en/services/' (EN).
   - Injects a capturing static-safe form handler (`FormSubmit.co` AJAX to info@roasist.com +
     GTM `generate_lead` event + zero-layout-shift button state + instant WhatsApp/Email card)
     so static form submissions NEVER fail with 405.
2. Creates `/en/start-your-project/index.html` and links `start-your-project` <-> `en/start-your-project`.
3. Updates English `FloatingStartButton` across all `/en/*` pages (`Projeye Başla` -> `Start Your Project`).
"""
import glob
import json
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

from update_about_page import parse_flight_stream, serialize_flight_stream
from update_tiktok_yandex_pages import extract_flight_chunks

FORM_STYLE_ID = "roasist-static-form-css"
FORM_SCRIPT_ID = "roasist-static-form-handler"

FORM_CSS = f"""<style id="{FORM_STYLE_ID}">
.roasist-form-status {{
  grid-column: 1 / -1;
  width: 100%;
  margin-top: 1.25rem;
  padding: 1.5rem;
  border-radius: 16px;
  background: #f8fafc;
  border: 1px solid rgba(15, 23, 42, 0.1);
  color: #0f172a;
  display: flex;
  flex-direction: column;
  gap: 0.9rem;
}}
.roasist-form-status__title {{
  font-size: 1.05rem;
  font-weight: 600;
  letter-spacing: -0.02em;
  margin: 0;
  color: #0f172a;
}}
.roasist-form-status__desc {{
  font-size: 0.94rem;
  line-height: 1.5;
  margin: 0;
  color: #475569;
}}
.roasist-form-status__actions {{
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-top: 0.25rem;
}}
.roasist-form-status__btn {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.65rem 1.2rem;
  border-radius: 999px;
  font-size: 0.875rem;
  font-weight: 600;
  text-decoration: none;
  transition: transform 160ms cubic-bezier(0.22, 1, 0.36, 1), opacity 160ms ease;
}}
.roasist-form-status__btn--primary {{
  background: #0f172a;
  color: #ffffff !important;
}}
.roasist-form-status__btn--outline {{
  background: transparent;
  color: #0f172a !important;
  border: 1px solid rgba(15, 23, 42, 0.22);
}}
.roasist-form-status__btn:hover {{
  transform: translateY(-1px);
}}
</style>"""


def build_form_script(is_en: bool) -> str:
    cfg = {
        "sending": "Sending..." if is_en else "Gönderiliyor...",
        "sentBtn": "Request Received ✓" if is_en else "Talebiniz Alındı ✓",
        "okTitle": "Thank you! Your project inquiry has been received." if is_en else "Teşekkürler! Proje talebiniz başarıyla alındı.",
        "okDesc": (
            "Our strategy team will review your details and reply within the same business day. For immediate priority, you can also send your brief directly via WhatsApp or Email below:"
            if is_en
            else "Uzman ekibimiz bilgilerinizi inceleyerek aynı iş günü içinde sizinle iletişime geçecektir. Dilerseniz tek tıkla WhatsApp hattımızdan veya e-posta ile de anında iletebilirsiniz:"
        ),
        "waBtn": "Confirm via WhatsApp →" if is_en else "WhatsApp ile Hızlı Onayla →",
        "mailBtn": "Send via Email" if is_en else "E-posta Uygulamasıyla Gönder",
        "waIntro": "Hello Roasist, I submitted a project inquiry on your website:" if is_en else "Merhaba Roasist, web sitenizden strateji ve teklif formu doldurdum:",
        "subject": "New Project Inquiry — Roasist Web" if is_en else "Yeni Proje & Teklif Talebi — Roasist Web",
    }
    return f"""<script id="{FORM_SCRIPT_ID}">
(function() {{
  var CFG = {json.dumps(cfg, ensure_ascii=False)};
  function handleFormSubmit(e) {{
    var form = e.target;
    if (!form || !form.classList || !form.classList.contains('Form_form___noC4')) return;
    e.preventDefault();
    e.stopImmediatePropagation();

    var hp = form.querySelector('.Form_honeypot__2s3Fd');
    if (hp && hp.value) return;

    var btn = form.querySelector('button[type="submit"]');
    var btnLabel = btn ? btn.querySelector('span') : null;
    if (btn) {{
      var rect = btn.getBoundingClientRect();
      btn.style.minWidth = Math.ceil(rect.width) + 'px';
      btn.style.minHeight = Math.ceil(rect.height) + 'px';
      btn.disabled = true;
    }}
    if (btnLabel) btnLabel.textContent = CFG.sending;

    var fd = new FormData(form);
    var firstName = (fd.get('firstName') || '').toString().trim();
    var lastName = (fd.get('lastName') || '').toString().trim();
    var fullName = (firstName + ' ' + lastName).trim();
    var email = (fd.get('email') || '').toString().trim();
    var budget = (fd.get('budget') || '-').toString().trim() || '-';
    var message = (fd.get('message') || '-').toString().trim() || '-';

    var services = [];
    form.querySelectorAll('input[name="interestedIn"]:checked').forEach(function(cb) {{
      var lbl = cb.closest('label') || (cb.id ? form.querySelector('label[for="' + cb.id + '"]') : null) || cb.parentElement;
      if (lbl && lbl.textContent) services.push(lbl.textContent.trim());
    }});
    var serviceStr = services.length ? services.join(', ') : '-';

    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({{
      event: 'generate_lead',
      form_location: window.location.pathname,
      lead_services: serviceStr
    }});

    var summaryLines = [
      CFG.waIntro,
      '',
      'Name: ' + fullName,
      'Email: ' + email,
      'Services: ' + serviceStr,
      'Budget: ' + budget,
      'Message: ' + message,
      'Page: ' + window.location.href
    ];
    var waUrl = 'https://wa.me/905405075350?text=' + encodeURIComponent(summaryLines.join('\\n'));
    var mailUrl = 'mailto:info@roasist.com?subject=' + encodeURIComponent(CFG.subject + ' (' + fullName + ')') + '&body=' + encodeURIComponent(summaryLines.join('\\n'));

    fetch('https://formsubmit.co/ajax/info@roasist.com', {{
      method: 'POST',
      headers: {{ 'Content-Type': 'application/json', 'Accept': 'application/json' }},
      body: JSON.stringify({{
        _subject: CFG.subject + ' — ' + fullName,
        name: fullName,
        email: email,
        services: serviceStr,
        budget: budget,
        message: message,
        page: window.location.href,
        _captcha: 'false'
      }})
    }}).catch(function() {{}}).finally(function() {{
      if (btnLabel) btnLabel.textContent = CFG.sentBtn;
      var box = form.querySelector('.roasist-form-status');
      if (!box) {{
        box = document.createElement('div');
        box.className = 'roasist-form-status';
        form.appendChild(box);
      }}
      box.innerHTML =
        '<p class="roasist-form-status__title">' + CFG.okTitle + '</p>' +
        '<p class="roasist-form-status__desc">' + CFG.okDesc + '</p>' +
        '<div class="roasist-form-status__actions">' +
          '<a class="roasist-form-status__btn roasist-form-status__btn--primary" href="' + waUrl + '" target="_blank" rel="noopener noreferrer">' + CFG.waBtn + '</a>' +
          '<a class="roasist-form-status__btn roasist-form-status__btn--outline" href="' + mailUrl + '">' + CFG.mailBtn + '</a>' +
        '</div>';
    }});
  }}
  document.addEventListener('submit', handleFormSubmit, true);
}})();
</script>"""


def apply_replacements_flight_safe(text: str, replacements: list) -> str:
    matches, _, full = extract_flight_chunks(text)
    if not matches:
        out = text
        for old, new in replacements:
            out = out.replace(old, new)
        return out

    recs = parse_flight_stream(full)
    for rec in recs:
        val = rec[2]
        for old, new in replacements:
            val = val.replace(old, new)
        rec[2] = val
    new_full = serialize_flight_stream(recs)

    out_parts = []
    last_end = 0
    for idx, m in enumerate(matches):
        seg = text[last_end : m.start()]
        for old, new in replacements:
            seg = seg.replace(old, new)
        out_parts.append(seg)
        if idx == 0:
            encoded = json.dumps(new_full, ensure_ascii=False)[1:-1].replace("</", "\\u003c/")
            out_parts.append(m.group(1) + encoded + m.group(3))
        else:
            out_parts.append("")
        last_end = m.end()
    tail = text[last_end:]
    for old, new in replacements:
        tail = tail.replace(old, new)
    out_parts.append(tail)
    return "".join(out_parts)


def upgrade_form_page(path: str, is_en: bool, is_gh_pages: bool):
    text = open(path, "r", encoding="utf-8").read()
    prefix = "/roasist-web" if is_gh_pages else ""

    if is_en:
        svcs_href = f"{prefix}/en/services/"
        priv_href = f"{prefix}/en/privacy-policy-and-terms-of-use/"
        reps = [
            ('href="/faqs" target="_blank"', f'href="{svcs_href}"'),
            ('href="/roasist-web/faqs" target="_blank"', f'href="{svcs_href}"'),
            ('"href":"/faqs","target":"_blank"', f'"href":"{svcs_href}"'),
            ('"href":"/roasist-web/faqs","target":"_blank"', f'"href":"{svcs_href}"'),
            ("İlgilendiğiniz Hizmet :", "Services You Need:"),
            ("Web Tasarım &amp; Geliştirme", "Web Design &amp; UI/UX"),
            ("Web Tasarım & Geliştirme", "Web Design & UI/UX"),
            (">Branding<", ">Performance Marketing (Ads)<"),
            ('"Branding"', '"Performance Marketing (Ads)"'),
            ("SEO &amp; İçerik Stratejisi", "Enterprise SEO"),
            ("SEO & İçerik Stratejisi", "Enterprise SEO"),
            (">E-Ticaret<", ">Conversion Optimization (CRO)<"),
            ('"E-Ticaret"', '"Conversion Optimization (CRO)"'),
            ("360° Dijital Pazarlama", "360° Digital Growth"),
            ("Kreatif &amp; Grafik Tasarım", "Graphic &amp; Ad Creative"),
            ("Kreatif & Grafik Tasarım", "Graphic & Ad Creative"),
            ("Lorem Ipsum", "AI Search (AEO & GEO)"),
            ("Bütçe planlaması ve hizmet kapsamlarımız hakkında detaylı bilgiye", "Explore detailed scope and capabilities across"),
            ("buradan ulaşabilirsiniz", "our services page"),
            ("Budget (£)", "Monthly Budget ($ / €)"),
            ("Message", "Project Goals & Notes"),
            ("Dosya Ekle", "Attach Brief"),
            ("Roasist dijital büyüme bültenini almak istiyorum", "Subscribe to Roasist digital growth insights"),
            ("Verilerimin Gizlilik Politikası ve KVKK kapsamında güvenle işlenmesini kabul ediyorum.", f"I agree to the processing of my information under the Privacy Policy."),
            (">Gönder<", ">Send Inquiry<"),
            ("Gönder<!-- --> ", "Send Inquiry<!-- --> "),
            ('"Gönder"', '"Send Inquiry"'),
        ]
    else:
        svcs_href = f"{prefix}/hizmetler/"
        reps = [
            ('href="/faqs" target="_blank"', f'href="{svcs_href}"'),
            ('href="/roasist-web/faqs" target="_blank"', f'href="{svcs_href}"'),
            ('"href":"/faqs","target":"_blank"', f'"href":"{svcs_href}"'),
            ('"href":"/roasist-web/faqs","target":"_blank"', f'"href":"{svcs_href}"'),
            (">Branding<", ">Performans Pazarlaması (Ads)<"),
            ('"Branding"', '"Performans Pazarlaması (Ads)"'),
            ("Lorem Ipsum", "Yapay Zeka Aramaları (AEO & GEO)"),
            ("First name*", "Adınız*"),
            ("Last name*", "Soyadınız*"),
            ("Email*", "E-posta Adresiniz*"),
            ("Budget (£)", "Aylık Bütçe Aralığı (₺ / $)"),
            ('placeholder="Message"', 'placeholder="Projeniz veya Hedefleriniz"'),
            ('"placeholder":"Message"', '"placeholder":"Projeniz veya Hedefleriniz"'),
        ]

    text = apply_replacements_flight_safe(text, reps)

    # Inject CSS & Capturing Form Handler idempotently
    style_re = re.compile(rf'<style id="{FORM_STYLE_ID}">.*?</style>', re.S)
    if style_re.search(text):
        text = style_re.sub(FORM_CSS, text, count=1)
    else:
        head_end = text.find("</head>")
        text = text[:head_end] + FORM_CSS + text[head_end:]

    script_block = build_form_script(is_en=is_en)
    script_re = re.compile(rf'<script id="{FORM_SCRIPT_ID}">.*?</script>', re.S)
    if script_re.search(text):
        text = script_re.sub(lambda _: script_block, text, count=1)
    else:
        body_end = text.rfind("</body>")
        text = text[:body_end] + script_block + text[body_end:]

    open(path, "w", encoding="utf-8").write(text)
    print(f"[OK] Upgraded form & fixed /faqs in {os.path.relpath(path, REPO_ROOT)}")


def create_en_start_your_project(root_dir: str, is_gh_pages: bool):
    src = os.path.join(root_dir, "en", "contact-us", "index.html")
    dst = os.path.join(root_dir, "en", "start-your-project", "index.html")
    tr_syp = os.path.join(root_dir, "start-your-project", "index.html")
    if not os.path.exists(src):
        return

    os.makedirs(os.path.dirname(dst), exist_ok=True)
    text = open(src, "r", encoding="utf-8").read()
    reps = [
        ("Contact Us | Roasist Digital Marketing Agency", "Start Your Project | Roasist Digital Marketing Agency"),
        ('data-tr-route="/iletisim/"', 'data-tr-route="/start-your-project/"'),
        ('data-en-route="/en/contact-us/"', 'data-en-route="/en/start-your-project/"'),
        ("/en/contact-us/", "/en/start-your-project/"),
    ]
    text = apply_replacements_flight_safe(text, reps)
    open(dst, "w", encoding="utf-8").write(text)
    print(f"[OK] Created {os.path.relpath(dst, REPO_ROOT)}")

    if os.path.exists(tr_syp):
        t_tr = open(tr_syp, "r", encoding="utf-8").read()
        t_tr = apply_replacements_flight_safe(t_tr, [
            ('data-en-route="/en/contact-us/"', 'data-en-route="/en/start-your-project/"'),
            ("İletişim | Roasist Dijital Pazarlama Ajansı", "Projeye Başlayın | Roasist Dijital Pazarlama Ajansı"),
        ])
        open(tr_syp, "w", encoding="utf-8").write(t_tr)


def fix_en_floating_buttons(root_dir: str, is_gh_pages: bool):
    en_dir = os.path.join(root_dir, "en")
    if not os.path.exists(en_dir):
        return
    prefix = "/roasist-web" if is_gh_pages else ""
    target_href = f"{prefix}/en/start-your-project/"
    count = 0
    for f in sorted(glob.glob(os.path.join(en_dir, "**", "*.html"), recursive=True)):
        orig = open(f, "r", encoding="utf-8").read()
        upd = orig
        # Replace SSR FloatingStartButton href & Turkish label on English pages
        upd = re.sub(
            r'(<a class="FloatingStartButton_button__Ncnrf" href=")[^"]*(".*?<span class="FloatingStartButton_text__70x9M"><span>)(?:Projeye Başlayın|Projeye Başla)(</span>)',
            rf'\g<1>{target_href}\g<2>Start Your Project\g<3>',
            upd,
        )
        # Also ensure runtime route map includes start-your-project
        if "'start-your-project':" not in upd and "'contact-us': '/en/contact-us/'," in upd:
            upd = upd.replace(
                "'contact-us': '/en/contact-us/',",
                "'contact-us': '/en/contact-us/',\n    'start-your-project': '/en/start-your-project/',",
            )
        if upd != orig:
            open(f, "w", encoding="utf-8").write(upd)
            count += 1
    print(f"[OK] Updated English FloatingStartButton on {count} pages in {os.path.relpath(en_dir, REPO_ROOT)}/")


def main():
    for root_name, is_gh in [("public", False), ("dist", True)]:
        root_dir = os.path.join(REPO_ROOT, root_name)
        if not os.path.exists(root_dir):
            continue
        for rel, is_en in [
            ("iletisim/index.html", False),
            ("start-your-project/index.html", False),
            ("en/contact-us/index.html", True),
        ]:
            p = os.path.join(root_dir, rel)
            if os.path.exists(p):
                upgrade_form_page(p, is_en=is_en, is_gh_pages=is_gh)

        create_en_start_your_project(root_dir, is_gh_pages=is_gh)
        fix_en_floating_buttons(root_dir, is_gh_pages=is_gh)


if __name__ == "__main__":
    main()
