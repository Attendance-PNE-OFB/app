import json
import pandas as pd
from extractMetadata import extract_metadata, dictionary_to_json

# Créer le fichier JSON en récupérant les métadonnées des images
dictionary_to_json(extract_metadata('../input/101_BTCF'))

# Charger le fichier JSON
with open('output_json/metadata.json', 'r') as json_file:
    json_data = json.load(json_file)

# Charger les fichiers CSV et les transformer en dictionnaire
df_yolo4 = pd.read_csv('../input/yolov4.csv')
df_yolo8 = pd.read_csv('../input/yolov8.csv')
df_yolo4_dict = df_yolo4.to_dict(orient='records')
df_yolo8_dict = df_yolo8.to_dict(orient='records')

# Fonction pour calculer le nombre de personnes pour une image donnée
def calculer_nombre_personnes(image_data):
    sum = 0;
    for x in image_data.get("genre", {}):
        for y in image_data["genre"][x]:
            sum += int(y)
    return sum

# Initialisation des variables pour les calculs
total_person_json = 0
total_images = len(json_data)
total_person_yolo4 = 0
bad_images_yolo4 = 0
mean_diff_yolo4 = 0
total_person_yolo8 = 0
bad_images_yolo8 = 0
mean_diff_yolo8 = 0

# Itérer sur chaque nom d'image dans le fichier JSON
for image_name in json_data:
    # Calculer le nombre de personnes pour l'image actuelle
    personnes_json = calculer_nombre_personnes(json_data[image_name])

    # Trouver l'indice du dictionnaire dans les dictionnaires contenant l'image_name
    index_yolov4 = next((i for i, d in enumerate(df_yolo4_dict) if d['photo'] == image_name), None)
    index_yolov8 = next((i for i, d in enumerate(df_yolo8_dict) if d['photo'] == image_name), None)
    # Si l'index est égal à None, c'est qu'il y a un problème. On devrait forcément avoir les images dans le JSON des métadonnées et dans les dict des
    # modèles yolo
    if (index_yolov4 != None):
        personnes_yolo4 = df_yolo4_dict[index_yolov4]['person']
    else:
        personnes_yolo4 = 0

    if (index_yolov8 != None):
        personnes_yolo8 = df_yolo8_dict[index_yolov8]['person']
    else:
        personnes_yolo8 = 0

    # Calculer le % de comptage total
    total_person_json += personnes_json
    total_person_yolo4 += personnes_yolo4
    total_person_yolo8 += personnes_yolo8
    # Calculer le % d'images bien comptées
    if (personnes_json != personnes_yolo4):
        bad_images_yolo4 += personnes_json-personnes_yolo4
        mean_diff_yolo4 = (mean_diff_yolo4 + (personnes_json-personnes_yolo4)) / 2
    if (personnes_json != personnes_yolo8):
        bad_images_yolo8 += personnes_json-personnes_yolo8
        mean_diff_yolo8 = (mean_diff_yolo8 + (personnes_json-personnes_yolo8)) / 2

print("-------------yoloV4-------------")
print(f"Pourcentage de comptage correct : {total_person_yolo4/total_person_json}")
print(f"Pourcentage d'images avec erreur de comptage' : {bad_images_yolo4/total_images}")
print(f"Erreur moyenne de comptage' : {mean_diff_yolo4}")
print("-------------yoloV8-------------")
print(f"Pourcentage de comptage correct : {total_person_yolo8/total_person_json}")
print(f"Pourcentage d'images avec erreur de comptage' : {bad_images_yolo8/total_images}")
print(f"Erreur moyenne de comptage' : {mean_diff_yolo8}")