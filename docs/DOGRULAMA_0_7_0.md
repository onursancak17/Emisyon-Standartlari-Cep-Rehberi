# 0.7.0 kaynak karşılaştırması ve kabul kaydı

26 Kasım 2026. Bu paket kaynak denetiminin devam eden geliştirme sürümüdür.

## Yeni kaynaklar ve içerik

Kullanıcının izin verdiği İndirilenler klasöründeki üç taranmış dosyanın 191 sayfası OCR ile okunabilir hale getirildi. Kapaklar, kritik çözelti tarifleri ve kabul tabloları sayfa görüntüleriyle de karşılaştırıldı. Lisanslı tam metinler bu açık depoya yüklenmez; kaynak kimliği, sürüm, SHA-256 ve sayfa/madde izleri tutulur.

| Kaynak | Gerçek nüsha | Sayfa | Yeni rehber kapsamı |
|---|---|---:|---|
| L01 | TS EN 1911:2010; TSE Ocak 2011 | 48 | HCl: izokinetik olmayan, tam akış ve yan kol; su, verim, blank, kaçak ve fraksiyonlar |
| L02 | BS EN 14385:2024; EN ana metni | 77 | 11 metal: tam akış ve yan kol; çözelti, üç absorber, verim, geri kazanım, taşıma ve bekletme |
| L03 | TS EN 13284-1, Ocak 2018; EN 13284-1:2017 | 66 | Baca içi/dışı filtre; nokta/süre/hacim, izokinetik, blank, tartım ve ön yıkama |

Dosya adında TS yazması L02'nin BS kapağını değiştirmez. EN 1911:2010'un EN 13284-1:2001 tarihli atfı korunur; 2017 süreleri ona otomatik aktarılmaz. EN 14385:2024 ise 2017 baskısına atıf yapar.

- 29 yöntem/varyant kartı, 23 ayrı çizim, 23 ortak saha konusu.
- 150 açıklamalı soru; 25 imisyon sorusu; mevcut 37 katalog başlığının hepsinde ilk soru kapsamı. Her standardın her maddesinin soru bankasında olduğu anlamına gelmez.
- EN 14385 çözeltisinin kütle/kütle temeli EPA 29 hacim/hacim tarifinden ayrılır. Seçili varyant üç dolu absorber ve ön boş kondensat kabı olmadan çizilmiştir; ön kap alternatifi metinde açıklanır.
- EN 14385 sıvıları: sahada/taşıma sırasında <25 °C; laboratuvarda <6 °C; numune alımından itibaren en geç dört haftada analiz. EN 1911 ve EN 13284-1'de bulunmayan sayısal bekletme koşulları uydurulmaz; laboratuvar kabul planı gerektirir.
- Toz ön yıkaması filtre kütlesiyle, metal ön yıkaması gaz hacmiyle paylaştırılır. Son absorber ayrı analiz ve yöntemlere özgü blank kararları ayrı anlatılır.
- EN ölçüm yeri açı/hız koşulları EPA null/alternatif yer prosedüründen ayrılır.
- Eski üç katalog kartındaki çelişkili genel rakamlar yeni kaynak karşılaştırmasına bağlandı. HCl ve metal yan kolları da tam ekran büyütülebilen çevrimdışı çizimlere eklendi.

## Kontrollerin kapsamı

Python testleri kaynak/sayfa, tren topolojisi, fraksiyon ve soru verisini; Flutter testleri yöntem seçimi, çizim, dar ekran/büyük yazı ve hesapları denetler. Android kabul akışı release APK'yı Wi-Fi/veri kapalı emülatöre kurup açar; ardından etkileşim sürümüyle parametre, çizim/yakınlaştırma ve açıklamalı imisyon testi akışını çalıştırır. Flutter'ın resmi integration driver giriş noktası kullanılır. Başarı durumu bu commitin Actions sonucudur; bu belge henüz koşmamış bir testi başarılı saymaz.

Fiziksel telefonda kabul yapılmamıştır. Mevcut sesler nedeniyle APK yaklaşık 500 MB'dır. Geliştirme imzası kalıcı üretim güncelleme anahtarı değildir.

## Açık teknik işler

EN 1911'in tarihli 2001 toz atfının tam karşılaştırması; EN 14385 §8.1'deki yüksek baca sıcaklığı/180 °C ifadesinin yazılı uygulama planı; ulusal TS nüsha/SOP eşleştirmesi; SCAQMD 207.1 tam prosedürü; ek PAH/dioksin varyantları; ISO 12141:2024 tam metni ve eski eğitim metni/görsel/seslerin ayrıntılı kaynak denetimi sürüyor. Güncel kartlarda yönteme özgü açık noktalar görünürdür.

Bu sürüm bütün standart külliyatının veya bütün saha talimatlarının nihai onayı değildir. 191 sayfanın OCR ile elde edilmesi her cümlenin bağımsız olarak doğrulandığı anlamına gelmez.
