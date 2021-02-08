# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 09:52:26 2021

@author: Alexandre
"""
import sys
import math
import cv2 as cv
import numpy as np

def hough_transform(src, filtre):
    """

    Parameters
    ----------
    src : IMAGE  (cv.imread)
        The image source.
    filtre : French for Filter
        A filter that returns a binary image.

    Returns
    -------
    list
        Hough Transform of the source image.
        
        - dst: filtered image
        - cdst: hough transform applied on the image (to plot)
        - lines: list of vector that are the found lines! 
    """
    if np.shape(src)[-1] == 3:
        src = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    dst = filtre.apply(src)
    
    # Copy edges to the images that will display the results in BGR
    cdst = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)     
    lines = cv.HoughLinesP(dst, 1, np.pi / 180, 50, None, 10, 5)
    
    if lines is not None:
        for i in range(0, len(lines)):
            l = lines[i][0]
            cv.line(cdst, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv.LINE_AA)
    
    return [dst, cdst, lines]