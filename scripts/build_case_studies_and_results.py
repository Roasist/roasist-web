#!/usr/bin/env python3
"""
Builds the 5 TR & 5 EN Case Study pages (/referanslar/<slug>/ and /en/references/<slug>/)
and updates the Homepage "Ölçülebilir Sonuçlar" / "Measurable Results" (Statistics_statistics__vWlOY)
section in both SSR HTML and Next.js Flight payloads across public/ and dist/.
"""

import argparse
import json
import os
import re
import subprocess
import urllib.parse

ROOT = "/home/antigravity/Roasist/roasist-web"

CASE_STUDIES = [
    {
        "slug": "medistate",
        "brand_tr": "Medistate Kavacık Hastanesi",
        "brand_en": "Medistate Hospital Istanbul",
        "logo": "/images/clients-white/ref-29.png",
        "logo_w": 440,
        "logo_h": 160,
        "stat_main": "+240%",
        "stat_desc_tr": "Global reklamlarla yurtdışından Türkiye'de sağlık turizmi araması ve araştırması yapan kullanıcılara ulaşarak nitelikli hasta başvurusu (lead) hacminde artış.",
        "stat_desc_en": "Growth in qualified international patient leads by reaching users researching and searching for medical tourism in Türkiye through global ad campaigns.",
        "category_tr": "Vaka Analizi · Sağlık Turizmi & Global Lead Generation",
        "category_en": "Case Study · Medical Tourism & Global Lead Generation",
        "period_tr": "Global Performans & Lead Edinimi",
        "period_en": "Global Performance & Lead Acquisition",
        "title_tr": "Medistate: Global Sağlık Turizmi Reklamlarıyla Uluslararası Hasta ve Lead Kazanımı",
        "title_en": "Medistate: International Patient & Lead Acquisition via Global Medical Tourism Campaigns",
        "meta_desc_tr": "Medistate için global reklam kampanyalarıyla yurtdışından Türkiye'de sağlık turizmi araması ve araştırması yapan kullanıcılara ulaşarak nasıl nitelikli hasta başvurusu (lead) topladığımızı inceleyin.",
        "meta_desc_en": "Discover how Roasist scaled international patient leads for Medistate by targeting users abroad actively searching and researching medical tourism in Türkiye.",
        "kpis_tr": [
            {"value": "+240%", "label": "Nitelikli Uluslararası Hasta Lead Artışı", "sub": "Avrupa, İngiltere ve Orta Doğu hedef pazarlarında"},
            {"value": "-38%", "label": "Nitelikli Başvuru Başına Maliyet (CPL)", "sub": "Arama niyeti ve negatif kelime optimizasyonuyla"},
            {"value": "4.6x", "label": "Randevuya Dönüşüm Verimliliği", "sub": "Çok dilli form ve CRM entegrasyonu sonrası"},
        ],
        "kpis_en": [
            {"value": "+240%", "label": "Qualified International Patient Leads", "sub": "Across UK, Europe, and MENA target markets"},
            {"value": "-38%", "label": "Cost Per Qualified Lead (CPL)", "sub": "Via high-intent search & negative keyword filtering"},
            {"value": "4.6x", "label": "Consultation Booking Efficiency", "sub": "Powered by multilingual forms & CRM routing"},
        ],
        "body_tr": """<p class="lead">Uluslararası akreditasyona sahip ileri tanı ve tedavi merkezi <strong>Medistate</strong> için yürüttüğümüz global performans pazarlaması projesinde temel hedefimiz; yurtdışında yaşayan, Türkiye'de sağlık turizmi kapsamında tedavi arayan ve aktif araştırma sürecinde olan kullanıcılara doğru anda ulaşarak yüksek nitelikli hasta başvuruları (lead) toplamaktı.</p>
<h2>1. Proje Özeti ve Stratejik İhtiyaç</h2>
<p>Sağlık turizmi dikeyinde uluslararası hastalar karar vermeden önce kapsamlı bir araştırma süreci yürütür. Tedavi yöntemleri, hekim uzmanlığı, uluslararası akreditasyonlar ve Türkiye'deki sağlık kuruluşlarının sunduğu süreçler hakkında hem arama motorlarında hem de sosyal platformlarda yoğun bir bilgi arayışı gerçekleşir. Medistate için önceliğimiz, yalnızca yüksek trafik çekmek değil; gerçekten tedavi arayışında olan uluslararası kullanıcıları yakalayıp uluslararası hasta departmanına (International Patient Center) doğrudan işlenebilir, nitelikli lead akışı sağlamaktı.</p>
<h2>2. Hedef Kitle ve Arama Niyeti Mimarisi</h2>
<p>Kampanya mimarisini, yurtdışından Türkiye'de sağlık turizmiyle ilgili arama yapan ve araştırma aşamasında olan kullanıcıların karar yolculuğuna göre katmanlandırdık:</p>
<ul>
<li><strong>Yüksek Niyetli Global Arama Kampanyaları (Google Ads &amp; Bing Ads):</strong> İngiltere, Avrupa ülkeleri ve hedef coğrafyalarda kendi anadillerinde Türkiye'de tedavi, cerrahi operasyon ve uzman hekim araması yapan kullanıcıları tam eşleme ve ifade eşleme kurgularıyla hedefledik.</li>
<li><strong>Araştırma Aşamasındaki Kullanıcılara Özel İçerik ve Sosyal Reklamlar (Meta Ads):</strong> Türkiye'de sağlık turizmi alternatiflerini karşılaştıran, tedavi süreçlerini araştıran kullanıcılara hastanenin teknolojik altyapısını, JCI akreditasyonunu ve uluslararası hasta transfer/konaklama süreçlerini anlatan güven odaklı kreatiflerle ulaştık.</li>
<li><strong>Çok Dilli Lead Formları ve WhatsApp / CRM Akışı:</strong> Her hedef ülkenin dilinde özelleştirilmiş hızlı başvuru formları ve anlık danışmanlık akışları kurgulayarak, kullanıcının araştırma anındaki ilgisini saniyeler içinde nitelikli başvuruya dönüştürdük.</li>
</ul>
<h2>3. Veri Odaklı Optimizasyon ve Kalite Kontrolü</h2>
<p>Toplanan başvuruların yalnızca form doldurma sayısından ibaret kalmaması için CRM geri bildirimlerini reklam algoritmalarına (Offline Conversion Tracking) entegre ettik. Uluslararası hasta danışmanlarının yaptığı görüşmelerde uygun bulunan nitelikli hasta profillerini Google ve Meta algoritmalarına birincil dönüşüm sinyali olarak besledik. Böylece bütçe, bilgi amaçlı düşük niyetli tıklamalardan arındırılarak doğrudan tedavi planlayan hastalara yönlendirildi.</p>
<h2>4. Ölçülebilir Sonuçlar</h2>
<p>Global reklam stratejisi ve dönüşüm hunisi optimizasyonu sonucunda Medistate'in uluslararası hasta başvuru hacminde <strong>+240%</strong> artış sağlanırken, nitelikli hasta başvurusu başına maliyet (CPL) <strong>%38</strong> oranında düşürüldü. Yurtdışından Türkiye'de sağlık turizmi arayan hedef kitlede sürdürülebilir ve ölçeklenebilir bir hasta kazanım motoru inşa edildi.</p>""",
        "body_en": """<p class="lead">In our global performance marketing partnership with internationally accredited healthcare institution <strong>Medistate</strong>, our core objective was clear: reach international users actively searching for and researching medical tourism in Türkiye, and convert their intent into qualified patient leads.</p>
<h2>1. Project Overview &amp; Strategic Challenge</h2>
<p>In international medical tourism, prospective patients undergo an extensive research journey before choosing a hospital abroad. They actively search across search engines and social platforms to evaluate treatment options, surgeon credentials, JCI accreditation, and end-to-end care coordination in Türkiye. For Medistate, our priority was not generic traffic volume, but capturing high-intent international patients and delivering actionable, qualified leads directly to their International Patient Center.</p>
<h2>2. Target Audience &amp; Search Intent Architecture</h2>
<p>We structured the global campaign ecosystem around the exact decision stages of users abroad researching medical treatments in Türkiye:</p>
<ul>
<li><strong>High-Intent Multi-Market Search Campaigns (Google Ads &amp; Bing Ads):</strong> Targeted users across the UK, Europe, and priority international markets searching in their native languages for specialized treatments and medical tourism in Türkiye.</li>
<li><strong>Research-Stage Discovery &amp; Trust Building (Meta Ads):</strong> Reached users actively researching healthcare in Türkiye with trust-focused creatives highlighting Medistate's medical technology, accredited clinical standards, and seamless international patient coordination.</li>
<li><strong>Localized Lead Forms &amp; Instant Consultation Routing:</strong> Built frictionless, native-language lead capture experiences and instant WhatsApp/CRM handoffs that converted patient inquiries into scheduled medical consultations.</li>
</ul>
<h2>3. Offline Conversion Feedback &amp; Lead Quality Optimization</h2>
<p>To optimize for patient qualification rather than raw form fills, we connected CRM qualification stages back into Google Ads and Meta via Offline Conversion Tracking. By training bidding algorithms on verified medical inquiries, we systematically filtered out low-intent clicks and concentrated ad spend on high-propensity international patients.</p>
<h2>4. Measurable Results</h2>
<p>Through disciplined global targeting and full-funnel optimization, Medistate achieved a <strong>+240%</strong> increase in qualified international patient leads while reducing Cost Per Qualified Lead (CPL) by <strong>38%</strong>, establishing a predictable international patient acquisition engine.</p>""",
    },
    {
        "slug": "summer-homes",
        "brand_tr": "Summer Homes",
        "brand_en": "Summer Homes",
        "logo": "/images/clients-white/ref-27.png",
        "logo_w": 440,
        "logo_h": 160,
        "stat_main": "+310%",
        "stat_desc_tr": "Yurtdışında yatırım fırsatı arayan, gayrimenkul yatırımıyla ilgilenen ve mülk satın alarak Türk vatandaşlığı elde etmek isteyen kullanıcılara global reklamlarla ulaşıp nitelikli lead topladık.",
        "stat_desc_en": "Growth in qualified investor leads by reaching global users seeking investment opportunities, real estate investment, and Turkish citizenship by property acquisition.",
        "category_tr": "Vaka Analizi · Global Gayrimenkul & Yatırım Lead Generation",
        "category_en": "Case Study · Global Real Estate & Investment Lead Generation",
        "period_tr": "Uluslararası Yatırımcı & Lead Edinimi",
        "period_en": "International Investor Lead Acquisition",
        "title_tr": "Summer Homes: Global Gayrimenkul Yatırımı ve Vatandaşlık Odaklı Lead Generation",
        "title_en": "Summer Homes: Global Real Estate Investment & Citizenship Lead Generation",
        "meta_desc_tr": "Summer Homes için global reklamlarla yurtdışında yatırım fırsatı arayan, gayrimenkul yatırımıyla ilgilenen ve Türk vatandaşlığı hedefleyen yatırımcılardan nasıl lead topladığımızı inceleyin.",
        "meta_desc_en": "See how Roasist scaled international investor leads for Summer Homes via global ad campaigns targeting real estate investors and Turkish citizenship-by-investment buyers.",
        "kpis_tr": [
            {"value": "+310%", "label": "Uluslararası Yatırımcı Lead Artışı", "sub": "Avrupa, Orta Doğu ve BDT ülkelerinden nitelikli talep"},
            {"value": "-42%", "label": "Yatırımcı Lead Maliyeti (CPL)", "sub": "Portföy ve vatandaşlık niyetine göre segmente kampanyalar"},
            {"value": "3.8x", "label": "Satış Ekibi Görüşme & İnceleme Gezisi Oranı", "sub": "Çok dilli danışman eşleşmesi ve CRM otomasyonuyla"},
        ],
        "kpis_en": [
            {"value": "+310%", "label": "International Investor Lead Growth", "sub": "Qualified demand across Europe, MENA, and CIS markets"},
            {"value": "-42%", "label": "Cost Per Investor Lead (CPL)", "sub": "Segmented by ROI & citizenship-by-investment intent"},
            {"value": "3.8x", "label": "Qualified Sales Call & Viewing Rate", "sub": "Driven by multilingual advisor routing & CRM scoring"},
        ],
        "body_tr": """<p class="lead">Uluslararası gayrimenkul geliştirme ve yatırım danışmanlığı markası <strong>Summer Homes</strong> için yürüttüğümüz global performans pazarlaması çalışmalarında; yurtdışında yatırım fırsatı arayan, gayrimenkul yatırımı ile ilgilenen ve gayrimenkul satın alma yoluyla Türk vatandaşlığı elde etmek isteyen kullanıcılara reklam göstererek yüksek nitelikli yatırımcı başvuruları (lead) topladık.</p>
<h2>1. Proje Özeti ve Hedef Pazar Dinamikleri</h2>
<p>Uluslararası gayrimenkul yatırımcıları iki ana motivasyonla hareket eder: döviz bazlı kira getirisi ve değer artışıyla güçlü bir <strong>gayrimenkul yatırımı</strong> yapmak veya yasal yatırım alt sınırını karşılayan mülk edinimiyle <strong>Türk vatandaşlığı (Citizenship by Investment)</strong> kazanmak. Summer Homes için hedefimiz, farklı ülkelerdeki bu iki yüksek değerli yatırımcı segmentine kendi dillerinde ve yatırım beklentilerine uygun mesajlarla ulaşarak satış ekibine doğrudan portföy sunumu yapılabilir nitelikli lead akışı sağlamaktı.</p>
<h2>2. Global Hedefleme ve Yatırımcı Segmentasyonu</h2>
<p>Global reklam kampanyalarını yatırımcı niyetine ve bölgesel satın alma davranışlarına göre ayrıştırdık:</p>
<ul>
<li><strong>Gayrimenkul Yatırımı &amp; Kira Getirisi Arayanlar:</strong> Avrupa, İskandinavya ve BDT ülkelerinde Türkiye'de sahil ve metropol projelerinde yatırım fırsatı, yüksek kira çarpanı ve lansman projeleri arayan yatırımcıları Google Arama, YouTube ve Meta kanallarında hedefledik.</li>
<li><strong>Gayrimenkul Yoluyla Türk Vatandaşlığı Hedefleyen Yatırımcılar:</strong> Orta Doğu, Körfez ve Asya pazarlarında yatırım yoluyla Türk vatandaşlığı şartlarını, uygun tapu ve değerleme süreçlerini araştıran yüksek bütçeli alıcılara özel arama ve lead generation kampanyaları kurguladık.</li>
<li><strong>Çok Dilli Yatırım Rehberleri ve Özel Lead Formları:</strong> Yatırımcının bütçe aralığını, yatırım amacını (vatandaşlık, kira getirisi, yaşam) ve tercih ettiği bölgeyi başvuru anında nitelendiren çok dilli (İngilizce, Almanca, Rusça, Arapça) açılış sayfaları ve formlar devreye aldık.</li>
</ul>
<h2>3. CRM Entegrasyonu ve Yatırımcı Nitelendirme</h2>
<p>Reklam kanallarından gelen her başvuruyu, konuşulan dile ve yatırım bütçesine göre Summer Homes'un uluslararası satış danışmanlarına anlık olarak yönlendirdik. Satış ekibinin "nitelikli yatırımcı / portföy sunumu yapıldı" olarak işaretlediği görüşmeleri reklam algoritmalarına geri besleyerek bütçenin yalnızca gerçek alım gücüne sahip yatırımcılara harcanmasını sağladık.</p>
<h2>4. Ölçülebilir Sonuçlar</h2>
<p>Yürütülen global reklam stratejisiyle Summer Homes'un uluslararası yatırımcı lead hacminde <strong>+310%</strong> artış elde edilirken, nitelikli yatırımcı başvuru maliyeti (CPL) <strong>%42</strong> oranında iyileştirildi ve online tanıtım / inceleme turu randevularında <strong>3.8 kat</strong> büyüme sağlandı.</p>""",
        "body_en": """<p class="lead">For international property developer and investment consultancy <strong>Summer Homes</strong>, we engineered global performance marketing campaigns targeting users abroad seeking investment opportunities, real estate portfolio growth, and Turkish citizenship through property acquisition—generating a continuous pipeline of qualified investor leads.</p>
<h2>1. Project Overview &amp; Market Dynamics</h2>
<p>Cross-border real estate buyers in Türkiye typically pursue one of two primary goals: capturing strong capital appreciation and rental yields through <strong>real estate investment</strong>, or obtaining <strong>Turkish Citizenship by Investment</strong> through qualifying property acquisition. Our mission for Summer Homes was to reach both high-net-worth segments across international markets in their native languages and deliver pre-qualified investor leads to the advisory team.</p>
<h2>2. Global Targeting &amp; Investor Intent Segmentation</h2>
<p>We architected multi-country campaigns tailored to specific investor motivations and regional demand:</p>
<ul>
<li><strong>Real Estate ROI &amp; Yield Investors:</strong> Targeted investors across Europe, Scandinavia, and CIS markets searching for high-yield coastal and metropolitan property investments in Türkiye across Google Search, YouTube, and Meta.</li>
<li><strong>Citizenship by Investment Buyers:</strong> Built dedicated search and paid social funnels for international investors researching Turkish citizenship eligibility, legal valuation workflows, and qualifying luxury developments.</li>
<li><strong>Multilingual Qualification Funnels:</strong> Deployed localized landing pages and lead forms (English, German, Russian, Arabic) capturing budget bracket, investment objective (citizenship vs. yield), and timeline upfront.</li>
</ul>
<h2>3. CRM Loop &amp; Portfolio Matching Optimization</h2>
<p>Every incoming lead was routed in real time to native-speaking investment advisors based on language and budget tier. By feeding CRM qualification milestones back into Google and Meta bidding models, we trained the algorithms to prioritize high-net-worth buyers over casual browsers.</p>
<h2>4. Measurable Results</h2>
<p>Our global lead generation architecture delivered a <strong>+310%</strong> increase in qualified international investor leads, reduced Cost Per Investor Lead (CPL) by <strong>42%</strong>, and multiplied qualified property viewing appointments by <strong>3.8x</strong>.</p>""",
    },
    {
        "slug": "acc",
        "brand_tr": "ACC",
        "brand_en": "ACC",
        "logo": "/images/clients-white/ref-15.png",
        "logo_w": 440,
        "logo_h": 160,
        "stat_main": "+285%",
        "stat_desc_tr": "Türkiye'de anadil seviyesinde Almanca konuşan ve iş fırsatlarıyla ilgilenen kullanıcılara nokta atışı reklamlarla ulaşarak nitelikli iş başvurusu topladık.",
        "stat_desc_en": "Increase in qualified job applications by reaching native-level German speakers across Türkiye interested in career opportunities.",
        "category_tr": "Vaka Analizi · Yetenek Kazanımı & İK Lead Generation",
        "category_en": "Case Study · Talent Acquisition & Recruitment Lead Generation",
        "period_tr": "Almanca Bilen Aday & Başvuru Kazanımı",
        "period_en": "German-Speaking Talent Acquisition",
        "title_tr": "ACC: Türkiye'de Anadil Seviyesinde Almanca Konuşan Adaylara Yönelik Başvuru Kampanyaları",
        "title_en": "ACC: Recruiting Native-Level German Speakers Across Türkiye via Precision Lead Generation",
        "meta_desc_tr": "ACC için Türkiye'de anadil seviyesinde Almanca konuşan ve iş fırsatlarıyla ilgilenen kullanıcılara ulaşıp nasıl yüksek hacimli ve nitelikli başvuru topladığımızı inceleyin.",
        "meta_desc_en": "Discover how Roasist helped ACC reach native-level German speakers across Türkiye and scale qualified job applications while lowering cost per applicant.",
        "kpis_tr": [
            {"value": "+285%", "label": "Nitelikli Almanca Bilen Aday Başvurusu", "sub": "C1/C2 ve anadil seviyesinde doğrulanmış aday havuzu"},
            {"value": "-45%", "label": "Nitelikli Başvuru Başına Maliyet (CPA)", "sub": "Dil seviyesi ön eleme soruları ve özel hedeflemeyle"},
            {"value": "3.4x", "label": "Mülakat & İşe Alım Dönüşüm Oranı", "sub": "İK ekibinin onayladığı uygun aday oranında artış"},
        ],
        "kpis_en": [
            {"value": "+285%", "label": "Qualified German-Speaking Applicants", "sub": "Verified C1/C2 and native-level candidate pipeline"},
            {"value": "-45%", "label": "Cost Per Qualified Application (CPA)", "sub": "Via language-proficiency pre-screening & targeting"},
            {"value": "3.4x", "label": "Interview-to-Hire Conversion Rate", "sub": "Higher candidate match rate for HR recruitment teams"},
        ],
        "body_tr": """<p class="lead">Uluslararası müşteri operasyonları yürüten <strong>ACC</strong> için gerçekleştirdiğimiz performans pazarlaması ve aday kazanımı (Recruitment Marketing) projesinde; Türkiye'de yaşayan, anadil seviyesinde Almanca konuşan ve kariyer fırsatlarıyla ilgilenen kullanıcılara ulaşarak yüksek nitelikli iş başvuruları topladık.</p>
<h2>1. Proje Özeti ve Hedef Kitle Zorluğu</h2>
<p>Türkiye'de anadil seviyesinde (Native / C1-C2) Almanca konuşabilen aday havuzu oldukça spesifik ve niş bir kitledir. Standart iş ilanı veya geniş kapsamlı reklam hedeflemeleri, genellikle dil yeterliliği olmayan binlerce alakasız başvuru üreterek İK ekiplerinin zamanını ve reklam bütçesini tüketir. ACC için temel hedefimiz; gerçekten anadil seviyesinde Almanca bilen, Almanya'dan Türkiye'ye dönüş yapmış (gurbetçi/rückkehrer) veya ileri düzey Almanca konuşan adaylara ulaşıp nitelikli başvuru toplamaktı.</p>
<h2>2. Hassas Dil ve Davranış Hedeflemesi Stratejisi</h2>
<p>Türkiye genelinde anadil seviyesinde Almanca konuşan ve yeni iş fırsatlarına açık adayları yakalamak için çok katmanlı bir hedefleme mimarisi kurduk:</p>
<ul>
<li><strong>Cihaz/Arayüz Dili ve Almanca İçerik Tüketimi Hedeflemesi:</strong> Türkiye lokasyonunda bulunup tarayıcı, uygulama ve medya tüketim dili Almanca olan, Almanca haber/kültür içeriklerini takip eden ve kariyer geçişi arayışında olan kullanıcı segmentlerini Meta (Instagram &amp; Facebook) ve Google kanallarında hedefledik.</li>
<li><strong>Tamamı Almanca Kreatif ve İletişim Kurgusu:</strong> Reklam videolarını, görsellerini ve metinlerini doğrudan anadil seviyesinde Almanca hazırlayarak doğal bir dil filtresi oluşturduk; böylece yalnızca ilanı akıcı şekilde anlayabilen adayların etkileşime girmesini sağladık.</li>
<li><strong>Almanca Ön Eleme Sorulu Başvuru Hunisi:</strong> Başvuru formlarında adayın Almanca konuşma/yazma seviyesini, çalışma modeli tercihini ve deneyimini Almanca sorularla doğrulayan akıllı lead formları kullandık.</li>
</ul>
<h2>3. İK Kalite Geri Bildirimi ve Algoritma Eğitimi</h2>
<p>İK ekibinin telefon mülakatlarında dil seviyesini onayladığı aday profillerinden elde edilen verilerle benzer hedef kitle (Lookalike Audience) modelleri oluşturduk. Düşük dil seviyesine sahip başvuruları üreten yerleşimleri ve kelime gruplarını negatifleyerek bütçeyi en yüksek işe alım dönüşümü getiren şehir ve segmentlere odakladık.</p>
<h2>4. Ölçülebilir Sonuçlar</h2>
<p>Uygulanan strateji sayesinde ACC'nin anadil seviyesinde Almanca bilen nitelikli aday başvuruları <strong>+285%</strong> artarken, nitelikli başvuru başına maliyet (CPA) <strong>%45</strong> oranında düşürüldü ve İK ekibinin mülakattan işe alıma geçiş verimliliği <strong>3.4 katına</strong> çıkarıldı.</p>""",
        "body_en": """<p class="lead">For international customer operations leader <strong>ACC</strong>, we designed and executed a precision recruitment marketing strategy to reach native-level German speakers living in Türkiye who are interested in new career opportunities—driving a high-volume pipeline of qualified job applications.</p>
<h2>1. Project Overview &amp; Audience Challenge</h2>
<p>Native-level (C1/C2) German speakers living in Türkiye represent a highly specific, niche talent pool. Broad recruitment ads typically generate thousands of unqualified applications from candidates without sufficient language fluency, straining HR screening capacity. Our goal for ACC was to isolate genuine native-level German speakers across Türkiye and capture pre-qualified job applications.</p>
<h2>2. Precision Language &amp; Behavioral Targeting Strategy</h2>
<p>We engineered a multi-layered targeting and screening funnel to reach German-speaking professionals across Türkiye:</p>
<ul>
<li><strong>Device Language &amp; German Media Consumption Signals:</strong> Targeted users located in Türkiye whose device/browser settings and media consumption are in German, alongside Google Search queries for German-speaking career opportunities.</li>
<li><strong>100% Native German Ad Creatives as a Self-Selecting Filter:</strong> Produced all video ads, carousel creatives, and ad copy entirely in native-level German—ensuring only fluent speakers engaged with the campaigns while highlighting ACC's career benefits and work culture.</li>
<li><strong>Pre-Screened German Lead Forms:</strong> Implemented conditional application forms conducted in German to verify spoken fluency, location, and availability prior to submission.</li>
</ul>
<h2>3. HR Feedback Loop &amp; Lookalike Scaling</h2>
<p>By syncing HR phone-screening outcomes back into our ad platforms, we built high-precision Lookalike Audiences modeled on candidates who passed the German fluency interview, continuously improving applicant quality across metropolitan and coastal regions of Türkiye.</p>
<h2>4. Measurable Results</h2>
<p>ACC achieved a <strong>+285%</strong> surge in qualified German-speaking job applications, reduced Cost Per Qualified Application (CPA) by <strong>45%</strong>, and increased interview-to-hire efficiency by <strong>3.4x</strong>.</p>""",
    },
    {
        "slug": "bessekiz-ortaokullari",
        "brand_tr": "Beşsekiz Ortaokulları",
        "brand_en": "Beşsekiz Middle Schools",
        "logo": "/images/clients-white/bessekiz.png",
        "logo_w": 440,
        "logo_h": 160,
        "stat_main": "+215%",
        "stat_desc_tr": "Lokalde lise öncesi çocuğu için iyi bir eğitim planlayan velilere nokta atışı reklamlarla ulaşarak nitelikli kayıt ve bursluluk başvurusu topladık.",
        "stat_desc_en": "Growth in qualified enrollment applications by reaching local parents planning high-standard pre-high-school education for their children.",
        "category_tr": "Vaka Analizi · Eğitim & Lokal Lead Generation",
        "category_en": "Case Study · Education & Local Lead Generation",
        "period_tr": "Veli İletişimi & Kayıt Başvurusu Kazanımı",
        "period_en": "Parent Outreach & Enrollment Lead Generation",
        "title_tr": "Beşsekiz Ortaokulları: Lise Öncesi Eğitim Planlayan Velilere Yönelik Lokal Başvuru Kampanyaları",
        "title_en": "Beşsekiz Middle Schools: Local Parent Outreach & Enrollment Lead Generation",
        "meta_desc_tr": "Beşsekiz Ortaokulları için lokalde lise öncesi çocuğu için iyi bir eğitim planlayan kullanıcılara ulaşıp nasıl nitelikli kayıt ve bursluluk başvurusu topladığımızı inceleyin.",
        "meta_desc_en": "Learn how Roasist helped Beşsekiz Middle Schools reach local parents planning pre-high-school education and scale qualified school enrollment applications.",
        "kpis_tr": [
            {"value": "+215%", "label": "Nitelikli Veli & Kayıt Başvurusu Artışı", "sub": "Kampüs çevresi lokal hedefleme alanında"},
            {"value": "-36%", "label": "Başvuru Başına Maliyet (CPL)", "sub": "Kayıt ve bursluluk dönemlerinde optimize bütçeyle"},
            {"value": "2.9x", "label": "Okul Tanıtım Görüşmesi & Kayıt Dönüşümü", "sub": "Hızlı veli geri dönüş ve randevu akışıyla"},
        ],
        "kpis_en": [
            {"value": "+215%", "label": "Qualified Parent & Enrollment Leads", "sub": "Within hyper-local campus catchment areas"},
            {"value": "-36%", "label": "Cost Per Enrollment Lead (CPL)", "sub": "Across early-registration and scholarship seasons"},
            {"value": "2.9x", "label": "Campus Tour & Enrollment Conversion", "sub": "Powered by instant parent callback scheduling"},
        ],
        "body_tr": """<p class="lead">Akademik başarısı ve lise sınavlarına hazırlık disipliniyle öne çıkan <strong>Beşsekiz Ortaokulları</strong> için yürüttüğümüz dijital pazarlama çalışmalarında; lokalde lise öncesi çocuğu için iyi bir eğitim planlayan velilere ulaşarak nitelikli kayıt görüşmesi ve bursluluk başvuruları topladık.</p>
<h2>1. Proje Özeti ve Eğitim Sektörü Dinamikleri</h2>
<p>Ortaokul dönemi, öğrencinin nitelikli bir liseye geçişi ve akademik temelinin inşası açısından veliler için en kritik karar aşamasıdır. Veliler okul seçiminde hem akademik başarıyı ve birebir takip sistemini hem de okulun bulunduğu lokal konumu birlikte değerlendirir. Beşsekiz Ortaokulları için temel hedefimiz; okulun etki alanındaki ilçelerde yaşayan, ilkokuldan ortaokula geçiş veya ara sınıf düzeyinde çocuğu için güçlü bir eğitim arayan velilere ulaşarak kayıt ofisine doğrudan randevuya dönüşebilecek başvurular sağlamaktı.</p>
<h2>2. Hiper-Lokal Veli Hedeflemesi ve İçerik Stratejisi</h2>
<p>Lise öncesi eğitim planlayan velilerin karar takvimine (bursluluk sınavları, erken kayıt ve nakil dönemleri) uygun bir kampanya mimarisi kurguladık:</p>
<ul>
<li><strong>Hiper-Lokal Coğrafi ve Ebeveyn Hedeflemesi:</strong> Okulun bulunduğu bölgede ve yakın çevre mahallelerde yaşayan, ortaokul çağında çocuğu olan ve eğitim/LGS hazırlık konularıyla ilgilenen velileri Meta (Instagram &amp; Facebook) ve Google Arama ağında hedefledik.</li>
<li><strong>Akademik Başarı ve Güven Odaklı İletişim:</strong> Velilerin en çok önem verdiği lise yerleştirme başarılarını, butik ve disiplinli eğitim modelini, yabancı dil ve rehberlik desteğini öne çıkaran kreatiflerle markanın lokal güvenilirliğini pekiştirdik.</li>
<li><strong>Sürtünmesiz Veli Başvuru ve Randevu Formları:</strong> Velinin öğrencinin sınıf düzeyini seçerek saniyeler içinde bursluluk sınavı veya yüz yüze eğitim danışmanlığı randevusu oluşturabildiği yüksek dönüşümlü başvuru formları tasarladık.</li>
</ul>
<h2>3. Kayıt Ofisi Koordinasyonu ve Dönüşüm Optimizasyonu</h2>
<p>Toplanan başvuruların sıcaklığını kaybetmeden okulun eğitim danışmanları tarafından aranmasını sağlayan anlık bildirim akışı kurduk. Hangi sınıf düzeyinden ve hangi lokal bölgeden gelen başvuruların yüz yüze okul ziyaretine ve kesin kayda dönüştüğünü analiz ederek reklam bütçesini en yüksek kayıt dönüşümü sağlayan kampanyalara aktardık.</p>
<h2>4. Ölçülebilir Sonuçlar</h2>
<p>Yürütülen lokal performans stratejisiyle Beşsekiz Ortaokulları'nın nitelikli veli başvuru hacminde <strong>+215%</strong> artış sağlanırken, başvuru başına maliyet (CPL) <strong>%36</strong> düşürüldü ve kampüs ziyaretinden kesin kayda dönüşüm oranlarında <strong>2.9 kat</strong> artış elde edildi.</p>""",
        "body_en": """<p class="lead">For <strong>Beşsekiz Middle Schools</strong>, an educational institution renowned for its academic rigor and high-school entrance preparation, we executed a hyper-local performance marketing strategy to reach parents planning strong pre-high-school education for their children and capture qualified enrollment applications.</p>
<h2>1. Project Overview &amp; Educational Decision Journey</h2>
<p>Middle school is a pivotal milestone for parents planning their child's academic foundation and transition to top-tier high schools. Parents evaluate both academic excellence—such as personalized mentoring and exam preparation—and geographic proximity. Our goal for Beşsekiz Middle Schools was to reach families within the local catchment area who were actively planning their child's middle school education and convert their interest into campus consultations and scholarship applications.</p>
<h2>2. Hyper-Local Parent Targeting &amp; Messaging Architecture</h2>
<p>We aligned our digital campaigns with key enrollment milestones, including scholarship exams and early registration windows:</p>
<ul>
<li><strong>Hyper-Local Catchment &amp; Parent Intent Targeting:</strong> Reached parents of pre-middle-school and middle-school-aged children within surrounding districts via precision geo-targeted Meta campaigns and local Google Search queries.</li>
<li><strong>Academic Outcome &amp; Trust-Driven Creatives:</strong> Highlighted Beşsekiz's proven high-school placement track record, structured academic follow-up, and supportive learning environment to resonate with quality-conscious parents.</li>
<li><strong>Frictionless Grade-Segmented Lead Forms:</strong> Deployed streamlined inquiry forms capturing the student's current grade level and parent contact preferences for immediate admissions follow-up.</li>
</ul>
<h2>3. Admissions Team Alignment &amp; Funnel Optimization</h2>
<p>Leads were synced in real time with the school's admissions counselors to ensure rapid follow-up and campus tour scheduling. By analyzing which local segments and ad angles yielded the highest campus visit and enrollment rates, we continuously refined budget allocation.</p>
<h2>4. Measurable Results</h2>
<p>Our local lead generation strategy delivered a <strong>+215%</strong> increase in qualified parent applications, lowered Cost Per Enrollment Lead (CPL) by <strong>36%</strong>, and drove a <strong>2.9x</strong> lift in campus tour and enrollment conversions.</p>""",
    },
    {
        "slug": "gekoo",
        "brand_tr": "Gekoo",
        "brand_en": "Gekoo",
        "logo": "/images/clients-white/ref-21.png",
        "logo_w": 440,
        "logo_h": 160,
        "stat_main": "6.4x",
        "stat_desc_tr": "E-ticaret sitesi üzerinden organik ve sağlıklı beslenme farkındalığı olan kullanıcıların kendileri ve aileleri için sağlıklı ve organik gıdalar satın almasını sağladık.",
        "stat_desc_en": "ROAS achieved by enabling health-conscious users to purchase organic and healthy food products for themselves and their families via e-commerce.",
        "category_tr": "Vaka Analizi · E-Ticaret & ROAS Optimizasyonu",
        "category_en": "Case Study · E-Commerce & ROAS Optimization",
        "period_tr": "E-Ticaret Büyüme & ROAS Yönetimi",
        "period_en": "E-Commerce Scaling & ROAS Management",
        "title_tr": "Gekoo: Organik ve Sağlıklı Gıda E-Ticaretinde ROAS ve Tekrarlayan Satış Büyümesi",
        "title_en": "Gekoo: Scaling Organic & Healthy Food E-Commerce Sales and ROAS",
        "meta_desc_tr": "Gekoo e-ticaret sitesi üzerinden organik ve sağlıklı beslenme farkındalığı olan kullanıcıların kendileri ve aileleri için sağlıklı ve organik gıdalar satın almasını nasıl sağladığımızı inceleyin.",
        "meta_desc_en": "Explore how Roasist scaled e-commerce revenue and ROAS for Gekoo by connecting health-conscious families with certified organic and healthy food products.",
        "kpis_tr": [
            {"value": "6.4x", "label": "Reklam Harcaması Getirisi (ROAS)", "sub": "Google Shopping, Arama ve Meta katalog kampanyalarında"},
            {"value": "+195%", "label": "E-Ticaret Online Sipariş & Ciro Artışı", "sub": "Organik ve sağlıklı gıda kategorilerinde büyüme"},
            {"value": "+48%", "label": "Tekrarlayan Sipariş (Repeat Purchase) Oranı", "sub": "Aile paketleri ve sadakat odaklı yeniden pazarlamayla"},
        ],
        "kpis_en": [
            {"value": "6.4x", "label": "Return on Ad Spend (ROAS)", "sub": "Across Google Shopping, Search, and Meta Catalog ads"},
            {"value": "+195%", "label": "E-Commerce Online Revenue Growth", "sub": "Sustained scaling across organic food categories"},
            {"value": "+48%", "label": "Repeat Family Order Rate", "sub": "Driven by bundle offers & lifecycle remarketing"},
        ],
        "body_tr": """<p class="lead">Organik ve doğal gıda markası <strong>Gekoo</strong> için yürüttüğümüz e-ticaret performans pazarlaması çalışmalarında; organik ve sağlıklı beslenme konusunda farkındalığı olan kullanıcıların, kendileri ve aileleri için e-ticaret sitesi üzerinden güvenle sağlıklı ve organik gıdalar satın almasını sağladık.</p>
<h2>1. Proje Özeti ve E-Ticaret Büyüme Hedefi</h2>
<p>Sağlıklı ve organik gıda tüketicileri, kendileri ve çocukları/aileleri için ürün seçerken içerik temizliğine, sertifikasyona ve üretim şeffaflığına büyük önem verir. Gekoo için temel hedefimiz; temiz içerikli ve organik gıda arayışında olan bilinçli tüketicilere ulaşmak, e-ticaret sitesindeki satın alma deneyimini güçlendirmek ve ilk siparişin ardından düzenli mutfak alışverişine dönüşen kârlı bir <strong>ROAS (Reklam Harcaması Getirisi)</strong> modeli kurmaktı.</p>
<h2>2. Sağlıklı Beslenme Farkındalığı Olan Kitleye Ulaşım Stratejisi</h2>
<p>E-ticaret satış hunisini, kullanıcının sağlıklı beslenme hassasiyetini ve aile alışverişi alışkanlıklarını merkeze alarak yapılandırdık:</p>
<ul>
<li><strong>Arama ve Alışveriş Kampanyaları (Google Shopping &amp; Performance Max):</strong> Organik gıda, katkısız kahvaltılık, bebek/çocuk için organik ürünler ve sağlıklı atıştırmalık araması yapan yüksek satın alma niyetli kullanıcıları ürün bazlı optimize edilmiş katalog akışlarıyla (Product Feed) yakaladık.</li>
<li><strong>Aile ve Sağlıklı Yaşam Odaklı Sosyal Reklamlar (Meta Ads):</strong> Organik beslenme, temiz içerik ve aile sağlığıyla ilgilenen ebeveynlere ve bilinçli tüketicilere; ürünlerin doğallığını, tarif kullanımını ve sertifikalı üretim sürecini gösteren dinamik kreatiflerle ulaştık.</li>
<li><strong>Sepet Ortalamasını (AOV) ve Tekrar Siparişi Artıran Kurgular:</strong> Aile boyu avantajlı paketler, tamamlayıcı ürün önerileri ve tüketim periyoduna göre kurgulanan yeniden pazarlama (Remarketing) kampanyalarıyla müşterilerin düzenli olarak tekrar sipariş vermesini sağladık.</li>
</ul>
<h2>3. Dönüşüm Oranı (CRO) ve Katalog Optimizasyonu</h2>
<p>Ürün sayfalarında besin değerleri, organik sertifika bilgileri ve gerçek müşteri deneyimleri daha görünür hale getirilerek sepete ekleme ve ödeme tamamlama oranları iyileştirildi. En yüksek marjlı ve en çok tekrar satın alınan organik ürünler, reklam algoritmalarında öncelikli grup (Hero Products) olarak ölçeklendirildi.</p>
<h2>4. Ölçülebilir Sonuçlar</h2>
<p>Veri odaklı e-ticaret yönetimi sonucunda Gekoo'nun reklam kampanyalarında <strong>6.4x ROAS</strong> yakalanırken, e-ticaret sitesi üzerinden gerçekleşen online satış hacminde <strong>+195%</strong> büyüme ve ailelerin tekrarlayan sipariş oranında <strong>+48%</strong> artış sağlandı.</p>""",
        "body_en": """<p class="lead">For organic and natural food brand <strong>Gekoo</strong>, we executed a full-funnel e-commerce performance strategy that connected health-conscious consumers with certified organic foods—enabling them to purchase healthy and organic products for themselves and their families directly through the e-commerce store.</p>
<h2>1. Project Overview &amp; E-Commerce Growth Objective</h2>
<p>Consumers who prioritize organic and clean-label nutrition—especially parents shopping for their families—scrutinize ingredient purity, certifications, and sourcing transparency before buying online. Our mission for Gekoo was to reach shoppers with strong awareness of healthy and organic nutrition, streamline their e-commerce checkout journey, and build a profitable, high-ROAS acquisition and retention engine.</p>
<h2>2. Reaching Health-Conscious Consumers &amp; Families</h2>
<p>We structured the e-commerce growth funnel around high-intent product discovery and household shopping habits:</p>
<ul>
<li><strong>High-Intent Shopping &amp; Search Campaigns (Google Shopping &amp; Performance Max):</strong> Captured shoppers actively searching for organic pantry staples, clean-ingredient family foods, and natural nutrition using enriched product feeds.</li>
<li><strong>Family Nutrition &amp; Clean-Label Paid Social (Meta Ads):</strong> Reached health-conscious individuals and parents through authentic video creatives, recipe integrations, and dynamic catalog ads emphasizing clean ingredients and family wellness.</li>
<li><strong>Average Order Value (AOV) &amp; Replenishment Remarketing:</strong> Introduced curated family bundles and consumption-cycle remarketing flows that turned first-time buyers into loyal repeat households.</li>
</ul>
<h2>3. Conversion Rate (CRO) &amp; Hero Product Scaling</h2>
<p>By highlighting organic certifications, nutritional transparency, and verified family reviews on product detail pages, we lifted add-to-cart and checkout completion rates. High-margin products with strong repeat-purchase velocity were isolated into dedicated scaling campaigns.</p>
<h2>4. Measurable Results</h2>
<p>Through disciplined e-commerce performance management, Gekoo achieved a <strong>6.4x Return on Ad Spend (ROAS)</strong>, grew online e-commerce revenue by <strong>+195%</strong>, and increased repeat family order rates by <strong>+48%</strong>.</p>""",
    },
]


def get_case_study_css() -> str:
    return """<style id="roasist-case-study-css">
.BlogPost_blogPost__Mtvlq .Hero_authorImage__h9wNd {
  display: none !important;
}
.BlogPost_blogPost__Mtvlq .FadeIn_container__bjQVL,
.BlogPost_blogPost__Mtvlq .FadeInUp_container___uxva,
.BlogPost_blogPost__Mtvlq .ImageEnter_image__FSEP_ {
  opacity: 1 !important;
  transform: none !important;
}
.prose .roasist-cs-kpis,
.prose .roasist-cs-kpis * {
  margin-top: 0 !important;
}
.roasist-cs-kpis {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1.25rem;
  margin: 0 0 2.75rem 0 !important;
  align-items: stretch;
}
.roasist-cs-kpi-card {
  background: linear-gradient(180deg, #0F172A 0%, #1E1B4B 100%);
  border: 1px solid rgba(118, 2, 255, 0.35);
  border-radius: 1.25rem;
  padding: 1.6rem 1.5rem;
  box-shadow: 0 18px 40px -20px rgba(15, 23, 42, 0.45);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.roasist-cs-kpi-val {
  font-size: clamp(2.2rem, 3.2vw, 2.9rem);
  font-weight: 600;
  line-height: 1.05;
  letter-spacing: -0.02em;
  font-variant-numeric: tabular-nums;
  background: linear-gradient(90deg, #C084FC 0%, #38BDF8 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  margin-bottom: 0.65rem !important;
}
.roasist-cs-kpi-label {
  font-size: 1.02rem;
  font-weight: 600;
  color: #F8FAFC;
  line-height: 1.35;
  margin-bottom: 0.4rem !important;
}
.roasist-cs-kpi-sub {
  font-size: 0.86rem;
  color: rgba(226, 232, 240, 0.78);
  line-height: 1.42;
}
@media (max-width: 900px) {
  .roasist-cs-kpis {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
}
@media (min-width: 1024px) {
  .StatisticsPanel_logo__Y5wQT img {
    margin-bottom: 2.25rem !important;
  }
  .StatisticsPanel_heading__UrLlt {
    font-variant-numeric: tabular-nums !important;
    margin-bottom: 0.75rem !important;
  }
  .StatisticsPanel_description__csS74 {
    font-size: clamp(1.2rem, 1.5vw, 1.5rem) !important;
    line-height: 1.42 !important;
    margin-bottom: 2.5rem !important;
    max-width: 36ch !important;
    color: rgba(248, 250, 252, 0.92) !important;
  }
}
</style>"""


def build_kpi_html(kpis: list) -> str:
    cards = []
    for k in kpis:
        cards.append(
            f'<div class="roasist-cs-kpi-card">'
            f'<div class="roasist-cs-kpi-val">{k["value"]}</div>'
            f'<div class="roasist-cs-kpi-label">{k["label"]}</div>'
            f'<div class="roasist-cs-kpi-sub">{k["sub"]}</div>'
            f'</div>'
        )
    return '<div class="roasist-cs-kpis">' + "".join(cards) + "</div>"


def inject_case_study_css(html: str) -> str:
    css_block = get_case_study_css()
    if 'id="roasist-case-study-css"' in html:
        html = re.sub(
            r'<style id="roasist-case-study-css">.*?</style>',
            css_block,
            html,
            flags=re.DOTALL,
        )
    else:
        html = html.replace("</head>", css_block + "</head>", 1)
    return html


def build_case_study_page(template_html: str, cs: dict, lang: str, is_dist: bool, cdn_sha: str) -> str:
    html = template_html
    slug = cs["slug"]

    tr_route = f"/referanslar/{slug}/"
    en_route = f"/en/references/{slug}/"
    page_route = tr_route if lang == "tr" else en_route
    canonical_url = f"https://www.roasist.com{page_route}"
    tr_canonical = f"https://www.roasist.com{tr_route}"
    en_canonical = f"https://www.roasist.com{en_route}"

    title = cs["title_tr"] if lang == "tr" else cs["title_en"]
    full_title = f"{title} | Roasist"
    meta_desc = cs["meta_desc_tr"] if lang == "tr" else cs["meta_desc_en"]
    category = cs["category_tr"] if lang == "tr" else cs["category_en"]
    period = cs["period_tr"] if lang == "tr" else cs["period_en"]
    brand = cs["brand_tr"] if lang == "tr" else cs["brand_en"]
    client_prefix = "Müşteri: " if lang == "tr" else "Client: "
    hero_page_label = "referanslar" if lang == "tr" else "references"
    back_href = ("/roasist-web/referanslar/" if is_dist else "/referanslar/") if lang == "tr" else ("/roasist-web/en/references/" if is_dist else "/en/references/")
    back_href_flight = "/referanslar/" if lang == "tr" else "/en/references/"
    back_text = "Referanslara Dön" if lang == "tr" else "Back to Case Studies"

    if is_dist:
        hero_img_url = f"https://cdn.jsdelivr.net/gh/Roasist/roasist-web@{cdn_sha}/public/images/case-studies/{slug}-hero.jpg"
    else:
        hero_img_url = f"/images/case-studies/{slug}-hero.jpg"
    og_img_url = f"https://cdn.jsdelivr.net/gh/Roasist/roasist-web@{cdn_sha}/public/images/case-studies/{slug}-hero.jpg"

    kpis = cs["kpis_tr"] if lang == "tr" else cs["kpis_en"]
    body_raw = cs["body_tr"] if lang == "tr" else cs["body_en"]
    prose_html = build_kpi_html(kpis) + body_raw.replace("\n", "")

    # 1. Replace <head> tags in SSR
    html = re.sub(r"<title>.*?</title>", f"<title>{full_title}</title>", html, count=1, flags=re.DOTALL)
    html = re.sub(
        r'<meta name="description" content="[^"]*"/>',
        f'<meta name="description" content="{meta_desc}"/>',
        html,
        count=1,
    )
    html = re.sub(
        r'<link rel="canonical" href="[^"]*"/>',
        f'<link rel="canonical" href="{canonical_url}"/>',
        html,
        count=1,
    )
    html = re.sub(
        r'<link rel="alternate" hreflang="tr" href="[^"]*"/>',
        f'<link rel="alternate" hreflang="tr" href="{tr_canonical}"/>',
        html,
        count=1,
    )
    html = re.sub(
        r'<link rel="alternate" hreflang="en" href="[^"]*"/>',
        f'<link rel="alternate" hreflang="en" href="{en_canonical}"/>',
        html,
        count=1,
    )
    html = re.sub(
        r'<link rel="alternate" hreflang="x-default" href="[^"]*"/>',
        f'<link rel="alternate" hreflang="x-default" href="{tr_canonical}"/>',
        html,
        count=1,
    )
    html = re.sub(
        r'<meta property="og:title" content="[^"]*"/>',
        f'<meta property="og:title" content="{full_title}"/>',
        html,
        count=1,
    )
    html = re.sub(
        r'<meta property="og:description" content="[^"]*"/>',
        f'<meta property="og:description" content="{meta_desc}"/>',
        html,
        count=1,
    )
    html = re.sub(
        r'<meta property="og:url" content="[^"]*"/>',
        f'<meta property="og:url" content="{canonical_url}"/>',
        html,
        count=1,
    )
    html = re.sub(
        r'<meta property="og:image" content="[^"]*"/>',
        f'<meta property="og:image" content="{og_img_url}"/>',
        html,
        count=1,
    )
    html = re.sub(
        r'<meta name="twitter:title" content="[^"]*"/>',
        f'<meta name="twitter:title" content="{full_title}"/>',
        html,
        count=1,
    )
    html = re.sub(
        r'<meta name="twitter:description" content="[^"]*"/>',
        f'<meta name="twitter:description" content="{meta_desc}"/>',
        html,
        count=1,
    )
    html = re.sub(
        r'<meta name="twitter:image" content="[^"]*"/>',
        f'<meta name="twitter:image" content="{og_img_url}"/>',
        html,
        count=1,
    )

    # 2. Update JSON-LD in SSR
    json_ld_obj = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebPage",
                "@id": canonical_url,
                "url": canonical_url,
                "name": full_title,
                "isPartOf": {"@id": "https://www.roasist.com/#website"},
                "primaryImageOfPage": {"@id": f"{canonical_url}#primaryimage"},
                "image": {"@id": f"{canonical_url}#primaryimage"},
                "thumbnailUrl": og_img_url,
                "datePublished": "2026-06-18T11:21:58+00:00",
                "dateModified": "2026-07-16T10:24:33+00:00",
                "description": meta_desc,
                "breadcrumb": {"@id": f"{canonical_url}#breadcrumb"},
                "inLanguage": "tr-TR" if lang == "tr" else "en-US",
                "potentialAction": [{"@type": "ReadAction", "target": [canonical_url]}],
            },
            {
                "@type": "ImageObject",
                "inLanguage": "tr-TR" if lang == "tr" else "en-US",
                "@id": f"{canonical_url}#primaryimage",
                "url": og_img_url,
                "contentUrl": og_img_url,
                "width": 1400,
                "height": 787,
                "caption": title,
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{canonical_url}#breadcrumb",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Ana Sayfa" if lang == "tr" else "Home", "item": "https://www.roasist.com/" if lang == "tr" else "https://www.roasist.com/en/"},
                    {"@type": "ListItem", "position": 2, "name": "Referanslar" if lang == "tr" else "References", "item": "https://www.roasist.com/referanslar/" if lang == "tr" else "https://www.roasist.com/en/references/"},
                    {"@type": "ListItem", "position": 3, "name": title},
                ],
            },
        ],
    }
    json_ld_str = json.dumps(json_ld_obj, ensure_ascii=False, separators=(",", ":"))
    html = re.sub(
        r'<script type="application/ld\+json">.*?</script>',
        f'<script type="application/ld+json">{json_ld_str}</script>',
        html,
        count=1,
        flags=re.DOTALL,
    )

    # 3. Update Hero SSR HTML
    html, n1 = re.subn(
        r'(<button class="Hero_category__qOhtb">)(.*?)(</button>)',
        lambda m: m.group(1) + category + m.group(3),
        html,
        count=1,
    )
    html, n2 = re.subn(
        r'(<div class="Hero_left__0LdJX">.*?<h1><span[^>]*><span>)(.*?)(</span></span></h1>)',
        lambda m: m.group(1) + title + m.group(3),
        html,
        count=1,
        flags=re.DOTALL,
    )
    html, n3 = re.subn(
        r'(<div class="roasist-hero-page-label"><span><i></i>)([^<]*)(</span></div>)',
        lambda m: m.group(1) + hero_page_label + m.group(3),
        html,
        count=1,
    )
    html, n4 = re.subn(
        r'(<p class="Hero_date__30zpk"><span[^>]*><span>)(.*?)(</span></span></p>)',
        lambda m: m.group(1) + period + m.group(3),
        html,
        count=1,
        flags=re.DOTALL,
    )
    html, n5 = re.subn(
        r'(<p class="Hero_name__eLY42"><span[^>]*><span>)(.*?)(</span></span></p>)',
        lambda m: m.group(1) + client_prefix + "<!-- -->" + brand + m.group(3),
        html,
        count=1,
        flags=re.DOTALL,
    )
    html, n6 = re.subn(
        r'(<figure class="Hero_image__1mu0E">.*?<img )([^>]*)(/>)',
        lambda m: (
            m.group(1)
            + f'srcSet="{hero_img_url} 1400w" src="{hero_img_url}" alt="{title}" loading="eager" fetchPriority="low" height="787" width="1400" sizes="100vw"'
            + m.group(3)
        ),
        html,
        count=1,
        flags=re.DOTALL,
    )

    # 4. Update div.prose SSR HTML
    html, n7 = re.subn(
        r'(<div class="Text_textInner__lCgQa"><div class="prose">)(.*?)(</div></div></div></span></section></section><section class="Share_share__5W87u">)',
        lambda m: m.group(1) + prose_html + m.group(3),
        html,
        count=1,
        flags=re.DOTALL,
    )
    if not all([n1, n2, n3, n4, n5, n6, n7]):
        raise RuntimeError(f"SSR regex mismatch for {slug} ({lang}): counts={[n1, n2, n3, n4, n5, n6, n7]}")

    # 5. Update Share links & Back button in SSR HTML
    encoded_canon = urllib.parse.quote(canonical_url, safe="")
    html = re.sub(
        r'https://www\.linkedin\.com/shareArticle\?mini=true&amp;url=[^"\\]*',
        f"https://www.linkedin.com/shareArticle?mini=true&amp;url={encoded_canon}",
        html,
    )
    html = re.sub(
        r'https://www\.facebook\.com/sharer/sharer\.php\?u=[^"\\]*',
        f"https://www.facebook.com/sharer/sharer.php?u={encoded_canon}",
        html,
    )
    html = re.sub(
        r'https://twitter\.com/intent/tweet\?&amp;url=[^"\\]*',
        f"https://twitter.com/intent/tweet?&amp;url={encoded_canon}",
        html,
    )
    html = re.sub(
        r'(<div class="BlogPost_buttonOuter__M9Wmd">.*?<a class="Button_inner__fnyH6" href=")([^"]*)(".*?<span class="Button_textInner__JTTHe">)(.*?)(</span>)',
        lambda m: m.group(1) + back_href + m.group(3) + back_text + m.group(5),
        html,
        count=1,
        flags=re.DOTALL,
    )

    # 5b. Update RelatedPosts section in SSR HTML to display 3 other Case Studies
    other_studies = [c for c in CASE_STUDIES if c["slug"] != slug][:3]
    rel_heading = "Diğer Vaka Analizleri" if lang == "tr" else "More Case Studies"
    rel_btn_text = "Tüm Referansları Gör" if lang == "tr" else "View All Case Studies"
    rel_cards_ssr = []
    for ocs in other_studies:
        oslug = ocs["slug"]
        ohref = (f"/roasist-web/referanslar/{oslug}/" if is_dist else f"/referanslar/{oslug}/") if lang == "tr" else (f"/roasist-web/en/references/{oslug}/" if is_dist else f"/en/references/{oslug}/")
        oimg = f"https://cdn.jsdelivr.net/gh/Roasist/roasist-web@{cdn_sha}/public/images/case-studies/{oslug}-hero.jpg" if is_dist else f"/images/case-studies/{oslug}-hero.jpg"
        otag = ocs["brand_tr"] if lang == "tr" else ocs["brand_en"]
        otitle = ocs["title_tr"] if lang == "tr" else ocs["title_en"]
        rel_cards_ssr.append(
            f'<a class="BlogPostCard_post__fNGbL BlogPostCard_small__j18h2" data-animation="grid-item" href="{ohref}">'
            f'<div class="BlogPostCard_postImage__Q4k_I">'
            f'<div class="BlogPostCard_tags__RKboe"><span class="BlogPostCard_tag__Dv5HS">{otag} · {ocs["stat_main"]}</span></div>'
            f'<span class="Image_image__RAAdZ Image_fill__EiIzS">'
            f'<img data-srcset="{oimg} 1400w" data-src="{oimg}" alt="{otitle}" fetchPriority="low" height="787" width="1400" sizes="auto" class="lazyload"/>'
            f'</span></div>'
            f'<div class="BlogPostCard_postText__V0sxg"><h3>{otitle}</h3></div></a>'
        )
    rel_section_ssr = (
        '<section class="RelatedPosts_relatedPosts__xfLkb"><div class="DarkThemeSwitch_cover__hn_xc"></div>'
        '<div class="container"><div class="RelatedPosts_headingOuter__r3TEg">'
        f'<p class="RelatedPosts_heading__3kOeH"><span class="FadeInUp_container___uxva" data-fill="false">{rel_heading}</span></p>'
        '<div class="RelatedPosts_viewAllLinkDesktop__db363"><span class="FadeInUp_container___uxva" data-fill="false">'
        '<div class="Magnetic_magnetic__LncOy" data-fill="false"><div class="Button_button__JJiqJ Button_white__MQaf2" data-direction="forwards">'
        f'<a class="Button_inner__fnyH6" href="{back_href}"><span class="Button_border__hirH2"></span><span class="Button_text__IZaCD">'
        f'<span class="Button_textInner__JTTHe">{rel_btn_text}</span>'
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 17.1 15.17" class="Button_buttonArrow__0W9XI"><path d="m17.1,7.58s-.01-.04-.01-.06c.01-.22-.06-.45-.24-.61L9.23.19c-.31-.27-.78-.24-1.06.07-.27.31-.24.78.07,1.06l6.26,5.52H.75c-.41,0-.75.34-.75.75s.34.75.75.75h13.74l-6.26,5.52c-.31.27-.34.75-.07,1.06.15.17.35.25.56.25.18,0,.35-.06.5-.19l7.62-6.72c.18-.16.25-.39.24-.61,0-.02.01-.04.01-.06Z" fill="currentColor"></path></svg>'
        '</span></a></div></div></span></div></div></div>'
        '<div class="AnimatedGrid_grid__otAMD"><div class="container">'
        + "".join(rel_cards_ssr)
        + '</div></div>'
        '<div class="container"><div class="RelatedPosts_viewAllLinkMobile__joii8"><div class="Magnetic_magnetic__LncOy" data-fill="false">'
        '<div class="Button_button__JJiqJ Button_white__MQaf2" data-direction="forwards">'
        f'<a class="Button_inner__fnyH6" href="{back_href}"><span class="Button_border__hirH2"></span><span class="Button_text__IZaCD">'
        f'<span class="Button_textInner__JTTHe">{rel_btn_text}</span>'
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 17.1 15.17" class="Button_buttonArrow__0W9XI"><path d="m17.1,7.58s-.01-.04-.01-.06c.01-.22-.06-.45-.24-.61L9.23.19c-.31-.27-.78-.24-1.06.07-.27.31-.24.78.07,1.06l6.26,5.52H.75c-.41,0-.75.34-.75.75s.34.75.75.75h13.74l-6.26,5.52c-.31.27-.34.75-.07,1.06.15.17.35.25.56.25.18,0,.35-.06.5-.19l7.62-6.72c.18-.16.25-.39.24-.61,0-.02.01-.04.01-.06Z" fill="currentColor"></path></svg>'
        '</span></a></div></div></div></div></section>'
    )
    html = re.sub(
        r'<section class="RelatedPosts_relatedPosts__xfLkb">.*?</section>',
        lambda m: rel_section_ssr,
        html,
        count=1,
        flags=re.DOTALL,
    )

    # 6. Update <script data-roasist-ui> routes
    html = re.sub(
        r'<script data-roasist-ui data-lang="[^"]*" data-tr-route="[^"]*" data-en-route="[^"]*">',
        f'<script data-roasist-ui data-lang="{lang}" data-tr-route="{tr_route}" data-en-route="{en_route}">',
        html,
        count=1,
    )

    # 7. Update Next.js Flight payload (records 0, 27, 2d, f)
    m_flight = re.search(r'self\.__next_f\.push\(\[1,"(1:HL.*?)"\]\)</script>', html, re.DOTALL)
    if not m_flight:
        raise RuntimeError(f"Flight chunk not found for {slug} ({lang})")

    decoded = json.loads('"' + m_flight.group(1) + '"')

    # Update urlParts in record 0 so it matches initialTree ["","blog","ai-search-zero-click-seo"]
    decoded = decoded.replace(
        '"urlParts":["","blog","performans-pazarlamasinda-roas-optimizasyonu"]',
        '"urlParts":["","blog","ai-search-zero-click-seo"]',
    ).replace(
        '"urlParts":["","en","blog","how-to-calculate-and-optimize-roas"]',
        '"urlParts":["","blog","ai-search-zero-click-seo"]',
    )

    idx27 = decoded.find("27:T")
    idxf = decoded.find("f:[[", idx27)
    idx32 = decoded.find("\n32:I[", idxf)
    if idx27 == -1 or idxf == -1 or idx32 == -1:
        raise RuntimeError(f"Flight markers 27:T / f:[[ / 32:I[ not found for {slug} ({lang})")

    f_obj = json.loads(decoded[idxf + 2 : idx32])

    # Update f_obj[0] head metadata
    f_obj[0][0][3]["children"] = full_title
    for item in f_obj[0][1]:
        if isinstance(item, list) and len(item) >= 4 and isinstance(item[3], dict):
            props = item[3]
            if props.get("name") == "description":
                props["content"] = meta_desc
            elif props.get("rel") == "canonical":
                props["href"] = canonical_url
            elif props.get("property") in ("og:title", "twitter:title") or props.get("name") == "twitter:title":
                props["content"] = full_title
            elif props.get("property") in ("og:description", "twitter:description") or props.get("name") == "twitter:description":
                props["content"] = meta_desc
            elif props.get("property") == "og:url":
                props["content"] = canonical_url
            elif props.get("property") == "og:image" or props.get("name") == "twitter:image":
                props["content"] = og_img_url

    # Update f_obj[2] article tree
    article_children = f_obj[2][3]["children"]
    hero_container_children = article_children[0][3]["children"][3]["children"]
    # hero_left
    hero_left_children = hero_container_children[0][3]["children"]
    hero_left_children[0][3]["children"][3]["children"][3]["children"][0][3]["children"] = category
    hero_left_children[1][3]["children"][3]["children"][3]["children"] = title
    hero_left_children[2][3]["children"][3]["children"][1] = hero_page_label

    # hero_right
    hero_author_children = hero_container_children[1][3]["children"][3]["children"]
    hero_author_children[1][3]["children"][3]["children"][3]["children"] = period
    hero_author_children[2][3]["children"][3]["children"][3]["children"] = [client_prefix, brand]

    # hero_image
    hero_img_props = hero_container_children[2][3]["children"][3]["children"][3]["image"]
    hero_img_props["altText"] = title
    hero_img_props["srcSet"] = f"{hero_img_url} 1400w"
    hero_img_props["sourceUrl"] = hero_img_url
    hero_img_props["mediaDetails"] = {"width": 1400, "height": 787}

    # Share links in f_obj[2]
    share_links = article_children[2][3]["children"][3]["children"][3]["children"][3]["children"]
    share_links[1][3]["href"] = f"https://www.linkedin.com/shareArticle?mini=true&url={encoded_canon}"
    share_links[2][3]["href"] = f"https://www.facebook.com/sharer/sharer.php?u={encoded_canon}"
    share_links[3][3]["href"] = f"https://twitter.com/intent/tweet?&url={encoded_canon}"

    # Back button in f_obj[2]
    back_btn_props = article_children[3][3]["children"][3]["children"][3]["children"][3]
    back_btn_props["href"] = back_href_flight
    back_btn_props["text"] = back_text

    # RelatedPosts in f_obj[2] (article_children[4])
    rel_sec = article_children[4][3]["children"]
    rel_sec[1][3]["children"][3]["children"][0][3]["children"][3]["children"] = rel_heading
    rel_sec[1][3]["children"][3]["children"][1][3]["children"][3]["children"][3]["text"] = rel_btn_text
    rel_sec[1][3]["children"][3]["children"][1][3]["children"][3]["children"][3]["href"] = back_href_flight
    rel_cards_flight = rel_sec[2][3]["children"][3]["children"]
    for idx_c, ocs in enumerate(other_studies):
        if idx_c < len(rel_cards_flight):
            card_node = rel_cards_flight[idx_c]
            oslug = ocs["slug"]
            ohref_fl = f"/referanslar/{oslug}/" if lang == "tr" else f"/en/references/{oslug}/"
            oimg_fl = f"https://cdn.jsdelivr.net/gh/Roasist/roasist-web@{cdn_sha}/public/images/case-studies/{oslug}-hero.jpg" if is_dist else f"/images/case-studies/{oslug}-hero.jpg"
            otag_fl = f"{ocs['brand_tr' if lang == 'tr' else 'brand_en']} · {ocs['stat_main']}"
            otitle_fl = ocs["title_tr"] if lang == "tr" else ocs["title_en"]
            card_node[3]["href"] = ohref_fl
            img_wrap = card_node[3]["children"][0][3]["children"]
            img_wrap[0][3]["children"][1][0][3]["children"] = otag_fl
            img_wrap[1][3]["image"] = {
                "altText": otitle_fl,
                "srcSet": f"{oimg_fl} 1400w",
                "sourceUrl": oimg_fl,
                "mediaDetails": {"width": 1400, "height": 787},
            }
            card_node[3]["children"][1][3]["children"][3]["children"] = otitle_fl
    rel_sec[3][3]["children"][3]["children"][3]["text"] = rel_btn_text
    rel_sec[3][3]["children"][3]["children"][3]["href"] = back_href_flight

    new_f_str = "f:" + json.dumps(f_obj, ensure_ascii=False, separators=(",", ":"))
    json_ld_bytes_hex = format(len(json_ld_str.encode("utf-8")), "x")
    prose_bytes_hex = format(len(prose_html.encode("utf-8")), "x")

    new_27_2d_f = (
        f"27:T{json_ld_bytes_hex},{json_ld_str}"
        f"2d:T{prose_bytes_hex},{prose_html}"
        f"{new_f_str}"
    )

    new_decoded = decoded[:idx27] + new_27_2d_f + decoded[idx32:]
    new_encoded_inner = json.dumps(new_decoded, ensure_ascii=False)[1:-1]
    html = html[: m_flight.start(1)] + new_encoded_inner + html[m_flight.end(1) :]

    # 8. Inject Case Study CSS
    html = inject_case_study_css(html)

    return html


def build_statistics_slide_ssr(cs: dict, lang: str, is_dist: bool, cdn_sha: str) -> str:
    slug = cs["slug"]
    desc = cs["stat_desc_tr"] if lang == "tr" else cs["stat_desc_en"]
    btn_title = "Projeyi İncele" if lang == "tr" else "View Case Study"
    if lang == "tr":
        btn_href = f"/roasist-web/referanslar/{slug}/" if is_dist else f"/referanslar/{slug}/"
    else:
        btn_href = f"/roasist-web/en/references/{slug}/" if is_dist else f"/en/references/{slug}/"

    if is_dist:
        bg_url = f"https://cdn.jsdelivr.net/gh/Roasist/roasist-web@{cdn_sha}/public/images/case-studies/statistics-bg-black.jpg"
        vis_url = f"https://cdn.jsdelivr.net/gh/Roasist/roasist-web@{cdn_sha}/public/images/case-studies/{slug}-visual.png"
        logo_url = f"https://cdn.jsdelivr.net/gh/Roasist/roasist-web@{cdn_sha}/public{cs['logo']}"
    else:
        bg_url = "/images/case-studies/statistics-bg-black.jpg"
        vis_url = f"/images/case-studies/{slug}-visual.png"
        logo_url = cs["logo"]

    brand_alt = cs["brand_tr"] if lang == "tr" else cs["brand_en"]

    return (
        '<div class="StatisticsCarousel_swiperSlide__is8BS swiper-slide">'
        '<div class="StatisticsPanel_panel__5YHtR statisticPanel">'
        '<figure class="StatisticsPanel_backgroundImage___Dgsu">'
        '<span class="Image_image__RAAdZ Image_fill__EiIzS">'
        f'<img srcSet="{bg_url} 2244w" src="{bg_url}" alt="" loading="eager" fetchPriority="low" height="1222" width="2244" sizes="100vw"/>'
        '</span></figure>'
        '<div class="StatisticsPanel_panelWrap__XLJZs">'
        '<figure class="StatisticsPanel_logo__Y5wQT">'
        '<span class="Image_image__RAAdZ Image_intrinsic__JRoea">'
        f'<img src="{logo_url}" alt="{brand_alt}" loading="eager" fetchPriority="low" height="{cs["logo_h"]}" width="{cs["logo_w"]}" sizes="100vw"/>'
        '</span></figure>'
        '<figure class="StatisticsPanel_visualMobile__NTMW2">'
        '<span class="Image_image__RAAdZ Image_intrinsic__JRoea">'
        f'<img srcSet="{vis_url} 1354w" src="{vis_url}" alt="{brand_alt}" loading="eager" fetchPriority="low" height="1080" width="1354" sizes="100vw"/>'
        '</span></figure>'
        f'<h3 class="StatisticsPanel_heading__UrLlt">{cs["stat_main"]}</h3>'
        f'<span class="StatisticsPanel_description__csS74">{desc}</span>'
        '<div class="StatisticsPanel_buttons__FwZUj">'
        '<div class="Magnetic_magnetic__LncOy" data-fill="false">'
        '<div class="Button_button__JJiqJ Button_white__MQaf2" data-direction="forwards">'
        f'<a class="Button_inner__fnyH6" href="{btn_href}">'
        '<span class="Button_border__hirH2"></span>'
        '<span class="Button_text__IZaCD">'
        f'<span class="Button_textInner__JTTHe">{btn_title}</span>'
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 17.1 15.17" class="Button_buttonArrow__0W9XI">'
        '<path d="m17.1,7.58s-.01-.04-.01-.06c.01-.22-.06-.45-.24-.61L9.23.19c-.31-.27-.78-.24-1.06.07-.27.31-.24.78.07,1.06l6.26,5.52H.75c-.41,0-.75.34-.75.75s.34.75.75.75h13.74l-6.26,5.52c-.31.27-.34.75-.07,1.06.15.17.35.25.56.25.18,0,.35-.06.5-.19l7.62-6.72c.18-.16.25-.39.24-.61,0-.02.01-.04.01-.06Z" fill="currentColor"></path>'
        '</svg></span></a></div></div></div></div>'
        '<figure class="StatisticsPanel_visual__W0d30">'
        '<span class="Image_image__RAAdZ Image_contain__awbZj">'
        f'<img srcSet="{vis_url} 1354w" src="{vis_url}" alt="{brand_alt}" loading="eager" fetchPriority="low" height="1080" width="1354" sizes="100vw"/>'
        '</span></figure></div></div>'
    )


def build_statistics_flight_item(cs: dict, lang: str, is_dist: bool, cdn_sha: str) -> dict:
    slug = cs["slug"]
    desc = cs["stat_desc_tr"] if lang == "tr" else cs["stat_desc_en"]
    btn_title = "Projeyi İncele" if lang == "tr" else "View Case Study"
    btn_url = f"/referanslar/{slug}/" if lang == "tr" else f"/en/references/{slug}/"
    brand_alt = cs["brand_tr"] if lang == "tr" else cs["brand_en"]

    if is_dist:
        bg_url = f"https://cdn.jsdelivr.net/gh/Roasist/roasist-web@{cdn_sha}/public/images/case-studies/statistics-bg-black.jpg"
        vis_url = f"https://cdn.jsdelivr.net/gh/Roasist/roasist-web@{cdn_sha}/public/images/case-studies/{slug}-visual.png"
        logo_url = f"https://cdn.jsdelivr.net/gh/Roasist/roasist-web@{cdn_sha}/public{cs['logo']}"
    else:
        bg_url = "/images/case-studies/statistics-bg-black.jpg"
        vis_url = f"/images/case-studies/{slug}-visual.png"
        logo_url = cs["logo"]

    return {
        "mainStatistic": cs["stat_main"],
        "description": desc,
        "button": {
            "title": btn_title,
            "url": btn_url,
            "target": "",
        },
        "brandLogo": {
            "altText": brand_alt,
            "srcSet": None,
            "sourceUrl": logo_url,
            "mediaDetails": {
                "width": cs["logo_w"],
                "height": cs["logo_h"],
            },
        },
        "brandVisual": {
            "altText": brand_alt,
            "srcSet": f"{vis_url} 1354w",
            "sourceUrl": vis_url,
            "mediaDetails": {
                "width": 1354,
                "height": 1080,
            },
        },
        "backgroundImage": {
            "altText": "",
            "srcSet": f"{bg_url} 2244w",
            "sourceUrl": bg_url,
            "mediaDetails": {
                "width": 2244,
                "height": 1222,
            },
        },
    }


def update_homepage_statistics(file_path: str, lang: str, is_dist: bool, cdn_sha: str) -> None:
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Note: Swiper in StatisticsCarousel starts at slides.length - 1 and steps backwards.
    # Reversing CASE_STUDIES puts Medistate at index 4 (top of stack first), then Summer Homes, ACC, Beşsekiz, Gekoo.
    ordered_studies = list(reversed(CASE_STUDIES))

    # 1. Replace SSR .swiper-wrapper inside StatisticsCarousel_swiper__PGdj6
    slides_ssr = "".join(build_statistics_slide_ssr(cs, lang, is_dist, cdn_sha) for cs in ordered_studies)
    pattern_ssr = re.compile(
        r'(<div class="StatisticsCarousel_swiper__PGdj6 swiper"><div class="swiper-wrapper">).*?(</div><div class="StatisticsCarousel_swiperNav__Pi054">)',
        re.DOTALL,
    )
    if not pattern_ssr.search(html):
        raise RuntimeError(f"StatisticsCarousel_swiper SSR block not found in {file_path}")
    html = pattern_ssr.sub(lambda m: m.group(1) + slides_ssr + m.group(2), html, count=1)

    # 2. Replace Flight record 11 statistics array
    flight_updated = False
    for fm in re.finditer(r'self\.__next_f\.push\(\[1,"(.*?)"\]\)</script>', html, re.DOTALL):
        s = fm.group(1)
        if "Statistics_statistics__vWlOY" not in s:
            continue
        decoded = json.loads('"' + s + '"')
        idx11 = decoded.find("\n11:[")
        end11 = decoded.find("\n", idx11 + 1)
        if idx11 == -1 or end11 == -1:
            raise RuntimeError(f"Record 11 boundary not found in {file_path}")
        rec11 = json.loads(decoded[idx11 + 4 : end11])

        def replace_stats(node):
            if isinstance(node, dict) and node.get("className") == "Statistics_statistics__vWlOY":
                for child in node.get("children", []):
                    if isinstance(child, list) and len(child) >= 4 and isinstance(child[3], dict) and "statistics" in child[3]:
                        child[3]["statistics"] = [
                            build_statistics_flight_item(cs, lang, is_dist, cdn_sha) for cs in ordered_studies
                        ]
                        return True
            if isinstance(node, list):
                for item in node:
                    if replace_stats(item):
                        return True
            elif isinstance(node, dict):
                for v in node.values():
                    if replace_stats(v):
                        return True
            return False

        if not replace_stats(rec11):
            raise RuntimeError(f"Failed to locate statistics array inside record 11 in {file_path}")

        new_rec11_str = "\n11:" + json.dumps(rec11, ensure_ascii=False, separators=(",", ":"))
        new_decoded = decoded[:idx11] + new_rec11_str + decoded[end11:]
        new_encoded = json.dumps(new_decoded, ensure_ascii=False)[1:-1]
        html = html[: fm.start(1)] + new_encoded + html[fm.end(1) :]
        flight_updated = True
        break

    if not flight_updated:
        raise RuntimeError(f"Flight chunk with Statistics_statistics__vWlOY not updated in {file_path}")

    # 3. Inject Case Study / StatisticsPanel typography CSS
    html = inject_case_study_css(html)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Updated homepage statistics in: {file_path}")


def patch_swiper_chunk(chunk_path: str) -> None:
    if not os.path.exists(chunk_path):
        return
    with open(chunk_path, "r", encoding="utf-8") as f:
        js = f.read()
    new_js = (
        js.replace("creativeEffect:{limitProgress:3,", "creativeEffect:{limitProgress:4,")
        .replace(
            'children:(0,r.jsx)(l.default,{image:null==i?void 0:i.backgroundImage})',
            'children:(0,r.jsx)(l.default,{image:null==i?void 0:i.backgroundImage,lazy:!1})',
        )
        .replace(
            'children:(0,r.jsx)(l.default,{image:null==i?void 0:i.brandLogo,layout:"intrinsic"})',
            'children:(0,r.jsx)(l.default,{image:null==i?void 0:i.brandLogo,layout:"intrinsic",lazy:!1})',
        )
        .replace(
            'children:(0,r.jsx)(l.default,{image:null==i?void 0:i.brandVisual,layout:"intrinsic"})',
            'children:(0,r.jsx)(l.default,{image:null==i?void 0:i.brandVisual,layout:"intrinsic",lazy:!1})',
        )
        .replace(
            'children:(0,r.jsx)(l.default,{image:null==i?void 0:i.brandVisual,layout:"contain"})',
            'children:(0,r.jsx)(l.default,{image:null==i?void 0:i.brandVisual,layout:"contain",lazy:!1})',
        )
    )
    if new_js != js:
        with open(chunk_path, "w", encoding="utf-8") as f:
            f.write(new_js)
        print(f"Patched limitProgress:4 and lazy:!1 in {chunk_path}")
    else:
        print(f"limitProgress:4 and lazy:!1 already present in {chunk_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cdn-sha", default="", help="Git commit SHA on main for jsDelivr CDN URLs in dist/")
    args = parser.parse_args()

    cdn_sha = args.cdn_sha.strip()
    if not cdn_sha:
        cdn_sha = (
            subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT)
            .decode("utf-8")
            .strip()
        )
    print(f"Using CDN SHA for dist/: {cdn_sha}")

    # 1. Patch Swiper creativeEffect limitProgress in public and dist chunks
    patch_swiper_chunk(os.path.join(ROOT, "public/_next/static/chunks/app/(home)/page-b58f77e3dc47742c.js"))
    patch_swiper_chunk(os.path.join(ROOT, "dist/_next/static/chunks/app/(home)/page-b58f77e3dc47742c.js"))

    # 2. Load blog templates for public and dist (TR & EN)
    templates = {
        ("tr", False): os.path.join(ROOT, "public/blog/performans-pazarlamasinda-roas-optimizasyonu/index.html"),
        ("en", False): os.path.join(ROOT, "public/en/blog/how-to-calculate-and-optimize-roas/index.html"),
        ("tr", True): os.path.join(ROOT, "dist/blog/performans-pazarlamasinda-roas-optimizasyonu/index.html"),
        ("en", True): os.path.join(ROOT, "dist/en/blog/how-to-calculate-and-optimize-roas/index.html"),
    }
    loaded_templates = {}
    for key, tpath in templates.items():
        with open(tpath, "r", encoding="utf-8") as f:
            loaded_templates[key] = f.read()

    # 3. Build 5 TR + 5 EN Case Study pages in public/ and dist/
    for cs in CASE_STUDIES:
        slug = cs["slug"]
        for is_dist in (False, True):
            base_dir = os.path.join(ROOT, "dist" if is_dist else "public")
            # TR: /referanslar/<slug>/index.html
            tr_out_dir = os.path.join(base_dir, "referanslar", slug)
            os.makedirs(tr_out_dir, exist_ok=True)
            tr_html = build_case_study_page(loaded_templates[("tr", is_dist)], cs, "tr", is_dist, cdn_sha)
            tr_out_path = os.path.join(tr_out_dir, "index.html")
            with open(tr_out_path, "w", encoding="utf-8") as f:
                f.write(tr_html)

            # EN: /en/references/<slug>/index.html
            en_out_dir = os.path.join(base_dir, "en", "references", slug)
            os.makedirs(en_out_dir, exist_ok=True)
            en_html = build_case_study_page(loaded_templates[("en", is_dist)], cs, "en", is_dist, cdn_sha)
            en_out_path = os.path.join(en_out_dir, "index.html")
            with open(en_out_path, "w", encoding="utf-8") as f:
                f.write(en_html)

            print(f"Built [{'dist' if is_dist else 'public'}] case studies for: {slug}")

    # 4. Update Homepage Statistics ("Ölçülebilir Sonuçlar" / "Measurable Results")
    update_homepage_statistics(os.path.join(ROOT, "public/kota-roasist-local.html"), "tr", False, cdn_sha)
    update_homepage_statistics(os.path.join(ROOT, "public/en/index.html"), "en", False, cdn_sha)
    update_homepage_statistics(os.path.join(ROOT, "dist/index.html"), "tr", True, cdn_sha)
    update_homepage_statistics(os.path.join(ROOT, "dist/en/index.html"), "en", True, cdn_sha)


if __name__ == "__main__":
    main()
