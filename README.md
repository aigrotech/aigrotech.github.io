# AIgro web sitesi

AIgro çözümlerini anlatan iki dilli (TR/EN) statik site: Akıllı Besin Dozajlama, Su Takip Sistemi ve Dikey Tarım Modülü. Türkçe sayfalar kökte, İngilizce sayfalar `en/` altında. Çıktı saf HTML/CSS/JS olduğu için GitHub Pages doğrudan yayınlar.

## Sayfalar

| Dosya | İçerik |
| --- | --- |
| `index.html` | Ana sayfa: çözümler, platform, panel, hedefler, saha, hakkımızda |
| `akilli-dozajlama.html` | Kapalı döngü, güvenlik katmanı, panel, pilot süreci, SSS |
| `su-takibi.html` | Özellikler, gerçek panel, saha kurulumu, SSS |
| `dikey-tarim.html` | Konsept, modül yapısı ve ölçüler, bitkiler |
| `iletisim.html` | İletişim; form e-posta uygulamasını açar (sunucuya veri göndermez) |
| `en/*.html` | İngilizce karşılıklar: `index`, `smart-dosing`, `water-monitoring`, `vertical-farming`, `contact` |

## Düzenleme

Sayfaları **`src/`** altında düzenleyin, sonra derleyin:

```bash
python tools/build.py
```

- `src/layout.html` — ortak header, menü, footer
- `src/pages/tr/*.html`, `src/pages/en/*.html` — sayfa içerikleri (üstte başlık/açıklama bilgisi)
- `tools/build.py` — dil metinleri (`STRINGS`), sayfa adları (`PAGES`) ve **iletişim e-postası (`CONTACT_EMAIL`, tek yerden)**
- `tools/og_cards.py` — paylaşım önizleme kartlarını yeniden üretir
- `src/icons.svg` — ikon seti
- `assets/css/style.css`, `assets/js/main.js` — tasarım sistemi ve davranışlar

Derleme; Unsplash görsel bağlantılarını, ikonları ve "AIgro" yazımını (büyük I'nın "l" gibi okunmaması için) otomatik üretir. Kök dizindeki `*.html` dosyalarını elle düzenlemeyin.

## Referans logoları

Alttaki kayan referans barı `src/layout.html` içinde. Logo dosyaları `assets/img/ref/` altında; şu an yalnızca Harves logosu var, AlPolimer ve Özdoğu geçici olarak yazıyla gösteriliyor. Logo geldiğinde dosyayı bu klasöre koyup ilgili `<span class="logo-word">` satırını `<img>` ile değiştirin (her iki listede de).

## Yerelde açma

```bash
python -m http.server 8765
```

## GitHub Pages ile yayın

1. Depoyu GitHub'a gönderin (`main`).
2. Settings → Pages → Source: **Deploy from a branch**, `main` / `(root)`.
3. Site `https://aigrotech.github.io/` adresinde açılır (organizasyon: aigrotech, depo: aigrotech.github.io). Adres değişirse `tools/build.py` içindeki `SITE_URL`'i güncelleyip yeniden derleyin (canonical ve paylaşım önizlemesi bu adresi kullanır).

## İçerik kuralları

- Metinler AKSİYOM ürün sunumundaki doğrulanmış içerikten alınmıştır. Doğrulanmamış donanım/performans iddiası eklemeyin.
- Dozaj paneli bir tasarımdır; değerleri **örnek veridir** (sayfada belirtilir).
- %25–35 su vb. oranlar literatüre dayalı **hedeflerdir**; ölçülmüş sonuç değildir.
- Dikey tarım görselleri **konsept** tasarımdır.
- Sera atmosfer fotoğrafları Unsplash lisanslı, temsili görsellerdir; ürün kanıtı olarak gerçek saha fotoğrafları kullanılır.
