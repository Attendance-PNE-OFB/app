import exiftool
import re


human_pattern = r'^humain.*'
man_pattern = r'^homme.*'
woman_pattern = r'^femme.*'
age1_pattern = r'^0-15.*'
age2_pattern = r'^15-35.*'
age3_pattern = r'^35-60.*'
age4_pattern = r'^>60.*'
direction_pattern = r'^droite|gauche'

result = {} # dictionnaire regroupant les noms des images, avec pour chacun leurs informations sous forme de dictionnaire (data)
data = {} # disctionnaire regroupant les informations de chaque image
genre = [] # liste de genre [nb_humains, nb_hommes, nb_femmes]
cat_age = [] # liste de catégorie d'âge [0-15, 15-35, 35-60, >60]

with exiftool.ExifTool() as et:

    # Obtention des métadonnées de toutes les images du dossier séléctionné

    # Indiquer ici le dossier vers les images
    metadata = et.execute_json("-json", "-r", "-ext", "jpg", "dossier/vers/images")

for i in range(len(metadata)):
    data = {}
    genre = []
    cat_age = []

    if 'XMP:Subject' in metadata[i]:
        for j in metadata[i]['XMP:Subject']:

            if metadata[i]['XMP:Subject'].index(j) == 0:
                data['type'] = j # ajout du type d'activité

            #-------------------Partie sexe-------------------
            if re.match(human_pattern, j):
                genre.append(j[-2:])
            elif re.match(man_pattern, j):
                genre.append(j[-2:])
            elif re.match(woman_pattern, j):
                genre.append(j[-2:])
            elif len(genre) < 3:
                genre.append('0')

            #-------------Partie Catégorie d'âge-------------
            if re.match(age1_pattern, j):
                cat_age.append(j)
            elif re.match(age2_pattern, j):
                cat_age.append(j)
            elif re.match(age3_pattern, j):
                cat_age.append(j)
            elif re.match(age4_pattern, j):
                cat_age.append(j)

            #----------------Partie Direction----------------
            if re.match(direction_pattern, j):
                #print("direction:", j)
                direction = j
                data['direction'] = j

        data['genre'] = genre
        data['age'] = cat_age
    result[metadata[i]['File:FileName']] = data
print(result)
