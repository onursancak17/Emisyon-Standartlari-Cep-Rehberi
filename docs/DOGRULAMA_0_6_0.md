# 0.6.0 teknik değişiklik ve kontrol kaydı

26 Kasım 2026. Bu sürüm ayrıntılı kaynak denetiminin devam eden paketidir.

## Değişiklikler

- 24 yöntem/varyant kartı, 16 ayrı tren çizimi; 23 ortak saha konusu.
- CTM-027 baca içi filtre, üçüncü şişe boş/asitli seçenekleri ve ayrı numune fraksiyonları.
- EPA 323:2023 küçük şişe düzeni, 20 mL su, 0,4 L/dk üst sınırı ve buz üzerinde koruma.
- EPA 11 rafineri yakıt gazı kapsamı, beş midget şişe, CdSO4 absorbanı, en fazla 30 g silika ve tükenme kontrolü.
- CARB 425 filtre konumu, alkali ortam, ayrı geri kazanım ve bekletme koşulları.
- CARB 426 pH/koruyucu temeli ve saha/laboratuvar filtresi ayrımı. Kaynak içindeki kap numarası çelişkisi görünürdür.
- ISO 7935:2024 birincil metin ve Tablo 1 görüntüsüyle SO2 performans koşulları karşılaştırıldı. Genel gaz kartındaki evrenselleştirilmiş toleranslar kaldırıldı; CTM-022 NO/NO2/NOx olarak düzeltildi.
- Kaynak adı, sürüm, PDF sayfası ve madde izleri çevrimdışı. ISO 12141 arşivinin 2002, katalog baskısının 2024 olduğu belirtilir.
- 125 açıklamalı soru, 25 imisyon sorusu; 37 katalog başlığının tümünde ilk soru kapsamı bulunur. Bu, her standardın tüm maddelerinin sorulduğu anlamına gelmez.
- EPA 26A tiyosülfat/blank planı; EPA 29 5A/5B/5C kapları ve blanklar; EPA 8 250/1000 mL son fraksiyon hacimleri; EPA 13A su yıkama sınırı.
- PAH ISO 11338-1 Metot B için ana/yan kolun ayrı gösterildiği, çevrimdışı büyütülebilen ek şema. Kaynak Şekil B.3'teki cihaz kapasiteleri evrensel çekiş debisi diye sunulmaz.
- EPA Method 1:30.05.2023 alternatif yer prosedürü: pitch/yaw, 40/42 nokta ve bileşke açı dağılımı ayrı anlatılır.
- NIST tabanlı ek birimler: inç, ft, psi, grain ve sıcaklık farkı. Gaz referans koşulları otomatik değiştirilmez.
- Dar ekran/büyük yazı testi; ana ekran yatay görünümde kaydırılabilir. Android kurulum ve internet kapalı etkileşim kabulü GitHub Actions akışına eklendi.

## Sonraki sürüm

Üç yerel EN PDF'si kullanıcının izniyle bulundu ve 0.7.0'da ilgili saha bölümleri karşılaştırıldı. Güncel açık işler ve kaynak durumu `DOGRULAMA_0_7_0.md` içindedir. Bu dosya 0.6.0 değişiklik tarihçesidir.

## Kontrolün anlamı

Python kaynak/sayfa, alan, şema ve soru testleri; Flutter birim/widget testleri; Android emülatöründe kurulum ve çevrimdışı etkileşim ayrı kontrollerdir. Başarı durumu ilgili commitin Actions kaydından değerlendirilir. Fiziksel telefonda kabul, emülatör testiyle aynı değildir. Bu akıştaki geliştirme imzası kalıcı üretim güncelleme anahtarı değildir.
