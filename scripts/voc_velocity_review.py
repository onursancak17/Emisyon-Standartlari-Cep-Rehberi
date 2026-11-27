"""Tam L04/L05 nüshalarının saha maddelerinden özgün Türkçe uygulama kartları."""
from copy import deepcopy

SOURCES=[
 dict(id='L04',title='TS EN ISO 16911-1 — elle hız ve debi referans yöntemi',edition='TSE Haziran 2013; ISO 16911-1:2013',pages=97,sha256='5458b8dab8c87c6989782d3aecdd7d1adba145919cd30d360863a975d39a5246'),
 dict(id='L05',title='TSE CEN/TS 13649 — tekil gaz VOC, sorbent tüp',edition='TSE Şubat 2015; CEN/TS 13649:2014',pages=49,sha256='38a1530489b3969090ce84f02b6f4e02a54fe0ab788906beb2969db1219ccba1'),
]

def extend(data,profile,node,imp,meter,delivery):
    def add(*args,evidence,**kwargs):
        p=profile(*args,state='sections_checked',**kwargs)
        p['evidence']=[dict(field=k,references=v[0],clause=v[1]) for k,v in evidence.items()]
        data.append(p)
        return p
    for td in (False,True):
        tubes=([node('primary','adsorber','Ana TD tüpü','Hedef VOC için seçilmiş ve şartlandırılmış sorbent'),
                node('backup','adsorber','Aynı tip yedek TD tüpü','Kırılma kontrolünde seri bağlanır; ayrı analiz','',True)] if td else
               [node('charcoal','adsorber','İki yataklı aktif karbon tüp','Ön ve arka yatak ayrı analiz edilir','Tipik 100 mg + 50 mg')])
        p=add('voc_13649_'+('td' if td else 'charcoal'),'VOC — tekil organik bileşikler','CEN/TS 13649','2014 / TSE Şubat 2015',
            'Doğrudan örnekleme — '+('termal desorpsiyon (TD)' if td else 'aktif karbon / çözücü desorpsiyonu'),
            ['L05:8-20,21,25-28'],
            [node('probe','probe','Numune probu','Uygulamaya göre ısıtılır; kısa inert bağlantı'),
             node('filter','filter','Partikül filtresi','Sorbent önünde; gerekiyorsa ısıtılmış dış filtre'),*tubes,
             node('dryer','trap','Pompa / sayaç koruması','Nemli gazda önerilen kurutucu sorbentten SONRA; hedef VOC’yi toplamadan önce kurutma yapılmaz'),meter],
            ['Tablo 1: TD için 10–100 mL/dk = 0,010–0,100 L/dk; Q belirsizliği <%5. Ek C’deki başka pompa aralıkları bu tipik aralığın yerine otomatik geçirilmez.' if td else 'Tablo 1: 0,1–0,5 L/dk; Q belirsizliği <%5. Hedef bileşik, sıcaklık, kapasite ve tayin sınırıyla seçilir.',
             ('Tipik 1–5 L' if td else 'Tipik 10–50 L')+'; zorunlu evrensel asgari/azami hacim değildir. Hacim belirsizliği <%5; her hedef bileşik için V≤%70 Vbreakthrough veya ≤%50 Vretention ve geçerli sıcaklık şartı değerlendirilir.',
             'Tablo 1: tüpte numune gazı <40 °C, sıcaklık belirsizliği <2,5 °C. Isıtılan prob kullanılıyorsa baca T+10 °C, en çok 180 °C. Yoğuşma riski varsa doğrudan tren yerine seyreltme varyantı.',
             'Süre, hedef gaz hacmi/Q ve prosesin temsil edilen ortalama süresiyle belirlenir; her VOC için sabit 30 dk yok. Küçük hacim nedeniyle çok kısa örnekleme gerekiyorsa zaman ağırlıklı seyreltme planını değerlendir.'],
            {'Hazırlık':['Bu yöntem gaz fazındaki tekil VOC içindir; FID ile toplam organik karbon ölçümü değildir. CEN/TS 13649:2014 eski EN 13649:2001’in yerini alır; dosya adındaki yalnız aktif karbon ifadesi TD seçeneğini dışlamaz.',
                'Su/solvent yoğuşması riski için bileşim, nem, sıcaklık ve sorbent kapasitesini değerlendir. Sorbent önüne Na₂SO₄ gibi kurutucu yerleştirme; VOC kaybı yapabilir. Tüpte sıvı birikmesine izin verilmez.',
                ('TD tüpü sorbent bileşimi hedef volatiliteye göre seçilir. Çoklu sorbentte örnekleme yönünde zayıf sorbent önce gelir. İki ayrı seri tüp kırılma denetiminde aynı tiptedir; inert bağlantı ve PTFE ferrül kullanılır.' if td else 'Açılmış/kullanılmış aktif karbon tüpü tekrar kullanılmaz. Tüpün yönü, ana/yedek yatağı ve lotu işaretlenir; çözücü geri kazanımının her hedef/karbon lotu için >%80 olması gerekir.'),
                'Saha blankı en az 1/gün; günlük >6 numunede 2, >10 numunede 3 blank. Aynı lot ve açma/kapama işlemi, prob bacaya sokulmadan ve gaz çekilmeden. Analitik blank ile saha blankını ayır.'],
             'Kaçak kontrolü':['Her örneklemeden önce ve sonra probdan hacim ölçere kadar bütün birleşik tren sınanır. Ölçümün en yüksek vakumunda kaçak örnekleme Q’sunun <%5’i veya hacim ölçümü belirsizliğinin altında olmalıdır (Ek A.1.3).',
                'Örnek: 0,1 L/dk için %5, 0,005 L/dk=5 mL/dk eder; 0,57 L/dk EPA büyük tren sınırı bu tüplere uygulanmaz.'],
             'Örnekleme':['Tüp yönü, Q, sayaç başlangıç/sonu, örnekleme süresi ve sayaç T/P kaydedilir; otomatik kompanzasyon yoksa ölçülen hacim T/P ile ilişkilendirilir. Küçük hacimlerde sistem ölü hacmini çekiş öncesi gazla süpür; hacim hesabına gerçek tüp örneklemesini al.',
                'İyi tanımlanmış gazda en az her 10 numunenin 1’inde ve kampanya başına en az 1 numunede yedek kademe ile kırılmayı kontrol et. Bileşimi belirsiz kaynakta daha sık kontrol gerekir; yedek kademe bütün koşullarda keyfi çıkarılmaz.',
                'Tablo 1’e göre arka kademe kütlesi iki kademenin toplamının <%5’i olmalı. §6.2’de “en çok %5” ifadesi de vardır; kart tabloda verilen daha sıkı <%5 kabulünü gösterir. Aşımda sonucu geçerli nicel sonuç gibi kullanma; §9.1/§10 rapor koşullarını uygula.'],
             'Geri kazanım':[('Tüpleri ayırıp inert sızdırmaz kapaklarla hemen kapat. Laboratuvarda desorpsiyon, örnekleme yönünün tersinedir; gerekiyorsa kuru gazla purge örnekleme yönündedir. Numune+purge hacmi kapasiteyi aşmamalı.' if td else 'Tüpü iki ucundan hemen kapat. Laboratuvarda ana ve yedek karbon yatakları ayrı viallere alınır; bunları sahada su/asetonla geri yıkama. Tipik CS₂ hacmi 100 mg karbon için 1 mL’dir; bu laboratuvar ekstraksiyon hacmidir.'),
                ('En az her 10 numunenin 1’i ve kampanya başına en az 1 tüp ikinci kez desorbe edilerek geri kazanım denetlenir. İkinci desorpsiyonda ≥%5 analit varsa işlem eksiktir; sorbent/analiz koşulları değiştirilir (Ek C.1).' if td else 'Partiye/hedefe özgü desorpsiyon verimi ve blank analizi gerekir; kaynağa uygun olmayan çözücüyle standart tarifini genelleme.')],
             'Saklama ve taşıma':['Temiz, hava sızdırmaz ve VOC yaymayan kapta, güneşten uzak, <25 °C. Ahşap, VOC yayan plastik ve yapışkan bant gibi bulaşma kaynaklarından kaçın.',
                '7 gün içinde analiz edilmeyecekse tüpler hava sızdırmaz kapta <4 °C’de tutulur (§6.5.1). Yedi gün mutlak analiz son tarihi değildir; kaynak bu cümlede soğuk saklama şartını başlatır.',
                'Soğuk kap oda sıcaklığına gelmeden açılmaz; kapalı halde dengelenir, ardından tüp çıkarılıp kapağı açılır. TD kapakları en düşük soğutma sıcaklığına ulaşıldığında yeniden sıkılır (§6.5.3).'],
             'Laboratuvara teslim':delivery+['Tüp/lot/sorbent, ana-yedek yönü, Q/V/T/P/süre, blanklar, seyreltme varsa ölçülen oran, saklama sıcaklığı ve zamanlar ile ayrı kademe analiz isteğini bildir.',
                'Saha blankı numuneden çıkarılmaz. Tablo 1’de <%10 emisyon sınırı; §9.1’de sonuç/ELV değerlendirmesi vardır. Numune blankın altındaysa ≤blank raporlanır; birden fazla blankta en yüksek değer esas alınır. Analitik blankın uygulanabilir düzeltmesi ayrı işlemdir.']},
            gaps=['Her hedef VOC için güvenli hacim, sorbent, desorpsiyon verimi ve laboratuvarın gerçek saklama kararlılığı doğrulanmalıdır. Tablo 1’de <40 °C, §6.2 metninde 40 °C’yi aşmama yazımı vardır; kart tablo sınırını korur.'],
            evidence={'Seçim / debi / hacim / sıcaklık':(['L05:8-13,19'],'§5–6, Tablo 1'),
                'Kaçak / doğrudan tren':(['L05:13,21-22'],'§6.4, Ek A.1'),
                'Saklama / blank / kabul':(['L05:13-14,18-20'],'§6.5–6.6, §9–10'),
                'Geri kazanım / sorbent':(['L05:15-17,25-28'],'§7.2, Ek B–C')})
        if td:
            next(n for n in p['train'] if n['id']=='backup')['optional']=False
            p['trainNote']='Bu çizim kırılma kontrolü yapılan seri iki tüplü TD koşusudur. Rutin koşuda yedek tüp kullanımı §9.1’deki kontrol sıklığı ve kaynak bilgisine göre planlanır.'

    # Dinamik seyreltmede iki giriş birleşir; fazla karışım ayrı çıkar.
    p=deepcopy(next(p for p in data if p['id']=='voc_13649_charcoal'))
    p.update(id='voc_13649_dynamic',variant='Dinamik seyreltme — aktif karbon; Ek A.2.1',train=[],
        sources=['L05:8-22,25'])
    p['diagram']=dict(type='dilution',asset='assets/diagrams/voc_13649_dynamic.png',
        shared=[node('source','probe','Baca gazı girişi','Ölçülen Vin; uygun partikül/ısıtma düzeni'),
                node('mixer','splitter','Dinamik karıştırıcı','Temiz kuru gaz ile baca gazı burada birleşir')],
        dilution=node('diluent','meter','Seyreltme gazı girişi','Temiz kuru hava veya N₂; ölçülen sabit Vr'),
        branches=[dict(id='excess',label='Fazla karışım çıkışı',nodes=[node('exhaust','trap','Fazla karışım','Vr + Vin − Vout; güvenli uygun çıkış')]),
                  dict(id='sample',label='Ölçülen analiz kolu',nodes=[node('tube','adsorber','İki yataklı aktif karbon','Ana ve yedek yatak ayrı analiz','Tipik 100 + 50 mg'),
                        node('dryer','trap','Pompa / sayaç koruması','Tüpten sonra uygun kurutma'),meter])])
    p['trainNote']='Ek A.2.1’in dinamik karıştırma ilkesini gösterir; seyreltme girişi ile fazla karışım çıkışı farklı bağlantılardır. Tüm debiler aynı T/P bazında ifade edilir. TD ile kullanım ayrıca kendi sorbent/kapasite koşullarını gerektirir.'
    p['limits'][0]['value']='Tüp kolu 0,1–0,5 L/dk tipik aralığında; baca Vin, seyreltme Vr ve tüp Vout ayrı ölçülür. Vr/Vin her koşulda sabit 0,5/1,0 kabul edilmez.'
    p['limits'][1]['value']='Tüpün seçilen güvenli hacmi ve ölçülen seyreltme faktörü birlikte. Fd=(Vr+Vin)/Vin. Vout bütün karışım debisi değildir; fazla karışım çıkışı nedeniyle Vin=Vout−Vr varsayımı genellikle yanlıştır.'
    p['phases'][0]['items']+=['Temiz kuru seyreltme gazı kaynağını bağla, Vr’yi bilinen sabit debiye ayarla; ölçülen Vin baca gazı ile karıştır. Vout kontrollü tüp koluna, kalan karışım ayrı çıkışa gider. Yoğuşmayı önleyecek oranı kaynağa göre doğrula (Ek A.2.1).']
    p['phases'][2]['items']+=['Seyreltme oranı, debi/T/P ve blank doğrulanır. Tüp gazından bulunan sonuç seyreltme faktörüyle baca gazına geri hesaplanır; kuru/yaş ve referans koşulları aynı bazda ele alınır.']
    p['evidence']+= [dict(field='Seyreltme topolojisi ve oranı',references=['L05:22'],clause='Ek A.2.1, Denklem A.1')]
    p['gaps']+=['Statik torba/lung yöntemi Ek A.2.2’de ayrı bir yöntemdir; bu dinamik çizimin torbalı karşılığı sayılmaz. Karıştırıcının gerçek debi ve örnekleme doğrulaması gerekir.']
    data.append(p)

    p=add('velocity_iso16911_pitot','Hız ve debi','EN ISO 16911-1','2013 / TSE Haziran 2013','Ek A — kalibre Pitot ile noktasal hız',
        ['L04:21-31,33-44'],[],
        ['Ölçülen baca hızı m/s; hacimsel debi q=vort×A. Bu ölçümde impingerle sabit L/dk gaz çekişi ayarlanmaz.',
         'Numune çekiş hacmi yoktur. Gerçek yaş q ve kuru normal q ayrı hesaplanır; normal referans 273,15 K / 101,325 kPa.',
         'Her noktanın baca T’si yoğunluk hesabına girer. Mutlak basınç=Pbar+işaretli statik P; T(K)=T(°C)+273,15.',
         'Her noktada ≥1 dk boyunca en az 3 anlık ΔP okumasının ortalaması veya ≥1 dk elektronik ortalama. Süreç dalgalanması/ortalama hedefi ayrıca planlanır.'],
        {'Hazırlık':['Kesit alanını gerçek iç ölçülerle doğrula; dairesel kesitte en az iki çap. Çizimi ölçmeden doğru kabul etme. Duvar kalınlığı, port derinliği ve sıcaklık etkisini kaydet; alan performans kriteri %2.',
            'Grid ve eş alan noktaları EN 15259’a göre belirlenir. Düz prob yaklaşımı dairesel kesitte teğetseldir. Prob/ekipman kesit tıkanması ≤%5 olmalıdır.',
            'Pitot katsayısı izlenebilir ve kullanım hız aralığını kapsayan kalibrasyondan gelir; tasarım sabiti yeterli değildir. Aynı prob/ekipman birleşimi kalibrasyonda korunur. S-tip için her ölçümde otomatik 0,84 atama.',
            'ΔP<5 Pa veya hız <5 m/s koşullarında Ek B kanatlı anemometre gibi daha düşük belirsizlikli uygun yöntem değerlendirilebilir. Ek A Tablo A.1 minimum ΔP=5 Pa; ölçüm alt sınırının altında kullanma.'],
         'Kaçak kontrolü':['Seri öncesi ve bağlantı açıldığında Pitot/basınç devresini kontrol et. En az baca statik basıncı kadar basınçlandırılıp tapalar kapatıldığında 5 dk basınç kaybı olmamalıdır (§9.3.3).',
            'S-tip ağızlar akışa dik, statik konumdayken iki port farkı <10 Pa olmalıdır. Hasar/çapak/tıkanma/kaçak/çarpılma kalibrasyonu geçersiz kılabilir; ölçüm öncesi ve sonrası gözle kontrol yapılır.'],
         'Örnekleme':['Saha tekrarlanabilirliği önceden sınanır: iki cihaz varsa aynı noktada 5 eşli okuma; tek cihazda art arda 5 adet 1 dakikalık okuma. Tablo 4 hız tekrarlanabilirliği ≤%5.',
            'Herhangi bir noktada teğetsel akış açısı >15° ise etkili girdap kabul edilir; hız ve yönü ölçebilen S/2D/3D cihazla her nokta değerlendirilir. Yön düzeltmesi vc=völçülen×cosθ; bu, cihazın açısal okuma hatasını kendiliğinden düzeltmez ve uygunsuz düzlemi otomatik onaylamaz.',
            'Tablo 4: sensör/akış açısı <15°, probun ölçüm düzlemine pitch açısı ≤10°, konum hatası komşu nokta aralığının ≤%10’u, yoğunluk belirsizliği ≤0,05 kg/m³. Sabit referans prob varsa traversle eşzamanlı kaydet.',
            'S-tip dışındaki ΔP cihazlarında tıkanma kontrolü gerekir. Temizlik öncesi/sonrası ΔP farkı ≤%5; referans debi değişimi ≤%2 veya varyasyon düzeltmesi. Başarısızlık son başarılı kontrolden sonraki ölçümleri geçersiz kılar (§9.6).'],
         'Geri kazanım':['Kimyasal numune fraksiyonu yoktur; ham hız basıncı, nokta konumu, açı, T/P, nem ve gaz bileşimi ile kalibrasyon kayıtları korunur.',
            'Önce her noktada ΔP ortalamasından vi=K√(2ΔPi/ρi) hesapla. Sonra yalnız eş alan gridinde nokta hızlarının aritmetik ortalamasını al. Bütün noktaların ΔP’sini önce ortalayıp tek karekök almak aynı işlem değildir.'],
         'Saklama ve taşıma':['Numune saklama sıcaklığı/analiz bekletme süresi uygulanmaz. Sensörleri temiz, kuru, darbeye karşı korunmuş taşı; saha verisini ham haliyle ve cihaz kimliğiyle sakla.',
            'Kuru normal debi: qn,dry=qwet×Pabs/101,325×273,15/TK×(1−H₂O/100); bu ifadede Pabs kPa’dır. O₂’ye göre debi dönüşümü (21−Ogerçek)/(21−Oref); derişim düzeltmesi bunun tersidir. Aynı bazda kütlesel debi korunur (§10.6).'],
         'Laboratuvara teslim':delivery+['Kesit/kroki, noktalar, kalibrasyon katsayıları ve aralık, hasar/kaçak/tekrarlanabilirlik/tıkanma kontrolleri, açılar, tüm ham ΔP/T/P/nem/bileşim ve belirsizlik bütçesi rapora aktarılır.',
            'Tablo 4 basınç okuma cihazı kalibrasyon belirsizliğine ≤%1 verirken Tablo A.1 ≤%1 veya 20 Pa’dan büyük olanı yazar. Bu iki farklı ifadeyi tek otomatik kabul eşiğine indirme; ölçüm kalite hedefi ve belirsizlik bütçesinde yazılı değerlendir.']},
        gaps=['Bu kart Ek A Pitot uygulamasıdır. Ek B anemometre, Ek C iz gazı ve Ek D enerji hesabı ayrı tekniklerdir; bu karta aynı kabul şartlarıyla birleştirilmez. EN 15259 tam metniyle düzlem/grid koşullarının nihai eşleştirmesi eksiktir.'],
        evidence={'Kurulum / saha kalite / girdap':(['L04:23-28'],'§7, §9; Tablo 3–4'),
            'Hesap / referans koşulları / belirsizlik':(['L04:29-31'],'§10–11'),
            'Pitot kalibrasyonu / ΔP / yoğunluk':(['L04:33-44'],'Ek A.1–A.3; Tablo A.1')})

    for p in data:
        if p['id'] not in ('ambient_pm10','ambient_pm2_5'):continue
        p['reviewState']='sections_checked';p['sourceVersion']='EN 12341:2023 — arşivde BS EN baskısı'
        p['sources']=['D23:8,18-25,28-37']
        phase=lambda title:next(s['items'] for s in p['phases'] if s['title']==title)
        phase('Hazırlık')[:] +=['Örnekleme başlığına uygun 2,3 m³/saat = 38,333… L/dk nominal ORTAM debisi. Dikey bağlantı borusu kıvrımsız, ≤3 m; filtre açık örnekleme çapı 34–44 mm. Filtre en az %99,5 verim @0,3 µm ve uygulamaya uygun malzemede olmalı.',
            'Ön tartım: 19–21 °C / %45–50 RH’de ≥48 saat şartlandır, tart; ≥12 saat sonra tekrar tart. Fark ≤40 µg. Başarısızsa ≥24 saat ek şartlandırma/son kontrol; yine başarısızsa filtreyi reddet. Son iki tartım ortalaması ön kütledir.',
            'En az iki tartım odası blankı tutulur; her tartım oturumunda kütle değişimi ≤40 µg. Terazi çözünürlüğü ≤10 µg, 0–200 mg aralığında kalibrasyon belirsizliği ≤25 µg; her oturumda referans kütle kontrolü yapılır.']
        phase('Kaçak kontrolü')[:]=['Tüm örnekleme hattı yılda bir ve her yeni kurulum/yer değişiminde kaçak kontrolünden geçer. Kaçak >%1 ise bakım ve yeniden test gerekir (§7.9).',
            '§5.1.10 düşük basınç yönteminde sistem ölü hacmi ve basınçtan hesaplanan süre (en çok 2 dk) kullanılır; test üç kez, en yüksek kaçakla değerlendirilir. Hacimsel yöntem yalnız düşük basınç ölçümü teknik olarak yapılamıyorsa kullanılır. Evrensel EPA 0,57 L/dk sınırı atanmaz.']
        phase('Örnekleme')[:] +=['Anlık ortam debisi nominalin ±%5’i, örnekleme ortalaması ±%2’si içinde. En az saatlik debi, süre/hacim, filtre hava T’si, ortam T/P ve filtre depolama T’si kayıtları bulunmalı; filtreler cihazda beklerken de kayıt sürer.',
            'Hedef 24 saat; filtre değişim kaybı, enerji kesintisi, erken tıkanma ve gerçek çalışma süresi kaydedilir. Tıkanmayla erken biten günlük numunede >18 saat kaynakta öneridir; her uygulamada otomatik geçerlilik onayı değildir.',
            'Üretici aralığı yoksa impaksiyon yüzeyi/nozül bakımı PM10’da en az her 30., PM2,5’te her 15. numunede; yüksek yükte daha sık olabilir. Debi kontrolü 3 ayda bir, kalibrasyonu yılda bir; sensor/clock kontrolleri Tablo 5’teki ayrı sıklıklarla.']
        phase('Saklama ve taşıma')[:]=['Filtre ve saha blankını temiz kapalı tutucu/petri, örtülü ve yalıtımlı taşıma kabında koru. Uçucu kaybını ve filtre üzerinde yoğuşmayı önle; sıcaklık kaydını koru. ≤23 °C depolama kaynakta bir seçenektir, bütün numunelere zorunlu evrensel +4 °C kuralı değildir.',
            'Gravimetrik analiz için alımdan itibaren 1 ay içinde tartım odasına al. Tablo 4: örneklenmemiş tartılmış filtre için 2 ay (blank uygun kalırsa daha uzun), cihazdaki örneklenmiş filtre/saha blankı için 1 ay, tartım odasında tartım öncesi 1 ay. Bu farklı adımlar birleştirilerek keyfi toplam analiz süresi oluşturulmaz.',
            'Son tartım: ≥48 saat şartlandırma, ilk tartım; 24–72 saat ek şartlandırma, ikinci tartım. Fark ≤60 µg. Aşımda ≥24 saat ek şartlandır/yeniden tart veya sonucu geçersiz say; tekrar aşım geçersizdir. Son iki tartım ortalaması son kütledir.']
        phase('Laboratuvara teslim')[:] +=['Saha blankı her noktada ve filtre kasetinde en az bir çekiş yapılmamış filtreyle yürütülür. |Son−ilk blank kütlesi|≤60 µg; bireysel saha blankı PM kütlesinden çıkarılmaz (§6.7.3).']
        p['gaps']=['Yerleşim/temsil edicilik ve ulusal izleme planı ölçüm noktasına göre seçilir. İkinci tartımdan vazgeçme ancak laboratuvarın ek belirsizliği hesaplayıp uygunluğunu göstermesiyle mümkündür; bu kart çift tartımlı prosedürü kullanır.']
        p['evidence']=[dict(field='Başlık / debi / süre / veri kaydı',references=['D23:18-25'],clause='§5.1.2–5.1.15'),
            dict(field='Tartım / saklama / blank / sürekli kalite',references=['D23:28-37'],clause='§6–7; Tablo 3–5')]

    for p in data:
        if p['id'] not in ('pah_iso11338_b','pah_iso11338_b_split'):continue
        p['reviewState']='sections_checked';p['sourceVersion']='ISO 11338-1:2003; Part 2:2003 hazırlık/saklama bağlantısı'
        p['sources']=list(dict.fromkeys(p['sources']+['D27:13-15','D28:8-11,14-18']))
        phase=lambda title:next(s['items'] for s in p['phases'] if s['title']==title)
        phase('Hazırlık')[:] += ['Örnekleme öncesi HPLC veya GC-MS analitik yolu, hedef PAH ve sahada eklenen iç standart ile laboratuvarda eklenen geri kazanım standardı ayrı planlanır. Filtreye saha iç standardı eklenmişse çekişten önce ≥2 saat bekletilir (§6.3.2).',
            'Filtre ve adsorban yakalama verimi hedef bileşiklerle doğrulanır. 1–6 m³/saat = yaklaşık 16,7–100 L/dk, Part1 B’de cihaz tasarım aralığıdır; her XAD-2 kartuşuna veya yan kola otomatik hedef debi değildir.']
        phase('Geri kazanım')[:] += ['Part1 §6.3.3: probu sırasıyla aseton, hekzan ve toluenle dikkatle yıka; yapışmış parçacıkları önceden temizlenmiş cam/kuvars yünü sürüntüsüyle al. Bu B varyantında “100 mL aseton+100 mL su” veya “yalnız 200 mL aseton” evrensel standart tarifi verilmez.',
            'Filtre kapalı cam kapta; yoğuşturucu ve adsorban gres kullanılmamış cam tıpalarla kapalı tutulur. İmpinger kullanılmışsa sıvı kahverengi şişeye; aseton/hekzan/toluen yıkamaları bu sıvıya eklenir. Fraksiyonları laboratuvarın analitik planına göre kimliklendir.']
        phase('Saklama ve taşıma')[:]=['Part1 §6.3.3 B saha geri kazanımında filtre, adsorban ve ilgili fraksiyonlar için karanlıkta −7 °C belirtir; bu değer kaynak görüntüsünden kontrol edildi.',
            'Part2 §6.1.4.1 (HPLC) ve §6.2.4.1 (GC-MS): kapalı/ışıktan korunmuş ham numune 0–4 °C’deyse alım bitiminden itibaren 1 hafta içinde EKSTRAKSİYON; −15 °C veya altındaysa 1 ay içinde ekstraksiyon. Bu süreler doğrudan analiz son tarihi değildir.',
            'Part2 kondensatın HCl ile yaklaşık pH2’ye asitlenmesini ve bu durumda en çok 14 gün saklamayı tarif eder. Bu koruma PAH kondensatı içindir; başka parametrelerin koruma işlemi diye genellenmez.',
            'Yoğunlaştırılmış ekstrakt ayrı aşamadır: kapalı kahverengi vial, ışıktan koruma ve <4 °C; 30 gün içinde analiz. Bu 30 gün ham filtre/kartuşa bekletme izni vermez.',
            'Part1’in −7 °C saha ifadesi ile Part2’nin analize hazırlık seçenekleri birbirinin yerine sessizce geçirilmez. Sahadan laboratuvara aşamalar, sıcaklık ve bütün süre başlangıçları numune planında birlikte belirlenir.']
        phase('Laboratuvara teslim')[:] += ['Ham numune/ekstrakt/kondensat ayrımı, alım bitimi/ekstraksiyon/yoğunlaştırma/analiz zamanları, sıcaklık geçmişi, pH ve iç/geri kazanım standartları kaydedilir.',
            'Part2 §6.1.7 HPLC geri kazanımını %50–150 aralığında ister; dışındaysa sonuç reddedilir. Bu HPLC harici standardı PAH sonucuna düzeltme faktörü yapılmaz. GC-MS izotop seyreltme yaklaşımı farklı değerlendirilir.',
            'D28 PDF14’ün normal koşul satırında 1013,25 kPa yazımı görüntüden doğrulandı. Bu, 1013,25 hPa ile aynı basınç değildir: 1,01325 bar=101,325 kPa=1013,25 hPa. Yazım otomatik hesap referansı yapılmaz; uygulanacak normal referans ve kaynak düzeltmesi yazılı planla kesinleştirilir.']
        p['evidence'] += [dict(field='B geri kazanım / saha iç standardı',references=['D27:14-15'],clause='Part1 §6.3.2–6.3.3'),
            dict(field='Ekstraksiyon / analiz / kondensat saklama',references=['D28:10-11,14-18'],clause='Part2 §6.1.4, §6.1.7; §6.2.4')]
        p['gaps']=['Part1 B kartıdır; A seyreltme ve C soğutulmuş prob varyantları burada tamamlanmış sayılmaz. Part1 ve Part2 sıcaklık hükümleri, seçilen laboratuvar analitik yolu ve fraksiyon planıyla yazılı eşleştirilmelidir; uygulama tek otomatik saklama hedefi atamaz.']
