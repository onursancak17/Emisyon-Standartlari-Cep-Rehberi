#!/usr/bin/env python3
import json,re,hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[1];j=json.loads((root/'assets/manuals.json').read_text());t=json.loads((root/'assets/training.json').read_text())
a=j['manuals'];assert len(a)==24 and len(t)==11
assert len({r['id'] for r in a+t})==len(a+t)
for r in [j['common']]+a+t:
 assert r['sections'] and all(s['title'] and s['items'] for s in r['sections'])
 for s in r['sections']:
  assert all(isinstance(v,str) and len(v.strip())>8 for v in s['items']),r['id']
  assert not any(re.search(r'REVİZYON|DOKÜMAN NO|Elektronik Nüsha|TEŞEKKÜRLER|@csb',v) for v in s['items']),r['id']
 narrative=[v.strip().casefold() for s in r['sections'] for v in s['items']]
 assert len(narrative)==len(set(narrative)),f'{r["id"]}: duplicated instruction'
 for tr in r['trains']:
  assert tr['bottles'] or tr.get('visual')=='resin'
  assert all(tr.get(k) for k in ['method','sampling','flow','condition','vesselType']),r['id']
  assert tr.get('filterAfter',0)<len(tr['bottles']) or not tr.get('filterAfter',0)
  assert not (tr['method']=='EPA Method 26A' and tr['sampling']=='Sabit debili örnekleme')
  for b in tr['bottles']:
   assert b['amount'] and b['content']
   assert (root/f'assets/equipment/{b["kind"]}.webp').is_file()
 # Shared preparation must remain exclusively in the common chapter.
 if r in a:
  assert not any('tesis yetkilileri ile yapılacak toplantı' in v.lower() for s in r['sections'] for v in s['items'])
by={r['id']:r for r in a}
assert [b['amount'] for b in by['hcl']['trains'][0]['bottles']][:2]==['40 veya 100 mL']*2
assert [b['content'] for b in by['halojen']['trains'][0]['bottles']]==['H₂SO₄']*3+['NaOH']*2+['Silika jel']
assert by['halojen']['trains'][0]['bottles'][0]['amount']=='50 mL'
assert len(by['metal-epa']['trains'][0]['bottles'])==7 and len(by['metal-epa']['trains'][1]['bottles'])==4
assert by['flor']['trains'][0]['bottles'][1]['tip'].startswith('Standart')
assert by['formaldehit']['trains'][0]['bottles'][1]['amount']=='20 mL'
assert by['halojen']['trains'][1]['method']=='EPA Method 26A' and len(by['halojen']['trains'][1]['bottles'])==5
assert by['halojen']['trains'][2]['method']=='EPA Method 26' and [b['amount'] for b in by['halojen']['trains'][2]['bottles'][:4]]==['15 mL']*4
assert len(by['hcl']['trains'])==3 and by['hcl']['trains'][2]['branch']
assert by['formaldehit']['trains'][1]['method']=='EPA Method 316'
assert by['flor']['trains'][0]['method']=='EPA Method 13A' and by['flor']['trains'][1]['method']=='ISO 15713'
assert [b['amount'] for b in by['nem']['trains'][0]['bottles']]==['100 mL','100 mL','Sıvı eklenmez','200 g']
assert by['nem']['trains'][0]['sampling']=='Sabit debili örnekleme'
assert by['nem']['trains'][1]['sampling']=='İzokinetik örnekleme'
assert by['nem']['trains'][2]['method']=='EN 14790'
assert by['sulfurik']['trains'][0]['filterAfter']==1
assert by['metal-en']['trains'][1]['branch'] and len(by['metal-en']['trains'][1]['bottles'])==4
assert (root/'assets/equipment/resin.webp').is_file()
assert all(not r['trains'] for r in a if r['id'] in ['yanma','islilik','voc','toc','cokentoz','pasif','hiz-ts','hiz-epa'])
print(f'Validated {len(a)} instructions, {len(t)} training chapters, all reagent amounts and diagram coverage.')


assert by['toz-epa']['filterPlacement']=='outside'
assert by['toz-epa17']['filterPlacement']=='inside'
assert by['cokentoz-metal']['visual']=='settled-metal' and not by['cokentoz-metal']['trains']
