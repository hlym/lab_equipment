# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 10:48:09 2019

@author: Heather
"""
import socket
import time

class FunctionGenerator(object):    
    def __init__(self,vna_addr=('128.112.85.243', 5025)):
        self.vna_addr = vna_addr
        
    def vna_send(self,message):
        try:
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.connect(self.vna_addr)
            s.send(message.encode())
        finally:
            s.close()
            
    def set_load_ohms(self, ohms):
        message = 'OUTPUT:LOAD %f \n' %ohms
        self.vna_send(message)
        
    def set_output_on(self):
        message = 'OUTPUT ON \n' 
        self.vna_send(message)
    
    def set_output_off(self):
        message = 'OUTPUT OFF \n' 
        self.vna_send(message)
    
    def set_dc_voltage(self, volts):
        message = 'APPLY:DC DEF, DEF, %f \n' %volts
        self.vna_send(message)
        
    def start_up(self):
        self.set_load_ohms(1000)
        time.sleep(0.3)
        self.set_dc_voltage(0)
        time.sleep(0.3)
        self.set_output_on()