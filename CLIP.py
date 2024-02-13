import os
from PIL import Image
import torch
import clip
import numpy as np
import timeit

start = timeit.default_timer()

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# Chemin du répertoire contenant les images
directory = "/home/aurelien/Documents/ProjetINFO5/input/100_BTCF"

# Liste des extensions d'images prises en charge
image_extensions = [".jpg", ".jpeg", ".png"]

# Liste des catégories textuelles associées à chaque indice
categories = ["man", "woman", "children", "adolescent", "adult", "senior", "it's a hiker", "it's a skier", "it's a bicyclist"]
sexe = ["man", "woman"] #man, male, boy | woman, female, girl
age = ["children", "adolescent", "adult", "senior"] #0-15, child, children, kid | 15-35, teen, ado, adolescent, teenager | 35-60, adult | 60-100, senior
activite = ["it's a hiker", "it's a skier", "it's a bicyclist"] #hiker, walker | skier | moutain biker, bicyclist

# Initialisation du dictionnaire pour stocker le nombre d'images trouvées pour chaque catégorie
categorie_count = {categorie: 0 for categorie in categories}

# Liste des chemins des fichiers image dans le répertoire
image_paths = [os.path.join(directory, file) for file in os.listdir(directory) if any(file.lower().endswith(ext) for ext in image_extensions)]


for image_path in image_paths:
    # Prétraitement de l'image et transfert sur le dispositif approprié
    image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
    
    with torch.no_grad():
        # Encodage de l'image pour obtenir les caractéristiques de l'image
        image_features = model.encode_image(image)
        for i in [0, 1, 2]:
            # Tokenisation des catégories et transfert sur le dispositif approprié
            if i == 0:
                text = clip.tokenize(sexe).to(device)
            elif i == 1:
                text = clip.tokenize(age).to(device)
            elif i == 2:
                text = clip.tokenize(activite).to(device)
            
            # Encodage du texte pour obtenir les caractéristiques du texte
            text_features = model.encode_text(text)

            # Calcul des logits pour l'image et le texte
            logits_per_image, logits_per_text = model(image, text)
            
            # Conversion des logits en probabilités
            probs = logits_per_image.softmax(dim=-1).cpu().numpy()
            
            # Récupérer l'indice de la plus haute probabilité
            indice_max = np.argmax(probs)

            # Récupérer la catégorie associée à l'indice maximal
            # Augmenter le compteur pour la catégorie correspondant à l'indice maximal
            if i == 0:
                categorie_max = sexe[indice_max]
                categorie_count[categorie_max] += 1
            elif i == 1:
                categorie_max = age[indice_max]
                categorie_count[categorie_max] += 1
            elif i == 2:
                categorie_max = activite[indice_max]
                categorie_count[categorie_max] += 1
        
            #print(f"Probabilités pour l'image {image_path}: {probs}")
            #print(f"Pour l'image {image_path}, la catégorie la plus probable est : {categorie_max}")
        
# Affichage du nombre d'images trouvées pour chaque catégorie
for categorie, count in categorie_count.items():
    print(f"Nombre d'individus trouvées pour la catégorie '{categorie}': {count}")

stop = timeit.default_timer()
print('Computing time: ', stop - start) # get an idea of computing time

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