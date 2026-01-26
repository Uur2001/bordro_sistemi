from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('ozellikler/', views.ozellikler, name='ozellikler'),
    path('hakkinda/', views.hakkinda, name='hakkinda'),
    path('iletisim/', views.iletisim, name='iletisim'),
    path('bordro-sihirbazi/', views.bordro_sihirbazi, name='bordro_sihirbazi'),
    path('bordro-sihirbazi/aylik/', views.aylik_hesapla, name='aylik_hesapla'),
    path('bordro-sihirbazi/yillik/', views.yillik_hesapla, name='yillik_hesapla'),
    path('tazminat-hesapla/', views.tazminat_hesapla, name='tazminat_hesapla'),
]