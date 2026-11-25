# Emisyon / İmisyon Ölçüm Standartları — geliştirme kaydı

25 Kasım 2026 · Kullanıcı kapsamı bu dosyada korunur. Ana emisyon hesaplama programı ve onun APK deposu bu çalışmanın dışındadır.

## Kullanıcı isteği

Telefona kurulabilen, çevrimdışı ve Türkçe saha rehberi. Mevcut Flutter projesi üzerinden GitHub’da geliştirilir. Kullanıcı aynı sohbeti telefonundan sürdürerek yönlendirebilir. Sohbet dışında kesintisiz çalışan bir geliştirme ajanı kurulmuş değildir.

- Parametre → standart/metot → kaynak sürümü → düzenek varyantı seçimi.
- Klor/HCl ve Cl₂, flor/florür, metaller (cıva dahil/hariç), PAH, dioksin/furan, nem, siyanür ve diğer absorpsiyon/adsorpsiyon metotları.
- Her metoda kendi impinger sayısı/sırası, tip, çözelti, derişim ve dolum miktarı. Opsiyonel şişe açıkça gösterilir; kaynak numarası korunur.
- Prob, filtre, soğutucu, XAD-2 veya başka adsorban, kondensat kabı ve varsa ana/yan kol dahil doğru tren çizimi.
- Debi, debinin referansı, toplam hacim, DGM/baca/referans hacim ayrımı, sıcaklık, süre, noktalar, kaçak, izokinetik oran ve kabul/ret koşulları.
- Ölçüm öncesinden numune geri kazanımı, fraksiyonlar, kap/kapak, koruma, ışık, sıcaklık, bekletme süresi ve laboratuvara teslim zincirine kadar talimat.
- Türkiye’de kullanılan birimler; orijinal referans koşulları ve derişim tanımları korunur. scm/scf doğrudan 0 °C Nm³ olarak etiketlenmez.
- Ölçüm yeri uygunsuzluğu, girdap/akış açısı ölçümü, ters akış, travers, port erişimi, homojenlik, sapma, gerekli alternatif yöntem/onay, düzeltme/tekrar/ret.
- Personelin bilmesi gereken diğer konular: saha güvenliği, proses temsili, ekipman/kalibrasyon, T90, drift, girişimler, blanklar, kontaminasyon, VOC/TOC, imisyon PM, çöken toz, pasif tüpler, meteoroloji, belirsizlik ve rapor.
- Tasarım ana programa yakın, telefon kullanımına uygun; şemada tam ekran, kaydırma ve yakınlaştırma.

## 0.5.0 geliştirme paketi

17 metot/varyant kartı; 10 ayrı çizim. Aynı parametrede farklı metot ve varyantlar birbirine karıştırılmaz. EPA 13A ön/arka filtre; EPA 29 cıva dahil/hariç; EPA 26A isteğe bağlı kondensat şişesi örnekleridir. EPA 8 filtresi ilk iki şişenin arasındadır. PAH/dioksin için katı adsorbanlı, akış bölünmesiz bir varyant seçilmiştir; tüm varyantlar tamamlanmış değildir.

23 ortak saha konusu, EPA Method 1 §11.4 null tekniği, mutlak açı ortalaması ve sınır değerlendirmesi, gazın referans koşullarını değiştirmeyen birim dönüştürücü eklendi.

## Tamamlanmış sayılmayan işler

Bu paket tam bir standart külliyatının onaylandığı anlamına gelmez. 54 kaynak yolu / 53 benzersiz PDF’nin her cümlesi, formülü ve şekli bağımsız olarak doğrulanmış değildir. Ayrıntılı inceleme bitmeden “tüm saha bilgisi eksiksizdir” denmez.

1. Her parametrede arşiv sürümünü güncel resmi katalog/metin ve laboratuvarın geçerli SOP’si ile eşleştirmek.
2. TS EN 1911, TS EN 14385, CARB 425/426, CTM 027, SCAQMD 207.1, EPA 323 ve EPA 11 kartlarının birincil kaynak doğrulamasını tamamlamak.
3. Her sayısal alanı özel madde/sayfa ile eşleştirmek; boş alana varsayılan miktar, sıcaklık, süre veya debi koymamak.
4. Her metotta tam geri kazanım, bekletme süresi ve taşıma talimatını tamamlamak. PAH arşivinde görülen −7 °C ifadesi görüntüden kontrol edildi; güncel sürüm doğrulaması yapılmadan +4 °C diye değiştirilmez.
5. Akış bölünmeli PAH/dioksin düzenekleri, sıvı absorban seçenekleri ve diğer geçerli varyantlar için ayrı şemalar hazırlamak.
6. EPA alternatif yer prosedürünü 29.03.2023 revizyonu ile değerlendirmek; eski eğitimdeki sayı ve tabloları körlemesine aktarmamak. EN/ISO açı kriterlerini birincil metinden ayrı doğrulamak.
7. Ana katalogdaki eski serbest metinleri ve eğitim notlarını yeni kaynak denetiminden geçirmek; yeni çizimlerin varlığı eski metinlerin tamamının onaylandığını göstermez.
8. Android cihazda gerçek ekran, erişilebilirlik, büyük yazı, yatay/dikey görünüm ve çevrimdışı kullanım kabulü.

## Veri ve test düzeni

`assets/field_guide.json` çevrimdışı yeni rehberdir. `scripts/build_field_guide.py` aynı içeriği yeniden üretir. `docs/SOURCE_INDEX.json` kaynak kimliği, PDF sayfa sayısı ve Git blob kimliğini taşır; özel kaynak PDF’ler bu depoya kopyalanmaz.

`scripts/validate_field_guide.py` kaynak/sayfa, yöntem kimliği, zorunlu koşullar, aşamalar ve çizim durumunu kontrol eder. Python testleri kritik şema farklılıklarını; Flutter testleri yöntem seçimi, çizim değişimi, açı ve birim hesaplarını denetler. Bu testler bilimsel içerik onayının yerine geçmez.

`Verify field guide` akışı Python + Flutter kontrollerini çalıştırır. `Build Android APK` akışı mevcut çevrimdışı içerik ve ses paketini koruyarak APK üretir. Hazırlık/dogrulama durumu kullanıcı arayüzünde görünür kalır.
