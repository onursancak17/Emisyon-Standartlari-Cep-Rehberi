# Telefondan APK Alma Talimatı

Bu talimat Android telefondan GitHub üzerinden APK dosyasını indirmek içindir.

## 1. Actions sekmesini aç

1. GitHub uygulamasında veya telefondaki tarayıcıda repoyu aç.
2. Üst menüden **Actions** sekmesine gir.
3. **Build Android APK** isimli workflow'u seç.

## 2. Otomatik build'i bekle

Repoya her dosya eklendiğinde workflow otomatik çalışır. Ayrıca elle çalıştırmak için:

1. **Build Android APK** sayfasında **Run workflow** düğmesine bas.
2. Branch olarak `main` seç.
3. Çalıştır.

## 3. APK artifact dosyasını indir

1. Yeşil tikli başarılı çalışmayı aç.
2. Sayfanın altına in.
3. **Artifacts** bölümünde `emisyon-standartlari-cep-rehberi-apk` dosyasını indir.
4. İnen dosya ZIP olur.
5. ZIP içinden `app-release.apk` dosyasını çıkar.

## 4. Android telefona kur

1. `app-release.apk` dosyasına dokun.
2. Telefon bilinmeyen kaynak uyarısı verirse izin ver.
3. Uygulamayı kur.

## Notlar

- Uygulama offline çalışır.
- İçerik `assets/standards.json` dosyasından gelir.
- APK üretimi GitHub Actions ile yapılır; bilgisayara gerek yoktur.
- İlk build birkaç dakika sürebilir.

## Sorun olursa

Actions ekranında kırmızı çarpı görünürse, hata kaydını açıp son 30-40 satırı ChatGPT'ye gönder. Hata Flutter, Android veya YAML kaynaklıysa düzeltilebilir.
