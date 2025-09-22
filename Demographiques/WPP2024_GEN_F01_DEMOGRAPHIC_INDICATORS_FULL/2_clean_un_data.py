# ==============================================================================
# TÂCHE 1 : ÉTAPE 5 — NETTOYAGE ET TRANSFORMATION DES DONNÉES ONU
# Projet : ANIP AI/Data Challenge 2025
# Objectif : Lire les données brutes extraites pour le Bénin, les nettoyer,
#            sélectionner les colonnes pertinentes, renommer les en-têtes,
#            et convertir les unités pour créer un dataset final propre.
# Source : Fichier un_data_benin_raw.csv (généré par le script 4)
# Auteur : SOULE Fadile
# Date : 21/09/25
# ==============================================================================

import pandas as pd
import os
import sys

# --- CONFIGURATION ---
# Chemin vers le fichier CSV brut généré par le script précédent
INPUT_CSV_PATH = 'un_data_benin_raw.csv'

# Chemin où sauvegarder le dataset final, nettoyé et prêt à l'analyse
OUTPUT_CLEANED_CSV_PATH = 'un_demographic_indicators_benin_cleaned.csv'

print("Script 5: Démarrage du nettoyage et de la transformation des données des Nations Unies.")

# --- Étape 1: Vérifier et charger le fichier source ---
if not os.path.exists(INPUT_CSV_PATH):
    print(f"ERREUR: Le fichier d'entrée '{INPUT_CSV_PATH}' n'a pas été trouvé.")
    print("Veuillez d'abord exécuter le script '4_load_un_data.py'.")
    sys.exit(1)

df_raw_benin = pd.read_csv(INPUT_CSV_PATH)
print("Fichier de données brutes pour le Bénin chargé.")

# --- Étape 2: Sélectionner et renommer les colonnes d'intérêt ---
try:
    # Liste des colonnes originales que nous souhaitons conserver
    columns_to_keep = [
        'Region, subregion, country or area *',
        'Year',
        'Total Population, as of 1 July (thousands)',
        'Population Density, as of 1 July (persons per square km)',
        'Life Expectancy at Birth, both sexes (years)'
    ]
    df_cleaned = df_raw_benin[columns_to_keep].copy()

    # Dictionnaire pour renommer les colonnes avec des noms simples et standardisés
    rename_dict = {
        'Region, subregion, country or area *': 'pays',
        'Year': 'annee',
        'Total Population, as of 1 July (thousands)': 'population_nationale_un',
        'Population Density, as of 1 July (persons per square km)': 'densite_nationale_un',
        'Life Expectancy at Birth, both sexes (years)': 'esperance_vie_un'
    }
    df_cleaned.rename(columns=rename_dict, inplace=True)
    print("Colonnes sélectionnées et renommées.")

except KeyError as e:
    print(f"ERREUR: La colonne {e} n'a pas été trouvée dans le fichier source.")
    sys.exit(1)

# --- Étape 3: Nettoyer les données et convertir les unités ---
# Convertir la population de 'milliers' en unité (ex: 2258.5 -> 2258500)
df_cleaned['population_nationale_un'] = (df_cleaned['population_nationale_un'] * 1000).astype(int)

# Convertir l'année en un nombre entier (ex: 1951.0 -> 1951)
df_cleaned['annee'] = df_cleaned['annee'].astype(int)

# S'assurer qu'il n'y a pas de valeurs manquantes dans les colonnes clés
df_cleaned.dropna(subset=['annee', 'population_nationale_un'], inplace=True)
print("Unités converties et types de données corrigés.")

# --- Étape 4: Sauvegarder le dataset final nettoyé ---
df_cleaned.to_csv(OUTPUT_CLEANED_CSV_PATH, index=False)

print("\nScript terminé.")
print(f"Le dataset nettoyé a été sauvegardé dans : '{OUTPUT_CLEANED_CSV_PATH}'")
print("\nAperçu du dataset final :")
print(df_cleaned.head())