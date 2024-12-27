import unittest
import pandas as pd
from script import chargement_csv, chercher_produit, filtrer_par_cat, filtrer_par_prix, generer_rapport

class TestInventoryManager(unittest.TestCase):

    def setUp(self):
        self.data = pd.DataFrame({
            'nom du produit': ['riz', 'pates', 'chocolat'],
            'catégorie': ['alimentaire', 'alimentaire', 'gourmandise'],
            'quantité': [500, 200, 100],
            'prix unitaire': [1.5, 2.0, 3.0]
        })

    def test_load_csv_files(self):
        df = chargement_csv('path_to_your_test_data')
        self.assertFalse(df.empty)

    def test_search_product(self):
        results = chercher_produit(self.data, 'riz')
        if results is not None:
            self.assertEqual(len(results), 1)
        else:
            self.fail("search_product returned None")

    def test_filter_by_category(self):
        results = filtrer_par_cat(self.data, 'alimentaire')
        self.assertEqual(len(results), 2)

    def test_filter_by_price(self):
        results = filtrer_par_prix(self.data, min_price=1.0, max_price=2.0)
        self.assertEqual(len(results), 2)

    def test_generate_report(self):
        summary = generer_rapport(self.data)
        self.assertIn('Total Quantité', summary.columns)
        self.assertIn('Prix Moyen', summary.columns)

if __name__ == '__main__':
    unittest.main()
