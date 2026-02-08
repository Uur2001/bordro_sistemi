from django.contrib import admin
from .models import Calisan, AylikBordro, YillikBordro, Tazminat

@admin.register(Calisan)
class CalisanAdmin(admin.ModelAdmin):
    list_display = ['tam_ad', 'aktif', 'created_at']
    list_filter = ['aktif']
    search_fields = ['ad', 'soyad']
    ordering = ['ad', 'soyad']

    def tam_ad(self, obj):
        return f"{obj.ad} {obj.soyad}"

    tam_ad.short_description = 'Ad Soyad'

@admin.register(AylikBordro)
class AylikBordroAdmin(admin.ModelAdmin):
    list_display = ['calisan', 'bordro_yil', 'bordro_ay', 'aylik_temel_ucret']
    list_filter = ['bordro_yil', 'bordro_ay']

admin.site.register(YillikBordro)
admin.site.register(Tazminat)
