# Emisyon / İmisyon Standartları Cep Rehberi

Bu proje, emisyon ve imisyon saha ölçüm personeli için hazırlanmış offline Android cep rehberi uygulamasıdır.

Ana emisyon hesaplama programından tamamen bağımsızdır. Bu repo sadece mobil standartlar rehberi içindir.

## İlk sürümde olanlar

- Offline çalışan Flutter Android uygulaması
- Standart arama ekranı
- Kategori filtreleme
- Emisyon / imisyon ayrımı
- Sahacı odaklı rehber alanları:
  - Amaç
  - Ölçüm süresi
  - Debi / hacim notu
  - Cihaz / ekipman
  - Çözelti / absorban
  - Saha adımları
  - Kritik teknik kontroller
  - Kabul / ret kriterleri
  - Raporlama notları
  - Sık yapılan saha hataları

## İlk veri tabanındaki başlıklar

- TS EN 13284-1 Partikül Madde
- TS ISO 9096 Yüksek Konsantrasyon Partikül Madde
- TS EN 15259 / EPA Method 1 Ölçüm Düzlemi ve Traverse
- EPA Method 4 Nem Tayini
- TS EN 1911 / EPA 26A HCl
- EPA Method 29 / TS EN 14385 Ağır Metal
- TS ISO 12039 / TS EN 14789 / TS EN 14792 / TS EN 15058 Yanma Gazları
- TS 12341 / EPA 40 CFR 50-53 PM10 İmisyon
- TS 2341 / TS 2342 Çöken Toz

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

Bu uygulama resmi standardın yerine geçmez. Sahada hızlı kontrol ve hatırlatma rehberi olarak kullanılır. Resmi raporlama ve denetim işlerinde yürürlükteki standart, mevzuat ve laboratuvar talimatı esas alınmalıdır.
