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
        bad['profiles'][-1]['train']=bad['profiles'][0]['train']
        with self.assertRaises(AssertionError):validate(bad,SOURCES)


if __name__=='__main__':unittest.main()
