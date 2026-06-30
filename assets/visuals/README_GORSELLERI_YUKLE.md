# Offline APK görselleri

Bu klasör, offline APK içine gömülecek görseller içindir.

## Doğru yol

Görseller şu klasöre doğrudan yüklenmelidir:

```text
assets/visuals/
```

Örnek dosya adları:

```text
assets/visuals/1000064893.jpg
assets/visuals/1000064901.jpg
assets/visuals/1000064801.jpg
```

## Yanlış yol örnekleri

```text
standards_app/assets/field_visuals_raw/...
field_visuals_ALL_COMBINED_final_20260630/assets/visuals/...
assets/visuals/assets/visuals/...
```

## Not

`assets/visual_notes_extra.json` içinde bazı görseller `imageAsset` yolu ile bu klasöre bağlanmıştır. Dosya yoksa APK çökmez; görsel kutusunda uyarı gösterir. Dosya yüklendiğinde bir sonraki APK build içinde offline olarak gömülür.
