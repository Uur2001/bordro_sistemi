from django.db import models
from django.utils import timezone


class Calisan(models.Model):
    """Çalışan Bilgileri"""
    ad_soyad = models.CharField(max_length=200)
    tc_no = models.CharField(max_length=11, unique=True)
    giris_tarihi = models.DateField()
    cikis_tarihi = models.DateField(null=True, blank=True)
    aktif = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Çalışan"
        verbose_name_plural = "Çalışanlar"

    def __str__(self):
        return self.ad_soyad


class AylikBordro(models.Model):
    """Aylık Bordro Hesaplaması"""
    BRUT_NET_CHOICES = [
        ('brut', 'Brüt'),
        ('net', 'Net'),
    ]

    ENGELLILIK_CHOICES = [
        ('normal', 'Normal'),
        ('1_derece', '1. Derece'),
        ('2_derece', '2. Derece'),
        ('3_derece', '3. Derece'),
    ]

    calisan = models.ForeignKey(Calisan, on_delete=models.CASCADE, related_name='bordrolar', null=True, blank=True)

    # Temel Ücret
    bordro_ay = models.IntegerField(choices=[(i, i) for i in range(1, 13)])
    bordro_yil = models.IntegerField()
    aylik_temel_ucret = models.DecimalField(max_digits=12, decimal_places=2)
    ucret_tipi = models.CharField(max_length=10, choices=BRUT_NET_CHOICES, default='brut')
    gelir_vergisi = models.BooleanField(default=True)
    damga_vergisi = models.BooleanField(default=True)
    engellilik_durumu = models.CharField(max_length=20, choices=ENGELLILIK_CHOICES, default='normal')
    yillik_gv_matrahi = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    yillik_asg_ucret_gv_matrahi = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Çalışma Bilgileri
    gun_sayisi_tipi = models.CharField(max_length=20, default='takvim')
    calisilan_gun = models.IntegerField(default=30)
    eksik_saat = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    # Sosyal Güvenlik
    sgk_tipi = models.CharField(max_length=100, default='01')
    kanun_no = models.CharField(max_length=20, default='00000')
    hazine_yardimi = models.BooleanField(default=True)
    bes = models.BooleanField(default=False)
    devir_matrah_2ay = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    devir_matrah_1ay = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Özel Sigortalar
    saglik_sig_isci = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    saglik_sig_isveren = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    hayat_sig_isci = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    hayat_sig_isveren = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Fazla Mesailer
    fm01_saat = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    fm02_saat = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    fm03_saat = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    # Hesaplama Sonuçları (JSON olarak saklanabilir)
    hesaplama_sonuc = models.JSONField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Aylık Bordro"
        verbose_name_plural = "Aylık Bordrolar"
        unique_together = ['calisan', 'bordro_yil', 'bordro_ay']

    def __str__(self):
        return f"{self.bordro_yil}/{self.bordro_ay} - {self.calisan if self.calisan else 'Anonim'}"


class YillikBordro(models.Model):
    """Yıllık Bordro Hesaplaması"""
    calisan = models.ForeignKey(Calisan, on_delete=models.CASCADE, related_name='yillik_bordrolar', null=True,
                                blank=True)
    bordro_yili = models.IntegerField()

    # Her ay için ayrı alanlar (JSON olarak da tutulabilir)
    aylik_veriler = models.JSONField()  # 12 aylık tüm veriler

    # Toplam Matrahlar
    toplam_gv_matrahi = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    toplam_sgk_matrahi = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Yıllık Bordro"
        verbose_name_plural = "Yıllık Bordrolar"
        unique_together = ['calisan', 'bordro_yili']


class Tazminat(models.Model):
    """Kıdem ve İhbar Tazminatı"""
    calisan = models.ForeignKey(Calisan, on_delete=models.CASCADE, related_name='tazminatlar')

    giris_tarihi = models.DateField()
    cikis_tarihi = models.DateField()
    kidem_disi_sure = models.IntegerField(default=0)  # gün cinsinden

    aylik_brut_ucret = models.DecimalField(max_digits=12, decimal_places=2)
    aylik_brut_ek_ucret = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    yillik_brut_ikramiye = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    ihbar_tazminati = models.BooleanField(default=True)
    ihbar_gelir_vergisi = models.BooleanField(default=True)
    ihbar_damga_vergisi = models.BooleanField(default=True)
    kidem_damga_vergisi = models.BooleanField(default=True)

    hesaplama_sonuc = models.JSONField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Tazminat"
        verbose_name_plural = "Tazminatlar"