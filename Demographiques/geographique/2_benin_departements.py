# ==============================================================================
# TÂCHE 1 : ÉTAPE 2 — PRÉPARATION DES LIMITES ADMINISTRATIVES
# Projet : ANIP AI/Data Challenge 2025
# Objectif : Télécharger un shapefile des divisions administratives, l'extraire,
#            et le filtrer pour créer un fichier contenant uniquement les
#            limites des départements du Bénin.
# Source : https://www.naturalearthdata.com/
# Auteur : SOULE Fadile
# Date : 21/09/25
# ==============================================================================

import requests
import zipfile
import os
import geopandas as gpd
import sys

# --- CONFIGURATION ---
SHAPEFILE_URL = "https://naturalearth.s3.amazonaws.com/10m_cultural/ne_10m_admin_1_states_provinces.zip"
OUTPUT_DIR = "shapes_data"
RAW_SHAPEFILE_NAME = "ne_10m_admin_1_states_provinces.shp"
FINAL_SHAPEFILE_NAME = "benin_departments.shp"

print("Script 2: Démarrage de la préparation des limites administratives du Bénin.")

# --- Étape 1: Téléchargement et extraction du shapefile mondial ---
os.makedirs(OUTPUT_DIR, exist_ok=True)
zip_path = os.path.join(OUTPUT_DIR, "world_admin_boundaries.zip")

try:
    print(f"Téléchargement du shapefile depuis {SHAPEFILE_URL}...")
    response = requests.get(SHAPEFILE_URL, timeout=30)
    response.raise_for_status()
    with open(zip_path, "wb") as f:
        f.write(response.content)

    print(f"Extraction des fichiers nécessaires depuis '{zip_path}'...")
    with zipfile.ZipFile(zip_path, "r") as z:
        for file in z.namelist():
            if file.endswith(('.shp', '.dbf', '.prj', '.shx')):
                z.extract(file, OUTPUT_DIR)
    print("Extraction terminée.")

except requests.exceptions.RequestException as e:
    print(f"ERREUR: Le téléchargement a échoué. Détails: {e}")
    sys.exit(1)

# --- Étape 2: Filtrage pour isoler les départements du Bénin ---
raw_shapefile_path = os.path.join(OUTPUT_DIR, RAW_SHAPEFILE_NAME)
try:
    print(f"Chargement du shapefile mondial depuis '{raw_shapefile_path}'...")
    world_gdf = gpd.read_file(raw_shapefile_path)
    
    print("Filtrage pour ne conserver que les départements du Bénin...")
    benin_departments = world_gdf[world_gdf['admin'] == 'Benin'].copy()

    if benin_departments.empty:
        print("AVERTISSEMENT: Aucun département trouvé pour le Bénin dans le fichier source.")
        sys.exit(0)

    # --- Étape 3: Sauvegarde du shapefile filtré ---
    final_shapefile_path = os.path.join(OUTPUT_DIR, FINAL_SHAPEFILE_NAME)
    benin_departments.to_file(final_shapefile_path, encoding='utf-8')
    print(f"Shapefile du Bénin sauvegardé avec succès.")

except Exception as e:
    print(f"ERREUR: Le traitement du shapefile a échoué. Détails: {e}")
    sys.exit(1)

print("\nScript terminé.")
print(f"Le shapefile des départements du Bénin est disponible ici : '{final_shapefile_path}'")