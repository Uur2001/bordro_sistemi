"""
Bordro Hesaplama Sistemi - Hesaplama Fonksiyonları
==================================================

Bu dosya tüm bordro hesaplama fonksiyonlarını içerir.
Her fonksiyon tek bir iş yapar ve test edilebilir şekilde tasarlanmıştır.

Kullanım:
    from bordro_app.calculations import hesapla_sgk, hesapla_gelir_vergisi, ...
"""

from decimal import Decimal, ROUND_HALF_UP
from . import constants as c


def yuvarla(sayi, basamak=2):
    """
    Sayıyı belirtilen basamağa yuvarlar.
    Bordro hesaplamalarında tutarlılık için kullanılır.

    Parametreler:
        sayi: Yuvarlanacak sayı
        basamak: Ondalık basamak sayısı (varsayılan: 2)


    """
    if sayi is None:
        return 0.0

    carpan = 10 ** basamak
    return round(float(sayi) * carpan) / carpan


# ==========================================
# 1. SGK HESAPLAMALARI
# ==========================================

def hesapla_sgk_matrahi(brut_kazanc, onceki_donem_brut=0, iki_onceki_donem_brut=0):
    """
    SGK matrahını hesaplar.

    SGK matrahı = Brüt Kazanç + Önceki dönem brüt + İki önceki dönem brüt

    Not: SGK matrahı, SGK tavanını geçemez.

    Parametreler:
        brut_kazanc: Bu ayki prime tabi brüt kazanç
        onceki_donem_brut: Önceki aydan devreden brüt (opsiyonel)
        iki_onceki_donem_brut: İki önceki aydan devreden brüt (opsiyonel)

    Döndürür:
        SGK matrahı (TL)

    Örnek (PDF'den):
        hesapla_sgk_matrahi(39113.52, 1111.00, 111.00) -> 40335.52
    """
    toplam = brut_kazanc + onceki_donem_brut + iki_onceki_donem_brut

    # SGK tavanı kontrolü
    if toplam > c.SGK_TAVAN:
        toplam = c.SGK_TAVAN

    return yuvarla(toplam)


def hesapla_sgk_isci_primi(sgk_matrahi):
    """
    İşçi SGK primini hesaplar.

    İşçi SGK Primi = SGK Matrahı × %14

    Parametreler:
        sgk_matrahi: SGK matrahı (TL)

    Döndürür:
        İşçi SGK primi (TL)

    Örnek (PDF'den):
        hesapla_sgk_isci_primi(40335.52) -> 5646.97
    """
    prim = sgk_matrahi * (c.SGK_ISCI_ORANI / 100)
    return yuvarla(prim)


def hesapla_issizlik_isci_primi(sgk_matrahi):
    """
    İşçi işsizlik sigortası primini hesaplar.

    İşsizlik Primi = SGK Matrahı × %1

    Parametreler:
        sgk_matrahi: SGK matrahı (TL)

    Döndürür:
        İşçi işsizlik primi (TL)

    Örnek (PDF'den):
        hesapla_issizlik_isci_primi(40335.52) -> 403.36
    """
    prim = sgk_matrahi * (c.ISSIZLIK_ISCI_ORANI / 100)
    return yuvarla(prim)


def hesapla_bes_kesintisi(sgk_matrahi, bes_aktif=True):
    """
    BES (Bireysel Emeklilik Sistemi) kesintisini hesaplar.

    BES Kesintisi = SGK Matrahı × %3 (aşağı yuvarlanır)

    Parametreler:
        sgk_matrahi: SGK matrahı (TL)
        bes_aktif: BES kesintisi yapılacak mı? (varsayılan: True)

    Döndürür:
        BES kesintisi (TL)
    """
    if not bes_aktif:
        return 0.0

    kesinti = sgk_matrahi * (c.BES_ORANI / 100)
    # BES kesintisi aşağı yuvarlanır (kuruş atılır)
    kesinti = float(int(kesinti))
    return kesinti


def hesapla_sgk_isveren_primi(sgk_matrahi, tehlikeli_is=False):
    """
    İşveren SGK primini hesaplar.

    Normal iş: SGK Matrahı × %15.5
    Tehlikeli iş: SGK Matrahı × %20.5

    Parametreler:
        sgk_matrahi: SGK matrahı (TL)
        tehlikeli_is: Tehlikeli iş mi? (varsayılan: False)

    Döndürür:
        İşveren SGK primi (TL)
    """
    oran = c.SGK_ISVEREN_TEHLIKELI if tehlikeli_is else c.SGK_ISVEREN_ORANI
    prim = sgk_matrahi * (oran / 100)
    return yuvarla(prim)


def hesapla_kvsk_primi(sgk_matrahi):
    """
    Kısa Vadeli Sigorta Kolları primini hesaplar (İşveren).

    KVSK = SGK Matrahı × %2.25

    Parametreler:
        sgk_matrahi: SGK matrahı (TL)

    Döndürür:
        KVSK primi (TL)
    """
    prim = sgk_matrahi * (c.SGK_KVSK_ORANI / 100)
    return yuvarla(prim)


def hesapla_issizlik_isveren_primi(sgk_matrahi):
    """
    İşveren işsizlik sigortası primini hesaplar.

    İşveren İşsizlik = SGK Matrahı × %2

    Parametreler:
        sgk_matrahi: SGK matrahı (TL)

    Döndürür:
        İşveren işsizlik primi (TL)
    """
    prim = sgk_matrahi * (c.ISSIZLIK_ISVEREN_ORANI / 100)
    return yuvarla(prim)


def hesapla_hazine_yardimi(sgk_matrahi, hazine_yardimi_aktif=True):
    """
    5 puanlık hazine yardımını hesaplar.

    Hazine Yardımı = SGK Matrahı × %2
    (İşveren SGK priminden düşülür)

    Parametreler:
        sgk_matrahi: SGK matrahı (TL)
        hazine_yardimi_aktif: Hazine yardımı uygulanacak mı?

    Döndürür:
        Hazine yardımı tutarı (TL)
    """
    if not hazine_yardimi_aktif:
        return 0.0

    yardim = sgk_matrahi * (c.HAZINE_YARDIMI_ORANI / 100)
    return yuvarla(yardim)


def hesapla_tum_sgk_primleri(sgk_matrahi, bes_aktif=True, hazine_yardimi_aktif=True, tehlikeli_is=False):
    """
    Tüm SGK primlerini tek seferde hesaplar.

    Parametreler:
        sgk_matrahi: SGK matrahı (TL)
        bes_aktif: BES kesintisi yapılacak mı?
        hazine_yardimi_aktif: Hazine yardımı uygulanacak mı?
        tehlikeli_is: Tehlikeli iş mi?

    Döndürür:
        dict: Tüm SGK primlerini içeren sözlük

    Örnek:
        hesapla_tum_sgk_primleri(40335.52) -> {
            'isci_sgk': 5646.97,
            'isci_issizlik': 403.36,
            'isci_bes': 1210.07,
            'isci_toplam': 7260.40,
            'isveren_sgk': 6251.99,
            'isveren_kvsk': 907.55,
            'isveren_issizlik': 806.71,
            'hazine_yardimi': 806.71,
            'isveren_toplam': 7159.54
        }
    """
    # İşçi primleri
    isci_sgk = hesapla_sgk_isci_primi(sgk_matrahi)
    isci_issizlik = hesapla_issizlik_isci_primi(sgk_matrahi)
    isci_bes = hesapla_bes_kesintisi(sgk_matrahi, bes_aktif)
    isci_toplam = yuvarla(isci_sgk + isci_issizlik + isci_bes)

    # İşveren primleri
    isveren_sgk = hesapla_sgk_isveren_primi(sgk_matrahi, tehlikeli_is)
    isveren_kvsk = hesapla_kvsk_primi(sgk_matrahi)
    isveren_issizlik = hesapla_issizlik_isveren_primi(sgk_matrahi)
    hazine_yardimi = hesapla_hazine_yardimi(sgk_matrahi, hazine_yardimi_aktif)
    isveren_toplam = yuvarla(isveren_sgk + isveren_kvsk + isveren_issizlik - hazine_yardimi)

    return {
        'isci_sgk': isci_sgk,
        'isci_issizlik': isci_issizlik,
        'isci_bes': isci_bes,
        'isci_toplam': isci_toplam,
        'isveren_sgk': isveren_sgk,
        'isveren_kvsk': isveren_kvsk,
        'isveren_issizlik': isveren_issizlik,
        'hazine_yardimi': hazine_yardimi,
        'isveren_toplam': isveren_toplam,
    }


# ==========================================
# 2. GELİR VERGİSİ HESAPLAMALARI
# ==========================================

def hesapla_ozel_sigorta_indirimi(brut_ucret, saglik_sigorta_primi=0, hayat_sigorta_primi=0,
                                  saglik_sigorta_kesinti=None, hayat_sigorta_kesinti=None,
                                  saglik_sigorta_isveren_kesinti=None, hayat_sigorta_isveren_kesinti=None):
    """
    Özel sigorta indirimlerini hesaplar.

    Kurallar:
    - Sağlık sigortası: İşçi kesinti + İşveren kesinti, brüt ücretin %15'ini geçemez
    - Hayat sigortası: Sadece İşçi kesintinin %50'si indirilebilir (İşveren dahil değil!)
    - Toplam: Yıllık asgari ücret toplamını geçemez

    Parametreler:
        brut_ucret: Brüt ücret (TL)
        saglik_sigorta_primi: Sağlık sigortası işveren payı brütü - brüte eklenen (TL)
        hayat_sigorta_primi: Hayat sigortası işveren payı brütü - brüte eklenen (TL)
        saglik_sigorta_kesinti: Sağlık sigortası işçi kesintisi (TL)
        hayat_sigorta_kesinti: Hayat sigortası işçi kesintisi (TL)
        saglik_sigorta_isveren_kesinti: Sağlık sigortası işveren kesintisi - indirim için (TL)
        hayat_sigorta_isveren_kesinti: Hayat sigortası işveren kesintisi - kullanılmıyor (TL)

    Döndürür:
        dict: Sağlık ve hayat sigortası indirim tutarları
    """
    # Kesinti tutarları
    saglik_isci = saglik_sigorta_kesinti if saglik_sigorta_kesinti is not None else 0
    saglik_isveren = saglik_sigorta_isveren_kesinti if saglik_sigorta_isveren_kesinti is not None else 0
    hayat_isci = hayat_sigorta_kesinti if hayat_sigorta_kesinti is not None else 0
    # hayat_isveren kullanılmıyor - indirime dahil değil

    # Sağlık sigortası indirimi = İşçi Kesinti + İşveren Kesinti
    # Brüt ücretin %15'ini geçemez
    saglik_toplam = saglik_isci + saglik_isveren
    saglik_limit = brut_ucret * (c.SAGLIK_SIGORTA_INDIRIM_ORANI / 100)
    saglik_indirim = min(saglik_toplam, saglik_limit)

    # Hayat sigortası indirimi = Sadece İşçi Kesinti × %50
    # İşveren kesintisi indirime dahil DEĞİL!
    hayat_indirim = hayat_isci * (c.HAYAT_SIGORTA_INDIRIM_ORANI / 100)

    # Toplam limit kontrolü (aylık bazda asgari ücret)
    toplam_indirim = saglik_indirim + hayat_indirim
    if toplam_indirim > c.ASGARI_UCRET_BRUT:
        # Orantılı olarak düşür
        oran = c.ASGARI_UCRET_BRUT / toplam_indirim
        saglik_indirim = yuvarla(saglik_indirim * oran)
        hayat_indirim = yuvarla(hayat_indirim * oran)

    return {
        'saglik_indirim': yuvarla(saglik_indirim),
        'hayat_indirim': yuvarla(hayat_indirim),
        'toplam_indirim': yuvarla(saglik_indirim + hayat_indirim)
    }


def hesapla_gelir_vergisi_matrahi(brut_kazanc, sgk_kesintileri, saglik_sigorta_indirimi=0,
                                  hayat_sigorta_indirimi=0, engellilik_indirimi=0):
    """
    Gelir Vergisi Matrahını hesaplar.

    GV Matrahı = Brüt Kazanç - SGK Kesintileri - Özel Sigorta İndirimleri - Engellilik İndirimi

    Not: SGK kesintileri = İşçi SGK + İşçi İşsizlik (BES dahil değil!)

    Parametreler:
        brut_kazanc: Toplam brüt kazanç (TL)
        sgk_kesintileri: İşçi SGK + İşsizlik toplamı (TL) - BES hariç!
        saglik_sigorta_indirimi: Sağlık sigortası indirimi (TL)
        hayat_sigorta_indirimi: Hayat sigortası indirimi (TL)
        engellilik_indirimi: Engellilik indirimi (TL)

    Döndürür:
        Gelir vergisi matrahı (TL)

    Örnek (PDF'den):
        Brüt: 40234.54 - SGK: 6050.33 - Sağlık: 1222.00 - Hayat: 555.50 = 32406.71
    """
    matrah = (brut_kazanc
              - sgk_kesintileri
              - saglik_sigorta_indirimi
              - hayat_sigorta_indirimi
              - engellilik_indirimi)

    # Matrah negatif olamaz
    if matrah < 0:
        matrah = 0

    return yuvarla(matrah)


def hesapla_gelir_vergisi(gv_matrahi, kumulatif_matrah_onceki=0):
    """
    Gelir vergisini kümülatif olarak hesaplar.

    Türkiye'de gelir vergisi yıl başından itibaren kümülatif hesaplanır.
    Her ay, o ana kadarki toplam matrah üzerinden vergi hesaplanır,
    önceki aylarda ödenen vergi düşülür.

    Parametreler:
        gv_matrahi: Bu ayki gelir vergisi matrahı (TL)
        kumulatif_matrah_onceki: Önceki aylardan devir matrah (TL)

    Döndürür:
        dict: Vergi detayları

    Örnek (PDF'den - Ocak ayı, önceki matrah 0):
        GV Matrahı: 32406.71 -> Vergi: 4861.01 (tamamı %15 diliminde)
    """
    # Kümülatif matrah hesapla
    kumulatif_matrah_yeni = kumulatif_matrah_onceki + gv_matrahi

    # Yeni kümülatif matrah üzerinden toplam vergiyi hesapla
    toplam_vergi_yeni = _hesapla_dilimli_vergi(kumulatif_matrah_yeni)

    # Önceki kümülatif matrah üzerinden ödenen vergiyi hesapla
    toplam_vergi_onceki = _hesapla_dilimli_vergi(kumulatif_matrah_onceki)

    # Bu ayki vergi = Yeni toplam - Önceki toplam
    bu_ayki_vergi = toplam_vergi_yeni - toplam_vergi_onceki

    return {
        'gv_matrahi': yuvarla(gv_matrahi),
        'kumulatif_matrah_onceki': yuvarla(kumulatif_matrah_onceki),
        'kumulatif_matrah_yeni': yuvarla(kumulatif_matrah_yeni),
        'hesaplanan_vergi': yuvarla(bu_ayki_vergi),
    }


def _hesapla_dilimli_vergi(matrah):
    """
    Vergi dilimlerine göre vergi hesaplar (dahili fonksiyon).

    Parametreler:
        matrah: Gelir vergisi matrahı (TL)

    Döndürür:
        Hesaplanan vergi (TL)
    """
    if matrah <= 0:
        return 0.0

    toplam_vergi = 0.0
    kalan_matrah = matrah
    onceki_limit = 0.0

    for ust_limit, oran in c.GELIR_VERGISI_DILIMLERI:
        if ust_limit is None:
            # Son dilim (sınırsız)
            dilim_matrahi = kalan_matrah
        else:
            # Bu dilimdeki matrah
            dilim_genisligi = ust_limit - onceki_limit
            dilim_matrahi = min(kalan_matrah, dilim_genisligi)

        # Bu dilimdeki vergi
        dilim_vergisi = dilim_matrahi * (oran / 100)
        toplam_vergi += dilim_vergisi

        # Kalan matrahı güncelle
        kalan_matrah -= dilim_matrahi

        if kalan_matrah <= 0:
            break

        if ust_limit is not None:
            onceki_limit = ust_limit

    return yuvarla(toplam_vergi)


# ==========================================
# 3. ASGARİ ÜCRET İSTİSNASI
# ==========================================

def hesapla_asgari_ucret_gv_matrahi():
    """
    Asgari ücretin gelir vergisi matrahını hesaplar.

    Asgari Ücret GV Matrahı = Brüt Asgari Ücret - SGK(%14) - İşsizlik(%1)

    Bu değer, asgari ücret istisnası hesaplamasında kullanılır.

    Döndürür:
        Asgari ücret GV matrahı (TL)

    Örnek (PDF'den):
        33030.00 - 4624.20 - 330.30 = 28075.50
    """
    brut = c.ASGARI_UCRET_BRUT
    sgk_kesinti = brut * (c.SGK_ISCI_ORANI / 100)
    issizlik_kesinti = brut * (c.ISSIZLIK_ISCI_ORANI / 100)

    matrah = brut - sgk_kesinti - issizlik_kesinti
    return yuvarla(matrah)


def hesapla_asgari_ucret_istisnasi(kumulatif_asgari_matrah_onceki=0):
    """
    Asgari ücret gelir vergisi istisnasını hesaplar.

    2024'ten itibaren AGİ (Asgari Geçim İndirimi) kalktı.
    Yerine, asgari ücretin vergisi kadar istisna uygulanıyor.

    Kümülatif hesaplanır (yıl içinde dilim değişebilir).

    Parametreler:
        kumulatif_asgari_matrah_onceki: Önceki ayların asgari ücret matrah toplamı

    Döndürür:
        dict: İstisna detayları

    Örnek (PDF'den - Ocak ayı):
        Asgari GV Matrahı: 28075.50
        İstisna Vergi: 28075.50 × %15 = 4211.33
    """
    # Bu ayki asgari ücret GV matrahı
    bu_ayki_asgari_matrah = hesapla_asgari_ucret_gv_matrahi()

    # Kümülatif asgari ücret matrahı
    kumulatif_asgari_matrah_yeni = kumulatif_asgari_matrah_onceki + bu_ayki_asgari_matrah

    # Yeni kümülatif matrah üzerinden istisna vergiyi hesapla
    istisna_vergi_yeni = _hesapla_dilimli_vergi(kumulatif_asgari_matrah_yeni)

    # Önceki kümülatif matrah üzerinden istisna vergiyi hesapla
    istisna_vergi_onceki = _hesapla_dilimli_vergi(kumulatif_asgari_matrah_onceki)

    # Bu ayki istisna = Yeni toplam - Önceki toplam
    bu_ayki_istisna = istisna_vergi_yeni - istisna_vergi_onceki

    return {
        'asgari_ucret_gv_matrahi': bu_ayki_asgari_matrah,
        'kumulatif_asgari_matrah_onceki': yuvarla(kumulatif_asgari_matrah_onceki),
        'kumulatif_asgari_matrah_yeni': yuvarla(kumulatif_asgari_matrah_yeni),
        'istisna_vergi': yuvarla(bu_ayki_istisna),
    }


def hesapla_odenecek_gelir_vergisi(hesaplanan_vergi, istisna_vergi):
    """
    Ödenecek gelir vergisini hesaplar.

    Ödenecek GV = Hesaplanan GV - İstisna GV

    Not: Sonuç negatif çıkarsa 0 kabul edilir.

    Parametreler:
        hesaplanan_vergi: Hesaplanan gelir vergisi (TL)
        istisna_vergi: Asgari ücret istisna vergisi (TL)

    Döndürür:
        Ödenecek gelir vergisi (TL)

    Örnek (PDF'den):
        4861.01 - 4211.33 = 649.68
    """
    odenecek = hesaplanan_vergi - istisna_vergi

    # Negatif olamaz
    if odenecek < 0:
        odenecek = 0

    return yuvarla(odenecek)


# ==========================================
# 4. DAMGA VERGİSİ HESAPLAMALARI
# ==========================================

def hesapla_damga_vergisi(brut_kazanc):
    """
    Damga vergisini hesaplar.

    Damga Vergisi = Brüt Kazanç × Binde 7.59 (%0.759)

    Asgari ücret kadar kısım istisna olduğundan,
    sadece asgari ücreti aşan kısım üzerinden hesaplanır.

    Parametreler:
        brut_kazanc: Toplam brüt kazanç (TL)

    Döndürür:
        dict: Damga vergisi detayları

    Örnek (PDF'den):
        Brüt: 40234.54, Asgari: 33030.00
        DV Matrahı: 40234.54 - 33030.00 = 7204.54
        Ödenecek DV: 7204.54 × 0.00759 = 54.68
    """
    # Hesaplanan DV (toplam brüt üzerinden)
    hesaplanan_dv = brut_kazanc * (c.DAMGA_VERGISI_ORANI / 100)

    # İstisna DV (asgari ücret üzerinden)
    istisna_dv = c.ASGARI_UCRET_BRUT * (c.DAMGA_VERGISI_ORANI / 100)

    # Ödenecek DV = Hesaplanan - İstisna
    odenecek_dv = hesaplanan_dv - istisna_dv

    # Negatif olamaz
    if odenecek_dv < 0:
        odenecek_dv = 0

    # DV Matrahı (asgari ücreti aşan kısım)
    dv_matrahi = brut_kazanc - c.ASGARI_UCRET_BRUT
    if dv_matrahi < 0:
        dv_matrahi = 0

    return {
        'brut_kazanc': yuvarla(brut_kazanc),
        'dv_matrahi': yuvarla(dv_matrahi),
        'hesaplanan_dv': yuvarla(hesaplanan_dv),
        'istisna_dv': yuvarla(istisna_dv),
        'odenecek_dv': yuvarla(odenecek_dv),
    }


# ==========================================
# 5. FAZLA MESAİ HESAPLAMALARI
# ==========================================

def hesapla_saatlik_ucret(aylik_brut_ucret):
    """
    Saatlik ücreti hesaplar.

    Saatlik Ücret = Aylık Brüt / 225

    225 = Aylık çalışma saati (haftalık 45 saat × 30/7 gün)

    Parametreler:
        aylik_brut_ucret: Aylık brüt ücret (TL)

    Döndürür:
        Saatlik ücret (TL)

    Örnek:
        33030 / 225 = 146.80 TL
    """
    saatlik = aylik_brut_ucret / c.AYLIK_SAAT
    return yuvarla(saatlik)


def hesapla_fazla_mesai(aylik_brut_ucret, fm01_saat=0, fm02_saat=0, fm03_saat=0):
    """
    Fazla mesai ücretlerini hesaplar.

    FM01 (%50 zamlı): Normal fazla mesai - Saatlik × 1.5 × Saat
    FM02 (%100 zamlı): Hafta sonu mesaisi - Saatlik × 2.0 × Saat
    FM03 (%200 zamlı): Resmi tatil mesaisi - Saatlik × 3.0 × Saat

    Parametreler:
        aylik_brut_ucret: Aylık brüt ücret (TL)
        fm01_saat: FM01 fazla mesai saati
        fm02_saat: FM02 fazla mesai saati
        fm03_saat: FM03 fazla mesai saati

    Döndürür:
        dict: Fazla mesai detayları

    Örnek (PDF'den):
        Saatlik: 146.80 TL
        FM01: 146.80 × 1.5 × 11 = 2422.20 TL
        FM02: 146.80 × 2.0 × 11 = 3229.60 TL
        FM03: 146.80 × 3.0 × 1 = 440.40 TL
    """
    saatlik_ucret = hesapla_saatlik_ucret(aylik_brut_ucret)

    # FM01: %50 zamlı (× 1.5)
    fm01_oran = 1 + (c.FAZLA_MESAI_ORANLARI['FM01'] / 100)  # 1.5
    fm01_ucret = saatlik_ucret * fm01_oran * fm01_saat

    # FM02: %100 zamlı (× 2.0)
    fm02_oran = 1 + (c.FAZLA_MESAI_ORANLARI['FM02'] / 100)  # 2.0
    fm02_ucret = saatlik_ucret * fm02_oran * fm02_saat

    # FM03: %200 zamlı (× 3.0)
    fm03_oran = 1 + (c.FAZLA_MESAI_ORANLARI['FM03'] / 100)  # 3.0
    fm03_ucret = saatlik_ucret * fm03_oran * fm03_saat

    # Toplam
    toplam_saat = fm01_saat + fm02_saat + fm03_saat
    toplam_ucret = fm01_ucret + fm02_ucret + fm03_ucret

    return {
        'saatlik_ucret': saatlik_ucret,
        'fm01': {
            'oran': c.FAZLA_MESAI_ORANLARI['FM01'],
            'saat': fm01_saat,
            'ucret': yuvarla(fm01_ucret),
        },
        'fm02': {
            'oran': c.FAZLA_MESAI_ORANLARI['FM02'],
            'saat': fm02_saat,
            'ucret': yuvarla(fm02_ucret),
        },
        'fm03': {
            'oran': c.FAZLA_MESAI_ORANLARI['FM03'],
            'saat': fm03_saat,
            'ucret': yuvarla(fm03_ucret),
        },
        'toplam_saat': toplam_saat,
        'toplam_ucret': yuvarla(toplam_ucret),
    }


# ==========================================
# 6. NET ÜCRET HESAPLAMA
# ==========================================

def hesapla_net_ucret(brut_kazanc, isci_sgk, isci_issizlik, isci_bes,
                      odenecek_gv, odenecek_dv, ozel_sigorta_kesintisi=0,
                      ek_kesintiler=0):
    """
    Net ücreti hesaplar.

    Net Ücret = Brüt Kazanç - Tüm Kesintiler

    Kesintiler:
    - İşçi SGK Primi
    - İşçi İşsizlik Primi
    - BES Kesintisi
    - Ödenecek Gelir Vergisi
    - Ödenecek Damga Vergisi
    - Özel Sigorta Kesintileri (Sağlık + Hayat primi ödemeleri)
    - Ek Kesintiler (İcra, nafaka vb.)

    Parametreler:
        brut_kazanc: Toplam brüt kazanç (TL)
        isci_sgk: İşçi SGK primi (TL)
        isci_issizlik: İşçi işsizlik primi (TL)
        isci_bes: BES kesintisi (TL)
        odenecek_gv: Ödenecek gelir vergisi (TL)
        odenecek_dv: Ödenecek damga vergisi (TL)
        ozel_sigorta_kesintisi: Özel sigorta kesintileri toplamı (TL)
        ek_kesintiler: Ek kesintiler toplamı (TL)

    Döndürür:
        dict: Net ücret detayları

    Örnek (PDF'den):
        Brüt: 40234.54
        SGK: 5646.97, İşsizlik: 403.36, BES: 1210.00
        GV: 649.68, DV: 54.68
        Özel Sigorta: 2222.00
        Yasal Kesinti: 7964.69
        Net: 30047.85
    """
    # Yasal kesintiler toplamı
    yasal_kesintiler = isci_sgk + isci_issizlik + isci_bes + odenecek_gv + odenecek_dv

    # Tüm kesintiler toplamı
    toplam_kesintiler = yasal_kesintiler + ozel_sigorta_kesintisi + ek_kesintiler

    # Net ücret
    net_ucret = brut_kazanc - toplam_kesintiler

    return {
        'brut_kazanc': yuvarla(brut_kazanc),
        'isci_sgk': yuvarla(isci_sgk),
        'isci_issizlik': yuvarla(isci_issizlik),
        'isci_bes': yuvarla(isci_bes),
        'odenecek_gv': yuvarla(odenecek_gv),
        'odenecek_dv': yuvarla(odenecek_dv),
        'yasal_kesintiler': yuvarla(yasal_kesintiler),
        'ozel_sigorta_kesintisi': yuvarla(ozel_sigorta_kesintisi),
        'ek_kesintiler': yuvarla(ek_kesintiler),
        'toplam_kesintiler': yuvarla(toplam_kesintiler),
        'net_ucret': yuvarla(net_ucret),
    }


def hesapla_isveren_maliyeti(brut_kazanc, isveren_sgk, isveren_kvsk,
                             isveren_issizlik, hazine_yardimi=0, tesvikler=0):
    """
    İşveren maliyetini hesaplar.

    İşveren Maliyeti = Brüt Kazanç + İşveren Primleri - Teşvikler

    Parametreler:
        brut_kazanc: Toplam brüt kazanç (TL)
        isveren_sgk: İşveren SGK primi (TL)
        isveren_kvsk: Kısa vadeli sigorta kolları primi (TL)
        isveren_issizlik: İşveren işsizlik primi (TL)
        hazine_yardimi: 5 puanlık hazine yardımı (TL)
        tesvikler: Diğer teşvikler (TL)

    Döndürür:
        dict: Maliyet detayları

    Örnek (PDF'den):
        Brüt: 40234.54
        İşveren SGK: 7865.43 + KVSK: 907.55 + İşsizlik: 806.71 = 9579.69
        Hazine Yardımı: -806.71
        Maliyet: 49007.52
    """
    # İşveren primleri toplamı
    isveren_primleri = isveren_sgk + isveren_kvsk + isveren_issizlik

    # Toplam maliyet
    maliyet = brut_kazanc + isveren_primleri - hazine_yardimi - tesvikler

    return {
        'brut_kazanc': yuvarla(brut_kazanc),
        'isveren_sgk': yuvarla(isveren_sgk),
        'isveren_kvsk': yuvarla(isveren_kvsk),
        'isveren_issizlik': yuvarla(isveren_issizlik),
        'isveren_primleri_toplam': yuvarla(isveren_primleri),
        'hazine_yardimi': yuvarla(hazine_yardimi),
        'tesvikler': yuvarla(tesvikler),
        'toplam_maliyet': yuvarla(maliyet),
    }


# ==========================================
# 7. ANA BORDRO HESAPLAMA FONKSİYONU
# ==========================================

def hesapla_bordro(
        # Temel bilgiler
        aylik_brut_ucret,
        ay=1,
        yil=2026,

        # Çalışma bilgileri
        calisan_gun=30,
        ay_gun_sayisi=30,
        eksik_saat=0,

        # Kümülatif matrahlar (önceki aylardan devir)
        kumulatif_gv_matrahi=0,
        kumulatif_asgari_gv_matrahi=0,

        # SGK devir matrahları
        onceki_donem_brut=0,
        iki_onceki_donem_brut=0,

        # Fazla mesailer
        fm01_saat=0,
        fm02_saat=0,
        fm03_saat=0,
        fm_baz_ucret=None,

        # Özel sigortalar
        saglik_sigorta_primi=0,
        hayat_sigorta_primi=0,
        saglik_sigorta_kesinti=None,
        hayat_sigorta_kesinti=None,
        saglik_sigorta_isveren_kesinti=None,
        hayat_sigorta_isveren_kesinti=None,

        # Ek ödemeler
        ek_odemeler=0,

        # Ek kesintiler
        ek_kesintiler=0,

        # Seçenekler
        gelir_vergisi_hesaplansin=True,
        damga_vergisi_hesaplansin=True,
        bes_aktif=True,
        hazine_yardimi_aktif=True,
        engellilik_derecesi=None,  # None, '1', '2', '3'
):
    """
    Tam bordro hesaplaması yapar.

    Bu fonksiyon tüm bordro hesaplama adımlarını sırasıyla çalıştırır
    ve detaylı bir sonuç döndürür.

    Parametreler:
        aylik_brut_ucret: Aylık brüt temel ücret (TL)
        ay: Bordro ayı (1-12)
        yil: Bordro yılı
        calisan_gun: Çalışılan gün sayısı
        ay_gun_sayisi: Ayın toplam gün sayısı (28-31)
        eksik_saat: Eksik çalışılan saat
        kumulatif_gv_matrahi: Önceki aylardan devir GV matrahı
        kumulatif_asgari_gv_matrahi: Önceki aylardan devir asgari ücret GV matrahı
        onceki_donem_brut: Önceki aydan devir SGK matrahı
        iki_onceki_donem_brut: İki önceki aydan devir SGK matrahı
        fm01_saat: FM01 fazla mesai saati (%50 zamlı)
        fm02_saat: FM02 fazla mesai saati (%100 zamlı)
        fm03_saat: FM03 fazla mesai saati (%200 zamlı)
        saglik_sigorta_primi: Özel sağlık sigortası primi (TL)
        hayat_sigorta_primi: Özel hayat sigortası primi (TL)
        ek_odemeler: Ek ödemeler toplamı (TL)
        ek_kesintiler: Ek kesintiler toplamı (TL)
        gelir_vergisi_hesaplansin: GV hesaplansın mı?
        damga_vergisi_hesaplansin: DV hesaplansın mı?
        bes_aktif: BES kesintisi yapılsın mı?
        hazine_yardimi_aktif: Hazine yardımı uygulansın mı?
        engellilik_derecesi: Engellilik derecesi (None, '1', '2', '3')

    Döndürür:
        dict: Tüm bordro detaylarını içeren sözlük
    """

    # ==========================================
    # ADIM 1: TEMEL ÜCRET HESABI
    # ==========================================

    # Günlük ücret
    gunluk_ucret = aylik_brut_ucret / ay_gun_sayisi

    # Çalışılan ücret
    calisilan_ucret = gunluk_ucret * calisan_gun

    # Eksik saat ücreti (ay gün sayısına göre dinamik hesaplanır)
    # Saatlik Ücret = Aylık Brüt / (Ay Gün Sayısı × 7.5)
    aylik_saat_dinamik = ay_gun_sayisi * 7.5
    saatlik_ucret_eksik = aylik_brut_ucret / aylik_saat_dinamik
    eksik_saat_ucreti = saatlik_ucret_eksik * eksik_saat

    # Fazla mesai için saatlik ücret (sabit 225 saat)
    saatlik_ucret = hesapla_saatlik_ucret(aylik_brut_ucret)

    # Bu ayki temel ücret
    bu_ayki_temel_ucret = calisilan_ucret - eksik_saat_ucreti

    # ==========================================
    # ADIM 2: FAZLA MESAİ HESABI
    # ==========================================

    fazla_mesai_baz = fm_baz_ucret if fm_baz_ucret is not None else aylik_brut_ucret
    fazla_mesai = hesapla_fazla_mesai(
        aylik_brut_ucret=fazla_mesai_baz,
        fm01_saat=fm01_saat,
        fm02_saat=fm02_saat,
        fm03_saat=fm03_saat
    )

    # ==========================================
    # ADIM 3: TOPLAM BRÜT KAZANÇ
    # ==========================================

    toplam_brut_kazanc = bu_ayki_temel_ucret + fazla_mesai['toplam_ucret'] + ek_odemeler

    # Prime tabi brüt kazanç (özel sigorta primleri hariç)
    prime_tabi_brut = toplam_brut_kazanc + hayat_sigorta_primi

    # Brüt kazançlar toplamı (özel sigorta işveren payı dahil - PDF'deki gibi)
    # Not: Hayat sigortası işveren payı brüt kazanca eklenir
    brut_kazanclar_toplami = prime_tabi_brut + saglik_sigorta_primi

    # ==========================================
    # ADIM 4: SGK HESAPLAMALARI
    # ==========================================

    # SGK matrahı
    sgk_matrahi = hesapla_sgk_matrahi(
        brut_kazanc=prime_tabi_brut,
        onceki_donem_brut=onceki_donem_brut,
        iki_onceki_donem_brut=iki_onceki_donem_brut
    )

    # SGK primleri
    sgk_primleri = hesapla_tum_sgk_primleri(
        sgk_matrahi=sgk_matrahi,
        bes_aktif=bes_aktif,
        hazine_yardimi_aktif=hazine_yardimi_aktif
    )

    # ==========================================
    # ADIM 5: ÖZEL SİGORTA İNDİRİMLERİ
    # ==========================================
    # Kesinti tutarları
    saglik_isci = saglik_sigorta_kesinti if saglik_sigorta_kesinti is not None else 0
    saglik_isveren = saglik_sigorta_isveren_kesinti if saglik_sigorta_isveren_kesinti is not None else 0
    hayat_isci = hayat_sigorta_kesinti if hayat_sigorta_kesinti is not None else 0
    hayat_isveren = hayat_sigorta_isveren_kesinti if hayat_sigorta_isveren_kesinti is not None else 0

    sigorta_indirimleri = hesapla_ozel_sigorta_indirimi(
        brut_ucret=brut_kazanclar_toplami,
        saglik_sigorta_primi=saglik_sigorta_primi,
        hayat_sigorta_primi=hayat_sigorta_primi,
        saglik_sigorta_kesinti=saglik_isci,
        hayat_sigorta_kesinti=hayat_isci,
        saglik_sigorta_isveren_kesinti=saglik_isveren,
        hayat_sigorta_isveren_kesinti=hayat_isveren
    )

    # ==========================================
    # ADIM 6: ENGELLİLİK İNDİRİMİ
    # ==========================================

    engellilik_indirimi = 0
    if engellilik_derecesi and engellilik_derecesi in c.ENGELLILIK_INDIRIMI:
        engellilik_indirimi = c.ENGELLILIK_INDIRIMI[engellilik_derecesi]

    # ==========================================
    # ADIM 7: GELİR VERGİSİ MATRAHI
    # ==========================================

    # SGK kesintileri (BES hariç - sadece SGK + İşsizlik)
    sgk_kesintileri_gv_icin = sgk_primleri['isci_sgk'] + sgk_primleri['isci_issizlik']

    gv_matrahi = hesapla_gelir_vergisi_matrahi(
        brut_kazanc=brut_kazanclar_toplami,
        sgk_kesintileri=sgk_kesintileri_gv_icin,
        saglik_sigorta_indirimi=sigorta_indirimleri['saglik_indirim'],
        hayat_sigorta_indirimi=sigorta_indirimleri['hayat_indirim'],
        engellilik_indirimi=engellilik_indirimi
    )

    # ==========================================
    # ADIM 8: GELİR VERGİSİ HESABI
    # ==========================================

    if gelir_vergisi_hesaplansin:
        # Hesaplanan gelir vergisi
        gv_hesabi = hesapla_gelir_vergisi(
            gv_matrahi=gv_matrahi,
            kumulatif_matrah_onceki=kumulatif_gv_matrahi
        )

        # Asgari ücret istisnası
        istisna = hesapla_asgari_ucret_istisnasi(
            kumulatif_asgari_matrah_onceki=kumulatif_asgari_gv_matrahi
        )

        # Ödenecek gelir vergisi
        odenecek_gv = hesapla_odenecek_gelir_vergisi(
            hesaplanan_vergi=gv_hesabi['hesaplanan_vergi'],
            istisna_vergi=istisna['istisna_vergi']
        )
    else:
        gv_hesabi = {
            'gv_matrahi': 0,
            'kumulatif_matrah_onceki': 0,
            'kumulatif_matrah_yeni': 0,
            'hesaplanan_vergi': 0,
        }
        istisna = {
            'asgari_ucret_gv_matrahi': 0,
            'kumulatif_asgari_matrah_onceki': 0,
            'kumulatif_asgari_matrah_yeni': 0,
            'istisna_vergi': 0,
        }
        odenecek_gv = 0

    # ==========================================
    # ADIM 9: DAMGA VERGİSİ HESABI
    # ==========================================

    if damga_vergisi_hesaplansin:
        dv_hesabi = hesapla_damga_vergisi(brut_kazanc=brut_kazanclar_toplami)
        odenecek_dv = dv_hesabi['odenecek_dv']
    else:
        dv_hesabi = {
            'brut_kazanc': 0,
            'dv_matrahi': 0,
            'hesaplanan_dv': 0,
            'istisna_dv': 0,
            'odenecek_dv': 0,
        }
        odenecek_dv = 0

    # ==========================================
    # ADIM 10: ÖZEL SİGORTA KESİNTİLERİ
    # ==========================================

    saglik_kesinti = saglik_sigorta_kesinti if saglik_sigorta_kesinti is not None else saglik_sigorta_primi
    hayat_kesinti = hayat_sigorta_kesinti if hayat_sigorta_kesinti is not None else hayat_sigorta_primi

    ozel_sigorta_kesintisi = saglik_kesinti + hayat_kesinti

    # ==========================================
    # ADIM 11: NET ÜCRET HESABI
    # ==========================================

    net_hesabi = hesapla_net_ucret(
        brut_kazanc=brut_kazanclar_toplami,
        isci_sgk=sgk_primleri['isci_sgk'],
        isci_issizlik=sgk_primleri['isci_issizlik'],
        isci_bes=sgk_primleri['isci_bes'],
        odenecek_gv=odenecek_gv,
        odenecek_dv=odenecek_dv,
        ozel_sigorta_kesintisi=ozel_sigorta_kesintisi,
        ek_kesintiler=ek_kesintiler
    )

    # ==========================================
    # ADIM 12: İŞVEREN MALİYETİ
    # ==========================================

    maliyet = hesapla_isveren_maliyeti(
        brut_kazanc=brut_kazanclar_toplami,
        isveren_sgk=sgk_primleri['isveren_sgk'],
        isveren_kvsk=sgk_primleri['isveren_kvsk'],
        isveren_issizlik=sgk_primleri['isveren_issizlik'],
        hazine_yardimi=sgk_primleri['hazine_yardimi']
    )

    # ==========================================
    # SONUÇ
    # ==========================================

    return {
        # Bordro bilgileri
        'donem': {
            'ay': ay,
            'ay_adi': c.AYLAR.get(ay, ''),
            'yil': yil,
        },

        # Temel ücret bilgileri
        'temel_ucret': {
            'aylik_brut': yuvarla(aylik_brut_ucret),
            'gunluk_ucret': yuvarla(gunluk_ucret),
            'saatlik_ucret': saatlik_ucret,
            'calisan_gun': calisan_gun,
            'ay_gun_sayisi': ay_gun_sayisi,
            'calisilan_ucret': yuvarla(calisilan_ucret),
            'eksik_saat': eksik_saat,
            'eksik_saat_ucreti': yuvarla(eksik_saat_ucreti),
            'bu_ayki_temel_ucret': yuvarla(bu_ayki_temel_ucret),
        },

        # Fazla mesai
        'fazla_mesai': fazla_mesai,

        # Ek ödemeler
        'ek_odemeler': yuvarla(ek_odemeler),

        # Brüt kazançlar
        'brut_kazanclar': {
            'temel_ucret': yuvarla(bu_ayki_temel_ucret),
            'fazla_mesai': fazla_mesai['toplam_ucret'],
            'ek_odemeler': yuvarla(ek_odemeler),
            'prime_tabi_brut': yuvarla(prime_tabi_brut),
            'toplam_brut': yuvarla(brut_kazanclar_toplami),
        },

        # SGK bilgileri
        'sgk': {
            'matrah': sgk_matrahi,
            'onceki_donem_brut': yuvarla(onceki_donem_brut),
            'iki_onceki_donem_brut': yuvarla(iki_onceki_donem_brut),
            'primler': sgk_primleri,
        },

        # Özel sigorta
        'ozel_sigorta': {
            'saglik_primi': yuvarla(saglik_sigorta_primi),
            'hayat_primi': yuvarla(hayat_sigorta_primi),
            'toplam_prim': yuvarla(ozel_sigorta_kesintisi),
            'indirimleri': sigorta_indirimleri,
        },

        # Engellilik
        'engellilik': {
            'derece': engellilik_derecesi,
            'indirim': yuvarla(engellilik_indirimi),
        },

        # Gelir vergisi
        'gelir_vergisi': {
            'matrah': yuvarla(gv_matrahi),
            'hesaplanan': gv_hesabi['hesaplanan_vergi'],
            'kumulatif_matrah_onceki': gv_hesabi['kumulatif_matrah_onceki'],
            'kumulatif_matrah_yeni': gv_hesabi['kumulatif_matrah_yeni'],
            'istisna': istisna,
            'odenecek': odenecek_gv,
        },

        # Damga vergisi
        'damga_vergisi': dv_hesabi,

        # Kesintiler
        'kesintiler': {
            'yasal': net_hesabi['yasal_kesintiler'],
            'ozel_sigorta': net_hesabi['ozel_sigorta_kesintisi'],
            'ek_kesintiler': net_hesabi['ek_kesintiler'],
            'toplam': net_hesabi['toplam_kesintiler'],
        },

        # Net ücret
        'net_ucret': net_hesabi['net_ucret'],

        # İşveren maliyeti
        'isveren_maliyeti': maliyet,
    }