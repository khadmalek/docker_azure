from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, Column, String


"""
Module définissant les modèles SQLModel pour la base de données.

Ce module contient les définitions des tables de la base de données,
notamment les utilisateurs (banques) et les demandes de prêts.
"""

class Users(SQLModel, table=True):      # la banque
    """
    Modèle représentant une banque utilisatrice du système.

    Attributes:
        id_banque (int): Identifiant unique de la banque (clé primaire)
        nom_banque (str): Nom unique de la banque
        email (str): Email unique de la banque
        hashed_password (str): Mot de passe hashé
        role (str): Rôle de l'utilisateur ('admin' ou 'user')
        is_active (bool): État d'activation du compte

    Note:
        - Les champs nom_banque et email sont uniques
        - Le rôle par défaut est 'user'
        - Le compte est inactif par défaut (is_active=False)
    """
    id_banque: Optional[int] = Field(default=None, primary_key=True, index=True)
    nom_banque: str = Field(sa_column=Column(String(255), unique=True))
    email: str = Field(sa_column=Column(String(255), unique=True))
    hashed_password: str = Field(sa_column=Column(String(255)))
    role: str = Field(sa_column=Column(String(50)), default="user")
    is_active: bool = Field(default=False)


class Loan_requests(SQLModel, table=True):
    """
    Modèle représentant une demande de prêt.

    Attributes:
        id (int): Identifiant unique de la demande (clé primaire)
        statut (bool): Statut de la demande (True si accordée, False si refusée)
        id_demandeur (int): ID de la banque ayant fait la demande
        date_demande (datetime): Date et heure de la demande

    Note:
        - La date est automatiquement définie à l'UTC actuel
        - L'id_demandeur est obligatoire et fait référence à Users.id_banque
        - Le statut est False par défaut
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    statut: bool = Field(default=False)
    id_demandeur: int = Field(nullable=False)       # id de la banque qui fait la demande
    date_demande: datetime = Field(default_factory=datetime.utcnow, nullable=False)

