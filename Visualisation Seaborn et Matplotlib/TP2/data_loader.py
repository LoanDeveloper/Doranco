"""
Module de chargement et préparation des données pour le dashboard Dash
Optimisé avec pré-agrégation et cache pour performances instantanées
"""
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
from functools import lru_cache
import time


class DataLoader:
    """Classe pour charger et préparer les données de retard des transports"""

    def __init__(self, data_path: str = "../tp/data/transit_delays.csv"):
        """
        Initialise le chargeur de données

        Args:
            data_path: Chemin vers le fichier CSV des données
        """
        self.data_path = data_path
        self.df = None
        self.df_clean = None

        # Cache des agrégations pré-calculées (perf instantanée)
        self._hourly_agg = None
        self._line_stats_cache = None
        self._heatmap_cache = None
        self._histogram_cache = None
        self._geo_sample_cache = None

    def load_data(self):
        """Charge les données depuis le fichier CSV"""
        print(f"Chargement des données depuis {self.data_path}...")
        self.df = pd.read_csv(self.data_path)

        # Conversion des timestamps
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
        self.df['hour'] = self.df['timestamp'].dt.hour
        self.df['minute'] = self.df['timestamp'].dt.minute
        self.df['time_str'] = self.df['timestamp'].dt.strftime('%H:%M')

        # Conversion des retards en minutes
        self.df['delay_minutes'] = self.df['delay_seconds'] / 60

        # Type de transport
        self.df['transport_type'] = self.df['route_type'].map({0: 'Tram', 3: 'Bus'})

        print(f"✅ {len(self.df):,} observations chargées")
        return self.df

    def clean_data(self):
        """Nettoie les données en supprimant les valeurs aberrantes"""
        if self.df is None:
            raise ValueError("Les données doivent être chargées avant nettoyage")

        print("Nettoyage des données...")

        # Suppression des valeurs nulles
        df_clean = self.df.dropna(subset=['delay_minutes', 'route_id', 'vehicle_id'])

        # Suppression des retards aberrants (> ±60 minutes)
        df_clean = df_clean[df_clean['delay_minutes'].abs() <= 60]

        # Vérification des coordonnées GPS valides (Nice: ~43.7°N, 7.2°E)
        df_clean = df_clean[
            (df_clean['latitude'].between(43.6, 43.8)) &
            (df_clean['longitude'].between(7.0, 7.5))
        ]

        self.df_clean = df_clean
        removed_pct = (1 - len(df_clean)/len(self.df)) * 100
        print(f"✅ Nettoyage terminé: {removed_pct:.1f}% de données filtrées")
        print(f"   {len(df_clean):,} observations retenues")

        # Pré-calcul automatique des agrégations pour perf instantanée
        self._precompute_aggregates()

        return self.df_clean

    def _precompute_aggregates(self):
        """
        🚀 Pré-calcule toutes les agrégations pour des performances instantanées
        Cette méthode est appelée une seule fois au démarrage
        """
        if self.df_clean is None:
            return

        print("⚡ Pré-calcul des agrégations pour performances optimales...")
        start_time = time.time()

        # 1. Agrégation horaire par ligne et type de transport
        self._hourly_agg = self.df_clean.groupby(['route_id', 'hour', 'transport_type']).agg({
            'delay_minutes': ['mean', 'std', 'count', 'median']
        }).reset_index()
        self._hourly_agg.columns = ['route_id', 'hour', 'transport_type', 'mean_delay', 'std_delay', 'count', 'median_delay']
        self._hourly_agg['ci'] = 1.96 * self._hourly_agg['std_delay'] / np.sqrt(self._hourly_agg['count'])

        # 2. Cache des stats par ligne
        self._line_stats_cache = {}

        # 3. Cache des heatmaps
        self._heatmap_cache = {}

        # 4. Échantillon géographique fixe (5k points)
        self._geo_sample_cache = self.df_clean.sample(n=min(5000, len(self.df_clean)), random_state=42)[
            ['route_id', 'latitude', 'longitude', 'delay_minutes', 'transport_type']
        ].copy()

        # 5. Pré-calcul des histogrammes par type de transport
        self._histogram_cache = {}
        for transport_type in self.df_clean['transport_type'].unique():
            df_type = self.df_clean[self.df_clean['transport_type'] == transport_type]
            hist, bins = np.histogram(df_type['delay_minutes'], bins=50, range=(-15, 15))
            self._histogram_cache[transport_type] = {'hist': hist, 'bins': bins}

        elapsed = time.time() - start_time
        print(f"✅ Agrégations pré-calculées en {elapsed:.2f}s")
        print(f"   • Données horaires: {len(self._hourly_agg):,} lignes")
        print(f"   • Échantillon géographique: {len(self._geo_sample_cache):,} points")

    def get_summary_stats(self):
        """Calcule les statistiques résumées"""
        if self.df_clean is None:
            raise ValueError("Les données doivent être nettoyées avant calcul des stats")

        stats = {
            'total_obs': len(self.df_clean),
            'mean_delay': self.df_clean['delay_minutes'].mean(),
            'median_delay': self.df_clean['delay_minutes'].median(),
            'std_delay': self.df_clean['delay_minutes'].std(),
            'ontime_pct': (self.df_clean['delay_minutes'].abs() <= 1).mean() * 100,
            'late_pct': (self.df_clean['delay_minutes'] > 2).mean() * 100,
            'early_pct': (self.df_clean['delay_minutes'] < -2).mean() * 100,
            'unique_lines': self.df_clean['route_id'].nunique(),
            'unique_vehicles': self.df_clean['vehicle_id'].nunique(),
            'start_time': self.df_clean['timestamp'].min(),
            'end_time': self.df_clean['timestamp'].max()
        }

        return stats

    def get_line_stats(self, min_observations: int = 50):
        """
        🚀 OPTIMISÉ: Calcule les statistiques par ligne (avec cache)

        Args:
            min_observations: Nombre minimum d'observations pour considérer une ligne

        Returns:
            DataFrame avec les statistiques par ligne
        """
        if self.df_clean is None:
            raise ValueError("Les données doivent être nettoyées avant calcul")

        # Utiliser le cache si disponible
        cache_key = f"min_obs_{min_observations}"
        if cache_key in self._line_stats_cache:
            return self._line_stats_cache[cache_key]

        # Calculer depuis les agrégations horaires (plus rapide)
        if self._hourly_agg is not None:
            line_delays = self._hourly_agg.groupby('route_id').agg({
                'mean_delay': 'mean',
                'median_delay': 'mean',
                'std_delay': 'mean',
                'count': 'sum'
            }).round(2)
            line_delays.columns = ['mean_delay', 'median_delay', 'std_delay', 'n_observations']
            line_delays = line_delays.reset_index()
        else:
            # Fallback si pas d'agrégations
            line_delays = self.df_clean.groupby('route_id').agg({
                'delay_minutes': ['mean', 'median', 'std', 'count']
            }).round(2)
            line_delays.columns = ['mean_delay', 'median_delay', 'std_delay', 'n_observations']
            line_delays = line_delays.reset_index()

        # Filtrer les lignes avec assez d'observations
        line_delays = line_delays[line_delays['n_observations'] >= min_observations]

        # Mettre en cache
        self._line_stats_cache[cache_key] = line_delays

        return line_delays

    def get_hourly_stats(self, transport_types=None, hours=None):
        """
        🚀 OPTIMISÉ: Calcule les statistiques par heure (utilise les agrégations)

        Args:
            transport_types: Liste des types de transport à inclure (None = tous)
            hours: Liste des heures à inclure (None = toutes)

        Returns:
            DataFrame avec les statistiques par heure
        """
        if self.df_clean is None:
            raise ValueError("Les données doivent être nettoyées avant calcul")

        # Utiliser les agrégations pré-calculées
        if self._hourly_agg is not None:
            df_agg = self._hourly_agg.copy()

            # Filtrer par type de transport
            if transport_types is not None and len(transport_types) > 0:
                df_agg = df_agg[df_agg['transport_type'].isin(transport_types)]

            # Filtrer par heure
            if hours is not None and len(hours) > 0:
                df_agg = df_agg[df_agg['hour'].isin(hours)]

            # Agréger par heure (tous types de transport confondus)
            hourly_delays = df_agg.groupby('hour').agg({
                'mean_delay': lambda x: np.average(x, weights=df_agg.loc[x.index, 'count']),
                'count': 'sum'
            }).reset_index()

            # Recalculer std et ci
            hourly_delays['std_delay'] = df_agg.groupby('hour')['std_delay'].mean().values
            hourly_delays['ci'] = 1.96 * hourly_delays['std_delay'] / np.sqrt(hourly_delays['count'])

            return hourly_delays
        else:
            # Fallback
            hourly_delays = self.df_clean.groupby('hour').agg({
                'delay_minutes': ['mean', 'std', 'count']
            }).reset_index()
            hourly_delays.columns = ['hour', 'mean_delay', 'std_delay', 'count']
            hourly_delays['ci'] = 1.96 * hourly_delays['std_delay'] / np.sqrt(hourly_delays['count'])
            return hourly_delays

    def get_heatmap_data(self, top_n_lines: int = 20):
        """
        🚀 OPTIMISÉ: Crée les données pour la heatmap ligne × heure (avec cache)

        Args:
            top_n_lines: Nombre de lignes principales à inclure

        Returns:
            DataFrame pivot pour la heatmap
        """
        if self.df_clean is None:
            raise ValueError("Les données doivent être nettoyées avant calcul")

        # Utiliser le cache si disponible
        if top_n_lines in self._heatmap_cache:
            return self._heatmap_cache[top_n_lines]

        # Utiliser les agrégations pré-calculées
        if self._hourly_agg is not None:
            # Sélection des N lignes principales (par nombre d'observations)
            top_lines = self._hourly_agg.groupby('route_id')['count'].sum().nlargest(top_n_lines).index.tolist()
            df_top = self._hourly_agg[self._hourly_agg['route_id'].isin(top_lines)]

            # Créer une matrice ligne × heure
            heatmap_data = df_top.pivot_table(
                values='mean_delay',
                index='route_id',
                columns='hour',
                aggfunc='mean'
            )
        else:
            # Fallback
            top_lines = self.df_clean['route_id'].value_counts().head(top_n_lines).index.tolist()
            df_top = self.df_clean[self.df_clean['route_id'].isin(top_lines)]
            heatmap_data = df_top.pivot_table(
                values='delay_minutes',
                index='route_id',
                columns='hour',
                aggfunc='mean'
            )

        # Trier les lignes par retard moyen décroissant
        heatmap_data['mean'] = heatmap_data.mean(axis=1)
        heatmap_data = heatmap_data.sort_values('mean', ascending=False).drop('mean', axis=1)

        # Mettre en cache
        self._heatmap_cache[top_n_lines] = heatmap_data

        return heatmap_data

    def get_transport_comparison(self):
        """Compare les statistiques par type de transport (Bus vs Tram)"""
        if self.df_clean is None:
            raise ValueError("Les données doivent être nettoyées avant calcul")

        comparison = self.df_clean.groupby('transport_type')['delay_minutes'].agg([
            'mean', 'median', 'std', 'count'
        ]).round(2)

        return comparison

    def get_geo_sample(self, transport_types=None, hours=None):
        """
        🚀 OPTIMISÉ: Retourne l'échantillon géographique pré-calculé (5k points)

        Args:
            transport_types: Liste des types de transport à inclure (None = tous)
            hours: Liste des heures à inclure (None = toutes)

        Returns:
            DataFrame échantillonné et filtré
        """
        if self._geo_sample_cache is None:
            # Fallback: créer un échantillon à la volée
            df_sample = self.df_clean.sample(n=min(5000, len(self.df_clean)), random_state=42)
        else:
            df_sample = self._geo_sample_cache.copy()

        # Filtrer
        if transport_types is not None and len(transport_types) > 0:
            df_sample = df_sample[df_sample['transport_type'].isin(transport_types)]

        return df_sample

    def get_filtered_data(self, route_ids=None, hours=None, transport_types=None, sample_size=None):
        """
        ⚠️ LEGACY: Filtre les données brutes (éviter si possible, utiliser les agrégations)

        Cette méthode est conservée pour compatibilité mais est LENTE sur 1.5M lignes.
        Préférer get_hourly_stats() ou get_geo_sample() selon le besoin.

        Args:
            route_ids: Liste des IDs de lignes à inclure (None = toutes)
            hours: Liste des heures à inclure (None = toutes)
            transport_types: Liste des types de transport à inclure (None = tous)
            sample_size: Si spécifié, échantillonne N lignes aléatoires (plus rapide)

        Returns:
            DataFrame filtré
        """
        if self.df_clean is None:
            raise ValueError("Les données doivent être nettoyées avant filtrage")

        # Si échantillonnage demandé, partir d'un échantillon
        if sample_size is not None:
            df_filtered = self.df_clean.sample(n=min(sample_size, len(self.df_clean)), random_state=42)
        else:
            df_filtered = self.df_clean.copy()

        if route_ids is not None and len(route_ids) > 0:
            df_filtered = df_filtered[df_filtered['route_id'].isin(route_ids)]

        if hours is not None and len(hours) > 0:
            df_filtered = df_filtered[df_filtered['hour'].isin(hours)]

        if transport_types is not None and len(transport_types) > 0:
            df_filtered = df_filtered[df_filtered['transport_type'].isin(transport_types)]

        return df_filtered


# Fonction utilitaire pour instancier et charger
def load_transit_data(data_path: str = "../tp/data/transit_delays.csv"):
    """
    Charge et nettoie les données de transit

    Args:
        data_path: Chemin vers le fichier CSV

    Returns:
        Tuple (DataLoader, DataFrame nettoyé)
    """
    loader = DataLoader(data_path)
    loader.load_data()
    df_clean = loader.clean_data()
    return loader, df_clean


if __name__ == "__main__":
    # Test du module
    loader, df = load_transit_data()
    stats = loader.get_summary_stats()

    print("\n📊 STATISTIQUES RÉSUMÉES:")
    print("=" * 60)
    print(f"Total observations: {stats['total_obs']:,}")
    print(f"Retard moyen: {stats['mean_delay']:.2f} min")
    print(f"Retard médian: {stats['median_delay']:.2f} min")
    print(f"% à l'heure (±1 min): {stats['ontime_pct']:.1f}%")
    print(f"Lignes uniques: {stats['unique_lines']}")
    print(f"Véhicules uniques: {stats['unique_vehicles']}")
