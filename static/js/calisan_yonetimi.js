
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

document.addEventListener('DOMContentLoaded', function() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    if (tabButtons.length > 0) {
        tabButtons.forEach(btn => {
            btn.addEventListener('click', function() {
                document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
                document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));

                this.classList.add('active');
                document.getElementById('tab-' + this.dataset.tab).classList.add('active');
            });
        });
    }

    const modal = document.getElementById('calisanModal');
    if (modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === this) modalKapat();
        });
    }
});

function filterTable(type) {
    const calisanSelect = document.getElementById('filter-calisan-' + type);
    const table = document.getElementById('table-' + type);

    if (!calisanSelect || !table) return;

    const calisanVal = calisanSelect.value;
    const rows = table.querySelectorAll('tbody tr');

    let yilVal = '';
    let ayVal = '';

    if (type === 'aylik') {
        const yilSelect = document.getElementById('filter-yil-aylik');
        const aySelect = document.getElementById('filter-ay-aylik');
        if (yilSelect) yilVal = yilSelect.value;
        if (aySelect) ayVal = aySelect.value;
    } else if (type === 'yillik') {
        const yilSelect = document.getElementById('filter-yil-yillik');
        if (yilSelect) yilVal = yilSelect.value;
    }

    rows.forEach(row => {
        if (row.querySelector('.empty-message')) return;

        const rowCalisan = row.dataset.calisan || '';
        const rowYil = row.dataset.yil || '';
        const rowAy = row.dataset.ay || '';

        let show = true;

        if (calisanVal && rowCalisan !== calisanVal) show = false;
        if (yilVal && rowYil !== yilVal) show = false;
        if (ayVal && rowAy !== ayVal) show = false;

        row.style.display = show ? '' : 'none';
    });
}

function yeniCalisanModal() {
    document.getElementById('modalTitle').textContent = 'Yeni Çalışan Ekle';
    document.getElementById('calisan_id').value = '';
    document.getElementById('calisan_ad').value = '';
    document.getElementById('calisan_soyad').value = '';
    document.getElementById('calisanModal').classList.add('active');
}

function calisanDuzenle(id, ad, soyad) {
    document.getElementById('modalTitle').textContent = 'Çalışan Düzenle';
    document.getElementById('calisan_id').value = id;
    document.getElementById('calisan_ad').value = ad;
    document.getElementById('calisan_soyad').value = soyad;
    document.getElementById('calisanModal').classList.add('active');
}

function modalKapat() {
    const modal = document.getElementById('calisanModal');
    if (modal) modal.classList.remove('active');
}

async function calisanKaydet() {
    const id = document.getElementById('calisan_id').value;
    const ad = document.getElementById('calisan_ad').value.trim();
    const soyad = document.getElementById('calisan_soyad').value.trim();

    if (!ad || !soyad) {
        alert('Ad ve soyad alanları zorunludur!');
        return;
    }

    const url = id ? `/api/calisan/${id}/guncelle/` : '/api/calisan/ekle/';

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ ad, soyad })
        });

        const result = await response.json();

        if (result.success) {
            alert(result.message);
            location.reload();
        } else {
            alert('Hata: ' + result.error);
        }
    } catch (error) {
        alert('Bağlantı hatası: ' + error.message);
    }
}

async function calisanSilById(id, ad) {
    if (!confirm(`"${ad}" isimli çalışanı silmek istediğinize emin misiniz?`)) return;

    try {
        const response = await fetch(`/api/calisan/${id}/sil/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });

        const result = await response.json();

        if (result.success) {
            alert(result.message);
            location.reload();
        } else {
            alert('Hata: ' + result.error);
        }
    } catch (error) {
        alert('Bağlantı hatası: ' + error.message);
    }
}

async function aylikBordroSil(id) {
    if (!confirm('Bu bordroyu silmek istediğinize emin misiniz?')) return;

    try {
        const response = await fetch(`/api/aylik-bordro/${id}/sil/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });

        const result = await response.json();

        if (result.success) {
            alert(result.message);
            location.reload();
        } else {
            alert('Hata: ' + result.error);
        }
    } catch (error) {
        alert('Bağlantı hatası: ' + error.message);
    }
}

async function yillikBordroSil(id) {
    if (!confirm('Bu bordroyu silmek istediğinize emin misiniz?')) return;

    try {
        const response = await fetch(`/api/yillik-bordro/${id}/sil/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });

        const result = await response.json();

        if (result.success) {
            alert(result.message);
            location.reload();
        } else {
            alert('Hata: ' + result.error);
        }
    } catch (error) {
        alert('Bağlantı hatası: ' + error.message);
    }
}

async function tazminatSil(id) {
    if (!confirm('Bu tazminat kaydını silmek istediğinize emin misiniz?')) return;

    try {
        const response = await fetch(`/api/tazminat/${id}/sil/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });

        const result = await response.json();

        if (result.success) {
            alert(result.message);
            location.reload();
        } else {
            alert('Hata: ' + result.error);
        }
    } catch (error) {
        alert('Bağlantı hatası: ' + error.message);
    }
}