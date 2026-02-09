
document.addEventListener('DOMContentLoaded', function() {
    calisanlariYukle();
    butonlariBagla();
    selectleriSenkronizeEt();
});

function calisanlariYukle() {
    const selectler = document.querySelectorAll('.action-select');
    if (selectler.length === 0) return;

    fetch('/api/calisanlar/')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const mevcutDeger = selectler[0].value;
                selectler.forEach(select => {
                    select.innerHTML = '<option value="">- Çalışan Seçin -</option>';
                    data.calisanlar.forEach(c => {
                        const option = document.createElement('option');
                        option.value = c.id;
                        option.textContent = c.tam_ad;
                        option.dataset.calisan = JSON.stringify(c);
                        select.appendChild(option);
                    });

                    if (mevcutDeger) {
                        select.value = mevcutDeger;
                    }
                });
            }
        })
        .catch(error => console.error('Çalışanlar yüklenemedi:', error));
}

function selectleriSenkronizeEt() {
    const selectler = document.querySelectorAll('.action-select');
    selectler.forEach(select => {
        select.addEventListener('change', function() {
            const secilenDeger = this.value;
            selectler.forEach(digerSelect => {
                if (digerSelect !== this) {
                    digerSelect.value = secilenDeger;
                }
            });

            if (secilenDeger) {
                calisanBilgileriniDoldur(secilenDeger);
            }
        });
    });
}

function calisanBilgileriniDoldur(calisanId) {
    fetch(`/api/calisan/${calisanId}/`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const c = data.calisan;
                console.log('Çalışan seçildi:', c.tam_ad);
            }
        })
        .catch(error => console.error('Çalışan bilgisi alınamadı:', error));
}

function butonlariBagla() {
    document.querySelectorAll('.icon-btn.green, .action-btn.green').forEach(btn => {
        if (!btn.classList.contains('action-btn-large')) {
            btn.addEventListener('click', yeniCalisanEkle);
        }
    });

    document.querySelectorAll('.icon-btn.yellow, .action-btn.cyan').forEach(btn => {
        btn.addEventListener('click', calisanAdiDuzenle);
    });

    document.querySelectorAll('.icon-btn.red, .action-btn.red').forEach(btn => {
        if (!btn.classList.contains('action-btn-large')) {
            btn.addEventListener('click', calisanSil);
        }
    });
}

function yeniCalisanEkle() {
    const adSoyad = prompt('Yeni çalışan adı soyadı:');
    if (!adSoyad || !adSoyad.trim()) return;

    const parcalar = adSoyad.trim().split(' ');
    const ad = parcalar[0];
    const soyad = parcalar.slice(1).join(' ') || '-';

    fetch('/api/calisan/ekle/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ ad: ad, soyad: soyad })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Çalışan eklendi: ' + data.calisan.tam_ad);
            calisanlariYukle();
            setTimeout(() => {
                document.querySelectorAll('.action-select').forEach(select => {
                    select.value = data.calisan.id;
                });
            }, 300);
        } else {
            alert('Hata: ' + data.error);
        }
    })
    .catch(error => alert('Hata oluştu: ' + error));
}

function calisanAdiDuzenle() {
    const select = document.querySelector('.action-select');

    if (!select) {
        alert('Bu sayfada çalışan seçimi bulunmuyor!');
        return;
    }

    const calisanId = select.value;

    if (!calisanId) {
        alert('Lütfen bir çalışan seçin!');
        return;
    }

    const mevcutAd = select.options[select.selectedIndex].textContent;
    const yeniAdSoyad = prompt('Yeni ad soyad:', mevcutAd);

    if (!yeniAdSoyad || !yeniAdSoyad.trim() || yeniAdSoyad === mevcutAd) return;

    const parcalar = yeniAdSoyad.trim().split(' ');
    const ad = parcalar[0];
    const soyad = parcalar.slice(1).join(' ') || '-';

    fetch(`/api/calisan/${calisanId}/guncelle/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ ad: ad, soyad: soyad })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Çalışan güncellendi!');
            calisanlariYukle();
            setTimeout(() => {
                document.querySelectorAll('.action-select').forEach(select => {
                    select.value = calisanId;
                });
            }, 300);
        } else {
            alert('Hata: ' + data.error);
        }
    })
    .catch(error => alert('Hata oluştu: ' + error));
}

function calisanSil() {
    const select = document.querySelector('.action-select');

    if (!select) {
        alert('Bu sayfada çalışan seçimi bulunmuyor!');
        return;
    }

    const calisanId = select.value;

    if (!calisanId) {
        alert('Lütfen bir çalışan seçin!');
        return;
    }

    const calisanAd = select.options[select.selectedIndex].textContent;

    if (!confirm(`"${calisanAd}" silinecek. Emin misiniz?`)) return;

    fetch(`/api/calisan/${calisanId}/sil/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            calisanlariYukle();
        } else {
            alert('Hata: ' + data.error);
        }
    })
    .catch(error => alert('Hata oluştu: ' + error));
}

function getSeciliCalisan() {
    const select = document.querySelector('.action-select');
    if (!select || !select.value) return null;

    const option = select.options[select.selectedIndex];
    if (option.dataset.calisan) {
        return JSON.parse(option.dataset.calisan);
    }
    return { id: select.value };
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}