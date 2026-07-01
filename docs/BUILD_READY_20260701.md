# APK build hazır notu

Bu not, **Emisyon İmisyon Ölçüm Standartları** APK build aşamasına geçildiğini kayıt altına almak için eklendi.

## Güncel profesyonel sürüm

```text
0.3.4+7
```

Bu sürümde son kullanıcı arayüzü sadeleştirildi. APK içinde yalnızca profesyonel standart rehberi mantığı gösterilir; geliştirici/test amaçlı görsel arşivi, program sayfaları ve offline test menüleri son kullanıcı ekranından çıkarıldı.

## Uygulama adı

Android telefonda görünecek ad:

```text
Emisyon İmisyon Ölçüm Standartları
```

## APK artifact adı

GitHub Actions başarılı olduğunda indirilecek artifact adı:

```text
emisyon-imisyon-olcum-standartlari-apk
```

ZIP içindeki APK dosyası:

```text
emisyon-imisyon-olcum-standartlari.apk
```

## Build öncesi kontrol

Workflow sırasında şu kontrol çalışır:

```text
python3 scripts/validate_assets.py
```

Bu kontrol şunları raporlar:

- Standart sayısı
- Eğitim notu anahtar sayısı
- Standart detay görsel notu sayısı
- `assets/visuals` içindeki JPG sayısı
- Standart detayına bağlanmamış JPG sayısı
- Eksik görsel asset var mı

## Güncel görsel davranışı

APK artık ham görsel arşivi mantığını son kullanıcıya göstermez. Bunun yerine sadece `assets/visual_notes_extra.json` içinde seçilmiş ve doğru standarda bağlanmış görseller standart detaylarında görünür.

Görseller `placement` alanına göre ilgili başlığın altında gösterilir:

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

Görsele dokunulduğunda tam ekran açılır ve kullanıcı parmakla zoom yapabilir.

## Manuel build alma

GitHub üzerinden:

```text
Actions → Build Android APK → Run workflow → main → Run workflow
```

Başarılı build sonrası artifact indirilir ve APK telefona kurulur.
