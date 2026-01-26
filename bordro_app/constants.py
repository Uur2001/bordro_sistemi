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
# Her tip için: (isci_sgk, isci_issizlik, isveren_sgk, isveren_kvsk, isveren_issizlik)
# Not: isci_sgk = MYÖ + GSS, isveren_sgk = MYÖ + GSS

SGK_TIPLERI = {
    # Belge No: (ad, isci_sgk, isci_issizlik, isveren_myo_gss, isveren_kvsk, isveren_issizlik, sgdp_mi)
    '1': {
        'ad': 'Hizmet Akdi ile Tüm Sigorta Kollarına Tabi Çalışanlar',
        'isci_sgk': 14.00,        # MYÖ %9 + GSS %5
        'isci_issizlik': 1.00,
        'isveren_sgk': 19.50,     # MYÖ %12 + GSS %7.5
        'isveren_kvsk': 2.25,
        'isveren_issizlik': 2.00,
        'sgdp': False,
    },
    '2': {
        'ad': 'Sosyal Güvenlik Destek Primine Tabi Çalışanlar',
        'isci_sgk': 7.50,         # SGDP işçi payı
        'isci_issizlik': 0.00,    # İşsizlik YOK
        'isveren_sgk': 22.50,     # SGDP işveren payı
        'isveren_kvsk': 2.25,
        'isveren_issizlik': 0.00, # İşsizlik YOK
        'sgdp': True,
    },
    '4': {
        'ad': 'Yer Altında Sürekli Çalışanlar',
        'isci_sgk': 14.00,        # MYÖ %9 + GSS %5
        'isci_issizlik': 1.00,
        'isveren_sgk': 22.50,     # MYÖ %15 + GSS %7.5 (3 puan fazla)
        'isveren_kvsk': 2.25,
        'isveren_issizlik': 2.00,
        'sgdp': False,
    },
    '5': {
        'ad': 'Yer Altında Gruplu (Münavebekli) Çalışanlar',
        'isci_sgk': 14.00,
        'isci_issizlik': 1.00,
        'isveren_sgk': 22.50,     # MYÖ %15 + GSS %7.5
        'isveren_kvsk': 2.25,
        'isveren_issizlik': 2.00,
        'sgdp': False,
    },
    '6': {
        'ad': 'Yerüstü Gruplu Çalışanlar',
        'isci_sgk': 14.00,
        'isci_issizlik': 1.00,
        'isveren_sgk': 22.50,     # MYÖ %15 + GSS %7.5
        'isveren_kvsk': 2.25,
        'isveren_issizlik': 2.00,
        'sgdp': False,
    },
}

# Varsayılan SGK Tipi
VARSAYILAN_SGK_TIPI = '1'