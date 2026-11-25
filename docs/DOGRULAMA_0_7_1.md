# 0.7.1 — amonyak ve dioksin varyantları

26 Kasım 2026. 0.7.0 EN kaynak karşılaştırmaları korunur.

- 32 yöntem/varyant kartı, 27 tren çizimi, 160 açıklamalı soru (25 imisyon); 37 katalog başlığının tamamında ilk soru kapsamı.
- SCAQMD 207.1:2006 resmi tam metninin saha/numune bölümlerine erişildi. Büyük Greenburg–Smith ve mini/flux odası trenleri ayrı kart ve çizimlerdir. İsteğe bağlı ön filtre mini trene taşınmaz.
- Büyük tren: iki adet 100 mL; mini tren: iki adet 15 mL 0,1 N H₂SO₄. Silika miktarı ve kaçak testleri de ayrıdır. Şekil 207.1-2'nin 0,1 M etiketi ile açık metnin 0,1 N tarifi arasındaki çelişki görünür tutulur.
- SCAQMD'de alımdan geri kazanıma yedi takvim günü ile geri kazanım sonrası dört hafta ayrı saatlerdir. Kaynaktaki 35–45 °F yaklaşık 1,67–7,22 °C'ye çevrilir. Eski katalogdaki yanlış “7 günde analiz” metni düzeltildi.
- EN 1948-1 Ek B.2 sıvı bubbler ve B.3 ana/yan akış örnekleri eklendi. Kondensat ve XAD sırası, çözücü/fraksiyonlar, kol oranı ve kartuş hızı ayrı açıklanır. B.4 kartına kurutma grubu ve kendi toluen geri kazanımı eklendi.
- Ek B bilgi amaçlı örneklerinin debi/kaçak/süreleri ana metnin genel normatif kabulü gibi sunulmaz. B.3 örneğinin filtre çapı/≥30 g XAD miktarı evrensel dioksin tarifi değildir.

26 Python testi yerelde geçti. Flutter, varlık kontrolü ve Android çevrimdışı kabulünün başarı durumu bu commitin Actions sonucundan izlenir. Her dört yan kol resmi çevrimdışı varlıktan açılıp büyütme testine girer.

0.7.0 Android koşusunda etkileşim testi ve driver sıfır çıkış koduyla geçti; sonraki görünüm adımı, driver test uygulamasını kaldırdığı için başarısız oldu. Bu sürüm görünüm kontrolünden önce asıl release APK'yı yeniden kurar ve işlem kimliğini doğrular.

Yeni SCAQMD kartları Chapter III/X'in tam kalibrasyon ve hacim düzeltme prosedürlerinin veya flux odası tasarım protokolünün yerine geçmez. Kaynak çelişkisi laboratuvar planıyla çözülmelidir. Diğer açık işler 0.7.0 kontrol kaydı ve yöntem kartlarında kalır; bütün kaynak külliyatının nihai onayı verilmemiştir.
