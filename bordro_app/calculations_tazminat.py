from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

KIDEM_TAVANI = 64948.77
DAMGA_VERGISI_ORANI = 0.00759
SGK_ISCI_PAYI = 0.14
ISS_ISCI_PAYI = 0.01


def vergi_hesapla(kumulatif_matrah: float, ay_matrah: float) -> float:


    def hesapla(m):
        lim1, lim2, lim3, lim4 = 190000, 400000, 1500000, 5300000
        oran1, oran2, oran3, oran4, oran5 = 0.15, 0.20, 0.27, 0.35, 0.40
        v1, v2, v3, v4 = 28500, 42000, 297000, 1330000

        if m <= lim1:
            return m * oran1
        elif m <= lim2:
            return v1 + ((m - lim1) * oran2)
        elif m <= lim3:
            return v1 + v2 + ((m - lim2) * oran3)
        elif m <= lim4:
            return v1 + v2 + v3 + ((m - lim3) * oran4)
        else:
            return v1 + v2 + v3 + v4 + ((m - lim4) * oran5)

    return hesapla(kumulatif_matrah + ay_matrah) - hesapla(kumulatif_matrah)


def ihbar_suresi_hesapla(toplam_ay: int) -> dict:
    """Çalışma süresine göre ihbar süresi hesapla"""
    if toplam_ay < 6:
        hafta = 2
    elif toplam_ay < 18:
        hafta = 4
    elif toplam_ay < 36:
        hafta = 6
    else:
        hafta = 8

    return {
        'hafta': hafta,
        'gun': hafta * 7
    }


def tazminat_hesapla(
        giris_tarihi: str,
        cikis_tarihi: str,
        aylik_brut_ucret: float,
        aylik_brut_ek_ucret: float = 0,
        yillik_brut_ikramiye: float = 0,
        kidem_disi_gun: int = 0,
        kumulatif_gv_matrahi: float = 0,
        ihbar_hesaplansin: bool = True,
        ihbar_gv_hesaplansin: bool = True,
        ihbar_dv_hesaplansin: bool = True,
        kidem_dv_hesaplansin: bool = True,
) -> dict:

    def parse_tarih(tarih_str):
        """Tarihi parse et (hem YYYY-MM-DD hem DD.MM.YYYY destekle)"""
        if '-' in tarih_str and len(tarih_str.split('-')[0]) == 4:
            return datetime.strptime(tarih_str, "%Y-%m-%d")
        else:
            return datetime.strptime(tarih_str, "%d.%m.%Y")

    giris_dt = parse_tarih(giris_tarihi)
    cikis_dt = parse_tarih(cikis_tarihi)
    ayarlanmis_cikis_dt = cikis_dt - timedelta(days=kidem_disi_gun)
    fark = relativedelta(ayarlanmis_cikis_dt, giris_dt)
    net_yil = fark.years
    net_ay = fark.months
    net_gun = fark.days
    brut_toplam_gun = (cikis_dt - giris_dt).days
    net_toplam_gun = (ayarlanmis_cikis_dt - giris_dt).days
    giydirilmis_brut = aylik_brut_ucret + aylik_brut_ek_ucret + (yillik_brut_ikramiye / 12)
    gunluk_brut = round(giydirilmis_brut / 30, 2)

    kidem_matrahi = min(giydirilmis_brut, KIDEM_TAVANI)

    kidem_sonuc = {
        'hak_edildi': net_toplam_gun >= 365,
        'yil': {'adet': net_yil, 'birim_tutar': 0, 'tutar': 0},
        'ay': {'adet': net_ay, 'birim_tutar': 0, 'tutar': 0},
        'gun': {'adet': net_gun, 'birim_tutar': 0, 'tutar': 0},
        'brut_toplam': 0,
        'damga_vergisi': 0,
        'net_toplam': 0,
    }

    if kidem_sonuc['hak_edildi']:

        kidem_sonuc['yil']['birim_tutar'] = round(kidem_matrahi, 2)
        kidem_sonuc['yil']['tutar'] = round(kidem_matrahi * net_yil, 2)
        kidem_sonuc['ay']['birim_tutar'] = round(kidem_matrahi / 12, 2)
        kidem_sonuc['ay']['tutar'] = round(kidem_matrahi / 12 * net_ay, 2)
        kidem_sonuc['gun']['birim_tutar'] = round(kidem_matrahi / 365, 2)
        kidem_sonuc['gun']['tutar'] = round(kidem_matrahi / 365 * net_gun, 2)
        kidem_sonuc['brut_toplam'] = round(
            kidem_sonuc['yil']['tutar'] +
            kidem_sonuc['ay']['tutar'] +
            kidem_sonuc['gun']['tutar'], 2
        )

        if kidem_dv_hesaplansin:
            kidem_sonuc['damga_vergisi'] = round(kidem_sonuc['brut_toplam'] * DAMGA_VERGISI_ORANI, 2)

        kidem_sonuc['net_toplam'] = round(
            kidem_sonuc['brut_toplam'] - kidem_sonuc['damga_vergisi'], 2
        )

    toplam_ay_ihbar = (net_yil * 12) + net_ay
    ihbar_suresi = ihbar_suresi_hesapla(toplam_ay_ihbar)

    ihbar_sonuc = {
        'hesaplansin': ihbar_hesaplansin,
        'sure_hafta': ihbar_suresi['hafta'],
        'sure_gun': ihbar_suresi['gun'],
        'gunluk_brut': gunluk_brut,
        'brut_toplam': 0,
        'gelir_vergisi': 0,
        'damga_vergisi': 0,
        'net_toplam': 0,
    }

    if ihbar_hesaplansin:
        ihbar_sonuc['brut_toplam'] = round(gunluk_brut * ihbar_suresi['gun'], 2)

        if ihbar_gv_hesaplansin:
            ihbar_sonuc['gelir_vergisi'] = round(
                vergi_hesapla(kumulatif_gv_matrahi, ihbar_sonuc['brut_toplam']), 2
            )

        if ihbar_dv_hesaplansin:
            ihbar_sonuc['damga_vergisi'] = round(
                ihbar_sonuc['brut_toplam'] * DAMGA_VERGISI_ORANI, 2
            )

        ihbar_sonuc['net_toplam'] = round(
            ihbar_sonuc['brut_toplam'] -
            ihbar_sonuc['gelir_vergisi'] -
            ihbar_sonuc['damga_vergisi'], 2
        )

    brut_tazminat_toplam = round(kidem_sonuc['brut_toplam'] + ihbar_sonuc['brut_toplam'], 2)
    toplam_gelir_vergisi = round(ihbar_sonuc['gelir_vergisi'], 2)
    toplam_damga_vergisi = round(kidem_sonuc['damga_vergisi'] + ihbar_sonuc['damga_vergisi'], 2)
    net_tazminat_toplam = round(kidem_sonuc['net_toplam'] + ihbar_sonuc['net_toplam'], 2)

    return {
        'hizmet_suresi': {
            'giris_tarihi': giris_dt.strftime('%d.%m.%Y'),
            'cikis_tarihi': cikis_dt.strftime('%d.%m.%Y'),
            'brut_gun': brut_toplam_gun,
            'kidem_disi_gun': kidem_disi_gun,
            'net_gun': net_toplam_gun,
            'yil': net_yil,
            'ay': net_ay,
            'gun': net_gun,
            'metin': f"{net_yil} Yıl, {net_ay} Ay, {net_gun} Gün",
        },
        'ucretler': {
            'aylik_brut': aylik_brut_ucret,
            'aylik_ek': aylik_brut_ek_ucret,
            'yillik_ikramiye': yillik_brut_ikramiye,
            'giydirilmis_brut': round(giydirilmis_brut, 2),
            'gunluk_brut': gunluk_brut,
            'kidem_tavani': KIDEM_TAVANI,
            'kidem_matrahi': round(kidem_matrahi, 2),
        },
        'kidem': kidem_sonuc,
        'ihbar': ihbar_sonuc,
        'toplam': {
            'brut_tazminat': brut_tazminat_toplam,
            'gelir_vergisi': toplam_gelir_vergisi,
            'damga_vergisi': toplam_damga_vergisi,
            'net_tazminat': net_tazminat_toplam,
        },
        'parametreler': {
            'kidem_tavani': KIDEM_TAVANI,
            'damga_vergisi_orani': DAMGA_VERGISI_ORANI,
            'kumulatif_gv_matrahi': kumulatif_gv_matrahi,
        }
    }