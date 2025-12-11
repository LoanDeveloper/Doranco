#!/usr/bin/env python3
"""
Script pour générer un rapport complet du TP
"""

import sqlite3
from datetime import datetime

def get_database_stats():
    """Récupère les statistiques de la base de données"""
    conn = sqlite3.connect('entreprise_dw.db')
    cursor = conn.cursor()
    
    # Nombre total de ventes
    cursor.execute("SELECT COUNT(*) FROM ventes")
    total_ventes = cursor.fetchone()[0]
    
    # Montant total des ventes
    cursor.execute("SELECT SUM(total) FROM ventes")
    montant_total = cursor.fetchone()[0]
    
    # Montant moyen par vente
    cursor.execute("SELECT AVG(total) FROM ventes")
    montant_moyen = cursor.fetchone()[0]
    
    # Produit le plus vendu (en quantité)
    cursor.execute("""
        SELECT produit, SUM(quantite) as total_quantite
        FROM ventes
        GROUP BY produit
        ORDER BY total_quantite DESC
        LIMIT 1
    """)
    produit_plus_vendu = cursor.fetchone()
    
    # Client ayant dépensé le plus
    cursor.execute("""
        SELECT client, SUM(total) as total_depense
        FROM ventes
        GROUP BY client
        ORDER BY total_depense DESC
        LIMIT 1
    """)
    client_plus_depensier = cursor.fetchone()
    
    conn.close()
    
    return {
        'total_ventes': total_ventes,
        'montant_total': montant_total,
        'montant_moyen': montant_moyen,
        'produit_plus_vendu': produit_plus_vendu,
        'client_plus_depensier': client_plus_depensier
    }

def generate_report():
    """Génère un rapport complet"""
    print("=" * 80)
    print("RAPPORT COMPLET - TP Data Lake vs Data Warehouse")
    print("=" * 80)
    print(f"Date de génération : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Statistiques de la base de données
    stats = get_database_stats()
    
    print("STATISTIQUES DES VENTES")
    print("-" * 80)
    print(f"Nombre total de ventes : {stats['total_ventes']}")
    print(f"Montant total des ventes : {stats['montant_total']:.2f} €")
    print(f"Montant moyen par vente : {stats['montant_moyen']:.2f} €")
    print(f"Produit le plus vendu : {stats['produit_plus_vendu'][0]} ({stats['produit_plus_vendu'][1]} unités)")
    print(f"Client ayant le plus dépensé : {stats['client_plus_depensier'][0]} ({stats['client_plus_depensier'][1]:.2f} €)")
    print()
    
    # Détail des ventes
    print("DÉTAIL DES VENTES")
    print("-" * 80)
    
    conn = sqlite3.connect('entreprise_dw.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ventes ORDER BY date")
    rows = cursor.fetchall()
    
    print(f"{'ID':<5} {'Date':<12} {'Client':<10} {'Produit':<15} {'Qté':<5} {'Prix U.':<12} {'Total':<10}")
    print("-" * 80)
    
    for row in rows:
        print(f"{row[0]:<5} {row[1]:<12} {row[2]:<10} {row[3]:<15} {row[4]:<5} {row[5]:<12.2f} {row[6]:<10.2f}")
    
    conn.close()
    print()
    
    # Structure du projet
    print("STRUCTURE DU PROJET")
    print("-" * 80)
    print("""
TP1/
├── data_lake/
│   ├── raw/
│   │   └── ventes_2024.csv      # Données brutes (Data Lake)
│   ├── transformed/
│   └── analytics/
├── entreprise_dw.db              # Data Warehouse (SQLite)
├── etl_script.py                 # Script ETL
├── analyse_comparative.md        # Analyse détaillée
├── verification.py               # Script de vérification
├── generer_rapport.py            # Ce script
└── README.md                     # Documentation
    """)
    
    # Synthèse comparative
    print("SYNTHÈSE COMPARATIVE")
    print("-" * 80)
    print("""
DATA LAKE vs DATA WAREHOUSE

1. STRUCTURATION
   - Data Lake : Données brutes, schéma flexible (schema-on-read)
   - Data Warehouse : Données structurées, schéma rigide (schema-on-write)

2. PERFORMANCES
   - Data Lake : Optimisé pour le volume et la variété
   - Data Warehouse : Optimisé pour les requêtes SQL complexes

3. QUALITÉ DES DONNÉES
   - Data Lake : Qualité variable, nettoyage reporté
   - Data Warehouse : Qualité garantie par le processus ETL

4. CAS D'USAGE
   - Data Lake : Big Data, Machine Learning, exploration
   - Data Warehouse : Reporting, analyse transactionnelle, BI

5. COÛT
   - Data Lake : Moins cher (stockage brut)
   - Data Warehouse : Plus cher (traitement et stockage structuré)
    """)
    
    print("CONCLUSION")
    print("-" * 80)
    print("""
Ce TP a permis de mettre en œuvre concrètement les deux approches de gestion
de données et d'en comprendre les différences fondamentales.

Le Data Lake est idéal pour stocker des données brutes avec flexibilité, tandis
que le Data Warehouse offre une structure optimisée pour l'analyse et le reporting.

Dans la pratique, une approche hybride combinant les deux est souvent la plus
efficace, utilisant le Data Lake pour le stockage brut et le Data Warehouse
pour l'analyse structurée.
    """)
    
    print("=" * 80)
    print("FIN DU RAPPORT")
    print("=" * 80)

if __name__ == '__main__':
    generate_report()