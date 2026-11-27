# Emisyon İmisyon Ölçüm Standartları

## 0.8.1 — kaynak karşılaştırmaları ve yöntem ayrımları

45 metot/varyant kartı, 37 çizim ve 200 açıklamalı soru (31 imisyon). Yeni kartlar: aktif karbon VOC, TD VOC, dinamik seyreltme, EN ISO 16911-1 Pitot, EPA2, EPA5, EPA17, EN12619, EPA25A, ISO9096 iç/dış filtre, ISO10780 ve ISO12039 dışarı çekişli AMS. Dinamik seyreltme çiziminde temiz gaz girişi, baca gazı girişi, analiz kolu ve fazla karışım çıkışı ayrı gösterilir.

VOC debi/hacim/sıcaklık ve tüp saklama, Pitot/girdap/yoğunluk ve kuru normal debi, EPA kimyasal kap/blank/geri kazanım, PM10/PM2,5 tartım ve kalite koşulları kaynak maddeleriyle karşılaştırıldı. Kaynak türleri (standart, kurum talimatı, eğitim sunumu, cihaz kılavuzu) uygulamada ayrılır. 0.7.2’de cıvasız metal kartına cıva geri kazanımının karışmasını engelleyen düzeltme korunur.

**Bütün standartların nihai teknik doğrulaması tamamlanmadı.** Uygulamadaki “Kaynaklar ve sürümler → 37 başlığın teknik doğrulama durumu” ekranı ve [teknik doğrulama matrisi](docs/TEKNIK_DOGRULAMA_MATRISI.md) her başlıktaki açık işi gösterir. Katalog kapsamı ve test sayısı nihai yöntem onayı değildir. [0.8.0](docs/DOGRULAMA_0_8_0.md) ve [0.8.1 değişiklikleri](docs/DOGRULAMA_0_8_1.md).

## Önceki 0.7.1 kapsamı

Ana ekrandaki **Parametre seç · Numune alma ve impinger rehberi** düğmesi yeni bölümü açar. 32 metot/varyant kartının 27’sinde ayrı tren çizimi bulunur. Metot değişince filtre yeri, şişeler ve miktarlar seçime göre değişir. Ana/yan akış kolları ayrı çizilir. Şema tam ekranda yakınlaştırılabilir ve çevrimdışı çalışır. Emisyon / imisyon filtreleri ve PM10, PM2,5, çöken toz, pasif örnekleme kartları vardır.

**Bilgini sına** bölümünde 160 açıklamalı soru (25 imisyon sorusu) vardır. Mevcut katalogdaki 37 başlığın her birine en az bir soru bağlanmıştır. Karışık / emisyon / imisyon / ortak kapsam; konu / standart-metot / parametre seçimi; 10, 20, 40, 60, 100 veya tüm sorular; soru ve seçenek karıştırma; ileri-geri gezinme; boş bırakma; test sonunda doğru-yanlış-boş sayısı, konu dağılımı, açıklama ve kaynak izi sunulur. Bu ilk bankadır; her standardın bütün ayrıntılarının sorulduğu iddia edilmez.

Girdap açısı ölçümü ve EPA Method 1 mutlak açı ortalaması; ölçüm yeri uygunsuzlukları; 23 ortak saha konusu; referans koşullarını koruyan birim dönüşümü eklendi. İncelemesi tamamlanmamış yöntemler açıkça **hazırlanıyor / talimat kaynaklı** görünür. Tam metot onayı veya bütün standartların güncel sürümlerinin eksiksiz işlendiği iddia edilmez.

Yeni kaynak karşılaştırmaları: [0.7.0 — üç EN nüshası](docs/DOGRULAMA_0_7_0.md), [0.7.1 — amonyak ve dioksin](docs/DOGRULAMA_0_7_1.md).

Kapsam, tamamlananlar ve kalan işler: [Geliştirme planı](docs/GELISTIRME_PLANI.md). Kaynak kimlikleri: [SOURCE_INDEX.json](docs/SOURCE_INDEX.json).

[Metoda göre ilk tren çizimlerini görüntüle](docs/impinger_ornekleri.png).

GitHub Actions: **Verify field guide** Python/Flutter kontrolleri; **Build Android APK** APK derlemesi. APK yalnızca başarılı derleme tamamlandıktan sonra Artifacts bölümünden indirilir.

Bu proje, emisyon ve imisyon saha ölçüm personeli için hazırlanmış **tam Türkçe**, offline Android cep rehberi uygulamasıdır.

Android telefonda görünecek APK uygulama adı:

```text
Emisyon İmisyon Ölçüm Standartları
```

Ana emisyon hesaplama programından tamamen bağımsızdır. Bu repo sadece mobil standartlar rehberi içindir.

## Proje yönü

Bu uygulama kısa standart özeti olmayacak. Amaç, sahadaki ölçüm personelinin telefondan açıp adım adım kullanabileceği ayrıntılı ve profesyonel bir Türkçe saha rehberi oluşturmaktır.

Uygulama arayüzü tüm emisyoncuların kullanacağı şekilde sade tutulur. Açıklamalı bilgi testleri ve çevrimdışı kaynak dizini ana ekrandan açılır.

Her standartta mümkün olduğunca şu bilgiler bulunur:

- Ölçüm amacı
- Kullanım alanı
- Ölçüm süresi
- Debi / hacim yaklaşımı
- Cihaz ve ekipman listesi
- Çözelti / absorban / impinger bilgileri
- Filtre, nozül, prob ve hat hazırlığı
- Saha adımları
- Kaçak testi
- Kritik teknik kontroller
- Kabul / ret kriterleri
- Numune geri alma ve saklama notları
- Ölçüm talimatı kontrol adımları
- Raporlama notları
- Sık yapılan saha hataları

## Kaynak işleme mantığı

Cep rehberi üç katmanla büyütülür:

1. Standart kaynakları: resmi metot ve standart mantığı
2. Eğitim dokümanları: sahacıya yönelik açıklamalar ve örnekler
3. Ölçüm talimatları: sahaya çıkmadan önce, ölçüm sırasında ve ölçüm sonunda yapılacak pratik kontrol adımları

## Birim dili

Uygulama Türkiye saha kullanımına göre hazırlanır. Amerikan/İngiliz kaynaklı birimler ekranda Türk saha birimlerine çevrilmiş olarak gösterilir.

Örnek dönüşümler:

- `scm` → kaynağın referans koşullarında standart m³; sıcaklık/basınç ve kuru/yaş baz korunur.
- `21 scf` → yaklaşık `0,595 standart m³`; tek başına 0 °C Nm³ dönüşümü değildir.
- `0,75 cfm` yerine yaklaşık `21 L/dk` veya `0,021 m³/dk`
- `0,020 cfm` yerine yaklaşık `0,57 L/dk` veya `0,00057 m³/dk`
- `m3` yerine `m³`

## Uygulamada olanlar

- Offline çalışan Flutter Android uygulaması
- Profesyonel standart arama ekranı
- Kategori filtreleme
- Emisyon / imisyon ayrımı
- Ayrıntılı standart detay sayfası
- Tam Türkçe saha rehberi içerikleri
- Eğitim PDF ayrıntıları
- Ölçüm talimatı kontrol notları
- Türkiye saha kullanımına uygun birim gösterimi
- Konuya göre yerleştirilmiş seçilmiş görseller
- Görsele dokununca tam ekran ve zoom desteği

## APK içine gömülen veri paketleri

Uygulama son kullanıcı APK'sında yalnızca gerekli veri paketlerini okur:

- `assets/field_guide.json`
- `assets/quiz_bank.json`
- `assets/source_index.json`
- `assets/diagrams/`
- `assets/standards.json`
- `assets/standards_extra.json`
- `assets/education_notes.json`
- `assets/education_notes_extra.json`
- `assets/visual_notes.json`
- `assets/visual_notes_extra.json`
- `assets/visuals/`

Görsel manifesti ve program sayfası dosyaları geliştirici/dokümantasyon amaçlı repoda kalabilir; son kullanıcı APK arayüzüne gereksiz menü olarak eklenmez.

## Genişletilmiş veri tabanındaki başlıklar

- TS EN 15259 / EPA Method 1 - Ölçüm düzlemi, port ve traverse
- EPA Method 2 / TS EN ISO 16911 / TS ISO 10780 - Hız ve debi
- EPA Method 5 - Partikül madde
- TS EN 13284-1 - Düşük derişimli partikül madde
- TS ISO 9096 - Yüksek konsantrasyon partikül madde
- EPA Method 17 - In-stack filtreli partikül madde
- EPA Method 4 - Nem tayini
- TS ISO 12039 / TS EN 14789 / TS EN 14792 / TS EN 15058 - Yanma gazları
- TS EN 1911 - HCl
- EPA Method 26A - HCl/HF ve halojenler
- EPA Method 29 - Ağır metal
- TS EN 14385 - Ağır metal
- TS EN 12619 / TSE CEN/TS 13649 - TOC/VOC
- TS ISO 11338 / PAH saha uygulamaları
- TS EN 1948-1 - PCDD/F dioksin-furan
- TS EN 12341 / EPA 40 CFR 50-53 - PM10/PM2.5 imisyon
- TS 2341 / TS 2342 / SKHKKY Ek-2 - Çöken toz
- ISDL / MID - hedef hacim ve raporlanabilirlik planı
- CARB Method 426 - Siyanür
- CARB Method 425 - Krom+6 / Cr(VI)
- EPA CTM 027 - Amonyak
- SCAQMD Method 207.1 - Amonyak

## Offline görsel mantığı

Görseller internetten çekilmez. APK içine gömülür.

Görsellerin doğru klasörü:

```text
assets/visuals/
```

Görsel bağlantıları:

```text
assets/visual_notes_extra.json
```

Her görsel için `placement` alanı kullanılır. Bu alan, görselin standardın hangi bölümünde gösterileceğini belirler:

```text
purpose
quality
flowRate
equipment
fieldSteps
criticalControls
acceptance
reporting
```

Detaylı yerleşim matrisi:

```text
docs/VISUAL_PLACEMENT_MATRIX.md
```

## Otomatik kontrol

GitHub Actions APK build öncesi şu script çalışır:

```text
scripts/validate_assets.py
```

Bu script JSON dosyalarını, standart anahtarlarını, görsel asset yollarını ve assets/visuals içindeki JPG sayısını kontrol eder. Eksik görseller şimdilik uyarıdır; build'i durdurmaz.

## APK nasıl alınır?

1. GitHub'da bu repoyu aç.
2. Üst menüden **Actions** sekmesine gir.
3. **Build Android APK** workflow'unu seç.
4. En son başarılı çalışmayı aç.
5. Sayfanın altındaki **Artifacts** bölümünden `emisyon-imisyon-olcum-standartlari-apk` dosyasını indir.
6. ZIP içinden `emisyon-imisyon-olcum-standartlari.apk` dosyasını çıkarıp Android telefona kur.

Detaylı telefon talimatı için:

`docs/TELEFONDAN_APK_ALMA.md`

## İçerik nasıl genişletilir?

Standart içerikleri `assets/standards.json` ve `assets/standards_extra.json` dosyalarında tutulur. Eğitim notları `assets/education_notes.json` ve `assets/education_notes_extra.json` dosyalarında tutulur. Görsel notları `assets/visual_notes.json` ve `assets/visual_notes_extra.json` dosyalarında tutulur.

## Önemli not

Bu uygulama sahada hızlı kontrol ve eğitim amaçlı Türkçe rehberdir. Resmi raporlama ve denetim işlerinde yürürlükteki standart, mevzuat ve laboratuvar talimatı esas alınmalıdır.

