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
        assert p['reviewState'] in {'train_checked', 'sop_only', 'pending'}
        assert [x['label'] for x in p['limits']] == ['Çekiş debisi', 'Toplam çekiş hacmi', 'Sıcaklık', 'Ölçüm süresi']
        assert all(x['value'].strip() for x in p['limits']), f'{p["id"]}: boş koşul'
        assert len(p['phases']) == 6 and all(x['items'] for x in p['phases'])
        for ref in p['sources']:
            match = re.fullmatch(r'(D\d{2}):([\d,\-]+)', ref)
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
        if nodes:
            assert nodes[0]['kind'] == 'probe' and nodes[-1]['kind'] == 'meter'
    assert len(data['fundamentals']) >= 20
    return len(ids)


if __name__ == '__main__':
    count = validate(json.loads((ROOT/'assets/field_guide.json').read_text(encoding='utf-8')),
                     json.loads((ROOT/'docs/SOURCE_INDEX.json').read_text(encoding='utf-8')))
    print(f'OK: {count} yöntem kartı; kaynak/sayfa ve koşul alanları geçerli.')
