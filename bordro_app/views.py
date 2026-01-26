from django.shortcuts import render

# Ana Sayfa - Nedir
def home(request):
    return render(request, 'home.html', {'active_page': 'nedir'})

# Özellikler Sayfası
def ozellikler(request):
    return render(request, 'ozellikler.html', {'active_page': 'ozellikler'})

# Hakkında Sayfası
def hakkinda(request):
    return render(request, 'hakkinda.html', {'active_page': 'hakkinda'})

# İletişim Sayfası
def iletisim(request):
    return render(request, 'iletisim.html', {'active_page': 'iletisim'})

# Bordro Sihirbazı Ana Sayfa
def bordro_sihirbazi(request):
    return render(request, 'bordro_sihirbazi.html', {'active_page': 'nedir'})

# Aylık Hesaplama Sihirbazı
def aylik_hesapla(request):
    return render(request, 'aylik_hesapla.html', {'active_page': 'nedir'})

# Yıllık Hesaplama Sihirbazı
def yillik_hesapla(request):
    return render(request, 'yillik_hesapla.html', {'active_page': 'nedir'})

# Tazminat Hesaplama Sayfası
def tazminat_hesapla(request):
    return render(request, 'tazminat_hesapla.html', {'active_page': 'nedir'})