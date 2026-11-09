import { getPermalink, getBlogPermalink } from './utils/permalinks';

export const headerData = {
  links: [
    {
      text: 'Anasayfa',
      href: getPermalink('/'),
    },
    {
      text: 'Hizmetler',
      links: [
        {
          text: 'Performans Pazarlaması',
          href: getPermalink('/hizmetler/performans-pazarlamasi/'),
        },
        {
          text: '360° Dijital Pazarlama Yönetimi',
          href: getPermalink('/hizmetler/360-derece-dijital-pazarlama-yonetimi/'),
        },
        {
          text: 'Arama Motoru Optimizasyonu (SEO)',
          href: getPermalink('/hizmetler/seo/'),
        },
        {
          text: 'Web Tasarım & Geliştirme',
          href: getPermalink('/hizmetler/web-tasarim/'),
        },
        {
          text: 'Kreatif & Grafik Tasarım',
          href: getPermalink('/hizmetler/grafik-tasarim/'),
        },
      ],
    },
    {
      text: 'Reklam Kanalları',
      links: [
        {
          text: 'Google Reklamları (Ads)',
          href: getPermalink('/hizmetler/performans-pazarlamasi/google-reklamlari/'),
        },
        {
          text: 'Instagram Reklamları',
          href: getPermalink('/hizmetler/performans-pazarlamasi/instagram-reklamlari/'),
        },
        {
          text: 'Facebook (Meta) Reklamları',
          href: getPermalink('/hizmetler/performans-pazarlamasi/facebook-reklamlari/'),
        },
        {
          text: 'TikTok Reklamları',
          href: getPermalink('/hizmetler/performans-pazarlamasi/tiktok-reklamlari/'),
        },
        {
          text: 'LinkedIn B2B Reklamları',
          href: getPermalink('/hizmetler/performans-pazarlamasi/linkedin-reklamlari/'),
        },
        {
          text: 'Yandex Reklamları',
          href: getPermalink('/hizmetler/performans-pazarlamasi/yandex-reklamlari/'),
        },
      ],
    },
    {
      text: 'Referanslar',
      href: getPermalink('/referanslar/'),
    },
    {
      text: 'Hakkımızda',
      href: getPermalink('/hakkimizda/'),
    },
    {
      text: 'Blog',
      href: getBlogPermalink(),
    },
    {
      text: 'İletişim',
      href: getPermalink('/iletisim/'),
    },
  ],
  actions: [
    {
      text: 'Strateji Görüşmesi Planla',
      href: getPermalink('/iletisim/'),
      variant: 'primary',
    },
  ],
};

export const footerData = {
  links: [
    {
      title: 'Büyüme Hizmetleri',
      links: [
        { text: 'Performans Pazarlaması', href: getPermalink('/hizmetler/performans-pazarlamasi/') },
        { text: '360° Dijital Pazarlama Yönetimi', href: getPermalink('/hizmetler/360-derece-dijital-pazarlama-yonetimi/') },
        { text: 'Arama Motoru Optimizasyonu (SEO)', href: getPermalink('/hizmetler/seo/') },
        { text: 'Web Tasarım & UI/UX', href: getPermalink('/hizmetler/web-tasarim/') },
        { text: 'Kreatif & Grafik Tasarım', href: getPermalink('/hizmetler/grafik-tasarim/') },
      ],
    },
    {
      title: 'Reklam Yönetimi',
      links: [
        { text: 'Google Ads Yönetimi', href: getPermalink('/hizmetler/performans-pazarlamasi/google-reklamlari/') },
        { text: 'Instagram Reklamları', href: getPermalink('/hizmetler/performans-pazarlamasi/instagram-reklamlari/') },
        { text: 'Facebook Reklamları', href: getPermalink('/hizmetler/performans-pazarlamasi/facebook-reklamlari/') },
        { text: 'TikTok Reklamları', href: getPermalink('/hizmetler/performans-pazarlamasi/tiktok-reklamlari/') },
        { text: 'LinkedIn B2B Reklamları', href: getPermalink('/hizmetler/performans-pazarlamasi/linkedin-reklamlari/') },
        { text: 'Yandex Reklamları', href: getPermalink('/hizmetler/performans-pazarlamasi/yandex-reklamlari/') },
      ],
    },
    {
      title: 'Kurumsal',
      links: [
        { text: 'Hakkımızda', href: getPermalink('/hakkimizda/') },
        { text: 'Referanslar & Başarılar', href: getPermalink('/referanslar/') },
        { text: 'Dijital Pazarlama Blogu', href: getBlogPermalink() },
        { text: 'İletişim & Randevu', href: getPermalink('/iletisim/') },
        { text: 'Marketing Intelligence OS', href: 'https://marketing.roasist.com' },
      ],
    },
    {
      title: 'İletişim & Destek',
      links: [
        { text: 'WhatsApp Hızlı Destek (+90 541 507 53 50)', href: 'https://wa.me/+905415075350' },
        { text: 'Ücretsiz Ön Analiz Talebi', href: getPermalink('/iletisim/#analiz-formu') },
        { text: 'Gizlilik Politikası ve Kullanım Şartları', href: getPermalink('/gizlilik-politikasi-ve-kullanim-sartlari/') },
      ],
    },
  ],
  secondaryLinks: [
    { text: 'Gizlilik Politikası ve Kullanım Şartları', href: getPermalink('/gizlilik-politikasi-ve-kullanim-sartlari/') },
    { text: 'Site Haritası', href: '/sitemap-index.xml' },
  ],
  socialLinks: [
    { ariaLabel: 'LinkedIn', icon: 'tabler:brand-linkedin', href: 'https://www.linkedin.com/company/roasist/' },
    { ariaLabel: 'Instagram', icon: 'tabler:brand-instagram', href: 'https://www.instagram.com/roasist/' },
    { ariaLabel: 'X (Twitter)', icon: 'tabler:brand-x', href: 'https://twitter.com/Roasistt' },
    { ariaLabel: 'YouTube', icon: 'tabler:brand-youtube', href: 'https://www.youtube.com/channel/UCY3G_IU2YJ326zGwU3_YlyA' },
    { ariaLabel: 'Facebook', icon: 'tabler:brand-facebook', href: 'https://www.facebook.com/roasistt' },
    { ariaLabel: 'WhatsApp', icon: 'tabler:brand-whatsapp', href: 'https://wa.me/+905415075350' },
  ],
  footNote: `
    © ${new Date().getFullYear()} <strong>Roasist</strong> — Özelleştirilmiş Dijital Pazarlama & Büyüme Teknolojileri. Tüm hakları saklıdır.
  `,
};
