from django.contrib import admin
from .models import Calisan, AylikBordro, YillikBordro, Tazminat

@admin.register(Calisan)
class CalisanAdmin(admin.ModelAdmin):
    list_display = ['ad_soyad', 'tc_no', 'giris_tarihi', 'aktif']
    search_fields = ['ad_soyad', 'tc_no']

@admin.register(AylikBordro)
class AylikBordroAdmin(admin.ModelAdmin):
    list_display = ['calisan', 'bordro_yil', 'bordro_ay', 'aylik_temel_ucret']
    list_filter = ['bordro_yil', 'bordro_ay']

admin.site.register(YillikBordro)
admin.site.register(Tazminat)
