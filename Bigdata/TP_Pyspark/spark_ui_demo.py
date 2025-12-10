#!/usr/bin/env python3
"""
Script pour visualiser la charge de travail PySpark via Spark UI.
Spark UI sera accessible sur http://localhost:4040 pendant l'exécution.
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count, max, min, desc, asc
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType
import time

print("=" * 60)
print("🚀 Démarrage de Spark avec Spark UI...")
print("=" * 60)

# Créer SparkSession avec configuration pour Spark UI
spark = SparkSession.builder \
    .appName("TP_PySpark_Spotify_UI_Demo") \
    .config("spark.ui.enabled", "true") \
    .config("spark.ui.port", "4040") \
    .getOrCreate()

spark_ui_url = spark.sparkContext.uiWebUrl
print(f"\n✅ SparkSession créée avec succès!")
print(f"📊 Spark UI disponible sur: {spark_ui_url}")
print("\n⏳ Ouvrez cette URL dans votre navigateur pour visualiser les Jobs, Stages, et Exécuteurs.")
print("=" * 60)

# Définir le schéma
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

print("\n📁 Chargement du dataset spotify-data.csv...")
df_spotify = spark.read.csv("spotify-data.csv", header=True, schema=schema)
df_spotify.cache()  # Cache pour de meilleures performances

print(f"📈 Nombre total de lignes: {df_spotify.count()}")

# Exécuter les opérations du TP pour générer du travail
print("\n" + "=" * 60)
print("🔄 Exécution des requêtes du TP...")
print("=" * 60)

# Q1: Chansons publiées après 2015 avec popularité > 85
print("\n📋 Q1: Filtrage des chansons populaires récentes...")
popular_recent = df_spotify.filter((col("year") > 2015) & (col("popularity") > 85))
count_q1 = popular_recent.count()
print(f"   ➡️ {count_q1} chansons trouvées")

# Q2: Non explicites et non instrumentales
print("\n📋 Q2: Filtrage non explicites et non instrumentales...")
non_explicit = df_spotify.filter((col("explicit") == 0) & (col("instrumentalness") == 0))
count_q2 = non_explicit.count()
print(f"   ➡️ {count_q2} chansons trouvées")

# Q3: Très dansables OU très positives
print("\n📋 Q3: Filtrage dansables ou positives...")
danceable = df_spotify.filter((col("danceability") > 0.8) | (col("valence") > 0.8))
count_q3 = danceable.count()
print(f"   ➡️ {count_q3} chansons trouvées")

# Q4: Durée moyenne par année
print("\n📋 Q4: Agrégation durée moyenne par année...")
avg_duration = df_spotify.groupBy("year").agg(avg("duration_ms").alias("avg_duration_ms")).orderBy("year")
avg_duration.collect()
print("   ➡️ Agrégation complétée")

# Q5: Artiste le plus prolifique
print("\n📋 Q5: Comptage par artiste...")
artist_count = df_spotify.groupBy("artists").agg(count("*").alias("nombre_titres")).orderBy(desc("nombre_titres"))
top_artist = artist_count.first()
print(f"   ➡️ Top artiste: {top_artist['artists']} avec {top_artist['nombre_titres']} titres")

# Q6: Caractéristiques par mode
print("\n📋 Q6: Caractéristiques moyennes par mode...")
by_mode = df_spotify.groupBy("mode").agg(
    avg("energy").alias("avg_energy"),
    avg("acousticness").alias("avg_acousticness")
).orderBy("mode")
by_mode.collect()
print("   ➡️ Agrégation complétée")

# Q7: Loudness par année
print("\n📋 Q7: Loudness par année...")
loudness_by_year = df_spotify.groupBy("year").agg(avg("loudness").alias("avg_loudness")).orderBy("avg_loudness")
loudness_by_year.collect()
print("   ➡️ Agrégation complétée")

# Q8: Jointure avec décennie
print("\n📋 Q8: Création et jointure avec les décennies...")
decades_data = [(y, f"{y//10 * 10}s") for y in range(1920, 2021)]
decades_df = spark.createDataFrame(decades_data, ["year", "decade_name"])
songs_with_decades = df_spotify.join(decades_df, "year", "left")
songs_with_decades.select("name", "year", "decade_name").show(5, truncate=False)

# Q9: Top 10 par décennie
print("\n📋 Q9: Top 10 chansons par décennie...")
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number
window_spec = Window.partitionBy("decade_name").orderBy(desc("popularity"))
top_by_decade = songs_with_decades.withColumn("rank", row_number().over(window_spec)).filter(col("rank") <= 10)
top_by_decade.select("decade_name", "name", "popularity", "rank").orderBy("decade_name", "rank").show(20, truncate=False)

# Q10: Statistiques par décennie
print("\n📋 Q10: Statistiques complètes par décennie...")
decade_stats = songs_with_decades.groupBy("decade_name").agg(
    count("*").alias("total_songs"),
    avg("popularity").alias("avg_popularity"),
    avg("danceability").alias("avg_danceability"),
    avg("energy").alias("avg_energy")
).orderBy("decade_name")
decade_stats.show()

print("\n" + "=" * 60)
print("✅ Toutes les opérations sont terminées!")
print(f"📊 Consultez Spark UI sur: {spark_ui_url}")
print("=" * 60)
print("\n💡 L'interface montrera:")
print("   - Jobs: Les 10 opérations du TP")
print("   - Stages: Le détail de chaque étape (map, reduce, shuffle)")
print("   - Storage: Le DataFrame en cache")
print("   - Executors: Les ressources utilisées")
print("\n🔴 Appuyez sur Ctrl+C pour arrêter Spark et fermer l'UI...")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n\n⏹️ Arrêt de Spark...")
    spark.stop()
    print("👋 SparkSession terminée.")
