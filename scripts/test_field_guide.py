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

    def test_dilution_has_two_distinct_outputs_and_an_independent_gas_input(self):
        d=P['voc_13649_dynamic']['diagram']
        self.assertEqual(d['type'],'dilution')
        self.assertEqual(d['dilution']['id'],'diluent')
        self.assertEqual([b['id'] for b in d['branches']],['excess','sample'])
        self.assertEqual(d['branches'][0]['nodes'][-1]['id'],'exhaust')
        self.assertEqual(d['branches'][1]['nodes'][-1]['kind'],'meter')

    def test_audit_preserves_unresolved_sources_without_method_number_collisions(self):
        audit=SOURCES['auditMatrix']
        self.assertFalse(audit['allStandardsFinallyVerified'])
        self.assertEqual(len(audit['rows']),37)
        r={r['code']:r for r in audit['rows']}
        self.assertEqual(r['ISO 12141']['state'],'source_missing')
        self.assertNotIn('velocity_epa2',r['EPA Method 29']['profileIds'])
        self.assertNotIn('moisture_epa4',r['CARB Method 425']['profileIds'])
        self.assertEqual(next(s['sourceKind'] for s in SOURCES['documents'] if s['id']=='D26'),'Eğitim sunumu')

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

    def test_mercury_recovery_instructions_do_not_leak_into_mercury_free_variant(self):
        hg=' '.join(P['metals_epa29_hg']['phases'][3]['items'])
        no_hg=' '.join(P['metals_epa29_no_hg']['phases'][3]['items'])
        self.assertIn('Kap 5C:',hg)
        for marker in ('Kap 5A:','Kap 5B:','Kap 5C:'):
            self.assertNotIn(marker,no_hg)

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
        pending=bad['profiles'][0]
        pending['reviewState']='pending'
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

    def test_split_pah_keeps_side_condensate_before_adsorber(self):
        p=P['pah_iso11338_b_split']
        self.assertFalse(p['train'])
        d=p['diagram']
        self.assertEqual([n['kind'] for n in d['shared']],['probe','filter','splitter'])
        self.assertEqual([n['kind'] for n in d['branches'][1]['nodes']],['condenser','trap','adsorber','meter'])
        self.assertEqual(d['branches'][0]['nodes'][-1]['id'],'main_meter')
        self.assertEqual(d['branches'][1]['nodes'][-1]['id'],'side_meter')

    def test_en14385_is_not_epa29_reagent_or_bottle_count(self):
        p=P['metals_en14385_full']
        filled=[n for n in p['train'] if n['kind']=='impinger' and 'boş' not in n['content']]
        self.assertEqual(len(filled),3)
        self.assertTrue(all('kütle/kütle' in n['content'] and '%1,6' in n['content'] for n in filled))
        self.assertIn('BS EN',next(s for s in SOURCES['documents'] if s['id']=='L02')['title'])

    def test_hcl_dated_reference_is_not_silently_upgraded(self):
        p=P['hcl_en1911_iso']
        self.assertIn('2001',p['limits'][3]['value'])
        self.assertNotIn('≥3 dk',p['limits'][3]['value'])
        filled=[n for n in p['train'] if n['kind']=='impinger' and 'boş' not in n['content']]
        self.assertEqual(len(filled),2)
        self.assertTrue(all('su' in n['content'] for n in filled))

    def test_dust_in_stack_filter_precedes_support_line(self):
        ids=[n['id'] for n in P['dust_en13284_in']['train']]
        self.assertEqual(ids[:3],['probe','filter','line'])
        self.assertIn('≥3 dk',P['dust_en13284_in']['limits'][3]['value'])

    def test_en_split_trains_keep_two_independent_meters_and_absorber_counts(self):
        for pid, count in (('hcl_en1911_split',2),('metals_en14385_split',3)):
            p=P[pid]
            self.assertFalse(p['train'])
            d=p['diagram']
            self.assertEqual([n['kind'] for n in d['shared']],['probe','filter','splitter'])
            self.assertEqual(len(d['branches']),2)
            for b in d['branches']:
                self.assertEqual(b['nodes'][-1]['kind'],'meter')
            side=d['branches'][1]['nodes']
            filled=[n for n in side if n['kind']=='impinger' and 'boş' not in n['content']]
            self.assertEqual(len(filled),count)
            self.assertNotEqual(d['branches'][0]['nodes'][-1]['id'],side[-1]['id'])

    def test_ammonia_small_and_large_trains_keep_different_fills_and_front_filter(self):
        large=P['ammonia_2071_gs']['train'];small=P['ammonia_2071_mini']['train']
        self.assertEqual(next(n for n in large if n['id']=='i1')['amount'],'100 mL')
        self.assertEqual(next(n for n in small if n['id']=='i1')['amount'],'15 mL')
        self.assertTrue(next(n for n in large if n['id']=='filter')['optional'])
        self.assertNotIn('filter',[n['id'] for n in small])

    def test_dioxin_condensate_moves_between_specific_variants(self):
        full=[n['id'] for n in P['dioxin_en1948_filter']['train']]
        side=[n['id'] for n in P['dioxin_en1948_split']['diagram']['branches'][1]['nodes']]
        self.assertLess(full.index('adsorber'),full.index('condensate'))
        self.assertLess(side.index('condensate'),side.index('adsorber'))
        self.assertEqual([n['amount'] for n in P['dioxin_en1948_liquid']['train'] if n['kind']=='impinger'],['150 mL','150 mL'])


if __name__=='__main__':unittest.main()
