# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 09:48:00 2021

@author: Alexandre
"""

import os
import cv2 as cv

pictures = []
names = []

def load_files(path, gray = True):
    arr = os.listdir(path)
    for f in arr:
        if f[-4:] == ".MP4":
            continue
        if gray is True:
            src = cv.imread(path + "//" + f, cv.IMREAD_GRAYSCALE)
        else:
            src = cv.imread(path + "//" + f)
            src = cv.cvtColor(src, cv.COLOR_BGR2RGB)
        names.append(f)
        pictures.append(src)
    return pictures, names
