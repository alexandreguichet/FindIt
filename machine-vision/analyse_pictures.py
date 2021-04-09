# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 09:48:25 2021

@author: Alexandre
"""
from tools.manage_file import load_files
from hough_transform import hough_transform
from tools.filters import Laplacian, Sobel, Gaussian, Adaptative, Canny

import matplotlib.pyplot as plt
import matplotlib.colors as colors

import numpy as np
import pandas as pd
import time
import os

from skimage.color import rgb2gray

from tools.utils import normalize_to_gray, calibrate_cam
from vertical_slicing import find_rail

from line import Line, Point, intersects

plt.ioff()

t = time.time()

path = r"..\data\unprocessed"
# path =  r"..\data\Crack_with_all_power"

result_path = r"..\\results\\"
gray = [138, 129, 124]

col =  ["ID", "X_POS", "Y_POS", "WIDTH", "HEIGHT", "AREA", "DANGER LEVEL", "DEFECT TYPE", "PATH"]

pictures, names = load_files(path, gray = False)

df = pd.DataFrame(columns = col)

for image, picID in zip(pictures, names):
    picID = picID[:-4]
    if not os.path.isdir(result_path + picID):
        os.mkdir(result_path + picID)
        
    image = calibrate_cam(image)
    
    grayscale = normalize_to_gray(rgb2gray(image))
    
    ind = find_rail(grayscale, [500, 1500])
    track_area = np.shape(image)[1] * abs(ind[0][2] - ind[0][1])
    track_height = abs(ind[0][2] - ind[0][1])
    
    # lp = Laplacian()
    # sb = Sobel()
    # gs = Gaussian()
    ad = Adaptative()
    # cn = Canny()
    
    filtered, final, hlines = hough_transform(image, ad)
    hlines = hlines.reshape(-1, 4)
    hlines = hlines[((hlines[:,1] < ind[0][2] ) & (hlines[:,1] > ind[0][1]) & (hlines[:,3] < ind[0][2]) & (hlines[:,3] > ind[0][1]))]
    
    #====================================================================================
    #Sort lines together
    
    all_lines = hlines.tolist()
    delta = 5
    # lines_combinations = list()
    
    lines = [Line(Point(i[0], i[1]), Point(i[2], i[3])) for i in all_lines]
    
    sweep = []
    for l in lines:
        p, q = l
     
        sweep.append((min(p.y, q.y) - delta, True, l))
        sweep.append((max(p.y, q.y) + delta, False, l))
    sweep.sort()
     
    #
    #   Check the active set for intersections
    #
     
    active = set()
     
    for pos, activate, line in sweep:    
        if activate:    
            for other in active:
                if intersects(line, other, delta):
                    line.join(other)
     
            active.add(line)
        else:  
            active.remove(line)
     
    groups = {}
    for l in lines:
        h = l.root()
        
        groups.setdefault(h, []);
        groups[h] += [l]
    
    print("got the groups")
    plt.figure(figsize = [16, 9])
    plt.imshow(filtered, cmap='gray')
    
    i = 0
    for l in list(groups):
        print("plot " + str(i) + " of " + str(len(groups)))
        i += 1
        v = groups[l]
        color = list(colors.CSS4_COLORS.values())[(20 + (i + 20)) % 147]
        for j in v:
            plt.plot([j[0][0], j[1][0]], [j[0][1], j[1][1]], c = color, alpha = 1)
    plt.show()
    
#     v = list(groups.values())[0]
#     i = 0
#     for k, v in groups.items():
#         ar = np.array([[i[0][0], i[0][1], i[1][0], i[1][1]] for i in v])
        
#         if len(ar) <= 2:
#             continue
#         aar = ar[:, [0,2]].reshape(-1,1)
#         bar = ar[:, [1,3]].reshape(-1,1)
        
#         far = np.column_stack((aar, bar))
        
#         left = far[np.any((far[:, 0] <= round(far[:, 0].mean() - 1 * far[:, 0].std())).reshape(-1,1), axis = 1)]
#         right = far[np.any((far[:, 0] >= round(far[:, 0].mean() + 1 * far[:, 0].std())).reshape(-1,1), axis = 1)]
        
#         if len(left) == 0 or len(right) == 0:
#             continue
#         # top = far[np.any((far[:, 1] > far[:, 1].mean() + 1 * far[:, 1].std()).reshape(-1,1), axis = 1)]
#         # bottom = far[np.any((far[:, 1] < far[:, 1].mean() - 1 * far[:, 1].std()).reshape(-1,1), axis = 1)]
        
#         left_top0 = left[int(np.argmax(left[:, 1]))]
#         right_top0 = right[int(np.argmax(right[:, 1]))]
#         right_bottom0 =  right[int(np.argmin(right[:, 1]))]
#         left_bottom0 = left[int(np.argmin(left[:, 1]))]
        
#         x = [left_top0[0], right_top0[0], left_bottom0[0], right_bottom0[0]]
#         y = [left_top0[1], left_bottom0[1], right_top0[1], right_bottom0[1]]
        
#         # area = 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))
        
#         width = abs((x[1] - x[0]) + (x[3] - x[2]))/2
#         height = abs((y[1] - y[0]) + (y[3] - y[2]))/2
        
#         area = width * height
        
#         danger_level = int((area/track_area)*100)
        
#         result_picture_path = result_path + picID + "\\" + picID + "_result_" + str(i)
        
#         defect_type = "Noise"
#         if height/width > 4 and danger_level >= 1:
#             defect_type = "Crack"
#         elif danger_level >= 1:
#             defect_type = "Shelling"
#         elif height >= 0.3 * track_height:
#             defect_type = "Crack"
#             danger_level = int(height/track_height*10)
            
#         fig = plt.figure(figsize = [16, 9])
#         plt.imshow(filtered, cmap='gray')
#         color = list(colors.CSS4_COLORS.values())[(20 + (0 + 20)) % 147]
#         for j in v:
#             plt.plot([j[0][0], j[1][0]], [j[0][1], j[1][1]], c = color, alpha = 1)
        
#         # plt.scatter(left_top0[0], left_top0[1], c = "r", s = 15)
#         # plt.scatter(right_top0[0], right_top0[1], c = "r", s = 15)
#         # plt.scatter(right_bottom0[0], right_bottom0[1], c = "r", s = 15)
#         # plt.scatter(left_bottom0[0], left_bottom0[1], c = "r", s= 15)

#         plt.savefig(result_picture_path)
#         plt.close(fig)
#         df = df.append(pd.DataFrame(np.array([picID, 40, 40, width, height, area, danger_level, defect_type, result_picture_path]).reshape(1, -1), 
#                                columns = col), ignore_index = True)
#         i+=1
#     print("done with one picture")
    
# df.to_excel(result_path + "results.xlsx")


# plt.figure(figsize = [16, 9])
# plt.imshow(filtered, cmap='gray')
# color = list(colors.CSS4_COLORS.values())[(20 + (i + 20)) % 147]
# for j in v:
#     plt.plot([j[0][0], j[1][0]], [j[0][1], j[1][1]], c = color, alpha = 1)

# plt.scatter(left_top0[0], left_top0[1], c = "r", s = 15)
# plt.scatter(right_top0[0], right_top0[1], c = "r", s = 15)
# plt.scatter(right_bottom0[0], right_bottom0[1], c = "r", s = 15)
# plt.scatter(left_bottom0[0], left_bottom0[1], c = "r", s= 15)

# plt.scatter(left_top0[0], left_top0[1], c = "r", s = 15)
# plt.scatter(right_top0[0], right_top0[1], c = "r", s = 15)
# plt.scatter(right_bottom0[0], right_bottom0[1], c = "r", s = 15)
# plt.scatter(left_bottom0[0], left_bottom0[1], c = "r", s= 15)
# plt.show()
# df.to_excel("results.xlsx")
