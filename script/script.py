import os
import csv
import pandas as pd
import unittest

# Fonction pour charger les fichiers CSV
def load_csv_files(directory):
    print("Chargement des fichiers CSV...")
    all_data = []
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            filepath = os.path.join(directory, filename)
            print(f"Chargement du fichier: {filename}")
            try:
                data = pd.read_csv(filepath, encoding="latin1")
                data['Source File'] = filename
                all_data.append(data)
            except Exception as e:
                print(f"Erreur lors du chargement de {filename}: {e}")
    if all_data:
        return pd.concat(all_data, ignore_index=True)
    else:
        print("Aucun fichier CSV dans le répertoire.")
        return pd.DataFrame()

# Fonction pour rechercher un produit
def search_product(data, query):
    results = data[data['nom du produit'].str.contains(query, case=False, na=False)]
    return results

# Fonction pour filtrer par catégorie
def filter_by_category(data, category):
    results = data[data['catégorie'].str.contains(category, case=False, na=False)]
    return results if not results.empty else None

# Fonction pour rechercher par plage de prix
def filter_by_price(data, min_price, max_price):
    try:
        results = data[(data['prix unitaire'] >= min_price) & (data['prix unitaire'] <= max_price)]
        return results if not results.empty else None
    except ValueError:
        print("Veuillez entrer des valeurs numériques valides pour les prix.")
        return None

# Fonction pour générer un rapport récapitulatif
def generate_report(data):
    summary = data.groupby('catégorie').agg({
        'quantité': 'sum',
        'prix unitaire': 'mean'
    }).rename(columns={
        'quantité': 'Total Quantité',
        'prix unitaire': 'Prix Moyen'
    })
    print("\n=== Rapport Récapitulatif ===")
    print(summary)

    export = input("Voulez-vous exporter ce rapport en CSV ? (y/n): ").lower()
    if export == 'y':
        output_path = input("Entrez le chemin pour enregistrer le fichier (par ex: rapport.csv): ")
        summary.to_csv(output_path)
        print(f"Rapport exporté avec succès vers {output_path}.")
    else:
        print("Exportation annulée.")

# Main
if __name__ == "__main__":
    data_dir = input("Entrez le chemin du répertoire contenant les fichiers CSV: ")
    if not os.path.exists(data_dir):
        print("Le chemin du répertoire est incorrect ou introuvable.")
    else:
        inventory_data = load_csv_files(data_dir)

        if not inventory_data.empty:
            while True:
                print("\n=== Gestionnaire d'Inventaire ===")
                print("1. Rechercher un produit")
                print("2. Filtrer par catégorie")
                print("3. Rechercher par plage de prix")
                print("4. Générer un rapport récapitulatif")
                print("5. Quitter")
                
                choice = input("Votre choix: ")
                if choice == "1":
                    query = input("Entrez le nom du produit ou un mot-clé: ").strip()
                    results = search_product(inventory_data, query)
                    print(results if not results.empty else "Aucun produit trouvé.")

                elif choice == "2":
                    category = input("Entrez la catégorie: ").strip()
                    results = filter_by_category(inventory_data, category)
                    if results is not None:
                        print(results)
                    else:
                        print("Aucun produit trouvé dans cette catégorie.")

                elif choice == "3":
                    try:
                        min_price = float(input("Entrez le prix minimum: "))
                        max_price = float(input("Entrez le prix maximum: "))
                        results = filter_by_price(inventory_data, min_price, max_price)
                        if results is not None:
                            print(results)
                        else:
                            print("Aucun produit trouvé dans cette plage de prix.")
                    except ValueError:
                        print("Veuillez entrer des valeurs numériques valides pour les prix.")

                elif choice == "4":
                    generate_report(inventory_data)

                elif choice == "5":
                    print("Merci d'avoir utilisé le Gestionnaire d'Inventaire. Au revoir !")
                    break

                else:
                    print("Choix invalide. Veuillez réessayer.")
        else:
            print("Aucune donnée à traiter. Fin du programme.")
