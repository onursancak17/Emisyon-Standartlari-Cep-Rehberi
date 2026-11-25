import copy
import json
import unittest
from pathlib import Path
from validate_field_guide import validate

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT/'assets/field_guide.json').read_text(encoding='utf-8'))
SOURCES = json.loads((ROOT/'docs/SOURCE_INDEX.json').read_text(encoding='utf-8'))
P = {p['id']:p for p in DATA['profiles']}


class FieldGuideTests(unittest.TestCase):
    def test_manifest_is_valid(self):
        self.assertGreaterEqual(validate(DATA,SOURCES),17)

    def test_fluoride_filter_really_moves(self):
        rear = [x['id'] for x in P['fluoride_epa13a_rear']['train']]
        front = [x['id'] for x in P['fluoride_epa13a_front']['train']]
        self.assertEqual(rear[rear.index('filter')-1:rear.index('filter')+2],['i3','filter','i4'])
        self.assertEqual(front[:3],['probe','filter','i1'])

    def test_mercury_changes_three_bottles(self):
        hg = [x['id'] for x in P['metals_epa29_hg']['train'] if x['kind']=='impinger']
        no_hg = [x['id'] for x in P['metals_epa29_no_hg']['train'] if x['kind']=='impinger']
        self.assertEqual(len(hg),7)
        self.assertEqual(len(no_hg),4)
        self.assertEqual(set(hg)-set(no_hg),{'i4','i5','i6'})

    def test_acid_filter_is_between_bottles(self):
        ids = [x['id'] for x in P['acid_epa8']['train']]
        self.assertEqual(ids[ids.index('filter')-1:ids.index('filter')+2],['i1','filter','i2'])

    def test_halogen_optional_knockout_is_50_ml(self):
        train = P['halogen_epa26a']['train']
        optional = [x for x in train if x['optional']]
        self.assertEqual(len(optional),1)
        self.assertEqual(optional[0]['amount'],'50 mL')
        self.assertEqual(sum(x['kind']=='impinger' and not x['optional'] for x in train),5)

    def test_pah_dioxin_do_not_share_generic_bottle_train(self):
        for pid in ('pah_iso11338_b','dioxin_en1948_filter'):
            kinds = [x['kind'] for x in P[pid]['train']]
            self.assertIn('adsorber',kinds)
            self.assertIn('condenser',kinds)
            self.assertIn('trap',kinds)

    def test_invalid_source_is_rejected(self):
        bad = copy.deepcopy(DATA)
        bad['profiles'][0]['sources']=['D08:999']
        with self.assertRaises(AssertionError):validate(bad,SOURCES)

    def test_pending_cannot_display_a_recipe(self):
        bad = copy.deepcopy(DATA)
        pending=next(p for p in bad['profiles'] if p['reviewState']=='pending')
        pending['train']=bad['profiles'][0]['train']
        with self.assertRaises(AssertionError):validate(bad,SOURCES)

    def test_ammonia_uses_in_stack_filter_and_two_third_bottle_variants(self):
        for pid in ('ammonia_ctm027_empty3','ammonia_ctm027_acid3'):
            p=P[pid]
            self.assertEqual([n['id'] for n in p['train']][:3],['probe','filter','line'])
            self.assertIn('Baca içi',p['train'][1]['label'])
        third=lambda pid:next(n for n in P[pid]['train'] if n['id']=='i3')
        self.assertIn('boş',third('ammonia_ctm027_empty3')['content'])
        self.assertEqual(third('ammonia_ctm027_acid3')['amount'],'100 mL')

    def test_chromium_filter_is_after_alkali_catch(self):
        ids=[n['id'] for n in P['chromium_carb425']['train']]
        self.assertEqual(ids[:4],['probe','i1','i2','filter'])

    def test_small_midget_methods_do_not_inherit_large_impinger_recipe(self):
        h2s=P['h2s_epa11']['train']
        self.assertEqual([n['amount'] for n in h2s if n['kind']=='impinger'],['15 mL','','15 mL','15 mL','15 mL'])
        self.assertEqual(next(n for n in h2s if n['id']=='dryer')['amount'],'En fazla 30 g')
        formal=P['formaldehyde_epa323']['train']
        self.assertEqual(next(n for n in formal if n['id']=='i2')['amount'],'20 mL')
        self.assertNotIn('filter',[n['id'] for n in formal])

    def test_offline_source_index_and_evidence_are_consistent(self):
        bundled=json.loads((ROOT/'assets/source_index.json').read_text(encoding='utf-8'))
        self.assertEqual(bundled,SOURCES)
        bad=copy.deepcopy(DATA)
        next(p for p in bad['profiles'] if p['reviewState']=='sections_checked')['evidence'][0]['references']=['W01:999']
        with self.assertRaises(AssertionError):validate(bad,SOURCES)


if __name__=='__main__':unittest.main()
