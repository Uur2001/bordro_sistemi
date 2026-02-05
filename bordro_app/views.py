from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
import json

from .models import AylikBordro, YillikBordro, Tazminat
from .calculations import hesapla_bordro
from .constants import SGK_TIPLERI, SGK_KANUNLARI, AYLAR
from .calculations_year import yillik_bordro_hesapla
from . import constants_year as c_year
from .calculations_tazminat import tazminat_hesapla as hesapla_tazminat


# Ana Sayfa - Nedir
def home(request):
    return render(request, 'home.html', {'active_page': 'nedir'})


# Bordro Sihirbazı Ana Sayfa
def bordro_sihirbazi(request):
    return render(request, 'bordro_sihirbazi.html', {'active_page': 'nedir'})


def aylik_hesapla(request):
    context = {
        'active_page': 'aylik_hesaplama',
        'sgk_tipleri': SGK_TIPLERI,
        'sgk_kanunlari': SGK_KANUNLARI,
        "aylar": AYLAR,
        'aylar_json': json.dumps(AYLAR),
    }

    if request.method == 'POST':
        try:
            # Yardımcı fonksiyon - Metin temizleme
            def temizle_sayi(value):
                """Sayıdan TL, saat, nokta, virgül gibi karakterleri temizler ve float döner"""
                if not value:
                    return 0.0
                value = value.replace('₺', '').replace('saat', '').replace(' ', '').strip()
                value = value.replace('.', '').replace(',', '.')
                return float(value) if value else 0.0

            # Parametreleri doğru isimlerle hazırla
            yil = int(request.POST.get('bordro_yil', 2026))
            ay = int(request.POST.get('bordro_ay', 1))

            # Hesaplama fonksiyonunu çağır - FLOAT değerlerle
            sonuc = hesapla_bordro(
                aylik_brut_ucret=temizle_sayi(request.POST.get('aylik_temel_ucret', '0')),
                ay=ay,
                yil=yil,
                calisan_gun=int(temizle_sayi(request.POST.get('calisilan_gun', '30'))),
                ay_gun_secimi=request.POST.get('gun_sayisi_tipi', 'takvim'),
                eksik_saat=temizle_sayi(request.POST.get('eksik_saat', '0')),
                kumulatif_gv_matrahi=temizle_sayi(request.POST.get('yillik_gv_matrahi', '0')),
                kumulatif_asgari_gv_matrahi=temizle_sayi(request.POST.get('yillik_asg_ucret_gv_matrahi', '0')),
                onceki_donem_brut=temizle_sayi(request.POST.get('devir_matrah_1ay', '0')),
                iki_onceki_donem_brut=temizle_sayi(request.POST.get('devir_matrah_2ay', '0')),
                fm01_saat=temizle_sayi(request.POST.get('fm01_saat', '0')),
                fm02_saat=temizle_sayi(request.POST.get('fm02_saat', '0')),
                fm03_saat=temizle_sayi(request.POST.get('fm03_saat', '0')),
                saglik_sigorta_primi=temizle_sayi(request.POST.get('saglik_sig_isci', '0')),
                hayat_sigorta_primi=temizle_sayi(request.POST.get('hayat_sig_isci', '0')),
                saglik_sigorta_isveren_kesinti=temizle_sayi(request.POST.get('saglik_sig_isveren', '0')),
                hayat_sigorta_isveren_kesinti=temizle_sayi(request.POST.get('hayat_sig_isveren', '0')),
                gelir_vergisi_hesaplansin=request.POST.get('gelir_vergisi') == 'on',
                damga_vergisi_hesaplansin=request.POST.get('damga_vergisi') == 'on',
                bes_aktif=request.POST.get('bes') == 'on',
                hazine_yardimi_aktif=request.POST.get('hazine_yardimi') == 'on',
                engellilik_derecesi=request.POST.get('engellilik_durumu') if request.POST.get(
                    'engellilik_durumu') != 'normal' else None,
                sgk_tipi=request.POST.get('sgk_tipi', '01'),
                kanun_kodu=request.POST.get('kanun_no') if request.POST.get('kanun_no') != '00000' else None,
            )

            # Veritabanına kaydet - Decimal ile
            bordro = AylikBordro.objects.create(
                bordro_yil=yil,
                bordro_ay=ay,
                aylik_temel_ucret=Decimal(str(temizle_sayi(request.POST.get('aylik_temel_ucret', '0')))),
                ucret_tipi=request.POST.get('ucret_tipi', 'brut'),
                gelir_vergisi=request.POST.get('gelir_vergisi') == 'on',
                damga_vergisi=request.POST.get('damga_vergisi') == 'on',
                engellilik_durumu=request.POST.get('engellilik_durumu', 'normal'),
                yillik_gv_matrahi=Decimal(str(temizle_sayi(request.POST.get('yillik_gv_matrahi', '0')))),
                yillik_asg_ucret_gv_matrahi=Decimal(
                    str(temizle_sayi(request.POST.get('yillik_asg_ucret_gv_matrahi', '0')))),
                gun_sayisi_tipi=request.POST.get('gun_sayisi_tipi', 'takvim'),
                calisilan_gun=int(temizle_sayi(request.POST.get('calisilan_gun', '30'))),
                eksik_saat=Decimal(str(temizle_sayi(request.POST.get('eksik_saat', '0')))),
                sgk_tipi=request.POST.get('sgk_tipi', '01'),
                kanun_no=request.POST.get('kanun_no', '00000'),
                hazine_yardimi=request.POST.get('hazine_yardimi') == 'on',
                bes=request.POST.get('bes') == 'on',
                devir_matrah_2ay=Decimal(str(temizle_sayi(request.POST.get('devir_matrah_2ay', '0')))),
                devir_matrah_1ay=Decimal(str(temizle_sayi(request.POST.get('devir_matrah_1ay', '0')))),
                saglik_sig_isci=Decimal(str(temizle_sayi(request.POST.get('saglik_sig_isci', '0')))),
                saglik_sig_isveren=Decimal(str(temizle_sayi(request.POST.get('saglik_sig_isveren', '0')))),
                hayat_sig_isci=Decimal(str(temizle_sayi(request.POST.get('hayat_sig_isci', '0')))),
                hayat_sig_isveren=Decimal(str(temizle_sayi(request.POST.get('hayat_sig_isveren', '0')))),
                fm01_saat=Decimal(str(temizle_sayi(request.POST.get('fm01_saat', '0')))),
                fm02_saat=Decimal(str(temizle_sayi(request.POST.get('fm02_saat', '0')))),
                fm03_saat=Decimal(str(temizle_sayi(request.POST.get('fm03_saat', '0')))),
                hesaplama_sonuc=sonuc,
            )

            context['sonuc'] = sonuc
            context['bordro_id'] = bordro.id
            context['success'] = True
            context['message'] = 'Hesaplama başarılı!'

        except Exception as e:
            context['error'] = True
            context['message'] = f'Hesaplama hatası: {str(e)}'
            import traceback
            context['traceback'] = traceback.format_exc()

    return render(request, 'aylik_hesapla.html', context)

def yillik_hesapla(request):
    """Yıllık hesaplama form sayfası"""
    context = {
        'active_page': 'yillik_hesaplama',
        'sgk_tipleri': c_year.SOSYAL_GUVENLIK_TIPI,
        'kanun_kodlari': c_year.KANUN_KODLARI,
        'aylar': c_year.AYLAR,
    }
    return render(request, 'yillik_hesapla.html', context)


@csrf_exempt
def yillik_hesapla_api(request):
    """Yıllık bordro hesaplama API endpoint'i"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Sadece POST metodu kabul edilir'}, status=405)

    try:
        data = json.loads(request.body)

        # Aylık verileri hazırla
        aylik_veriler = []
        for ay in range(1, 13):
            ay_key = f'ay_{ay}'
            ay_data = data.get(ay_key, {})

            brut = temizle_sayi_yillik(ay_data.get('brut', '33030'))
            gun = int(temizle_sayi_yillik(ay_data.get('gun', '30')))

            aylik_veriler.append({
                'brut': brut,
                'gun': gun
            })

        # Genel parametreler
        sgk_tipi = data.get('sgk_tipi', '01')
        kanun_kodu = data.get('kanun_kodu', '00000')
        bes_aktif = data.get('bes_aktif', False)
        engellilik_derecesi = int(data.get('engellilik_derecesi', 0))
        takvim_esasli = data.get('takvim_esasli', True)

        # Hesaplamayı yap
        sonuc = yillik_bordro_hesapla(
            aylik_veriler=aylik_veriler,
            sgk_tipi=sgk_tipi,
            kanun_kodu=kanun_kodu,
            bes_aktif=bes_aktif,
            engellilik_derecesi=engellilik_derecesi,
            takvim_esasli=takvim_esasli
        )

        # Veritabanına kaydet
        yillik_ozet = sonuc.get('yillik_ozet', {})

        bordro = YillikBordro.objects.create(
            bordro_yili=data.get('yil', 2026),
            sgk_tipi=sgk_tipi,
            kanun_kodu=kanun_kodu,
            bes_aktif=bes_aktif,
            engellilik_derecesi=engellilik_derecesi if engellilik_derecesi == 0 else f'{engellilik_derecesi}_derece',
            takvim_esasli=takvim_esasli,
            aylik_veriler=data,
            aylik_sonuclar=sonuc.get('aylik_sonuclar', []),
            yillik_ozet=yillik_ozet,
            toplam_brut=Decimal(str(yillik_ozet.get('toplam_brut', 0))),
            toplam_net=Decimal(str(yillik_ozet.get('toplam_net', 0))),
            toplam_gv=Decimal(str(yillik_ozet.get('toplam_gv', 0))),
            toplam_sgk_isci=Decimal(str(yillik_ozet.get('toplam_sgk_personel', 0))),
            toplam_isveren_maliyeti=Decimal(str(yillik_ozet.get('toplam_isveren_maliyeti', 0))),
        )

        # Session'a kaydet (sonuç sayfası için)
        request.session['yillik_bordro_id'] = bordro.id

        return JsonResponse({
            'success': True,
            'bordro_id': bordro.id,
            'sonuc': sonuc,
            'redirect_url': f'/bordro-sihirbazi/yillik/sonuc/{bordro.id}/'
        })

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Geçersiz JSON formatı'}, status=400)
    except ValueError as e:
        return JsonResponse({'success': False, 'error': f'Değer hatası: {str(e)}'}, status=400)
    except Exception as e:
        import traceback
        return JsonResponse({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }, status=500)


def yillik_sonuc(request, bordro_id):
    """Yıllık hesaplama sonuç sayfası"""
    try:
        bordro = YillikBordro.objects.get(id=bordro_id)
    except YillikBordro.DoesNotExist:
        from django.shortcuts import redirect
        return redirect('yillik_hesapla')

    context = {
        'active_page': 'yillik_hesaplama',
        'bordro': bordro,
        'aylik_sonuclar': bordro.aylik_sonuclar,
        'yillik_ozet': bordro.yillik_ozet,
        'parametreler': {
            'sgk_tipi': bordro.sgk_tipi,
            'kanun_kodu': bordro.kanun_kodu,
            'bes_aktif': bordro.bes_aktif,
            'engellilik_derecesi': bordro.engellilik_derecesi,
            'takvim_esasli': bordro.takvim_esasli,
        },
    }
    return render(request, 'yillik_sonuc.html', context)


def temizle_sayi_yillik(value):
    """Türkçe sayı formatını Python float'a çevirir"""
    if isinstance(value, (int, float)):
        return float(value)

    s = str(value).strip()

    # Birim ve sembolleri kaldır
    for unit in ['₺', 'TL', 'gün', 'saat', '%']:
        s = s.replace(unit, '')

    s = s.strip()
    if not s:
        return 0.0

    # Türkçe format: 33.030,00 -> 33030.00
    s = s.replace('.', '')  # Binlik ayracını kaldır
    s = s.replace(',', '.')  # Virgülü noktaya çevir

    try:
        return float(s)
    except ValueError:
        return 0.0


def tazminat_hesapla(request):
    context = {
        'active_page': 'tazminat_hesaplama',
    }
    return render(request, 'tazminat_hesapla.html', context)


# AJAX için hesaplama endpoint'i
@csrf_exempt
def hesapla_ajax(request):
    """JavaScript'ten AJAX ile çağrılacak hesaplama endpoint'i"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # String değerleri Decimal'e çevir
            for key in ['aylik_temel_ucret', 'yillik_gv_matrahi', 'yillik_asg_ucret_gv_matrahi',
                        'devir_matrah_2ay', 'devir_matrah_1ay', 'saglik_sig_isci',
                        'saglik_sig_isveren', 'hayat_sig_isci', 'hayat_sig_isveren',
                        'eksik_saat', 'fm01_saat', 'fm02_saat', 'fm03_saat']:
                if key in data:
                    data[key] = Decimal(str(data[key]).replace('.', '').replace(',', '.'))

            sonuc = hesapla_bordro(data)
            return JsonResponse({'success': True, 'sonuc': sonuc})
        except Exception as e:
            import traceback
            return JsonResponse({
                'success': False,
                'error': str(e),
                'traceback': traceback.format_exc()
            })

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@csrf_exempt
def tazminat_hesapla_api(request):
    """Tazminat hesaplama API endpoint'i"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Sadece POST metodu kabul edilir'}, status=405)

    try:
        data = json.loads(request.body)

        # Tarihleri al
        giris_tarihi = data.get('giris_tarihi', '')
        cikis_tarihi = data.get('cikis_tarihi', '')

        # Ücretleri al ve temizle
        aylik_brut = temizle_sayi_yillik(data.get('aylik_brut_ucret', '0'))
        aylik_ek = temizle_sayi_yillik(data.get('aylik_brut_ek_ucret', '0'))
        yillik_ikramiye = temizle_sayi_yillik(data.get('yillik_brut_ikramiye', '0'))
        kidem_disi_gun = int(temizle_sayi_yillik(data.get('kidem_disi_gun', '0')))
        kumulatif_gv = temizle_sayi_yillik(data.get('kumulatif_gv_matrahi', '0'))

        # Parametreleri al
        ihbar_hesaplansin = data.get('ihbar_hesaplansin', True)
        ihbar_gv = data.get('ihbar_gv_hesaplansin', True)
        ihbar_dv = data.get('ihbar_dv_hesaplansin', True)
        kidem_dv = data.get('kidem_dv_hesaplansin', True)

        # Hesaplamayı yap
        sonuc = hesapla_tazminat(
            giris_tarihi=giris_tarihi,
            cikis_tarihi=cikis_tarihi,
            aylik_brut_ucret=aylik_brut,
            aylik_brut_ek_ucret=aylik_ek,
            yillik_brut_ikramiye=yillik_ikramiye,
            kidem_disi_gun=kidem_disi_gun,
            kumulatif_gv_matrahi=kumulatif_gv,
            ihbar_hesaplansin=ihbar_hesaplansin,
            ihbar_gv_hesaplansin=ihbar_gv,
            ihbar_dv_hesaplansin=ihbar_dv,
            kidem_dv_hesaplansin=kidem_dv,
        )

        # Veritabanına kaydet
        from datetime import datetime

        def parse_tarih(tarih_str):
            if '-' in tarih_str and len(tarih_str.split('-')[0]) == 4:
                return datetime.strptime(tarih_str, "%Y-%m-%d").date()
            else:
                return datetime.strptime(tarih_str, "%d.%m.%Y").date()

        tazminat_kayit = Tazminat.objects.create(
            giris_tarihi=parse_tarih(giris_tarihi),
            cikis_tarihi=parse_tarih(cikis_tarihi),
            kidem_disi_sure=kidem_disi_gun,
            aylik_brut_ucret=Decimal(str(aylik_brut)),
            aylik_brut_ek_ucret=Decimal(str(aylik_ek)),
            yillik_brut_ikramiye=Decimal(str(yillik_ikramiye)),
            kumulatif_gv_matrahi=Decimal(str(kumulatif_gv)),
            ihbar_tazminati=ihbar_hesaplansin,
            ihbar_gelir_vergisi=ihbar_gv,
            ihbar_damga_vergisi=ihbar_dv,
            kidem_damga_vergisi=kidem_dv,
            hesaplama_sonuc=sonuc,
        )

        return JsonResponse({
            'success': True,
            'tazminat_id': tazminat_kayit.id,
            'sonuc': sonuc,
        })

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Geçersiz JSON formatı'}, status=400)
    except ValueError as e:
        return JsonResponse({'success': False, 'error': f'Değer hatası: {str(e)}'}, status=400)
    except Exception as e:
        import traceback
        return JsonResponse({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }, status=500)