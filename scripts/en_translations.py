#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Complete English (Roasist Global /en/*) content & bidirectional route definitions.
"""

CDN_BASE = "https://cdn.jsdelivr.net/gh/Roasist/roasist-web@189b2e0aee16a196d88d8895fb3795810c6d17f9"

# Bidirectional route map (canonical paths with trailing slashes)
TR_TO_EN_ROUTES = {
    "/": "/en/",
    "/hakkimizda/": "/en/who-we-are/",
    "/hizmetler/": "/en/services/",
    "/hizmetler/performans-pazarlamasi/": "/en/performance-marketing/",
    "/hizmetler/performans-pazarlamasi/google-reklamlari/": "/en/google-ads/",
    "/hizmetler/google-reklamlari/": "/en/google-ads/",
    "/hizmetler/performans-pazarlamasi/instagram-reklamlari/": "/en/instagram-ads/",
    "/hizmetler/instagram-reklamlari/": "/en/instagram-ads/",
    "/hizmetler/performans-pazarlamasi/facebook-reklamlari/": "/en/facebook-ads/",
    "/hizmetler/facebook-reklamlari/": "/en/facebook-ads/",
    "/hizmetler/performans-pazarlamasi/tiktok-reklamlari/": "/en/tiktok-ads/",
    "/hizmetler/tiktok-reklamlari/": "/en/tiktok-ads/",
    "/hizmetler/performans-pazarlamasi/linkedin-reklamlari/": "/en/linkedin-ads/",
    "/hizmetler/linkedin-reklamlari/": "/en/linkedin-ads/",
    "/hizmetler/performans-pazarlamasi/yandex-reklamlari/": "/en/yandex-ads/",
    "/hizmetler/yandex-reklamlari/": "/en/yandex-ads/",
    "/hizmetler/performans-pazarlamasi/bing-reklamlari/": "/en/bing-ads/",
    "/hizmetler/bing-reklamlari/": "/en/bing-ads/",
    "/hizmetler/seo/": "/en/seo/",
    "/hizmetler/grafik-tasarim/": "/en/graphic-design/",
    "/hizmetler/web-tasarim/": "/en/web-design/",
    "/hizmetler/360-derece-dijital-pazarlama-yonetimi/": "/en/360-digital-marketing-management/",
    "/referanslar/": "/en/references/",
    "/blog/": "/en/blog/",
    "/blog/Performans-Pazarlamasi-Nedir/": "/en/blog/what-is-performance-marketing/",
    "/blog/Veriye-Dayali-Dijital-Pazarlama-Stratejisi-Nedir/": "/en/blog/what-is-performance-marketing/",
    "/blog/kurumsal-seo-ve-yapay-zeka-aramalari-aeo-rehberi/": "/en/blog/enterprise-seo-and-ai-search-aeo-guide/",
    "/blog/360-dijital-pazarlama-kanallar-arasi-sinerji/": "/en/blog/enterprise-seo-and-ai-search-aeo-guide/",
    "/blog/performans-pazarlamasinda-roas-optimizasyonu/": "/en/blog/how-to-calculate-and-optimize-roas/",
    "/blog/Reklam-Harcamalarinin-Geri-Donusu-ROAS-Nasil-Hesaplanir/": "/en/blog/how-to-calculate-and-optimize-roas/",
    "/iletisim/": "/en/contact-us/",
    "/start-your-project/": "/en/contact-us/",
    "/gizlilik-politikasi-ve-kullanim-sartlari/": "/en/privacy-policy-and-terms-of-use/",
}

EN_TO_TR_ROUTES = {
    "/en/": "/",
    "/en/who-we-are/": "/hakkimizda/",
    "/en/services/": "/hizmetler/",
    "/en/performance-marketing/": "/hizmetler/performans-pazarlamasi/",
    "/en/google-ads/": "/hizmetler/performans-pazarlamasi/google-reklamlari/",
    "/en/instagram-ads/": "/hizmetler/performans-pazarlamasi/instagram-reklamlari/",
    "/en/facebook-ads/": "/hizmetler/performans-pazarlamasi/facebook-reklamlari/",
    "/en/tiktok-ads/": "/hizmetler/performans-pazarlamasi/tiktok-reklamlari/",
    "/en/linkedin-ads/": "/hizmetler/performans-pazarlamasi/linkedin-reklamlari/",
    "/en/yandex-ads/": "/hizmetler/performans-pazarlamasi/yandex-reklamlari/",
    "/en/bing-ads/": "/hizmetler/performans-pazarlamasi/bing-reklamlari/",
    "/en/seo/": "/hizmetler/seo/",
    "/en/graphic-design/": "/hizmetler/grafik-tasarim/",
    "/en/web-design/": "/hizmetler/web-tasarim/",
    "/en/360-digital-marketing-management/": "/hizmetler/360-derece-dijital-pazarlama-yonetimi/",
    "/en/references/": "/referanslar/",
    "/en/blog/": "/blog/",
    "/en/blog/what-is-performance-marketing/": "/blog/Performans-Pazarlamasi-Nedir/",
    "/en/blog/enterprise-seo-and-ai-search-aeo-guide/": "/blog/kurumsal-seo-ve-yapay-zeka-aramalari-aeo-rehberi/",
    "/en/blog/how-to-calculate-and-optimize-roas/": "/blog/Reklam-Harcamalarinin-Geri-Donusu-ROAS-Nasil-Hesaplanir/",
    "/en/contact-us/": "/iletisim/",
    "/en/privacy-policy-and-terms-of-use/": "/gizlilik-politikasi-ve-kullanim-sartlari/",
}

# Navigation Menu & Footer EN
NAV_NODES_EN = [
    {"databaseId": 936, "label": "Work", "uri": "/en/references/", "childItems": {"nodes": []}},
    {"databaseId": 946, "label": "About Us", "uri": "/en/who-we-are/", "childItems": {"nodes": []}},
    {
        "databaseId": 937,
        "label": "Services",
        "uri": "#",
        "childItems": {
            "nodes": [
                {"databaseId": 942, "label": "Performance Marketing", "uri": "/en/performance-marketing/"},
                {"databaseId": 944, "label": "SEO", "uri": "/en/seo/"},
                {"databaseId": 945, "label": "Graphic Design", "uri": "/en/graphic-design/"},
                {"databaseId": 943, "label": "Web Design", "uri": "/en/web-design/"},
                {"databaseId": 941, "label": "360° Digital Marketing", "uri": "/en/360-digital-marketing-management/"},
            ]
        },
    },
    {"databaseId": 938, "label": "Blog", "uri": "/en/blog/", "childItems": {"nodes": []}},
    {"databaseId": 940, "label": "Contact", "uri": "/en/contact-us/", "childItems": {"nodes": []}},
]

FOOTER_NAV_EN = [
    ("Contact", "/en/contact-us/"),
    ("About Us", "/en/who-we-are/"),
    ("Privacy Policy", "/en/privacy-policy-and-terms-of-use/"),
]

FOOTER_SERVICES_EN = [
    ("Performance Marketing", "/en/performance-marketing/"),
    ("SEO", "/en/seo/"),
    ("Graphic Design", "/en/graphic-design/"),
    ("Web Design", "/en/web-design/"),
    ("360° Digital Marketing", "/en/360-digital-marketing-management/"),
]

# 3 Real Roasist Testimonials in English (for inner service pages + homepage)
ROASIST_TESTIMONIALS_EN = [
    {
        "text": (
            '"Their strategic ownership throughout our ad campaigns, going above and beyond our agreement '
            "with proactive graphic design contributions, and providing 24/7 support proved they care about "
            "our business as much as we do. You can partner with Roasist with complete confidence.\""
        ),
        "backgroundColor": "#EDE9FE",
        "name": "Burak Özhan",
        "speciality": "Project Program Coordinator",
        "button": {"title": "View Case Study", "url": "/en/references/", "target": ""},
        "logo_rel": "ref-14.png",
        "width": 241,
        "height": 34,
    },
    {
        "text": (
            '"We have been working with Roasist for nearly two years. Every question is answered with complete '
            "honesty and every challenge is resolved swiftly. Comparing our before-and-after revenue, their "
            "impact on our profitability has been tremendous. Thank you for a truly professional partnership.\""
        ),
        "backgroundColor": "#E0E7FF",
        "name": "Gaye Tukar",
        "speciality": "Entrepreneur & Founder",
        "button": {"title": "View Case Study", "url": "/en/references/", "target": ""},
        "logo_rel": "ref-04.png",
        "width": 640,
        "height": 388,
    },
    {
        "text": (
            '"They work relentlessly for your growth without watching the clock. If you are looking for a '
            "transparent, disciplined, and genuinely ROI-obsessed digital marketing agency, I wholeheartedly "
            'recommend Roasist."'
        ),
        "backgroundColor": "#F3E8FF",
        "name": "Celal Kandemir",
        "speciality": "Business Owner",
        "button": {"title": "View Case Study", "url": "/en/references/", "target": ""},
        "logo_rel": "ref-25.png",
        "width": 233,
        "height": 53,
    },
]

# 3 English Blog Articles
BLOG_CATEGORIES_EN = [
    {"databaseId": 101, "name": "Performance Marketing", "slug": "performance-marketing"},
    {"databaseId": 102, "name": "SEO & AEO", "slug": "seo-aeo"},
    {"databaseId": 103, "name": "Digital Strategy", "slug": "digital-strategy"},
]

BLOG_POSTS_EN = [
    {
        "databaseId": 3001,
        "slug": "what-is-performance-marketing",
        "title": "What Is Performance Marketing & How Does It Scale Revenue?",
        "seo_title": "What Is Performance Marketing & How Does It Scale Revenue? | Roasist Blog",
        "meta_desc": (
            "Discover how data-driven performance marketing across Google Ads, Meta, TikTok, LinkedIn, "
            "Yandex, and Bing turns ad spend into predictable, profitable revenue."
        ),
        "category": BLOG_CATEGORIES_EN[0],
        "read_time": "6 min read",
        "date_label": "2026",
        "image": "https://kota-content.b-cdn.net/app/uploads/2025/05/10-creative-websites-blog-header-1400x788.png",
        "img_w": 1400,
        "img_h": 788,
        "intro": (
            "Performance marketing replaces guesswork with full-funnel accountability—aligning every "
            "impression, click, and creative asset around measurable customer acquisition and ROAS."
        ),
        "body_html": (
            "<h2>Why Performance Marketing Wins in 2026</h2>\n"
            "<p>Traditional brand advertising asks you to spend budget up front and hope awareness eventually "
            "converts. Performance marketing flips the equation: every campaign across <strong>Google Ads</strong>, "
            "<strong>Meta (Instagram &amp; Facebook)</strong>, <strong>TikTok</strong>, <strong>LinkedIn</strong>, "
            "<strong>Yandex</strong>, and <strong>Bing</strong> is engineered around verifiable commercial actions—"
            "qualified leads, booked consultations, e-commerce purchases, and net revenue.</p>\n"
            "<h2>Core Pillars of a High-ROAS Architecture</h2>\n"
            "<ul>"
            "<li><strong>Server-Side Measurement (GA4 + GTM + CAPI):</strong> Accurate first-party conversion signals "
            "feed smart bidding algorithms with real purchase values rather than noisy pageviews.</li>"
            "<li><strong>Intent &amp; Audience Segmentation:</strong> High-intent search queries on Google, Bing, and "
            "Yandex capture active demand, while Meta, TikTok, and LinkedIn build qualified pipeline.</li>"
            "<li><strong>Continuous Creative &amp; CRO Testing:</strong> Systematic A/B testing across hooks, ad formats, "
            "and landing pages compounds conversion rates month over month.</li>"
            "</ul>\n"
            "<h2>Full Account Ownership &amp; Radical Transparency</h2>\n"
            "<p>At Roasist, every ad account and analytics property belongs 100% to your company. Through live "
            "Looker Studio dashboards, your leadership team tracks spend, CPA, and ROAS in real time—so scaling "
            "decisions are always backed by hard numbers.</p>\n"
        ),
    },
    {
        "databaseId": 3002,
        "slug": "enterprise-seo-and-ai-search-aeo-guide",
        "title": "Enterprise SEO & AI Search (AEO / GEO): The Complete Growth Guide",
        "seo_title": "Enterprise SEO & AI Search (AEO / GEO) Guide | Roasist Blog",
        "meta_desc": (
            "Learn how technical SEO, semantic content architecture, and Answer Engine Optimization (AEO) "
            "position your brand at the top of Google and AI search engines like ChatGPT and Perplexity."
        ),
        "category": BLOG_CATEGORIES_EN[1],
        "read_time": "7 min read",
        "date_label": "2026",
        "image": "https://kota-content.b-cdn.net/app/uploads/2025/05/AI-Search-zero-click-SEO-blog-header-1400x788.png",
        "img_w": 1400,
        "img_h": 788,
        "intro": (
            "Modern search happens simultaneously on Google SERPs and inside AI answer engines like ChatGPT, "
            "Google AI Overviews, Gemini, and Perplexity. Winning both requires technical precision and authority."
        ),
        "body_html": (
            "<h2>From Keywords to Entities &amp; Answer Engines</h2>\n"
            "<p>Decision-makers no longer search with two-word phrases alone—they ask complex commercial questions "
            "directly to AI assistants and search engines. Combining <strong>Enterprise Technical SEO</strong> with "
            "<strong>Answer Engine Optimization (AEO &amp; GEO)</strong> ensures your brand is cited as the trusted "
            "recommendation when buyers evaluate solutions.</p>\n"
            "<h2>Three Foundations of Sustainable Organic Dominance</h2>\n"
            "<ul>"
            "<li><strong>Core Web Vitals &amp; Crawl Efficiency:</strong> Clean information architecture, instant load "
            "speeds, and structured Schema.org JSON-LD markup allow crawlers and LLMs to parse your expertise effortlessly.</li>"
            "<li><strong>Commercial-Intent Topic Clusters:</strong> Authoritative, data-backed pages built around "
            "real search demand rather than superficial traffic padding.</li>"
            "<li><strong>Paid + Organic Synergy:</strong> High-converting search terms from Google Ads inform your "
            "SEO roadmap, while stronger landing page relevance lowers your paid CPCs.</li>"
            "</ul>\n"
            "<h2>Compounding Returns Without Rising Ad Costs</h2>\n"
            "<p>Unlike paid traffic alone, enterprise SEO builds a permanent digital asset that lowers blended "
            "customer acquisition cost (CAC) quarter after quarter.</p>\n"
        ),
    },
    {
        "databaseId": 3003,
        "slug": "how-to-calculate-and-optimize-roas",
        "title": "How to Calculate & Optimize ROAS Across Multi-Channel Campaigns",
        "seo_title": "How to Calculate & Optimize ROAS | Roasist Blog",
        "meta_desc": (
            "Master Return on Ad Spend (ROAS) calculation, unit economics, break-even thresholds, and "
            "multi-channel budget optimization for e-commerce and lead-generation brands."
        ),
        "category": BLOG_CATEGORIES_EN[2],
        "read_time": "5 min read",
        "date_label": "2026",
        "image": "https://kota-content.b-cdn.net/app/uploads/2025/04/10-tips-blog-header-1400x788.png",
        "img_w": 1400,
        "img_h": 788,
        "intro": (
            "Return on Ad Spend (ROAS) is the north-star metric of performance marketing—yet maximizing true "
            "profit requires pairing ROAS with gross margin, LTV, and conversion rate optimization."
        ),
        "body_html": (
            "<h2>Understanding the ROAS Formula &amp; Break-Even Target</h2>\n"
            "<p><strong>ROAS = Revenue Attributable to Ads / Total Ad Spend.</strong> If your campaign invests "
            "$10,000 and generates $64,000 in verified revenue, your ROAS is <strong>6.4x (640%)</strong>. "
            "However, healthy scaling begins by calculating your exact break-even ROAS based on product margins "
            "and fulfillment costs.</p>\n"
            "<h2>Four High-Leverage Levers to Lift ROAS</h2>\n"
            "<ul>"
            "<li><strong>Eliminate Wasted Search &amp; Placement Spend:</strong> Rigorous negative keyword hygiene "
            "and placement exclusions immediately reclaim 15%–30% of wasted budget.</li>"
            "<li><strong>Value-Based Bidding (tROAS):</strong> Passing dynamic cart values or offline CRM deal "
            "stages back to Google and Meta trains bidding models to pursue high-value buyers.</li>"
            "<li><strong>Landing Page Speed &amp; Friction Removal:</strong> Lifting conversion rate from 1.5% to "
            "2.4% increases ROAS by 60% without spending an extra dollar on media.</li>"
            "<li><strong>Cross-Channel Retargeting:</strong> Capturing high-intent visitors across Meta, YouTube, "
            "Yandex, and Display closes complex B2B and luxury decision cycles.</li>"
            "</ul>\n"
        ),
    },
]

# Timeline Turkish -> English exact dictionary (reversing build_1to1_kota_pages.py COMMON_PAIRS)
TIMELINE_TR_TO_EN = [
    ("1. Aşama", "Phase 1"),
    ("2. Aşama", "Phase 2"),
    ("Uygulama", "Execution"),
    ("Test & Kalite", "QA & Testing"),
    ("Sürekli Büyüme", "Ongoing Scale"),
    ("Marka ve hedef analizi", "Brand & commercial goal audit"),
    ("Mevcut dijital varlık denetimi", "Existing digital asset audit"),
    ("GA4 ve dönüşüm verisi incelemesi", "GA4 & conversion tracking review"),
    ("Rakip ve pazar araştırması", "Competitor & market intelligence"),
    ("Hedef kitle segmentasyonu", "Audience & intent segmentation"),
    ("Stratejik başlangıç toplantısı", "Strategic kick-off workshop"),
    ("Büyüme ve KPI hedefleri", "Growth & unit-economics KPIs"),
    ("İçerik ve mesaj mimarisi", "Messaging & content architecture"),
    ("Arama görünürlüğü planlaması", "Search & AI visibility roadmap"),
    ("Dönüşüm hunisi (CRO) kurgusu", "Conversion funnel (CRO) blueprint"),
    ("Teknik gereksinim analizi", "Technical & tracking specification"),
    ("Veri ve altyapı yol haritası", "Data & attribution roadmap"),
    ("Bilgi ve sayfa mimarisi", "Information & landing architecture"),
    ("Kullanıcı akış (UX) tasarımı", "User journey (UX) design"),
    ("Müşteri yolculuğu haritalama", "Full-funnel customer mapping"),
    ("Dönüşüm odaklı içerik planı", "Conversion-focused content plan"),
    ("Prototip ve wireframe kurgusu", "Wireframing & interactive flows"),
    ("Fonksiyonel teknik şartname", "Functional & technical specs"),
    ("Kreatif konsept geliştirme", "Creative concept development"),
    ("Dijital sanat yönetmenliği", "Digital art direction"),
    ("Görsel kimlik ve tipografi", "Visual identity & typography"),
    ("Mikro etkileşim ve hareket dili", "Micro-interactions & motion"),
    ("Deneyim ve etkileşim kurgusu", "Interactive experience design"),
    ("Kreatif sunum ve onay", "Creative review & sign-off"),
    ("Mobil öncelikli (Responsive) tasarım", "Mobile-first responsive design"),
    ("Modüler tasarım sistemi", "Modular design system"),
    ("Yüksek dönüşümlü arayüz kurgusu", "High-converting UI architecture"),
    ("CRO temas noktası optimizasyonu", "CRO touchpoint optimization"),
    ("Uygulamaya hazır tasarım teslimi", "Production-ready creative assets"),
    ("Yüksek hızlı önyüz geliştirme", "High-speed front-end engineering"),
    ("Güvenli altyapı ve entegrasyon", "Secure infrastructure & APIs"),
    ("Yönetim paneli ve veri kurulumu", "CMS & data layer configuration"),
    ("Özel bileşen ve modül kodlaması", "Custom component engineering"),
    ("Akıcı animasyon entegrasyonu", "Fluid motion integration"),
    ("CRM, Pixel ve CAPI entegrasyonları", "CRM, Pixel & Server-Side CAPI"),
    ("Core Web Vitals hız optimizasyonu", "Core Web Vitals speed tuning"),
    ("İçerik ve kampanya girişi", "Campaign & content deployment"),
    ("Tüm cihazlarda uyumluluk testi", "Cross-device compatibility QA"),
    ("Tarayıcı ve hız testleri", "Browser & load-speed verification"),
    ("Kullanılabilirlik ve erişim kontrolü", "Accessibility & usability audit"),
    ("Yük ve dönüşüm takip testleri", "Conversion tag & event verification"),
    ("Ekip eğitimi ve dokümantasyon", "Team onboarding & documentation"),
    ("Kapsamlı kalite kontrol (QA)", "End-to-end quality assurance"),
    ("Canlıya geçiş ve lansman planı", "Go-live & launch orchestration"),
    ("Canlı yayın ve sunucu aktivasyonu", "Production launch & monitoring"),
    ("Yönlendirme ve veri koruma", "URL integrity & data protection"),
    ("Teknik SEO ve AI görünürlük", "Technical SEO & AI search readiness"),
    ("GA4, GTM ve Looker Studio kurulumu", "GA4, GTM & Looker Studio live"),
    ("Lansman sonrası canlı izleme", "Post-launch performance monitoring"),
    ("Raporlama ve yönetim kılavuzu", "Executive reporting playbook"),
    ("Sürekli büyüme ve optimizasyon packages", "Continuous growth & ROAS scaling"),
    ("Sürekli büyüme ve optimizasyon", "Continuous growth & ROAS scaling"),
]

# 13 English Service Pages mapped to their source TR service HTML template
EN_SERVICES_SPECS = [
    {
        "en_slug": "services",
        "src_tr": "hizmetler",
        "title": "Our Services | 360° Digital Marketing, SEO & Web Design | Roasist",
        "metaDesc": (
            "Scale your brand profitably with Roasist's integrated performance marketing, Google & Meta Ads, "
            "enterprise SEO & AEO, creative design, and conversion-focused web development."
        ),
        "h1": "360° Digital Growth & Marketing Services",
        "heroLines": ["360° solutions", "built to <em>scale</em>", "your brand."],
        "introText": (
            "We unite performance marketing, enterprise SEO, creative design, and conversion-engineered web "
            "experiences under one strategic roof."
        ),
        "introHeading": "Data, technology, and creativity in one growth engine.",
        "introBody": (
            "From multi-channel paid acquisition and AI search optimization to high-velocity web design, "
            "every discipline at Roasist works together to compound your revenue and ROAS."
        ),
        "features": [
            {
                "title": "Performance Marketing & Paid Media.",
                "text": (
                    "AI-assisted bidding, Server-Side CAPI tracking, and profit-focused campaign management "
                    "across Google Ads, Meta, TikTok, LinkedIn, Yandex, and Bing."
                ),
                "href": "/en/performance-marketing/",
            },
            {
                "title": "Enterprise SEO & AI Search (AEO).",
                "text": (
                    "Technical SEO, semantic content architecture, and Answer Engine Optimization that secure "
                    "top positions on Google, ChatGPT, Gemini, and Perplexity."
                ),
                "href": "/en/seo/",
            },
            {
                "title": "Conversion Web & Creative Studio.",
                "text": (
                    "Ultra-fast, mobile-first websites and high-converting ad creatives engineered to turn "
                    "every click into measurable pipeline and sales."
                ),
                "href": "/en/web-design/",
            },
        ],
        "metrics": [
            {"value": "+185%", "label": "Year-over-year revenue growth across paid & organic."},
            {"value": "6.4x", "label": "Average Return on Ad Spend (ROAS) across managed accounts."},
            {"value": "-38%", "label": "Reduction in Cost Per Acquisition (CPA) via CRO."},
            {"value": "100%", "label": "Transparent live reporting inside your own accounts."},
        ],
        "processHeading": "Our 360° Digital Growth Methodology.",
        "processSubheading": (
            "From initial audit and unit-economics modeling to multi-channel execution, creative testing, "
            "and live Looker Studio reporting—every step is transparent and accountable."
        ),
        "steps": [
            ("Audit & Diagnostics", "We audit your digital assets, historical ad data, and competitors to establish realistic KPI and revenue targets."),
            ("Growth Strategy", "We architect channel allocation, audience segmentation, and full-funnel conversion milestones tailored to your margins."),
            ("Tracking & Setup", "We deploy GTM, GA4, Enhanced Conversions, and Server-Side CAPI alongside clean campaign structures."),
            ("Creative Production", "Our studio crafts scroll-stopping video hooks, ad visuals, and high-converting landing experiences."),
            ("Continuous Optimization", "Weekly A/B testing, negative keyword hygiene, and bid refinements steadily lower your acquisition costs."),
            ("Transparent Reporting", "Live 24/7 Looker Studio dashboards show exact spend, attribution, CPA, and net ROAS across every channel."),
            ("Conversion Testing", "We continuously test landing page layouts, offers, and CTAs to lift conversion rates across devices."),
            ("Global Scaling", "Once target ROAS and CPA benchmarks are proven, we scale budgets into new segments and international markets."),
        ],
        "faqs": [
            ("What does 360° digital marketing management include?", "It unites strategic planning, Performance Marketing (Google, Meta, TikTok, LinkedIn, Yandex, Bing), Enterprise SEO & AEO, Web Design, Creative Production, and live analytics under a single dedicated team."),
            ("Can we customize the service scope around our current stage?", "Yes. Whether you need a single high-impact channel such as Google Ads or SEO, or a fully integrated 360° growth department, we tailor our engagement to your commercial priorities."),
            ("What is the biggest advantage of consolidating channels with Roasist?", "Eliminating fragmented agency silos. Your paid search insights directly fuel your SEO roadmap, and your creative studio iterates directly on live ad conversion data."),
            ("Who owns our ad accounts, pixels, and analytics data?", "You retain 100% ownership of all Google, Meta, TikTok, LinkedIn, Yandex, Bing, and GA4 accounts at all times. We operate transparently via official partner manager permissions."),
            ("How are performance results reported?", "Through real-time Looker Studio executive dashboards paired with structured strategy reviews covering spend, pipeline quality, CPA, and ROAS."),
            ("How do we start working with Roasist?", "Reach out via our Contact page for a complimentary digital audit. We review your accounts and present a clear, data-backed growth roadmap."),
        ],
    },
    {
        "en_slug": "performance-marketing",
        "src_tr": "hizmetler/performans-pazarlamasi",
        "title": "Performance Marketing Agency | ROAS & Paid Media | Roasist",
        "metaDesc": (
            "Scale your sales and qualified pipeline with data-driven performance marketing across Google Ads, "
            "Instagram & Meta, TikTok, Yandex, Bing, and LinkedIn."
        ),
        "h1": "Performance Marketing",
        "heroLines": ["Data-driven", "<em>high-ROAS</em>", "architecture."],
        "introText": (
            "Turn ad spend into predictable profit with full-funnel performance marketing across Google, Meta, "
            "TikTok, Yandex, Bing, and LinkedIn."
        ),
        "introHeading": "What Is Performance Marketing?",
        "introBody": (
            "Performance marketing aligns every media dollar with measurable commercial outcomes—qualified leads, "
            "e-commerce sales, and net revenue. By combining granular intent segmentation, server-side conversion "
            "tracking, and relentless creative testing, we reduce CPA while scaling profitable volume."
        ),
        "features": [
            {
                "title": "Google Ads (Search, Shopping, PMax, YouTube)",
                "text": "Capture high-intent buyers at the exact moment they search across Google Search, Shopping, Performance Max, YouTube, and Display.",
                "href": "/en/google-ads/",
            },
            {
                "title": "Instagram & Facebook (Meta Ads)",
                "text": "Drive scalable demand and repeat purchases with precision audience modeling, Dynamic Product Ads, Reels creatives, and Meta Conversions API.",
                "href": "/en/instagram-ads/",
            },
            {
                "title": "TikTok Ads",
                "text": "Turn attention into action with native short-form video hooks, Spark Ads, and full-funnel catalog campaigns across TikTok.",
                "href": "/en/tiktok-ads/",
            },
            {
                "title": "Yandex Ads",
                "text": "Expand across CIS and international markets through high-converting Yandex Direct search, product feeds, and Yandex Advertising Network campaigns.",
                "href": "/en/yandex-ads/",
            },
            {
                "title": "Bing Ads",
                "text": "Reach high-purchasing-power desktop and enterprise audiences across Bing, Yahoo, DuckDuckGo, and Microsoft Advertising at lower CPCs.",
                "href": "/en/bing-ads/",
            },
            {
                "title": "LinkedIn Ads",
                "text": "Generate qualified enterprise B2B pipeline by targeting exact company sizes, industries, and C-level decision-makers.",
                "href": "/en/linkedin-ads/",
            },
        ],
        "metrics": [
            {"value": "+185%", "label": "ROAS-Focused — Bid management built around real revenue & margin"},
            {"value": "6.4x", "label": "6+ Channels — Unified Google, Meta, TikTok, Yandex, Bing & LinkedIn"},
            {"value": "-38%", "label": "100% Transparent — Full ownership of your ad accounts & data"},
            {"value": "+210%", "label": "Average conversion and ROAS uplift across scaled campaigns."},
        ],
        "processHeading": "Our Performance Marketing Process",
        "processSubheading": "From account audit and attribution setup to creative testing and international scaling, every step is engineered for measurable ROI.",
        "steps": [
            ("Audit & Diagnostics", "We audit your historical ad accounts, tracking accuracy, unit economics, and competitor landscape to define clear KPIs."),
            ("Channel & Budget Strategy", "We map budget allocation, bidding models, and full-funnel audience architecture around your target CPA and ROAS."),
            ("Tracking & Campaign Setup", "We implement GTM, GA4, Enhanced Conversions, and Server-Side CAPI before launching structured campaigns."),
            ("Continuous Optimization", "Daily search term pruning, bid calibration, placement refinement, and audience exclusions protect every dollar."),
            ("Transparent Reporting", "Visual Looker Studio dashboards give you 24/7 clarity into channel-level spend, conversions, CPA, and ROAS."),
            ("New Growth Opportunities", "We proactively uncover emerging search demand, new geographic markets, and high-margin segments."),
            ("Creative & Landing A/B Tests", "We systematically test ad hooks, visuals, and landing page CTAs to compound conversion rates."),
            ("Profitable Scaling", "Once unit-economic targets are validated, we scale budgets across channels and global markets without diluting ROI."),
        ],
        "faqs": [
            ("How is performance marketing different from traditional advertising?", "Every campaign is optimized toward verifiable business outcomes—sales, qualified leads, or bookings—allowing you to track exact ROAS and ROI down to every dollar spent."),
            ("Which metrics do you prioritize?", "We focus on Return on Ad Spend (ROAS), Cost Per Acquisition (CPA/CPL), Conversion Rate (CR), Customer Lifetime Value (LTV), and qualified pipeline revenue—never vanity clicks."),
            ("Who owns our advertising accounts?", "Your company retains 100% ownership of all Google, Meta, TikTok, Yandex, Bing, and LinkedIn accounts. Roasist manages campaigns transparently via official partner manager access."),
            ("What minimum ad budget do you recommend?", "Optimal starting budgets depend on your industry CPCs, target geographies, and revenue goals. During our initial audit, we analyze real search volumes to recommend an efficient budget."),
            ("How is reporting and transparency handled?", "All ad and analytics accounts stay in your ownership, paired with 24/7 live Looker Studio dashboards tracking spend, conversions, and ROAS."),
            ("How can we get started with Roasist?", "Contact our team via the Contact page for a free account audit and custom performance growth roadmap."),
        ],
    },
    {
        "en_slug": "google-ads",
        "src_tr": "hizmetler/performans-pazarlamasi/google-reklamlari",
        "title": "Google Ads Management Agency | Search, PMax & Shopping | Roasist",
        "metaDesc": "Official Google Partner agency delivering high-ROAS Search, Shopping, Performance Max, and YouTube Ads management.",
        "h1": "Google Ads Management",
        "heroLines": ["High-intent", "<em>Google Ads</em>", "performance."],
        "introText": "Capture buyers at the exact moment of commercial intent across Google Search, Shopping, Performance Max, and YouTube.",
        "introHeading": "Turn Search Intent Into Profitable Revenue.",
        "introBody": "As a certified Google Partner team, we structure granular Search, Shopping, Performance Max, and YouTube campaigns backed by Enhanced Conversions and value-based bidding—maximizing Quality Score while lowering CPC and CPA.",
        "features": [
            {"title": "Search & High-Intent Capture.", "text": "Exact-intent keyword architecture, dynamic ad copy, and strict negative keyword hygiene that convert active searchers into customers.", "href": "/en/contact-us/"},
            {"title": "Shopping & Performance Max.", "text": "Optimized Merchant Center product feeds, margin-tier segmentation, and AI-guided asset groups built to scale e-commerce ROAS.", "href": "/en/contact-us/"},
            {"title": "YouTube & Demand Generation.", "text": "High-impact video sequences and remarketing funnels that build authority and close high-consideration buyers.", "href": "/en/contact-us/"},
        ],
        "metrics": [
            {"value": "+195%", "label": "Increase in qualified conversion volume within 90 days."},
            {"value": "6.8x", "label": "Average ROAS across Google Search & Shopping accounts."},
            {"value": "-34%", "label": "Reduction in wasted spend via negative keyword architecture."},
            {"value": "9/10", "label": "Average Quality Score across core commercial search terms."},
        ],
        "processHeading": "Our Google Ads Management Process.",
        "processSubheading": "Precision account structure, first-party conversion signals, and disciplined bid management.",
        "steps": [
            ("Account & Search Audit", "Deep audit of historical search terms, Quality Scores, Merchant Center feeds, and conversion tag accuracy."),
            ("Keyword & Funnel Blueprint", "Mapping commercial-intent keywords, match types, negative lists, and margin-based tROAS/tCPA targets."),
            ("Enhanced Conversions Setup", "Deploying GTM, GA4, Google Tag, and server-side Enhanced Conversions for rock-solid attribution."),
            ("Ad Copy & Asset Engineering", "Crafting high-CTR Responsive Search Ads, extensions, and Performance Max creative assets."),
            ("Bid & Query Optimization", "Continuous search term pruning, auction insight tracking, and device/geo bid adjustments."),
            ("Live Looker Reporting", "24/7 transparent reporting on impression share, CPC, conversion rate, CPA, and net ROAS."),
            ("Landing Page CRO", "Aligning landing page speed and messaging with search intent to lift Quality Score and conversion rates."),
            ("Multi-Market Scaling", "Expanding winning campaigns across new product lines, languages, and international territories."),
        ],
        "faqs": [
            ("How quickly do Google Ads campaigns generate results?", "Search and Shopping traffic begins immediately upon launch, while smart bidding algorithms typically reach peak efficiency within 2 to 4 weeks of clean conversion data."),
            ("How do you prevent wasted spend on irrelevant clicks?", "Through granular intent grouping, proactive negative keyword lists, placement exclusions, and daily search query audits."),
            ("Do you manage Google Merchant Center for e-commerce?", "Yes. We optimize product titles, GTINs, custom labels by profit margin, and feed health to maximize Shopping and PMax visibility."),
            ("Can you audit our existing Google Ads account first?", "Absolutely. We provide a complimentary diagnostic audit uncovering wasted spend, tracking gaps, and immediate ROAS opportunities."),
            ("Who owns the Google Ads account?", "Your business owns the Google Ads account 100%, connected securely to our Google Partner MCC."),
            ("How do we begin?", "Reach out through our Contact page to schedule your complimentary Google Ads audit."),
        ],
    },
    {
        "en_slug": "instagram-ads",
        "src_tr": "hizmetler/performans-pazarlamasi/instagram-reklamlari",
        "title": "Instagram Ads Agency | Reels, Story & Meta ROAS | Roasist",
        "metaDesc": "Scale e-commerce sales and qualified leads with data-driven Instagram Reels, Story, Feed, and Dynamic Catalog Ads.",
        "h1": "Instagram Ads Management",
        "heroLines": ["Scroll-stopping", "<em>Instagram</em>", "sales growth."],
        "introText": "Combine thumb-stopping Reels and Story creatives with Meta Conversions API precision to turn attention into revenue.",
        "introHeading": "Creative Velocity Meets Meta Algorithm Mastery.",
        "introBody": "Winning on Instagram requires both native creative storytelling and clean first-party data signals. We pair scroll-stopping Reels, Story, and Carousel assets with Meta CAPI and Advantage+ Shopping structures to scale profitable acquisitions.",
        "features": [
            {"title": "Reels & Story Performance Creatives.", "text": "Native vertical video hooks and visual storytelling engineered specifically to maximize thumb-stop ratio and CTR.", "href": "/en/contact-us/"},
            {"title": "Dynamic Product & Catalog Ads.", "text": "Automated catalog retargeting and Advantage+ Shopping funnels that recover abandoned carts and boost AOV.", "href": "/en/contact-us/"},
            {"title": "Conversions API (CAPI) & Lookalikes.", "text": "Server-side event matching and high-LTV customer seed audiences that feed Meta's delivery engine with accurate signals.", "href": "/en/contact-us/"},
        ],
        "metrics": [
            {"value": "+215%", "label": "Growth in attributed Instagram e-commerce and lead volume."},
            {"value": "5.9x", "label": "Average ROAS across Reels, Story & Dynamic Catalog funnels."},
            {"value": "-36%", "label": "Lower Cost Per Acquisition via systematic creative testing."},
            {"value": "+48%", "label": "Higher event match quality with Meta Conversions API."},
        ],
        "processHeading": "Our Instagram Ads Process.",
        "processSubheading": "Full-funnel social acquisition powered by creative testing and server-side attribution.",
        "steps": [
            ("Pixel, CAPI & Audience Audit", "Reviewing Meta Pixel health, Event Match Quality, catalog feeds, and historical creative performance."),
            ("Full-Funnel Architecture", "Structuring prospecting, social proof engagement, and dynamic retargeting layers around your CPA/ROAS goals."),
            ("CAPI & Catalog Configuration", "Implementing Server-Side Conversions API and clean product sets inside your Meta Business Manager."),
            ("Hook & Creative Production", "Designing high-converting Reels, Story, and Carousel variations tailored to each buyer persona."),
            ("Creative Sprint Testing", "Testing hooks, headlines, and offers weekly to combat ad fatigue and surface breakout winners."),
            ("Real-Time Attribution Reporting", "Tracking ROAS, CPA, frequency, and hook-retention metrics in live Looker Studio dashboards."),
            ("Landing & Checkout Optimization", "Streamlining mobile landing pages to maximize conversion rates from Instagram mobile traffic."),
            ("Horizontal & Vertical Scaling", "Scaling winning creative concepts across broader audiences and international markets."),
        ],
        "faqs": [
            ("Why is creative testing so important on Instagram?", "In modern Meta campaigns, creative is the primary targeting lever. Fresh hooks and formats allow the algorithm to unlock new high-converting buyer pockets."),
            ("Do you set up Meta Conversions API (CAPI)?", "Yes. We configure server-side CAPI via GTM so iOS privacy restrictions and browser blockers don't blind your campaign optimization."),
            ("Does Instagram work for service & B2B brands as well as e-commerce?", "Yes. Healthcare, real estate, education, and B2B brands achieve strong lead volume using instant forms with qualification questions and WhatsApp/landing funnels."),
            ("Are Instagram and Facebook managed together?", "Both run through Meta Ads Manager, allowing us to allocate budget dynamically to whichever placement delivers the strongest ROAS."),
            ("Who owns our Meta Business Manager?", "Your Business Manager, Pixel, and Ad Account remain 100% under your company's ownership."),
            ("How do we start?", "Request a free Meta Ads audit via our Contact page."),
        ],
    },
    {
        "en_slug": "facebook-ads",
        "src_tr": "hizmetler/performans-pazarlamasi/facebook-reklamlari",
        "title": "Facebook & Meta Ads Agency | CAPI & Full-Funnel ROAS | Roasist",
        "metaDesc": "Data-driven Facebook and Meta Ads management combining Conversions API, Advantage+ Shopping, and high-converting creatives.",
        "h1": "Facebook & Meta Ads",
        "heroLines": ["Smart data,", "<em>Meta Ads</em>", "conversions."],
        "introText": "Scale domestic and international customer acquisition with Meta Conversions API, Advantage+ campaigns, and precision retargeting.",
        "introHeading": "Predictable Customer Acquisition Across the Meta Ecosystem.",
        "introBody": "We engineer full-funnel Meta advertising architectures that unite first-party CRM data, high-match-quality CAPI events, and persuasive creative variations to drive profitable e-commerce sales and qualified leads worldwide.",
        "features": [
            {"title": "Advantage+ & Full-Funnel Scaling.", "text": "Balanced prospecting and remarketing structures engineered to maintain stable ROAS as daily spend scales.", "href": "/en/contact-us/"},
            {"title": "CRM & Offline Conversion Sync.", "text": "Feeding qualified CRM deal stages back into Meta so lead-generation campaigns optimize for real buyers, not spam forms.", "href": "/en/contact-us/"},
            {"title": "Dynamic Catalog & Cross-Sell.", "text": "Automated product catalog campaigns that turn one-time shoppers into high-LTV repeat customers.", "href": "/en/contact-us/"},
        ],
        "metrics": [
            {"value": "6.2x", "label": "Average ROAS across e-commerce & global lead campaigns."},
            {"value": "-41%", "label": "Reduction in cost per qualified lead via CRM signal sync."},
            {"value": "+175%", "label": "Increase in scalable monthly conversion volume."},
            {"value": "9.1/10", "label": "Target Meta CAPI Event Match Quality score."},
        ],
        "processHeading": "Our Facebook & Meta Ads Process.",
        "processSubheading": "Data integrity, creative iteration, and disciplined budget scaling.",
        "steps": [
            ("Account & Attribution Audit", "Auditing Pixel/CAPI deduplication, attribution windows, audience overlap, and creative fatigue."),
            ("Funnel & Offer Strategy", "Designing cold acquisition, mid-funnel proof, and bottom-funnel conversion offers."),
            ("Server-Side CAPI Deployment", "Ensuring purchase values and qualified lead events pass cleanly with zero signal loss."),
            ("Multi-Format Creative Build", "Producing static, carousel, and video assets aligned with each stage of buyer awareness."),
            ("Algorithmic Bid & Budget Tuning", "Optimizing cost caps, value bidding, and placement performance daily."),
            ("Live Executive Dashboards", "Transparent 24/7 reporting on ROAS, MER, CPA, and cohort performance."),
            ("A/B Creative & Offer Sprints", "Continuous testing of hooks, social proof angles, and landing pages."),
            ("International Market Expansion", "Scaling proven Meta funnels into Europe, UK, North America, and MENA."),
        ],
        "faqs": [
            ("How do you improve lead quality in Meta Lead Ads?", "By pairing conditional qualification questions and SMS/WhatsApp verification with offline CRM conversion imports so Meta optimizes for closed deals."),
            ("What is the role of Server-Side CAPI?", "It restores lost browser conversion signals, lowering CPA and stabilizing campaign performance across iOS and privacy-restricted browsers."),
            ("Can you scale international e-commerce stores?", "Yes. Multi-country catalog localization, currency feeds, and international Advantage+ scaling are core specialties at Roasist."),
            ("How often do you refresh ad creatives?", "We monitor frequency and thumb-stop ratios continuously, introducing fresh creative iterations in structured bi-weekly sprints."),
            ("Do we keep full account ownership?", "Yes—100% of ad accounts, pixels, catalogs, and data stay in your Business Manager."),
            ("How do we launch?", "Contact us for a complimentary Meta account diagnostic and growth plan."),
        ],
    },
    {
        "en_slug": "tiktok-ads",
        "src_tr": "hizmetler/performans-pazarlamasi/tiktok-reklamlari",
        "title": "TikTok Ads Agency | Spark Ads, Video Commerce & Growth | Roasist",
        "metaDesc": "Official TikTok Partner agency scaling brands with native In-Feed creatives, Spark Ads, and full-funnel conversion tracking.",
        "h1": "TikTok Ads Management",
        "heroLines": ["Viral momentum,", "<em>TikTok Ads</em>", "conversions."],
        "introText": "Capture fast-growing audiences with native short-form video strategy, Spark Ads, and TikTok Events API performance tracking.",
        "introHeading": "Native Short-Form Video Engineered for Commercial ROI.",
        "introBody": "As a TikTok Partner team, we build native, creator-style advertising campaigns that don't feel like intrusive ads—capturing attention in the first 2 seconds and driving measurable e-commerce purchases, app installs, and lead volume.",
        "features": [
            {"title": "In-Feed & Spark Ads Strategy.", "text": "Amplify high-performing organic and creator posts into scalable conversion engines with native social proof.", "href": "/en/contact-us/"},
            {"title": "Video Shopping & Catalog Ads.", "text": "Seamless product cards and dynamic catalog retargeting that shorten the path from discovery to checkout.", "href": "/en/contact-us/"},
            {"title": "TikTok Events API & Attribution.", "text": "Server-side event tracking ensuring accurate purchase and lead optimization across mobile devices.", "href": "/en/contact-us/"},
        ],
        "metrics": [
            {"value": "+240%", "label": "New-to-brand customer reach and acquisition growth."},
            {"value": "-32%", "label": "Lower CPM & CPC compared to saturated social channels."},
            {"value": "5.1x", "label": "Average ROAS on native Spark & Video Shopping campaigns."},
            {"value": "38%+", "label": "2-second hook retention benchmark across winning creatives."},
        ],
        "processHeading": "Our TikTok Ads Growth Process.",
        "processSubheading": "Hook engineering, native creative velocity, and Events API optimization.",
        "steps": [
            ("Category & Creative Audit", "Analyzing competitor TikTok hooks, sound trends, and audience buying triggers in your vertical."),
            ("Funnel & Bidding Roadmap", "Mapping awareness, consideration, and conversion campaigns with clear CPA/ROAS targets."),
            ("Pixel & Events API Setup", "Deploying TikTok Pixel + server-side Events API for full-funnel mobile attribution."),
            ("Hook-First Script & Edit Direction", "Structuring 3-part video scripts (Hook -> Value/Proof -> Clear CTA) built for TikTok native pacing."),
            ("Rapid Creative Testing", "Testing multiple opening hooks per concept to identify low-CPA, scalable winners."),
            ("Transparent Performance Reporting", "Live dashboards tracking hook rate, hold rate, CTR, CPA, and ROAS."),
            ("Mobile Landing CRO", "Optimizing fast-loading mobile landing experiences for instant thumb-friendly conversion."),
            ("Cross-Market Scaling", "Scaling winning video frameworks across regions and demographics."),
        ],
        "faqs": [
            ("Is TikTok only for Gen Z audiences?", "No. Today over 65% of TikTok's active purchasing power comes from 25–54+ demographics across e-commerce, health, real estate, beauty, and apps."),
            ("What makes a TikTok ad convert?", "Authentic, native pacing in the first 2 seconds, clear visual product demonstration, social proof, and a frictionless mobile offer."),
            ("What are Spark Ads?", "Spark Ads allow us to run paid conversion campaigns directly from organic brand or creator posts, preserving likes, comments, and trust."),
            ("Do we need a huge video studio to start?", "Not at all. Native UGC-style and agile motion edits consistently outperform overly polished TV-style commercials on TikTok."),
            ("Who owns our TikTok Ads Manager?", "Your company owns the TikTok Business Center and Ad Account 100%."),
            ("How do we get started?", "Reach out on our Contact page for a tailored TikTok growth strategy."),
        ],
    },
    {
        "en_slug": "linkedin-ads",
        "src_tr": "hizmetler/performans-pazarlamasi/linkedin-reklamlari",
        "title": "LinkedIn Ads Agency | Enterprise B2B Lead Generation | Roasist",
        "metaDesc": "Generate high-value B2B pipeline and enterprise SQLs with precision LinkedIn Ads targeting C-suite and key decision-makers.",
        "h1": "LinkedIn B2B Ads",
        "heroLines": ["Precision B2B", "<em>LinkedIn</em>", "pipeline."],
        "introText": "Reach exact C-suite executives, procurement leaders, and target enterprise accounts with Account-Based Marketing on LinkedIn.",
        "introHeading": "High-Value B2B Pipeline Without Wasted Impressions.",
        "introBody": "When a single enterprise contract is worth tens or hundreds of thousands of dollars, broad targeting fails. We use LinkedIn's unmatched professional graph—industry, company headcount, seniority, job title, and ABM company lists—to put your value proposition directly in front of real decision-makers.",
        "features": [
            {"title": "ABM & Executive Job-Title Targeting.", "text": "Upload target enterprise company lists or filter by exact C-level, VP, and Director roles with zero consumer waste.", "href": "/en/contact-us/"},
            {"title": "Thought Leadership & Document Ads.", "text": "Build executive trust directly in the feed with high-engagement carousel documents, case studies, and video insights.", "href": "/en/contact-us/"},
            {"title": "Lead Gen Forms & CRM Sync.", "text": "Pre-filled LinkedIn Lead Gen Forms synced instantly to your CRM for rapid sales follow-up and SQL tracking.", "href": "/en/contact-us/"},
        ],
        "metrics": [
            {"value": "+165%", "label": "Growth in Sales-Qualified B2B Pipeline (SQLs)."},
            {"value": "3.4x", "label": "Higher lead-to-opportunity conversion vs generic channels."},
            {"value": "-29%", "label": "Reduction in Cost Per Qualified Executive Lead."},
            {"value": "100%", "label": "Verified professional & company-level attribution."},
        ],
        "processHeading": "Our LinkedIn B2B Ads Process.",
        "processSubheading": "Account-Based Marketing, executive messaging, and closed-loop CRM optimization.",
        "steps": [
            ("ICP & ABM List Architecture", "Defining exact Ideal Customer Profile industries, company sizes, geographies, and buying-committee roles."),
            ("Full-Funnel B2B Offer Design", "Pairing executive thought leadership at the top of funnel with high-intent demos and audits at the bottom."),
            ("Insight Tag & CRM Integration", "Deploying LinkedIn Insight Tag, Conversions API, and instant CRM webhook routing."),
            ("Executive Ad Copy & Creative", "Crafting concise, authority-driven ad creatives, Document Ads, and Conversation Ads."),
            ("Bid & Demographic Tuning", "Manual CPC floor control and company-demographics auditing to ensure budget hits tier-1 accounts."),
            ("Company-Level Reporting", "See exactly which companies and job titles are viewing, clicking, and converting on your campaigns."),
            ("Lead-to-SQL Optimization", "Optimizing campaigns based on downstream CRM deal progression rather than raw form fills."),
            ("International B2B Expansion", "Scaling B2B demand generation across Europe, UK, US, and MENA enterprise markets."),
        ],
        "faqs": [
            ("Aren't LinkedIn CPCs higher than other platforms?", "While raw CPC is higher, LinkedIn eliminates non-decision-maker waste—resulting in significantly higher deal sizes and stronger pipeline ROI for B2B companies."),
            ("Can we target a specific list of 500 dream enterprise companies?", "Yes. Using Matched Audiences (ABM), we upload your exact target account list and serve ads exclusively to decision-makers inside those companies."),
            ("Which industries benefit most from LinkedIn Ads?", "B2B SaaS, manufacturing & export, enterprise consulting, financial services, logistics, commercial real estate, and corporate education."),
            ("Do LinkedIn Lead Gen Forms integrate with our CRM?", "Yes. Leads flow automatically into HubSpot, Salesforce, Pipedrive, Zoho, or custom CRMs in real time."),
            ("Who owns the LinkedIn Campaign Manager?", "Your company retains 100% ownership of the Campaign Manager account and all audience data."),
            ("How do we start?", "Contact our B2B growth team via the Contact page for a custom ICP & LinkedIn reach analysis."),
        ],
    },
    {
        "en_slug": "yandex-ads",
        "src_tr": "hizmetler/performans-pazarlamasi/yandex-reklamlari",
        "title": "Yandex Ads Agency | Yandex Direct & CIS Market Growth | Roasist",
        "metaDesc": "Reach high-value buyers across Russia, CIS, and international Russian-speaking markets with expert Yandex Direct & YAN management.",
        "h1": "Yandex Ads Management",
        "heroLines": ["Global reach,", "<em>Yandex Ads</em>", "dominance."],
        "introText": "Scale international patient acquisition, real estate investment, hospitality bookings, and export sales across Russia & CIS via Yandex Direct.",
        "introHeading": "Direct Access to 100M+ High-Intent CIS & Global Buyers.",
        "introBody": "For medical tourism, luxury real estate, hospitality, and export brands, Yandex is the #1 search and media ecosystem across Russia and CIS countries. Our specialists manage native Russian/English Yandex Direct Search, Product Campaigns, and Yandex Advertising Network (YAN) funnels tied to Yandex Metrica conversion goals.",
        "features": [
            {"title": "Yandex Direct Search Campaigns.", "text": "Capture active Russian- and CIS-based buyers searching with high commercial intent for clinics, property, hotels, and B2B suppliers.", "href": "/en/contact-us/"},
            {"title": "Yandex Advertising Network (YAN).", "text": "Visual banner, video, and smart-feed retargeting across thousands of premium CIS portals and mobile apps.", "href": "/en/contact-us/"},
            {"title": "Yandex Metrica & Offline Goals.", "text": "Full session replay (Webvisor), call/WhatsApp tracking, and offline CRM conversion feedback to train autotargeting.", "href": "/en/contact-us/"},
        ],
        "metrics": [
            {"value": "+220%", "label": "Growth in qualified CIS & international inquiries."},
            {"value": "5.7x", "label": "Average ROAS across medical tourism, real estate & export."},
            {"value": "-35%", "label": "Lower Cost Per Qualified Lead via Metrica goal optimization."},
            {"value": "100%", "label": "Native Russian & English ad copy localization."},
        ],
        "processHeading": "Our Yandex Ads Management Process.",
        "processSubheading": "Wordstat demand intelligence, native localization, and Yandex Metrica conversion optimization.",
        "steps": [
            ("Yandex Wordstat Demand Audit", "Analyzing real regional search volumes across Moscow, St. Petersburg, Kazakhstan, Uzbekistan, Belarus, and global expat hubs."),
            ("Regional & Funnel Strategy", "Separating high-intent Search from YAN retargeting with geo-specific bid multipliers."),
            ("Yandex Metrica & Goal Setup", "Configuring Webvisor, WhatsApp/Telegram click tracking, form goals, and CRM offline conversions."),
            ("Native Russian/EN Copywriting", "Writing culturally fluent headlines, sitelinks, callouts, and visual YAN banners that pass strict moderation."),
            ("Placement & Query Cleaning", "Continuous negative keyword filtering and YAN placement blacklisting to block low-quality mobile app clicks."),
            ("Transparent Reporting", "Clear performance dashboards showing exact spend, CPL, lead quality, and revenue by region."),
            ("Landing Page Localization CRO", "Optimizing Russian/English landing pages and instant messaging flows (WhatsApp/Telegram) for maximum conversion."),
            ("Multi-Region CIS Scaling", "Expanding profitable campaigns across high-growth CIS territories and seasonal peaks."),
        ],
        "faqs": [
            ("Which industries see the highest ROI on Yandex Ads?", "Medical tourism (dental, hair transplant, plastic surgery, hospitals), luxury real estate, hotels & resorts, B2B manufacturing exports, and e-commerce."),
            ("Do you write ads in native Russian?", "Yes. Campaign keywords, ad extensions, and visual creatives are localized natively to match real Russian and CIS search behavior."),
            ("How do you block bot or low-quality network traffic on YAN?", "We maintain strict YAN placement exclusion lists, anti-fraud Metrica engagement filters, and pay-for-conversion bidding models."),
            ("Can WhatsApp and Telegram leads be tracked accurately?", "Yes. Every WhatsApp, Telegram, and form interaction is tracked in Yandex Metrica and linked to CRM lead quality."),
            ("Who owns the Yandex Direct & Metrica accounts?", "Your company retains full ownership and access at all times."),
            ("How do we start?", "Contact us for a free Yandex Wordstat search demand report for your sector."),
        ],
    },
    {
        "en_slug": "bing-ads",
        "src_tr": "hizmetler/performans-pazarlamasi/bing-reklamlari",
        "title": "Bing Ads (Microsoft Advertising) Agency | Global PPC | Roasist",
        "metaDesc": "Reach affluent desktop and enterprise decision-makers across US, UK, and Europe at lower CPCs with Microsoft Advertising (Bing Ads).",
        "h1": "Bing Ads (Microsoft Advertising)",
        "heroLines": ["Global search,", "<em>Bing Ads</em>", "efficiency."],
        "introText": "Unlock affluent desktop, corporate, and Copilot AI search audiences across the US, UK, and Europe with lower CPCs and higher ROAS.",
        "introHeading": "Lower Competition, Higher Purchasing Power Across Microsoft's Ecosystem.",
        "introBody": "Microsoft Advertising powers search across Windows, Edge, Bing, Yahoo, DuckDuckGo, and Microsoft Copilot—reaching millions of corporate laptops and high-income households where Google competition is fiercest. We turn Bing Ads into a high-margin incremental revenue channel.",
        "features": [
            {"title": "Bing, Edge & Copilot Search.", "text": "Capture high-converting desktop and AI-assisted search queries across North America, the UK, DACH, and global markets.", "href": "/en/contact-us/"},
            {"title": "LinkedIn Profile Targeting in Search.", "text": "Uniquely layer LinkedIn company, industry, and job-function bid modifiers directly onto search campaigns.", "href": "/en/contact-us/"},
            {"title": "Microsoft Shopping & Audience Ads.", "text": "Sync Merchant Center catalogs and retarget buyers across MSN, Outlook, and Microsoft's premium publisher network.", "href": "/en/contact-us/"},
        ],
        "metrics": [
            {"value": "-33%", "label": "Average lower CPC compared to equivalent US/EU Google auctions."},
            {"value": "6.6x", "label": "Average ROAS on desktop & B2B search campaigns."},
            {"value": "+28%", "label": "Incremental high-AOV conversions added to paid search mix."},
            {"value": "100%", "label": "UET & GA4 server-verified conversion attribution."},
        ],
        "processHeading": "Our Microsoft Advertising Process.",
        "processSubheading": "Custom calibration beyond simple Google imports—built for Microsoft's unique auction dynamics.",
        "steps": [
            ("Market & Desktop Share Audit", "Evaluating Bing/Microsoft search share across your target countries (US, UK, Germany, Canada, Australia, Global)."),
            ("Campaign & LinkedIn Layering", "Structuring search & shopping campaigns enhanced with LinkedIn industry and job-function targeting."),
            ("UET Tag & Enhanced Tracking", "Deploying Microsoft UET tags via GTM with dynamic revenue and offline conversion tracking."),
            ("Tailored Bid & Match Calibration", "Adjusting match types, partner network exclusions, and CPC bids specifically for Bing's auction behavior."),
            ("Syndicated Partner Hygiene", "Filtering search partner placements so budget stays exclusively on high-converting properties."),
            ("Unified Cross-Search Reporting", "Compare Google, Bing, and Yandex CPC, CPA, and ROAS side by side in Looker Studio."),
            ("Desktop Landing Page CRO", "Optimizing high-information desktop layouts for corporate and affluent buyers."),
            ("International Tier-1 Scaling", "Expanding winning campaigns across English, German, French, and global search markets."),
        ],
        "faqs": [
            ("Why add Bing Ads if we already run Google Ads?", "Millions of corporate Windows workstations default to Edge and Bing—giving you incremental buyers with 25%–40% lower CPCs and higher average order values."),
            ("Can you really target LinkedIn profiles inside Bing Search?", "Yes. Microsoft owns LinkedIn, making Bing Ads the only search engine where you can bid higher for specific industries, companies, and job functions."),
            ("Which geographies perform strongest on Microsoft Advertising?", "The United States, United Kingdom, Germany, Canada, Australia, Nordics, and global B2B English-speaking markets."),
            ("Do you just auto-import Google Ads and leave it?", "Never. Blind auto-imports waste budget on broad match and syndicated partners. We custom-calibrate bids, negatives, and network settings."),
            ("Who owns our Microsoft Advertising account?", "Your company owns the account 100%."),
            ("How do we start?", "Request a complimentary US/EU Microsoft Advertising opportunity audit via our Contact page."),
        ],
    },
    {
        "en_slug": "seo",
        "src_tr": "hizmetler/seo",
        "title": "Enterprise SEO & AI Search (AEO) Agency | Roasist",
        "metaDesc": "Compound your organic traffic and revenue with technical SEO, semantic content strategy, digital authority, and AI Search (AEO/GEO) optimization.",
        "h1": "Enterprise SEO & AI Search (AEO)",
        "heroLines": ["Organic", "<em>search</em>", "leadership."],
        "introText": "Dominate Google rankings and AI answer engines (ChatGPT, Gemini, Perplexity) with technical precision and commercial-intent content.",
        "introHeading": "What Is Modern SEO & How Do We Execute It?",
        "introBody": "Search visibility is no longer about stuffing keywords—it is about technical speed, semantic authority, and capturing buyers with real commercial intent across both Google SERPs and AI answer engines (AEO & GEO). We build compounding organic revenue assets.",
        "features": [
            {"title": "Technical SEO & Core Web Vitals", "text": "Crawl budget optimization, site speed, mobile UX, indexing hygiene, canonical architecture, and rich Schema.org JSON-LD markup.", "href": "/en/contact-us/"},
            {"title": "Search Intent & AEO Content Architecture", "text": "Topic clusters and authoritative commercial pages engineered around verified search demand—winning both Google #1 spots and AI citations.", "href": "/en/contact-us/"},
            {"title": "Digital PR & Domain Authority", "text": "White-hat editorial authority building, brand mentions, and internal link equity sculpting compliant with Google quality guidelines.", "href": "/en/contact-us/"},
        ],
        "metrics": [
            {"value": "+210%", "label": "Growth in non-branded commercial organic traffic."},
            {"value": "Top 3", "label": "Rankings across high-intent revenue keywords."},
            {"value": "-42%", "label": "Lower blended CAC as organic pipeline compounds."},
            {"value": "95+", "label": "Target Core Web Vitals & technical health score."},
        ],
        "processHeading": "Our Enterprise SEO & AEO Process.",
        "processSubheading": "Technical excellence, verified search-volume intelligence, and authority building.",
        "steps": [
            ("Deep Technical & Crawl Audit", "Full crawl diagnostics covering indexation, Core Web Vitals, rendering, schema markup, and internal linking."),
            ("Verified Keyword & Intent Mapping", "Mapping real Google API search volumes and buyer intent across informational, commercial, and transactional stages."),
            ("Site Architecture & On-Page", "Optimizing URL hierarchy, H1–H3 structure, metadata, semantic entities, and internal link flow."),
            ("AEO & Authority Content Creation", "Producing expert, structured content formatted to win Featured Snippets, AI Overviews, and LLM citations."),
            ("Technical Sprint Implementation", "Working directly with your codebase or CMS to ship speed, schema, and UX fixes cleanly."),
            ("White-Hat Authority Building", "Securing relevant industry placements and brand citations that strengthen E-E-A-T."),
            ("GSC & GA4 Revenue Attribution", "Tracking exact rankings, impressions, AI referrals, and organic conversions in Looker Studio."),
            ("Continuous Content Expansion", "Scaling new commercial hubs and international hreflang clusters quarter after quarter."),
        ],
        "faqs": [
            ("How long does SEO take to deliver measurable results?", "Technical fixes improve crawling within weeks, while competitive commercial rankings and compounding organic revenue typically accelerate across months 3 to 6."),
            ("What is AEO / GEO (AI Search Optimization)?", "Answer Engine Optimization structures your entities, schema, and authoritative answers so ChatGPT, Google AI Overviews, and Perplexity cite your brand directly."),
            ("Should we run SEO and Google Ads together?", "Yes. Paid search query conversion data sharpens your SEO priorities, while stronger SEO landing pages boost Google Ads Quality Scores and lower CPCs."),
            ("Do you ever use risky automated backlinks?", "Never. Every technical and off-page initiative adheres strictly to Google's official Search Essentials and E-E-A-T standards."),
            ("How do you report SEO progress?", "Via live Looker Studio dashboards integrating Google Search Console and GA4—tracking impressions, clicks, rankings, and organic conversions."),
            ("How can we begin?", "Contact us for a complimentary technical SEO & AI visibility audit."),
        ],
    },
    {
        "en_slug": "graphic-design",
        "src_tr": "hizmetler/grafik-tasarim",
        "title": "Creative & Graphic Design Studio | Brand Identity & Ad Creatives | Roasist",
        "metaDesc": "Elevate your brand authority and ad conversion rates with strategic brand identity, performance ad creatives, and social visual systems.",
        "h1": "Graphic & Creative Design",
        "heroLines": ["Distinctive", "<em>creative</em>", "visual craft."],
        "introText": "Visual identity systems, scroll-stopping performance ad creatives, and brand communications built to command attention and convert.",
        "introHeading": "Design That Captures Attention and Drives Action.",
        "introBody": "Great design at a performance agency does two jobs at once: it elevates your brand's perceived value in milliseconds and guides the viewer's eye straight to action. Our creative studio unites brand aesthetics with live conversion data.",
        "features": [
            {"title": "Performance Ad & Motion Creatives.", "text": "High-CTR static, carousel, and motion assets engineered specifically for Meta, TikTok, YouTube, LinkedIn, and Display.", "href": "/en/contact-us/"},
            {"title": "Brand Identity & Visual Systems.", "text": "Logos, typography, color systems, and comprehensive brand guidelines that make your company unmistakable.", "href": "/en/contact-us/"},
            {"title": "Social Media & Corporate Collateral.", "text": "Cohesive social templates, investor pitch decks, digital catalogs, and launch assets with razor-sharp craft.", "href": "/en/contact-us/"},
        ],
        "metrics": [
            {"value": "+68%", "label": "Average CTR uplift with performance-engineered creatives."},
            {"value": "-31%", "label": "Reduction in CPA through structured visual A/B testing."},
            {"value": "100%", "label": "Bespoke vector & motion craft—zero generic templates."},
            {"value": "48h", "label": "Agile creative turnaround for active growth campaigns."},
        ],
        "processHeading": "Our Creative & Graphic Design Process.",
        "processSubheading": "Strategic discovery, bold art direction, and conversion-informed iteration.",
        "steps": [
            ("Brand & Audience Immersion", "Understanding your positioning, competitive landscape, buyer psychology, and channel requirements."),
            ("Creative Concept & Moodboards", "Exploring distinct visual territories, typography, and art direction rules before production."),
            ("Visual Identity & Asset System", "Crafting scalable design systems across digital, social, and advertising touchpoints."),
            ("Ad Hook & Layout Engineering", "Designing multiple visual hierarchies and value-proposition angles for paid media testing."),
            ("Motion & Multi-Ratio Adaptation", "Delivering crisp 9:16, 4:5, 1:1, and 16:9 adaptations for every platform."),
            ("Collaborative Feedback Rounds", "Transparent, structured review cycles ensuring every detail aligns with your brand vision."),
            ("Performance Data Feedback Loop", "Analyzing CTR and conversion metrics from live ads to evolve the next creative sprint."),
            ("Brand Book & Source Delivery", "Handing over organized Figma systems, guidelines, and production-ready vector/source files."),
        ],
        "faqs": [
            ("Do you design performance ad creatives for ongoing campaigns?", "Yes. Our studio works hand-in-hand with our media buyers to produce weekly and monthly batches of high-converting static and motion creatives."),
            ("Can you build a brand identity from scratch?", "Absolutely. From naming direction and logo mark creation to full typography, color palette, and brand guidelines."),
            ("How are revisions handled?", "Every project includes clear, collaborative review stages where your feedback shapes refinements smoothly and rapidly."),
            ("Do we receive editable source files?", "Yes. Upon completion, organized vector, print, and digital source assets belong to your brand."),
            ("Can graphic design be bundled with 360° marketing?", "Yes—integrating creative production directly into your performance and social retainers delivers the fastest velocity."),
            ("How do we start?", "Share your project goals on our Contact page to schedule a creative briefing call."),
        ],
    },
    {
        "en_slug": "web-design",
        "src_tr": "hizmetler/web-tasarim",
        "title": "Web Design & Development Agency | UI/UX, Speed & CRO | Roasist",
        "metaDesc": "Ultra-fast, mobile-first, SEO-ready corporate and e-commerce websites engineered for brand authority and high conversion rates.",
        "h1": "Web Design & Development",
        "heroLines": ["Next-gen", "<em>conversion</em>", "web design."],
        "introText": "Bespoke UI/UX design, blazing-fast engineering, and conversion rate optimization (CRO) that turn visitors into customers.",
        "introHeading": "Websites Built to Impress Humans and Convert Traffic.",
        "introBody": "A slow or confusing website silently burns half your ad budget. We design and engineer distinctive, mobile-first websites with sub-second responsiveness, clean technical SEO foundations, and persuasive UX flows built to maximize ROI from day one.",
        "features": [
            {"title": "Bespoke UI/UX & Interactive Design.", "text": "Tailor-made interfaces, clear typographic hierarchy, and refined micro-interactions crafted around your buyer journey.", "href": "/en/contact-us/"},
            {"title": "High-Speed, SEO-Native Engineering.", "text": "Clean modern code, 95+ Core Web Vitals performance, structured Schema markup, and rock-solid security.", "href": "/en/contact-us/"},
            {"title": "Conversion Rate Optimization (CRO).", "text": "Frictionless forms, persuasive social proof placement, and analytics-backed UX layouts that multiply lead and sales conversion.", "href": "/en/contact-us/"},
        ],
        "metrics": [
            {"value": "+142%", "label": "Average lift in website conversion rate post-relaunch."},
            {"value": "<1.2s", "label": "Target Largest Contentful Paint (LCP) load speed."},
            {"value": "95+", "label": "Mobile & Desktop PageSpeed / Core Web Vitals benchmark."},
            {"value": "+110%", "label": "Growth in organic search impressions within 60 days."},
        ],
        "processHeading": "Our Web Design & Development Process.",
        "processSubheading": "Strategy, UX architecture, bespoke UI, clean engineering, and SEO-ready launch.",
        "steps": [
            ("Discovery & UX Audit", "Analyzing user behavior, heatmaps, competitor sites, and conversion bottlenecks."),
            ("Information Architecture & Wireframes", "Structuring sitemap hierarchy, messaging flow, and conversion touchpoints before visual styling."),
            ("Bespoke UI & Art Direction", "Designing responsive desktop and mobile screens with distinctive brand character."),
            ("Clean Front-End & CMS Build", "Engineering fast, modular, easy-to-manage pages without bloated plugins."),
            ("Technical SEO & Schema Setup", "Baking canonicals, metadata, hreflang, sitemaps, and JSON-LD directly into the build."),
            ("GTM, GA4 & CRM Integration", "Wiring every form, phone click, WhatsApp trigger, and checkout event into your analytics stack."),
            ("Cross-Device QA & Speed Tuning", "Rigorous testing across iOS, Android, Safari, Chrome, and Core Web Vitals."),
            ("Zero-Downtime Launch & Support", "Careful deployment, 301 redirect protection, team training, and ongoing CRO evolution."),
        ],
        "faqs": [
            ("Are your websites custom-designed or template-based?", "Every Roasist web project is custom-architected around your brand identity, audience journey, and conversion goals."),
            ("Will our new website be SEO and mobile friendly from day one?", "Yes. Mobile-first responsiveness, Core Web Vitals speed, and clean technical SEO architecture are built in from the first line of code."),
            ("How long does a corporate or e-commerce web project take?", "Depending on scope, integrations, and multilingual requirements, most projects launch smoothly within 4 to 8 weeks."),
            ("Can our internal team update content easily after launch?", "Yes. We provide a clean, modular content management workflow along with walkthrough training for your team."),
            ("Do you protect our existing SEO rankings during a redesign?", "Yes. Full URL mapping and 301 redirect verification ensure your existing search equity is preserved and strengthened."),
            ("How do we request a web proposal?", "Tell us about your project on our Contact page for a tailored scope and timeline."),
        ],
    },
    {
        "en_slug": "360-digital-marketing-management",
        "src_tr": "hizmetler/360-derece-dijital-pazarlama-yonetimi",
        "title": "360° Digital Marketing Management | Outsourced Growth Team | Roasist",
        "metaDesc": "Unite performance marketing, enterprise SEO, web & creative design, and analytics under one accountable 360° growth partnership.",
        "h1": "360° Digital Marketing Management",
        "heroLines": ["Unified across", "<em>360° channels,</em>", "one growth team."],
        "introText": "Your dedicated external growth department—orchestrating paid media, SEO & AEO, creative studio, CRO, and analytics in complete harmony.",
        "introHeading": "End Channel Silos. Multiply Cross-Channel ROI.",
        "introBody": "When one vendor runs ads, another writes SEO content, and a third edits your website, insights get lost and budget leaks. Our 360° Digital Marketing Management model aligns every digital touchpoint around one shared north star: profitable, measurable business growth.",
        "features": [
            {"title": "Omnichannel Paid Acquisition.", "text": "Coordinated Google, Meta, TikTok, LinkedIn, Yandex, and Bing campaigns sharing unified audience and attribution signals.", "href": "/en/performance-marketing/"},
            {"title": "Compounding Organic & AI Search.", "text": "Technical SEO, content clusters, and AEO optimization working in lockstep with paid search insights.", "href": "/en/seo/"},
            {"title": "Dedicated Creative & CRO Sprints.", "text": "Ongoing ad creative production, landing page iterations, and conversion rate optimization without agency bottlenecks.", "href": "/en/web-design/"},
        ],
        "metrics": [
            {"value": "+230%", "label": "Blended multi-channel revenue growth over 12 months."},
            {"value": "6.4x", "label": "Unified cross-channel Return on Ad Spend (ROAS)."},
            {"value": "-39%", "label": "Lower blended Customer Acquisition Cost (CAC)."},
            {"value": "24/7", "label": "Executive Looker Studio dashboard & dedicated squad."},
        ],
        "processHeading": "How Our 360° Growth Partnership Works.",
        "processSubheading": "One strategic roadmap, agile bi-weekly sprints, and full executive accountability.",
        "steps": [
            ("360° Ecosystem Audit", "Auditing your brand positioning, website conversion rate, SEO footprint, ad accounts, and analytics stack."),
            ("Unified 90-Day Growth Roadmap", "Prioritizing the highest-ROI levers across paid acquisition, organic search, and conversion UX."),
            ("Full-Stack Tracking & Attribution", "Connecting GA4, GTM, Server-Side CAPI, and CRM stages into a single source of truth."),
            ("Omnichannel Campaign Launch", "Deploying synchronized search, social, and retargeting funnels backed by fresh studio creatives."),
            ("SEO, AEO & Content Velocity", "Shipping technical improvements and commercial-intent pages that lower long-term CAC."),
            ("Bi-Weekly CRO & Creative Sprints", "Continuously testing offers, ad creatives, and landing experiences based on live user data."),
            ("Executive Strategy Reviews", "Clear monthly and bi-weekly reviews focused on revenue, margin, CAC, LTV, and pipeline."),
            ("Global & Category Expansion", "Scaling your brand confidently into new product lines, languages, and international markets."),
        ],
        "faqs": [
            ("Who is 360° Digital Marketing Management ideal for?", "Ambitious e-commerce, healthcare, real estate, SaaS, B2B, and multi-location brands seeking a senior, full-stack growth team without hiring 6 separate in-house specialists."),
            ("Which channels are covered in a 360° retainer?", "Google Ads, Meta, TikTok, LinkedIn, Yandex, Bing, Enterprise SEO & AEO, Graphic/Motion Ad Creatives, Landing Page CRO, and GA4/Looker Analytics."),
            ("How do we communicate with our dedicated team?", "You work directly with senior strategists via dedicated Slack/WhatsApp channels, structured sprint boards, and regular executive review calls."),
            ("Do we retain ownership of every asset and account?", "100%. Every ad account, analytics property, creative file, and landing page belongs permanently to your company."),
            ("How is budget split across channels?", "Dynamically—guided by marginal ROAS, search demand ceilings, and unit economics rather than rigid silo quotas."),
            ("How do we begin?", "Schedule a complimentary 360° growth diagnostic via our Contact page."),
        ],
    },
]

# Homepage (/en/) 1:1 SSR + Flight string pairs (sorted longest-first at runtime)
HOME_TR_TO_EN_PAIRS = [
    ("Roasist | 360° Dijital Pazarlama, Web Tasarım & Büyüme Ajansı", "Roasist | 360° Digital Marketing, Performance & Growth Agency"),
    ("Roasist; veri odaklı performans pazarlaması (ROAS), yapay zeka destekli SEO & AEO, kreatif web tasarım ve marka stratejisiyle markaları büyüten 360° dijital ajans.", "Roasist is a data-driven 360° digital growth agency scaling ambitious brands through high-ROAS performance marketing, AI-ready SEO & AEO, and conversion web design."),
    ("ROASIST DIGITAL — 360° BÜYÜME & KREATİF AJANS : ", "ROASIST GLOBAL — 360° DIGITAL GROWTH & PERFORMANCE : "),
    ("Teklif Al", "Get a Proposal"),
    (">veriden<", ">data-led<"),
    (">beslenen<", ">scalable<"),
    (">büyüme.<", ">growth.<"),
    ('"children":"veriden"', '"children":"data-led"'),
    ('"children":"beslenen"', '"children":"scalable"'),
    ('"children":"büyüme."', '"children":"growth."'),
    (
        "Büyüyen işletmeler için dijital pazarlama çözümleri; <strong>kapsamlı ve özelleştirilmiş dijital pazarlama hizmetlerimizle işinizi bir sonraki seviyeye taşımanıza yardımcı olalım.</strong>",
        "Digital growth solutions for ambitious brands; <strong>let us take your business to the next level with tailored, data-driven performance marketing, SEO, and web engineering.</strong>",
    ),
    ("Trafiği yüksek dönüşüme, reklam yatırımını kârlı ciroya dönüştürüyoruz.", "We turn qualified traffic into conversions, and ad spend into profitable revenue."),
    ("Büyümek isteyen markaların tahmine değil, ölçülebilir performansa ihtiyacı vardır. Roasist; reklam yönetimi, SEO ve dönüşüm odaklı tasarımı tek stratejide birleştirir.", "Ambitious brands don't need guesswork—they need measurable performance. Roasist unites paid media, enterprise SEO, and conversion-led design in one strategy."),
    ("Veri Stratejisi", "Data Strategy"),
    ("Pazar, rakip ve arama niyeti analizleriyle bütçenizi en kârlı kanallara odaklayan büyüme planı.", "Market, competitor, and search-intent intelligence that focuses your budget on the highest-ROI channels."),
    ("Dönüşüm Tasarımı", "Conversion Craft"),
    ("Dikkat çeken reklam kreatifleri ve ziyaretçiyi müşteriye dönüştüren hızlı, ikna edici web deneyimi.", "Scroll-stopping ad creatives and blazing-fast, persuasive web experiences that turn visitors into buyers."),
    ("Yüksek ROAS", "Scalable ROAS"),
    ("Google, Meta, TikTok, Yandex ve SEO’da sürdürülebilir ciro üreten performans sistemleri.", "Performance architectures across Google, Meta, TikTok, LinkedIn, Yandex, Bing, and SEO built for compounding revenue."),
    ("HİZMETLER", "SERVICES"),
    ("Google Ads Yönetimi", "Google Ads"),
    ("Reklam bütçenizi sadece harcamıyor, kârlı yatırıma dönüştürüyoruz. Google, Meta, TikTok, LinkedIn, Yandex ve Bing’de veri odaklı ROAS mimarisiyle satışlarınızı ölçeklendiriyoruz.", "We don't just spend media budgets—we engineer profitable returns. Scale your sales with data-driven ROAS systems across Google, Meta, TikTok, LinkedIn, Yandex, and Bing."),
    ("Web Tasarım & Kreatif Stüdyo", "Web Design & Creative Studio"),
    ("Web Tasarım ve Kreatif Stüdyo", "Web Design & Creative Studio"),
    ("UI/UX & Web Tasarım", "UI/UX & Web Design"),
    ("Grafik & Kreatif Tasarım", "Graphic & Ad Creative"),
    ("Dönüşüm Optimizasyonu (CRO)", "Conversion Optimization (CRO)"),
    ("Estetiğin yüksek dönüşüm oranlarıyla (ROI) buluştuğu, ultra hızlı, mobil öncelikli web deneyimleri ve dikkat çekici kreatif reklam görselleri tasarlıyoruz.", "Ultra-fast, mobile-first web experiences and scroll-stopping ad creatives where distinctive aesthetics meet measurable conversion rates."),
    ("SEO, AEO & 360° Dijital Büyüme", "SEO, AEO & 360° Digital Growth"),
    ("SEO, AEO ve 360 Dijital Büyüme", "SEO, AEO & 360° Digital Growth"),
    ("Teknik & Kurumsal SEO", "Enterprise & Technical SEO"),
    ("Yapay Zeka Aramaları (AEO & GEO)", "AI Search (AEO & GEO)"),
    ("360° Dijital Yönetim", "360° Growth Management"),
    ("Google organik aramalarında ve ChatGPT, Gemini, Perplexity gibi yapay zeka yanıt motorlarında (AEO & GEO) markanızı sektör lideri konumuna taşıyoruz.", "Position your brand at the top of Google organic search and AI answer engines including ChatGPT, Gemini, and Perplexity."),
    ("Adım adım büyüme metodolojimiz.", "Our step-by-step growth methodology."),
    ("Önce veri ve strateji.", "Data & strategy first."),
    ("Önce veri ve strateji", "Data & strategy first"),
    ("Her şey derinlemesine analizle başlar. Pazarınızı, rakiplerinizi, birim ekonominizi ve hedef kitlenizi inceleyerek görsel veya kampanya öncesinde büyüme yol haritanızı netleştiririz.", "Everything begins with rigorous diagnostics. We analyze your market, competitors, unit economics, and buyer intent to map a clear roadmap before launching a single ad or pixel."),
    ("Yaratıcı ve cesur fikir.", "Bold creative direction."),
    ("Yaratıcı ve cesur fikir", "Bold creative direction"),
    ("Kreatif sınırları zorlarken her zaman veriye ve stratejiye sadık kalırız. Marka kimliğinden reklam kreatiflerine ve web etkileşimlerine kadar her detay dönüşüm için tasarlanır.", "We push creative boundaries while staying anchored in commercial data. From brand identity to video hooks and web interactions, every detail is built to convert."),
    ("Kusursuz süreç yönetimi.", "Seamless sprint execution."),
    ("Kusursuz süreç yönetimi", "Seamless sprint execution"),
    ("İlk günden itibaren şeffaf, çevik ve sonuç odaklıyız. Gerçek zamanlı veri panelleri ve düzenli sprintlerle projenizin her aşamasında ivmeyi hissedersiniz.", "Transparent, agile, and accountable from day one. With live Looker Studio dashboards and structured sprints, you feel momentum at every stage."),
    ("Dönüşüm için tasarla.", "Engineered to convert."),
    ("Dönüşüm için tasarla", "Engineered to convert"),
    ("En küçük detayı bile optimize ederiz. Kreatif görsellerden teknik SEO mimarisine ve kullanıcı deneyimi (UX) akışına kadar her karar ROAS ve etkileşimi artırmak içindir.", "We optimize every micro-interaction. From ad creatives to technical SEO architecture and UX flows, every decision serves higher ROAS and conversion."),
    ("Ölçeklenebilir büyüme.", "Scalable global growth."),
    ("Ölçeklenebilir büyüme", "Scalable global growth"),
    ("Markanızın büyümesine hazırız. Yeni ürün lansmanlarından global pazar açılımlarına kadar dijital altyapınızı ve kampanyalarınızı sürdürülebilir ölçeklenmeye hazırlarız.", "Built to scale alongside your ambition. From new product launches to international market expansion, we prepare your infrastructure and campaigns for compounding growth."),
    ("SEÇİLMİŞ", "SELECTED"),
    ("PROJELER", "WORK"),
    ("Markaları dijitalde çok daha güçlü kılıyoruz.", "We make ambitious brands unstoppable online."),
    ("Öne çıkan projelerimizi ve onları şekillendiren stratejik kararları inceleyin. ", "Explore our featured client partnerships and the strategic decisions behind their growth. "),
    ("Öne çıkan projelerimizi ve onları şekillendiren stratejik kararları inceleyin.", "Explore our featured client partnerships and the strategic decisions behind their growth."),
    ("Tüm Referansları Gör", "View All Case Studies"),
    ("ÖLÇÜLEBİLİR", "MEASURABLE"),
    ("SONUÇLAR", "RESULTS"),
    ("1 ay içinde kullanıcı başına etkileşimli oturum oranında artış.", "Increase in engaged sessions per user within 30 days."),
    ("3 ay içinde ortalama etkileşim süresinde ve dönüşüm kalitesinde artış.", "Increase in average engagement duration and lead quality within 90 days."),
    ("Teknik SEO ve AEO optimizasyonu sonrası organik trafikte büyüme", "Organic search traffic growth following technical SEO & AEO rollout"),
    ("Projeyi İncele", "View Case Study"),
    ("Müşterilerimiz ne diyor?", "What our clients say."),
    (
        '"Web sitemizin yeniden tasarım ve dönüşüm optimizasyonu sürecinde sundukları yaratıcı yaklaşım ve stratejik derinlikten ilk anda etkilendik. Birlikte çalışması son derece keyifli ve profesyonel bir ekip!"',
        '"We were immediately impressed by their strategic depth and creative precision during our website redesign and CRO rollout. An exceptionally responsive and results-driven team!"',
    ),
    ("DermaDerm E-Ticaret", "DermaDerm E-Commerce"),
    ("Pazarlama & E-Ticaret Yönetimi", "Marketing & E-Commerce Lead"),
    (
        '"Marka konumlandırma ve 360° performans çalışmalarımız tüm dijital kanallarda taşları yerine oturttu. Roasist ekibi hızlı, esnek ve hem kreatif tasarımda hem de ROAS yönetiminde olağanüstü yetenekli."',
        '"Our positioning and 360° performance overhaul made every digital channel click together. Roasist is fast, agile, and extraordinary across both creative craft and ROAS scaling."',
    ),
    ("Medistate Dijital Ekibi", "Medistate Digital Team"),
    ("Kurumsal İletişim & Büyüme", "Corporate Communications & Growth"),
    (
        '"Estetiğin çok ötesinde, yüksek dönüşüm üreten bir altyapı kurdular. SEO mimarisi ve performans kampanyaları sayesinde hem organik trafiğimiz hem de nitelikli müşteri taleplerimiz katlanarak arttı."',
        '"Beyond standout aesthetics, they engineered a high-converting growth engine. Thanks to their SEO architecture and paid media synergy, both our organic traffic and qualified leads multiplied."',
    ),
    ("Sekiz Oniki Kurumsal", "Sekiz Oniki Corporate"),
    ("Yönetim Kurulu", "Executive Board"),
    (
        '"Reklam sürecinde projeye yaklaşımları, anlaşmamızın ötesinde sorumluluk alarak grafik tasarım katkısı sunmaları ve 7/24 destekleriyle işimiz için en az bizim kadar dertlenen bir ekiple çalıştığımız için şanslıyız. Roasist ile gönül rahatlığıyla çalışabilirsiniz."',
        ROASIST_TESTIMONIALS_EN[0]["text"],
    ),
    (
        '"Roasist ile yaklaşık iki senedir çalışıyoruz. Her sorumuza dürüstlükle yanıt alıyor, tüm sorunlarımızı efektif bir şekilde çözüyorlar. Öncesi-sonrası değerlendirmesi yaptığımda kazanç konusunda bize çok büyük katkıları oldu. Profesyonel yaklaşımları için çok teşekkür ederim."',
        ROASIST_TESTIMONIALS_EN[1]["text"],
    ),
    ("Girişimci & Kurucu", "Entrepreneur & Founder"),
    (
        '"Mesai kavramı olmaksızın sizin için çalışıyorlar. İşinde profesyonel, şeffaf ve doğrudan sonuç odaklı bir dijital pazarlama ajansı arıyorsanız Roasist\'i kesinlikle tavsiye ederim."',
        ROASIST_TESTIMONIALS_EN[2]["text"],
    ),
    ("İşletme Sahibi", "Business Owner"),
    ("Güncel yazılar", "Latest insights"),
    ("Performans Pazarlamasında ROAS ve Dönüşüm Oranı Nasıl Artırılır?", BLOG_POSTS_EN[2]["title"]),
    ("Kurumsal SEO ve Yapay Zeka Aramaları (AEO) Rehberi", BLOG_POSTS_EN[1]["title"]),
    ("Performans Pazarlaması Nedir? Markanızı Nasıl Ölçeklendirir?", BLOG_POSTS_EN[0]["title"]),
    ("Veriye Dayalı Dijital Pazarlama Stratejisi Nedir?", BLOG_POSTS_EN[0]["title"]),
    ("Reklam Harcamalarının Geri Dönüşü (ROAS) Nasıl Hesaplanır?", BLOG_POSTS_EN[2]["title"]),
    ("6 dk okuma", "6 min read"),
    ("7 dk okuma", "7 min read"),
    ("5 dk okuma", "5 min read"),
    ("Dijital Strateji", "Digital Strategy"),
    ("Tüm makaleler", "All articles"),
    ("Sıkça Sorulan Sorular", "Frequently Asked Questions"),
    ("Roasist hangi dijital pazarlama hizmetlerini sunuyor?", "Which digital marketing services does Roasist provide?"),
    ("Performans Pazarlaması (Google Ads, Meta, TikTok, LinkedIn, Yandex, Bing), Kurumsal SEO & Yapay Zeka Aramaları (AEO/GEO), Dönüşüm Odaklı Web Tasarım & Yazılım, Grafik/Kreatif Tasarım ve 360° Dijital Pazarlama Yönetimi sunuyoruz.", "We provide Performance Marketing (Google Ads, Meta, TikTok, LinkedIn, Yandex, Bing), Enterprise SEO & AI Search (AEO/GEO), Conversion-Led Web Design & Engineering, Graphic/Ad Creative Design, and 360° Digital Marketing Management."),
    ("Çalışma süreciniz nasıl başlıyor?", "How does your onboarding process begin?"),
    ("Sürecimiz ücretsiz ön analiz ve strateji görüşmesiyle başlar. Mevcut dijital varlıklarınızı, reklam hesaplarınızı ve sektörünüzdeki gerçek arama hacimlerini inceler; işletmenize özel KPI ve büyüme yol haritasını çıkarırız.", "We begin with a complimentary digital diagnostic and strategy session—auditing your website, ad accounts, and real API search demand to craft a custom KPI and growth roadmap."),
    ("Reklam hesapları ve veriler kimin mülkiyetinde oluyor?", "Who owns the ad accounts and analytics data?"),
    ("Şeffaflık ilkemiz gereği tüm reklam hesapları (Google Ads, Meta, TikTok, LinkedIn, Yandex) ve analitik mülkleri doğrudan sizin adınıza açılır ve %100 sizin mülkiyetinizde kalır. Tüm performans verilerini 7/24 canlı olarak takip edebilirsiniz.", "By principle, every ad account (Google, Meta, TikTok, LinkedIn, Yandex, Bing) and analytics property is created under your company and stays 100% in your ownership, paired with 24/7 live dashboards."),
    ("Sadece tek bir hizmet (örneğin SEO veya Google Ads) alabilir miyiz?", "Can we engage Roasist for a single service like SEO or Google Ads?"),
    ("Evet. İhtiyacınıza göre yalnızca Google Reklamları, SEO veya Web Tasarım gibi tekil uzmanlık hizmetlerimizden faydalanabileceğiniz gibi, tüm dijital kanallarınızı kapsayan 360° Dijital Pazarlama Yönetimi modelimizle de çalışabilirsiniz.", "Yes. You can partner with us for a focused specialist channel—such as Google Ads, Enterprise SEO, or Web Design—or choose our integrated 360° Digital Marketing Management model."),
    ("Tasarım ve kampanya süreçlerinde revizyon ve geri bildirimleri nasıl yönetiyorsunuz?", "How do you manage feedback and iterations across design and campaigns?"),
    ("Geri bildirimleriniz tasarım ve strateji sürecimizin merkezindedir. Her aşamada şeffaf iletişim kurarak görüşlerinizi iterasyonlara dahil ediyor, markanızın vizyonunu tam olarak yansıtan kusursuz sonuca birlikte ulaşıyoruz.", "Your input sits at the center of our sprint workflow. Through transparent communication and structured review rounds, we refine every detail around your brand vision and commercial targets."),
    ("Web projelerine SEO ve performans reklamlarını entegre etmek nasıl bir avantaj sağlar?", "What is the advantage of integrating SEO and paid media into web design?"),
    ("Web tasarım sürecine daha ilk günden teknik SEO, AEO ve dönüşüm odaklı performans pazarlamasını entegre etmek dijital büyümenize çarpan etkisi yapar. İhtiyacınıza göre tekil hizmet veya 360° entegre büyüme paketlerimiz için bizimle iletişime geçebilirsiniz.", "Baking technical SEO, AEO, and conversion psychology into your website from day one multiplies both organic rankings and paid ROAS. Contact us for single-discipline or 360° growth packages."),
    ("Showreel İzle", "Watch Showreel"),
]

# Shared Project / Portfolio / References TR -> EN pairs (used on Homepage, Service pages, and /en/references/)
REFERENCES_TR_TO_EN_PAIRS = [
    ("Referanslar & Başarı Hikayeleri | Roasist", "Our Work & Case Studies | Roasist"),
    ("Roasist olarak birlikte büyüdüğümüz markaların performans pazarlaması, kurumsal SEO, web tasarım ve 360° dijital pazarlama başarı hikayelerini inceleyin.", "Explore how Roasist scales ambitious brands across healthcare, real estate, e-commerce, SaaS, hospitality, and B2B through performance marketing, SEO, and web design."),
    ("Markaları <em>dijitalde</em> büyüten uzmanlık.", "Expertise that scales brands <em>digitally.</em>"),
    ("Veri odaklı performans pazarlaması, kurumsal SEO ve dönüşüm mimarisiyle büyüttüğümüz markaları keşfedin.", "Discover the brands we have scaled through data-driven performance marketing, enterprise SEO, and conversion engineering."),
    # Featured 5 + 24 Reference descriptions
    ("Lüks gayrimenkul projeleri için yatırımcı odaklı büyüme.", "Investor-focused global acquisition for luxury real estate developments."),
    ("Uluslararası gayrimenkul lideri için 360° dijital büyüme.", "360° international digital growth for a leading real estate brand."),
    ("Sağlık turizminde hasta edinimini ölçekleyen performans.", "High-ROAS international patient acquisition in medical tourism."),
    ("Uluslararası sağlık grubu için veri odaklı hasta edinimi.", "Data-driven international patient acquisition for a global hospital group."),
    ("Sektör lideri çağrı merkezi için yetenek kazanımı.", "Scalable multilingual talent acquisition for an industry-leading call center."),
    ("Almanya'da çocuk kitabı yayıncılığında marka bilinirliği ve kültürel erişim.", "Brand awareness and cultural reach for children's book publishing in Germany."),
    ("Bitkisel cilt ve saç bakımında doğrudan tüketiciye satış ölçekleme.", "Direct-to-consumer (D2C) e-commerce scaling in botanical skin and hair care."),
    ("Butik tatil ve gayrimenkul konseptinde yüksek etkileşimli doluluk.", "High-engagement booking growth for a boutique hospitality and property concept."),
    ("Cerrahi uzmanlık alanlarında küresel hasta iletişimi ve randevu hacmi.", "Global patient outreach and consultation volume for surgical specialists."),
    ("Dermokozmetik laboratuvar ürünlerinde pazaryeri ve web satışı.", "Marketplace and D2C web revenue growth for dermocosmetic laboratory formulas."),
    ("E-ticaret entegrasyonu yazılımında SaaS büyüme ve müşteri edinimi.", "B2B SaaS user acquisition and recurring growth for an e-commerce integration platform."),
    ("Ege gastronomisinde marka konumlandırma ve ziyaretçi trafiği.", "Brand positioning and guest reservation growth in Aegean fine dining."),
    ("Erken çocukluk eğitiminde güven ve veli odaklı kayıt stratejisi.", "Parent-focused enrollment and trust strategy in early childhood education."),
    ("Estetik ve cerrahide hasta odaklı dijital büyüme.", "Patient-focused international digital growth in aesthetic surgery."),
    ("Ev dekorasyonunda ortalama sepet tutarı ve e-ticaret ROAS artışı.", "Higher average order value (AOV) and e-commerce ROAS in home decor."),
    ("Evsel ve kurumsal su arıtma sistemlerinde talep ve satış dönüşümü.", "Lead generation and sales conversion for residential & commercial water systems."),
    ("Eğitim sektöründe hedef kitle odaklı öğrenci kayıt dönüşümü.", "Targeted student enrollment campaigns in private education."),
    ("Gastronomide yerel marka bilinirliği ve masa rezervasyonu.", "Local brand authority and table reservation growth in gastronomy."),
    ("Lokal butik otel konseptinde doğrudan rezervasyon ve doluluk artışı.", "Direct booking and occupancy growth for a boutique hotel group."),
    ("Lokal böcek ve haşere ilaçlama hizmetinde anlık çağrı dönüşümü.", "High-intent local search call conversions for commercial pest control."),
    ("Medya ve iletişim eğitimlerinde sektör profesyonellerine erişim.", "Targeted enrollment growth for media and communication academy programs."),
    ("Mobil oyun ekosisteminde kullanıcı edinimi ve küresel ölçeklenme.", "Global user acquisition (UA) and scaling in the mobile gaming ecosystem."),
    ("Mobil ulaşım teknolojisinde aktif kullanıcı edinimi ve büyüme.", "Active rider acquisition and retention in urban mobility technology."),
    ("Müşteri iletişim merkezleri için veri odaklı büyüme stratejisi.", "Data-driven recruitment and B2B growth for customer contact centers."),
    ("Online kitap satışında sepet dönüşüm oranı ve ROAS optimizasyonu.", "Checkout conversion rate and ROAS optimization in online book retail."),
    ("Organik bebek ve çocuk beslenmesinde güven odaklı satış dönüşümü.", "Trust-led e-commerce sales growth in organic baby and child nutrition."),
    ("Organik ve doğal yaşam ürünlerinde sürdürülebilir e-ticaret geliri.", "Sustainable D2C e-commerce revenue in organic and natural living products."),
    ("Otomotiv performans teknolojisinde e-ticaret satış ve lead artışı.", "E-commerce sales and global dealer leads in automotive performance tech."),
    ("Premium dermokozmetikte e-ticaret satış hacmi ve marka sadakati.", "E-commerce volume and repeat customer loyalty in premium dermocosmetics."),
    ("Sağlık turizminde global hasta kazanımı ve ölçekleme.", "Global patient acquisition and multi-market scaling in medical tourism."),
    ("Sınav hazırlık eğitiminde hedefli veli iletişimi ve şube kayıtları.", "Parent engagement and campus enrollments in academic exam preparation."),
    ("Uluslararası saç ekimi ve estetikte yüksek dönüşümlü hasta edinimi.", "High-converting international patient acquisition in hair restoration & aesthetics."),
    ("Yabancı yatırımcı odaklı lüks gayrimenkul portföy pazarlaması.", "International investor marketing for luxury real estate portfolios."),
    ("Yatırım ve yaşam danışmanlığında nitelikli müşteri portföyü.", "Qualified international client acquisition in investment & relocation consulting."),
    ("Yazılım ve teknoloji yayıncılığında e-ticaret odaklı satış artışı.", "E-commerce revenue acceleration in software and technology publishing."),
    ("Çağrı merkezi sektöründe nitelikli lead ve yetenek kazanımı.", "Qualified B2B leads and multilingual talent recruitment in BPO."),
    ("Çok dilli çağrı merkezi operasyonları için nitelikli yetenek kazanımı.", "Multilingual talent acquisition for European-facing call center operations."),
    ("Özel okul eğitiminde veli etkileşimi ve yeni dönem kayıt başarısı.", "Parent engagement and new-term enrollment growth for private schools."),
    # Sector & Service Tags
    ("Gayrimenkul ve Turizm", "Real Estate & Hospitality"),
    ("Çağrı Merkezi", "Call Center & BPO"),
    ("Yeme İçme", "Gastronomy"),
    ("Sağlık", "Healthcare"),
    ("Eğitim", "Education"),
    ("Performans Pazarlaması", "Performance Marketing"),
    ("360° Dijital Pazarlama Yönetimi", "360° Digital Marketing"),
    ("360° Dijital Pazarlama", "360° Digital Marketing"),
    ("Büyüme Stratejisi", "Growth Strategy"),
    ("Web Analitik", "Web Analytics"),
    ("Web Analitiği", "Web Analytics"),
    ("Kreatif İletişim", "Creative Direction"),
    ("Kurumsal İletişim", "Corporate Communications"),
    ("Web Tasarım", "Web Design"),
    ("Grafik Tasarım", "Graphic Design"),
    ("E-Ticaret Büyüme", "E-Commerce Growth"),
    ("E-Ticaret Reklamları", "E-Commerce Ads"),
    ("E-Ticaret Stratejisi", "E-Commerce Strategy"),
    ("Kayıt Stratejisi", "Enrollment Strategy"),
    ("Lokal Arama Reklamları", "Local Search Ads"),
    ("Marka Bilinirliği", "Brand Awareness"),
    ("Rezervasyon Büyümesi", "Booking Growth"),
    ("Talep Oluşturma", "Demand Generation"),
    ("Uygulama Büyüme", "App Growth"),
    ("Yayıncılık İletişimi", "Publishing Growth"),
    ("Yetenek Kazanımı", "Talent Acquisition"),
]

# About Us (/en/who-we-are/) pairs
ABOUT_TR_TO_EN_PAIRS = [
    ("Hakkımızda | Roasist Dijital Pazarlama Ajansı", "Who We Are | About Roasist Digital Growth Agency"),
    (
        "Roasist, dijital pazarlama sektöründe özelleştirilmiş, kalite, süreç ve hız odaklı yaklaşımıyla öne çıkan yeni nesil dijital büyüme ve performans ajansıdır.",
        "Roasist is a next-generation digital growth and performance marketing agency defined by tailored strategy, process discipline, creative quality, and speed.",
    ),
    ("<i></i>Hakkımızda", "<i></i>Who We Are"),
    ("Veriyle büyüyen markaların stratejik ortağı.", "The strategic partner for data-driven brands."),
    ("Güçlü", "Bold"),
    ("Özgün", "Tailored"),
    ("Özelleştirilmiş ve veri odaklı stratejilerle markanızın büyüme sorumluluğunu üstleniyoruz.", "We take full ownership of your brand's digital growth with tailored, data-driven strategies."),
    (
        "Çoğu insan gerçekte özgürlük istemez, çünkü özgürlük sorumluluk gerektirir ve çoğu insan sorumluluktan korkar.",
        "Most people do not really want freedom, because freedom involves responsibility, and most people are frightened of responsibility.",
    ),
    (
        "<p>Özgürlüğü ve sorumluluğu bir arada benimsiyor; çalıştığımız her markanın dijital büyüme hedeflerini kendi işimiz gibi sahipleniyoruz.</p>\n<p>Roasist, dijital pazarlama sektöründe özelleştirilmiş ve yenilikçi yaklaşımıyla öne çıkan bir dijital pazarlama ajansıdır. Müşterilerimize en güçlü sonuçları sunmak için kanıtlanmış pazarlama prensiplerini modern fikirler ve veri analitiğiyle birleştiriyor; hızla değişen dijital dünyayı yakından takip ederek araştırmaya ve kendimizi geliştirmeye sürekli yatırım yapıyoruz.</p>\n",
        "<p>We embrace creative freedom and commercial responsibility together, owning every partner brand’s revenue and digital growth targets as if they were our own.</p>\n<p>Roasist stands apart as a tailored, innovation-led digital growth agency. To deliver compounding results, we pair proven marketing fundamentals with modern creative execution and deep analytics—continually investing in research as algorithms, AI search, and buyer behaviors evolve.</p>\n",
    ),
    (
        "<p>“Çoğu insan gerçekte özgürlük istemez, çünkü özgürlük sorumluluk gerektirir ve çoğu insan sorumluluktan korkar.” — Sigmund Freud’un bu sözü, Roasist’in kuruluş felsefesini yansıtır. Biz özgürlüğü ve sorumluluğu bir arada benimsiyor; çalıştığımız her markanın dijital büyüme hedeflerini kendi işimiz gibi sahipleniyoruz.</p>\n<p>Roasist, dijital pazarlama sektöründe özelleştirilmiş ve yenilikçi yaklaşımıyla öne çıkan bir dijital pazarlama ajansıdır. Müşterilerimize en güçlü sonuçları sunmak için kanıtlanmış pazarlama prensiplerini modern fikirler ve veri analitiğiyle birleştiriyor; hızla değişen dijital dünyayı yakından takip ederek araştırmaya ve kendimizi geliştirmeye sürekli yatırım yapıyoruz.</p>\n",
        "<p>“Most people do not really want freedom, because freedom involves responsibility, and most people are frightened of responsibility.” — Sigmund Freud’s observation sits at the heart of Roasist’s founding philosophy. We embrace creative freedom and commercial responsibility together, owning every partner brand’s revenue targets as if they were our own.</p>\n<p>Roasist stands apart as a tailored, innovation-led digital growth agency. To deliver compounding results, we pair proven marketing fundamentals with modern creative execution and deep analytics—continually investing in research as algorithms, AI search, and buyer behaviors evolve.</p>\n",
    ),
    ("Yaklaşım", "Our Approach"),
    (
        "<p>Kalite ve süreç odaklı bir yaklaşım benimsiyoruz. Her bir müşterimizin hedefleri ve ihtiyaçları farklı olduğundan, standart kalıplar yerine markanıza özel kurgulanmış bütünsel dijital pazarlama çözümleri sunuyoruz.</p>\n<p>Esnekliği, çeşitliliği ve yakın işbirliği kültürünü değerli buluyoruz. Markalarımızla güçlü ve şeffaf ilişkiler kuruyor; Google, Meta, TikTok ve Yandex resmi partnerliklerimizle en güncel reklam teknolojilerini işiniz için uyguluyoruz.</p>\n<p>Dijital dünyada hızın belirleyici olduğunun bilinciyle hareket ediyoruz. Acil ihtiyaçları çevik bir şekilde ele alıyor; kalite, esneklik ve hızı koruyarak markanıza daha fazla müşteri, satış ve sürdürülebilir büyüme kazandırıyoruz.</p>\n",
        "<p>We operate with a quality- and process-driven mindset. Because every business has distinct unit economics and growth bottlenecks, we never force copy-paste packages—instead architecting bespoke, full-funnel digital marketing systems.</p>\n<p>We value agility, transparency, and close executive collaboration. Backed by our official Google, Meta, TikTok, and Yandex partnerships, we deploy the latest advertising and attribution technologies directly inside your accounts.</p>\n<p>In digital markets, speed is a competitive moat. We respond swiftly to market shifts while protecting craft and data accuracy—delivering more customers, stronger ROAS, and sustainable scale.</p>\n",
    ),
    ("<em>Özgürlük ve sorumluluk</em> yaptığımız her işin temelidir.", "<em>Freedom and responsibility</em> are at the core of everything we build."),
    (
        "Keşfetmek için ilkeleri ve kanalları sürükleyin veya bir düğüme tıklayın.",
        "Drag or click any principle or channel node to explore.",
    ),
    ("Randevu Planlayın", "Schedule a Call"),
    (
        "<p>Roasist’in özelleştirilmiş pazarlama yaklaşımlarıyla markanızın gerçek potansiyelini ortaya çıkarıyoruz. Bize güvenen iş ortaklarımızın dijital varlıklarını güçlendiriyor, pazarlama güçlerini ölçülebilir sonuçlarla artırıyoruz.</p>\n",
        "<p>Through Roasist’s tailored growth architecture, we unlock your brand’s full commercial potential—strengthening digital assets and multiplying marketing ROI for every partner who trusts us.</p>\n",
    ),
    (
        "<p>Performans pazarlaması, kurumsal SEO, kreatif tasarım ve web geliştirme disiplinlerinde uzman ekibimizle dijital varlıklarınızı güçlendiriyor ve işinizi büyütüyoruz.</p>\n",
        "<p>Our multidisciplinary specialists across performance marketing, enterprise SEO, creative design, and web engineering work as one cohesive team to scale your business.</p>\n",
    ),
    ("Resmi Partnerlikler & Başarılar", "Official Partnerships & Credentials"),
    ("Resmi Ajans Partneri", "Official Agency Partner"),
    ("Resmi Pazarlama Partneri", "Official Marketing Partner"),
    ("Sertifikalı Performans Uzmanlığı", "Certified Performance Specialists"),
    ("Yüksek ROAS & Büyüme Ödülü", "High-ROAS & Growth Excellence"),
    ("Pazarlama Direktörü", "Marketing Director"),
    (
        "<p>Roasist’te Brand Partner olarak stratejik iş ortaklıkları kuruyor, yeni büyüme fırsatları geliştiriyor ve markaları hedeflerine özel dijital pazarlama çözümleriyle buluşturuyor.</p>\n<p>İş stratejisi, müşteri danışmanlığı ve uzman ekipleri tek köprüde birleştirerek, hizmet sunumunun ötesine geçen kalıcı değer ve sürdürülebilir marka ortaklıkları inşa etmeye odaklanıyor.</p>\n",
        "<p>As a Brand Partner at Roasist, Leyla focuses on building strategic partnerships, developing business opportunities, and connecting brands with tailored digital marketing solutions.</p>\n<p>Bridging business strategy, client advisory, and cross-functional digital expertise, she builds trusted relationships and long-term partnerships that deliver lasting value beyond service delivery.</p>\n",
    ),
    ("Markanızı Roasist ile büyütmeye hazır mısınız?", "Ready to scale your brand with Roasist?"),
    (
        '<p>Bize hemen ulaşın:<br />\n<a href="mailto:info@roasist.com">info@roasist.com</a></p>\n',
        '<p>Drop us a line today:<br />\n<a href="mailto:info@roasist.com">info@roasist.com</a></p>\n',
    ),
    (
        "Performans pazarlaması, Google & Meta reklamları, SEO, kreatif tasarım ve web yazılım çözümleriyle markanızı kârlı biçimde ölçeklendiren 360° dijital büyüme ajansıyız.",
        "We are a 360° digital growth agency scaling ambitious brands profitably through performance marketing, Google & Meta Ads, enterprise SEO, creative design, and web engineering.",
    ),
]

# Contact Us (/en/contact-us/) pairs
CONTACT_TR_TO_EN_PAIRS = [
    ("İletişim | Roasist Dijital Pazarlama Ajansı", "Contact Us | Roasist Digital Marketing Agency"),
    (
        "Markanızın dijital büyüme hedefleri, performans pazarlaması, kurumsal SEO ve web tasarım projeleri için Roasist uzman ekibiyle iletişime geçin.",
        "Get in touch with Roasist's growth specialists for performance marketing, Google & Meta Ads, enterprise SEO, and conversion web design.",
    ),
    ("Birlikte <br />\r\nbüyük başarılar <br />\r\niçin merhaba <em>deyin.</em>", "Say hello <br />\r\nto bigger <br />\r\ndigital <em>growth.</em>"),
    ("Birlikte <br />\nbüyük başarılar <br />\niçin merhaba <em>deyin.</em>", "Say hello <br />\nto bigger <br />\ndigital <em>growth.</em>"),
    ("Hızlıca yanıtlanmasını istediğiniz bir sorunuz mu var?<br />\nHizmetlerimiz :", "Have a question about scaling your brand?<br />\nDirect Channels :"),
    ("Yeni Proje & Teklif", "New Project & Audit"),
    ("Genel Sorular", "General Inquiries"),
    ("İletişim Hattı", "Phone & WhatsApp"),
    ("Roasist ile Çalışmak", "Partnering With Roasist"),
    ("Kariyer & İş Birliği", "Careers & Partnerships"),
    ("Roasist Dijital Pazarlama Ajansı<br />\nİstanbul, Türkiye", "Roasist Digital Growth Agency<br />\nIstanbul, Turkey"),
    ("Bizi Takip Edin", "Follow Us"),
    ("Mesajınız için teşekkür ederiz!", "Thank you for your message!"),
    (
        "Roasist ekibimiz en kısa sürede sizinle iletişime geçecek. Bu sırada öne çıkan başarı hikayelerimizi inceleyebilirsiniz :",
        "Our strategy team will review your inquiry and get back to you shortly. Meanwhile, explore our featured case studies :",
    ),
    ("Küresel gayrimenkul yatırımlarında çok kanallı performans mimarisi.", "Omnichannel performance architecture for luxury global real estate."),
    ("Uluslararası yatırımcı kazanımında Google, Meta ve Yandex büyüme stratejisi.", "Google, Meta, and Yandex investor acquisition strategy."),
    ("Uluslararası Satış", "Global Acquisition"),
    ("SEO & Performans", "SEO & Performance"),
    ("İstanbul", "Istanbul"),
]

# Privacy Policy (/en/privacy-policy-and-terms-of-use/) English Prose
PRIVACY_EN_HTML = (
    "<h2>1. Data Controller &amp; Privacy Commitment</h2>"
    "<p>At Roasist Digital Marketing Agency (“Roasist”), we are committed to protecting the personal data and privacy "
    "of all visitors, prospective clients, and business partners across our digital properties in strict compliance "
    "with GDPR and Law No. 6698 on the Protection of Personal Data (KVKK).</p>"
    "<h2>2. Information We Collect &amp; Purpose of Processing</h2>"
    "<p>Information voluntarily submitted via our contact forms—such as your full name, corporate email address, phone "
    "number, company name, and project brief—alongside anonymized first-party analytics data is processed solely to "
    "prepare tailored digital marketing audits, respond to your inquiries, and deliver contracted services.</p>"
    "<h2>3. Cookies &amp; Google Consent Mode v2</h2>"
    "<p>Our website uses strictly necessary operational cookies and, subject to your explicit consent preference, "
    "analytics and performance tags managed via Google Tag Manager (GTM-TRVG2SF) with Consent Mode v2. Your personal "
    "data is never sold or shared with unauthorized third parties.</p>"
    "<h2>4. Data Security &amp; Retention</h2>"
    "<p>All inquiries and client records are protected behind TLS encryption and strict role-based access controls, "
    "and are retained only for the duration required by commercial and statutory obligations.</p>"
    "<h2>5. Terms of Use &amp; Intellectual Property</h2>"
    "<p>All text, custom graphics, videos, case studies, logos, and software code published on www.roasist.com are the "
    "intellectual property of Roasist Digital Marketing Agency and may not be reproduced commercially without prior "
    "written permission.</p>"
    "<h2>6. Your Rights &amp; Contact</h2>"
    "<p>You may request access to, rectification of, or deletion of your personal data at any time by contacting us at "
    '<a href="mailto:info@roasist.com">info@roasist.com</a> or calling <a href="tel:+905405075350">+90 540 507 53 50</a>.</p>'
)
