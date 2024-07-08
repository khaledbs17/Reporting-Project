import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import pathlib
import kaleido
import plotly.express as px
import plotly.io as pio

from IPython.display import display, Markdown

pd.set_option('future.no_silent_downcasting', True)

# labéliser les colonnes pour les visuels
labels = {
    "nom_amenageur": "Nom amenageur"
    , "nom_operateur": "Nom opérateur"
    , "nom_enseigne": "Nom enseigne"
    , "mis_en_service_cette_annee": "Mise en service en 2023"
    , "date_mise_en_service": "Date de mise en service"
    , "puissance_nominale_cat": "Puissance nominale"
    , "prise_type_combo_ccs": "Possède une prise combo"
    , "prise_type_2": "Possède une prise type 2"
}

# borne de recharge
df = pd.read_csv(
    ".\data\consolidation-etalab-schema-irve-statique-v-2.3.1-20240705.csv",
    low_memory=False
    , parse_dates=["date_mise_en_service"]
    , dtype={"consolidated_code_postal": str
             }) \
    .sort_values(['id_pdc_itinerance', 'last_modified']) \
 \
# Département
df_dep = pd.read_csv(
    ".\data\departements-france.csv"
    , dtype={"code_departement": str
             })

# Suppression des colonnes qui ont plus que 50% des données manquantes
df = df.drop(columns=['id_pdc_local', 'observations', 'cable_t2_attache', 'tarification', 'num_pdl'])

# Suppression des colonnes qui ne peuvent pas etre remplises () et surtout ils ont une pourcentage importante manquante
df = df.drop(columns=['id_station_local'])

# le pourcentage des valeurs manquantes dans les colonnes suivantes est faible
df.dropna(subset=['contact_amenageur', 'telephone_operateur'], inplace=True)

# Id des PDC
df_filter = df["id_pdc_itinerance"] == "Non concerné"

df = pd.concat([
    df[~df_filter].drop_duplicates('id_pdc_itinerance', keep='last'),
    df[df_filter]
])

# Date de mise en service
# Remplacer les valeurs de mise en service avant 2010 par None
df.loc[df["date_mise_en_service"] < pd.to_datetime("2010-01-01"), "date_mise_en_service"] = None
# Vérifier si la mise en service a eu lieu en 2024 en ajoutant une colonne 'mis_en_service_cette_annee'
df["mis_en_service_cette_annee"] = np.where(df["date_mise_en_service"].dt.year == pd.to_datetime("2024-01-01").year
                                            , "Oui"
                                            , "Non")

# Power
# Normaliser les valeurs de la puissance et les catégoriser
df["puissance_nominale_cat"] = pd.cut( \
    df["puissance_nominale"].apply(lambda x: x / 1000 if x > 1000 else x) \
    , [0, 1.8, 3.5, 7.5, 26, 52, 151, 500]
    , labels=["1.7", "3.4", "7.5", "22", "50", "150", ">150"]
    , include_lowest=False)

# les types de prise
df["prise_type_combo_ccs"] = (df["prise_type_combo_ccs"].str.lower().map
                              ({"0": "Non", "false": "Non", "1": "Oui", "true": "Oui"}))
df["prise_type_2"] = (df["prise_type_2"].str.lower().map
                      ({"0": "Non", "false": "Non", "1": "Oui", "true": "Oui"}))
# les types de paiment
df["paiement_autre"] = (df["paiement_autre"].str.lower().map
                        ({"0": "FALSE", "false": "FALSE", "False": "FALSE", "1": "TRUE", "true": "TRUE",
                          "True": "TRUE"}))
df["paiement_cb"] = (df["paiement_cb"].str.lower().map
                     ({"0": "FALSE", "false": "FALSE", "False": "FALSE", "1": "TRUE", "true": "TRUE", "True": "TRUE"}))

df["gratuit"] = (df["gratuit"].str.lower().map
                 ({"0": "FALSE", "false": "FALSE", "False": "FALSE", "1": "TRUE", "true": "TRUE", "True": "TRUE"}))

# Ajout d'une colonne 'code_departement' à partir de 'consolidated_code_postal'
df["code_departement"] = df["consolidated_code_postal"].str[:2]

# Join des deux tables sur la colonne 'code_departement'
df = pd.merge(df, df_dep, how='left', on='code_departement')


# le but de la fonction c'est de remplacer les valeurs nan par des randoms values pour les remplir
def replace_nan_with_random(df, column):
    # Sélectionner les valeurs non manquantes
    non_nan_values = df[column].dropna().unique()
    # Générer des valeurs aléatoires pour remplacer les NaN
    random_values = np.random.choice(non_nan_values, size=df[column].isna().sum(), replace=True)
    # Remplacer les NaN par les valeurs aléatoires générées
    df.loc[df[column].isna(), column] = random_values


# Remplacer les valeurs NaN par des valeurs aléatoires pour chaque colonne spécifiée
for column in ['paiement_cb', 'paiement_autre', 'raccordement']:
    replace_nan_with_random(df, column)
