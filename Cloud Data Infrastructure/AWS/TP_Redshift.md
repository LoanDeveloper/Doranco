# TP – Analyse de ventes avec AWS Redshift

## Objectifs pédagogiques

À l’issue du TP, vous serez capable de :

* utiliser AWS Learner Lab et la console AWS ;
* créer un entrepôt de données avec Amazon Redshift ;
* charger des données depuis Amazon S3 ;
* modéliser des données analytiques (schéma en étoile) ;
* écrire des requêtes SQL analytiques (OLAP).

Durée indicative : 3 à 4 heures

---

## Contexte

Vous travaillez pour une entreprise de distribution qui souhaite analyser ses ventes.
Les données proviennent d’un système transactionnel et sont fournies sous forme de fichiers CSV.
Votre mission consiste à charger ces données dans Redshift et à produire des analyses décisionnelles.

On part d’un fichier transactionnel unique et on le transforme en un schéma en étoile, adapté à l’analytique.

Faites des recherches sur le principe de l'organisation en étoile.
Mettez en perspective les différences entre une base de données OLTP et une base de données OLAP
---

## Description du dataset

Chaque ligne correspond à une transaction de vente.

Champs disponibles :

* transaction_id : identifiant unique de la transaction
* date : date de la transaction
* customer_id : identifiant client
* gender : sexe du client (Male / Female)
* age : âge du client
* product_category : catégorie du produit
* quantity : nombre d’unités achetées
* unit_price : prix unitaire
* total_amount : montant total de la transaction

---

## Partie 1 – Démarrage de l’environnement AWS (30 min)

1. Démarrer le **AWS Learner Lab**.
2. Accéder à la **AWS Management Console**.
3. Respectez les conditions suivantes pour utiliser dans un Learner Lab (conditions depuis le README du Lab):
    * This service can assume the LabRole IAM role.
    * Supported instance type: ra3.large
    * Supported cluster size: maximum two instances

Questions conceptuelles:

* Quelle différence entre Redshift Serverless data warehouses et Redshift provisioned data warehouses ?

---

## Partie 2 – Création de l’entrepôt Redshift

Créer un **Redshift Serverless**.

Paramètres attendus :

* Nom explicite (ex. `retail-redshift`)
* Identifiants administrateur
* Accès via **Query Editor v2** (à revérifier)

Vérifier que l’état est *Available*.

---

## Partie 3 – Stockage des données dans S3

1. Créer un bucket S3 (ex. `retail-sales-<id>`).
2. Importer le fichier CSV du dataset.
3. Vérifier que le fichier est bien accessible.

Livrables :

* Nom du bucket
* Chemin complet du fichier CSV

---

## Partie 4 – Modélisation analytique (45 min)

Vous devez transformer les données transactionnelles en **schéma en étoile**.

### Tables à créer

**Dimension client**

* customer_id (PK)
* gender
* age

**Dimension produit**

* product_category (PK)

**Dimension date**

* date_id (PK)
* year
* month
* day

**Table de faits ventes** (table centrale)

* transaction_id
* date_id
* customer_id
* product_category
* quantity
* unit_price
* total_amount

Contraintes :

* utiliser des types compatibles Redshift ;
* définir une clé de tri (SORTKEY) sur la date (https://docs.aws.amazon.com/fr_fr/redshift/latest/dg/t_Sorting_data.html)

Livrable :

* script SQL de création des tables.

---

## Partie 5 – Chargement des données (45 min)

1. Charger les données CSV dans une table de staging.
2. Alimenter les dimensions (clients, produits, dates).
3. Alimenter la table de faits.

Vous devez utiliser la commande `COPY` depuis S3.

Livrables :

* scripts COPY
* nombre de lignes dans chaque table

Questions conceptuelles :

* Pourquoi COPY est-il plus efficace que INSERT ?
* Pourquoi séparer staging et tables finales ?

---

## Partie 6 – Requêtes analytiques (45 min)

Écrire et exécuter les requêtes suivantes :

1. Chiffre d’affaires total par catégorie de produit.
2. Chiffre d’affaires mensuel.
3. Panier moyen par sexe.
4. Top 5 des clients en montant total dépensé.
5. Répartition des ventes par tranche d’âge (ex. <25, 25–40, >40).

Livrables :

* requêtes SQL
* résultats obtenus
* interprétation courte (2–3 lignes par requête)