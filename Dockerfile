# Base image 
FROM python:3.9


# Diretorio em que vamos trabalhar
WORKDIR /app

# Variaveis de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instalando dependencias pro SQLalchemy

RUN apt-get update \
	&& apt-get install -y --no-install-recommends gcc libpq-dev \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/*

# Instalar dependencias do python
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copiar codigo pro container
COPY . /app/

# Comando pra rodar a aplicacao
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]