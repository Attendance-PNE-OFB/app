import os
import exiftool
import re
import json

save_file_directory = './output_json/'
def extract_metadata(file_path):
    human_pattern = r'^humain.*'
    man_pattern = r'^homme.*'
    woman_pattern = r'^femme.*'
    age_pattern = r'^(((<|>)\d{1,2})|(\d{1,2}-\d{1,2}))ans$'
    direction_pattern = r'^droite|gauche'
    type_pattern = r'^rando.*|^trail|vtt.*'

    result = {}  # dictionnaire regroupant les noms des images, avec leurs informations sous forme de dictionnaire

    path = None
    if os.name == 'nt':
        path = os.path.join("C:/Users/esto5/anaconda3/envs/s101/Lib/site-packages/exiftool/exiftool.exe")

    with exiftool.ExifTool(path) as et:
        # Obtention des métadonnées de toutes les images du dossier séléctionné
        metadata = et.execute_json("-json", "-r", "-ext", "jpg", file_path)

    for i in range(len(metadata)):
        data = {}  # disctionnaire regroupant les informations de chaque image
        genre = {}  # liste de genre [nb_humains, nb_hommes, nb_femmes]
        cat_age = []  # liste de catégorie d'âge [0-15, 15-35, 35-60, >60]

        if 'XMP:Subject' in metadata[i]:
            for j in metadata[i]['XMP:Subject']:
                if re.match(type_pattern, j):
                    data['type'] = j  # ajout du type d'activité

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
                if re.match(direction_pattern, j):
                    data['direction'] = j

            data['genre'] = genre
            data['age'] = cat_age
        result[metadata[i]['File:FileName']] = data
    return result

def dictionary_to_json(dict):
    filename = create_unic_file(save_file_directory + 'metadata.json')
    f = open(filename, "w")
    f.write("{\n")
    for key in dict:
        json_obj = json.dumps(key, indent=0)
        f.write(json_obj+":{\n")
        for data in dict[key]:
            cat_name = json.dumps(data)
            f.write("    " + cat_name + ":")
            cat_val = json.dumps(dict[key][data])
            if cat_name == "\"age\"":
                f.write(cat_val + "\n")
            else:
                f.write(cat_val + ",\n")
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
