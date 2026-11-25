"""Eski katalogda yeni karşılaştırılmış üç yöntemin çelişkili sayıları kalmasın."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
profiles={p['id']:p for p in json.loads((ROOT/'assets/field_guide.json').read_text(encoding='utf-8'))['profiles']}
mapping={'TS EN 1911':'hcl_en1911_iso','TS EN 14385':'metals_en14385_full','TS EN 13284-1':'dust_en13284_out',
         'SCAQMD Method 207.1':'ammonia_2071_gs','TS EN 1948-1':'dioxin_en1948_filter'}
for filename in ('standards.json','standards_extra.json','standards_overrides.json'):
    path=ROOT/'assets'/filename;items=json.loads(path.read_text(encoding='utf-8'))
    for item in items:
        if item['code']=='EPA CTM 027 / SCAQMD Method 207.1':
            item.update(purpose='İki ayrı amonyak yöntemi: CTM-027 izokinetik baca örneklemesi; SCAQMD 207.1 izokinetik olmayan baca ve ayrı mini/flux odası varyantı. Parametre rehberinden yöntemi ve varyantı seç.',
                duration='Hedef hacim/proses/mevzuat planı; SCAQMD saatlik kütle sınırında en az 1 saat. CTM ve SCAQMD koşulları ayrı değerlendirilir.',
                flowRate='CTM-027: izokinetik. SCAQMD büyük tren: 15–30 L/dk; mini tren Ek B tipik 0,75–1 L/dk. Aynı debi kuralı değildir.',
                equipment=['Yönteme özgü baca içi filtre, bağlantı ve kap düzeni parametre rehberinde ayrı çizilir.'],
                reagents=['CTM-027 üçüncü şişe boş/asitli varyantlıdır. SCAQMD büyük tren iki adet 100 mL, mini tren iki adet 15 mL 0,1 N H₂SO₄ kullanır; kaynak şeklinin M/N çelişkisi kartta belirtilir.'],
                fieldSteps=['Kurulum, kaçak, örnekleme ve geri kazanımı seçili yöntemin ayrı kartından uygula.'],
                criticalControls=['SCAQMD: alımdan itibaren ≤7 günde geri kazanım; geri kazanım sonrası 1,67–7,22 °C ve ≤4 hafta saklama. Bu, 7 günlük analiz sınırı değildir.','CTM-027 koruma/blank kurallarını kendi kartından izle.'],
                acceptance=['Kaçak, pH, blank ve verim seçili yöntemle değerlendirilir.'],reporting=['Yöntem/sürüm, varyant, gaz/sıvı hacimleri, koşullar ve teslim zincirini kaydet.'],
                mistakes=['İzokinetik CTM-027 ile izokinetik olmayan SCAQMD trenini birleştirmek.','Geri kazanım ve analiz bekletme sürelerini karıştırmak.'])
            continue
        if item['code'] not in mapping:continue
        p=profiles[mapping[item['code']]]
        phases={s['title']:s['items'] for s in p['phases']}
        item.update(
            purpose=f"{p['method']} — {p['sourceVersion']}. {phases['Hazırlık'][0]}",
            duration=p['limits'][3]['value'],flowRate=p['limits'][0]['value'],
            equipment=['Bu yöntemin şema/numune fraksiyonları ana ekrandaki parametre rehberinde ayrı varyantlarla bulunur.'],
            reagents=phases['Hazırlık'][1:],
            fieldSteps=phases['Kaçak kontrolü']+phases['Örnekleme']+phases['Geri kazanım'],
            criticalControls=[p['limits'][1]['value'],p['limits'][2]['value']]+phases['Saklama ve taşıma'],
            acceptance=['Kontrol sonucu yalnız seçili yöntem ve kaynak baskısıyla değerlendirilir. Açık kalan kaynak/uygulama ayrıntıları parametre kartında görünür.'],
            reporting=phases['Laboratuvara teslim']+['Kaynak: '+', '.join(p['sources'])],
            mistakes=['Dolum, yüzde türü, blank, süre veya saklama kuralını başka yöntemden aktarmak.','Eski eğitim notunu yeni standart baskısı diye kullanmak.'])
    path.write_text(json.dumps(items,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
