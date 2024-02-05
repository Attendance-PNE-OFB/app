# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 13:34:10 2024

@author: esto5
"""

# Si 1 left et 1 verticale alors prendre l'avis de la tete
from functions import GetImage
from Directions import GetDirection
from DataManagment import GetCsvDatas, GetMetadonnee, GetMetadonnee
from Prediction import PositionImages
from PIL import Image

"""
[left,right,up,down,vertical]
[0,0,0,0,0]
"""

from PIL import Image, ExifTags
# Open the image file
def main():
    print("start")
    #Chooose your photos
    #images = GetImage("https://cdn-s-www.ledauphine.com/images/F8760FA5-EE86-4DE0-A872-DABEE3B5F0BF/NW_raw/ce-qui-semble-etre-une-evidence-pour-une-bonne-partie-des-pratiquants-ne-l-est-pas-forcement-pour-le-grand-public-photo-le-dl-th-g-1624931170.jpg")
    #images = GetImage("D:/Folders/Code/Python/AttendancePNE-OFB/datasets/coco128/images/train2017/")
    #images = GetImage("D:/Folders/Code/Python/AttendancePNE-OFB/datasets/coco128/images/train2017/000000000036.jpg")
    #images = GetImage("D:\Folders\Code\Python\AttendancePNE-OFB\datasets\Randonneurs")
    #images = GetImage('D:/Folders/Code/Python/app/datasets/Sample/20200709_20200802/101_BTCF')
    images = GetImage('D:/Folders/Code/Python/app/datasets/Sample/20200709_20200802/sousousEnsemble')

    #For predict the images
    #filename = PositionImages("yolov8n-pose.pt", images)
    results = GetCsvDatas('D:\\Folders\\Code\\Python\\app\\results\\results_17.csv')[1:]
    #•results = GetCsvDatas(filename)[1:]
    for liste in results:
        for i in range(1, len(liste)):
            liste[i] = float(liste[i])

    positions = ["left","right","up","down","vertical"]

    for result in results:
        print("Image : ", result[0])

        """
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
        """
        image_path = result[0]
        result = result[1:]
        directions = GetDirection(result)



        if directions[0]> directions[1]:
            print("LEFT")
        elif directions[1]> directions[0]:
            print("RIGHT")
        else:
            for k in range(len(directions)):
                direction = directions[k]
                if direction!=0:
                    print(positions[k],": ",direction)
        print()

    print(GetMetadonnee('D:/Folders/Code/Python/app/datasets/Sample/20200709_20200802/sousousEnsemble'))

if __name__ == '__main__':
    main()