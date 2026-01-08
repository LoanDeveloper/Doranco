### 1. Reformulation du Sujet : "Mission Control - Lignes d'Azur"

L'idée est de vous placer dans la peau de **Data Analysts** consultants.

#### Titre du Projet : 🚍 **Nice Traffic Watch : Création d'un Dashboard de Monitoring des Retards**

##### Contexte 
La métropole de Nice et le Réseau urbain Lignes d'Azur souhaitent réaliser un premier produit (MVP) qui permet d'avoir en temps réel les retards, il s'agit alors de livrer un outil qui puisse permettre aux équipes dédiées de prendre des décisions.

    Données :
    https://www.data.gouv.fr/datasets/donnees-statiques-et-dynamiques-du-reseau-de-transport-lignes-dazur/
    https://transport.data.gouv.fr/datasets/donnees-statiques-et-dynamiques-du-reseau-de-transport-lignes-dazur/

##### Votre Mission :
Vous avez une journée (9h00 - 17h00) pour développer un **MVP (Minimum Viable Product)** d'aide à la décision. Votre objectif est de livrer un **Notebook Jupyter narratif** capable de transformer des flux de données complexes en graphiques clairs.
##### La Contrainte "Live" :
Le flux de données est éphémère. Dès le début du TP, vous devrez mettre en place un script de collecte ("scraper") qui interroge l'API toutes les X minutes (ex: 1 min), horodate chaque requête, et stocke l'historique dans un fichier local (CSV ou Pickle). C'est cet historique accumulé au fil de la journée qui nourrira vos graphiques finaux.

**GTFS**
Il s'agit d'un standard ouvert de données pour décrire les réseaux de transport public.
Il permet aux agences de transport (RATP, SNCF) de publier leurs données de manière uniforme, et aux applications (Google Maps etc..) de les exploiter facilement.
Et donc à vous aussi de les exploiter facilement…
Ce standard tend à être adopté par la plupart des compagnies de transports publics du monde entier.
Exemple pour le métro de Los Angeles:
https://www.transit.land/feeds/f-metro~losangeles~rail~rt

**GTFS-RT**
Pour ouvrir un flux temps réel : gtfs-realtime-bindings   
```bash
pip install requests gtfs-realtime-bindings
```

Exemple en Python :  
```py
import requests
from google.transit import gtfs_realtime_pb2

url = "https://exemple.com/gtfs-rt"
response = requests.get(url, timeout=10)

feed = gtfs_realtime_pb2.FeedMessage()
feed.ParseFromString(response.content)

for entity in feed.entity:
    if entity.HasField("vehicle"):
        print(entity.vehicle.vehicle.id, entity.vehicle.position)
    if entity.HasField("trip_update"):
        print(entity.trip_update.trip.trip_id)
    if entity.HasField("alert"):
        print(entity.alert.header_text.translation[0].text)
```


> **Livrable attendu :**
> Un notebook propre, commenté, présentant l'analyse de la journée écoulée via des visualisations Matplotlib et Seaborn pertinentes.

---

### 2. Idées de Visualisations (Matplotlib & Seaborn)

Pour ce type de données, il faut varier les angles : distribution globale, évolution temporelle et disparités géographiques/catégorielles.

#### A. Les Indispensables (Vue d'ensemble)

* **L'Histogramme des retards (Seaborn `histplot` ou `kdeplot`) :**
    * *Question :* Quelle est la "santé" globale du réseau ?
    * *Visuel :* Axe X = Minutes de retard, Axe Y = Fréquence.
    * *Intérêt :* Voir si la distribution est normale ou s'il y a une "longue traîne" (quelques bus avec des retards massifs).


* **Le "Hit Parade" des Lignes (Seaborn `barplot` horizontal) :**
    * *Question :* Quelles sont les 10 lignes les plus problématiques aujourd'hui ?
    * *Visuel :* Axe Y = Numéro de ligne, Axe X = Retard moyen (ou médian).
    * *Astuce :* Utiliser une palette de couleurs divergente (vert pour à l'heure, rouge pour retard).



#### B. L'Analyse Temporelle (Evolution 9h-17h)

* **L'évolution du retard moyen (Matplotlib `plot` ou Seaborn `lineplot`) :**
    * *Question :* Y a-t-il eu un pic d'incidents à l'heure du déjeuner ou à la sortie des écoles ?
    * *Visuel :* Axe X = Heure de la journée (Time series), Axe Y = Retard moyen sur tout le réseau.
    * *Ajout :* Ajouter une zone ombrée (intervalle de confiance) avec Seaborn pour montrer l'écart type des retards à chaque instant.


* **La Heatmap Horaire (Seaborn `heatmap`) :**
    * *Question :* À quelle heure et sur quelle ligne les retards s'accumulent-ils ?
    * *Visuel :* Axe X = Créneaux horaires (par quart d'heure), Axe Y = Les 20 lignes principales. La couleur indique l'intensité du retard.
    * *Intérêt :* Permet d'identifier d'un coup d'œil les "points chauds".



#### C. L'Analyse Catégorielle (Comparaisons)

* **Boxplots par type de transport (Seaborn `boxplot` ou `violinplot`) :**
    * *Question :* Le Tramway est-il plus fiable que le Bus ?
    * *Visuel :* Comparaison des distributions de retards entre les différents modes (Bus vs Tram).
    * *Intérêt :* Montrer la dispersion (le bus est souvent plus aléatoire que le tram).


* **Scatter Plot Géographique (Seaborn `scatterplot`) :**
    * *Question :* Où sont les bus en retard ?
    * *Visuel :* Utiliser la latitude et la longitude (présentes dans le GTFS) comme axes X et Y.
    * *Astuce :* Utiliser la couleur (`hue`) pour l'intensité du retard et la taille du point (`size`) pour le nombre de passagers (si dispo) ou le numéro de la ligne. Cela recrée une "carte" abstraite de Nice.


(Attention aux valeurs négatives qui signifient "en avance")