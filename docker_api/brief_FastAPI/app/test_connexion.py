import os
from dotenv import load_dotenv
import urllib.parse

load_dotenv(dotenv_path="./app/.env")

connection_string = (
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={os.getenv('HOST_NAME')};"
    f"DATABASE={os.getenv('DATABASE_NAME')};"
    f"UID={os.getenv('DATABASE_USERNAME')};"
    f"PWD={os.getenv('DATABASE_PASSWORD')};"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

params = urllib.parse.quote_plus(connection_string)
DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={params}"

import pyodbc
conn = pyodbc.connect(connection_string)