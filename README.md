# AIgro web sitesi

AKSİYOM İleri Teknoloji ve Ar-Ge'nin AIgro çözümlerini anlatan statik kurumsal site: Akıllı Besin Dozajlama, Su Takip Sistemi ve Dikey Tarım Modülü. Çıktı saf HTML/CSS/JS olduğu için GitHub Pages doğrudan yayınlar.

## Sayfalar

| Dosya | İçerik |
| --- | --- |
| `index.html` | Ana sayfa: çözümler, platform, panel, hedefler, saha, hakkımızda |
| `akilli-dozajlama.html` | Kapalı döngü, güvenlik katmanı, panel, pilot süreci, SSS |
| `su-takibi.html` | Özellikler, gerçek panel, saha kurulumu, referanslar, SSS |
| `dikey-tarim.html` | Konsept, modül yapısı ve ölçüler, bitkiler |
| `iletisim.html` | İletişim; form e-posta uygulamasını açar (sunucuya veri göndermez) |

## Düzenleme

Sayfaları **`src/`** altında düzenleyin, sonra derleyin:

```bash
python tools/build.py
```

- `src/layout.html` — ortak header, menü, footer
- `src/pages/*.html` — sayfa içerikleri (üstte başlık/açıklama bilgisi)
- `src/icons.svg` — ikon seti
- `assets/css/style.css`, `assets/js/main.js` — tasarım sistemi ve davranışlar

Derleme; Unsplash görsel bağlantılarını, ikonları ve "AIgro" yazımını (büyük I'nın "l" gibi okunmaması için) otomatik üretir. Kök dizindeki `*.html` dosyalarını elle düzenlemeyin.

## Yerelde açma

```bash
python -m http.server 8765
```

## GitHub Pages ile yayın

1. Depoyu GitHub'a gönderin (`main`).
2. Settings → Pages → Source: **Deploy from a branch**, `main` / `(root)`.
3. Site `https://<kullanıcı>.github.io/<depo>/` adresinde açılır. Adres farklıysa `tools/build.py` içindeki `SITE_URL`'i güncelleyip yeniden derleyin (canonical ve paylaşım önizlemesi bu adresi kullanır).

## İçerik kuralları

- Metinler AKSİYOM ürün sunumundaki doğrulanmış içerikten alınmıştır. Doğrulanmamış donanım/performans iddiası eklemeyin.
- Dozaj paneli bir tasarımdır; değerleri **örnek veridir** (sayfada belirtilir).
- %25–35 su vb. oranlar literatüre dayalı **hedeflerdir**; ölçülmüş sonuç değildir.
- Dikey tarım görselleri **konsept** tasarımdır.
- Sera atmosfer fotoğrafları Unsplash lisanslı, temsili görsellerdir; ürün kanıtı olarak gerçek saha fotoğrafları kullanılır.
