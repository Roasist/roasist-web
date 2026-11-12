import os

PUBLIC_DIR = "/home/antigravity/Roasist/roasist-web/public"

# Official SVG vector logos (transparent background, sitting directly on Hero & Footer like KOTA's badges)
badges_light = {
    # 1. Official Google Partner (4-color Google 'G' + Google PARTNER lockup)
    "badge-google-partner.svg": '''<svg xmlns="http://www.w3.org/2000/svg" width="132" height="40" viewBox="0 0 132 40" fill="none">
  <g transform="translate(2, 6) scale(0.107)">
    <path d="M255.878 133.451c0-10.734-.871-18.567-2.756-26.69H130.55v48.448h71.947c-1.45 12.04-9.283 30.172-26.69 42.356l-.244 1.622 38.755 30.023 2.685.268c24.659-22.774 38.875-56.282 38.875-96.027" fill="#4285F4"/>
    <path d="M130.55 261.1c35.248 0 64.839-11.605 86.453-31.622l-41.196-31.913c-11.024 7.688-25.82 13.055-45.257 13.055-34.523 0-63.824-22.773-74.269-54.25l-1.531.13-40.298 31.187-.527 1.465C35.393 231.798 79.49 261.1 130.55 261.1" fill="#34A853"/>
    <path d="M56.281 156.37c-2.756-8.123-4.351-16.827-4.351-25.82 0-8.994 1.595-17.697 4.206-25.82l-.073-1.73L15.26 71.312l-1.335.635C5.077 89.644 0 109.517 0 130.55s5.077 40.905 13.925 58.602l42.356-32.782" fill="#FBBC05"/>
    <path d="M130.55 50.479c24.514 0 41.05 10.589 50.479 19.438l36.844-35.974C195.245 12.91 165.798 0 130.55 0 79.49 0 35.393 29.301 13.925 71.947l42.211 32.783c10.59-31.477 39.891-54.251 74.414-54.251" fill="#EB4335"/>
  </g>
  <text x="38" y="19" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="14.5" font-weight="700" letter-spacing="-0.02em" fill="#111827">Google</text>
  <rect x="38" y="23.5" width="58" height="11.5" rx="2.5" fill="#4285F4"/>
  <text x="43" y="32" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="8.2" font-weight="700" letter-spacing="0.09em" fill="#FFFFFF">PARTNER</text>
</svg>''',

    # 2. Official Meta Business Partner (Official Meta Infinity Loop + Meta Business Partner lockup)
    "badge-meta-partner.svg": '''<svg xmlns="http://www.w3.org/2000/svg" width="165" height="40" viewBox="0 0 165 40" fill="none">
  <defs>
    <linearGradient id="metaGrad" x1="2" y1="10" x2="36" y2="30" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#0064E0"/>
      <stop offset="50%" stop-color="#0082FB"/>
      <stop offset="100%" stop-color="#0099FF"/>
    </linearGradient>
  </defs>
  <g transform="translate(-7, -2) scale(1.08)">
    <path d="M32.2 14C29.4 14 27.1 15.8 25.1 18.6C23.8 16.5 21.8 14 18.7 14C14.1 14 10.5 18.3 10.5 23.7C10.5 27.2 12.6 29.8 15.6 29.8C18.1 29.8 20.1 28.2 22.3 24.9L24.1 22.1L25.5 24.4C27.8 28.1 29.8 29.8 32.6 29.8C35.8 29.8 38.3 27.1 38.3 23.5C38.3 18.1 35.9 14 32.2 14ZM16.1 26.5C14.6 26.5 13.7 25.3 13.7 23.5C13.7 19.9 15.9 17.2 18.5 17.2C20.3 17.2 21.7 18.6 23.2 21.1L21.3 24C19.4 26.9 17.8 26.5 16.1 26.5ZM32.3 26.5C30.6 26.5 29.1 25.2 27.3 22.3L25.9 20.1C27.5 17.9 29.3 17.2 31.3 17.2C33.8 17.2 35.1 19.9 35.1 23.4C35.1 25.3 34 26.5 32.3 26.5Z" fill="url(#metaGrad)"/>
  </g>
  <text x="41" y="19" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="14.5" font-weight="700" letter-spacing="-0.02em" fill="#111827">Meta</text>
  <text x="41" y="31.5" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="9.2" font-weight="700" letter-spacing="0.06em" fill="#475569">BUSINESS PARTNER</text>
</svg>''',

    # 3. Official TikTok Marketing Partner (3D Layered Cyan #25F4EE + Red #FE2C55 + Core Note)
    "badge-tiktok-partner.svg": '''<svg xmlns="http://www.w3.org/2000/svg" width="170" height="40" viewBox="0 0 170 40" fill="none">
  <circle cx="17" cy="20" r="14.5" fill="#0F172A"/>
  <g transform="translate(5.5, 8.5) scale(0.76)">
    <path d="M16.2 3.5V17.4C16.2 19.4 14.6 21 12.6 21C10.6 21 9 19.4 9 17.4C9 15.4 10.6 13.8 12.6 13.8C13 13.8 13.4 13.9 13.8 14V10.2C13.4 10.1 13 10.1 12.6 10.1C8.6 10.1 5.3 13.4 5.3 17.4C5.3 21.4 8.6 24.7 12.6 24.7C16.6 24.7 19.9 21.4 19.9 17.4V10.6C21.4 11.7 23.3 12.3 25.3 12.3V8.6C22.2 8.6 19.7 6.3 19.5 3.5H16.2Z" fill="#25F4EE" transform="translate(-1.4, -1.1)"/>
    <path d="M16.2 3.5V17.4C16.2 19.4 14.6 21 12.6 21C10.6 21 9 19.4 9 17.4C9 15.4 10.6 13.8 12.6 13.8C13 13.8 13.4 13.9 13.8 14V10.2C13.4 10.1 13 10.1 12.6 10.1C8.6 10.1 5.3 13.4 5.3 17.4C5.3 21.4 8.6 24.7 12.6 24.7C16.6 24.7 19.9 21.4 19.9 17.4V10.6C21.4 11.7 23.3 12.3 25.3 12.3V8.6C22.2 8.6 19.7 6.3 19.5 3.5H16.2Z" fill="#FE2C55" transform="translate(1.4, 1.1)"/>
    <path d="M16.2 3.5V17.4C16.2 19.4 14.6 21 12.6 21C10.6 21 9 19.4 9 17.4C9 15.4 10.6 13.8 12.6 13.8C13 13.8 13.4 13.9 13.8 14V10.2C13.4 10.1 13 10.1 12.6 10.1C8.6 10.1 5.3 13.4 5.3 17.4C5.3 21.4 8.6 24.7 12.6 24.7C16.6 24.7 19.9 21.4 19.9 17.4V10.6C21.4 11.7 23.3 12.3 25.3 12.3V8.6C22.2 8.6 19.7 6.3 19.5 3.5H16.2Z" fill="#FFFFFF"/>
  </g>
  <text x="39" y="19" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="14.5" font-weight="700" letter-spacing="-0.02em" fill="#111827">TikTok</text>
  <text x="39" y="31.5" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="9.2" font-weight="700" letter-spacing="0.06em" fill="#475569">MARKETING PARTNER</text>
</svg>''',

    # 4. Official Yandex Advertising Partner (Official Yandex Red #FC3F1D Circle + 'Я' Mark + Yandex Partner lockup)
    "badge-ai-seo.svg": '''<svg xmlns="http://www.w3.org/2000/svg" width="142" height="40" viewBox="0 0 142 40" fill="none">
  <circle cx="17" cy="20" r="14.5" fill="#FC3F1D"/>
  <path d="M19.2 11.5H16.5C13.6 11.5 11.8 13.2 11.8 16.0C11.8 18.2 12.9 19.7 14.9 20.5L11.4 28.3H14.5L17.7 21.2H18.9V28.3H21.8V11.5H19.2ZM18.9 18.7H16.8C15.4 18.7 14.7 17.8 14.7 16.2C14.7 14.5 15.5 13.8 16.8 13.8H18.9V18.7Z" fill="#FFFFFF"/>
  <text x="39" y="19" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="14.5" font-weight="700" letter-spacing="-0.02em" fill="#111827"><tspan fill="#FC3F1D">Y</tspan>andex</text>
  <text x="39" y="31.5" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="9.2" font-weight="700" letter-spacing="0.06em" fill="#475569">ADS PARTNER</text>
</svg>'''
}

for name, svg in badges_light.items():
    open(f"{PUBLIC_DIR}/images/{name}", "w", encoding="utf-8").write(svg)
    # Create dark-surface variant (-w.svg) for Footer
    w_name = name.replace(".svg", "-w.svg")
    w_svg = (
        svg.replace('fill="#111827"', 'fill="#FFFFFF"')
           .replace('fill="#475569"', 'fill="#CBD5E1"')
           .replace('circle cx="17" cy="20" r="14.5" fill="#0F172A"', 'circle cx="17" cy="20" r="14.5" fill="#1E293B" stroke="#334155" stroke-width="1"')
    )
    open(f"{PUBLIC_DIR}/images/{w_name}", "w", encoding="utf-8").write(w_svg)

css_8419 = f"{PUBLIC_DIR}/_next/static/css/84191844b30595bc.css"
txt = open(css_8419, "r", encoding="utf-8").read()
marker_p = "/* ROASIST_PARTNER_BADGES_CUSTOM */"
if marker_p in txt:
    txt = txt[:txt.find(marker_p)]
txt += f"""{marker_p}
.Hero_logosInner__D4sWL {{
  gap: 2.5rem !important;
  align-items: center !important;
}}
.Hero_logosInner__D4sWL img,
.Footer_logos__jFNys img {{
  height: 38px !important;
  width: auto !important;
  max-height: 38px !important;
  object-fit: contain !important;
}}
@media (max-width: 768px) {{
  .Hero_logosInner__D4sWL {{
    gap: 1.25rem !important;
  }}
  .Hero_logosInner__D4sWL img,
  .Footer_logos__jFNys img {{
    height: 28px !important;
    max-height: 28px !important;
  }}
}}
"""
open(css_8419, "w", encoding="utf-8").write(txt)

print("Successfully generated borderless official Partner SVG logos!")
