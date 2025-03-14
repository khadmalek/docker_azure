from sqlmodel import Session, create_engine, SQLModel
from faker import Faker
import random
from app.utils import bcrypt_context
from app.modeles import Users, Loan_requests
import urllib.parse
from dotenv import load_dotenv
import os

load_dotenv()

# Configuration SQL Server
server = os.getenv("HOST_NAME")
database = os.getenv("DATABASE_NAME")
username = os.getenv("DATABASE_USERNAME")
password = os.getenv("DATABASE_PASSWORD")
driver = "{ODBC Driver 18 for SQL Server}"

# Créer l'URL de connexion
params = urllib.parse.quote_plus(
    f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
)
DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={params}"

# Créer le moteur
engine = create_engine(DATABASE_URL, echo=True)

def populate_db():
    fake = Faker()

    with Session(engine) as session:
        session.query(Users).delete()
        session.query(Loan_requests).delete()
        session.commit()

    with Session(engine) as session:
        # Vérifier si l'utilisateur Admin existe déjà
        admin_user = session.query(Users).filter_by(email="admin").first()
        if not admin_user:  # Si l'utilisateur n'existe pas, le créer
            admin_user = Users(
                nom_banque="Admin",
                email="admin",
                hashed_password=bcrypt_context.hash("admin"),
                role="admin",
                is_active=1
            )
            session.add(admin_user)
            
        # vérifier si l'utilisateur de la banque existe 
        bank_user = session.query(Users).filter_by(email="administrator@californiabankandtrust.com").first()
        if not bank_user:  # Si l'utilisateur n'existe pas, le créer
            bank_user = Users(
                nom_banque="CALIFORNIA BANK AND TRUST",
                email="administrator@californiabankandtrust.com",
                hashed_password=bcrypt_context.hash("azerty12"),
                role="admin",
                is_active=1
            )
            session.add(bank_user)

        users = []
        for _ in range(2):
            user = Users(
                nom_banque=fake.company_suffix() + " Bank " + str(random.randint(1000, 9999)),
                email=f"user_{random.randint(1000, 9999)}@example.com",
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


if __name__ == "__main__":
    SQLModel.metadata.create_all(engine)
    populate_db()