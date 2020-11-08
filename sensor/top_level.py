#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create
d on Mon Nov  2 16:27:01 2020




@author: pi
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
        self.data = pd.DataFrame(np.array([0,0,0,0,0,0,0,0]).reshape(1, -1), columns = self.col)
        # wr("CMD", 0x11)
        wr("CMD", 0x00)
    
    def capture(self):
        
        # data = rd("gyr_x_7_0", 12) #burst read
        # xPos_0 = rd("acc_x_7_0", 1)
        # xPos_1 = rd("acc_x_15_8", 1)
         # [x_gyr_0, x_gyr_1, 
         # y_gyr_0, y_gyr_1, 
         # z_gyr_0, z_gyr_1, 
         # x_pos_0, x_pos_1,
         # y_pos_0, y_pos_1,
         # z_pos_0, z_pos_1] = data[0]
       
        x_15_8 = rd("acc_x_15_8", 1)
        x_7_0 = rd("acc_x_0_7", 1)
        z_15_8 = rd("acc_z_15_8", 1)
        z_7_0 = rd("acc_z_7_0", 1)
        y_15_8 = rd("acc_y_15_8", 1)
        y_7_0 = rd("acc_y_7_0", 1)
        
        gyr_z_15_8 = rd("gyr_z_15_8", 1)
        gyr_z_7_0 = rd("gyr_z_7_0" , 1)
        gyr_y_15_8 = rd("gyr_y_15_8", 1)
        gyr_y_7_0 = rd("gyr_y_7_0", 1)
        gyr_x_15_8 = rd("gyr_x_15_8", 1)
        gyr_x_7_0 = rd("gyr_x_7_0", 1)
        
        
        z_pos = self.sign((z_15_8 << 8) + z_7_0, 16)/2**14*1000
        y_pos = self.sign((y_15_8 << 8) + y_7_0, 16)/2**14*1000
        x_pos = self.sign((x_15_8 << 8) + x_7_0, 16)/2**14*1000
        
        #CYNRIC TO FILL
        z_gyr = self.sign((gyr_z_15_8 << 8) + gyr_z_7_0, 16)/131
        y_gyr = self.sign((gyr_y_15_8 << 8) + gyr_y_7_0, 16)/131
        x_gyr = self.sign((gyr_x_15_8 << 8) + gyr_x_7_0, 16)/131

        # z_pos = self.sign((z_pos_1 << 8) + z_pos_0, 16)/2**14*1000
        # y_pos = self.sign((y_pos_1 << 8) + y_pos_0, 16)/2**14*1000
        # x_pos = self.sign((x_pos_1 << 8) + x_pos_0, 16)/2**14*1000
        # z_gyr = self.sign((z_gyr_1 << 8) + z_gyr_0, 16)/2**14*1000
        # y_gyr = self.sign((y_gyr_1 << 8) + y_gyr_0, 16)/2**14*1000
        # x_gyr = self.sign((x_gyr_1 << 8) + x_gyr_0, 16)/2**14*1000
    
        t = time.time() - self.start_time
        delta_time = t - self.data["time"][-1:].values[0]
        values = np.array([t, delta_time, x_pos, y_pos, z_pos, x_gyr, y_gyr, z_gyr]).reshape(1, -1)
        
        self.data = self.data.append(pd.DataFrame(values, columns = self.col))
    
    def sign(self, val, bit_length):
        if val >= 2**(bit_length - 1):
            val -= 2**bit_length
        return val
    
    def get_distance(self):
        print('get the distance')
        

# chip_id = rd("chip_id", 1)[0]
# rev_id = rd("rev_id", 1)[0]
# print("Chip id: " + str(chip_id))
# print("Rev id: " + str(rev_id))

fdit = FindItSensor()
fdit.capture()
fdit.capture()
fdit.capture()
fdit.capture()
df = fdit.data