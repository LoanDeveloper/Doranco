#!/usr/bin/env python3
"""
Script ETL pour charger les données du Data Lake vers le Data Warehouse
"""

import sqlite3
import csv
import os
from pathlib import Path

def create_database():
    """Crée la base de données et la table ventes"""
    conn = sqlite3.connect('entreprise_dw.db')
    cursor = conn.cursor()
    
    # Créer la table ventes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ventes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            client TEXT,
            produit TEXT,
            quantite INTEGER,
            prix_unitaire REAL,
            total REAL
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Base de données et table créées avec succès.")

def load_data_from_csv():
    """Charge les données depuis le CSV vers la base de données"""
    csv_path = Path('data_lake/raw/ventes_2024.csv')
    
    if not csv_path.exists():
        print(f"Erreur : Le fichier {csv_path} n'existe pas.")
        return
    
    conn = sqlite3.connect('entreprise_dw.db')
    cursor = conn.cursor()
    
    # Lire le fichier CSV et insérer les données
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            # Calculer le total
            quantite = int(row['Quantite'])
            prix_unitaire = float(row['PrixUnitaire'])
            total = quantite * prix_unitaire
            
            # Insérer dans la base
            cursor.execute('''
                INSERT INTO ventes (date, client, produit, quantite, prix_unitaire, total)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (row['Date'], row['Client'], row['Produit'], quantite, prix_unitaire, total))
    
    conn.commit()
    conn.close()
    print(f"Données chargées avec succès depuis {csv_path}")

def display_table():
    """Affiche le contenu de la table ventes"""
    conn = sqlite3.connect('entreprise_dw.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM ventes')
    rows = cursor.fetchall()
    
    print("\nContenu de la table ventes :")
    print("-" * 80)
    print(f"{'ID':<5} {'Date':<12} {'Client':<10} {'Produit':<15} {'Quantité':<10} {'Prix Unitaire':<15} {'Total':<10}")
    print("-" * 80)
    
    for row in rows:
        print(f"{row[0]:<5} {row[1]:<12} {row[2]:<10} {row[3]:<15} {row[4]:<10} {row[5]:<15.2f} {row[6]:<10.2f}")
    
    conn.close()

def main():
    """Fonction principale"""
    print("Début du processus ETL...")
    print("=" * 50)
    
    # Étape 1 : Créer la base de données
    create_database()
    
    # Étape 2 : Charger les données
    load_data_from_csv()
    
    # Étape 3 : Afficher le résultat
    display_table()
    
    print("\n" + "=" * 50)
    print("Processus ETL terminé avec succès !")

if __name__ == '__main__':
    main()