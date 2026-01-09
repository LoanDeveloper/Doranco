"""
Script de test pour vérifier que l'application Dash se charge correctement
"""
import sys

try:
    print("🧪 Test 1: Import des modules...")
    import dash
    from dash import dcc, html
    import plotly.express as px
    import plotly.graph_objects as go
    import pandas as pd
    import numpy as np
    print("   ✅ Tous les modules importés avec succès")

    print("\n🧪 Test 2: Chargement du data_loader...")
    from data_loader import load_transit_data
    print("   ✅ Module data_loader importé")

    print("\n🧪 Test 3: Chargement des données...")
    loader, df_clean = load_transit_data()
    print(f"   ✅ {len(df_clean):,} observations chargées")

    print("\n🧪 Test 4: Calcul des statistiques...")
    stats = loader.get_summary_stats()
    print(f"   ✅ Retard moyen: {stats['mean_delay']:.2f} min")
    print(f"   ✅ {stats['unique_lines']} lignes analysées")

    print("\n🧪 Test 5: Test des agrégations...")
    line_stats = loader.get_line_stats()
    print(f"   ✅ {len(line_stats)} lignes avec statistiques")

    hourly_stats = loader.get_hourly_stats()
    print(f"   ✅ {len(hourly_stats)} heures avec statistiques")

    heatmap_data = loader.get_heatmap_data(top_n_lines=10)
    print(f"   ✅ Heatmap {heatmap_data.shape[0]}x{heatmap_data.shape[1]} générée")

    print("\n🧪 Test 6: Test des filtres...")
    df_filtered = loader.get_filtered_data(
        route_ids=None,
        hours=[8, 9, 10],
        transport_types=['Bus']
    )
    print(f"   ✅ {len(df_filtered):,} observations après filtrage")

    print("\n🧪 Test 7: Création d'un graphique Plotly...")
    fig = px.histogram(df_clean.sample(1000), x='delay_minutes', nbins=50)
    print("   ✅ Graphique Plotly créé avec succès")

    print("\n" + "=" * 60)
    print("✅ TOUS LES TESTS SONT PASSÉS!")
    print("=" * 60)
    print("\n💡 L'application est prête à être lancée avec:")
    print("   python app.py")
    print("\n📚 Consultez le README.md pour plus d'informations")

except Exception as e:
    print(f"\n❌ ERREUR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
