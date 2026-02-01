from decimal import Decimal, ROUND_HALF_UP
from . import constants as c

def yuvarla(sayi, basamak=2):

    if sayi is None:
        return 0.0
    carpan = 10 ** basamak
    return round(float(sayi) * carpan) / carpan
# 1. SGK HESAPLAMALARI
def hesapla_sgk_matrahi(brut_kazanc, onceki_donem_brut=0, iki_onceki_donem_brut=0):
    toplam = brut_kazanc + onceki_donem_brut + iki_onceki_donem_brut
    if toplam > c.SGK_TAVAN:
        toplam = c.SGK_TAVAN
    return yuvarla(toplam)

def hesapla_sgk_isci_primi(sgk_matrahi, oran=None):
    if oran is None:
        oran = c.SGK_ISCI_ORANI
    prim = sgk_matrahi * (oran / 100)
    return yuvarla(prim)

def hesapla_issizlik_isci_primi(sgk_matrahi, oran=None):
    if oran is None:
        oran = c.ISSIZLIK_ISCI_ORANI
    prim = sgk_matrahi * (oran / 100)
    return yuvarla(prim)

def hesapla_bes_kesintisi(sgk_matrahi, bes_aktif=True):
    if not bes_aktif:
        return 0.0
    kesinti = sgk_matrahi * (c.BES_ORANI / 100)
    kesinti = float(int(kesinti))
    return kesinti

def hesapla_sgk_isveren_primi(sgk_matrahi, oran=None):
    if oran is None:
        oran = c.SGK_ISVEREN_ORANI
    prim = sgk_matrahi * (oran / 100)
    return yuvarla(prim)

def hesapla_kvsk_primi(sgk_matrahi, oran=None):
    if oran is None:
        oran = c.SGK_KVSK_ORANI
    prim = sgk_matrahi * (oran / 100)
    return yuvarla(prim)

def hesapla_issizlik_isveren_primi(sgk_matrahi, oran=None):
    if oran is None:
        oran = c.ISSIZLIK_ISVEREN_ORANI
    prim = sgk_matrahi * (oran / 100)
    return yuvarla(prim)

def hesapla_hazine_yardimi(sgk_matrahi, hazine_yardimi_aktif=True, oran=None):
    if not hazine_yardimi_aktif:
        return 0.0
    if oran is None:
        oran = c.HAZINE_YARDIMI_ORANI
    if oran == 0:
        return 0.0
    yardim = sgk_matrahi * (oran / 100)
    return yuvarla(yardim)

def hesapla_tum_sgk_primleri(sgk_matrahi, sgk_tipi='1', bes_aktif=True, hazine_yardimi_aktif=True):
    oranlar = c.get_sgk_oranlari(sgk_tipi)
    isci_sgk = hesapla_sgk_isci_primi(sgk_matrahi, oranlar['sgk_isci'])
    isci_issizlik = hesapla_issizlik_isci_primi(sgk_matrahi, oranlar['issizlik_isci'])
    isci_bes = hesapla_bes_kesintisi(sgk_matrahi, bes_aktif)
    isci_toplam = yuvarla(isci_sgk + isci_issizlik + isci_bes)
    isveren_sgk = hesapla_sgk_isveren_primi(sgk_matrahi, oranlar['sgk_isveren'])
    isveren_kvsk = hesapla_kvsk_primi(sgk_matrahi, oranlar['kvsk'])
    isveren_issizlik = hesapla_issizlik_isveren_primi(sgk_matrahi, oranlar['issizlik_isveren'])
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

# 1.1. SGK TEŞVİK HESAPLAMALARI
def hesapla_tesvikli_sgk(
    sgk_matrahi,
    calisan_gun=30,
    kanun_kodu=None,
    sgk_tipi='1',
    bes_aktif=True,
    hazine_yardimi_aktif=True
):
    normal_primler = hesapla_tum_sgk_primleri(
        sgk_matrahi=sgk_matrahi,
        sgk_tipi=sgk_tipi,
        bes_aktif=bes_aktif,
        hazine_yardimi_aktif=hazine_yardimi_aktif
    )

    kanun = c.get_kanun_bilgisi(kanun_kodu)
    if kanun is None:
        normal_primler['tesvik'] = {
            'aktif': False,
            'kanun_kodu': None,
            'kanun_adi': None,
            'tesvik_tutari': 0,
            'detay': None,
        }
        return normal_primler

    oranlar = c.get_sgk_oranlari(sgk_tipi)
    if kanun['matrah_tipi'] == 'pek':
        tesvik_matrahi = sgk_matrahi
    elif kanun['matrah_tipi'] == 'pek_alt_sinir':
        tesvik_matrahi = min(sgk_matrahi, c.ASGARI_UCRET_BRUT)
    elif kanun['matrah_tipi'] == 'gun_hesabi':
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

        normal_primler['tesvikli_isveren_toplam'] = yuvarla(
            normal_primler['isveren_toplam'] - tesvik_tutari
        )
        return normal_primler
    else:
        tesvik_matrahi = sgk_matrahi

    tesvik_tutari = 0
    detay = {}
    indirim_orani = kanun['indirim_orani']
    kapsam = kanun['kapsam']

    if 'ozel_oran' in kapsam:
        tesvik_tutari = yuvarla(tesvik_matrahi * (indirim_orani / 100))
        detay['ozel_oran_indirimi'] = tesvik_tutari
        detay['hesaplama'] = f"Matrah × %{indirim_orani} = {tesvik_tutari}"
    else:
        if 'sgk_isveren' in kapsam:
            isveren_orani = kanun.get('isveren_orani', oranlar['sgk_isveren'])
            sgk_isveren_indirimi = yuvarla(
                tesvik_matrahi * (isveren_orani / 100) * (indirim_orani / 100)
            )
            tesvik_tutari += sgk_isveren_indirimi
            detay['sgk_isveren_indirimi'] = sgk_isveren_indirimi

            if 'kvsk_kismi' not in kapsam:
                kvsk_indirimi = yuvarla(
                    tesvik_matrahi * (oranlar['kvsk'] / 100) * (indirim_orani / 100)
                )
                tesvik_tutari += kvsk_indirimi
                detay['kvsk_indirimi'] = kvsk_indirimi

                if indirim_orani == 100 or kanun_kodu in ['24447', '44447', '64447', '84447', '54857']:
                    hazine_dusulecek = yuvarla(
                        tesvik_matrahi * (oranlar['hazine_yardimi'] / 100) * (indirim_orani / 100)
                    )
                    tesvik_tutari -= hazine_dusulecek
                    detay['hazine_yardimi_duslen'] = hazine_dusulecek

        if 'sgk_isci' in kapsam:
            sgk_isci_indirimi = yuvarla(
                tesvik_matrahi * (oranlar['sgk_isci'] / 100) * (indirim_orani / 100)
            )
            tesvik_tutari += sgk_isci_indirimi
            detay['sgk_isci_indirimi'] = sgk_isci_indirimi

        if 'kvsk_kismi' in kapsam:
            kvsk_ozel_oran = kanun.get('kvsk_orani', 1)
            kvsk_kismi_indirimi = yuvarla(tesvik_matrahi * (kvsk_ozel_oran / 100))
            tesvik_tutari += kvsk_kismi_indirimi
            detay['kvsk_kismi_indirimi'] = kvsk_kismi_indirimi
            detay['kvsk_orani'] = kvsk_ozel_oran

        if 'issizlik_isveren' in kapsam:
            issizlik_isveren_indirimi = yuvarla(
                tesvik_matrahi * (oranlar['issizlik_isveren'] / 100) * (indirim_orani / 100)
            )
            tesvik_tutari += issizlik_isveren_indirimi
            detay['issizlik_isveren_indirimi'] = issizlik_isveren_indirimi

        if 'issizlik_isci' in kapsam:
            issizlik_isci_indirimi = yuvarla(
                tesvik_matrahi * (oranlar['issizlik_isci'] / 100) * (indirim_orani / 100)
            )
            tesvik_tutari += issizlik_isci_indirimi
            detay['issizlik_isci_indirimi'] = issizlik_isci_indirimi

    tesvik_tutari = yuvarla(tesvik_tutari)
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

    normal_primler['tesvikli_isveren_toplam'] = yuvarla(
        normal_primler['isveren_toplam'] - tesvik_tutari
    )
    return normal_primler

def hesapla_tesvik_ozeti(sgk_matrahi, calisan_gun=30, kanun_kodlari=None, sgk_tipi='1'):
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
def hesapla_ozel_sigorta_indirimi(brut_ucret, saglik_sigorta_primi=0, hayat_sigorta_primi=0,
                                   saglik_sigorta_kesinti=0, hayat_sigorta_kesinti=0,
                                   saglik_sigorta_isveren_kesinti=0, hayat_sigorta_isveren_kesinti=0):
    saglik_toplam = saglik_sigorta_kesinti + saglik_sigorta_isveren_kesinti
    saglik_limit_yuzde = brut_ucret * (c.SAGLIK_SIGORTA_INDIRIM_ORANI / 100)
    saglik_limit_asgari = c.ASGARI_UCRET_BRUT
    saglik_indirim = min(saglik_toplam, saglik_limit_yuzde, saglik_limit_asgari)
    hayat_indirim_ham = hayat_sigorta_kesinti * (c.HAYAT_SIGORTA_INDIRIM_ORANI / 100)
    hayat_limit_asgari = c.ASGARI_UCRET_BRUT
    hayat_indirim = min(hayat_indirim_ham, hayat_limit_asgari)
    toplam_indirim = saglik_indirim + hayat_indirim
    return {
        'saglik_indirim': yuvarla(saglik_indirim),
        'hayat_indirim': yuvarla(hayat_indirim),
        'toplam_indirim': yuvarla(toplam_indirim),
    }

def hesapla_gelir_vergisi_matrahi(brut_kazanc, sgk_kesintileri, saglik_sigorta_indirimi=0,
                                   hayat_sigorta_indirimi=0, engellilik_indirimi=0):
    matrah = brut_kazanc - sgk_kesintileri - saglik_sigorta_indirimi - hayat_sigorta_indirimi - engellilik_indirimi
    if matrah < 0:
        matrah = 0
    return yuvarla(matrah)

def _hesapla_dilimli_vergi(matrah):
    if matrah <= 0:
        return 0

    toplam_vergi = 0
    onceki_limit = 0
    for ust_limit, oran in c.GELIR_VERGISI_DILIMLERI:
        if ust_limit is None:
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
    kumulatif_matrah_yeni = kumulatif_matrah_onceki + gv_matrahi
    vergi_yeni = _hesapla_dilimli_vergi(kumulatif_matrah_yeni)
    vergi_onceki = _hesapla_dilimli_vergi(kumulatif_matrah_onceki)
    bu_ayki_vergi = vergi_yeni - vergi_onceki
    return {
        'gv_matrahi': yuvarla(gv_matrahi),
        'kumulatif_matrah_onceki': yuvarla(kumulatif_matrah_onceki),
        'kumulatif_matrah_yeni': yuvarla(kumulatif_matrah_yeni),
        'hesaplanan_vergi': yuvarla(bu_ayki_vergi),
    }

# 3. ASGARİ ÜCRET İSTİSNASI
def hesapla_asgari_ucret_gv_matrahi():
    brut = c.ASGARI_UCRET_BRUT
    sgk_kesinti = brut * (c.SGK_ISCI_ORANI / 100)
    issizlik_kesinti = brut * (c.ISSIZLIK_ISCI_ORANI / 100)
    matrah = brut - sgk_kesinti - issizlik_kesinti
    return yuvarla(matrah)

def hesapla_asgari_ucret_istisnasi(kumulatif_asgari_matrah_onceki=0):
    bu_ayki_asgari_matrah = hesapla_asgari_ucret_gv_matrahi()
    kumulatif_asgari_matrah_yeni = kumulatif_asgari_matrah_onceki + bu_ayki_asgari_matrah
    istisna_vergi_yeni = _hesapla_dilimli_vergi(kumulatif_asgari_matrah_yeni)
    istisna_vergi_onceki = _hesapla_dilimli_vergi(kumulatif_asgari_matrah_onceki)
    bu_ayki_istisna = istisna_vergi_yeni - istisna_vergi_onceki
    return {
        'asgari_ucret_gv_matrahi': bu_ayki_asgari_matrah,
        'kumulatif_asgari_matrah_onceki': yuvarla(kumulatif_asgari_matrah_onceki),
        'kumulatif_asgari_matrah_yeni': yuvarla(kumulatif_asgari_matrah_yeni),
        'istisna_vergi': yuvarla(bu_ayki_istisna),
    }

def hesapla_odenecek_gelir_vergisi(hesaplanan_vergi, istisna_vergi):
    odenecek = hesaplanan_vergi - istisna_vergi
    if odenecek < 0:
        odenecek = 0
    return yuvarla(odenecek)

# 4. DAMGA VERGİSİ HESAPLAMALARI
def hesapla_damga_vergisi(brut_kazanc):
    hesaplanan_dv = brut_kazanc * (c.DAMGA_VERGISI_ORANI / 100)
    istisna_dv = c.ASGARI_UCRET_BRUT * (c.DAMGA_VERGISI_ORANI / 100)
    odenecek_dv = hesaplanan_dv - istisna_dv

    if odenecek_dv < 0:
        odenecek_dv = 0
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

# 5. FAZLA MESAİ HESAPLAMALARI
def hesapla_saatlik_ucret(aylik_brut_ucret):
    saatlik = aylik_brut_ucret / c.AYLIK_SAAT
    return yuvarla(saatlik)

def hesapla_fazla_mesai(aylik_brut_ucret, fm01_saat=0, fm02_saat=0, fm03_saat=0):
    saatlik_ucret = hesapla_saatlik_ucret(aylik_brut_ucret)
    fm01_oran = 1 + (c.FAZLA_MESAI_ORANLARI['FM01'] / 100)
    fm01_ucret = saatlik_ucret * fm01_oran * fm01_saat
    fm02_oran = 1 + (c.FAZLA_MESAI_ORANLARI['FM02'] / 100)
    fm02_ucret = saatlik_ucret * fm02_oran * fm02_saat
    fm03_oran = 1 + (c.FAZLA_MESAI_ORANLARI['FM03'] / 100)
    fm03_ucret = saatlik_ucret * fm03_oran * fm03_saat
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
# 6. NET ÜCRET HESABI
def hesapla_net_ucret(brut_kazanc, isci_sgk, isci_issizlik, isci_bes, odenecek_gv, odenecek_dv,
                       ozel_sigorta_kesintisi=0, ek_kesintiler=0):
    yasal_kesintiler = isci_sgk + isci_issizlik + isci_bes + odenecek_gv + odenecek_dv
    toplam_kesintiler = yasal_kesintiler + ozel_sigorta_kesintisi + ek_kesintiler
    net_ucret = brut_kazanc - toplam_kesintiler
    return {
        'brut_kazanc': yuvarla(brut_kazanc),
        'yasal_kesintiler': yuvarla(yasal_kesintiler),
        'ozel_sigorta_kesintisi': yuvarla(ozel_sigorta_kesintisi),
        'ek_kesintiler': yuvarla(ek_kesintiler),
        'toplam_kesintiler': yuvarla(toplam_kesintiler),
        'net_ucret': yuvarla(net_ucret),
    }
# 7. İŞVEREN MALİYETİ
def hesapla_isveren_maliyeti(brut_kazanc, isveren_sgk, isveren_kvsk, isveren_issizlik, hazine_yardimi=0):
    isveren_prim_toplami = isveren_sgk + isveren_kvsk + isveren_issizlik
    net_isveren_yuku = isveren_prim_toplami - hazine_yardimi
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

def hesapla_sigorta_brutu_kesintiden(kesinti, sigorta_tipi='saglik', sgk_tipi='1', kumulatif_gv_matrahi=0, bu_ayki_brut_tahmini=0):
    if kesinti is None or kesinti <= 0:
        return 0.0

    oranlar = c.get_sgk_oranlari(sgk_tipi)
    dv_orani = c.DAMGA_VERGISI_ORANI / 100
    sgk_isci_toplam = (oranlar['sgk_isci'] + oranlar['issizlik_isci']) / 100
    tahmini_bu_ayki_gv_matrahi = bu_ayki_brut_tahmini * (1 - sgk_isci_toplam)
    toplam_gv_matrahi = kumulatif_gv_matrahi + tahmini_bu_ayki_gv_matrahi
    if toplam_gv_matrahi < 190000:
        gv_dilim_orani = 0.15
    elif toplam_gv_matrahi < 400000:
        gv_dilim_orani = 0.20
    elif toplam_gv_matrahi < 1500000:
        gv_dilim_orani = 0.27
    elif toplam_gv_matrahi < 5300000:
        gv_dilim_orani = 0.35
    else:
        gv_dilim_orani = 0.40

    if sigorta_tipi == 'saglik':
        brut = kesinti / (1 - dv_orani - 0.00134)
    elif sigorta_tipi == 'hayat':
        sgk_orani = sgk_isci_toplam
        carpan = 1 - sgk_orani - gv_dilim_orani + (sgk_orani * gv_dilim_orani) - dv_orani
        brut = kesinti / carpan
    else:
        brut = kesinti

    return yuvarla(brut)
# 8. ANA BORDRO HESAPLAMA FONKSİYONU
def hesapla_bordro(

        aylik_brut_ucret,
        ay=1,
        yil=2026,
        calisan_gun=30,
        ay_gun_sayisi=None,
        ay_gun_secimi='takvim',
        eksik_saat=0,
        kumulatif_gv_matrahi=0,
        kumulatif_asgari_gv_matrahi=0,
        onceki_donem_brut=0,
        iki_onceki_donem_brut=0,
        fm01_saat=0,
        fm02_saat=0,
        fm03_saat=0,
        fm_baz_ucret=None,
        saglik_sigorta_primi=0,
        hayat_sigorta_primi=0,
        saglik_sigorta_kesinti=None,
        hayat_sigorta_kesinti=None,
        saglik_sigorta_isveren_kesinti=None,
        hayat_sigorta_isveren_kesinti=None,
        ek_odemeler=0,
        ek_kesintiler=0,
        gelir_vergisi_hesaplansin=True,
        damga_vergisi_hesaplansin=True,
        bes_aktif=True,
        hazine_yardimi_aktif=True,
        engellilik_derecesi=None,
        sgk_tipi='1',
        kanun_kodu=None,

):
    if ay_gun_sayisi is None:
        ay_gun_sayisi = c.get_ay_gun_sayisi(ay, yil, ay_gun_secimi)
    # ADIM 1: TEMEL ÜCRET HESABI
    gunluk_ucret = aylik_brut_ucret / 30
    if calisan_gun >= ay_gun_sayisi:
        calisilan_ucret = aylik_brut_ucret
    else:
        gunluk_ucret_dinamik = aylik_brut_ucret / ay_gun_sayisi
        calisilan_ucret = gunluk_ucret_dinamik * calisan_gun
    aylik_saat_dinamik = ay_gun_sayisi * 7.5
    saatlik_ucret_eksik = aylik_brut_ucret / aylik_saat_dinamik
    eksik_saat_ucreti = saatlik_ucret_eksik * eksik_saat
    saatlik_ucret = hesapla_saatlik_ucret(aylik_brut_ucret)
    bu_ayki_temel_ucret = calisilan_ucret - eksik_saat_ucreti
    # ADIM 2: FAZLA MESAİ HESABI
    fazla_mesai_baz = fm_baz_ucret if fm_baz_ucret is not None else aylik_brut_ucret
    fazla_mesai = hesapla_fazla_mesai(
        aylik_brut_ucret=fazla_mesai_baz,
        fm01_saat=fm01_saat,
        fm02_saat=fm02_saat,
        fm03_saat=fm03_saat
    )

    tahmini_bu_ayki_brut = bu_ayki_temel_ucret + fazla_mesai['toplam_ucret'] + ek_odemeler
    if saglik_sigorta_primi == 0 and saglik_sigorta_isveren_kesinti is not None and saglik_sigorta_isveren_kesinti > 0:
        saglik_sigorta_primi = hesapla_sigorta_brutu_kesintiden(
            saglik_sigorta_isveren_kesinti, 'saglik', sgk_tipi, kumulatif_gv_matrahi, tahmini_bu_ayki_brut
        )
    if hayat_sigorta_primi == 0 and hayat_sigorta_isveren_kesinti is not None and hayat_sigorta_isveren_kesinti > 0:
        hayat_sigorta_primi = hesapla_sigorta_brutu_kesintiden(
            hayat_sigorta_isveren_kesinti, 'hayat', sgk_tipi, kumulatif_gv_matrahi, tahmini_bu_ayki_brut
        )

    # ADIM 3: TOPLAM BRÜT KAZANÇ
    toplam_brut_kazanc = bu_ayki_temel_ucret + fazla_mesai['toplam_ucret'] + ek_odemeler
    prime_tabi_brut = toplam_brut_kazanc + hayat_sigorta_primi
    brut_kazanclar_toplami = prime_tabi_brut + saglik_sigorta_primi
    # ADIM 4: SGK HESAPLAMALARI
    sgk_matrahi = hesapla_sgk_matrahi(
        brut_kazanc=prime_tabi_brut,
        onceki_donem_brut=onceki_donem_brut,
        iki_onceki_donem_brut=iki_onceki_donem_brut
    )
    sgk_primleri = hesapla_tum_sgk_primleri(
        sgk_matrahi=sgk_matrahi,
        sgk_tipi=sgk_tipi,
        bes_aktif=bes_aktif,
        hazine_yardimi_aktif=hazine_yardimi_aktif
    )
    # ADIM 5: ÖZEL SİGORTA İNDİRİMLERİ
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

    # ADIM 6: ENGELLİLİK İNDİRİMİ
    engellilik_indirimi = 0
    if engellilik_derecesi and engellilik_derecesi in c.ENGELLILIK_INDIRIMI:
        engellilik_indirimi = c.ENGELLILIK_INDIRIMI[engellilik_derecesi]
    # ADIM 7: GELİR VERGİSİ MATRAHI
    sgk_kesintileri_gv_icin = sgk_primleri['isci_sgk'] + sgk_primleri['isci_issizlik']
    gv_matrahi = hesapla_gelir_vergisi_matrahi(
        brut_kazanc=brut_kazanclar_toplami,
        sgk_kesintileri=sgk_kesintileri_gv_icin,
        saglik_sigorta_indirimi=sigorta_indirimleri['saglik_indirim'],
        hayat_sigorta_indirimi=sigorta_indirimleri['hayat_indirim'],
        engellilik_indirimi=engellilik_indirimi
    )
    # ADIM 8: GELİR VERGİSİ HESABI
    if gelir_vergisi_hesaplansin:
        gv_hesabi = hesapla_gelir_vergisi(
            gv_matrahi=gv_matrahi,
            kumulatif_matrah_onceki=kumulatif_gv_matrahi
        )
        istisna = hesapla_asgari_ucret_istisnasi(
            kumulatif_asgari_matrah_onceki=kumulatif_asgari_gv_matrahi
        )
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
    # ADIM 9: DAMGA VERGİSİ HESABI
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
    # ADIM 10: ÖZEL SİGORTA KESİNTİLERİ
    saglik_kesinti = saglik_sigorta_isveren_kesinti if saglik_sigorta_isveren_kesinti else 0
    hayat_kesinti = hayat_sigorta_isveren_kesinti if hayat_sigorta_isveren_kesinti else 0
    ozel_sigorta_kesintisi = saglik_kesinti + hayat_kesinti
    # ADIM 11: NET ÜCRET HESABI
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
    # ADIM 12: TEŞVİK HESABI
    tesvik_sonuc = None
    tesvik_tutari = 0
    if kanun_kodu:
        tesvik_sonuc = hesapla_tesvikli_sgk(
            sgk_matrahi=sgk_matrahi,
            calisan_gun=calisan_gun,
            kanun_kodu=kanun_kodu,
            sgk_tipi=sgk_tipi,
            bes_aktif=bes_aktif,
            hazine_yardimi_aktif=hazine_yardimi_aktif
        )
        tesvik_tutari = tesvik_sonuc['tesvik']['tesvik_tutari']
        if calisan_gun < 30 and tesvik_sonuc['tesvik'].get('matrah_tipi') == 'pek_alt_sinir':
            tesvik_tutari = yuvarla(tesvik_tutari * (calisan_gun / 30))
    # ADIM 13: İŞVEREN MALİYETİ
    maliyet = hesapla_isveren_maliyeti(
        brut_kazanc=brut_kazanclar_toplami,
        isveren_sgk=sgk_primleri['isveren_sgk'],
        isveren_kvsk=sgk_primleri['isveren_kvsk'],
        isveren_issizlik=sgk_primleri['isveren_issizlik'],
        hazine_yardimi=sgk_primleri['hazine_yardimi']
    )
    maliyet['tesvik_tutari'] = tesvik_tutari
    maliyet['toplam_maliyet'] = yuvarla(maliyet['toplam_maliyet'] - tesvik_tutari)
    # SONUÇ
    return {
        'donem': {
            'ay': ay,
            'ay_adi': c.AYLAR.get(ay, ''),
            'yil': yil,
        },
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
        'fazla_mesai': fazla_mesai,
        'ek_odemeler': yuvarla(ek_odemeler),
        'brut_kazanclar': {
            'temel_ucret': yuvarla(bu_ayki_temel_ucret),
            'fazla_mesai': fazla_mesai['toplam_ucret'],
            'ek_odemeler': yuvarla(ek_odemeler),
            'prime_tabi_brut': yuvarla(prime_tabi_brut),
            'toplam_brut': yuvarla(brut_kazanclar_toplami),
        },
        'sgk': {
            'matrah': sgk_matrahi,
            'sgk_tipi': sgk_tipi,
            'onceki_donem_brut': yuvarla(onceki_donem_brut),
            'iki_onceki_donem_brut': yuvarla(iki_onceki_donem_brut),
            'primler': sgk_primleri,
        },
        'ozel_sigorta': {
            'saglik_primi': yuvarla(saglik_sigorta_primi),
            'hayat_primi': yuvarla(hayat_sigorta_primi),
            'toplam_prim': yuvarla(ozel_sigorta_kesintisi),
            'indirimleri': sigorta_indirimleri,
        },
        'engellilik': {
            'derece': engellilik_derecesi,
            'indirim': yuvarla(engellilik_indirimi),
        },
        'gelir_vergisi': {
            'matrah': yuvarla(gv_matrahi),
            'hesaplanan': gv_hesabi['hesaplanan_vergi'],
            'kumulatif_matrah_onceki': gv_hesabi['kumulatif_matrah_onceki'],
            'kumulatif_matrah_yeni': gv_hesabi['kumulatif_matrah_yeni'],
            'istisna': istisna,
            'odenecek': odenecek_gv,
        },
        'damga_vergisi': dv_hesabi,
        'kesintiler': {
            'yasal': net_hesabi['yasal_kesintiler'],
            'ozel_sigorta': net_hesabi['ozel_sigorta_kesintisi'],
            'ek_kesintiler': net_hesabi['ek_kesintiler'],
            'toplam': net_hesabi['toplam_kesintiler'],
        },
        'net_ucret': net_hesabi['net_ucret'],
        'isveren_maliyeti': maliyet,
        'tesvik': tesvik_sonuc,
    }