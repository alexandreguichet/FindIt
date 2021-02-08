# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 10:31:19 2021

@author: Alexandre


Binary/Adaptive Threshold: 

    https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_thresholding/py_thresholding.html
    

"""
from abc import ABC, abstractmethod

from matplotlib.colors import LogNorm, Normalize

import numpy as np
import pandas as pd
import cv2
from skimage import filters
from scipy.ndimage import gaussian_filter

class Filter(ABC):
    def __init__(self, threshold):
        self.threshold = threshold    
        
    @abstractmethod
    def apply(self):
        pass

class Laplacian(Filter):
    def __init__(self, depth = cv2.CV_32F, kernel_size = 5, threshold = 80):
        super().__init__(threshold)
        
        self.depth = depth
        self.kernel_size = kernel_size

        
    def apply(self, image):
        image = cv2.GaussianBlur(image, (3, 3), 0)
        image = cv2.Laplacian(image, self.depth,  ksize=self.kernel_size)
        image = cv2.convertScaleAbs(image)
        image = np.flip(image, 0)
        ret,image = cv2.threshold(image,self.threshold, 255,cv2.THRESH_BINARY)
        return image

class Sobel(Filter):
    def __init__(self, threshold = 20):
        super().__init__(threshold)
    
    def apply(self, image):
        image = filters.sobel(image)
        image = cv2.normalize(src = image, dst=None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
        ret,image = cv2.threshold(image, self.threshold, 255,cv2.THRESH_BINARY)
        return image
    
class Gaussian(Filter):
    def __init__(self, sigma = 1, norm = False, threshold = 80):
        super().__init__(threshold)
        self.sigma = sigma
        self.norm = norm
        
    def apply(self, image):
        image = image.astype(float)
        image = gaussian_filter(image, sigma = self.sigma)
        
        df = pd.DataFrame(image)
        gx = df.diff(axis = 1).drop(columns = df.columns[0])
        gy = df.diff().drop(df.index[0])
        
        image = (gx.drop(df.index[0]).values**2 + gy.drop(columns = df.columns[0]).values**2)**(1/2)
        
        image = cv2.normalize(src = image, dst=None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
        
        if self.norm == True:
            #TODO: apply norm to magnitude
            norm = LogNorm(image.mean().mean() + 0.5 * image.std().std(), image.max().max())
            image *= norm
        return image

class Adaptative(Filter):
    def __init__(self, sigma = 1, norm = False, threshold = 20):
        super().__init__(threshold)
        self.sigma = sigma
        self.norm = norm
        
    def apply(self, image):
        image = image.astype(float)
        image = gaussian_filter(image, sigma = self.sigma)
        
        df = pd.DataFrame(image)
        gx = df.diff(axis = 1).drop(columns = df.columns[0])
        gy = df.diff().drop(df.index[0])
        
        image = (gx.drop(df.index[0]).values**2 + gy.drop(columns = df.columns[0]).values**2)**(1/2)
        
        vmin = image.mean().mean() + 0.5 * image.std().std()
        vmax = image.max().max()
        np.log(image, image)
        result = image.copy()
        result -= np.log(vmin)
        result /= (np.log(vmax) - np.log(vmin))       
        image = result * 255
        
        #TODO: add binary threshold there
        ret,image = cv2.threshold(image, self.threshold, 255,cv2.THRESH_BINARY)

        image = cv2.normalize(src = image, dst=None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
        return image

class Canny(Filter):
    def __init__(self, threshold = 80):
        super().__init__(threshold)
        
    def apply(self, image):
        image = cv2.Canny(image, 50, 200, None, 3)
        return image