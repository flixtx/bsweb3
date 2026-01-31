FROM python:3.11-slim-bullseye

# Define o diretório de trabalho
WORKDIR /app

# Copia apenas os arquivos necessários para a instalação das dependências primeiro
# Isso aproveita o cache de camadas do Docker
COPY requirements.txt .

# Instala as dependências do Python
# Não precisamos do git se copiarmos os arquivos diretamente
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante dos arquivos do projeto para o contêiner
COPY . .

# Expõe a porta que a aplicação utiliza
EXPOSE 8080

# Comando para iniciar a aplicação
CMD ["uvicorn", "run:main_app", "--host", "0.0.0.0", "--port", "8080", "--workers", "1"]
