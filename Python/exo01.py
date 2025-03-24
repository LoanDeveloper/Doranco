employes = {}  # Dictionnaire : {ID: Nom}

def ajouter_employe(nom, identifiant):
    if identifiant in employes:
        print(f"Erreur : L'ID {identifiant} est déjà attribué à {employes[identifiant]}.")
        return
    employes[identifiant] = nom
    print(f"Employé ajouté : {nom} (ID : {identifiant})")

def afficher_employes():
    if not employes:
        print("Aucun employé enregistré.")
        return
    print("\nListe des employés :")
    for i, (id, nom) in enumerate(employes.items(), start=1):
        print(f"{i}. {nom} (ID : {id})")

def supprimer_employe(valeur):
    if isinstance(valeur, int):  # Suppression par ID
        if valeur in employes:
            nom = employes.pop(valeur)
            print(f"L'employé {nom} (ID : {valeur}) a été supprimé.")
        else:
            print("Erreur : Aucun employé avec cet ID.")
    elif isinstance(valeur, str):  # Suppression par nom
        for id, nom in list(employes.items()):
            if nom == valeur:
                del employes[id]
                print(f"L'employé {valeur} a été supprimé.")
                return
        print("Erreur : Aucun employé avec ce nom.")
    else:
        print("Erreur : Entrée invalide.")

# Exemple d'utilisation
ajouter_employe("Dupont", 101)
ajouter_employe("Martin", 102)
ajouter_employe("Durand", 103)
afficher_employes()
supprimer_employe("Martin")
afficher_employes()