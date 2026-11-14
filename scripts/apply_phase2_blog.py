#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Faz 2 Comprehensive Blog Unification for Roasist Web:
  1. Unifies all 6 Roasist Turkish blog articles into the 1:1 KOTA blog article template
     in BOTH public/blog/<slug>/index.html and dist/blog/<slug>/index.html:
       - Performans-Pazarlamasi-Nedir
       - performans-pazarlamasinda-roas-optimizasyonu
       - kurumsal-seo-ve-yapay-zeka-aramalari-aeo-rehberi
       - 360-dijital-pazarlama-kanallar-arasi-sinerji
       - Veriye-Dayali-Dijital-Pazarlama-Stratejisi-Nedir
       - Reklam-Harcamalarinin-Geri-Donusu-ROAS-Nasil-Hesaplanir
     Removes English "By Emily", "June 1st 2026", broken BriefingBanner, and KOTA share URLs,
     replacing them with Turkish author/date, clean Roasist Share section, "Blog'a Dön", and
     3 real Roasist RelatedPosts cards.
  2. Updates /blog/index.html (and /blog/kategori/*, /blog/etiket/*) in public/ and dist/:
     - Fixes corrupted CSS class names FeaturedBlogPost_featuredPost__aRcs9 & AnimatedFeaturedBlog_container__mnIll
     - Replaces ~20 English KOTA posts and categories with Roasist's 6 Turkish articles and 3 Turkish categories
  3. Updates RelatedPosts_relatedPosts__xfLkb across all 20 /hizmetler/* pages (SSR + Flight)
     with Roasist's 3 core Turkish blog articles.
  4. Updates Homepage Articles_articlesList__CXW8a (public/kota-roasist-local.html & dist/index.html)
     to render the 6 real Turkish blog articles linking directly to /blog/<slug>/ (removing 🎉 emoji).
  5. Updates mapKotaHref in <script data-roasist-runtime> across all pages so /blog/<slug>/ links
     route directly to their article pages instead of redirecting to /blog/.
  6. Removes leftover Astro-only dist/etiket/ and dist/kategori/ directories.
"""

import glob
import html as html_mod
import json
import os
import re
import shutil
import sys
import urllib.parse

ROOT = "/home/antigravity/Roasist/roasist-web"
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from apply_phase1_cleanup import (  # noqa: E402
    BUTTON_ARROW_PATH_D,
    CDN_BASE,
    PUSH_RE,
    find_node_by_class,
    rewrite_flight_in_html,
)

BLOG_CATEGORIES_TR = [
    {
        "node": {
            "slug": "performans-pazarlamasi",
            "name": "Performans Pazarlaması",
            "databaseId": 101,
            "id": "dGVybToxMDE=",
            "isContentNode": False,
            "isTermNode": True,
            "count": 3,
        }
    },
    {
        "node": {
            "slug": "seo-aeo",
            "name": "SEO & AEO",
            "databaseId": 102,
            "id": "dGVybToxMDI=",
            "isContentNode": False,
            "isTermNode": True,
            "count": 1,
        }
    },
    {
        "node": {
            "slug": "dijital-strateji",
            "name": "Dijital Strateji",
            "databaseId": 103,
            "id": "dGVybToxMDM=",
            "isContentNode": False,
            "isTermNode": True,
            "count": 2,
        }
    },
]

BLOG_POSTS_TR = [
    {
        "slug": "Performans-Pazarlamasi-Nedir",
        "db_id": 9101,
        "title": "Performans Pazarlaması Nedir? Markanızı Nasıl Ölçeklendirir?",
        "description": (
            "Performans pazarlaması nedir, hangi reklam kanallarını kapsar ve veri odaklı ROAS "
            "mimarisiyle markanızı nasıl kârlı biçimde ölçeklendirir? Kapsamlı rehber."
        ),
        "cat_slug": "performans-pazarlamasi",
        "cat_name": "Performans Pazarlaması",
        "date_display": "12 Kasım 2026",
        "date_iso": "2026-11-12T09:00:00+03:00",
        "author": "Roasist Strateji Ekibi",
        "img_src": "https://kota-content.b-cdn.net/app/uploads/2025/01/creative-web-design-inspo-2025.png",
        "img_srcset": (
            "https://kota-content.b-cdn.net/app/uploads/2025/01/creative-web-design-inspo-2025.png 1400w, "
            "https://kota-content.b-cdn.net/app/uploads/2025/01/creative-web-design-inspo-2025-500x281.png 500w, "
            "https://kota-content.b-cdn.net/app/uploads/2025/01/creative-web-design-inspo-2025-768x432.png 768w"
        ),
        "img_w": 1400,
        "img_h": 787,
        "prose_html": (
            "<h2>Performans Pazarlaması Nedir?</h2>"
            "<p>Performans pazarlaması; reklam bütçenizin her bir kuruşunun tıklama, form, telefon araması "
            "veya doğrudan satış gibi <strong>ölçülebilir ticari sonuçlara</strong> dönüştüğü veri odaklı "
            "dijital pazarlama yaklaşımıdır. Geleneksel reklamcılığın aksine, yalnızca gerçek etkileşim ve "
            "dönüşüm elde ettiğinizde bütçenizi ölçeklendirirsiniz.</p>"
            "<h2>Hangi Kanallar Performans Pazarlamasının Merkezindedir?</h2>"
            "<p>Roasist olarak performans pazarlaması mimarisini tek bir kanal üzerine değil, kullanıcı "
            "yolculuğunun tamamını kapsayan entegre bir ekosistem üzerine kuruyoruz:</p>"
            "<ul>"
            "<li><strong>Google Ads (Arama, Alışveriş, Performance Max, YouTube):</strong> Satın alma niyeti "
            "en yüksek kullanıcıları tam karar anında yakalar.</li>"
            "<li><strong>Meta Reklamları (Instagram &amp; Facebook):</strong> Görsel hikaye anlatımı ve "
            "gelişmiş Conversions API (CAPI) veri sinyalleriyle talep yaratır ve yeniden pazarlama dönüşümlerini katlar.</li>"
            "<li><strong>TikTok Ads:</strong> Kısa video dinamikleri ve Spark Ads kurgularıyla markanızı "
            "yüksek etkileşimli satış hunisine taşır.</li>"
            "<li><strong>Yandex Ads, Bing Ads &amp; LinkedIn Ads:</strong> Rusya/BDT ihracat pazarlarına, "
            "yüksek satın alma güçlü masaüstü aramalarına ve kurumsal B2B karar vericilere nokta atışı erişim sağlar.</li>"
            "</ul>"
            "<h2>Veri Doğruluğu ve ROAS Optimizasyonu</h2>"
            "<p>Başarılı bir performans pazarlaması stratejisinin temeli <strong>temiz veri</strong>dir. "
            "GA4, Google Tag Manager, Sunucu Taraflı İzleme (Server-Side Tracking) ve Dönüşüm API (CAPI) "
            "kurulumları olmadan yapay zeka algoritmalarının doğru müşteriyi bulması imkânsızdır. Roasist "
            "ekibi olarak reklam hesaplarınızı uçtan uca veri doğruluğuyla yönetiyor, sürdürülebilir ROAS "
            "büyümesi sağlıyoruz.</p>"
        ),
    },
    {
        "slug": "performans-pazarlamasinda-roas-optimizasyonu",
        "db_id": 9102,
        "title": "Performans Pazarlamasında ROAS ve Dönüşüm Oranı Nasıl Artırılır?",
        "description": (
            "Google Ads ve Meta reklamlarında bütçe israfını önleyerek gerçek satış ve yatırım getirisi "
            "(ROAS) büyütmenin veri odaklı adımları."
        ),
        "cat_slug": "performans-pazarlamasi",
        "cat_name": "Performans Pazarlaması",
        "date_display": "8 Kasım 2026",
        "date_iso": "2026-11-08T09:00:00+03:00",
        "author": "Roasist Strateji Ekibi",
        "img_src": "https://kota-content.b-cdn.net/app/uploads/2025/11/brand-trend-2026.png",
        "img_srcset": (
            "https://kota-content.b-cdn.net/app/uploads/2025/11/brand-trend-2026.png 1400w, "
            "https://kota-content.b-cdn.net/app/uploads/2025/11/brand-trend-2026-500x281.png 500w, "
            "https://kota-content.b-cdn.net/app/uploads/2025/11/brand-trend-2026-768x432.png 768w"
        ),
        "img_w": 1400,
        "img_h": 787,
        "prose_html": (
            "<p>Dijital reklam bütçelerinin her geçen yıl daha rekabetçi hale geldiği günümüzde, "
            "<strong>Performans Pazarlaması</strong> yalnızca reklam yayınlamak değil; harcanan her 1 TL’nin "
            "ne kadar ciro ve kâr ürettiğini kuruşu kuruşuna yönetme bilimidir.</p>"
            "<h2>1. Veri Kayıpsız Dönüşüm Ölçümlemesi (GTM, GA4 ve CAPI)</h2>"
            "<p>Reklam algoritmaları (Google Smart Bidding ve Meta Advantage+) yalnızca kendilerine beslenen "
            "dönüşüm sinyalleri kadar akıllıdır. Tarayıcı kısıtlamaları nedeniyle yalnızca klasik piksel takibi "
            "yapmak verilerin önemli bir bölümünün kaybolmasına yol açar.</p>"
            "<ul>"
            "<li><strong>Google Enhanced Conversions (Gelişmiş Dönüşümler):</strong> Birincil taraf dönüşüm "
            "verilerini güvenli biçimde eşleştirerek teklif stratejilerini güçlendirir.</li>"
            "<li><strong>Meta Conversions API (CAPI):</strong> Sunucu taraflı veri aktarımı ile sepet, başvuru "
            "ve satın alma verilerinin eksiksiz raporlanmasını sağlar.</li>"
            "</ul>"
            "<h2>2. Arama Niyeti (Search Intent) ve Negatif Kelime Disiplini</h2>"
            "<p>Google Ads ve Bing Ads yönetiminde en büyük bütçe kaçağı, ticari satın alma niyeti taşımayan "
            "bilgi amaçlı sorgulara tıklama maliyeti ödemektir. Düzenli arama terimi denetimi ve katmanlı "
            "negatif kelime listeleri ile bütçenizi yalnızca satın almaya hazır kullanıcılara yönlendiriyoruz.</p>"
            "<h2>3. Açılış Sayfası Hızı ve Dönüşüm Optimizasyonu (CRO)</h2>"
            "<p>Reklamınız ne kadar güçlü olursa olsun, kullanıcının indiği web sayfası geç açılıyorsa dönüşüm "
            "oranınız hızla düşer. Hızlı, mobil öncelikli ve net harekete geçirici mesajlar (CTA) barındıran "
            "açılış sayfaları hem <strong>Google Kalite Puanınızı</strong> yükseltir hem de tıklama başı "
            "maliyetlerinizi (CPC) düşürür.</p>"
        ),
    },
    {
        "slug": "kurumsal-seo-ve-yapay-zeka-aramalari-aeo-rehberi",
        "db_id": 9103,
        "title": "Kurumsal SEO ve Yapay Zeka Aramaları (AEO) Rehberi",
        "description": (
            "Google sıralamalarının yanı sıra ChatGPT, Perplexity ve Google AI Overviews yanıtlarında "
            "markanızın önerilmesi için uygulanması gereken teknik SEO ve AEO adımları."
        ),
        "cat_slug": "seo-aeo",
        "cat_name": "SEO & AEO",
        "date_display": "28 Ekim 2026",
        "date_iso": "2026-10-28T09:00:00+03:00",
        "author": "Roasist SEO Ekibi",
        "img_src": "https://kota-content.b-cdn.net/app/uploads/2025/12/Design-with-guts.png",
        "img_srcset": (
            "https://kota-content.b-cdn.net/app/uploads/2025/12/Design-with-guts.png 1400w, "
            "https://kota-content.b-cdn.net/app/uploads/2025/12/Design-with-guts-500x281.png 500w, "
            "https://kota-content.b-cdn.net/app/uploads/2025/12/Design-with-guts-768x432.png 768w"
        ),
        "img_w": 1400,
        "img_h": 788,
        "prose_html": (
            "<p>Arama alışkanlıkları hızla dönüşüyor. Potansiyel müşteriler artık yalnızca klasik arama "
            "çubuğuna iki kelimelik sorgular yazmıyor; yapay zeka destekli arama motorlarına doğrudan sorular "
            "sorarak tedarikçi ve marka kararı veriyor.</p>"
            "<h2>AEO (Answer Engine Optimization) Nedir?</h2>"
            "<p><strong>AEO</strong>, web sitenizdeki içeriklerin hem Google’ın Öne Çıkan Snippet "
            "(Featured Snippet) alanlarında hem de ChatGPT, Gemini, Perplexity ve Google AI Overviews gibi "
            "yapay zeka yanıt motorlarında doğrudan güvenilir kaynak olarak gösterilecek şekilde yapılandırılmasıdır.</p>"
            "<h2>Temel Uygulama Kriterleri</h2>"
            "<ul>"
            "<li><strong>Doğrudan Yanıt Blokları:</strong> Her hizmet ve rehber sayfasının girişinde soruyu "
            "net, veriye dayalı ve özet biçimde yanıtlayan semantik paragraflar yer almalıdır.</li>"
            "<li><strong>Schema.org (JSON-LD) Yapısal Verileri:</strong> <code>Service</code>, "
            "<code>FAQPage</code>, <code>Organization</code> ve <code>BreadcrumbList</code> şemaları arama "
            "motoru ve yapay zeka botlarına içeriğin bağlamını hatasız aktarır.</li>"
            "<li><strong>Core Web Vitals ve Teknik SEO Mükemmelliği:</strong> Sunucu ilk yanıt süresi (TTFB) "
            "düşük, temiz HTML hiyerarşisine sahip sayfalar hem tarama bütçesini hem de organik dönüşüm "
            "oranlarını maksimuma çıkarır.</li>"
            "</ul>"
        ),
    },
    {
        "slug": "360-dijital-pazarlama-kanallar-arasi-sinerji",
        "db_id": 9104,
        "title": "360° Dijital Pazarlama Yönetiminde Kanallar Arası Sinerji",
        "description": (
            "SEO, Google Ads, Sosyal Medya Reklamları ve Web Tasarım süreçlerini tek bir büyüme stratejisi "
            "altında birleştirmenin ciroya etkisi."
        ),
        "cat_slug": "dijital-strateji",
        "cat_name": "Dijital Strateji",
        "date_display": "21 Ekim 2026",
        "date_iso": "2026-10-21T09:00:00+03:00",
        "author": "Roasist Strateji Ekibi",
        "img_src": "https://kota-content.b-cdn.net/app/uploads/2025/11/Lovie-awards.png",
        "img_srcset": (
            "https://kota-content.b-cdn.net/app/uploads/2025/11/Lovie-awards.png 1400w, "
            "https://kota-content.b-cdn.net/app/uploads/2025/11/Lovie-awards-500x281.png 500w, "
            "https://kota-content.b-cdn.net/app/uploads/2025/11/Lovie-awards-768x432.png 768w"
        ),
        "img_w": 1400,
        "img_h": 787,
        "prose_html": (
            "<p>Birçok işletmede SEO, Google reklamları, sosyal medya ve web tasarım süreçleri birbirinden "
            "kopuk ilerler. Oysa modern bir müşterinin satın alma yolculuğu çok kanallıdır.</p>"
            "<h2>Çok Kanallı Satın Alma Yolculuğu Nasıl Çalışır?</h2>"
            "<ul>"
            "<li><strong>Farkındalık:</strong> Kullanıcı markanızı ilk kez yaratıcı bir Instagram Reels, "
            "YouTube veya TikTok reklamında keşfeder.</li>"
            "<li><strong>Araştırma:</strong> Birkaç gün sonra Google, Yandex veya Bing’de markanızı ya da "
            "hizmetinizi aradığında güçlü <strong>SEO</strong> ve <strong>Arama Ağı Reklamları</strong> varlığınızla karşılaşır.</li>"
            "<li><strong>Karar &amp; Dönüşüm:</strong> Hızlı açılan, güven veren <strong>Web Sitenize</strong> "
            "girer ve çok kanallı yeniden pazarlama (Retargeting) kampanyalarıyla müşteriye dönüşür.</li>"
            "</ul>"
            "<h2>Neden Tek Çatı Altında 360° Yönetim?</h2>"
            "<p>Roasist’in <strong>360° Dijital Pazarlama Yönetimi</strong> yaklaşımı; kreatif tasarım, "
            "web yazılım, teknik SEO ve performans reklamcılığını tek bir ortak KPI ve veri çatısı altında "
            "birleştirerek bütçe verimliliğinizi ve toplam cironuzu katlar.</p>"
        ),
    },
    {
        "slug": "Veriye-Dayali-Dijital-Pazarlama-Stratejisi-Nedir",
        "db_id": 9105,
        "title": "Veriye Dayalı Dijital Pazarlama Stratejisi Nedir?",
        "description": (
            "Birinci taraf veri (First-Party Data), sunucu taraflı izleme ve sürekli A/B testleriyle "
            "veriye dayalı dijital pazarlama stratejisi nasıl kurulur?"
        ),
        "cat_slug": "dijital-strateji",
        "cat_name": "Dijital Strateji",
        "date_display": "14 Ekim 2026",
        "date_iso": "2026-10-14T09:00:00+03:00",
        "author": "Roasist Analitik Ekibi",
        "img_src": "https://kota-content.b-cdn.net/app/uploads/2026/06/Zero-click-AI-SEO-May-2026-2.png",
        "img_srcset": (
            "https://kota-content.b-cdn.net/app/uploads/2026/06/Zero-click-AI-SEO-May-2026-2.png 1400w, "
            "https://kota-content.b-cdn.net/app/uploads/2026/06/Zero-click-AI-SEO-May-2026-2-500x281.png 500w, "
            "https://kota-content.b-cdn.net/app/uploads/2026/06/Zero-click-AI-SEO-May-2026-2-768x432.png 768w"
        ),
        "img_w": 1400,
        "img_h": 787,
        "prose_html": (
            "<h2>Tahmin Değil, Veri Odaklı Karar Alma</h2>"
            "<p>Veriye dayalı dijital pazarlama; kampanya kurgularından kreatif tasarıma, bütçe dağılımından "
            "açılış sayfası (landing page) deneyimine kadar her kararın <strong>gerçek kullanıcı davranışları "
            "ve dönüşüm verileriyle</strong> şekillendirilmesidir.</p>"
            "<h2>Birinci Taraf Veri (First-Party Data) Neden Kritik?</h2>"
            "<p>Üçüncü taraf çerezlerin etkisini yitirdiği güncel dijital ekosistemde, kendi web sitenizden "
            "ve CRM altyapınızdan topladığınız birinci taraf veriler en değerli büyüme varlığınızdır. Sunucu "
            "taraflı (Server-Side) etiketleme ve gelişmiş dönüşüm takibi sayesinde reklam platformlarındaki "
            "yapay zeka modellerini gerçek satış verilerinizle besliyoruz.</p>"
            "<h2>Sürekli A/B Testi ve Kreatif İterasyon</h2>"
            "<p>Veri yalnızca geçmişi raporlamak için değil, geleceği inşa etmek için kullanılır. Isı "
            "haritaları, oturum kayıtları, mikro dönüşüm hunileri ve kreatif kanca (hook) testleriyle reklam "
            "bütçenizi en yüksek kârlılık üreten segmentlere dinamik biçimde yönlendiriyoruz.</p>"
        ),
    },
    {
        "slug": "Reklam-Harcamalarinin-Geri-Donusu-ROAS-Nasil-Hesaplanir",
        "db_id": 9106,
        "title": "Reklam Harcamalarının Geri Dönüşü (ROAS) Nasıl Hesaplanır?",
        "description": (
            "ROAS nedir, nasıl hesaplanır ve e-ticaret ile lead kampanyalarında ROAS kârlılığı nasıl yükseltilir? "
            "Formüller ve pratik optimizasyon ipuçları."
        ),
        "cat_slug": "performans-pazarlamasi",
        "cat_name": "Performans Pazarlaması",
        "date_display": "5 Ekim 2026",
        "date_iso": "2026-10-05T09:00:00+03:00",
        "author": "Roasist Performans Ekibi",
        "img_src": "https://kota-content.b-cdn.net/app/uploads/2025/07/GEO-AI-search.png",
        "img_srcset": (
            "https://kota-content.b-cdn.net/app/uploads/2025/07/GEO-AI-search.png 1400w, "
            "https://kota-content.b-cdn.net/app/uploads/2025/07/GEO-AI-search-500x281.png 500w, "
            "https://kota-content.b-cdn.net/app/uploads/2025/07/GEO-AI-search-768x432.png 768w"
        ),
        "img_w": 1400,
        "img_h": 787,
        "prose_html": (
            "<h2>ROAS (Return on Ad Spend) Nedir?</h2>"
            "<p><strong>ROAS (Reklam Harcamalarının Geri Dönüşü)</strong>, dijital reklam kampanyalarınıza "
            "yatırdığınız her 1 TL karşılığında kaç TL brüt gelir elde ettiğinizi gösteren en temel performans metriğidir.</p>"
            "<h2>ROAS Formülü ve Örnek Hesaplama</h2>"
            "<p>ROAS hesaplaması son derece nettir: <strong>ROAS = Reklamdan Elde Edilen Gelir / Reklam Harcaması</strong>. "
            "Örneğin bir ay içinde Google ve Meta reklamlarına 100.000 TL bütçe ayırdığınızda bu kampanyalardan "
            "650.000 TL ciro elde ettiyseniz, ROAS değeriniz <strong>6.5 (veya %650)</strong> olur.</p>"
            "<h2>ROAS Nasıl Artırılır?</h2>"
            "<ul>"
            "<li><strong>Negatif Anahtar Kelime ve Kitle Temizliği:</strong> Bütçenizi dönüşüm getirmeyen "
            "aramalardan ve alakasız gösterimlerden koruyun.</li>"
            "<li><strong>Yüksek Dönüşümlü Kreatif ve Teklif Kurgusu:</strong> Tıklama oranını (CTR) artıran "
            "kreatifler tıklama başı maliyetinizi düşürerek ROAS’ı doğrudan yükseltir.</li>"
            "<li><strong>Sepet Ortalaması (AOV) ve CRO Çalışmaları:</strong> Açılış sayfası hızınızı ve "
            "çapraz satış kurgularınızı iyileştirerek aynı trafikle daha yüksek ciro üretin.</li>"
            "</ul>"
        ),
    },
]


# ==============================================================================
# HELPER: BUILD RELATED POSTS CARDS (SSR + FLIGHT)
# ==============================================================================
def build_related_posts_ssr_cards(posts: list) -> str:
    cards = []
    for p in posts:
        cards.append(
            f'<a class="BlogPostCard_post__fNGbL BlogPostCard_small__j18h2" data-animation="grid-item" href="/blog/{p["slug"]}/">'
            f'<div class="BlogPostCard_postImage__Q4k_I">'
            f'<div class="BlogPostCard_tags__RKboe"><span class="BlogPostCard_tag__Dv5HS">{html_mod.escape(p["cat_name"])}</span></div>'
            f'<span class="Image_image__RAAdZ Image_fill__EiIzS">'
            f'<img data-srcset="{p["img_srcset"]}" data-src="{p["img_src"]}" alt="" fetchPriority="low" height="{p["img_h"]}" width="{p["img_w"]}" sizes="auto" class="lazyload"/>'
            f"</span></div>"
            f'<div class="BlogPostCard_postText__V0sxg"><h3>{html_mod.escape(p["title"])}</h3></div></a>'
        )
    return "".join(cards)


def build_related_posts_flight_cards(posts: list, link_id: str, img_id: str) -> list:
    out = []
    for p in posts:
        out.append(
            [
                "$",
                link_id,
                str(p["db_id"]),
                {
                    "className": "BlogPostCard_post__fNGbL BlogPostCard_small__j18h2",
                    "href": f"/blog/{p['slug']}/",
                    "data-animation": "grid-item",
                    "children": [
                        [
                            "$",
                            "div",
                            None,
                            {
                                "className": "BlogPostCard_postImage__Q4k_I",
                                "children": [
                                    [
                                        "$",
                                        "div",
                                        None,
                                        {
                                            "className": "BlogPostCard_tags__RKboe",
                                            "children": [
                                                False,
                                                [
                                                    [
                                                        "$",
                                                        "span",
                                                        p["cat_name"],
                                                        {
                                                            "className": "BlogPostCard_tag__Dv5HS",
                                                            "children": p["cat_name"],
                                                        },
                                                    ]
                                                ],
                                            ],
                                        },
                                    ],
                                    [
                                        "$",
                                        img_id,
                                        None,
                                        {
                                            "image": {
                                                "altText": p["title"],
                                                "srcSet": p["img_srcset"],
                                                "sourceUrl": p["img_src"],
                                                "mediaDetails": {"width": p["img_w"], "height": p["img_h"]},
                                            },
                                            "layout": "fill",
                                        },
                                    ],
                                ],
                            },
                        ],
                        [
                            "$",
                            "div",
                            None,
                            {
                                "className": "BlogPostCard_postText__V0sxg",
                                "children": ["$", "h3", None, {"children": p["title"]}],
                            },
                        ],
                    ],
                },
            ]
        )
    return out


# ==============================================================================
# STEP 1: GENERATE ALL 6 KOTA-STYLED TURKISH BLOG ARTICLES (public/ + dist/)
# ==============================================================================
def build_all_6_blog_detail_pages():
    for base_name in ("public", "dist"):
        is_dist = base_name == "dist"
        template_path = os.path.join(ROOT, base_name, "blog", "Performans-Pazarlamasi-Nedir", "index.html")
        template_html = open(template_path, "r", encoding="utf-8").read()
        icon_url = f"{CDN_BASE}/icon.png" if is_dist else "/icon.png"

        for idx, post in enumerate(BLOG_POSTS_TR):
            related_3 = [BLOG_POSTS_TR[(idx + 1) % 6], BLOG_POSTS_TR[(idx + 2) % 6], BLOG_POSTS_TR[(idx + 3) % 6]]
            canonical_url = f"https://www.roasist.com/blog/{post['slug']}/"
            enc_url = urllib.parse.quote(canonical_url, safe="")

            pushes = list(PUSH_RE.finditer(template_html))
            ssr = template_html[: pushes[0].start()]
            tail = template_html[pushes[0].start() :]

            # 1a. SSR Title & Meta
            ssr = re.sub(
                r"<title>.*?</title>",
                lambda _: f"<title>{html_mod.escape(post['title'])} | Roasist Blog</title>",
                ssr,
                count=1,
                flags=re.S,
            )
            ssr = re.sub(
                r'<meta name="description" content="[^"]*"/>',
                lambda _: f'<meta name="description" content="{html_mod.escape(post["description"], quote=True)}"/>',
                ssr,
                count=1,
            )

            # 1b. Rebuild SSR <article class="BlogPost_blogPost__Mtvlq">...</article> cleanly
            # Keep existing RelatedProjects & LargeCta sections verbatim from template SSR!
            rp_match = re.search(
                r'<section class="RelatedProjects_relatedProjects__opNhl">.*?</section><section class="LargeCta_largeCta__ylf5C">.*?</section>',
                ssr,
                re.S,
            )
            if not rp_match:
                raise RuntimeError(f"Could not locate RelatedProjects+LargeCta in {template_path}")
            rp_and_cta_ssr = rp_match.group(0)

            new_article_ssr = (
                '<article class="BlogPost_blogPost__Mtvlq">'
                '<div class="Hero_hero__mn1R_"><div class="container">'
                '<div class="Hero_left__0LdJX">'
                '<div><span class="FadeIn_container__bjQVL" data-fill="false">'
                f'<div class="Hero_categoriesInner__G68BO"><button class="Hero_category__qOhtb">{html_mod.escape(post["cat_name"])}</button></div>'
                "</span></div>"
                f'<h1><span class="FadeIn_container__bjQVL" data-fill="false"><span>{html_mod.escape(post["title"])}</span></span></h1>'
                "</div>"
                '<div class="Hero_right__AZ10b"><div class="Hero_author__3asj1">'
                '<figure class="Hero_authorImage__h9wNd"><span class="FadeIn_container__bjQVL" data-fill="true">'
                f'<span class="Image_image__RAAdZ Image_fill__EiIzS"><img src="{icon_url}" alt="Roasist" loading="eager" fetchPriority="high" height="512" width="512" sizes="100vw"/></span>'
                "</span></figure>"
                f'<p class="Hero_date__30zpk"><span class="FadeIn_container__bjQVL" data-fill="false"><span>{html_mod.escape(post["date_display"])}</span></span></p>'
                f'<p class="Hero_name__eLY42"><span class="FadeIn_container__bjQVL" data-fill="false"><span>Yazar: <!-- -->{html_mod.escape(post["author"])}</span></span></p>'
                "</div></div>"
                '<figure class="Hero_image__1mu0E"><div class="ImageEnter_image__FSEP_" data-fill="true">'
                f'<span class="Image_image__RAAdZ Image_fill__EiIzS"><img srcSet="{post["img_srcset"]}" src="{post["img_src"]}" alt="{html_mod.escape(post["title"], quote=True)}" loading="eager" fetchPriority="low" height="{post["img_h"]}" width="{post["img_w"]}" sizes="100vw"/></span>'
                "</div></figure></div></div>"
                '<section class="ContentBuilder_contentBuilder__jY2p_">'
                '<section class="Text_text__jOaGN"><span class="FadeInUp_container___uxva" data-fill="false">'
                f'<div class="container"><div class="Text_textInner__lCgQa"><div class="prose">{post["prose_html"]}</div></div></div>'
                "</span></section></section>"
                '<section class="Share_share__5W87u"><span class="FadeIn_container__bjQVL" data-fill="false">'
                '<div class="container"><div class="Share_links__CutyY">'
                "<p>Paylaş : </p>"
                f'<a class="Share_link__ERF_r" href="https://www.linkedin.com/shareArticle?mini=true&amp;url={enc_url}" target="_blank" rel="noopener noreferrer">LinkedIn</a>'
                f'<a class="Share_link__ERF_r" href="https://www.facebook.com/sharer/sharer.php?u={enc_url}" target="_blank" rel="noopener noreferrer">Facebook</a>'
                f'<a class="Share_link__ERF_r" href="https://twitter.com/intent/tweet?&amp;url={enc_url}" target="_blank" rel="noopener noreferrer">𝕏</a>'
                "</div></div></span></section>"
                '<div class="container"><div class="BlogPost_buttonOuter__M9Wmd">'
                '<span class="FadeIn_container__bjQVL" data-fill="false"><div class="Magnetic_magnetic__LncOy" data-fill="false">'
                '<div class="Button_button__JJiqJ" data-direction="backwards"><a class="Button_inner__fnyH6" href="/blog/">'
                '<span class="Button_border__hirH2"></span><span class="Button_text__IZaCD">'
                "<span class=\"Button_textInner__JTTHe\">Blog&#x27;a Dön</span>"
                f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 17.1 15.17" class="Button_buttonArrow__0W9XI"><path d="{BUTTON_ARROW_PATH_D}" fill="currentColor"></path></svg>'
                "</span></a></div></div></span></div></div>"
                '<section class="RelatedPosts_relatedPosts__xfLkb">'
                '<div class="DarkThemeSwitch_cover__hn_xc"></div>'
                '<div class="container"><div class="RelatedPosts_headingOuter__r3TEg">'
                '<p class="RelatedPosts_heading__3kOeH"><span class="FadeInUp_container___uxva" data-fill="false">İlgili Blog Yazıları</span></p>'
                '<div class="RelatedPosts_viewAllLinkDesktop__db363"><span class="FadeInUp_container___uxva" data-fill="false">'
                '<div class="Magnetic_magnetic__LncOy" data-fill="false"><div class="Button_button__JJiqJ Button_white__MQaf2" data-direction="forwards">'
                '<a class="Button_inner__fnyH6" href="/blog/"><span class="Button_border__hirH2"></span><span class="Button_text__IZaCD">'
                '<span class="Button_textInner__JTTHe">Tüm Yazıları Gör</span>'
                f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 17.1 15.17" class="Button_buttonArrow__0W9XI"><path d="{BUTTON_ARROW_PATH_D}" fill="currentColor"></path></svg>'
                "</span></a></div></div></span></div></div></div>"
                f'<div class="AnimatedGrid_grid__otAMD"><div class="container">{build_related_posts_ssr_cards(related_3)}</div></div>'
                '<div class="container"><div class="RelatedPosts_viewAllLinkMobile__joii8"><div class="Magnetic_magnetic__LncOy" data-fill="false">'
                '<div class="Button_button__JJiqJ Button_white__MQaf2" data-direction="forwards"><a class="Button_inner__fnyH6" href="/blog/">'
                '<span class="Button_border__hirH2"></span><span class="Button_text__IZaCD">'
                '<span class="Button_textInner__JTTHe">Tüm Yazıları Gör</span>'
                f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 17.1 15.17" class="Button_buttonArrow__0W9XI"><path d="{BUTTON_ARROW_PATH_D}" fill="currentColor"></path></svg>'
                "</span></a></div></div></div></div></section>"
                f"{rp_and_cta_ssr}"
                "</article>"
            )

            ssr, n_art = re.subn(
                r'<article class="BlogPost_blogPost__Mtvlq">.*?</article>',
                lambda _: new_article_ssr,
                ssr,
                count=1,
                flags=re.S,
            )
            if n_art != 1:
                raise RuntimeError("Failed to replace SSR <article>")

            # Ensure author avatar icon looks crisp in circular badge
            author_css = (
                "/* ROASIST_BLOG_AUTHOR_CSS */"
                ".Hero_authorImage__h9wNd img{object-fit:contain!important;background:#0f172a!important;padding:8px!important;border-radius:50%!important;}"
            )
            if "ROASIST_BLOG_AUTHOR_CSS" not in ssr and "</style>" in ssr:
                ssr = ssr.replace("</style>", author_css + "</style>", 1)

            # 1c. Mutate Flight records (0 urlParts, 2d prose text, f article AST)
            def post_mutator(records):
                for rec in records:
                    kind, key, val = rec
                    if kind == "line" and key == "0":
                        ast0 = json.loads(val)
                        ast0[3]["urlParts"] = ["", "blog", post["slug"]]
                        rec[2] = json.dumps(ast0, ensure_ascii=False, separators=(",", ":"))
                    elif kind == "text" and key == "2d":
                        rec[2] = post["prose_html"]
                    elif kind == "line" and key == "f":
                        ast = json.loads(val)
                        # Head meta in ast[0]
                        ast[0][0][3]["children"] = f"{post['title']} | Roasist Blog"
                        for m_item in ast[0][1]:
                            if isinstance(m_item, list) and len(m_item) >= 4 and isinstance(m_item[3], dict):
                                mp = m_item[3]
                                if mp.get("name") == "description" or mp.get("property") == "og:description":
                                    mp["content"] = post["description"]
                                elif mp.get("property") == "og:title":
                                    mp["content"] = f"{post['title']} | Roasist Blog"
                                elif mp.get("property") == "og:image":
                                    mp["content"] = post["img_src"]
                                elif mp.get("rel") == "canonical":
                                    mp["href"] = canonical_url
                                elif mp.get("property") == "og:url":
                                    mp["content"] = canonical_url

                        art_children = ast[2][3]["children"]
                        # ch[0]: Hero
                        hero_node = art_children[0]
                        # Extract module IDs ($L29 FadeIn, $L2a Image, $L2b ImageEnter)
                        hero_container_ch = hero_node[3]["children"][3]["children"]
                        left_ch = hero_container_ch[0][3]["children"]
                        fade_id = left_ch[0][3]["children"][1]
                        left_ch[0][3]["children"][3]["children"][3]["children"] = [
                            ["$", "button", post["cat_slug"], {"className": "Hero_category__qOhtb", "children": post["cat_name"]}]
                        ]
                        left_ch[1][3]["children"][3]["children"][3]["children"] = post["title"]

                        author_ch = hero_container_ch[1][3]["children"][3]["children"]
                        img_comp_id = author_ch[0][3]["children"][3]["children"][1]
                        author_ch[0][3]["children"][3]["children"][3]["image"] = {
                            "altText": "Roasist",
                            "srcSet": None,
                            "sourceUrl": icon_url,
                            "mediaDetails": {"width": 512, "height": 512},
                        }
                        author_ch[1][3]["children"][3]["children"][3]["children"] = post["date_display"]
                        author_ch[2][3]["children"][3]["children"][3]["children"] = ["Yazar: ", post["author"]]

                        hero_fig = hero_container_ch[2]
                        hero_fig[3]["children"][3]["children"][3]["image"] = {
                            "altText": post["title"],
                            "srcSet": post["img_srcset"],
                            "sourceUrl": post["img_src"],
                            "mediaDetails": {"width": post["img_w"], "height": post["img_h"]},
                        }

                        # ch[1]: ContentBuilder -> keep ONLY Text_text__jOaGN (drop BriefingBanner!)
                        cb_node = art_children[1]
                        cb_node[3]["children"] = [cb_node[3]["children"][0]]

                        # ch[2]: Replace $L2f client Share with clean static Share AST using Turkish "Paylaş : " & roasist.com URL
                        art_children[2] = [
                            "$",
                            "section",
                            None,
                            {
                                "className": "Share_share__5W87u",
                                "children": [
                                    "$",
                                    fade_id,
                                    None,
                                    {
                                        "children": [
                                            "$",
                                            "div",
                                            None,
                                            {
                                                "className": "container",
                                                "children": [
                                                    "$",
                                                    "div",
                                                    None,
                                                    {
                                                        "className": "Share_links__CutyY",
                                                        "children": [
                                                            ["$", "p", None, {"children": "Paylaş : "}],
                                                            [
                                                                "$",
                                                                "a",
                                                                None,
                                                                {
                                                                    "className": "Share_link__ERF_r",
                                                                    "href": f"https://www.linkedin.com/shareArticle?mini=true&url={enc_url}",
                                                                    "target": "_blank",
                                                                    "rel": "noopener noreferrer",
                                                                    "children": "LinkedIn",
                                                                },
                                                            ],
                                                            [
                                                                "$",
                                                                "a",
                                                                None,
                                                                {
                                                                    "className": "Share_link__ERF_r",
                                                                    "href": f"https://www.facebook.com/sharer/sharer.php?u={enc_url}",
                                                                    "target": "_blank",
                                                                    "rel": "noopener noreferrer",
                                                                    "children": "Facebook",
                                                                },
                                                            ],
                                                            [
                                                                "$",
                                                                "a",
                                                                None,
                                                                {
                                                                    "className": "Share_link__ERF_r",
                                                                    "href": f"https://twitter.com/intent/tweet?&url={enc_url}",
                                                                    "target": "_blank",
                                                                    "rel": "noopener noreferrer",
                                                                    "children": "𝕏",
                                                                },
                                                            ],
                                                        ],
                                                    },
                                                ],
                                            },
                                        ]
                                    },
                                ],
                            },
                        ]

                        # ch[3]: Back to blog -> Blog'a Dön
                        back_btn = art_children[3][3]["children"][3]["children"][3]["children"]
                        back_btn[3]["href"] = "/blog/"
                        back_btn[3]["children"] = None if "children" not in back_btn[3] else back_btn[3]["children"]
                        if "children" in back_btn[3] and back_btn[3]["children"] is None:
                            del back_btn[3]["children"]
                        back_btn[3]["text"] = "Blog'a Dön"

                        # ch[4]: RelatedPosts
                        rp_sec = art_children[4]
                        # Update desktop & mobile "Tüm Yazıları Gör" href="/blog/"
                        rp_sec_str = json.dumps(rp_sec, ensure_ascii=False, separators=(",", ":"))
                        rp_sec_str = rp_sec_str.replace('"href":"/blog"', '"href":"/blog/"')
                        rp_sec = json.loads(rp_sec_str)
                        grid_container = rp_sec[3]["children"][2][3]["children"]
                        first_card = grid_container[3]["children"][0]
                        card_link_id = first_card[1]
                        card_img_id = first_card[3]["children"][0][3]["children"][1][1]
                        grid_container[3]["children"] = build_related_posts_flight_cards(
                            related_3, card_link_id, card_img_id
                        )
                        art_children[4] = rp_sec

                        rec[2] = json.dumps(ast, ensure_ascii=False, separators=(",", ":"))
                return True

            new_tail = rewrite_flight_in_html(tail, post_mutator)
            out_dir = os.path.join(ROOT, base_name, "blog", post["slug"])
            os.makedirs(out_dir, exist_ok=True)
            out_fp = os.path.join(out_dir, "index.html")
            with open(out_fp, "w", encoding="utf-8") as f:
                f.write(ssr + new_tail)
            print(f"[BLOG POST] Generated {base_name}/blog/{post['slug']}/index.html")


# ==============================================================================
# STEP 2: UPDATE /blog/index.html (AND /blog/kategori/*, /blog/etiket/*)
# ==============================================================================
def update_blog_index_pages():
    featured = BLOG_POSTS_TR[0]
    blog_desc_tr = (
        "Roasist uzman ekibinden performans pazarlaması, ROAS optimizasyonu, kurumsal SEO, AEO ve "
        "veri odaklı 360° dijital büyüme rehberleri."
    )

    flight_posts_nodes = [
        {
            "node": {
                "title": p["title"],
                "databaseId": p["db_id"],
                "categories": {"edges": [{"node": {"slug": p["cat_slug"], "name": p["cat_name"]}}]},
                "slug": p["slug"],
                "singlePost": {
                    "postDetails": {
                        "featuredImage": {
                            "altText": p["title"],
                            "srcSet": p["img_srcset"],
                            "sourceUrl": p["img_src"],
                            "mediaDetails": {"width": p["img_w"], "height": p["img_h"]},
                        }
                    }
                },
            }
        }
        for p in BLOG_POSTS_TR
    ]

    for base_name in ("public", "dist"):
        targets = [os.path.join(ROOT, base_name, "blog", "index.html")]
        targets += sorted(glob.glob(os.path.join(ROOT, base_name, "blog", "kategori", "*", "index.html")))
        targets += sorted(glob.glob(os.path.join(ROOT, base_name, "blog", "etiket", "*", "index.html")))

        for fp in targets:
            if not os.path.exists(fp):
                continue
            html = open(fp, "r", encoding="utf-8").read()
            pushes = list(PUSH_RE.finditer(html))
            ssr = html[: pushes[0].start()]
            tail = html[pushes[0].start() :]

            # Fix corrupted FeaturedBlogPost CSS classes in SSR
            ssr = ssr.replace("Öne ÇıkanBlogPost_featuredPost__aRcs9", "FeaturedBlogPost_featuredPost__aRcs9")
            ssr = ssr.replace("AnimatedÖne ÇıkanBlog_container__mnIll", "AnimatedFeaturedBlog_container__mnIll")
            ssr = re.sub(
                r'<meta name="description" content="[^"]*"/>',
                lambda _: f'<meta name="description" content="{blog_desc_tr}"/>',
                ssr,
                count=1,
            )

            # Update SSR Featured Post card
            new_featured_ssr = (
                '<div class="FeaturedBlogPost_featuredPost__aRcs9"><div class="container">'
                '<span class="AnimatedFeaturedBlog_container__mnIll" data-fill="false">'
                f'<a class="BlogPostCard_post__fNGbL BlogPostCard_large__STeKf" data-animation="grid-item" href="/blog/{featured["slug"]}/">'
                '<div class="BlogPostCard_postImage__Q4k_I">'
                '<div class="BlogPostCard_tags__RKboe">'
                '<span class="BlogPostCard_tag__Dv5HS">Öne Çıkan</span>'
                f'<span class="BlogPostCard_tag__Dv5HS">{html_mod.escape(featured["cat_name"])}</span>'
                "</div>"
                '<span class="Image_image__RAAdZ Image_fill__EiIzS">'
                f'<img data-srcset="{featured["img_srcset"]}" data-src="{featured["img_src"]}" alt="{html_mod.escape(featured["title"], quote=True)}" fetchPriority="low" height="{featured["img_h"]}" width="{featured["img_w"]}" sizes="auto" class="lazyload"/>'
                "</span></div>"
                f'<div class="BlogPostCard_postText__V0sxg"><h3>{html_mod.escape(featured["title"])}</h3></div>'
                "</a></span></div></div>"
            )
            ssr, n_f = re.subn(
                r'<div class="FeaturedBlogPost_featuredPost__aRcs9">.*?(<div class="Blog_postsWithFilters__aXNNs">)',
                lambda m: new_featured_ssr + m.group(1),
                ssr,
                count=1,
                flags=re.S,
            )
            if n_f != 1:
                raise RuntimeError(f"Could not update SSR FeaturedBlogPost in {fp}")

            def blog_idx_mutator(records):
                for rec in records:
                    if rec[0] == "line" and rec[1] == "d":
                        ast = json.loads(rec[2])
                        for m_item in ast[0][1]:
                            if isinstance(m_item, list) and len(m_item) >= 4 and isinstance(m_item[3], dict):
                                mp = m_item[3]
                                if mp.get("name") == "description" or mp.get("property") == "og:description":
                                    mp["content"] = blog_desc_tr

                        main_ch = ast[2][3]["children"]
                        # Fix FeaturedBlogPost class and card
                        feat_wrap = main_ch[1]
                        feat_wrap[3]["className"] = "FeaturedBlogPost_featuredPost__aRcs9"
                        feat_card = feat_wrap[3]["children"][3]["children"][3]["children"]
                        feat_card[2] = str(featured["db_id"])
                        feat_card[3]["href"] = f"/blog/{featured['slug']}/"
                        feat_tags = feat_card[3]["children"][0][3]["children"][0][3]["children"]
                        feat_tags[1] = [
                            [
                                "$",
                                "span",
                                featured["cat_name"],
                                {"className": "BlogPostCard_tag__Dv5HS", "children": featured["cat_name"]},
                            ]
                        ]
                        feat_card[3]["children"][0][3]["children"][1][3]["image"] = {
                            "altText": featured["title"],
                            "srcSet": featured["img_srcset"],
                            "sourceUrl": featured["img_src"],
                            "mediaDetails": {"width": featured["img_w"], "height": featured["img_h"]},
                        }
                        feat_card[3]["children"][1][3]["children"][3]["children"] = featured["title"]

                        # Update Filters ($L2b categories) and Grid ($L2c posts)
                        pwf = main_ch[2]
                        inner_pair = pwf[3]["children"][3]["children"][3]["children"][3]["children"]
                        inner_pair[0][3]["children"][3]["categories"] = BLOG_CATEGORIES_TR
                        inner_pair[1][3]["posts"] = flight_posts_nodes

                        rec[2] = json.dumps(ast, ensure_ascii=False, separators=(",", ":"))
                return True

            new_tail = rewrite_flight_in_html(tail, blog_idx_mutator)
            with open(fp, "w", encoding="utf-8") as f:
                f.write(ssr + new_tail)
            print(f"[BLOG INDEX] Updated {os.path.relpath(fp, ROOT)}")

    # Remove old Astro-only dist/etiket and dist/kategori directories
    for legacy_dir in ("etiket", "kategori"):
        p = os.path.join(ROOT, "dist", legacy_dir)
        if os.path.isdir(p):
            shutil.rmtree(p)
            print(f"[CLEANUP] Removed obsolete Astro directory dist/{legacy_dir}/")


# ==============================================================================
# STEP 3: UPDATE RelatedPosts ON ALL 20 /hizmetler/* PAGES & HOMEPAGE Articles
# ==============================================================================
def update_service_related_posts():
    top_3 = [BLOG_POSTS_TR[0], BLOG_POSTS_TR[2], BLOG_POSTS_TR[5]]
    ssr_cards = build_related_posts_ssr_cards(top_3)
    count = 0

    for base_name in ("public", "dist"):
        for fp in sorted(glob.glob(os.path.join(ROOT, base_name, "hizmetler", "**", "*.html"), recursive=True)):
            html = open(fp, "r", encoding="utf-8").read()
            if "RelatedPosts_relatedPosts__xfLkb" not in html:
                continue

            pushes = list(PUSH_RE.finditer(html))
            ssr = html[: pushes[0].start()]
            tail = html[pushes[0].start() :]

            def repl_rp_ssr(m):
                sec = m.group(0)
                sec = sec.replace('href="/blog"', 'href="/blog/"')
                sec, n_g = re.subn(
                    r'(<div class="AnimatedGrid_grid__otAMD"><div class="container">).*?(</div></div><div class="container"><div class="RelatedPosts_viewAllLinkMobile__joii8">)',
                    lambda gm: gm.group(1) + ssr_cards + gm.group(2),
                    sec,
                    count=1,
                    flags=re.S,
                )
                if n_g != 1:
                    raise RuntimeError(f"Could not replace RelatedPosts SSR cards in {fp}")
                return sec

            ssr, n_sec = re.subn(
                r'<section class="RelatedPosts_relatedPosts__xfLkb">.*?</section>',
                repl_rp_ssr,
                ssr,
                count=1,
                flags=re.S,
            )
            if n_sec != 1:
                raise RuntimeError(f"Expected 1 RelatedPosts section in {fp}")

            def srv_rp_mutator(records):
                c = False
                for rec in records:
                    if rec[0] == "line" and "RelatedPosts_relatedPosts__xfLkb" in rec[2]:
                        ast = json.loads(rec[2])
                        rp = find_node_by_class(ast, "RelatedPosts_relatedPosts__xfLkb")
                        rp_s = json.dumps(rp, ensure_ascii=False, separators=(",", ":")).replace(
                            '"href":"/blog"', '"href":"/blog/"'
                        )
                        rp_new = json.loads(rp_s)
                        grid_c = rp_new[3]["children"][2][3]["children"]
                        fc = grid_c[3]["children"][0]
                        c_link_id = fc[1]
                        c_img_id = fc[3]["children"][0][3]["children"][1][1]
                        grid_c[3]["children"] = build_related_posts_flight_cards(top_3, c_link_id, c_img_id)
                        rp[:] = rp_new
                        rec[2] = json.dumps(ast, ensure_ascii=False, separators=(",", ":"))
                        c = True
                return c

            new_tail = rewrite_flight_in_html(tail, srv_rp_mutator)
            with open(fp, "w", encoding="utf-8") as f:
                f.write(ssr + new_tail)
            count += 1
    print(f"[RELATED POSTS] Updated {count} service HTML files (public + dist)")


def update_homepage_articles():
    for rel_fp in ("public/kota-roasist-local.html", "dist/index.html"):
        fp = os.path.join(ROOT, rel_fp)
        html = open(fp, "r", encoding="utf-8").read()
        pushes = list(PUSH_RE.finditer(html))
        ssr = html[: pushes[0].start()]
        tail = html[pushes[0].start() :]

        ssr_items = "".join(
            f'<a data-animation="grid-item" href="/blog/{p["slug"]}/">'
            f'<article class="Articles_article__3ZS4Y">'
            f'<figure class="Articles_image__Cvgsi"><span class="Image_image__RAAdZ Image_fill__EiIzS">'
            f'<img data-srcset="{p["img_srcset"]}" data-src="{p["img_src"]}" alt="{html_mod.escape(p["title"], quote=True)}" fetchPriority="low" height="{p["img_h"]}" width="{p["img_w"]}" sizes="auto" class="lazyload"/>'
            f"</span></figure>"
            f'<div class="Articles_text__HhO2L">'
            f'<p class="Articles_filterNames__mCWt8">{html_mod.escape(p["cat_name"])}</p>'
            f'<h3 class="Articles_title__h86PB">{html_mod.escape(p["title"])}</h3>'
            f"</div></article></a>"
            for p in BLOG_POSTS_TR
        )

        ssr = ssr.replace('class="Button_inner__fnyH6" href="/blog"', 'class="Button_inner__fnyH6" href="/blog/"')
        ssr, n_al = re.subn(
            r'(<div class="Articles_articlesList__CXW8a">).*?(<div class="Articles_mobileButton__Df7CF">)',
            lambda m: m.group(1) + ssr_items + m.group(2),
            ssr,
            count=1,
            flags=re.S,
        )
        if n_al != 1:
            raise RuntimeError(f"Could not update SSR Articles_articlesList__CXW8a in {rel_fp}")

        def home_art_mutator(records):
            c = False
            for rec in records:
                if rec[0] == "line" and "Articles_articlesList__CXW8a" in rec[2]:
                    ast = json.loads(rec[2])
                    art_wrap = find_node_by_class(ast, "Articles_articles__Wcz2C")
                    # Update "Blog'u İncele" href="/blog" -> "/blog/"
                    aw_s = json.dumps(art_wrap, ensure_ascii=False, separators=(",", ":")).replace(
                        '"href":"/blog"', '"href":"/blog/"'
                    )
                    art_wrap[:] = json.loads(aw_s)

                    alist = find_node_by_class(art_wrap, "Articles_articlesList__CXW8a")
                    first_card = alist[3]["children"][0][0]
                    link_id = first_card[1]
                    img_id = first_card[3]["children"][3]["children"][0][3]["children"][1]

                    new_cards = [
                        [
                            "$",
                            link_id,
                            str(p["db_id"]),
                            {
                                "href": f"/blog/{p['slug']}/",
                                "data-animation": "grid-item",
                                "children": [
                                    "$",
                                    "article",
                                    None,
                                    {
                                        "className": "Articles_article__3ZS4Y",
                                        "children": [
                                            [
                                                "$",
                                                "figure",
                                                None,
                                                {
                                                    "className": "Articles_image__Cvgsi",
                                                    "children": [
                                                        "$",
                                                        img_id,
                                                        None,
                                                        {
                                                            "image": {
                                                                "altText": p["title"],
                                                                "srcSet": p["img_srcset"],
                                                                "sourceUrl": p["img_src"],
                                                                "mediaDetails": {
                                                                    "width": p["img_w"],
                                                                    "height": p["img_h"],
                                                                },
                                                            }
                                                        },
                                                    ],
                                                },
                                            ],
                                            [
                                                "$",
                                                "div",
                                                None,
                                                {
                                                    "className": "Articles_text__HhO2L",
                                                    "children": [
                                                        [
                                                            "$",
                                                            "p",
                                                            None,
                                                            {
                                                                "className": "Articles_filterNames__mCWt8",
                                                                "children": p["cat_name"],
                                                            },
                                                        ],
                                                        [
                                                            "$",
                                                            "h3",
                                                            None,
                                                            {
                                                                "className": "Articles_title__h86PB",
                                                                "children": p["title"],
                                                            },
                                                        ],
                                                    ],
                                                },
                                            ],
                                        ],
                                    },
                                ],
                            },
                        ]
                        for p in BLOG_POSTS_TR
                    ]
                    alist[3]["children"][0] = new_cards
                    rec[2] = json.dumps(ast, ensure_ascii=False, separators=(",", ":"))
                    c = True
            return c

        new_tail = rewrite_flight_in_html(tail, home_art_mutator)
        with open(fp, "w", encoding="utf-8") as f:
            f.write(ssr + new_tail)
        print(f"[HOMEPAGE ARTICLES] Updated {rel_fp} (6 Turkish articles, removed 🎉 emoji)")


# ==============================================================================
# STEP 4: UPDATE mapKotaHref SO ALL 6 /blog/<slug>/ ROUTES WORK DIRECTLY
# ==============================================================================
def update_runtime_blog_routing():
    old_rule_re = re.compile(
        r"else if \(h\.startsWith\('/blog/'\) && h !== '/blog/' && !h\.startsWith\('/blog/Performans'\).*?h = '/blog/';"
    )
    valid_prefixes = [
        "/blog/Performans-Pazarlamasi-Nedir",
        "/blog/performans-pazarlamasinda-roas-optimizasyonu",
        "/blog/kurumsal-seo-ve-yapay-zeka-aramalari-aeo-rehberi",
        "/blog/360-dijital-pazarlama-kanallar-arasi-sinerji",
        "/blog/Veriye-Dayali-Dijital-Pazarlama-Stratejisi-Nedir",
        "/blog/Reklam-Harcamalarinin-Geri-Donusu-ROAS-Nasil-Hesaplanir",
        "/blog/kategori/",
        "/blog/etiket/",
    ]
    cond_js = " && ".join(f"!h.startsWith('{vp}')" for vp in valid_prefixes)
    new_rule = (
        f"else if (h.startsWith('/blog/') && h !== '/blog/' && {cond_js}) h = '/blog/';\n"
        f"    else if (h.startsWith('/blog/') && !h.endsWith('/')) h = h + '/';"
    )

    updated = 0
    for base_name in ("public", "dist"):
        for fp in sorted(glob.glob(os.path.join(ROOT, base_name, "**", "*.html"), recursive=True)):
            txt = open(fp, "r", encoding="utf-8").read()
            if "mapKotaHref" not in txt:
                continue
            new_txt, n = old_rule_re.subn(lambda _: new_rule, txt)
            if n > 0 and new_txt != txt:
                with open(fp, "w", encoding="utf-8") as f:
                    f.write(new_txt)
                updated += 1
    print(f"[RUNTIME ROUTER] Updated mapKotaHref in {updated} HTML files")


def main():
    build_all_6_blog_detail_pages()
    update_blog_index_pages()
    update_service_related_posts()
    update_homepage_articles()
    update_runtime_blog_routing()


if __name__ == "__main__":
    main()
