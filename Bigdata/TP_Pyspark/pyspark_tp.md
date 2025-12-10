

# TP d’introduction à PySpark

## Objectifs du TP

* Installer et configurer PySpark dans un environnement Python.
* Créer une `SparkSession`.
* Comprendre les notions clés :

  * RDD vs DataFrame
  * Partitions et répartition
  * Cache / persist
  * Broadcast variables
  * Paradigme master–worker
  * Tolérance aux pannes

* Manipuler un DataFrame Spark :

  * Filtres (`filter`)
  * Sélections (`select`)
  * Agrégations (`groupBy`)
  * Joins (`join`)

---

# Installation et configuration de PySpark

## 🔧 Créer un environnement virtuel Python

```bash
python -m venv env
source env/bin/activate
```

## 🔧 Installer PySpark

```bash
pip install pyspark
```

Avec cette installation, **les binaires Spark sont automatiquement intégrés dans le package PySpark**, donc aucune installation séparée d’Apache Spark n’est nécessaire.

---

# Votre première session Spark

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("SparkConfigured") \
    .getOrCreate()
```

---

# Concepts essentiels de Spark

## RDD vs DataFrame

| Concept      | RDD                              | DataFrame                       |
| ------------ | -------------------------------- | ------------------------------- |
| API          | Bas niveau                       | Haut niveau                     |
| Typage       | Non structuré                    | Structuré (schéma)              |
| Optimisation | Aucune, transformations directes | Optimisé par le moteur Catalyst |
| Usage        | Flexibilité maximale             | Performance, SQL, analytics     |

Pour 99% des cas : **DataFrame**.
Le dataFrame est une structure de donnée splus moderne et plus efficace dans notre contexte.

---

## Partitions & répartition

* Spark **divise** les données en **partitions**.
* Chaque partition est traitée en parallèle par un worker.
* Répartition = placement optimal des partitions selon les opérations.
* Repartition vs coalesce :

  * `df.repartition(n)` → reshuffle complet (lent)
  * `df.coalesce(n)` → fusion sans reshuffle (rapide)

* Consultez les docstrings de ces fonctions, faites un bref résumé de ce que vous en avez compris.
---

## Paradigme master–worker

* **Driver (master)** :
  programme Python qui soumet des tâches
* **Workers (executors)** :
  machines exécutant les transformations sur les partitions

---

## Tolérance aux pannes

Si un worker meurt :

* Spark récupère la partition depuis sa source
* rejoue les transformations
* redéploie la tâche sur un autre worker
=> Le modèle est **résilient par conception**.

---

# Partie pratique

Nous utiliserons un dataset simple : **Spotify**

## Dataset proposé

Le dataset se compose d'infos sur des chansons
https://www.kaggle.com/datasets/kapturovalexander/spotify-data-from-pyspark-course/data

## Exercices pratiques


### 1. Charger le CSV

```python
df = spark.read.csv("spotify-data.csv", header=True, inferSchema=True)
df.show()
df.printSchema()
```
Expliquez ce que fait ce code :

```python
decades_data = [
    (y, f"{y//10 * 10}s")
    for y in range(1920, 2021)
]
decades_df = spark.createDataFrame(decades_data, ["year", "decade_name"])

decades_df.show(5)
```

### 2. Questions métier

**Q1**	Quelles sont les chansons publiées après 2015 qui ont un score de Popularité supérieur à 85 ?  
**Q2**	Quelles sont les chansons qui ne sont ni explicites (explicit = 0) ni instrumentales (instrumentalness = 0) ?  
**Q3**	Quels titres sont très "dansables" (danceability > 0.8) OU très "positifs" (valence > 0.8) ?  
**Q4**	Calculer la durée moyenne des chansons (duration_ms) pour chaque année de sortie.  

Exemple de code pour la Q1 :  

```python
popular_recent_songs = df_spotify.filter(
    (col("year") > 2016) & (col("popularity") < 15)
)
popular_recent_songs.select("name", "main_artist", "year", "popularity").show(5)
```  

Example de code pour la Q4 :  

```python
from pyspark.sql.functions import avg

avg_duration_by_year = df_spotify.groupBy("year").agg(
    avg("speechiness").alias("avg_speechiness")
).orderBy("year")

avg_speechiness_by_year.show(5)
```

**Q5**	Quel est l'artiste principal (main_artist) qui possède le plus grand nombre de titres dans le dataset ?  
**Q6**	Quelles sont les caractéristiques moyennes (energy, acousticness) des titres en Mode majeur (mode = 1) par rapport au Mode mineur (mode = 0) ?  
**Q7**	Trouver l'année où le score de Loudness (volume) moyen est le plus faible et l'année où il est le plus élevé.  
**Q8**	Associer chaque chanson à sa Décennie de sortie en utilisant le DataFrame de référence decades_df créé en amont.   



Exemple de code pour Q8 :  

```python
# Jointure interne du DataFrame Spotify et du DataFrame Décennies sur la colonne 'year'
df_with_decades = df_spotify.join(
    decades_df,
    on="year",
    how="inner" # Jointure interne : on ne garde que les correspondances
)

df_with_decades.select("name", "main_artist", "year", "decade_name").show(5, truncate=False)
```  


**Q9**	Après avoir trouvé l'artiste principal le plus populaire (selon la popularité moyenne), afficher tous les titres de cet artiste uniquement.  

**Q10**	Calculer l'écart entre la Popularité de chaque chanson et la Popularité moyenne de l'année de sortie de cette chanson.  



---

N'oubliez pas d'arrêter la SparkSession avec :

```python
spark.stop()a()
```