import unittest
import pandas as pd
from script import load_csv_files, search_product, filter_by_category, filter_by_price, generate_report

class TestInventoryManager(unittest.TestCase):

    def setUp(self):
        # Setup - création de données fictives pour les tests
        self.data = pd.DataFrame({
            'nom du produit': ['riz', 'pates', 'chocolat'],
            'catégorie': ['alimentaire', 'alimentaire', 'gourmandise'],
            'quantité': [500, 200, 100],
            'prix unitaire': [1.5, 2.0, 3.0]
        })

    def test_load_csv_files(self):
        # Test for loading CSV files
        df = load_csv_files('path_to_your_test_data')  # Replace with actual path
        self.assertFalse(df.empty)

    def test_search_product(self):
        results = search_product(self.data, 'riz')
        if results is not None:
            self.assertEqual(len(results), 1)
        else:
            self.fail("search_product returned None")

    def test_filter_by_category(self):
        results = filter_by_category(self.data, 'alimentaire')
        self.assertEqual(len(results), 2)  # Expects 2 matches for 'alimentaire'

    def test_filter_by_price(self):
        results = filter_by_price(self.data, min_price=1.0, max_price=2.0)
        self.assertEqual(len(results), 2)  # Expects 2 products within the given price range

    def test_generate_report(self):
        summary = generate_report(self.data)
        self.assertIn('Total Quantité', summary.columns)
        self.assertIn('Prix Moyen', summary.columns)

if __name__ == '__main__':
    unittest.main()
