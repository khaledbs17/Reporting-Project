# Reporting Project :  Infrastructure des bornes de recharge en France

## Description
Ce projet a pour objectif l'analyse de l'infrastructure des bornes de recharge des véhicules électriques.

## Table des matières
- **main_file** : une brève analyse des données avec les premiers traitements (normalisation de la puissance nominale, mapping entre les deux tables qui se trouvent dans le dossier `data`, etc.).
- **notebook_borne** : l'analyse des points de charge au fil des années.
- **notebook_actors** : l'analyse des différents acteurs (aménageurs, opérateurs, enseignes).
- **notebook_location** : l'analyse de la répartition des points de charge dans les différents emplacements (région, département).
- **notebook_puissance** : l'analyse des caractéristiques électriques (puissance, type de prise, etc.) des bornes de recharge.

## Jeux de données : 
- consolidation-etalab-schema-irve-statique-v-2.3.1-20240705.csv : données relatives à la localisation géographique et aux caractèriqtiques techniques des stations et des points de recharge de véhicules électriques.
- departements-france.csv :  données relatives aux départements et région de France
  ### Quelques informations sur quelques colonnes de la base de données :
  - Point de charge =  PDC. Le PDC a un id_pdc_itenerance
  - Le PDC est rattaché a une seule station de recharge id_station_itinerance
  - Chaque station a une localisation : coordonnéesXY
  -  Aménageurs - propriétaire des infrastructures.
  - Opérateurs - la personne qui exploite l'infrastructure de recharge
  - Enseigne - Le nom commercial du réseau.
  - Puissance nominale : les voitures ont des batteries de plus en plus capacitaires, et elles sont capables d'absorber de plus en plus de puissance. Pour répondre à ce besoin l'infrastructure s'adapte avec le          nouveau standard - CCS2 capable de déliverer encore plus de puissance et réduire le temps de charge
