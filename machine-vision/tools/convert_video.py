# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 10:44:22 2021

@author: Alexandre
"""

import cv2

video = r"..\..\data\2.7K-120_None_(20)\2.7K-120 None (20).MP4"

vidcap = cv2.VideoCapture(video)
success,image = vidcap.read()
count = 0
while success:
    pic_path = video.replace(" ", "_").replace(".MP4", ".png")
    pic_path = pic_path[:-4] + "_frame%d" +  pic_path[-4:]
    cv2.imwrite(pic_path % count, image)     # save frame as JPEG file      
    success,image = vidcap.read()
    count += 1