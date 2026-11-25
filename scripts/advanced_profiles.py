"""SCAQMD birincil metni ve EN 1948 Ek B'nin ayrı işletim örnekleri."""
from copy import deepcopy

EXTRA_SOURCES=[dict(id='W06',title='SCAQMD Method 207.1 — Ammonia',edition='Nisan 2006; madde ve basılı sayfa izleri',pages=49,
    url='https://www.aqmd.gov/docs/default-source/laboratory-procedures/methods-procedures/stm-207-1.pdf')]


def extend(data,profile,node,imp,meter,delivery):
    data[:]=[p for p in data if p['id']!='ammonia_2071']
    def add(*args,evidence,**kwargs):
        p=profile(*args,**kwargs);p['reviewState']='sections_checked'
        p['evidence']=[dict(field=k,references=v[0],clause=v[1]) for k,v in evidence.items()]
        data.append(p);return p
    for mini in (False,True):
        front=([node('line','probe','Flux odası / kaynak bağlantısı','İnert PE/PTFE hat; bu varyantta ön filtre yok')]
               if mini else [node('nozzle','probe','Baca giriş nozülü','Akışa ters bakar; izokinetik yöntem değildir'),
                   node('filter','filter','İsteğe bağlı baca içi filtre','Sinter metal veya bağlayıcısız cam/kuvars elyaf','',True),
                   node('probe','probe','Prob / bağlantı','Cam veya 316 çelik; PTFE için §2.2.1.1 konum/sıcaklık koşulları')])
        p=add('ammonia_2071_'+('mini' if mini else 'gs'),'Amonyak','SCAQMD Method 207.1','Nisan 2006',
            'Mini impinger — flux odası / baca dışı kaynak' if mini else 'Greenburg–Smith — baca gazı, izokinetik olmayan',
            ['W06:1-49'],[*front,imp(1,'0,1 N H₂SO₄','15 mL' if mini else '100 mL'),imp(2,'0,1 N H₂SO₄','15 mL' if mini else '100 mL'),
             imp(3,'Başlangıçta boş'),imp(4,'Ön tartımlı silika jel','Yaklaşık 30–45 g' if mini else 'Yaklaşık 200–300 g'),
             node('meter','meter','Pompa / kalibre hacim sistemi','Kalibre debi ölçer; referans koşulları kayıtlı' if mini else 'DGM ve sıcaklık/basınç kaydı')],
            ['Ek B genel planlama aralığı 0,75–1,0 L/dk; kaynağa özgü onaylı planla belirlenir.' if mini else
             '§3.1.5: 0,015–0,030 m³/dk = 15–30 L/dk. Kaynakta yanındaki 0,50–1,0 cfm yuvarlatılmıştır; Ek B tipik 14,16–21,24 L/dk aralığı ayrıca planlama örneğidir.',
             'Ek B: PSV = RL / STC × F, F≥1. Kuru standart hacim, gaz debisiyle aynı referansa getirilir; sıvı son hacmiyle karıştırılmaz.',
             'Şişeler buz-su banyosunda; su düzeyi absorbanın üstüne çıkar. Geri kazanım sonrası buzdolabı 1,67–7,22 °C (kaynak 35–45 °F).',
             'PST=PSV/VSR; debi hedefi sağlanmazsa süreyi yeniden hesapla. Saatlik kütle sınırı için ≥1 saat; çevrimli proseste tam çevrim ve aynı fazda başlangıç/son gerekir.'],
            {'Hazırlık':['Gaz halindeki serbest amonyak hedeflenir; partikül/amonyum tuzu, nem ve kuvvetli baz girişimlerini değerlendir. Baca ve flux odası düzenekleri ayrı seçilir. Nem Method 4.1 bağlantılıdır.',
                 '0,1 N asit hazırla veya belgeli hazır çözelti kullan. N ve mol/L aynı sayı değildir; Şekil 207.1-2 üzerindeki 0,1 M etiketi ile §2.2.2/2.3.4/2.4.2’deki 0,1 N metni çelişir. Bu kart açık metindeki 0,1 N tarifini izler; laboratuvar uygulama planında çelişkiyi çöz.',
                 'En az bir blank tren/test seti ve en az günlük bir blank; örnekle aynı kurulum/geri kazanım. Blank numune sonucundan çıkarılmaz. İki ayrı test koşusu gerekir; eşzamanlı iki tren yazılı özel izin olmadan bu tekrarın yerini almaz.'],
             'Kaçak kontrolü':(['Ön/son ve parça değişimi öncesi/sonrası kaçak: ortalama örnekleme debisinin <%4’ü. Sonucu ve değişen parçayı kaydet (§3.2.4–3.2.6).'] if mini else
                 ['Ön test: nozül kapalı 380 mmHg ≈50,66 kPa vakum; daha düşük vakum ancak koşu bunu aşmıyorsa. Kaçak hem Q’nun %4’ünü hem yaklaşık 0,57 L/dk’yı aşmamalı (§3.1.4).',
                  'Son test ve parça değişiminde koşuda görülen en yüksek vakum veya üstü. Aşımda yalnız Chapter X §7’nin izin verdiği hacim düzeltmesi veya ret uygulanır. Tıkacı yavaş açıp sonra pompayı kapat; sıvıyı proba geri çekme.']),
             'Örnekleme':['Debi, başlangıç/son sayaç, süre, banyo ve süreç değişimlerini izle. Baca kütlesel emisyonunda hız ve eşzamanlı sabit gaz ölçümü gerekir; tabakalaşma varsa travers uygulanır.',
                 'Bu gaz yöntemine izokinetik toz nozülü kuralı aktarma. Baca varyantında nozül akışa ters yerleştirilir; isteğe bağlı filtre probun önündedir. Mini varyanta bu filtre eklenmez.'],
             'Geri kazanım':['Numune geri kazanımı alımdan itibaren en geç 7 takvim gününde; rüzgâr/toz/amonyaktan korunmuş ortamda yapılır. Şişeleri 0,1 g hassasiyetle tart; her absorbanın pH’ını kaydet. Herhangi birinde pH>2 ise sonuç geçersizdir.',
                 'Prob/numune hattı, silika dışındaki şişeler ve bağlantıları DI suyla en az üç durulama ile geri kazan. '+('Son hacim 75 mL; reaktif blankı 30 mL asit çözeltisinden aynı son hacme getir (§4.1.2).' if mini else 'Son hacim 500 mL; gerekirse 1000 mL. Reaktif blankı 200 mL asit çözeltisinden aynı son hacme getir (§4.1.1).'),
                 'Son analiz hacmi hedefini yıkama/kondensat nedeniyle aşıyorsan numuneyi kaybetme; gerçek son hacmi laboratuvarla kaydet. NH₃-N sonucunu NH₃’e 17,03/14,01 ile çevir; kütle hesabında gerçek son hacmi kullan.'],
             'Saklama ve taşıma':['Tren açıklıklarını kontaminasyona karşı kapat; soğurken ucu sıkıca kapatıp absorbanı geri yürütme. Numune kaybını ve buharlaşmayı önle; kimlikli, temiz, sızdırmaz laboratuvar kabı kullan.',
                 'Geri kazanım sonrası numune ve metot blankı 1,67–7,22 °C’de saklanır; en çok 4 hafta. Bu dört haftanın başlangıcı geri kazanımdır; alımdan sonraki 7 günlük geri kazanım sınırı ayrı izlenir.'],
             'Laboratuvara teslim':delivery+['Hangi trenin kullanıldığı, pH, gerçek son sıvı hacmi, reaktif/saha blankları, iki koşunun ayrı sonuçları, gaz hacmi/bazı ve zaman çizelgesi teslim edilir. SCAQMD uyum değerlendirmesinde en yüksek geçerli koşu kullanılır; yerel mevzuat planını ayrıca doğrula.']},
            gaps=['SCAQMD Chapter III/X ekipman kalibrasyonu ve özel hacim düzeltme denklemleri bu karta tam aktarılmadı. Flux odası alan/akış/temsil protokolü ayrı onaylanmalıdır. Asit etiket çelişkisi laboratuvar planında kapanmalıdır.'],
            evidence={'Tren / dolum':(['W06:1-49'],'§1.2, §2.2–2.4; basılı s.1,5–10; Şekil 207.1-1/2'),
                      'Kaçak / saha':(['W06:1-49'],'§3.1–3.2; basılı s.11–18'),
                      'Koruma / geri kazanım / hacim':(['W06:1-49'],'§1.3.5, §4.1, §5.1, Ek B; basılı s.3,19–21,31,B1–B2')})
        p['phases'][0]['items']+=[('Mini kaplar yaklaşık 30 mL; düz uçlu. İlk iki ucun kabarcıkları tabana çarpar; üçüncü/dördüncü uç kabın en az dörtte üçüne uzanır (§2.2.2.2).' if mini else
            'İlk iki kap standart uçlu Greenburg–Smith; üçüncü/dördüncü düz uçlu modifiye GS. Düz boru iç çapı yaklaşık 13 mm, tabandan yaklaşık 13 mm yukarıda (§2.2.1.3).')]
        p['trainNote']='0,1 N seçimi açık metindeki tarife dayanır. Şekil 207.1-2’deki 0,1 M etiketi aynı derişim değildir; kaynak çelişkisi görünür tutulur.'

    base=next(p for p in data if p['id']=='dioxin_en1948_filter')
    # Mevcut sıra B.4 ile eşleşir; eksik kurutma grubunu ve varyantın geri kazanımını tamamla.
    base['variant']='Ek B.4 — XAD-2 kondensat kabından önce; akış bölünmesiz'
    base['sources']=['D25:15,20-26,41-43']
    base['train'].insert(-1,node('dryer','trap','Silika jel kurutma','Kondensat kabı sonrasında; bu ek örnekte evrensel gram verilmez'))
    base['limits'][0]['value']='Ek B.4 işletim örneği yaklaşık 5–25 L/dk için tasarlanmıştır; gerçek debi izokinetik ve doğrulanmış aralıkta seçilir.'
    base['phases'][1]['items']=['Genel §9.3.3 EN 13284-1 bağlantısı ile kurulum testi; hat değişiminde ve sonda tekrar. Ek B.4 örneği 50 kPa vakumda <0,03 m³/saat =0,5 L/dk verir; bilgi amaçlı örnek genel normatif kabulün yerine geçirilmez.']
    base['phases'][3]['items']+=['Ek B.4: probu toluenle yıka; filtre/reçine kartuşlarını kapat; kondensatı ayrı koru. Kalan cam toluen yıkamalarını prob yıkamasına birleştir. Bu reçete, başka bir varyantın aseton/su yıkaması değildir.']

    for split in (False,True):
        notes=deepcopy({s['title']:s['items'] for s in base['phases']})
        notes['Hazırlık']=['Ek B bilgi amaçlı işletim örnekleridir; ana metnin minimum şartları ayrıca sağlanmalıdır. Validasyonlarda kullanılan 6 saat, bütün mevzuata evrensel süre atanması değildir.',
            ('Ek B.3: filtre çapı 125 mm; ≥30 g temizlenmiş XAD-2. Nozül/prob iç çapı ≥8 mm önerilir. Filtreye örnekleme standardı uygulaması sonrası ≥2 saat bekleme bu varyantın örneğidir.' if split else
             'Ek B.2: iki adet 0,5 L kabın her birinde 150 mL dietilen glikol/su (1:2 hacim/hacim). HPLC saflığı ve ön temizlik/blank şartlarını uygula. Başlangıç dolumu 150 mL, şişe kapasitesi 500 mL’dir.')]
        notes['Kaçak kontrolü']=['Genel §9.3.3 EN 13284-1 bağlantısını ve geçerli uygulama planını kullan. Hat değişiminde ve ölçüm sonunda kaçak testi gerekir. '+('Ek B.3’teki <%5 normal debi bilgi amaçlı örnektir; genel normatif kaçağı otomatik gevşetmez.' if split else 'Ek B.2 otomatik debi kontrolüyle sızdırmazlığın doğrulanmasını anlatır.')]
        notes['Örnekleme']=['Filtre çiy üstünde ve <125 °C; bu ek örnekte çiy+10 °C koşulu verilir. Soğutucu/adsorber <20 °C; buzlanmayı önle. O₂ kaydı ve genel en az 15 dakikalık sıcaklık/debi/hız kaydı sürer.']
        if split:notes['Örnekleme']+=['Ana/yan debi oranını ±%10 içinde sabit tut. XAD-2 kartuşu içindeki gaz hızı ≤34 cm/s; kartuş hızını baca hızıyla karıştırma. İki sayaç hacmini ayrı kaydet; filtre ve gaz fazı hesaplarında doğru kol hacmini kullan.']
        notes['Geri kazanım']=[('Ek B.3: filtre ve XAD kartuşunu kapatıp ışık almayan taşıma kutusuna al; kondensat ayrı kahverengi şişede. Nozül/prob laboratuvarda aseton ardından toluenle, tekrar edilerek yıkanır; uygun kuvars swab filtreye eklenir. Filtre tutucusu yaklaşık 20 mL toluenle iki kez yıkanır ve ekstraksiyon çözücüsüne katılır. Kondensatöre ait aseton/toluen yıkama ile kartuş toluen yıkaması kondensata katılır.' if split else
            'Ek B.2: cam ve bağlantıları 100 mL aseton ve 100 mL diklorometanla yıka; bu yıkamalar kondensatla birleşir. Bubbler çözeltilerini temiz cam kaba aktar; şişeleri su, aseton, ardından diklorometanla durula. Filtre tutucusunu kapat. Bu varyantta diklorometan yerine rastgele saf su atanmaz.'),
            'Saha blankı kurulum, kaçak testi ve sökümü içerir; prob bacaya sokulmaz ve gaz çekilmez. Blank ≤%10 ELV; sonuçtan çıkarılmaz. Sahada tekrar kullanılan parçaların son yıkaması saklanır; takip eden örnek sınırı aşarsa analiz edilir (§7.3).']
        p=add('dioxin_en1948_'+('split' if split else 'liquid'),'Dioksin / furan','EN 1948-1','2006',
            'Ek B.3 — filtre sonrası ana/yan kol; XAD-2' if split else 'Ek B.2 — iki sıvı bubbler; akış bölünmesiz',
            ['D25:15-26,32-38'],[],
            ['Ek B.3 doğrulanmış ana kol 3–5 m³/saat =50–83,33 L/dk; yan kol 0,5–0,7 m³/saat =8,33–11,67 L/dk. İki kolun referans koşulları planla doğrulanır.' if split else 'Ek B.2 örneği yaklaşık 2 m³/saat =33,33 L/dk için doğrulanmıştır; izokinetik çalışma sağlanır.',
             'Tayin sınırı ve mevzuat hedefinden planla; ana/yan hacimleri, DGM koşulları ve kuru standart baz ayrı tutulur.',
             'Filtre: çiy üstü ve <125 °C; bu ek örnek çiy+10 °C. Yoğuşturucu ve adsorber <20 °C, donma yok.',
             'İlgili mevzuat ve plan belirler. Ek B validasyonunun 6 saati bütün uygulamalara otomatik atanmaz.'],notes,
            gaps=['Ek B örneğinin seçili ekipman ve laboratuvar kalite planıyla eşdeğerliği ayrıca gösterilmelidir. İşaretli standart geri kazanımı ve EN 1948-2/3 laboratuvar yeterlilik kontrolü devam eder. EN 13284-1 tarihli atıf baskısı ayrıca eşleştirilmelidir.'],
            evidence={'Varyant / sınırlar':(['D25:15-22,32-38'],'§5.1.2, §7.4; bilgi amaçlı Ek B.2/B.3'),
                      'Geri kazanım / taşıma':(['D25:25,34,36-37'],'§9.3.5; Ek B.2.9/B.3.9')})
        if split:
            p['diagram']=dict(asset='assets/diagrams/dioxin_en1948_split.png',shared=[node('probe','probe','Cam nozül / prob','İzokinetik toplam gaz'),node('filter','filter','Filtre','Çiy+10 °C, <125 °C'),node('split','splitter','Akış bölücü','Ana/yan oran ±%10')],branches=[
                dict(id='main',label='Ana kol',nodes=[node('main_meter','meter','Ana kol pompa / sayaç','Doğrulanmış örnek 50–83,33 L/dk')]),
                dict(id='side',label='Analiz yan kolu',nodes=[node('condenser','condenser','Yoğuşturucu','Gaz <20 °C, donma yok'),node('condensate','trap','Kondensat kabı','XAD-2’den önce'),node('adsorber','adsorber','XAD-2','Kartuş gaz hızı ≤34 cm/s','Bu ek örnekte ≥30 g'),node('dryer','trap','Kurutma kulesi','Yan kol gazı'),node('side_meter','meter','Yan kol pompa / sayaç','Doğrulanmış örnek 8,33–11,67 L/dk')])])
        else:p['train']=[node('nozzle','probe','Nozül / prob','Seçili ısıtmalı düzen'),node('filter','filter','Filtre','Çiy üstünde <125 °C'),node('condenser','condenser','Yoğuşturucu','Çıkış <20 °C'),node('condensate','trap','Kondensat kabı','Bubblerlerden önce'),imp(1,'Dietilen glikol/su 1:2 (hacim/hacim)','150 mL'),imp(2,'Dietilen glikol/su 1:2 (hacim/hacim)','150 mL'),node('dryer','trap','Kurutma kulesi','Kaynağın ekipman örneği'),meter]
