from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('giris/', views.giris_yap, name='giris'),
    path('kayit/', views.kayit_ol, name='kayit'),
    path('cikis/', views.cikis_yap, name='cikis'),
    path('bordro-sihirbazi/', views.bordro_sihirbazi, name='bordro_sihirbazi'),
    path('bordro-sihirbazi/aylik/', views.aylik_hesapla, name='aylik_hesapla'),
    path('bordro-sihirbazi/yillik/', views.yillik_hesapla, name='yillik_hesapla'),
    path('bordro-sihirbazi/yillik/api/', views.yillik_hesapla_api, name='yillik_hesapla_api'),
    path('bordro-sihirbazi/yillik/sonuc/<int:bordro_id>/', views.yillik_sonuc, name='yillik_sonuc'),
    path('tazminat-hesapla/', views.tazminat_hesapla, name='tazminat_hesapla'),
    path('tazminat-hesapla/api/', views.tazminat_hesapla_api, name='tazminat_hesapla_api'),
    path('hesapla-ajax/', views.hesapla_ajax, name='hesapla_ajax'),
    path('api/calisanlar/', views.calisan_listele, name='calisan_listele'),
    path('api/calisan/ekle/', views.calisan_ekle, name='calisan_ekle'),
    path('api/calisan/<int:calisan_id>/', views.calisan_detay, name='calisan_detay'),
    path('api/calisan/<int:calisan_id>/guncelle/', views.calisan_guncelle, name='calisan_guncelle'),
    path('api/calisan/<int:calisan_id>/sil/', views.calisan_sil, name='calisan_sil'),
]