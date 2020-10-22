# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 14:39:06 2020

@author: Alexandre
"""

import smbus2
import spidev

class PiSensorAdapter():
    
    def __init__(self, name = "SPI", device_address: int=0x00, config: dict={}):  
        self.name = name
        self.device_address = device_address
        self._config = config
        self._open_sensor()
        self._word_length = 1
        
    @property
    def config(self):
        return self._config
    
    @config.setter
    def config(self, value):
        self._config = value

    @property
    def word_length(self):
        return self._word_length
    
    @word_length.setter
    def word_length(self, value):
        self._word_length = value

    def _open_sensor(self):
        if self.name.upper() in ["SPI", "SPI3", "SPI4"]:
            #TODO: spidev stuff
            print("to be done")
        elif self.name.upper() in ["I2C"]:
            self.bus = smbus2.SMBus(3)
            self.bus.write_byte_data(self.device_address, 0x6b, 0)            
        
    def _read_reg(self, data: int, payload_words: int):
        #Implement burst_read here
        #SPI reading
        if self.name.upper() in ["SPI", "SPI3", "SPI4"]:
            reg = data >> (payload_words * self.word_length) & 0x7F
            result = 0 #TODO: Implement spidev readability
            
        #I2C reading 
        elif self.name.upper() in ["I2C"]:
            reg = data >> ((payload_words * self.word_length) + 8)  
            result = [self.bus.read_byte_data(self.device_address, reg + i) for i in range(payload_words)] #burst read  
        return result 