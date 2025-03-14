FROM --platform=linux/amd64 python:3.11-slim

WORKDIR /app

# Installation des dépendances de base
RUN apt-get update && apt-get install -y \
    curl \
    gnupg2 \
    gcc \
    g++ \
    python3-dev \
    unixodbc \
    unixodbc-dev \
    apt-transport-https \
    && rm -rf /var/lib/apt/lists/*

# Configuration et installation de SQL Server ODBC
RUN curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /usr/share/keyrings/microsoft-archive-keyring.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft-archive-keyring.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y \
        msodbcsql18 \
        unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*

# Vérification de l'installation
RUN odbcinst -j

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Configuration de l'entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN apt-get update && apt-get install -y dos2unix && rm -rf /var/lib/apt/lists/*
RUN dos2unix /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]