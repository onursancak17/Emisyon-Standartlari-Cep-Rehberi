# 0.6.0 teknik değişiklik ve kontrol kaydı

25 Kasım 2026. Bu sürüm ayrıntılı kaynak denetiminin devam eden paketidir.

## Değişiklikler

- 23 yöntem/varyant kartı, 15 ayrı tren çizimi; 23 ortak saha konusu.
- CTM-027 baca içi filtre, üçüncü şişe boş/asitli seçenekleri ve ayrı numune fraksiyonları.
- EPA 323:2023 küçük şişe düzeni, 20 mL su, 0,4 L/dk üst sınırı ve buz üzerinde koruma.
- EPA 11 rafineri yakıt gazı kapsamı, beş midget şişe, CdSO4 absorbanı, en fazla 30 g silika ve tükenme kontrolü.
- CARB 425 filtre konumu, alkali ortam, ayrı geri kazanım ve bekletme koşulları.
- CARB 426 pH/koruyucu temeli ve saha/laboratuvar filtresi ayrımı. Kaynak içindeki kap numarası çelişkisi görünürdür.
- ISO 7935:2024 birincil metin ve Tablo 1 görüntüsüyle SO2 performans koşulları karşılaştırıldı. Genel gaz kartındaki evrenselleştirilmiş toleranslar kaldırıldı; CTM-022 NO/NO2/NOx olarak düzeltildi.
- Kaynak adı, sürüm, PDF sayfası ve madde izleri çevrimdışı. ISO 12141 arşivinin 2002, katalog baskısının 2024 olduğu belirtilir.
- 122 açıklamalı soru, 25 imisyon sorusu; 37 katalog başlığının tümünde ilk soru kapsamı bulunur. Bu, her standardın tüm maddelerinin sorulduğu anlamına gelmez.
- Dar ekran/büyük yazı testi; ana ekran yatay görünümde kaydırılabilir. Android kurulum ve internet kapalı etkileşim kabulü GitHub Actions akışına eklendi.

## Açık teknik işler

TS EN 1911, TS EN 14385:2024 ve EN 13284-1 kaynaklarının okunabilir tam metin karşılaştırması; SCAQMD 207.1 tam prosedürü; PAH/dioksin akış bölünmeli ve diğer yöntem varyantları; her metotta bütün fraksiyon, saklama ve kalite ayrıntıları; eski eğitim notları/görseller/seslerin tek tek içerik denetimi devam ediyor. ISO 12141:2024 tam metni ayrıca gerekli.

Bu açık maddeler kapanmadan tam ve nihai saha talimatı onayı verilemez. Yeni kartta belirtilmeyen bir koşul, kaynakta koşul yok demek değildir. Lisanslı standart PDF'leri kamuya açık depoya kopyalanmaz.

## Kontrolün anlamı

Python kaynak/sayfa, alan, şema ve soru testleri; Flutter birim/widget testleri; Android emülatöründe kurulum ve çevrimdışı etkileşim ayrı kontrollerdir. Başarı durumu ilgili commitin Actions kaydından değerlendirilir. Fiziksel telefonda kabul, emülatör testiyle aynı değildir. Bu akıştaki geliştirme imzası kalıcı üretim güncelleme anahtarı değildir.
