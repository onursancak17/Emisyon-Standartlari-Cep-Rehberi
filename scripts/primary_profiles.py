"""Birincil metinle karşılaştırılan ayrı yöntemler; lisanslı PDF içermez."""


WEB_SOURCES = [
    dict(id='W01', title='US EPA CTM-027 — Ammonia', edition='Taslak / koşullu yöntem, 14.08.1997', pages=10,
         url='https://www.epa.gov/sites/default/files/2020-08/documents/ctm-027.pdf'),
    dict(id='W02', title='CARB Method 425 — Total Chromium and Hexavalent Chromium', edition='28.07.1997', pages=38,
         url='https://ww2.arb.ca.gov/sites/default/files/classic/testmeth/vol3/m_425.pdf'),
    dict(id='W03', title='CARB Method 426 — Cyanide', edition='22.01.1987', pages=23,
         url='https://ww2.arb.ca.gov/sites/default/files/classic/testmeth/vol3/meth426.pdf'),
    dict(id='W04', title='US EPA Method 323 — Formaldehyde', edition='31.05.2023 revizyonu', pages=12,
         url='https://www.epa.gov/system/files/documents/2023-06/Method%20323%202023%20revision.pdf'),
    dict(id='W05', title='CARB Method 5 — Particulate Matter', edition='28.07.1997', pages=32,
         url='https://ww2.arb.ca.gov/sites/default/files/classic/testmeth/vol1/m_5.pdf'),
]


def extend(data, profile, node, imp, meter, delivery):
    # Eski taslaklar yerine yalnız aynı metoda ait karşılaştırılmış kartlar konur.
    replaced = {'hcn_tl115', 'ammonia_ctm027', 'chromium_carb425', 'formaldehyde_epa323', 'h2s_epa11'}
    data[:] = [p for p in data if p['id'] not in replaced]

    def add(*args, evidence, **kwargs):
        p = profile(*args, **kwargs)
        p['reviewState'] = 'sections_checked'
        p['evidence'] = [dict(field=k, references=v[0], clause=v[1]) for k, v in evidence.items()]
        data.append(p)

    add('so2_iso7935','SO₂ — gaz analizörü','ISO 7935','2024, ikinci baskı','Ekstraktif veya baca içi AMS; absorpsiyon treni değildir',
        ['D32:1,11-15'],[],
        ['Seçilen AMS’nin doğrulanmış numune debisi; tek L/dk atanmaz.',
         'Toplanan sıvı numune hacmi yerine zamanla eşleşen gaz derişimi kaydı vardır.',
         'Sistemin sıcak-kuru / sıcak-yaş / seyreltmeli koşullandırmasını gaz matrisine göre seç; yoğuşma ve SO₂ kaybını önle.',
         'Sistem tepki süresi performans kriteri ≤200 s. Bu, tek ölçümün 200 s sürmesi gerektiği anlamına gelmez.'],
        {'Hazırlık':['Su buharı, toz, beklenen SO₂ ve girişim yapan bileşenleri belirle. Isıtmalı filtre gereksinimini ve kısa hattı değerlendir (§8.1).'],
         'Kaçak kontrolü':['Tablo 1: hat/koşullandırma kayıp ve kaçağı ölçülen değerin ≤%2’si; deney D.12–D.13. EPA impinger kaçak debisiyle aynı büyüklük değildir.'],
         'Örnekleme':['Temsilî konum ve gaz homojenliğini doğrula. Ekstraktif ve in situ sistemin ilgili bağlantılarını ayrı uygula.',
                      '24 saatte sıfır/span drift sınırı kullanılan en düşük aralığın üst değerinin ≤%2’sidir. Payda ölçülen derişim değildir.'],
         'Geri kazanım':['Laboratuvar sıvı geri yıkaması uygulanmaz; ham zaman serisi, sıfır/span, drift, aralık ve olay kayıtlarını koru.'],
         'Saklama ve taşıma':['Bu düzende kimyasal numune saklama süresi yoktur; veri ve kalibrasyon kayıtlarının bütünlüğünü koru.'],
         'Laboratuvara teslim':['Derişim, metot/sürüm, QA/QC ve belirsizlik kayıtlarını rapor birimine teslim et. §8.3 kütle dönüşümü 0 °C / 101,325 kPa içindir; kuru/yaş baz ayrıca düzeltilir.']},
        gaps=['Tablo 1’in bütün performans deneyleri ve kurulu/taşınabilir sistemin kullanım planı ayrıca tamamlanmalı.'],
        evidence={'Performans / drift':(['D32:12-13'],'§7; Tablo 1'), 'Yer / koşullandırma / baz':(['D32:11-15'],'§6, §8–9')})
    data[-1]['trainNote']='Bu kartta impinger çizimi yoktur: ekstraktif analizör hattı veya in situ optik sistem seçilir.'

    for third_acid in (False, True):
        add('ammonia_ctm027_'+('acid3' if third_acid else 'empty3'), 'Amonyak', 'EPA CTM 027', '14.08.1997 — koşullu / taslak',
            'İn-stack filtre; üçüncü şişe '+('asitli — yüksek yük / kırılma kontrolü' if third_acid else 'boş'),
            ['W01:1-6'], [node('probe','probe','Baca içi başlık','Cam/kuvars nozül'),
             node('filter','filter','Baca içi filtre','Bağlayıcısız cam elyaf; Method 17 düzeni'),
             node('line','probe','Prob / bağlantı','Cam/kuvars numune hattı'),
             imp(1,'0,1 N H₂SO₄','100 mL'),imp(2,'0,1 N H₂SO₄','100 mL'),
             imp(3,'0,1 N H₂SO₄' if third_acid else 'Başlangıçta boş','100 mL' if third_acid else ''),
             imp(4,'Ön tartımlı silika jel','200–300 g'),meter],
            ['İzokinetik; evrensel sabit debi yok.','Hedef derişim ve analiz tayin sınırından planlanır.',
             'Filtre/ön hat baca sıcaklığında veya biraz üzerinde; şişeler buz-su banyosunda.',
             'Hedef hacme göre; 3 ölçüm. Blankta 1 saat gaz çekilmeden bekletme, ölçüm süresi değildir.'],
            {'Hazırlık':['Yöntem kömürlü kazanda doğrulanmıştır; başka kaynakta uygulanabilirlik doğrulaması gerekir. Banyo sıvının en az 10 cm üstüne çıksın; 10 dk soğut.'],
             'Kaçak kontrolü':['Method 17 §4.1.4 bağlantısını uygula; test vakumu ve sonucu kaydet.'],
             'Örnekleme':['Üçüncü şişeye asit seçeneğini yüksek NH₃/yüksek debide kırılmayı değerlendirmek için kullan.'],
             'Geri kazanım':['1–3 numaralı şişeyi ayrı HDPE kaplara, kendi deiyonize su yıkamasıyla al. Her fraksiyonu laboratuvarın 250 mL son hacmi için ≤230 mL tut. Aseton kurutma yıkamasını numuneye katma; filtreyi sakla.',
                              'Filtre arkası/prob bağlantısı ve prob yıkama fraksiyonlarını Tablo A-1’deki asit/su sırasıyla ayrı geri kazan; yalnız şişe sıvılarını teslim etmek tam geri kazanım değildir.'],
             'Saklama ve taşıma':['Buzlu soğutucuda taşı; 4 °C’de, dondurmadan sakla; 2 hafta içinde analiz et. Filtreyi temiz petride serin/kuru tut.'],
             'Laboratuvara teslim':delivery+['Üç sıvı fraksiyonu, filtre, asit blankı, hacimler ve zamanları bildir.']},
            gaps=['Diğer kaynak tipleri ve tüm Method 17 bağlantılı koşulların uygulama yeterliliği ayrıca doğrulanmalı.'],
            evidence={'Düzen / dolum':(['W01:2-4'],'§1–2'), 'Debi / hacim / süre':(['W01:4-5'],'§3.1–3.5'),
                      'Sıcaklık / geri kazanım':(['W01:4-5'],'§3.2–3.4'), 'Saklama / teslim':(['W01:5-7'],'§3.4, §4.1; Tablo A-1')})

    add('formaldehyde_epa323','Formaldehit','EPA Method 323','31.05.2023','Üç midget impinger; doğalgaz yakılan sabit kaynaklar',
        ['W04:1-7'],[node('probe','probe','Prob ve hat','Isıtma zorunlu değil; yoğuşan madde geri kazanılır'),
         imp(1,'Başlangıçta boş — kondensat tutucu'),imp(2,'Reaktif su','20 mL'),
         imp(3,'Silika jel','Metinde sabit gram değeri verilmez'),meter],
        ['0,2–0,4 L/dk; 0,4 L/dk aşılmaz.','Beklenen derişim ve tayin sınırına göre.',
         'Isıtılmış numune hattı gerektirmez; numuneyi buz üzerinde koru.','Hedef hacme göre; sabit 30 dk atanmaz.'],
        {'Hazırlık':['Doğalgaz yakılan kaynak kapsamını kontrol et. Şişeleri dolum sonrası 0,5 g hassasiyetle tart.'],
         'Kaçak kontrolü':['Ön/son kaçak, planlanan/gerçek debinin %2’sinden küçük olmalı.'],
         'Örnekleme':['Debi ve DGM sıcaklığını 5–10 dakikada bir kaydet; geri yıkamadan önce son tartımı yap.'],
         'Geri kazanım':['Prob, hat ve kondensatı suyla geri kazan. Yıkama genellikle ≤10 mL; uzun hattın tam geri kazanımı önceliklidir. Amber, PTFE kapaklı 40 mL VOA kullan; gerekirse büyük kap seç, boşluğu reaktif suyla tamamla ve hacmi kaydet.'],
         'Saklama ve taşıma':['Buz üzerinde taşı/sakla, mümkün olan en kısa sürede analiz et. Bu metinde evrensel sayısal azami bekletme süresi verilmez.'],
         'Laboratuvara teslim':delivery+['Hacim artışı ve tayin sınırı etkisini bildir; en az bir çift numune kontrolünü kaydet.']},
        gaps=['Kapsam dışı prosesler ve bütün analitik kalite kriterleri ayrıca değerlendirilmeli.'],
        evidence={'Düzen / dolum':(['W04:2-3'],'§6–7'),'Debi / kaçak / kayıt':(['W04:3-5'],'§8'),
                  'Geri kazanım / saklama':(['W04:5-6'],'§8.3–8.4')})

    add('h2s_epa11','Hidrojen sülfür','EPA Method 11','03.08.2017','Rafineri yakıt gazı; beş midget impinger',
        ['D04:1-8'],[node('probe','probe','Yakıt gazı hattı','Kapsama uygun güvenli basınçlı gaz bağlantısı'),
         imp(1,'%3 H₂O₂','15 mL'),imp(2,'Başlangıçta boş'),
         imp(3,'Metoda göre hazırlanmış CdSO₄ çözeltisi','15 mL'),imp(4,'Metoda göre hazırlanmış CdSO₄ çözeltisi','15 mL'),
         imp(5,'Metoda göre hazırlanmış CdSO₄ çözeltisi','15 mL'),
         node('dryer','trap','Kurutma tüpü','Silika jel','En fazla 30 g'),meter],
        ['Yaklaşık 1 L/dk; sabitlik ±%10.','Gerçek debi ve süreden / sayaçtan belirlenir.',
         'İmpingerler buz-su banyosunda.','En az 10 dk; sonra ayrı 15 dk temiz hava geçirme.'],
        {'Hazırlık':['30 mL midget şişeler; ilk şişeye peroksit, 3–5’e CdSO₄. Basınçlı yakıt gazında pompa normalde gerekmez.',
                     'CdSO₄ absorbanı §7.1.1: 41 g 3CdSO₄·8H₂O + 15 mL 0,1 M H₂SO₄, deiyonize/distile suyla 1 L; pH 3 ±0,1. 10 damla Antifoam B; kullanılmazsa §11.2 geri kazanımı değişir.'],
         'Kaçak kontrolü':['25 cm su sütununda basınç düşüşü 1 dakikada ≤1 cm. Pompa kullanılırsa onun ek kaçak testini de yap.'],
         'Örnekleme':['Hattı 1–2 dk ön süpür. Son CdSO₄ şişesinde sararma tükenme göstergesidir: ölçüm geçersizdir.'],
         'Geri kazanım':['Ölçüm sonrası aktif karbonla temizlenmiş havayı 1 L/dk, 15 dk geçir. Peroksit fraksiyonunu ayır; 3–5’i suyla 500 mL iyot balonuna geri kazan; §11.2 alternatifini gerektiğinde kontrol et.'],
         'Saklama ve taşıma':['Isıdan ve doğrudan güneşten koru. Sayısal azami bekletme süresi bu kartta doğrulanmadı.'],
         'Laboratuvara teslim':delivery+['Son şişenin renk kontrolünü, süpürme süresini ve CdSO₄ fraksiyonunu bildir.']},
        gaps=['CdSO₄ hazırlama ve titrasyon ayrıntıları §7 ve §11 ile; sayısal bekletme süresi laboratuvarla tamamlanmalı.'],
        evidence={'Kapsam / düzen':(['D04:1-4,6'],'§1, §6–8.1'),'Debi / süre / kaçak':(['D04:6-7'],'§8.2–8.4'),
                  'Geri kazanım / saklama':(['D04:7-8'],'§8.5–8.6')})

    add('chromium_carb425','Krom(VI)','CARB Method 425','28.07.1997','İki alkali şişeden sonra filtre; toplam Cr ve Cr(VI)',
        ['W02:11-14,22-24','W05:9-12'],[node('probe','probe','Cam nozül / cam iç prob','Numuneye temas eden yüzeylerden Cr bulaşmasını önle'),
         imp(1,'0,1 N NaOH','100 mL'),imp(2,'0,1 N NaOH','100 mL'),
         node('filter','filter','Şişelerden sonra filtre','PTFE kaplı cam elyaf'),
         node('dryer','trap','Silika jel nem tutucu','CARB Method 5 bağlantılı ön tartımlı silika jel','200–300 g'),meter],
        ['İzokinetik; sabit debi atanmaz.','Ön plan: hedef derişim ve tayin sınırı.',
         'Buz banyosu; numunenin pH’ı örnekleme/taşımada >8.','En az 3 ölçüm; CARB 5 §4.1.2’de nokta başına ≥2 dk; gerekli toplam hacim de sağlanır.'],
        {'Hazırlık':['Aynı parti taze 0,1 N NaOH kullan; yüksek partiküllü kaynakta uygulanabilirlik gösterilmemiştir.'],
         'Kaçak kontrolü':['CARB 5 §4.1.4: ön/son test zorunlu; sınır min(%4 ortalama debi, 0,57 L/dk). Vakum koşullarını da uygula.'],
         'Örnekleme':['Filtre şişelerden sonradır; en az bir saha blankında tüm işlemler yapılır, kaynak gazı çekilmez.'],
         'Geri kazanım':['24 saat içinde geri kazan. Probu ≥100 mL 0,1 N NaOH ile yıka; ölçüp Cr(VI)/toplam Cr için böl. İmpinger yıkaması gerekmez. Yüksek derişimde iki şişe birleştirilir, filtre ≥30 dk ekstrakte edilip bölünür; düşük derişimde §13.3.2’ye göre ayrı tut.'],
         'Saklama ve taşıma':['Geri kazanım sonrası ≤4 °C, analiz öncesi en fazla 2 hafta; pH >8 koşulunu koru.'],
         'Laboratuvara teslim':delivery+['pH, geri kazanım zamanı ve her bölüntünün hacmini bildir.']},
        gaps=['Metot bağlantıları ve kaynağa özgü performans protokolü ayrıca uygulanmalı; tüm analitik adımlar bu kartta yoktur.'],
        evidence={'Düzen / dolum':(['W02:13,22-24','W05:10'],'§7.1, §12–13; CARB 5 §4.1.3'),
                  'Kaçak / süre':(['W05:9-12'],'§4.1.2–4.1.4'),'Geri kazanım / saklama':(['W02:11,22-24'],'§4.1, §12–13')})

    add('cyanide_carb426','Siyanür / HCN','CARB Method 426','22.01.1987','Gaz ve aerosol siyanürleri; toplam siyanür',
        ['W03:2-7,9-13','W05:9-12'],[node('probe','probe','Nozül / prob','CARB 5 bağlantılı izokinetik düzen'),
         node('filter','filter','Cam elyaf filtre','Laboratuvardaki Whatman 42 ile karıştırma'),
         imp(1,'0,1 N NaOH','100 mL'),imp(2,'0,1 N NaOH','100 mL'),imp(3,'Başlangıçta boş'),
         imp(4,'Ön tartımlı silika jel','200–300 g'),meter],
        ['İzokinetik; sabit debi atanmaz.','Gaz hacmi ile geri kazanılan sıvı hacmi farklıdır.',
         'CARB 5 bağlantılı ısıtma/soğutma; TL115’teki <42 °C burada bağımsız norm olarak doğrulanmadı.',
         'CARB 5 §4.1.2: nokta başına ≥2 dk; toplam süre ve hacim kaynak planına bağlı.'],
        {'Hazırlık':['Yalnız gaz HCN türlemesi değildir. İlk/üçüncü/dördüncü şişe modifiye, ikinci standart tiptir. Yüksek CO₂’de §4.1.2 alternatifini ayrıca değerlendir.'],
         'Kaçak kontrolü':['CARB 5 §4.1.4 ön/son ve değişim testlerini uygula; kabul min(%4 Q, 0,57 L/dk).'],
         'Örnekleme':['Siyanürü sahada asitleme; korumada pH ≥12 gerekir.'],
         'Geri kazanım':['Filtreyi 50 mL 0,1 N NaOH içeren cam kaba al. Prob/nozülü 0,1 N NaOH ile geri kazan. İlk üç şişe fraksiyonunu koru; silika jelle karıştırma.',
                         'Oksidanı KI-nişasta kâğıdıyla kontrol et. Mavi sonuçta askorbik asitle gider, ardından 0,6 g/L ekle. Koruyucu 10 N NaOH: numunenin her litresine 2 mL ve pH ≥12 kontrolü.'],
         'Saklama ve taşıma':['§4.2.3 alkaliye dayanıklı yaklaşık 1 L PE kap ve uygun PTFE/alkali dayanımlı kapak astarı verir; filtre ve ön prob yıkaması için §6.2.1–2 cam kap belirtir. Fraksiyonları kendi kap kuralıyla tut, seviyeyi işaretle ve sızdırmaz kapat.',
             'İncelenen Method 426 numune/koruma maddelerinde sayısal saklama sıcaklığı ve azami bekletme süresi verilmez. Kaynak pH≥12 ve oksidan giderme koşulları korunur; analiz yönteminin/laboratuvarın kabul planı süre ve sıcaklığı ayrıca tanımlamalıdır. Başka siyanür yönteminin 14/28 gününü otomatik aktarma.'],
         'Laboratuvara teslim':delivery+['pH, oksidan testi, koruyucu dozları ve fraksiyon hacimlerini bildir.']},
        gaps=['§6.2.4 yıkama kabı numarasında metin içi çelişki var: silika jel kabına sıvı eklenmez; fraksiyon planı laboratuvarla çözülmeden uygulama talimatı tamamlanmış sayılmaz.',
              'Metnin sayısal vermediği saklama T/süre koşulları geçerli analitik yöntem ve laboratuvar kabul planıyla belirlenmelidir.'],
        evidence={'Düzen / dolum':(['W03:3-4,9-10'],'§4.1, §6.1'),'Geri kazanım / koruma':(['W03:10-13'],'§6.2'),
                  'Kaçak / süre':(['W05:9-12'],'§4.1.2–4.1.4')})
