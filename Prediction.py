# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 10:59:44 2024

@author: esto5
"""

from ultralytics import YOLO
from DataManagment import SaveResults

def PositionImages(model,images,save=False,txt=False,conf=False,crop=False):
    model = YOLO(model) #Load the model
    results = model.predict(images, save=save, save_txt=txt,save_conf=conf,save_crop=crop) #Generate the prediction
    return SaveResults(results)