# Projet de Prêt Bancaire sur Azure

Application de gestion de prêts bancaires combinant une API FastAPI et une interface Django, déployée sur Azure. Ce projet utilise Docker pour la conteneurisation et Azure SQL Database pour le stockage des données.

![Azure](https://img.shields.io/badge/Azure-0078D4?style=flat&logo=microsoft-azure&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=flat&logo=django&logoColor=white)
![SQL Server](https://img.shields.io/badge/SQL%20Server-CC2927?style=flat&logo=microsoft-sql-server&logoColor=white)

---

## 📌 Contexte du Projet

Ce projet s'inscrit dans la continuité du travail effectué sur le projet **US SBA**. Après avoir conçu et testé les applications localement, l'objectif est maintenant de les déployer sur **Azure** en utilisant différentes méthodes d’automatisation.

## 🔍 Architecture du Projet

### 🌐 Services Utilisés

- **Azure Container Instance (ACI)**
  - Conteneur FastAPI pour l'API
  - Conteneur Django pour l'interface web
- **Azure SQL Database**
  - Base de données relationnelle pour stocker les données
- **Docker**
  - Conteneurisation des applications

## 🚀 Étapes du Projet

### 🏗 Niveau 1 : Déploiement via le Portail Azure
1. Création d'une base de données SQL Azure
2. Configuration du pare-feu et des règles d'accès
3. Déploiement manuel des conteneurs via Azure Container Instances
4. Configuration des variables d'environnement

### 🤖 Niveau 2 : Automatisation avec un Script Bash
1. Développement de scripts d'automatisation (`deploy_fastapi.sh` et `deploy_django.sh`)
2. Utilisation d'Azure CLI pour le déploiement automatisé
3. Gestion sécurisée des secrets via fichiers `.env`

### 🎯 [Bonus] Niveau 3 : Infrastructure as Code avec Terraform
- Mise en place de la configuration avec Terraform (optionnel)

---

## 📌 Prérequis

- Compte Azure avec abonnement actif
- Azure CLI installé localement
- Docker Desktop
- Python 3.11+

## ⚙️ Procédure de Déploiement

### 1️⃣ Configuration des Variables d'Environnement

Créer un fichier `.env` dans chaque dossier de service :

**Pour FastAPI (`docker_api/.env`)** :
```env
DATABASE_URL=sqlserver://<nom-du-serveur>.database.windows.net:1433;database=<nom-de-la-bdd>
SQL_USER=<votre_username>
SQL_PASSWORD=<votre_password>
```

**Pour Django (`docker_django/.env`)** :
```env
DJANGO_SECRET_KEY=<votre_secret_key>
DATABASE_NAME=<nom-de-la-bdd>
DATABASE_USER=<votre_username>
DATABASE_PASSWORD=<votre_password>
DATABASE_HOST=<nom-du-serveur>.database.windows.net
DATABASE_PORT=1433
```

ℹ️ **Aucune information sensible ne doit être exposée publiquement !**

### 2️⃣ Configuration de la Base de Données Azure SQL

1. Accéder au portail Azure
2. Créer une base de données SQL ou utiliser une existante
3. Configurer le pare-feu pour autoriser les connexions
4. Exécuter les migrations Django pour créer les tables nécessaires

### 3️⃣ Déploiement Automatisé avec Scripts Bash

#### Déploiement de l'API FastAPI
```bash
cd docker_api/brief_FastAPI
chmod +x deploy_fastapi.sh
./deploy_fastapi.sh
```

Le script `deploy_fastapi.sh` effectue les opérations suivantes :
- Construction de l'image Docker
- Envoi de l'image vers Azure Container Registry
- Création d'une instance de conteneur Azure
- Configuration des variables d'environnement

#### Déploiement de l'Application Django
```bash
cd docker_django/appli_django
chmod +x deploy_django.sh
./deploy_django.sh
```

Le script `deploy_django.sh` effectue les opérations suivantes :
- Construction de l'image Docker
- Envoi de l'image vers Azure Container Registry
- Création d'une instance de conteneur Azure
- Configuration des variables d'environnement

---

## 📊 Monitoring et Maintenance

### 📂 Base de Données
- Vérifier régulièrement l'état via le portail Azure
- Surveiller l'utilisation des ressources
- Effectuer des sauvegardes régulières

### 🖥️ Applications
- Utiliser les outils de monitoring Azure
- Vérifier les logs des conteneurs
- Surveiller les performances des applications

---

## 💰 Optimisation des Coûts

- Configuration de la base de données SQL Azure pour limiter les coûts
- Utilisation du délai de pause automatique
- Monitoring des ressources pour éviter la surcharge

---

## 🔗 Connexion aux Applications

### 🌍 FastAPI
- **URL de l'API** : `[URL de votre API]`
- **Documentation Swagger** : `[URL]/docs`
- **Documentation ReDoc** : `[URL]/redoc`

### 🏠 Django
- **URL de l'interface web** : `[URL de votre application Django]`
- **Panel d'administration** : `[URL]/admin`

---

## 🔐 Sécurité

- **Configuration du pare-feu Azure SQL** pour restreindre les accès
- **Gestion sécurisée des secrets** via fichiers `.env`
- **Authentification et autorisation** des conteneurs

---

## 📁 Dépôt GitHub

Ce dépôt contient :
- 📂 Le code du projet
- 📜 Le script Bash d’automatisation
- 📑 (Bonus) Les fichiers Terraform si niveau 3 réalisé
- 📖 Un fichier README expliquant les étapes du projet et la procédure de déploiement

🚀 **Bon déploiement !** 🎯
