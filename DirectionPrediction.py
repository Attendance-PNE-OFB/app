# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 13:34:10 2024

@author: esto5
"""

from ultralytics import YOLO
import numpy as np
from PIL import Image
import requests
from io import BytesIO
import os
import re
from pydantic import BaseModel
import validators
import csv

"""
[left,right,up,down,vertical]
[0,0,0,0,0]
"""

"""
True if the path is an image, false otherwise
"""
def IsImage(path):
    return path.endswith(".jpg") or path.endswith(".png") or path.endswith(".jpeg")

"""
Get the images in an array form.
Can be a folder, an image in local or an url
"""
def GetImage(path):
    image_names = []
    if os.path.isdir(path):
        for filename in os.listdir(path):
            image = os.path.join(path,filename)
            if IsImage(image):
                image_names.append(image)
    elif IsImage(path):
        if validators.url(path):
            response = requests.get(path)
            image = Image.open(BytesIO(response.content))
            image_names.append(np.asarray(image))
        else :
            image_names.append(path)
    else:
        raise ValueError('Object unknow')
    return image_names




class GetKeypoint(BaseModel):
    NOSE:           int = 0
    LEFT_EYE:       int = 1
    RIGHT_EYE:      int = 2
    LEFT_EAR:       int = 3
    RIGHT_EAR:      int = 4
    LEFT_SHOULDER:  int = 5
    RIGHT_SHOULDER: int = 6
    LEFT_ELBOW:     int = 7
    RIGHT_ELBOW:    int = 8
    LEFT_WRIST:     int = 9
    RIGHT_WRIST:    int = 10
    LEFT_HIP:       int = 11
    RIGHT_HIP:      int = 12
    LEFT_KNEE:      int = 13
    RIGHT_KNEE:     int = 14
    LEFT_ANKLE:     int = 15
    RIGHT_ANKLE:    int = 16

def GetDirection(result,keypoints):
    directions = np.add(GetDirectionLegs(result, keypoints),GetDirectionArms(result, keypoints))
    return GetDirectionHead(result,keypoints) if all(direction==0 for direction in directions) else directions


# si bras gauche à gauche du torse et bras droite à droite alors verticale sinon orienté

def GetDirectionArms(result,keypoints):
    left_shoulder_x, left_shoulder_y = result[keypoints.LEFT_SHOULDER]
    left_elbow_x, left_elbow_y = result[keypoints.LEFT_ELBOW]
    left_wrist_x, left_wrist_y = result[keypoints.LEFT_WRIST]

    right_shoulder_x, right_shoulder_y = result[keypoints.RIGHT_SHOULDER]
    right_elbow_x, right_elbow_y = result[keypoints.RIGHT_ELBOW]
    right_wrist_x, right_wrist_y = result[keypoints.RIGHT_WRIST]

    left = 0
    right = 0

    if left_shoulder_x>0 and left_shoulder_y>0 and left_elbow_x>0 and left_elbow_y>0 and left_wrist_x>0 and left_wrist_y>0:
        left = TraingleDirectionLR(left_shoulder_x, left_shoulder_y, left_elbow_x, left_elbow_y, left_wrist_x, left_wrist_y)

    if right_shoulder_x>0 and right_shoulder_y>0 and right_elbow_x>0 and right_elbow_y>0 and right_wrist_x>0 and right_wrist_y>0:
        right = TraingleDirectionLR(right_shoulder_x, right_shoulder_y, right_elbow_x, right_elbow_y, right_wrist_x, right_wrist_y)

    result = left+right

    if result == 2:
        return [1,0,0,0,0]
    elif result ==-2:
        return [0,1,0,0,0]
    elif result ==1:
        return [0.5,0,0,0,0]
    elif result == -1:
        return [0,0.5,0,0,0]
    elif right!=0 and left+right==0:
        return [0,0,0,0,1]
    else:
        return [0,0,0,0,0]

def GetDirectionLegs(result,keypoints):
    left_hip_x, left_hip_y = result[keypoints.LEFT_HIP]
    left_knee_x, left_knee_y = result[keypoints.LEFT_KNEE]
    left_ankle_x, left_ankle_y = result[keypoints.LEFT_ANKLE]

    right_hip_x, right_hip_y = result[keypoints.RIGHT_HIP]
    right_knee_x, right_knee_y = result[keypoints.RIGHT_KNEE]
    right_ankle_x, right_ankle_y = result[keypoints.RIGHT_ANKLE]

    left = 0
    right = 0

    if left_hip_x>0 and left_hip_y>0 and left_knee_x>0 and left_knee_y>0 and left_ankle_x>0 and left_ankle_y>0:
        left = TraingleDirectionLR(left_hip_x, left_hip_y, left_knee_x, left_knee_y, left_ankle_x, left_ankle_y)

    if right_hip_x>0 and right_hip_y>0 and right_knee_x>0 and right_knee_y>0 and right_ankle_x>0 and right_ankle_y>0:
        right = TraingleDirectionLR(right_hip_x, right_hip_y, right_knee_x, right_knee_y, right_ankle_x, right_ankle_y)

    result = left+right

    if result == 2:
        return [0,1,0,0,0]
    elif result ==-2:
        return [1,0,0,0,0]
    elif result ==1:
        return [0,0.5,0,0,0]
    elif result == -1:
        return [0.5,0,0,0,0]
    elif right!=0 and left+right==0:
        return [0,0,0,0,1]
    else:
        return [0,0,0,0,0]


def TraingleDirectionLR(x1,y1,x2,y2,x3,y3):
    # Définition des sommets du triangle
    A = np.array([x1, y1])  # Sommet A
    B = np.array([x2, y2])  # Sommet B
    C = np.array([x3, y3])  # Sommet C

    # Calcul du centre du triangle (moyenne des coordonnées des sommets)
    center = (A + B + C) / 3

    # Vecteurs entre le centre et les sommets du triangle
    vec_AB = B - A
    vec_BC = C - B
    vec_CA = A - C

    # Calcul du produit vectoriel
    cross_AB_BC = np.cross(vec_AB, vec_BC)
    cross_BC_CA = np.cross(vec_BC, vec_CA)
    cross_CA_AB = np.cross(vec_CA, vec_AB)

    # Vérification de l'orientation
    if cross_AB_BC > 0 and cross_BC_CA > 0 and cross_CA_AB > 0:
        return 1
    elif cross_AB_BC < 0 and cross_BC_CA < 0 and cross_CA_AB < 0:
        return -1
    else:
        return 0



def GetDirectionHead(result,keypoints):
    nose_x, nose_y = result[keypoints.NOSE]
    left_eye_x, left_eye_y = result[keypoints.LEFT_EYE]
    right_eye_x, right_eye_y = result[keypoints.RIGHT_EYE]
    left_ear_x, left_ear_y = result[keypoints.LEFT_EAR]
    right_ear_x, right_ear_y = result[keypoints.RIGHT_EAR]

    eyes_distance = left_eye_x-right_eye_x

    if nose_x>0 and left_eye_x>0 and right_eye_x>0:
        if nose_x<left_eye_x and nose_x<right_eye_x:
            return [1,0,0,0,0]
        elif nose_x>left_eye_x and nose_x>right_eye_x:
            return [0,1,0,0,0]
    if left_ear_x>0 and right_ear_x>0 and left_eye_x==0 and right_eye_x==0:
        return [0,0,1,0,0]
    if left_ear_x>0 and right_ear_x==0:
        if left_eye_x>0 and right_eye_x==0:
            return [1,0,0,0,0]
        elif left_eye_x>0 and right_eye_x>0:
            return [0.5,0,0,0.5,0]
        elif left_eye_x==0 and right_eye_x==0:
            return [1,0,0.5,0,0]
    if left_ear_x==0 and right_ear_x>0:
        if left_eye_x==0 and right_eye_x>0:
            return [0,1,0,0,0]
        elif left_eye_x>0 and right_eye_x>0:
            return [0,0.5,0,0.5,0]
        elif left_eye_x==0 and right_eye_x==0:
            return [0,1,0.5,0,0]
    if nose_x>0 and left_eye_x>0 and right_eye_x>0 and right_eye_x<nose_x and nose_x<left_eye_x:
        return [0,0,0,1,0]
    else: return [0,0,0,0,0]

def CreateUnicCsv(filename):
    base_name, extension = os.path.splitext(filename)
    counter = 0
    while os.path.exists(filename):
        counter += 1
        filename = f"{base_name}_{counter}{extension}"
    print(f"Le fichier CSV '{filename}' a été créé avec succès.")
    return filename


def SaveResults(results):
    directory = os.path.join(os.getcwd(), "results")
    filename = CreateUnicCsv(os.path.join(directory, "results.csv"))
    data = []
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(filename, mode='w+', newline='') as file:
        data.append([])
        data[0].extend(["image","nose_x" , "nose_y" , "left_eye_x" , "left_eye_y" , "right_eye_x" , "right_eye_y" , "left_ear_x" , "left_ear_y" , "right_ear_x" , "right_ear_y" , "left_shoulder_x" , "left_shoulder_y" , "right_shoulder_x" , "right_shoulder_y" , "left_elbow_x" , "left_elbow_y" , "right_elbow_x" , "right_elbow_y" , "left_wrist_x" , "left_wrist_y" , "right_wrist_y" , "right_wrist_y" , "left_hip_x" , "left_hip_y" , "right_hip_x" , "right_hip_y" , "left_knee_x" , "left_knee_y" , "right_knee_x" , "right_knee_y" , "left_ankle_x" , "left_ankle_y" , "right_ankle_x" , "right_ankle_y" ])
        for i in range(len(results)):
            result = results[i]
            data.append([])
            result_keypoints = result.keypoints.xyn.cpu().numpy()
            keypoints = GetKeypoint()
            if len(result_keypoints) > 0 and len(result_keypoints[0]) > 0:
                for j in range(len(result_keypoints)):
                    person = result_keypoints[j]
                    nose_x, nose_y = person[keypoints.NOSE]
                    left_eye_x, left_eye_y = person[keypoints.LEFT_EYE]
                    right_eye_x, right_eye_y = person[keypoints.RIGHT_EYE]
                    left_ear_x, left_ear_y = person[keypoints.LEFT_EAR]
                    right_ear_x, right_ear_y = person[keypoints.RIGHT_EAR]
                    left_shoulder_x, left_shoulder_y = person[keypoints.LEFT_SHOULDER]
                    right_shoulder_x, right_shoulder_y = person[keypoints.RIGHT_SHOULDER]
                    left_elbow_x, left_elbow_y = person[keypoints.LEFT_ELBOW]
                    right_elbow_x, right_elbow_y = person[keypoints.RIGHT_ELBOW]
                    left_wrist_x, left_wrist_y = person[keypoints.LEFT_WRIST]
                    right_wrist_y, right_wrist_y = person[keypoints.RIGHT_WRIST]
                    left_hip_x, left_hip_y = person[keypoints.LEFT_HIP]
                    right_hip_x, right_hip_y = person[keypoints.RIGHT_HIP]
                    left_knee_x, left_knee_y = person[keypoints.LEFT_KNEE]
                    right_knee_x, right_knee_y = person[keypoints.RIGHT_KNEE]
                    left_ankle_x, left_ankle_y  = person[keypoints.LEFT_ANKLE]
                    right_ankle_x, right_ankle_y = person[keypoints.RIGHT_ANKLE]
            data[i+1].append(result.path)
            data[i+1].extend([nose_x , nose_y , left_eye_x , left_eye_y , right_eye_x , right_eye_y , left_ear_x , left_ear_y , right_ear_x , right_ear_y , left_shoulder_x , left_shoulder_y , right_shoulder_x , right_shoulder_y , left_elbow_x , left_elbow_y , right_elbow_x , right_elbow_y , left_wrist_x , left_wrist_y , right_wrist_y , right_wrist_y , left_hip_x , left_hip_y , right_hip_x , right_hip_y , left_knee_x , left_knee_y , right_knee_x , right_knee_y , left_ankle_x , left_ankle_y , right_ankle_x , right_ankle_y ])

        writer = csv.writer(file)
        writer.writerows(data)


def PositionImages(model,images,save_results=False,save=False,txt=False,conf=False,crop=False):
    model = YOLO(model) #Load the model
    results = model.predict(images, save=save, save_txt=txt,save_conf=conf,save_crop=crop) #Generate the prediction
    if save_results:
        SaveResults(results)
    return results

def main():
    #Chooose your photos
    #images = GetImage("https://cdn-s-www.ledauphine.com/images/F8760FA5-EE86-4DE0-A872-DABEE3B5F0BF/NW_raw/ce-qui-semble-etre-une-evidence-pour-une-bonne-partie-des-pratiquants-ne-l-est-pas-forcement-pour-le-grand-public-photo-le-dl-th-g-1624931170.jpg")
    #images = GetImage("D:/Folders/Code/Python/AttendancePNE-OFB/datasets/coco128/images/train2017/")
    #images = GetImage("D:/Folders/Code/Python/AttendancePNE-OFB/datasets/coco128/images/train2017/000000000036.jpg")
    images = GetImage("D:\Folders\Code\Python\AttendancePNE-OFB\datasets\Randonneurs")

    #Get the results
    results = PositionImages("yolov8n-pose.pt", images,save_results=True)

    positions = ["left","right","up","down","vertical"]
    #for result in results:
    for i in range(len(results)):
        result = results[i]
        print()
        print("Image ",os.path.splitext(result.path)[0])
        result_keypoints = result.keypoints.xyn.cpu().numpy()
        get_keypoint = GetKeypoint()

        if len(result_keypoints) > 0 and len(result_keypoints[0]) > 0:
            for j in range(len(result_keypoints)):
                person = result_keypoints[j]
                print("Personne ",j)
                directions = GetDirection(person,get_keypoint)
                for k in range(len(directions)):
                    direction = directions[k]
                    if direction!=0:
                        print(positions[k],": ",direction)
                print()

if __name__ == '__main__':
    main()