# Use a imagem oficial do Python como base
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de dependências (COM CAMINHO CORRIGIDO)
COPY backend/requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código (COM CAMINHO CORRIGIDO)
COPY backend/ .

# Expõe a porta que a API do FastAPI vai usar
EXPOSE 8000

# Comando para iniciar o servidor Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]