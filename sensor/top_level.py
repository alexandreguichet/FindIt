#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 16:27:01 2020

@author: Alexandre Guichet
"""

from settings import *
import pandas as pd
import numpy as np
import time

class FindItSensor():
    
    def __init__(self):
        self.start_time = time.time()
        
        self.col = ['time', 'delta_time', 
               'x_pos', 'y_pos', 'z_pos', 
               'x_gyr', 'y_gyr', 'z_gyr']
        self._data = pd.DataFrame(np.array([0,0,0,0,0,0,0,0]).reshape(1, -1), columns = self.col)
    
    @property
    def data(self):
        data = self._data
        return data.iloc[1:]
            
    def capture(self):      
        wr("CMD", 0x11) #open accelerometer config
        data = rd("acc_x_7_0", 6) #burst read
        
        [x_pos_0, x_pos_1,
          y_pos_0, y_pos_1,
          z_pos_0, z_pos_1] = data[0]
       
        wr("CMD", 0x15) #open gyro config
        data = rd("gyr_x_7_0", 6)
        
        [x_gyr_0, x_gyr_1, 
          y_gyr_0, y_gyr_1, 
          z_gyr_0, z_gyr_1] = data[0]

        
        z_pos = self.sign((z_pos_1 << 8) + z_pos_0, 16)/2**14*1000
        y_pos = self.sign((y_pos_1 << 8) + y_pos_0, 16)/2**14*1000
        x_pos = self.sign((x_pos_1 << 8) + x_pos_0, 16)/2**14*1000
        z_gyr = self.sign((z_gyr_1 << 8) + z_gyr_0, 16)/131
        y_gyr = self.sign((y_gyr_1 << 8) + y_gyr_0, 16)/131
        x_gyr = self.sign((x_gyr_1 << 8) + x_gyr_0, 16)/131
    
        t = time.time() - self.start_time
        delta_time = t - self._data["time"][-1:].values[0]
        values = np.array([t, delta_time, x_pos, y_pos, z_pos, x_gyr, y_gyr, z_gyr]).reshape(1, -1)
        
        self._data = self._data.append(pd.DataFrame(values, columns = self.col))
    
    def sign(self, val, bit_length):
        if val >= 2**(bit_length - 1):
            val -= 2**bit_length
        return val
    
    def get_distance(self):
        print('get the distance')
        


#chip_id = rd("chip_id", 1)[0]
#rev_id = rd("rev_id", 1)[0]
#print("Chip id: " + str(chip_id))
#print("Rev id: " + str(rev_id))

fdit = FindItSensor()
fdit.capture()
fdit.capture()
fdit.capture()
fdit.capture()
df = fdit.data