#!/bin/bash

# Script de lancement rapide du dashboard Nice Traffic Watch
# Usage: ./run.sh

echo "🚀 Lancement du Dashboard Nice Traffic Watch..."
echo ""

# Vérifier que nous sommes dans le bon répertoire
if [ ! -f "app.py" ]; then
    echo "❌ Erreur: app.py non trouvé"
    echo "   Assurez-vous d'être dans le répertoire tp2/"
    exit 1
fi

# Activer l'environnement virtuel
if [ -d ".venv" ]; then
    echo "✅ Activation de l'environnement virtuel..."
    source .venv/bin/activate
else
    echo "❌ Erreur: Environnement virtuel .venv non trouvé"
    echo "   Créez-le avec: python3 -m venv .venv"
    exit 1
fi

# Vérifier que les dépendances sont installées
echo "✅ Vérification des dépendances..."
python -c "import dash, plotly, pandas, numpy" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Installation des dépendances manquantes..."
    pip install --quiet dash plotly pandas numpy
fi

# Lancer l'application
echo "✅ Lancement de l'application..."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🌐 Dashboard accessible sur: http://127.0.0.1:8050/"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "💡 Appuyez sur Ctrl+C pour arrêter le serveur"
echo ""

python app.py
