# Use uma imagem oficial do Python como base
FROM python:3.9

# Defina o diretório de trabalho no container
WORKDIR /app

# Defina variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instale as dependências do sistema
RUN apt-get update \
	&& apt-get install -y --no-install-recommends gcc libpq-dev \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/*

# Instale as dependências do Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copie o código do projeto para o container
COPY . /app/

# Comando para rodar a aplicação
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
