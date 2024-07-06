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
    ,"nom_operateur": "Nom opérateur"
    ,"nom_enseigne": "Nom enseigne"
    ,"mis_en_service_cette_annee": "Mise en service en 2023"
    ,"date_mise_en_service": "Date de mise en service"
    ,"puissance_nominale_cat": "Puissance nominale"
    ,"prise_type_combo_ccs": "Possède une prise combo"
    ,"prise_type_2": "Possède une prise type 2"
}

# borne de recharge
df = pd.read_csv(
    ".\data\consolidation-etalab-schema-irve-statique-v-2.3.1-20240705.csv",
    low_memory=False
    ,parse_dates=["date_mise_en_service"]
    ,dtype={"consolidated_code_postal": str
                       })\
  .sort_values(['id_pdc_itinerance', 'last_modified'])\

# Département
df_dep = pd.read_csv(
    ".\data\departements-france.csv"
    ,dtype={"code_departement": str
                        })

# Ajout d'une colonne 'code_departement' à partir de 'consolidated_code_postal'
df["code_departement"] = df["consolidated_code_postal"].str[:2]

# Join des deux tables sur la colonne 'code_departement'
df = pd.merge(df,df_dep, how='left', on='code_departement')

df_filter = df["id_pdc_itinerance"]=="Non concerné"

df = pd.concat([
  df[~df_filter].drop_duplicates('id_pdc_itinerance', keep='last'),
  df[df_filter]
])

# Date de mise en service
# Remplacer les valeurs de mise en service avant 2010 par None
df.loc[df["date_mise_en_service"]<pd.to_datetime("2010-01-01"),"date_mise_en_service"]=None
# Vérifier si la mise en service a eu lieu en 2024 en ajoutant une colonne 'mis_en_service_cette_annee'
df["mis_en_service_cette_annee"] = np.where(df["date_mise_en_service"].dt.year==pd.to_datetime("2024-01-01").year
         , "Oui"
         , "Non")

# Power
# Normaliser les valeurs de la puissance et les catégoriser
df["puissance_nominale_cat"] = pd.cut(\
  df["puissance_nominale"].apply(lambda x: x/1000 if x >1000 else x)\
,[0,1.8,3.5,7.5,26,52,151,500]
,labels=["1.7","3.4","7.5","22","50","150",">150"]
, include_lowest=False)

# les types de prise
df["prise_type_combo_ccs"] = (df["prise_type_combo_ccs"].str.lower().map
                      ({"0":"Non","false":"Non","1":"Oui","true":"Oui"}))
df["prise_type_2"] = (df["prise_type_2"].str.lower().map
                      ({"0":"Non","false":"Non","1":"Oui","true":"Oui"}))
