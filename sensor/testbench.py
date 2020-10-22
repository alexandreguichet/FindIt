# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 12:08:47 2020

@author: Alexandre Guichet
"""
import tmla
import time
import os

class Testbench(object):
    
    def __init__(self, log_path: str= "./log/data.log"):
        tmla.tb = self
        
        self.device_address = 0
        self.variables = {}
        
        self._log_path = log_path
        
        self._sensor = {}     
        self._register_map = {}

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
        #TODO: read_register
        results = list()
        for sen in self.sensor:
            #Create byte with data      
            data = 0
            conf = sen.config
            conf["default_value"]["register_address"] = self.get_register(register_name)
            
            for field in [f for f in conf["read_date"] if f != "value"]:
                data = data << conf["length"][field]
                data != conf["default_value"][field]
                
            for v in range(payload_words):
                data = data << conf["length"]["value"]
                data != 0 
            
            r = sen.read_register(data, payload_words) #result of the burst read       
            results.append(r)
        return results
        
    def write_register(self, register_name: str, value: [list, int]):
        #TODO: implement write_register
        print("TODO")        
    
    def delay(self, delay: [float, int]=0):
        time.sleep(delay)
        
#-----------------------------------------------------------------------------
# Variables/Properties

    @property
    def log_path(self) -> str:
        """Set log path
        """
        return self._log_path
    
    @log_path.setter
    def log_path(self, log_path_str: str):
        """Make sure the logfile exists already and is already set
        """
        #TODO: Log_path
        print("to be done")
        
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
        #TODO: make it work for time-series
        self.variable[var] = value
        
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
        #get register value from address
        assert address in self._register_map
        return self._register_map[address]
        
    #TODO: might not be needed
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
        #TODO: make it dictionary 
        self.sensor[sensor.name] = sensor
        
    def main_sensor(self, adapter_name: str) -> type(None):
        #TODO: what is the best way to chose the main adapter?
        #TODO: not sure we'll use that
        self._main_adapter = adapter_name
    