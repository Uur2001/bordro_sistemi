ASGARI_UCRET_BRUT = 33030.00
SGK_ISCI_ORANI = 0.14
SGK_TAVANI = ASGARI_UCRET_BRUT * 9
ISSIZLIK_ISCI_ORANI = 0.01

BES_ORANI = 0.03
SGK_ISVEREN_ORANI = 0.2175
ISSIZLIK_ISVEREN_ORANI = 0.02
DAMGA_VERGISI_ORANI = 0.00759

HAZINE_ORANI = 0.05
STD_ISVEREN_PAYI = SGK_ISVEREN_ORANI  # 0.2175
BOLGESEL_EK_PUAN = 0.06

SOSYAL_GUVENLIK_TIPI = {

    "00": {
        "Ad": "SGK'ya Tabi Değil",
        "Isci_SGK": 0.00,
        "Isci_Iss": 0.00,
        "Isveren_SGK": 0.00,
        "Isveren_Iss": 0.00,
        "Vergi_Muaf": False
    },

    "01": {
        "Ad": "Hizmet Akdi ile Tüm Sigorta Kollarında Çalışanlar",
        "Isci_SGK": SGK_ISCI_ORANI,
        "Isci_Iss": ISSIZLIK_ISCI_ORANI,
        "Isveren_SGK": SGK_ISVEREN_ORANI,
        "Isveren_Iss": ISSIZLIK_ISVEREN_ORANI,
        "Vergi_Muaf": False
    },

    "02": {
        "Ad": "Sosyal Güvenlik Destek Primine Tabi Çalışanlar (Emekliler)",
        "Isci_SGK": 0.075,
        "Isci_Iss": 0.00,
        "Isveren_SGK": 0.245,
        "Isveren_Iss": 0.00,
        "Vergi_Muaf": False
    },

    "04": {
        "Ad": "Yeraltında Sürekli Çalışanlar",
        "Isci_SGK": SGK_ISCI_ORANI,
        "Isci_Iss": ISSIZLIK_ISCI_ORANI,
        "Isveren_SGK": SGK_ISVEREN_ORANI + 0.03,
        "Isveren_Iss": ISSIZLIK_ISVEREN_ORANI,
        "Vergi_Muaf": False
    },

    "05": {
        "Ad": "Yer Altında Gruplu (Münavebeli) Çalışanlar",
        "Isci_SGK": SGK_ISCI_ORANI,
        "Isci_Iss": ISSIZLIK_ISCI_ORANI,
        "Isveren_SGK": SGK_ISVEREN_ORANI + 0.03,
        "Isveren_Iss": ISSIZLIK_ISVEREN_ORANI,
        "Vergi_Muaf": False
    },

    "06": {
        "Ad": "Yer Üstü Gruplu Çalışanlar",
        "Isci_SGK": SGK_ISCI_ORANI,
        "Isci_Iss": ISSIZLIK_ISCI_ORANI,
        "Isveren_SGK": SGK_ISVEREN_ORANI,
        "Isveren_Iss": ISSIZLIK_ISVEREN_ORANI,
        "Vergi_Muaf": False
    },

    "07": {
        "Ad": "3308 Sayılı Kanun (Aday Çırak, Çırak ve Öğrenciler)",
        "Isci_SGK": 0.00,
        "Isci_Iss": 0.00,
        "Isveren_SGK": 0.02,
        "Isveren_Iss": 0.00,
        "Vergi_Muaf": True
    },

    "12": {
        "Ad": "Geçici 20. Maddeye Tabi Olanlar (Banka/Borsa Sandıkları)",
        "Isci_SGK": SGK_ISCI_ORANI,
        "Isci_Iss": ISSIZLIK_ISCI_ORANI,
        "Isveren_SGK": SGK_ISVEREN_ORANI,
        "Isveren_Iss": ISSIZLIK_ISVEREN_ORANI,
        "Vergi_Muaf": False
    },

    "13": {
        "Ad": "Tüm Sigorta Kollarında Olup İşsizlik Primi Kesilmeyenler",
        "Isci_SGK": SGK_ISCI_ORANI,
        "Isci_Iss": 0.00,
        "Isveren_SGK": SGK_ISVEREN_ORANI,
        "Isveren_Iss": 0.00,
        "Vergi_Muaf": False
    },

    "14": {
        "Ad": "Libya'da Çalışanlar",
        "Isci_SGK": 0.05,
        "Isci_Iss": 0.00,
        "Isveren_SGK": 0.095,
        "Isveren_Iss": 0.00,
        "Vergi_Muaf": False
    },

    "19": {
        "Ad": "Ceza İnfaz Kurumlarında Çalıştırılan Hükümlü ve Tutuklular",
        "Isci_SGK": 0.00,
        "Isci_Iss": 0.00,
        "Isveren_SGK": 0.02,
        "Isveren_Iss": 0.00,
        "Vergi_Muaf": True
    },

    "20": {
        "Ad": "İstisna Akdine İstinaden Almanya'ya Götürülen Türk İşçiler",
        "Isci_SGK": 0.00,
        "Isci_Iss": 0.00,
        "Isveren_SGK": 0.00,
        "Isveren_Iss": 0.00,
        "Vergi_Muaf": False
    },

    "21": {
        "Ad": "Sözleşmesiz Ülkelere Götürülen Türk İşçileri",
        "Isci_SGK": 0.06,
        "Isci_Iss": 0.00,
        "Isveren_SGK": 0.115,
        "Isveren_Iss": 0.00,
        "Vergi_Muaf": False
    },

    "22": {
        "Ad": "Meslek Lisesi/Yüksek Öğrenim Stajyerleri ve Kısmi Zamanlı Öğrenciler",
        "Isci_SGK": 0.00,
        "Isci_Iss": 0.00,
        "Isveren_SGK": 0.02,
        "Isveren_Iss": 0.00,
        "Vergi_Muaf": True
    },

    "23": {
        "Ad": "Harp/Vazife Malullüğü Aylığı Alanlardan Tüm Sigorta Kollarına Tabi Olanlar",
        "Isci_SGK": SGK_ISCI_ORANI,
        "Isci_Iss": ISSIZLIK_ISCI_ORANI,
        "Isveren_SGK": SGK_ISVEREN_ORANI,
        "Isveren_Iss": ISSIZLIK_ISVEREN_ORANI,
        "Vergi_Muaf": False
    },

    "25": {
        "Ad": "İŞKUR Tarafından Düzenlenen Eğitimlere Katılan Kursiyer",
        "Isci_SGK": 0.00,
        "Isci_Iss": 0.00,
        "Isveren_SGK": 0.00,
        "Isveren_Iss": 0.00,
        "Vergi_Muaf": True
    },

    "28": {
        "Ad": "4046 Sayılı Kanun Kapsamında İş Kaybı Tazminatı Alanlar",
        "Isci_SGK": 0.00,
        "Isci_Iss": 0.00,
        "Isveren_SGK": 0.00,
        "Isveren_Iss": 0.00,
        "Vergi_Muaf": False
    },

    "29": {
        "Ad": "Tüm Sigorta Kolları + 60 Gün Fiili Hizmet Süresi Zammı",
        "Isci_SGK": SGK_ISCI_ORANI,
        "Isci_Iss": ISSIZLIK_ISCI_ORANI,
        "Isveren_SGK": SGK_ISVEREN_ORANI + 0.01,
        "Isveren_Iss": ISSIZLIK_ISVEREN_ORANI,
        "Vergi_Muaf": False
    },

    "30": {
        "Ad": "İşsizlik Sigortası Hariç + 60 Gün Fiili Hizmet Süresi Zammı",
        "Isci_SGK": SGK_ISCI_ORANI,
        "Isci_Iss": 0.00,
        "Isveren_SGK": SGK_ISVEREN_ORANI + 0.01,
        "Isveren_Iss": 0.00,
        "Vergi_Muaf": False
    },

    "31": {
        "Ad": "Harp/Vazife Malulleri + 60 Gün Fiili Hizmet Süresi Zammı",
        "Isci_SGK": SGK_ISCI_ORANI,
        "Isci_Iss": ISSIZLIK_ISCI_ORANI,
        "Isveren_SGK": SGK_ISVEREN_ORANI + 0.01,
        "Isveren_Iss": ISSIZLIK_ISVEREN_ORANI,
        "Vergi_Muaf": False
    },

    "32": {
        "Ad": "Tüm Sigorta Kolları + 90 Gün Fiili Hizmet Süresi Zammı",
        "Isci_SGK": SGK_ISCI_ORANI,
        "Isci_Iss": ISSIZLIK_ISCI_ORANI,
        "Isveren_SGK": SGK_ISVEREN_ORANI + 0.015,
        "Isveren_Iss": ISSIZLIK_ISVEREN_ORANI,
        "Vergi_Muaf": False
    },

    "33": {
        "Ad": "İşsizlik Sigortası Hariç + 90 Gün Fiili Hizmet Süresi Zammı",
        "Isci_SGK": SGK_ISCI_ORANI,
        "Isci_Iss": 0.00,
        "Isveren_SGK": SGK_ISVEREN_ORANI + 0.015,
        "Isveren_Iss": 0.00,
        "Vergi_Muaf": False
    },

    "34": {
        "Ad": "Harp/Vazife Malulleri + 90 Gün Fiili Hizmet Süresi Zammı",
        "Isci_SGK": SGK_ISCI_ORANI,
        "Isci_Iss": ISSIZLIK_ISCI_ORANI,
        "Isveren_SGK": SGK_ISVEREN_ORANI + 0.015,
        "Isveren_Iss": ISSIZLIK_ISVEREN_ORANI,
        "Vergi_Muaf": False
    },

    "35": {
        "Ad": "Tüm Sigorta Kolları + 180 Gün Fiili Hizmet Süresi Zammı",
        "Isci_SGK": SGK_ISCI_ORANI,
        "Isci_Iss": ISSIZLIK_ISCI_ORANI,
        "Isveren_SGK": SGK_ISVEREN_ORANI + 0.03,
        "Isveren_Iss": ISSIZLIK_ISVEREN_ORANI,
        "Vergi_Muaf": False
    },

    "37": {
        "Ad": "Harp/Vazife Malulleri + 180 Gün Fiili Hizmet Süresi Zammı",
        "Isci_SGK": SGK_ISCI_ORANI,
        "Isci_Iss": ISSIZLIK_ISCI_ORANI,
        "Isveren_SGK": SGK_ISVEREN_ORANI + 0.03,
        "Isveren_Iss": ISSIZLIK_ISVEREN_ORANI,
        "Vergi_Muaf": False
    },

    "39": {
        "Ad": "Birleşik Krallık/İsviçre Vatandaşı (Uzun Vadeli Talep Etmeyen)",
        "Isci_SGK": 0.05,
        "Isci_Iss": 0.00,
        "Isveren_SGK": 0.095,
        "Isveren_Iss": 0.00,
        "Vergi_Muaf": False
    },

    "41": {
        "Ad": "Kamu İdarelerinde İş Akdi Askıda Olanlar",
        "Isci_SGK": 0.00,
        "Isci_Iss": 0.00,
        "Isveren_SGK": 0.12,
        "Isveren_Iss": 0.00,
        "Vergi_Muaf": False
    },

    "90": {
        "Ad": "İtibari Hizmet Süresine Tabi Çalışanlar",
        "Isci_SGK": SGK_ISCI_ORANI,
        "Isci_Iss": ISSIZLIK_ISCI_ORANI,
        "Isveren_SGK": SGK_ISVEREN_ORANI,
        "Isveren_Iss": ISSIZLIK_ISVEREN_ORANI,
        "Vergi_Muaf": False
    },

    "91": {
        "Ad": "60 Gün FHSZ + İtibari Hizmet Süresine Tabi Olanlar",
        "Isci_SGK": SGK_ISCI_ORANI,
        "Isci_Iss": ISSIZLIK_ISCI_ORANI,
        "Isveren_SGK": SGK_ISVEREN_ORANI + 0.01,
        "Isveren_Iss": ISSIZLIK_ISVEREN_ORANI,
        "Vergi_Muaf": False
    },

    "92": {
        "Ad": "90 Gün FHSZ + İtibari Hizmet Süresine Tabi Olanlar",
        "Isci_SGK": SGK_ISCI_ORANI,
        "Isci_Iss": ISSIZLIK_ISCI_ORANI,
        "Isveren_SGK": SGK_ISVEREN_ORANI + 0.015,
        "Isveren_Iss": ISSIZLIK_ISVEREN_ORANI,
        "Vergi_Muaf": False
    },
}

KANUN_KODLARI = {

    "00000": {
        "Ad": "Teşviksiz (Borçlu İşveren)",
        "Indirim": 0.00,
        "Aciklama": "Herhangi bir indirim uygulanmaz (SGK borcu olanlar)"
    },

    "05510": {
        "Ad": "Hazine Yardımı (5 Puan)",
        "Indirim": HAZINE_ORANI,
        "Aciklama": "Primlerini düzenli ödeyen işverenler için 5 puan indirim"
    },

    "00687": {
        "Ad": "KHK 687 İstihdam Desteği",
        "Indirim": STD_ISVEREN_PAYI,
        "Aciklama": "4447 Sayılı Kanun Geçici 17. Madde (İstihdam Seferberliği)"
    },

    "05746": {
        "Ad": "Ar-Ge Merkezi Teşviki",
        "Indirim": STD_ISVEREN_PAYI,
        "Aciklama": "Ar-Ge ve tasarım merkezlerinde çalışan personeller"
    },

    "05921": {
        "Ad": "İşsizlik Ödeneği Teşviki",
        "Indirim": STD_ISVEREN_PAYI,
        "Aciklama": "5921 Sayılı Kanun (İşsizlik ödeneği alanların istihdamı)"
    },

    "06111": {
        "Ad": "Genç/Kadın İstihdamı (4447/G.10)",
        "Indirim": STD_ISVEREN_PAYI,
        "Aciklama": "Genç, kadın ve mesleki belge sahibi istihdamı teşviki"
    },

    "06486": {
        "Ad": "Bölgesel Teşvik (6 Puan)",
        "Indirim": HAZINE_ORANI + BOLGESEL_EK_PUAN,
        "Aciklama": "51 il ve 2 ilçeyi kapsayan 6 puanlık bölgesel indirim"
    },

    "06645": {
        "Ad": "İşbaşı Eğitim Teşviki (4447/G.15)",
        "Indirim": STD_ISVEREN_PAYI,
        "Aciklama": "İşbaşı eğitim programını tamamlayanların istihdamı"
    },

    "14447": {
        "Ad": "İşsizlik Ödeneği (4447/Md.50)",
        "Indirim": HAZINE_ORANI,
        "Aciklama": "İşsizlik ödeneği alan personelin istihdamı (Prim mahsuplaşması)"
    },

    "14857": {
        "Ad": "Engelli Teşviki (4857/Md.30)",
        "Indirim": STD_ISVEREN_PAYI,
        "Aciklama": "Özel sektör engelli kontenjanı teşviki"
    },

    "15921": {
        "Ad": "5921 Teşviki (Eski)",
        "Indirim": STD_ISVEREN_PAYI,
        "Aciklama": "5921 Sayılı Kanun kapsamındaki eski teşvikler"
    },

    "16322": {
        "Ad": "Yatırım Teşviki (6322)",
        "Indirim": HAZINE_ORANI,
        "Aciklama": "Yatırımlarda Devlet Yardımı (Sigorta Primi İşveren Hissesi)"
    },

    "24447": {
        "Ad": "İlave İstihdam (Hizmet - 27103)",
        "Indirim": STD_ISVEREN_PAYI,
        "Aciklama": "4447/G.19 Hizmet ve diğer sektörler için ilave istihdam"
    },

    "25225": {
        "Ad": "Kültür Yatırımları",
        "Indirim": STD_ISVEREN_PAYI,
        "Aciklama": "Kültür Yatırım ve Girişimlerini Teşvik Kanunu"
    },

    "25510": {
        "Ad": "Yatırım Teşviki (5510 Ek-2)",
        "Indirim": HAZINE_ORANI,
        "Aciklama": "Bölgesel yatırım teşvik belgesi kapsamındaki indirimler"
    },

    "26322": {
        "Ad": "Yatırım Teşviki (Genel)",
        "Indirim": HAZINE_ORANI,
        "Aciklama": "Yatırım teşvik belgesine istinaden uygulanan destek"
    },

    "44447": {
        "Ad": "İlave İstihdam (İmalat - 17103)",
        "Indirim": STD_ISVEREN_PAYI,
        "Aciklama": "4447/G.19 İmalat ve bilişim sektörü ilave istihdam"
    },

    "46486": {
        "Ad": "Bölgesel Teşvik (Ek Puan)",
        "Indirim": HAZINE_ORANI + BOLGESEL_EK_PUAN,
        "Aciklama": "Öncelikli illerde uygulanan bölgesel teşvik varyasyonu"
    },

    "54857": {
        "Ad": "Korumalı İşyeri (Engelli)",
        "Indirim": STD_ISVEREN_PAYI,
        "Aciklama": "Korumalı işyerlerinde çalışan engelliler için %100 destek"
    },

    "55225": {
        "Ad": "Kültür Girişimleri",
        "Indirim": STD_ISVEREN_PAYI,
        "Aciklama": "Kültür teşviklerinin farklı oranlı varyasyonu"
    },

    "56486": {
        "Ad": "Bölgesel Teşvik (6 Puan)",
        "Indirim": HAZINE_ORANI + BOLGESEL_EK_PUAN,
        "Aciklama": "51 İl 2 İlçe teşviki (En yaygın kullanılan 6 puanlık kod)"
    },

    "64447": {
        "Ad": "4447 Sayılı Kanun (Diğer)",
        "Indirim": STD_ISVEREN_PAYI,
        "Aciklama": "Normalleşme desteği veya sektörel 4447 ek teşvikleri"
    },

    "66476": {
        "Ad": "Ar-Ge/Teknoloji (6676)",
        "Indirim": STD_ISVEREN_PAYI,
        "Aciklama": "6676 Sayılı Kanun ile güncellenen Ar-Ge/Tasarım destekleri"
    },

    "84447": {
        "Ad": "4447 Sayılı Kanun (Özel)",
        "Indirim": STD_ISVEREN_PAYI,
        "Aciklama": "Belirli yazılımlarda kullanılan özel 4447 teşvik kodu"
    },
}

VERGI_DILIMLERI = [
    (190000, 0.15),
    (400000, 0.20),
    (1500000, 0.27),
    (5300000, 0.35),
    (float('inf'), 0.40)
]

ENGELLILIK_INDIRIMLERI = {
    0: 0,
    '0': 0,
    1: 12000,
    '1': 12000,
    '1_derece': 12000,
    2: 7000,
    '2': 7000,
    '2_derece': 7000,
    3: 3500,
    '3': 3500,
    '3_derece': 3500,
}

# --- AYLAR ---
AYLAR = {
    1: {"ad": "Ocak", "gun": 31},
    2: {"ad": "Şubat", "gun": 28},
    3: {"ad": "Mart", "gun": 31},
    4: {"ad": "Nisan", "gun": 30},
    5: {"ad": "Mayıs", "gun": 31},
    6: {"ad": "Haziran", "gun": 30},
    7: {"ad": "Temmuz", "gun": 31},
    8: {"ad": "Ağustos", "gun": 31},
    9: {"ad": "Eylül", "gun": 30},
    10: {"ad": "Ekim", "gun": 31},
    11: {"ad": "Kasım", "gun": 30},
    12: {"ad": "Aralık", "gun": 31},
}