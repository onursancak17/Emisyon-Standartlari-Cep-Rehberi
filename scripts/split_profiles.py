"""Akış bölünmeli PAH varyantı: ISO 11338-1:2003 §6 / Şekil B.3."""
from copy import deepcopy


def extend(data, node):
    p=deepcopy(next(p for p in data if p['id']=='pah_iso11338_b'))
    p.update(id='pah_iso11338_b_split', variant='Metot B — filtre sonrası ana / yan akış; Şekil B.3 örnek düzeni',
             sources=['D27:13-15,25'], reviewState='sections_checked', train=[])
    p['diagram'] = dict(asset='assets/diagrams/pah_b_split.png',
        shared=[node('probe','probe','Nozül / ısıtılmış prob','İzokinetik toplam çekiş'),
                node('filter','filter','Partikül filtresi','Çiy noktası üstü; baca sıcaklığını aşma'),
                node('split','splitter','Akış bölücü','Filtre sonrasında')],
        branches=[dict(id='main',label='Ana kol',nodes=[node('main_meter','meter','Ana kol çekiş / hacim kontrolü','İzokinetik toplam akışı sağlar; kaynak şeklinin cihaz kapasitesi ≤120 L/dk')]),
                  dict(id='side',label='Yan kol — gaz fazı PAH',nodes=[
                      node('side_condenser','condenser','Yoğuşturucu','Gaz <20 °C; soğutucu akışkan 0–20 °C'),
                      node('side_condensate','trap','Kondensat kabı','Bu varyantta adsorbandan önce'),
                      node('side_adsorber','adsorber','Doğrulanmış katı adsorban','Hedef PAH için verim kontrolü'),
                      node('side_meter','meter','Yan kol çekiş / hacim kontrolü','Kaynak şeklinin cihaz kapasitesi ≤15 L/dk')])])
    p['limits'][0]['value']='İzokinetik toplam çekiş. Şekil B.3 örnek cihazında ana kol ≤120 L/dk, yan kol ≤15 L/dk kapasite belirtilir; bunlar her cihaz için ayarlanacak debi değildir.'
    p['limits'][1]['value']='Ana ve yan kol sayaç/hacimlerini ayrı kaydet. Partikül ve gaz fazı farklı akış paylarını temsil eder; aynı referans koşullarına getirilmeyen hacimler toplanmaz.'
    phases={x['title']:x for x in p['phases']}
    phases['Hazırlık']['items']=['Bu varyant filtre sonrası akış bölücü kullanır. Yan kol debisini adsorbanın doğrulanmış yakalama aralığında seç; bu cihazın kapasitesini bütün PAH sistemlerine uygulama.',
                                'Filtre ve işaretli standartlar, yoğuşturucu, kondensat, adsorban ve her iki hacim ölçümünü planla.']
    phases['Örnekleme']['items']=['Toplam çekişte izokinetik koşulu koru; ana ve yan kolu ayrı ölç/kontrol et. Gaz fazı için analiz edilen yan kolun bilinen akış payı kullanılmalıdır.',
                                  'Bu çizimde kondensat kabı adsorbandan öncedir; adsorban sonrası kondensat seçeneği ayrı düzendir. Yan kol hacmini bütün filtre hacmi yerine yazma.']
    p['evidence']=[dict(field='Bölücü / kollar / kapasiteler',references=['D27:13-14,25'],clause='§6.1–6.3; bilgi amaçlı Şekil B.3')]
    p['gaps']=['Bu kart Şekil B.3’ün katı adsorbanlı yan kol varyantını gösterir. İmpingerli / sıvı absorbanlı alternatifler ve bütün analitik fraksiyon hesapları ayrıca tamamlanmalı.']
    p.pop('trainNote',None)
    data.append(p)
