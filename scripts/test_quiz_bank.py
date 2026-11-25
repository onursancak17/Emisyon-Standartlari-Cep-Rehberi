import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BANK=json.loads((ROOT/'assets/quiz_bank.json').read_text(encoding='utf-8'))


class QuizBankTests(unittest.TestCase):
    def test_questions_have_unique_ids_and_explained_answers(self):
        questions=BANK['questions']
        self.assertGreaterEqual(len(questions),100)
        self.assertEqual(len({q['id'] for q in questions}),len(questions))
        for q in questions:
            with self.subTest(question=q['id']):
                self.assertEqual(len(q['choices']),4)
                self.assertEqual(len(set(q['choices'])),4)
                self.assertIn(q['correctIndex'],range(4))
                self.assertGreater(len(q['explanation']),90)
                self.assertTrue(q['source'])
                self.assertTrue(q['parameters'])
                self.assertTrue(q['topic'])
                self.assertIn(q['scope'],{'Emisyon','İmisyon','Ortak'})

    def test_every_catalog_heading_has_questions(self):
        catalog={}
        for filename in ('standards.json','standards_extra.json','standards_overrides.json'):
            for x in json.loads((ROOT/'assets'/filename).read_text(encoding='utf-8')):catalog[x['code']]=x
        self.assertEqual(set(catalog),{c['code'] for c in BANK['catalog']})
        for code in catalog:
            self.assertTrue(any(code in q['standards'] for q in BANK['questions']),code)

    def test_immission_has_substantial_coverage(self):
        qs=[q for q in BANK['questions'] if q['scope']=='İmisyon']
        self.assertGreaterEqual(len(qs),25)
        for parameter in ('PM10 / PM2,5','Çöken toz','Pasif örnekleme'):
            self.assertTrue(any(parameter in q['parameters'] for q in qs),parameter)

    def test_no_foreign_standard_keys(self):
        keys={c['code'] for c in BANK['catalog']}
        for q in BANK['questions']:self.assertTrue(set(q['standards'])<=keys,q['id'])

    def test_method_numbers_do_not_collide_in_parameter_filters(self):
        for method,param in [('CARB Method 426','Siyanür / HCN'),('CARB Method 425','Krom(VI)')]:
            qs=[q for q in BANK['questions'] if method in q['standards']]
            self.assertTrue(qs)
            for q in qs:
                self.assertIn(param,q['parameters'])
                self.assertNotIn('Nem',q['parameters'])

    def test_method_one_is_not_method_thirteen_or_seventeen(self):
        q=next(q for q in BANK['questions'] if 'açılar +30°' in q['prompt'])
        self.assertIn('TS EN 15259 / EPA Method 1',q['standards'])
        self.assertNotIn('EPA Method 13A',q['standards'])
        self.assertNotIn('EPA Method 17',q['standards'])
        velocity=next(q for q in BANK['questions'] if q['prompt'].startswith('Pitot ile hız hesabında'))
        self.assertNotIn('EPA Method 26A',velocity['standards'])
        self.assertNotIn('EPA Method 29',velocity['standards'])


if __name__=='__main__':unittest.main()
