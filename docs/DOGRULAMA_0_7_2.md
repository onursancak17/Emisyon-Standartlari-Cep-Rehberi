# 0.7.2 — yöntem varyantlarının talimatlarını ayırma

27 Kasım 2026. Teknik inceleme sırasında veri üreticisinde ortak liste kullanımı bulundu: EPA 29 cıva geri kazanım adımları cıvasız varyanta da ekleniyordu. EPA 13A iki filtre varyantında ve EPA 29'da bazı cümleler tekrarlanıyordu.

Profil üretiminde tren ve aşamalar bağımsız kopyalanır. Cıvasız metal kartından cıva kabı 5A/5B/5C talimatları çıkarıldı; cıva içeren kartta korunur. Tekrarlı aşama cümleleri veri doğrulamasında artık hatadır. Regresyon testi cıva fraksiyonlarının cıvasız karta geçmesini reddeder.

32 kart, 27 çizim, 160 soru korunur. 27 Python testi yerelde geçti. Bu sürüm teknik kaynak denetiminin tamamlandığı anlamına gelmez. Yeni birincil PDF'lerin incelenmesi ayrıca sürüyor; yazılım kabulü bu commitin Actions sonucundan izlenir.
