# APK görsel yükleme kontrol listesi

Bu liste, `assets/visual_notes_extra.json` içinde tanımlanmış görsellerin APK içine gömülmesi için gereken dosyaları gösterir.

## Hedef klasör

```text
assets/visuals/
```

## Yüklenmesi gereken görseller

Aşağıdaki dosyalar doğrudan `assets/visuals/` klasörüne konmalıdır:

```text
1000064767.jpg
1000064778.jpg
1000064792.jpg
1000064801.jpg
1000064854.jpg
1000064871.jpg
1000064887.jpg
1000064893.jpg
1000064894.jpg
1000064901.jpg
1000064908.jpg
1000064909.jpg
```

## Doğru yol örneği

```text
assets/visuals/1000064893.jpg
```

## Yanlış yol örneği

```text
assets/visuals/assets/visuals/1000064893.jpg
apk_offline_visuals_pack_20260701/assets/visuals/1000064893.jpg
```

## Kontrol

GitHub Actions içinde `scripts/validate_assets.py` bu dosyaları kontrol eder. Görseller eksikse uyarı verir. Görseller yüklendikten sonra uyarı sıfırlanır ve APK içine offline olarak gömülür.
