#!/usr/bin/env python3
import json
from pathlib import Path

root=Path(__file__).resolve().parents[1]
guides=json.loads((root/'assets/field_guides.json').read_text())
assert len(guides)==31
assert len({g['code'] for g in guides})==len(guides)
for guide in guides:
    for section in ['preparation','setup','sampling','recovery','checks']:
        assert guide[section], (guide['code'],section)
        assert all(p['title'] and p['kind'] for p in guide[section])
    for train in guide['trains']:
        assert (root/train['imageAsset']).is_file(),train['imageAsset']
        assert train['nodes']
        if train['verified']:
            assert guide['sources'],guide['code']
        else:
            assert train['note'],guide['code']
    assert all(source['url'].startswith('https://') for source in guide['sources'])

by_code={g['code']:g for g in guides}
def nodes(code):return by_code[code]['trains'][0]['nodes']
# Scientific regressions: these methods must not share one generic filter/impinger layout.
for code in ['EPA Method 5','EPA Method 17']:
    assert len([n for n in nodes(code) if n['label'].startswith('İmpinger')])==4
m8=nodes('EPA Method 8')
assert m8[1]['label']=='İmpinger 1' and m8[2]['kind']=='filter' and m8[3]['label']=='İmpinger 2'
m13=nodes('EPA Method 13A')
assert m13[3]['label']=='İmpinger 3' and m13[4]['kind']=='filter'
assert '0,2–0,4' in by_code['EPA Method 323']['flowRate']
assert '4 hafta' in by_code['SCAQMD Method 207.1']['duration']
assert 'izokinetik' in by_code['EPA CTM 027']['method'].lower()
assert 'izokinetik olmayan' in by_code['SCAQMD Method 207.1']['method']
assert len(by_code['TS ISO 12039 / TS EN 14789 / TS EN 14792 / TS EN 15058']['concepts'])==7
audio=json.loads((root/'assets/standard_audio.json').read_text())
assert len(audio)==13
print(f'{len(guides)} guides: phases, diagrams and critical method distinctions verified')
