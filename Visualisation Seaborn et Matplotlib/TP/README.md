# 🚍 Nice Traffic Watch - Dashboard de Monitoring des Retards

> **TP Doranco - Visualisation avec Seaborn et Matplotlib**
> Analyse en temps réel des retards du réseau Lignes d'Azur (Métropole de Nice)

---

## 📋 Vue d'Ensemble du Projet

Ce projet implémente un **système complet de monitoring des retards** pour le réseau de transport public de Nice. Il combine:

1. 🔄 **Collecte de données en temps réel** via GTFS-RT
2. 💾 **Stockage structuré** en CSV pour analyse
3. 📊 **Visualisations professionnelles** avec Matplotlib et Seaborn
4. 💡 **Insights automatiques** et recommandations

---

## 🏗️ Architecture du Système

```
nice_traffic_watch/
├── data_collector_v2.py      # Collecteur intelligent avec calcul de retards
├── nice_traffic_analysis.ipynb # Notebook d'analyse complet
├── requirements.txt           # Dépendances Python
├── data/
│   ├── gtfs/                 # GTFS statique (horaires programmés)
│   ├── transit_delays.csv    # Données collectées avec retards calculés
│   ├── collector_v2.log      # Logs du collecteur
│   └── gtfs.zip              # Archive GTFS
└── README.md                 # Ce fichier
```

---

## 🚀 Démarrage Rapide

### 1. Activer l'environnement virtuel

```bash
source ./.venv/bin/activate
```

### 2. Lancer le collecteur de données

Le collecteur est **déjà en cours d'exécution en arrière-plan** 🎉

Pour vérifier son état:

```bash
tail -f data/collector_v2.log
```

Vous devriez voir des lignes comme:
```
10:06:49 | INFO | ✅ Calculated 3380 delay observations
10:06:49 | INFO | 💾 Saved 3380 observations
10:06:49 | INFO | 💤 Next collection in 59.6s (Total: 3)
```

### 3. Analyser les données avec Jupyter

```bash
jupyter notebook nice_traffic_analysis.ipynb
```

Ou avec JupyterLab:

```bash
jupyter lab nice_traffic_analysis.ipynb
```

---

## 📊 Le Notebook d'Analyse

Le notebook `nice_traffic_analysis.ipynb` est structuré en **5 parties narratives**:

### **Partie 0: Introduction et Chargement**
- 📚 Contexte et objectifs
- 🔧 Import et configuration
- 📥 Chargement et exploration initiale
- 🧹 Nettoyage des données

### **Partie 1: Vue d'Ensemble du Réseau**
- 📊 **Histogramme + KDE**: Distribution statistique des retards
- 🏆 **Barplot horizontal**: Top 15 des lignes les plus problématiques

### **Partie 2: Analyse Temporelle**
- ⏰ **Time Series**: Évolution du retard moyen au cours de la journée
- 🔥 **Heatmap**: Points chauds (Ligne × Heure)

### **Partie 3: Analyse Catégorielle**
- 🚌 **Boxplot/Violin**: Comparaison Bus vs Tram

### **Partie 4: Analyse Géographique**
- 🗺️ **Scatter Plot GPS**: Carte abstraite des retards à Nice

### **Partie 5: Conclusions**
- 📝 Rapport exécutif automatique
- 💡 Recommandations data-driven

---

## 🎯 Visualisations Créées

Toutes les visualisations demandées dans le sujet du TP sont implémentées:

| Visualisation | Type | Objectif | Status |
|--------------|------|----------|--------|
| Distribution des retards | `histplot` + `kdeplot` | Santé globale du réseau | ✅ |
| Hit Parade des lignes | `barplot` horizontal | Identifier les lignes problématiques | ✅ |
| Évolution temporelle | `lineplot` avec IC | Détecter les heures de pointe | ✅ |
| Heatmap horaire | `heatmap` | Points chauds Ligne×Heure | ✅ |
| Comparaison Bus/Tram | `boxplot` + `violinplot` | Fiabilité par mode | ✅ |
| Carte géographique | `scatterplot` GPS | Localisation des retards | ✅ |

---

## 🔧 Comment Fonctionne le Collecteur V2

### Architecture Intelligente

Le `data_collector_v2.py` est bien plus qu'un simple scraper:

```python
1. Chargement du GTFS Statique (horaires programmés)
   └─> 114 routes, 19,819 trips, schedules pour tous les arrêts

2. Collecte GTFS-RT toutes les 60 secondes
   ├─> Trip Updates (horaires réels)
   └─> Vehicle Positions (GPS des véhicules)

3. Calcul Intelligent des Retards
   └─> delay = actual_arrival_time - scheduled_arrival_time

4. Enrichissement des Données
   ├─> Type de transport (Bus=3, Tram=0)
   ├─> Position GPS
   └─> Contexte temporel

5. Stockage en CSV Structuré
   └─> ~3,300 observations par minute
```

### Robustesse

- ✅ **Gestion d'erreurs** avec exponential backoff
- ✅ **Logging détaillé** de toutes les opérations
- ✅ **Validation des données** (coordonnées GPS, retards cohérents)
- ✅ **Pas de crash** en cas d'indisponibilité temporaire de l'API

### Performance

```
Collecte toutes les 60 secondes
↓
~3,300 observations/minute
↓
~200,000 observations/heure
↓
~1.6M observations/jour (8h)
```

---

## 📈 Exemple de Résultats

Avec seulement **quelques minutes de collecte**, vous obtenez:

```
📊 Delay Data Summary
====================================
Total observations: 13,138
Unique vehicles: 184
Unique routes: 53

Delay Statistics:
  Mean delay: -1.11 minutes (en avance!)
  Median delay: -0.47 minutes
  Std deviation: 3.44 minutes
  Range: -9.9 min (early) → +38 min (late)
```

---

## 🎨 Palettes de Couleurs Utilisées

Le notebook utilise des palettes **divergentes** pour une lecture intuitive:

- 🟢 **Vert**: En avance / Performance excellente
- 🟡 **Jaune**: À l'heure / Performance acceptable
- 🔴 **Rouge**: En retard / Performance problématique

Exemples:
- `RdYlGn_r` (Red-Yellow-Green reversed) pour les heatmaps
- `husl` pour les graphiques multicatégories
- Couleurs personnalisées pour Bus (coral) vs Tram (lightblue)

---

## 📝 Points Clés du TP

### Contraintes Respectées ✅

- [x] Collecte de données **éphémères** GTFS-RT
- [x] Script de scraping avec **horodatage** et stockage local
- [x] Calcul des **retards réels** (non simulés)
- [x] **Notebook narratif** avec contexte
- [x] **6 types de visualisations** différentes (histplot, barplot, lineplot, heatmap, boxplot/violin, scatterplot)
- [x] Utilisation de **Matplotlib ET Seaborn**
- [x] Gestion des **valeurs négatives** (avance)
- [x] Code **propre et commenté**

### Innovations 💡

- 🚀 **Calcul intelligent des retards** via fusion GTFS statique + RT
- 📊 **Génération automatique d'insights** dans le notebook
- 🎯 **Rapport exécutif** avec recommandations data-driven
- 🗺️ **Visualisation géographique** avec coordonnées réelles
- 🔄 **Collecteur robuste** avec gestion d'erreurs professionnelle

---

## 🛠️ Dépannage

### Le collecteur ne collecte plus

```bash
# Vérifier s'il tourne
ps aux | grep data_collector_v2.py

# Relancer si nécessaire
source ./.venv/bin/activate
nohup python3 data_collector_v2.py > data/collector_bg.log 2>&1 &
```

### Le notebook ne trouve pas les données

Vérifiez que le fichier CSV existe:

```bash
ls -lh data/transit_delays.csv
```

Si absent, le collecteur doit tourner au moins 1 minute.

### Erreur "ModuleNotFoundError"

```bash
source ./.venv/bin/activate
pip install -r requirements.txt
```

---

## 📚 Sources et Documentation

### APIs Utilisées

- **GTFS-RT Trip Updates**: `https://ara-api.enroute.mobi/rla/gtfs/trip-updates`
- **GTFS-RT Vehicle Positions**: `https://ara-api.enroute.mobi/rla/gtfs/vehicle-positions`
- **GTFS Statique**: `https://chouette.enroute.mobi/api/v1/datas/OpendataRLA/gtfs.zip`

### Documentation

- [GTFS Realtime Reference](https://gtfs.org/documentation/realtime/reference/)
- [Seaborn Documentation](https://seaborn.pydata.org/)
- [Matplotlib Gallery](https://matplotlib.org/stable/gallery/index.html)
- [Transport Data Gouv - Lignes d'Azur](https://transport.data.gouv.fr/datasets/donnees-statiques-et-dynamiques-du-reseau-de-transport-lignes-dazur)

---

## 🎓 Compétences Démontrées

### Data Engineering
- ✅ Collecte de données temps réel (API GTFS-RT)
- ✅ Parsing de Protocol Buffers (protobuf)
- ✅ Fusion de données multi-sources
- ✅ ETL Pipeline (Extract-Transform-Load)

### Data Analysis
- ✅ Nettoyage et validation de données
- ✅ Statistiques descriptives
- ✅ Analyse temporelle (time series)
- ✅ Analyse géospatiale (GPS)

### Data Visualization
- ✅ Choix de visualisations adaptées aux questions
- ✅ Palettes de couleurs professionnelles
- ✅ Annotations et storytelling
- ✅ Création de dashboards narratifs

### Python & Libraries
- ✅ Pandas (manipulation de données)
- ✅ NumPy (calculs numériques)
- ✅ Matplotlib (graphiques de base)
- ✅ Seaborn (graphiques statistiques)
- ✅ Logging (traçabilité)
- ✅ Error Handling (robustesse)

---

## 🚀 Pour Aller Plus Loin

### Améliorations Possibles

1. **Dashboard Temps Réel**
   - Streamlit ou Dash pour interface web
   - Rafraîchissement automatique toutes les minutes

2. **Prédiction des Retards**
   - Machine Learning (Random Forest, LSTM)
   - Prédire les retards en fonction de l'heure, météo, etc.

3. **Alertes Automatiques**
   - Envoyer un email/SMS si retard > 10 min
   - Notification Slack pour les opérateurs

4. **Analyse Avancée**
   - Corrélation retards ↔ météo
   - Impact des événements (matchs, concerts)
   - Patterns saisonniers

---

## 👨‍💻 Auteur

**Data Analyst Consultant** - TP Doranco Visualisation 2026

---

## 📄 Licence

Projet éducatif - Doranco Formation

---

**Bon courage pour la présentation ! 🎉**
