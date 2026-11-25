"""Kullanıcının yerel nüshalarından karşılaştırılan EN saha bölümleri."""
from copy import deepcopy

LOCAL_SOURCES=[
 dict(id='L01',title='TS EN 1911:2010 — HCl olarak gaz halindeki klorürler',edition='TSE Ocak 2011; EN 1911:2010',pages=48,sha256='a1e0cb304290cb520fa865382f667867ed5da563bb5b8409595526629f07bd8d'),
 dict(id='L02',title='BS EN 14385:2024 — 11 metalin toplam emisyonu',edition='EN 14385:2024 ana metni; yerel dosya adı TS olsa da kapak BS',pages=77,sha256='e120d09e8396e32162cec4ab0f8267957ab62f331b1f9c18006dfd76aed97311'),
 dict(id='L03',title='TS EN 13284-1 — düşük derişimli toz, manuel gravimetri',edition='TSE Ocak 2018; EN 13284-1:2017',pages=66,sha256='6959ae26b6a6d70cb56a3f521c693021b1fa6beeb642ca808f812e73fdb07f69'),
]


def extend(data,profile,node,imp,meter,delivery):
    data[:]=[p for p in data if p['id'] not in {'hcl_tl89','metals_en14385'}]
    def add(*args,evidence,**kwargs):
        p=profile(*args,**kwargs);p['reviewState']='sections_checked'
        p['evidence']=[dict(field=k,references=v[0],clause=v[1]) for k,v in evidence.items()]
        data.append(p);return p
    def dryer(key,label='Kurutma grubu'):
        return node(key,'trap',label,'Kuru sayaç için seçilen nem uzaklaştırma sistemi; kaynağın artık nem koşulunu sağla')
    def branch(p,stem,shared,main,side):
        p['train']=[]
        p['diagram']=dict(asset=f'assets/diagrams/{stem}.png',shared=shared,
            branches=[dict(id='main',label='Ana kol',nodes=main),dict(id='side',label='Analiz için yan kol',nodes=side)])

    hcl_notes={
      'Hazırlık':['Hedef gaz halindeki uçucu inorganik klorürlerdir; HCl olarak raporlanır. Damlacık biliniyor/şüphe ediliyorsa izokinetik gerekir. Nokta/homojenlik planı EN 15259 bağlantılıdır.',
         'En az iki seri absorbere EN ISO 3696 derece 2, klorür içermeyen su koy. Dolum verim deneyindeki hacimle aynı olmalı; 40–100 mL kaynakta örnektir, evrensel sabit dolum değildir.',
         'Cam/titanyum/PTFE numuneye temas edebilir; absorbere kadar paslanmaz çelik kullanma. Filtre verimi >%99,5 @0,3 µm test aerosolü veya >%99,9 @0,6 µm. Bunlar filtre gözenek çapı değildir.'],
      'Kaçak kontrolü':['Tam treni işletim sıcaklığında denetle; kaçak beklenen debinin %2’sini aşamaz. Ön/ölçüm sırası testini kaydet; grid ölçümü sonrası test önerilir.',
         'Saha blankında hazırlık, kurulum, geri kazanım ve analiz izlenir; emme/pompa çalıştırma adımı yapılmaz. Seri/gün sıklığını §5.3.3.3’e göre uygula; sahada yıka-yeniden kullanımda seri sonu blankı da gerekir.'],
      'Örnekleme':['Prob/filtreyi ön ısıt; başlangıç sayaç değerini kaydet. Debi, sayaç sıcaklık/basıncı ve süreç koşullarını izleyerek seçili noktaları örnekle; port değişiminde hattı/pompayı durdurma prosedürünü uygula.',
         'Her kampanyada absorpsiyon verimini doğrula. Son absorberde en çok %5 tutulma veya son absorber derişiminin 5×analitik tespit sınırından (LOD) küçük olması koşulunu değerlendir (§5.2.1.2.2).'],
      'Geri kazanım':['Son absorberi kendi kabında ayrı geri kazan; arkasındaki koruma kabına taşınan sıvı bu SON fraksiyona eklenir. Absorberleri kendi klorürsüz suyuyla iyice yıka.',
         'Filtre–ilk absorber arasındaki ısıtılmayan kısımların su yıkamasını İLK fraksiyona ekle. Verim kontrolü için ilk/son fraksiyonu ayrı analiz ettir; katı klorürleri gaz klorür sonucuna rastgele ekleme. Gereksiz yüksek yıkama hacmiyle tayin sınırını kötüleştirme.'],
      'Saklama ve taşıma':['Numuneyi klorür bulaştırmayan, sızdırmaz ve laboratuvarın onayladığı kapta; fraksiyon kimliği ve sıvı seviyesiyle taşı. İncelenen EN 1911 metninde sayısal taşıma/saklama sıcaklığı veya azami analiz bekletme süresi bulunmadı. Bu alanları teslim öncesi laboratuvarın geçerli numune kabul planıyla belirle.'],
      'Laboratuvara teslim':delivery+['İlk/son absorber kimliği, gerçek su/yıkama/son hacimler, blank ve verim hesabı için ayrı analiz isteğini bildir. Blank <%10 ELV olmalı; blankı aşmayan sonuç ≤blank olarak raporlanır (§5.3.3.3).']}
    hcl_evidence={'Metot / düzen / verim':(['L01:13-21'],'§4-5.3.2.1'),
        'Tarihli atıf':(['L01:8'],'§2 — EN 13284-1:2001'),
        'Kaçak / blank / geri kazanım':(['L01:18,21-24'],'§5.2.1.2.2, §5.3.2–5.3.3, §6.2'),
        'Sayaç / sıcaklık':(['L01:17-20'],'§5.2.1–5.2.4')}
    for variant in ('noniso','iso','split'):
        isokin=variant!='noniso'
        water=[imp(1,'Klorür içermeyen derece 2 su','Verim deneyindeki dolum; kaynak örneği 40–100 mL'),
               imp(2,'Klorür içermeyen derece 2 su — son absorber ayrı analiz','Verim deneyindeki dolum; kaynak örneği 40–100 mL'),
               imp(3,'Başlangıçta boş — taşınan sıvı koruma kabı','',True),dryer('dryer'),meter]
        p=add('hcl_en1911_'+variant,'Klor / halojenler','TS EN 1911','EN 1911:2010 / TSE Ocak 2011',
            {'noniso':'İzokinetik olmayan; düz prob / dış filtre', 'iso':'İzokinetik; yan kol olmadan', 'split':'İzokinetik; filtre sonrası yan kol'}[variant],
            ['L01:8,13-24,31'],[node('probe','probe','Nozül / prob' if isokin else 'Düz ısıtılmış prob','Numuneye uygun cam / titanyum / PTFE'),
             node('filter','filter','Isıtılmış dış filtre','Çiy noktasının en az 20 °C üstü'),*water],
            [('İzokinetik toplam çekiş. Yan kolda yaklaşık 2–3 L/dk kaynakta yaygın örnektir; verim esastır.' if variant=='split' else
              'İzokinetik çekiş; absorber verimi aynı debi/kap/dolumla sağlanmalı.' if isokin else 'Seçili absorbere ve verim testine uygun kontrollü debi; sabit evrensel L/dk yok.'),
             'Hedef derişim, analiz tayin sınırı ve son sıvı hacminden hesapla; kuru gazı kaynak ref. 273 K / 101,3 kPa ile raporla.',
             'Dış filtre ≥çiy noktası+20 °C; prob/bağlantıda soğuk nokta bırakma. Kuru sayaç önünde artık nem <10 g/m³.',
             'Grid örneklemede EN 1911:2010’un tarihli EN 13284-1:2001 atfındaki temsil/süre koşulları uygulanır. 2017 toz standardının süreleri bu eski atfa otomatik taşınmaz; hacim ve ortalama süresini ayrıca planla.' if isokin else 'Hedef hacim ve gerekli ortalama süresine göre; her gaz ölçümüne sabit 30 dk atanmaz.'],
            deepcopy(hcl_notes),gaps=['EN 13284-1:2001 tarihli atfının süre koşulları ve laboratuvarın numune kabul/koruma koşulları tamamlanmalı. Seçili absorberin dolumu verimle doğrulanmalı. İç filtre alternatifinin damlacık/sıcaklık koşulları ayrı seçilmelidir.'],evidence=hcl_evidence)
        if variant=='iso':p['phases'][2]['items']+=['Yan kol olmadan kullanım yalnız absorber verimi sağlanıyorsa mümkündür; bir üst sınıra rastgele sabit debi ayarlama.']
        if variant=='split':
            p['phases'][2]['items']+=['İki kolun sayaç/çekişi ayrıdır. Konsantrasyon homojen değilse EN 15259 yerel hızla orantılı yan kol/örnekleme koşulunu ölçüm kalite hedefiyle değerlendir (§5.1.3.1).']
            branch(p,'hcl_en1911_split',[*p['train'][:2],node('split','splitter','Isıtılmış T parçası','Filtre sonrası akış ayrımı')],
                [dryer('main_dryer','Ana kol kurutma'),node('main_meter','meter','Ana kol çekiş ve hacmi','İzokinetik toplam ayarında yan kolu da hesaba kat')],
                [dict(n,id='side_'+n['id']) for n in water])

    metal_notes={
      'Hazırlık':['Bu nüsha EN 14385:2024 ana metninin BS baskısıdır; hedefler As, Cd, Cr, Co, Cu, Mn, Ni, Pb, Sb, Tl ve V. Cıva bu listenin parçası değildir. Numuneye temas eden yüzeyleri ve PE kapları önceden temizle.',
         '§5.2.8: yaklaşık %65 (kütle/kütle) HNO₃ ve %30 (kütle/kütle) H₂O₂ stoklarından eş hacimleri karıştır; bu karışımın 1 hacmini 9 hacim suya ekle. Nihai yaklaşık %4,4 HNO₃ / %1,6 H₂O₂ (kütle/kütle). Çözeltiyi taze hazırla veya peroksiti sahada ekleme alternatifini uygula.',
         'En az üç dolu seri absorber. Uygun dolum, örneğin kap hacminin en az %25’i, gaz–sıvı teması ve verimle belirlenir. Tek bir mL bütün kaplara atanmaz. Sonrasında boş koruma kabı; yüksek nemde ilk dolu öncesi boş kondensat kabı kullanılabilir.'],
      'Kaçak kontrolü':['Her örnekleme başlangıcında tam tren testi: kaçak ≤beklenen Q’nun %2’si. Annex B’deki yöntem/uygun eşdeğer prosedürü uygula; sıvının geriye yürümesini önle.',
         'O₂ karşılaştırması büyük kaçağı gösterebilir; ana kaçak testinin yerini almaz.'],
      'Örnekleme':['EN 13284-1 bağlantılı izokinetik/grid örnekleme; gerçek sayaç değerleri, basınç/sıcaklık ve süreleri kaydet. En az bir ölçümde son absorber ayrı tutularak grup bazında verim denetimi yapılır.',
         'Son absorberde bir metalin kütlesi o metalin filtre+prob+absorber toplamının %10’undan fazlaysa ait olduğu grubun sonuçları reddedilir. Grup içi <%1 kütle veya grup toplamı <%30 ELV istisnaları yalnız §6.3 koşullarıyla değerlendirilir.'],
      'Geri kazanım':['Filtreyi kimlikli taşıma kabına al. Bu varyantta nozül/prob/filtre önünü kendi absorpsiyon çözeltisiyle yıka (§8.4.3). Ön yüzeyler en az seri/günde bir geri kazanılır; birden fazla ölçüme ait yıkama, gaz hacimleri oranında paylaştırılır.',
         'Filtre arkası ve ilk absorbere bağlantı her ölçümde İLK absorber fraksiyonuna yıkanır. Her şişe/bağlantı yıkaması ilgili absorber kabına eklenir. Ön boş kondensat kabı varsa içerik+yıkaması ilk dolu absorbere katılır.',
         'En az bir ölçümün son absorberini ayrı analiz ettir. Diğer uygun ölçümlerde absorberler birleşebilir. Gereksiz seyreltmeden kaçın; hacim/kütle ve sıvı düzeylerini kaydet.'],
      'Saklama ve taşıma':['Sıvılar PE kapta; kapak PTFE/PFA/FEP/PP veya renksiz PE. Sahada/taşımada <25 °C; laboratuvarda <6 °C. Analiz numune alımından itibaren en geç 4 hafta içinde (§8.6).',
         'Peroksit bozunması basınç oluşturabilir: cam absorber/depo şişesini laboratuvarda doldurup bekletme uyarısını §8.2.3’e göre uygula.'],
      'Laboratuvara teslim':delivery+['Filtre, ön yıkama, absorberler/son kademe ve blank kimlikleri; kaynak başına verim denetimi; grup A/B hesapları için hacim ve zamanları bildir.',
         'Saha blankı platformda kurulur, prob bacaya sokulmaz; kurulum/kaçak/geri kazanım kapsanır. Blank numuneden çıkarılmaz; ayrı raporlanır. Blank >%10 düzenleyici sınırsa ilgili kampanya kısmı reddedilir.']}
    for split in (False,True):
        bottles=[imp(i,'Yaklaşık %4,4 HNO₃ / %1,6 H₂O₂ (kütle/kütle)','Kap/verimle belirlenen dolum; sabit 100 mL normu yok') for i in (1,2,3)]
        tail=[*bottles,imp(4,'Başlangıçta boş — koruma kabı'),dryer('dryer'),meter]
        p=add('metals_en14385_'+('split' if split else 'full'),'Ağır metaller','EN 14385','2024 — yerel BS EN nüshası',
            'Ön boş kondensat kabı olmadan; dış filtre; '+('ısıtılmış bölücü ve yan kol' if split else 'bütün gaz absorberlerden geçer'),['L02:12-23','L03:27-30'],
            [node('probe','probe','Nozül / ısıtılmış prob','Cam / kuvars / PTFE veya uygun titanyum'),node('filter','filter','Isıtılmış dış filtre','Kuvars elyaf / PTFE; düşük metal blankı'),*tail],
            ['İzokinetik, EN 13284 bağlantılı %95–115; sabit L/dk yok. Yan kol varsa iki debi ayrı.',
             'Analitik LOQ/blank ve mevzuat hedefini sağlayacak kuru standart hacim. Sıvı numune hacmi gaz hacmi değildir.',
             'Absorberler ≤30 °C. Prob/dış filtre/T: §8.1 gaz T+20 K veya asit çiy+20 K (en çok 180 °C ifadesi), yüksek olan; yüksek baca T uygulaması yazılı planla kesinleştirilir.',
             'EN 13284 grid süreleri: ≥3 dk/nokta, ≥30 dk toplam; hedef hacim/ilgili mevzuat daha uzun gerektirebilir.'],
            deepcopy(metal_notes),gaps=['§8.1’deki 180 °C ifadesinin yüksek baca sıcaklığına uygulanışı ve ulusal TS baskısı/yerel SOP eşleştirmesi doğrulanmalı; uygulama otomatik sıcaklık hedefi üretmez.',
              'Yıkama asidi §5.2.11 yerine izin verilen kendi absorpsiyon çözeltisiyle yıkama varyantı seçildi. Numune planındaki her fraksiyon laboratuvarla eşleşmeli. Cıva birlikte istenirse kapsamda EN 13211 yan kol seçeneği vardır; onun düzeneği bu karta eklenmiş değildir.'],
            evidence={'Çözelti / kap / dolum':(['L02:13-20'],'§5–6; §8.2'), 'Geri kazanım / saklama / blank':(['L02:21-23'],'§8.4–8.6'),
                      'Sıcaklık / verim':(['L02:18-19'],'§6.3, §8.1'),'Süre / izokinetik':(['L03:27-28'],'§9.4–9.5 bağlantısı')})
        if split:branch(p,'metals_en14385_split',[*p['train'][:2],node('split','splitter','Isıtılmış T parçası','Yalıtım tek başına yeterli değildir')],
            [dryer('main_dryer'),node('main_meter','meter','Ana kol çekiş ve hacmi','Toplam izokinetik koşulda yan kol da hesaba katılır')],
            [dict(n,id='side_'+n['id']) for n in tail])

    for inside in (False,True):
        front=[node('probe','probe','Giriş nozülü','Nozül doğrudan baca içi filtre önünde'),node('filter','filter','Baca içi filtre','Nozülün hemen arkasında'),node('line','probe','Destek / çıkış hattı','Filtre sonrasında')]
        if not inside:front=[node('probe','probe','Nozül / ısıtılmış emiş tüpü','Ön birikim yüzeyleri geri kazanılır'),node('filter','filter','Isıtılmış dış filtre','Filtrasyon sıcaklığı ölçülür / raporlanır')]
        p=add('dust_en13284_'+('in' if inside else 'out'),'Partikül madde / toz','TS EN 13284-1','TSE Ocak 2018 / EN 13284-1:2017',
            ('Baca içi filtre' if inside else 'Baca dışı filtre')+' — kuru gaz hacim sistemi',['L03:8,14,16-30,43-45,63'],
            [*front,node('dryer','condenser','Soğutma / kurutma grubu','Kuru gaz ölçüm sistemine uygun; evrensel impinger dolumu belirtilmez'),meter],
            ['İzokinetik %95–115; nozül akış yönünden en çok 10° sapmalı. Her noktada gerçek hız, çap, nem, T ve basınçla ayarla.',
             'Ek E: Vmin=10U/E. U tüm tartım prosedürünün genişletilmiş belirsizliği; E emisyon sınırı. U mg, E mg/m³ ise Vmin m³. Qmin=Vmin/t; nozül/pompa kapasitesini ayrıca kontrol et.',
             'Filtrasyon: seçili amaç/gaz koşulu; baca T veya en az önerilen 160 °C yaklaşımı. Yoğuşma olmamalı; uçucu bileşenlerde sıcaklık sonucun tanımını etkiler (Ek H).',
             'Her noktada aynı süre ve ≥3 dk; toplam ≥30 dk. N noktada seri tek tren için en az max(3N,30) dk; hacim hedefi daha uzun gerektirebilir.'],
            {'Hazırlık':['Yöntem <50 mg/m³ için geliştirilmiş, özellikle yaklaşık 5 mg/m³’te doğrulanmıştır; diğer kaynaklarda kapsam/performansı değerlendir. Ölçüm planı EN 15259 bağlantılıdır.',
                 'Ön tartım: ≥1 saat, örnekleme ve son işlemdeki en yüksek sıcaklıktan ≥20 °C yüksek kurutma. Tartım odasında desikatörde ≥4 saat; büyük parçalarda 12 saat gerekebilir. Terazi/iklim ve aynı tip kontrol parçasıyla tartım prosedürünü doğrula.'],
             'Kaçak kontrolü':['Her ölçüm öncesinde tam trenin kaçağı ≤beklenen Q’nun %2’si. İşletim sıcaklığında yap; kaçakları araştır ve düzelt.'],
             'Örnekleme':['Her noktada ve en az 5 dakikada bir hız hesabı parametrelerini kaydet; debiyi buna göre ayarla. Başlangıç/son sayaç, T ve basınç kayıtlarını koru.',
                 'Basit prob/ön hız profili yalnız kararlılığı gösterilmiş proseste; sabit referans Pitot hız değişimi <%10 koşulunu uygula. Aksi halde noktanın gerçek hızıyla izokinetik ayar yapılır.',
                 'Filtre kırığı veya filtre/tutucuda yoğuşma görürsen ölçüm geçersizdir. 30 dk ile kısıtlanan planlarda yeterli hacim ve bütün noktalar için paralel sistem ihtiyacını §6.1’e göre değerlendir.'],
             'Geri kazanım':['Filtre önündeki tartılmayan numuneye temas eden yüzeyleri suyla, toz özelliğine göre ardından asetonla aynı kaba yıka. Bu geri kazanımda mekanik temizleme uygulama (§9.6.2).',
                 'Aynı düzlemde en az seri/günde bir yıka. Birden çok ölçümün yıkama kütlesi, filtrelerde toplanan kütle oranında paylaştırılır. Dirseksiz baca içi düzenin dar istisnası ancak §9.6.1 validasyonu ile kullanılabilir.'],
             'Saklama ve taşıma':['Filtre/tutucuyu kimlikli, kapalı, elektrostatik etkiden korunmuş taşıma kabına al. Yıkama kabı asetonla uyumlu ve sızdırmaz olmalı; dış kirlenmeyi ve numune kaybını önle.',
                 'İncelenen metinde sayısal azami bekletme süresi/taşıma sıcaklığı verilmez. Son tartım hazırlığı: ≥1 saat 160 °C, sonra §8.2 soğutması; gerekçeli alternatif sıcaklık Ek H ve raporla. Laboratuvara teslim planını önceden kesinleştir.'],
             'Laboratuvara teslim':delivery+['Filtre ve ön yıkama ayrı kimliklerle, solvent blankı ve saha blanklarıyla teslim edilir. Saha blankı ≤max(%10 ELV; 0,5 mg/m³); her blank ayrı raporlanır.',
                 'Sıcaklıklar, hacim bazları, izokinetik kayıt, tartım belirsizliği ve yıkama paylaştırma verilerini aktar.']},
            gaps=['EN 15259/ISO 16911 bağlantılarının tam ekipman prosedürleri ve kaynağa özgü termal/analitik hedef ayrıca doğrulanmalı.'],
            evidence={'Süre / debi / kaçak':(['L03:26-30'],'§9.3–10'),'Hacim / belirsizlik':(['L03:45'],'Normatif Ek E'),
                      'Tartım / taşıma / geri kazanım':(['L03:23-30,63'],'§7.3–9.7; Ek H')})
        p['trainNote']='Bu varyant kuru sayaçlıdır. Nem uzaklaştırmada tek bir EPA tipi şişe sayısı veya mL reçetesi bu standarttan otomatik atanmaz.'
