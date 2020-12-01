# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 10:58:59 2020

@author: Alexandre
"""
import cv2

from scipy.ndimage import gaussian_filter, sobel
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, Normalize

from skimage import filters
from skimage.io import imread
from skimage.color import rgb2gray


"""
Laplacian Filter
"""

# depth = cv2.CV_32F
# kernel_size = 3


# image = cv2.imread('../data/GPTempDownload(0).jpg')
# image = cv2.GaussianBlur(image, (3, 3), 0)
# image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# plt.figure(figsize = [20, 20])
# plt.subplot(121)
# plt.imshow(image)
# plt.title('original', size=20)

# image = cv2.Laplacian(image, depth,  ksize=kernel_size)
# image = cv2.convertScaleAbs(image)

# plt.subplot(122)
# norm = LogNorm(image.mean() + 0 * image.std(), image.max())
# plt.imshow(image, norm = norm, origin = "lower")
# plt.title('laplacian filter', size=20)
# plt.tight_layout()

"""
Sobel Filter
"""

# image = imread('../data/GPTempDownload(0).jpg')
# image = rgb2gray(image)

# plt.figure(figsize = [20, 20])
# plt.subplot(221)
# plt.imshow(image)
# plt.title('original', size=20)

# plt.subplot(222)
# edges_x = filters.sobel_v(image)
# plt.imshow(edges_x)
# plt.title('sobel_x', size=20)

# plt.subplot(223)
# edges_y = filters.sobel_h(image) 
# plt.imshow(edges_y)
# plt.title('sobel_y', size=20)

# plt.subplot(224)
# edges = filters.sobel(image)
# plt.imshow(edges)
# plt.title('sobel', size=20)

"""
Gaussian Filter
"""

image = cv2.imread('../data/GPTempDownload(0).jpg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# plt.figure(figsize = [20, 20])
# plt.subplot(221)
# plt.imshow(image, cmap='gray', vmin = 0, vmax = 255)
# plt.title('original', size=20)

image = image.astype(float)
image = gaussian_filter(image, sigma = 1)

df = pd.DataFrame(image)
gx = df.diff(axis = 1).drop(columns = df.columns[0])
gy = df.diff().drop(df.index[0])

magnitude = (gx.drop(df.index[0]).values**2 + gy.drop(columns = df.columns[0]).values**2)**(1/2)

# plt.subplot(222)
# norm = LogNorm(gx.mean().mean() + 0.5 * gx.std().std(), gx.max().max())
# plt.imshow(gx.values, norm = norm, origin = "lower", cmap = 'gray')
# plt.imshow(gx.values)
# plt.title('gradiant in x', size=20)

# plt.subplot(223)
# norm = LogNorm(gy.mean().mean() + 0.5 * gy.std().std(), gy.max().max())
# plt.imshow(gy.values, norm = norm, origin = "lower", cmap = 'gray')
# plt.imshow(gy.values)
# plt.title('gradiant in y', size=20)

# plt.subplot(224)
# norm = LogNorm(magnitude.mean().mean() + 0.5 * magnitude.std().std(), magnitude.max().max())
# plt.imshow(magnitude, norm = norm, origin = "lower", cmap = 'gray')
# plt.imshow(magnitude)
# plt.title('grandiant magnitude', size=20)

# plt.tight_layout(h_pad = 20, rect=[0, 0.03, 1, 0.95])

"""
Adaptive Thresholding
"""
vmin = magnitude.mean().mean() + 0.5 * magnitude.std().std()
vmax = magnitude.max().max()
np.log(magnitude, magnitude)
result = magnitude.copy()
result -= np.log(vmin)
result /= (np.log(vmax) - np.log(vmin))

magnitude = result.copy() * 255
plt.imshow(result, cmap = "gray")
plt.title("Custom Logarithmic Scaling Algorithm")
plt.tight_layout()

# magnitude = cv2.normalize(src = magnitude, dst=None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)

# magnitude = cv2.imread('../data/Gradiants/log_norm_magnitude.png')
# magnitude = cv2.cvtColor(magnitude, cv2.COLOR_BGR2GRAY)

ret,thresh1 = cv2.threshold(magnitude,20, 255,cv2.THRESH_BINARY)
plt.figure()
plt.imshow(thresh1, cmap='gray')
plt.title('Binary Image, threshold = 20')
plt.tight_layout()
# ret,th1 = cv2.threshold(magnitude,magnitude.mean(),255,cv2.THRESH_BINARY)
# th2 = cv2.adaptiveThreshold(magnitude,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
#             cv2.THRESH_BINARY,11,2)
# th3 = cv2.adaptiveThreshold(magnitude,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
#             cv2.THRESH_BINARY,11,2)
    

# titles = ['Original Image', 'Binary', 'Global Thresholding (v = 127)',
#             'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
# images = [magnitude, thresh1, th1, th2, th3]


# for i in range(5):
#     plt.subplot(2,3,i+1),plt.imshow(images[i],'gray')
#     plt.title(titles[i])
#     plt.xticks([]),plt.yticks([])
# plt.show()