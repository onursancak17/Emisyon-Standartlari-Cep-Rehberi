# 0.8.0 — 27 Kasım 2026

Bu sürüm seçili saha maddelerinin karşılaştırmasını genişletir. Bütün PDF’lerin her maddesinin veya bütün standartların güncel sürümlerinin nihai onayı değildir. Kalanlar [matriste](TEKNIK_DOGRULAMA_MATRISI.md) ve uygulamada görünür.

## Kaynaklardan bulunan ve ayrılan koşullar

- L04: TS EN ISO 16911-1:2013 tam metni. D26 aynı standardın tam metni değil, eğitim sunumudur. Pitot, kaçak, tekrarlanabilirlik, yön, tıkanma ve hesap bölümleri karşılaştırıldı. Tablo 4 ve A.1 basınç belirsizliği yazımları birleştirilmedi. Yaklaşan ikinci baskı 60.00 aşamasındadır; yayımlanmış diye işlenmedi.
- L05: CEN/TS 13649:2014 tam metni. Aktif karbon ve termal desorpsiyon ayrı. Tablo 1’in `<40 °C`, `<%5` ve belirsizlik işaretleri görüntüden kontrol edildi. 7 gün/<4 °C hükmü mutlak analiz son tarihi olarak çevrilmedi. Dinamik seyreltmenin iki giriş ve iki çıkışı özgün çizildi.
- Kullanıcının yeni 12141 PDF’si D31 ile aynıdır: TS ISO 12141:2004, esas ISO 12141:2002. ISO 12141:2024 yerine kullanılamaz.
- EN14789/14792/15058 için resmî kapsam/katalog ve yetkili ön izlemeler bulundu. Tam metin bulunmadı. Bunların sayısal saha hükümlerinin tamamı doğrulanmış gösterilmedi.
- EPA4 güncel EMC bağlantısı ve referans koşulları, EPA5/17 filtre yeri ve kapsam, EPA13A filtre/kap, EPA29 reaktif saflığı/kap/blank düzeltmesi, EPA8 fraksiyon ve EPA11 iyot sonrası saklama yasağı karşılaştırıldı.
- EN12341:2023 tartım, saha blankı, debi/gerçek ortam hacmi, saklama/taşıma ve kalite kontrol bölümleri karşılaştırıldı. Kaynakta süre adımlarının farklı başlangıçları korunur; bireysel saha blankı numuneden çıkarılmaz.
- EN12619 ve EPA25A ısıtma, T90/T95, kalibrasyon ve drift eşikleri ayrı kartlarda tutuldu. Tekil VOC ile FID toplam organik yanıtı birleştirilmedi.
- ISO11338-1:2003 §6.3.3’teki -7 °C görüntüden yeniden kontrol edildi. ISO 2026 teyidi, 2003 baskısını yeni içerikli bir 2026 baskısına dönüştürmez.

## Teknik kontroller

Python kaynak/sayfa/topoloji/audit kontrolleri ve test bankası kontrolleri yerelde çalıştırılır. Flutter analiz, dar ekran/iki kat yazı, yöntem seçimi, şema yakınlaştırma ve test akışı GitHub Actions’ta doğrulanır. APK ayrıca Android35 emülatörde Wi-Fi/veri kapalı kurulum ve etkileşim kontrolünden geçmeden çıktı olarak yayımlanmaz.

Program testlerinin geçmesi teknik standart hükümlerinin tamamının onaylandığı anlamına gelmez. Fiziksel telefonda kurulum testi henüz yapılmadı.
