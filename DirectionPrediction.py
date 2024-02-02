# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 13:34:10 2024

@author: esto5
"""

# Si 1 left et 1 verticale alors prendre l'avis de la tete
from functions import GetImage
from Directions import GetDirection
from DataManagment import GetCsvDatas

"""
[left,right,up,down,vertical]
[0,0,0,0,0]
"""

def main():
    #Chooose your photos
    #images = GetImage("https://cdn-s-www.ledauphine.com/images/F8760FA5-EE86-4DE0-A872-DABEE3B5F0BF/NW_raw/ce-qui-semble-etre-une-evidence-pour-une-bonne-partie-des-pratiquants-ne-l-est-pas-forcement-pour-le-grand-public-photo-le-dl-th-g-1624931170.jpg")
    #images = GetImage("D:/Folders/Code/Python/AttendancePNE-OFB/datasets/coco128/images/train2017/")
    #images = GetImage("D:/Folders/Code/Python/AttendancePNE-OFB/datasets/coco128/images/train2017/000000000036.jpg")
    images = GetImage("D:\Folders\Code\Python\AttendancePNE-OFB\datasets\Randonneurs")

    #For predict the images
    #filename = PositionImages("yolov8n-pose.pt", images)
    results = GetCsvDatas('D:\\Folders\\Code\\Python\\app\\results\\results_6.csv')[1:]
    for liste in results:
        for i in range(1, len(liste)):
            liste[i] = float(liste[i])

    positions = ["left","right","up","down","vertical"]

    for result in results:
        print("Image : ", result[0])

        size=34
        result = [result[i:i+size] for i in range(1, len(result), size)] #Nséparate the peoples
        if len(result) > 0 and len(result[0]) > 0:
            for j in range(len(result)):
                person = result[j]
                print("Personne ",j)
                directions = GetDirection(person)
                #directions = GetDirection(person,get_keypoint)
                for k in range(len(directions)):
                    direction = directions[k]
                    if direction!=0:
                        print(positions[k],": ",direction)
                print()

if __name__ == '__main__':
    main()