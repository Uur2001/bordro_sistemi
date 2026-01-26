"""
Bordro Hesaplama Sistemi - Sabit Parametreler
2026 Yılı Değerleri

Bu dosya tüm bordro hesaplamalarında kullanılan
sabit değerleri içerir. Yıl değiştiğinde sadece
bu dosyayı güncellemeniz yeterlidir.
"""

# ==========================================
# ASGARİ ÜCRET (2026)
# ==========================================
ASGARI_UCRET_BRUT = 33030.00  # Aylık Brüt Asgari Ücret
ASGARI_UCRET_GUNLUK = 1101.00  # Günlük Brüt (33030 / 30)
ASGARI_UCRET_SAATLIK = 146.80  # Saatlik Brüt (33030 / 225)

# ==========================================
# ÇALIŞMA SÜRELERİ
# ==========================================
AYLIK_GUN = 30  # Aylık gün sayısı (sabit)
AYLIK_SAAT = 225  # Aylık çalışma saati (45 saat x 5 gün x 30/7)
HAFTALIK_SAAT = 45  # Haftalık çalışma saati

# ==========================================
# SGK ORANLARI (%)
# ==========================================
SGK_ISCI_ORANI = 14.00  # İşçi SGK primi
SGK_ISVEREN_ORANI = 19.50  # İşveren SGK primi (normal)
SGK_ISVEREN_TEHLIKELI = 20.50  # İşveren SGK primi (tehlikeli iş)
SGK_KVSK_ORANI = 2.25  # Kısa vadeli sigorta kolları (işveren)
ISSIZLIK_ISCI_ORANI = 1.00  # İşçi işsizlik sigortası
ISSIZLIK_ISVEREN_ORANI = 2.00  # İşveren işsizlik sigortası
BES_ORANI = 3.00  # Bireysel Emeklilik Sistemi (otomatik katılım)
HAZINE_YARDIMI_ORANI = 2.00  # 5 puanlık hazine yardımı

# SGK Taban ve Tavan
SGK_TABAN = ASGARI_UCRET_BRUT  # SGK matrah tabanı = Asgari ücret
SGK_TAVAN_KATSAYI = 9  # Tavan = Asgari Ücret x 7.5
SGK_TAVAN = ASGARI_UCRET_BRUT * SGK_TAVAN_KATSAYI  # 247.725 TL

# ==========================================
# GELİR VERGİSİ DİLİMLERİ (2026)
# ==========================================
# Her dilim: (üst_limit, oran)
# Son dilim için üst limit None (sınırsız)
GELIR_VERGISI_DILIMLERI = [
    (190000.00, 15.00),   # 0 - 190.000 TL arası %15
    (400000.00, 20.00),   # 190.001 - 400.000 TL arası %20
    (1500000.00, 27.00),  # 400.001 - 1.500.000 TL arası %27
    (5300000.00, 35.00),  # 1.500.001 - 5.300.000 TL arası %35
    (None, 40.00),        # 5.300.001 TL ve üzeri %40
]

# ==========================================
# DAMGA VERGİSİ
# ==========================================
DAMGA_VERGISI_ORANI = 0.759  # Binde 7.59 = %0.759

# ==========================================
# ÖZEL SİGORTA İNDİRİM LİMİTLERİ
# ==========================================
# Sağlık sigortası: Brüt ücretin %15'ini geçemez
SAGLIK_SIGORTA_INDIRIM_ORANI = 15.00

# Hayat sigortası: Ödenen primin %50'si indirilebilir
HAYAT_SIGORTA_INDIRIM_ORANI = 50.00

# Yıllık toplam limit: Yıllık asgari ücret toplamı
YILLIK_SIGORTA_INDIRIM_LIMIT = ASGARI_UCRET_BRUT * 12

# ==========================================
# FAZLA MESAİ ORANLARI (%)
# ==========================================
FAZLA_MESAI_ORANLARI = {
    'FM01': 50.00,   # Normal fazla mesai (%50 zamlı)
    'FM02': 100.00,  # Hafta sonu mesaisi (%100 zamlı)
    'FM03': 200.00,  # Resmi tatil mesaisi (%200 zamlı)
}

# ==========================================
# ENGELLİLİK İNDİRİMİ (Aylık TL)
# ==========================================
ENGELLILIK_INDIRIMI = {
    '1': 12000.00,  # 1. Derece (%80 ve üzeri)
    '2': 7000.00,  # 2. Derece (%60-79)
    '3': 3000.00,  # 3. Derece (%40-59)
}

# ==========================================
# AYLAR (Türkçe)
# ==========================================
AYLAR = {
    1: 'Ocak',
    2: 'Şubat',
    3: 'Mart',
    4: 'Nisan',
    5: 'Mayıs',
    6: 'Haziran',
    7: 'Temmuz',
    8: 'Ağustos',
    9: 'Eylül',
    10: 'Ekim',
    11: 'Kasım',
    12: 'Aralık',
}

# ==========================================
# SGK TİPLERİ VE ORANLARI (2026)
# ==========================================
# Her tip için oranlar (%)
# kvsk: Kısa Vadeli Sigorta Kolları (İşveren) - ✓ ise 2.25, ✗ ise 0
# sgk_isci: SGK İşçi Payı
# sgk_isveren: SGK İşveren Payı
# issizlik_isci: İşsizlik Sigortası İşçi Payı
# issizlik_isveren: İşsizlik Sigortası İşveren Payı
# hazine_yardimi: Hazine Yardımı Oranı

SGK_TIPLERI = {
    '1': {
        'ad': 'Hizmet Akdi ile Tüm Sigorta Kollarına Tabi Çalışanlar',
        'kvsk': 2.25,
        'sgk_isci': 14.00,
        'sgk_isveren': 19.50,
        'issizlik_isci': 1.00,
        'issizlik_isveren': 2.00,
        'hazine_yardimi': 2.00,
    },
    '2': {
        'ad': 'Sosyal Güvenlik Destek Primine Tabi Çalışanlar (Emekliler)',
        'kvsk': 2.25,
        'sgk_isci': 7.50,
        'sgk_isveren': 22.50,
        'issizlik_isci': 0.00,
        'issizlik_isveren': 0.00,
        'hazine_yardimi': 0.00,
    },
    '4': {
        'ad': 'Yer Altında Sürekli Çalışanlar',
        'kvsk': 2.25,
        'sgk_isci': 14.00,
        'sgk_isveren': 21.50,
        'issizlik_isci': 1.00,
        'issizlik_isveren': 2.00,
        'hazine_yardimi': 4.00,
    },
    '5': {
        'ad': 'Yer Altında Gruplu (Münavebeli) Çalışanlar',
        'kvsk': 2.25,
        'sgk_isci': 14.00,
        'sgk_isveren': 21.50,
        'issizlik_isci': 1.00,
        'issizlik_isveren': 2.00,
        'hazine_yardimi': 4.00,
    },
    '6': {
        'ad': 'Yer Üstü Gruplu Çalışanlar',
        'kvsk': 2.25,
        'sgk_isci': 14.00,
        'sgk_isveren': 21.50,
        'issizlik_isci': 1.00,
        'issizlik_isveren': 2.00,
        'hazine_yardimi': 4.00,
    },
    '7': {
        'ad': '3308 Sayılı Kanunda Belirtilen Aday Çırak, Çırak ve İşletmelerde Eğitim Gören Öğrenciler',
        'kvsk': 0.00,
        'sgk_isci': 0.00,
        'sgk_isveren': 1.00,
        'issizlik_isci': 0.00,
        'issizlik_isveren': 0.00,
        'hazine_yardimi': 0.00,
    },
    '12': {
        'ad': 'Geçici 20. Maddeye Tabi Olanlar (Sandık, Oda, Borsa ve Birlik)',
        'kvsk': 0.00,
        'sgk_isci': 0.00,
        'sgk_isveren': 0.00,
        'issizlik_isci': 1.00,
        'issizlik_isveren': 2.00,
        'hazine_yardimi': 0.00,
    },
    '13': {
        'ad': 'Tüm Sigorta Kollarına Tabi Olup İşsizlik Sigortası Primi Kesilmeyenler',
        'kvsk': 2.25,
        'sgk_isci': 14.00,
        'sgk_isveren': 19.50,
        'issizlik_isci': 0.00,
        'issizlik_isveren': 0.00,
        'hazine_yardimi': 2.00,
    },
    '14': {
        'ad': 'Libya\'da Çalışanlar',
        'kvsk': 2.25,
        'sgk_isci': 9.00,
        'sgk_isveren': 11.00,
        'issizlik_isci': 1.00,
        'issizlik_isveren': 2.00,
        'hazine_yardimi': 0.00,
    },
    '19': {
        'ad': 'Ceza İnfaz Kurumları ile Tutukevleri Bünyesinde Oluşturulan Tesis Atölye ve Benzeri Ünitelerde Çalıştırılan Hükümlü ve Tutuklular',
        'kvsk': 2.25,
        'sgk_isci': 0.00,
        'sgk_isveren': 0.00,
        'issizlik_isci': 0.00,
        'issizlik_isveren': 0.00,
        'hazine_yardimi': 0.00,
    },
    '20': {
        'ad': 'İstisna Akdine İstinaden Almanya\'ya Götürülen Türk İşçiler',
        'kvsk': 2.25,
        'sgk_isci': 14.00,
        'sgk_isveren': 19.50,
        'issizlik_isci': 1.00,
        'issizlik_isveren': 2.00,
        'hazine_yardimi': 0.00,
    },
    '21': {
        'ad': 'Türk İşverenler Tarafından Sosyal Güvenlik Sözleşmesi İmzalanmamış Ülkelere Götürülerek Çalıştırılan Türk İşçileri',
        'kvsk': 2.25,
        'sgk_isci': 5.00,
        'sgk_isveren': 7.50,
        'issizlik_isci': 0.00,
        'issizlik_isveren': 0.00,
        'hazine_yardimi': 0.00,
    },
    '22': {
        'ad': 'Meslek Liselerinde Okumakta İken veya Yüksek Öğrenimleri Sırasında Staja Tabi Tutulan Öğrenciler ile Üniversitelerde Kısmi Zamanlı Çalıştırılan Öğrenciler',
        'kvsk': 0.00,
        'sgk_isci': 0.00,
        'sgk_isveren': 1.00,
        'issizlik_isci': 0.00,
        'issizlik_isveren': 0.00,
        'hazine_yardimi': 0.00,
    },
    '23': {
        'ad': 'Harp Malulleri ile 3713 ve 2330 Sayılı Kanunlara Göre Vazife Malullüğü Aylığı Alanlardan Kısa Vadeli Sigorta Kollarına Tabi Olanlar',
        'kvsk': 2.25,
        'sgk_isci': 0.00,
        'sgk_isveren': 0.00,
        'issizlik_isci': 0.00,
        'issizlik_isveren': 0.00,
        'hazine_yardimi': 0.00,
    },
    '24': {
        'ad': 'Harp Malulleri ile 3713 ve 2330 Sayılı Kanunlara Göre Vazife Malullüğü Aylığı Alanlardan Kısa ve Uzun Vadeli Sigorta Kollarına Tabi Olanlar',
        'kvsk': 2.25,
        'sgk_isci': 9.00,
        'sgk_isveren': 11.00,
        'issizlik_isci': 0.00,
        'issizlik_isveren': 0.00,
        'hazine_yardimi': 4.00,
    },
    '25': {
        'ad': 'Türkiye İş Kurumu Tarafından Düzenlenen Eğitimlere Katılan Kursiyerler',
        'kvsk': 0.00,
        'sgk_isci': 0.00,
        'sgk_isveren': 1.00,
        'issizlik_isci': 0.00,
        'issizlik_isveren': 0.00,
        'hazine_yardimi': 0.00,
    },
    '28': {
        'ad': '4046 Sayılı Kanunun 21 inci Maddesi Kapsamında İş Kaybı Tazminatı Alanlar',
        'kvsk': 0.00,
        'sgk_isci': 0.00,
        'sgk_isveren': 32.00,
        'issizlik_isci': 0.00,
        'issizlik_isveren': 0.00,
        'hazine_yardimi': 0.00,
    },
    '29': {
        'ad': 'Tüm Sigorta Kollarına Tabi Çalışıp 60 Gün Fiili Hizmet Süresi Zammına Tabi Çalışanlar',
        'kvsk': 2.25,
        'sgk_isci': 14.00,
        'sgk_isveren': 19.50,
        'issizlik_isci': 1.00,
        'issizlik_isveren': 2.00,
        'hazine_yardimi': 4.00,
    },
    '30': {
        'ad': 'İşsizlik Sigortası Hariç 60 Gün Fiili Hizmet Süresi Zammına Tabi Çalışanlar',
        'kvsk': 2.25,
        'sgk_isci': 14.00,
        'sgk_isveren': 19.50,
        'issizlik_isci': 0.00,
        'issizlik_isveren': 0.00,
        'hazine_yardimi': 4.00,
    },
    '31': {
        'ad': 'Harp Malülleri ile Vazife Malullüğü Aylığı Alanlardan Kısa ve Uzun Vadeli Sigorta Kollarına Tabi Olup 60 Gün Fiili Hizmet Süresi Zammına Tabi Çalışanlar',
        'kvsk': 2.25,
        'sgk_isci': 9.00,
        'sgk_isveren': 12.00,
        'issizlik_isci': 0.00,
        'issizlik_isveren': 0.00,
        'hazine_yardimi': 0.00,
    },
    '32': {
        'ad': 'Tüm Sigorta Kollarına Tabi Çalışıp 90 Gün Fiili Hizmet Süresi Zammına Tabi Çalışanlar',
        'kvsk': 2.25,
        'sgk_isci': 14.00,
        'sgk_isveren': 20.00,
        'issizlik_isci': 1.00,
        'issizlik_isveren': 2.00,
        'hazine_yardimi': 4.00,
    },
    '33': {
        'ad': 'İşsizlik Sigortası Hariç 90 Gün Fiili Hizmet Süresi Zammına Tabi Çalışanlar',
        'kvsk': 2.25,
        'sgk_isci': 14.00,
        'sgk_isveren': 20.00,
        'issizlik_isci': 0.00,
        'issizlik_isveren': 0.00,
        'hazine_yardimi': 4.00,
    },
    '34': {
        'ad': 'Harp Malülleri ile Vazife Malullüğü Aylığı Alanlardan Kısa ve Uzun Vadeli Sigorta Kollarına Tabi Olup 90 Gün Fiili Hizmet Süresi Zammına Tabi Çalışanlar',
        'kvsk': 2.25,
        'sgk_isci': 9.00,
        'sgk_isveren': 12.50,
        'issizlik_isci': 0.00,
        'issizlik_isveren': 0.00,
        'hazine_yardimi': 4.00,
    },
    '35': {
        'ad': 'Tüm Sigorta Kollarına Tabi Çalışıp 180 Gün Fiili Hizmet Süresi Zammına Tabi Çalışanlar',
        'kvsk': 2.25,
        'sgk_isci': 14.00,
        'sgk_isveren': 21.50,
        'issizlik_isci': 1.00,
        'issizlik_isveren': 2.00,
        'hazine_yardimi': 4.00,
    },
    '36': {
        'ad': 'İşsizlik Sigortası Hariç 180 Gün Fiili Hizmet Süresi Zammına Tabi Çalışanlar',
        'kvsk': 2.25,
        'sgk_isci': 14.00,
        'sgk_isveren': 21.50,
        'issizlik_isci': 0.00,
        'issizlik_isveren': 0.00,
        'hazine_yardimi': 4.00,
    },
    '37': {
        'ad': 'Harp Malülleri ile Vazife Malullüğü Aylığı Alanlardan Kısa ve Uzun Vadeli Sigorta Kollarına Tabi Olup 180 Gün Fiili Hizmet Süresi Zammına Tabi Çalışanlar',
        'kvsk': 2.25,
        'sgk_isci': 9.00,
        'sgk_isveren': 14.00,
        'issizlik_isci': 0.00,
        'issizlik_isveren': 0.00,
        'hazine_yardimi': 4.00,
    },
    '39': {
        'ad': 'Birleşik Krallıkta İkamet Edenler ve İsviçre Vatandaşı Olanlardan Uzun Vadeli Sigorta Kolunun Uygulanmasını Talep Etmeyenler',
        'kvsk': 2.25,
        'sgk_isci': 5.00,
        'sgk_isveren': 7.50,
        'issizlik_isci': 1.00,
        'issizlik_isveren': 2.00,
        'hazine_yardimi': 4.00,
    },
    '41': {
        'ad': 'Kamu İdarelerinde İş Akdi Askıda Olanlar',
        'kvsk': 0.00,
        'sgk_isci': 0.00,
        'sgk_isveren': 12.00,
        'issizlik_isci': 0.00,
        'issizlik_isveren': 0.00,
        'hazine_yardimi': 0.00,
    },
    '90': {
        'ad': 'İtibari Hizmet Süresine Tabi Çalışanlar',
        'kvsk': 0.00,
        'sgk_isci': 0.00,
        'sgk_isveren': 20.00,
        'issizlik_isci': 0.00,
        'issizlik_isveren': 0.00,
        'hazine_yardimi': 0.00,
    },
    '91': {
        'ad': '60 Gün Fiili Hizmet Süresi Zammına Tabi Olanlardan İtibari Hizmet Süresine Tabi Olarak Çalışanlar',
        'kvsk': 0.00,
        'sgk_isci': 0.00,
        'sgk_isveren': 21.00,
        'issizlik_isci': 0.00,
        'issizlik_isveren': 0.00,
        'hazine_yardimi': 0.00,
    },
    '92': {
        'ad': '90 Gün Fiili Hizmet Süresi Zammına Tabi Olanlardan İtibari Hizmet Süresine Tabi Olarak Çalışanlar',
        'kvsk': 0.00,
        'sgk_isci': 0.00,
        'sgk_isveren': 21.50,
        'issizlik_isci': 0.00,
        'issizlik_isveren': 0.00,
        'hazine_yardimi': 0.00,
    },
}

# Varsayılan SGK Tipi
VARSAYILAN_SGK_TIPI = '1'

# ==========================================
# SGK TEŞVİK KANUNLARI (2026)
# ==========================================
# Her kanun için:
# - ad: Kanun adı
# - aciklama: Hesaplama açıklaması
# - matrah_tipi: 'pek' (Prime Esas Kazanç), 'pek_alt_sinir' (Asgari Ücret), 'gun_hesabi' (Gün başına)
# - kapsam: Hangi primler kapsamda ['sgk_isveren', 'kvsk', 'sgk_isci', 'issizlik_isveren', 'issizlik_isci']
# - indirim_orani: İndirim oranı (100 = tamamı, 50 = yarısı, vb.)
# - gunluk_tutar: Gün hesabı için günlük TL tutarı (sadece gun_hesabi tipi için)
# - belgeler: İlgili SGK belge kodları

SGK_KANUNLARI = {
    '00687': {
        'ad': 'İşveren Desteği (4447 nolu kanunun geçici 17. maddesi)',
        'aciklama': 'Çalışma gün sayısı × 22,22 TL',
        'matrah_tipi': 'gun_hesabi',
        'kapsam': [],
        'indirim_orani': 0,
        'gunluk_tutar': 22.22,
        'belgeler': ['2017-010'],
    },
    '05746': {
        'ad': 'Araştırma Geliştirme Faaliyetlerinin Desteklenmesi Hakkındaki Kanun',
        'aciklama': 'PEK üzerinden SGK işveren hissesinin yarısı',
        'matrah_tipi': 'pek',
        'kapsam': ['sgk_isveren'],
        'indirim_orani': 50,
        'gunluk_tutar': 0,
        'belgeler': ['2008-085', '2009-021'],
    },
    '05921': {
        'ad': 'Sosyal Sigortalar ve Genel Sağlık Sigortası Kanunu (4447 nolu kanunun geçici 9. maddesi)',
        'aciklama': 'PEK alt sınırı üzerinden SGK işveren hissesinin tamamı',
        'matrah_tipi': 'pek_alt_sinir',
        'kapsam': ['sgk_isveren'],
        'indirim_orani': 100,
        'gunluk_tutar': 0,
        'belgeler': ['2011-045'],
    },
    '06111': {
        'ad': 'Sosyal Sigortalar ve Genel Sağlık Sigortası Kanunu (4447 nolu kanunun geçici 10. maddesi)',
        'aciklama': 'PEK üzerinden SGK işveren hissesinin tamamı',
        'matrah_tipi': 'pek',
        'kapsam': ['sgk_isveren'],
        'indirim_orani': 100,
        'gunluk_tutar': 0,
        'belgeler': ['2011-045'],
    },
    '06486': {
        'ad': 'Sosyal Sigortalar ve Genel Sağlık Sigortası (5510 nolu kanunun 81 maddesinin 1. fıkrası)',
        'aciklama': 'PEK üzerinden %5',
        'matrah_tipi': 'pek',
        'kapsam': ['ozel_oran'],
        'indirim_orani': 5,
        'gunluk_tutar': 0,
        'belgeler': ['2013-030'],
    },
    '06645': {
        'ad': '4447 Sayılı Kanunun Geçici 15. maddesinde Öngörülen Sigorta Primi Teşviği',
        'aciklama': 'PEK alt sınırı üzerinden SGK işveren hissesinin tamamı',
        'matrah_tipi': 'pek_alt_sinir',
        'kapsam': ['sgk_isveren'],
        'indirim_orani': 100,
        'gunluk_tutar': 0,
        'belgeler': ['2016-001'],
    },
    '14447': {
        'ad': 'Genç İstihdam Teşviği 1. Sene - %100 (4447 nolu kanunun geçici 7. maddesi)',
        'aciklama': 'PEK alt sınırı üzerinden SGK işveren hissesinin tamamı',
        'matrah_tipi': 'pek_alt_sinir',
        'kapsam': ['sgk_isveren'],
        'indirim_orani': 100,
        'gunluk_tutar': 0,
        'belgeler': ['2011-045'],
    },
    '14857': {
        'ad': 'Özürlü Personel İşveren Teşviği Kanunu (Kontenjan Dahili)',
        'aciklama': 'PEK alt sınırı üzerinden SGK işveren hissesinin tamamı',
        'matrah_tipi': 'pek_alt_sinir',
        'kapsam': ['sgk_isveren'],
        'indirim_orani': 100,
        'gunluk_tutar': 0,
        'belgeler': ['2008-077'],
    },
    '15921': {
        'ad': 'Sosyal Sigortalar ve Genel Sağlık Sigortası Kanunu (4447 nolu kanunun 50. maddesinin 5. fıkrası)',
        'aciklama': 'PEK alt sınırı üzerinden KVSK\'nin %1\'i ile SGK işçi ve işveren hissesinin tamamı',
        'matrah_tipi': 'pek_alt_sinir',
        'kapsam': ['sgk_isveren', 'sgk_isci', 'kvsk_kismi'],
        'indirim_orani': 100,
        'kvsk_orani': 1,
        'gunluk_tutar': 0,
        'belgeler': ['2009-149'],
    },
    '16322': {
        'ad': 'Yatırımlarda Devlet Yardımları Hakkında Karar Gereği Uygulanan Teşvik (6322 sayılı kanun)',
        'aciklama': 'PEK alt sınırı üzerinden SGK işveren hissesinin tamamı',
        'matrah_tipi': 'pek_alt_sinir',
        'kapsam': ['sgk_isveren'],
        'indirim_orani': 100,
        'gunluk_tutar': 0,
        'belgeler': ['2012-030'],
    },
    '24447': {
        'ad': 'Genç İstihdam Teşviği 5. Sene - %20 (4447 nolu kanunun geçici 7. maddesi)',
        'aciklama': 'PEK alt sınırı üzerinden SGK işveren hissesinin %20\'si',
        'matrah_tipi': 'pek_alt_sinir',
        'kapsam': ['sgk_isveren'],
        'indirim_orani': 20,
        'gunluk_tutar': 0,
        'belgeler': ['2011-045'],
    },
    '25225': {
        'ad': 'Kültür Yatırımları Kapsamında Sağlanan Teşvik (5225 nolu kanunun 5. maddesi)',
        'aciklama': 'PEK üzerinden SGK işveren hissesinin yarısı',
        'matrah_tipi': 'pek',
        'kapsam': ['sgk_isveren'],
        'indirim_orani': 50,
        'gunluk_tutar': 0,
        'belgeler': ['2010-109'],
    },
    '25510': {
        'ad': 'Yatırımlarda Devlet Yardımları Hakkında Karar Gereği Uygulanan Teşvik (5510 nolu kanunun Ek 2. maddesi)',
        'aciklama': 'PEK alt sınırı üzerinden SGK işveren hissesinin tamamı',
        'matrah_tipi': 'pek_alt_sinir',
        'kapsam': ['sgk_isveren'],
        'indirim_orani': 100,
        'gunluk_tutar': 0,
        'belgeler': ['2011-054'],
    },
    '26322': {
        'ad': 'Yatırımlarda Devlet Yardımları Hakkında Karar Gereği Uygulanan Teşvik (6322 sayılı kanun)',
        'aciklama': 'PEK alt sınırı üzerinden SGK işçi ve işveren hissesinin tamamı',
        'matrah_tipi': 'pek_alt_sinir',
        'kapsam': ['sgk_isveren', 'sgk_isci'],
        'indirim_orani': 100,
        'gunluk_tutar': 0,
        'belgeler': ['2012-030'],
    },
    '44447': {
        'ad': 'Genç İstihdam Teşviği 4. Sene - %40 (4447 nolu kanunun geçici 7. maddesi)',
        'aciklama': 'PEK alt sınırı üzerinden SGK işveren hissesinin %40\'ı',
        'matrah_tipi': 'pek_alt_sinir',
        'kapsam': ['sgk_isveren'],
        'indirim_orani': 40,
        'gunluk_tutar': 0,
        'belgeler': ['2011-045'],
    },
    '46486': {
        'ad': 'Sosyal Sigortalar ve Genel Sağlık Sigortası Kanunu (I.Bölge) (5510 nolu kanunun 81 maddesinin 2. fıkrası)',
        'aciklama': 'PEK alt sınırı üzerinden %6',
        'matrah_tipi': 'pek_alt_sinir',
        'kapsam': ['ozel_oran'],
        'indirim_orani': 6,
        'gunluk_tutar': 0,
        'belgeler': ['2013-030', '2016-008'],
    },
    '54857': {
        'ad': 'Özürlü Personel İşveren Teşviği Kanunu (Kontenjan Fazlası)',
        'aciklama': 'PEK alt sınırı üzerinden SGK işveren hissesinin yarısı',
        'matrah_tipi': 'pek_alt_sinir',
        'kapsam': ['sgk_isveren'],
        'indirim_orani': 50,
        'gunluk_tutar': 0,
        'belgeler': ['2008-077'],
    },
    '55225': {
        'ad': 'Kültür Girişimleri Kapsamında Sağlanan Teşvik (5225 nolu kanunun 5. maddesi)',
        'aciklama': 'PEK üzerinden SGK işveren hissesinin %25\'i',
        'matrah_tipi': 'pek',
        'kapsam': ['sgk_isveren'],
        'indirim_orani': 25,
        'gunluk_tutar': 0,
        'belgeler': ['2010-109'],
    },
    '56486': {
        'ad': 'Sosyal Sigortalar ve Genel Sağlık Sigortası Kanunu (II.Bölge) (5510 nolu kanunun 81 maddesinin 2. fıkrası)',
        'aciklama': 'PEK alt sınırı üzerinden %6',
        'matrah_tipi': 'pek_alt_sinir',
        'kapsam': ['ozel_oran'],
        'indirim_orani': 6,
        'gunluk_tutar': 0,
        'belgeler': ['2013-030', '2016-008'],
    },
    '64447': {
        'ad': 'Genç İstihdam Teşviği 3. Sene - %60 (4447 nolu kanunun geçici 7. maddesi)',
        'aciklama': 'PEK alt sınırı üzerinden SGK işveren hissesinin %60\'ı',
        'matrah_tipi': 'pek_alt_sinir',
        'kapsam': ['sgk_isveren'],
        'indirim_orani': 60,
        'gunluk_tutar': 0,
        'belgeler': ['2011-045'],
    },
    '66486': {
        'ad': 'Sosyal Sigortalar ve Genel Sağlık Sigortası Kanunu (III.Bölge) (5510 nolu kanunun 81 maddesinin 2. fıkrası)',
        'aciklama': 'PEK alt sınırı üzerinden %6',
        'matrah_tipi': 'pek_alt_sinir',
        'kapsam': ['ozel_oran'],
        'indirim_orani': 6,
        'gunluk_tutar': 0,
        'belgeler': ['2013-030', '2016-008'],
    },
    '84447': {
        'ad': 'Genç İstihdam Teşviği 2. Sene - %80 (4447 nolu kanunun geçici 7. maddesi)',
        'aciklama': 'PEK alt sınırı üzerinden SGK işveren hissesinin %80\'i',
        'matrah_tipi': 'pek_alt_sinir',
        'kapsam': ['sgk_isveren'],
        'indirim_orani': 80,
        'gunluk_tutar': 0,
        'belgeler': ['2011-045'],
    },
}

# Varsayılan Kanun (teşvik yok)
VARSAYILAN_KANUN = None


def get_sgk_oranlari(sgk_tipi='1'):
    """
    Belirtilen SGK tipine göre oranları döndürür.

    Parametreler:
        sgk_tipi: SGK belge tipi kodu (string)

    Döndürür:
        dict: İlgili SGK tipinin oranları
    """
    if sgk_tipi not in SGK_TIPLERI:
        sgk_tipi = VARSAYILAN_SGK_TIPI

    return SGK_TIPLERI[sgk_tipi]


def get_kanun_bilgisi(kanun_kodu):
    """
    Belirtilen kanun koduna göre teşvik bilgilerini döndürür.

    Parametreler:
        kanun_kodu: SGK teşvik kanun kodu (string)

    Döndürür:
        dict: İlgili kanunun bilgileri veya None
    """
    if kanun_kodu is None:
        return None

    kanun_kodu = str(kanun_kodu).zfill(5)  # 5 karaktere tamamla (00687, 05746, vb.)
    return SGK_KANUNLARI.get(kanun_kodu)