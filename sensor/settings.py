# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 14:43:14 2020

@author: Alexandre Guichet
"""

#================================================
# Variables
#================================================
#the device address, put in there in which port it appears with i2c_detect.
device_address = 0x18


#Use config
use_config = "SPI" #one of ["SPI", "I2C"]


#the register, these are the addresses for BMI160,
#replace by your own Cynric! 
register = {"acc_z_15_8": 0x17, 
            "acc_z_7_0": 0x16,
            "acc_y_15_8": 0x15,
            "acc_y_7_0": 0x14,
            "acc_x_15_8": 0x13,
            "acc_x_7_0": 0x12, 
            "gyr_z_15_8": 0x11,
            "gyr_z_7_0": 0x10,
            "gyr_y_15_8": 0x0F,
            "gyr_y_7_0": 0x0E, 
            "gyr_x_15_8": 0x0D,
            "gyr_x_7_0": 0x0C}


#================================================
# Settings
#================================================
from tmla import read_and_save as rsav

from pisensor import PiSensorAdapter
from testbench import Testbench

tb = Testbench()

tb.use_adapter(use_config)

#load registermap into register
for n, v in register.items():
    tb.add_register(n, v)

#================================================
# I2C protocol
#================================================
config_name = "I2C"

read_date = ['device_address',   
             'wr',                #1st byte
             'register_address',  #2nd byte
             'device_address',    
             'rd',                #3rd byte
             'value']             #4rth byte

write_date = ['device_address', 
              'wr',
              'register_address',
              'value']

length = {"device_address": 7, "rd": 1, "wr": 1, "register_address": 8, "value": 8}
default_value = {"device_address": device_address, "wr": 0, "rd": 1}

I2C_config = {'name': config_name,
              'read_date': read_date,
              'write_date': write_date,
              'length': length,
              'default_value': default_value,}

#Create and configure I2C port
I2C = PiSensorAdapter("MySensor1", device_address, I2C_config)
tb.add_sensor(I2C)

#================================================
# SPI protocol
#================================================
config_name = "SPI"

read_date = ['rd', 'register_address', 'value']
write_date = ['wr', 'register_address', 'value']

length = {'rd': 1, 'wr': 1, 'register_address': 7, 'value':8}
default_value = {'wr': 0, 'rd': 1}

SPI_config = {'name': config_name,
              'read_date': read_date,
              'write_date': write_date,
              'length': length,
              'default_value': default_value,}

#Create and configure SPI port
SPI = PiSensorAdapter("MySensor2", device_address, SPI_config)
tb.add_sensor(SPI)