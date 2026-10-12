# Emisyon İmisyon Ölçüm Standartları — Saha Rehberi 1.0.0

Offline Flutter Android rehberi. Ana emisyon hesaplama programından bağımsızdır.

## Bu sürüm

- 31 ayrı rehber; tekrar eden birleşik kayıtlar tek ölçüm konusuna yönlendirilir.
- Ölçümü tanı → Hazırlan → Treni kur → Ölçümü yap → Numuneyi toparla → Kontrol et.
- Numaralı adımlar, işlem gerekçeleri ve açık metot/kontrol etiketleri.
- 31 büyük, Türkçe etiketli düzenek veya işlem şeması; dokunarak tam ekran yakınlaştırma.
- EPA 26A, 29, 23, 13A, 323, 8, 11 ve amonyak yöntemlerinde farklı trenler.
- Yanma gazlarında T90 tanımı, örnek hesabı, sistem/sensör cevabı ayrımı ve uygulama sırası.
- Türkçe karakterlere dayanıklı arama, emisyon/imisyon filtreleri, favoriler ve son açılanlar.
- Cihazda saklanan kişisel saha kontrol listeleri; her yeni ölçümde sıfırlanır.
- Açık/koyu tema ve yazı büyütme.
- Mevcut 13 eğitim ses kaydı ve önceki konu görselleri korunur. Sesler yeni metnin yeniden seslendirmesi değildir.
- Tek ses oynatıcısı, hız seçimi, konum kaydı ve Android bildirim/arka plan çalma desteği.
- Baca ve ortam havası cihazını temsil eden yeni uygulama simgesi.

## İçerik kaynakları ve sınırlar

`assets/field_guides.json` kullanıcıya gösterilen yeni düzenlenmiş içeriği içerir.
Eski JSON ve eğitim notları arşiv olarak korunur; eski metinler yeni rehber altında tekrar yüklenmez.

Açık resmi EPA, CARB ve SCAQMD metinleri mevcut oldukları kapsamda kullanılır. Tam TS/EN/ISO metnine veya CARB 425 tam PDF'sine erişilemeyen konularda prensip şeması gösterilir; doğrulanmamış hacim, sıcaklık ve kabul sınırları kesin şart gibi yazılmaz. Bu kayıtlar uygulamanın kaynak bölümünde açıkça işaretlenir. Rehber, tam standardın ve onaylı laboratuvar prosedürünün yerine geçmez.

EPA standart hacmi otomatik olarak 0 °C normal hacme dönüştürülmez. Referans sıcaklık/basınç ve kuru/yaş baz açıkça değerlendirilir.

## Derleme

GitHub Actions → Build Android APK. Başarılı çalışmanın `emisyon-saha-rehberi-v1.0.0` artifact'i ZIP içinde APK içerir.
Flutter 3.47.7 ve Java 17 kullanılır. Android projesi temiz oluşturulur; `scripts/configure_android.py` simgeyi ve arka plan ses servisini uygular.

Üretim imzalama anahtarı depoda saklanmaz. Mevcut derleme Flutter'ın release için varsayılan geliştirme imzasını kullanır; önceki APK'nin imzasından farklı olabilir. Gerçek cihazda eski sürüm üzerine güncelleme kabul edilmeyebilir. Dağıtım için sabit üretim anahtarının GitHub Secrets üzerinden ayrıca tanımlanması gerekir.

## Kontroller

- `python3 scripts/validate_assets.py`
- `python3 scripts/validate_field_guides.py`
- `flutter analyze lib --no-fatal-infos --no-fatal-warnings`
- `flutter test`

Widget testleri arama, favori, kontrol listesi, 31 rehberin dar ekran/büyük yazı yerleşimi ve ses bağlantılarını kontrol eder. Test sırasında UI önizlemeleri artifact olarak alınır. Ses çıkışı ve Android kilit ekranı gerçek cihazda ayrıca denenmelidir.

İçerik kaynağı: `scripts/build_field_guides.py`. Çizim kaynağı: `scripts/draw_assets.py` (Pillow ve DejaVu Sans). Bu iki script değişirse JSON/PNG çıktıları yeniden üretilip commit edilir.
