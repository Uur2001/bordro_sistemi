from django.shortcuts import render,redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
import json
from .models import AylikBordro, YillikBordro, Tazminat, Calisan
from .calculations import hesapla_bordro
from .constants import SGK_TIPLERI, SGK_KANUNLARI, AYLAR
from .calculations_year import yillik_bordro_hesapla
from . import constants_year as c_year
from .calculations_tazminat import tazminat_hesapla as hesapla_tazminat
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .exports import create_aylik_bordro_excel, create_yillik_bordro_excel, create_tazminat_excel
from django.contrib.admin.views.decorators import staff_member_required


def home(request):
    return render(request, 'home.html', {'active_page': 'nedir'})


def bordro_sihirbazi(request):
    return render(request, 'bordro_sihirbazi.html', {'active_page': 'nedir'})

@login_required(login_url='giris')
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
            def temizle_sayi(value):
                if not value:
                    return 0.0
                value = value.replace('₺', '').replace('saat', '').replace(' ', '').strip()
                value = value.replace('.', '').replace(',', '.')
                return float(value) if value else 0.0
            yil = int(request.POST.get('bordro_yil', 2026))
            ay = int(request.POST.get('bordro_ay', 1))
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
                ucret_tipi=request.POST.get('ucret_tipi', 'brut'),
            )
            calisan_id = request.POST.get('calisan_id', '')
            calisan = None
            if calisan_id and calisan_id not in ['', '-', 'None']:
                try:
                    calisan = Calisan.objects.filter(id=int(calisan_id), user=request.user).first()
                except (ValueError, TypeError):
                    calisan = None

            bordro = AylikBordro.objects.create(
                user=request.user,
                calisan=calisan,
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

@login_required(login_url='giris')
def yillik_hesapla(request):
    context = {
        'active_page': 'yillik_hesaplama',
        'sgk_tipleri': c_year.SOSYAL_GUVENLIK_TIPI,
        'kanun_kodlari': c_year.KANUN_KODLARI,
        'aylar': c_year.AYLAR,
    }
    return render(request, 'yillik_hesapla.html', context)

@csrf_exempt
@login_required(login_url='giris')
def yillik_hesapla_api(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Sadece POST metodu kabul edilir'}, status=405)
    try:
        data = json.loads(request.body)
        ucret_tipi = data.get('ucret_tipi', 'brut')
        aylik_veriler = []
        for ay in range(1, 13):
            ay_key = f'ay_{ay}'
            ay_data = data.get(ay_key, {})
            tutar = temizle_sayi_yillik(ay_data.get('brut', '33030'))
            gun = int(temizle_sayi_yillik(ay_data.get('gun', '30')))

            if ucret_tipi == 'net':
                aylik_veriler.append({
                    'net': tutar,
                    'gun': gun
                })
            else:
                aylik_veriler.append({
                    'brut': tutar,
                    'gun': gun
                })
        sgk_tipi = data.get('sgk_tipi', '01')
        kanun_kodu = data.get('kanun_kodu', '00000')
        bes_aktif = data.get('bes_aktif', False)
        engellilik_derecesi = int(data.get('engellilik_derecesi', 0))
        takvim_esasli = data.get('takvim_esasli', True)
        sonuc = yillik_bordro_hesapla(
            aylik_veriler=aylik_veriler,
            sgk_tipi=sgk_tipi,
            kanun_kodu=kanun_kodu,
            bes_aktif=bes_aktif,
            engellilik_derecesi=engellilik_derecesi,
            takvim_esasli=takvim_esasli,
            ucret_tipi=ucret_tipi
        )
        calisan_id = data.get('calisan_id', '')
        calisan = None
        if calisan_id and calisan_id not in ['', '-', 'None']:
            try:
                calisan = Calisan.objects.filter(id=int(calisan_id), user=request.user).first()
            except (ValueError, TypeError):
                calisan = None
        yillik_ozet = sonuc.get('yillik_ozet', {})
        bordro = YillikBordro.objects.create(
            user=request.user,
            calisan=calisan,
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

@login_required(login_url='giris')
def yillik_sonuc(request, bordro_id):
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
    if isinstance(value, (int, float)):
        return float(value)

    s = str(value).strip()
    for unit in ['₺', 'TL', 'gün', 'saat', '%']:
        s = s.replace(unit, '')

    s = s.strip()
    if not s:
        return 0.0

    s = s.replace('.', '')
    s = s.replace(',', '.')

    try:
        return float(s)
    except ValueError:
        return 0.0

@login_required(login_url='giris')
def tazminat_hesapla(request):
    context = {
        'active_page': 'tazminat_hesaplama',
    }
    return render(request, 'tazminat_hesapla.html', context)

@csrf_exempt
def hesapla_ajax(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
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
@login_required(login_url='giris')
def tazminat_hesapla_api(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Sadece POST metodu kabul edilir'}, status=405)

    try:
        data = json.loads(request.body)
        giris_tarihi = data.get('giris_tarihi', '')
        cikis_tarihi = data.get('cikis_tarihi', '')
        aylik_brut = temizle_sayi_yillik(data.get('aylik_brut_ucret', '0'))
        aylik_ek = temizle_sayi_yillik(data.get('aylik_brut_ek_ucret', '0'))
        yillik_ikramiye = temizle_sayi_yillik(data.get('yillik_brut_ikramiye', '0'))
        kidem_disi_gun = int(temizle_sayi_yillik(data.get('kidem_disi_gun', '0')))
        kumulatif_gv = temizle_sayi_yillik(data.get('kumulatif_gv_matrahi', '0'))
        ihbar_hesaplansin = data.get('ihbar_hesaplansin', True)
        ihbar_gv = data.get('ihbar_gv_hesaplansin', True)
        ihbar_dv = data.get('ihbar_dv_hesaplansin', True)
        kidem_dv = data.get('kidem_dv_hesaplansin', True)
        calisan_id = data.get('calisan_id')
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

        calisan_id = data.get('calisan_id', '')
        calisan = None
        if calisan_id and calisan_id not in ['', '-', 'None']:
            try:
                calisan = Calisan.objects.filter(id=int(calisan_id), user=request.user).first()
            except (ValueError, TypeError):
                calisan = None

        from datetime import datetime

        def parse_tarih(tarih_str):
            if '-' in tarih_str and len(tarih_str.split('-')[0]) == 4:
                return datetime.strptime(tarih_str, "%Y-%m-%d").date()
            else:
                return datetime.strptime(tarih_str, "%d.%m.%Y").date()

        tazminat_kayit = Tazminat.objects.create(
            user=request.user,
            calisan=calisan,
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

def giris_yap(request):
    if request.user.is_authenticated:
        return redirect('home')
    context = {'active_page': 'giris'}

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            context['error'] = 'Kullanıcı adı veya şifre hatalı!'

    return render(request, 'giris.html', context)


def kayit_ol(request):
    if request.user.is_authenticated:
        return redirect('home')

    context = {'active_page': 'kayit'}

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        errors = []

        if not username:
            errors.append('Kullanıcı adı gerekli!')
        elif len(username) < 3:
            errors.append('Kullanıcı adı en az 3 karakter olmalı!')
        elif User.objects.filter(username=username).exists():
            errors.append('Bu kullanıcı adı zaten kullanılıyor!')

        if not email:
            errors.append('E-posta adresi gerekli!')
        elif User.objects.filter(email=email).exists():
            errors.append('Bu e-posta adresi zaten kayıtlı!')

        if not password:
            errors.append('Şifre gerekli!')
        elif len(password) < 8:
            errors.append('Şifre en az 8 karakter olmalı!')
        elif not any(c.isupper() for c in password):
            errors.append('Şifre en az bir büyük harf içermeli!')
        elif not any(c.isdigit() for c in password):
            errors.append('Şifre en az bir rakam içermeli!')
        elif password != password2:
            errors.append('Şifreler eşleşmiyor!')

        if errors:
            context['errors'] = errors
            context['form_data'] = {
                'username': username,
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
            }
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            login(request, user)
            return redirect('home')

    return render(request, 'kayit.html', context)

def cikis_yap(request):
    logout(request)
    return redirect('giris')

@login_required(login_url='giris')
def calisan_listele(request):
    calisanlar = Calisan.objects.filter(user=request.user, aktif=True).order_by('ad', 'soyad')

    data = [{
        'id': c.id,
        'ad': c.ad,
        'soyad': c.soyad,
        'tam_ad': c.tam_ad,
    } for c in calisanlar]

    return JsonResponse({'success': True, 'calisanlar': data})


@csrf_exempt
@login_required(login_url='giris')
def calisan_ekle(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Sadece POST metodu kabul edilir'}, status=405)

    try:
        data = json.loads(request.body)
        ad = data.get('ad', '').strip()
        soyad = data.get('soyad', '').strip()

        if not ad or not soyad:
            return JsonResponse({'success': False, 'error': 'Ad ve soyad zorunludur!'}, status=400)

        calisan = Calisan.objects.create(
            user=request.user,
            ad=ad,
            soyad=soyad,
        )

        return JsonResponse({
            'success': True,
            'message': 'Çalışan başarıyla eklendi!',
            'calisan': {
                'id': calisan.id,
                'ad': calisan.ad,
                'soyad': calisan.soyad,
                'tam_ad': calisan.tam_ad,
            }
        })

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Geçersiz JSON formatı'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
@login_required(login_url='giris')
def calisan_guncelle(request, calisan_id):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Sadece POST metodu kabul edilir'}, status=405)

    try:
        calisan = Calisan.objects.filter(id=calisan_id, user=request.user).first()
        if not calisan:
            return JsonResponse({'success': False, 'error': 'Çalışan bulunamadı!'}, status=404)

        data = json.loads(request.body)

        if 'ad' in data:
            calisan.ad = data['ad'].strip()
        if 'soyad' in data:
            calisan.soyad = data['soyad'].strip()

        calisan.save()

        return JsonResponse({
            'success': True,
            'message': 'Çalışan başarıyla güncellendi!',
            'calisan': {
                'id': calisan.id,
                'ad': calisan.ad,
                'soyad': calisan.soyad,
                'tam_ad': calisan.tam_ad,
            }
        })

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Geçersiz JSON formatı'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
@login_required(login_url='giris')
def calisan_sil(request, calisan_id):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Sadece POST metodu kabul edilir'}, status=405)

    try:
        calisan = Calisan.objects.filter(id=calisan_id, user=request.user).first()
        if not calisan:
            return JsonResponse({'success': False, 'error': 'Çalışan bulunamadı!'}, status=404)
        calisan.aktif = False
        calisan.save()
        return JsonResponse({
            'success': True,
            'message': f'{calisan.tam_ad} başarıyla silindi!'
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required(login_url='giris')
def calisan_detay(request, calisan_id):
    try:
        calisan = Calisan.objects.filter(id=calisan_id, user=request.user).first()
        if not calisan:
            return JsonResponse({'success': False, 'error': 'Çalışan bulunamadı!'}, status=404)

        return JsonResponse({
            'success': True,
            'calisan': {
                'id': calisan.id,
                'ad': calisan.ad,
                'soyad': calisan.soyad,
                'tam_ad': calisan.tam_ad,
            }
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required(login_url='giris')
def export_aylik_excel(request, bordro_id):
    try:
        bordro = AylikBordro.objects.filter(id=bordro_id,user=request.user).first()
        if not bordro:
            return HttpResponse("Bordro bulunamadı", status=404)

        calisan_adi = bordro.calisan.tam_ad if bordro.calisan else "Anonim"
        sonuc = bordro.hesaplama_sonuc

        output = create_aylik_bordro_excel(
            sonuc=sonuc,
            calisan_adi=calisan_adi,
            ay=bordro.bordro_ay,
            yil=bordro.bordro_yil
        )

        ay_adi = sonuc.get('donem', {}).get('ay_adi', {}).get('ad', 'Ocak') if isinstance(
            sonuc.get('donem', {}).get('ay_adi'), dict) else 'Ocak'
        filename = f"Bordro_{bordro.bordro_yil}_{ay_adi}_{calisan_adi.replace(' ', '_')}.xlsx"

        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

    except Exception as e:
        return HttpResponse(f"Hata: {str(e)}", status=500)


@login_required(login_url='giris')
def export_yillik_excel(request, bordro_id):
    try:
        bordro = YillikBordro.objects.filter(id=bordro_id, user=request.user).first()
        if not bordro:
            return HttpResponse("Bordro bulunamadı", status=404)

        calisan_adi = bordro.calisan.tam_ad if bordro.calisan else "Anonim"

        sonuc = {
            'aylik_sonuclar': bordro.aylik_sonuclar,
            'yillik_ozet': bordro.yillik_ozet
        }

        output = create_yillik_bordro_excel(
            sonuc=sonuc,
            calisan_adi=calisan_adi,
            yil=bordro.bordro_yili
        )

        filename = f"Yillik_Bordro_{bordro.bordro_yili}_{calisan_adi.replace(' ', '_')}.xlsx"

        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

    except Exception as e:
        return HttpResponse(f"Hata: {str(e)}", status=500)


@login_required(login_url='giris')
def export_tazminat_excel(request, tazminat_id):
    try:
        tazminat = Tazminat.objects.filter(id=tazminat_id, user=request.user).first()
        if not tazminat:
            return HttpResponse("Tazminat bulunamadı", status=404)

        calisan_adi = tazminat.calisan.tam_ad if tazminat.calisan else "Anonim"
        sonuc = tazminat.hesaplama_sonuc

        output = create_tazminat_excel(
            sonuc=sonuc,
            calisan_adi=calisan_adi
        )

        filename = f"Tazminat_{calisan_adi.replace(' ', '_')}.xlsx"

        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

    except Exception as e:
        return HttpResponse(f"Hata: {str(e)}", status=500)


@login_required(login_url='giris')
def calisan_yonetimi(request):
    calisan_filter = request.GET.get('calisan', '')
    yil_filter = request.GET.get('yil', '')
    ay_filter = request.GET.get('ay', '')
    tur_filter = request.GET.get('tur', 'hepsi')
    calisanlar = Calisan.objects.filter(user=request.user, aktif=True).order_by('ad', 'soyad')
    aylik_bordrolar = AylikBordro.objects.filter(user=request.user).order_by('-created_at')
    yillik_bordrolar = YillikBordro.objects.filter(user=request.user).order_by('-created_at')
    tazminatlar = Tazminat.objects.filter(user=request.user).order_by('-created_at')

    if calisan_filter:
        aylik_bordrolar = aylik_bordrolar.filter(calisan_id=calisan_filter)
        yillik_bordrolar = yillik_bordrolar.filter(calisan_id=calisan_filter)
        tazminatlar = tazminatlar.filter(calisan_id=calisan_filter)

    if yil_filter:
        aylik_bordrolar = aylik_bordrolar.filter(bordro_yil=yil_filter)
        yillik_bordrolar = yillik_bordrolar.filter(bordro_yili=yil_filter)

    if ay_filter:
        aylik_bordrolar = aylik_bordrolar.filter(bordro_ay=ay_filter)

    yillar = list(range(2020, 2031))
    aylar = [
        (1, 'Ocak'), (2, 'Şubat'), (3, 'Mart'), (4, 'Nisan'),
        (5, 'Mayıs'), (6, 'Haziran'), (7, 'Temmuz'), (8, 'Ağustos'),
        (9, 'Eylül'), (10, 'Ekim'), (11, 'Kasım'), (12, 'Aralık')
    ]

    context = {
        'active_page': 'calisan_yonetimi',
        'calisanlar': calisanlar,
        'aylik_bordrolar': aylik_bordrolar[:50],  # Son 50 kayıt
        'yillik_bordrolar': yillik_bordrolar[:50],
        'tazminatlar': tazminatlar[:50],
        'yillar': yillar,
        'aylar': aylar,
        'selected_calisan': calisan_filter,
        'selected_yil': yil_filter,
        'selected_ay': ay_filter,
        'selected_tur': tur_filter,
        'toplam_calisan': calisanlar.count(),
        'toplam_aylik': AylikBordro.objects.filter(user=request.user).count(),
        'toplam_yillik': YillikBordro.objects.filter(user=request.user).count(),
        'toplam_tazminat': Tazminat.objects.filter(user=request.user).count(),
    }

    return render(request, 'calisan_yonetimi.html', context)


@csrf_exempt
@login_required(login_url='giris')
def aylik_bordro_sil(request, bordro_id):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Sadece POST metodu kabul edilir'}, status=405)

    try:
        bordro = AylikBordro.objects.filter(id=bordro_id, user=request.user).first()
        if not bordro:
            return JsonResponse({'success': False, 'error': 'Bordro bulunamadı!'}, status=404)

        bordro.delete()
        return JsonResponse({'success': True, 'message': 'Bordro başarıyla silindi!'})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
@login_required(login_url='giris')
def yillik_bordro_sil(request, bordro_id):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Sadece POST metodu kabul edilir'}, status=405)

    try:
        bordro = YillikBordro.objects.filter(id=bordro_id, user=request.user).first()
        if not bordro:
            return JsonResponse({'success': False, 'error': 'Bordro bulunamadı!'}, status=404)

        bordro.delete()
        return JsonResponse({'success': True, 'message': 'Bordro başarıyla silindi!'})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
@login_required(login_url='giris')
def tazminat_sil(request, tazminat_id):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Sadece POST metodu kabul edilir'}, status=405)

    try:
        tazminat = Tazminat.objects.filter(id=tazminat_id, user=request.user).first()
        if not tazminat:
            return JsonResponse({'success': False, 'error': 'Tazminat bulunamadı!'}, status=404)

        tazminat.delete()
        return JsonResponse({'success': True, 'message': 'Tazminat başarıyla silindi!'})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required(login_url='giris')
def profil(request):
    """Kullanıcı profil sayfası"""
    user = request.user

    # İstatistikler
    toplam_calisan = Calisan.objects.filter(user=user, aktif=True).count()
    toplam_aylik = AylikBordro.objects.filter(user=user).count()
    toplam_yillik = YillikBordro.objects.filter(user=user).count()
    toplam_tazminat = Tazminat.objects.filter(user=user).count()

    context = {
        'active_page': 'profil',
        'toplam_calisan': toplam_calisan,
        'toplam_aylik': toplam_aylik,
        'toplam_yillik': toplam_yillik,
        'toplam_tazminat': toplam_tazminat,
    }

    return render(request, 'profil.html', context)


@csrf_exempt
@login_required(login_url='giris')
def profil_guncelle(request):
    """Profil bilgilerini güncelle"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Sadece POST metodu kabul edilir'}, status=405)

    try:
        data = json.loads(request.body)
        user = request.user

        # Bilgileri güncelle
        if 'first_name' in data:
            user.first_name = data['first_name'].strip()
        if 'last_name' in data:
            user.last_name = data['last_name'].strip()
        if 'email' in data:
            user.email = data['email'].strip()

        user.save()

        return JsonResponse({
            'success': True,
            'message': 'Profil bilgileri güncellendi!'
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
@login_required(login_url='giris')
def sifre_degistir(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Sadece POST metodu kabul edilir'}, status=405)
    try:
        data = json.loads(request.body)
        user = request.user
        mevcut_sifre = data.get('mevcut_sifre', '')
        yeni_sifre = data.get('yeni_sifre', '')
        yeni_sifre_tekrar = data.get('yeni_sifre_tekrar', '')

        if not user.check_password(mevcut_sifre):
            return JsonResponse({'success': False, 'error': 'Mevcut şifre yanlış!'}, status=400)

        if len(yeni_sifre) < 8:
            return JsonResponse({'success': False, 'error': 'Şifre en az 8 karakter olmalı!'}, status=400)

        if not any(c.isupper() for c in yeni_sifre):
            return JsonResponse({'success': False, 'error': 'Şifre en az bir büyük harf içermeli!'}, status=400)

        if not any(c.isdigit() for c in yeni_sifre):
            return JsonResponse({'success': False, 'error': 'Şifre en az bir rakam içermeli!'}, status=400)

        if yeni_sifre != yeni_sifre_tekrar:
            return JsonResponse({'success': False, 'error': 'Yeni şifreler eşleşmiyor!'}, status=400)

        user.set_password(yeni_sifre)
        user.save()
        from django.contrib.auth import update_session_auth_hash
        update_session_auth_hash(request, user)
        return JsonResponse({
            'success': True,
            'message': 'Şifreniz başarıyla değiştirildi!'
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@staff_member_required(login_url='giris')
def admin_panel(request):
    """Admin paneli - Kullanıcı yönetimi"""

    # Tüm kullanıcıları getir
    kullanicilar = User.objects.all().order_by('-date_joined')

    # Her kullanıcı için istatistik hesapla
    kullanici_listesi = []
    for user in kullanicilar:
        kullanici_listesi.append({
            'user': user,
            'calisan_sayisi': Calisan.objects.filter(user=user, aktif=True).count(),
            'aylik_bordro': AylikBordro.objects.filter(user=user).count(),
            'yillik_bordro': YillikBordro.objects.filter(user=user).count(),
            'tazminat': Tazminat.objects.filter(user=user).count(),
        })

    context = {
        'active_page': 'admin_panel',
        'kullanicilar': kullanici_listesi,
        'toplam_kullanici': kullanicilar.count(),
    }

    return render(request, 'admin_panel.html', context)


@csrf_exempt
@staff_member_required(login_url='giris')
def admin_kullanici_ekle(request):
    """Yeni kullanıcı ekle"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Sadece POST metodu kabul edilir'}, status=405)

    try:
        data = json.loads(request.body)

        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()
        is_staff = data.get('is_staff', False)

        # Validasyonlar
        if not username:
            return JsonResponse({'success': False, 'error': 'Kullanıcı adı zorunludur!'}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'success': False, 'error': 'Bu kullanıcı adı zaten mevcut!'}, status=400)

        if email and User.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'error': 'Bu e-posta zaten kullanılıyor!'}, status=400)

        if len(password) < 8:
            return JsonResponse({'success': False, 'error': 'Şifre en az 8 karakter olmalı!'}, status=400)

        if not any(c.isupper() for c in password):
            return JsonResponse({'success': False, 'error': 'Şifre en az bir büyük harf içermeli!'}, status=400)

        if not any(c.isdigit() for c in password):
            return JsonResponse({'success': False, 'error': 'Şifre en az bir rakam içermeli!'}, status=400)

        # Kullanıcı oluştur
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_staff = is_staff
        user.save()

        return JsonResponse({
            'success': True,
            'message': f'"{username}" kullanıcısı başarıyla oluşturuldu!',
            'user_id': user.id
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
@staff_member_required(login_url='giris')
def admin_kullanici_guncelle(request, user_id):
    """Kullanıcı bilgilerini güncelle"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Sadece POST metodu kabul edilir'}, status=405)

    try:
        user = User.objects.filter(id=user_id).first()
        if not user:
            return JsonResponse({'success': False, 'error': 'Kullanıcı bulunamadı!'}, status=404)

        data = json.loads(request.body)

        # Bilgileri güncelle
        if 'first_name' in data:
            user.first_name = data['first_name'].strip()
        if 'last_name' in data:
            user.last_name = data['last_name'].strip()
        if 'email' in data:
            new_email = data['email'].strip()
            if new_email and new_email != user.email:
                if User.objects.filter(email=new_email).exclude(id=user_id).exists():
                    return JsonResponse({'success': False, 'error': 'Bu e-posta zaten kullanılıyor!'}, status=400)
                user.email = new_email
        if 'is_active' in data:
            user.is_active = data['is_active']
        if 'is_staff' in data:
            user.is_staff = data['is_staff']

        # Şifre değişikliği (opsiyonel)
        if data.get('password'):
            password = data['password']
            if len(password) < 8:
                return JsonResponse({'success': False, 'error': 'Şifre en az 8 karakter olmalı!'}, status=400)
            if not any(c.isupper() for c in password):
                return JsonResponse({'success': False, 'error': 'Şifre en az bir büyük harf içermeli!'}, status=400)
            if not any(c.isdigit() for c in password):
                return JsonResponse({'success': False, 'error': 'Şifre en az bir rakam içermeli!'}, status=400)
            user.set_password(password)

        user.save()

        return JsonResponse({
            'success': True,
            'message': f'"{user.username}" kullanıcısı güncellendi!'
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
@staff_member_required(login_url='giris')
def admin_kullanici_sil(request, user_id):
    """Kullanıcıyı sil"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Sadece POST metodu kabul edilir'}, status=405)

    try:
        user = User.objects.filter(id=user_id).first()
        if not user:
            return JsonResponse({'success': False, 'error': 'Kullanıcı bulunamadı!'}, status=404)

        # Kendini silmeye çalışıyorsa engelle
        if user.id == request.user.id:
            return JsonResponse({'success': False, 'error': 'Kendinizi silemezsiniz!'}, status=400)

        # Superuser'ı silmeye çalışıyorsa engelle
        if user.is_superuser:
            return JsonResponse({'success': False, 'error': 'Superuser silinemez!'}, status=400)

        username = user.username
        user.delete()

        return JsonResponse({
            'success': True,
            'message': f'"{username}" kullanıcısı silindi!'
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)