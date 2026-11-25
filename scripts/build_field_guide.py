"""Kaynak kontrollü başlangıç veri paketi; kaynak PDF'leri yayımlamaz."""
import json
from pathlib import Path
from primary_profiles import extend, WEB_SOURCES

ROOT = Path(__file__).resolve().parents[1]


def node(key, kind, label, content='', amount='', optional=False):
    return dict(id=key, kind=kind, label=label, content=content, amount=amount, optional=optional)


def imp(n, content, amount='', optional=False):
    return node(f'i{n}', 'impinger', f'İmpinger {n}', content, amount, optional)


probe = node('probe', 'probe', 'Nozül ve prob', 'Metoda uygun malzeme / sıcaklık')
filt = node('filter', 'filter', 'Filtre', 'Metoda uygun filtre tutucu')
meter = node('meter', 'meter', 'Çekiş ve hacim ölçümü', 'Pompa, DGM ve debi kontrol grubu; iç bağlantı sırası cihaz şemasına göre')
gel = lambda n: imp(n, 'Ön tartımı yapılmış silika jel', 'yaklaşık 200–300 g')
water_train = [imp(1, 'Su', '100 mL'), imp(2, 'Su', '100 mL'), imp(3, 'Başlangıçta boş'), gel(4)]
phases = ['Hazırlık', 'Kaçak kontrolü', 'Örnekleme', 'Geri kazanım', 'Saklama ve taşıma', 'Laboratuvara teslim']


def profile(id, parameter, method, version, variant, sources, train, limits, notes, state='train_checked', gaps=None):
    return dict(id=id, scope='Emisyon', parameter=parameter, method=method, sourceVersion=version, variant=variant,
                sources=sources, reviewState=state, train=train, limits=[dict(label=k, value=v) for k, v in zip(
                    ['Çekiş debisi', 'Toplam çekiş hacmi', 'Sıcaklık', 'Ölçüm süresi'], limits)],
                phases=[dict(title=t, items=notes.get(t, ['Bu aşamanın ayrıntılı kaynak doğrulaması henüz tamamlanmadı.'])) for t in phases],
                gaps=gaps if gaps is not None else ['Bu kartın doğrulaması şema ve belirtilen kaynak maddeleriyle sınırlıdır; tam yöntem yeterlilik incelemesi sürüyor.',
                    'Kaynak sürümünün güncel yürürlük durumu ve laboratuvarın onaylı uygulaması ayrıca kontrol edilmeli.'])


common_delivery = ['Tesis, baca/nokta, tarih, başlangıç–bitiş, metot/sürüm, numuneci ve fraksiyon kimliklerini etiketle.',
                   'Numune kabı, kapak, miktar, blank, mühür, taşıma koşulu, teslim saati ve teslim alanı izlenebilir teslim formuna kaydet.']
data = []
data.append(profile('moisture_epa4', 'Nem', 'EPA Method 4', '07.10.2020', 'Referans yöntem — dört impinger',
    ['D08:4-6', 'D09:8'], [probe, node('filter', 'filter', 'Filtre (gerektiğinde)', 'Yoğuşmayı önleyen ısıtma'), *water_train, meter],
    ['En fazla 21 L/dk; sabit debiden ±%10. İzokinetik metotla eşzamanlıysa izokinetik koşullar esas.',
     'En az 0,60 standart m³. DGM hacmi ile referans koşullara düzeltilmiş hacmi ayrı tut; doğrudan 0 °C Nm³ diye yeniden etiketleme.',
     'Prob ve gerekiyorsa filtre yaklaşık 120 °C; silika jel çıkışı <20 °C; buz + su banyosu.',
     'Asgari hacmi sağlayacak süreyi planla. Kirleticiyle eşzamanlı belirlemede, ilgili istisnalar dışında aynı toplam süre.'],
    {'Hazırlık':['İlk iki şişeye su, üçüncüye sıvı koyma, dördüncüye tartılmış silika jel yerleştir. 100 mL dolumları Method 5 §8.3.1 bağlantısındandır.',
                 'Başlangıç impinger kütlelerini en az 0,5 g çözünürlükle kaydet; DGM başlangıcı, kalibrasyon, sıcaklık ve basıncı kontrol et.'],
     'Kaçak kontrolü':['Ön kaçak testi önerilir; son kaçak testi zorunludur. Parça değiştirmeden önce test yap.',
                       'Kabul sınırı: ortalama örnekleme debisinin %4’ü ile 0,57 L/dk değerinden küçük olanı. Son testi ölçümde ulaşılan en yüksek vakuma eşit veya daha yüksek vakumda yap.'],
     'Örnekleme':['Metoda uygun travers noktalarında eşit süre çekiş yap; her süre aralığında DGM okumalarını kaydet.',
                  'Prob önünde yoğuşmayı önle, soğutmayı ve silika jel çıkış sıcaklığını izle. Debi, süre ve hacmi ayrı kaydet.'],
     'Geri kazanım':['Son DGM okumasını ve son kaçak sonucunu kaydet; su ve silika jel kütle artışını belirle.'],
     'Saklama ve taşıma':['Sadece nem tayininde sonuç sahada kütle/hacim ölçümüyle belirlenebilir. Kirleticiyle birlikte örneklenmişse o kirleticinin fraksiyon ve taşıma kurallarını uygula.'],
     'Laboratuvara teslim':common_delivery + ['Ham sayaç hacmi, referans koşullardaki hacim, tartımlar, gaz sıcaklığı/basıncı ve kaçak sonuçlarını aktar.']}))

halogen_notes = {
 'Hazırlık':['İsteğe bağlı ilk kondensat şişesi kısaltılmış giriş boruludur; asit şişeleri standart, alkali ve silika şişeleri modifiye Greenburg–Smith tipindedir.',
             'Prob/filtre bölümünü 120–134 °C aralığında tut; uygun alt mevzuat veya onaylı istisnayı ayrıca kontrol et.'],
 'Kaçak kontrolü':['EPA Method 5 §8.4.2–8.4.4 bağlantılı ön, değişim ve son kaçak prosedürlerini uygula.'],
 'Örnekleme':['İzokinetik çekişi koru. Kondensat şişesi dolarsa boşaltılan numuneyi koru; yeniden eklenen 50 mL absorbanı nem hesabında dikkate al.',
              'Filtrede/siklonda sıvı varsa metottaki ölçüm sonrası nem uzaklaştırma koşulunu değerlendir.'],
 'Geri kazanım':['Kondensat + asit şişelerini hidrojen halojenür fraksiyonu olarak; alkali şişeleri halojen fraksiyonu olarak ayrı geri kazan. Asit ve alkali fraksiyonları birleştirme.'],
 'Saklama ve taşıma':['Metotta belirtilen sızdırmaz numune kaplarını kullan; sıvı seviyesini işaretle. Sayısal saklama sıcaklığı ve analiz bekletme süresinin bu kartta doğrulaması tamamlanmadı.'],
 'Laboratuvara teslim':common_delivery + ['Asit/alkali fraksiyonları, yıkamalar ve reaktif blanklarını ayrı kimlikle bildir.']}
data.append(profile('halogen_epa26a', 'Klor / halojenler', 'EPA Method 26A', '07.10.2020', 'Hidrojen halojenürler ve halojenler; kondensat şişesi isteğe bağlı',
 ['D06:4,6-8'], [probe, filt, imp(1, '0,1 N H₂SO₄ / kondensat tutucu', '50 mL', True),
 imp(2, '0,1 N H₂SO₄', '100 mL'), imp(3, '0,1 N H₂SO₄', '100 mL'),
 imp(4, '0,1 N NaOH', '100 mL'), imp(5, '0,1 N NaOH', '100 mL'), gel(6), meter],
 ['İzokinetik; sabit bir L/dk değeri atanmaz.', 'Hedef tayin sınırı, koşullar ve metot planıyla belirlenir.',
  'Prob / filtre 120–134 °C; ilgili onaylı istisnalar saklıdır.', 'Bu kartta evrensel sabit süre tanımlanmadı.'], halogen_notes))

fluor_notes = {
 'Hazırlık':['Dört impinger kullanılır. Dolumlar Method 5 §8.3 bağlantısına göre: 100 mL su + 100 mL su + boş + tartılmış silika jel.',
             'Filtre konumunu saha formuna yaz. Ön filtre seçeneğinde 20-mesh paslanmaz destek koşulunu kontrol et.'],
 'Kaçak kontrolü':['Method 5 §8.4 bağlantılı kaçak testlerini uygula.'],
 'Örnekleme':['İzokinetik debi 28 L/dk altında olmalıdır. Gerekli ısıtmada prob / filtre 120 ±14 °C sınırını aşma.',
              'Florür numunesi ile silika jel nem fraksiyonunu ayrı tut.'],
 'Geri kazanım':['Filtre ve numuneye temas eden prob / ilk üç impinger / uygun filtre tutucu yüzeylerini metottaki suyla yıkama prosedürüne göre nicel geri kazan.',
                'Numune polietilen kabında toplanır. Kullanılmamış filtre ve eş hacim su ile numune blankı hazırlanır.'],
 'Saklama ve taşıma':['Kabı sızdırmaz kapat, sıvı seviyesini işaretle. Bu kartta sayısal bekletme süresi doğrulanmadı; başka bir metodun süresini aktarma.'],
 'Laboratuvara teslim':common_delivery + ['Numune, blank ve silika jel kayıtlarını birbirinden ayır.']}
for front in (False, True):
    train = [probe, *([filt] if front else []), *water_train[:3], *([] if front else [filt]), water_train[3], meter]
    data.append(profile('fluoride_epa13a_'+('front' if front else 'rear'), 'Flor / florür', 'EPA Method 13A', '03.08.2017',
       'Filtre probdan sonra — alternatif' if front else 'Filtre 3. ve 4. impinger arasında', ['D05:2,5-7', 'D09:8'], train,
       ['İzokinetik, <28 L/dk.', 'Tayin sınırı ve örnekleme planına bağlı; bu kartta sabit asgari hacim doğrulanmadı.',
        'Gerekli ısıtmada 120 ±14 °C; yoğuşma kontrolü.', 'Süre, hedef hacim ve izokinetik çekişe göre planlanır.'], fluor_notes))

metal_notes = {
 'Hazırlık':['Cam ekipmanın temizlik / asit yıkama işlemini Method 29 §8.1.1’e göre tamamla; filtre ve bağlantılarda metal bulaşmasını önle.',
             'İlk boş şişe, beklenen nem toplaması yaklaşık 100 mL altında ise metot koşullarıyla çıkarılabilir.'],
 'Kaçak kontrolü':['Method 5 bağlantılı ön, parça değişimi ve son testlerini uygula; PTFE veya bulaşma yapmayan sızdırmazlık kullan.'],
 'Örnekleme':['İzokinetik örnekle; debi, toplam hacim, sıcaklık, vakum ve noktaları kaydet.',
              'Cıva varsa permanganat yakalama durumunu izle. Asitli peroksit ile asitli permanganatı karıştırma.'],
 'Geri kazanım':['Filtre, prob yıkaması, ilk üç impinger fraksiyonu ve cıva fraksiyonlarını metot numaralarıyla ayır.',
                'Prob / ön yüzey yıkamasında toplam 100 mL 0,1 N HNO₃; ilk üç şişe ve bağlantı yıkamasında ayrı toplam 100 mL 0,1 N HNO₃ kullanımı §8.2.7–8.2.8’dendir.',
                'Cıva geri kazanımında 5A / 5B / 5C farklı kaplardır. Tam ayrıntı ve basınç oluşumu önlemleri için §8.2.9 kontrolü zorunludur; tek kaba birleştirme.'],
 'Saklama ve taşıma':['Sıvı seviyelerini işaretle, kap kimliklerini ve reaktif blanklarını koru. Cıva kaplarının kapanma/taşıma düzenini metot ve laboratuvarla doğrula.',
                       'Bu kartta sayısal saklama sıcaklığı / bekletme süresi tamamlanmadı.'],
 'Laboratuvara teslim':common_delivery + ['Hedef metal listesi, cıvanın dahil olup olmadığı, filtre ve her yıkama fraksiyonunu açıkça belirt.']}
for hg in (True, False):
    train = [probe, filt, imp(1, 'Kondensat tutucu; başlangıçta boş', '', True),
       imp(2, '%5 HNO₃ / %10 H₂O₂ (hacim/hacim)', '100 mL'), imp(3, '%5 HNO₃ / %10 H₂O₂ (hacim/hacim)', '100 mL')]
    if hg:
        train += [imp(4, 'Başlangıçta boş'), imp(5, '%4 KMnO₄ (kütle/hacim) / %10 H₂SO₄ (hacim/hacim)', '100 mL'), imp(6, '%4 KMnO₄ (kütle/hacim) / %10 H₂SO₄ (hacim/hacim)', '100 mL')]
    train += [gel(7), meter]
    data.append(profile('metals_epa29_'+('hg' if hg else 'no_hg'), 'Ağır metaller', 'EPA Method 29', '02.08.2017',
        'Cıva dahil' if hg else 'Cıva analizi yok — 4, 5 ve 6 çıkarılır', ['D07:6-7,11-14'], train,
        ['İzokinetik; sabit debi atanmaz.', 'Tayin sınırı ve örnekleme planı; evrensel sabit hacim tanımlanmadı.',
         'Method 5 bağlantılı ısıtma koşulları; sayısal alanın ek doğrulaması bekleniyor.', 'Metot ve hedef hacimle planlanır.'], metal_notes))

for dioxin in (False, True):
    pid = 'dioxin_en1948_filter' if dioxin else 'pah_iso11338_b'
    method = 'EN 1948-1' if dioxin else 'ISO 11338-1'
    train = [probe, filt, node('condenser', 'condenser', 'Yoğuşturucu', 'Gaz çıkışı <20 °C'),
        node('adsorber', 'adsorber', 'Katı adsorban', 'Doğrulanmış adsorban / kartuş; ör. XAD-2' if not dioxin else 'Seçilen düzeneğe uygun doğrulanmış katı adsorban', 'Sabit bir evrensel gram değeri yok'),
        node('condensate', 'trap', 'Kondensat kabı', 'Bu varyantta adsorbandan sonra'), meter]
    notes = {
      'Hazırlık':['Bu çizim akış bölünmesi olmayan filtre–yoğuşturucu–katı adsorban varyantıdır; diğer metotların impinger sayısını buraya aktarma.',
                  'Adsorban miktarını, boyutunu ve yakalama verimini ekipmanın doğrulanmış düzeneği ve hedef bileşiklere göre belirle.'],
      'Kaçak kontrolü':['Ön / son ve gerekli yer değişimi kaçak testlerini seçilen metot prosedürüyle kaydet.'],
      'Örnekleme':['İzokinetik koşulları ve yoğuşturucu çıkışını izle. Akış bölücü kullanılan düzenek bu çizimde yoktur; yan kol debisi ana kol debisi yerine kullanılamaz.'],
      'Geri kazanım':['Filtre, adsorban, kondensat ve numuneye temas etmiş yüzeylerin yıkamaları numune bütünlüğüne dahildir; fraksiyonları seçilen yönteme göre etiketle.'],
      'Saklama ve taşıma':[],
      'Laboratuvara teslim':common_delivery + ['Adsorban partisi, eklenen işaretli standart / geri kazanım bilgisi ve blankı bildir.']}
    if dioxin:
        notes['Hazırlık'] += ['Filtre ve/veya adsorbana ¹³C₁₂ işaretli örnekleme standardı ekleme ve geri kazanım koşullarını §7.2’ye göre planla.']
        notes['Örnekleme'] += ['En az 15 dakikada bir baca hızı/sıcaklığı, çekiş, filtre ve adsorban sıcaklığı kaydı; örnekleme boyunca O₂ kaydı (§9.3.4).']
        notes['Saklama ve taşıma'] = ['Arşiv EN 1948-1:2006 §9.3.5.2: karanlıkta, oda sıcaklığını (yaklaşık 25 °C) aşmadan sakla; tüm kaplar için teslim zinciri tut.']
        notes['Geri kazanım'] += ['Saha blankı ölçüm serisinden önce aynı yerde kurulur; prob bacaya sokulmaz, gaz çekilmez, kaçak testi yapılır (§7.3).']
        limits = ['Düzeneğin validasyon aralığında izokinetik; evrensel sabit debi yok.', 'Hedef derişim / tayin sınırı / geçerli metot planı.',
                  'Filtre çiy noktasının üstünde ve <125 °C; yoğuşturucu sonrası <20 °C.', 'İlgili mevzuat ve örnekleme planıyla doğrulanacak; bu kartta sabit süre atanmadı.']
    else:
        notes['Kaçak kontrolü'] = ['§6.3.2’de iki alternatif test vardır; kaçak normal örnekleme debisinin %5’inden küçük olmalı.']
        notes['Saklama ve taşıma'] = ['Arşiv ISO 11338-1:2003 §6.3.3 metni filtre, adsorban ve ilgili fraksiyonlar için ışıktan koruma ve −7 °C soğuk saklama belirtir. Bu arşiv değeri otomatik +4 °C’ye çevrilmez; geçerli sürüm ve laboratuvar uygulaması doğrulanmalı.']
        limits = ['İzokinetik; cihaz düzenine bağlı. Metindeki 1–6 m³/saat olası cihaz aralığıdır, tüm XAD kartuşlarına uygulanacak debi değildir.',
                  'Hedef PAH listesi ve tayin sınırına göre.', 'Filtre çiy noktasının üstünde, baca sıcaklığından yüksek olmayacak; yoğuşturucu çıkışı <20 °C, soğutucu akışkan ≥0 °C.',
                  'Hedef hacim ve doğrulanmış yakalama verimine göre planlanır.']
    data.append(profile(pid, 'Dioksin / furan' if dioxin else 'PAH', method, '2006' if dioxin else '2003',
        'Filtre / yoğuşturucu / katı adsorban; akış bölünmesiz', ['D25:15,21-26'] if dioxin else ['D27:13-15'], train, limits, notes))

data.append(profile('acid_epa8', 'Sülfürik asit / SO₂', 'EPA Method 8', '14.01.2019', 'Filtre ilk ve ikinci impinger arasında',
 ['D10:2,4-7'], [probe, imp(1, '%80 izopropanol', '100 mL'), node('filter', 'filter', 'Isıtılmayan filtre', '1. ve 2. şişe arasında'),
 imp(2, '%3 H₂O₂', '100 mL'), imp(3, '%3 H₂O₂', '100 mL'), imp(4, 'Silika jel', 'yaklaşık 200 g'), meter],
 ['İzokinetik; en fazla 30 L/dk (§8.6.1).', 'Örnekleme planı / tayin sınırı.',
  'Cam probda görünür yoğuşmayı önleyen en düşük ısıtma; filtre tutucuyu ısıtma.', 'Metot ve plan; ölçüm sonrası 15 dk temiz hava geçirme işlemi ayrı bir aşamadır.'],
 {'Hazırlık':['Metal iç prob kullanma; filtreyi kesinlikle ilk impingerin önüne yerleştirme. Reaktif blanklarını ayır.'],
  'Kaçak kontrolü':['Ön test önerilir; parça değişiminden önce ve ölçüm sonunda ilgili kaçak testleri yapılır.'],
  'Örnekleme':['Prob–ilk şişe bağlantısında yoğuşmayı izle; 30 L/dk üst sınırını aşma.',
               'Ölçüm sonrasında prob ayrılmışken kalan trenden ortalama örnekleme debisinde 15 dk temiz hava geçir (§8.6.3).'],
  'Geri kazanım':['Sülfürik asit ve SO₂ fraksiyonlarını ayır. Laboratuvar son hacimleriyle başlangıç impinger dolum hacimlerini karıştırma.'],
  'Saklama ve taşıma':['Sızdırmaz kap, fraksiyon kimliği ve sıvı seviyesi kaydı; sayısal saklama sıcaklığı / süre doğrulaması bekleniyor.'],
  'Laboratuvara teslim':common_delivery + ['İzopropanol ve peroksit fraksiyonlarını, filtreyi ve blankları açıkça tanımla.']}))

data.append(profile('hcn_tl115', 'Siyanür / HCN', 'CARB Method 426 — TL115 aktarımı', 'TL115 rev.07 / 05.03.2021', 'Talimat kaynaklı dört şişeli düzen',
 ['D41:5-7'], [probe, filt, imp(1, '0,1 N NaOH', '100 mL'), imp(2, '0,1 N NaOH', '100 mL'), imp(3, 'Başlangıçta boş'), gel(4), meter],
 ['Talimat izokinetik örnekleme belirtir; sabit debi atanmaz.', 'Talimat tablosundaki 500 mL numune miktarı, çekilen gaz hacmi değildir.',
  'Talimat: şişelere giren gaz <42 °C; buz banyosu.', 'Talimat: her örnekleme noktasında en az 2 dk.'],
 {'Hazırlık':['Birincil CARB metniyle karşılaştırma tamamlanmadı. Gösterilen çözelti ve miktarlar TL115 §5.4.1.3 aktarımıdır.'],
  'Kaçak kontrolü':['TL115’teki 0,57 L/dk ifadesi tek başına evrensel kabul sınırı yapılmadı; birincil metot doğrulaması gerekli.'],
  'Örnekleme':['Dört şişeli talimat düzenini ve sıcaklığı kaydet; talimat ile laboratuvarın güncel uygulamasını eşleştir.'],
  'Geri kazanım':['Nozül, prob, şişe içerikleri, filtre ve blank ayrı kimliklerle izlenir. Koruyucu ilavesi ve girişim giderme ayrıntılarının birincil doğrulaması bekleniyor.'],
  'Saklama ve taşıma':['TL115 soğukta saklama belirtir; sayısal sıcaklık ve azami süre doğrulanmadı. Siyanür numunesi için asitleme yönlendirmesi verilmez.'],
  'Laboratuvara teslim':common_delivery}, 'sop_only'))

data.append(profile('hcl_tl89', 'Klor / halojenler', 'TS EN 1911 — TL89 aktarımı', 'TL89 rev.09 / 20.01.2026', 'Gaz halindeki klorürler, HCl olarak; Cl₂ ile aynı parametre değildir',
 ['D53:5-9'], [], ['Sabit / izokinetik / yan akış seçimi damlacık ve homojenlik durumuna bağlı.',
  'Hedef tayin sınırı ve geçerli metot planı.', 'Birincil standartla doğrulanacak.', 'Birincil standartla doğrulanacak.'],
 {'Hazırlık':['Talimat mevcut; birincil TS EN 1911 metni arşivde yok. Doğrulanmamış tam tren çizimi bu karta atanmadı.'],
  'Örnekleme':['Sıvı damlacıkları, gaz homojenliği ve absorpsiyon verimi yöntem seçiminde birlikte değerlendirilir.'],
  'Laboratuvara teslim':common_delivery}, 'sop_only', ['Birincil standart, impinger tipi, dolum, sıcaklık, verim, geri kazanım ve saklama koşulları karşılaştırılacak.']))

for pid, param, method, src in [
 ('metals_en14385','Ağır metaller','TS EN 14385','D47:4-6'),
 ('ammonia_ctm027','Amonyak','EPA CTM 027','D17:20-24'),
 ('ammonia_2071','Amonyak','SCAQMD Method 207.1','D17:20-24'),
 ('chromium_carb425','Krom(VI)','CARB Method 425','D17:12-19'),
 ('formaldehyde_epa323','Formaldehit','EPA Method 323','D39:4-8'),
 ('h2s_epa11','Hidrojen sülfür','EPA Method 11','D04:3-7')]:
    data.append(profile(pid,param,method,'Arşiv kaynağı — ayrıntılı inceleme bekliyor','Yöntem kartı hazırlanıyor',[src],[],
       ['Henüz doğrulanmadı.']*4, {'Hazırlık':['Bu metodun kapsamı, tren düzeni ve sayısal koşulları birincil kaynaktan tamamlanacak. Başka bir metodun şeması burada kullanılmaz.'],
                               'Laboratuvara teslim':common_delivery}, 'pending',
       ['Şema, reaktif miktarı, debi, hacim, süre, sıcaklık, geri kazanım, saklama ve bekletme süresi kaynakları tamamlanacak.']))

for fraction in ('PM10', 'PM2,5'):
    p = profile('ambient_'+fraction.replace(',','_').lower(), fraction+' — ortam havası', 'EN 12341', '2023', 'Ortam havası — gravimetrik filtre örneklemesi',
      ['D23:8,30-31'], [], ['Anma debisi 2,3 m³/saat = yaklaşık 38,33 L/dk; giriş yakınındaki ortam koşullarında.',
       'Anma debisi × 24 saat = 55,2 m³; gerçek geçerli hacim ölçülen debi ve süreden gelir, otomatik sabit kabul edilmez.',
       'Ön tartım koşullandırması: 19–21 °C, %45–50 bağıl nem.', 'Anma süresi 24 saat; geçerlilik ve veri kaybı kuralları ayrıca kontrol edilir.'],
      {'Hazırlık':['Doğru boyut ayırıcı başlığı ve temiz giriş sistemini kullan. Filtreyi benzersiz kimlikle, temiz ortamda kasete yerleştir.',
                  'Arşiv §6.3: ≥48 saat koşullandırma sonrası ilk tartım; ≥12 saat ek koşullandırma sonrası ikinci tartım. İlgili kabul ve belirsizlik istisnalarını standarttan kontrol et.'],
       'Kaçak kontrolü':['Örnekleyicinin kaçak ve debi doğrulamasını EN 12341 ekipman gereklilikleri / onaylı cihaz prosedürüyle yap. Baca EPA kaçak sınırı buraya otomatik taşınmaz.'],
       'Örnekleme':['Gerçek debi, başlangıç/bitiş zamanı, kesintiler ve cihaz bayraklarını kaydet. Örneklenen hacim ortam koşullarındadır.',
                    'Kasette en az bir filtre gaz çekilmeden saha blankı olarak bırakılır (§6.4.2).'],
       'Geri kazanım':['Örneklenen filtreyi yüzeyine temas etmeden koruyucu tutucusuna / temiz kaba al; filtre ile kaset konumunu eşleştir.'],
       'Saklama ve taşıma':['Dış kirlenme ve aşırı ısınmadan korunmuş kapalı / yalıtımlı kaplarda taşı; uçucu kayıplarını ve yoğuşmayı önle.',
                            'Arşiv §6.4.3: gravimetrik analiz için tartım odasına numune alımından itibaren 1 ay içinde alınır. Bu ifade her parametre için 1 ay analiz bekletme izni değildir.'],
       'Laboratuvara teslim':common_delivery+['Filtre, saha blankı, ortam hacmi, gerçek süre, debi/arıza kayıtları ve meteorolojiyi teslim et.']})
    p['scope']='İmisyon'
    p['trainNote']='İmpinger kullanılmaz; boyut ayırıcı giriş → filtre → debi/hacim kontrolü.'
    data.append(p)

for pid, param, method, refs, steps in [
 ('dustfall','Çöken toz','TS 2341 / TS 2342 — TL14 aktarımı',['D44:4-6'],
  ['Toplama alanı, yerleşim, gerçek maruziyet süresi ve saha olaylarını kaydet.', 'Yaprak/böcek gibi yabancı cisimleri ve kap duvarındaki birikintileri talimatın geri kazanım adımlarıyla değerlendir.']),
 ('passive','Pasif örnekleme / difüzyon tüpü','EN 13528 — TL15 aktarımı',['D46:4-5'],
  ['Hedef gaza uygun tüp, koruyucu kap, alım hızı, maruziyet aralığı ve üretici koşullarını seç.', 'Açma/kapama tarih-saatini, sıcaklık/nem/rüzgâr koşullarını ve tüp partisini kaydet.'])]:
    p=profile(pid,param,method,'Arşiv talimatı','İmisyon — pompalı impinger treni kullanılmaz',refs,[],
      ['Uygulanmaz; bu düzende pompalı gaz çekişi yok.', 'Uygulanmaz; çöken tozda toplama alanı × gün, pasif tüpte doğrulanmış alım hızı × maruziyet esastır.',
       'Seçilen yöntem / tüp koşullarından doğrulanacak.', 'Seçilen yöntem ve ölçüm planına bağlı; evrensel tek süre atanmaz.'],
      {'Hazırlık':steps,'Örnekleme':['Konum, süre, meteoroloji ve saha olaylarını kaydet; kaybolan / bozulan numuneyi gizleme.'],
       'Saklama ve taşıma':['Kap / tüp ağzını kapat; kirlenme ve kaybı önle. Parametreye özgü taşıma sıcaklığı ve azami süreyi geçerli metot/üretici talimatıyla doğrula.'],
       'Laboratuvara teslim':common_delivery},'sop_only')
    p['scope']='İmisyon'
    p['trainNote']='Bu metoda impinger veya izokinetik baca nozülü atanmaz.'
    data.append(p)

extend(data, profile, node, imp, meter, common_delivery)

source_index = json.loads((ROOT/'docs/SOURCE_INDEX.json').read_text(encoding='utf-8'))
source_index['documents'] = [s for s in source_index['documents'] if not s['id'].startswith('W')] + WEB_SOURCES
source_index['catalogChecks'] = [
    dict(method='ISO 12141', archiveEdition='2002', currentEdition='2024',
         status='Arşiv metni eski. Yeni sürümün tam koşulları karşılaştırılmadı.', url='https://www.iso.org/standard/85643.html'),
    dict(method='EN 14385', archiveEdition='TL179:2018', currentEdition='2024',
         status='Yeni standart bulundu; okunabilir tam metin karşılaştırması sürüyor.',
         url='https://knowledge.bsigroup.com/products/stationary-source-emissions-determination-of-the-total-emission-of-as-cd-cr-co-cu-mn-ni-pb-sb-tl-and-v'),
    dict(method='EPA CTM-022', status='NO, NO₂ ve NOₓ için elektrokimyasal yöntem; SO₂ yöntemi değildir.',
         url='https://www.epa.gov/emc/emc-conditional-test-methods'),
]
for s in source_index['documents']:
    s.setdefault('title', Path(s.get('path','')).name.replace('_',' '))
for p in data:
    lookup = {s['id']:s for s in source_index['documents']}
    p['sourceDetails'] = [dict(reference=r, **{k:lookup[r.split(':')[0]].get(k,'') for k in ('title','edition','url')}) for r in p['sources']]
    p.setdefault('evidence', [])
(ROOT/'docs/SOURCE_INDEX.json').write_text(json.dumps(source_index,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(ROOT/'assets/source_index.json').write_text(json.dumps(source_index,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

topics = [
 ('Planlama ve metot seçimi', ['Emisyon / imisyon ayrımı, hedef kirletici ve fiziksel faz; ilgili mevzuat, metot sürümü ve laboratuvar yeterliliğini eşleştir.', 'Hedef tayin sınırı, beklenen derişim, toplam numune hacmi ve analitik yöntem laboratuvarla birlikte planlanır.']),
 ('Temsil edicilik ve proses', ['Üretim koşulu, yakıt/hammadde, yük, arıtma sistemi ve proses duruşlarını kaydet.', 'Ölçüm serisinin tesisi temsil etmesini ve duruş/başlatma koşullarının ilgili metoda uygun değerlendirilmesini sağla.']),
 ('Saha güvenliği', ['Platform, korkuluk, sıcak yüzey, elektrik, basınçlı gaz, kimyasal ve düşen cisim risklerini saha sorumlusuyla değerlendir.', 'Uygun erişim, kişisel koruyucu ekipman ve acil durum düzeni olmadan çalışmayı başlatma.']),
 ('Ölçüm düzlemi, port ve travers', ['Akış yönünü gösteren kroki hazırla; en yakın dirsek, fan, klape, kesit değişimi ve açık baca ağzına uzaklıkları ölç.', 'Gerçek kesit, port sayısı/açısı, prob erişimi ve nokta konumlarını seçilen metoda göre belirle. Eksik noktaları sessizce kaldırma.']),
 ('Girdap açısı ve ters akış', ['EPA Method 1 §11.4 null tekniği bu uygulamada ayrı adımlarla açıklanır. EN/ISO için EPA eşiği otomatik uygulanmaz.', 'S-tip Pitotun tek eksendeki null açısı, üç boyutlu akış yönünün tüm bileşenlerini ölçmez.']),
 ('Uygunsuz ölçüm yeri ve sapmalar', ['Nokta artırmak, uygunsuz akışı kendiliğinden uygun hale getirmez. Uygulanabilir alternatif prosedürün tüm koşulları ayrıca doğrulanır.', 'Sapma; gerekçe, etkilenen sonuç, alınan önlem ve gereken yetkili onayıyla kaydedilir. Sadece rapora not düşmek yöntemin geçerliliğini sağlamaz.']),
 ('Kalibrasyon ve doğrulama', ['Pitot, nozül, DGM, basınç/sıcaklık sensörü, terazi, debi kontrolü ve gaz analizörünün geçerli kalibrasyonunu kontrol et.', 'Sıfır/span, tepki süresi, drift ve sızdırmazlık kontrollerini ilgili metot koşullarıyla yap; evrensel tek tolerans kullanma.']),
 ('Kaçak testi', ['Ön / ara / son testin hangisinin zorunlu olduğunu seçilen metottan belirle; vakum ve kaçak debisini kaydet.', 'Kaçak sınırı aşılırsa yalnızca metodun izin verdiği hacim düzeltmesi / ret prosedürünü uygula; kaydı silme.']),
 ('İzokinetik ve sabit debi', ['İzokinetik örneklemede debi; baca hızı, nozül, sıcaklık, basınç ve nemle ilişkilidir. Sabit L/dk tüm bacalara atanmaz.', 'Ana kol / yan kol / seyreltme akışlarını ve hacimlerini ayrı tut; validasyon aralığı dışında adsorbanı yüksek debiye zorlamama kontrolü yap.']),
 ('Nem, yoğuşma ve sıcaklık', ['Isıtılan bölümde erken yoğuşma ve soğutulan bölümde yetersiz tutma farklı hatalardır; sensörün ölçtüğü noktayı açıkça adlandır.', 'Prob, filtre, kartuş, soğutucu çıkışı, sayaç ve ortam sıcaklıklarını birbirinin yerine kullanma.']),
 ('Debi, hacim ve referans koşulları', ['Ham DGM, baca şartları ve referans koşullarındaki hacim ayrı büyüklüklerdir; kuru/yaş baz ve sıcaklık/basıncı yaz.', 'Sabit debide V=Q×t yalnızca aynı koşullara ait Q ve t için kullanılır; değişken debide aralıklı hacimleri topla / sayaç farkını kullan.']),
 ('Filtre ve adsorban hazırlığı', ['Filtre tipi, şartlandırma, tartım, kartuş partisi ve saha blankını hedef metoda göre hazırla.', 'Filtre ve XAD-2 birlikte gereken yöntemlerde sadece impinger şişeleriyle çizim yapma.']),
 ('Çözelti hazırlığı ve izlenebilirlik', ['Derişim, derişim türü, saflık, lot, hazırlama tarihi ve kullanım süresini kaydet. N, mol/L ve yüzde birbirine bağlamsız çevrilmez.', 'Başlangıç dolum hacmi, yıkama hacmi ve analiz son hacmini ayrı alanlarda tut.']),
 ('Blank, şahit ve bulaşma', ['Reaktif blankı, saha blankı, taşıma blankı ve kullanılmamış filtre aynı kontrol değildir.', 'Blankın kurulum, kaçak testi, gaz çekişi ve yıkama kapsamını ilgili metot belirler; tek bir blank kuralı tüm yöntemlere uygulanmaz.']),
 ('Geri kazanım ve fraksiyonlar', ['Prob/nozül, filtre, ön/arka yüzey, kondensat, absorban ve adsorban fraksiyonlarını yönteme göre ayır.', 'Yıkama çözücüsü ve miktarı doğrulanmadan başka yöntemin aseton/su miktarını kopyalama.']),
 ('Koruma, saklama ve teslim', ['Kap malzemesi, kapak/conta, ışık, sıcaklık ve azami bekletme süresini ayrı doğrula.', 'Numune alma, geri kazanım, teslim ve analiz zamanlarını izlenebilir kaydet. Bilinmeyen süreye varsayılan 24/48 saat atama.']),
 ('Gaz analizörleri ve T90', ['Metotla uyumlu ölçüm aralığı, girişim, sıfır/span, tepki süresi ve drift kontrolü gerekir.', 'T90, bekleme zamanı ve ortalama süresi aynı şey değildir; cihaz hattı dahil sistem cevabını değerlendir.']),
 ('VOC / TOC ve seyreltme', ['Toplam organik karbon ile tekil VOC aynı sonuç değildir; FID ve adsorban tüp metotlarını ayır.', 'Seyreltme, nem, sıcaklık, adsorban kapasitesi ve kırılma kontrolünü ilgili metoda göre planla.']),
 ('PM10 / PM2,5 imisyon', ['Ortam havası örnekleyici başlığı, giriş yüksekliği/yerleşimi, gerçek hacimsel debi ve filtre koşullandırması ilgili imisyon metodundan gelir.', 'Baca izokinetik nozülü ve baca travers kuralları ortam havası PM örneklemesine aktarılmaz.']),
 ('Çöken toz ve pasif örnekleme', ['Toplama yüzeyi/maruziyet süresi, meteoroloji, saha konumu, kap kirlenmesi ve tüp açma-kapama zamanı kayıt altındadır.', 'Pasif tüpe pompa debisi atanmaz; çöken toz sonucu çekilen hava hacmine bölünmez.']),
 ('Meteoroloji ve saha kayıtları', ['İmisyon çalışmasında rüzgâr, yağış, çevre kaynaklar, engeller, koordinat ve saha olaylarını planla ve kaydet.', 'Veri kaybı, enerji kesintisi, filtre değişimi, numune taşıması ve proses duruşu zamanlarını sakla.']),
 ('Hesap, belirsizlik ve kalite', ['Hedef tayin sınırı, blank etkisi, kalibrasyon, hacim ve nem düzeltmesi, referans O₂ ve belirsizlik bağımsız kontrol edilir.', 'Ham veriyi sakla; yuvarlama ve birim dönüşümünü en son aşamada kontrollü yap.']),
 ('Rapor ve teslim zinciri', ['Metot/sürüm, saha koşulları, gerçek okumalar, düzeltmeler, sapmalar, blanklar ve numune kimlikleri sonuçla izlenebilir olmalı.', 'Konsantrasyon ve kütlesel debiyi doğru kuru/yaş baz ve referans koşullarıyla birlikte raporla.']),
]

payload = dict(schemaVersion=1, reviewedAt='2026-11-25',
 notice='Geliştirme sürümü: şema kontrolü, tam yöntem onayı ve güncel yürürlük kontrolü aynı şey değildir. Arşiv kaynaklı bilgi güncel metotla eşleştirilmeden sahada tek başına talimat sayılmaz.',
 profiles=data, fundamentals=[dict(title=t, items=items) for t, items in topics])
(ROOT/'assets/field_guide.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'{len(data)} yöntem kartı; {sum(bool(x["train"]) for x in data)} çizim; {len(topics)} ortak saha konusu')
