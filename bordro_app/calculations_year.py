from . import constants_year as c


def vergi_hesapla(kumulatif_matrah: float, ay_matrah: float) -> float:

    toplam_matrah = kumulatif_matrah + ay_matrah

    def hesapla(m):
        lim1, lim2, lim3, lim4 = 190000, 400000, 1500000, 5300000
        oran1, oran2, oran3, oran4, oran5 = 0.15, 0.20, 0.27, 0.35, 0.40

        v1 = lim1 * oran1
        v2 = (lim2 - lim1) * oran2
        v3 = (lim3 - lim2) * oran3
        v4 = (lim4 - lim3) * oran4

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

    return hesapla(toplam_matrah) - hesapla(kumulatif_matrah)


def yillik_bordro_hesapla(
        aylik_veriler: list,
        sgk_tipi: str = "01",
        kanun_kodu: str = "00000",
        bes_aktif: bool = True,
        engellilik_derecesi: int = 0,
        takvim_esasli: bool = True
) -> dict:

    if len(aylik_veriler) != 12:
        raise ValueError(f"aylik_veriler 12 elemanlı olmalı, {len(aylik_veriler)} eleman verildi")

    secilen_tip = c.SOSYAL_GUVENLIK_TIPI.get(sgk_tipi)
    if not secilen_tip:
        raise ValueError(f"Geçersiz SGK tipi: {sgk_tipi}")

    secilen_kanun = c.KANUN_KODLARI.get(kanun_kodu)
    if not secilen_kanun:
        raise ValueError(f"Geçersiz kanun kodu: {kanun_kodu}")

    engellilik_tutari = c.ENGELLILIK_INDIRIMLERI.get(engellilik_derecesi, 0)

    kumulatif_personel_gv_matrah = 0
    kumulatif_asgari_gv_matrah = 0

    bordro_listesi = []

    for ay_index in range(12):
        ay_no = ay_index + 1
        ay_bilgi = c.AYLAR[ay_no]
        ay_adi = ay_bilgi["ad"]
        ay_gun_sayisi = ay_bilgi["gun"]

        ay_veri = aylik_veriler[ay_index]
        tam_brut = ay_veri.get('brut', c.ASGARI_UCRET_BRUT)

        if takvim_esasli:

            gun = ay_gun_sayisi
            if gun > 30:
                hesap_brut = round(tam_brut * (30 / gun), 2)
            else:
                hesap_brut = tam_brut
        else:

            gun = ay_veri.get('gun', 30)
            if gun == 30:
                hesap_brut = tam_brut
            else:
                hesap_brut = round((tam_brut / 30) * gun, 2)

        if gun >= 28:
            ay_tavan = c.SGK_TAVANI
            ay_asgari = c.ASGARI_UCRET_BRUT
        else:
            ay_tavan = round((c.SGK_TAVANI / 30) * gun, 2)
            ay_asgari = round((c.ASGARI_UCRET_BRUT / 30) * gun, 2)

        sgk_matrah = round(min(hesap_brut, ay_tavan), 2)
        sgk_personel = round(sgk_matrah * secilen_tip['Isci_SGK'], 2)
        issizlik_personel = round(sgk_matrah * secilen_tip['Isci_Iss'], 2)

        bes_kesintisi = 0
        if bes_aktif:
            bes_kesintisi = round(sgk_matrah * c.BES_ORANI, 2)

        gv_matrah_personel = round(max(0, hesap_brut - sgk_personel - issizlik_personel - engellilik_tutari), 2)

        if secilen_tip['Vergi_Muaf']:
            ham_gv = 0
        else:
            ham_gv = round(vergi_hesapla(kumulatif_personel_gv_matrah, gv_matrah_personel), 2)

        sgk_asgari = round(ay_asgari * c.SGK_ISCI_ORANI, 2)
        issizlik_asgari = round(ay_asgari * c.ISSIZLIK_ISCI_ORANI, 2)
        gv_matrah_asgari = round(ay_asgari - sgk_asgari - issizlik_asgari, 2)

        if secilen_tip['Vergi_Muaf']:
            istisna_gv = 0
        else:
            istisna_gv = round(vergi_hesapla(kumulatif_asgari_gv_matrah, gv_matrah_asgari), 2)

        ham_dv = round(hesap_brut * c.DAMGA_VERGISI_ORANI, 2)
        istisna_dv = round(ay_asgari * c.DAMGA_VERGISI_ORANI, 2)

        odeme_gv = round(max(0, ham_gv - istisna_gv), 2)
        odeme_dv = round(max(0, ham_dv - istisna_dv), 2)

        toplam_kesinti = round(sgk_personel + issizlik_personel + odeme_gv + odeme_dv + bes_kesintisi, 2)
        net_maas = round(hesap_brut - toplam_kesinti, 2)

        isveren_sgk_brut = round(sgk_matrah * secilen_tip['Isveren_SGK'], 2)
        hazine_indirim = round(sgk_matrah * secilen_kanun['Indirim'], 2)
        odeme_isveren_sgk = round(max(0, isveren_sgk_brut - hazine_indirim), 2)
        isveren_issizlik = round(sgk_matrah * secilen_tip['Isveren_Iss'], 2)
        toplam_maliyet = round(hesap_brut + odeme_isveren_sgk + isveren_issizlik, 2)

        bordro_listesi.append({
            "ay": ay_no,
            "ay_adi": ay_adi,
            "gun": gun,
            "tam_brut": tam_brut,
            "hesap_brut": hesap_brut,
            "sgk_matrahi": sgk_matrah,
            "sgk_personel": sgk_personel,
            "issizlik_personel": issizlik_personel,
            "bes_kesintisi": bes_kesintisi,
            "gv_matrahi": gv_matrah_personel,
            "tahakkuk_gv": ham_gv,
            "istisna_gv": istisna_gv,
            "odenecek_gv": odeme_gv,
            "odenecek_dv": odeme_dv,
            "toplam_kesinti": toplam_kesinti,
            "net_maas": net_maas,
            "isveren_sgk": isveren_sgk_brut,
            "hazine_indirimi": hazine_indirim,
            "isveren_issizlik": isveren_issizlik,
            "isveren_maliyeti": toplam_maliyet,
            "kumulatif_gv_matrahi": kumulatif_personel_gv_matrah + gv_matrah_personel,
            "kumulatif_asgari_gv_matrahi": kumulatif_asgari_gv_matrah + gv_matrah_asgari,
        })

        kumulatif_personel_gv_matrah += gv_matrah_personel
        kumulatif_asgari_gv_matrah += gv_matrah_asgari

    yillik_ozet = {
        "toplam_brut": round(sum(b["hesap_brut"] for b in bordro_listesi), 2),
        "toplam_net": round(sum(b["net_maas"] for b in bordro_listesi), 2),
        "toplam_sgk_personel": round(sum(b["sgk_personel"] for b in bordro_listesi), 2),
        "toplam_issizlik_personel": round(sum(b["issizlik_personel"] for b in bordro_listesi), 2),
        "toplam_bes": round(sum(b["bes_kesintisi"] for b in bordro_listesi), 2),
        "toplam_gv": round(sum(b["odenecek_gv"] for b in bordro_listesi), 2),
        "toplam_dv": round(sum(b["odenecek_dv"] for b in bordro_listesi), 2),
        "toplam_kesinti": round(sum(b["toplam_kesinti"] for b in bordro_listesi), 2),
        "toplam_hazine_indirimi": round(sum(b["hazine_indirimi"] for b in bordro_listesi), 2),
        "toplam_isveren_maliyeti": round(sum(b["isveren_maliyeti"] for b in bordro_listesi), 2),
        "ortalama_net": round(sum(b["net_maas"] for b in bordro_listesi) / 12, 2),
        "ortalama_brut": round(sum(b["hesap_brut"] for b in bordro_listesi) / 12, 2),
    }

    parametreler = {
        "sgk_tipi": sgk_tipi,
        "sgk_tipi_ad": secilen_tip['Ad'],
        "kanun_kodu": kanun_kodu,
        "kanun_ad": secilen_kanun['Ad'],
        "kanun_indirim": secilen_kanun['Indirim'],
        "bes_aktif": bes_aktif,
        "engellilik_derecesi": engellilik_derecesi,
        "engellilik_tutari": engellilik_tutari,
        "takvim_esasli": takvim_esasli,
        "vergi_muaf": secilen_tip['Vergi_Muaf'],
    }

    return {
        "aylik_sonuclar": bordro_listesi,
        "yillik_ozet": yillik_ozet,
        "parametreler": parametreler
    }


def aylik_veri_olustur(
        brut_liste: list = None,
        tek_brut: float = None,
        gun_liste: list = None
) -> list:

    if brut_liste is None and tek_brut is None:
        tek_brut = c.ASGARI_UCRET_BRUT

    if brut_liste is None:
        brut_liste = [tek_brut] * 12

    if len(brut_liste) != 12:
        raise ValueError(f"brut_liste 12 elemanlı olmalı, {len(brut_liste)} eleman verildi")

    aylik_veriler = []
    for i in range(12):
        veri = {'brut': brut_liste[i]}
        if gun_liste and i < len(gun_liste):
            veri['gun'] = gun_liste[i]
        aylik_veriler.append(veri)

    return aylik_veriler