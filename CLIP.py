import os
from PIL import Image
import torch
import clip
import numpy as np
import timeit

start = timeit.default_timer()

###############################################
############### VARIABLES #####################
###############################################

# Chemin du répertoire contenant les images (chemin absolu ou relatif)
directory = "../input/101_BTCF"

# Liste des extensions d'images prises en charge
image_extensions = [".jpg", ".jpeg", ".png", ".JPEG", ".JPG", ".PNG"]

# Liste des catégories textuelles associées à chaque indice
sexe = ["man", "woman"]
age = ["children", "adolescent", "adult", "senior"]
activite = ["it's a hiker", "it's a skier", "it's a bicyclist"]

# Pas besoin de modifier si uniquement le texte change
# En revanche, si le nombre de texte pour une catégorie change, à modifier
categories = [sexe[0], sexe[1], age[0], age[1], age[2], age[3], activite[0], activite[1], activite[2]]

###############################################
#################### CODE #####################
###############################################

# Optimisation avec le GPU si disponible sur la machine
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# Initialisation du dictionnaire pour stocker le nombre d'images trouvées pour chaque catégorie
categorie_count = {categorie: 0 for categorie in categories}

# Liste des chemins des fichiers image dans le répertoire
image_paths = [os.path.join(directory, file) for file in os.listdir(directory) if any(file.lower().endswith(ext) for ext in image_extensions)]

# Parcours des images
for image_path in image_paths:
    # Prétraitement de l'image et transfert sur le dispositif approprié
    image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
    
    with torch.no_grad():
        # Encodage de l'image pour obtenir les caractéristiques de l'image
        image_features = model.encode_image(image)

        # Trois itérations, une pour chaque catégorie (sexe, age, activité)        
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
        
# Affichage du nombre d'images trouvées pour chaque catégorie
for categorie, count in categorie_count.items():
    print(f"Nombre d'individus trouvées pour la catégorie '{categorie}': {count}")

stop = timeit.default_timer()
print('Computing time: ', stop - start) # get an idea of computing time