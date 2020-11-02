# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 14:03:39 2020
Test Meta-Language Abstraction 

@author: Alexandre Guichet
"""

tb = None

def read(register_name: str, number_of_items: int=1):
    """
    Read the register

    Parameters
    ----------
    register_name : str
        The register to be read.
    number_of_items : int
        Number of registers to be read.

    Returns
    -------
    read_value : List([str, int])
        The read value from the sensor as list.
    """
    read_value = tb.read_register(register_name, number_of_items)
    return read_value 

def read_and_save(variable_name: str, register_name: str, number_of_items: int=1):
    """
    Read the register and save the value inside the testbench

    Parameters
    ----------
    variable_name : str
        The variable name in which the list read_value will be stored into.
    register_name : str
        The register to be read.
    number_of_items : int
        Number of registers to be read.

    Returns
    -------
    read_value : List([str, int])
        The read value from the sensor as list.
    """
    read_value = tb.read_register(register_name, number_of_items)
    tb.set_variable(variable_name, read_value)    
    return read_value 

#TODO: implement write

def write_and_check(register_name: str, value: [int, list], dly: [float, int]=0):
    """
    

    Parameters
    ----------
    variable_name : str
        The variable name in which the list read_value will be stored into.
    register_name : str
        The register to be read.
    number_of_items : int
        Number of registers to be read.

    Returns
    -------
    read_value : List([str, int])
        The read value from the sensor as List.
    """
    tb.write_register(register_name, value)
    tb.delay(dly)
    read_value = tb.read_register(register_name, len(value))    
    return read_value 
