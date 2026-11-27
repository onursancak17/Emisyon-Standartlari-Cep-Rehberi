# 0.8.1 — ISO saha karşılaştırmaları

45 metot/varyant kartı, 37 çizim, 200 açıklamalı soru (31 imisyon).

ISO9096:2017 / TS2020 nüshasının kurulum, iki filtre konumu, grid, süre, tartım, overall blank, yıkama, ısıl davranış ve kabul bölümleri karşılaştırıldı. Ana metindeki ±%10 izokinetik bantla Tablo3’ün −%5/+%15 bandı farklıdır. Filtre verimi de ana metinde >%99,0, tabloda >%99,5 yazılıdır. Bu farklar görünür kaydedilir; uygulama tek bir otomatik kabul eşiği üretmez. Blankın bacada pompasız 15 dakika ve akışa ters yönde tutulması, örnek sonrası fırçalama yasağı ve seri yıkamasının filtre kütlesi oranıyla paylaştırılması ayrı yöntem koşullarıdır.

ISO10780:1994 / TS1999 L/S Pitot kartı; cihaz/geometri/kalibrasyon, açı, cidara mesafe, nokta, kaçak, hesap ve bakım bölümleriyle eklendi. Kesit değişimi ve düzlem seçimine ilişkin farklı yazımlar, ENISO16911 veya EPA2’ye karıştırılmadan korunur.

ISO12039:2019 / TS2020 dışarı çekişli soğuk-kuru AMS kartı eklendi. CO/CO₂ aralık üstüne göre bağıl ölçütleri ile O₂ hacim yüzdesi cinsinden mutlak yüzde puanı ölçütleri ayrıldı. Kalıcı AMS yıllık QA tablosu periyodik cihazın seri başlangıcı kontrolünün yerine geçirilmez. ISO10396 bağlantısı ve eksik EN referans metotları nihai karşılaştırma matrisinde açık kalır.

İmisyon seçimini sınayan Flutter testindeki eski sabit 25 soru beklentisi, bankadaki gerçek İmisyon sorusu sayısıyla karşılaştırılacak şekilde düzeltildi. Kapsam/filtreleme kontrolü korunur.

Yerel kaynak/sayfa, şema, yöntem ayrımı, matris ve test bankası kontrolleri: 29 Python testi geçti. Flutter ve çevrimdışı Android sonuçları bu commit’in GitHub Actions kayıtlarında doğrulanır. Bütün standartların nihai teknik onayı tamamlanmış değildir; [matris](TEKNIK_DOGRULAMA_MATRISI.md) kapsamı ve açık işleri gösterir.
