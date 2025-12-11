# TP1 - Data Lake vs Data Warehouse

## Description

Ce projet est une implémentation pratique comparant deux approches de gestion de données : **Data Lake** et **Data Warehouse**. Il démontre les différences fondamentales entre le stockage brut de données et le stockage structuré.

## Structure du projet

```
TP1/
├── data_lake/
│   ├── raw/                  # Données brutes (Data Lake)
│   │   └── ventes_2024.csv   # Fichier CSV avec les données de ventes
│   ├── transformed/          # Données transformées
│   └── analytics/            # Résultats d'analyse
├── entreprise_dw.db          # Base de données Data Warehouse (SQLite)
├── etl_script.py             # Script ETL pour charger les données
├── analyse_comparative.md    # Analyse comparative détaillée
├── verification.py           # Script de vérification du projet
└── README.md                 # Ce fichier
```

## Prérequis

- Python 3.x
- SQLite (inclus avec Python)
- Bibliothèques Python standard (csv, sqlite3, pathlib)

## Installation et exécution

### 1. Cloner le projet (si nécessaire)

```bash
git clone [url-du-depot]
cd TP1
```

### 2. Exécuter le script ETL

```bash
python etl_script.py
```

Ce script va :
- Créer la base de données `entreprise_dw.db`
- Créer la table `ventes` avec la structure appropriée
- Lire les données du fichier CSV
- Calculer le total pour chaque vente (quantité × prix unitaire)
- Charger les données dans la base

### 3. Vérifier le projet

```bash
python verification.py
```

Ce script vérifie que tous les composants du projet sont correctement mis en place.

## Contenu détaillé

### Data Lake

Le Data Lake est implémenté dans le dossier `data_lake/` avec la structure suivante :

- **raw/** : Contient les données brutes au format CSV
  - `ventes_2024.csv` : Données de ventes avec les colonnes Date, Client, Produit, Quantité, PrixUnitaire

- **transformed/** : Prévu pour les données transformées (non utilisé dans ce TP basique)
- **analytics/** : Prévu pour les résultats d'analyse

### Data Warehouse

Le Data Warehouse est implémenté avec SQLite :

- **Base de données** : `entreprise_dw.db`
- **Table** : `ventes` avec les colonnes :
  - `id` : Clé primaire auto-incrémentée
  - `date` : Date de la vente
  - `client` : Nom du client
  - `produit` : Nom du produit
  - `quantite` : Quantité vendue
  - `prix_unitaire` : Prix unitaire du produit
  - `total` : Total calculé (quantité × prix unitaire)

### Script ETL

Le script `etl_script.py` implémente un processus ETL (Extract, Transform, Load) simple :

1. **Extract** : Lit les données du fichier CSV
2. **Transform** : Calcule le total pour chaque enregistrement
3. **Load** : Charge les données dans la base SQLite

### Analyse comparative

Le fichier `analyse_comparative.md` contient une analyse détaillée comparant :

- Types de requêtes possibles dans chaque approche
- Niveau de structuration des données
- Gouvernance, qualité et sécurité
- Cas d'usage appropriés
- Tableau comparatif synthétique

## Résultats

### Données de vente

| ID | Date       | Client | Produit   | Quantité | Prix Unitaire | Total  |
|----|------------|--------|------------|-----------|----------------|--------|
| 1  | 2024-01-01 | Jean   | PC         | 2         | 1200.00        | 2400.00|
| 2  | 2024-01-02 | Marie  | Téléphone  | 1         | 700.00         | 700.00 |
| 3  | 2024-01-03 | Paul   | Écran      | 3         | 300.00         | 900.00 |

### Total des ventes : 4000.00 €

## Conclusion

Ce TP illustre les différences fondamentales entre :

- **Data Lake** : Stockage brut, flexible, idéal pour l'exploration et le big data
- **Data Warehouse** : Stockage structuré, optimisé pour l'analyse et le reporting

Le choix entre les deux approches dépend des besoins spécifiques de l'entreprise en termes de flexibilité, performance, qualité des données et cas d'usage.

## Auteur

Mistral Vibe - Assistant IA pour l'implémentation technique