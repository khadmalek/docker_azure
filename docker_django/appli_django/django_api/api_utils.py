# connexion à l'API et demande de pret
import requests
from dotenv import load_dotenv, set_key, find_dotenv
import os
import json
import fileinput


dot_env_path = find_dotenv()
load_dotenv(dotenv_path=dot_env_path)
EMAIL = os.getenv("EMAIL", None)
PASSWORD = os.getenv("PASSWORD", None)



class API_Requests() : 
    pass


def account_activation(email : str, new_password : str, confirm_password : str) : 
    url = f"http://localhost:8080/auth/activation/{email}"
    
    headers = {
        'accept' : 'application/json', 
        'Content-Type' : 'application/json'
    }
    
    data = {
        "new_password": new_password,
        "confirm_password": confirm_password
    }
    requete = requests.post(url = url, headers = headers, data = data)
    
    return requete.json()["message"]


# def get_token(self, user_name, password) :
def get_token(email = EMAIL, password = PASSWORD) :
    url = 'http://localhost:8080/auth/login'

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {
        'grant_type': 'password',
        'username': email,
        'password': password,
        'scope': '',
        'client_id': 'string',
        'client_secret': 'string'
    }
    
    response = requests.post(url = url, headers = headers, data = data)
    if response.status_code == 200 :
        return response.json()["access_token"]
    else : 
        raise Exception(f"Erreur API : {response.status_code}")


def loan_request_to_api(donnees : dict) : 
    
    TOKEN = os.getenv("ACCESS_TOKEN", None)
    
    try : 
        url = "http://127.0.0.1:8080/loans/request"
        
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type" : "application/json"
        }
        json_data = json.dumps(donnees)
        response = requests.post(url = url, headers = headers, data = json_data)
        
        # si le token est valide
        if response.status_code == 200 :
            return response.json()["result"]
        
        else : 
            # on recupere le token
            new_token = get_token()
            
            # on écrit le nouveau token dans le .env
            set_key(dot_env_path, "ACCESS_TOKEN", new_token, quote_mode="never")
            
            # on modifie le token dans le headers
            headers["Authorization"] = f"Bearer {new_token}"
            
            # on renvoie une requete avec le nouveau token
            response = requests.post(url = url, headers = headers, data = json_data)
            if response.status_code == 200 :
                return response.json()["result"]
            else : 
                raise Exception(f"Erreur API : {response.status_code}")
            
    except Exception as e : 
        raise Exception(f"Erreur lors de la requête: {str(e)}")



if __name__ == "__main__" :
    # token = get_token(email, password)
    
    data = {
    "ApprovalFY": 2008,
    "Bank": "BBCN BANK",
    "BankState": "CA",
    "City": "SPRINGFIELD",
    "CreateJob": 2,
    "DisbursementGross": 20000,
    "FranchiseCode": 1,
    "GrAppv": 20000,
    "LowDoc": 0,
    "NAICS": 453110,
    "NewExist": 1,
    "NoEmp": 4,
    "RetainedJob": 250,
    "RevLineCr": 0,
    "State": "TN",
    "Term": 6,
    "UrbanRural": 1,
    "Zip": 37172
    }
    
    print(loan_request_to_api(donnees = data))

    # print(account_activation())