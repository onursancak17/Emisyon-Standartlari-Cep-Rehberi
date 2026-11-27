"""27 Kasım 2026: EPA saha hazırlığı, kabul ve teslim bölümleri karşılaştırması."""
from copy import deepcopy

SOURCES=[
 dict(id='W07',title='US EPA Method 4 — Moisture',edition='EMC sayfasında 30.05.2023 etiketli 15 sayfalık nüsha',pages=15,url='https://www.epa.gov/sites/default/files/2020-12/documents/method_4.pdf'),
 dict(id='W08',title='US EPA Method 17 — In-stack particulate',edition='03.08.2017',pages=7,url='https://www.epa.gov/sites/default/files/2017-08/documents/method_17.pdf'),
 dict(id='W09',title='US EPA Method 2 — S-type Pitot velocity',edition='02.08.2017',pages=22,url='https://www.epa.gov/sites/default/files/2017-08/documents/method_2.pdf'),
 dict(id='W10',title='US EPA Method 25A — FID',edition='03.08.2017',pages=7,url='https://www.epa.gov/sites/default/files/2017-08/documents/method_25a.pdf'),
]

def extend(data,profile,node,imp,meter,delivery):
    byid={p['id']:p for p in data}
    def phase(p,title):return next(s['items'] for s in p['phases'] if s['title']==title)
    def evidence(p,field,refs,clause):p['evidence'].append(dict(field=field,references=refs,clause=clause))
    leak=['Ön kaçak testi önerilir; parça değişiminden hemen önce ve ölçüm sonunda test zorunludur. Sonda/ara testte koşuda görülen en yüksek vakum veya üstü kullanılır.',
          'Method 5 §8.4: kabul edilen kaçak ≤min(ortalama Q ×0,04; 0,57 L/dk). 380 mmHg yaklaşık 50,66 kPa vakumdur; düşük ön test vakumu ancak ölçüm sırasında aşılmıyorsa kullanılabilir. Aşımda yalnız §12.3 hacim düzeltmesi veya ölçümün reddi uygulanır.']

    p=byid['moisture_epa4'];p['sourceVersion']='EMC 30.05.2023 etiketli nüsha';p['sources']=['W07:1-10','D09:3,8'];p['reviewState']='sections_checked'
    p['variant']='Referans yöntem — dış partikül filtresi ve dört impinger'
    p['train'][0].update(label='Isıtılmış numune probu',content='Yoğuşma önlenir; bu bağımsız nem varyantı izokinetik nozül gerektirmez')
    p['train'][1].update(label='Isıtılmış dış partikül filtresi',content='Alternatif baca içi filtre §6.1.1’de tanımlıdır')
    p['limits'][1]['value']='En az 0,60 standart m³; kaynak standardı 20 °C / 101,325 kPa. Ham DGM ile kuru standart hacim ayrı; 0 °C Nm³ değildir.'
    p['limits'][3]['value']='Hedef standart hacim ve eşit nokta süreleriyle planla. Kirletici ölçümüyle eşzamanlı tayinde aynı toplam süre ve eşzamanlı örnekleme gerekir; 16–20 dk gibi otomatik sabit süre atanmaz.'
    phase(p,'Hazırlık')[:]=['Dört GS impinger: 1/3/4 modifiye düz uçlu, 2 standart uçlu; ilk ikide 100’er mL su, üçüncü boş, sonuncuda yaklaşık 200–300 g silika jel. Başlangıç ve son tartımları en az 0,5 g hassasiyetle kaydet.',
        'Bağımsız nem referansında: dairesel D<0,61 m için en az 8; dikdörtgen eşdeğer çap<0,61 m için en az 9; diğerlerinde en az 12 travers noktası. Konumlar Method 1; daha az nokta özel yetkili onayı gerektirir (§8.1.1.1).',
        'Günlük saha terazisi kontrolü: en az 500 g veya dolu impinger kütlesine ±50 g yakın, ASTM E617 Class 6 veya iyi ağırlık; sertifikalı değere ±0,5 g içinde. Uygunsuzsa düzeltip kontrolü tekrar et (§10.3).']
    phase(p,'Kaçak kontrolü')[:]=['Sayaç kutusunun pompa sonrası bölümü ilk kullanım ve her sevkten sonra denetlenir; 13–18 cm su sütunu basınçta 1 dk basınç kaybı kontrol edilir.']+leak
    phase(p,'Örnekleme')[:]=['Prob/ısıtılan filtreyi yaklaşık 120 °C’ye getirip kararlı hale gelmesini bekle; ön yoğuşmayı önle. Silika jel çıkış gazı <20 °C tutulur; banyo sıcaklığı ile çıkış gazı sıcaklığı aynı büyüklük değildir.',
        'Bağımsız ölçümde debi ≤21 L/dk ve sabit değerin ±%10’u içinde; eşzamanlı izokinetik yöntemde sabit debi yerine izokinetik koşul izlenir. Başlangıç/son ve her nokta-zaman aralığı sayaç/T/P okumaları korunur.',
        'Gaz doymuşsa veya damlacık şüphesi varsa eşzamanlı sıcaklık ve doygunluk buhar basıncı/psikrometriyle ikinci nem tayini yap. İki nemden düşük olanı kullan; damlacıkları su buharı diye sayma (§4.1, §12.1.6).']
    phase(p,'Geri kazanım')[:]=['İmpinger ve silika jel son kütlelerini yıkama yapmadan belirle; her ikisinin net kütle artışı nem hesabına dahildir. Silika jeli aktarırken su/çözelti ekleme.',
        'Kaynakta su buharı dönüşümü 0,001335 m³/g (20 °C referansı); Vw,std toplam su kütle artışından, Vm,std DGM/Y/T/P’den hesaplanır. Bws=Vw,std/(Vm,std+Vw,std). Ham DGM hacmi bu kesrin paydasında düzeltilmiş hacmin yerine kullanılmaz.']
    phase(p,'Saklama ve taşıma')[:]=['Bu ölçümde laboratuvara kimyasal analiz için bekletilen bir kirletici çözeltisi yoktur; nem kütlesi/tartım verileri saha prosedüründe belirlenir. Tartım gecikecekse nem alımı/kaybı önlenecek kapama ve izlenebilirlik gerekir. Kimyasal numunelerin bekletme sürelerini nem verisine aktarma.']
    phase(p,'Laboratuvara teslim')[:]=delivery+['Başlangıç/son impinger ve silika kütleleri, terazi günlük kontrolü, sayaç/Y/T/P, kaçaklar, nokta/süreler ve doygunluk karşılaştırması rapor birimine verilir.']
    p['evidence']=[]
    evidence(p,'Tren / nokta / debi / süre',['W07:2-5','D09:3,8'],'§6.1, §8.1')
    evidence(p,'Kaçak / tartım / hesap / doygunluk',['W07:2-10'],'§4.1, §8.1.3–4, §10.3, §11–12')
    p['gaps']=['Uygulanacak mevzuatın ve eşzamanlı kirletici metodunun özel şartları ölçüm planında seçilmelidir. Bu kart referans nem yöntemidir; yaklaşık nem yöntemi aynı amaçla kullanılamaz.']

    for pid in ('fluoride_epa13a_rear','fluoride_epa13a_front'):
        p=byid[pid];p['reviewState']='sections_checked';p['sources']=['D05:1-7','D09:7-10,15-18,22-23']
        phase(p,'Hazırlık')[:] +=['Hedef toplam inorganik florürdür; florokarbon/Freon ölçümü değildir. Yüksek klorür girişimi ve numuneye temas eden gresin düşük sonuç oluşturması değerlendirilir (§1, §4).',
            ('Arka filtre Whatman No.1 veya eşdeğeridir.' if pid.endswith('rear') else 'Ön filtre ≥%95 verim @0,3 µm test aerosolü, <0,015 mg F/cm² blank ve 135 °C’ye dayanım şartlıdır. En az 3 filtreden lot blank ortalaması belirlenir; cam elyaf genellikle yüksek/değişken flor blankı nedeniyle uygun değildir.'),
            '1/3/4 modifiye GS; 2 standart GS uçlu. Ön filtrede 20-mesh çelik destek; cam frit/sinter metal destek kullanılmaz. Arka filtrede cam frit destek mümkündür (§6.1).']
        phase(p,'Kaçak kontrolü')[:]=deepcopy(leak)
        phase(p,'Saklama ve taşıma')[:]=['Sıvı numune geniş ağızlı, yaklaşık 1 L HDPE kapta; filtre, ilk üç şişe ve bütün su yıkamaları aynı numuneye alınır. Filtreyi ayrı işleme yalnız izin verilen alternatif prosedürle yap (§6.2.2, §8.6.4).',
            'Kap sızdırmaz kapatılır, seviye işaretlenir. İncelenen Method 13A numune bölümünde sayısal saklama sıcaklığı/azami bekletme süresi verilmez; bunlar laboratuvarın geçerli kabul planında tanımlanmalıdır. Reaktifin raf ömrü numune bekletme süresi değildir.']
        phase(p,'Laboratuvara teslim')[:] +=['Numune blankı: kullanılmamış filtre ve numuneyle eşit toplam su hacmi; aynı analiz prosedürü. Ön filtre lot blankı ile bu numune blankı ayrı kontrollerdir (§7.1.1.2, §8.6.4.2).']
        p['gaps']=['Metot bağlantılı Method 1/2/3 saha geometrisi ve gaz yoğunluğu, ilgili ölçüm planında tamamlanır; numune kabul koşulları laboratuvarca yazılı tanımlanır.']
        evidence(p,'Kapsam / filtre türü / destek / kap',['D05:1-6'],'§1, §4, §6–8')
        evidence(p,'Kaçak / izokinetik / süre',['D09:7-10,22-23'],'Method 5 §8.2, §8.4–5, §12.11 bağlantısı')

    for pid in ('metals_epa29_hg','metals_epa29_no_hg'):
        p=byid[pid];hg=pid.endswith('_hg') and not pid.endswith('no_hg')
        p['reviewState']='sections_checked';p['sources']=['D07:3-7,10-15,24-26','D09:1-3,7-10,15-18,22-23']
        p['train'][0].update(content='Cam nozül / borosilikat veya kuvars iç prob; hedef metal bulaşması yapmayan bağlantı')
        p['train'][1].update(content='Organik bağlayıcısız, metal blankı uygun filtre; metal içermeyen PTFE destek')
        p['limits'][0]['value']='Method 5 bağlantılı izokinetik: genel kabul %90–110. Sabit L/dk atanmaz; EN toz standardının %95–115 bandı buraya taşınmaz.'
        p['limits'][2]['value']='Method 5 bağlantılı prob/filtre 120±14 °C; farklı uygulama sıcaklığı özel hüküm/onay gerektirir. Son impinger çıkış gazı <20 °C.'
        p['limits'][3]['value']='Method 5: noktalarda eşit süre ve en az 2 dk/nokta; mevzuatın toplam süre/hacmi ayrıca sağlanır. Her bacaya evrensel 30 dk/3 tekrar atanmaz.'
        phase(p,'Hazırlık')[:] +=['Camlar: sıcak su/sabun, musluk ve uygun saf suyla üçer durulama, ≥4 saat %10 hacim/hacim HNO₃ içinde bekletme, su ve son aseton durulaması, hava kurutması (§8.1.1).',
            'Filtre hedef metal başına <1,3 µg/in² =yaklaşık 0,2015 µg/cm²; üretici verisi yoksa lot blank analizi. Su hedef metal başına <1 µg/L; absorpsiyon çözeltisi <2 µg/L hedef metal saflığında (§7.2–7.3).',
            'Asitli peroksit tarifi: yaklaşık 500 mL suya 50 mL derişik HNO₃, sonra 333 mL %30 H₂O₂ stok çözeltisi; son hacim 1 L. Stok yüzde tanımı kaynağın hacim/hacim tarifidir; EN 14385 kütle/kütle reçetesiyle değiştirme.']
        if hg:phase(p,'Hazırlık')[:] +=['Asitli permanganat taze günlük hazırlanır: %4 kütle/hacim KMnO₄, %10 hacim/hacim H₂SO₄ ortamında. Camda hazırlanıp saklanır; §7.3.2 filtreleme ve basınç önlemleri uygulanır.']
        phase(p,'Kaçak kontrolü')[:]=deepcopy(leak)
        phase(p,'Saklama ve taşıma')[:]=[('Cıva/permanganat numune ve blankları oksitleyiciye dayanıklı PTFE astarlı kapaklı 500/1000 mL camda; diğer fraksiyonlarda cam veya PE kap kullanılabilir (§6.2.2).' if hg else 'Cıva içermeyen bu varyantın fraksiyonları için cam veya PE numune kapları kullanılır (§6.2.2).'),
            'Kaplar etiketli ve dik; sıvı seviyeleri işaretli. Method 29 saha bölümü sayısal genel saklama sıcaklığı/azami bekletme süresi vermez. Analitik yöntem ve numune matrisiyle uyumlu laboratuvar kabul/koruma planı ayrıca gerekir. EN 14385’in dört haftasını buraya otomatik aktarma.']
        if hg:phase(p,'Saklama ve taşıma')[:] +=['Permanganat kaplarında basınç oluşabilir; ağzına kadar doldurma, bulaşmaya izin vermeyen basınç tahliyesini §5.3/§8.2.9.2 ve laboratuvar taşıma planıyla uygula.']
        phase(p,'Laboratuvara teslim')[:] +=['Blank düzeltmesi EN 14385 ile aynı değildir. Method 29 §12.6–12.7, fraksiyon ve hedefe göre sınırlı düzeltmeler verir; ölçülen blankı sınırsız çıkarma. Ön/arka fraksiyonları ayrı analize ve hesaba izlenebilir teslim et.',
            'Cıva dışı metalde: ön yarı eşiği A=1,4 µg/in² × toplam filtre alanı(in²), arka yarı A=1 µg. Blank B≤A ise B çıkarılır; B>A ise çıkarılacak miktar max(A; min(B; numune kütlesinin %5’i)). Filtre kabulündeki 1,3 µg/in² ile bu 1,4 düzeltme eşiğini karıştırma.']
        if hg:phase(p,'Laboratuvara teslim')[:] +=['Cıvada bütün fraksiyonlar için toplam blank eşiği 0,6 µg: blank bunun altındaysa tamamı, üstündeyse max(0,6 µg; min(toplam blank; toplam numune Hg kütlesinin %5’i)) çıkarılır (§12.7).']
        p['gaps']=['Hedef metal listesi, analitik tayin sınırı, blank düzeltmesi ve laboratuvarın numune kabul koşulları numune planında eşleştirilmelidir. Cıva istenirse cıva içeren varyant kullanılmalıdır.']
        evidence(p,'Sıcaklık / süre / izokinetik',['D07:4,11,26','D09:1-3,7-10,22-23'],'§6.1.4, §8.1.4–6, §12.9; Method 5 bağlantıları')
        evidence(p,'Kap / reaktif / saflık / taşıma',['D07:3-7,10-15'],'§5.3, §6.2.2, §7.2–7.4, §8.1–8.2')
        evidence(p,'Blank düzeltmesinin ayrımı',['D07:24-26'],'§12.6–12.7')

    p=byid['acid_epa8'];p['reviewState']='sections_checked';p['sources']=['D10:2-7','D09:7-10,22-23']
    for n in p['train']:
        if n['id']=='i1':n['content']='%80 izopropanol (hacim/hacim); standart GS uç'
        if n['id']=='i2':n['content']='%3 H₂O₂ (hacim/hacim); modifiye GS uç'
        if n['id']=='i3':n['content']='%3 H₂O₂ (hacim/hacim); standart GS uç'
    phase(p,'Hazırlık')[:] +=['İlk ve üçüncü şişe standart, ikinci/dördüncü modifiye GS uçludur. İzopropanolün peroksit safsızlığı kontrol edilir; %3 H₂O₂ günlük taze hazırlanır. Florür, serbest NH₃ veya dimetil anilin varsa girişim için onaylı alternatif gerekir (§4.1, §6.1, §7.1).']
    phase(p,'Kaçak kontrolü')[:]=deepcopy(leak)+['Ön testte filtre girişi yerine ilk impinger girişi tıkanır; prob yalnız yoğuşmayı önleyecek kadar ısıtılır; filtre tutucusu ısıtılmaz.']
    phase(p,'Saklama ve taşıma')[:]=['Her ölçümün iki fraksiyonu ayrı, sızdırmaz yaklaşık 1 L PE şişede; buharlaşma önlenir, seviye işaretlenir ve kaplar dik taşınır (§6.2.3, §8.8).',
        'Method 8 saha bölümünde sayısal genel saklama sıcaklığı/azami bekletme süresi belirtilmez; laboratuvarın matris/analiz kabul koşulları önceden yazılı belirlenir. 15 dakikalık temiz hava süpürmesi analiz bekletme süresi değildir.']
    p['gaps']=['İlgili uygulamanın toplam süre/hacmi ve laboratuvar numune kabul planı gerekir; kaynakta bulunmayan sayısal saklama süresi atanmaz.']
    evidence(p,'Girişimler / uç tipleri / reaktif / kap',['D10:2-4'],'§4, §6–7')
    evidence(p,'Kaçak / süre / izokinetik',['D10:4-6','D09:7-10,22-23'],'§8.4–8.7; Method 5 bağlantısı')

    p=byid['h2s_epa11']
    next(n for n in p['train'] if n['id']=='meter')['content']='DGM / debi ve basınç kaydı; pompa basınçlı yakıt gazı örneklemesinde normalde gerekmez'
    phase(p,'Geri kazanım')[:] +=['Antifoam B kullanılmadıysa veya şişede belirgin sarı CdS kaldıysa §11.2 asitlendirilmiş iyotla alternatif ekstraksiyon gerekir; yıkama bir impingerden diğerine aktarılmaz, doğrudan iyot balonuna alınır.']
    phase(p,'Saklama ve taşıma')[:]=['Geri kazanım temiz, ısı kaynağından uzak ve doğrudan güneş almayan yerde. Açıklıklar kapatılır; CdSO₄/CdS fraksiyonu ve peroksit fraksiyonu ayrıdır.',
        'Asitlendirilmiş iyot eklenmiş numune saklanamaz: yaklaşık 30 dk karanlıkta absorpsiyon sonrası §11.3 titrasyon takvimi uygulanır. İyot eklenmeden önce keyfi 24 saat/7 gün bekletme kuralı bu metotta verilmez.']
    phase(p,'Hazırlık')[:] +=['DGM ilk kalibrasyonu üç bağımsız koşuda ≥5 devir; Y değerleri ortalamadan en çok %2 sapmalı. Seri sonu iki koşu ≥3 devir kontrol; başlangıçtan >%5 farkta yeniden kalibrasyon ve düşük gaz hacmini veren katsayı (§10.1.1).']
    p['gaps']=['Bu yöntem rafineri yakıt gazı kapsamlıdır. Farklı kaynağa uygulanabilirlik ve laboratuvar/yerinde titrasyon planı önceden doğrulanmalıdır.']
    evidence(p,'Saklama yasağı / alternatif geri kazanım',['D04:7-9'],'§8.6–8.7, §10.1.1, §11.2–11.3')

    # Tam saha PM kartları: 5 dış filtre, 17 baca içi filtre.
    for inside in (False,True):
        train=([node('nozzle','probe','Giriş nozülü','Akışa dönük'),node('filter','filter','Baca içi filtre','Baca sıcaklığında'),node('probe','probe','Filtre sonrası uzatma','Toplanan PM’nin önünde prob yok')] if inside else
               [node('probe','probe','Nozül / ısıtılmış prob','İzokinetik; 120±14 °C'),node('filter','filter','Isıtılmış dış filtre','Filtre çıkış gazı 120±14 °C')])
        train += [imp(1,'Su; modifiye GS','100 mL'),imp(2,'Su; standart GS','100 mL'),imp(3,'Başlangıçta boş; modifiye GS'),imp(4,'Ön tartımlı silika jel; modifiye GS','Yaklaşık 200–300 g'),meter]
        p=profile('dust_epa17' if inside else 'dust_epa5','Partikül madde / toz','EPA Method 17' if inside else 'EPA Method 5','03.08.2017' if inside else '07.12.2020',
            'Baca içi filtre' if inside else 'Isıtılmış dış filtre; dört impingerle nem',
            ['W08:1-7','D09:6-18,21-23'] if inside else ['D09:1-18,21-23'],train,
            ['İzokinetik %90–110; anlık hedef baca hızı/nozül/nem/T/P ile belirlenir. Sabit L/dk yok.',
             'Uygulanacak kaynak mevzuatının asgari kuru standart hacmi. Sayaç hacmi/Y/T/P ve kaçak düzeltmeleri birlikte; standart 20 °C bazını 0 °C Nm³ ile karıştırma.',
             'Baca içi filtrasyon baca sıcaklığında; doymuş/damlacıklı gazda uygulanmaz. Son nem tutucu çıkış gazı <20 °C.' if inside else 'Prob ve filtre çıkış gazı 120±14 °C; özel alt düzenleme/onay farklı koşul getirebilir. Son nem tutucu çıkış gazı <20 °C.',
             'Eşit süreli noktalar, en az 2 dk/nokta; kaynak mevzuatının toplam süresi/hacmi ayrıca. Daha kısa örnekleme özel yetkili onayı gerektirir.'],
            {'Hazırlık':['Method 1 yer/nokta, Method 2 hız/yoğunluk ve uygun nem tayiniyle nozül seç. Koşu içinde nozül çapını değiştirme. Nozül üç eksende 0,025 mm çözünürlükle ölçülür; en büyük-küçük fark ≤0,1 mm (§10.1).',
                 'Bağlayıcısız cam elyaf filtre: ≥%99,95 yakalama @0,3 µm; SO₂/SO₃’e reaksiyon vermemeli. Aseton reaktif saflığında, kalıntı ≤%0,001; saha öncesi blankı kontrol et.',
                 'Ön filtre şartlandırma: 20±5,6 °C’de ≥24 saat desikatör; ≥6 saat aralıklı tartımlarda fark ≤0,5 mg, kayıt 0,1 mg. Her tartımda laboratuvar havasına maruz kalma <2 dk; izin verilen fırın alternatifi ayrı prosedürdür.',
                 'Saha terazisi günlük ±0,5 g kontrolü; analitik terazi kullanım öncesi ve altı aylık çok noktalı kalibrasyon, günlük sertifikalı kütle kontrolü (§10.7–10.8).'],
             'Kaçak kontrolü':deepcopy(leak),
             'Örnekleme':['Filtre/prob koşulunu kararlı hale getir. Her nokta-zaman aralığında sayaç, sıcaklık, vakum, hız basıncı ve gerekli gaz verilerini kaydet; hız basıncında %20 değişimde ek debi ayarı/kayıt gerekir.',
                 'Nozül akışa bakar; porta/duvara çarpıp birikinti toplama. Port boşluğunu çevre hava ile seyrelmeyi önleyecek şekilde kapat. Pompa/vanaları geri sıvı yürümeyecek sırayla yönet.',
                 'Filtre değişecekse önce kaçak testi; bütün filtrelerin PM kütlesi numuneye dahildir. Seri sonu DGM kontrolünde Y farkı >%5 ise tam kalibrasyon; ret veya düşük toplam hacmi veren katsayı (§10.3.2–3).'],
             'Geri kazanım':['Filtreyi etiketli petriye, tortu içe bakacak şekilde al. Nozül ve filtre önündeki numuneye temas eden yüzeyleri asetonla nicel geri kazan; cam kapta ayrı topla, seviye işaretle. Dış yüzey tozunu numuneye karıştırma.',
                 'Temizlikte kullanılan her aseton deposundan 200 mL blank ayır. Method 5 ön yıkamasına Method 29’daki sabit 100 mL zorunluluğunu aktarma; kullanılan gerçek yıkama hacmini kaydet.',
                 'İlk üç impingerin nem kütlesini ≥0,5 g doğrulukla belirle. Silika jeli sıvı eklemeden ayrı kaba al veya yerinde tart. İmpinger çözeltisi ayrıca istenmiyorsa filtre edilebilir PM sonucuna otomatik eklenmez.'],
             'Saklama ve taşıma':['Filtre kimlikli kapalı petride; aseton fraksiyonu sızdırmaz cam kapta; seviye çizgisi, kap kimliği ve dik taşıma korunur. Bu metotta bütün numunelere uygulanacak genel sayısal azami taşıma/analiz süresi verilmez; laboratuvar planı bunu tamamlar.',
                 'Son filtre tartımı: ≥24 saat desikatör; ≥6 saat aralıklı iki tartımda fark ≤max(0,5 mg; net kütlenin %1’i). Bu son tartım kriteri ön tartımdaki sabit ≤0,5 mg ile karıştırılmaz.'],
             'Laboratuvara teslim':delivery+['Filtre(ler), ön aseton yıkaması, aseton blankı, varsa ayrı impinger analizi, nem/Y/T/P/kaçak/izokinetik ve süreç kayıtları birlikte teslim edilir. Numune kütlesi filtre+ön yıkama−izin verilen aseton blankıdır.']},
            state='sections_checked',gaps=['Kaynak mevzuatının asgari süre/hacmi, sıcaklık istisnası ve varsa kondanse olabilir PM için ayrı yöntem ölçüm planında belirlenmelidir.'])
        p['evidence']=[dict(field='Saha / geri kazanım / taşıma',references=['D09:6-13'],clause='§7–8'),dict(field='Kalibrasyon / tartım / kabul',references=['D09:15-18,21-23'],clause='§10–12')]
        if inside:
            phase(p,'Hazırlık')[:] +=['PM’nin normal kaynak sıcaklık aralığında sıcaklıktan bağımsız olduğu ve Method 17 kullanımına izin verildiği doğrulanır. Prob uzatma/filtre tutucu izdüşüm alanı baca kesitinin >%5’i ise standart düzen olduğu gibi kullanılamaz; dış filtre veya onaylı ayrı hız/örnekleme düzeni gerekir (§1.2, §8.1.2).']
            phase(p,'Kaçak kontrolü')[:] +=['Filtre tutucusu nozül sıcaklığa dayanıklı tıkaçla kapalıyken bacaya yerleştirilir; yaklaşık 5 dk veya kararlı hale gelene kadar beklenip kaçak testi yapılır (§8.1.4).']
            phase(p,'Geri kazanım')[:] +=['Method 17 ön yarısı nozül/filtre tutucudur; filtre SONRASI uzatma borusunu ön PM yıkamasına katma. Kaynağın eski Method 5 madde numaraları, güncel Method 5’in ilgili başlığıyla eşleştirilir.']
            evidence(p,'Baca içi varyantın özel koşulları',['W08:1-5'],'§1.2, §6, §8')
        data.append(p)
