from sqlmodel import SQLModel, create_engine, text, Session
from dotenv import load_dotenv
import os
from .modeles import *
import pyodbc
import urllib.parse

"""
Module de configuration et de gestion de la connexion à la base de données.

Ce module gère la configuration de la base de données, supporte SQLite et MariaDB,
et fournit une fonction de connexion pour les sessions de base de données.

Attributes:
    DATABASE_URL (str): URL de connexion à la base de données
    engine: Instance du moteur SQLAlchemy pour la connexion à la base de données
"""

load_dotenv(dotenv_path="./app/.env")

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")  # Par défaut SQLite si non défini

# # Vérifier si on utilise MariaDB pour créer la base de données si nécessaire
# if "mariadb" in DATABASE_URL:
#     DATABASE_USERNAME = os.getenv("DATABASE_USERNAME", None)
#     DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", None)
#     DB_NAME = "loan"

#     # moteur pour créer la BDD
#     temp_engine = create_engine(f"mariadb+pymysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@localhost:3306/")

#     with temp_engine.connect() as conn:
#         conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"))
#         conn.execute(text("FLUSH PRIVILEGES"))
#     temp_engine.dispose()

#     DATABASE_URL = f"mariadb+pymysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@localhost:3306/{DB_NAME}"  # BDD définitive sous mariadb

DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
HOST_NAME = os.getenv("HOST_NAME")
DATABASE_NAME = os.getenv("DATABASE_NAME")
PORT = os.getenv("PORT", "1433")  # Ajouté le port SQL Server

connection_string = (
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={HOST_NAME};"
    f"DATABASE={DATABASE_NAME};"
    f"UID={DATABASE_USERNAME};"
    f"PWD={DATABASE_PASSWORD};"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

params = urllib.parse.quote_plus(connection_string)
DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={params}"
sqlite_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
engine = create_engine(DATABASE_URL, connect_args=sqlite_args, echo=True)

SQLModel.metadata.create_all(engine)    # Crée les tables dans la base de données

def db_connection():
    """
    Générateur de session de base de données pour FastAPI.

    Yields:
        Session: Session SQLModel active pour les opérations de base de données.

    Note:
        - Utilise le pattern contextuel pour garantir la fermeture de la session
        - Compatible avec le système de dépendances de FastAPI
        - Gère automatiquement la fermeture de la session après utilisation
        - Utilisé comme dépendance dans les routes de l'API

    Example:
        ```python
        @app.get("/users")
        def get_users(db: Session = Depends(db_connection)):
            return db.query(User).all()
        ```
    """
    session = Session(engine)  # Ouvre une session SQLModel
    try:
        yield session  # Garde la session ouverte pour l'API
    finally:
        session.close()  # Ferme la session après utilisation


