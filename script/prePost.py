class InventoryManager:
    """Class representing an inventory management system.

    This class provides functionalities for managing inventory data loaded from CSV files.
    Author: Théo Mertens
    Date: January 2025
    """

    def do_charger(self, directory_path: str):
        """Load inventory data from CSV files in a specified directory.

        PRE:
        - directory_path est une chaîne non vide représentant le chemin d'un dossier.
        - Le dossier spécifié existe et contient au moins un fichier CSV valide.
        - Les fichiers CSV doivent inclure les colonnes requises : nom du produit, catégorie, quantité, prix unitaire.

        POST:
        - Tous les fichiers CSV valides sont chargés dans l'inventaire (DataFrame self.inventory).
        - Les colonnes des fichiers CSV sont uniformisées en fonction des colonnes requises.
        - La propriété self.inventory contient toutes les données consolidées des fichiers CSV valides.
        - Les fichiers invalides sont signalés avec leurs erreurs spécifiques.
        """

    def do_afficher(self, arg: str):
        """Display the entire inventory in tabular format.

        PRE:
        - La propriété self.inventory contient des données (elle n'est pas vide).

        POST:
        - Affiche tout l'inventaire sous forme de tableau dans le terminal.
        - Si l'inventaire est vide, il y a un message d'erreur qui est affiché.
        """

    def do_rechercher(self, term: str):
        """Search for a product by its name.

        PRE:
        - term est une chaîne non vide représentant le terme a recherché.
        - La propriété self.inventory contient des données (elle n'est pas vide).

        POST:
        - Affiche tous les produits dont le champ nom du produit correspond au terme de recherche (recherche insensible à la casse).
        - Si aucun produit ne correspond, affiche un message d'information indiquant qu'aucun résultat n'a été trouvé.
        - En cas d'erreur, affiche un message d'erreur spécifique.
        """

    def do_rapport(self, export_path: Optional[str] = None):
        """Generate a summary report of the inventory.

        PRE:
        - La propriété self.inventory contient des données (elle n'est pas vide).

        POST:
        - Affiche un rapport récapitulatif basé sur la catégorie (quantité totale, moyenne, prix unitaire moyen, etc.).
        - Si un chemin est spécifié, exporte le rapport sous format CSV à l'emplacement donné.
        - Si aucun chemin n'est donné, demande à l'utilisateur s'il souhaite exporter et gère l'opération en conséquence.
        - En cas d'erreur, affiche un message d'erreur spécifique.
        """

    def do_quitter(self):
        """Exit the inventory management system.

        PRE:

        POST:
        - Termine l'exécution du programme avec un message d'au revoir.
        """
