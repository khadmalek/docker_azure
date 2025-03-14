#!/bin/bash

# Variables
RESOURCE_GROUP="kabdelmalekRG"
CONTAINER_NAME="khadija-django"
ACR_NAME="kabdelmalekregistry"
ACR_IMAGE="django-ubuntu:latest"
ACR_URL="$ACR_NAME.azurecr.io"

# Variables pour SQL Server
SQL_SERVER="kabdelmalekserver.database.windows.net"
SQL_DATABASE="kabdelmalekdb"
SQL_USERNAME="kabdelmalek"
SQL_PASSWORD="Khadija@2024"

# Connexion au registre ACR
echo "Connexion au registre ACR..."
az acr login --name $ACR_NAME

# Création d'un Dockerfile basé sur Ubuntu
cat > Dockerfile << EOF
FROM ubuntu:22.04

# Éviter les interactions pendant l'installation
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Installation des dépendances système
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    curl \
    gnupg \
    gcc \
    g++ \
    unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*

# Installation du pilote Microsoft ODBC pour SQL Server
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key adv --keyserver keyserver.ubuntu.com --recv-keys EB3E94ADBE1229CF \
    && curl https://packages.microsoft.com/config/ubuntu/22.04/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
    && rm -rf /var/lib/apt/lists/*

# Copier les fichiers requirements
COPY requirements.txt .

# Installation des dépendances Python
RUN pip3 install --no-cache-dir -r requirements.txt \
    && pip3 install --no-cache-dir pytz django-mssql-backend pyodbc gunicorn

# Copier le reste des fichiers
COPY . .

# Définir les variables d'environnement Python
ENV PYTHONPATH=/app
ENV DJANGO_SETTINGS_MODULE=pret_bancaire.pret_bancaire.settings

EXPOSE 8080

# Pour Django avec Gunicorn
CMD ["python3", "-m", "gunicorn", "--bind", "0.0.0.0:8080", "pret_bancaire.pret_bancaire.wsgi:application", "--env", "DJANGO_SETTINGS_MODULE=pret_bancaire.pret_bancaire.settings"]
EOF

# Construction de l'image Docker avec le Dockerfile
echo "Construction de l'image Docker..."
docker build --platform linux/amd64 -t $ACR_URL/$ACR_IMAGE .

# Push de l'image vers ACR
echo "Push de l'image vers ACR..."
docker push $ACR_URL/$ACR_IMAGE

# Récupération des identifiants ACR
echo "Récupération des identifiants ACR..."
ACR_USERNAME=$(az acr credential show --name $ACR_NAME --query "username" -o tsv)
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query "passwords[0].value" -o tsv)

# Suppression du conteneur existant s'il existe
echo "Suppression du conteneur existant..."
az container delete --name $CONTAINER_NAME --resource-group $RESOURCE_GROUP --yes || true

# Déploiement du nouveau conteneur
echo "Déploiement du nouveau conteneur..."
az container create \
  --resource-group $RESOURCE_GROUP \
  --name $CONTAINER_NAME \
  --image $ACR_URL/$ACR_IMAGE \
  --cpu 1 \
  --memory 1.5 \
  --registry-login-server $ACR_URL \
  --registry-username $ACR_USERNAME \
  --registry-password $ACR_PASSWORD \
  --ports 8080 \
  --ip-address Public \
  --dns-name-label khad-django \
  --os-type Linux \
  --environment-variables \
    DJANGO_SECRET_KEY="django-insecure-#u2atll*45j4v46!^9@%_))@aqzf94iafmibgl#^ctx1y@d=oq" \
    DEBUG="False" \
    ALLOWED_HOSTS="*,khad-django.francecentral.azurecontainer.io,khad-django.francecentral.azurecontainer.io:8080" \
    DATABASE_ENGINE="mssql" \
    DATABASE_NAME="$SQL_DATABASE" \
    DATABASE_USER="$SQL_USERNAME" \
    DATABASE_PASSWORD="$SQL_PASSWORD" \
    DATABASE_HOST="$SQL_SERVER" \
    DATABASE_PORT="1433" \
    DATABASE_OPTIONS_DRIVER="ODBC Driver 18 for SQL Server" \
    API_URL="http://khad-fastapi.francecentral.azurecontainer.io:8000" \
    ALGORITHM="HS256" \
    ACCESS_TOKEN_EXPIRE_MINUTES="30" \
    ROOT_URLCONF="pret_bancaire.pret_bancaire.urls"

# Vérifier l'état du déploiement
echo "Vérification de l'état du déploiement..."
sleep 10
DEPLOYMENT_STATUS=$(az container show --resource-group $RESOURCE_GROUP --name $CONTAINER_NAME --query "provisioningState" -o tsv 2>/dev/null)
echo "État du déploiement: $DEPLOYMENT_STATUS"

# Afficher l'URL du conteneur
echo "URL du conteneur:"
CONTAINER_URL=$(az container show --resource-group $RESOURCE_GROUP --name $CONTAINER_NAME --query "ipAddress.fqdn" -o tsv 2>/dev/null)
if [ -n "$CONTAINER_URL" ]; then
    echo "http://$CONTAINER_URL:8080"
else
    echo "Impossible de récupérer l'URL du conteneur."
    echo "Vérifiez l'état du déploiement avec: az container show --resource-group $RESOURCE_GROUP --name $CONTAINER_NAME"
fi

# Afficher les logs
echo "Logs du conteneur:"
az container logs --resource-group $RESOURCE_GROUP --name $CONTAINER_NAME || true

# Nettoyage
rm -f Dockerfile