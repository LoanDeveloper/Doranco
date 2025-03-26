# TP-03 Python : Recherche Optimisée avec Binary Search sur des Données Issues d’une API

## 📌 Objectif
Ce TP est une extension du TP-02 et vise à :
- Appliquer l’algorithme **Binary Search** pour une recherche optimisée.
- Comparer ses performances avec la recherche linéaire.

## 🛠 Installation
### 1. Installer les dépendances
Si ce n’est pas encore fait, installez les bibliothèques nécessaires :
```sh
pip install requests pymongo
```

### 2. Installer et démarrer MongoDB
Assurez-vous que MongoDB est installé et en cours d’exécution :
```sh
mongod --dbpath /chemin/vers/le/dossier-de-donnees
```

## 🚀 Utilisation
Exécutez le script :
```sh
python tp_api_search.py
```
Le script :
1. Charge les données stockées en MongoDB.
2. Trie les données selon un critère.
3. Demande un élément à rechercher.
4. Applique **Binary Search** et affiche le résultat.

## 🔍 Algorithmes utilisés
- **Recherche linéaire** (O(n))
- **Binary Search** (O(log n))

## 📊 Résultats
Le script compare le temps d’exécution des deux méthodes et affiche le plus performant.

Bonne exploration ! 🚀

