#!/bin/bash

set -e

# Activer l'environnement virtuel
source /env/bin/activate

# Afficher la structure des répertoires
echo "Contenu du répertoire actuel :"
ls -la

# Naviguer vers le répertoire contenant manage.py
cd appli_django/pret_bancaire

# Afficher le contenu pour vérification
echo "Contenu du répertoire pret_bancaire :"
ls -la

# Collecter les fichiers statiques
echo "Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

if [ "$1" == 'gunicorn' ]; then
    # Exécuter gunicorn avec le bon module WSGI
    exec gunicorn pret_bancaire.wsgi:application -b 0.0.0.0:8000
else
    # Pour le développement
    python manage.py runserver 0.0.0.0:8000
fi