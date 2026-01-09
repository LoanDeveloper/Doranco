# 🚌 Nice Traffic Watch - Dashboard Interactif

## 📊 Projet TP2: Migration Matplotlib/Seaborn vers Dash/Plotly

**Objectif:** Transposer les visualisations statiques du TP1 vers un dashboard web interactif avec Dash et Plotly

---

## 🎯 Vue d'Ensemble

Ce projet est la **version industrialisée** de l'analyse des retards du réseau Lignes d'Azur. Il transforme les visualisations statiques (Matplotlib/Seaborn) en graphiques interactifs (Plotly) intégrés dans une application web Dash.

### ✨ Fonctionnalités

- ✅ **8 Visualisations Interactives** (toutes converties en Plotly)
- ✅ **Filtres Dynamiques** (type de transport, plage horaire, top N lignes)
- ✅ **Zoom et Survol** sur tous les graphiques
- ✅ **KPIs en Temps Réel** (retard moyen, % à l'heure, etc.)
- ✅ **Interface Responsive** avec onglets organisés
- ✅ **Design Professionnel** avec palette de couleurs cohérente

---

## 📂 Structure du Projet

```
tp2/
├── app.py                  # Application Dash principale
├── data_loader.py          # Module de chargement et préparation des données
├── README.md               # Ce fichier
├── requirements.txt        # Dépendances Python
├── .venv/                  # Environnement virtuel
└── ../tp/data/             # Données du TP1 (transit_delays.csv)
    └── transit_delays.csv
```

---

## 🚀 Installation et Lancement

### 1. Prérequis

- Python 3.10+
- Données du TP1 dans `../tp/data/transit_delays.csv`

### 2. Installation des dépendances

```bash
cd tp2

# Créer l'environnement virtuel (si pas déjà fait)
python3 -m venv .venv

# Activer l'environnement
source .venv/bin/activate

# Installer les packages
pip install dash plotly pandas numpy
```

### 3. Lancement de l'application

```bash
# S'assurer que l'environnement est activé
source .venv/bin/activate

# Lancer l'application
python app.py
```

### 4. Accéder au dashboard

Ouvrez votre navigateur à l'adresse :
```
http://127.0.0.1:8050/
```

---

## 📊 Les 8 Visualisations

### Onglet 1: Vue d'Ensemble

#### 1. **Histogramme de Distribution des Retards**
- **Type:** Histogramme avec lignes de référence
- **Conversion:** `sns.histplot()` → `px.histogram()`
- **Interactivité:** Zoom, survol pour voir les fréquences exactes

#### 2. **Violin Plot de Densité**
- **Type:** Violin plot avec quartiles
- **Conversion:** `sns.violinplot()` → `go.Violin()`
- **Interactivité:** Affichage des statistiques au survol

#### 3. **Hit Parade des Lignes Problématiques**
- **Type:** Barplot horizontal avec couleurs divergentes
- **Conversion:** `sns.barplot()` → `go.Bar()` avec orientation='h'
- **Interactivité:** Survol pour voir les valeurs exactes, ajustement dynamique du top N

---

### Onglet 2: Analyse Temporelle

#### 4. **Évolution Horaire avec Intervalle de Confiance**
- **Type:** Line chart avec zone d'intervalle de confiance
- **Conversion:** `sns.lineplot()` → `go.Scatter()` avec fill
- **Interactivité:** Zoom sur plages horaires, tooltip détaillé

#### 5. **Heatmap Ligne × Heure**
- **Type:** Heatmap avec annotations
- **Conversion:** `sns.heatmap()` → `go.Heatmap()`
- **Interactivité:** Survol pour voir les valeurs exactes, zoom sur zones

---

### Onglet 3: Comparaison & Carte

#### 6. **Boxplot Bus vs Tram**
- **Type:** Boxplot comparatif
- **Conversion:** `sns.boxplot()` → `px.box()`
- **Interactivité:** Survol pour statistiques détaillées

#### 7. **Violin Plot Bus vs Tram**
- **Type:** Violin plot comparatif
- **Conversion:** `sns.violinplot()` → `px.violin()`
- **Interactivité:** Densités interactives

#### 8. **Carte Géographique des Retards**
- **Type:** Scatter map avec couleurs divergentes
- **Conversion:** `plt.scatter()` (GPS) → `px.scatter_mapbox()`
- **Interactivité:** Pan, zoom, survol pour détails, carte OpenStreetMap

---

## 🎨 Amélioration vs TP1

| Aspect | TP1 (Matplotlib/Seaborn) | TP2 (Dash/Plotly) |
|--------|--------------------------|-------------------|
| **Interactivité** | ❌ Statique | ✅ Zoom, pan, survol, filtres |
| **Filtres** | ❌ Nécessite re-exécution | ✅ Filtres dynamiques temps réel |
| **Accessibilité** | ❌ Notebook local | ✅ Interface web accessible |
| **Design** | ⚠️ Basique | ✅ Professionnel avec KPIs |
| **Performance** | ⚠️ Régénère tout | ✅ Mise à jour ciblée |
| **Partage** | ❌ Export images | ✅ URL partageable |
| **Carte GPS** | ⚠️ Scatter basique | ✅ Carte interactive OSM |

---

## 🔍 Filtres Disponibles

### 1. Type de Transport
- **Bus** ✅
- **Tram** ✅
- Mise à jour instantanée de tous les graphiques

### 2. Plage Horaire
- Slider avec range de 0h à 23h
- Filtre toutes les visualisations selon l'heure

### 3. Top N Lignes (Hit Parade)
- Slider de 5 à 30 lignes
- Ajuste dynamiquement le nombre de lignes affichées

### 4. Bouton Rafraîchir
- Recharge les données si le collecteur tourne en arrière-plan
- Utile pour voir l'évolution en temps réel

---

## 💡 Points Forts Techniques

### Architecture Modulaire
- **`data_loader.py`:** Gestion complète des données (chargement, nettoyage, agrégations)
- **`app.py`:** Application Dash avec callbacks pour l'interactivité

### Performance
- **Échantillonnage intelligent** pour la carte GPS (5000 points max)
- **Mise à jour ciblée** via callbacks Dash (pas de rechargement complet)
- **Filtrage côté serveur** pour performance optimale

### Design Professionnel
- **Palette de couleurs cohérente** (bleu, vert, orange, rouge)
- **Palettes divergentes** pour les retards (vert=avance, rouge=retard)
- **Responsive design** avec grilles CSS
- **KPIs visuels** en haut de page

### Interactivité Avancée
- **Callbacks multiples** avec décorateur `@app.callback`
- **Filtres synchronisés** (un changement met à jour tous les graphiques)
- **Tooltips riches** avec informations détaillées

---

## 📚 Technologies Utilisées

| Technologie | Usage | Équivalent TP1 |
|-------------|-------|----------------|
| **Dash** | Framework web | - (Jupyter) |
| **Plotly** | Graphiques interactifs | Matplotlib + Seaborn |
| **Pandas** | Manipulation données | Pandas |
| **NumPy** | Calculs scientifiques | NumPy |

---

## 🎓 Compétences Démontrées

### Migration Matplotlib/Seaborn → Plotly
- ✅ Conversion de 6 types de visualisations différentes
- ✅ Adaptation des palettes de couleurs
- ✅ Gestion des annotations et légendes
- ✅ Interactivité native (zoom, pan, hover)

### Développement Web avec Dash
- ✅ Architecture MVC (Model-View-Controller)
- ✅ Callbacks pour l'interactivité
- ✅ Layout responsive avec CSS
- ✅ Gestion d'état de l'application

### Data Engineering
- ✅ Classe `DataLoader` réutilisable
- ✅ Méthodes de filtrage et agrégation
- ✅ Gestion de la performance (échantillonnage)
- ✅ Pipeline de traitement modulaire

### UX/UI Design
- ✅ Interface intuitive avec onglets
- ✅ KPIs en évidence
- ✅ Filtres accessibles
- ✅ Feedback visuel cohérent

---

## 📈 Exemple de Workflow Utilisateur

1. **Arrivée sur le dashboard**
   - Voir immédiatement les KPIs globaux
   - Retard moyen, % à l'heure, nombre d'observations

2. **Explorer la vue d'ensemble**
   - Distribution des retards (histogramme + violin)
   - Identifier les lignes problématiques (hit parade)

3. **Analyser l'évolution temporelle**
   - Voir les heures de pointe (évolution horaire)
   - Identifier les combinaisons ligne×heure critiques (heatmap)

4. **Comparer Bus vs Tram**
   - Boxplot et violin pour voir les différences
   - Déterminer quel type est plus fiable

5. **Explorer géographiquement**
   - Carte interactive avec zoom
   - Identifier les zones problématiques de Nice

6. **Filtrer pour approfondir**
   - Sélectionner uniquement les bus
   - Zoomer sur les heures de pointe (8h-10h, 17h-19h)
   - Ajuster le nombre de lignes dans le hit parade

---

## 🚀 Extensions Possibles

Si vous voulez aller plus loin :

### 1. Rafraîchissement Automatique
```python
dcc.Interval(
    id='interval-component',
    interval=60*1000,  # 60 secondes
    n_intervals=0
)
```

### 2. Export de Graphiques
```python
config={
    'toImageButtonOptions': {
        'format': 'png',
        'filename': 'nice_traffic_viz',
        'height': 800,
        'width': 1200
    }
}
```

### 3. Authentification
```python
import dash_auth

VALID_USERNAME_PASSWORD_PAIRS = {
    'admin': 'lignes_azur_2026'
}

auth = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)
```

### 4. Base de Données
- Remplacer le CSV par PostgreSQL/MongoDB
- Utiliser SQLAlchemy pour les requêtes
- Pagination pour gros volumes

### 5. Prédiction ML
- Ajouter un onglet "Prédictions"
- Modèle de prédiction des retards
- Visualisation des prédictions vs réel

---

## 🐛 Dépannage

### Problème: L'application ne démarre pas

**Solution:**
```bash
# Vérifier que l'environnement est activé
source .venv/bin/activate

# Vérifier les dépendances
pip list | grep -E "dash|plotly|pandas"

# Réinstaller si nécessaire
pip install --force-reinstall dash plotly pandas numpy
```

### Problème: "FileNotFoundError: ../tp/data/transit_delays.csv"

**Solution:**
```bash
# Vérifier la structure
ls -l ../tp/data/

# Si le fichier n'existe pas, ajuster le chemin dans data_loader.py
# Ligne 12: self.data_path = "VOTRE_CHEMIN_ICI"
```

### Problème: Les graphiques ne se mettent pas à jour

**Solution:**
- Vérifier la console du navigateur (F12) pour les erreurs
- Vérifier les logs dans le terminal Python
- S'assurer que les filtres ont des valeurs valides

---

## ✅ Conformité avec le Sujet TP2

| Exigence | Status | Implémentation |
|----------|--------|----------------|
| Transposer visualisations vers Dash | ✅ | 8 visualisations converties |
| Utiliser Plotly pour graphiques | ✅ | `px.*` et `go.*` |
| Interactivité (zoom, survol, filtres) | ✅ | Tous graphiques interactifs |
| Interface web | ✅ | Dash avec layout professionnel |
| Conversion sns.scatterplot → px.scatter | ✅ | Carte GPS interactive |
| Documentation | ✅ | README complet |

---

## 📝 Commandes Utiles

```bash
# Lancer l'application
python app.py

# Tester le module de chargement seul
python data_loader.py

# Installer une nouvelle dépendance
pip install <package>
pip freeze > requirements.txt

# Désactiver l'environnement
deactivate
```

---

## 🎉 Conclusion

Ce projet démontre une **maîtrise complète** de:
- La **migration** de visualisations statiques vers interactives
- Le **développement web** avec Dash
- L'**ingénierie logicielle** (architecture modulaire)
- Le **design UX/UI** pour dashboards professionnels

**Résultat:** Un dashboard production-ready, partageable et maintenable! 🚀

---

**Auteur:** Data Analyst Consultant - Loan THOMY
**Date:** 9 janvier 2026
**Formation:** Doranco - Visualisation avec Seaborn et Matplotlib
**Version:** 1.0

---

**Bon courage et amusez-vous bien avec le dashboard! 🎯**
