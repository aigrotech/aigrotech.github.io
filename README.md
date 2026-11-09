# AIgro tanıtım sitesi

AKSİYOM İleri Teknoloji ve Ar-Ge'nin AIgro çözümlerini (Su Takip Sistemi + Akıllı Besin Dozajlama) anlatan tek sayfalık statik site. Derleme adımı yok; GitHub Pages doğrudan yayınlar.

## Yerelde açma

```bash
python -m http.server 8765
```

Sonra http://localhost:8765 adresini açın.

## GitHub Pages ile yayın

1. Depoyu GitHub'a gönderin (`main` dalı).
2. Settings → Pages → Source: **Deploy from a branch**, Branch: `main` / `(root)`.
3. Birkaç dakika sonra site `https://<kullanıcı>.github.io/<depo-adı>/` adresinde açılır.

## İçerik kaynağı ve kurallar

- Metinler `AKSIYOM_Urun_Tanitimi` sunumundaki doğrulanmış içerikten alınmıştır.
- Dozaj paneli görseli bir tasarımdır; değerleri **örnek veridir** (sayfada belirtilir).
- %25–35 su vb. rakamlar literatüre dayalı **hedeflerdir**, ölçülmüş sonuç değildir.
- Doğrulanmamış donanım/performans iddiası eklemeyin.

## Dosyalar

- `index.html` — içerik
- `style.css` — tasarım (AKSİYOM renkleri, Montserrat + Inter)
- `script.js` — mobil menü
- `assets/` — WebP görseller, logo, favicon
