# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 09:48:25 2021

@author: Alexandre
"""
from tools.manage_file import load_files
from hough_transform import hough_transform
from tools.filters import Laplacian, Sobel, Gaussian, Adaptative, Canny

import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, Normalize
import matplotlib.colors as colors

import numpy as np
import pandas as pd
import os
import time

# from skimage import color
from skimage import io
from skimage.color import rgb2gray

from tools.utils import find_gray, to_hex, find_val, to_rgb, normalize_to_gray, calibrate_cam
from vertical_slicing import find_rail

from tools.checkcollision import check_collision
from line import Line, Point, intersects

t = time.time()

path = r"..\data\unprocessed"
gray = [138, 129, 124]

pictures = load_files(path, gray = False)

image = pictures[0]
image = calibrate_cam(image)

grayscale = normalize_to_gray(rgb2gray(image))

ind = find_rail(grayscale, [500, 2500])

# hist_hex, image_hex = to_hex(image)

# plt.figure(figsize = [16, 9])
# plt.hist(grayscale.flatten(), bins = 2000)
# plt.title('Source', size=20)
# plt.tight_layout()

# plt.figure(figsize = [16, 9])
# plt.imshow(pictures[0])
# plt.title('Source', size=20)
# plt.tight_layout()

# plt.figure(figsize = [16, 9])
# plt.imshow(image_hex, cmap='gray')
# plt.title('Source', size=20)
# plt.tight_layout()

# val, count = np.unique(grayscale.flatten(), return_counts = True)
# target = val[np.argmax(count)]
# temp = find_val(grayscale, target, tolerance = 0.1)

# extracted_image = image.copy()
# extracted_image[temp == 0] = 0

# plt.figure(figsize = [16, 9])
# plt.imshow(extracted_image)
# plt.title('Source', size=20)
# plt.tight_layout()

# lp = Laplacian()
# sb = Sobel()
# gs = Gaussian()
ad = Adaptative()
# cn = Canny()

filtered, final, hlines = hough_transform(image, ad)
hlines = hlines.reshape(-1, 4)
hlines = hlines[((hlines[:,1] < ind[0][2] ) & (hlines[:,1] > ind[0][1]) & (hlines[:,3] < ind[0][2]) & (hlines[:,3] > ind[0][1]))]
# filtered, final, lines = hough_transform(pictures[0], cn)
# filtered, final, lines = hough_transform(pictures[0], gs)
# filtered, final, lines = hough_transform(pictures[0], lp)
# filtered, final, lines = hough_transform(pictures[0], sb)

# debug only
# plt.figure(figsize = [16, 9])
# plt.imshow(image, cmap='gray')
# plt.title('Source', size=20)
# plt.tight_layout()

# plt.figure(figsize = [16, 9])
# plt.imshow(filtered, cmap='gray')
# plt.title('Source after filtering', size=20)
# plt.tight_layout()

# plt.figure(figsize = [16, 9])
# plt.imshow(filtered, cmap='gray')
# for l in lines: 
#     plt.plot([l[0], l[2]], [l[1], l[3]], c = 'salmon', alpha = 0.7)
# plt.title('Source after filtering', size=20)
# plt.tight_layout()

# plt.figure(figsize = [16, 9])
# plt.imshow(filtered, cmap='gray')
# for i in range(20):
#     plt.plot([lines[i][0], lines[i][2]], [lines[i][1], lines[i][3]], c = 'salmon', alpha = 1)


# all_lines = lines.tolist()
# iterate_through = all_lines.copy()
# # aa.append([1360, 1360, 1440, 1380])
# pix = 5

# rarr = np.array(range(len(all_lines)))

# def root(x):
#     while (rarr[x] != x):
#         x = rarr[x]
#     return rarr[x]

# i = 0
# for l in iterate_through:
#     print(str(i) + " of " + str(len(iterate_through))) 
#     iterate_through.remove(l)
    
#     for j in range(len(iterate_through)):
#         ol = iterate_through[j]
#         if check_collision(l, ol, pix):
#             rarr[j] = root(i)
#     i += 1


# plt.figure(figsize = [16, 9])
# plt.imshow(filtered, cmap='gray')
# c = ["salmon", "aqua", "forestgreen", 'khaki', 'peru', 'lightcoral', 'plum']
# for i in np.unique(rarr):
#     indexes = np.where(rarr == i)[0]
    
#     print("plot " + str(i))
#     l = np.array(all_lines)[indexes]
#     color = list(colors.CSS4_COLORS.values())[(20 + (i + 3)) % 147]
#     for j in l:
#         plt.plot([j[0], j[2]], [j[1], j[3]], c = color, alpha = 1)
# plt.show()

# plt.figure(figsize = [16, 9])
# plt.imshow(image)
# plt.title('Source', size=20)
# plt.tight_layout()

# bb = list()
# bb.append(aa[-1])
# bb.append(aa[42])
# lines_combinations = list()
# pix = 5

# plt.figure(figsize = [16, 9])
# plt.imshow(filtered, cmap='gray')
# for i in bb:
#     plt.plot([i[0], i[2]], [i[1], i[3]], alpha = 1)

#====================================================================================
#WORKS SOMEHOW

all_lines = hlines.tolist()
delta = 20
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


plt.figure(figsize = [16, 9])
plt.imshow(filtered, cmap='gray')
i = 0
for l in list(groups):
    print("plot " + str(i) + " of " + str(len(lines)))
    i += 1
    v = groups[l]
    color = list(colors.CSS4_COLORS.values())[(20 + (i + 20)) % 147]
    for j in v:
        plt.plot([j[0][0], j[1][0]], [j[0][1], j[1][1]], c = color, alpha = 1)
plt.show()



# i = 0
# for l in lines_class:           # find intersections
#     g = l.root()

#     for k in lines_class[i + 1:]:
#         if g != k.root() and check_collision(l[:], k[:], pix):
#             l.join(k)
#     i += 1

# groups = {}

# for l in lines_class:                         # find groups
#     h = l.root()
    
#     groups.setdefault(h, []);
#     groups[h] += [l]
   
# print(time.time() - t)

# plt.figure(figsize = [16, 9])
# plt.imshow(filtered, cmap='gray')
# i = 0

# for l in list(groups):
#     print("plot " + str(i) + " of " + str(len(lines_class)))
#     i += 1
#     v = groups[l]
#     color = list(colors.CSS4_COLORS.values())[(20 + (i + 20)) % 147]
#     for j in v:
#         plt.plot([j[0][0], j[0][2]], [j[0][1], j[0][3]], c = color, alpha = 1)
# plt.show()

limites = [0, 2900]
plt.figure(figsize = [16, 9])
plt.imshow(filtered, cmap='gray')
i = 0
l = list(groups)[0]
# for l in list(groups)[0]:
print("plot " + str(i) + " of " + str(len(lines_class)))
i += 1
v = groups[l]
color = list(colors.CSS4_COLORS.values())[(20 + (i + 20)) % 147]
for j in v:
    if ((j[0][2] >= limites[0]) and (j[0][2] <= limites[1])) and ((j[0][3] >= limites[0]) and  (j[0][1] <= limites[1])):
        plt.plot([j[0][0], j[0][2]], [j[0][1], j[0][3]], c = color, alpha = 1)
plt.show()

# plt.figure(figsize = [16, 9])
# plt.imshow(filtered, cmap='gray')
# c = ["salmon", "aqua", "forestgreen", 'khaki', 'peru', 'lightcoral', 'plum']
# i = 0
# for l in lines_combinations:
#     print("plot " + str(i) + " of " + str(len(lines_combinations)))
#     i += 1
#     color = list(colors.CSS4_COLORS.values())[(20 + (i + 50)) % 147]
#     for j in l:
#         plt.plot([j[0], j[2]], [j[1], j[3]], c = color, alpha = 1)
# plt.show()

    
# i= 0
# for l in all_lines[:5]:
#     print(str(i) + " of " + str(len(all_lines))) 
    
#     #Find if the potential line already belongs to a group
#     line_group = False;
#     to_remove = list()
    
#     if i == 23:
#         print("here")
        
#     for j in lines_combinations: #Iterate through all combination found already
#         if tuple(l) in j:
#             line_group = j
#             to_remove.append(j)
            
#     if line_group == False: #if not in a group already, create a new set
#         line_group = {tuple(l)}
        
#     #Remove a from the total line list 
#     all_lines.remove(l)
    
#     #Iterate through all potential lines
#     for ol in all_lines:
#         if check_collision(l, ol, pix): 
#             #If collision, check if k is in another group
#             is_group = False
#             for k in lines_combinations: 
#                 if tuple(ol) in k:
#                     #If true, append both groups together
#                     line_group = line_group.union(k)
#                     is_group = True
#                     if k not in to_remove:
#                         to_remove.append(k)
#             if not is_group:
#                 line_group.add(tuple(ol))
                
#     if len(to_remove) > 0:
#         for m in to_remove:
#             try:
#                 lines_combinations.remove(m)
#             except:
#                 pass
        
#     lines_combinations.append(line_group)
#     i += 1


# print(time.time() - t)

# plt.figure(figsize = [16, 9])
# plt.imshow(filtered, cmap='gray')
# c = ["salmon", "aqua", "forestgreen", 'khaki', 'peru', 'lightcoral', 'plum']
# i = 0
# for l in lines_combinations:
#     print("plot " + str(i) + " of " + str(len(lines_combinations)))
#     i += 1
#     color = list(colors.CSS4_COLORS.values())[(20 + (i + 50)) % 147]
#     for j in l:
#         plt.plot([j[0], j[2]], [j[1], j[3]], c = color, alpha = 1)
# plt.show()



#====================================================================================

# all_lines = lines.tolist()
# lines_combinations = list()

# for l in all_lines:
    
#     #Find if the potential line already belongs to a group in line_combination
#     remove_list_l = False  #is line (l) in a group in lines_combination
#     remove_list_ol = False #is other line (ol) in a group in lines_combination
#     line_group = False;
    
#     for j in lines_combinations: #Iterate through all combination found already
#         if tuple(l) in j:
#             line_group = j
#             remove_list_l = True
#     if not line_group:
#         line_group = {tuple(l)}
        
#     #Remove a from the total line list 
#     all_lines.remove(l)
    
#     #Iterate through all potential lines
#     for ol in all_lines:
#         if check_collision(l, ol, pix): 
#             #If collision, check if k is in another group
#             for k in lines_combinations: 
#                  if tuple(ol) in k:
#                      #If true, append both groups together
#                      line_group.union(k)
#                      replace_list_ol = True
#             if not replace_list_ol:
#                 line_group.add(tuple(ol))
                
#     #Remove both groups and add the new joint one
#     if remove_list_l:   
#         lines_combinations.remove(j)
#     if replace_list_ol:
#          if j != k:
#              lines_combinations.remove(k)
        
#     lines_combinations.append(line_group)

    


#=============================================================================
# i= 0
# for a in bb:
#     print(str(i) + "of " + str(len(aa))) 
#     replace_list = False
#     list_a = False;
#     for j in lines_combinations:
#         if tuple(a) in j:
#             list_a = j
#             replace_list = True
#     if list_a == False:
#         list_a = {tuple(a)}
#     aa.remove(a)
#     for b in bb:
#         if check_collision(a, b, pix): 
#             list_a.add(tuple(b))
#     if replace_list:   
#         lines_combinations.remove(j)
#     lines_combinations.append(list_a)
#     i += 1

# i= 0
# for pl in potentiallines:
#     print(str(i) + " of " + str(len(potentiallines))) 
    
#     #Find if a already belongs to a group
#     replace_list_pl = False #is potential line (pl) in a group
#     replace_list_ol = False #is other line (ol) in a group
#     line_group = False;
    
#     for j in lines_combinations:
#         if tuple(pl) in j:
#             line_group = j
#             replace_list_pl = True
#     if line_group == False:
#         line_group = {tuple(pl)}
        
#     #Remove a from the total line list 
#     potentiallines.remove(pl)
    
#     #Iterate through all potential lines
#     for ol in potentiallines:
#         if check_collision(pl, ol, pix): 
#             #If collision, check if k is in another group
#             for k in lines_combinations: 
#                 if tuple(ol) in k:
#                     #If true, append both groups together
#                     line_group.union(k)
#                     replace_list_ol = True
#             if not replace_list_ol:
#                 line_group.add(tuple(ol))
                
#     #Remove both groups and add the new joint one
#     if replace_list_pl:   
#         lines_combinations.remove(j)
#     if replace_list_ol:
#         if j != k:
#             lines_combinations.remove(k)
        
#     lines_combinations.append(line_group)
#     i += 1
#=============================================================================


# plt.figure(figsize = [16, 9])
# plt.imshow(filtered, cmap='gray')
# c = ["salmon", "aqua", "forestgreen", 'khaki', 'peru', 'lightcoral', 'plum']
# for i in range(len(lines_combinations)):
#     print("plot " + str(i) + " of " + str(len(lines_combinations)))
#     l = lines_combinations[i]
#     color = list(colors.CSS4_COLORS.values())[(20 + (i + 3)) % 147]
#     for j in l:
#         plt.plot([j[0], j[2]], [j[1], j[3]], c = color, alpha = 1)
# plt.show()

# plt.figure(figsize = [16, 9])
# plt.imshow(image)
# plt.title('Source', size=20)
# plt.tight_layout()

# df = pd.DataFrame(columns = ["ID", "X_POS", "Y_POS", "WIDTH", "HEIGHT", "AREA", "DANGER LEVEL", "DEFECT TYPE", "PATH"])
# df.to_excel("results.xlsx")
# for l in lines_combinations:
#     ar = np.array(list(l))
#     left_most = ar[int(np.argmin(ar[:, [0,2]])/2)]
    
# plt.figure(figsize = [16, 9])
# plt.imshow(filtered, cmap='gray')
# c = ["salmon", "aqua", "forestgreen", 'khaki', 'peru', 'lightcoral', 'plum']
# i = 0
# ind = [1]
# for j in ind:  
#     l = lines_combinations[j]
#     print("plot " + str(i) + " of " + str(len(lines_combinations)))
#     for j in l:
#         plt.plot([j[0], j[2]], [j[1], j[3]], c = c[i], alpha = 1)
#     i += 1
    
# plt.show()

# df = pd.DataFrame(lines, columns = ["X0", "Y0", "X1", "Y1"])
