# BASE API FASTAPI
FROM python:3.11

WORKDIR /app

# Copia arquivos do backend
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

EXPOSE 8000

# Comando que sobe a API online
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
