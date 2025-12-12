#!/usr/bin/env python3
"""
Script de validation du pipeline ETL
"""

import os
import pandas as pd
import sqlite3
import logging

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def validate_data_lake():
    """Validation de la zone curated du Data Lake"""
    logger.info("Validation de la zone curated...")
    
    curated_path = "etl_star_schema_dataset/etl_star_schema/data_lake/curated"
    parquet_file = os.path.join(curated_path, "orders_clean.parquet")
    
    if not os.path.exists(parquet_file):
        logger.error(f"Fichier curated introuvable: {parquet_file}")
        return False
    
    try:
        df = pd.read_parquet(parquet_file)
        logger.info(f"Fichier curated validé: {len(df)} lignes, {len(df.columns)} colonnes")
        logger.info(f"Colonnes: {list(df.columns)}")
        return True
    except Exception as e:
        logger.error(f"Erreur de lecture du fichier curated: {e}")
        return False

def validate_warehouse():
    """Validation du Data Warehouse"""
    logger.info("Validation du Data Warehouse...")
    
    warehouse_path = "etl_star_schema_dataset/etl_star_schema/warehouse.db"
    
    try:
        conn = sqlite3.connect(warehouse_path)
        cursor = conn.cursor()
        
        # Vérification des tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [table[0] for table in cursor.fetchall()]
        
        expected_tables = ['fact_sales', 'dim_customer', 'dim_product', 'dim_time', 'dim_currency']
        missing_tables = [table for table in expected_tables if table not in tables]
        
        if missing_tables:
            logger.error(f"Tables manquantes dans le Data Warehouse: {missing_tables}")
            return False
        
        # Vérification des données dans fact_sales
        cursor.execute("SELECT COUNT(*) FROM fact_sales;")
        count = cursor.fetchone()[0]
        logger.info(f"Table fact_sales: {count} lignes")
        
        # Vérification de quelques enregistrements
        cursor.execute("SELECT * FROM fact_sales LIMIT 3;")
        sample_data = cursor.fetchall()
        logger.info(f"Échantillon de données: {sample_data}")
        
        conn.close()
        logger.info("Data Warehouse validé avec succès")
        return True
        
    except Exception as e:
        logger.error(f"Erreur de validation du Data Warehouse: {e}")
        return False

def validate_data_quality():
    """Validation de la qualité des données"""
    logger.info("Validation de la qualité des données...")
    
    try:
        # Chargement des données transformées
        df = pd.read_parquet("etl_star_schema_dataset/etl_star_schema/data_lake/curated/orders_clean.parquet")
        
        # Vérifications de qualité
        checks = []
        
        # 1. Pas de valeurs manquantes
        missing_values = df.isnull().sum().sum()
        checks.append(("Valeurs manquantes", missing_values == 0))
        
        # 2. Types de données corrects
        expected_types = {
            'order_id': 'int64',
            'customer_id': 'int64', 
            'product_id': 'int64',
            'quantity': 'int64',
            'unit_price': 'float64',
            'total_amount': 'float64'
        }
        
        type_checks = []
        for col, expected_type in expected_types.items():
            if col in df.columns:
                actual_type = str(df[col].dtype)
                type_checks.append(actual_type == expected_type)
        
        checks.append(("Types de données", all(type_checks)))
        
        # 3. Cohérence des montants
        df['calculated_check'] = df['quantity'] * df['unit_price']
        discrepancy_count = (abs(df['total_amount'] - df['calculated_check']) > 0.01).sum()
        checks.append(("Cohérence des montants", discrepancy_count == 0))
        
        # 4. Dates valides
        date_check = df['order_date'].notna().all()
        checks.append(("Dates valides", date_check))
        
        # Affichage des résultats
        for check_name, result in checks:
            status = "✓" if result else "✗"
            logger.info(f"{status} {check_name}: {'OK' if result else 'ÉCHEC'}")
        
        all_passed = all(result for _, result in checks)
        logger.info(f"Validation de la qualité: {'SUCCESS' if all_passed else 'ÉCHEC'}")
        return all_passed
        
    except Exception as e:
        logger.error(f"Erreur de validation de la qualité: {e}")
        return False

def main():
    """Exécution des validations"""
    logger.info("Début de la validation du pipeline ETL")
    
    validations = [
        ("Data Lake", validate_data_lake),
        ("Data Warehouse", validate_warehouse),
        ("Qualité des données", validate_data_quality)
    ]
    
    results = []
    for name, validation_func in validations:
        logger.info(f"\n--- Validation: {name} ---")
        result = validation_func()
        results.append((name, result))
    
    # Résumé
    logger.info("\n=== Résumé de la validation ===")
    all_passed = True
    for name, result in results:
        status = "✓ SUCCESS" if result else "✗ ÉCHEC"
        logger.info(f"{status} - {name}")
        if not result:
            all_passed = False
    
    if all_passed:
        logger.info("\n🎉 Toutes les validations ont réussi !")
        return True
    else:
        logger.error("\n❌ Certaines validations ont échoué")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)