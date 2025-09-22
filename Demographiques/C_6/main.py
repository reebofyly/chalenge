# =========================================================
# TÂCHE 1 : COLLECTE ET PRÉPARATION DES DONNÉES
# Projet : ANIP AI/Data Challenge 2025
# Objectif : Télécharger, nettoyer et structurer les données de persistance scolaire des garçons jusqu'à la dernière année du primaire au Bénin
# Source : Banque Mondiale - Indicateur SE.PRM.PRSL.MA.ZS (https://api.worldbank.org/v2/en/indicator/SE.PRM.PRSL.MA.ZS?downloadformat=csv)
# Auteur : SOULE Fadile
# Date : 20/09/25
# =========================================================


import pandas as pd
import requests
import zipfile
import io
import os

# === Configuration des chemins ===
DATA_RAW_DIR = "/content/data/raw"
DATA_CLEANED_DIR = "/content/data/cleaned"

# Création des répertoires si nécessaire
os.makedirs(DATA_RAW_DIR, exist_ok=True)
os.makedirs(DATA_CLEANED_DIR, exist_ok=True)

# === ÉTAPE 1 : Définition de l’indicateur et de l’URL ===
indicator_code = "SE.PRM.PRSL.MA.ZS"  # Persistance jusqu'à la dernière année du primaire, hommes (% de la cohorte)
url = f"https://api.worldbank.org/v2/en/indicator/{indicator_code}?downloadformat=csv"

print(f"Téléchargement du fichier ZIP pour l'indicateur : {indicator_code}")
response = requests.get(url)
response.raise_for_status()  # Lève une exception en cas d'erreur HTTP

# Sauvegarde locale du fichier ZIP
zip_path = os.path.join(DATA_RAW_DIR, f"wb_persistence_male_primary_benin.zip")
with open(zip_path, "wb") as f:
    f.write(response.content)

print(f"Fichier ZIP téléchargé : {zip_path}")

# === ÉTAPE 2 : Extraction des fichiers contenus dans le ZIP ===
print("Extraction des fichiers du ZIP...")

with zipfile.ZipFile(zip_path, "r") as z:
    file_list = z.namelist()
    print("Fichiers contenus dans le ZIP :")
    for filename in file_list:
        print(f"  - {filename}")

    # Recherche du fichier de données principal (non métadonnées)
    data_file = None
    for filename in file_list:
        if filename.startswith(f"API_{indicator_code}") and "Metadata" not in filename and filename.endswith(".csv"):
            data_file = filename
            break

    if not data_file:
        raise FileNotFoundError(
            f"Aucun fichier de données principal (CSV) trouvé dans le ZIP pour l'indicateur {indicator_code}. "
            "Vérifiez le code indicateurs ou le fichier téléchargé."
        )

    print(f"Fichier de données identifié : {data_file}")

    # Extraction du fichier CSV dans le dossier raw
    z.extract(data_file, DATA_RAW_DIR)

# === ÉTAPE 3 : Chargement du fichier CSV avec saut des lignes d'en-tête ===
csv_path = os.path.join(DATA_RAW_DIR, data_file)
print(f"Chargement du fichier CSV : {csv_path}")

# Les 4 premières lignes sont des métadonnées ; elles doivent être ignorées
df = pd.read_csv(csv_path, skiprows=4)

print(f"Dimensions du jeu de données : {df.shape[0]} pays × {df.shape[1]} colonnes")

# === ÉTAPE 4 : Filtrage des données pour le Bénin ===
benin_data = df[df["Country Name"] == "Benin"].copy()

if benin_data.empty:
    raise ValueError("Aucune donnée trouvée pour le Bénin. Vérifiez le code pays ou le fichier source.")

print(f"Données du Bénin extraites : {len(benin_data)} ligne(s)")

# === ÉTAPE 5 : Sélection des années et préparation des colonnes ===
# Définir la plage d'années couverte (1970 à 2023 — période cohérente avec les autres indicateurs)
years = [str(year) for year in range(1970, 2024)]

# Colonnes nécessaires : identifiants + années
cols_to_keep = [
    "Country Name",
    "Country Code",
    "Indicator Name",
    "Indicator Code"
] + years

df_benin_clean = benin_data[cols_to_keep]

# === ÉTAPE 6 : Transformation du format large en format long ===
df_benin_long = df_benin_clean.melt(
    id_vars=["Country Name", "Country Code", "Indicator Name", "Indicator Code"],
    var_name="Année",
    value_name="Persistance_Scolaire_Garcons_Primaire"
)

print(f"Format transformé : {len(df_benin_long)} lignes après pivotage")

# === ÉTAPE 7 : Nettoyage des données ===
# Conversion de la colonne Année en entier
df_benin_long["Année"] = pd.to_numeric(df_benin_long["Année"], errors="coerce")

# Suppression des valeurs manquantes pour le taux de persistance
df_benin_long = df_benin_long.dropna(subset=["Persistance_Scolaire_Garcons_Primaire"])

# Conservation uniquement des colonnes essentielles
df_benin_final = df_benin_long[[
    "Country Name",
    "Country Code",
    "Année",
    "Persistance_Scolaire_Garcons_Primaire"
]]

# Vérification finale des types
df_benin_final["Année"] = df_benin_final["Année"].astype(int)

print(f"Données nettoyées : {len(df_benin_final)} observations valides")
print(f"Période couverte : {df_benin_final['Année'].min()} à {df_benin_final['Année'].max()}")

# === ÉTAPE 8 : Sauvegarde du jeu de données final ===
output_path = os.path.join(DATA_CLEANED_DIR, "wb_persistence_male_primary_benin.csv")
df_benin_final.to_csv(output_path, index=False, encoding="utf-8")

print(f"Fichier final sauvegardé : {output_path}")

# === ÉTAPE 9 : Aperçu des premières et dernières lignes ===
print("\nAperçu des 10 premières lignes :")
print(df_benin_final.head(10).to_string(index=False))

print("\nAperçu des 10 dernières lignes :")
print(df_benin_final.tail(10).to_string(index=False))