FROM python:3.10-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de dependências para o container
COPY .docker/python/requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Mantém o container rodando para que possamos entrar nele
CMD ["tail", "-f", "/dev/null"]