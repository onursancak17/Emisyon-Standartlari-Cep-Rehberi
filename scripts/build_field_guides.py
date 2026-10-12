#!/usr/bin/env python3
"""Editorial source for the offline field guide. Run from repository root."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
original = {}
for filename in ['standards.json', 'standards_extra.json', 'standards_overrides.json']:
    for item in json.loads((ASSETS / filename).read_text()):
        original[item['code']] = item

def node(label, value='', role='', kind='equipment', zone=''):
    return dict(label=label, value=value, role=role, kind=kind, zone=zone)

def imp(n, value, role, kind='water'):
    return node(f'İmpinger {n}', value, role, kind, 'Buz / su banyosu')

PROBE = node('Nozul + prob', 'Bacadan numune', 'Akışı ve fazları temsil eden numune alır.', 'probe')
FILTER = node('Filtre', 'Metoda uygun ortam', 'Partikül fazını tutar.', 'filter')
PUMP = node('Pompa', 'Kontrollü çekiş', 'Gazı tren boyunca çeker.', 'pump')
DGM = node('Kuru gaz sayacı', 'T ve P kaydı', 'Örneklenen kuru gaz hacmini ölçer.', 'meter')
SILICA = '200–300 g silika jel'

def train(name, nodes, source, note='', verified=True):
    return dict(title=name, nodes=nodes, source=source, note=note, verified=verified)

def point(title, text, kind='Saha uygulaması'):
    return dict(title=title, text=text, kind=kind)

def steps(*lines):
    return [point(*line) if isinstance(line, tuple) else point(line.split(' — ')[0], line.split(' — ', 1)[-1] if ' — ' in line else '') for line in lines]

EPA = 'https://www.epa.gov/emc/'
SOURCES = {
 '26a': ('EPA Method 26A · §6.1.6, §8', 'https://www.epa.gov/sites/default/files/2019-06/documents/method_26a.pdf'),
 '29': ('EPA Method 29 · §8.1.3 ve Şekil 29-1', 'https://www.epa.gov/sites/default/files/2017-08/documents/method_29.pdf'),
 '23': ('EPA Method 23 · 2023 · §8 ve Şekil 23-1', 'https://www.epa.gov/system/files/documents/2023-03/2023%20Method%2023%20Revision%20Final.pdf'),
 '323': ('EPA Method 323 · 2023 · §6.3, §8', 'https://www.epa.gov/system/files/documents/2023-06/Method%20323%202023%20revision.pdf'),
 '13a': ('EPA Method 13A · §6 ve §8', 'https://www.epa.gov/sites/default/files/2017-08/documents/method_13a.pdf'),
 '8': ('EPA Method 8 · §6.1.1.2 ve §8.3', 'https://www.epa.gov/sites/default/files/2017-08/documents/method_8.pdf'),
 '11': ('EPA Method 11 · §7.1 ve §8.1', 'https://www.epa.gov/sites/default/files/2017-08/documents/method_11.pdf'),
 '027': ('EPA CTM-027 · 1997 · §1–4', 'https://www.epa.gov/sites/default/files/2020-08/documents/ctm-027.pdf'),
 '207': ('SCAQMD Method 207.1 · 2006 · §2.2.1.3 ve §3.1', 'https://www.aqmd.gov/docs/default-source/laboratory-procedures/methods-procedures/stm-207-1.pdf'),
 '426': ('CARB Method 426 · §6.1.3', 'https://ww2.arb.ca.gov/sites/default/files/classic/testmeth/vol3/meth426.pdf'),
 '425': ('CARB Method 425 · 1997', 'https://ww2.arb.ca.gov/sites/default/files/classic/testmeth/vol3/m_425.pdf'),
 'nova': ('MRU NOVAplus · üretici kullanım kılavuzu', 'https://www.mru.eu/fileadmin/user_upload/files/bedienungsanleitungen-en/62851EN_USER_MANUAL_NOVAplus.pdf'),
 '1911': ('EN 1911:2010 · standart kuruluşu kapsam kaydı', 'https://www.evs.ee/en/evs-en-1911-2010'),
 '1948': ('EN 1948-1:2006 · standart kuruluşu kapsam kaydı', 'https://www.evs.ee/en/evs-en-1948-1-2006'),
 '11338': ('ISO 11338-1:2003 · ISO kapsam / metotlar', 'https://www.iso.org/standard/32903.html'),
 '4': ('EPA Method 4 · §8.1 referans yöntemi', 'https://www.epa.gov/sites/default/files/2017-08/documents/method_4_0.pdf'),
 '5': ('EPA Method 5 · 2020 · §8.3', 'https://www.epa.gov/sites/default/files/2019-08/documents/method_5_0.pdf'),
 '17': ('EPA Method 17 · baca içi filtre', EPA+'method-17-particulate-matter'),
 '1': ('EPA Method 1 · ölçüm yeri ve traverse', EPA+'method-1-sample-and-velocity-traverses-stationary-sources'),
 '2': ('EPA Method 2 · hız ve debi', EPA+'method-2-velocity-s-type-pitot'),
 '25a': ('EPA Method 25A · toplam gaz organikleri', EPA+'method-25a-total-gaseous-organic-concentration-using-flame-ionization-detector'),
}

BASE_PREP = steps(
 ('Ölçüm planını aç', 'Tesis, baca, parametre, seçilen metot ve sürümü ile prosesin hangi çalışma koşulunda ölçüleceğini kaydet.'),
 ('Numune kimliğini oluştur', 'Baca, ölçüm sırası, tarih ve fraksiyon kodlarını ölçüm başlamadan kaplara ve saha formuna yaz.'),
 ('Cihaz durumunu doğrula', 'Seri numarası, kalibrasyon, bakım, batarya ve kayıt kapasitesini kontrol et. Uygun olmayan cihazı ölçüme hazırlama.'),
)
BASE_REC = steps(
 ('Son kayıtları tamamla', 'Bitiş saatini, son hacmi ve ölçüm boyunca meydana gelen kesinti veya proses değişikliklerini yaz.'),
 ('Numuneyi kimliğiyle teslim et', 'Kap etiketi ile saha formunu eşleştir; alınan fraksiyonları ve saklama koşullarını teslim tutanağına geçir.'),
)
BASE_CHECK = steps(
 ('Temsil edicilik', 'Proses yükünü, ölçüm yerini ve kesinti kayıtlarını birlikte değerlendir. İşletme değişikliğini numune süresinden bağımsız düşünme.', 'Kritik kontrol'),
 ('Hacim ve birim', 'Sayaç şartı, baca şartı, kuru/yaş baz ve referans sıcaklık-basıncı birbirinden ayır. Konsantrasyonda kullanılan hacmin bazını yaz.', 'Kritik kontrol'),
)

guides=[]
def add(code, title, group, purpose, method, duration, flow, preparation, setup, sampling, recovery, checks, trains, sources=(), aliases=(), concepts=(), scope=''):
    old=original.get(code,{})
    guide=dict(id=f'g{len(guides)+1:02}', title=title, code=code, category=old.get('category','Emisyon'), group=group,
       purpose=purpose, method=method, duration=duration, flowRate=flow,
       equipment=old.get('equipment',[]), keywords=old.get('keywords',[]), aliases=list(aliases),
       preparation=BASE_PREP+preparation, setup=setup, sampling=sampling, recovery=recovery+BASE_REC,
       checks=checks+BASE_CHECK, trains=trains, concepts=list(concepts),
       sources=[dict(title=SOURCES[s][0],url=SOURCES[s][1]) for s in sources], sourceScope=scope,
       mistakes=old.get('mistakes',[]))
    guides.append(guide)
    return guide

ISO_SCOPE='Tam TS/EN/ISO metni bu güncellemede erişilebilir değildi. Şema yöntemin prensibini gösterir; çözelti miktarı, sıcaklık, süre ve kabul sınırları kullanılan standart sürümü ve onaylı laboratuvar talimatıyla doğrulanmalıdır.'

add('TS EN 15259 / EPA Method 1','Ölçüm düzlemi, port ve traverse','Hız ve debi',
 'Bacadan alınan numunenin akışı temsil etmesini sağlamak için uygun ölçüm kesitini ve noktaları belirlemek.',
 'Ölçüm öncesi geometrik ve akış uygunluğu değerlendirmesi. TS EN 15259 ile EPA Method 1 aynı mesafe/nokta tablosu değildir.',
 'Numune süresi değil, ölçüm yerinin ve nokta planının hazırlanması söz konusudur.', 'Numune çekişi yok; hız profili ilgili hız metoduyla belirlenir.',
 steps(('Kesiti ölç','Dairesel bacada iç çapı; dikdörtgende iki iç kenarı ve port derinliğini ölç. İzolasyon dış ölçüsünü iç çap yerine kullanma.'),('Bozucuları işaretle','Dirsek, fan, klape, genişleme ve daralmaların ölçüm düzlemine uzaklıklarını krokiye işle.')),
 steps(('Metot tablosunu seç','Dairesel/dikdörtgen kesit ve seçilen standarda ait nokta yerleşimini kullan.'),('Prob işaretlerini hazırla','Her port için iç duvardan itibaren ilerleme mesafelerini hesaplayıp prob üzerinde işaretle.')),
 steps(('Erişimi kontrol et','Platform, port çapı ve karşı duvara erişimin tüm noktaları ölçmeye izin verdiğini doğrula.'),('Akış uygunluğunu değerlendir','Girdap, ters akış ve yerel hız/sıcaklık dağılımını ilgili metotla değerlendir.'),('Nokta planını kaydet','Port sayısı, nokta sayısı, duvar referansı ve gerekçeyi saha formuna yaz.')),
 steps(('Krokiyi sakla','İç kesit, ölçüm düzlemi, bozucular ve port/nokta numaralarının tek çizimde bulunmasını sağla.')),
 steps(('Metot ayrımı','EPA mesafe çiftlerini TS şartı olarak sunma; uygun olmayan kesitte en az nokta sayısını tek başına yeterli kabul etme.','Kritik kontrol')),
 [train('Port / traverse planlama akışı',[node('Baca kesiti','İç çap / kenarlar'),node('Bozucu etkiler','Mesafe / akış'),node('Ölçüm düzlemi','Uygunluk'),node('Port ve noktalar','Metot tablosu'),node('Prob işaretleri','cm ile mesafe')],'TS EN 15259 / EPA Method 1','Kimyasal ve impinger kullanılmaz.',False)],('1',),scope=ISO_SCOPE)

add('EPA Method 2 / TS EN ISO 16911 / TS ISO 10780','Baca gazı hızı ve debisi','Hız ve debi',
 'Gaz hızını ve hacimsel debiyi belirlemek; kütlesel emisyon ve izokinetik örnekleme hesabına temel sağlamak.',
 'Pitot basınç farkı, sıcaklık, mutlak basınç ve gaz yoğunluğu birlikte değerlendirilir.',
 'Her noktada kararlı okuma alınır; toplam süre kesit planına ve akış dalgalanmasına bağlıdır.', 'Gaz emişi gerekmez. Hacimsel debi Q = ortalama hız × iç kesit alanı; baz dönüşümü ayrı yapılır.',
 steps(('Pitot katsayısını kontrol et','Kullanılan Pitot tipi ve kalibrasyon katsayısını cihaz kaydından al.'),('Basınç ve gaz bilgilerini hazırla','Barometrik/statik basınç, sıcaklık, nem ve molekül ağırlığı için gerekli yardımcı ölçümleri planla.')),
 steps(('Basınç hatlarını bağla','Pitot yüksek/düşük basınç uçlarını doğru girişlere bağla; hortumda su ve tıkanma bulunmadığını kontrol et.'),('Sıfır ve sızdırmazlık','Manometrenin sıfırını ve Pitot hatlarının kaçaksız olduğunu doğrula.')),
 steps(('Noktaya yerleş','Probu işaretli derinliğe getir; Pitot yönünü akışa göre ayarla.'),('Kararlı değerleri yaz','Her noktada ΔP ve sıcaklığı kaydet; ters akış/kararsızlığı işaretle.'),('Kesiti tamamla','Bütün noktalara aynı planla ilerle; eksik noktayı sessizce atlama.'),('Hızı ve debiyi hesapla','Nokta hızlarını uygun yoğunluk ve Pitot katsayısıyla hesapla; alan ağırlığını metoda göre uygula.')),
 steps(('Sıfırı yeniden kontrol et','Son sıfır ve hat kontrolünü kaydet.')),
 steps(('Düşük hız','Küçük ΔP değerinde ölçüm çözünürlüğü ve belirsizliğin yeterli olduğunu doğrula; 4 m/s tek başına evrensel kabul/ret sınırı değildir.','Kritik kontrol')),
 [train('Hız ölçüm bağlantısı',[node('Baca noktası','Akış / sıcaklık'),node('S-tip Pitot','Yüksek ve düşük basınç'),node('ΔP ölçer','Pa / mmSS'),node('Hesap','Yoğunluk + alan'),node('Sonuç','m/s ve m³/h')],'Seçilen hız metodu','İmpinger kullanılmaz.',False)],('2',),scope=ISO_SCOPE)

PM_PREP=steps(('Filtreyi tanımla','Metoda uygun filtreyi laboratuvarda koşullandırılmış ve tartım kaydıyla hazırla; kimliğini pensle işlem öncesi eşleştir.'),('Nozulu planla','Ön hız, nem ve sıcaklıktan izokinetik çekişi planla; hedef kuru hacim ile sayaç hacmini ayır.'))
PM_SETUP=steps(('Treni kur','Nozul, prob, filtre ve hacim ölçüm sistemini şemaya göre bağla; contanın filtreyi baypas ettirmediğini kontrol et.'),('Isıtma ve soğutmayı hazırla','Seçilen metodun filtre/prob sıcaklığını uygula; nem tutucuyu hazırla.'),('Ön kaçak testi','Metoda ait vakum ve kaçak sınırıyla testi yap; sonucu kaydet.'))
PM_SAMPLE=steps(('Başlangıcı kaydet','Sayaç ilk değeri, sıcaklık, basınç, saat ve filtre/nozul kimliğini yaz.'),('İzokinetik çekişi ayarla','Nozul giriş hızını baca gazı hızına eşleştir; yeni noktada değişen koşullara göre debiyi yeniden ayarla.'),('Noktaları sırayla tamamla','Planlanan süreyi her travers noktasında uygula; ΔP, çekiş, vakum, sayaç T/P ve ısıtma değerlerini kaydet.'),('Sorun halinde kayıt tut','Filtre tıkanması, kaçak veya kesintide zamanı ve ilgili hacmi yaz; parçayı değiştirirken metot prosedürünü uygula.'),('Ölçümü kapat','Son hacmi/saatini yaz ve son kaçak testini gerçekleştir.'))
PM_REC=steps(('Filtreyi al','Numune yüzeyine dokunmadan filtreyi kimlikli petri/kap içine al.'),('Ön fraksiyonu geri kazan','Nozul, prob ve filtre önü birikimini seçilen metodun yıkama sıvısıyla ayrı, etiketli kaba al.'),('Nem bölümünü değerlendir','Toplanan su ve silika jel artışını kaydet; nem fraksiyonunu otomatik olarak partikül kütlesine ekleme.'))
PM_CHECK=steps(('Geçerlilik','Kaçak, izokinetiklik, sıcaklık ve blank şartlarını birlikte kontrol et. Evrensel bir süre/hacim tüm toz metotlarına uygulanmaz.','Kritik kontrol'),('Hesap','C = metotla belirlenen partikül kütlesi / aynı referans bazındaki numune hacmi. mg ve g dönüşümünü kontrol et.','Açıklama'))
for code,title,location,source in [
 ('EPA Method 5','Partikül madde · dış filtre','Baca dışı ısıtmalı filtre','5'),
 ('EPA Method 17','Partikül madde · baca içi filtre','Nozulun ardından baca içi filtre','17'),
 ('TS EN 13284-1','Düşük derişimli partikül madde','Onaylı filtre konumu ve sıcaklığı','5'),
 ('TS ISO 9096','Yüksek derişimli partikül madde','Onaylı filtre / ön ayırıcı konfigürasyonu','5'),
 ('ISO 12141','Düşük toz · elle gravimetrik ölçüm','Seçilen ISO konfigürasyonu','5')]:
    aliases={'EPA Method 5':['EPA Method 5 / EPA Method 17'],'TS EN 13284-1':['TS EN 13284-1 / TS ISO 9096 / ISO 12141'],'ISO 12141':['TS ISO 12141']}.get(code,[])
    front=[PROBE,node('Filtre',location,'Partikül fazını toplar.','filter')]
    if code=='EPA Method 17': front=[node('Nozul + filtre','Baca içinde','Yerinde partikül tutma.','filter'),node('Prob','Filtre arkasında','Gazı nem bölümüne taşır.','probe')]
    add(code,title,'Partikül madde','Partikül kütlesini numune hacmine oranlayarak baca toz derişimini belirlemek.',
      'İzokinetik örnekleme ve gravimetrik tayin. '+location+'.','Süre ve hacim, tayin limiti ile ölçüm planına göre seçilir.','Sabit 20 L/dk zorunluluğu yok; çekiş izokinetik hesapla belirlenir.',
      PM_PREP,PM_SETUP,PM_SAMPLE,PM_REC,PM_CHECK,
      [train(code+' · işlevsel düzenek',front+[node('Nem tutucu','Metoda göre su / boş şişe','Sayaç öncesi nemi tutar.','water','Soğutma'),node('Kurutucu','Tartımı bilinen silika jel','Kalan nemi tutar.','silica'),PUMP,DGM],code,'Nem şişelerinin miktarları ve sıcaklıklar seçilen metotla belirlenir.',False)],(source,),aliases,scope=ISO_SCOPE if not code.startswith('EPA') else 'Şema işlevsel akışı gösterir; Method 5 ve Method 17 filtre yerleşimleri ayrıdır. Sayısal kabul şartları seçilen resmi metinden uygulanır.')

add('EPA Method 4','Baca gazında nem tayini','Hız ve debi',
 'Su buharı oranını belirlemek; kuru/yaş baz dönüşümü ve izokinetik örnekleme hesabını doğru yapmak.',
 'Gazdaki su yoğunlaştırılır; kalan nem silika jelde tutulur. Toplanan su, kuru gaz hacmiyle birlikte hesaplanır.',
 'Referans yöntem hedefi en az 0,60 standart m³’tür; süre debiye göre hesaplanır. 30 dakika saha planı olabilir, tek başına evrensel metot süresi değildir.',
 'Yaklaşık 21 L/dk üst sınırı referans yönteme aittir; kaynak koşuluna göre daha düşük çekiş seçilebilir.',
 steps(('Tartımları hazırla','İmpingerler, başlangıç suyu ve silika jel için ilk tartım/hacim kayıtlarını hazırla.'),('Damla taşınmasını değerlendir','Doygun/damlacıklı bacada su buharı ile sürüklenen sıvının ayrımını değerlendirmek için yöntemin ilgili prosedürünü kullan.')),
 steps(('Şişeleri bağla','Su, su, boş şişe ve silika jel sırasını koru; soğutma banyosunu hazırla.'),('Kaçak ve sıcaklık','Ön kaçak testi yap ve probda kontrolsüz yoğuşmayı önle.')),
 steps(('Sayaç ilk değerini yaz','İlk kuru gaz hacmi, T/P ve saati kaydet.'),('Çekişi başlat','Şişelerde sıçrama olmadan planlanan çekişi uygula; banyo ve çıkış sıcaklığını izle.'),('Hedefi tamamla','Süre ve hacmi birlikte takip et; birini sağlayıp diğerini ihmal etme.'),('Son testi yap','Bitişte sayaç ve kaçak kayıtlarını tamamla.')),
 steps(('Toplanan suyu ölç','İmpinger artışını ve silika jel kütle artışını ölç; dış yüzeydeki suyu tartıma katma.'),('Nem oranını hesapla','Su buharı eşdeğer hacmini kuru gaz hacmiyle aynı sıcaklık/basınç bazında değerlendir.')),
 steps(('Yaş/kuru hacim','Silika jel sonrası sayaç kuru gazı ölçer. Bu kuru hacimden tekrar nem düşümü yapma.','Kritik kontrol')),
 [train('EPA Method 4 · referans düzenek',[node('Isıtmalı prob','Yoğuşmayı önle','Numuneyi taşır.','probe'),imp(1,'100 mL saf su','Yoğunlaşan suyu toplar.'),imp(2,'100 mL saf su','İkinci yoğunlaştırma.'),imp(3,'Başlangıçta boş','Sıvı sürüklenmesini azaltır.','empty'),imp(4,SILICA,'Kalan nemi tutar.','silica'),PUMP,DGM],'EPA Method 4','İmpinger tipleri, çıkış sıcaklığı ve kabul sınırları resmi metinle eşleştirilir.',False)],('4',))

T90=[point('T90 ne demektir?','Gaz derişimi basamak biçiminde değiştiğinde cihazın toplam gösterge değişiminin %90’ına ulaşması için geçen süredir. Başlangıç sıfır olmak zorunda değildir.','Kavram'),
 point('Basit örnek','Okuma 20 ppm’den 120 ppm’e değişecekse toplam değişim 100 ppm’dir. %90 noktası 20 + 0,90 × 100 = 110 ppm olur. 110 ppm’e ulaşma süresi T90’dır.','Örnek'),
 point('Sensör ve bütün sistem farklıdır','Üretici sensör T90’ı; prob, uzun hortum, filtre, soğutucu ve pompa dahil sistem cevabıyla aynı olmayabilir. Gazın hattı doldurması ayrıca gecikme yaratır.','Kritik kontrol'),
 point('Her gazın cevabı ayrı','O₂, CO, SO₂, NO ve NO₂ için sensör tipi ve şartlandırma farklı cevap oluşturabilir. Tek sensörün süresini bütün kanallara uygulama.','Açıklama'),
 point('T90 bir ölçüm süresi değildir','T90 kadar beklemek otomatik olarak tam kararlılık veya metodun ortalama alma süresi demek değildir. Kayıt başlangıcında bütün sistem cevabı ve kararlılık kontrol edilir.','Kritik kontrol'),
 point('Beklemeyi nasıl değerlendirirsin?','Doğrulama gazını mümkün olduğunda prob girişinden vererek bütün hattın cevabını izle. Gaz değişiminin saatini ve ilgili kanalların %90 noktalarına ulaştığı zamanı kaydet. Gaz doğrulamasını üretici/metot prosedürüyle yap.','Saha uygulaması'),
 point('Nokta değiştiğinde','Hattaki eski gazın etkisini ve yeni noktanın kararlılığını yeniden değerlendir. Önceki noktanın okumasını yeni noktanın sonucu olarak kaydetme.','Saha uygulaması')]
gas=add('TS ISO 12039 / TS EN 14789 / TS EN 14792 / TS EN 15058','Yanma gazları · O₂, CO, CO₂, NOₓ, SO₂','Yanma gazları',
 'Yanma kalitesini, kirletici derişimlerini ve gerektiğinde referans oksijene düzeltilmiş sonuçları belirlemek.',
 'Analizörle sürekli numune çekişi. Her parametre için ilgili referans yöntemin kapsamı ve cihazın ölçüm tekniği ayrı kontrol edilir. NOₓ için NO₂ ölçümü/konvertörü veya izinli hesap yaklaşımı belirtilir.',
 'Sistem cevap süresi ve kararlılık beklenir; ardından ilgili metot ve mevzuata göre temsil edici kayıt periyodu uygulanır.',
 'Analizörün onaylı pompa debisi kullanılır. Hortum hacmi ve filtre/soğutucu yükü sistem cevabını etkiler.',
 steps(('Gaz kanallarını doğrula','Cihazın gerçek sensörlerini, aralıklarını ve doğrudan ölçülen / hesaplanan değerleri kaydet. Yakıttan hesaplanan CO₂ ile doğrudan ölçülen CO₂’yi ayır.'),('T90 bilgisini hazırla','Her sensörün üretici cevabını ve mümkünse bütün hat için ölçülmüş sistem cevabını incele.'),('Sıfır/span gazlarını hazırla','Sertifikalı gaz, derişim, geçerlilik tarihi ve regülatör uygunluğunu kontrol et. Temiz hava, her gaz için her metodun sıfır gazının yerine geçmez.')),
 steps(('Prob ve hattı seç','Gaz bileşenlerine uygun malzeme ve şartlandırma kullan; suda çözünen gaz kayıplarını dikkate al.'),('Sistemi sızdırmaz kur','Prob, filtre, hat ve analizör bağlantılarını kontrol et.'),('Cihazı hazırla','Isınma ve üreticinin sıfır prosedürünü tamamla; ön doğrulamayı aynı ölçüm düzeniyle uygula.')),
 steps(('Probu yerleştir','Temsil edici noktaya yerleş; porttan seyrelme yaratacak hava girişini önle.'),('Eski gazın çıkmasını bekle','Hattın yeni gazla dolmasını izle; yalnız sensör T90 sayısına bakarak hemen kayıt başlatma.'),('Bütün kanalları izle','O₂, CO ve diğer kanalların eğilimini, akışı ve cihaz uyarılarını kontrol et.','Kritik kontrol'),('Kararlılık kararını kaydet','Metodun kararlılık/cevap kriteri ve ölçülen sistem cevabı sağlandığında kayıt başlangıcını yaz.'),('Ölçüm periyodunu tamamla','Ham değerleri ve proses yükünü aynı zaman çizelgesinde kaydet; aşım ve aralık dışı okumaları işaretle.'),('Nokta veya baca değiştir','Yeni gaz koşulları için bekleme/kararlılık kontrolünü yeniden uygula.'),('Son doğrulamayı yap','Sıfır/span sürüklenmesini kontrol et; cihazı üretici talimatıyla temiz gazla temizle.')),
 steps(('Veriyi bazına göre ayır','Ham ppm, ölçülen O₂, kuru/yaş baz, referans O₂ ve düzeltme hesabını ayrı sakla.'),('Hattı kontrol et','Kondensat ve filtre durumunu bakım kaydına yaz; numune birikimini prosedüre göre temizle.')),
 steps(('Oksijen düzeltmesi','Aynı kuru bazdaki Cref = Cölç × (21 − O₂ref)/(21 − O₂ölç). Referans O₂’yi yakıt menüsünden değil, uygulanacak düzenlemeden doğrula.','Hesap'),('ppm dönüşümü','mg/m³ dönüşümü molekül ağırlığı ve referans sıcaklık/basınca bağlıdır. EPA standart hacmi otomatik olarak 0 °C normal hacim değildir.','Kritik kontrol')),
 [train('Yanma gazı analiz bağlantısı',[node('Prob','Baca noktası','Temsil edici gazı alır.','probe'),node('Filtre / hat','Uygun sıcaklık','Partikül ve yoğuşma kontrolü.','filter'),node('Şartlandırma','Gaz uyumluluğu','Nem yönetimi; çözünen gaz kaybı kontrolü.','cooler'),node('Analizör pompası','Onaylı debi','Numuneyi taşır.','pump'),node('Sensörler','O₂ / CO / NOₓ…','Gaz kanallarını ölçer.','meter')],'Seçilen gaz metodu + cihaz kılavuzu','Bu cihazlı ölçümde kimyasal impinger zorunlu değildir.',False)],('nova',),aliases=['TS ISO 12039 / TS ISO 7935 / EPA CTM-022','TS ISO 12039'],concepts=T90,scope=ISO_SCOPE)

CHEM_PREP=steps(('Absorbanı doğrula','Şemadaki kimyasal, derişim, başlangıç miktarı ve reaktif lotunu etiketlerle eşleştir. Laboratuvarda hazırlanmış onaylı reaktifi kullan.'),('Blankları hazırla','Metodun reaktif ve saha blanklarını ayrı kaplarla hazırla; numuneyle aynı malzeme ve taşıma koşullarını uygula.'))
CHEM_SETUP=steps(('Akış yönünü kontrol et','Numune girişini şişenin dalma borusuna bağla; gazın sıvıdan geçmesini sağla. Ters bağlantı taşmaya ve eksik tutulmaya yol açar.'),('Soğutmayı hazırla','Şişeleri dik ve güvenli yerleştir; tanımlı buz/su banyosunu ve çıkış sıcaklık ölçümünü hazırla.'),('Sızdırmazlığı doğrula','Metodun kaçak prosedürünü uygula; çatlak cam, contalar ve bağlantıları kontrol et.'))
CHEM_SAMPLE=steps(('İlk değerleri yaz','Saat, DGM ilk hacim, sayaç T/P, reaktif miktarları ve gerekli ilk tartımları kaydet.'),('Çekişi uygula','Seçilen metoda ait sabit akış veya izokinetik çekişi başlat.'),('Treni izle','Debi, vakum, sıcaklık, kabarcıklanma, köpürme, taşma ve tutma kapasitesini düzenli kontrol et.'),('Değişikliği kaydet','Kesinti ve parça değişiminde saat/hacmi yaz; gerekli kaçak kontrollerini tekrarla.'),('Ölçümü bitir','Son hacim/süreyi ve metodun son kaçak kontrolünü tamamla.'))
CHEM_REC=steps(('Son miktarları belirle','Geri almadan önce sıvı hacmi veya tartımı kaydet; başlangıç ve son miktarı karıştırma.'),('Fraksiyonları ayır','Metot birleştirmeyi açıkça istemedikçe farklı kimyasal fraksiyonları aynı kaba dökme.'),('Yüzeyleri geri kazan','Numuneyle temas eden parçaları yalnız ilgili metodun yıkama sıvısıyla yıka; yıkama fraksiyonunun kimliğini yaz.'),('Kapları koru','Metoda uygun kap, pH, sıcaklık ve analiz süresini laboratuvar teslim planıyla uygula.'))
CHEM_CHECK=steps(('Tutma verimi','Arka şişede yakalanan miktarı ve absorban kapasitesini metot kriteriyle değerlendir. Son şişenin bulunması tek başına verim kanıtı değildir.','Kritik kontrol'))

add('TS EN 1911','Gaz halindeki klorürler · HCl','Halojen ve asit gazları',
 'Gaz halindeki klorürleri HCl olarak ifade ederek belirlemek.', 'Filtre sonrası gaz halindeki klorürlerin uygun suda absorpsiyonu; analiz tekniği seçilen standardın izin verdiği prosedüre bağlıdır.',
 'Süre, yeterli numune ve tayin limiti hedefiyle planlanır; güncel metot sürümü kontrol edilir.', 'Absorpsiyon debisi ve gerekirse yan akım, kullanılan düzeneğin verimiyle doğrulanır.',
 CHEM_PREP+steps(('HCl / Cl₂ ayrımı','Bu ölçümün kapsamı gaz halindeki klorürdür. Moleküler klor ve HF için aynı şema otomatik uygulanmaz.')),
 CHEM_SETUP,CHEM_SAMPLE,CHEM_REC,CHEM_CHECK,
 [train('EN 1911 · suyla absorpsiyon prensibi',[PROBE,FILTER,imp(1,'Klorür blankı uygun saf su\nMiktar: onaylı talimat','HCl tutulması.'),imp(2,'Aynı saflıkta su\nMiktar: onaylı talimat','Verim kontrolü; ayrı analiz.'),node('Kurutucu / koruma','Onaylı konfigürasyon'),PUMP,DGM],'EN 1911 · prensip şeması','Şişe sayısı, hacim ve yan akım seçimi onaylı metot konfigürasyonuna bağlıdır.',False)],('1911',),scope=ISO_SCOPE)

add('EPA Method 26A','HCl, HF ve gaz halindeki halojenler','Halojen ve asit gazları',
 'Hidrojen halidleri ve halojenleri farklı absorban fraksiyonlarında toplamak.', 'İzokinetik örnekleme. Asit ve alkali fraksiyonlar ayrı tutulur; HF ölçümü moleküler F₂ ölçümü anlamına gelmez.',
 'Temsil edici nokta süresi ve toplam hedef hacim planlanır.', 'İzokinetik çekiş; absorban kapasitesi korunur.',CHEM_PREP,
 CHEM_SETUP,CHEM_SAMPLE,CHEM_REC+steps(('Asit / alkali kaplarını ayır','Asit toplama ve alkali toplama fraksiyonlarını kendi metot yıkamalarıyla ayrı kaplara al.')),
 CHEM_CHECK+steps(('Prob ve filtre sıcaklığı','Method 26A’da 120–134 °C veya kaynak için izinli farklı sıcaklık uygulanır.','Metot şartı')),
 [train('EPA Method 26A · yüksek nem seçeneği',[PROBE,FILTER,imp('K','50 mL 0,1 N H₂SO₄\nİsteğe bağlı','Yüksek nem için kondens kapanı.','acid'),imp(1,'100 mL 0,1 N H₂SO₄','Asit fraksiyonu.','acid'),imp(2,'100 mL 0,1 N H₂SO₄','Asit fraksiyonu devamı.','acid'),imp(3,'100 mL 0,1 N NaOH','Alkali fraksiyonu.','alkali'),imp(4,'100 mL 0,1 N NaOH','Alkali fraksiyonu devamı.','alkali'),imp(5,'Tartımı bilinen silika jel','Artık nem.','silica'),PUMP,DGM],'EPA Method 26A §6.1.6','K şişesi opsiyoneldir; çıkarılırsa diğer şişelerin görevi/sırası korunur.')],('26a',))

add('EPA Method 13A','Toplam florür · gaz + partikül','Halojen ve asit gazları',
 'Gaz ve partikül fazındaki toplam florürü belirlemek. Yalnız HF analizinden kapsamı farklıdır.', 'İzokinetik çekiş; su ve filtrede tutma. Temel konfigürasyonda filtre üçüncü ile dördüncü impinger arasındadır.',
 'Süre yeterli kütle/hacim ve nokta planına göre belirlenir.', 'İzokinetik çekiş 28 L/dk altında yürütülür.',CHEM_PREP+steps(('Filtre blankı','Florür blankı düşük ve metoda uygun filtreyi seç; cam elyaf filtreyi otomatik uygun kabul etme.')),
 CHEM_SETUP,CHEM_SAMPLE,CHEM_REC,CHEM_CHECK,
 [train('EPA Method 13A · temel filtre konumu',[PROBE,imp(1,'100 mL uygun saf su','Florür toplama.'),imp(2,'100 mL uygun saf su','Florür toplama.'),imp(3,'Başlangıçta boş','Sıvı sürüklenmesi kontrolü.','empty'),node('Filtre','3 ve 4 arasında','Temel konfigürasyon.','filter'),imp(4,SILICA,'Kalan nem.','silica'),PUMP,DGM],'EPA Method 13A §6, §8; Method 5 su/nem dizisi','Filtrenin prob sonrasına alınabildiği alternatif için resmi destek/ısıtma şartları ayrıca kontrol edilir.')],('13a','5'))

metals=[PROBE,FILTER,imp(1,'Başlangıçta boş','Nem kapanı; koşula bağlı çıkarılabilir.','empty'),imp(2,'100 mL %5 HNO₃ / %10 H₂O₂','Metal toplama.','acid'),imp(3,'100 mL %5 HNO₃ / %10 H₂O₂','Metal toplama devamı.','acid'),imp(4,'Başlangıçta boş','Cıva hattı öncesi koruma.','empty'),imp(5,'100 mL asidik KMnO₄','Cıva toplama.','purple'),imp(6,'100 mL asidik KMnO₄','Cıva toplama devamı.','purple'),imp(7,SILICA,'Nem tutma.','silica'),PUMP,DGM]
add('EPA Method 29','Metaller ve cıva · EPA 29','Metaller',
 'Partikül ve gaz fazındaki metalleri; gerektiğinde cıvayı da belirlemek.', 'İzokinetik filtre + asidik toplama; cıva için ayrı permanganat fraksiyonu.',
 'Hedef tayin limiti, proses ve nokta planına göre süre/hacim belirlenir.', 'İzokinetik çekiş; metal kontaminasyonu düşük malzeme.',CHEM_PREP+steps(('Metal listesini kesinleştir','Hg dahil olup olmadığını laboratuvarla belirle; bu seçim impinger konfigürasyonunu değiştirir.')),
 CHEM_SETUP,CHEM_SAMPLE,CHEM_REC+steps(('Cıva fraksiyonlarını ayrı al','Permanganat ve ilgili yıkamaları metal asit fraksiyonuyla birleştirme; metot kap kodlarını kullan.')),
 CHEM_CHECK+steps(('Cıva seçeneği','Hg analiz edilmiyorsa 4–6. şişeler gerekmez. İlk boş şişenin çıkarılması ise metottaki nem koşuluna bağlıdır.','Metot şartı')),
 [train('EPA Method 29 · cıva dahil',metals,'EPA Method 29 §8.1.3','Asidik KMnO₄: %4 (kütle/hacim) KMnO₄ + %10 (hacim/hacim) H₂SO₄. Cıva fraksiyonu ayrı tutulur.')],('29',))

add('TS EN 14385','Cıva dışındaki metaller · EN 14385','Metaller',
 'Sb, As, Cd, Cr, Co, Cu, Pb, Mn, Ni, Tl ve V gibi hedef metallerin numunesini almak.', 'İzokinetik filtre ve onaylı asidik absorpsiyon treni. Cıva için EPA 29 hattı bu standardın eşdeğeri değildir.',
 'Süre ve hacim, metal bazında tayin limiti ile planlanır.', 'İzokinetik çekiş.',CHEM_PREP+steps(('Malzemeyi kontrol et','Metal kontaminasyonu düşük cam/kuvars/PTFE ve laboratuvarın temizlediği kapları kullan.')),
 CHEM_SETUP,CHEM_SAMPLE,CHEM_REC,CHEM_CHECK,
 [train('EN 14385 · metal toplama prensibi',[PROBE,FILTER,node('Absorpsiyon kademeleri','Onaylı HNO₃/H₂O₂\nSayı ve miktar: talimat','Hedef metal yakalama ve verim kontrolü.','acid','Soğutma'),node('Boş kapan','Konfigürasyona bağlı'),node('Kurutucu','Tartımı bilinen silika jel','Artık nem.','silica'),PUMP,DGM],'EN 14385 · prensip şeması','EPA 29’a ait şişe sayıları EN 14385 şartı olarak kullanılmaz.',False)],scope=ISO_SCOPE)

organic_prep=steps(('Laboratuvar hazırlığını doğrula','Temiz filtre, adsorban, cam malzeme ve gerekiyorsa ön örnekleme standartlarını teslim kayıtlarıyla kontrol et.'),('Fraksiyon planını hazırla','Filtre, prob yıkaması, adsorban ve kondensat kaplarını ölçüm öncesinde ayrı etiketle.'),('Kontaminasyonu önle','Açık bağlantıları kurulum anına kadar kapalı tut; adsorbanı ışık ve ısıdan koru.'))
organic_setup=steps(('Varyantı seç','Filtre/soğutucu/adsorban sırasını seçilen metot varyantıyla eşleştir.'),('Isıtmayı ve soğutmayı başlat','Filtre, prob ve adsorban sıcaklığını kendi sensörlerinden izle; yalnız banyo sıcaklığını yeterli kabul etme.'),('Kaçak kontrolünü yap','Bütün numune hattında ön kaçak testini kaydet.'))
organic_sample=steps(('İlk kayıtları yaz','Saat, hacim, sayaç T/P, filtre/adsorban kimliği ve sıcaklıkları kaydet.'),('İzokinetik örnekle','Nokta değişimlerinde çekişi güncelle; zaman ve toplam hacmi birlikte takip et.'),('Adsorbanı koru','Soğutma, akış, kondensat ve reçine sıcaklığını izle; sapmayı süresiyle kaydet.'),('Proses çevrimini temsil et','Kesintileri ve yük değişimini işaretle; numune sonlandırmayı yalnız saat dolmasına bağlama.'),('Son kaçak testini yap','Bitiş hacim ve saatini kaydet; treni numune kaybı yaratmadan kapat.'))
organic_rec=steps(('Filtre ve adsorbanı ayrı al','Numune yüzeyine dokunma; bütün kap ve kartuş kimliklerini eşleştir.'),('Kondensatı kaybetme','Soğutucu, kap ve bağlantılardaki kondensatı seçilen metot fraksiyonuna al.'),('Metoda uygun yıkama yap','Yıkama çözücüsünü ve birleşecek fraksiyonu laboratuvar talimatından kontrol et; fraksiyonları gelişigüzel birleştirme.'),('Işık ve sıcaklıktan koru','Saklama sıcaklığı ve analiz süresini seçilen metot/laboratuvar planıyla uygula. Numuneyi sahada keyfi olarak etüvde kurutma.'))
organic_check=steps(('İç standart / blank','Gerekli standart geri kazanımı ve blank uygunluğu laboratuvarla değerlendirilmeden sonucu geçerli sayma.','Kritik kontrol'),('Sonuç kapsamı','PAH kütlesi, PCDD/F kütlesi ve TEQ hesabı farklıdır; analit listesi ile eşdeğerlik faktörü sistemini belirt.','Açıklama'))

add('TS ISO 11338 / ilgili PAH saha uygulamaları','PAH · gaz ve partikül faz','Organik bileşikler',
 'Polisiklik aromatik hidrokarbonların gaz ve partikül fazlarını temsil eden numune almak.', 'ISO 11338-1’de A: seyreltme, B: filtre/soğutucu/adsorban, C: soğutulmuş prob/adsorban yöntemleri ayrıdır. Burada B prensibi gösterilir.',
 'Süre ve hacim, PAH analit listesi ve tayin limiti hedefiyle planlanır; tek sabit değer bütün varyantlara uygulanmaz.', 'İzokinetik çekiş ve adsorbanın kapasite/akış şartları birlikte kontrol edilir.',
 organic_prep,organic_setup,organic_sample,organic_rec,organic_check,
 [train('ISO 11338-1 · B yöntemi prensibi',[PROBE,node('Isıtmalı filtre','Metot sıcaklığı','Partikül fazı.','filter'),node('Soğutucu','Onaylı çıkış sıcaklığı','Gazı soğutur.','cooler'),node('Adsorban','Temizlenmiş uygun reçine','Gaz fazı.','resin'),node('Kondensat / nem treni','Varyanta göre kaplar','Şişe sayısı ve su miktarı: onaylı talimat.','water'),PUMP,DGM],'ISO 11338-1 · B yöntemi','EPA Method 23’ün 5 şişeli dizisi ISO B’nin evrensel zorunluluğu değildir.',False)],('11338',),aliases=['TS ISO 11338-1'],scope=ISO_SCOPE)

add('TS EN 1948-1','Dioksin / furan · PCDD/F','Organik bileşikler',
 'PCDD/F bileşiklerini gaz ve partikül fazlarını kaybetmeden toplamak; analiz ve TEQ değerlendirmesine uygun numune sağlamak.', 'EN 1948-1’de filtre/soğutucu, seyreltme ve soğutulmuş prob yaklaşımları birbirinden ayrılır. Gösterilen EN şeması filtre/soğutucu prensibidir.',
 'Süre, izin/mevzuat, proses ve hedef tayin limitiyle belirlenir. Her yönteme otomatik 6–8 saat kuralı taşınmaz.', 'İzokinetik örnekleme ve seçilen adsorban/soğutma koşulları.',
 organic_prep,organic_setup,organic_sample,organic_rec,organic_check,
 [train('EN 1948-1 · filtre / soğutucu prensibi',[PROBE,node('Filtre','Onaylı metot sıcaklığı','Partikül fazı.','filter'),node('Soğutucu','Kontrollü soğutma','Gaz fazını soğutur.','cooler'),node('Adsorban / impinger','Seçilen EN varyantı','Gaz fazı toplama.','resin'),node('Kondensat ve nem koruması','Varyanta ait sıra / miktar','Onaylı talimatla belirlenir.','water'),PUMP,DGM],'EN 1948-1 · prensip şeması','Bu EN prensip şemasıdır. Aşağıdaki EPA 23 çizimi ayrı bir metottur.',False)],('1948',),scope=ISO_SCOPE)

add('EPA Method 23','Dioksin, furan ve hedef organikler · EPA 23','Organik bileşikler',
 'Method 23 kapsamındaki PCDD/F, PCB ve PAH analitlerini seçilen analiz planına göre toplamak.', 'Filtre, soğutucu, XAD-2 ve beş impinger içeren izokinetik düzenek. EN 1948-1 ile aynı standart değildir.',
 'Aksi belirtilmedikçe nokta başına en az 2 dakika; metotta en az 2,5 kuru standart m³ önerilir.', 'İzokinetik çekiş; filtre çıkışı 120 ±14 °C veya izinli kaynak şartı. XAD-2 giriş gazı ilgili metot şartıyla kontrol edilir.',
 organic_prep,organic_setup,organic_sample,organic_rec,organic_check+steps(('XAD-2 sıcaklığı','Reçine 50 °C’yi hiçbir zaman aşmamalıdır. Bu üst sınır işletme hedef sıcaklığı anlamına gelmez.','Metot şartı')),
 [train('EPA Method 23 · 2023 treni',[PROBE,node('Isıtmalı filtre','120 ±14 °C','Partikül fazı.','filter','Isıtma'),node('Soğutucu','Dolaşımlı soğutma','Adsorban öncesi gaz soğutma.','cooler'),node('XAD-2 modülü','Dikey / ışıktan korunmuş','Gaz fazını tutar.','resin'),imp(1,'Başlangıçta boş','Kondensat toplama.','empty'),imp(2,'Yaklaşık 100 mL su','Nem toplama.'),imp(3,'Yaklaşık 100 mL su','Nem toplama.'),imp(4,'Başlangıçta boş','Sürüklenme kontrolü.','empty'),imp(5,'Yaklaşık 200 g veya daha çok\nsilika jel','Artık nem.','silica'),PUMP,DGM],'EPA Method 23 · 2023 §8.1.3','Şişe dizisi EPA 23’e aittir; EN 1948 için kendiliğinden zorunlu değildir.')],('23',))

add('CARB Method 426','Siyanür / HCN','Özel parametreler',
 'Metot kapsamındaki gaz ve aerosol siyanürü toplamak.', 'İzokinetik filtre ve alkali absorpsiyon; HCN kaybını önleyen koruma koşulları.',
 'Süre, kesit planı ve laboratuvarın hacim/kütle hedefiyle belirlenir.', 'İzokinetik çekiş. Numune çözeltisi hacmi ile örneklenen gaz hacmi farklıdır.',
 CHEM_PREP,CHEM_SETUP,CHEM_SAMPLE,CHEM_REC+steps(('Alkali korumayı sürdür','pH ve oksitleyici/girişim kontrolünü CARB prosedürüne göre yap; numuneyi asitleştirme.')),
 CHEM_CHECK+steps(('Reaktif güvenliği','Siyanürlü çözeltinin asitle teması HCN açığa çıkarabilir; geri alma işlemini laboratuvarın güvenli prosedürüyle yürüt.','Kritik kontrol')),
 [train('CARB Method 426 · temel tren',[PROBE,FILTER,imp(1,'100 mL 0,1 N NaOH','Alkali siyanür tutma.','alkali'),imp(2,'100 mL 0,1 N NaOH','İkinci tutma.','alkali'),imp(3,'Başlangıçta boş','Sürüklenme kontrolü.','empty'),imp(4,SILICA,'Artık nem.','silica'),PUMP,DGM],'CARB Method 426 §6.1.3','Yüksek CO₂ kaynaklarındaki metot alternatifi ayrıca laboratuvarla değerlendirilir.')],('426',))

add('CARB Method 425','Krom(VI) ve toplam krom','Metaller',
 'Cr(VI) ile toplam kromu ayrı analiz planlarında belirlemek; kimyasal tür dönüşümünü kontrol etmek.', 'Alkali impinger toplaması ve metot konumundaki yedek filtre. Genel ağır metal treniyle aynı kabul edilmez.',
 'Hacim ve süre tayin limiti ile temsil edici kesit planından belirlenir.', 'Seçilen CARB konfigürasyonuyla izokinetik çekiş.',
 CHEM_PREP+steps(('Tür dönüşümü planı','Numunenin pH, kap, saklama süresi ve Cr(VI)/toplam Cr ayrımını laboratuvarla netleştir.')),
 CHEM_SETUP,CHEM_SAMPLE,CHEM_REC,CHEM_CHECK,
 [train('CARB 425 · kurulum doğrulama şeması',[PROBE,node('Alkali impinger kademesi','NaOH\nDerişim / miktar: resmi §8','Cr(VI) koruması.','alkali'),node('Boş kapan','Metot konumu','Sıvı sürüklenmesi kontrolü.','empty'),node('Yedek filtre','Onaylı filtre konumu','Metot fraksiyonu.','filter'),node('Kurutucu','Tartımı bilinen silika jel','Artık nem.','silica'),PUMP,DGM],'CARB Method 425','Resmi PDF’nin tam metni erişim engeli nedeniyle doğrulanamadı. Sayısal şişe dizisi kesin şart olarak sunulmaz.',False)],('425',),scope='Kapsam ve kaynak kaydı doğrulandı; resmi tam PDF erişim engelli. Kesin NaOH miktarları, filtre konumu ve saklama şartları CARB 425 metni / onaylı talimatla doğrulanmalıdır.')

add('EPA CTM 027','Amonyak · izokinetik CTM-027','Özel parametreler',
 'CTM-027 kapsamındaki kaynaklarda amonyağı asit çözeltisinde toplamak.', 'Method 17 temelli izokinetik tren. Koşullu yöntemdir; diğer kaynaklarda uygun validasyon gerekir.',
 'Süre/hacim numune planından; saklama 4 °C, analiz en geç 2 hafta (CTM-027).', 'İzokinetik çekiş; yüksek nem ve taşma takip edilir.',
 CHEM_PREP,CHEM_SETUP,CHEM_SAMPLE,CHEM_REC,CHEM_CHECK,
 [train('CTM-027 · Method 17 temelli tren',[node('Nozul / baca içi filtre','Method 17 düzeni','İzokinetik numune.','filter'),node('Cam prob','Metot sıcaklığı','Gaz taşınması.','probe'),imp(1,'100 mL 0,1 N H₂SO₄','Amonyak toplama.','acid'),imp(2,'100 mL 0,1 N H₂SO₄','Amonyak toplama.','acid'),imp(3,'Boş veya 100 mL\n0,1 N H₂SO₄','Yüksek NH₃ / akışta metot seçeneği.','empty'),imp(4,SILICA,'Artık nem.','silica'),PUMP,DGM],'EPA CTM-027 §1.1.7','3. şişe koşula göre seçilir; SCAQMD sabit akış kuralı buraya taşınmaz.')],('027',),aliases=['EPA CTM 027 / SCAQMD Method 207.1'])

add('SCAQMD Method 207.1','Amonyak · sabit akış SCAQMD','Özel parametreler',
 'Baca gazındaki serbest amonyağı asit absorpsiyonuyla toplamak.', 'Baca için Greenburg-Smith treninde izokinetik olmayan örnekleme; mini-impinger alan kaynağı seçeneği ayrıdır.',
 'Proses çevrimini temsil eden plan; geri alma sonrası metot azami saklama süresi 4 haftadır.', 'Baca Greenburg-Smith seçeneği: 15–30 L/dk. Bu değer mini-impinger seçeneğine taşınmaz.',
 CHEM_PREP,CHEM_SETUP,CHEM_SAMPLE,CHEM_REC,CHEM_CHECK,
 [train('SCAQMD 207.1 · baca seçeneği',[node('Nozul / prob','İzokinetik olmayan','Gerekirse baca içi filtre.','probe'),imp(1,'100 mL 0,1 N H₂SO₄','NH₃ tutma.','acid'),imp(2,'100 mL 0,1 N H₂SO₄','NH₃ tutma.','acid'),imp(3,'Başlangıçta boş','Sıvı sürüklenmesini azaltır.','empty'),imp(4,'Tartımı bilinen silika jel','Artık nem.','silica'),PUMP,DGM],'SCAQMD Method 207.1 §2.2.1.3','2006 resmi metin esas alındı; önceki rehberdeki 7 gün ifadesi burada evrensel şart olarak kullanılmaz.')],('207',))

add('EPA Method 323','Formaldehit · doğal gazlı kaynaklar','Özel parametreler',
 'Doğal gazla çalışan sabit kaynaklarda formaldehit emisyonunu Method 323 ile belirlemek.', 'Mini-impingerlerde suyla toplama; asetilaseton türevlendirmesi analiz aşamasıdır, saha impingerine DNPH konmaz.',
 'Süre ve toplam numune hedefi ilgili metot ve test planından alınır.', '0,2–0,4 L/dk; 0,4 L/dk üstüne çıkılmaz.',
 CHEM_PREP+steps(('Mini-impinger kullan','Büyük Greenburg-Smith kapları yerine Method 323’te belirtilen mini-impingerleri hazırla.')),
 CHEM_SETUP,CHEM_SAMPLE,CHEM_REC+steps(('Hat yıkamasını unutma','Prob ve bağlantılarda kalan formaldehiti reaktif suyla geri kazan; numune fraksiyonuna ekle.')),
 CHEM_CHECK+steps(('Yöntem kapsamı','Doğal gaz dışındaki kaynaklarda yöntemin uygunluğunu ayrıca doğrula.','Kritik kontrol')),
 [train('EPA Method 323 · mini-impinger treni',[node('Prob + PTFE hat','Hat yıkaması geri alınır','Numuneyi taşır.','probe'),imp(1,'Başlangıçta boş','Kondens / nem kapanı.','empty'),imp(2,'20 mL reaktif su','Formaldehit toplama.'),imp(3,'Tartımı bilinen silika jel','Kuru sayaç koruması.','silica'),PUMP,DGM],'EPA Method 323 · 2023 §6.3 ve §8','Kimyasal türevlendirme laboratuvar analiz aşamasındadır.')],('323',))

add('EPA Method 8','Sülfürik asit / SO₃ ve SO₂','Halojen ve asit gazları',
 'Asit sisi/SO₃ ve SO₂ fraksiyonlarını ayrı belirlemek.', 'İzopropanol fraksiyonu, ardından filtre ve peroksit fraksiyonu. Analizörün anlık SO₂ sonucu ile aynı yöntem değildir.',
 'Metot ve test planına göre temsil edici nokta süresi / hacim.', 'İzokinetik çekiş; 30 L/dk üstüne çıkılmaz.',CHEM_PREP,
 CHEM_SETUP,CHEM_SAMPLE,CHEM_REC+steps(('Asit ve SO₂ fraksiyonlarını ayır','İzopropanol/filtre fraksiyonunu peroksit fraksiyonuyla karıştırma; ilgili geri alma prosedürünü uygula.')),
 CHEM_CHECK+steps(('Filtre yeri','Filtre 1. ve 2. impinger arasındadır; filtre tutucu ısıtılmaz.','Metot şartı')),
 [train('EPA Method 8 · filtre konumuna dikkat',[PROBE,imp(1,'100 mL %80 izopropanol','Asit sisi / SO₃ fraksiyonu.','organic'),node('Filtre','Isıtılmaz','1 ve 2 arasında.','filter'),imp(2,'100 mL %3 H₂O₂','SO₂ toplama.'),imp(3,'100 mL %3 H₂O₂','SO₂ toplama devamı.'),imp(4,'Yaklaşık 200 g silika jel','Artık nem.','silica'),PUMP,DGM],'EPA Method 8 §6 ve §8','Prob yoğuşmayı önleyecek şekilde hazırlanır; farklı filtre yerleşimiyle karıştırılmaz.')],('8',))

add('EPA Method 11','Hidrojen sülfür · H₂S','Özel parametreler',
 'Method 11 kapsamındaki gazlarda H₂S’yi CdSO₄ çözeltisinde toplamak.', 'Mini-impinger treni ve iyodometrik analiz. Kaynak uygulanabilirliği ayrıca kontrol edilir.',
 'Metot kapsamında 10 dakika.', 'Yaklaşık 1 L/dk; izokinetik numune alma değildir.',CHEM_PREP,
 CHEM_SETUP,CHEM_SAMPLE,CHEM_REC,CHEM_CHECK+steps(('CdSO₄ reaktifi','Absorban pH’ı resmi metinde 3 ±0,1; önceki rehberdeki ±1 değeri düzeltilmiştir.','Metot şartı')),
 [train('EPA Method 11 · mini-impinger treni',[node('Numune bağlantısı','Gerekirse uygun basınç / soğuk kapan','Kaynak kapsamı kontrolü.','probe'),imp(1,'15 mL %3 H₂O₂','Girişim gazı kontrolü.'),imp(2,'Başlangıçta boş','Sürüklenme koruması.','empty'),imp(3,'15 mL CdSO₄','H₂S toplama.','acid'),imp(4,'15 mL CdSO₄','H₂S toplama.','acid'),imp(5,'15 mL CdSO₄','H₂S toplama.','acid'),node('Kurutucu','Metoda uygun silika jel','Artık nem.','silica'),PUMP,DGM],'EPA Method 11 §7–8','Kadmiyumlu numune ve atıklar laboratuvarın tehlikeli atık prosedürüyle yönetilir.')],('11',))

add('TS EN 12619 / EPA Method 25A','Toplam organik karbon · TOC / FID','Organik bileşikler',
 'Gaz halindeki toplam organik içeriği FID ile belirlemek.', 'Isıtmalı hat ve alev iyonizasyon dedektörü. Sonuç bazını mg C/m³ veya seçilen kalibrasyon eşdeğeri olarak açıkça belirt.',
 'Sistem cevabı ve proses temsiline göre kayıt periyodu.', 'FID cihazının onaylı numune debisi; tüple VOC örnekleme debisi değildir.',
 steps(('Gazları hazırla','Yakıt gazı, yanma havası, sıfır ve kalibrasyon gazını üretici/metot şartıyla hazırla.'),('Karbon bazını belirle','Propan eşdeğeri, ppm ve mg C/m³ ifadelerinin hangi kalibrasyonla elde edildiğini kaydet.')),
 steps(('Isıtmalı hattı kur','Prob, filtre ve hattın soğuk noktalarını önle; T90 / sistem cevabını ölçüm düzeniyle doğrula.'),('FID’i doğrula','Alev, sıfır, span ve gerekli cevap kontrollerini tamamla.')),
 steps(('Kararlılığı bekle','Kaynak gazı hatta ulaşıp kararlı cevap oluşana kadar ortalama kaydı başlatma.'),('Veriyi kaydet','TOC, O₂ gerekiyorsa O₂, proses koşulları, hat sıcaklığı ve cihaz uyarılarını kaydet.'),('Son doğrulamayı yap','Sıfır/span sürüklenmesini değerlendir; cihazı üretici talimatıyla kapat.')),
 steps(('Sonuç bazını yaz','Toplam karbon ile tek tek VOC bileşiği sonuçlarını farklı göster.')),
 steps(('Yöntem ayrımı','EN 12619 ve EPA 25A’nın şartları seçilen metne göre uygulanır; tek bir kalibrasyon gazı bütün bileşiklere eşit cevap anlamına gelmez.','Kritik kontrol')),
 [train('TOC / FID ölçüm bağlantısı',[node('Isıtmalı prob','Numune alma','Yoğuşmayı önler.','probe'),node('Isıtmalı filtre / hat','Metot sıcaklığı','Organik kaybı kontrolü.','filter'),node('FID','Alev + dedektör','Toplam organik cevap.','meter'),node('Kayıt','Karbon / kalibrasyon bazı','Ortalama ve kalite kayıtları.')],'EN 12619 / EPA 25A','Kimyasal impinger treni kullanılmaz.',False)],('25a',),aliases=['TS EN 12619 / TSE CEN/TS 13649'],scope=ISO_SCOPE)

add('TS EN 13649','VOC · aktif adsorban tüp','Organik bileşikler',
 'Belirli uçucu organik bileşikleri adsorban tüpte toplayıp laboratuvarda ayrı ayrı analiz etmek.', 'Aktif örnekleme; ön/arka adsorban kademeleri ve desorpsiyon/analiz planı birlikte seçilir. FID-TOC sonucu değildir.',
 'Hedef hacim, beklenen derişim ve adsorban kapasitesine göre süre planlanır.', 'Tüp ve debi aralığı bileşik/metot validasyonuna göre seçilir. Her bacada 0,5 L/dk ve 30 dakika evrensel şart değildir.',
 steps(('Bileşik listesini kesinleştir','Hedef VOC listesi, adsorban tipi, kapasite, saklama ve analiz süresini laboratuvarla planla.'),('Debiyi kalibre et','Pompayı gerçek tüp ve bağlantılarla ölçüm öncesi kontrol et.'),('Sıcak gaz planı','Gaz sıcaklığının tüpe uygunluğunu değerlendir; gerekiyorsa doğrulanmış seyreltme sistemini kullan.')),
 steps(('Tüp yönünü bağla','Ön/arka kademe ve pompa yönünü tüp işaretinden kontrol et; gaz kaçaksız tüpten geçmeli.'),('Seyreltmeyi kaydet','Varsa örnek gaz, seyreltme gazı ve tüp akışlarını ayrı kaydet; seyreltme oranını doğrula.')),
 steps(('Tüpü aç ve başlat','Açılış saati, tüp kimliği ve ilk debiyi yaz.'),('Akışı takip et','Süre, sıcaklık ve debi değişimini kaydet; tıkanma veya adsorban kapasite aşımını izle.'),('Örneklemeyi kapat','Son debiyi doğrula ve tüpü uygun kapaklarla hemen kapat.')),
 steps(('Tüpü koru','Tüp, blank ve gerekiyorsa arka kademeyi ayırt ederek ışık/sıcaklık şartlarıyla taşı.')),
 steps(('Breakthrough','Arka kademedeki miktarı laboratuvarın metot kriterine göre değerlendir.','Kritik kontrol'),('Seyreltme hesabı','Tüp hacmi ile bacadan çekilen ham numune hacmini karıştırma; derişim hesabına doğru oranı uygula.','Hesap')),
 [train('VOC aktif tüp bağlantısı',[node('Prob / hat','Hedef bileşiğe uygun','Duvar kaybını azaltır.','probe'),node('Seyreltme','Yalnız gerekiyorsa\nDoğrulanmış oran','Yüksek sıcaklık / derişim yönetimi.'),node('Adsorban tüp','Ön + arka kademe','Bileşikleri tutar.','resin'),node('Debi kontrolü','Gerçek tüple kalibrasyon','Çekiş doğrulaması.','meter'),PUMP],'EN 13649 · işlevsel şema','Kimyasal impinger yerine adsorban tüp kullanılır.',False)],aliases=['TS EN 12619 / TSE CEN/TS 13649','TSE CEN/TS 13649'],scope=ISO_SCOPE)

add('TS EN 12341 / EPA 40 CFR 50-53','PM₁₀ / PM₂․₅ · ortam havası','İmisyon',
 'Ortam havasındaki boyut seçilmiş partikül madde derişimini belirlemek.', 'Boyut seçici giriş başlığı, sabit akışlı filtre örneklemesi ve gravimetri. Başlık tasarım debisi yöntemin parçasıdır.',
 'Seçilen referans yönteme uygun günlük örnekleme ve geçerli süre kriteri uygulanır.', 'Qamb: ortam şartı debisi; Qref: tanımlı referans şartı debisi. Başlık hangi debi bazına göre çalışıyorsa o baz kullanılır.',
 steps(('Başlık ve filtreyi seç','PM₁₀ / PM₂․₅ ayrımını, cihazın referans/eşdeğer yöntem kaydını ve tasarım debisini kontrol et.'),('Filtre kimliğini eşleştir','Koşullandırma, ilk tartım ve saha blank kayıtlarını hazırla.'),('Konumu kontrol et','Çevre engelleri, yakın kaynaklar, giriş yüksekliği ve güvenliği saha planına göre değerlendir.')),
 steps(('Başlığı kur','Dik konum, temiz giriş, conta ve filtre oturuşunu kontrol et.'),('Debi ve kaçak','Kalibre debi kontrolüyle cihazı doğrula; seçilen metot kaçak testini yap.')),
 steps(('Başlangıç kaydı','Filtre, başlık, cihaz, saat ve ilk hacmi yaz.'),('Periyodu izle','Akış, ortam T/P, kesinti ve cihaz uyarılarını kaydet.'),('Örneklemeyi bitir','Geçerli süre/hacmi değerlendir; filtreyi pensle kapalı kimlikli kaba al.')),
 steps(('Laboratuvar teslimi','Filtreyi ve blankı uygun taşıma koşullarıyla tartım laboratuvarına teslim et.')),
 steps(('Sonuç hesabı','C = (son filtre kütlesi − ilk filtre kütlesi, metot blank değerlendirmesiyle) / seçilen bazdaki hava hacmi.','Hesap'),('Başlık debisi','Bir cihazın EPA ve EN ayarlarını aynı debi/basınç şartı gibi kabul etme.','Kritik kontrol')),
 [train('Ortam havası PM ölçümü',[node('Ortam havası','Konum kriterleri'),node('PM başlığı','PM₁₀ veya PM₂․₅','Boyut seçimi.'),node('Filtre','Koşullandırılmış / tartılmış','Partikül kütlesi.','filter'),node('Hacim ve akış','Seçilen T/P bazı','Geçerli hava hacmi.','meter'),PUMP],'Seçilen EN / EPA referans yöntemi','İmpinger veya baca nozul treni kullanılmaz.',False)],aliases=['TS EN 12341 / EPA 40 CFR Part 50-53'],scope=ISO_SCOPE)

add('TS 2341 / TS 2342 / SKHKKY Ek-2','Çöken toz','İmisyon',
 'Belirli alana ve maruziyet süresine çöken toz miktarını belirlemek.', 'Toplama kabıyla pasif çökelme; pompalı PM₁₀ ölçümünden farklıdır.', 'Maruziyet süresi seçilen yöntem ve izleme planına göre belirlenir.', 'Pompa debisi yoktur; kap alanı ve geçerli gün sayısı hesabın temelidir.',
 steps(('Kapları hazırla','Temiz kap, kimlik, açılma/kapanma zamanı ve saha blanklarını planla.'),('Noktaları belirle','Tesis ve çevre temsilini, rüzgar etkisini, engelleri ve kap güvenliğini değerlendirmek için kroki hazırla.')),
 steps(('Kabı yerleştir','Düzgün, güvenli konumu ve seçilen yöntemin koruyucu sıvısını uygula; ağız alanını kaydet.')),
 steps(('Maruziyeti başlat','Başlangıç tarih/saatini yaz; kabın açık olduğunu ve kimliğini doğrula.'),('Saha durumunu izle','Devrilme, taşma, kuş/böcek ve yabancı madde gibi durumları kaydet.'),('Kabı kapat','Bitiş zamanını yaz; numune kaybı olmadan kapağı kapat.')),
 steps(('Numuneyi teslim et','Kap bütünlüğünü ve maruziyet kaydını kontrol et; laboratuvarla çözünür/çözünmez fraksiyon planını eşleştir.')),
 steps(('Hesap','Alan ve gün sayısıyla normalize edilir. Örneğin mg/(m²·gün) bazında kütle / alan / gün; farklı rapor bazını açıkça belirt.','Hesap')),
 [train('Çöken toz saha düzeni',[node('Ölçüm noktası','Kroki / çevre'),node('Toplama kabı','Bilinen ağız alanı','Pasif çökelme.'),node('Maruziyet','Başlangıç / bitiş','Geçerli gün.'),node('Laboratuvar','Fraksiyon / kütle'),node('Sonuç','Alan ve süre bazı')],'TS 2341 / TS 2342 · saha prensibi','Pompa, kuru gaz sayacı ve impinger yoktur.',False)],aliases=['TS 2341 / TS 2342 / SKHKKY Ek-2 saha yaklaşımı'],scope=ISO_SCOPE)

add('Pasif Örnekleme / Difüzyon Tüpü','Pasif gaz örnekleme · difüzyon tüpü','İmisyon',
 'Ortam gazlarını pompa kullanmadan adsorbanla toplamak.', 'Üretici/metot tarafından doğrulanmış alım hızı ile maruziyet süresi kullanılır.', 'Bileşik, tüp ve izleme planına göre maruziyet; her tüpe tek süre uygulanmaz.', 'Pompa debisi yok. Konsantrasyon hesabında doğrulanmış difüzyon alım hızı kullanılır.',
 steps(('Tüpü seç','Hedef bileşik, alım hızı, saklama süresi ve çevresel geçerlilik aralığını laboratuvarla doğrula.'),('Blankları ayır','Saha ve taşıma blankını tüp kimlikleriyle planla.')),
 steps(('Koruyucuyu yerleştir','Shelter, yön ve yükseklik şartını tüp/metot talimatına göre uygula.')),
 steps(('Tüpü aç','Açılış saatini yaz; blankı maruziyete bırakma.'),('Noktayı kontrol et','Yerinden çıkma, kirlenme ve hava olaylarını kaydet.'),('Tüpü kapat','Bitiş saatini yaz ve uygun kapakları hemen tak.')),
 steps(('Taşıma','Tüp ve blankları belirlenen sıcaklık/ışık şartlarıyla laboratuvara gönder.')),
 steps(('Geçerli maruziyet','Süre ve alım hızı farklı tüp modellerinden alınmaz; üretici validasyonuyla eşleşmelidir.','Kritik kontrol')),
 [train('Pasif tüp düzeni',[node('Ortam havası','Seçilen konum'),node('Shelter','Yağış / rüzgar koruması'),node('Difüzyon tüpü','Hedef bileşiğe uygun','Adsorpsiyon.','resin'),node('Maruziyet kaydı','Açılma / kapanma'),node('Analiz','Alım hızı + süre')],'Seçilen tüp / metot talimatı','Aktif pompa veya impinger kullanılmaz.',False)],scope='Tüp üreticisinin güncel alım hızı ve çevresel validasyonu kullanılır.')

add('TS 9503 / Bacada İslilik Ölçümü','Bacada islilik','Diğer ölçümler',
 'Seçilen yöntemde gaz numunesinin filtrede oluşturduğu islilik derecesini belirlemek.', 'Filtre lekesinin doğrulanmış ölçekle değerlendirilmesi; gravimetrik partikül derişimi değildir.', 'Çekiş sayısı/hacmi ve süre cihaz/metot talimatından alınır.', 'Seçilen pompanın hacmi ve tam strok şartı kontrol edilir.',
 steps(('Filtre ve ölçeği hazırla','Temiz filtre, pompa ve karşılaştırma ölçeğinin uygunluğunu kontrol et.')),
 steps(('Sızdırmaz kur','Prob, filtre ve pompa bağlantılarını yerleştir; filtre baypasını önle.')),
 steps(('Numuneyi çek','Metodun çekiş sayısı/hacmini uygula; eksik strok veya yoğuşmayı kaydet.'),('Lekeyi değerlendir','Standart ışık/ölçek şartına göre karşılaştır; sonucu ve numune kimliğini yaz.')),
 steps(('Filtreyi koru','Lekenin kirlenmesini önleyerek kimlikli kapta sakla.')),
 steps(('Sonuç ayrımı','İslilik derecesini mg/m³ partikül sonucu gibi raporlama.','Kritik kontrol')),
 [train('İslilik ölçüm bağlantısı',[node('Baca probu','Seçilen nokta','Gaz numunesi.','probe'),node('Filtre','Leke oluşumu','İslilik numunesi.','filter'),node('Pompa','Tanımlı çekiş','Hacim / strok.','pump'),node('Ölçek','Metoda uygun','Görsel karşılaştırma.')],'TS 9503 · saha prensibi','İmpinger kullanılmaz.',False)],scope=ISO_SCOPE)

add('ISDL / MID','Hedef hacim ve raporlama limiti','Kalite kontrol',
 'Sahaya çıkmadan numunenin hedef raporlama seviyesine ulaşabilecek kadar hacim/kütle sağlayacağını kontrol etmek.', 'Ölçüm metodu değildir; laboratuvar tayin limiti, blank ve beklenen derişim üzerinden planlama yapılır.', 'Planlanan süre = hedef hacim / uygun bazdaki ortalama çekiş; metodun minimum süresi ayrıca korunur.', 'Debi seçilen kirletici yönteminden alınır; tayin limitini sağlamak için metot dışına çıkılmaz.',
 steps(('Laboratuvar bilgisini al','Analit bazında kütle tayin limiti, blank seviyesi ve istenen raporlama hedefini öğren.')),
 steps(('Bazı eşleştir','Kütle ve hacim birimlerini aynı hesapta tut; hedef kuru referans hacimle ham sayaç hacmini ayır.')),
 steps(('Hedef hacmi hesapla','Basit planlama: Vhedef = hedef kütle / hedef derişim. Güvenlik payı ve blank etkisini laboratuvarla belirle.'),('Süreyi planla','Uygun metot debisiyle süreyi hesapla; yöntem süre/kapsam şartlarını ayrıca kontrol et.'),('Sahada gerçekleşeni izle','Gerçek hacim hedefe ulaşmadıysa numune/analiz kararını laboratuvarla değerlendir.')),
 steps(('Planı sonuçla karşılaştır','Gerçek hacim, blank ve elde edilen raporlama limitini aynı kayıtta sakla.')),
 steps(('Tayin limiti / sınır değer','Laboratuvar tayin limiti ile yönetmelik sınır değeri aynı kavram değildir.','Kritik kontrol')),
 [train('Numune hacmi planlama',[node('Analit ve limit','Raporlama hedefi'),node('Laboratuvar','Kütle LOD / LOQ'),node('Hedef hacim','Kütle / derişim'),node('Saha planı','Metot debisi ve süre'),node('Son kontrol','Gerçek hacim + blank')],'Laboratuvar validasyonu + seçilen numune metodu','Numune treni değildir; planlama akışıdır.',False)])

# Equipment follows the curated diagram, rather than old mixed-method lists.
for g in guides:
    g['equipment'] = list(dict.fromkeys([n['label'] + (' — ' + n['value'].replace('\n', '; ') if n['value'] else '') for t in g['trains'] for n in t['nodes']])) + ['Metoda uygun sıcaklık / basınç ve zaman kayıt ekipmanı.', 'Numune ve blank kapları; saha formu ve etiketler.']
    g['mistakes'] = ['Farklı metotların trenini veya sayısal şartlarını birbirine taşımak.', 'Ölçüm kesintisini ve proses değişikliğini kaydetmemek.', 'Sayaç hacmi ile kuru referans hacmi aynı kabul etmek.']
    if g['group'] == 'İmisyon':
        g['mistakes'] = ['Başlangıç ve bitiş zamanını eksik kaydetmek.', 'Blank ve numune kimliğini karıştırmak.', 'Geçersiz maruziyet / kesinti kaydını değerlendirmemek.']
# Keep all legacy dataset files as an archive; the app displays only this curated dataset.
# Remove exact duplicate statements across sections without discarding different conditions.
for g in guides:
    seen=set()
    for section in ['preparation','setup','sampling','recovery','checks']:
        clean=[]
        for p in g[section]:
            key=' '.join((p['title']+' '+p['text']).lower().split())
            if key not in seen:
                clean.append(p);seen.add(key)
        g[section]=clean
    for i,t in enumerate(g['trains']):
        t['imageAsset']=f"assets/trains/{g['id']}_{i+1}.png"

(ASSETS/'field_guides.json').write_text(json.dumps(guides,ensure_ascii=False,indent=2)+'\n')
print(f'{len(guides)} guides, {sum(len(g["trains"]) for g in guides)} diagrams')
