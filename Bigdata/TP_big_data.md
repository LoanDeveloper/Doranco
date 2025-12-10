
## TP Big Data : Travail introductif (3h30)

Ce TP est conçu pour que vous **découvriez et construisiez** les concepts en Big Data par la recherche et l'application.

---

### Phase 1 : Découverte Guidée (1h30)

Travail en **groupe de 2**. Chaque groupe doit produire une synthèse (présentation de 15 minutes environ) pour la restitution.

#### 1. Le Concept de **3V** du Big Data

* **Objectif :** Définir et illustrer les 3V.
* **Tâche :**
    1.  Faire une recherche pour identifier les **trois caractéristiques principales** souvent associées au Big Data (les **3V**).
    2.  Définir chaque terme avec des **mots simples** mais avec le plus de détails possible.
    3.  Pour chaque V, trouver un **exemple concret d’application** dans une entreprise (ex : Volume $\rightarrow$ les logs d'un site e-commerce ; Vélocité $\rightarrow$ les transactions boursières ; Variété $\rightarrow$ les données de capteurs IoT + les commentaires clients).
    4.  Rechercher si d'autres V (4V, 5V...) existent et les définir brièvement.
    5.  Faites une présentation brève de l'algorithme MapReduce (fonctionnement, intérêts)

#### 2. Architecture et Besoins Techniques

* **Objectif :** Comprendre les différentes approches de traitement.
* **Tâche :**
    1.  Rechercher et définir les concepts suivants : **Traitement Batch** et **Traitement Temps Réel (ou Stream)**.
    2.  Quelles sont les **principales différences** en termes de latence, de cas d'usage et de complexité de mise en œuvre ?
    3.  Rechercher la différence entre une architecture **On-Premise (locale)** et une architecture **Cloud** pour le Big Data (avantages/inconvénients).
    4.  Identifier un outil/technologie **emblématique** pour le Batch (ex : Hadoop, Spark) et un outil/technologie pour le Stream (ex : Kafka, Flink). Faites une présentation de chacun d'uex, trouver les avantages et inconvénients de chacun d'eux.

---

### Phase 2 : Étude de Cas Clients (environ 1h30)

Je vous propose d'appliquer les recherches que vous avez effectué pour proposer une première solution technique sur des scénarios concrets (mais ces cas sont fictifs, il s'agit vulgairement de cas d'école).

#### Analyse des Besoins et Orientation Technique (1h30)

* **Objectif :** Transférer les concepts théoriques à des situations pratiques.
* **Tâche :** Chaque groupe reçoit les **4 cas clients** présentés ci-dessous. Pour chaque cas, ils doivent :
    1.  **Identifier** clairement les **3V** (Volume, Vélocité, Variété) dominants pour le cas d'étude.
    2.  **Identifier** le besoin client principal (analyse rétrospective, alerte immédiate, modélisation prédictive, etc.).
    3.  **Proposer** une **orientation technique** initiale (Batch *ou* Stream, Cloud *ou* Local) en **justifiant** le choix en fonction des 3V et du besoin.
    4.  **Initier** une étude pour comparer les coûts des offres de providers (Azure, AWS, Google Cloud Platform) en utilisant les outils d'estimation de coûts proposés par ces fournisseurs.
    5.  **Elaborez** un plan de pour estimer les jours nécessaires pour atteindre l'objectif client, proposez une organisation.

---

### Phase 3 : Restitution et Débat (15 min maxi par groupe)

* **Objectif :** Partager et débattre des choix techniques.
* **Activité :** Chaque groupe choisit **un des cas clients** pour une présentation rapide (5 minutes max pour le traitement du cas client avec présentation de la solution) de son analyse des 3V et de son orientation technique. Le but est d'ouvrir ensuite une courte discussion sur les divergences les choix entre les groupes.

---

## 4 Cas Clients pour l'Analyse

Voici les 4 cas clients proposés :

### Cas Client 1 :  Le Réseau de Compteurs Intelligents

| Catégorie | Description du Projet |
| :--- | :--- |
| **Client** | Une compagnie nationale de distribution d'électricité. |
| **Données** | 10 millions de compteurs envoient une mesure de consommation **toutes les 10 minutes** (tension, consommation actuelle, état). S'ajoutent des logs d'erreurs sporadiques (texte) et des données météo (tabulaires). |
| **Objectif Client** | **Optimiser la production d'énergie** en ajustant en temps réel la charge du réseau et **détecter immédiatement** les pannes et les fraudes pour envoyer une équipe d'intervention. |
| **Contraintes** | La détection de panne doit être **quasi instantanée** (moins de 1 minute). Les données historiques (plus d'un mois) sont utilisées pour la facturation et les modèles de prédiction à long terme. |

### Cas Client 2 : L'Analyse Rétrospective E-Commerce

| Catégorie | Description du Projet |
| :--- | :--- |
| **Client** | Une grande plateforme de vente en ligne (e-commerce). |
| **Données** | 500 To de données : Historique des commandes (structuré), logs de navigation des utilisateurs (semi-structuré), images et vidéos des produits (non-structuré), commentaires clients (texte). |
| **Objectif Client** | Améliorer le **taux de conversion**. Il faut analyser les parcours clients qui n'ont pas abouti à un achat, identifier les produits les plus souvent consultés sans être achetés, et segmenter la clientèle pour des campagnes marketing ciblées. |
| **Contraintes** | Le client est prêt à attendre **jusqu'à 12 heures** pour obtenir les rapports d'analyse agrégés journaliers, mais le stockage doit être **économique** car le volume grossit rapidement. |

### Cas Client 3 :  La Détection de Fraude Bancaire

| Catégorie | Description du Projet |
| :--- | :--- |
| **Client** | Une banque internationale traitant des transactions par carte de crédit. |
| **Données** | Des milliards de transactions par jour. Chaque transaction contient le montant, la localisation, l'heure, et l'identifiant du terminal. La donnée est très structurée. |
| **Objectif Client** | **Bloquer immédiatement** toute transaction suspecte qui ne correspond pas au profil habituel du client, avant que celle-ci ne soit validée. |
| **Contraintes** | L'analyse et la décision de bloquer ou non une transaction doivent être prises en **quelques millisecondes** pour ne pas impacter l'expérience utilisateur au terminal de paiement. La sécurité des données est la priorité absolue. |

### Cas Client 4 :  Le Moteur de Recommandation Vidéo

| Catégorie | Description du Projet |
| :--- | :--- |
| **Client** | Une plateforme de streaming vidéo. |
| **Données** | Métadonnées des films/séries (structuré), données de visionnage (quel utilisateur a regardé quoi, quand, et pendant combien de temps), *feedback* des utilisateurs (notes, commentaires). |
| **Objectif Client** | **Suggérer instantanément** (au chargement de la page d'accueil) de nouveaux contenus pertinents pour l'utilisateur, et faire des analyses hebdomadaires sur les tendances générales de visionnage. |
| **Contraintes** | Le moteur de recommandation doit être **extrêmement réactif** pour offrir une suggestion pertinente basée sur l'historique immédiat. L'infrastructure doit pouvoir gérer l'augmentation rapide du nombre d'abonnés et de contenus. |

Je vous encourage à la **collaboration** et la **recherche autonome**, soyez créatif (au sens "ingénieurie" du terme), proposez pourquoi pas des composantes intégrant du machine learning.