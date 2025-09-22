# ==============================================================================
# TÂCHE 1 : ÉTAPE 4 — CHARGEMENT ET FILTRAGE DES DONNÉES ONU
# Projet : ANIP AI/Data Challenge 2025
# Objectif : Charger les données démographiques des Nations Unies (WPP 2024),
#            gérer le formatage complexe du fichier Excel, et extraire
#            uniquement les données brutes concernant le Bénin.
# Source : Fichier WPP2024_GEN_F01_DEMOGRAPHIC_INDICATORS_FULL.xlsx de Kaggle
# Auteur : SOULE Fadile
# Date : 21/09/25
# ==============================================================================

import pandas as pd
import os
import sys

# --- CONFIGURATION ---
# Chemin vers le fichier Excel brut décompressé
INPUT_EXCEL_PATH = 'kaggle_data_unzipped/WPP2024_GEN_F01_DEMOGRAPHIC_INDICATORS_FULL.xlsx'

# Chemin où sauvegarder le fichier CSV intermédiaire
OUTPUT_CSV_PATH = 'un_data_benin_raw.csv'

# Le numéro de ligne qui contient les en-têtes (identifié après inspection)
HEADER_ROW_INDEX = 16

print("Script 4: Démarrage du chargement et filtrage des données des Nations Unies.")

# --- Étape 1: Vérifier que le fichier source existe ---
if not os.path.exists(INPUT_EXCEL_PATH):
    print(f"ERREUR: Le fichier d'entrée '{INPUT_EXCEL_PATH}' n'a pas été trouvé.")
    sys.exit(1)

# --- Étape 2: Charger les données en spécifiant la ligne d'en-tête ---
try:
    print(f"Chargement de la feuille 'Estimates' depuis '{INPUT_EXCEL_PATH}'...")
    # On ne charge que la feuille 'Estimates' pour les données historiques
    df_estimates = pd.read_excel(INPUT_EXCEL_PATH, sheet_name='Estimates', header=HEADER_ROW_INDEX)
    print("Fichier Excel chargé avec succès.")

except Exception as e:
    print(f"ERREUR: Impossible de lire le fichier Excel. Détails : {e}")
    sys.exit(1)

# --- Étape 3: Filtrer les données pour ne conserver que le Bénin ---
try:
    # Nom exact de la colonne contenant les noms de pays
    location_col = 'Region, subregion, country or area *'
    
    print(f"Filtrage des données pour 'Benin'...")
    df_estimates_benin = df_estimates[df_estimates[location_col] == 'Benin'].copy()
    
    if df_estimates_benin.empty:
        print("AVERTISSEMENT: Aucune donnée trouvée pour 'Benin'. Le script va s'arrêter.")
        sys.exit(0)
        
    print(f"Filtrage réussi. {len(df_estimates_benin)} lignes trouvées pour le Bénin.")

except KeyError:
    print(f"ERREUR: La colonne '{location_col}' n'a pas été trouvée.")
    print("Vérifiez que la ligne d'en-tête et que le nom de la colonne sont corrects.")
    sys.exit(1)

# --- Étape 4: Sauvegarder le résultat intermédiaire ---
df_estimates_benin.to_csv(OUTPUT_CSV_PATH, index=False)
print("\nScript terminé.")
print(f"Les données brutes pour le Bénin ont été sauvegardées dans : '{OUTPUT_CSV_PATH}'")