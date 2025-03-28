import pandas as pd  # Pour la manipulation des données
import argparse     # Pour gérer les arguments en ligne de commande
from cmd import Cmd # Pour créer une interface en ligne de commande
from colorama import Fore, Style, init  # Pour colorer la sortie console
from typing import List, Optional       # Pour le typage
from pathlib import Path               # Pour la gestion des chemins de fichiers

init(autoreset=True)

# mets les messsages d'erreur en couleur
class ColorLogger:
    @staticmethod
    def error(message: str) -> None:
        print(Fore.RED + str(message) + Style.RESET_ALL)

    @staticmethod
    def success(message: str) -> None:
        print(Fore.GREEN + str(message) + Style.RESET_ALL)

    @staticmethod
    def info(message: str) -> None:
        print(Fore.BLUE + str(message) + Style.RESET_ALL)

class InventoryManager(Cmd):
    intro = "\nBienvenue dans le Gestionnaire d'Inventaire. Tapez 'aide' ou '?' pour voir les commandes disponibles.\n"
    prompt = "(inventaire) "

    def __init__(self):
        super().__init__()
        self.inventory = pd.DataFrame()  # DataFrame vide pour stocker l'inventaire
        self.required_columns = ['nom du produit', 'catégorie', 'quantité', 'prix unitaire']
        self.logger = ColorLogger()

    def validate_data(self, data: pd.DataFrame) -> tuple[bool, List[str]]:
        """valider les datas avec les bonnes colonnes."""
        missing_columns = [col for col in self.required_columns if col not in data.columns]
        return len(missing_columns) == 0, missing_columns

    def do_charger(self, directory_path: str) -> None:
        """
        Charger les fichiers CSV du dossier spécifié.
        Usage: charger <chemin_du_dossier>
        Parcourt un dossier pour trouver des fichiers CSV
        Vérifie que chaque fichier a les colonnes requises
        Concatène tous les fichiers valides dans un seul DataFrame
        """
        directory_path = directory_path.strip()
        if not directory_path:
            self.logger.error("Veuillez spécifier un chemin de dossier.")
            return

        directory = Path(directory_path)
        if not directory.is_dir():
            self.logger.error("Dossier non trouvé.")
            return

        all_data = []
        valid_files = 0

        for file_path in directory.glob('*.csv'):
            try:
                data = pd.read_csv(file_path, encoding="latin1")
                is_valid, missing_cols = self.validate_data(data)

                if is_valid:
                    data = data[self.required_columns]
                    data['Fichier Source'] = file_path.name
                    all_data.append(data)
                    valid_files += 1
                    self.logger.success(f"Chargé: {file_path.name}")
                else:
                    self.logger.error(f"Colonnes manquantes dans {file_path.name}: {missing_cols}")
            except Exception as e:
                self.logger.error(f"Erreur lors du chargement de {file_path.name}: {str(e)}")

        if valid_files > 0:
            self.inventory = pd.concat(all_data, ignore_index=True)
            self.logger.success(f"{valid_files} fichier(s) chargé(s) avec succès.")
        else:
            self.logger.error("Aucun fichier valide trouvé.")

    def do_afficher(self, arg: str) -> None:
        """
        Afficher l'inventaire complet.
        Usage: afficher
        """
        if self.inventory.empty:
            self.logger.error("L'inventaire est vide. Chargez d'abord des données.")
            return

        with pd.option_context('display.max_rows', None,
                               'display.max_columns', None,
                               'display.width', None):
            self.logger.info("\n" + self.inventory.to_string())

    def do_chercher(self, term: str) -> None:
        """
        Chercher un produit par nom.
        Usage: chercher <nom_du_produit>
        Utiliser pandas pour filtrer les données
        Gestion des erreurs avec try/sauf
        Affichage formaté des résultats
        """
        if not term:
            self.logger.error("Veuillez spécifier un terme de recherche.")
            return

        if self.inventory.empty:
            self.logger.error("L'inventaire est vide. Chargez d'abord des données.")
            return

        try:
            results = self.inventory[
                self.inventory['nom du produit'].str.contains(term, case=False, na=False)
            ]
            if results.empty:
                self.logger.info("Aucun produit trouvé.")
            else:
                self.logger.info("\n" + results.to_string())
        except Exception as e:
            self.logger.error(f"Erreur lors de la recherche: {str(e)}")

    def do_chercher_prix(self, arg: str) -> None:
        """
        Chercher des produits par intervalle de prix.
        Usage: chercher_prix <prix_min> <prix_max>
        """
        if self.inventory.empty:
            self.logger.error("L'inventaire est vide. Chargez d'abord des données.")
            return

        try:
            args = arg.split()
            if len(args) != 2:
                self.logger.error("Usage: chercher_prix <prix_min> <prix_max>")
                return

            prix_min, prix_max = float(args[0]), float(args[1])
            results = self.inventory[
                (self.inventory['prix unitaire'] >= prix_min) &
                (self.inventory['prix unitaire'] <= prix_max)
            ]

            if results.empty:
                self.logger.info(f"Aucun produit trouvé entre {prix_min}€ et {prix_max}€.")
            else:
                self.logger.info(f"\nProduits entre {prix_min}€ et {prix_max}€:")
                self.logger.info("\n" + results.to_string())

        except ValueError:
            self.logger.error("Les prix doivent être des nombres valides.")
        except Exception as e:
            self.logger.error(f"Erreur lors de la recherche: {str(e)}")

    def do_chercher_quantite(self, arg: str) -> None:
        """
        Chercher des produits par intervalle de quantité.
        Usage: chercher_quantite <quantite_min> <quantite_max>
        """
        if self.inventory.empty:
            self.logger.error("L'inventaire est vide. Chargez d'abord des données.")
            return

        try:
            args = arg.split()
            if len(args) != 2:
                self.logger.error("Usage: chercher_quantite <quantite_min> <quantite_max>")
                return

            qte_min, qte_max = int(args[0]), int(args[1])
            results = self.inventory[
                (self.inventory['quantité'] >= qte_min) &
                (self.inventory['quantité'] <= qte_max)
            ]

            if results.empty:
                self.logger.info(f"Aucun produit trouvé avec une quantité entre {qte_min} et {qte_max}.")
            else:
                self.logger.info(f"\nProduits avec quantité entre {qte_min} et {qte_max}:")
                self.logger.info("\n" + results.to_string())

        except ValueError:
            self.logger.error("Les quantités doivent être des nombres entiers valides.")
        except Exception as e:
            self.logger.error(f"Erreur lors de la recherche: {str(e)}")

    def do_chercher_categorie(self, categorie: str) -> None:
        """
        Chercher des produits par catégorie.
        Usage: chercher_categorie <nom_categorie>
        """
        if not categorie:
            self.logger.error("Veuillez spécifier une catégorie.")
            return

        if self.inventory.empty:
            self.logger.error("L'inventaire est vide. Chargez d'abord des données.")
            return

        try:
            results = self.inventory[
                self.inventory['catégorie'].str.contains(categorie, case=False, na=False)
            ]
            if results.empty:
                self.logger.info(f"Aucun produit trouvé dans la catégorie '{categorie}'.")
            else:
                self.logger.info(f"\nProduits de la catégorie '{categorie}':")
                self.logger.info("\n" + results.to_string())
        except Exception as e:
            self.logger.error(f"Erreur lors de la recherche: {str(e)}")

    def do_rapport(self, export_path: Optional[str] = None) -> None:
        """
        Générer un rapport d'inventaire avec option d'export.
        Usage: rapport [chemin_fichier]
        """
        if self.inventory.empty:
            self.logger.error("L'inventaire est vide. Chargez d'abord des données.")
            return

        try:
            report = self.inventory.groupby('catégorie').agg({
                'quantité': ['sum', 'mean', 'count'],
                'prix unitaire': ['mean', 'min', 'max']
            }).round(2)

            report.columns = [f"{col[0]}_{col[1]}" for col in report.columns]

            self.logger.info("\n=== Rapport Récapitulatif ===")
            self.logger.info("\n" + report.to_string())

            if export_path:
                report.to_csv(export_path)
                self.logger.success(f"Rapport exporté vers {export_path}")
            else:
                if input("Voulez-vous exporter ce rapport (o/n)? ").lower() == 'o':
                    path = input("Chemin du fichier d'export: ")
                    report.to_csv(path)
                    self.logger.success(f"Rapport exporté vers {path}")

        except Exception as e:
            self.logger.error(f"Erreur lors de la génération du rapport: {str(e)}")

    def do_quitter(self, arg: str) -> bool:
        """
        Quitter le programme.
        Usage: quitter
        """
        self.logger.info("Au revoir!")
        return True

    def do_aide(self, arg: str) -> None:
        """Afficher l'aide des commandes."""
        commands = {
            'charger': 'Charger les fichiers CSV du dossier spécifié',
            'afficher': "Afficher l'inventaire complet",
            'chercher': 'Chercher un produit par nom',
            'chercher_prix': 'Chercher des produits par intervalle de prix',
            'chercher_quantite': 'Chercher des produits par intervalle de quantité',
            'chercher_categorie': 'Chercher des produits par catégorie',
            'rapport': "Générer un rapport d'inventaire",
            'quitter': 'Quitter le programme',
            'aide': 'Afficher cette aide'
        }

        self.logger.info("\n=== Commandes Disponibles ===")
        for cmd, desc in commands.items():
            self.logger.info(f"{cmd:20} : {desc}")

def main():
    parser = argparse.ArgumentParser(description="Gestionnaire d'Inventaire CLI")
    parser.add_argument("--charger", help="Charger les fichiers CSV d'un dossier")
    parser.add_argument("--chercher", help="Chercher un produit par nom")
    parser.add_argument("--chercher-prix", nargs=2, type=float, help="Chercher par intervalle de prix (min max)")
    parser.add_argument("--chercher-quantite", nargs=2, type=int, help="Chercher par intervalle de quantité (min max)")
    parser.add_argument("--chercher-categorie", help="Chercher par catégorie")
    parser.add_argument("--rapport", help="Générer et sauvegarder un rapport (chemin du fichier)")
    parser.add_argument("--afficher", action="store_true", help="Afficher l'inventaire complet")

    args = parser.parse_args()
    manager = InventoryManager()

    if any(vars(args).values()):
        if args.charger:
            manager.do_charger(args.charger)
        if args.chercher:
            manager.do_chercher(args.chercher)
        if args.chercher_prix:
            manager.do_chercher_prix(f"{args.chercher_prix[0]} {args.chercher_prix[1]}")
        if args.chercher_quantite:
            manager.do_chercher_quantite(f"{args.chercher_quantite[0]} {args.chercher_quantite[1]}")
        if args.chercher_categorie:
            manager.do_chercher_categorie(args.chercher_categorie)
        if args.rapport:
            manager.do_rapport(args.rapport)
        if args.afficher:
            manager.do_afficher("")
    else:
        manager.cmdloop()

if __name__ == "__main__":
    main()
