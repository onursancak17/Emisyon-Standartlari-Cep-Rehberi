"""Soruların kaynakla karşılaştırılmış özel ayrıntıları ve senaryo hesapları."""


def extend(add):
    t, e = 'İmpinger ve özel metotlar', 'Emisyon'
    cases = [
      (['EPA Method 11'], 'EPA 11’de 200–300 g silika jel kullanmak neden yanlış bir aktarım olur?', 'Bu yöntem kurutma tüpünde en fazla 30 g ister.',
       ['Bütün yöntemler 300 g ister.', 'Silika jel bu yöntemde daima yasaktır.', 'Gram ile mL tamamen aynıdır.'],
       'EPA 11’in küçük debili yakıt gazı düzeni büyük Greenburg–Smith treniyle aynı değildir. Fazla kurutucu hidrokarbon tutarak hacim ölçümünü etkileyebilir.', 'D04:3,6'),
      (['EPA Method 11'], 'EPA 11’de son CdSO₄ şişesi sararırsa ne yapılır?', 'Ölçüm geçersiz kabul edilir.',
       ['Son şişe numuneye katılmaz ve ölçüm geçerli olur.', 'Süre ikiyle çarpılır.', 'DGM değeri rastgele düşürülür.'],
       'Son yakalama kademesindeki sararma, kapasitenin tükenmesine işaret eder. Sonuç seçilerek veya hacim değiştirilerek geçerlilik sağlanamaz.', 'D04:7'),
      (['EPA Method 323'], 'EPA 323:2023 için doğru başlangıç dolumu hangisidir?', 'Boş / 20 mL reaktif su / silika jel',
       ['100 mL NaOH / 100 mL NaOH / su', 'Üç şişede de 100 mL asit', 'İlk şişede 200 g silika, diğerleri boş'],
       'Kondensat tutucu ilk şişe boştur; su ikinci şişededir. Başka bir formaldehit türevlendirme yönteminin reaktifi bu yönteme aktarılmaz.', 'W04:2-4'),
      (['EPA Method 323'], 'EPA 323’te 0,5 L/dk ayarlanması uygun mudur?', 'Hayır, 0,4 L/dk üst sınırını aşar.',
       ['Evet, her formaldehit yöntemi 1 L/dk ister.', 'Evet, yalnız şişe sayısı önemlidir.', 'Ancak 30 dakika olursa uygundur.'],
       'Bu sınır seçilen yönteme aittir. Daha yüksek debiyle aynı süre çekmek, yakalama performansının geçerli kalacağını tek başına göstermez.', 'W04:3-5'),
      (['CARB Method 425'], 'CARB 425’te numune filtresi nereye yerleştirilir?', 'İki alkali impingerden sonra',
       ['Nozülün önüne', 'Her zaman ilk impingerin önüne', 'DGM egzozuna'],
       'CARB 425 düzeni prob, alkali şişeler, PTFE kaplı cam elyaf filtre ve nem tutucu sırasındadır. EPA 29 ön filtre düzeni burada kullanılamaz.', 'W02:13,22'),
      (['CARB Method 425'], 'CARB 425’te genel olarak impinger yıkaması zorunlu mudur?', '§13.3 impinger yıkaması gerektirmez.',
       ['Her şişeye mutlaka 200 mL aseton gerekir.', 'Daima saf sülfürik asit gerekir.', 'Yıkama sıvısı silikaya dökülür.'],
       'Prob geri kazanımı ile impinger geri kazanımı farklı adımlardır. Bir yöntemdeki yıkama alışkanlığı başka metoda otomatik taşınmamalıdır.', 'W02:23'),
      (['CARB Method 426'], 'CARB 426’da numune koruması için 2 mL 10 N NaOH hangi temelde verilir?', 'Numunenin her litresi için; pH ≥12 kontrolüyle',
       ['Her kaba hacimden bağımsız 2 mL', 'Her litre çekilen gaz için', 'Her metre prob için'],
       'Koruyucu dozu sıvı numunenin hacmiyle ilişkilidir. Gaz hacmi ile sıvı numune hacmini karıştırmak yanlış kimyasal dozuna yol açar.', 'W03:10-13'),
      (['CARB Method 426'], 'CARB 426’daki Whatman 42 ifadesi doğrudan saha filtresi seçimi midir?', 'Hayır, laboratuvar filtrasyon ekipmanı bağlamındadır.',
       ['Evet, her baca filtresi Whatman 42 olmalıdır.', 'Hayır, bu bir gaz debisidir.', 'Evet, impingerdeki çözelti adıdır.'],
       'Aynı metindeki laboratuvar ve saha ekipmanları ayrılır. Başlıktaki bağlamı atlayarak filtre adı aktarmak örnekleme sistemini değiştirebilir.', 'W03:3-5'),
      (['EPA CTM 027'], 'CTM-027’de filtre hangi konumdadır?', 'Baca içinde, Method 17 düzeninde',
       ['Üçüncü impingerden sonra', 'Pompa çıkışında', 'Yalnız laboratuvar hunisinde'],
       'Kaynakta in-stack filtre belirtilir. Genel bir ısıtmalı dış filtre simgesi, bu metoda özgü filtre konumunu doğru biçimde göstermez.', 'W01:2-4'),
      (['EPA CTM 027'], 'CTM-027’de üçüncü impinger hangi iki başlangıç seçeneğine sahiptir?', 'Boş veya 100 mL 0,1 N H₂SO₄',
       ['100 mL permanganat veya aseton', 'Daima 500 mL su', 'Daima 30 g CdSO₄'],
       'Yüksek yükte veya yüksek debide ek asit kademesi kullanılabilir. İki düzen aynı parametre altında farklı varyantlar olarak kaydedilmelidir.', 'W01:3-4'),
      (['EPA CTM-022'], 'EPA CTM-022 hangi bileşenler için elektrokimyasal yöntemdir?', 'NO, NO₂ ve NOₓ',
       ['Yalnız SO₂', 'Yalnız dioksin', 'Yalnız çöken toz'],
       'Resmî EPA koşullu yöntem listesi CTM-022’yi azot oksitleriyle eşleştirir. SO₂ için ISO 7935 ile aynı yöntem gibi sunulması yanlıştır.', 'US EPA EMC Conditional Test Methods: CTM-022'),
      (['ISO 12141'], 'Arşivde ISO 12141:2002 varken katalogda 2024 sürümü bulunursa ne yapılır?', 'Yeni tam metin karşılaştırılana kadar eski kurallar güncel diye sunulmaz.',
       ['Dosya adına 2024 yazmak yeterlidir.', 'Eski PDF otomatik yeni sürüme dönüşür.', 'Bütün sayılar mutlaka değişmiştir denir.'],
       'Sürüm değişikliğini bilmek hangi maddelerin değiştiğini bilmek değildir. Katalog kaydıyla tam prosedürün teknik karşılaştırması ayrı işlemlerdir.', 'ISO katalog: https://www.iso.org/standard/85643.html; D31'),
    ]
    for tags, prompt, right, wrong, why, source in cases:
        add(t,e,tags,prompt,right,wrong,why,source)
    add('Gaz analizörleri',e,['TS ISO 7935'],'ISO 7935:2024’te ≤200 s tepki süresi kriteri neyi belirtir?',
        'AMS performans koşulunu; her ölçümün toplam süresi değildir.',
        ['Her ölçüm tam 200 saniye sürer.', 'Her gazda T90 yerine 200 yazılır.', 'Numune 200 saniye içinde laboratuvara ulaşır.'],
        'Cihaz/sistem cevabı ile temsilî ortalama alma süresi farklı kavramlardır. Bir performans sınırından tek bir saha ölçüm süresi türetilemez.', 'D32:12; ISO 7935:2024 Tablo 1')
    add('Gaz analizörleri',e,['TS ISO 7935'],'ISO 7935:2024’te 24 saat sıfır/span driftinin %2 sınırında payda nedir?',
        'Kullanılan en düşük ölçüm aralığının üst değeri',
        ['Her an ölçülen SO₂ derişimi', 'DGM başlangıç hacmi', 'Baca çapı'],
        'Yüzde bir sınır, paydası belirtilmeden uygulanamaz. Aynı tabloda hat kaybı/kaçak için ölçülen değer kullanılması iki yüzdeyi özdeş yapmaz.', 'D32:12; ISO 7935:2024 Tablo 1')

    # Aynı kaynak koşulunun uygulama hesabı; referans koşulları değiştirilmez.
    add('Birimler ve hacim',e,['EPA Method 323'],'0,4 L/dk sabit debiyle 30 dk çekişin hacmi aynı koşullarda kaçtır?',
        '12 L',['120 L','0,12 L','75 L'], 'V=Q×t=0,4×30=12 L. Bu sadece aynı koşullardaki hacim hesabıdır; yöntemin her kaynak için 30 dakika istediği anlamına gelmez.', 'Boyutsal hesap; W04:3-5 debi sınırı')
    add('Birimler ve hacim',e,['EPA Method 4'],'Qort=10 L/dk ise EPA 4’ün %4 ve 0,57 L/dk kıyasından hangi kaçak sınırı çıkar?',
        '0,40 L/dk',['0,57 L/dk','4 L/dk','0,97 L/dk'], 'Ortalama debinin %4’ü 0,40 L/dk’dir. İki sınırın küçüğü kullanıldığı için 0,57 L/dk tek başına kabul ölçütü olamaz.', 'D08:5; boyutsal hesap')
    add('Birimler ve hacim',e,['EPA Method 4'],'Qort=20 L/dk iken %4 debi 0,80 L/dk çıkarsa EPA 4 kaçak sınırı nedir?',
        '0,57 L/dk',['0,80 L/dk','1,37 L/dk','20 L/dk'], 'Yüzde sınırı 0,80 L/dk olsa da mutlak 0,57 L/dk daha sıkıdır. Karşılaştırma her ölçümün gerçek ortalama debisiyle yapılır.', 'D08:5; boyutsal hesap')
    add('Birimler ve hacim',e,['EPA Method 4'],'21 L/dk × 20 dk hesabı tek başına 0,60 standart m³ şartını kanıtlar mı?',
        'Hayır; 420 L çıkar ve hacimlerin referans koşulları da eşleştirilmelidir.',
        ['Evet, 420 L her zaman 600 L’ye eşittir.', 'Evet, süre 20 dakika olunca her yöntem uygundur.', 'Evet, referans sıcaklığı önemsizdir.'],
        'Çarpım yalnız aynı koşullardaki hacmi verir. Hem asgari hacim hem sıcaklık, basınç ve kuru/yaş baz birlikte kontrol edilmelidir.', 'D08:4-6; boyutsal hesap')
    add('Girdap ve uygunsuz yer',e,['EPA Method 1'],'Null açılar +25°, −25° ve 0° ise ortalama mutlak açı kaçtır?',
        'Yaklaşık 16,67°',['0°','25°','50°'], 'Mutlak değerler toplamı 50° ve nokta sayısı 3’tür. İşaretlerin birbirini götürmesi, girdap değerlendirmesinin amacına aykırıdır.', 'EPA Method 1 §11.4; boyutsal hesap')
    add('Girdap ve uygunsuz yer',e,['EPA Method 1'],'EPA Method 1 null tekniğinde ortalama mutlak açı tam 20° ise yalnız >20° kuralı bakımından ne söylenir?',
        'Bu eşik aşılmış değildir; diğer uygunluk koşulları ayrıca gerekir.',
        ['Kesinlikle bütün standartlara uygundur.', '20° her durumda 30° sayılır.', 'Noktalar hesap dışına çıkarılır.'],
        'Bir eşik için matematiksel karşılaştırma bütün saha kabulünün yerine geçmez. Akış, konum ve ilgili yöntemin diğer gerekleri de değerlendirilir.', 'EPA Method 1 §11.4')
    add('Kalite ve teslim',e,['EPA Method 26A'],'Asitli ve alkali halojen fraksiyonları aynı kaba dökülürse ilk yapılacak değerlendirme nedir?',
        'Fraksiyon bütünlüğünün bozulduğunu kaydetmek ve yöntem geçerliliğini değerlendirmek',
        ['pH’ı rastgele değiştirip olayı gizlemek', 'Numune etiketini değiştirerek düzeltmek', 'DGM hacmini ikiyle çarpmak'],
        'Fraksiyonlar farklı türlerin ölçümüne hizmet eder. Karıştırma, sonradan sayaç veya etiket değiştirilerek giderilebilecek bir kayıt hatası değildir.', 'D06:7-8; fraksiyon kontrolü')
    add('Kalite ve teslim',e,['EPA Method 29'],'Asitli peroksit ve asitli permanganat şişelerinin aynı kimlikle raporlanması neden yetersizdir?',
        'Farklı metal/cıva fraksiyonlarının geri kazanım ve analiz izi kaybolur.',
        ['Şişe sayısı yalnız estetik amaçlıdır.', 'Bütün metaller aynı tek kapta olmak zorundadır.', 'Kalibrasyon katsayısı otomatik sıfırlanır.'],
        'EPA 29 düzeninde cıva ve diğer fraksiyonlar ayrı işlemler gerektirir. Kap numarası, içerik ve analiz hedefi teslim zincirinde eşleşmelidir.', 'D07:11-14')
