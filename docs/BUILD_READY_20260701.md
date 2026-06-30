# APK build hazır notu

Bu not, **Emisyon İmisyon Ölçüm Standartları** APK build aşamasına geçildiğini kayıt altına almak için eklendi.

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
- Görsel manifest kayıt sayısı
- `assets/visuals` içindeki JPG sayısı
- Manifestte olmayan JPG sayısı
- Standart detayına bağlanmamış JPG sayısı
- Eksik görsel asset var mı

## Offline görsel davranışı

`assets/visuals/` içindeki JPG dosyaları APK içine gömülür. Manifestte yazmayan JPG dosyaları uygulamada otomatik olarak:

```text
Kontrol bekliyor / Ham görsel
```

etiketiyle Görsel Arşivi ekranında görünür.

## Manuel build alma

GitHub üzerinden:

```text
Actions → Build Android APK → Run workflow → main → Run workflow
```

Başarılı build sonrası artifact indirilir ve APK telefona kurulur.
