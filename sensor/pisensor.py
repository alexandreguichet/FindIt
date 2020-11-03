# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 14:39:06 2020

@author: Alexandre
"""

import smbus2
import spidev
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

class PiSensorAdapter():
    
    def __init__(self, name = "SPI", device_address: int=0x00, config: dict={}):  
        self.name = name
        self.device_address = device_address
        self._config = config
        self._open_sensor()
        self._word_length = 8
        
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
        if self._config["name"].upper() in ["SPI", "SPI3", "SPI4"]:
            self.mSPI = spidev.SpiDev()
            self.mSPI.open(0,0)
            self.mSPI.max_speed_hz = int(10e6)
            
        elif self._config["name"].upper() in ["I2C"]:
            self.bus = smbus2.SMBus(1)
        
    def _read_register(self, data: int, payload_words: int):
        #Implement burst_read here
        #SPI reading
        if self._config["name"].upper() in ["SPI", "SPI3", "SPI4"]:
            reg = [data >> (payload_words * self.word_length)]         
            i=0
            while i < payload_words:
                reg.append(0)
                i += 1      
            result = self.mSPI.xfer2(reg)
            result.pop(0)
        elif self._config["name"].upper() in ["I2C"]:
            reg = data >> ((payload_words * self.word_length) + 8)  
            result = [self.bus.read_byte_data(self.device_address, reg + i) for i in range(payload_words)] #burst read
        return result
    
    def _write_register(self, data: int, payload_words: int):
        if self._config["name"].upper() in ["SPI", "SPI3", "SPI4"]:
            reg = [data >> (payload_words * self.word_length)]         
            i=0
            while i < payload_words:
                reg.append((data >> (payload_words - i - 1) * self.word_length) & (2**self.word_length - 1))
                i += 1      
            self.mSPI.xfer2(reg)
        
        


