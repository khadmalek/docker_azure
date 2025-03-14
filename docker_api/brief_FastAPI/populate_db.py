from sqlmodel import Session
from faker import Faker
import random
from app.utils import bcrypt_context
from sqlmodel import SQLModel
from app.database import engine
from app.modeles import Users, Loan_requests



"""
Script de population initiale de la base de données.

Ce script crée et remplit la base de données avec des données de test,
incluant un administrateur par défaut et des données fictives générées
avec la bibliothèque Faker.

Functions:
    populate_db(): Remplit la base de données avec des données de test

Données générées:
    - Un administrateur avec identifiants fixes
    - Utilisateurs (banques) fictifs
    - Demandes de prêts fictives

Note:
    - Utilise SQLModel pour la gestion de la base de données
    - Utilise Faker pour la génération de données réalistes
    - Les mots de passe sont hashés avec bcrypt
"""

def populate_db():
    """
    Remplit la base de données avec des données de test.

    Crée:
        - Un administrateur (email: 'admin', mot de passe: 'admin')
        - 2 banques fictives avec emails et mots de passe aléatoires
        - 5 demandes de prêts fictives avec statuts aléatoires

    Note:
        - Les mots de passe sont automatiquement hashés
        - Les dates des demandes sont générées sur les 2 dernières années
        - Les statuts des prêts sont aléatoires (50% approuvés)
        - Les IDs des demandeurs sont des nombres aléatoires entre 1000 et 9999

    Raises:
        SQLAlchemyError: En cas d'erreur de base de données
    """
    fake = Faker()

    # Ouvrir une session SQLModel
    with Session(engine) as session:
        
        # Ajouter un utilisateur admin
        admin_user = Users(
            nom_banque="Admin",
            email="admin",
            hashed_password=bcrypt_context.hash("admin"),  # Mot de passe hashé
            role="admin",  # Assure-toi que ce champ existe dans Users
            is_active=1
            )
        session.add(admin_user)
        # Générer des utilisateurs fictifs
        users = []
        for _ in range(2):
            user = Users(
                nom_banque=fake.company_suffix() + " Bank",  # Exemple : 'TechCorp Bank'
                email=fake.unique.email(),
                hashed_password=bcrypt_context.hash(fake.password(length=12)),
            )
            session.add(user)
            users.append(user)
        
        # Générer des demandes de prêt fictives
        for _ in range(5):
            loan_request = Loan_requests(
                statut=fake.boolean(chance_of_getting_true=50),  # 50% approuvé/refusé
                id_demandeur=random.randint(1000, 9999),
                date_demande=fake.date_time_between(start_date="-2y", end_date="now")  # Entre 2 ans et aujourd'hui
            )
            session.add(loan_request)

        session.commit()  # On commit pour enregistrer les demandes de prêt

    print("Base de données remplie avec succès !")
    
if __name__ == "__main__" : 
    """
    Point d'entrée du script.

    Exécute:
        1. La création des tables dans la base de données
        2. Le remplissage avec les données de test
    """
    # remplir la BDD avec faker
    populate_db()

    # Créer les tables dans la base de données
    SQLModel.metadata.create_all(engine)

