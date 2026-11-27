"""Doğrudan saha cihazları: kimyasal numune bekletme kuralları uygulanmaz."""
def extend(data,profile,node,imp,meter,delivery):
    def add(*args,evidence,**kwargs):
        p=profile(*args,state='sections_checked',**kwargs)
        p['evidence']=[dict(field=k,references=v[0],clause=v[1]) for k,v in evidence.items()]
        data.append(p)
    add('velocity_epa2','Hız ve debi','EPA Method 2','02.08.2017','S-tip Pitot — Method 1 bağlantılı',
        ['W09:1-6'],[],
        ['Hız m/s, baca debisi m³/saat gibi hacim/zaman birimlerinde hesaplanır; L/dk kimyasal numune çekişi bu ölçüm değildir.',
         'Çekilen numune gazı hacmi yoktur; kesit×ortalama hız ve gerekiyorsa kuru standart debi hesaplanır.',
         'T ölçer hata sınırı en düşük MUTLAK baca sıcaklığının %1,5’i. Örneğin 100 °C için esas 373,15 K’dir; 100’ün %1,5’i değildir.',
         'Her Method 1 noktasında hız basıncı ve sıcaklık; manometre seviye/sıfır kontrolü travers sırasında en az saatte bir. EN/ISO’nun 1 dk/nokta şartı buraya kendiliğinden aktarılmaz.'],
        {'Hazırlık':['Method 1’e uygun düzlem/grid ve girdap değerlendirmesi gerekir. Uygunsuz siklonik akışta bu yöntem doğrudan kullanılamaz; yer değiştirme, akış düzenleme veya yetkili onaylı alternatif gerekir.',
            'Pitot kimliği ve katsayısı kayıtlı olmalı. §10.1’in geometri şartlarını sağlayan izole S-tip için 0,84 atanabilmesi, her prob/nozül/termokupl birleşiminin katsayısının 0,84 olduğu anlamına gelmez; aerodinamik etkileşim kalibrasyon gerektirebilir.',
            '1,27 mmH₂O yaklaşık 12,45 Pa’dır. Ortalama ΔP bunun altındaysa; ≥12 noktalı traversin >%10 noktası veya <12 noktalı traversin birden fazla noktası bunun altındaysa daha duyarlı gösterge gerekir. §6.2.1 alternatif T oranı >1,05 ise de veri kabul edilmez.'],
         'Kaçak kontrolü':['Ön test önerilir; son test zorunludur. İmpakt tarafında ≥7,6 cmH₂O basınç, statik tarafta aynı büyüklükte emiş uygula ve kapat; ≥15 s boyunca ±2,5 mmH₂O içinde kararlılık gerekir (§8.1–8.3).',
            'Birim karşılıkları yaklaşık 745 Pa test basıncı ve ±24,5 Pa kararlılık bandıdır. Bu basınç devresi kontrolü, DGM treninin 0,57 L/dk kaçağıyla aynı test değildir.'],
         'Örnekleme':['Manometreyi sıfırla ve seviyesini ayarla. Her noktada ΔP ve T, bacada statik basınç ve ortam barometrik basıncı ölç. Daha hassas manometreye geçilirse bütün noktaların ΔP/T okumaları yeniden alınır.',
            'Kuru gaz molekül kütlesi uygun Method 3 gaz bileşiminden; nem Method 4 referans/eşdeğer veya Method 5’ten belirlenir. Esas olarak hava veren proseste kuru mol kütlesi 29,0 kullanılabilir; her yanma gazı için aynı kabul edilmez.',
            'Standart Pitot kullanılmışsa tıkanmayı geri üfleme öncesi/sonrası aynı okunabilir noktada ΔP farkının %5 içinde olmasıyla doğrula; değilse traversi reddet ve tekrarla (§6.1.2).'],
         'Geri kazanım':['Kimyasal fraksiyon yoktur; nokta okumaları, kesit, Cp, T/P, nem ve bileşim kayıtları saklanır. Formüldeki basınç, sıcaklık ve mol kütlesiyle uyumlu birim katsayısı seç; Amerikan birimli katsayıyı SI girdilerine takma.'],
         'Saklama ve taşıma':['Veri ve cihaz kimliği korunur; Pitot uçlarını darbe/tıkanmadan koru. Kimyasal numune saklama sıcaklığı veya analiz süresi atanmaz.'],
         'Laboratuvara teslim':delivery+['Nokta tablosu, gerçek iç çap/alan, Cp sertifikası/geometri, hassasiyet/kaçak/tıkanma kontrolleri ve ham T/P/ΔP/nem/bileşim rapor birimine aktarılır.']},
        gaps=['Bu kart saha seçimi ve §6–8 kontrollerini kapsar. Tam Pitot kalibrasyon laboratuvarı prosedürü §10, katsayı/hesap §12 ve Method 1’in uygulamaya özgü onayları ayrıca izlenir.'],
        evidence={'Kapsam / cihaz / hassasiyet':(['W09:1-4'],'§1, §6'),
            'Saha / kaçak / katsayı':(['W09:4-6'],'§8, §10.1–10.1.1')})
    for epa in (False,True):
        method='EPA Method 25A' if epa else 'EN 12619'
        add('toc_epa25a' if epa else 'toc_en12619','TOC — toplam organik karbon',method,'03.08.2017' if epa else '2013 / TSE Haziran 2013',
            'Isıtılmış hat — sürekli FID ölçümü', ['W10:1-6'] if epa else ['D24:8-15'],
            [node('probe','probe','Numune probu','Isıtılmış, uygun inert malzeme'),
             node('filter','filter','Partikül filtresi','Önemli toz yükünde önerilir; dış filtre yoğuşmayı önleyecek kadar ısıtılır' if epa else 'Örnekleme hattı önünde ısıtılmış filtre'),
             node('line','probe','Isıtılmış numune hattı','Yoğuşma ve adsorpsiyon kaybı önlenir'),
             node('analyzer','meter','FID ve kayıt sistemi','Uygun çekiş / yakıt / yanma havası; sıfır-span gazları')],
            ['Cihazın doğrulanmış debisi; sabit evrensel L/dk yok. Yan akış/haricî pompa varsa analizör gereksinimini karşılamalı.',
             'Şişede/tüpte toplanan gaz hacmi yoktur; sonuç eşzamanlı analizle üretilir. Seyreltme varsa doğrulanmış oranla değerlendirilir.',
             'Analizöre kadar örnekleme bileşenleri ≥110 °C; FID bloğu >120 °C. §5.2 güvenlik istisnası ayrıca değerlendirilir.' if epa else 'Örnekleme sistemi boyunca ≥180 °C; PTFE hattın üst sıcaklığı 200 °C. Hat/filtrede soğuk nokta ve yoğuşma olmamalı.',
             'İlgili kaynak mevzuatının ortalama/ölçüm süresi. En az 1 değer/dk kayıt; tepki testi %95 seviyesine göre.' if epa else 'Süre ve temsil EN 15259/ölçüm planından gelir. Hat gaz kalış süresi <60 s; seri başına sistem T90≤200 s. T90 toplam ölçüm süresi değildir.'],
            {'Hazırlık':['Toplam organik yanıt ölçülür; tekil VOC türünü ayırmaz. Kalibrasyon gazı ve sonuç bazını (propan eşdeğeri / karbon) açık yaz. CO ve CO₂ toplam organik karbon diye raporlanmaz.',
                'Sıfır ve sertifikalı span gazı, gaz matrisi/O₂ etkisi, FID yakıtı ve aralık cihazın/yöntemin koşullarıyla seçilir. Propan kalibrasyonu diğer bileşiklerin farklı yanıt faktörlerini ortadan kaldırmaz.',
                ('Span yoksa beklenen derişimin 1,5–2,5 katı. Düşük gaz %25–35, orta %45–55, yüksek %80–90 span; ilave elektronik aralık orta gazla kontrol edilir.' if epa else 'Span propan, yaklaşık yarım saatlik ELV veya ölçüm aralığının %50–90’ı; sertifikalı derişim belirsizliği ≤%2. Yakıt/yanma havası ve sıfır gazı için kaynak saflık koşulları uygulanır.')],
             'Kaçak kontrolü':[('Seriden önce en çok 2 saat içinde sıfır/yüksek ayarı ve düşük/orta gazlarla kalibrasyon hatası kontrolü yapılır; hata ilgili kalibrasyon gazı değerinin <%5’i. Bu yüzde spanın %5’i değildir.' if epa else 'Önce doğrudan analizör sıfır/span ayarı; sonra filtre önündeki prob girişine yakın noktadan aynı gazlarla bütün sistem kontrolü. Doğrudan ve hat üzerinden yanıt farkı spanın <%2’si olmalı (§6.2.1–2).'),
                'Hat/filtre/bağlantıların tümünü kontrol et; yalnız analizöre gaz vermek hattın sızdırmazlığını ve bellek etkisini göstermez.'],
             'Örnekleme':[('Sistem tepki süresi yüksek gaz adımının %95’ine ulaşma süresidir; üç tekrarın ortalaması alınır. En az dakikada bir derişim ve proses duruş/çevrim bilgisi kaydedilir.' if epa else 'Sistem T90 ve hat kalış süresini ayrı değerlendir. Seri başına tepki/sampling kontrolü; yıllık ve onarım sonrası doğrusallık/girişim kontrolleri Tablo 1’e göre. O₂ sinerjisi yaklaşık %10 O₂ civarında önemlidir.'),
                ('Ölçüm sonu ve her saat sıfır/orta gazla drift kontrolü; iki sonuç görülmeden ayar yapma. Sıfır ve kalibrasyon drifti spanın ±%3’ünden küçük olmalı. Aşımda önceki dönemi reddedip düzelt/tekrarla veya §8.6.2’nin iki kalibrasyonla raporlama alternatifini uygula.' if epa else 'Başlangıç/son ve en az günlük sıfır-span kontrolü. Drift >%2 span ise sıfır ve span için düzeltme; drift <%5 span olmalı, aksi halde sonuç geçersiz (§6.2.3). Düzeltmeden önce değerleri kaydet.')],
             'Geri kazanım':['Bu yöntemde kimyasal yıkama fraksiyonu laboratuvara gönderilmez. Ham derişim zaman serisi, kalibrasyon, drift, tepki, nem/O₂ ve proses kayıtları korunur.',
                ('ppmv propan eşdeğerinden ppmv karbon eşdeğerine geçişte çarpan 3’tür; farklı kalibrasyon gazında uygun karbon/yanıt faktörü kullanılır. mg/m³ dönüşümü için ayrıca referans T/P gerekir.' if epa else 'Kaynak 273 K/101,3 kPa’da propan ppmv → mg C/m³ için 3×12/22,4 katsayısını verir. Kuru ve O₂ referans düzeltmeleri ayrı; nem <%2 ise nem izleme/düzeltme istisnasını §6.3.2’ye göre değerlendir.')],
             'Saklama ve taşıma':['Numune şişesi için kimyasal bekletme sıcaklığı/süresi uygulanmaz; analiz alımla eşzamanlıdır. Ham veri, cihaz/hat ayarı ve kalibrasyon gazı sertifikaları raporla izlenebilir saklanır.'],
             'Laboratuvara teslim':delivery+['Zaman serisi, aralık, kalibrasyon gazı/sertifika/matris, kontrol sonuçları, kullanılan düzeltmeler, referans koşulları ve temsil edilen proses dönemleri rapor birimine verilir.']},
            gaps=['Uygulanacak kaynak ortalama süresi, uygun ölçüm düzlemi/temsil, cihazın hedef bileşiklere yanıtı ve toplam belirsizlik ölçüm planıyla tamamlanır. Yöntemler arası ısıtma, T90/T95 veya drift sınırları birleştirilmez.'],
            evidence={'Sistem / sıcaklık / gazlar / süre':(['W10:1-4'],'§3, §6–8') if epa else (['D24:8-11'],'§4–5, Tablo 1'),
                'Kontrol / hesap / rapor':(['W10:4-6'],'§8–13') if epa else (['D24:12-15'],'§6–7, Ek A')})
