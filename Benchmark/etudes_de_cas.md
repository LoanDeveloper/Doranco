

### Étude de Cas 1 : "SecuLegal" – L'IA dans un environnement confidentiel

**Contexte :** Un cabinet d’avocats d’affaires souhaite utiliser l’IA pour résumer des contrats et faire de la recherche de jurisprudence.
**Contrainte majeure :** La confidentialité des données (RGPD, secret professionnel) est non négociable.

* **Module 1 (S'initier) :**
* **Objectif :** Identifier les solutions capables de traiter du texte long (grande fenêtre de contexte) et sécurisées.
* **Typologie :** LLM orientés texte et analyse juridique.
* **Comparaison :** OpenAI (ChatGPT Enterprise), Mistral (Self-hosted/Le Chat), Claude 3 (Anthropic). 


* **Module 2 (Réaliser la veille) :**
* **Critères techniques :** *Data Policy* (les données servent-elles à l'entraînement ?), localisation des serveurs, fenêtre de contexte (ex: 128k vs 200k tokens).
* **Livrable :** Une fiche synthétique comparant le coût d'une solution SaaS vs une solution Open Source hébergée en interne (On-premise). Faites une recherche approndie sur le cas d'usage et sur les coûts.


* **Module 3 (Présenter) :**
* **Le Pitch :** Présenter la solution retenue (ex: Mistral Large via API sécurisée) aux associés du cabinet qui ne comprennent rien à la tech.
* **Adaptation :** Si un associé demande "Pourquoi pas juste la version gratuite de ChatGPT ?", vous devez expliquer le risque de fuite de données sans jargon complexe.


* **Module 4 (Convaincre) :**
* **Freins à lever :** Risque d'hallucination (inventer une loi) et éthique.
* **Simulation :** Un associé "Attaquant" affirme que l'IA va remplacer les juristes juniors. Vous devez contre-argumenter sur l'augmentation de la productivité et non le remplacement, appuyez voussur des cas concrets d'augmentation de la productivité (au delà du domaine de ce cas d'étude) via des articles de blogs.



---

### Étude de Cas 2 : "GlobalShop" – Assistant Service Client Multilingue

**Contexte :** Un site e-commerce français veut s'étendre en Asie et aux US. Ils ne peuvent pas embaucher 50 personnes pour le support client 24/7. Ils veulent un chatbot IA capable de gérer les réclamations et de se connecter à leur base de stock.
**Contrainte majeure :** Intégrabilité (API) et latence (vitesse de réponse).

* **Module 1 (S'initier) :**
* **Objectif :** Repérer les modèles performants en traduction et en conversationnel.
* **Typologie :** Agents conversationnels, RAG (Retrieval Augmented Generation).


* **Module 2 (Réaliser la veille) :**
* **Critères techniques :** Qualité de l'API, coût par million de tokens, capacité à suivre des instructions complexes (JSON mode).
* **Comparaison :** GPT-4o mini (rapide/pas cher) vs Gemini 1.5 Flash vs Claude Haiku., voir des services Azure.
* **Livrable :** Tableau comparatif des coûts à l'échelle (pour 10 000 conversations/jour par exemple).


* **Module 3 (Présenter) :**
* **Le Pitch :** Vendre la solution au Directeur Financier (CFO) et au CTO.
* **Adaptation :** Le CTO annonce soudainement que le budget API a été réduit de 20%. Vous devez pivoter en temps réel vers une solution moins coûteuse ou hybride.


* **Module 4 (Convaincre) :**
* **Freins à lever :** La peur que le chatbot insulte un client (Brand Safety).
* **Simulation :** Soutenance face à un Directeur Marketing qui pense que "parler à un robot dégrade l'image de marque". Vous devez prouver la qualité d'un chatbot en vous basant sur les solutions existantes pour éviter les "dérapages".



---

### Étude de Cas 3 : "DevFlow" – L'assistant de code pour une ESN

**Contexte :** Une Entreprise de Services du Numérique (ESN) veut équiper ses 200 développeurs d'outils d'IA pour coder plus vite (génération de tests, refactoring).
**Contrainte majeure :** Performance technique pure (code) et coût de licence.

* **Module 1 (S'initier) :**
* **Objectif :** Distinguer les modèles généralistes des modèles spécialisés "Code".
* **Typologie :** Coding Assistants par exemple.
* **Comparaison :** GitHub Copilot (basé sur OpenAI) vs Cursor (Claude/GPT) vs CodeLlama/DeepSeek (Open Source) ou encore d'autres solutions


* **Module 2 (Réaliser la veille) :**
* **Critères techniques :** Intégration dans l'IDE (VS Code), pertinence du code généré (benchmarks HumanEval), autocomplétion.
* **Livrable :** Une fiche comparative "Propriétaire vs Open Source".


* **Module 3 (Présenter) :**
* **Le Pitch :** Présenter le ROI (Retour sur Investissement) attendu : "Si on gagne 20% de temps par dev, l'outil est remboursé en 1 semaine" (exemple).


* **Module 4 (Convaincre) :**
* **Freins à lever :** Propriété intellectuelle du code généré (à qui appartient le code ?).
* **Simulation :** Le Directeur Juridique bloque le projet car il a peur que le code client soit envoyé dans le cloud de Microsoft/OpenAI. Vous devez proposer une alternative (ex: Ollama en local) ou expliquer les clauses "No-training" des offres Enterprise.





### Étude de Cas 4 : "AdAgency" – La production de contenu marketing

**Contexte :** Une agence de publicité souhaite réduire ses coûts d'achat de photos (stock images) et accélérer la création de maquettes (storyboards) pour ses clients. Ils veulent intégrer l'IA générative d'images.
**Contrainte majeure :** Droit d'auteur (Copyright), protection juridique et cohérence visuelle de la marque.

* **Module 1 (S'initier) :**
* **Objectif :** Comprendre la différence entre LLM (texte) et modèles de diffusion (image).
* **Typologie :** Image Generators (Text-to-Image).
* **Comparaison :** Midjourney v6, DALL-E 3 (via ChatGPT), Adobe Firefly (Enterprise).


* **Module 2 (Réaliser la veille) :**
* **Critères techniques :** Propriété intellectuelle (l'outil offre-t-il une garantie légale ?), photoréalisme, capacité à modifier une zone précise de l'image (*inpainting*), respect des prompts complexes.
* **Livrable :** Un comparatif "Risque vs Qualité". Adobe est plus "safe" juridiquement mais Midjourney souvent plus esthétique.


* **Module 3 (Présenter) :**
* **Le Pitch :** Proposer un workflow où l'IA sert à l'idéation rapide, mais où l'humain finalise. Présentation visuelle obligatoire (avant/après).
* **Adaptation :** Le Directeur de Création déteste l'IA et trouve les résultats "moches et sans âme". Vous devez montrer comment l'IA peut être un outil de "crayonné" et non de finition.


* **Module 4 (Convaincre) :**
* **Freins à lever :** Aspects juridiques (droits d'auteur des images générées) et éthique (remplacement des graphistes).
* **Simulation :** Un client refuse de payer pour des visuels "faits par un robot". Vous devez justifier la valeur ajoutée du "Prompt Engineering" et de la retouche humaine, ou proposer un modèle de facturation différent.



---

### Étude de Cas 5 : "TalentScan" – L'IA au service du Recrutement (RH)

**Contexte :** Un grand groupe reçoit 5 000 CV par mois. Les recruteurs n'arrivent plus à suivre. La DRH veut un outil pour pré-analyser les CV, extraire les compétences clés et rédiger des synthèses pour les entretiens.
**Contrainte majeure :** Éthique (Biais cognitifs), RGPD et explicabilité (pourquoi ce candidat est-il retenu ?).

* **Module 1 (S'initier) :**
* **Objectif :** Identifiez des solutions capables d'analyser des documents non structurés (PDF, Word) sans halluciner, il faut aussi penser au document qui peut manquer de structure.
* **Typologie :** NLP (Natural Language Processing), Parsing de documents, OCR.
* **Comparaison :** Solutions spécialisée RH vs LLM générique (Claude 3 Opus pour sa capacité d'analyse, GPT-4).


* **Module 2 (Réaliser la veille) :**
* **Critères techniques :** Capacité à anonymiser les CV avant analyse, détection des biais (genre, origine), conformité à l'AI Act européen (le recrutement est un cas "Haut Risque").
* **Livrable :** Une matrice des risques éthiques selon la solution choisie.


* **Module 3 (Présenter) :**
* **Le Pitch :** Vendre un gain de temps de 40% sur le tri, permettant aux RH de se concentrer sur l'humain (l'entretien).
* **Adaptation :** La DRH craint que l'IA ne rejette des profils atypiques (les "moutons à cinq pattes"). Vous devez expliquer le concept de "Human in the loop" (l'IA trie, l'humain décide).


* **Module 4 (Convaincre) :**
* **Freins à lever :** La déshumanisation du processus.
* **Simulation :** Un représentant du personnel attaque le projet : "Vous allez laisser un algorithme décider de notre avenir ?". Vous devez défendre la transparence de l'algorithme et les garde-fous mis en place. VOus devez mettre l'accent sur l'interprétabilité.




### Étude de Cas 6 : "SafeFactory" – Vision par ordinateur pour la sécurité

**Contexte :** Une usine métallurgique veut détecter automatiquement si les ouvriers portent bien leurs EPI (casque, gilet jaune) et identifier les intrusions dans les zones dangereuses.
**Contrainte majeure :** Temps réel (latence faible), environnement sans internet stable (Edge Computing) et vie privée.

* **Module 1 (S'initier) :**
* **Objectif :** Sortir du texte pour aller vers la Vision par Ordinateur (Computer Vision).
* **Typologie :** Object Detection, Vision AI.
* **Comparaison :** Google Vertex AI Vision, AWS Rekognition, YOLO (You Only Look Once - Open Source), Azure.


* **Module 2 (Réaliser la veille) :**
* **Critères techniques :** FPS (Frames Per Second), précision de détection dans des conditions de faible luminosité, coût du matériel (caméras + serveurs locaux), floutage automatique des visages (GDPR).
* **Livrable :** Comparatif Cloud (AWS/Google/Azure) vs Local (YOLO sur un serveur local).


* **Module 3 (Présenter) :**
* **Le Pitch :** Présenter le projet sous l'angle "Objectif Zéro Accident" et non "Surveillance des employés".
* **Adaptation :** Coupure de budget : on ne peut pas changer les caméras existantes (qui sont vieilles). Vous devez proposer une solution logicielle compatible avec le vieux matériel (RTSP streams).


* **Module 4 (Convaincre) :**
* **Freins à lever :** La surveillance de masse (Big Brother).
* **Simulation :** Le Directeur de l'usine est d'accord, mais les chefs d'équipe sont contre, craignant que l'IA ne soit utilisée pour chronométrer les pauses. Vous devez prouver techniquement que le système ne stocke pas l'identité des personnes, mais uniquement des alertes de sécurité (Privacy by design).




### Étude de Cas 7 : "MediDictate" – L'automatisation des comptes-rendus médicaux

**Contexte :** Un réseau de cliniques privées souhaite libérer ses médecins de la charge administrative. Actuellement, les médecins passent 2h par jour à taper leurs comptes-rendus de consultation. La direction veut une solution où le médecin dicte à l'oral, et le texte s'écrit automatiquement dans le dossier patient.

**Contrainte majeure :**

1. **Vocabulaire métier :** L'IA ne doit pas confondre "Pericardite" et "Péritonite" (risque médical grave).
2. **Confidentialité (HDS) :** Les données de santé sont sensibles, l'audio ne doit pas servir à entraîner l'IA publique.

---

* **Module 1 (S’initier) :**
* **Objectif :** Comprendre les nuances du marché ASR (Reconnaissance vocale automatique).
* **Typologie :**
* Modèles généralistes (très bons partout) vs Modèles "Fine-tuned" (spécialisés médecine).
* Traitement par lots (envoi d'un fichier MP3 après coup) vs Streaming (texte qui s'affiche en temps réel).


* **Comparaison de solutions (Benchmark) à creuser :**
* **OpenAI Whisper (via API ou Azure) :** La référence actuelle en précision multilingue.
* **Nuance Dragon Medical One (Microsoft) :** Le leader historique, très cher, mais spécialisé médecine.
* **Gladia (Startup Française)** et **Deepgram :** 



* **Module 2 (Réaliser une veille) :**
* **Identifier les critères pertinents (Grille de benchmark) :**
* **WER (Word Error Rate) :** Le taux d'erreur par mot (le critère roi).
* **Terminologie médicale :** Capacité à écrire correctement les noms de médicaments complexes.
* **Diarisation :** Capacité à distinguer la voix du médecin de celle du patient.
* **Déploiement :** SaaS (Cloud) vs On-Premise (Local sur les serveurs de l'hôpital pour la sécurité).


* **Sources d'information :** Hugging Face, documentation technique des API, études de cas "Healthcare".
* **Livrable :** Un comparatif "Coût vs Sécurité" Exemple : Whisper Open Source hébergé en interne (gratuit mais demande des GPU).


* **Module 3 (Présenter) :**
* **Le Pitch :** Présenter la solution retenue au Directoire de la clinique.
* *Angle proposé:* "Transformons 2h de paperasse en 2h de consultation supplémentaire ou de repos pour nos médecins".


* **Adaptation (Improvisation) :**
* *Scénario surprise :* Un médecin dans la salle intervient : "Je dicte souvent dans les couloirs bruyants ou avec mon masque, ça ne marchera jamais."
* *Réaction attendue :* Vous devez parler de la robustesse au bruit (*noise cancellation*) ou proposer une démo technique sur un enregistrement bruyant.



* **Module 4 (Convaincre) :**
* **Identifier les freins :**
* **Juridique/Sécurité :** Peur que les enregistrements vocaux des patients fuitent.
* **Résistance au changement :** Les médecins habitués à leur dictaphone humain (secrétaire).


* **Simulation de soutenance :**
* **L'opposant (joué par le formateur ou un autre groupe) :** Le DPO (Délégué à la protection des données). Il refuse toute solution SaaS américaine (Cloud Act).
* **La réponse attendue :** VOus devez soit proposer une solution souveraine (ex: hébergement OVH/Scaleway avec un modèle Open Source type Whisper Large v3), soit montrer les clauses "Zero Data Retention" des contrats Enterprise.



Quelques question pour cette étude de cas pour vous orienter :

1. **Les Hallucinations :** Certains modèles de STT (comme les premières versions de Whisper) ont tendance, en cas de silence prolongé, à inventer des phrases (ex: "Merci de regarder cette vidéo"). C'est inacceptable dans un rapport médical.
2. **La Ponctuation :** Une dictée médicale nécessite une ponctuation parfaite. L'IA met-elle les points et virgules automatiquement ou faut-il dire "Point à la ligne" ?
3. **Les Accents :** Comment le modèle gère-t-il un médecin avec un fort accent étranger ?





Pour le **Module 2**, cette structure vierge à remplir selon leur étude de cas pourrait vous aider :

| Critères | Solution A (ex: OpenAI) | Solution B (ex: Mistral) | Solution C (ex: Claude) |
| --- | --- | --- | --- |
| **Performance (Qualité)** | *Note /5 sur la tâche précise* | ... | ... |
| **Confidentialité (Data)** | *Entraînement sur données ?* | ... | ... |
| **Coût (Pricing)** | *Abonnement ou Token* | ... | ... |
| **Facilité d'intégration** | *API / Plug & Play* | ... | ... |
| **Fenêtre de contexte** | *Taille (ex: 128k)* | ... | ... |
| **Verdict** | *Gagnant / Perdant* | ... | ... |