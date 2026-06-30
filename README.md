# Emisyon / İmisyon Standartları Cep Rehberi

Bu proje, emisyon ve imisyon saha ölçüm personeli için hazırlanmış **tam Türkçe**, offline Android cep rehberi uygulamasıdır.

Ana emisyon hesaplama programından tamamen bağımsızdır. Bu repo sadece mobil standartlar rehberi içindir.

## Proje yönü

Bu uygulama kısa standart özeti olmayacak. Amaç, sahadaki ölçüm personelinin telefondan açıp adım adım kullanabileceği ayrıntılı bir Türkçe saha rehberi oluşturmaktır.

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
- Raporlama notları
- Sık yapılan saha hataları

## Birim dili

Uygulama Türkiye saha kullanımına göre hazırlanır. Amerikan/İngiliz kaynaklı birimler ekranda Türk saha birimlerine çevrilmiş olarak gösterilir.

Örnek dönüşümler:

- `scm` yerine `Nm³`
- `21 scf` yerine yaklaşık `0,60 Nm³`
- `0,75 cfm` yerine yaklaşık `21 L/dk` veya `0,021 m³/dk`
- `0,020 cfm` yerine yaklaşık `0,57 L/dk` veya `0,00057 m³/dk`
- `m3` yerine `m³`

## İlk sürümde olanlar

- Offline çalışan Flutter Android uygulaması
- Standart arama ekranı
- Kategori filtreleme
- Emisyon / imisyon ayrımı
- Ayrıntılı standart detay sayfası
- Tam Türkçe saha rehberi içerikleri
- Türkiye saha kullanımına uygun birim gösterimi

## Genişletilmiş ilk veri tabanındaki başlıklar

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

## APK nasıl alınır?

1. GitHub'da bu repoyu aç.
2. Üst menüden **Actions** sekmesine gir.
3. **Build Android APK** workflow'unu seç.
4. En son başarılı çalışmayı aç.
5. Sayfanın altındaki **Artifacts** bölümünden `emisyon-standartlari-cep-rehberi-apk` dosyasını indir.
6. ZIP içinden `app-release.apk` dosyasını çıkarıp Android telefona kur.

Detaylı telefon talimatı için:

`docs/TELEFONDAN_APK_ALMA.md`

## İçerik nasıl genişletilir?

Standart içerikleri `assets/standards.json` dosyasında tutulur. Yeni standart eklemek için aynı JSON yapısında yeni kayıt eklemek yeterlidir.

## Önemli not

Bu uygulama sahada hızlı kontrol ve eğitim amaçlı Türkçe rehberdir. Resmi raporlama ve denetim işlerinde yürürlükteki standart, mevzuat ve laboratuvar talimatı esas alınmalıdır.
