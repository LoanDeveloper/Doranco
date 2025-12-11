#!/usr/bin/env python3
"""
Script de vérification du TP
"""

import sqlite3
import os
from pathlib import Path

def verify_data_lake():
    """Vérifie la structure du Data Lake"""
    print("Vérification du Data Lake...")
    print("-" * 50)
    
    # Vérifier la structure des dossiers
    required_dirs = [
        'data_lake',
        'data_lake/raw',
        'data_lake/transformed',
        'data_lake/analytics'
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"✓ {dir_path} existe")
        else:
            print(f"✗ {dir_path} est manquant")
            all_exist = False
    
    # Vérifier le fichier CSV
    csv_path = Path('data_lake/raw/ventes_2024.csv')
    if csv_path.exists():
        print(f"✓ Fichier CSV existe : {csv_path}")
        with open(csv_path, 'r') as f:
            lines = f.readlines()
            print(f"  - Nombre de lignes : {len(lines)}")
            print(f"  - En-tête : {lines[0].strip()}")
    else:
        print(f"✗ Fichier CSV manquant : {csv_path}")
        all_exist = False
    
    return all_exist

def verify_data_warehouse():
    """Vérifie la base de données Data Warehouse"""
    print("\nVérification du Data Warehouse...")
    print("-" * 50)
    
    db_exists = False
    table_exists = False
    data_loaded = False
    
    # Vérifier si la base existe
    if Path('entreprise_dw.db').exists():
        print("✓ Base de données existe : entreprise_dw.db")
        db_exists = True
        
        # Vérifier la structure de la table
        conn = sqlite3.connect('entreprise_dw.db')
        cursor = conn.cursor()
        
        # Vérifier si la table existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ventes'")
        if cursor.fetchone():
            print("✓ Table 'ventes' existe")
            table_exists = True
            
            # Vérifier la structure de la table
            cursor.execute("PRAGMA table_info(ventes)")
            columns = cursor.fetchall()
            print("  Structure de la table :")
            for col in columns:
                print(f"    - {col[1]} ({col[2]})")
            
            # Vérifier si des données sont chargées
            cursor.execute("SELECT COUNT(*) FROM ventes")
            count = cursor.fetchone()[0]
            if count > 0:
                print(f"✓ Données chargées : {count} enregistrements")
                data_loaded = True
                
                # Afficher quelques exemples
                cursor.execute("SELECT * FROM ventes LIMIT 3")
                rows = cursor.fetchall()
                print("  Exemples de données :")
                for row in rows:
                    print(f"    {row}")
            else:
                print("✗ Aucune donnée dans la table")
        else:
            print("✗ Table 'ventes' introuvable")
        
        conn.close()
    else:
        print("✗ Base de données introuvable : entreprise_dw.db")
    
    return db_exists and table_exists and data_loaded

def verify_etl_script():
    """Vérifie le script ETL"""
    print("\nVérification du script ETL...")
    print("-" * 50)
    
    script_path = Path('etl_script.py')
    if script_path.exists():
        print(f"✓ Script ETL existe : {script_path}")
        
        # Vérifier la taille du script
        size = script_path.stat().st_size
        print(f"  Taille : {size} octets")
        
        # Vérifier quelques fonctionnalités clés
        with open(script_path, 'r') as f:
            content = f.read()
            
            checks = [
                ('import sqlite3', 'Import SQLite'),
                ('import csv', 'Import CSV'),
                ('CREATE TABLE', 'Création de table'),
                ('INSERT INTO', 'Insertion de données'),
                ('quantite * prix_unitaire', 'Calcul du total'),
            ]
            
            for check, description in checks:
                if check in content:
                    print(f"  ✓ {description}")
                else:
                    print(f"  ✗ {description} manquant")
        
        return True
    else:
        print(f"✗ Script ETL manquant : {script_path}")
        return False

def verify_analysis():
    """Vérifie le document d'analyse"""
    print("\nVérification de l'analyse comparative...")
    print("-" * 50)
    
    analysis_path = Path('analyse_comparative.md')
    if analysis_path.exists():
        print(f"✓ Document d'analyse existe : {analysis_path}")
        
        with open(analysis_path, 'r') as f:
            content = f.read()
            
            # Vérifier la présence de sections clés
            sections = [
                'Types de requêtes',
                'Niveau de structuration',
                'Gouvernance',
                'Qualité',
                'Sécurité',
                'Conclusion'
            ]
            
            found_sections = 0
            for section in sections:
                if section in content:
                    print(f"  ✓ Section '{section}' présente")
                    found_sections += 1
            
            print(f"\n  Sections trouvées : {found_sections}/{len(sections)}")
        
        return True
    else:
        print(f"✗ Document d'analyse manquant : {analysis_path}")
        return False

def main():
    """Fonction principale de vérification"""
    print("=" * 60)
    print("VÉRIFICATION DU TP - Data Lake vs Data Warehouse")
    print("=" * 60)
    
    # Lancer toutes les vérifications
    dl_ok = verify_data_lake()
    dw_ok = verify_data_warehouse()
    etl_ok = verify_etl_script()
    analysis_ok = verify_analysis()
    
    # Résumé
    print("\n" + "=" * 60)
    print("RÉSUMÉ DE LA VÉRIFICATION")
    print("=" * 60)
    
    checks = [
        ("Data Lake", dl_ok),
        ("Data Warehouse", dw_ok),
        ("Script ETL", etl_ok),
        ("Analyse comparative", analysis_ok),
    ]
    
    all_ok = True
    for name, status in checks:
        symbol = "✓" if status else "✗"
        print(f"{symbol} {name}: {'OK' if status else 'ÉCHEC'}")
        if not status:
            all_ok = False
    
    print("\n" + "=" * 60)
    if all_ok:
        print("🎉 TOUS LES COMPOSANTS SONT VALIDÉS !")
        print("Le TP est terminé avec succès.")
    else:
        print("⚠️  Certains composants nécessitent une attention.")
        print("Veuillez vérifier les messages d'erreur ci-dessus.")
    print("=" * 60)

if __name__ == '__main__':
    main()