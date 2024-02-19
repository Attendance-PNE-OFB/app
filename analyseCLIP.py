import json

###############################################
############### VARIABLES #####################
###############################################

# Chemin du fichier JSON (chemin absolu ou relatif)
chemin_json = "output_json/metadata_101_BTCF.json"

###############################################
#################### CODE #####################
###############################################

# Charger le fichier JSON
with open(chemin_json, 'r') as json_file:
    json_data = json.load(json_file)

# Saisir les données et les transformer en dictionnaire
donnees = {
    'man': 1682,
    'women': 1229,
    'children': 247,
    'adolescent': 2555,
    'adult': 109,
    'senior': 0,
    'hiker': 2895,
    'skier': 0,
    'bicyclist': 16
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
    if donnees['children']<ages_json[0]:
        diff_ages0_15 = (donnees['children']/ages_json[0])
    else:  
        diff_ages0_15 = (ages_json[0]/donnees['children'])
except ZeroDivisionError:
    diff_ages0_15 = 1

try:
    if donnees['adolescent']<ages_json[1]:
        diff_ages15_35 = (donnees['adolescent']/ages_json[1])
    else:  
        diff_ages15_35 = (ages_json[1]/donnees['adolescent'])
except ZeroDivisionError:
    diff_ages15_35 = 1

try:
    if donnees['adult']<ages_json[2]:
        diff_ages35_60 = (donnees['adult']/ages_json[2])
    else:  
        diff_ages35_60 = (ages_json[2]/donnees['adult'])
except ZeroDivisionError:
    diff_ages35_60 = 1

try:
    if donnees['senior']<ages_json[3]:
        diff_ages60_ = (donnees['senior']/ages_json[3])
    else:  
        diff_ages60_ = (ages_json[3]/donnees['senior'])
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
    if donnees['bicyclist']<activitee_json[2]:
        diff_moutain_biker = donnees['bicyclist']/activitee_json[2]
    else:
        diff_moutain_biker = activitee_json[2]/donnees['bicyclist']
except ZeroDivisionError:
    diff_moutain_biker = 1


print("-------------CLIP-------------")
print(f"Pourcentage d'identification de sexe correct : {(diff_man+diff_women)/2}")
print(f"Pourcentage d'identification de tranches d'âge correct : {(diff_ages0_15+diff_ages15_35+diff_ages35_60+diff_ages60_)/4}")
print(f"Pourcentage d'identification d'activité correcte : {(diff_hiker+diff_skier+diff_moutain_biker)/3}")

###############################################
################### BONUS #####################
###############################################
# Liste exhausitve des outputs que j'ai pu sortir pendant les tests

''' dataset1 -> 101_BTCF
Output avec : categories = ["man", "women", "0-15", "15-35", "35-60", "60-100", "hiker", "skier", "moutain biker"]
Computing time:  207.09778789400025
Nombre d'individus trouvées pour la catégorie 'man': 2150
Nombre d'individus trouvées pour la catégorie 'women': 761
Nombre d'individus trouvées pour la catégorie '0-15': 839
Nombre d'individus trouvées pour la catégorie '15-35': 4
Nombre d'individus trouvées pour la catégorie '35-60': 2067
Nombre d'individus trouvées pour la catégorie '60-100': 1
Nombre d'individus trouvées pour la catégorie 'hiker': 2766
Nombre d'individus trouvées pour la catégorie 'skier': 0
Nombre d'individus trouvées pour la catégorie 'moutain biker': 145

Output avec : categories = ["man", "women", "child", "teen", "adult", "senior", "hiker", "skier", "moutain biker"]
Computing time:  201.71157141999993
Nombre d'individus trouvées pour la catégorie 'man': 2150
Nombre d'individus trouvées pour la catégorie 'women': 761
Nombre d'individus trouvées pour la catégorie 'child': 365
Nombre d'individus trouvées pour la catégorie 'teen': 5
Nombre d'individus trouvées pour la catégorie 'adult': 2538
Nombre d'individus trouvées pour la catégorie 'senior': 3
Nombre d'individus trouvées pour la catégorie 'hiker': 2766
Nombre d'individus trouvées pour la catégorie 'skier': 0
Nombre d'individus trouvées pour la catégorie 'moutain biker': 145

Output avec : categories = ["man", "women", "child", "ado", "adult", "senior", "hiker", "skier", "moutain biker"]
Computing time:  210.3337343609992
Nombre d'individus trouvées pour la catégorie 'man': 2150
Nombre d'individus trouvées pour la catégorie 'women': 761
Nombre d'individus trouvées pour la catégorie 'child': 365
Nombre d'individus trouvées pour la catégorie 'ado': 0
Nombre d'individus trouvées pour la catégorie 'adult': 2543
Nombre d'individus trouvées pour la catégorie 'senior': 3
Nombre d'individus trouvées pour la catégorie 'hiker': 2766
Nombre d'individus trouvées pour la catégorie 'skier': 0
Nombre d'individus trouvées pour la catégorie 'moutain biker': 145

Output avec : categories = ["man", "women", "child", "adolescent", "adult", "senior", "hiker", "skier", "moutain biker"]
Computing time:  202.38966674999938
Nombre d'individus trouvées pour la catégorie 'man': 2150
Nombre d'individus trouvées pour la catégorie 'women': 761
Nombre d'individus trouvées pour la catégorie 'child': 23
Nombre d'individus trouvées pour la catégorie 'adolescent': 2771
Nombre d'individus trouvées pour la catégorie 'adult': 116
Nombre d'individus trouvées pour la catégorie 'senior': 1
Nombre d'individus trouvées pour la catégorie 'hiker': 2766
Nombre d'individus trouvées pour la catégorie 'skier': 0
Nombre d'individus trouvées pour la catégorie 'moutain biker': 145

Output avec : categories = ["man", "women", "child", "teenager", "adult", "senior", "hiker", "skier", "moutain biker"]
Computing time:  202.6587808410004
Nombre d'individus trouvées pour la catégorie 'man': 2150
Nombre d'individus trouvées pour la catégorie 'women': 761
Nombre d'individus trouvées pour la catégorie 'child': 354
Nombre d'individus trouvées pour la catégorie 'teenager': 21
Nombre d'individus trouvées pour la catégorie 'adult': 2533
Nombre d'individus trouvées pour la catégorie 'senior': 3
Nombre d'individus trouvées pour la catégorie 'hiker': 2766
Nombre d'individus trouvées pour la catégorie 'skier': 0
Nombre d'individus trouvées pour la catégorie 'moutain biker': 145

Output avec : categories = ["man", "women", "children", "teen", "adult", "senior", "hiker", "skier", "moutain biker"]
Computing time:  205.42920508499992
Nombre d'individus trouvées pour la catégorie 'man': 2150
Nombre d'individus trouvées pour la catégorie 'women': 761
Nombre d'individus trouvées pour la catégorie 'children': 587
Nombre d'individus trouvées pour la catégorie 'teen': 3
Nombre d'individus trouvées pour la catégorie 'adult': 2319
Nombre d'individus trouvées pour la catégorie 'senior': 2
Nombre d'individus trouvées pour la catégorie 'hiker': 2766
Nombre d'individus trouvées pour la catégorie 'skier': 0
Nombre d'individus trouvées pour la catégorie 'moutain biker': 145

Output avec : categories = ["man", "women", "children", "ado", "adult", "senior", "hiker", "skier", "moutain biker"]
Computing time:  204.35569252999994
Nombre d'individus trouvées pour la catégorie 'man': 2150
Nombre d'individus trouvées pour la catégorie 'women': 761
Nombre d'individus trouvées pour la catégorie 'children': 588
Nombre d'individus trouvées pour la catégorie 'ado': 0
Nombre d'individus trouvées pour la catégorie 'adult': 2321
Nombre d'individus trouvées pour la catégorie 'senior': 2
Nombre d'individus trouvées pour la catégorie 'hiker': 2766
Nombre d'individus trouvées pour la catégorie 'skier': 0
Nombre d'individus trouvées pour la catégorie 'moutain biker': 145

Output avec : categories = ["man", "women", "children", "adolescent", "adult", "senior", "hiker", "skier", "moutain biker"]
Computing time:  203.8991124339991
Nombre d'individus trouvées pour la catégorie 'man': 2150
Nombre d'individus trouvées pour la catégorie 'women': 761
Nombre d'individus trouvées pour la catégorie 'children': 247
Nombre d'individus trouvées pour la catégorie 'adolescent': 2555
Nombre d'individus trouvées pour la catégorie 'adult': 109
Nombre d'individus trouvées pour la catégorie 'senior': 0
Nombre d'individus trouvées pour la catégorie 'hiker': 2766
Nombre d'individus trouvées pour la catégorie 'skier': 0
Nombre d'individus trouvées pour la catégorie 'moutain biker': 145

Output avec : categories = ["man", "women", "children", "teenager", "adult", "senior", "hiker", "skier", "moutain biker"]
Computing time:  204.7085630069996
Nombre d'individus trouvées pour la catégorie 'man': 2150
Nombre d'individus trouvées pour la catégorie 'women': 761
Nombre d'individus trouvées pour la catégorie 'children': 583
Nombre d'individus trouvées pour la catégorie 'teenager': 19
Nombre d'individus trouvées pour la catégorie 'adult': 2307
Nombre d'individus trouvées pour la catégorie 'senior': 2
Nombre d'individus trouvées pour la catégorie 'hiker': 2766
Nombre d'individus trouvées pour la catégorie 'skier': 0
Nombre d'individus trouvées pour la catégorie 'moutain biker': 145

Output avec : categories = ["man", "women", "kid", "teen", "adult", "senior", "hiker", "skier", "moutain biker"]
Computing time:  200.94633128399983
Nombre d'individus trouvées pour la catégorie 'man': 2150
Nombre d'individus trouvées pour la catégorie 'women': 761
Nombre d'individus trouvées pour la catégorie 'kid': 195
Nombre d'individus trouvées pour la catégorie 'teen': 8
Nombre d'individus trouvées pour la catégorie 'adult': a
Nombre d'individus trouvées pour la catégorie 'senior': 4
Nombre d'individus trouvées pour la catégorie 'hiker': 2766
Nombre d'individus trouvées pour la catégorie 'skier': 0
Nombre d'individus trouvées pour la catégorie 'moutain biker': 145

Output avec : categories = ["man", "women", "kid", "ado", "adult", "senior", "hiker", "skier", "moutain biker"]
Computing time:  203.02195479199872
Nombre d'individus trouvées pour la catégorie 'man': 2150
Nombre d'individus trouvées pour la catégorie 'women': 761
Nombre d'individus trouvées pour la catégorie 'kid': 196
Nombre d'individus trouvées pour la catégorie 'ado': 0
Nombre d'individus trouvées pour la catégorie 'adult': 2711
Nombre d'individus trouvées pour la catégorie 'senior': 4
Nombre d'individus trouvées pour la catégorie 'hiker': 2766
Nombre d'individus trouvées pour la catégorie 'skier': 0
Nombre d'individus trouvées pour la catégorie 'moutain biker': 145

Output avec : categories = ["man", "women", "kid", "adolescent", "adult", "senior", "hiker", "skier", "moutain biker"]
Computing time:  207.10342226900048
Nombre d'individus trouvées pour la catégorie 'man': 2150
Nombre d'individus trouvées pour la catégorie 'women': 761
Nombre d'individus trouvées pour la catégorie 'kid': 4
Nombre d'individus trouvées pour la catégorie 'adolescent': 2790
Nombre d'individus trouvées pour la catégorie 'adult': 116
Nombre d'individus trouvées pour la catégorie 'senior': 1
Nombre d'individus trouvées pour la catégorie 'hiker': 2766
Nombre d'individus trouvées pour la catégorie 'skier': 0
Nombre d'individus trouvées pour la catégorie 'moutain biker': 145

Output avec : categories = ["man", "women", "kid", "teenager", "adult", "senior", "hiker", "skier", "moutain biker"]
Computing time:  204.96466140700068
Nombre d'individus trouvées pour la catégorie 'man': 2150   
Nombre d'individus trouvées pour la catégorie 'women': 761
Nombre d'individus trouvées pour la catégorie 'kid': 189
Nombre d'individus trouvées pour la catégorie 'teenager': 24
Nombre d'individus trouvées pour la catégorie 'adult': 2694
Nombre d'individus trouvées pour la catégorie 'senior': 4
Nombre d'individus trouvées pour la catégorie 'hiker': 2766
Nombre d'individus trouvées pour la catégorie 'skier': 0
Nombre d'individus trouvées pour la catégorie 'moutain biker': 145

Output avec : categories = ["male", "female", "children", "adolescent", "adult", "senior", "hiker", "skier", "moutain biker"]
Computing time:  209.21722835200035
Nombre d'individus trouvées pour la catégorie 'male': 2911
Nombre d'individus trouvées pour la catégorie 'female': 0
Nombre d'individus trouvées pour la catégorie 'children': 247
Nombre d'individus trouvées pour la catégorie 'adolescent': 2555
Nombre d'individus trouvées pour la catégorie 'adult': 109
Nombre d'individus trouvées pour la catégorie 'senior': 0
Nombre d'individus trouvées pour la catégorie 'hiker': 2766
Nombre d'individus trouvées pour la catégorie 'skier': 0
Nombre d'individus trouvées pour la catégorie 'moutain biker': 145

Output avec : categories = ["boy", "girl", "children", "adolescent", "adult", "senior", "hiker", "skier", "moutain biker"]
Computing time:  216.35936191899964
Nombre d'individus trouvées pour la catégorie 'boy': 2304
Nombre d'individus trouvées pour la catégorie 'girl': 607
Nombre d'individus trouvées pour la catégorie 'children': 247
Nombre d'individus trouvées pour la catégorie 'adolescent': 2555
Nombre d'individus trouvées pour la catégorie 'adult': 109
Nombre d'individus trouvées pour la catégorie 'senior': 0
Nombre d'individus trouvées pour la catégorie 'hiker': 2766
Nombre d'individus trouvées pour la catégorie 'skier': 0
Nombre d'individus trouvées pour la catégorie 'moutain biker': 145

Output avec : categories = ["man", "women", "children", "adolescent", "adult", "senior", "walker", "skier", "bicyclist"]
Computing time:  204.04707614100062
Nombre d'individus trouvées pour la catégorie 'man': 2150
Nombre d'individus trouvées pour la catégorie 'women': 761
Nombre d'individus trouvées pour la catégorie 'children': 247
Nombre d'individus trouvées pour la catégorie 'adolescent': 2555
Nombre d'individus trouvées pour la catégorie 'adult': 109
Nombre d'individus trouvées pour la catégorie 'senior': 0
Nombre d'individus trouvées pour la catégorie 'walker': 737
Nombre d'individus trouvées pour la catégorie 'skier': 161
Nombre d'individus trouvées pour la catégorie 'bicyclist': 2013

Output avec : categories = ["man", "women", "children", "adolescent", "adult", "senior", "hiker", "skier", "bicyclist"]
Computing time:  215.48729843
Nombre d'individus trouvées pour la catégorie 'man': 2150
Nombre d'individus trouvées pour la catégorie 'women': 761
Nombre d'individus trouvées pour la catégorie 'children': 247
Nombre d'individus trouvées pour la catégorie 'adolescent': 2555
Nombre d'individus trouvées pour la catégorie 'adult': 109
Nombre d'individus trouvées pour la catégorie 'senior': 0
Nombre d'individus trouvées pour la catégorie 'hiker': 2881
Nombre d'individus trouvées pour la catégorie 'skier': 0
Nombre d'individus trouvées pour la catégorie 'bicyclist': 30
'''

''' dataset2 -> 100_BTCF
Output avec : categories = ["man", "women", "0-15", "15-35", "35-60", "60-100", "hiker", "skier", "moutain biker"]
Computing time:  700.8178772619999
Nombre d'individus trouvées pour la catégorie 'man': 7636
Nombre d'individus trouvées pour la catégorie 'women': 2335
Nombre d'individus trouvées pour la catégorie '0-15': 1887
Nombre d'individus trouvées pour la catégorie '15-35': 6
Nombre d'individus trouvées pour la catégorie '35-60': 8072
Nombre d'individus trouvées pour la catégorie '60-100': 6
Nombre d'individus trouvées pour la catégorie 'hiker': 9529
Nombre d'individus trouvées pour la catégorie 'skier': 0
Nombre d'individus trouvées pour la catégorie 'moutain biker': 442

Output avec : categories = ["man", "women", "children", "adolescent", "adult", "senior", "hiker", "skier", "moutain biker"]
Computing time:  692.9412942050003
Nombre d'individus trouvées pour la catégorie 'man': 7636
Nombre d'individus trouvées pour la catégorie 'women': 2335
Nombre d'individus trouvées pour la catégorie 'children': 697
Nombre d'individus trouvées pour la catégorie 'adolescent': 8969
Nombre d'individus trouvées pour la catégorie 'adult': 305
Nombre d'individus trouvées pour la catégorie 'senior': 0
Nombre d'individus trouvées pour la catégorie 'hiker': 9529
Nombre d'individus trouvées pour la catégorie 'skier': 0
Nombre d'individus trouvées pour la catégorie 'moutain biker': 442

Output avec : categories = ["male", "female", "children", "adolescent", "adult", "senior", "hiker", "skier", "moutain biker"]
Computing time:  697.60131594
Nombre d'individus trouvées pour la catégorie 'male': 9962
Nombre d'individus trouvées pour la catégorie 'female': 9
Nombre d'individus trouvées pour la catégorie 'children': 697
Nombre d'individus trouvées pour la catégorie 'adolescent': 8969
Nombre d'individus trouvées pour la catégorie 'adult': 305
Nombre d'individus trouvées pour la catégorie 'senior': 0
Nombre d'individus trouvées pour la catégorie 'hiker': 9529
Nombre d'individus trouvées pour la catégorie 'skier': 0
Nombre d'individus trouvées pour la catégorie 'moutain biker': 442

Output avec : categories = ["man", "women", "children", "adolescent", "adult", "senior", "hiker", "skier", "bicyclist"]
Computing time:  707.7005316210007
Nombre d'individus trouvées pour la catégorie 'man': 7636
Nombre d'individus trouvées pour la catégorie 'women': 2335
Nombre d'individus trouvées pour la catégorie 'children': 697
Nombre d'individus trouvées pour la catégorie 'adolescent': 8969
Nombre d'individus trouvées pour la catégorie 'adult': 305
Nombre d'individus trouvées pour la catégorie 'senior': 0
Nombre d'individus trouvées pour la catégorie 'hiker': 9788
Nombre d'individus trouvées pour la catégorie 'skier': 0
Nombre d'individus trouvées pour la catégorie 'bicyclist': 183
'''



'''
Avec le pronom a
Nombre d'images trouvées pour la catégorie 'a person': 824
Nombre d'images trouvées pour la catégorie 'a dog': 247
Nombre d'images trouvées pour la catégorie 'a bicycle': 276
Nombre d'images trouvées pour la catégorie 'a backpack': 239
Nombre d'images trouvées pour la catégorie 'a handbag': 646
Nombre d'images trouvées pour la catégorie 'a ski': 585
Nombre d'images trouvées pour la catégorie 'a snowboard': 650
Nombre d'images trouvées pour la catégorie 'a car': 187
Nombre d'images trouvées pour la catégorie 'a motorcycle': 156
Nombre d'images trouvées pour la catégorie 'a bus': 508
Nombre d'images trouvées pour la catégorie 'a horse': 440
Nombre d'images trouvées pour la catégorie 'a sheep': 242

Sans le pronom a
Nombre d'images trouvées pour la catégorie 'person': 1417
Nombre d'images trouvées pour la catégorie 'dog': 244
Nombre d'images trouvées pour la catégorie 'bicycle': 192
Nombre d'images trouvées pour la catégorie 'backpack': 318
Nombre d'images trouvées pour la catégorie 'handbag': 421
Nombre d'images trouvées pour la catégorie 'ski': 285
Nombre d'images trouvées pour la catégorie 'snowboard': 518
Nombre d'images trouvées pour la catégorie 'car': 307
Nombre d'images trouvées pour la catégorie 'motorcycle': 141
Nombre d'images trouvées pour la catégorie 'bus': 463
Nombre d'images trouvées pour la catégorie 'horse': 398
Nombre d'images trouvées pour la catégorie 'sheep': 296
'''