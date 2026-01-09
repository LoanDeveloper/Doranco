# 🚀 Quick Start - Nice Traffic Watch Dashboard

## Lancement Rapide en 3 Étapes

### 1️⃣ Activer l'environnement virtuel

```bash
cd /mnt/data/Documents/Doranco/Visualisation\ Seaborn\ et\ Matplotlib/tp2
source .venv/bin/activate
```

### 2️⃣ Lancer l'application

```bash
python app.py
```

### 3️⃣ Accéder au dashboard

Ouvrez votre navigateur à :
```
http://127.0.0.1:8050/
```

---

## 🎯 Ce que vous allez voir

### En haut de page: KPIs Globaux
- 📊 **Retard Moyen**: Performance globale du réseau
- ⏱️ **% à l'heure**: Ponctualité (±1 minute)
- 📈 **Observations**: Volume de données analysées
- 🚌 **Lignes**: Nombre de lignes dans l'analyse
- ⚠️ **% en retard**: Proportion de retards significatifs

### Section Filtres Interactifs
- **Type de Transport**: Bus, Tram ou les deux
- **Plage Horaire**: Slider pour sélectionner les heures
- **Top N Lignes**: Ajuster le nombre de lignes dans le hit parade
- **Bouton Rafraîchir**: Recharger les données

### Onglet 1: Vue d'Ensemble 📊
1. **Distribution des retards** (Histogramme)
   - Cliquez-glissez pour zoomer
   - Survolez pour voir les fréquences

2. **Densité de probabilité** (Violin plot)
   - Voir la distribution complète
   - Quartiles affichés

3. **Hit Parade des lignes problématiques**
   - Top 15 lignes (ajustable)
   - Couleurs: Vert=ponctuel, Rouge=retard

### Onglet 2: Analyse Temporelle ⏰
1. **Évolution horaire du retard moyen**
   - Ligne bleue avec intervalle de confiance
   - Identifiez les heures de pointe

2. **Heatmap Ligne × Heure**
   - 20 lignes × 24 heures
   - Points chauds en rouge
   - Zones d'avance en vert

### Onglet 3: Comparaison & Carte 🗺️
1. **Boxplot Bus vs Tram**
   - Comparaison statistique

2. **Violin plot Bus vs Tram**
   - Densités de distribution

3. **Carte interactive de Nice**
   - Zoom, pan, rotation
   - Points colorés par retard
   - Carte OpenStreetMap

---

## 💡 Tips d'Utilisation

### Zoom sur un graphique
- **Cliquez-glissez** sur la zone à zoomer
- **Double-clic** pour revenir au zoom initial
- **Bouton "Autoscale"** pour réinitialiser

### Filtrer les données
1. Décochez "Tram" pour voir uniquement les Bus
2. Ajustez le slider horaire sur 8h-10h (heure de pointe matin)
3. Observez comment tous les graphiques se mettent à jour

### Explorer la carte
1. Allez dans l'onglet "Comparaison & Carte"
2. Zoomez sur le centre-ville de Nice
3. Survolez les points pour voir les détails
4. Les points rouges = retards, verts = avance

### Comparer Bus vs Tram
1. Onglet 3
2. Observez les boxplots et violins
3. Identifiez quel type de transport est plus fiable

---

## 🐛 En cas de problème

### L'application ne démarre pas
```bash
# Vérifier l'environnement
which python
# Devrait afficher: .../tp2/.venv/bin/python

# Réinstaller les dépendances
pip install --force-reinstall -r requirements.txt
```

### Erreur "FileNotFoundError"
```bash
# Vérifier que les données existent
ls -l ../tp/data/transit_delays.csv

# Si le fichier n'existe pas, lancez d'abord le collecteur du TP1
cd ../tp
python data_collector_v2.py
```

### Le dashboard est lent
- C'est normal avec 1M+ observations
- L'échantillonnage est déjà activé pour la carte GPS
- Utilisez les filtres pour réduire le volume

### Les graphiques ne se mettent pas à jour
- Vérifiez la console du navigateur (F12)
- Vérifiez les logs dans le terminal Python
- Essayez de rafraîchir la page (Ctrl+R)

---

## 📚 Pour aller plus loin

- Consultez le **README.md** pour la documentation complète
- Explorez le code dans **app.py** pour comprendre les callbacks
- Modifiez **data_loader.py** pour ajouter de nouvelles agrégations
- Ajoutez vos propres visualisations!

---

## ⏹️ Arrêter l'application

Dans le terminal où tourne l'app:
```
Ctrl + C
```

Puis désactiver l'environnement:
```bash
deactivate
```

---

**Bon amusement avec le dashboard! 🎉**
