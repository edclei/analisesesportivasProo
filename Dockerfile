# ============================
#  AnalisesEsportivasPro — Backend
#  Deploy Railway / FastAPI / Python
# ============================

FROM python:3.11

# Pasta de trabalho no container
WORKDIR /app

# Instala dependências
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo conteúdo do backend
COPY backend .

# Porta exposta pro Railway
EXPOSE 8000

# Inicializa servidor FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
