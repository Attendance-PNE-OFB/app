# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 10:59:44 2024

@author: esto5
"""

from ultralytics import YOLO
from DataManagment import SaveResults

def PositionImages(model,images,batch=50,save=False,txt=False,conf=False,crop=False):
    model = YOLO(model) #Load the model
    results = []
    for i in range(0, len(images), batch):
        sample = images[i:i + batch]
        results.append(model.predict(sample, save=save, save_txt=txt,save_conf=conf,save_crop=crop)) #Generate the prediction
        print("Prediction : ", round(((i+batch)*100/len(images)),2),"%")
    return SaveResults(results)