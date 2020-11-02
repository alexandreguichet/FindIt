# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 12:08:47 2020

@author: Alexandre Guichet
"""
import tmla
import time
import os

class Testbench(object):
    
    def __init__(self):
        tmla.tb = self
        
        self.variables = {}
                
        self._sensor = {}     
        self._register_map = {}
        self._main_sensor = ""

    def read_register(self, register_name: str, payload_words: int) -> list:
        """
        Read Register
        
        Parameters
        ----------
        register_name : str
            Register name
        
        payload_words : int
            Number of registers to read
            
        Returns
        -------
        results : list
            Values read
        """
        results = list()
        sensors = [self.sensor[i] for i in self._main_sensor]
        for sen in sensors:
            #Create byte with data   
            data = 0
            conf = sen.config
            conf["default_value"]["register_address"] = self.get_register(register_name)
            
            for field in [f for f in conf["read_date"] if f != "value"]:
                data = data << conf["length"][field]
                data |= conf["default_value"][field]
                
            for v in range(payload_words):
                data = data << conf["length"]["value"]
                data |= 0 
            
            r = sen._read_register(data, payload_words) #result of the burst read       
            results.append(r)
        return results
        
    def write_register(self, register_name: str, value: [list, int]):
        #TODO: implement write_register
        print("TODO")        
    
    def delay(self, delay: [float, int]=0):
        time.sleep(delay)
        
#-----------------------------------------------------------------------------
# Variables/Properties
        
    def set_variable(self, var: str, 
                     value: [int, float, str, list, dict, set, tuple]):
        """
        Set variable to use.

        Parameters
        ----------
        var : str
            Variable name.
        value : [int, float, str, list, dict, set, tuple]
            Variable value.


        """
        self.variables[var] = value
        
    def get_variable(self, var: str) -> [int, float, str, list, dict, set, tuple]:
        """Get a variable from the dictionary
        """
        if var in self.variables:
            return self.variables[var]
        else:
            return None
    
    def get_register(self, address: str) -> int:
        """
        Get address from register map
        
        Parameters
        ----------
        address : str
            Register name
            
        Returns
        -------
        reg : int
            Register value
        """
        assert address in self._register_map
        return self._register_map[address]
        
    @property
    def sensor(self):
        return self._sensor
    
    @sensor.setter
    def sensor(self, sensor):
        self._sensor = sensor
           
#-----------------------------------------------------------------------------
# Setup
        
    def add_register(self, register_name: str, address: int) -> type(None):
        self._register_map[register_name] = address
    
    def add_sensor(self, sensor) -> type(None):
        self.sensor[sensor.name] = sensor
        
    def select_sensor(self, sensor_name: list) -> type(None):
        #TODO: what is the best way to chose the main adapter?
        #TODO: not sure we'll use that
        self._main_sensor = sensor_name
    