# Routes admin
from fastapi import APIRouter, Depends
from app.schemas import CreateUserRequest
from app.utils import db_dependency, bcrypt_context, get_current_user
from app.modeles import Users
from sqlalchemy import text
from typing import Annotated


router = APIRouter(prefix="/admin", tags=["admin"])  # pour les routes d'administration


@router.get("/users")   # Obtenir la liste des utilisateurs
async def get_users(db : db_dependency, current_user: Annotated[Users, Depends(get_current_user)]):
    """
    Récupère la liste de tous les utilisateurs de l'application.

    Args:
        db (Session): Session de base de données SQLAlchemy.
        current_user (Users): Utilisateur actuellement authentifié.

    Returns:
        list: Liste des utilisateurs sous forme de dictionnaires.

    Raises:
        HTTPException: Si l'utilisateur n'a pas les droits d'administration.

    Note:
        - Nécessite des droits d'administration
        - Retourne tous les champs de la table users
    """
    role = current_user.role
    if role == "admin" : 
        result = db.execute(text("SELECT * FROM users")).mappings().all()
        return result


@router.post("/users")  # Créer un utilisateur
async def create_user(create_user_request: CreateUserRequest, db: db_dependency, current_user: Annotated[Users, Depends(get_current_user)]):
    """
    Crée un nouvel utilisateur dans le système.

    Args:
        create_user_request (CreateUserRequest): Données du nouvel utilisateur.
        db (Session): Session de base de données SQLAlchemy.
        current_user (Users): Utilisateur actuellement authentifié.

    Returns:
        dict: Message de confirmation avec le nom de la banque créée.

    Raises:
        HTTPException: Si l'utilisateur n'a pas les droits d'administration.

    Note:
        - Nécessite des droits d'administration
        - Le mot de passe est automatiquement hashé avant stockage
        - CreateUserRequest doit contenir :
            - nom_banque (str)
            - email (str)
            - password (str)
    """
    role = current_user.role
    if role == "admin" : 
        create_user_model = Users(
            nom_banque=create_user_request.nom_banque,
            email=create_user_request.email, 
            hashed_password=bcrypt_context.hash(create_user_request.password)
            )
        db.add(create_user_model)
        db.commit()
        return {"message": f"Utilisateur {create_user_request.nom_banque} créé"}
    