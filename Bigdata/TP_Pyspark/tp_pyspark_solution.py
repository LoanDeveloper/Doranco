"""
TP PySpark - Solution Complète
Analyse du dataset Spotify avec PySpark

Ce script répond aux 10 questions du TP en utilisant les opérations PySpark:
- Filtres (filter)
- Sélections (select)
- Agrégations (groupBy)
- Joins (join)
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count, max, min, desc, asc, abs as spark_abs
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType

# =============================================================================
# 1. Créer une SparkSession
# =============================================================================
print("=" * 80)
print("CRÉATION DE LA SESSION SPARK")
print("=" * 80)

spark = SparkSession.builder \
    .appName("TP_PySpark_Spotify") \
    .getOrCreate()

print("✅ SparkSession créée avec succès!")

# =============================================================================
# 2. Charger le CSV avec un schéma explicite
# =============================================================================
print("\n" + "=" * 80)
print("CHARGEMENT DES DONNÉES")
print("=" * 80)

# Définir le schéma explicitement pour éviter les erreurs de type
schema = StructType([
    StructField("id", StringType(), True),
    StructField("name", StringType(), True),
    StructField("artists", StringType(), True),
    StructField("duration_ms", IntegerType(), True),
    StructField("release_date", StringType(), True),
    StructField("year", IntegerType(), True),
    StructField("acousticness", DoubleType(), True),
    StructField("danceability", DoubleType(), True),
    StructField("energy", DoubleType(), True),
    StructField("instrumentalness", DoubleType(), True),
    StructField("liveness", DoubleType(), True),
    StructField("loudness", DoubleType(), True),
    StructField("speechiness", DoubleType(), True),
    StructField("tempo", DoubleType(), True),
    StructField("valence", DoubleType(), True),
    StructField("mode", IntegerType(), True),
    StructField("key", IntegerType(), True),
    StructField("popularity", IntegerType(), True),
    StructField("explicit", IntegerType(), True)
])

df_spotify = spark.read.csv("spotify-data.csv", header=True, schema=schema)

print("\n📊 Aperçu des données:")
df_spotify.show(5)

print("\n📋 Schéma du DataFrame:")
df_spotify.printSchema()

print(f"\n📈 Nombre total de lignes: {df_spotify.count()}")

# =============================================================================
# Création du DataFrame des décennies (exemple fourni dans le TP)
# =============================================================================
print("\n" + "=" * 80)
print("CRÉATION DU DATAFRAME DES DÉCENNIES")
print("=" * 80)

# Explication: Ce code génère une liste de tuples où chaque tuple contient
# une année (y) et le nom de sa décennie (ex: 1985 -> "1980s").
# La formule y//10 * 10 arrondit à la décennie inférieure.
decades_data = [
    (y, f"{y//10 * 10}s")
    for y in range(1920, 2021)
]
decades_df = spark.createDataFrame(decades_data, ["year", "decade_name"])

print("📅 Aperçu du DataFrame des décennies:")
decades_df.show(5)

# =============================================================================
# Explication repartition vs coalesce
# =============================================================================
print("\n" + "=" * 80)
print("EXPLICATION: repartition vs coalesce")
print("=" * 80)
print("""
📌 repartition(n):
   - Effectue un "full shuffle" des données
   - Peut augmenter OU diminuer le nombre de partitions
   - Plus lent car redistribue toutes les données sur le cluster
   - Utilisé quand on veut une distribution équilibrée des données

📌 coalesce(n):
   - Fusionne les partitions existantes SANS shuffle
   - Ne peut QUE diminuer le nombre de partitions
   - Beaucoup plus rapide car pas de transfert réseau
   - Utilisé pour réduire le nombre de fichiers en sortie
""")

# =============================================================================
# QUESTIONS MÉTIER
# =============================================================================

# -----------------------------------------------------------------------------
# Q1: Quelles sont les chansons publiées après 2015 qui ont un score de 
#     Popularité supérieur à 85 ?
# -----------------------------------------------------------------------------
print("\n" + "=" * 80)
print("Q1: Chansons après 2015 avec popularité > 85")
print("=" * 80)

popular_recent_songs = df_spotify.filter(
    (col("year") > 2015) & (col("popularity") > 85)
)
popular_recent_songs.select("name", "artists", "year", "popularity").show(10, truncate=False)
print(f"📊 Nombre de chansons trouvées: {popular_recent_songs.count()}")

# -----------------------------------------------------------------------------
# Q2: Quelles sont les chansons qui ne sont ni explicites (explicit = 0) 
#     ni instrumentales (instrumentalness = 0) ?
# -----------------------------------------------------------------------------
print("\n" + "=" * 80)
print("Q2: Chansons non explicites ET non instrumentales")
print("=" * 80)

non_explicit_non_instrumental = df_spotify.filter(
    (col("explicit") == 0) & (col("instrumentalness") == 0)
)
non_explicit_non_instrumental.select("name", "artists", "explicit", "instrumentalness").show(10, truncate=False)
print(f"📊 Nombre de chansons trouvées: {non_explicit_non_instrumental.count()}")

# -----------------------------------------------------------------------------
# Q3: Quels titres sont très "dansables" (danceability > 0.8) 
#     OU très "positifs" (valence > 0.8) ?
# -----------------------------------------------------------------------------
print("\n" + "=" * 80)
print("Q3: Chansons très dansables OU très positives")
print("=" * 80)

danceable_or_positive = df_spotify.filter(
    (col("danceability") > 0.8) | (col("valence") > 0.8)
)
danceable_or_positive.select("name", "artists", "danceability", "valence").show(10, truncate=False)
print(f"📊 Nombre de chansons trouvées: {danceable_or_positive.count()}")

# -----------------------------------------------------------------------------
# Q4: Calculer la durée moyenne des chansons (duration_ms) pour chaque année.
# -----------------------------------------------------------------------------
print("\n" + "=" * 80)
print("Q4: Durée moyenne des chansons par année de sortie")
print("=" * 80)

avg_duration_by_year = df_spotify.groupBy("year").agg(
    avg("duration_ms").alias("avg_duration_ms")
).orderBy("year")

# Convertir en minutes pour plus de lisibilité
avg_duration_by_year = avg_duration_by_year.withColumn(
    "avg_duration_minutes",
    col("avg_duration_ms") / 60000
)
avg_duration_by_year.show(20)

# -----------------------------------------------------------------------------
# Q5: Quel est l'artiste principal (main_artist ou artists) qui possède 
#     le plus grand nombre de titres dans le dataset ?
# Note: Le dataset a une colonne 'artists', pas 'main_artist'
# -----------------------------------------------------------------------------
print("\n" + "=" * 80)
print("Q5: Artiste avec le plus grand nombre de titres")
print("=" * 80)

# Compter le nombre de titres par artiste
artist_count = df_spotify.groupBy("artists").agg(
    count("*").alias("nombre_titres")
).orderBy(desc("nombre_titres"))

print("🎤 Top 10 des artistes les plus prolifiques:")
artist_count.show(10, truncate=False)

top_artist = artist_count.first()
print(f"\n🏆 L'artiste avec le plus de titres: {top_artist['artists']} avec {top_artist['nombre_titres']} titres")

# -----------------------------------------------------------------------------
# Q6: Quelles sont les caractéristiques moyennes (energy, acousticness) 
#     des titres en Mode majeur (mode = 1) vs Mode mineur (mode = 0) ?
# -----------------------------------------------------------------------------
print("\n" + "=" * 80)
print("Q6: Caractéristiques moyennes par Mode (majeur/mineur)")
print("=" * 80)

characteristics_by_mode = df_spotify.groupBy("mode").agg(
    avg("energy").alias("avg_energy"),
    avg("acousticness").alias("avg_acousticness")
).orderBy("mode")

print("🎵 Mode 0 = Mineur, Mode 1 = Majeur")
characteristics_by_mode.show()

# -----------------------------------------------------------------------------
# Q7: Trouver l'année où le score de Loudness moyen est le plus faible 
#     et l'année où il est le plus élevé.
# -----------------------------------------------------------------------------
print("\n" + "=" * 80)
print("Q7: Année avec le Loudness le plus faible et le plus élevé")
print("=" * 80)

loudness_by_year = df_spotify.groupBy("year").agg(
    avg("loudness").alias("avg_loudness")
).orderBy("avg_loudness")

print("🔊 Distribution du loudness moyen par année (ordre croissant):")
loudness_by_year.show(10)

# Année avec le loudness le plus faible
quietest_year = loudness_by_year.first()
print(f"\n📉 Année avec le loudness le plus FAIBLE: {quietest_year['year']} (avg: {quietest_year['avg_loudness']:.2f} dB)")

# Année avec le loudness le plus élevé
loudest_year = loudness_by_year.orderBy(desc("avg_loudness")).first()
print(f"📈 Année avec le loudness le plus ÉLEVÉ: {loudest_year['year']} (avg: {loudest_year['avg_loudness']:.2f} dB)")

# -----------------------------------------------------------------------------
# Q8: Associer chaque chanson à sa Décennie de sortie en utilisant le 
#     DataFrame de référence decades_df créé en amont.
# -----------------------------------------------------------------------------
print("\n" + "=" * 80)
print("Q8: Association des chansons avec leur décennie (JOIN)")
print("=" * 80)

df_with_decades = df_spotify.join(
    decades_df,
    on="year",
    how="inner"
)

df_with_decades.select("name", "artists", "year", "decade_name").show(10, truncate=False)

# Distribution par décennie
print("\n📊 Distribution des chansons par décennie:")
df_with_decades.groupBy("decade_name").count().orderBy("decade_name").show()

# -----------------------------------------------------------------------------
# Q9: Après avoir trouvé l'artiste principal le plus populaire 
#     (selon la popularité moyenne), afficher tous les titres de cet artiste.
# -----------------------------------------------------------------------------
print("\n" + "=" * 80)
print("Q9: Artiste le plus populaire (popularité moyenne) et ses titres")
print("=" * 80)

# Trouver l'artiste avec la popularité moyenne la plus élevée
# (en ne gardant que ceux avec au moins 5 titres pour éviter les biais)
avg_popularity_by_artist = df_spotify.groupBy("artists").agg(
    avg("popularity").alias("avg_popularity"),
    count("*").alias("nombre_titres")
).filter(col("nombre_titres") >= 5).orderBy(desc("avg_popularity"))

print("🎤 Top 10 des artistes les plus populaires (min 5 titres):")
avg_popularity_by_artist.show(10, truncate=False)

most_popular_artist = avg_popularity_by_artist.first()
print(f"\n🏆 L'artiste le plus populaire: {most_popular_artist['artists']}")
print(f"   Popularité moyenne: {most_popular_artist['avg_popularity']:.2f}")
print(f"   Nombre de titres: {most_popular_artist['nombre_titres']}")

# Afficher tous les titres de cet artiste
print(f"\n🎵 Tous les titres de {most_popular_artist['artists']}:")
df_spotify.filter(col("artists") == most_popular_artist['artists']) \
    .select("name", "year", "popularity") \
    .orderBy(desc("popularity")) \
    .show(20, truncate=False)

# -----------------------------------------------------------------------------
# Q10: Calculer l'écart entre la Popularité de chaque chanson et la 
#      Popularité moyenne de l'année de sortie de cette chanson.
# -----------------------------------------------------------------------------
print("\n" + "=" * 80)
print("Q10: Écart de popularité par rapport à la moyenne de l'année")
print("=" * 80)

# Calculer la popularité moyenne par année
avg_pop_by_year = df_spotify.groupBy("year").agg(
    avg("popularity").alias("avg_popularity_year")
)

# Joindre avec le DataFrame original
df_with_avg_pop = df_spotify.join(avg_pop_by_year, on="year", how="inner")

# Calculer l'écart
df_with_deviation = df_with_avg_pop.withColumn(
    "popularity_deviation",
    col("popularity") - col("avg_popularity_year")
)

print("📊 Chansons avec leur écart de popularité par rapport à la moyenne annuelle:")
df_with_deviation.select(
    "name", "artists", "year", "popularity", 
    "avg_popularity_year", "popularity_deviation"
).orderBy(desc("popularity_deviation")).show(10, truncate=False)

# Top des chansons les plus "surperformantes" par rapport à leur année
print("\n🚀 Top 10 des chansons qui surperforment le plus par rapport à leur année:")
df_with_deviation.select(
    "name", "artists", "year", "popularity", "popularity_deviation"
).orderBy(desc("popularity_deviation")).show(10, truncate=False)

# Top des chansons les plus "sous-performantes" par rapport à leur année
print("\n📉 Top 10 des chansons qui sous-performent le plus par rapport à leur année:")
df_with_deviation.select(
    "name", "artists", "year", "popularity", "popularity_deviation"
).orderBy(asc("popularity_deviation")).show(10, truncate=False)

spark.stop()
print("\n🛑 SparkSession arrêtée.")
