# ==============================================================================
# TÂCHE 1 : ÉTAPE 1 — TÉLÉCHARGEMENT DES DONNÉES DE POPULATION
# Projet : ANIP AI/Data Challenge 2025
# Objectif : Télécharger les fichiers raster GeoTIFF de population pour le Bénin
#            à partir du hub de données WorldPop.
# Source : https://hub.worldpop.org/
# Auteur : SOULE Fadile
# Date : 21/09/25
# ==============================================================================

import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse
from tqdm import tqdm
import sys

# --- CONFIGURATION ---
# Définir la plage d'IDs des pages de données à télécharger
START_ID = 73172  # ID de la première page
END_ID = 73157    # ID de la dernière page
BASE_URL = "https://hub.worldpop.org/geodata/summary?id="

# Dossier de destination pour les fichiers .tif téléchargés
OUTPUT_DIR = "downloaded_tifs"

print("Script 1: Démarrage du téléchargement des données de population de WorldPop.")

# --- Étape 1: Préparation de l'environnement ---
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Étape 2: Génération des URLs à scraper ---
page_urls = [f"{BASE_URL}{id_num}" for id_num in range(START_ID, END_ID - 1, -1)]
print(f"Génération de {len(page_urls)} URLs à traiter (ID de {START_ID} à {END_ID}).")

# --- Étape 3: Boucle de scraping et de téléchargement ---
print(f"Début du processus de téléchargement vers le dossier '{OUTPUT_DIR}'...")
for page_url in tqdm(page_urls, desc="Progression des pages"):
    try:
        # Extraire le lien du fichier .tif depuis la page de résumé
        response = requests.get(page_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        files_div = soup.find('div', id='files')
        if not files_div:
            print(f"AVERTISSEMENT: Section de fichiers introuvable sur {page_url}")
            continue

        link_tag = files_div.find('a', href=True)
        if not link_tag or not link_tag['href'].endswith('.tif'):
            print(f"AVERTISSEMENT: Lien de téléchargement .tif introuvable sur {page_url}")
            continue
            
        tif_url = link_tag['href'].strip()
        
        # Préparer le téléchargement du fichier
        filename = os.path.basename(urlparse(tif_url).path)
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        if os.path.exists(filepath):
            continue  # Ignorer si le fichier existe déjà

        # Télécharger le fichier en mode stream pour gérer les gros fichiers
        with requests.get(tif_url, stream=True) as r:
            r.raise_for_status()
            with open(filepath, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
                    
    except requests.exceptions.RequestException as e:
        print(f"ERREUR: Impossible de traiter l'URL {page_url}. Détails: {e}")

print("\nScript terminé.")
print(f"Les fichiers TIF ont été téléchargés dans : '{OUTPUT_DIR}'")