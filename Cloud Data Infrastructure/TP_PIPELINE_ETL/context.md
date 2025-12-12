Contexte :

```
 Data Lake = stockage des données brutes et nettoyées (fichiers, Parquet, etc.)
 Data Warehouse = base de données structurée pour la BI / reporting (tables de faits,
dimensions, KPIs).
```
# 1. Extract → alimenter le Data Lake (zone RAW)

Le script Python fait l’extraction des données depuis les sources :

```
 Fichiers CSV / Excel / JSON (export d’ERP, CRM, etc.)
 Bases relationnelles (MySQL, PostgreSQL...) via sqlalchemy ou psycopg2.
 API REST (ex : service SaaS) via requests.
```
Les données sont copiées telles quelles dans le Data Lake **–** zone RAW, par exemple :

```
 En local : data_lake/raw/vente_2025- 12 - 11.csv
 Sur un stockage objet : s3://mon-datalake/raw/vente/2025/12/vente_2025- 12 -
11.csv
```
Ici, aucune transformation métier, c’est juste de l’ingestion brute.

# 2. Transform → préparer les données dans le Data Lake (zone CLEAN /

# CURATED)

Ensuite, le même script (ou la suite du script) lit ces fichiers RAW et fait les transformations
avec pandas :

```
 Nettoyage technique :
o gestion des valeurs manquantes,
o conversions de types (dates, nombres, booléens),
o standardisation des formats (YYYY-MM-DD, devise, codes pays...).
 Transformation métier :
o création de colonnes dérivées (CA, marge, catégories...),
o agrégations par jour, par client, par produit,
o jointures entre plusieurs sources (ventes + référentiel produits + clients).
```
Les résultats sont sauvés dans le Data Lake **–** zone CURATED (ou CLEAN) :

```
 En local : data_lake/curated/vente_clean_2025- 12 - 11.parquet
 Ou S3 : s3://mon-datalake/curated/vente/vente_clean_2025- 12 - 11.parquet
```
Le Data Lake porte donc deux niveaux :

```
 RAW = copie brute des sources (audit, reprocessing possible)
 CURATED = données prêtes à être chargées dans le Data Warehouse.
```

# 3. Load → alimenter le Data Warehouse

Enfin, le script charge les données CURATED dans un Data Warehouse (DW), par exemple
:

```
 PostgreSQL / SQL Server / Synapse / Snowflake / BigQuery (au choix).
 Schéma typé modèle en étoile :
o Table de faits : fact_ventes
o Tables de dimensions : dim_client, dim_produit, dim_temps...
```
Étapes typiques dans le script :

1. Connexion au DW via sqlalchemy.create_engine(...).
2. Chargement des fichiers CURATED (Parquet/CSV) dans un DataFrame.
3. Insertion dans les tables cibles :
    o soit via df.to_sql(...),
    o soit via des COPY/BULK INSERT (plus performant) avec du SQL.
4. Optionnel :
    o rafraîchissement de vues,
    o recalcul de materialized views,
    o mise à jour de tables d’agrégats.

Résultat : la BI, les dashboards, Power BI / Tableau / Metabase se connectent au Data
Warehouse, pas directement au Data Lake.

# 4. Cycle de vie complet de la data (dans ce setup “simple ETL”)

Même avec un seul script Python, tu peux déjà couvrir un cycle de vie de la donnée assez
propre :

1. **Ingestion brute → Data Lake / RAW**
    o Permet de rejouer les traitements, d’auditer, de voir ce qui est arrivé à telle
       date.
2. **Nettoyage & préparation → Data Lake /** CURATED
    o Séparation claire entre ce qui est “techniquement propre” et ce qui est brut.
3. **Modélisation & exposition → Data Warehouse**
    o Structure pensée pour l’analyse (rapports, KPI, visualisations).
4. Traçabilité minimale :
    o Fichier de log (logging) qui note :
        date/heure du run,
        fichiers sources lus,
        nombre de lignes RAW lues,
        nombre de lignes CURATED générées,
        nombre de lignes chargées dans le DW,
        erreurs éventuelles.
5. Organisation projet :


o data_lake/raw/
o data_lake/curated/
o logs/etl.log
o config/config.yml (chemins, accès DB, options)


