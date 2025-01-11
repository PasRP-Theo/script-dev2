# Gestionnaire d'Inventaire

Le script se trouve aussi dans le wiki

## Description
Ce script permet de gérer un inventaire stocké dans des fichiers CSV. Il propose différentes fonctionnalités telles que la recherche de produits, le filtrage par catégorie ou par prix, et la génération de rapports récapitulatifs.

# Gestionnaire d'Inventaire

## Fonctionnalités Principales
- Charger des fichiers CSV contenant l'inventaire.
- Rechercher des produits par nom, catégorie, quantité ou prix.
- Filtrer les produits par plage de prix ou de quantité.
- Générer un rapport récapitulatif de l'inventaire.
- Exporter les résultats ou rapports au format CSV.

---

## Installation

### Prérequis
- Python 3.8 ou supérieur.
- Modules Python requis :
  - `pandas`
  - `argparse`
  - `colorama`

### Installation des dépendances
Installez les modules requis avec la commande suivante :

pip install pandas colorama

Voici votre documentation convertie au format Wiki pour un dépôt Git : 

# Gestionnaire d'Inventaire

## Utilisation

### Démarrer le programme
Pour démarrer le gestionnaire d'inventaire, exécutez le script principal :

```bash
python gestionnaire_inventaire.py
```

### Menu Interactif
Le programme offre une interface interactive où vous pouvez utiliser les commandes suivantes :

#### Commandes disponibles
- **`charger <chemin_du_dossier>`** : Charger tous les fichiers CSV d'un dossier.
- **`afficher`** : Afficher l'inventaire complet.
- **`chercher <nom_du_produit>`** : Rechercher un produit par son nom.
- **`chercher_prix <prix_min> <prix_max>`** : Rechercher des produits dans une plage de prix.
- **`chercher_quantite <quantite_min> <quantite_max>`** : Rechercher des produits par quantité.
- **`chercher_categorie <nom_categorie>`** : Rechercher des produits par catégorie.
- **`rapport [chemin_fichier]`** : Générer un rapport de l'inventaire (optionnellement exporté au format CSV).
- **`quitter`** : Quitter le programme.

---

### Exemple d'utilisation

#### Charger un dossier contenant des fichiers CSV :
```bash
charger /chemin/vers/repertoire
```

#### Rechercher un produit par son nom :
```bash
chercher "chaise"
```

#### Rechercher par plage de prix :
```bash
chercher_prix 50 200
```

#### Générer un rapport exporté au format CSV :
```bash
rapport /chemin/vers/rapport.csv
```

---

## Structure des fichiers CSV
Vos fichiers CSV doivent contenir les colonnes suivantes :

- **`nom du produit`**
- **`catégorie`**
- **`quantité`**
- **`prix unitaire`**

---

## Lancer des Commandes Directement
Vous pouvez également utiliser les arguments en ligne de commande sans entrer dans le mode interactif :

```bash
python gestionnaire_inventaire.py --charger /chemin/vers/repertoire
python gestionnaire_inventaire.py --chercher "chaise"
python gestionnaire_inventaire.py --chercher-prix 50 200
python gestionnaire_inventaire.py --rapport /chemin/vers/rapport.csv
```

---

## Exemple de rapport
Un rapport regroupe l'inventaire par catégorie, en affichant les informations suivantes :

- **Quantité totale**
- **Quantité moyenne**
- **Nombre de produits**
- **Prix moyen, minimum et maximum**

---


## Utilisation de l'ia
- Conception du script
- Fonctionnalitées smart de l'ia
- Test Unitaires
- Aides a la conception du script

