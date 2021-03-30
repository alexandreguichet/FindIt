# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 19:12:30 2021

@author: Alexandre
"""

from tools.manage_file import load_files
from hough_transform import hough_transform
from tools.filters import Laplacian, Sobel, Gaussian, Adaptative, Canny

import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, Normalize

import numpy as np
import os

from skimage import color
from skimage import io
from skimage.color import rgb2gray

from tools.utils import find_gray, to_hex, find_val, to_rgb, normalize_to_gray

from image_calibration_test import calibrate_cam

path = r"..\data\unprocessed"
gray = [138, 129, 124]

pictures = load_files(path, gray = False)

image = pictures[3]
image = calibrate_cam(image)

grayscale = normalize_to_gray(rgb2gray(image))

ss = [500, 2500]

low_s = 730
high_s = 1700

def find_rail(src, val, orientation = 'v'):  
    if orientation == 'v':
        
        indexes = list()
        for v in val:
            s = np.transpose(np.array([src[low_s:high_s, v], np.zeros(high_s-low_s)]))
            s[abs(s[:,0] - np.mean(s[:,0])) < 0.5 * np.std(s[:,0]), 1] = 1
            
            ind = [i + low_s for i, e in enumerate(s[:,1]) if e ==1]
            # plt.figure(figsize = [16,9])
            # plt.imshow(image)
            # plt.scatter(v, ind[0], c = 'r', marker = 's', s = 5)
            # plt.scatter(v, ind[-1], c = 'r', marker = 's', s = 5)
            # plt.show()
            indexes.append([v, ind[0],  ind[-1]])
    return indexes

    # plt.figure(figsize = [16, 9]) 
    # plt.scatter(list(range(len(src[:, val]))), src[:, val])
    # plt.title("Slice of image at pixel = " + str(val))
    # plt.show()     
    
# ind = slice_image(grayscale, ss)
# plt.figure(figsize = [16,9])
# plt.imshow(image)
# plt.plot([ind[0][0], ind[1][0]], [ind[0][1], ind[1][1]], c = 'r')
# plt.plot([ind[0][0], ind[1][0]], [ind[0][2], ind[1][2]], c = 'r')
# plt.show()