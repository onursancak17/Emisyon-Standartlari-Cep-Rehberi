"""Yeni saha verisinin eksik, karışık veya izlenemez yayımlanmasını engeller."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def validate(data, source_index):
    assert data['schemaVersion'] == 1, 'schemaVersion'
    assert data['notice'].strip(), 'Geliştirme kapsamı görünür olmalı'
    sources = {s['id']: s for s in source_index['documents']}
    assert len(sources) == len(source_index['documents']), 'Tekrarlı kaynak kimliği'
    assert data['profiles'], 'Yöntemler boş'
    ids = set()
    for p in data['profiles']:
        assert p['id'] not in ids, f'Tekrarlı metot {p["id"]}'
        ids.add(p['id'])
        for key in ('parameter', 'method', 'sourceVersion', 'variant', 'sources', 'gaps'):
            assert p.get(key), f'{p["id"]}: {key}'
        assert p['reviewState'] in {'train_checked', 'sections_checked', 'sop_only', 'pending'}
        assert [x['label'] for x in p['limits']] == ['Çekiş debisi', 'Toplam çekiş hacmi', 'Sıcaklık', 'Ölçüm süresi']
        assert all(x['value'].strip() for x in p['limits']), f'{p["id"]}: boş koşul'
        assert len(p['phases']) == 6 and all(x['items'] for x in p['phases'])
        refs = list(p['sources'])
        if p['reviewState'] == 'sections_checked':
            assert p['evidence'], f'{p["id"]}: alan bazında kaynak izi yok'
        for e in p.get('evidence', []):
            assert e['field'] and e['clause'] and e['references']
            refs.extend(e['references'])
        for ref in refs:
            match = re.fullmatch(r'([DW]\d{2}):([\d,\-]+)', ref)
            assert match, f'Kaynak biçimi: {ref}'
            did, selections = match.groups()
            assert did in sources, ref
            for selection in selections.split(','):
                pages = [int(x) for x in selection.split('-')]
                assert 1 <= min(pages) <= max(pages) <= sources[did]['pages'], ref
        nodes = p['train']
        assert len({x['id'] for x in nodes}) == len(nodes), f'{p["id"]}: düğüm kimliği'
        for n in nodes:
            assert n['kind'] in {'probe', 'filter', 'impinger', 'condenser', 'adsorber', 'trap', 'meter'}
            assert n['label'] and n['content']
        if p['reviewState'] == 'pending':
            assert not nodes, 'Doğrulanmamış metoda komşu metodun şeması atanamaz'
            assert not p.get('diagram'), 'Doğrulanmamış metoda bölünmeli şema atanamaz'
        if nodes:
            assert nodes[0]['kind'] == 'probe' and nodes[-1]['kind'] == 'meter'
        assert len(p['sourceDetails']) == len(p['sources']), 'Çevrimdışı kaynak açıklaması eksik'
        if p.get('diagram'):
            diagram=p['diagram']
            asset=Path(diagram['asset'])
            assert asset.parts[:2]==('assets','diagrams') and '..' not in asset.parts and asset.suffix=='.png'
            assert (ROOT/asset).read_bytes().startswith(b'\x89PNG\r\n\x1a\n'), 'Şema PNG asseti eksik/bozuk'
            assert not nodes, 'Aynı kartta iki çelişkili tren gösterilemez'
            assert diagram['shared'][-1]['kind']=='splitter'
            assert len(diagram['branches'])==2
            all_nodes=diagram['shared']+sum([b['nodes'] for b in diagram['branches']],[])
            assert len({n['id'] for n in all_nodes})==len(all_nodes), 'Kol/düğüm kimlikleri çakışıyor'
            for branch in diagram['branches']:
                assert branch['label'] and branch['nodes'][-1]['kind']=='meter'
    assert len(data['fundamentals']) >= 20
    return len(ids)


if __name__ == '__main__':
    count = validate(json.loads((ROOT/'assets/field_guide.json').read_text(encoding='utf-8')),
                     json.loads((ROOT/'docs/SOURCE_INDEX.json').read_text(encoding='utf-8')))
    print(f'OK: {count} yöntem kartı; kaynak/sayfa ve koşul alanları geçerli.')
