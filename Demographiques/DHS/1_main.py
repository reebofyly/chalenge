# ==============================================================================
# SCRIPT D'EXPLORATION : DÉCOUVERTE DES INDICATEURS DHS POUR LE BÉNIN
# Objectif : Utiliser une route API générale pour lister tous les indicateurs
#            disponibles pour le Bénin afin d'identifier de nouvelles
#            variables pertinentes pour l'analyse.
# ==============================================================================

import requests
import pandas as pd

# URL directe pour toutes les données du Bénin
url = "https://api.dhsprogram.com/rest/dhs/data/BJ?perPage=5000"
print("Interrogation de l'API pour l'ensemble des données du Bénin...")

try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    if 'Data' in data and data['Data']:
        print(f"Réponse reçue. {len(data['Data'])} points de données trouvés au total.")
        
        # Convertir en DataFrame pour une exploration facile
        df_full = pd.DataFrame(data['Data'])
        
        # --- Exploration des indicateurs disponibles ---
        print("\n--- Analyse des indicateurs uniques disponibles ---")
        
        # Grouper par ID d'indicateur et nom pour voir tout ce qui est disponible
        unique_indicators = df_full[['IndicatorId', 'Indicator']].drop_duplicates().sort_values('Indicator')
        
        print(f"{len(unique_indicators)} indicateurs uniques ont été trouvés pour le Bénin.")
        
        print("\nExtrait de la liste des indicateurs disponibles :")
        # 'display' est utilisé pour un meilleur affichage dans les notebooks
        display(unique_indicators.head(15))
        
        # Sauvegarder la liste complète pour référence future
        unique_indicators.to_csv('dhs_liste_indicateurs_benin.csv', index=False)
        print("\nLa liste complète de tous les indicateurs a été sauvegardée dans 'dhs_liste_indicateurs_benin.csv'")

except requests.exceptions.RequestException as e:
    print(f"ERREUR: La requête a échoué. Détails : {e}")