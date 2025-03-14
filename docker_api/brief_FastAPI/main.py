# Point d'entrée de l'application
from fastapi import FastAPI
from app.endpoints import route_loans, route_admin, route_auth



"""
Point d'entrée principal de l'API de prédiction de prêts.

Ce module initialise l'application FastAPI et configure les routes
pour l'authentification, l'administration et la gestion des prêts.

Application Properties:
    title: "API de prêts"
    description: "API pour prédire l'accord de prêts"
    version: "0.1"

Routes incluses:
    - /loans: Gestion des demandes de prêts et prédictions
    - /admin: Administration des utilisateurs
    - /auth: Authentification et gestion des tokens

Note:
    L'API utilise FastAPI pour:
    - Documentation automatique (Swagger UI sur /docs)
    - Validation des données avec Pydantic
    - Gestion des routes avec APIRouter
    - Support asynchrone natif
"""

# Créer l'application FastAPI
app = FastAPI(title="API de prêts", description="API pour prédire l'accord de prêts", version="0.2")

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API de prêts. Consultez /docs pour la documentation."}

# inclure les routes
app.include_router(route_loans.router)
app.include_router(route_admin.router)
app.include_router(route_auth.router)

