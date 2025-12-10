## TP : Introduction à d'Hadoop

* livrable : Notebook présentant le code et les commandes à utilisant, n'hésitez pas à utiliser 

-----

### 1\. Notions théoriques de base


  * **Le Problème du Big Data** : Qu'est-ce qui rend les données "Big" (Volume, Vitesse, Variété, Véracité) et pourquoi les systèmes traditionnels ne suffisent plus.
  * **Philosophie et objectif d'Hadoop** :
      * Le principe de la **distribution** et de la **tolérance aux pannes**.
  * **Les Composants fondamentaux d'Hadoop** :
      * **HDFS (Hadoop Distributed File System)** : Son rôle, les concepts de **NameNode** (gestionnaire de métadonnées) et de **DataNode** (stockage réel des blocs de données).
      * **YARN (Yet Another Resource Negotiator)** : Son rôle en tant que gestionnaire de ressources et d'ordonnanceur des tâches.
      * Revoyez la définition de **MapReduce (M/R)** : Le modèle de programmation pour le traitement distribué (phases de **Map** et de **Reduce**).

-----

### 2\. Cas d'étude concret et léger : analyse de logs de serveur Web

Ce cas d'étude pour introduire Hadoop s'évertue à analyser des logs de trafic web.

#### Objectif métiers : déterminer les 10 adresse IP les plus courantes + bonus

#### Étapes du TP proposé :

1.  **Exploration locale**

      * Utiliser des commandes Linux standards (`head`, `tail`, `grep`, `wc -l`, `awk`) pour **inspecter** et **manipuler** le fichier localement.
      * *Exemple :* Combien de lignes ? Quelle est la première ligne ? Comment extraire toutes les adresses IP avec `awk` ou `cut` ?.
      * Faites une présentation rapide de l'ensemble de ces commandes.

2.  **Configuration et démarrage du pseudo-cluster**

      * Installation ou utilisation d'une machine virtuelle / conteneur Docker pré-configuré avec **Hadoop en mode Standalone ou Pseudo-Distribué**. C'est la solution la plus simple.
      * Vérification des services (`jps`, `hdfs dfsadmin -report`).

3.  **Manipulation de fichiers avec HDFS**

      * Créer un répertoire dans HDFS (`hdfs dfs -mkdir`).
      * Charger le fichier de logs dans HDFS : `hdfs dfs -put` exemple: `dfs -put simulated_access.log /user/etudiant1/logs/`.
      * Vérifier le contenu du fichier dans HDFS (`hdfs dfs -ls`, `hdfs dfs -cat` sur un petit bout, pour éviter d'inonder la console !).
      * **Concept de bloc :** Utiliser la commande `hdfs fsck /chemin/du/fichier -files -blocks -locations` pour **visualiser où sont stockés les blocs** et combien de réplicas existent (normalement  un seul en mode pseudo-distribué).

4.  **Application MapReduce (conceptuel)**

      * **Etape 1** : Utiliser la logique des commandes Linux développées en étape 1 pour **décrire** comment les phases de **Map** et **Reduce** traiteraient le fichier :
          * **Map** : Lire chaque ligne et émettre l'**adresse IP** comme clé, et la valeur **1** (pour compter chaque occurrence).
          * **Shuffle & Sort** : Le système regroupe toutes les 1 du même IP.
          * **Reduce** : Somme de toutes les 1 pour chaque IP unique.

      * **Etape 2 (Pratique)** : Exécuter un script Python/Jar adapté pour **compter les adresses IP**.

      * **Etape 3** : Etendez votre script et répondez aux autres questions métier suivantes :

        * Déterminer le contenu populaire. Identifier les pages, images ou API qui génèrent le plus de charge sur le serveur.

        * Évaluer la santé du service. Quel pourcentage de requêtes a abouti à un succès (code 200, 201, etc.) ?

        * Identifier les problèmes de navigation ou de configuration. Savoir quelles ressources sont introuvables (404) ou interdites (403).

        * Comprendre le type d'interaction. Mesurer le rapport entre la simple consultation (GET) et l'envoi de données/formulaire (POST).

        * Optimisation des ressources. Déterminer l'heure de la journée ou le jour de la semaine où le trafic est maximum (le pic de charge).

        * Sécurité. Identifier les IP qui font un nombre anormalement élevé de requêtes en peu de temps, signalant potentiellement un DDoS ou une tentative de force brute.


5.  **Conclusion et bilan**

      * Récupérer le résultat (`hdfs dfs -get`).
      * Trier le résultat localement (`sort -nrk 2`) pour trouver le Top 10.
      * Donnez les résultats pour les autres questions métier
      * Faites un point sur ces commandes en les définissant :

        hdfs dfs -mkdir /<path>
        hdfs dfs -ls /<path>
        hdfs dfs -put <local_path> /<hdfs_path>
        hdfs dfs -get /<hdfs_path> <local_path>
        hdfs dfs -cat /<path>/<file>
        hdfs dfs -tail /<path>/<file>
        hdfs dfs -stat /<path>
        hdfs dfs -du -h /<path>
        hdfs dfsadmin -report
