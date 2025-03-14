#!/bin/bash

# Variables
RESOURCE_GROUP="kabdelmalekRG"
CONTAINER_NAME="khadija-fastapi"
ACR_NAME="kabdelmalekregistry"
ACR_IMAGE="fastapi-app:latest"
ACR_URL="$ACR_NAME.azurecr.io"
CPU="1"
MEMORY="2"
PORT=8000
IP_ADDRESS="Public"
DNS_LABEL="khad-fastapi"
OS_TYPE="Linux"

# Connexion et build
echo "Connexion au registre ACR..."
az acr login --name $ACR_NAME

echo "Construction de l'image Docker..."
docker build --platform linux/amd64 -t $ACR_URL/$ACR_IMAGE .

echo "Push de l'image vers ACR..."
docker push $ACR_URL/$ACR_IMAGE

# Récupération des identifiants ACR
echo "Récupération des identifiants ACR..."
ACR_USERNAME=$(az acr credential show --name $ACR_NAME --query "username" -o tsv)
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query "passwords[0].value" -o tsv)

# Suppression du conteneur existant
echo "Suppression du conteneur existant..."
az container delete --name $CONTAINER_NAME --resource-group $RESOURCE_GROUP --yes

# Chargement des variables d'environnement
echo "Chargement des variables d'environnement..."
source .env

# Déploiement du conteneur
echo "Déploiement du nouveau conteneur..."
az container create \
  --name $CONTAINER_NAME \
  --resource-group $RESOURCE_GROUP \
  --location "France Central" \
  --image $ACR_URL/$ACR_IMAGE \
  --cpu $CPU \
  --memory $MEMORY \
  --registry-login-server $ACR_URL \
  --registry-username $ACR_USERNAME \
  --registry-password $ACR_PASSWORD \
  --ports 8000 \
  --ip-address $IP_ADDRESS \
  --os-type $OS_TYPE \
  --dns-name-label $DNS_LABEL \
  --environment-variables \
    SECRET_KEY="$SECRET_KEY" \
    ALGORITHM="$ALGORITHM" \
    ACCESS_TOKEN_EXPIRE_MINUTES="$ACCESS_TOKEN_EXPIRE_MINUTES" \
    DATABASE_NAME="$DATABASE_NAME" \
    DATABASE_USERNAME="$DATABASE_USERNAME" \
    DATABASE_PASSWORD="$DATABASE_PASSWORD" \
    HOST_NAME="$HOST_NAME" \
    PORT="$PORT" \
    DATABASE_URL="$DATABASE_URL"

# Configuration du pare-feu SQL
echo "Configuration du pare-feu SQL..."
az sql server firewall-rule create \
    --resource-group kabdelmalekRG \
    --server kabdelmaleksqlserver \
    --name "AllowAzureServices" \
    --start-ip-address 0.0.0.0 \
    --end-ip-address 0.0.0.0

# Ajout de l'IP du conteneur
CONTAINER_IP=$(az container show \
    --resource-group $RESOURCE_GROUP \
    --name $CONTAINER_NAME \
    --query ipAddress.ip \
    --output tsv)

echo "Ajout de l'IP du conteneur aux règles du pare-feu..."
az sql server firewall-rule create \
    --resource-group kabdelmalekRG \
    --server kabdelmaleksqlserver \
    --name "AllowContainerIP" \
    --start-ip-address $CONTAINER_IP \
    --end-ip-address $CONTAINER_IP

# Affichage des informations
CONTAINER_URL=$(az container show \
    --resource-group $RESOURCE_GROUP \
    --name $CONTAINER_NAME \
    --query ipAddress.fqdn \
    --output tsv)

echo "Déploiement terminé avec succès!"
echo "URL de l'application: http://$CONTAINER_URL:8000"
echo "Documentation Swagger: http://$CONTAINER_URL:8000/docs"

# Affichage des logs
echo "Logs du conteneur (Ctrl+C pour quitter):"
az container logs --resource-group $RESOURCE_GROUP --name $CONTAINER_NAME --follow