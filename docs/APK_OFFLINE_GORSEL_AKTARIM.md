# Offline APK görsel aktarım rehberi

Bu repo, telefona kurulacak **tamamen offline Android APK** üretmek içindir. Streamlit/WebView mantığı kullanılmaz.

Telefonda görünecek uygulama adı:

```text
Emisyon İmisyon Ölçüm Standartları
```

## Doğru repo

```text
onursancak17/Emisyon-Standartlari-Cep-Rehberi
```

## Görseller nereye konacak?

Görseller APK içine gömülmek için şu klasöre yüklenir:

```text
assets/visuals/
```

Örnek:

```text
assets/visuals/1000064893.jpg
assets/visuals/1000064901.jpg
assets/visuals/1000064801.jpg
```

## Görseller nasıl bağlanıyor?

Görsel notları şu dosyada tanımlanır:

```text
assets/visual_notes_extra.json
```

Görsel arşivi / aktif-bilinçli arşiv-kontrol bekliyor sınıflandırması şu dosyada tutulur:

```text
assets/visual_manifest_extra.json
```

Örnek kayıt:

```json
{
  "standards": ["CARB Method 426"],
  "title": "Siyanür örnekleme treni",
  "caption": "NaOH alkali absorban hattı ve pH kontrolü.",
  "imageAsset": "assets/visuals/1000064893.jpg"
}
```

Bu yapı sayesinde görsel internetten çekilmez; APK build sırasında uygulamanın içine gömülür.

## Eksik görsel olursa ne olur?

Görsel dosyası henüz yüklenmediyse APK çökmez. Uygulama ilgili yerde:

```text
Görsel APK içinde bulunamadı. Dosya yolu: ...
```

uyarısı gösterir.

## Otomatik kontrol

GitHub Actions build sırasında şu script çalışır:

```text
scripts/validate_assets.py
```

Bu script:

- JSON dosyaları okunuyor mu?
- Ek standart dosyaları doğru mu?
- Görsel notlarında tanımlı `imageAsset` dosyaları var mı?
- Görsel manifest kayıtları doğru mu?
- `assets/visuals/` içindeki JPG sayısı kaç?
- Eğitim notu anahtarları standartlarda karşılık buluyor mu?
- Standart kodlarında çakışma var mı?

kontrollerini yapar.

Eksik görseller şu aşamada **uyarı** sayılır; build'i durdurmaz. Çünkü bazı görseller manuel olarak sonra yüklenebilir.

## APK nasıl alınır?

1. GitHub'da repo sayfasını aç.
2. **Actions** sekmesine gir.
3. **Build Android APK** workflow'unu aç.
4. En son başarılı run'ı seç.
5. **Artifacts** bölümünden `emisyon-imisyon-olcum-standartlari-apk` paketini indir.
6. ZIP içindeki `emisyon-imisyon-olcum-standartlari.apk` dosyasını telefona kur.

## Kritik not

Bu repo, ana emisyon hesaplama programı değildir. Bu repo sadece offline standartlar cep rehberi APK'sidir.
