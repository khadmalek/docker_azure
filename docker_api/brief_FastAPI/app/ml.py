# Modèle prédiction
import pickle
import pandas as pd


"""
Module de prédiction pour l'évaluation des demandes de prêts.

Ce module fournit les fonctions nécessaires pour charger le modèle CatBoost
et effectuer des prédictions sur les demandes de prêts.

Functions:
    transform_naics: Transforme les codes NAICS
    transform_franchise: Transforme les codes de franchise
    charger_modele: Charge le modèle depuis un fichier pickle
    predire: Effectue une prédiction avec le modèle
"""

def transform_naics(X):
    """
    Transforme les codes NAICS en gardant uniquement les deux premiers chiffres.

    Args:
        X (pd.DataFrame): DataFrame contenant la colonne 'NAICS'

    Returns:
        numpy.ndarray: Array 2D des codes NAICS transformés

    Note:
        Convertit les codes NAICS en entiers à 2 chiffres pour la classification
    """
    return X['NAICS'].astype(str).str[:2].astype(int).values.reshape(-1, 1)

def transform_franchise(X):
    """
    Transforme les codes de franchise en indicateur binaire.

    Args:
        X (pd.DataFrame): DataFrame contenant la colonne 'FranchiseCode'

    Returns:
        numpy.ndarray: Array 2D avec 1 pour les codes 0 ou 1, 0 sinon

    Note:
        Simplifie les codes de franchise en classification binaire
    """
    return X['FranchiseCode'].apply(lambda x: 1 if x in [0, 1] else 0).values.reshape(-1, 1)

def charger_modele(fichier_pkl : str ="best_cat_boost.pkl") -> "model":
    """
    Charge le modèle CatBoost depuis un fichier pickle.

    Args:
        fichier_pkl (str): Chemin vers le fichier pickle du modèle

    Returns:
        CatBoostClassifier: Modèle CatBoost chargé

    Raises:
        FileNotFoundError: Si le fichier du modèle n'existe pas
        pickle.UnpicklingError: Si le fichier est corrompu
    """
    with open(fichier_pkl, 'rb') as f:
        return pickle.load(f)

def predire(model : "model", donnees : pd.DataFrame) -> int: 
    """
    Effectue une prédiction sur des données d'entrée.

    Args:
        model: Modèle CatBoost chargé
        donnees (pd.DataFrame): DataFrame contenant les features nécessaires

    Returns:
        int: 1 si le prêt est accordé, 0 sinon

    Note:
        Les données doivent contenir toutes les features utilisées lors de l'entraînement
    """
    return model.predict(donnees)


if __name__ == "__main__":
    model = charger_modele("best_cat_boost.pkl")
    features = model.feature_names_
    # features = ['City', 'State', 'Zip', 'Bank', 'BankState', 'NAICS', 'ApprovalFY', 'Term', 'NoEmp', 'NewExist', 'CreateJob', 'RetainedJob', 'FranchiseCode', 'UrbanRural', 'LowDoc', 'DisbursementGross', 'GrAppv', 'RevLineCr']
    test = ["SPRINGFIELD", "TN", 37172, "BBCN BANK", "CA", 453110, 2008, 6, 4, 1.0, 2, 250, 1, 1, 0, 20000.0, 20000.0, 0] 
    # test_df = pd.DataFrame([test], columns=features)
    test_df = test

    prediciton = model.predict(test)
    print("va payer" if prediciton else "ne va pas payer")
    print(prediciton)
    print(model.predict_proba(test_df))
    print(list(features))
    print(model.get_cat_feature_indices())

