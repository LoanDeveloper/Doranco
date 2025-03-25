# Projet : Client API RappelConsommation

## Description :
    Ce script interroge l’API de rappel de consommation (data.economie.gouv.fr)
    et affiche les résultats de manière claire dans la console. Il inclut :
        - Une fonction pour envoyer une requête HTTP à l’API.
        - Une gestion des erreurs pour éviter les plantages en cas de problème.
        - Une vérification de la validité des entrées utilisateur.
        - Un filtrage des résultats selon certains critères (ex : catégorie, marque, libellé).
        - Quelques tests de validation de la bonne exécution du programme.

### Utilisation :
    - Installez la librairie requests (si nécessaire) : pip install requests
    - Exécutez le script : python rappelconso_client.py
    - Vous serez invité à choisir si vous souhaitez filtrer les résultats.
