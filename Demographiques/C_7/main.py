# ==============================================================================
# TÂCHE 1 : ÉTAPE 7 — COLLECTE ET CONSOLIDATION DES DONNÉES SUR L'ÉDUCATION
# Projet : ANIP AI/Data Challenge 2025
# Objectif : Télécharger, nettoyer et consolider plusieurs indicateurs sur
#            l'éducation au Bénin à partir de l'API de la Banque Mondiale.
# Source : World Bank Open Data API (https://data.worldbank.org/)
# Auteur : SOULE Fadile
# Date : 21/09/25
# ==============================================================================

import pandas as pd
import requests
import zipfile
import io
import os
import sys
from functools import reduce

# --- CONFIGURATION ---
DATA_RAW_DIR = "data/raw"
DATA_CLEANED_DIR = "data/cleaned"
COUNTRY_NAME = "Benin"

# Dictionnaire central des indicateurs à télécharger
# Clé = Code de l'indicateur, Valeur = Nom de la colonne dans le fichier final
INDICATORS = {
    "SE.PRM.ENRR": "tx_scolarisation_primaire_brut",
    "SE.PRM.ENRR.FE": "tx_scolarisation_primaire_feminin",
    "SE.PRM.TCAQ.ZS": "pct_enseignants_formes",
    "SE.PRM.TCAQ.FE.ZS": "pct_enseignantes_formees",
    "SE.PRM.TCAQ.MA.ZS": "pct_enseignants_hommes_formes",
    "SE.PRM.PRSL.MA.ZS": "tx_persistance_primaire_masculin"
}

def process_indicator(indicator_code, value_name):
    """
    Télécharge, nettoie et formate les données pour un indicateur de la Banque Mondiale.
    """
    print(f"\nTraitement de l'indicateur : {indicator_code}...")
    
    # Étape 1: Téléchargement
    url = f"https://api.worldbank.org/v2/en/indicator/{indicator_code}?downloadformat=csv"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"ERREUR: Téléchargement échoué pour {indicator_code}. Détails: {e}")
        return None

    # Étape 2: Extraction
    try:
        with zipfile.ZipFile(io.BytesIO(response.content), "r") as z:
            data_file = next(f for f in z.namelist() if f.startswith(f"API_{indicator_code}") and "Metadata" not in f)
            with z.open(data_file) as csvfile:
                df = pd.read_csv(csvfile, skiprows=4)
    except (zipfile.BadZipFile, StopIteration, FileNotFoundError) as e:
        print(f"ERREUR: Impossible d'extraire le CSV pour {indicator_code}. Détails: {e}")
        return None

    # Étape 3: Filtrage et Transformation
    if "Country Name" not in df.columns or df[df["Country Name"] == COUNTRY_NAME].empty:
        print(f"AVERTISSEMENT: Aucune donnée trouvée pour {COUNTRY_NAME} dans l'indicateur {indicator_code}.")
        return None

    benin_data = df[df["Country Name"] == COUNTRY_NAME].copy()
    
    years = [str(year) for year in range(1960, 2025)]
    id_vars = ["Country Name", "Country Code"]
    cols_to_keep = id_vars + [y for y in years if y in benin_data.columns]
    
    df_benin_long = benin_data[cols_to_keep].melt(
        id_vars=id_vars,
        var_name="annee",
        value_name=value_name
    )

    # Étape 4: Nettoyage
    df_benin_long["annee"] = pd.to_numeric(df_benin_long["annee"], errors="coerce")
    df_benin_long.dropna(subset=[value_name], inplace=True)
    df_benin_long["annee"] = df_benin_long["annee"].astype(int)
    
    df_final = df_benin_long[["annee", value_name]]
    print(f"Traitement réussi. {len(df_final)} observations valides trouvées.")
    return df_final

# --- SCRIPT PRINCIPAL ---
if __name__ == "__main__":
    print("Script 7: Démarrage de la collecte des données sur l'éducation de la Banque Mondiale.")
    
    os.makedirs(DATA_RAW_DIR, exist_ok=True)
    os.makedirs(DATA_CLEANED_DIR, exist_ok=True)
    
    all_dfs = []
    
    for code, name in INDICATORS.items():
        processed_df = process_indicator(code, name)
        if processed_df is not None:
            all_dfs.append(processed_df)
            
    if not all_dfs:
        print("ERREUR: Aucune donnée n'a pu être collectée. Le script s'arrête.")
        sys.exit(1)

    # --- Étape finale: Consolidation ---
    print("\nConsolidation de tous les indicateurs d'éducation...")
    
    # Fusionner tous les DataFrames sur la colonne 'annee'
    df_consolidated = reduce(lambda left, right: pd.merge(left, right, on='annee', how='outer'), all_dfs)
    
    # Trier par année
    df_consolidated.sort_values('annee', inplace=True)
    
    output_path = os.path.join(DATA_CLEANED_DIR, "education_indicators_benin_consolidated.csv")
    df_consolidated.to_csv(output_path, index=False, encoding="utf-8-sig")
    
    print("\nScript terminé.")
    print(f"Le dataset consolidé sur l'éducation a été sauvegardé dans : '{output_path}'")
    print("\nAperçu du dataset final :")
    print(df_consolidated.tail(15))