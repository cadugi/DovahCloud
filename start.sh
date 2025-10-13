#!/bin/bash

# Inicia backend Flask y frontend React/Vite en paralelo
# Puerto 4238 -> Flask, Puerto 4237 -> Vite

# --- Backend ---
echo "🚀 Iniciando backend Flask en puerto 4238..."
pip install -r requirements.txt >/dev/null 2>&1
# exporta las variables de entorno y arranca
export FLASK_APP=app.py
export FLASK_DEBUG=1
python - <<'PYCODE' &
from app import app
app.run(host="0.0.0.0", port=4238, debug=True)
PYCODE

# --- Frontend ---
echo "🚀 Iniciando frontend Vite en puerto 4237..."
cd frontend || exit 1
npm install >/dev/null 2>&1
npm run dev -- --host 0.0.0.0 --port 4237 &

# --- Espera y muestra info ---
cd ..
echo ""
echo "✅ Todo arrancado:"
echo "   - Backend (Flask): http://localhost:4238"
echo "   - Frontend (React/Vite): http://localhost:4237"
echo ""
echo "⚠️ En Codespaces abre la pestaña 'Ports' y publica los puertos 4238 y 4237 para acceder a estas URLs públicas."

# Mantener script vivo (para que no se cierre)
wait
