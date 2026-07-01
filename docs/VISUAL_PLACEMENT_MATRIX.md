# Görsel Yerleşim Matrisi

Bu doküman, APK içindeki görsellerin profesyonel yerleşim kuralını kayıt altına alır.

## Ana kural

Görseller artık rastgele veya çoklu tekrar mantığıyla dağıtılmaz. Her görsel:

1. Gerçekten ait olduğu standarda bağlanır.
2. Standardın doğru konu başlığına yerleştirilir.
3. Metin ağırlıklı ise gerektiğinde görsel yerine metin bilgiye dönüştürülür.
4. Tekrar eden görseller sadece en temsil edici olanlarıyla tutulur.

## Placement alanları

`assets/visual_notes_extra.json` içinde her görsel için `placement` alanı kullanılır.

| placement | APK içinde gösterileceği bölüm |
|---|---|
| `purpose` | Amaç / kullanım alanı |
| `quality` | Kalite kontrol / ISDL / raporlanabilirlik |
| `flowRate` | Debi / hacim notu |
| `equipment` | Cihaz / ekipman |
| `fieldSteps` | Saha adımları |
| `criticalControls` | Kritik teknik kontroller |
| `acceptance` | Kabul / ret kriterleri |
| `reporting` | Raporlama notları |

## Şu an uygulanan temiz yerleşim

### ISDL / MID

ISDL, MID, hedef hacim, ELV/10, tayin limiti ve raporlanabilirlik görselleri artık toz, hız, HCl veya metal standartlarının içine tekrar tekrar dağıtılmaz.

Bağlandığı ayrı bölüm:

```text
ISDL / MID
```

Kullanılan görseller:

```text
1000064732.jpg
1000064734.jpg
1000064735.jpg
1000064736.jpg
1000064737.jpg
1000064738.jpg
1000064739.jpg
1000064740.jpg
1000064741.jpg
```

### Toz / izokinetik örnekleme

Bağlandığı standartlar:

```text
EPA Method 5
TS EN 13284-1
TS ISO 9096
EPA Method 17
```

Kullanılan görseller:

```text
1000064744.jpg  → amaç / metot seçimi
1000064748.jpg  → izokinetik prensip / saha adımları
1000064749.jpg  → izokinetik hata / kritik kontrol
1000064750.jpg  → EPA17 in-stack filtre
1000064751.jpg  → out-stack filtre
1000064753.jpg  → nozul seçimi
1000064761.jpg  → kaçak testi / kabul kontrolü
```

### PAH

Bağlandığı standart:

```text
TS ISO 11338 / ilgili PAH saha uygulamaları
```

Kullanılan görseller:

```text
1000064766.jpg  → PAH örnekleme genel akışı
1000064767.jpg  → PAH adsorban ve numune hattı
1000064773.jpg  → PAH numune geri kazanımı
1000064775.jpg  → PAH blank ve taşıma
```

### PCDD/F Dioksin-Furan

Bağlandığı standart:

```text
TS EN 1948-1
```

Kullanılan görseller:

```text
1000064776.jpg  → PCDD/DF numune alma genel düzeni
1000064778.jpg  → XAD-2 koruma ve ekipman
1000064782.jpg  → XAD-2 uyarısı / kritik kontrol
1000064785.jpg  → son kontrol / kabul kontrolü
```

### Hız / debi / Pitot

Bağlandığı standart:

```text
EPA Method 2 / TS EN ISO 16911 / TS ISO 10780
```

Kullanılan görseller:

```text
1000064786.jpg  → hız/debi genel şema
1000064789.jpg  → S tipi Pitot
1000064792.jpg  → pitot hız/debi kontrolü
1000064798.jpg  → karekök ortalama / raporlama
```

### EPA Method 4 / Nem tayini

Kullanılan görseller:

```text
1000064800.jpg  → nem tayini genel akışı
1000064801.jpg  → impinger dizilimi
1000064803.jpg  → silika jel kontrolü
```

### Ölçüm düzlemi / traverse

Bağlandığı standart:

```text
TS EN 15259 / EPA Method 1
```

Kullanılan görseller:

```text
1000064807.jpg  → H1/H2 ölçüm düzlemi
1000064811.jpg  → nokta mesafesi / traverse tablosu
1000064815.jpg  → uygunsuz ölçüm yeri örneği
```

### VOC / TOC

Bağlandığı standart:

```text
TS EN 12619 / TSE CEN/TS 13649
```

Kullanılan görseller:

```text
1000064824.jpg  → VOC yöntem seçim ağacı
1000064835.jpg  → VOC numune alma treni
1000064842.jpg  → adsorban/çözücü kontrolü
```

### Ağır metaller

Bağlandığı standartlar:

```text
EPA Method 29
TS EN 14385
```

Kullanılan görseller:

```text
1000064854.jpg  → metal örnekleme treni
1000064859.jpg  → EPA29 geri kazanım
1000064861.jpg  → blank kontrolü
```

### HCl / Halojen

Bağlandığı standartlar:

```text
TS EN 1911
EPA Method 26A
```

Kullanılan görseller:

```text
1000064871.jpg  → HCl / halojen örnekleme hattı
1000064875.jpg  → EN1911 HCl geri kazanım
1000064868.jpg  → EPA26A halojen tren şeması
```

### İmisyon

Bağlandığı standartlar:

```text
TS EN 12341 / EPA 40 CFR 50-53
TS 2341 / TS 2342 / SKHKKY Ek-2
```

Kullanılan görseller:

```text
1000064883.jpg  → PM10 saha şartları
1000064882.jpg  → çöken toz yerleşimi
```

### Yanma gazı

Bağlandığı standart:

```text
TS ISO 12039 / TS EN 14789 / TS EN 14792 / TS EN 15058
```

Kullanılan görseller:

```text
1000064887.jpg  → referans O2 düzeltmesi
1000064888.jpg  → yanma gazı ölçümleri neden yapılır
```

### Özel parametreler

Bağlandığı standartlar:

```text
CARB Method 426
CARB Method 425
EPA CTM 027
SCAQMD Method 207.1
```

Kullanılan görseller:

```text
1000064893.jpg  → siyanür örnekleme treni
1000064894.jpg  → siyanür NaOH absorban hattı
1000064901.jpg  → Cr(VI) numune alma treni
1000064905.jpg  → Cr(VI) geri kazanım
1000064908.jpg  → CTM-027 amonyak tren şeması
1000064909.jpg  → Greenburg-Smith amonyak yaklaşımı
1000064910.jpg  → mini bubbler yaklaşımı
```

## Sonraki temizlik kuralı

Kalan ham görseller tek tek incelendiğinde:

- birebir tekrar ise APK detaylarına eklenmez,
- sadece yazıysa metin bilgiye dönüştürülür,
- şema/düzenek ise ilgili standarda ve doğru placement alanına eklenir,
- kalite/hesap görseliyse standart içine değil ISDL/MID bölümüne alınır.
