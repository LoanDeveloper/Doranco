#!/usr/bin/env python3
"""
Pipeline ETL pour un schéma en étoile
- Extraction des données brutes
- Transformation et nettoyage
- Chargement dans le Data Warehouse
"""

import os
import sys
import logging
import json
import pandas as pd
import sqlite3
from sqlalchemy import create_engine
from datetime import datetime
import yaml
import glob

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('etl_pipeline/logs/etl.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ETLPipeline:
    def __init__(self, config_path='etl_pipeline/config/config.yml'):
        """Initialisation du pipeline avec la configuration"""
        self.config = self._load_config(config_path)
        self.raw_path = self.config['data_lake']['raw']
        self.curated_path = self.config['data_lake']['curated']
        self.warehouse_path = self.config['warehouse']['path']
        
        # Créer les répertoires si nécessaire
        os.makedirs(self.curated_path, exist_ok=True)
        os.makedirs(os.path.dirname(self.config['logging']['file']), exist_ok=True)
        
        logger.info("Pipeline ETL initialisé avec succès")
    
    def _load_config(self, config_path):
        """Charger la configuration YAML"""
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            return config
        except Exception as e:
            logger.error(f"Erreur de chargement de la configuration: {e}")
            raise
    
    def extract_data(self):
        """Extraction des données brutes depuis différentes sources"""
        logger.info("Début de l'extraction des données brutes")
        
        all_data = []
        
        # 1. Extraction des fichiers CSV
        csv_files = glob.glob(os.path.join(self.raw_path, 'csv', '*.csv'))
        for csv_file in csv_files:
            try:
                df = pd.read_csv(csv_file)
                # Standardisation des noms de colonnes
                df.columns = [col.lower().replace(' ', '_') for col in df.columns]
                all_data.append(df)
                logger.info(f"Fichier CSV extrait: {csv_file} ({len(df)} lignes)")
            except Exception as e:
                logger.error(f"Erreur d'extraction du fichier {csv_file}: {e}")
        
        # 2. Extraction des fichiers Excel
        excel_files = glob.glob(os.path.join(self.raw_path, 'excel', '*.xlsx'))
        for excel_file in excel_files:
            try:
                df = pd.read_excel(excel_file)
                # Standardisation des noms de colonnes
                df.columns = [col.lower().replace(' ', '_') for col in df.columns]
                # Renommage des colonnes spécifiques Excel
                df = df.rename(columns={
                    'orderid': 'order_id',
                    'orderdate': 'order_date',
                    'customerid': 'customer_id',
                    'productid': 'product_id',
                    'qty': 'quantity',
                    'unitprice': 'unit_price',
                    'total': 'total_amount'
                })
                all_data.append(df)
                logger.info(f"Fichier Excel extrait: {excel_file} ({len(df)} lignes)")
            except Exception as e:
                logger.error(f"Erreur d'extraction du fichier {excel_file}: {e}")
        
        # 3. Extraction des fichiers JSON
        json_files = glob.glob(os.path.join(self.raw_path, 'json', '*.json'))
        for json_file in json_files:
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                df = pd.DataFrame(data)
                # Standardisation des noms de colonnes
                df.columns = [col.lower().replace(' ', '_').replace('.', '_') for col in df.columns]
                # Renommage des colonnes spécifiques JSON
                df = df.rename(columns={
                    'orderid': 'order_id',
                    'orderdate': 'order_date', 
                    'customerid': 'customer_id',
                    'productid': 'product_id',
                    'qty': 'quantity',
                    'unitprice': 'unit_price',
                    'total': 'total_amount'
                })
                all_data.append(df)
                logger.info(f"Fichier JSON extrait: {json_file} ({len(df)} lignes)")
            except Exception as e:
                logger.error(f"Erreur d'extraction du fichier {json_file}: {e}")
        
        if not all_data:
            logger.error("Aucune donnée extraite")
            return None
        
        # Concatenation de toutes les données
        raw_df = pd.concat(all_data, ignore_index=True)
        logger.info(f"Extraction terminée: {len(raw_df)} lignes au total")
        
        return raw_df
    
    def transform_data(self, raw_df):
        """Transformation et nettoyage des données"""
        if raw_df is None or raw_df.empty:
            logger.error("Aucune donnée à transformer")
            return None
            
        logger.info("Début de la transformation des données")
        
        # Copie du DataFrame pour éviter les modifications directes
        df = raw_df.copy()
        
        # 1. Vérification des colonnes attendues
        expected_columns = ['order_id', 'order_date', 'customer_id', 'product_id', 'quantity', 'unit_price', 'total_amount', 'currency']
        missing_cols = [col for col in expected_columns if col not in df.columns]
        if missing_cols:
            logger.warning(f"Colonnes manquantes dans les données: {missing_cols}")
        
        # 2. Nettoyage des valeurs manquantes
        initial_count = len(df)
        logger.info(f"Avant nettoyage: {initial_count} lignes")
        
        # Vérification des valeurs manquantes avant suppression
        missing_values = df.isnull().sum()
        logger.info(f"Valeurs manquantes avant nettoyage: {missing_values}")
        
        # Ne supprimer que si nécessaire
        if missing_values.sum() > 0:
            df = df.dropna()
            cleaned_count = len(df)
            logger.info(f"Nettoyage des valeurs manquantes: {initial_count - cleaned_count} lignes supprimées")
        else:
            cleaned_count = initial_count
            logger.info("Aucune valeur manquante à supprimer")
        
        # 3. Conversion des types de données
        # Conversion des dates
        df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
        
        # Conversion des IDs en entiers
        df['order_id'] = df['order_id'].astype(int)
        df['customer_id'] = df['customer_id'].astype(int)
        df['product_id'] = df['product_id'].astype(int)
        
        # Conversion des valeurs numériques
        df['quantity'] = df['quantity'].astype(int)
        df['unit_price'] = df['unit_price'].astype(float)
        df['total_amount'] = df['total_amount'].astype(float)
        
        # 4. Standardisation des devises
        if 'currency' in df.columns and df['currency'].dtype == object:
            df['currency'] = df['currency'].str.upper()
        else:
            df['currency'] = df['currency'].astype(str).str.upper()
        
        # 5. Calculs de colonnes dérivées
        # Vérification de la cohérence des montants
        df['calculated_amount'] = df['quantity'] * df['unit_price']
        df['amount_discrepancy'] = abs(df['total_amount'] - df['calculated_amount'])
        
        # 6. Extraction des composants de date
        df['order_year'] = df['order_date'].dt.year
        df['order_month'] = df['order_date'].dt.month
        df['order_day'] = df['order_date'].dt.day
        df['order_quarter'] = df['order_date'].dt.quarter
        
        logger.info(f"Transformation terminée: {len(df)} lignes transformées")
        
        return df
    
    def load_to_curated(self, transformed_df, filename='orders_clean.parquet'):
        """Sauvegarde des données transformées dans la zone curated"""
        if transformed_df is None or transformed_df.empty:
            logger.error("Aucune donnée à sauvegarder dans la zone curated")
            return None
            
        file_path = os.path.join(self.curated_path, filename)
        
        try:
            transformed_df.to_parquet(file_path, index=False)
            logger.info(f"Données sauvegardées dans la zone curated: {file_path}")
            return file_path
        except Exception as e:
            logger.error(f"Erreur de sauvegarde dans la zone curated: {e}")
            return None
    
    def create_star_schema(self):
        """Création du schéma en étoile dans le Data Warehouse"""
        try:
            conn = sqlite3.connect(self.warehouse_path)
            cursor = conn.cursor()
            
            # Création des tables de dimensions
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS dim_customer (
                    customer_id INTEGER PRIMARY KEY,
                    customer_name TEXT,
                    customer_segment TEXT
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS dim_product (
                    product_id INTEGER PRIMARY KEY,
                    product_name TEXT,
                    product_category TEXT,
                    unit_price REAL
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS dim_time (
                    date_id TEXT PRIMARY KEY,
                    date_value TEXT,
                    year INTEGER,
                    month INTEGER,
                    day INTEGER,
                    quarter INTEGER,
                    day_of_week INTEGER
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS dim_currency (
                    currency_code TEXT PRIMARY KEY,
                    currency_name TEXT
                )
            ''')
            
            # Création de la table de faits
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS fact_sales (
                    sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id INTEGER,
                    customer_id INTEGER,
                    product_id INTEGER,
                    date_id TEXT,
                    quantity INTEGER,
                    unit_price REAL,
                    total_amount REAL,
                    currency_code TEXT,
                    FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id),
                    FOREIGN KEY (product_id) REFERENCES dim_product(product_id),
                    FOREIGN KEY (date_id) REFERENCES dim_time(date_id),
                    FOREIGN KEY (currency_code) REFERENCES dim_currency(currency_code)
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("Schéma en étoile créé avec succès")
            
        except Exception as e:
            logger.error(f"Erreur de création du schéma en étoile: {e}")
    
    def load_to_warehouse(self, transformed_df):
        """Chargement des données dans le Data Warehouse"""
        if transformed_df is None or transformed_df.empty:
            logger.error("Aucune donnée à charger dans le Data Warehouse")
            return
            
        try:
            # Connexion à la base de données
            engine = create_engine(f'sqlite:///{self.warehouse_path}')
            
            # Chargement des données dans la table de faits
            transformed_df.to_sql('fact_sales', engine, if_exists='replace', index=False)
            
            logger.info(f"Données chargées dans le Data Warehouse: {len(transformed_df)} lignes")
            
        except Exception as e:
            logger.error(f"Erreur de chargement dans le Data Warehouse: {e}")
    
    def run_pipeline(self):
        """Exécution complète du pipeline ETL"""
        logger.info("Début du pipeline ETL")
        
        try:
            # 1. Extraction
            raw_df = self.extract_data()
            if raw_df is None:
                return False
                
            # 2. Transformation
            transformed_df = self.transform_data(raw_df)
            if transformed_df is None:
                return False
                
            # 3. Sauvegarde dans la zone curated
            curated_file = self.load_to_curated(transformed_df)
            if curated_file is None:
                return False
                
            # 4. Création du schéma en étoile
            self.create_star_schema()
            
            # 5. Chargement dans le Data Warehouse
            self.load_to_warehouse(transformed_df)
            
            logger.info("Pipeline ETL terminé avec succès")
            return True
            
        except Exception as e:
            logger.error(f"Erreur dans le pipeline ETL: {e}")
            return False

if __name__ == "__main__":
    # Exécution du pipeline
    pipeline = ETLPipeline()
    success = pipeline.run_pipeline()
    
    if success:
        logger.info("Pipeline ETL exécuté avec succès")
        sys.exit(0)
    else:
        logger.error("Échec du pipeline ETL")
        sys.exit(1)