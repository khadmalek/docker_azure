# Projet de Prêt Bancaire sur Azure et Docker

Application de gestion de prêts bancaires combinant une API FastAPI et une interface Django, déployée sur Azure et Docker. Ce projet utilise Docker pour la conteneurisation et Azure SQL Database pour le stockage des données.

![Azure](https://img.shields.io/badge/Azure-0078D4?style=flat&logo=microsoft-azure&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=flat&logo=django&logoColor=white)
![SQL Server](https://img.shields.io/badge/SQL%20Server-CC2927?style=flat&logo=microsoft-sql-server&logoColor=white)

## Architecture du Projet

### Services Azure
- **Azure Container Instance (ACI)**
  - Conteneur FastAPI pour l'API
  - Conteneur Django pour l'interface web
- **Azure SQL Database**

### Services Docker
- **Images Docker personnalisées** pour FastAPI et Django
- **Gestion des conteneurs via Docker CLI**
- **Volumes Docker** pour la persistance des données en local

## Déploiement Docker en Local

1. **Installer Docker**
   - Télécharger et installer [Docker Desktop](https://www.docker.com/products/docker-desktop/)
   
2. **Créer une image Docker pour FastAPI**
   - Placer un `Dockerfile` dans le répertoire de l'API FastAPI et construire l'image :
     
   ```sh
   docker build -t fastapi-app ./fastapi/
   ```

3. **Créer une image Docker pour Django**
   - Placer un `Dockerfile` dans le répertoire Django et construire l'image :
     
   ```sh
   docker build -t django-app ./django/
   ```

4. **Lancer les conteneurs**
   
   ```sh
   docker run -d -p 8000:8000 --name fastapi-container fastapi-app
   docker run -d -p 8001:8000 --name django-container django-app
   ```

5. **Accéder aux services**
   - FastAPI : `http://localhost:8000/docs`
   - Django : `http://localhost:8001/admin`

## Déploiement sur Azure

### Niveau 1 : Déploiement via le Portail Azure
1. Création d'une base de données SQL Azure
2. Configuration du pare-feu et des règles d'accès
3. Déploiement manuel des conteneurs via Azure Container Instances

### Niveau 2 : Automatisation avec Script Bash
1. Développement de scripts d'automatisation (`deploy_fastapi.sh` et `deploy_django.sh`)
2. Utilisation d'Azure CLI pour le déploiement automatisé

### [Bonus] Niveau 3 : Infrastructure as Code
- Configuration avec Terraform (non implémenté dans cette version)

## Prérequis

- Compte Azure avec abonnement actif
- Azure CLI installé localement
- Docker Desktop
- Python 3.11+


## Sécurité
- Configuration du pare-feu Azure SQL
- Gestion sécurisée des secrets via fichiers `.env`
- Authentification et autorisation des conteneurs
