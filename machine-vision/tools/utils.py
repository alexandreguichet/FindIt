# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 21:27:19 2021

@author: Alexandre
"""
import numpy as np
import pandas as pd
import cv2

from matplotlib.colors import rgb2hex

def find_gray(src, tolerance = 0.01):  
    shape = np.shape(src)
    temp = src.reshape(-1, 3)
    results = []
    
    results = temp.copy()
    results[temp.std(1) >= (tolerance * 255)] = 0
    results = results.reshape(shape)
    return results
    
def find_val(src, val, tolerance = 0.01):  
    shape = np.shape(src)
    temp = src.copy()
    results = []
    
    results = temp.copy()
    results[temp > val * (1 + tolerance)] = 0
    results[temp < val * (1 - tolerance)] = 0
    results = results.reshape(shape)
    return results

def to_hex(src):
    shape = np.shape(src)
    temp = pd.DataFrame(src.reshape(-1, 3), columns = ["R", "G", "B"])
    src_hex = (temp["R"] * 256 + temp["G"]) * 256 + temp["B"]
    return src_hex, src_hex.values.reshape(shape[:2]) 

    # return np.array([rgb2hex(temp[i,:]) for i in range(temp.shape[0])])
def to_rgb(src):
    shape = np.shape(src)
    temp = src.flatten()

    b = np.array(temp & 0xFF).reshape(shape)
    g = np.array(temp & (0xFF << 8)).reshape(shape)
    r = np.array(temp & (0xFF << 16)).reshape(shape)
    
    return np.array([r,g,b])

def normalize_to_gray(image):
    return cv2.normalize(src = image, dst=None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)

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