import os
import exiftool
import re
import json
import pandas as pd


save_file_directory = './output_json/'
def extract_metadata(file_path):
    human_pattern = r'^humain.*'
    man_pattern = r'^homme.*'
    woman_pattern = r'^femme.*'
    age_pattern = r'^(((<|>)\d{1,2})|(\d{1,2}-\d{1,2}))ans$'
    direction_d_pattern = r'^droite.*'
    direction_g_pattern = r'^gauche.*'
    type_pattern = [r'^rando.*', r'^trail.*', r'^vtt.*', r'^ski.*', r'^snowboard']

    result = {}  # dictionnaire regroupant les noms des images, avec leurs informations sous forme de dictionnaire

    with exiftool.ExifTool() as et:
        # Obtention des métadonnées de toutes les images du dossier séléctionné
        metadata = et.execute_json("-json", "-r", "-ext", "jpg", file_path)

    for i in range(len(metadata)):
        data = {}  # disctionnaire regroupant les informations de chaque image
        genre = {}  # liste de genre [nb_humains, nb_hommes, nb_femmes]
        direction = [] # liste de direction [droite, gauche]
        cat_age = []  # liste de catégorie d'âge [0-15, 15-35, 35-60, >60]
        type = []  # liste de type d'activité [rando, trail, vtt, ...]

        if 'XMP:Subject' in metadata[i]:
            for j in metadata[i]['XMP:Subject']:
                for k in range(len(type_pattern)):
                    if re.match(type_pattern[k], j):
                        type.append(j)  # ajout du type d'activité

                # -------------------Partie sexe-------------------
                if re.match(human_pattern, j):
                    genre['humains'] = j[-2:]
                elif re.match(man_pattern, j):
                    genre['hommes'] = j[-2:]
                elif re.match(woman_pattern, j):
                    genre['femmes'] = j[-2:]

                # -------------Partie Catégorie d'âge-------------
                if re.match(age_pattern, j):
                    cat_age.append(j)

                # ----------------Partie Direction----------------
                if re.match(direction_d_pattern, j):
                    direction.append(j)
                elif re.match(direction_g_pattern, j):
                    direction.append(j)

            data['type'] = type
            data['direction'] = direction
            data['genre'] = genre
            data['age'] = cat_age
        result[metadata[i]['File:FileName']] = data
    return result

def extract_activities(file_path) :
    df = pd.read_csv(file_path)

    dictionnaire_photos = {}

    for i in range(df.shape[0]):

        dictionnaire_activites = {}

        # Parcourir chaque colonne d'activité
        for nom_activite in df.columns[1:]:
            # Si l'activité est présente, ajouter le nombre de personnes à l'activité correspondante
            if nom_activite == 'Bicycle' and df.loc[i, nom_activite] > 0:
                dictionnaire_activites['vtt'] = str(df.loc[i, nom_activite])
            elif (nom_activite == 'Hiking equipment' and df.loc[i, nom_activite] > 0 ) or (nom_activite == 'Backpack' and df.loc[i, nom_activite] > 0) or (nom_activite == 'Footwear' and df.loc[i, nom_activite] > 0):
                dictionnaire_activites['randonnee'] = str(max(df.loc[i, 'Hiking equipment'], df.loc[i, 'Backpack'], df.loc[i, 'Footwear']))
            elif nom_activite == 'Ski' and df.loc[i, nom_activite] > 0:
                dictionnaire_activites['ski'] = str(df.loc[i, nom_activite])
        # Ajouter l'information de la photo au dictionnaire
        dictionnaire_photos[df.loc[i, 'photo']] = {'activites': dictionnaire_activites}

    return(dictionnaire_photos)


def dictionary_to_json(dict, file_path):
    filename = create_unic_file(save_file_directory + 'metadata_' + os.path.basename(file_path) + '.json')
    f = open(filename, "w")
    f.write("{\n")
    for key in dict:
        json_obj = json.dumps(key, indent=0)
        f.write(json_obj+":{\n")
        for i, (data, value) in enumerate(dict[key].items()):  # Iterate with indices
            cat_name = json.dumps(data)
            f.write("    " + cat_name + ":")
            cat_val = json.dumps(value)
            if i < len(dict[key]) - 1:  # Check if it's the last item
                f.write(cat_val + ",\n")
            else:
                f.write(cat_val + "\n")
        if key == list(dict.keys())[-1]:
            f.write("}\n")
        else:
            f.write("},\n\n")
    f.write("}")
    f.close()


def create_unic_file(filename):
    base_name, extension = os.path.splitext(filename)
    counter = 0
    if not os.path.exists(save_file_directory):
        os.makedirs(save_file_directory)
    while os.path.exists(filename):
        counter += 1
        filename = f"{base_name}_{counter}{extension}"
    print(f"Le fichier '{filename}' a été créé avec succès.")
    return filename
