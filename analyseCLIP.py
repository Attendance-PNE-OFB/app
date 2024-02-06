import json
import pandas as pd
from extractMetadata import extract_metadata, dictionary_to_json

# Créer le fichier JSON en récupérant les métadonnées des images
#dictionary_to_json(extract_metadata('~/media/aurelien/COSTE EXT/PROJET_DATA/20200709_20200802/101_BTCF'))

# Charger le fichier JSON
with open('output_json/metadata.json', 'r') as json_file:
    json_data = json.load(json_file)

# Charger les données et les transformer en dictionnaire
donnees = {
    'man': 2150,
    'women': 761,
    '0-15': 839,
    '15-35': 4,
    '35-60': 2067,
    '60-100': 1,
    'hiker': 2766,
    'skier': 0,
    'moutain biker': 145
}

# Créer un dictionnaire à partir des données
dictionnaire = dict(donnees)

# Fonction pour calculer le nombre de personnes pour une image donnée
def calculer_nombre_personnes(image_data):
    sum = 0;
    for x in image_data.get("genre", {}):
        for y in image_data["genre"][x]:
            sum += int(y)
    return sum

# Fonction pour calculer le nombre d'hommes pour une image donnée
def calculer_nombre_hommes(image_data):
    sum = 0;
    for x in image_data.get("genre", {}):
        if x == 'hommes':
            sum += int(image_data["genre"][x])
    return sum

# Fonction pour calculer le nombre de femmes pour une image donnée
def calculer_nombre_femmes(image_data):
    sum = 0;
    for x in image_data.get("genre", {}):
        if x == 'femmes':
            sum += int(image_data["genre"][x])
    return sum

# Fonction pour calculer le nombre de personnes par tranche d'âge
def calculer_nombre_age(json_data):
    sum = [0, 0, 0, 0] #0_15 | 15_35 | 35_60 | 60_100
    for image_name in json_data:
        for x in json_data[image_name].get("age", {}):
            if x=="0-15ans":
                sum[0] += 1
            elif x=="15-35ans":
                sum[1] += 1
            elif x=="35-60ans":
                sum[2] += 1
            elif x==">60ans":
                sum[3] += 1
    return sum

# Fonction pour calculer le nombre de personnes par activités
def calculer_nombre_activite(json_data):
    sum = [0, 0, 0] #hiker | skier | moutain biker
    for image_name in json_data:
        for x in json_data[image_name].get("type", {}):
            if x=="randonnee":
                sum[0] += 1
            elif x=="ski":
                sum[1] += 1
            elif x=="vtt" or x=="vtt-electrique":
                sum[2] += 1
    return sum

# Initialisation des variables pour les calculs
total_humain_json = 0
total_hommes_json = 0
total_femmes_json = 0
total_images = len(json_data)
ages_json = calculer_nombre_age(json_data)
activitee_json = calculer_nombre_activite(json_data)

# Récupérer le nombre d'humain, d'hommes et de femmes par image
for image_name in json_data:
    # Calculer le nombre de personnes pour l'image actuelle
    humains_json = calculer_nombre_personnes(json_data[image_name]) #humains prends aussi en compte les gens annotés comme humain et pas par sexe
    hommes_json = calculer_nombre_hommes(json_data[image_name])
    femmes_json = calculer_nombre_femmes(json_data[image_name])
    # Calculer les sommes
    total_humain_json += humains_json
    total_hommes_json += hommes_json
    total_femmes_json += femmes_json
    

# Calculer les %
if donnees["man"]<total_hommes_json:
    diff_man = donnees["man"]/total_hommes_json
else:  
    diff_man = total_hommes_json/donnees["man"]

if donnees["women"]<total_hommes_json:
    diff_women = donnees["women"]/total_femmes_json
else:  
    diff_women = total_femmes_json/donnees["women"]

try:
    if donnees['0-15']<ages_json[0]:
        diff_ages0_15 = (donnees['0-15']/ages_json[0])
    else:  
        diff_ages0_15 = (ages_json[0]/donnees['0-15'])
except ZeroDivisionError:
    diff_ages0_15 = 1

try:
    if donnees['15-35']<ages_json[1]:
        diff_ages15_35 = (donnees['15-35']/ages_json[1])
    else:  
        diff_ages15_35 = (ages_json[1]/donnees['15-35'])
except ZeroDivisionError:
    diff_ages15_35 = 1

try:
    if donnees['35-60']<ages_json[2]:
        diff_ages35_60 = (donnees['35-60']/ages_json[2])
    else:  
        diff_ages35_60 = (ages_json[2]/donnees['35-60'])
except ZeroDivisionError:
    diff_ages35_60 = 1

try:
    if donnees['60-100']<ages_json[3]:
        diff_ages60_ = (donnees['60-100']/ages_json[3])
    else:  
        diff_ages60_ = (ages_json[3]/donnees['60-100'])
except ZeroDivisionError:
    diff_ages60_ = 1

try:
    if donnees['hiker']<activitee_json[0]:
        diff_hiker = donnees['hiker']/activitee_json[0]
    else:
        diff_hiker = activitee_json[0]/donnees['hiker']
except ZeroDivisionError:
    diff_hiker = 1

try:
    if donnees['skier']<activitee_json[1]:
        diff_skier = donnees['skier']/activitee_json[1]
    else:
        diff_skier = activitee_json[1]/donnees['skier']
except ZeroDivisionError:
    diff_skier = 1

try:
    if donnees['moutain biker']<activitee_json[2]:
        diff_moutain_biker = donnees['moutain biker']/activitee_json[2]
    else:
        diff_moutain_biker = activitee_json[2]/donnees['moutain biker']
except ZeroDivisionError:
    diff_moutain_biker = 1


print("-------------CLIP-------------")
print(f"Pourcentage d'identification de sexe correct : {(diff_man+diff_women)/2}")
print(f"Pourcentage d'identification de tranches d'âge correct : {(diff_ages0_15+diff_ages15_35+diff_ages35_60+diff_ages60_)/4}")
print(f"Pourcentage d'identification d'activitée correcte : {(diff_hiker+diff_skier+diff_moutain_biker)/3}")