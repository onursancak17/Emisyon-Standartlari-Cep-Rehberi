"""Eski katalogda yeni karşılaştırılmış üç yöntemin çelişkili sayıları kalmasın."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
profiles={p['id']:p for p in json.loads((ROOT/'assets/field_guide.json').read_text(encoding='utf-8'))['profiles']}
mapping={'TS EN 1911':'hcl_en1911_iso','TS EN 14385':'metals_en14385_full','TS EN 13284-1':'dust_en13284_out'}
for filename in ('standards.json','standards_extra.json','standards_overrides.json'):
    path=ROOT/'assets'/filename;items=json.loads(path.read_text(encoding='utf-8'))
    for item in items:
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
