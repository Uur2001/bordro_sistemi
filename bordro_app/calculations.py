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


def hesapla_sgk_isci_primi(sgk_matrahi, oran=None):
    """
    İşçi SGK primini hesaplar.

    Parametreler:
        sgk_matrahi: SGK matrahı (TL)
        oran: SGK işçi oranı (varsayılan: constants'tan alınır)

    Döndürür:
        İşçi SGK primi (TL)
    """
    if oran is None:
        oran = c.SGK_ISCI_ORANI
    prim = sgk_matrahi * (oran / 100)
    return yuvarla(prim)


def hesapla_issizlik_isci_primi(sgk_matrahi, oran=None):
    """
    İşçi işsizlik sigortası primini hesaplar.

    Parametreler:
        sgk_matrahi: SGK matrahı (TL)
        oran: İşsizlik işçi oranı (varsayılan: constants'tan alınır)

    Döndürür:
        İşçi işsizlik primi (TL)
    """
    if oran is None:
        oran = c.ISSIZLIK_ISCI_ORANI
    prim = sgk_matrahi * (oran / 100)
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


def hesapla_sgk_isveren_primi(sgk_matrahi, oran=None):
    """
    İşveren SGK primini hesaplar.

    Parametreler:
        sgk_matrahi: SGK matrahı (TL)
        oran: SGK işveren oranı (varsayılan: constants'tan alınır)

    Döndürür:
        İşveren SGK primi (TL)
    """
    if oran is None:
        oran = c.SGK_ISVEREN_ORANI
    prim = sgk_matrahi * (oran / 100)
    return yuvarla(prim)


def hesapla_kvsk_primi(sgk_matrahi, oran=None):
    """
    Kısa Vadeli Sigorta Kolları primini hesaplar (İşveren).

    Parametreler:
        sgk_matrahi: SGK matrahı (TL)
        oran: KVSK oranı (varsayılan: constants'tan alınır)

    Döndürür:
        KVSK primi (TL)
    """
    if oran is None:
        oran = c.SGK_KVSK_ORANI
    prim = sgk_matrahi * (oran / 100)
    return yuvarla(prim)


def hesapla_issizlik_isveren_primi(sgk_matrahi, oran=None):
    """
    İşveren işsizlik sigortası primini hesaplar.

    Parametreler:
        sgk_matrahi: SGK matrahı (TL)
        oran: İşsizlik işveren oranı (varsayılan: constants'tan alınır)

    Döndürür:
        İşveren işsizlik primi (TL)
    """
    if oran is None:
        oran = c.ISSIZLIK_ISVEREN_ORANI
    prim = sgk_matrahi * (oran / 100)
    return yuvarla(prim)


def hesapla_hazine_yardimi(sgk_matrahi, hazine_yardimi_aktif=True, oran=None):
    """
    Hazine yardımını hesaplar.

    Parametreler:
        sgk_matrahi: SGK matrahı (TL)
        hazine_yardimi_aktif: Hazine yardımı uygulanacak mı?
        oran: Hazine yardımı oranı (varsayılan: constants'tan alınır)

    Döndürür:
        Hazine yardımı tutarı (TL)
    """
    if not hazine_yardimi_aktif:
        return 0.0

    if oran is None:
        oran = c.HAZINE_YARDIMI_ORANI

    # Oran 0 ise yardım yok
    if oran == 0:
        return 0.0

    yardim = sgk_matrahi * (oran / 100)
    return yuvarla(yardim)


def hesapla_tum_sgk_primleri(sgk_matrahi, sgk_tipi='1', bes_aktif=True, hazine_yardimi_aktif=True):
    """
    Tüm SGK primlerini tek seferde hesaplar.

    Parametreler:
        sgk_matrahi: SGK matrahı (TL)
        sgk_tipi: SGK belge tipi kodu (varsayılan: '1')
        bes_aktif: BES kesintisi yapılacak mı?
        hazine_yardimi_aktif: Hazine yardımı uygulanacak mı?

    Döndürür:
        dict: Tüm SGK primlerini içeren sözlük
    """
    # SGK tipine göre oranları al
    oranlar = c.get_sgk_oranlari(sgk_tipi)

    # İşçi primleri
    isci_sgk = hesapla_sgk_isci_primi(sgk_matrahi, oranlar['sgk_isci'])
    isci_issizlik = hesapla_issizlik_isci_primi(sgk_matrahi, oranlar['issizlik_isci'])
    isci_bes = hesapla_bes_kesintisi(sgk_matrahi, bes_aktif)
    isci_toplam = yuvarla(isci_sgk + isci_issizlik + isci_bes)

    # İşveren primleri
    isveren_sgk = hesapla_sgk_isveren_primi(sgk_matrahi, oranlar['sgk_isveren'])
    isveren_kvsk = hesapla_kvsk_primi(sgk_matrahi, oranlar['kvsk'])
    isveren_issizlik = hesapla_issizlik_isveren_primi(sgk_matrahi, oranlar['issizlik_isveren'])

    # Hazine yardımı (SGK tipine göre oran değişebilir)
    hazine_yardimi = hesapla_hazine_yardimi(
        sgk_matrahi,
        hazine_yardimi_aktif,
        oranlar['hazine_yardimi']
    )

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
        'sgk_tipi': sgk_tipi,
        'oranlar': oranlar,
    }


# ==========================================
# 1.1. SGK TEŞVİK HESAPLAMALARI
# ==========================================

def hesapla_tesvikli_sgk(
    sgk_matrahi,
    calisan_gun=30,
    kanun_kodu=None,
    sgk_tipi='1',
    bes_aktif=True,
    hazine_yardimi_aktif=True
):
    """
    Teşvik kanunlarına göre SGK indirimlerini hesaplar.

    Bu fonksiyon, SGK teşvik kanunlarına göre işveren için
    uygulanacak indirimleri hesaplar.

    Parametreler:
        sgk_matrahi: SGK matrahı (TL) - Prime Esas Kazanç (PEK)
        calisan_gun: Çalışılan gün sayısı (gün hesaplı teşvikler için)
        kanun_kodu: Uygulanacak teşvik kanun kodu (ör: '14447', '05746')
        sgk_tipi: SGK belge tipi kodu (varsayılan: '1')
        bes_aktif: BES kesintisi yapılacak mı?
        hazine_yardimi_aktif: Hazine yardımı uygulanacak mı?

    Döndürür:
        dict: SGK primleri ve teşvik bilgileri
            - Normal SGK primleri (teşviksiz)
            - Teşvik tutarı
            - Teşvikli işveren maliyeti
            - Kanun bilgileri

    Örnek:
        # Genç istihdam teşviği (%100) - 14447
        sonuc = hesapla_tesvikli_sgk(
            sgk_matrahi=33030,  # Asgari ücret
            kanun_kodu='14447',
            sgk_tipi='1'
        )
        # sonuc['tesvik_tutari'] = 6440.85 (Asgari ücret × %19.5)
    """
    # Önce normal SGK primlerini hesapla
    normal_primler = hesapla_tum_sgk_primleri(
        sgk_matrahi=sgk_matrahi,
        sgk_tipi=sgk_tipi,
        bes_aktif=bes_aktif,
        hazine_yardimi_aktif=hazine_yardimi_aktif
    )

    # Teşvik bilgilerini al
    kanun = c.get_kanun_bilgisi(kanun_kodu)

    # Teşvik yoksa normal primleri döndür
    if kanun is None:
        normal_primler['tesvik'] = {
            'aktif': False,
            'kanun_kodu': None,
            'kanun_adi': None,
            'tesvik_tutari': 0,
            'detay': None,
        }
        return normal_primler

    # SGK oranlarını al
    oranlar = c.get_sgk_oranlari(sgk_tipi)

    # Teşvik matrahını belirle
    if kanun['matrah_tipi'] == 'pek':
        # PEK (Prime Esas Kazanç) = SGK Matrahı
        tesvik_matrahi = sgk_matrahi
    elif kanun['matrah_tipi'] == 'pek_alt_sinir':
        # PEK Alt Sınırı = Asgari Ücret
        # Matrah asgari ücretten düşükse, matrah kullanılır
        tesvik_matrahi = min(sgk_matrahi, c.ASGARI_UCRET_BRUT)
    elif kanun['matrah_tipi'] == 'gun_hesabi':
        # Gün başına hesaplama
        tesvik_tutari = yuvarla(calisan_gun * kanun['gunluk_tutar'])
        normal_primler['tesvik'] = {
            'aktif': True,
            'kanun_kodu': kanun_kodu,
            'kanun_adi': kanun['ad'],
            'aciklama': kanun['aciklama'],
            'tesvik_tutari': tesvik_tutari,
            'matrah_tipi': 'gun_hesabi',
            'calisan_gun': calisan_gun,
            'gunluk_tutar': kanun['gunluk_tutar'],
            'detay': {
                'hesaplama': f"{calisan_gun} gün × {kanun['gunluk_tutar']} TL",
            },
        }
        # İşveren toplamını güncelle
        normal_primler['tesvikli_isveren_toplam'] = yuvarla(
            normal_primler['isveren_toplam'] - tesvik_tutari
        )
        return normal_primler
    else:
        tesvik_matrahi = sgk_matrahi

    # Teşvik tutarını hesapla
    tesvik_tutari = 0
    detay = {}

    indirim_orani = kanun['indirim_orani']
    kapsam = kanun['kapsam']

    # Özel oran durumu (06486, 46486, vb. - sabit % indirim)
    if 'ozel_oran' in kapsam:
        tesvik_tutari = yuvarla(tesvik_matrahi * (indirim_orani / 100))
        detay['ozel_oran_indirimi'] = tesvik_tutari
        detay['hesaplama'] = f"Matrah × %{indirim_orani} = {tesvik_tutari}"
    else:
        # SGK İşveren hissesi indirimi
        if 'sgk_isveren' in kapsam:
            sgk_isveren_indirimi = yuvarla(
                tesvik_matrahi * (oranlar['sgk_isveren'] / 100) * (indirim_orani / 100)
            )
            tesvik_tutari += sgk_isveren_indirimi
            detay['sgk_isveren_indirimi'] = sgk_isveren_indirimi

        # SGK İşçi hissesi indirimi (nadir - 26322, 15921 gibi)
        if 'sgk_isci' in kapsam:
            sgk_isci_indirimi = yuvarla(
                tesvik_matrahi * (oranlar['sgk_isci'] / 100) * (indirim_orani / 100)
            )
            tesvik_tutari += sgk_isci_indirimi
            detay['sgk_isci_indirimi'] = sgk_isci_indirimi

        # KVSK indirimi (tamamı)
        if 'kvsk' in kapsam:
            kvsk_indirimi = yuvarla(
                tesvik_matrahi * (oranlar['kvsk'] / 100) * (indirim_orani / 100)
            )
            tesvik_tutari += kvsk_indirimi
            detay['kvsk_indirimi'] = kvsk_indirimi

        # KVSK kısmi indirimi (15921 - %1)
        if 'kvsk_kismi' in kapsam:
            kvsk_ozel_oran = kanun.get('kvsk_orani', 1)  # Varsayılan %1
            kvsk_kismi_indirimi = yuvarla(tesvik_matrahi * (kvsk_ozel_oran / 100))
            tesvik_tutari += kvsk_kismi_indirimi
            detay['kvsk_kismi_indirimi'] = kvsk_kismi_indirimi
            detay['kvsk_orani'] = kvsk_ozel_oran

        # İşsizlik İşveren indirimi
        if 'issizlik_isveren' in kapsam:
            issizlik_isveren_indirimi = yuvarla(
                tesvik_matrahi * (oranlar['issizlik_isveren'] / 100) * (indirim_orani / 100)
            )
            tesvik_tutari += issizlik_isveren_indirimi
            detay['issizlik_isveren_indirimi'] = issizlik_isveren_indirimi

        # İşsizlik İşçi indirimi
        if 'issizlik_isci' in kapsam:
            issizlik_isci_indirimi = yuvarla(
                tesvik_matrahi * (oranlar['issizlik_isci'] / 100) * (indirim_orani / 100)
            )
            tesvik_tutari += issizlik_isci_indirimi
            detay['issizlik_isci_indirimi'] = issizlik_isci_indirimi

    tesvik_tutari = yuvarla(tesvik_tutari)

    # Teşvik bilgilerini ekle
    normal_primler['tesvik'] = {
        'aktif': True,
        'kanun_kodu': kanun_kodu,
        'kanun_adi': kanun['ad'],
        'aciklama': kanun['aciklama'],
        'tesvik_tutari': tesvik_tutari,
        'matrah_tipi': kanun['matrah_tipi'],
        'tesvik_matrahi': tesvik_matrahi,
        'indirim_orani': indirim_orani,
        'kapsam': kapsam,
        'belgeler': kanun['belgeler'],
        'detay': detay,
    }

    # Teşvikli işveren toplamını hesapla
    normal_primler['tesvikli_isveren_toplam'] = yuvarla(
        normal_primler['isveren_toplam'] - tesvik_tutari
    )

    return normal_primler


def hesapla_tesvik_ozeti(sgk_matrahi, calisan_gun=30, kanun_kodlari=None, sgk_tipi='1'):
    """
    Birden fazla teşvik kanunu için karşılaştırmalı özet hesaplar.

    Parametreler:
        sgk_matrahi: SGK matrahı (TL)
        calisan_gun: Çalışılan gün sayısı
        kanun_kodlari: Liste halinde kanun kodları (None ise tüm kanunlar)
        sgk_tipi: SGK belge tipi kodu

    Döndürür:
        dict: Her kanun için teşvik tutarları ve karşılaştırma
    """
    if kanun_kodlari is None:
        kanun_kodlari = list(c.SGK_KANUNLARI.keys())

    sonuclar = {}
    for kanun_kodu in kanun_kodlari:
        sonuc = hesapla_tesvikli_sgk(
            sgk_matrahi=sgk_matrahi,
            calisan_gun=calisan_gun,
            kanun_kodu=kanun_kodu,
            sgk_tipi=sgk_tipi
        )
        sonuclar[kanun_kodu] = {
            'kanun_adi': sonuc['tesvik']['kanun_adi'],
            'tesvik_tutari': sonuc['tesvik']['tesvik_tutari'],
            'normal_isveren_toplam': sonuc['isveren_toplam'],
            'tesvikli_isveren_toplam': sonuc.get('tesvikli_isveren_toplam', sonuc['isveren_toplam']),
        }

    return sonuclar
# 2. GELİR VERGİSİ HESAPLAMALARI
# ==========================================

def hesapla_ozel_sigorta_indirimi(brut_ucret, saglik_sigorta_primi=0, hayat_sigorta_primi=0,
                                   saglik_sigorta_kesinti=0, hayat_sigorta_kesinti=0,
                                   saglik_sigorta_isveren_kesinti=0, hayat_sigorta_isveren_kesinti=0):
    """
    Özel sigorta indirimlerini hesaplar.

    Sağlık Sigortası İndirimi:
        - İşçi kesintisi + İşveren kesintisi
        - Brüt ücretin %15'ini geçemez
        - Aylık asgari ücretin brütünü geçemez

    Hayat Sigortası İndirimi:
        - Sadece İşçi kesintisi × %50 (İşveren kesintisi dahil DEĞİL)
        - Aylık asgari ücretin brütünü geçemez

    Parametreler:
        brut_ucret: Brüt ücret (TL)
        saglik_sigorta_primi: Sağlık sigortası brüt tutarı
        hayat_sigorta_primi: Hayat sigortası brüt tutarı
        saglik_sigorta_kesinti: Sağlık sigortası işçi kesintisi
        hayat_sigorta_kesinti: Hayat sigortası işçi kesintisi
        saglik_sigorta_isveren_kesinti: Sağlık sigortası işveren kesintisi
        hayat_sigorta_isveren_kesinti: Hayat sigortası işveren kesintisi

    Döndürür:
        dict: İndirim detayları
    """
    # Sağlık sigortası indirimi: İşçi kesintisi + İşveren kesintisi
    saglik_toplam = saglik_sigorta_kesinti + saglik_sigorta_isveren_kesinti

    # Limit: Brüt ücretin %15'i
    saglik_limit_yuzde = brut_ucret * (c.SAGLIK_SIGORTA_INDIRIM_ORANI / 100)

    # Limit: Aylık asgari ücret
    saglik_limit_asgari = c.ASGARI_UCRET_BRUT

    # En düşük limiti uygula
    saglik_indirim = min(saglik_toplam, saglik_limit_yuzde, saglik_limit_asgari)

    # Hayat sigortası indirimi: Sadece işçi kesintisi × %50
    hayat_indirim_ham = hayat_sigorta_kesinti * (c.HAYAT_SIGORTA_INDIRIM_ORANI / 100)

    # Limit: Aylık asgari ücret
    hayat_limit_asgari = c.ASGARI_UCRET_BRUT

    hayat_indirim = min(hayat_indirim_ham, hayat_limit_asgari)

    # Toplam indirim
    toplam_indirim = saglik_indirim + hayat_indirim

    return {
        'saglik_indirim': yuvarla(saglik_indirim),
        'hayat_indirim': yuvarla(hayat_indirim),
        'toplam_indirim': yuvarla(toplam_indirim),
    }


def hesapla_gelir_vergisi_matrahi(brut_kazanc, sgk_kesintileri, saglik_sigorta_indirimi=0,
                                   hayat_sigorta_indirimi=0, engellilik_indirimi=0):
    """
    Gelir vergisi matrahını hesaplar.

    GV Matrahı = Brüt Kazanç - SGK Kesintileri - Özel Sigorta İndirimleri - Engellilik İndirimi

    Parametreler:
        brut_kazanc: Brüt kazanç toplamı (TL)
        sgk_kesintileri: SGK + İşsizlik kesintileri toplamı (TL)
        saglik_sigorta_indirimi: Sağlık sigortası indirimi (TL)
        hayat_sigorta_indirimi: Hayat sigortası indirimi (TL)
        engellilik_indirimi: Engellilik indirimi (TL)

    Döndürür:
        Gelir vergisi matrahı (TL)
    """
    matrah = brut_kazanc - sgk_kesintileri - saglik_sigorta_indirimi - hayat_sigorta_indirimi - engellilik_indirimi

    # Matrah negatif olamaz
    if matrah < 0:
        matrah = 0

    return yuvarla(matrah)


def _hesapla_dilimli_vergi(matrah):
    """
    Kümülatif matrah üzerinden toplam vergiyi hesaplar (yardımcı fonksiyon).

    Parametreler:
        matrah: Kümülatif matrah

    Döndürür:
        Toplam vergi
    """
    if matrah <= 0:
        return 0

    toplam_vergi = 0
    onceki_limit = 0

    for ust_limit, oran in c.GELIR_VERGISI_DILIMLERI:
        if ust_limit is None:
            # Son dilim (sınırsız)
            dilim_matrahi = matrah - onceki_limit
            if dilim_matrahi > 0:
                toplam_vergi += dilim_matrahi * (oran / 100)
            break
        else:
            if matrah <= onceki_limit:
                break

            dilim_matrahi = min(matrah, ust_limit) - onceki_limit
            if dilim_matrahi > 0:
                toplam_vergi += dilim_matrahi * (oran / 100)

            onceki_limit = ust_limit

    return yuvarla(toplam_vergi)


def hesapla_gelir_vergisi(gv_matrahi, kumulatif_matrah_onceki=0):
    """
    Gelir vergisini hesaplar (kümülatif yöntemle).

    Bu ay için vergi = Yeni kümülatif vergi - Önceki kümülatif vergi

    Parametreler:
        gv_matrahi: Bu ayki GV matrahı (TL)
        kumulatif_matrah_onceki: Önceki ayların toplam GV matrahı (TL)

    Döndürür:
        dict: Vergi hesaplama detayları
    """
    # Yeni kümülatif matrah
    kumulatif_matrah_yeni = kumulatif_matrah_onceki + gv_matrahi

    # Kümülatif vergiler
    vergi_yeni = _hesapla_dilimli_vergi(kumulatif_matrah_yeni)
    vergi_onceki = _hesapla_dilimli_vergi(kumulatif_matrah_onceki)

    # Bu ayki vergi
    bu_ayki_vergi = vergi_yeni - vergi_onceki

    return {
        'gv_matrahi': yuvarla(gv_matrahi),
        'kumulatif_matrah_onceki': yuvarla(kumulatif_matrah_onceki),
        'kumulatif_matrah_yeni': yuvarla(kumulatif_matrah_yeni),
        'hesaplanan_vergi': yuvarla(bu_ayki_vergi),
    }


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
    """
    brut = c.ASGARI_UCRET_BRUT
    sgk_kesinti = brut * (c.SGK_ISCI_ORANI / 100)
    issizlik_kesinti = brut * (c.ISSIZLIK_ISCI_ORANI / 100)

    matrah = brut - sgk_kesinti - issizlik_kesinti
    return yuvarla(matrah)


def hesapla_asgari_ucret_istisnasi(kumulatif_asgari_matrah_onceki=0):
    """
    Asgari ücret gelir vergisi istisnasını hesaplar.

    Parametreler:
        kumulatif_asgari_matrah_onceki: Önceki ayların asgari ücret matrah toplamı

    Döndürür:
        dict: İstisna detayları
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
        istisna_vergi: İstisna gelir vergisi (TL)

    Döndürür:
        Ödenecek gelir vergisi (TL)
    """
    odenecek = hesaplanan_vergi - istisna_vergi

    if odenecek < 0:
        odenecek = 0

    return yuvarla(odenecek)


# ==========================================
# 4. DAMGA VERGİSİ HESAPLAMALARI
# ==========================================

def hesapla_damga_vergisi(brut_kazanc):
    """
    Damga vergisini hesaplar.

    DV = Brüt Kazanç × Binde 7.59

    Asgari ücretin altında kalan kısım için DV istisnası uygulanır.

    Parametreler:
        brut_kazanc: Brüt kazanç toplamı (TL)

    Döndürür:
        dict: DV hesaplama detayları
    """
    # Hesaplanan DV (brüt üzerinden)
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
# 6. NET ÜCRET HESABI
# ==========================================

def hesapla_net_ucret(brut_kazanc, isci_sgk, isci_issizlik, isci_bes, odenecek_gv, odenecek_dv,
                       ozel_sigorta_kesintisi=0, ek_kesintiler=0):
    """
    Net ücreti hesaplar.

    Net Ücret = Brüt Kazanç - Tüm Kesintiler

    Parametreler:
        brut_kazanc: Brüt kazanç toplamı (TL)
        isci_sgk: İşçi SGK primi (TL)
        isci_issizlik: İşçi işsizlik primi (TL)
        isci_bes: İşçi BES kesintisi (TL)
        odenecek_gv: Ödenecek gelir vergisi (TL)
        odenecek_dv: Ödenecek damga vergisi (TL)
        ozel_sigorta_kesintisi: Özel sigorta kesintileri (TL)
        ek_kesintiler: Diğer ek kesintiler (TL)

    Döndürür:
        dict: Net ücret hesaplama detayları
    """
    # Yasal kesintiler
    yasal_kesintiler = isci_sgk + isci_issizlik + isci_bes + odenecek_gv + odenecek_dv

    # Toplam kesintiler
    toplam_kesintiler = yasal_kesintiler + ozel_sigorta_kesintisi + ek_kesintiler

    # Net ücret
    net_ucret = brut_kazanc - toplam_kesintiler

    return {
        'brut_kazanc': yuvarla(brut_kazanc),
        'yasal_kesintiler': yuvarla(yasal_kesintiler),
        'ozel_sigorta_kesintisi': yuvarla(ozel_sigorta_kesintisi),
        'ek_kesintiler': yuvarla(ek_kesintiler),
        'toplam_kesintiler': yuvarla(toplam_kesintiler),
        'net_ucret': yuvarla(net_ucret),
    }


# ==========================================
# 7. İŞVEREN MALİYETİ
# ==========================================

def hesapla_isveren_maliyeti(brut_kazanc, isveren_sgk, isveren_kvsk, isveren_issizlik, hazine_yardimi=0):
    """
    İşveren maliyetini hesaplar.

    İşveren Maliyeti = Brüt Kazanç + İşveren SGK + KVSK + İşveren İşsizlik - Hazine Yardımı

    Parametreler:
        brut_kazanc: Brüt kazanç toplamı (TL)
        isveren_sgk: İşveren SGK primi (TL)
        isveren_kvsk: İşveren KVSK primi (TL)
        isveren_issizlik: İşveren işsizlik primi (TL)
        hazine_yardimi: Hazine yardımı tutarı (TL)

    Döndürür:
        dict: İşveren maliyeti detayları
    """
    # İşveren prim toplamı
    isveren_prim_toplami = isveren_sgk + isveren_kvsk + isveren_issizlik

    # Net işveren yükü (hazine yardımı düşülmüş)
    net_isveren_yuku = isveren_prim_toplami - hazine_yardimi

    # Toplam maliyet
    toplam_maliyet = brut_kazanc + net_isveren_yuku

    return {
        'brut_kazanc': yuvarla(brut_kazanc),
        'isveren_sgk': yuvarla(isveren_sgk),
        'isveren_kvsk': yuvarla(isveren_kvsk),
        'isveren_issizlik': yuvarla(isveren_issizlik),
        'isveren_prim_toplami': yuvarla(isveren_prim_toplami),
        'hazine_yardimi': yuvarla(hazine_yardimi),
        'net_isveren_yuku': yuvarla(net_isveren_yuku),
        'toplam_maliyet': yuvarla(toplam_maliyet),
    }


# ==========================================
# 8. ANA BORDRO HESAPLAMA FONKSİYONU
# ==========================================

def hesapla_bordro(
        # Temel parametreler
        aylik_brut_ucret,
        ay=1,
        yil=2026,
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

        # SGK Tipi (YENİ PARAMETRE)
        sgk_tipi='1',  # Varsayılan: Standart çalışan
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
        sgk_tipi: SGK belge tipi kodu (varsayılan: '1')

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

    # SGK primleri (SGK tipine göre dinamik oranlarla)
    sgk_primleri = hesapla_tum_sgk_primleri(
        sgk_matrahi=sgk_matrahi,
        sgk_tipi=sgk_tipi,
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
            'sgk_tipi': sgk_tipi,
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