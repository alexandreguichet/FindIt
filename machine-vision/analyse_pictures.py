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

import numpy as np
import os

from skimage import color
from skimage import io
from skimage.color import rgb2gray

from tools.utils import find_gray, to_hex, find_val, to_rgb, normalize_to_gray

path = r"..\data\unprocessed"
gray = [138, 129, 124]

pictures = load_files(path, gray = False)

image = pictures[0]
grayscale = normalize_to_gray(rgb2gray(image))

hist_hex, image_hex = to_hex(image)

plt.figure(figsize = [16, 9])
plt.hist(grayscale.flatten(), bins = 2000)
plt.title('Source', size=20)
plt.tight_layout()

# plt.figure(figsize = [16, 9])
# plt.imshow(pictures[0])
# plt.title('Source', size=20)
# plt.tight_layout()

# plt.figure(figsize = [16, 9])
# plt.imshow(image_hex, cmap='gray')
# plt.title('Source', size=20)
# plt.tight_layout()

val, count = np.unique(grayscale.flatten(), return_counts = True)
target = val[np.argmax(count)]
temp = find_val(grayscale, target, tolerance = 0.1)

extracted_image = image.copy()
extracted_image[temp == 0] = 0

plt.figure(figsize = [16, 9])
plt.imshow(extracted_image)
plt.title('Source', size=20)
plt.tight_layout()

# lp = Laplacian()
# sb = Sobel()
# gs = Gaussian()
# ad = Adaptative()
# cn = Canny()

# filtered, final, lines = hough_transform(pictures[3], ad)
# filtered, final, lines = hough_transform(pictures[0], cn)
# filtered, final, lines = hough_transform(pictures[0], gs)
# filtered, final, lines = hough_transform(pictures[0], lp)
# filtered, final, lines = hough_transform(pictures[0], sb)

# debug only
# plt.figure(figsize = [16, 9])
# plt.imshow(pictures[3], cmap='gray')
# plt.title('Source', size=20)
# plt.tight_layout()

# plt.figure(figsize = [16, 9])
# plt.imshow(filtered, cmap='gray')
# plt.title('Source after filtering', size=20)
# plt.tight_layout()

# plt.figure(figsize = [16, 9])
# plt.imshow(filtered, cmap='gray')
# for l in lines: 
#     l = l[0]
#     plt.plot([l[0], l[2]], [l[1], l[3]], c = 'salmon', alpha = 0.7)
# plt.title('Source after filtering', size=20)
# plt.tight_layout()

# plt.figure(figsize = [16, 9])
# plt.imshow(image)
# plt.title('Source', size=20)
# plt.tight_layout()

aa = find_gray(image, tolerance = 0.01)

# plt.figure(figsize = [16, 9])
# plt.imshow(aa)
# plt.title('Source', size=20)
# plt.tight_layout()
