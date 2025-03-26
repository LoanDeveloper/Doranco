# TP Python : Récupération, Stockage et Tri Optimisé de Données Issues d’une API

## 📌 Objectif
Ce projet vise à :
- Récupérer des données depuis une API (CoinGecko)
- Stocker ces données dans une base NoSQL (MongoDB)
- Trier ces données avec plusieurs algorithmes et comparer leurs performances

## 🛠 Installation
### 1. Installer les dépendances
Assurez-vous d’avoir Python installé, puis exécutez :
```sh
pip install requests pymongo
```

### 2. Installer et démarrer MongoDB
Si MongoDB n'est pas encore installé, suivez [cette documentation](https://www.mongodb.com/docs/manual/installation/).
Démarrez ensuite le serveur MongoDB :
```sh
mongod --dbpath /chemin/vers/le/dossier-de-donnees
```

## 🚀 Utilisation
Lancez simplement le script :
```sh
python tp_api_sort.py
```
Le script va :
1. Récupérer des données de l’API CoinGecko
2. Les stocker dans MongoDB
3. Appliquer et mesurer les performances de plusieurs tris
4. Afficher le tri le plus efficace

## 🏆 Résultats
Le script affichera les temps d’exécution des différents tris et sélectionnera le plus rapide, puis affichera les données triées.

## 📚 Algorithmes de tri utilisés
- Bubble Sort (O(n²))
- Selection Sort (O(n²))
- Insertion Sort (O(n²))
- Quick Sort (O(n log n))

## 🎯 Remarque
Le critère de tri utilisé est `current_price` (prix actuel des cryptos).

Amusez-vous bien ! 🚀

