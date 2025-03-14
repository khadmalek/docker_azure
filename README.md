# Projet de Prêt Bancaire sur Azure

Application de gestion de prêts bancaires combinant une API FastAPI et une interface Django, déployée sur Azure. Ce projet utilise Docker pour la conteneurisation et Azure SQL Database pour le stockage des données.

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
  - Serveur : kabdelmaleksqlserver
  - Base : bddjango
  - Région : France Central
  - Groupe de ressources : kabdelmalekRG
  - État : Paused
  - Délai de pause : 1 heure
  - Abonnement : Simplon - HDF - Roubaix - DEV IA P5 (116666)
  - ID d'abonnement : 72eb7803-e874-44cb-b6d9-33f2fa3eb88c
  - Premier point de restauration : 2025-03-12
  - Niveau tarifaire : Usage général

## Étapes du Projet

### Niveau 1 : Déploiement via le Portail Azure
1. Création d'une base de données SQL Azure
2. Configuration du pare-feu et des règles d'accès
3. Déploiement manuel des conteneurs via Azure Container Instances
4. Configuration des variables d'environnement

### Niveau 2 : Automatisation avec Script Bash
1. Développement de scripts d'automatisation (`deploy_fastapi.sh` et `deploy_django.sh`)
2. Utilisation d'Azure CLI pour le déploiement automatisé
3. Gestion sécurisée des secrets via fichiers `.env`

### [Bonus] Niveau 3 : Infrastructure as Code
- Configuration avec Terraform (non implémentée dans cette version)

## Structure des Dossiers

.
├── README.md.backup
├── docker_api
│   └── brief_FastAPI
│       ├── Dockerfile
│       ├── alembic.ini
│       ├── app
│       │   ├── __init__.py
│       │   ├── database.py
│       │   ├── endpoints
│       │   │   ├── __init__.py
│       │   │   ├── route_admin.py
│       │   │   ├── route_auth.py
│       │   │   └── route_loans.py
│       │   ├── ml.py
│       │   ├── modeles.py
│       │   ├── schemas.py
│       │   ├── test_connexion.py
│       │   └── utils.py
│       ├── best_cat_boost.tar.xz
│       ├── deploy_fastapi.sh
│       ├── entrypoint.sh
│       ├── main.py
│       ├── populate_db.py
│       ├── populate_db_sqlserver.py
│       └── requirements.txt
└── docker_django
    ├── appli_django
    │   ├── db.sqlite3
    │   ├── deploy_django.sh
    │   ├── django_api
    │   │   ├── __init__.py
    │   │   ├── __pycache__
    │   │   │   ├── __init__.cpython-311.pyc
    │   │   │   ├── admin.cpython-311.pyc
    │   │   │   ├── api_utils.cpython-311.pyc
    │   │   │   ├── apps.cpython-311.pyc
    │   │   │   ├── forms.cpython-311.pyc
    │   │   │   ├── models.cpython-311.pyc
    │   │   │   ├── urls.cpython-311.pyc
    │   │   │   └── views.cpython-311.pyc
    │   │   ├── admin.py
    │   │   ├── api_utils.py
    │   │   ├── apps.py
    │   │   ├── forms.py
    │   │   ├── migrations
    │   │   │   ├── 0001_initial.py
    │   │   │   ├── __init__.py
    │   │   │   └── __pycache__
    │   │   │       ├── 0001_initial.cpython-311.pyc
    │   │   │       └── __init__.cpython-311.pyc
    │   │   ├── models.py
    │   │   ├── templates
    │   │   │   ├── article1.html
    │   │   │   ├── article2.html
    │   │   │   ├── article3.html
    │   │   │   ├── authentication.html
    │   │   │   ├── create_client.html
    │   │   │   ├── create_news.html
    │   │   │   ├── home_page.html
    │   │   │   ├── loan_request.html
    │   │   │   ├── loan_request_list.html
    │   │   │   ├── loan_result.html
    │   │   │   ├── news.html
    │   │   │   ├── news_detail.html
    │   │   │   └── profil.html
    │   │   ├── tests.py
    │   │   ├── urls.py
    │   │   └── views.py
    │   ├── main.py
    │   ├── manage.py
    │   ├── media
    │   ├── pret_bancaire
    │   │   └── pret_bancaire
    │   │       ├── __init__.py
    │   │       ├── __pycache__
    │   │       │   ├── __init__.cpython-311.pyc
    │   │       │   ├── settings.cpython-311.pyc
    │   │       │   ├── urls.cpython-311.pyc
    │   │       │   └── wsgi.cpython-311.pyc
    │   │       ├── asgi.py
    │   │       ├── settings.py
    │   │       ├── settings_override.py
    │   │       ├── templates
    │   │       │   ├── 401.html
    │   │       │   ├── 404.html
    │   │       │   ├── 500.html
    │   │       │   ├── base.html
    │   │       │   └── includes
    │   │       │       ├── footer.html
    │   │       │       └── header.html
    │   │       ├── urls.py
    │   │       └── wsgi.py
    │   ├── requirements.txt
    │   ├── static
    │   │   ├── images
    │   │   │   ├── femme.jpg
    │   │   │   ├── garanties.jpg
    │   │   │   ├── homme.jpg
    │   │   │   ├── image_connexion.jpeg
    │   │   │   ├── networking.jpg
    │   │   │   ├── offre.jpg
    │   │   │   ├── rapidite.jpg
    │   │   │   ├── services.jpg
    │   │   │   └── tarif.jpg
    │   │   └── logo_entreprise.png
    │   ├── staticfiles
    │   └── test.py
    └── entrypoint.sh

21 directories, 88 files

## Prérequis

- Compte Azure avec abonnement actif
- Azure CLI installé localement
- Docker Desktop
- Python 3.11+

## Procédure de Déploiement

### 1. Configuration des Variables d'Environnement

Créer un fichier `.env` dans chaque dossier service :

Pour FastAPI (`docker_api/.env`):
```env
DATABASE_URL=sqlserver://kabdelmaleksqlserver.database.windows.net:1433;database=bddjango
SQL_USER=your_username
SQL_PASSWORD=your_password
Pour Django (docker_django/.env):
DJANGO_SECRET_KEY=your_secret_key
DATABASE_NAME=bddjango
DATABASE_USER=your_username
DATABASE_PASSWORD=your_password
DATABASE_HOST=kabdelmaleksqlserver.database.windows.net
DATABASE_PORT=1433
AZURE_SUBSCRIPTION_ID=72eb7803-e874-44cb-b6d9-33f2fa3eb88c
RESOURCE_GROUP=kabdelmalekRG
LOCATION=France Central
```

### 2. Configuration de la Base de Données Azure SQL

1. Accéder au portail Azure
2. Créer une base de données SQL ou utiliser une existante
3. Configurer le pare-feu pour autoriser les connexions
4. Créer les tables nécessaires via les migrations Django

### 3. Déploiement Automatisé avec Scripts Bash

#### Déploiement de l'API FastAPI
cd docker_api/brief_FastAPI
chmod +x deploy_fastapi.sh
./deploy_fastapi.sh

Le script `deploy_fastapi.sh` effectue les opérations suivantes :
- Construction de l'image Docker
- Envoi de l'image vers Azure Container Registry
- Création d'une instance de conteneur Azure
- Configuration des variables d'environnement

#### Déploiement de l'Application Django
cd docker_django/appli_django
chmod +x deploy_django.sh
./deploy_django.sh

Le script `deploy_django.sh` effectue les opérations suivantes :
- Construction de l'image Docker
- Envoi de l'image vers Azure Container Registry
- Création d'une instance de conteneur Azure
- Configuration des variables d'environnement

## Monitoring et Maintenance

### Base de Données
- Vérifier régulièrement l'état via le portail Azure
- Surveiller le délai de pause (actuellement 1 heure)
- Monitorer l'utilisation des ressources

### Applications
- Utiliser les outils de monitoring Azure
- Vérifier les logs des conteneurs
- Surveiller les performances des applications

## Optimisation des Coûts
- Configuration de la base de données SQL Azure pour limiter les coûts
- Utilisation du délai de pause automatique (1 heure)
- Monitoring des ressources pour éviter la surcharge

## Connexion aux Applications

### FastAPI
- URL de l'API : [URL de votre API]
- Documentation Swagger : [URL]/docs
- Documentation ReDoc : [URL]/redoc

### Django
- URL de l'interface web : [URL de votre application Django]
- Panel d'administration : [URL]/admin

## Sécurité
- Configuration du pare-feu Azure SQL
- Gestion sécurisée des secrets via fichiers `.env`
- Authentification et autorisation des conteneurs
# docker_azure
