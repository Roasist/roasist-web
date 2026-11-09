export interface ServiceFeature {
  title: string;
  description: string;
  icon: string;
}

export interface ServiceFAQ {
  question: string;
  answer: string;
}

export interface ServiceComparisonRow {
  criteria: string;
  traditional: string;
  roasist: string;
}

export interface ServicePageData {
  slug: string;
  permalink: string;
  category: 'Ana Hizmet' | 'Performans Kanalı';
  icon: string;
  seoTitle: string;
  seoDescription: string;
  h1: string;
  heroQuestion: string;
  aeoDirectAnswer: string;
  metrics: Array<{ value: string; label: string; detail: string }>;
  overviewHeading: string;
  overviewParagraphs: string[];
  subFeaturesTitle: string;
  subFeaturesSubtitle: string;
  subFeatures: ServiceFeature[];
  processTitle: string;
  processSteps: Array<{ step: string; title: string; description: string }>;
  comparisonRows: ServiceComparisonRow[];
  faqs: ServiceFAQ[];
}

export const defaultWhyUs = [
  {
    title: 'Şeffaf & Ölçülebilir Süreç',
    description: 'İşbirliğine dayalı bir çalışma kültürü benimsiyor, reklam hesaplarınızı ve canlı veri panellerini 7/24 şeffaf şekilde sizinle paylaşıyoruz.',
    icon: 'tabler:chart-dots-3',
  },
  {
    title: 'Yenilikçi Teknoloji (Roasist OS)',
    description: 'Geleneksel yöntemleri kendi geliştirdiğimiz Roasist Marketing Intelligence OS veri analiz ve anahtar kelime teknolojileriyle destekliyoruz.',
    icon: 'tabler:cpu',
  },
  {
    title: 'Araştırmacı & Veri Odaklı',
    description: 'Sektörünüzdeki gerçek arama hacimlerini, rakip stratejilerini ve dönüşüm maliyetlerini derinlemesine analiz ederek bütçenizi koruyoruz.',
    icon: 'tabler:analyze',
  },
  {
    title: 'Kalite ve Süreç Odaklı',
    description: 'Derin düşünür ve bütünsel hareket ederiz. Trafik artışına değil, nitelikli potansiyel müşteriye ve gerçek satışa (ROAS) odaklanırız.',
    icon: 'tabler:target-arrow',
  },
  {
    title: 'Esnek ve Kavrayıcı Strateji',
    description: 'Standart kalıpları dayatmaz; her markanın büyüme evresine, kar marjına ve hedef kitlesine özel özgün pazarlama planları kurgularız.',
    icon: 'tabler:adjustments-horizontal',
  },
  {
    title: 'Hızlı Refleks & Optimizasyon',
    description: 'Pazar dinamiklerine ve kampanya sinyallerine ani refleks gösterir, bütçe israfını önleyen hızlı optimizasyon aksiyonları alırız.',
    icon: 'tabler:bolt',
  },
];

export const defaultProcessSteps = [
  {
    step: '01',
    title: 'Analiz & Denetim',
    description: 'Mevcut dijital varlıklarınızı, geçmiş kampanya verilerinizi ve rakiplerinizi denetler; işinize özel gerçekçi KPI ve büyüme hedefleri belirleriz.',
  },
  {
    step: '02',
    title: 'Strateji Oluşturma',
    description: 'Belirlenen hedefler doğrultusunda bütçe dağılımını, kanal kırılımını ve hedef kitle segmentasyonunu içeren ölçeklenebilir yol haritasını kurarız.',
  },
  {
    step: '03',
    title: 'Kurulum & Proje Yönetimi',
    description: 'Dönüşüm takibi (GTM, GA4, Pixel, Conversion API), kampanya mimarisi ve kreatif varlıkları eksiksiz kurarak süreci uçtan uca yönetiriz.',
  },
  {
    step: '04',
    title: 'Sürekli Optimizasyon',
    description: 'A/B testleri, negatif kelime temizliği, teklif stratejisi güncellemeleri ve kreatif rotasyonlarla birim dönüşüm maliyetlerinizi (CPA) düşürürüz.',
  },
  {
    step: '05',
    title: 'Şeffaf Raporlama',
    description: 'Yaptığımız çalışmaları anlaşılır ve görsel raporlar halinde sunarız. Hangi kanalın ne kadar ciro ve ROAS ürettiğini net biçimde gösteririz.',
  },
  {
    step: '06',
    title: 'Yeni Büyüme Fırsatları',
    description: 'Pazar trendlerini, yeni arama sorgularını ve sektörünüzdeki gelişmeleri takip ederek markanızı rakiplerinizin önüne taşıyacak fırsatlar yaratırız.',
  },
];

export const servicesData: ServicePageData[] = [
  {
    slug: 'seo',
    permalink: '/hizmetler/seo/',
    category: 'Ana Hizmet',
    icon: 'tabler:search',
    seoTitle: 'Roasist - SEO - Çevrimiçi Varlığınızı Güçlendirin',
    seoDescription: 'Kurumsal SEO ve arama motoru optimizasyonu hizmetleriyle organik trafiğinizi ve satışlarınızı artırın. Teknik SEO, içerik stratejisi ve otorite inşası.',
    h1: 'SEO (Arama Motoru Optimizasyonu)',
    heroQuestion: 'SEO (Search Engine Optimization) ile arama motorlarında organik büyümeye hazır mısınız?',
    aeoDirectAnswer:
      'SEO (Arama Motoru Optimizasyonu), bir web sitesinin Google ve yapay zeka arama motorlarında (ChatGPT, Perplexity, Google AI) hedef anahtar kelimelerde üst sıralarda yer alarak reklamsız, sürdürülebilir ve yüksek dönüşümlü organik trafik kazanmasını sağlayan teknik, içeriksel ve otorite odaklı büyüme disiplinidir.',
    metrics: [
      { value: 'Teknik + İçerik', label: 'Bütünsel SEO Mimarisi', detail: 'Core Web Vitals, Schema.org ve semantik içerik kümeleme' },
      { value: 'Gerçek Veri', label: 'Arama Hacmi Analizi', detail: 'Resmi Google verileriyle ticari niyet (intent) odaklı kelime seçimi' },
      { value: 'SEO + AEO', label: 'Yeni Nesil Görünürlük', detail: 'Hem klasik SERP hem AI arama motorları için yapısal optimizasyon' },
    ],
    overviewHeading: 'SEO Nedir ve Nasıl Yapılır?',
    overviewParagraphs: [
      'Roasist, kalite ve performans odaklı çalışma prensibini gözetir, doğru ölçümleme için gerekli entegrasyonları ve teknolojileri kullanır, detaylı analizler sonucu SEO stratejinizi inşa eder, verilerin ışığında süreçleri daha iyi hale getirir ve anlamlı raporlar ile sürece sizi de dahil eder.',
      'SEO (Search Engine Optimization), online pazarlama dünyasında oldukça önemli bir konudur. Bir web sitesinin arama motorları tarafından daha yüksek sıralarda görünmesi, potansiyel müşteriler tarafından daha kolay bulunması anlamına gelir. Fakat SEO’nun ne olduğunu tam olarak anlamak için bu tanımın ötesine bakmak gerekmektedir.',
      'SEO, bir dizi farklı teknik kullanarak bir web sitesinin arama motoru sonuçlarında üst sıralara çıkmasını sağlayan bir süreçtir. Ana hedefi ise organik arama sonuçlarında daha iyi sıralamalar elde etmektir. Ayrıca SEO stratejileri değişkenlik göstermekle beraber, işletmenin hedeflerine bağlı olarak belirlenir.',
      'SEO çalışmalarının en temel amacı web sitelerinde organik trafiği arttırarak ziyaretçilere ürün ve hizmetlerini sunmaktır. Bu da doğru anahtar kelime seçimi, içerik optimizasyonu, link inşası ve teknik optimizasyon gibi faktörlerin yer aldığı sürekli geliştirilen bir çalışma gerektirmektedir.',
      'İlk olarak, site içi (On-Page) SEO çalışmaları kapsamında anahtar kelime seçimi ve yerleştirme, içerik optimizasyonu, teknik optimizasyon ve yapısal unsur optimizasyonu yer almaktadır. Site dışındaki (Off-Page) SEO çalışmalarını ise sosyal medya bağlantıları, marka bilinirliği ve sektörünüzde saygın web sitelerinden alınan otoriter sinyaller olarak ele alıyoruz.',
    ],
    subFeaturesTitle: 'Kapsamlı SEO Hizmet Bileşenlerimiz',
    subFeaturesSubtitle: 'Site içi teknik mükemmellikten site dışı otorite inşasına kadar tüm sıralama faktörlerini yönetiyoruz.',
    subFeatures: [
      {
        title: 'Teknik SEO & Core Web Vitals',
        description: 'Tarama bütçesi (Crawl Budget), site hızı, mobil uyumluluk, indeksleme hataları, canonical yapısı ve Schema.org (JSON-LD) işaretlemelerini kusursuzlaştırıyoruz.',
        icon: 'tabler:code',
      },
      {
        title: 'Anahtar Kelime & Arama Niyeti Analizi',
        description: 'Sadece yüksek hacimli değil, satın alma niyeti (Commercial & Transactional Intent) yüksek anahtar kelimeleri gerçek verilerle tespit ediyoruz.',
        icon: 'tabler:key',
      },
      {
        title: 'Site İçi (On-Page) & Semantik İçerik',
        description: 'H1-H6 hiyerarşisi, meta etiketler, iç linkleme ağı ve kullanıcı sorularını doğrudan yanıtlayan (AEO uyumlu) otoriter içerik kümeleri oluşturuyoruz.',
        icon: 'tabler:file-text',
      },
      {
        title: 'Site Dışı (Off-Page) SEO & Dijital PR',
        description: 'Marka bilinirliğinizi ve alan adı otoritenizi (Domain Authority) artıran doğal, sektörel ve güvenilir referans sinyalleri inşa ediyoruz.',
        icon: 'tabler:world-www',
      },
      {
        title: 'E-Ticaret & Kategori SEO Yönetimi',
        description: 'Ürün ve kategori sayfalarınızın filtreleme (faceted navigation), stok ve zengin sonuç (Product Schema) optimizasyonlarını yönetiyoruz.',
        icon: 'tabler:shopping-cart',
      },
      {
        title: 'Yerel (Local) & Uluslararası SEO',
        description: 'Google İşletme Profili optimizasyonu ve çok dilli (`hreflang`) mimariyle hem yerel haritalarda hem küresel pazarlarda görünürlük sağlıyoruz.',
        icon: 'tabler:map-pin',
      },
    ],
    processTitle: 'SEO Sürecimiz',
    processSteps: defaultProcessSteps,
    comparisonRows: [
      {
        criteria: 'Anahtar Kelime Seçimi',
        traditional: 'Tahmini ve genel kelimelerle trafik şişirme',
        roasist: 'Satın alma niyeti yüksek, gerçek arama hacimli ticari kelimeler',
      },
      {
        criteria: 'Teknik Altyapı Müdahalesi',
        traditional: 'Sadece yüzeysel eklenti kurulumu',
        roasist: 'Core Web Vitals, JSON-LD Schema, tarama bütçesi ve kod seviyesinde hız optimizasyonu',
      },
      {
        criteria: 'Yapay Zeka Aramaları (AEO)',
        traditional: 'Yalnızca klasik anahtar kelime tekrarı',
        roasist: 'ChatGPT, Perplexity ve Google AI Overviews için doğrudan yanıt mimarisi',
      },
      {
        criteria: 'Raporlama',
        traditional: 'Aylık standart sıralama tablosu',
        roasist: 'Organik trafik, dönüşüm katkısı ve gelir odaklı şeffaf performans raporu',
      },
    ],
    faqs: [
      {
        question: 'SEO nedir ve işletmem için neden önemlidir?',
        answer: 'SEO, “Arama Motoru Optimizasyonu”nun kısaltılmış halidir. Google ve diğer küresel arama motorlarında bir web sitesinin görünürlüğünü ve organik arama sonuçlarını iyileştirmek için kullanılan uzun vadeli bir pazarlama stratejisidir. Artan web sitesi trafiği, nitelikli potansiyel müşteri kazanımı, marka bilinirliği ve reklama bağımlı kalmadan sürdürülebilir satış sağlar.',
      },
      {
        question: 'SEO çalışmalarından ne kadar sürede sonuç alınır?',
        answer: 'SEO çalışması için zaman çerçevesi web sitenizin mevcut teknik durumuna, sektör rekabetine ve içerik derinliğine göre değişebilir. Teknik düzeltmeler ilk haftalarda indekslemeye yansırken, rekabetçi kelimelerde kalıcı ve güçlü organik büyüme sonuçlarının görülmesi ortalama 3 ile 6 ay arasında gerçekleşir.',
      },
      {
        question: 'En sık yapılan SEO hataları nelerdir?',
        answer: 'En yaygın SEO hataları arasında anahtar kelime doldurma (keyword stuffing), kopya veya zayıf içerik kullanımı, bozuk/404 iç linkler, yavaş açılan mobil sayfalar, eksik H1/meta etiketleri ve kalitesiz backlink alımları yer alır. Roasist olarak tüm süreci Google’ın resmi kalite yönergelerine %100 uyumlu yürütüyoruz.',
      },
      {
        question: 'SEO ve Google Ads (SEM) birlikte yürütülmeli mi?',
        answer: 'Kesinlikle evet. Google Ads kampanyalarından elde edilen yüksek dönüşümlü arama terimi verileri SEO içerik stratejisini beslerken, SEO ile güçlenen açılış sayfası kalitesi Google Ads Kalite Puanınızı (Quality Score) artırarak tıklama başı maliyetlerinizi (CPC) düşürür.',
      },
    ],
  },
  {
    slug: 'performans-pazarlamasi',
    permalink: '/hizmetler/performans-pazarlamasi/',
    category: 'Ana Hizmet',
    icon: 'tabler:chart-arrows-vertical',
    seoTitle: 'Roasist - Performans Pazarlaması',
    seoDescription: 'Performans pazarlaması ve veri odaklı reklam yönetimiyle ROAS ve satışlarınızı büyütün. Google Ads, Meta, TikTok, LinkedIn ve Yandex reklam uzmanlığı.',
    h1: 'Performans Pazarlaması',
    heroQuestion: 'Performans Pazarlaması ile işletmeni büyütmeye hazır mısın?',
    aeoDirectAnswer:
      'Performans pazarlaması, dijital reklam bütçelerinin tıklama, form (lead), uygulama indirme veya doğrudan satış (ROAS) gibi tamamen ölçülebilir ticari sonuçlara odaklanarak yönetildiği; Google Ads, Meta, TikTok, LinkedIn ve Yandex kanallarını kapsayan veri odaklı büyüme stratejisidir.',
    metrics: [
      { value: 'ROAS Odaklı', label: 'Yatırım Getirisi Maksimizasyonu', detail: 'Trafiğe değil, gerçek ciroya ve kârlılığa odaklanan teklif yönetimi' },
      { value: '6+ Kanal', label: 'Çok Kanallı (Omnichannel) Mimari', detail: 'Google, Instagram, Facebook, TikTok, LinkedIn ve Yandex entegrasyonu' },
      { value: '%100 Şeffaf', label: 'Kendi Hesabınızda Yönetim', detail: 'Tüm kampanya verileri ve reklam hesapları doğrudan sizin mülkiyetinizde' },
    ],
    overviewHeading: 'Performans Pazarlaması Nedir?',
    overviewParagraphs: [
      'Roasist, her büyüklükteki işletmeye eksiksiz bir çevrimiçi pazarlama hizmetleri yelpazesi sunan bir dijital büyüme ajansıdır. Arama motoru optimizasyonu (SEO), tıklama başına ödeme (PPC) yönetimi, sosyal medya pazarlaması, dönüşüm optimizasyonu ve daha fazlasını içeren kapsamlı çözümler sunuyoruz.',
      'Performans pazarlaması, dijital pazarlama stratejileri arasında belirli hedef kitleleri segmente ederek dönüşüm oranlarını artırmayı amaçlayan en güçlü yöntemdir. Bu yaklaşım ile işletmeler belirledikleri büyüme hedeflerine ulaşarak daha düşük birim maliyetle (CPA) daha fazla müşteri edinirler.',
      'Bu dijital pazarlama yaklaşımının en önemli avantajı sonuçların kuruşu kuruşuna ölçülebilmesidir. Tıklama oranları (CTR), dönüşüm oranları (CR), tıklama başına maliyet (CPC) ve reklam harcaması getirisi (ROAS) gerçek zamanlı olarak takip edilir ve optimize edilir.',
      'Hedef kitlenizi demografik, davranışsal ve niyet sinyallerine göre tanımlayarak reklamlarınızın yalnızca doğru kişiye çıkmasını sağlıyoruz. Böylece soyut trafik artışına değil, doğrudan gerçek satışa ve nitelikli talebe odaklanıyoruz.',
    ],
    subFeaturesTitle: 'Performans Pazarlama Sürecinde Kullandığımız Kanallar',
    subFeaturesSubtitle: 'Hedef kitlenizin bulunduğu tüm dijital temas noktalarında entegre reklam mimarisi kuruyoruz.',
    subFeatures: [
      {
        title: 'Google Ads (Arama, Alışveriş, PMax, YouTube)',
        description: 'Google arama sonuçlarında (SERP), Alışveriş sekmesinde, YouTube ve GDN ağında satın alma niyeti en yüksek kullanıcılara tam aradıkları anda ulaşın.',
        icon: 'tabler:brand-google',
      },
      {
        title: 'Instagram & Facebook (Meta Ads)',
        description: 'Gelişmiş kitle segmentasyonu, katalog reklamları (DPA), Reels/Story kreatifleri ve Conversions API kurulumuyla sosyal medyada ölçeklenebilir satış yakalayın.',
        icon: 'tabler:brand-meta',
      },
      {
        title: 'TikTok Ads',
        description: 'Kısa video dinamiklerine uygun dikkat çekici kreatifler ve Spark Ads modelleriyle markanızı milyonlarca aktif kullanıcıyla buluşturun.',
        icon: 'tabler:brand-tiktok',
      },
      {
        title: 'LinkedIn B2B Reklamları',
        description: 'Şirket büyüklüğü, sektör ve iş unvanına (CEO, Satın Alma Müdürü vb.) göre nokta atışı hedefleme yaparak kurumsal B2B potansiyel müşteriler kazanın.',
        icon: 'tabler:brand-linkedin',
      },
      {
        title: 'Yandex Ads',
        description: 'Rusya, BDT ülkeleri ve uluslararası pazarlarda hedef kitlenize Yandex Arama ve Reklam Ağı (YAN) üzerinden doğrudan erişin.',
        icon: 'tabler:world',
      },
      {
        title: 'Programatik & Yeniden Pazarlama (Retargeting)',
        description: 'Sitenizi ziyaret edip henüz satın almayan kullanıcıları çok kanallı dinamik yeniden pazarlama kurgularıyla müşteriye dönüştürün.',
        icon: 'tabler:refresh-dot',
      },
    ],
    processTitle: 'Performans Pazarlama Sürecimiz',
    processSteps: defaultProcessSteps,
    comparisonRows: [
      {
        criteria: 'Kampanya Hedefi',
        traditional: 'Sadece gösterim ve ucuz tıklama odaklı yönetim',
        roasist: 'Ciro, ROAS, nitelikli lead (MQL/SQL) ve kârlılık odaklı yönetim',
      },
      {
        criteria: 'Dönüşüm Takibi',
        traditional: 'Temel sayfa görüntüleme pikseli',
        roasist: 'GTM, GA4, Enhanced Conversions ve Sunucu Taraflı (CAPI) tam huni ölçümleme',
      },
      {
        criteria: 'Bütçe Yönetimi',
        traditional: 'Sabit bırakılan kampanya bütçeleri',
        roasist: 'Verimli kanallara ve saat/lokasyon kırılımlarına dinamik bütçe aktarımı',
      },
      {
        criteria: 'Kreatif & A/B Testi',
        traditional: 'Tek görselle aylarca devam eden reklamlar',
        roasist: 'Sürekli kreatif varyasyon, kanca (hook) ve açılış sayfası A/B testleri',
      },
    ],
    faqs: [
      {
        question: 'Performans pazarlaması diğer pazarlama yöntemlerinden nasıl ayrılır?',
        answer: 'Performans pazarlama, reklam harcamalarının ölçülebilir ticari sonuçlar (satış, form, randevu, indirme) elde etmek amacıyla optimize edildiği veri odaklı bir stratejidir. Geleneksel pazarlama yalnızca görünürlük hedeflerken, performans pazarlamasında yatırdığınız her 1 TL’nin ne kadar geri dönüş (ROAS/ROI) ürettiğini net olarak görürsünüz.',
      },
      {
        question: 'Performans pazarlamada hangi metrikler takip edilir?',
        answer: 'Başlıca takip ettiğimiz metrikler arasında Reklam Harcaması Getirisi (ROAS), Yatırım Getirisi (ROI), Edinme Başına Maliyet (CPA/CPL), Dönüşüm Oranı (CR), Tıklama Oranı (CTR), Tıklama Başına Maliyet (CPC) ve Müşteri Yaşam Boyu Değeri (LTV) yer alır.',
      },
      {
        question: 'Reklam hesaplarımızın mülkiyeti kimde oluyor?',
        answer: 'Tüm reklam hesaplarınız (Google Ads, Meta Business, TikTok, LinkedIn, Yandex) %100 sizin mülkiyetinizde kalır. Roasist, resmi yönetici (MCC / Business Partner) hesabımız üzerinden yetki alarak kampanyalarınızı şeffaf biçimde sizin adınıza yönetir.',
      },
      {
        question: 'Minimum ne kadar reklam bütçesiyle başlamalıyız?',
        answer: 'Optimum reklam bütçesi sektörünüzdeki tıklama maliyetlerine, hedeflediğiniz coğrafyaya ve büyüme hedeflerinize göre belirlenir. Ön analiz görüşmemizde sektörünüzün gerçek arama hacimlerini ve rekabet verilerini inceleyerek size en verimli başlangıç bütçesini çıkarıyoruz.',
      },
    ],
  },
  {
    slug: '360-derece-dijital-pazarlama-yonetimi',
    permalink: '/hizmetler/360-derece-dijital-pazarlama-yonetimi/',
    category: 'Ana Hizmet',
    icon: 'tabler:360-view',
    seoTitle: 'Roasist - 360° Dijital Pazarlama Yönetimi',
    seoDescription: '360 derece dijital pazarlama yönetimi ile markanızın SEO, performans reklamları, sosyal medya, web ve kreatif süreçlerini tek merkezden büyütün.',
    h1: '360° Dijital Pazarlama Yönetimi',
    heroQuestion: '360° dijital pazarlama yönetimi ile işletmenizi büyütmeye hazır mısınız?',
    aeoDirectAnswer:
      '360° dijital pazarlama yönetimi; bir markanın arama motoru optimizasyonu (SEO), performans reklamları (PPC), sosyal medya yönetimi, kreatif tasarım, web deneyimi ve veri analitiği süreçlerinin birbiriyle tam entegre, tek bir büyüme stratejisi altında uçtan uca planlanması, yürütülmesi ve ölçülmesidir.',
    metrics: [
      { value: '360° Entegre', label: 'Tek Merkezden Büyüme', detail: 'SEO, PPC, Kreatif, Web ve Analitik ekiplerinin tam uyumu' },
      { value: 'Tam Huni', label: 'Farkındalıktan Sadakate', detail: 'Marka bilinirliği, müşteri kazanımı ve yeniden pazarlama kurgusu' },
      { value: 'Veri Odaklı', label: 'Birleşik Raporlama', detail: 'Tüm dijital kanalların birbirine olan katkısını (Attribution) ölçümleme' },
    ],
    overviewHeading: '360° Dijital Pazarlama Yönetimi Nedir?',
    overviewParagraphs: [
      'Roasist, her büyüklükteki işletmeye eksiksiz bir çevrimiçi pazarlama hizmetleri yelpazesi sunan bir dijital pazarlama ajansıdır. Arama motoru optimizasyonu (SEO), tıklama başına ödeme (PPC) yönetimi, sosyal medya pazarlaması, kreatif tasarım ve dönüşüm optimizasyonunu içeren tüm dijital pazarlama ihtiyaçlarınız için tek durak noktasıyız.',
      '360 derece dijital pazarlama yönetimi, markaların çevrimiçi varlıklarını etkili bir şekilde yönetmelerini sağlayan stratejik bir yaklaşımdır. Bu yönetim biçimi, markaların dijital pazarlama faaliyetlerini tüm yönleriyle kapsar ve bütünsel bir yaklaşımı temsil eder.',
      'Markaların çevrimiçi varlıklarını optimize etmek, hedef kitlelerine ulaşmak ve dönüşümleri artırmak için web siteleri, sosyal medya pazarlama (SMM), arama motoru optimizasyonu (SEO), arama motoru pazarlaması (SEM), e-posta pazarlama ve içerik pazarlama kanallarını entegre biçimde kullanıyoruz.',
      'Veri analitiği ve ölçümleme sayesinde kampanya performansını gerçek zamanlı takip ediyor, kullanıcı davranışlarını analiz ediyor ve pazarlama bütçenizi en yüksek getiri sağlayan kanallara yönlendiriyoruz.',
    ],
    subFeaturesTitle: '360° Dijital Pazarlama Yönetiminin Avantajları',
    subFeaturesSubtitle: 'Parçalı ajans yönetimi yerine tüm dijital kanallarınızın tek bir hedef doğrultusunda konuşmasını sağlıyoruz.',
    subFeatures: [
      {
        title: 'Bütünsel Marka İletişimi',
        description: 'Google reklamlarınızdan Instagram kreatiflerinize, web sitenizden SEO içeriklerinize kadar tüm kanallarda tutarlı ve güven veren bir marka dili kuruyoruz.',
        icon: 'tabler:affiliate',
      },
      {
        title: 'Kanallar Arası Sinerji & Attribution',
        description: 'Sosyal medya reklamlarıyla başlayan farkındalığı Google Arama ve SEO ile yakalıyor, yeniden pazarlama ile satışa dönüştürüyoruz.',
        icon: 'tabler:arrows-join-2',
      },
      {
        title: 'Dönüşüm Oranı Optimizasyonu (CRO)',
        description: 'Sadece reklamdan trafik çekmekle kalmıyor; web sitenizin açılış sayfalarını, formlarını ve satın alma adımlarını iyileştirerek dönüşüm oranınızı artırıyoruz.',
        icon: 'tabler:trending-up',
      },
      {
        title: 'Kreatif & Tasarım Desteği',
        description: 'Kampanyalarınızın ihtiyaç duyduğu yüksek dönüşümlü reklam görsellerini, sosyal medya tasarımlarını ve kurumsal materyalleri içeride üretiyoruz.',
        icon: 'tabler:palette',
      },
      {
        title: 'Zaman ve Maliyet Tasarrufu',
        description: 'Farklı ajansları ve freelancer’ları koordine etme yükünü ortadan kaldırıyor, şirketinizin dışarıdaki tam teşekküllü büyüme departmanı gibi çalışıyoruz.',
        icon: 'tabler:clock-check',
      },
      {
        title: 'Gerçek Zamanlı Veri Analitiği',
        description: 'GA4, GTM, Looker Studio ve Roasist Marketing Intelligence OS ile tüm kanallarınızın performansını tek ekranda şeffaf biçimde raporluyoruz.',
        icon: 'tabler:device-analytics',
      },
    ],
    processTitle: '360° Hizmet Sürecimiz',
    processSteps: defaultProcessSteps,
    comparisonRows: [
      {
        criteria: 'Kanal Yönetimi',
        traditional: 'Birbirinden kopuk SEO, reklam ve tasarım süreçleri',
        roasist: 'Tek strateji altında birbirini besleyen tam entegre büyüme ekosistemi',
      },
      {
        criteria: 'Sorumluluk & Koordinasyon',
        traditional: 'Farklı ekipler arasında zaman kaybı ve kopukluk',
        roasist: 'Tek muhatap, uçtan uca sorumluluk ve hızlı aksiyon',
      },
      {
        criteria: 'Bütçe Dağılımı',
        traditional: 'Kanal bazlı sabit harcama',
        roasist: 'Performansa göre kanallar arası esnek ve kârlı bütçe optimizasyonu',
      },
    ],
    faqs: [
      {
        question: '360° dijital pazarlama yönetimi neleri kapsar?',
        answer: '360° dijital pazarlama yönetimi; stratejik planlama, Performans Pazarlaması (Google, Meta, TikTok, LinkedIn, Yandex reklamları), Arama Motoru Optimizasyonu (SEO), Web Sitesi & Açılış Sayfası (Landing Page) Tasarımı, Kreatif Grafik Tasarım, Dönüşüm Optimizasyonu (CRO) ve Veri Analitiği/Raporlama süreçlerinin tamamını kapsar.',
      },
      {
        question: '360° dijital pazarlama yönetiminin işletmeme en büyük faydası nedir?',
        answer: 'En büyük faydası, pazarlama kanallarınızın birbirinden kopuk çalışmasını önleyerek bütçe israfını bitirmesidir. Geliştirilmiş marka bilinirliği, artan potansiyel müşteriler ve satışlar, daha yüksek müşteri tutma oranları (retention) ve yönetim süreçlerinde ciddi zaman tasarrufu sağlar.',
      },
      {
        question: 'Hizmet kapsamını işletmemizin ihtiyaçlarına göre özelleştirebiliyor muyuz?',
        answer: 'Evet. Her işletmenin bulunduğu büyüme aşaması farklıdır. İlk analiz toplantımızda öncelikli ihtiyaçlarınızı belirleyerek size özel modüler ve ölçeklenebilir bir 360° büyüme paketi oluşturuyoruz.',
      },
    ],
  },
  {
    slug: 'web-tasarim',
    permalink: '/hizmetler/web-tasarim/',
    category: 'Ana Hizmet',
    icon: 'tabler:layout-dashboard',
    seoTitle: 'Roasist - Web Tasarım - Çevrimiçi Varlığınızı Güçlendirin',
    seoDescription: 'Kullanıcı deneyimi (UI/UX) yüksek, mobil ve SEO uyumlu, ultra hızlı kurumsal web tasarım hizmetleri. Dönüşüm odaklı modern web siteleri inşa ediyoruz.',
    h1: 'Web Tasarım',
    heroQuestion: 'Kullanıcı deneyimi yüksek, mobil uyumlu web sitesine mi ihtiyacınız var?',
    aeoDirectAnswer:
      'Profesyonel web tasarım; markanızın dijital vitrinini kullanıcı deneyimi (UI/UX), mobil öncelikli (responsive) mimari, yüksek açılış hızı (Core Web Vitals) ve arama motoru optimizasyonu (SEO) standartlarıyla birleştirerek ziyaretçileri müşteriye dönüştüren stratejik tasarım ve yazılım sürecidir.',
    metrics: [
      { value: '100/100', label: 'Hız & Performans Odaklı', detail: 'Core Web Vitals ve Google PageSpeed standartlarında temiz mimari' },
      { value: '%100 Mobil', label: 'Responsive Deneyim', detail: 'Telefon, tablet ve masaüstünde kusursuz çalışan akıcı arayüzler' },
      { value: 'SEO + CRO', label: 'Dönüşüm Odaklı Yapı', detail: 'Ziyaretçiyi harekete geçiren bilgi mimarisi ve teknik SEO uyumu' },
    ],
    overviewHeading: 'Web Tasarımı Nedir ve Neden Kritik Öneme Sahiptir?',
    overviewParagraphs: [
      'Web site tasarım hizmetimiz, sektörde uzun yıllara dayanan deneyime sahip uzmanlarımız tarafından yönetilmektedir. Yalnızca görsel olarak çarpıcı değil, aynı zamanda kullanıcı dostu, hızlı ve duyarlı (responsive) bir web sitesi oluşturmak için sizinle birlikte çalışıyoruz. Ayrıca daha fazla organik ziyaretçi çekebilmeniz için web sitenizin arama motorları için baştan sona optimize edildiğinden emin oluyoruz.',
      'Web tasarımı; kullanımı kolay, görsel olarak çekici ve bilgilendirici bir web sitesi oluşturmayı içerir. Düzen, renk şeması, tipografi ve bilgi hiyerarşisi dahil olmak üzere her detay, ziyaretçinin markanıza güven duymasını ve kolayca aksiyon almasını sağlayacak şekilde kurgulanır.',
      'İyi tasarlanmış bir web sitesi, hem organik SEO sıralamalarınızı yükseltir hem de Google/Meta reklamlarından gelen ziyaretçilerin müşteriye dönüşme oranını (Conversion Rate) doğrudan artırarak reklam maliyetlerinizi düşürür.',
    ],
    subFeaturesTitle: 'Web Tasarım Yaklaşımlarımız ve Çözüm Türlerimiz',
    subFeaturesSubtitle: 'Markanızın kimliğine ve ticari hedeflerine en uygun modern web tasarım standartlarını uyguluyoruz.',
    subFeatures: [
      {
        title: 'Reaktif & Mobil Öncelikli Tasarım (Responsive)',
        description: 'Web sitenizin telefon, tablet ve masaüstü dahil tüm ekran boyutlarında kusursuz, hızlı ve kaymasız görüntülenmesini sağlıyoruz.',
        icon: 'tabler:devices',
      },
      {
        title: 'Minimalist & Düz Tasarım (Flat / Modern UI)',
        description: 'Gereksiz karmaşadan arınmış, tipografisi güçlü, ferah boşluk kullanımıyla kullanıcının doğrudan mesajınıza ve CTA butonlarına odaklandığı arayüzler.',
        icon: 'tabler:sparkles',
      },
      {
        title: 'Gezinti ve Dönüşüm Odaklı Mimari (UX/CRO)',
        description: 'Ziyaretçilerin aradıkları hizmet veya ürüne en fazla 2 tıklamayla ulaşabildiği, sürtünmesiz ve yüksek dönüşümlü bilgi mimarisi.',
        icon: 'tabler:compass',
      },
      {
        title: 'SEO ve Yapay Zeka (AEO) Uyumlu Kodlama',
        description: 'Semantik HTML5, doğru H1-H6 hiyerarşisi, otomatik XML Sitemap, Schema.org yapısal verileri ve şimşek hızında açılış süreleri.',
        icon: 'tabler:seo',
      },
      {
        title: 'Reklam Açılış Sayfaları (Landing Page)',
        description: 'Google Ads ve sosyal medya kampanyalarınız için Kalite Puanını (Quality Score) ve form/satış dönüşümlerini katlayan özel açılış sayfaları.',
        icon: 'tabler:rocket',
      },
      {
        title: 'Etkileşimli & Dinamik Deneyim',
        description: 'Mikro animasyonlar, derinlik katmanları ve modern görsel bileşenlerle markanızın teknoloji ve kalite algısını zirveye taşıyan tasarım dili.',
        icon: 'tabler:layers-intersect',
      },
    ],
    processTitle: 'Web Tasarım Hizmet Sürecimiz',
    processSteps: defaultProcessSteps,
    comparisonRows: [
      {
        criteria: 'Sayfa Açılış Hızı',
        traditional: 'Ağır hazır şablonlar ve eklenti şişkinliği (2-5 saniye)',
        roasist: 'Optimize edilmiş modern mimari ile anında açılış (<0.3 saniye)',
      },
      {
        criteria: 'SEO Altyapısı',
        traditional: 'Sonradan eklentiyle yamalanmaya çalışılan yapı',
        roasist: 'Kod seviyesinde yerleşik semantik HTML, Schema ve Core Web Vitals uyumu',
      },
      {
        criteria: 'Dönüşüm Odaklılık',
        traditional: 'Sadece görsel broşür mantığı',
        roasist: 'Performans pazarlaması ve müşteri kazanımı (CRO) odaklı UX kurgusu',
      },
    ],
    faqs: [
      {
        question: 'Web tasarımı işletmemin satışlarını nasıl etkiler?',
        answer: 'Web siteniz tüm dijital pazarlama çalışmalarınızın kalbidir. Yavaş açılan, mobilde bozulan veya güven vermeyen bir siteye ne kadar reklam bütçesi harcarsanız harcayın ziyaretçiler sayfayı terk eder. İyi tasarlanmış, hızlı ve kullanıcı dostu bir web sitesi mevcut trafiğinizden elde ettiğiniz satış ve form sayısını doğrudan artırır.',
      },
      {
        question: 'En yaygın web sitesi tasarım hataları nelerdir?',
        answer: 'Çok fazla ve okunması güç metin yığınları kullanmak, optimize edilmemiş ağır görsellerle siteyi yavaşlatmak, karmaşık menü yapısıyla ziyaretçiyi kaybettirmek, mobil deneyimi ikinci plana atmak ve net harekete geçirici mesajlar (CTA) kullanmamak en sık yapılan hatalardır.',
      },
      {
        question: 'Yeni yapılan web sitem SEO ve mobil uyumlu olacak mı?',
        answer: 'Evet. Roasist tarafından geliştirilen tüm web siteleri %100 mobil öncelikli (Mobile-First), teknik SEO standartlarına tam uyumlu, SSL güvenlik sertifikalı ve Google PageSpeed kriterlerine göre optimize edilmiş olarak teslim edilir.',
      },
      {
        question: 'Mevcut web sitemi yenilerken Google’daki SEO sıralamalarım kaybolur mu?',
        answer: 'Hayır. Mevcut URL yapınızı, meta verilerinizi, başlık hiyerarşinizi ve 301 yönlendirme haritanızı birebir koruyarak yenileme yapıyoruz. Böylece hiçbir SEO kaybı yaşamadan, artan hız ve kullanıcı deneyimi sayesinde sıralamalarınızda yükseliş elde edersiniz.',
      },
    ],
  },
  {
    slug: 'grafik-tasarim',
    permalink: '/hizmetler/grafik-tasarim/',
    category: 'Ana Hizmet',
    icon: 'tabler:palette',
    seoTitle: 'Roasist - Grafik Tasarım - Görsel Kimliğinizi Güçlendirin',
    seoDescription: 'Reklam kampanyalarınızı ve markanızı öne çıkaracak profesyonel grafik tasarım hizmetleri. Kurumsal kimlik, sosyal medya ve performans reklam kreatifleri.',
    h1: 'Grafik Tasarım',
    heroQuestion: 'Yaratıcı ve ilgi çekici tasarımları keşfetmeye hazır mısınız?',
    aeoDirectAnswer:
      'Grafik tasarım; tipografi, renk psikolojisi, kompozisyon ve görsel hikaye anlatımı yoluyla markanızın değer önerisini hedef kitlenize saniyeler içinde aktaran, kurumsal kimlikten yüksek dönüşümlü reklam kreatiflerine kadar tüm görsel iletişimi kapsayan stratejik tasarım disiplinidir.',
    metrics: [
      { value: 'Yüksek CTR', label: 'Performans Kreatifleri', detail: 'Kaydırmayı durduran (scroll-stopping) reklam görselleri' },
      { value: 'Kurumsal Dil', label: 'Marka Tutarlılığı', detail: 'Tüm dijital kanallarda bütünlüklü görsel kimlik' },
      { value: 'Hızlı Üretim', label: 'A/B Test Varyasyonları', detail: 'Kampanya optimizasyonu için çevik kreatif üretimi' },
    ],
    overviewHeading: 'Grafik Tasarım Nedir ve Neden Önemlidir?',
    overviewParagraphs: [
      'Reklam kampanyalarınızı öne çıkaracak tasarımlar mı arıyorsunuz? Dikkat çekecek ve kalıcı bir izlenim bırakacak özel tasarımlar yaratma konusunda uzmanız.',
      'Grafik tasarım; yazı, alan ve görüntü kullanımı yoluyla iletişim, stil oluşturma ve problem çözme sanatıdır. İyi bir grafik tasarımın yaratıcı, görsel olarak çekici ve istenilen mesajı iletmede etkili olması gerekir. Tasarım ekibimiz, iletişim hedeflerinize görsel çözümler üretmek için estetik ve pazarlama psikolojisini birleştirir.',
      'Kurumsal kimlik, marka bilinci oluşturma, sosyal medya iletişimi, dijital reklam kreatifleri ve web arayüz tasarımı başta olmak üzere markanızın ihtiyaç duyduğu tüm görsel dünyayı kurguluyoruz.',
      'Doğru yapılandırılmış bir görsel tasarım dili, hem markanızın güvenilirliğini hem de reklam kampanyalarınızın tıklama (CTR) ve dönüşüm oranlarını doğrudan artırır.',
    ],
    subFeaturesTitle: 'Grafik Tasarım Hizmet Alanlarımız',
    subFeaturesSubtitle: 'Estetiği performans pazarlaması verileriyle birleştiren sonuç odaklı tasarımlar üretiyoruz.',
    subFeatures: [
      {
        title: 'Performans Reklam Kreatifleri (Meta, TikTok, GDN)',
        description: 'Sosyal medya ve görüntülü reklam ağlarında kullanıcıların dikkatini ilk 2 saniyede yakalayan, tıklama oranı (CTR) yüksek reklam tasarımları.',
        icon: 'tabler:ad-2',
      },
      {
        title: 'Sosyal Medya Görsel Yönetimi',
        description: 'Instagram, LinkedIn ve diğer platformlarda markanızın prestijini yansıtan post, carousel, hikaye (story) ve kapak tasarımları.',
        icon: 'tabler:brand-instagram',
      },
      {
        title: 'Kurumsal Kimlik & Marka Tasarımı',
        description: 'Logo tasarımı, renk paleti, tipografi rehberi ve kurumsal dökümanlarla markanıza akılda kalıcı ve güçlü bir kimlik kazandırıyoruz.',
        icon: 'tabler:award',
      },
      {
        title: 'E-Ticaret & Ürün Görsel Tasarımları',
        description: 'Ürünlerinizin özelliklerini ve faydalarını net biçimde vurgulayan katalog, banner ve pazaryeri görsel tasarımları.',
        icon: 'tabler:shopping-bag',
      },
      {
        title: 'Web & UI Görsel Bileşenleri',
        description: 'Web siteniz ve açılış sayfalarınız için özel ikon setleri, infografikler ve dönüşüm artırıcı görsel bloklar.',
        icon: 'tabler:vector-bezier',
      },
      {
        title: 'Kreatif A/B Test Varyasyonları',
        description: 'Performans kampanyalarında hangi görsel mesajın daha çok sattığını bulmak için farklı kanca (hook) ve tasarım varyasyonları.',
        icon: 'tabler:arrows-split-2',
      },
    ],
    processTitle: 'Grafik Tasarım Sürecimiz',
    processSteps: defaultProcessSteps,
    comparisonRows: [
      {
        criteria: 'Tasarım Amacı',
        traditional: 'Sadece göze hoş görünen ama mesajı belirsiz görseller',
        roasist: 'Marka prestijini korurken tıklama ve satış (CTR & ROAS) getiren stratejik tasarım',
      },
      {
        criteria: 'Platform Uyumu',
        traditional: 'Tek boyutta hazırlanan standart görsel',
        roasist: 'Feed, Story, Reels ve GDN formatlarına tam uyarlanmış çoklu teslimat',
      },
    ],
    faqs: [
      {
        question: 'Grafik tasarım reklam kampanyalarımın başarısını nasıl etkiler?',
        answer: 'Dijital reklamlarda (özellikle Instagram, Facebook, TikTok ve Google Görüntülü Reklam Ağı) başarının %60’ından fazlası kreatif kalitesine bağlıdır. Doğru görsel hiyerarşi ve güçlü bir mesajla tasarlanan kreatifler tıklama oranınızı (CTR) yükseltir, tıklama başı maliyetinizi (CPC) düşürür.',
      },
      {
        question: 'Hangi tasarım araçları ve standartlarıyla çalışıyorsunuz?',
        answer: 'Tasarım ekibimiz Adobe Photoshop, Adobe Illustrator, InDesign ve Figma gibi endüstri standardı profesyonel yazılımları kullanarak markanıza özel, özgün ve yüksek çözünürlüklü çalışmalar üretir.',
      },
      {
        question: 'Mevcut kurumsal kimliğimize sadık kalarak mı tasarım yapıyorsunuz?',
        answer: 'Evet. Markanızın mevcut kurumsal kimlik rehberine (renk, font, tonlama) tam uyum sağlıyoruz. Eğer henüz bir kurumsal kimlik rehberiniz yoksa, markanız için sıfırdan modern bir görsel standart oluşturuyoruz.',
      },
    ],
  },
  {
    slug: 'performans-pazarlamasi/google-reklamlari',
    permalink: '/hizmetler/performans-pazarlamasi/google-reklamlari/',
    category: 'Performans Kanalı',
    icon: 'tabler:brand-google',
    seoTitle: 'Roasist - Google Reklamları',
    seoDescription: 'Veriye dayalı ve performans odaklı Google Reklamları (Google Ads) yönetimi. Arama Ağı, Alışveriş, Performance Max ve YouTube reklamlarıyla satışlarınızı artırın.',
    h1: 'Google Reklamları',
    heroQuestion: 'Veriye dayalı ve performans odaklı Google reklamları ile tanışmaya hazır mısınız?',
    aeoDirectAnswer:
      'Google Reklamları (Google Ads); ürün veya hizmetinizi Google’da aktif olarak arayan potansiyel müşterilere Arama Ağı, Alışveriş (Shopping), Performance Max, YouTube ve Görüntülü Reklam Ağı (GDN) üzerinden tam satın alma anında ulaşmanızı sağlayan, tıklama ve dönüşüm odaklı en güçlü dijital reklam platformudur.',
    metrics: [
      { value: 'Yüksek Niyet', label: 'Tam Arandığı Anda Görünürlük', detail: 'Ürün veya hizmetinizi aktif arayan kullanıcılara anında erişim' },
      { value: '6 Kampanya Tipi', label: 'Tam Kapsamlı Google Ads', detail: 'Arama, Alışveriş, PMax, GDN, YouTube ve Uygulama reklamları' },
      { value: 'Düşük CPA', label: 'Akıllı Teklif & Negatif Kelime', detail: 'Bütçe israfını sıfırlayan sürekli arama terimi optimizasyonu' },
    ],
    overviewHeading: 'İşletmeler için Google Reklamlarının Önemi Nedir?',
    overviewParagraphs: [
      'Roasist, kalite ve performans odaklı çalışma prensibini gözetir, doğru ölçümleme için gerekli entegrasyonları ve teknolojileri kullanır, detaylı analizler sonucu reklam stratejinizi inşa eder, verilerin ışığında kampanya süreçlerini daha iyi hale getirir ve anlamlı raporlar ile sürece sizi de dahil eder.',
      'Google, dünyanın lider arama motorudur. Dünyadaki arama motoru pazarının büyük çoğunluğu Google tarafından domine edilmiştir ve saniyede milyarlarca arama gerçekleşmektedir. Dünyadaki her 10 kişiden 7’si bir bilgiye, ürüne veya hizmete ulaşmak için Google arama motorunu kullanır.',
      'Google reklamları; Google ürünlerini ve Google iş ortağı web sitelerini kullanan ziyaretçileri sitenize çekerek size bu ziyaretçileri satışa, potansiyel müşterilere ve kayıtlara dönüştürme fırsatı sunar.',
      'Aylık reklam bütçenizi, reklamlarınızın gösterime gireceği lokasyonları, gösterim sıklığını, hangi gün ve saatlerde gösterileceğini ve hedef ROAS/CPA hedeflerinizi veriye dayalı olarak optimize ediyoruz.',
    ],
    subFeaturesTitle: 'Google Reklamlarında Yönettiğimiz Kampanya Türleri',
    subFeaturesSubtitle: 'Sektörünüze ve satış huninize en uygun Google Ads kampanya mimarisini kuruyoruz.',
    subFeatures: [
      {
        title: 'Arama Ağı (Search) Kampanyaları',
        description: 'Google arama sonuçları sayfalarında (SERP) ürün veya hizmetinizle ilgili anahtar kelimelerle yapılan aramalarda en üst sırada yer alın.',
        icon: 'tabler:search',
      },
      {
        title: 'Alışveriş (Shopping) & Performance Max',
        description: 'E-ticaret siteleri için ürün fotoğrafı, fiyat ve mağaza adını doğrudan arama sonuçlarında göstererek satın alma niyeti yüksek müşterileri yakalayın.',
        icon: 'tabler:shopping-cart-bolt',
      },
      {
        title: 'Görüntülü Reklam Ağı (GDN) Kampanyaları',
        description: 'Milyonlarca haber sitesi, blog ve mobil uygulamada görsel banner reklamlarınızla marka farkındalığı ve yeniden pazarlama (remarketing) yapın.',
        icon: 'tabler:photo',
      },
      {
        title: 'YouTube Video Kampanyaları',
        description: 'YouTube videolarının başında ve akışında demografik, ilgi alanı ve arama geçmişine göre hedeflenmiş etkileyici video reklamlar yayınlayın.',
        icon: 'tabler:brand-youtube',
      },
      {
        title: 'Mobil Uygulama Kampanyaları',
        description: 'Google Arama, Google Play, YouTube ve GDN üzerinde uygulamanızın indirme (install) ve uygulama içi satın alma sayılarını ölçekleyin.',
        icon: 'tabler:device-mobile',
      },
      {
        title: 'Yerel (Local) & Harita Kampanyaları',
        description: 'Fiziksel mağaza, klinik veya ofisinize yakın konumdaki kullanıcıları Google Arama ve Google Haritalar üzerinden işletmenize yönlendirin.',
        icon: 'tabler:map-pin-filled',
      },
    ],
    processTitle: 'Google Reklamları Hizmet Sürecimiz',
    processSteps: defaultProcessSteps,
    comparisonRows: [
      {
        criteria: 'Anahtar Kelime & Eşleme',
        traditional: 'Geniş eşleme ile alakasız aramalara bütçe harcanması',
        roasist: 'Tam/Sıralı eşleme stratejisi ve günlük negatif anahtar kelime temizliği',
      },
      {
        criteria: 'Kalite Puanı (Quality Score)',
        traditional: 'Düşük alaka düzeyi nedeniyle yüksek tıklama maliyeti (CPC)',
        roasist: 'Reklam metni, anahtar kelime ve açılış sayfası uyumuyla düşük CPC & yüksek sıralama',
      },
    ],
    faqs: [
      {
        question: 'Google Ads reklamları ne kadar sürede sonuç verir?',
        answer: 'Google Ads kampanyaları onaylandığı andan itibaren hedef anahtar kelimelerinizde gösterim ve tıklama almaya başlar. İlk günden itibaren trafik ve dönüşüm akışı başlar; akıllı teklif algoritmalarının verilerle olgunlaşmasıyla birlikte her geçen hafta birim dönüşüm maliyetleriniz daha da optimize olur.',
      },
      {
        question: 'Google Ads hesabımı kendim görebilecek miyim?',
        answer: 'Evet. Reklam hesabınızı 7/24 görebilir, harcanan bütçeyi ve tüm performans göstergelerini şeffaf şekilde takip edebilirsiniz. Roasist, sizin Google Ads hesabınız üzerinden yönetici erişimi alarak kampanyalarınızı sizin adınıza yönetir.',
      },
      {
        question: 'Alakasız tıklamalara bütçe gitmesini nasıl engelliyorsunuz?',
        answer: 'Kampanya kurulum aşamasında kapsamlı bir negatif anahtar kelime listesi ekliyor, kampanya süresince Arama Terimleri (Search Terms) raporunu düzenli denetleyerek ticari niyeti olmayan sorguları anında engelliyoruz.',
      },
    ],
  },
  {
    slug: 'performans-pazarlamasi/instagram-reklamlari',
    permalink: '/hizmetler/performans-pazarlamasi/instagram-reklamlari/',
    category: 'Performans Kanalı',
    icon: 'tabler:brand-instagram',
    seoTitle: 'Instagram Reklamları - Roasist',
    seoDescription: 'Veriye dayalı ve performans odaklı Instagram reklamları yönetimi. Reels, Story, Akış ve Katalog reklamlarıyla hedef kitlenize ulaşın ve satışlarınızı artırın.',
    h1: 'Instagram Reklamları',
    heroQuestion: 'Veriye dayalı ve performans odaklı Instagram reklamları ile tanışmaya hazır mısınız?',
    aeoDirectAnswer:
      'Instagram Reklamları; Türkiye’de 52 milyondan fazla, dünyada ise 2 milyarı aşkın aktif kullanıcıya sahip Instagram platformunda Reels, Hikayeler (Stories), Akış ve Keşfet alanlarında gelişmiş demografik ve davranışsal hedeflemeyle satış, form ve marka bilinirliği sağlayan performans reklam modelidir.',
    metrics: [
      { value: '52M+ TR', label: 'Aktif Kullanıcı Erişimi', detail: 'Türkiye’nin en yüksek etkileşimli görsel ve video platformu' },
      { value: 'Reels & Story', label: 'Yüksek Dönüşümlü Formatlar', detail: 'Tam ekran dikey video ve dinamik ürün katalog reklamları' },
      { value: 'Meta CAPI', label: 'Gelişmiş Dönüşüm Takibi', detail: 'Pixel + Conversions API ile veri kayıpsız optimizasyon' },
    ],
    overviewHeading: 'Instagram Reklamları İşletmeler İçin Neden Önemli?',
    overviewParagraphs: [
      'Roasist, kalite ve performans odaklı çalışma prensibini gözetir, doğru ölçümleme için gerekli entegrasyonları ve teknolojileri kullanır, detaylı analizler sonucu reklam stratejinizi inşa eder, verilerin ışığında kampanya süreçlerini daha iyi hale getirir ve anlamlı raporlar ile sürece sizi de dahil eder.',
      'Instagram, Türkiye’de 52 milyon aktif kullanıcıya, dünya genelinde ise 2 milyardan fazla aktif kullanıcıya sahip olan lider bir sosyal medya platformudur. Bu muazzam erişim gücü, işletmelerin potansiyel müşterilere görsel ve işitsel olarak en etkileyici biçimde ulaşmasını sağlar.',
      'Instagram reklamları; belirli demografik özelliklere, ilgi alanlarına ve satın alma davranışlarına sahip kullanıcıları hedeflemek için gelişmiş segmentasyon araçları sunar. Bu sayede reklam bütçenizin doğru kişiye ulaştığından emin olur ve kampanyalarınızın yatırım getirisini (ROAS) artırırsınız.',
    ],
    subFeaturesTitle: 'Instagram Reklamlarının Avantajları Nelerdir?',
    subFeaturesSubtitle: 'Görsel etkileşimi doğrudan ticari sonuca ve satışa dönüştüren kampanya kurguları.',
    subFeatures: [
      {
        title: 'Geniş ve Etkileşimli Kitleye Ulaşım',
        description: 'Milyonlarca aktif kullanıcının her gün saatler geçirdiği Akış, Hikayeler (Stories), Reels ve Keşfet alanlarında markanızı öne çıkarıyoruz.',
        icon: 'tabler:users',
      },
      {
        title: 'Nokta Atışı Hedefleme & Lookalike Kitleler',
        description: 'Mevcut müşterilerinize en çok benzeyen (Lookalike) kitleleri ve ilgi alanı segmentlerini hedefleyerek müşteri edinme maliyetinizi düşürüyoruz.',
        icon: 'tabler:target',
      },
      {
        title: 'E-Ticaret & Dinamik Katalog Satışları',
        description: 'Web sitenizde incelediği ürünü kullanıcıya Instagram üzerinde dinamik olarak tekrar göstererek (DPA) sepet terk oranlarını satışa çeviriyoruz.',
        icon: 'tabler:shopping-bag-check',
      },
      {
        title: 'Potansiyel Müşteri (Lead) Formları & WhatsApp',
        description: 'Hizmet sektörleri ve klinikler için uygulama içinden çıkmadan hızlı form toplama veya doğrudan WhatsApp/DM mesajlaşma kampanyaları kuruyoruz.',
        icon: 'tabler:message-circle-bolt',
      },
      {
        title: 'Marka Farkındalığı ve Takipçi Kazanımı',
        description: 'Hedef kitlenizin görsel beklentileriyle uyumlu kreatiflerle organik etkileşiminizi ve nitelikli takipçi kitlenizi büyütüyoruz.',
        icon: 'tabler:sparkles',
      },
      {
        title: 'Kreatif A/B Testleri & ROAS Optimizasyonu',
        description: 'Farklı görsel, video kancası (hook) ve harekete geçirici mesajları test ederek en çok satış getiren reklam kombinasyonuna bütçe aktarıyoruz.',
        icon: 'tabler:chart-bar',
      },
    ],
    processTitle: 'Instagram Reklamlarında Hizmet Sürecimiz',
    processSteps: defaultProcessSteps,
    comparisonRows: [
      {
        criteria: 'Reklam Yöntemi',
        traditional: 'Telefondan "Gönderiyi Öne Çıkar" butonuyla yüzeysel harcama',
        roasist: 'Meta Ads Manager üzerinden CAPI destekli, huni (funnel) mimarili profesyonel yönetim',
      },
      {
        criteria: 'Kitle Yapısı',
        traditional: 'Tek bir genel ilgi alanı hedeflemesi',
        roasist: 'Soğuk kitle, etkileşimde bulunanlar ve sepet terk edenler için katmanlı retargeting',
      },
    ],
    faqs: [
      {
        question: 'Instagram Reklamları nedir ve nasıl çalışır?',
        answer: 'Instagram Reklamları, işletmelerin ürünlerini veya hizmetlerini Instagram Akış, Hikayeler (Stories), Reels ve Keşfet alanlarında tanıtmalarına olanak tanıyan ücretli performans reklamlarıdır. İlgi alanlarına, demografiye, web sitesi ziyaret geçmişine ve benzer kitle (Lookalike) sinyallerine göre en doğru kullanıcılara gösterilir.',
      },
      {
        question: '“Gönderiyi Öne Çıkar” ile profesyonel Instagram reklam yönetimi arasındaki fark nedir?',
        answer: '“Gönderiyi Öne Çıkar” seçeneği sınırlı hedefleme ve etkileşim odaklı çalışır. Profesyonel Meta Business Manager yönetiminde ise dönüşüm pikseli, Sunucu Taraflı Takip (CAPI), katalog entegrasyonu, özel kitleler, A/B testleri ve doğrudan satış/form optimizasyonu kullanılır.',
      },
    ],
  },
  {
    slug: 'performans-pazarlamasi/facebook-reklamlari',
    permalink: '/hizmetler/performans-pazarlamasi/facebook-reklamlari/',
    category: 'Performans Kanalı',
    icon: 'tabler:brand-facebook',
    seoTitle: 'Roasist - Facebook Reklamları',
    seoDescription: 'Veriye dayalı ve performans odaklı Facebook Reklamları yönetimi. Gelişmiş hedefleme, katalog reklamları ve retargeting ile dönüşümlerinizi artırın.',
    h1: 'Facebook Reklamları',
    heroQuestion: 'Veriye dayalı ve performans odaklı Facebook reklamları ile tanışmaya hazır mısınız?',
    aeoDirectAnswer:
      'Facebook Reklamları; Meta’nın gelişmiş yapay zeka algoritması (Advantage+) ve 2.9 milyardan fazla küresel kullanıcı verisiyle demografik, ilgi alanı, davranış ve yeniden pazarlama (retargeting) hedeflemeleri sunarak e-ticaret satışlarını ve potansiyel müşteri formlarını ölçeklendiren reklam platformudur.',
    metrics: [
      { value: '2.9B+ Küresel', label: 'Dev Kullanıcı Ekosistemi', detail: 'Yurt içi ve yurt dışı (ihracat) pazarlarda en geniş erişim' },
      { value: 'Advantage+', label: 'Yapay Zeka Optimizasyonu', detail: 'Meta algoritmasıyla en yüksek satın alma eğilimli kitle eşleşmesi' },
      { value: 'Tam Retargeting', label: 'Dinamik Yeniden Pazarlama', detail: 'Web sitesi ziyaretçilerini ve sepet terkleri satışa dönüştürme' },
    ],
    overviewHeading: 'Neden Facebook Reklamları Kullanmalısınız?',
    overviewParagraphs: [
      'Roasist, kalite ve performans odaklı çalışma prensibini gözetir, doğru ölçümleme için gerekli entegrasyonları ve teknolojileri kullanır, detaylı analizler sonucu reklam stratejinizi inşa eder, verilerin ışığında kampanya süreçlerini daha iyi hale getirir ve anlamlı raporlar ile sürece sizi de dahil eder.',
      'Facebook, Türkiye dahil birçok ülkede yüksek aktif kullanıcı sayısına sahip olan güçlü bir sosyal medya ve reklam platformudur. Dünyada 2.93 milyarı aşan kullanıcı tabanıyla hem yerel pazarda hem de küresel ihracat kampanyalarında en etkili müşteri kazanım kanallarından biridir.',
      'Facebook reklamları ile konum, yaş, cinsiyet ve dil gibi demografik seçimlerin yanı sıra kullanıcıların davranışlarına, ilgi alanlarına, özel kitlelere (Custom Audiences) ve benzer hedef kitlelere (Lookalike) göre kampanyalarınızı en ince ayrıntısına kadar özelleştiriyoruz.',
    ],
    subFeaturesTitle: 'Facebook Reklamlarının Avantajları Nelerdir?',
    subFeaturesSubtitle: 'Meta ekosisteminin tüm veri gücünü işletmenizin büyümesi için kullanıyoruz.',
    subFeatures: [
      {
        title: 'Gelişmiş Demografik ve Davranışsal Hedefleme',
        description: 'Konum, yaş, eğitim, ilgi alanları ve satın alma alışkanlıklarına göre yalnızca potansiyel müşterilerinize bütçe harcayın.',
        icon: 'tabler:user-check',
      },
      {
        title: 'Advantage+ Alışveriş & Katalog Kampanyaları',
        description: 'E-ticaret ürün kataloğunuzu Meta’nın makine öğrenimiyle birleştirerek her kullanıcıya satın alma ihtimali en yüksek ürünü gösterin.',
        icon: 'tabler:shopping-cart',
      },
      {
        title: 'Yeniden Pazarlama (Retargeting) Gücü',
        description: 'Web sitenizi ziyaret eden, ürün inceleyen veya sosyal medya hesabınızla etkileşime giren sıcak kitleyi özel tekliflerle yakalayın.',
        icon: 'tabler:repeat',
      },
      {
        title: 'Yurt Dışı & İhracat Kampanyaları',
        description: 'Avrupa, Amerika, Orta Doğu ve küresel pazarlarda doğru kitlelere ulaşarak döviz bazlı satış ve hasta/müşteri kazanımı sağlayın.',
        icon: 'tabler:world-upload',
      },
      {
        title: 'Zengin Reklam Formatları',
        description: 'Dönen (Carousel) kartlar, koleksiyon reklamları, video reklamlar ve anında deneyim (Instant Experience) formatlarıyla yüksek etkileşim alın.',
        icon: 'tabler:layout-cards',
      },
      {
        title: 'Ölçülebilir Bütçe ve ROAS Kontrolü',
        description: 'Harcanan her kuruşun getirdiği tıklama, form ve sepet tutarını şeffaf panellerde anlık olarak izleyin.',
        icon: 'tabler:chart-pie',
      },
    ],
    processTitle: 'Facebook Reklamlarında Hizmet Sürecimiz',
    processSteps: defaultProcessSteps,
    comparisonRows: [
      {
        criteria: 'Veri & Sinyal Kalitesi',
        traditional: 'Çerez kısıtlamaları nedeniyle eksik dönüşüm ölçümü',
        roasist: 'Meta Pixel + Conversions API (CAPI) ile %100’e yakın veri eşleşmesi',
      },
      {
        criteria: 'Kreatif Stratejisi',
        traditional: 'Uzun ve karmaşık metinli standart görseller',
        roasist: 'Kısa, vurucu reklam metinleri, yüksek kaliteli videolar ve net CTA kurgusu',
      },
    ],
    faqs: [
      {
        question: 'Facebook Reklamları nedir ve nasıl oluşturulur?',
        answer: 'Facebook Reklamları, işletmelerin ürün ve hizmetlerini Meta Reklam Yöneticisi (Ads Manager) üzerinden hedef kitlelerine ulaştırdığı performans reklamlarıdır. Hedef kitle, bütçe, yerleşim ve dönüşüm hedefi profesyonel olarak yapılandırılarak yayınlanır.',
      },
      {
        question: 'Etkili Facebook Reklamları oluşturmak için en önemli kriterler nelerdir?',
        answer: 'Doğru dönüşüm kurulumu (Pixel + CAPI), katmanlı kitle segmentasyonu, kısa ve ikna edici reklam metinleri, yüksek kaliteli görsel/video kreatifler ve net harekete geçirici mesaj (CTA) kullanımı en kritik başarı faktörleridir.',
      },
    ],
  },
  {
    slug: 'performans-pazarlamasi/tiktok-reklamlari',
    permalink: '/hizmetler/performans-pazarlamasi/tiktok-reklamlari/',
    category: 'Performans Kanalı',
    icon: 'tabler:brand-tiktok',
    seoTitle: 'TikTok Reklamları - Roasist',
    seoDescription: 'TikTok reklamlarıyla dijital pazarlama stratejinizi güçlendirin. In-Feed, Spark Ads ve dinamik video reklamlarıyla hedef kitlenizle bağ kurun ve satışlarınızı artırın.',
    h1: 'TikTok Reklamları',
    heroQuestion: 'TikTok reklamlarıyla dijital pazarlama stratejinizi güçlendirmeye ve izleyicilerinizle bağ kurmaya hazır mısınız?',
    aeoDirectAnswer:
      'TikTok Reklamları; yüksek izlenme ve etkileşim oranlarına sahip kısa video ekosisteminde In-Feed, Spark Ads, TopView ve Katalog reklam formatlarıyla markaların geniş kitlelere hızlıca ulaşmasını, viral farkındalık yaratmasını ve doğrudan e-ticaret/uygulama dönüşümü elde etmesini sağlayan reklam platformudur.',
    metrics: [
      { value: 'Yüksek Etkileşim', label: 'Organik Görünümlü Reklamlar', detail: 'Sizin İçin (For You) akışında doğal video deneyimi' },
      { value: 'Spark Ads', label: 'İçerik Üreticisi & Marka Gücü', detail: 'Organik içerikleri performans reklamına dönüştürme' },
      { value: 'Düşük CPM', label: 'Verimli Erişim Maliyeti', detail: 'Geniş kitlelere rekabetçi maliyetlerle hızlı ulaşım' },
    ],
    overviewHeading: 'İşletmeler İçin TikTok Reklamlarının Önemi Nedir?',
    overviewParagraphs: [
      'Roasist, kalite ve performans odaklı çalışma prensibini gözetir, doğru ölçümleme için gerekli entegrasyonları ve teknolojileri kullanır, detaylı analizler sonucu reklam stratejinizi inşa eder, verilerin ışığında kampanya süreçlerini daha iyi hale getirir ve anlamlı raporlar ile sürece sizi de dahil eder.',
      'TikTok, dünya genelinde ve Türkiye’de milyonlarca aktif kullanıcıya sahip, her gün milyarlarca videonun izlendiği en dinamik sosyal medya platformudur. TikTok reklamları sayesinde markanızı geniş bir kitleye ulaştırabilir ve potansiyel müşterilerle güçlü bir etkileşim kurabilirsiniz.',
      'TikTok’un gelişmiş reklam hedefleme özellikleri sayesinde reklamlarınızı demografik özelliklere, konuma, ilgi alanlarına ve video izleme davranışlarına göre hedefliyor; yeniden pazarlama (retargeting) ve benzer hedef kitlelerle (Lookalike) dönüşümlerinizi ölçeklendiriyoruz.',
    ],
    subFeaturesTitle: 'TikTok Reklam Formatlarımız ve Çözümlerimiz',
    subFeaturesSubtitle: 'TikTok’un eğlenceli ve hızlı tüketilen doğasına uygun, satış getiren kreatif reklam stratejileri.',
    subFeatures: [
      {
        title: 'In-Feed (Akış İçi) Video Reklamları',
        description: 'Kullanıcıların “Sizin İçin” (For You) akışında organik videolar arasında tam ekran ve sesli olarak görünen, doğrudan sitenize yönlendiren reklamlar.',
        icon: 'tabler:video',
      },
      {
        title: 'Spark Ads (Organik Gönderi Güçlendirme)',
        description: 'Markanızın veya işbirliği yaptığınız içerik üreticilerinin (UGC) organik TikTok videolarını dönüşüm butonlu performans reklamlarına dönüştürün.',
        icon: 'tabler:flame',
      },
      {
        title: 'TikTok E-Ticaret & Katalog Satışları',
        description: 'Dinamik ürün kartları ve katalog entegrasyonuyla videoyu izleyen kullanıcıları tek dokunuşla ürün satın alma sayfasına taşıyın.',
        icon: 'tabler:shopping-cart-plus',
      },
      {
        title: 'Potansiyel Müşteri (Lead Generation) Formları',
        description: 'TikTok içinden ayrılmadan saniyeler içinde doldurulabilen anlık formlarla hızlı ve düşük maliyetli müşteri talepleri toplayın.',
        icon: 'tabler:forms',
      },
      {
        title: 'Yeniden Pazarlama & Benzer Kitleler',
        description: 'Web sitenizi ziyaret eden veya videolarınızı sonuna kadar izleyen kullanıcılara özel yeniden pazarlama kurguları oluşturun.',
        icon: 'tabler:users-group',
      },
      {
        title: 'TikTok Pixel & Events API Kurulumu',
        description: 'İzlenme, tıklama, sepete ekleme ve satın alma verilerini Events API ile eksiksiz ölçerek algoritmayı en kârlı müşteriler için eğitin.',
        icon: 'tabler:activity',
      },
    ],
    processTitle: 'TikTok Reklamları Hizmet Sürecimiz',
    processSteps: defaultProcessSteps,
    comparisonRows: [
      {
        criteria: 'Video Kurgusu',
        traditional: 'Klasik kurumsal reklam videosunun olduğu gibi yüklenmesi',
        roasist: 'İlk 3 saniyede yakalayan (Hook), platform diline uygun UGC ve dinamik kurgu',
      },
      {
        criteria: 'Ölçümleme',
        traditional: 'Sadece izlenme sayısına bakılması',
        roasist: 'TikTok Pixel, Events API, CPA ve ROAS metrikleriyle gerçek satış takibi',
      },
    ],
    faqs: [
      {
        question: 'TikTok reklamları hangi işletmeler için uygundur?',
        answer: 'E-ticaret markaları, mobil uygulamalar, kozmetik, moda, eğitim, sağlık turizmi ve hızlı tüketim ürünleri başta olmak üzere hem genç hem de satın alma gücü yüksek yetişkin kitleye ulaşmak isteyen tüm B2C ve modern B2B markalar için son derece etkilidir.',
      },
      {
        question: 'TikTok reklamlarında hangi metrikler takip edilir?',
        answer: 'İzlenme sayısı, ilk 2 ve 6 saniye tutma oranı (Hook Rate / Hold Rate), etkileşim oranı, tıklama oranı (CTR), tıklama başı maliyet (CPC), dönüşüm sayısı ve reklam harcaması getirisi (ROAS) detaylı olarak takip edilir.',
      },
    ],
  },
  {
    slug: 'performans-pazarlamasi/linkedin-reklamlari',
    permalink: '/hizmetler/performans-pazarlamasi/linkedin-reklamlari/',
    category: 'Performans Kanalı',
    icon: 'tabler:brand-linkedin',
    seoTitle: 'Linkedin Reklamları - Roasist',
    seoDescription: 'LinkedIn reklamlarıyla B2B ağınızı ve kurumsal satışlarınızı büyütün. Şirket, sektör ve unvan bazlı hedeflemeyle karar vericilere doğrudan ulaşın.',
    h1: 'LinkedIn Reklamları',
    heroQuestion: 'LinkedIn reklamlarıyla B2B ağınızı geliştirmeye hazır mısınız?',
    aeoDirectAnswer:
      'LinkedIn Reklamları; dünya genelinde 1 milyara yakın iş profesyonelini barındıran LinkedIn üzerinde şirket büyüklüğü, sektör, kıdem ve iş unvanına göre nokta atışı hedefleme yaparak B2B (şirketler arası) potansiyel müşteri ve kurumsal satış fırsatı yaratan en prestijli reklam platformudur.',
    metrics: [
      { value: '%100 B2B', label: 'Karar Verici Hedefleme', detail: 'CEO, Direktör, Satın Alma ve İK yöneticilerine doğrudan erişim' },
      { value: 'Lead Gen', label: 'Hazır Kurumsal Formlar', detail: 'LinkedIn profil bilgileriyle otomatik dolan yüksek dönüşümlü formlar' },
      { value: 'ABM', label: 'Şirket Bazlı Pazarlama', detail: 'Hedeflediğiniz spesifik şirket listelerine özel reklam gösterimi' },
    ],
    overviewHeading: 'Şirketler İçin LinkedIn Reklamlarının Önemi Nedir?',
    overviewParagraphs: [
      'Roasist, kalite ve performans odaklı çalışma prensibini gözetir, doğru ölçümleme için gerekli entegrasyonları ve teknolojileri kullanır, detaylı analizler sonucu reklam stratejinizi inşa eder, verilerin ışığında kampanya süreçlerini daha iyi hale getirir ve anlamlı raporlar ile sürece sizi de dahil eder.',
      'LinkedIn, iş dünyasının liderlerini, yöneticilerini ve profesyonellerini bir araya getiren en güçlü iş ağıdır. İşletmeler ve B2B markalar için nitelikli kurumsal müşterilere erişmek ve yüksek hacimli ticari anlaşmalar başlatmak için benzersiz bir kanaldır.',
      'LinkedIn’in kapsamlı profesyonel verileri sayesinde reklamlarınızı belirli sektörlere, şirket büyüklüklerine, iş unvanlarına, kıdem düzeylerine ve coğrafi konumlara göre nokta atışı hedefliyoruz. Ayrıca LinkedIn Lead Gen Forms özelliğiyle karar vericilerden doğrudan talep topluyoruz.',
    ],
    subFeaturesTitle: 'LinkedIn Reklam Formatlarımız ve B2B Stratejilerimiz',
    subFeaturesSubtitle: 'Kurumsal satış döngünüzü hızlandıran ve nitelikli B2B toplantılar üreten kampanya modelleri.',
    subFeatures: [
      {
        title: 'Sponsored Content (Desteklenen İçerik)',
        description: 'Hedeflediğiniz yöneticilerin LinkedIn akışında tek görsel, video, carousel veya belge (Document Ads) formatında kurumsal çözümlerinizi sunun.',
        icon: 'tabler:presentation',
      },
      {
        title: 'LinkedIn Lead Gen Forms (Potansiyel Müşteri Formları)',
        description: 'Kullanıcının adı, iş e-postası, unvanı ve şirket bilgisinin otomatik dolduğu formlarla sürtünmesiz ve yüksek dönüşümlü B2B talepler toplayın.',
        icon: 'tabler:file-analytics',
      },
      {
        title: 'Sponsored Messaging (InMail & Conversation Ads)',
        description: 'Hedeflediğiniz karar vericilerin doğrudan LinkedIn mesaj kutusuna kişiselleştirilmiş kurumsal teklifler ve toplantı davetleri gönderin.',
        icon: 'tabler:mail-fast',
      },
      {
        title: 'Account-Based Marketing (ABM / Şirket Hedefleme)',
        description: 'Çalışmak istediğiniz hedef şirketlerin listesini yükleyerek yalnızca o firmalardaki karar vericilere özel kampanyalar yürütün.',
        icon: 'tabler:building-skyscraper',
      },
      {
        title: 'Dynamic Ads & Text Ads',
        description: 'Masaüstü sağ sütun ve üst bant yerleşimleriyle hedef kitlenizin profil fotoğrafıyla kişiselleştirilmiş dikkat çekici reklamlar yayınlayın.',
        icon: 'tabler:ad',
      },
      {
        title: 'Insight Tag & B2B Dönüşüm Analitiği',
        description: 'Web sitenizi hangi şirketlerin ve hangi unvandaki profesyonellerin ziyaret ettiğini analiz ederek yeniden pazarlama yapın.',
        icon: 'tabler:chart-infographic',
      },
    ],
    processTitle: 'LinkedIn Reklamları Hizmet Sürecimiz',
    processSteps: defaultProcessSteps,
    comparisonRows: [
      {
        criteria: 'Hedef Kitle Kalitesi',
        traditional: 'Genel sosyal medya kitlelerinde B2B karar verici aramak',
        roasist: 'Doğrudan Şirket Boyutu + Sektör + Unvan (C-Level / Müdür) kesişimiyle sıfır kayıp',
      },
      {
        criteria: 'Form Dönüşümü',
        traditional: 'Dış sitede uzun form doldurtmaya çalışmak',
        roasist: 'LinkedIn Lead Gen Forms ile 2 tıklamada doğrulanmış kurumsal iletişim bilgisi',
      },
    ],
    faqs: [
      {
        question: 'LinkedIn Reklamları hangi hedefleme seçeneklerini sunar?',
        answer: 'LinkedIn; sektör, şirket büyüklüğü, şirket adı (ABM), iş unvanı, iş fonksiyonu, kıdem düzeyi, yetenekler, mezun olunan okul ve coğrafi konum gibi hiçbir başka platformda bulunmayan doğrulanmış profesyonel hedefleme seçenekleri sunar.',
      },
      {
        question: 'B2B firmamız için LinkedIn reklamları nasıl ölçülür?',
        answer: 'Görüntülenme sayısı, tıklama oranı (CTR), tıklama başı maliyet (CPC), form doldurma oranı, potansiyel müşteri başına maliyet (CPL) ve toplanan kurumsal taleplerin satış ekibinizde toplantıya/satışa dönüşme oranı (SQL/ROI) ile ölçülür.',
      },
    ],
  },
  {
    slug: 'performans-pazarlamasi/yandex-reklamlari',
    permalink: '/hizmetler/performans-pazarlamasi/yandex-reklamlari/',
    category: 'Performans Kanalı',
    icon: 'tabler:world',
    seoTitle: 'Yandex Reklamları - Roasist',
    seoDescription: 'Yandex reklamlarıyla Rusya, BDT ülkeleri ve küresel pazarlarda hedef kitlenize ulaşın. Yandex Direct arama ve görüntülü reklam ağı yönetimi.',
    h1: 'Yandex Reklamları',
    heroQuestion: 'Yandex reklamlarıyla dijital pazarlama stratejinizi güçlendirmeye hazır mısınız?',
    aeoDirectAnswer:
      'Yandex Reklamları (Yandex Direct); Rusya, BDT (Bağımsız Devletler Topluluğu) ülkeleri ve Rusça konuşan pazarlarda lider arama motoru olan Yandex’in Arama Sonuçları ve Yandex Reklam Ağı (YAN) üzerinden ihracat, turizm, sağlık turizmi ve gayrimenkul markalarını doğrudan potansiyel müşterilerle buluşturan reklam platformudur.',
    metrics: [
      { value: '#1 Arama', label: 'Rusya & BDT Pazar Lideri', detail: 'Rusça konuşulan coğrafyada en yüksek arama ve erişim payı' },
      { value: 'Yandex Direct', label: 'Arama + YAN Ağı', detail: 'Arama sonuçları ve binlerce iş ortağı sitede görsel reklamlar' },
      { value: 'Metrica', label: 'Isı Haritası & Analitik', detail: 'Yandex Metrica ve Webvisor ile kullanıcı davranış analizi' },
    ],
    overviewHeading: 'İşletmeler İçin Yandex Reklamlarının Önemi Nedir?',
    overviewParagraphs: [
      'Roasist, kalite ve performans odaklı çalışma prensibini gözetir, doğru ölçümleme için gerekli entegrasyonları ve teknolojileri kullanır, detaylı analizler sonucu reklam stratejinizi inşa eder, verilerin ışığında kampanya süreçlerini daha iyi hale getirir ve anlamlı raporlar ile sürece sizi de dahil eder.',
      'Yandex Reklamları, Rusya ve BDT ülkelerinin önde gelen arama motoru ve dijital ekosistemi olan Yandex üzerinde markaların ürün veya hizmetlerini tanıtmak için kullanılan en güçlü reklam kanalıdır.',
      'Özellikle sağlık turizmi, gayrimenkul, turizm/otelcilik, tekstil ve ihracat yapan işletmeler için Yandex Direct üzerinden bölgesel, demografik ve arama niyetine dayalı hedefleme yaparak yüksek dönüşümlü uluslararası müşteriler kazandırıyoruz.',
    ],
    subFeaturesTitle: 'Yandex Reklam Formatlarımız ve Çözümlerimiz',
    subFeaturesSubtitle: 'Rusya ve BDT pazarlarında markanızı yerel kullanıcı alışkanlıklarına tam uyumlu şekilde büyütüyoruz.',
    subFeatures: [
      {
        title: 'Yandex Arama (Search) Reklamları',
        description: 'Yandex arama motorunda ürün veya hizmetinizi Rusça veya yerel dilde arayan kullanıcılara en üst sırada reklamlarınızı gösterin.',
        icon: 'tabler:search',
      },
      {
        title: 'Yandex Reklam Ağı (YAN) Gösterim Reklamları',
        description: 'Yandex’in ortaklık ağındaki binlerce popüler web sitesi ve mobil uygulamada görsel, metin ve video reklamlarla erişiminizi katlayın.',
        icon: 'tabler:browser',
      },
      {
        title: 'Sağlık Turizmi & Gayrimenkul Uzmanlığı',
        description: 'Türkiye’ye gelen uluslararası hasta ve gayrimenkul yatırımcılarının arama alışkanlıklarına özel yüksek dönüşümlü kampanya kurguları.',
        icon: 'tabler:plane-arrival',
      },
      {
        title: 'Yandex Metrica & Webvisor Analitiği',
        description: 'Ziyaretçilerin sitenizdeki tıklama, kaydırma ve form doldurma davranışlarını ısı haritalarıyla izleyerek dönüşüm oranınızı artırın.',
        icon: 'tabler:chart-dots',
      },
      {
        title: 'Yeniden Pazarlama (Retargeting)',
        description: 'Sitenizi ziyaret edip henüz form bırakmayan uluslararası ziyaretçileri Yandex ekosisteminde tekrar yakalayarak müşteriye dönüştürün.',
        icon: 'tabler:refresh',
      },
      {
        title: 'Coğrafi ve Demografik Mikro Hedefleme',
        description: 'Moskova, St. Petersburg, Kazakistan, Özbekistan, Azerbaycan veya Türkiye içindeki Rusça konuşan kitleleri şehir bazında hedefleyin.',
        icon: 'tabler:map-2',
      },
    ],
    processTitle: 'Yandex Reklamları Hizmet Sürecimiz',
    processSteps: defaultProcessSteps,
    comparisonRows: [
      {
        criteria: 'Pazar Erişimi',
        traditional: 'Sadece Google ile Rusya/BDT pazarına ulaşmaya çalışmak',
        roasist: 'Pazarın gerçek hakimi olan Yandex Direct + YAN ağıyla tam kapsama',
      },
      {
        criteria: 'Analitik & Optimizasyon',
        traditional: 'Yüzeysel tıklama takibi',
        roasist: 'Yandex Metrica hedef (Goal) entegrasyonuyla gerçek başvuru ve satış optimizasyonu',
      },
    ],
    faqs: [
      {
        question: 'Yandex Reklamları nedir ve nerelerde görüntülenir?',
        answer: 'Yandex Reklamları (Yandex Direct), Rusya ve BDT ülkelerinin lider arama motoru Yandex’in arama sonuçları sayfalarında, Yandex Haritalar’da ve Yandex Reklam Ağı (YAN) bünyesindeki binlerce web sitesi ile mobil uygulamada görüntülenen performans reklamlarıdır.',
      },
      {
        question: 'Hangi sektörler mutlaka Yandex Reklamları kullanmalıdır?',
        answer: 'Başta sağlık turizmi (saç ekimi, diş, estetik, hastane), gayrimenkul/inşaat, turizm ve otelcilik, e-ihracat, lojistik ve B2B üretim sektörleri olmak üzere Rusya ve BDT coğrafyasından müşteri kazanmak isteyen tüm işletmeler için vazgeçilmez bir kanaldır.',
      },
    ],
  },
];

export function getServiceBySlug(slug: string): ServicePageData | undefined {
  return servicesData.find((s) => s.slug === slug);
}
