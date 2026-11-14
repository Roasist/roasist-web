#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Full comprehensive updater for public/hakkimizda/index.html.
Localizes all texts, cleans all KOTA leftovers, synchronizes SSR HTML + Next.js Flight JSON.
"""

import json
import os
import re

ROOT = "/home/antigravity/Roasist/roasist-web"
HTML_PATH = os.path.join(ROOT, "public", "hakkimizda", "index.html")

with open(HTML_PATH, "r", encoding="utf-8") as f:
    full_content = f.read()

start_marker = "self.__next_f.push([1, "
end_marker = "])</script></body></html>"

start_idx = full_content.find(start_marker)
end_idx = full_content.find(end_marker)

if start_idx == -1 or end_idx == -1:
    raise ValueError("Could not locate flight stream boundaries in HTML!")

ssr_html = full_content[:start_idx]
flight_json_str = full_content[start_idx + len(start_marker):end_idx]
flight_str = json.loads(flight_json_str)

# 1. Navigation Menu Replacement in SSR HTML
old_nav = '''<nav class="PrimaryNavigation_navigation__l8Jgb"><ul><li><a href="/referanslar//">Work</a></li><li><a href="https://kota.co.uk/agency/">Hakkımızda</a></li><li><div class="PrimaryNavigation_parent__bfX37">Services<figure class="PrimaryNavigation_toggleSign__XESvT "><span class="PrimaryNavigation_toggleInner__Lz3QB"><span class="PrimaryNavigation_toggleLine__QUlfd"></span><span class="PrimaryNavigation_toggleLine__QUlfd"></span></span></figure></div><ul class="PrimaryNavigation_submenu__ryGWu "><li><a href="https://kota.co.uk/service/brand-strategy-and-identity/">Brand strategy &amp; identity</a></li><li><a href="https://kota.co.uk/service/web-design-development/">Web design &amp; development</a></li><li><a href="https://kota.co.uk/service/growth-marketing/">Growth marketing</a></li></ul></li><li><a href="/blog//">Blog</a></li><li><a href="https://kota.co.uk/culture/">Culture</a></li><li><a href="https://kota.co.uk/contact/">Contact</a></li></ul>'''

new_nav = '''<nav class="PrimaryNavigation_navigation__l8Jgb"><ul><li><a href="/referanslar">Referanslar</a></li><li><a href="/hakkimizda">Hakkımızda</a></li><li><div class="PrimaryNavigation_parent__bfX37">Hizmetler<figure class="PrimaryNavigation_toggleSign__XESvT "><span class="PrimaryNavigation_toggleInner__Lz3QB"><span class="PrimaryNavigation_toggleLine__QUlfd"></span><span class="PrimaryNavigation_toggleLine__QUlfd"></span></span></figure></div><ul class="PrimaryNavigation_submenu__ryGWu "><li><a href="/hizmetler/360-derece-dijital-pazarlama-yonetimi">360° Dijital Pazarlama &amp; Marka</a></li><li><a href="/hizmetler/web-tasarim">Web Tasarım &amp; Geliştirme</a></li><li><a href="/hizmetler/performans-pazarlamasi">Performans Pazarlaması &amp; SEO</a></li></ul></li><li><a href="/blog">Blog</a></li><li><a href="/hizmetler/grafik-tasarim">Kreatif Stüdyo</a></li><li><a href="/iletisim">İletişim</a></li></ul>'''

if old_nav in ssr_html:
    ssr_html = ssr_html.replace(old_nav, new_nav)
    print("Nav menu updated in SSR HTML")

# 2. SSR Team Bio Replacement
old_james_bio = '''<div class="Team_bio__EVTbV"><p>James fell in love with design when he was 17. </p>
<p>After a stint at college where he mostly learnt that college wasn’t for him, he busked his way into the industry and had eight great years as a freelance graphic designer contracting for some of the biggest agencies in London before setting up KOTA with Jonny Bradford in 2012.</p>
</div>'''

new_roasist_bio = '''<div class="Team_bio__EVTbV"><p>Büyüme &amp; Strateji Liderliği Ekibimiz.</p>
<p>Google Ads, Meta, TikTok ve Yandex ekosistemlerinde büyük ölçekli bütçe yönetimi, çok kanallı büyüme hunileri ve birim kârlılık (ROAS) optimizasyonu konusunda 10 yılı aşkın deneyimle markalarımızın büyüme hedeflerini sahiplenir.</p>
</div>'''

if old_james_bio in ssr_html:
    ssr_html = ssr_html.replace(old_james_bio, new_roasist_bio)
    print("James bio updated in SSR HTML")

# 3. Culture button in SSR HTML
ssr_html = ssr_html.replace('href="culture"', 'href="/iletisim"')

# 4. Yoast Schema / JSON-LD in SSR HTML
ROASIST_DESC = "Roasist; geleneksel pazarlama yöntemlerini modern veri analitiğiyle birleştiren, kârlılık ve büyüme sorumluluğunu üstlenen yeni nesil dijital pazarlama ve performans ajansıdır."
ssr_html = ssr_html.replace("We are KOTA, award-winning Creative Studio based in London &amp; New York. Meet our expert team of creative designers, developers and strategists.", ROASIST_DESC)
ssr_html = ssr_html.replace("We are KOTA, award-winning Creative Studio based in London & New York. Meet our expert team of creative designers, developers and strategists.", ROASIST_DESC)
ssr_html = ssr_html.replace("https://kota.co.uk/agency/", "https://www.roasist.com/hakkimizda/")
ssr_html = ssr_html.replace("https://kota.co.uk/agency", "https://www.roasist.com/hakkimizda/")
ssr_html = ssr_html.replace("https://kota.co.uk/", "https://www.roasist.com/")
ssr_html = ssr_html.replace('"name":"KOTA"', '"name":"Roasist"')
ssr_html = ssr_html.replace('"alternateName":"KOTA creative"', '"alternateName":"Roasist Dijital Pazarlama"')
ssr_html = ssr_html.replace("https://www.facebook.com/kotacreative/", "https://www.facebook.com/roasist/")
ssr_html = ssr_html.replace("https://x.com/kotacreative", "https://x.com/roasist")

# 5. In Flight string: replace all remaining metadata & descriptions
flight_str = flight_str.replace("We are KOTA, award-winning Creative Studio based in London & New York. Meet our expert team of creative designers, developers and strategists.", ROASIST_DESC)
flight_str = flight_str.replace("We are KOTA, award-winning Creative Studio based in London &amp; New York. Meet our expert team of creative designers, developers and strategists.", ROASIST_DESC)
flight_str = flight_str.replace("https://kota.co.uk/agency/", "https://www.roasist.com/hakkimizda/")
flight_str = flight_str.replace("https://kota.co.uk/agency", "https://www.roasist.com/hakkimizda/")
flight_str = flight_str.replace("https://kota.co.uk/", "https://www.roasist.com/")
flight_str = flight_str.replace('"name":"KOTA"', '"name":"Roasist"')
flight_str = flight_str.replace('"alternateName":"KOTA creative"', '"alternateName":"Roasist Dijital Pazarlama"')
flight_str = flight_str.replace('"twitter:site","content":"@kotacreative"', '"twitter:site","content":"@roasist"')
flight_str = flight_str.replace("https://www.facebook.com/kotacreative/", "https://www.facebook.com/roasist/")
flight_str = flight_str.replace("https://x.com/kotacreative", "https://x.com/roasist")

# Replace culture link in flight
flight_str = flight_str.replace('"href":"culture"', '"href":"/iletisim"')

# Re-serialize Flight string
new_flight_json = json.dumps(flight_str, ensure_ascii=False).replace("<", "\\u003c")

final_html = ssr_html + start_marker + new_flight_json + end_marker

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(final_html)

print("Finished comprehensive update of public/hakkimizda/index.html!")
