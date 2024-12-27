import unittest
import pandas as pd
from script import load_csv_files, search_product, filter_by_category, filter_by_price, generate_report

class TestInventoryManager(unittest.TestCase):

    def setUp(self):
        self.data = pd.DataFrame({
            'nom du produit': ['riz', 'pates', 'chocolat'],
            'catégorie': ['alimentaire', 'alimentaire', 'gourmandise'],
            'quantité': [500, 200, 100],
            'prix unitaire': [1.5, 2.0, 3.0]
        })

    def test_load_csv_files(self):
        df = load_csv_files('path_to_your_test_data')
        self.assertFalse(df.empty)

    def test_search_product(self):
        results = search_product(self.data, 'riz')
        if results is not None:
            self.assertEqual(len(results), 1)
        else:
            self.fail("search_product returned None")

    def test_filter_by_category(self):
        results = filter_by_category(self.data, 'alimentaire')
        self.assertEqual(len(results), 2)

    def test_filter_by_price(self):
        results = filter_by_price(self.data, min_price=1.0, max_price=2.0)
        self.assertEqual(len(results), 2)

    def test_generate_report(self):
        summary = generate_report(self.data)
        self.assertIn('Total Quantité', summary.columns)
        self.assertIn('Prix Moyen', summary.columns)

if __name__ == '__main__':
    unittest.main()
