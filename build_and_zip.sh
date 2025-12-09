#!/bin/bash

echo "🚀 INICIANDO BUILD COMPLETO DO ANALISESESPORTIVASPRO..."
sleep 1

############################################
# 1. VERIFICAÇÃO DE AMBIENTE
############################################
echo "🔎 Verificando dependências principais..."

if ! command -v python3 &>/dev/null; then
  echo "❌ Python3 não encontrado — instale antes de rodar o script"
  exit 1
fi

if ! command -v npm &>/dev/null; then
  echo "❌ Node/NPM não encontrados — instale antes de rodar o script"
  exit 1
fi

if ! command -v zip &>/dev/null; then
  echo "❌ zip não instalado — instale com:"
  echo "Ubuntu/Debian: sudo apt install zip"
  echo "Mac: brew install zip"
  exit 1
fi

############################################
# 2. BACKEND BUILD + ENV CHECK
############################################
echo "📌 PROCESSANDO BACKEND..."
cd backend || exit

if [ ! -f ".env" ]; then
  echo "⚠ Nenhum .env encontrado no backend — criando template..."
  cat <<EOF > .env.example
ODDS_API_KEY=
SPORTMONKS_KEY=
BOLTODDS_KEY=
SUPABASE_URL=
SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=
DATABASE_URL=
ENABLE_REAL_BETS=false
EOF

  echo "⚠ Preencha o .env com suas chaves em /backend/.env"
fi

echo "📦 Instalando dependências Python..."
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "▶ Testando backend..."
uvicorn main:app --port 8000 --timeout-keep-alive 5 &
SERVER_PID=$!
sleep 3
curl -s http://localhost:8000/api/health || echo "⚠ API não respondeu — revise erros."

kill $SERVER_PID
deactivate
cd ..

############################################
# 3. FRONTEND VITE BUILD
############################################
echo "🎨 PROCESSANDO FRONT-END..."
cd frontend || exit
npm install
npm run build
cd ..

############################################
# 4. GERAR ZIP FINAL
############################################
echo "📦 GERANDO ARQUIVO FINAL..."

zip -r AnalisesEsportivasPro_Final.zip . \
  -x "*/.git/*" \
  -x "*/.env" \
  -x "*/node_modules/*" \
  -x "backend/.venv/*" \
  -x "*.zip"

echo "🎉 ZIP GERADO COM SUCESSO!"
echo "🔽 Baixe: AnalisesEsportivasPro_Final.zip"
echo "--------------------------------------------"
echo "📍 Agora você pode:"
echo "1) subir no Railway"
echo "2) converter em APK"
echo "3) rodar localmente com segurança"
echo "--------------------------------------------"
