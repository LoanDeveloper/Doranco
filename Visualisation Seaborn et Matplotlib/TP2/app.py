"""
Nice Traffic Watch - Dashboard Interactif
Application Dash pour le monitoring des retards du réseau Lignes d'Azur
"""

import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from data_loader import load_transit_data

# Initialisation de l'application Dash
app = dash.Dash(__name__, title="Nice Traffic Watch")

# Chargement des données
print("🚀 Démarrage de l'application Nice Traffic Watch...")
loader, df_clean = load_transit_data()
stats = loader.get_summary_stats()

# Configuration des couleurs
COLORS = {
    'background': '#f8f9fa',
    'card': '#ffffff',
    'primary': '#0066cc',
    'success': '#28a745',
    'warning': '#ffc107',
    'danger': '#dc3545',
    'text': '#212529',
    'border': '#dee2e6'
}

# Palette divergente pour les retards (vert=avance, rouge=retard)
DELAY_COLORSCALE = [
    [0.0, '#1a9850'],   # Vert foncé (très en avance)
    [0.25, '#91cf60'],  # Vert clair
    [0.5, '#ffffbf'],   # Jaune (à l'heure)
    [0.75, '#fc8d59'],  # Orange
    [1.0, '#d73027']    # Rouge (très en retard)
]

# Layout de l'application
app.layout = html.Div(style={'backgroundColor': COLORS['background'], 'minHeight': '100vh'}, children=[

    # Header
    html.Div(style={
        'backgroundColor': COLORS['primary'],
        'color': 'white',
        'padding': '30px',
        'marginBottom': '30px',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
    }, children=[
        html.H1('🚌 Nice Traffic Watch', style={'margin': '0', 'fontSize': '36px'}),
        html.P('Dashboard Interactif de Monitoring des Retards - Réseau Lignes d\'Azur',
               style={'margin': '10px 0 0 0', 'fontSize': '16px', 'opacity': '0.9'})
    ]),

    # Section des KPIs
    html.Div(style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '0 20px'}, children=[

        # Cartes de statistiques
        html.Div(style={'display': 'grid', 'gridTemplateColumns': 'repeat(auto-fit, minmax(200px, 1fr))',
                        'gap': '20px', 'marginBottom': '30px'}, children=[

            # KPI 1: Retard Moyen
            html.Div(style={
                'backgroundColor': COLORS['card'],
                'padding': '20px',
                'borderRadius': '8px',
                'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                'border': f'2px solid {COLORS["danger"] if stats["mean_delay"] > 2 else COLORS["success"]}'
            }, children=[
                html.H3('Retard Moyen', style={'margin': '0 0 10px 0', 'fontSize': '14px', 'color': '#666'}),
                html.H2(f'{stats["mean_delay"]:.2f} min',
                        style={'margin': '0', 'color': COLORS['danger'] if stats["mean_delay"] > 2 else COLORS['success']})
            ]),

            # KPI 2: % à l'heure
            html.Div(style={
                'backgroundColor': COLORS['card'],
                'padding': '20px',
                'borderRadius': '8px',
                'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
            }, children=[
                html.H3('À l\'heure (±1 min)', style={'margin': '0 0 10px 0', 'fontSize': '14px', 'color': '#666'}),
                html.H2(f'{stats["ontime_pct"]:.1f}%', style={'margin': '0', 'color': COLORS['primary']})
            ]),

            # KPI 3: Observations
            html.Div(style={
                'backgroundColor': COLORS['card'],
                'padding': '20px',
                'borderRadius': '8px',
                'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
            }, children=[
                html.H3('Observations', style={'margin': '0 0 10px 0', 'fontSize': '14px', 'color': '#666'}),
                html.H2(f'{stats["total_obs"]:,}', style={'margin': '0', 'color': COLORS['primary']})
            ]),

            # KPI 4: Lignes
            html.Div(style={
                'backgroundColor': COLORS['card'],
                'padding': '20px',
                'borderRadius': '8px',
                'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
            }, children=[
                html.H3('Lignes Analysées', style={'margin': '0 0 10px 0', 'fontSize': '14px', 'color': '#666'}),
                html.H2(f'{stats["unique_lines"]}', style={'margin': '0', 'color': COLORS['primary']})
            ]),

            # KPI 5: % en retard
            html.Div(style={
                'backgroundColor': COLORS['card'],
                'padding': '20px',
                'borderRadius': '8px',
                'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
            }, children=[
                html.H3('En retard (>2 min)', style={'margin': '0 0 10px 0', 'fontSize': '14px', 'color': '#666'}),
                html.H2(f'{stats["late_pct"]:.1f}%', style={'margin': '0', 'color': COLORS['danger']})
            ]),
        ]),

        # Section des filtres
        html.Div(style={
            'backgroundColor': COLORS['card'],
            'padding': '20px',
            'borderRadius': '8px',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
            'marginBottom': '30px'
        }, children=[
            html.H3('🔍 Filtres Interactifs', style={'marginTop': '0', 'color': COLORS['primary']}),

            html.Div(style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr 1fr', 'gap': '20px'}, children=[

                # Filtre par type de transport
                html.Div(children=[
                    html.Label('Type de Transport:', style={'fontWeight': 'bold', 'marginBottom': '5px', 'display': 'block'}),
                    dcc.Checklist(
                        id='transport-filter',
                        options=[
                            {'label': ' Bus', 'value': 'Bus'},
                            {'label': ' Tram', 'value': 'Tram'}
                        ],
                        value=['Bus', 'Tram'],
                        style={'display': 'flex', 'gap': '15px'}
                    )
                ]),

                # Filtre par heure
                html.Div(children=[
                    html.Label('Plage Horaire:', style={'fontWeight': 'bold', 'marginBottom': '5px', 'display': 'block'}),
                    dcc.RangeSlider(
                        id='hour-filter',
                        min=0,
                        max=23,
                        step=1,
                        marks={i: f'{i:02d}h' for i in range(0, 24, 3)},
                        value=[0, 23],
                        tooltip={"placement": "bottom", "always_visible": False}
                    )
                ]),

                # Filtre par nombre de lignes
                html.Div(children=[
                    html.Label('Top N Lignes (Hit Parade):', style={'fontWeight': 'bold', 'marginBottom': '5px', 'display': 'block'}),
                    dcc.Slider(
                        id='top-lines-filter',
                        min=5,
                        max=30,
                        step=5,
                        marks={i: str(i) for i in range(5, 35, 5)},
                        value=15,
                        tooltip={"placement": "bottom", "always_visible": True}
                    )
                ]),
            ]),

            html.Div(style={'marginTop': '15px', 'textAlign': 'center'}, children=[
                html.Button('🔄 Rafraîchir les données', id='refresh-button', n_clicks=0, style={
                    'padding': '10px 30px',
                    'backgroundColor': COLORS['primary'],
                    'color': 'white',
                    'border': 'none',
                    'borderRadius': '5px',
                    'cursor': 'pointer',
                    'fontSize': '14px',
                    'fontWeight': 'bold'
                })
            ])
        ]),

        # Onglets pour les visualisations
        dcc.Tabs(id='tabs', value='tab-overview', children=[

            # Onglet 1: Vue d'ensemble
            dcc.Tab(label='📊 Vue d\'Ensemble', value='tab-overview', children=[
                html.Div(style={'padding': '20px'}, children=[

                    # Graphique 1 & 2: Distribution des retards
                    html.Div(style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '20px', 'marginBottom': '20px'}, children=[
                        html.Div(style={'backgroundColor': COLORS['card'], 'padding': '20px', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}, children=[
                            dcc.Graph(id='graph-distribution')
                        ]),
                        html.Div(style={'backgroundColor': COLORS['card'], 'padding': '20px', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}, children=[
                            dcc.Graph(id='graph-violin')
                        ]),
                    ]),

                    # Graphique 3: Hit Parade des lignes
                    html.Div(style={'backgroundColor': COLORS['card'], 'padding': '20px', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'marginBottom': '20px'}, children=[
                        dcc.Graph(id='graph-hit-parade')
                    ]),
                ])
            ]),

            # Onglet 2: Analyse Temporelle
            dcc.Tab(label='⏰ Analyse Temporelle', value='tab-temporal', children=[
                html.Div(style={'padding': '20px'}, children=[

                    # Graphique 4: Évolution horaire
                    html.Div(style={'backgroundColor': COLORS['card'], 'padding': '20px', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'marginBottom': '20px'}, children=[
                        dcc.Graph(id='graph-hourly')
                    ]),

                    # Graphique 5: Heatmap
                    html.Div(style={'backgroundColor': COLORS['card'], 'padding': '20px', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}, children=[
                        dcc.Graph(id='graph-heatmap')
                    ]),
                ])
            ]),

            # Onglet 3: Comparaison & Géographie
            dcc.Tab(label='🗺️ Comparaison & Carte', value='tab-comparison', children=[
                html.Div(style={'padding': '20px'}, children=[

                    # Graphique 6: Bus vs Tram
                    html.Div(style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '20px', 'marginBottom': '20px'}, children=[
                        html.Div(style={'backgroundColor': COLORS['card'], 'padding': '20px', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}, children=[
                            dcc.Graph(id='graph-boxplot')
                        ]),
                        html.Div(style={'backgroundColor': COLORS['card'], 'padding': '20px', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}, children=[
                            dcc.Graph(id='graph-violin-compare')
                        ]),
                    ]),

                    # Graphique 7: Carte géographique
                    html.Div(style={'backgroundColor': COLORS['card'], 'padding': '20px', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}, children=[
                        dcc.Graph(id='graph-map')
                    ]),
                ])
            ]),
        ]),

        # Footer
        html.Div(style={
            'textAlign': 'center',
            'padding': '30px',
            'color': '#666',
            'marginTop': '30px'
        }, children=[
            html.P('📊 Nice Traffic Watch - Dashboard Interactif avec Dash & Plotly'),
            html.P(f'Données: {stats["start_time"]} → {stats["end_time"]}'),
            html.P('Créé avec ❤️ pour le TP Visualisation - Doranco', style={'fontSize': '12px'})
        ])
    ])
])


# Callbacks pour mettre à jour les graphiques
@app.callback(
    [Output('graph-distribution', 'figure'),
     Output('graph-violin', 'figure'),
     Output('graph-hit-parade', 'figure'),
     Output('graph-hourly', 'figure'),
     Output('graph-heatmap', 'figure'),
     Output('graph-boxplot', 'figure'),
     Output('graph-violin-compare', 'figure'),
     Output('graph-map', 'figure')],
    [Input('transport-filter', 'value'),
     Input('hour-filter', 'value'),
     Input('top-lines-filter', 'value'),
     Input('refresh-button', 'n_clicks')]
)
def update_graphs(transport_types, hour_range, top_n_lines, n_clicks):
    """
    🚀 OPTIMISÉ: Mise à jour de tous les graphiques en fonction des filtres
    Utilise les agrégations pré-calculées pour des performances instantanées
    """

    # Paramètres de filtrage
    hours_list = list(range(hour_range[0], hour_range[1] + 1))

    # ⚡ Échantillon optimisé pour les distributions (10k points au lieu de 1.5M)
    df_sample = loader.get_filtered_data(
        route_ids=None,
        hours=hours_list,
        transport_types=transport_types,
        sample_size=10000  # 150x plus rapide !
    )

    # ==================== GRAPHIQUE 1: Distribution (Histogramme) ====================
    fig_dist = px.histogram(
        df_sample,
        x='delay_minutes',
        nbins=50,
        title='Distribution des Retards (échantillon 10k)',
        labels={'delay_minutes': 'Retard (minutes)', 'count': 'Fréquence'},
        color_discrete_sequence=['#0066cc']
    )

    # Ajouter la ligne à l'heure
    fig_dist.add_vline(x=0, line_dash="dash", line_color="red", annotation_text="À l'heure")
    fig_dist.add_vline(x=df_sample['delay_minutes'].mean(), line_dash="dash", line_color="orange",
                       annotation_text=f"Moyenne: {df_sample['delay_minutes'].mean():.1f} min")

    fig_dist.update_layout(
        template='plotly_white',
        hovermode='x unified',
        showlegend=False
    )

    # ==================== GRAPHIQUE 2: Violin Plot ====================
    fig_violin = go.Figure()

    fig_violin.add_trace(go.Violin(
        y=df_sample['delay_minutes'],
        name='Retards',
        box_visible=True,
        meanline_visible=True,
        fillcolor='lightblue',
        opacity=0.6,
        line_color='black'
    ))

    fig_violin.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="À l'heure")

    fig_violin.update_layout(
        title='Densité de Probabilité des Retards (échantillon 10k)',
        yaxis_title='Retard (minutes)',
        template='plotly_white',
        showlegend=False
    )

    # ==================== GRAPHIQUE 3: Hit Parade des Lignes ====================
    line_stats = loader.get_line_stats(min_observations=50)
    top_worst = line_stats.nlargest(top_n_lines, 'mean_delay')

    # Couleurs divergentes
    colors = ['#d73027' if x > 2 else '#fee08b' if x > 0 else '#1a9850' for x in top_worst['mean_delay']]

    fig_hitparade = go.Figure(go.Bar(
        y=[f"Ligne {r}" for r in top_worst['route_id']],
        x=top_worst['mean_delay'],
        orientation='h',
        marker=dict(color=colors, line=dict(color='black', width=1)),
        text=[f"{val:.1f} min" for val in top_worst['mean_delay']],
        textposition='outside'
    ))

    fig_hitparade.add_vline(x=0, line_dash="solid", line_color="black", line_width=2)

    fig_hitparade.update_layout(
        title=f'Top {top_n_lines} des Lignes avec les Plus Grands Retards Moyens',
        xaxis_title='Retard moyen (minutes)',
        yaxis_title='',
        template='plotly_white',
        height=max(400, top_n_lines * 30),
        showlegend=False
    )

    # ==================== GRAPHIQUE 4: Évolution Horaire ====================
    # ⚡ Utiliser les agrégations pré-calculées (100x plus rapide)
    hourly_stats = loader.get_hourly_stats(
        transport_types=transport_types,
        hours=hours_list
    )

    fig_hourly = go.Figure()

    # Zone d'intervalle de confiance
    fig_hourly.add_trace(go.Scatter(
        x=hourly_stats['hour'].tolist() + hourly_stats['hour'].tolist()[::-1],
        y=(hourly_stats['mean_delay'] + hourly_stats['ci']).tolist() +
          (hourly_stats['mean_delay'] - hourly_stats['ci']).tolist()[::-1],
        fill='toself',
        fillcolor='rgba(0,102,204,0.2)',
        line=dict(color='rgba(255,255,255,0)'),
        name='IC 95%',
        showlegend=True
    ))

    # Ligne principale
    fig_hourly.add_trace(go.Scatter(
        x=hourly_stats['hour'],
        y=hourly_stats['mean_delay'],
        mode='lines+markers',
        name='Retard moyen',
        line=dict(color='#0066cc', width=3),
        marker=dict(size=8)
    ))

    fig_hourly.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="À l'heure")

    fig_hourly.update_layout(
        title='Évolution du Retard Moyen au Cours de la Journée',
        xaxis_title='Heure de la journée',
        yaxis_title='Retard moyen (minutes)',
        template='plotly_white',
        hovermode='x unified',
        xaxis=dict(tickmode='linear', tick0=0, dtick=1, ticksuffix='h')
    )

    # ==================== GRAPHIQUE 5: Heatmap ====================
    heatmap_data = loader.get_heatmap_data(top_n_lines=20)

    fig_heatmap = go.Figure(go.Heatmap(
        z=heatmap_data.values,
        x=[f'{h:02d}h' for h in heatmap_data.columns],
        y=[f'Ligne {r}' for r in heatmap_data.index],
        colorscale='RdYlGn_r',
        zmid=0,
        text=np.round(heatmap_data.values, 1),
        texttemplate='%{text}',
        textfont={"size": 10},
        colorbar=dict(title="Retard (min)")
    ))

    fig_heatmap.update_layout(
        title='Heatmap des Retards : 20 Lignes Principales × Heures de la Journée',
        xaxis_title='Heure de la journée',
        yaxis_title='Ligne',
        template='plotly_white',
        height=600
    )

    # ==================== GRAPHIQUE 6 & 7: Bus vs Tram ====================
    if len(df_sample['transport_type'].unique()) >= 2:
        # Boxplot
        fig_boxplot = px.box(
            df_sample,
            x='transport_type',
            y='delay_minutes',
            color='transport_type',
            title='Distribution des Retards par Type de Transport (Boxplot)',
            labels={'delay_minutes': 'Retard (minutes)', 'transport_type': 'Type de Transport'},
            color_discrete_map={'Bus': '#ff7f50', 'Tram': '#87ceeb'}
        )
        fig_boxplot.add_hline(y=0, line_dash="dash", line_color="red")
        fig_boxplot.update_layout(template='plotly_white', showlegend=False)

        # Violin plot
        fig_violin_compare = px.violin(
            df_sample,
            x='transport_type',
            y='delay_minutes',
            color='transport_type',
            title='Distribution des Retards par Type de Transport (Violin)',
            labels={'delay_minutes': 'Retard (minutes)', 'transport_type': 'Type de Transport'},
            color_discrete_map={'Bus': '#ff7f50', 'Tram': '#87ceeb'},
            box=True
        )
        fig_violin_compare.add_hline(y=0, line_dash="dash", line_color="red")
        fig_violin_compare.update_layout(template='plotly_white', showlegend=False)
    else:
        # Si un seul type de transport
        fig_boxplot = px.box(
            df_sample,
            y='delay_minutes',
            title=f'Distribution des Retards - {df_sample["transport_type"].iloc[0]}',
            labels={'delay_minutes': 'Retard (minutes)'}
        )
        fig_boxplot.add_hline(y=0, line_dash="dash", line_color="red")
        fig_boxplot.update_layout(template='plotly_white')

        fig_violin_compare = px.violin(
            df_sample,
            y='delay_minutes',
            title=f'Distribution des Retards - {df_sample["transport_type"].iloc[0]}',
            labels={'delay_minutes': 'Retard (minutes)'},
            box=True
        )
        fig_violin_compare.add_hline(y=0, line_dash="dash", line_color="red")
        fig_violin_compare.update_layout(template='plotly_white')

    # ==================== GRAPHIQUE 8: Carte Géographique ====================
    # ⚡ Utiliser l'échantillon géographique pré-calculé (instantané)
    df_geo = loader.get_geo_sample(transport_types=transport_types)

    # ✅ FIXÉ: scatter_map au lieu de scatter_mapbox (deprecated)
    fig_map = px.scatter_map(
        df_geo,
        lat='latitude',
        lon='longitude',
        color='delay_minutes',
        size=abs(df_geo['delay_minutes']) + 1,
        color_continuous_scale='RdYlGn_r',
        range_color=[-10, 10],
        zoom=11,
        height=600,
        title='Carte des Retards à Nice (5k points pré-échantillonnés)',
        labels={'delay_minutes': 'Retard (min)'},
        hover_data={'route_id': True, 'delay_minutes': ':.1f', 'latitude': ':.4f', 'longitude': ':.4f'}
    )

    fig_map.update_layout(
        template='plotly_white'
    )

    return fig_dist, fig_violin, fig_hitparade, fig_hourly, fig_heatmap, fig_boxplot, fig_violin_compare, fig_map


# Lancement de l'application
if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("✅ Application Nice Traffic Watch démarrée avec succès!")
    print("🌐 Accédez au dashboard: http://127.0.0.1:8050/")
    print("=" * 60 + "\n")
    app.run(debug=True, host='127.0.0.1', port=8050)
