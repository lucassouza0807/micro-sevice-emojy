# Etapa 1: Construção da imagem
FROM python:3.10-slim AS builder

# Define o diretório de trabalho
WORKDIR /app

# Copia o arquivo de dependências
COPY requirements.txt .

# Cria o ambiente virtual
RUN python3 -m venv /env

# Ativa o ambiente virtual e instala as dependências
RUN /env/bin/pip install --no-cache-dir -r requirements.txt

# Copia o código-fonte para o container
COPY . .

# Etapa 2: Imagem final
FROM python:3.10-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia o ambiente virtual do container de build
COPY --from=builder /env /env

# Copia o código-fonte para o container final
COPY --from=builder /app /app

# Ativa o ambiente virtual ao rodar o container
ENV PATH="/env/bin:$PATH"

# Expõe a porta que o FastAPI usará
EXPOSE 8000

# Comando para rodar a aplicação FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
