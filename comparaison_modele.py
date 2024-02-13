import json
import pandas as pd
import argparse
import os

# Fonction pour calculer le nombre de personnes pour une image donnée
def calculer_nombre_personnes(image_data):
    sum = 0;
    for x in image_data.get("genre", {}):
        for y in image_data["genre"][x]:
            sum += int(y)
    return sum

# Créer un objet ArgumentParser
parser = argparse.ArgumentParser(description='Ce code permet de comparer deux modèles yolo entraînés sur COCO ou OpenImageV7 entre eux.')

# Ajouter une option d'aide personnalisée
parser.add_argument('-m', '--metadata', action='store', dest='chemin_metadonnee', help="Le chemin des images, à renseigné uniquement si vous n'avez pas le fichier JSON des métadonnées.")
parser.add_argument('--json', action='store', dest='chemin_fichierJSON', help="Le chemin du fichier JSON des métadonnées, à renseigné uniquement si vous avez déjà le fichier JSON des métadonnées.")
parser.add_argument('-c1', '--chemin1', action='store', dest='chemin_csvmodele1', required=True,  help="Le chemin du fichier CSV de sortie du premier modèle.")
parser.add_argument('-c2', '--chemin2', action='store', dest='chemin_csvmodele2', required=True, help="Le chemin du fichier CSV de sortie du second modèle.")
parser.add_argument('-d', '--dataset', action='store', dest='nom_dataset', required=True, help="Le nom du dataset d'entraînement des deux modèles (COCO ou OpenImageV7).")

# Analyser les arguments de la ligne de commande
args = parser.parse_args()

# Si ni le chemin des images pour créer le JSON des métadonnées ni le chemin du JSON déjà existant a été renseigné, alors on stop l'exécution
if (args.chemin_metadonnee==None) and (args.chemin_fichierJSON==None):
    print("Il faut renseigner le chemin des images pour créer le JSON des métadonnées ou renseigné le chemin du fichier JSON si vous l'avez déjà.")
    exit()

if args.chemin_metadonnee!=None:
    try:
        from extractMetadata import extract_metadata, dictionary_to_json
        # Créer le fichier JSON en récupérant les métadonnées des images
        print("Création du fichier JSON des métadonnées des images...")
        dictionary_to_json(extract_metadata(args.chemin_metadonnee), os.path.basename(args.chemin_metadonnee))
    except ModuleNotFoundError:
        print("Erreur dans la création du fichier JSON des métadonnées des images. Veuillez vérifier la présence du code d'extraction des métadonnées.")
        exit()
    try:
        with open('output_json/metadata_'+os.path.basename(args.chemin_metadonnee)+'.json', 'r') as json_file:
            json_data = json.load(json_file)
    except FileNotFoundError:
        print("Erreur dans l'ouverture du fichier JSON des métadonnées. Veuillez vérifier le chemin.")
        exit()

# Charger le fichier JSON
print("Chargement du fichier JSON des métadonnées des images...")
if args.chemin_fichierJSON!=None:
    try:
        with open(args.chemin_fichierJSON, 'r') as json_file:
            json_data = json.load(json_file)
    except FileNotFoundError:
        print("Mauvais chemin renseigné pour le fichier JSON des métadonnées. Veuillez vérifier le chemin.")
        exit()

# Charger les fichiers CSV
print("Chargement des fichiers CSV de sortie des modèles...")
try:
    df_model1 = pd.read_csv(args.chemin_csvmodele1)
except (FileNotFoundError,UnicodeDecodeError):
    print("Erreur dans l'ouverture du fichier CSV du premier modèle. Veuillez vérifier le chemin.")
    exit()

try:
    df_model2 = pd.read_csv(args.chemin_csvmodele2)
except (FileNotFoundError,UnicodeDecodeError):
    print("Erreur dans l'ouverture du fichier CSV du second modèle. Veuillez vérifier le chemin.")
    exit()

#Transformation des CSV en dictionnaire
df_model1 = df_model1.to_dict(orient='records')
df_model2 = df_model2.to_dict(orient='records')

# Initialisation des variables pour les calculs
total_person_json = 0
total_images = len(json_data)
total_person_model1 = 0
bad_images_model1 = 0
mean_diff_model1 = 0
total_person_model2 = 0
bad_images_model2 = 0
mean_diff_model2 = 0

# Itérer sur chaque nom d'image dans le fichier JSON
print("Calculs en cours...")
for image_name in json_data:
    # Calculer le nombre de personnes pour l'image actuelle
    personnes_json = calculer_nombre_personnes(json_data[image_name])

    # Trouver l'indice du dictionnaire dans les dictionnaires contenant l'image_name
    index_model1 = next((i for i, d in enumerate(df_model1) if d['photo'] == image_name), None)
    index_model2 = next((i for i, d in enumerate(df_model2) if d['photo'] == image_name), None)
    # Si l'index est égal à None, c'est qu'il y a un problème. On devrait forcément avoir les images dans le JSON des métadonnées et dans les dict des
    # modèles yolo
    if (index_model1 != None):
        try:
            if args.nom_dataset=="COCO":
                personnes_model1 = df_model1[index_model1]['person']
            elif args.nom_dataset=="OpenImageV7":
                personnes_model1 = max(df_model1[index_model1]['Person'], df_model1[index_model1]['Girl'] + df_model1[index_model1]['Boy'] + df_model1[index_model1]['Man'] + df_model1[index_model1]['Woman'])
            else:
                print("Le nom du dataset d'entraînement des modèles n'est pas COCO, ni OpenImageV7. Veuillez vérifier le nom indiqué. Doit être 'COCO' ou 'OpenImageV7'.")
                exit()
        except KeyError:
            print("Le nom du dataset d'entraînement saisi ne correspond pas à celui qui a été utilisé par le modèle renseigné. Veuillez vérifier le nom indiqué. Doit être 'COCO' ou 'OpenImageV7'.")
            exit()
    else:
        personnes_model1 = 0
        print("Le code a détecté une différence entre les images du JSON et les images du modèle 1. Veuillez vérifier sur quelles images ont été construit le JSON et/ou le CSV.")
        exit()

    if (index_model2 != None):
        try:
            if args.nom_dataset=="COCO":
                personnes_model2 = df_model2[index_model2]['person']
            elif args.nom_dataset=="OpenImageV7":
                personnes_model2 = max(df_model2[index_model2]['Person'], df_model2[index_model2]['Girl'] + df_model2[index_model2]['Boy'] + df_model2[index_model2]['Man'] + df_model2[index_model2]['Woman'])
            else:
                print("Le nom du dataset d'entraînement des modèles n'est pas COCO, ni OpenImageV7. Veuillez vérifier le nom indiqué. Doit être 'COCO' ou 'OpenImageV7'.")
                exit()
        except KeyError:
            print("Le nom du dataset d'entraînement saisi ne correspond pas à celui qui a été utilisé par le modèle renseigné. Veuillez vérifier le nom indiqué. Doit être 'COCO' ou 'OpenImageV7'.")
            exit()
    else:
        personnes_model2 = 0
        print("Le code a détecté une différence entre les images du JSON et les images du modèle 2. Veuillez vérifier sur quelles images ont été construit le JSON et/ou le CSV.")
        exit()

    # Calculer le % de comptage total
    total_person_json += personnes_json
    total_person_model1 += personnes_model1
    total_person_model2 += personnes_model2

    # Calculer le % d'images bien comptées ainsi que l'écart de comptage moyen sur les images avec erreur
    if (personnes_json != personnes_model1):
        bad_images_model1 += 1
        if mean_diff_model1==0:
            mean_diff_model1 = personnes_model1-personnes_json
        else:
            mean_diff_model1 = (mean_diff_model1 + (personnes_model1-personnes_json)) / 2
    if (personnes_json != personnes_model2):
        bad_images_model2 += 1
        if mean_diff_model2==0:
            mean_diff_model2 = personnes_model2-personnes_json
        else:
            mean_diff_model2 = (mean_diff_model2 + (personnes_model2-personnes_json)) / 2

if (total_person_model1<total_person_json):
    print("-------------Modèle 1-------------")
    print(f"Pourcentage de comptage correct : {total_person_model1/total_person_json}")
    print(f"Pourcentage d'images avec erreur de comptage' : {bad_images_model1/total_images}")
    print(f"Erreur moyenne de comptage' : {mean_diff_model1}")
else:
    print("-------------Modèle 1-------------")
    print(f"Pourcentage de comptage correct : {total_person_json/total_person_model1}")
    print(f"Pourcentage d'images avec erreur de comptage' : {bad_images_model1/total_images}")
    print(f"Erreur moyenne de comptage' : {mean_diff_model1}")

if (total_person_model2<total_person_json):
    print("-------------Modèle 2-------------")
    print(f"Pourcentage de comptage correct : {total_person_model2/total_person_json}")
    print(f"Pourcentage d'images avec erreur de comptage' : {bad_images_model2/total_images}")
    print(f"Erreur moyenne de comptage' : {mean_diff_model2}")
else:
    print("-------------Modèle 2-------------")
    print(f"Pourcentage de comptage correct : {total_person_json/total_person_model2}")
    print(f"Pourcentage d'images avec erreur de comptage' : {bad_images_model2/total_images}")
    print(f"Erreur moyenne de comptage' : {mean_diff_model2}")