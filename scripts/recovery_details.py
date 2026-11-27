"""EPA kaynaklarının saha geri kazanımında karışması önlenen fraksiyonları."""


def extend(profiles):
    for p in profiles:
        phases={x['title']:x['items'] for x in p['phases']}
        if p['id'].startswith('fluoride_epa13a_'):
            phases['Geri kazanım'] += [
                '§8.6.4.1: bütün numuneye temas eden yüzeylerin toplam su yıkaması <500 mL. İlk üç şişeyi ve bağlantıları üç ayrı küçük porsiyonla yıka; probu fırçala, görünür kalıntı bırakma.',
                'Filtre 3–4 arasındaysa tutucunun ön yarısını geri kazan. Silika jeli sıvıyla aktarma; net kütle artışı nem hesabındadır.'
            ]
            p['evidence'].append(dict(field='Geri kazanım / blank',references=['D05:6-7'],clause='§8.6.4'))
        if p['id']=='halogen_epa26a':
            p['sources']=['D06:3-4,6-9']
            phases['Hazırlık'] += ['Nozül/prob numuneye temasında cam/kuvars kullan; metal iç prob kullanma. Baca >210 °C ise tek parça cam nozül/iç prob düzeni gerekir (§6.1.1).']
            phases['Örnekleme'] += ['§8.1.6: siklon kullanılmışsa veya filtrede sıvı görülüyorsa prob girişinden koşullandırılmış hava geçir; filtre 120–134 °C. Önce 30 dk, hâlâ sıvı varsa 15 dk aralıklarla kuruluğu kontrol et. Bu süre numune gazı çekiş süresi değildir.']
            phases['Geri kazanım'] += [
                'Kap 3: kondensat + asit şişeleri ve filtre arkasından asit şişelerine kadar bağlantıların su yıkaması. Kap 4: iki alkali şişe ve kendi bağlantılarının su yıkaması. Nem için dolum öncesi/sonrası hacim veya kütleyi yıkamadan önce belirle.',
                '§8.2.4 alkali fraksiyonuna sodyum tiyosülfat: 25 mg × beklenen halojen (ppm) × örneklenen kuru standart gaz hacmi (dscm). Beklenen derişim ve kaynak referansındaki gerçek hacim olmadan sabit mg atanmaz.',
                'Alkali reaktif blankına numuneyle aynı oranda tiyosülfat ekle. Asit, alkali, su ve gerekiyorsa aseton blanklarını ayrı tut; partikül isteniyorsa filtre/ön yıkama ayrı kaplardır.'
            ]
            phases['Saklama ve taşıma'] += ['§8.2.7: kapak çevresini PTFE bantla emniyete al; sıvıları dik, filtre tortulu yüzü yukarıda taşı.']
            p['evidence'].extend([
                dict(field='Malzeme / nem uzaklaştırma',references=['D06:3,7'],clause='§6.1.1–6.1.2; §8.1.6'),
                dict(field='Fraksiyon / tiyosülfat / taşıma',references=['D06:8'],clause='§8.2.3–8.2.7')])
        if p['id'].startswith('metals_epa29_'):
            hg=p['id'].endswith('_hg') and not p['id'].endswith('no_hg')
            if not hg:
                phases['Geri kazanım'][:]=[x.replace(' ve cıva fraksiyonlarını',' fraksiyonlarını') for x in phases['Geri kazanım']]
                phases['Örnekleme'][:]=[x for x in phases['Örnekleme'] if not x.startswith('Cıva varsa')]
            p['sources']=['D07:3-7,11-15']
            phases['Geri kazanım'][:]=[x for x in phases['Geri kazanım'] if not x.startswith('Cıva geri kazanımında')]
            phases['Geri kazanım'] += [
                'Kap 1: filtreyi asitle temizlenmiş metal içermeyen aletle petriye al; tortuyu koru. Yalnız eşzamanlı partikül tayininde kap 2’ye ön yüzeylerden tam 100 mL aseton yıkaması yapılır.',
                'Kap 3: ön yüzeylerin tam 100 mL 0,1 N HNO₃ yıkaması. Son temizlikteki su/aseton yıkamasını numuneye ekleme. Kap 4: ilk üç şişe sıvısı + filtre arkası/bağlantıların ayrı tam 100 mL 0,1 N HNO₃ yıkaması.'
            ]
            if hg:
                phases['Geri kazanım'] += [
                    'Kap 5A: 4. boş şişede biriken sıvı + tam 100 mL 0,1 N HNO₃ yıkaması.',
                    'Kap 5B: iki permanganat şişesi sıvısı + her iki şişe/bağlantı için toplam tam 100 mL yeni asitli permanganatla ≥3 yıkama + toplam 100 mL suyla ≥3 yıkama.',
                    'Kap 5C: önce kaba 200 mL su koy. İki permanganat şişesini toplam yalnız 25 mL 8 N HCl ile sırayla yıka; aynı yıkamayı ikinci şişeden geçirip su bulunan kaba dikkatle aktar. 5A, 5B ve 5C birleştirilmez.'
                ]
                phases['Saklama ve taşıma'] += ['Permanganat kaplarında basınç oluşabilir: kabı ağzına kadar doldurma; §7.3.2 ve §8.2.9.2’deki basınç tahliye/taşıma düzenini laboratuvarla uygula.']
            phases['Hazırlık'] += ['§8.2.12–17 blank planı: 0,1 N HNO₃ 300 mL; su 100 mL; asitli peroksit 200 mL; aynı partiden 3 boş filtre. Cıva varsa asitli permanganat 100 mL ve 200 mL su + 25 mL 8 N HCl blankı da ayrı hazırlanır. Partikül/aseton kullanılıyorsa 100 mL aseton blankı.']
            phases['Geri kazanım'] += ['Silika jel ayrı kaba, sıvı kullanmadan aktarılır veya sahada 0,5 g hassasiyetle tartılır. Bütün sıvı düzeylerini, hacimleri ve fraksiyon kimliklerini kaydet.']
            p['evidence'].append(dict(field='Geri kazanım / blanklar',references=['D07:12-15'],clause='§8.2.5–8.2.17'))
        if p['id']=='acid_epa8':
            phases['Geri kazanım'] += [
                'Kap 1, H₂SO₄: ilk şişe sıvısı; prob/ilk şişe/filtre ön yüzeylerini %80 izopropanolle yıka. 225 mL’ye tamamla, kaba aktar; mezürü 25 mL %80 izopropanolle yıkayıp ekle. Filtre de bu kaba alınır; toplam 250 mL.',
                'Kap 2, SO₂: 2–3. şişe sıvıları; filtre arkası ile silika jel öncesi yüzeylerin su yıkaması. 950 mL’ye tamamla, kaba aktar; mezürü 50 mL suyla yıkayıp ekle. Toplam 1000 mL. Bu son hacimler başlangıç dolumları değildir.'
            ]
            p['evidence'].append(dict(field='H₂SO₄ / SO₂ fraksiyon hacimleri',references=['D10:5-7'],clause='§8.8; §12.1'))
