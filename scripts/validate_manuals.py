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
 for tr in r['trains']:
  assert tr['bottles']
  for b in tr['bottles']:
   assert b['amount'] and b['content']
   assert (root/f'assets/equipment/{b["kind"]}.webp').is_file()
 # Shared preparation must remain exclusively in the common chapter.
 if r in a:
  assert not any('tesis yetkilileri ile yapılacak toplantı' in v.lower() for s in r['sections'] for v in s['items'])
by={r['id']:r for r in a}
assert [b['amount'] for b in by['hcl']['trains'][0]['bottles']][:2]==['100 mL']*2
assert [b['content'] for b in by['halojen']['trains'][0]['bottles']]==['H₂SO₄']*3+['NaOH']*2+['Silika jel']
assert by['halojen']['trains'][0]['bottles'][0]['amount']=='50 mL'
assert len(by['metal-epa']['trains'][0]['bottles'])==7 and len(by['metal-epa']['trains'][1]['bottles'])==4
assert by['flor']['trains'][0]['bottles'][1]['tip'].startswith('Standart')
assert by['formaldehit']['trains'][0]['bottles'][1]['amount']=='20 mL'
assert (root/'assets/equipment/resin.webp').is_file()
assert all(not r['trains'] for r in a if r['id'] in ['yanma','islilik','voc','toc','cokentoz','pasif','hiz-ts','hiz-epa'])
print(f'Validated {len(a)} instructions, {len(t)} training chapters, all reagent amounts and diagram coverage.')
