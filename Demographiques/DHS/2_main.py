# ==============================================================================
# TÂCHE 1 : COLLECTE DE DONNÉES SOCIALES VIA L'API DHS
# Projet : ANIP AI/Data Challenge 2025
# Objectif : Collecter des indicateurs sanitaires et sociaux pour le Bénin
#            directement depuis l'API du DHS Program, en gérant la structure
#            spécifique de la réponse de l'API et en filtrant les indicateurs
#            non pertinents pour produire un dataset propre.
# Source : https://api.dhsprogram.com/
# Auteur : SOULE Fadile
# Date : 21/09/25
# ==============================================================================

import requests
import pandas as pd
import sys

# --- CONFIGURATION ---
INDICATOR_IDS = {
    "HC_ELEC_H_ELC": "pct_menages_electricite",
    "ED_LITR_W_LIT": "pct_alphab_femmes",
    "CM_ECMR_C_IMR": "tx_mortalite_infantile",
    "WS_SRCE_H_IMP": "pct_acces_eau_potable"
}
COUNTRY_CODE = 'BJ'
OUTPUT_CSV_PATH = 'dhs_indicators_benin_api.csv'

# print("Script 6: Démarrage de la collecte des indicateurs via l'API du DHS Program.")

# --- Étape 1: Exécuter la requête API ---
try:
    base_url = "https://api.dhsprogram.com/rest/dhs/data"
    params = {"countryIds": COUNTRY_CODE, "indicatorIds": ",".join(INDICATOR_IDS.keys()), "f": "json", "perPage": 1000}
    
    print("Envoi de la requête à l'API DHS...")
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    data = response.json()

    # --- Étape 2: Valider et traiter la réponse ---
    if 'Data' not in data or not data['Data']:
        print("AVERTISSEMENT: L'API n'a retourné aucune donnée pour cette sélection.")
        sys.exit(0)

    print(f"{len(data['Data'])} points de données bruts reçus de l'API.")
    df_api = pd.DataFrame(data['Data'])
    
    # --- Étape 3: Filtrer et nettoyer les données ---
    df_filtered = df_api[df_api['IsPreferred'] == 1].copy()
    print(f"{len(df_filtered)} points de données pertinents conservés après filtrage.")
    
    # **On sélectionne 'IndicatorId' au lieu de 'Indicator'**
    df_cleaned = df_filtered[['IndicatorId', 'SurveyYear', 'Value']].copy()
    
    # --- Étape 4: Pivoter les données pour obtenir le format final ---
    # **On pivote sur 'IndicatorId'**
    df_pivot = df_cleaned.pivot_table(
        index='SurveyYear', 
        columns='IndicatorId', 
        values='Value'
    ).reset_index()
    
    # Le renommage va maintenant fonctionner car les noms de colonnes sont les IDs
    df_pivot.rename(columns=INDICATOR_IDS, inplace=True)
    df_pivot.rename(columns={'SurveyYear': 'annee'}, inplace=True)
    
    # On supprime le nom de l'index des colonnes pour un résultat plus propre
    df_pivot.rename_axis(None, axis=1, inplace=True)
    
    print("Données transformées avec succès.")

except requests.exceptions.RequestException as e:
    print(f"ERREUR: La requête à l'API a échoué. Détails: {e}")
    sys.exit(1)
except Exception as e:
    print(f"ERREUR: Le traitement des données a échoué. Détails: {e}")
    sys.exit(1)

# --- Étape 5: Sauvegarder le dataset final ---
df_pivot.to_csv(OUTPUT_CSV_PATH, index=False)

print("\nScript terminé.")
print(f"Le dataset des indicateurs DHS a été sauvegardé dans : '{OUTPUT_CSV_PATH}'")
print(df_pivot) # Afficher tout le DataFrame car il est petit