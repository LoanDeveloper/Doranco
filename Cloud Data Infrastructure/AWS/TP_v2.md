# TP – Construction d’un pipeline ETL cloud avec AWS (2 jours)

## Contexte

Vous travaillez pour une collectivité locale souhaitant analyser l’offre de transport public à partir de données **GTFS** (General Transit Feed Specification). Ces données sont publiées gratuitement par de nombreux réseaux de transport et décrivent les arrêts, lignes, trajets et horaires. Nous réaliserons un premier POC avec les données du réseau de transports Lignes d'Azur de l'agglomération de Nice.

https://transport.data.gouv.fr/datasets/donnees-statiques-et-dynamiques-du-reseau-de-transport-lignes-dazur

Votre mission consiste à concevoir et implémenter un **pipeline ETL cloud** complet, depuis l’ingestion de données brutes jusqu’à leur exploitation dans une base de données relationnelle.

Vous devrez utiliser un planificateur pour récupérer les données avec une récupération des données toutes les heures par exemple.

La partie pratique s’effectue **exclusivement via un Learner Lab AWS Academy**.

Pour ce TP qui est assez conséquent et assez dense, je vous laisse quelques libertés dans votre approche, notamment lors des dernières étapes silver.

---

## Objectifs pédagogiques

* Comprendre une architecture data lake / base relationnelle
* Mettre en œuvre un ETL simple avec S3 et Glue (PySpark)
* Concevoir un modèle logique de données relationnel
* Charger des données propres dans PostgreSQL (RDS)
* (Bonus) Exposer les données via une API REST + Ralison une visualisatgio avec streamlit

---

## Contraintes techniques

* Environnement : AWS Academy Learner Lab
* Services autorisés : S3, Glue, RDS (PostgreSQL)
* Données : GTFS statiques (CSV)
* Pas de streaming, pas de services temps réel

---

# Jour 1 – Ingestion et transformations (Bronze → Silver)

## 1. Récupération des données GTFS (Extraction)

1. Identifier la source GTFS.
2. Télécharger l’archive GTFS (`.zip`).
3. Décompresser localement les fichiers CSV principaux :

   * `stops.txt`
   * `routes.txt`
   * `trips.txt`
   * `stop_times.txt`

### Stockage Bronze (S3)

* Créer un bucket S3 dédié au TP.
* Créer la structure suivante :

  * `bronze/gtfs/`
* Charger les fichiers GTFS **sans modification** dans ce préfixe (rajouter un horodatage dans le nom du fichier).

Livrable : bucket S3 structuré avec données brutes.

---

## 2. Catalogage des données (Glue Crawler)

1. Créer une base de métadonnées Glue (ex. `gtfs_bronze_db`).
2. Créer un crawler Glue pointant vers `s3://<bucket>/bronze/gtfs/`.
3. Lancer le crawler.
4. Vérifier les tables détectées et leurs schémas.

---

## 3. Transformations avec AWS Glue (PySpark)

Vous devez créer un **job Glue PySpark** réalisant les transformations suivantes (de manière planifiée également).

### 3.1 Nettoyage

* Supprimer les colonnes inutiles dans chaque table.
* S'assurer qu'il n'y a pas de doublons dans les différents fichiers
* Convertir les types numériques (`lat`, `lon`, identifiants).
* Supprimer les lignes avec valeurs manquantes.

### 3.2 Enrichissement

* Ajouter une colonne `area_type` aux arrêts :

  * `center` si l’arrêt est à moins de 2 km (distance d'haversine) de l'hyper centre (43.6957999,7.2710084)
  * `periphery` sinon.
* Extraire l’heure depuis `arrival_time` (`HH:MM:SS`) et créer une colonne `hour`.


### 3.3 Agrégation

Créer plusieurs tables agrégées à partir des données jointes.

Transformations demandées :

* nombre de passages par arrêt et par ligne
* nombre total de passages par arrêt (toutes lignes confondues)
* nombre de passages par ligne

Exemples de tables produites :

```
(stop_id, route_id, nb_passages)
(stop_id, nb_passages_total)
(route_id, nb_passages_total)
```

---

### 3.4 Transformation temporelle avancée

À partir de `arrival_time` :

* créer une colonne `time_bucket` avec les valeurs :

  * `morning` (05:00–09:59)
  * `day` (10:00–15:59)
  * `evening` (16:00–19:59)
  * `night` (20:00–04:59)

* calculer le nombre de passages par arrêt et par tranche horaire

---


### Stockage Silver (S3)

* Écrire les résultats transformés au format **Parquet** dans :

  * `silver/gtfs/`

Livrable : données propres et enrichies dans S3 (silver).

---

# Jour 2 – Chargement et exploitation (Silver → PostgreSQL)

## 4. Modélisation des données

À partir des données transformées, proposer un **modèle logique relationnel** comprenant au minimum :

* une table des arrêts
* une table des lignes
* une table de faits de fréquentation

Justifier :

* les clés primaires
* les clés étrangères
* les index utiles

Livrable : schéma logique (diagramme ou description textuelle).

---

## 5. Création de la base PostgreSQL (RDS)

1. Créer une instance PostgreSQL sur RDS (petite instance).
2. Autoriser l’accès public (pour le TP).
3. Se connecter via pgAdmin (ou autre).
4. Créer les tables correspondant au modèle logique.

---

## 6. Chargement des données dans RDS

Deux options possibles :

* depuis Glue (écriture JDBC),
* depuis S3 puis import SQL.

Les tables doivent être correctement remplies et cohérentes.

---

## 7. Exploitation SQL

Écrire des requêtes permettant de :

* identifier les arrêts les plus fréquentés,
* identifier les lignes les plus actives,
* comparer centre-ville / périphérie,
* analyser les heures de pointe.

Livrable : script SQL commenté.

---

# Bonus 1 – Exposition via API REST

Deux approches possibles :

### Option A – API locale (recommandée)

* Développer une API REST avec FastAPI ou Flask en local et en Python.
* Connexion directe à la base RDS PostgreSQL.
* Exemples d’endpoints :

  * `/stops`
  * `/routes`
  * `/stats/top-stops`
  * `/stats/by-time-bucket`

### Option B – Approche serverless (si possible via le Learner Lab)

* Décrire une architecture RDS → Lambda → API Gateway.
* Expliquer les contraintes dans AWS Academy.

Livrable : code API ou schéma d’architecture commenté.

---

# Bonus 2 – Visualisation des données avec Streamlit

Objectif : proposer une **interface de visualisation interactive** connectée à la base PostgreSQL RDS.

## Principe

* Application **Streamlit** exécutée en local sur votre poste.
* Connexion directe à la base PostgreSQL RDS.
* Lecture des tables agrégées.

## Visualisations attendues

* Top 10 des arrêts les plus fréquentés (bar chart)
* Activité par ligne (bar chart ou table)
* Répartition des passages par tranche horaire (pie ou bar chart)
* Comparaison centre / périphérie

## Contraintes

* Pas d’hébergement cloud requis
* Authentification simple (variables d’environnement)

## Livrable

* Code Streamlit fonctionnel
* Captures d’écran des visualisations
* Court README expliquant le lancement de l’application

---

## Livrables attendus

* Bucket S3 structuré (bronze / silver)
* Crawler et job Glue fonctionnels
* Modèle logique de données
* Base PostgreSQL remplie
* Requêtes SQL
* (Bonus) API REST + visualisation streamlit

---

## Critères d’évaluation

* Compréhension de l’architecture
* Qualité des transformations
* Cohérence du modèle relationnel
* Exploitabilité des données
* Clarté des livrables