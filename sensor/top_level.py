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
        dly(5e-3) #delay of 5ms to wait for accel stabilisation
        
        a_range = rd("acc_range")[0][0]
        if a_range == 3:
            a_range = 2 #G
        elif a_range == 5:
            a_range = 4 #G
            
        data = rd("acc_x_7_0", 6) #burst read
                
        [x_pos_0, x_pos_1,
          y_pos_0, y_pos_1,
          z_pos_0, z_pos_1] = data[0]
       
        wr("CMD", 0x15) #open gyro config
        dly(80e-3) #delay of 80ms to wait for gyro stabilisation
        
        gyro_range = rd("gyro_range")[0][0]
        
        if gyro_range == 0:
            gyro_range = 2000 #*/s
        elif gyro_range == 1:
            gyro_range = 1000 #*/s
        elif gyro_range == 2:
            gyro_range = 500
        elif gyro_range == 3:
            gyro_range = 250
        elif gyro_range == 4:
            gyro_range = 125
            
        data = rd("gyr_x_7_0", 6)
        
        [x_gyr_0, x_gyr_1, 
          y_gyr_0, y_gyr_1, 
          z_gyr_0, z_gyr_1] = data[0]

        
        z_pos = self.sign((z_pos_1 << 8) + z_pos_0, 16)/(2**15/a_range*9.81)
        y_pos = self.sign((y_pos_1 << 8) + y_pos_0, 16)/(2**15/a_range*9.81)
        x_pos = self.sign((x_pos_1 << 8) + x_pos_0, 16)/(2**15/a_range*9.81)
        z_gyr = self.sign((z_gyr_1 << 8) + z_gyr_0, 16)/(2**15/gyro_range)
        y_gyr = self.sign((y_gyr_1 << 8) + y_gyr_0, 16)/(2**15/gyro_range)
        x_gyr = self.sign((x_gyr_1 << 8) + x_gyr_0, 16)/(2**15/gyro_range)
    
        t = time.time() - self.start_time
        delta_time = t - self._data["time"][-1:].values[0]
        values = np.array([t, delta_time, x_pos, y_pos, z_pos, x_gyr, y_gyr, z_gyr]).reshape(1, -1)
        
        self._data = self._data.append(pd.DataFrame(values, columns = self.col), ignore_index = True)
    
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