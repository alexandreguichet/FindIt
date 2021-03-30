# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 13:53:21 2021

@author: Alexandre
"""

import numpy as np
import cv2
import glob

from tools.manage_file import load_files
import matplotlib.pyplot as plt

def calibrate_cam(src):
    width  = src.shape[1]
    height = src.shape[0]
    
    distCoeff = np.zeros((4,1),np.float64)
    
    # TODO: add your coefficients here!
    ks = [
          #-7.5e-6 , -7.0e-6, 
          -6.5e-6, 
          #-6.0e-6, -5.5e-6, -5.0e-6
          ]
    for k in ks:
        k1 = k; #-6.0e-6; # negative to remove barrel distortion, adjusted for GoPro4
        k2 = 0.0;
        p1 = 0.0;
        p2 = 0.0;
        
        distCoeff[0,0] = k1;
        distCoeff[1,0] = k2;
        distCoeff[2,0] = p1;
        distCoeff[3,0] = p2;
        
        # assume unit matrix for camera
        cam = np.eye(3,dtype=np.float32)
        
        cam[0,2] = width/2.0  # define center x
        cam[1,2] = height/2.0 # define center y
        cam[0,0] = 10.        # define focal length x
        cam[1,1] = 10.        # define focal length y
        
        # here the undistortion will be computed
        dst = cv2.undistort(src,cam,distCoeff)
        return dst