# Emisyon Saha Talimatları 2.0

Android için çevrimdışı ölçüm talimatları ve ayrı emisyon–imisyon eğitim bölümü.

- Ana ekran: arama, Ortak Saha Talimatları, Emisyon / İmisyon listeleri.
- 22 ölçüm başlığı; TS/EPA hız ve PM₁₀ ortak anlatımları kendi başlıkları altında birleştirilir; ortak hazırlık ayrı bölümde tutulur.
- 11 eğitim konusu, 246 alt başlık. Aynı içerikteki iki formaldehit eğitim PDF’i birleştirilmiştir.
- Gerçekçi cam ekipman görselleri; şişe sırası, mL, gram ve derişimler JSON’dan native metin olarak gösterilir. Yakınlaştırma ve yatay kaydırma desteklenir.
- PAH/dioksin XAD-2 kartuşu dik, alt giriş/üst çıkış şeklinde gösterilir. Pompa/sayaç görseli yoktur.
- Türkçe seslendirme ekrandaki metinden üretilir. Android TTS’de Türkçe ses gerekir; yüklü yerel sesle internet gerekmez. Başlat/duraklat/devam/önceki-sonraki madde ve bölüm bazında dinleme vardır.
- Kaynak belge, revizyon ve sayfa bilgisi uygulama arayüzünde gösterilmez.

## Derleme
GitHub Actions Java 17 ve Flutter 3.47.7 ile Android projesini oluşturur; veri doğrulaması, Flutter analyze ve widget testlerinden sonra release APK hazırlar. Yeni APK eski büyük ses arşivini paketlemez. Arşiv repo içinde korunur.

## İçerik
`assets/manuals.json`, `assets/training.json` uygulamada kullanılan derlenmiş içeriktir. `scripts/build_manuals.py` gözden geçirilmiş saha maddelerini üretir. Eğitim derleyicisi metni çıkarılmış PDF klasörünü `--source-dir` ile alır. Kaynak eşleşmeleri yalnız geliştirici inceleme dosyasında bulunur.

Dioksin eğitim kaynağı XAD-2 için evrensel reçine kütlesi vermediğinden, PAH’taki yaklaşık 30 g değeri dioksine kopyalanmamıştır. Kaynakta sabit miktarı tanımlanmamış nem tutucular ön tartım notuyla gösterilir. Dietilen glikollü alternatif eğitimde açıklanır; miktarı doğrulanmamış bir işletme reçetesi üretilmez.
