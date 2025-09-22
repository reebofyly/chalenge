# ==============================================================================
# TÂCHE 1 : ÉTAPE 3 — AGRÉGATION DES DONNÉES DE POPULATION
# Projet : ANIP AI/Data Challenge 2025
# Objectif : Agréger les données de population raster (GeoTIFF) par département
#            en utilisant le shapefile du Bénin. Le résultat est un fichier CSV
#            contenant la population estimée pour chaque département par année.
# Sources : Sorties des scripts 1 et 2.
# Auteur : SOULE Fadile
# Date : 21/09/25
# ==============================================================================

import rasterio
from rasterio.mask import mask
import geopandas as gpd
import pandas as pd
import os
from tqdm import tqdm
import sys

# --- CONFIGURATION ---
INPUT_RASTER_DIR = "downloaded_tifs"
INPUT_SHAPEFILE_PATH = "shapes_data/benin_departments.shp"
OUTPUT_CSV_PATH = "population_par_departement_benin.csv"

print("Script 3: Démarrage de l'agrégation de la population par département.")

# --- Étape 1: Vérifier et charger les fichiers d'entrée ---
if not os.path.exists(INPUT_SHAPEFILE_PATH):
    print(f"ERREUR: Fichier shapefile '{INPUT_SHAPEFILE_PATH}' non trouvé. Exécutez le script 2.")
    sys.exit(1)
if not os.path.exists(INPUT_RASTER_DIR):
    print(f"ERREUR: Dossier raster '{INPUT_RASTER_DIR}' non trouvé. Exécutez le script 1.")
    sys.exit(1)

try:
    admin_boundaries = gpd.read_file(INPUT_SHAPEFILE_PATH)
    tif_files = sorted([f for f in os.listdir(INPUT_RASTER_DIR) if f.endswith('.tif')])
    if not tif_files:
        print(f"ERREUR: Aucun fichier .tif trouvé dans '{INPUT_RASTER_DIR}'.")
        sys.exit(1)
except Exception as e:
    print(f"ERREUR: Impossible de charger les fichiers d'entrée. Détails: {e}")
    sys.exit(1)

# --- Étape 2: Initialiser le DataFrame de résultats ---
final_df = admin_boundaries[['name', 'geometry']].copy()
final_df.rename(columns={'name': 'departement'}, inplace=True)

# --- Étape 3: Boucle de traitement pour chaque fichier raster ---
for tif_file in tqdm(tif_files, desc="Agrégation de la population par année"):
    filepath = os.path.join(INPUT_RASTER_DIR, tif_file)
    
    try:
        year = next(part for part in tif_file.split('_') if part.isdigit() and len(part) == 4)
        col_name = f"population_{year}"
    except StopIteration:
        col_name = f"population_{os.path.splitext(tif_file)[0]}"
    
    populations = []
    with rasterio.open(filepath) as src:
        # Reprojeter le shapefile si le CRS ne correspond pas
        if admin_boundaries.crs != src.crs:
            admin_boundaries_reprojected = admin_boundaries.to_crs(src.crs)
        else:
            admin_boundaries_reprojected = admin_boundaries
            
        for index, row in admin_boundaries_reprojected.iterrows():
            out_image, out_transform = mask(src, [row.geometry], crop=True, nodata=0)
            population_sum = out_image[0][out_image[0] >= 0].sum()
            populations.append(population_sum)

    final_df[col_name] = populations

# --- Étape 4: Nettoyage final et sauvegarde ---
final_df = final_df.drop(columns='geometry')

# Correction orthographique d'un problème d'encodage connu
if 'OuÃ©mÃ©' in final_df['departement'].values:
    final_df['departement'] = final_df['departement'].str.replace('OuÃ©mÃ©', 'Ouémé')

final_df.to_csv(OUTPUT_CSV_PATH, index=False, encoding='utf-8-sig')

print("\nScript terminé.")
print(f"Le dataset agrégé a été sauvegardé dans : '{OUTPUT_CSV_PATH}'")
print("\nAperçu du dataset final :")
print(final_df.head())