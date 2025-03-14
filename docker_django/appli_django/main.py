import os
import django
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pret_bancaire.pret_bancaire.settings')
django.setup()

# Import après la configuration de Django
from django.core.wsgi import get_wsgi_application

# Création de l'application FastAPI
app = FastAPI()

# Obtention de l'application WSGI Django
django_app = get_wsgi_application()

# Montage de l'application Django
app.mount("/django", WSGIMiddleware(django_app))

# Route FastAPI de test
@app.get("/")
async def root():
    return {"message": "Hello World"}