# Glossaire des Variables - Challenge ANIP (Tâche 1)

**Projet :** ANIP AI/Data Challenge 2025
**Auteur :** SOULE Fadile
**Date :** 21/09/25

Ce document constitue le dictionnaire des variables pour tous les datasets consolidés produits durant la Tâche 1. Il détaille la définition, l'unité, la source, la période et le niveau de désagrégation géographique de chaque variable.

---

### 1. Données Démographiques (Niveau Départemental)
*   **Dataset source :** `population_par_departement_benin.csv` (produit par `3_aggregate_population_data.py`)
*   **Description :** Ce jeu de données contient les estimations de la population totale pour chaque département du Bénin, agrégées à partir de données raster à haute résolution.

| Nom de la Variable | Définition | Unité | Source | Période | Géographie |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `departement` | Nom officiel de l'un des 12 départements de la République du Bénin. | Texte | Natural Earth | N/A | Département |
| `population_AAAA` | Estimation de la population totale résidente pour l'année spécifiée (AAAA). | Habitants (nombre) | WorldPop | 2015 - 2030 | Département |

---

### 2. Indicateurs Démographiques (Niveau National)
*   **Dataset source :** `un_demographic_indicators_benin_cleaned.csv` (produit par `5_clean_un_data.py`)
*   **Description :** Ce jeu de données contient les indicateurs démographiques clés pour le Bénin au niveau national, basés sur les estimations historiques des Nations Unies.

| Nom de la Variable | Définition | Unité | Source | Période | Géographie |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `pays` | Le pays concerné par les indicateurs (Bénin). | Texte | UN WPP 2024 | 1950 - 2023 | National |
| `annee` | L'année de référence pour l'indicateur. | Année (entier) | UN WPP 2024 | 1950 - 2023 | National |
| `population_nationale_un` | Population totale du pays au 1er juillet de l'année. | Habitants (nombre) | UN WPP 2024 | 1950 - 2023 | National |
| `densite_nationale_un` | Densité de la population au 1er juillet de l'année. | Personnes / km² | UN WPP 2024 | 1950 - 2023 | National |
| `esperance_vie_un` | Espérance de vie à la naissance pour les deux sexes combinés. | Années | UN WPP 2024 | 1950 - 2023 | National |

---

### 3. Indicateurs Sociaux et Sanitaires (Niveau National)
*   **Dataset source :** `dhs_indicators_benin_api.csv` (produit par `6_collect_dhs_api_data.py`)
*   **Description :** Ce jeu de données contient des indicateurs sociaux et sanitaires clés, collectés lors des Enquêtes Démographiques et de Santé (DHS) au Bénin. La période est discontinue car elle dépend des années de réalisation des enquêtes.

| Nom de la Variable | Définition | Unité | Source | Période | Géographie |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `annee` | L'année de l'enquête DHS de référence. | Année (entier) | DHS Program API | Discontinue | National |
| `pct_menages_electricite` | Pourcentage de ménages ayant accès à l'électricité. | Pourcentage (%) | DHS Program API | Discontinue | National |
| `pct_alphab_femmes` | Pourcentage de femmes (âgées de 15 à 49 ans) qui savent lire et écrire. | Pourcentage (%) | DHS Program API | Discontinue | National |
| `tx_mortalite_infantile` | Taux de mortalité infantile : décès d'enfants de moins d'un an pour 1000 naissances vivantes. | Taux pour 1000 naissances | DHS Program API | Discontinue | National |
| `pct_acces_eau_potable` | Pourcentage de ménages utilisant une source d'eau potable améliorée. | Pourcentage (%) | DHS Program API | Discontinue | National |

---

### 4. Indicateurs sur l'Éducation (Niveau National)
*   **Dataset source :** `education_indicators_benin_consolidated.csv` (produit par `7_collect_world_bank_education_data.py`)
*   **Description :** Ce jeu de données consolide plusieurs indicateurs sur le système éducatif primaire au Bénin. Les données sont annuelles mais peuvent être manquantes pour certaines années.

| Nom de la Variable | Définition | Unité | Source | Période | Géographie |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `annee` | L'année de référence pour les indicateurs. | Année (entier) | Banque Mondiale | 1971 - 2021 (discontinue) | National |
| `tx_scolarisation_primaire_brut` | Taux brut de scolarisation dans le primaire, tous sexes. Peut dépasser 100%. | Pourcentage (%) | Banque Mondiale | 1971 - 2021 (discontinue) | National |
| `tx_scolarisation_primaire_feminin` | Taux brut de scolarisation des filles dans l'enseignement primaire. | Pourcentage (%) | Banque Mondiale | 1971 - 2021 (discontinue) | National |
| `pct_enseignants_formes` | Pourcentage d'enseignants du primaire (tous sexes) ayant reçu la formation pédagogique minimale requise. | Pourcentage (%) | Banque Mondiale | 1971 - 2021 (discontinue) | National |
| `pct_enseignantes_formees` | Pourcentage d'enseignantes du primaire ayant reçu la formation pédagogique minimale requise. | Pourcentage (%) | Banque Mondiale | 1971 - 2021 (discontinue) | National |
| `pct_enseignants_hommes_formes` | Pourcentage d'enseignants (hommes) du primaire ayant reçu la formation pédagogique minimale requise. | Pourcentage (%) | Banque Mondiale | 1971 - 2021 (discontinue) | National |
| `tx_persistance_primaire_masculin`| Pourcentage de garçons d'une cohorte qui atteignent la dernière année du primaire. | Pourcentage (%) | Banque Mondiale | 1971 - 2021 (discontinue) | National |