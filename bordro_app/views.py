from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
import json

from .models import AylikBordro
from .calculations import hesapla_bordro
from .constants import SGK_TIPLERI, SGK_KANUNLARI, AYLAR


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


# Yıllık Hesaplama Sihirbazı - Henüz pasif
def yillik_hesapla(request):
    return render(request, 'yillik_hesapla.html', {'active_page': 'nedir'})


# Tazminat Hesaplama - Henüz pasif
def tazminat_hesapla(request):
    return render(request, 'tazminat_hesapla.html', {'active_page': 'nedir'})


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