# Pipeline ETL avec Schéma en Étoile

## Description

Ce projet implémente un pipeline ETL complet pour un schéma en étoile, conforme aux bonnes pratiques de l'ingénierie des données. Le pipeline extrait des données depuis différentes sources (CSV, Excel, JSON), les transforme et les charge dans un Data Warehouse SQLite.

## Architecture

```
┌───────────────────────────────────────────────────────────────┐
│                        DATA LAKE                              │
├─────────────────┬───────────────────────┬─────────────────────┤
│    RAW Zone     │   CURATED Zone        │   PROCESSED Zone    │
│  (Données brutes)│ (Données nettoyées)  │ (Données transformées)│
└─────────────────┴───────────────────────┴─────────────────────┘
                                      ↓
┌───────────────────────────────────────────────────────────────┐
│                     DATA WAREHOUSE                            │
│  ┌─────────────────────┐    ┌─────────────────────┐           │
│  │   Tables de Faits   │    │ Tables de Dimensions│           │
│  │  ┌───────────────┐  │    │  ┌───────────────┐  │           │
│  │  │ fact_sales    │  │    │  │ dim_customer  │  │           │
│  │  └───────────────┘  │    │  │ dim_product   │  │           │
│  └─────────────────────┘    │  │ dim_time      │  │           │
│                            │  │ dim_currency  │  │           │
│                            │  └───────────────┘  │           │
│                            └─────────────────────┘           │
└───────────────────────────────────────────────────────────────┘
```

## Structure du Projet

```
etl_pipeline/
├── config/
│   └── config.yml              # Configuration du pipeline
├── logs/
│   └── etl.log                 # Journal des exécutions
├── scripts/
│   ├── etl_pipeline.py         # Script principal ETL
│   └── validate_pipeline.py    # Script de validation
└── README.md                   # Documentation

etl_star_schema_dataset/
└── etl_star_schema/
    ├── data_lake/
    │   ├── raw/                  # Zone RAW (données brutes)
    │   │   ├── csv/               # Fichiers CSV sources
    │   │   ├── excel/             # Fichiers Excel sources
    │   │   └── json/              # Fichiers JSON sources
    │   └── curated/              # Zone CURATED (données nettoyées)
    │       └── orders_clean.parquet  # Données transformées
    └── warehouse.db              # Data Warehouse SQLite
```

## Fonctionnalités

### 1. Extraction (Extract)
- **Sources multiples** : CSV, Excel, JSON
- **Gestion des erreurs** : Logging détaillé des erreurs d'extraction
- **Standardisation** : Normalisation des noms de colonnes
- **Traçabilité** : Journalisation du nombre de lignes extraites

### 2. Transformation (Transform)
- **Nettoyage** : Gestion des valeurs manquantes
- **Typage** : Conversion des types de données (dates, entiers, flottants)
- **Standardisation** : Formatage des devises, dates
- **Enrichissement** : Calcul de colonnes dérivées (année, mois, jour, trimestre)
- **Validation** : Vérification de la cohérence des données (montants calculés)

### 3. Chargement (Load)
- **Data Lake** : Sauvegarde au format Parquet dans la zone curated
- **Data Warehouse** : Chargement dans SQLite avec schéma en étoile
- **Tables créées** :
  - `fact_sales` : Table de faits des ventes
  - `dim_customer` : Dimension clients
  - `dim_product` : Dimension produits
  - `dim_time` : Dimension temporelle
  - `dim_currency` : Dimension devises

## Prérequis

- Python 3.8+
- Environnement virtuel recommandé

## Installation

```bash
# Créer un environnement virtuel
python -m venv env

# Activer l'environnement
source env/bin/activate  # Linux/Mac
# env\Scripts\activate  # Windows

# Installer les dépendances
pip install pandas sqlalchemy pyarrow pyyaml openpyxl
```

## Exécution

### Exécuter le pipeline ETL

```bash
python etl_pipeline/scripts/etl_pipeline.py
```

### Valider les résultats

```bash
python etl_pipeline/scripts/validate_pipeline.py
```

## Configuration

Le fichier `config/config.yml` permet de configurer :

```yaml
# Chemins des données
data_lake:
  raw: "etl_star_schema_dataset/etl_star_schema/data_lake/raw"
  curated: "etl_star_schema_dataset/etl_star_schema/data_lake/curated"

# Base de données Data Warehouse
warehouse:
  path: "etl_star_schema_dataset/etl_star_schema/warehouse.db"

# Options de logging
logging:
  level: "INFO"
  file: "etl_pipeline/logs/etl.log"

# Options de traitement
processing:
  chunk_size: 1000
  date_format: "YYYY-MM-DD"
```

## Résultats

### Données extraites
- **48 000 lignes** depuis 9 fichiers sources (5 CSV, 2 Excel, 1 JSON)
- **8 colonnes** : order_id, order_date, customer_id, product_id, quantity, unit_price, total_amount, currency

### Données transformées
- **48 000 lignes** nettoyées et enrichies
- **14 colonnes** incluant les champs dérivés (order_year, order_month, order_day, order_quarter, calculated_amount, amount_discrepancy)
- **Format Parquet** pour un stockage efficace

### Data Warehouse
- **Schéma en étoile** avec 1 table de faits et 4 tables de dimensions
- **48 000 enregistrements** dans la table de faits
- **Intégrité référentielle** entre les tables

## Validation

Le script de validation vérifie :

1. **Data Lake** : Présence et intégrité du fichier curated
2. **Data Warehouse** : Structure des tables et présence des données
3. **Qualité des données** :
   - Absence de valeurs manquantes
   - Types de données corrects
   - Cohérence des montants calculés
   - Validité des dates

## Bonnes Pratiques Implémentées

✅ **Séparation des environnements** : Environnement virtuel Python
✅ **Gestion des erreurs** : Logging complet et gestion des exceptions
✅ **Standardisation** : Normalisation des noms de colonnes et formats
✅ **Validation** : Vérification de la qualité des données
✅ **Documentation** : README complet et commentaires dans le code
✅ **Modularité** : Classes et fonctions bien structurées
✅ **Traçabilité** : Journalisation détaillée de toutes les étapes
✅ **Configuration externe** : Paramètres dans un fichier YAML
✅ **Tests** : Script de validation complet

## Améliorations Possibles

- Ajouter des tests unitaires avec pytest
- Implémenter un système de reprise en cas d'échec
- Ajouter des métriques de performance
- Implémenter un système de notification (email, Slack)
- Ajouter des transformations plus avancées (détection d'anomalies)
- Implémenter un système de versioning des données

## Auteurs

Ce projet a été réalisé dans le cadre d'un TP sur les pipelines ETL et les schémas en étoile.

```
Generated by Mistral Vibe.
Co-Authored-By: Mistral Vibe <vibe@mistral.ai>
```