# Schémas Pydantic pour les formulaires de l'API
from pydantic import BaseModel, Field, EmailStr
from typing import Union


"""
Module définissant les schémas Pydantic pour la validation des données d'entrée de l'API.

Ce module contient les modèles de validation pour les demandes de prêts,
la création d'utilisateurs et le changement de mot de passe.
"""

class LoanRequest(BaseModel):
    """
    Schéma de validation pour une demande de prêt.

    Attributes:
        City (str): Ville du demandeur
        State (str): Code état à 2 caractères
        Zip (int): Code postal
        Bank (str): Nom de la banque
        BankState (str): Code état de la banque à 2 caractères
        NAICS (int): Code NAICS de l'entreprise
        ApprovalFY (int): Année fiscale d'approbation
        Term (int): Durée du prêt en mois
        NoEmp (int): Nombre d'employés
        NewExist (float): Indicateur entreprise nouvelle/existante
        CreateJob (int): Nombre d'emplois à créer
        RetainedJob (int): Nombre d'emplois à conserver
        FranchiseCode (int): Code de franchise
        UrbanRural (int): Indicateur zone urbaine (1) ou rurale (0)
        LowDoc (int): Indicateur programme LowDoc
        DisbursementGross (float): Montant brut du décaissement
        GrAppv (float): Montant brut approuvé
        RevLineCr (int): Indicateur ligne de crédit renouvelable

    Note:
        Inclut un exemple complet dans Config.json_schema_extra
    """
    City: str = Field(..., description="Ville")
    State: str = Field(..., description="État", max_length=2)
    Zip: int = Field(..., description="Code postal")
    Bank: str = Field(..., description="Nom de la banque")
    BankState: str = Field(..., description="État de la banque", max_length=2)
    NAICS: int = Field(..., description="Code NAICS")
    ApprovalFY: int = Field(..., description="Année fiscale d'approbation")
    Term: int = Field(..., description="Durée du prêt en mois")
    NoEmp: int = Field(..., description="Nombre d'employés")
    NewExist: float = Field(..., description="Nouvelle entreprise ou existante")  # Changed to float
    CreateJob: int = Field(..., description="Nombre d'emplois créés")
    RetainedJob: int = Field(..., description="Nombre d'emplois conservés")
    FranchiseCode: int = Field(..., description="Code franchise")
    UrbanRural: int = Field(..., description="Zone urbaine (1) ou rurale (0)")
    LowDoc: int = Field(..., description="Programme LowDoc (1) ou non (0)")
    DisbursementGross: float = Field(..., description="Montant brut distribué")  # Moved up
    GrAppv: float = Field(..., description="Montant brut approuvé")  # Moved up
    RevLineCr: int = Field(..., description="Ligne de crédit renouvelable")  # Changed to int

    class Config:
        json_schema_extra = {
            "example": {
                "City": "SPRINGFIELD",
                "State": "TN",
                "Zip": 37172,
                "Bank": "BBCN BANK",
                "BankState": "CA",
                "NAICS": 453110,
                "ApprovalFY": 2008,
                "Term": 6,
                "NoEmp": 4,
                "NewExist": 1.0,
                "CreateJob": 2,
                "RetainedJob": 250,
                "FranchiseCode": 1,
                "UrbanRural": 1,
                "LowDoc": 0,
                "DisbursementGross": 20000.0,
                "GrAppv": 20000.0,
                "RevLineCr": 0
            }
        }        


class CreateUserRequest(BaseModel):
    """
    Schéma de validation pour la création d'un nouvel utilisateur.

    Attributes:
        nom_banque (str): Nom unique de la banque
        email (EmailStr): Adresse email valide
        password (str): Mot de passe (minimum 8 caractères)

    Note:
        - L'email est validé automatiquement par EmailStr
        - Le mot de passe doit faire au moins 8 caractères
        - Inclut un exemple dans Config.json_schema_extra
    """
    nom_banque: str = Field(..., description="Nom de la banque")
    email: EmailStr
    password: str = Field(..., min_length=8, description="longueur minimale de 8 caractères")
    
    class Config:
        json_schema_extra = {
            "example": {
                "nom_banque": "Bank 1",
                "email": "mon_email@domaine.com",
                "password": "azerty12",
            }
        }        
        

class NewPassword(BaseModel) : 
    """
    Schéma de validation pour le changement de mot de passe.

    Attributes:
        new_password (str): Nouveau mot de passe (minimum 8 caractères)
        confirm_password (str): Confirmation du nouveau mot de passe

    Note:
        - Les deux mots de passe doivent être identiques
        - Minimum 8 caractères pour chaque mot de passe
        - Inclut un exemple dans Config.json_schema_extra
    """
    new_password : str = Field(..., min_length=8, description="longueur minimale de 8 caractères")
    confirm_password : str = Field(..., min_length=8, description="longueur minimale de 8 caractères")
    class Config:
        json_schema_extra = {
            "example": {
                "new_password": "azerty12",
                "confirm_password": "azerty12",
            }
        }

