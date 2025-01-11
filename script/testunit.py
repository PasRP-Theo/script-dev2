import unittest
import pandas as pd
from unittest.mock import patch
from io import StringIO
import tempfile
from pathlib import Path
import sys
import os

# Ajout du dossier parent au PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from inventaire_gestionnaire import InventoryManager, ColorLogger


class TestColorLogger(unittest.TestCase):
    @patch('builtins.print')
    def test_all_logger_methods(self, mock_print):
        logger = ColorLogger()

        logger.error("erreur test")
        logger.success("succès test")
        logger.info("info test")

        self.assertEqual(mock_print.call_count, 3)


class TestInventoryManager(unittest.TestCase):
    def setUp(self):
        """Configuration initiale pour chaque test"""
        self.manager = InventoryManager()
        self.test_dir = tempfile.mkdtemp()

        # Données de test valides
        self.valid_data = pd.DataFrame({
            'nom du produit': ['Produit1', 'Produit2'],
            'catégorie': ['Cat1', 'Cat2'],
            'quantité': [10, 20],
            'prix unitaire': [100.0, 200.0]
        })

        # Données invalides
        self.invalid_data = pd.DataFrame({
            'nom du produit': ['Produit1'],
            'catégorie': ['Cat1']
        })

    def tearDown(self):
        """Nettoyage après chaque test"""
        # Supprimer les fichiers temporaires
        for file in Path(self.test_dir).glob('*.csv'):
            file.unlink()
        os.rmdir(self.test_dir)

    def create_test_csv(self, data, filename):
        """Crée un fichier CSV de test"""
        filepath = Path(self.test_dir) / filename
        data.to_csv(filepath, index=False, encoding='latin1')
        return filepath

    def test_validate_data(self):
        """Test de la validation des données"""
        # Test données valides
        is_valid, missing = self.manager.validate_data(self.valid_data)
        self.assertTrue(is_valid)
        self.assertEqual(len(missing), 0)

        # Test données invalides
        is_valid, missing = self.manager.validate_data(self.invalid_data)
        self.assertFalse(is_valid)
        self.assertEqual(len(missing), 2)

    def test_charger_valid_files(self):
        """Test du chargement de fichiers valides"""
        # Créer plusieurs fichiers valides
        self.create_test_csv(self.valid_data, 'valid1.csv')
        self.create_test_csv(self.valid_data, 'valid2.csv')

        with patch('sys.stdout', new=StringIO()):
            self.manager.do_charger(self.test_dir)

        self.assertEqual(len(self.manager.inventory), 4)

    def test_charger_mixed_files(self):
        # Créer un mélange de fichiers valides et invalides
        self.create_test_csv(self.valid_data, 'valid.csv')
        self.create_test_csv(self.invalid_data, 'invalid.csv')

        with patch('sys.stdout', new=StringIO()):
            self.manager.do_charger(self.test_dir)

        self.assertEqual(len(self.manager.inventory), 2)

    def test_charger_directory_not_found(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.manager.do_charger("/chemin/inexistant")
        self.assertIn("Dossier non trouvé", mock_stdout.getvalue())

    def test_charger_empty_directory(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.manager.do_charger(self.test_dir)
        self.assertIn("Aucun fichier valide trouvé", mock_stdout.getvalue())

    def test_afficher_empty_inventory(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.manager.do_afficher("")
        self.assertIn("L'inventaire est vide", mock_stdout.getvalue())

    def test_afficher_with_data(self):
        self.manager.inventory = self.valid_data

        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.manager.do_afficher("")
        output = mock_stdout.getvalue()

        self.assertIn("Produit1", output)
        self.assertIn("Produit2", output)

    def test_chercher_empty_term(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.manager.do_chercher("")
        self.assertIn("Veuillez spécifier un terme de recherche", mock_stdout.getvalue())

    def test_chercher_empty_inventory(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.manager.do_chercher("test")
        self.assertIn("L'inventaire est vide", mock_stdout.getvalue())

    def test_chercher_exact_match(self):
        self.manager.inventory = self.valid_data

        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.manager.do_chercher("Produit1")
        output = mock_stdout.getvalue()

        self.assertIn("Produit1", output)
        self.assertNotIn("Produit2", output)

    def test_chercher_partial_match(self):
        self.manager.inventory = self.valid_data

        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.manager.do_chercher("Produit")
        output = mock_stdout.getvalue()

        self.assertIn("Produit1", output)
        self.assertIn("Produit2", output)

    def test_chercher_no_match(self):
        self.manager.inventory = self.valid_data

        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.manager.do_chercher("InexistantProduit")
        self.assertIn("Aucun produit trouvé", mock_stdout.getvalue())

    def test_chercher_case_insensitive(self):
        self.manager.inventory = self.valid_data

        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.manager.do_chercher("produit1")
        self.assertIn("Produit1", mock_stdout.getvalue())

    def test_chercher_prix_empty_inventory(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.manager.do_chercher_prix("100 200")
        self.assertIn("L'inventaire est vide", mock_stdout.getvalue())

    def test_chercher_prix_valid_range(self):
        self.manager.inventory = self.valid_data
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.manager.do_chercher_prix("50 150")
        output = mock_stdout.getvalue()
        self.assertIn("Produit1", output)
        self.assertNotIn("Produit2", output)

    def test_chercher_quantite_empty_inventory(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.manager.do_chercher_quantite("10 20")
        self.assertIn("L'inventaire est vide", mock_stdout.getvalue())

    def test_chercher_quantite_valid_range(self):
        self.manager.inventory = self.valid_data
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.manager.do_chercher_quantite("5 15")
        output = mock_stdout.getvalue()
        self.assertIn("Produit1", output)
        self.assertNotIn("Produit2", output)

    # Nouveaux tests pour chercher_categorie
    def test_chercher_categorie_empty_term(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.manager.do_chercher_categorie("")
        self.assertIn("Veuillez spécifier une catégorie", mock_stdout.getvalue())

    def test_chercher_categorie_empty_inventory(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.manager.do_chercher_categorie("Cat1")
        self.assertIn("L'inventaire est vide", mock_stdout.getvalue())

    def test_chercher_categorie_exact_match(self):
        self.manager.inventory = self.valid_data
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.manager.do_chercher_categorie("Cat1")
        output = mock_stdout.getvalue()
        self.assertIn("Produit1", output)
        self.assertNotIn("Produit2", output)

    def test_chercher_categorie_no_match(self):
        self.manager.inventory = self.valid_data
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.manager.do_chercher_categorie("CatInexistante")
        self.assertIn("Aucun produit trouvé dans la catégorie", mock_stdout.getvalue())

    def test_rapport_empty_inventory(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.manager.do_rapport()
        self.assertIn("L'inventaire est vide", mock_stdout.getvalue())

    def test_rapport_generation(self):
        self.manager.inventory = self.valid_data

        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            with patch('builtins.input', return_value='n'):
                self.manager.do_rapport()

        output = mock_stdout.getvalue()
        self.assertIn("Rapport Récapitulatif", output)
        self.assertIn("Cat1", output)
        self.assertIn("Cat2", output)

    def test_rapport_export(self):
        self.manager.inventory = self.valid_data
        export_path = Path(self.test_dir) / "rapport.csv"

        with patch('sys.stdout', new=StringIO()):
            self.manager.do_rapport(str(export_path))

        self.assertTrue(export_path.exists())
        exported_data = pd.read_csv(export_path)
        self.assertGreater(len(exported_data), 0)

    def test_rapport_interactive_export(self):
        self.manager.inventory = self.valid_data
        export_path = Path(self.test_dir) / "rapport_interactif.csv"

        with patch('sys.stdout', new=StringIO()):
            with patch('builtins.input', side_effect=['o', str(export_path)]):
                self.manager.do_rapport()

        self.assertTrue(export_path.exists())

    def test_quitter(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            result = self.manager.do_quitter("")

        self.assertTrue(result)
        self.assertIn("Au revoir!", mock_stdout.getvalue())

    def test_aide(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.manager.do_aide("")

        output = mock_stdout.getvalue()
        self.assertIn("Commandes Disponibles", output)
        self.assertIn("charger", output)
        self.assertIn("afficher", output)
        self.assertIn("chercher", output)
        self.assertIn("chercher_prix", output)
        self.assertIn("chercher_quantite", output)
        self.assertIn("chercher_categorie", output)
        self.assertIn("rapport", output)
        self.assertIn("quitter", output)

    def test_rapport_huge_numbers(self):
        huge_data = pd.DataFrame({
            'nom du produit': ['Produit1', 'Produit2'],
            'catégorie': ['Cat1', 'Cat1'],
            'quantité': [1000000, 2000000],
            'prix unitaire': [1000000.0, 2000000.0]
        })
        self.manager.inventory = huge_data

        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            with patch('builtins.input', return_value='n'):
                self.manager.do_rapport()

        output = mock_stdout.getvalue()
        self.assertIn("1500000.0", output)  # Moyenne des quantités

    def test_input_sanitization(self):
        # Test avec des chemins malformés
        with patch('sys.stdout', new=StringIO()):
            self.manager.do_charger("../../../etc/passwd")  # Tentative d'accès à un fichier système
            self.assertTrue(self.manager.inventory.empty)

            self.manager.do_charger("C:\\Windows\\System32")  # Tentative d'accès à un dossier système
            self.assertTrue(self.manager.inventory.empty)


if __name__ == '__main__':
    unittest.main()
