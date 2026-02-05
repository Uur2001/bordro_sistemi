from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('bordro-sihirbazi/', views.bordro_sihirbazi, name='bordro_sihirbazi'),
    path('bordro-sihirbazi/aylik/', views.aylik_hesapla, name='aylik_hesapla'),
    path('bordro-sihirbazi/yillik/', views.yillik_hesapla, name='yillik_hesapla'),
    path('bordro-sihirbazi/yillik/api/', views.yillik_hesapla_api, name='yillik_hesapla_api'),
    path('bordro-sihirbazi/yillik/sonuc/<int:bordro_id>/', views.yillik_sonuc, name='yillik_sonuc'),
    path('tazminat-hesapla/', views.tazminat_hesapla, name='tazminat_hesapla'),
    path('tazminat-hesapla/api/', views.tazminat_hesapla_api, name='tazminat_hesapla_api'),
    path('hesapla-ajax/', views.hesapla_ajax, name='hesapla_ajax'),
]