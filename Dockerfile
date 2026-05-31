FROM python:3.11-slim

#evita geração de arquivos .pyc
ENV PYTHONDONTWRITEBYTECODE=1

#exibição logs
ENV PYTHONUNBUFFERED=1

WORKDIR /app

#dependências do opencv
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

#instalação dependências python
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

#copia todo o projeto
COPY . .

#porta utilizada pela aplicação
EXPOSE 8000

#inicializacao da API
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000}"]