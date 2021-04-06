# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 10:44:22 2021

@author: Alexandre
"""
import cv2

def getFrame(sec, count):
    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    hasFrames,image = vidcap.read()
    pic_name = pic_path[:-4] + "_frame_%d" % count +  pic_path[-4:]
    if hasFrames:
        cv2.imwrite(pic_name, image)     # save frame as JPG file
    return hasFrames

video = r"..\..\data\Crack_with_all_power\Crack_with_all_power.MP4"

vidcap = cv2.VideoCapture(video)
sec = 0
frameRate = 0.26 #//it will capture image in each 0.5 second
count=1

pic_path = video.replace(" ", "_").replace(".MP4", ".jpg")

success = getFrame(sec, count)
while success:
    print(sec)
    count = count + 1
    sec = sec + frameRate
    sec = round(sec, 2)
    success = getFrame(sec, count)