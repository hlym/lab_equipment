# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 10:57:13 2019

@author: Heather
"""
import socket
import time

class VNA(object):    
    def __init__(self,addr = ('128.112.84.171', 5025)):
        self.addr = addr
        
    def send_cmd(self, message):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect(self.addr)
        s.send(message.encode())
        s.close()
        
    def query(self,message):
        time.sleep(1)
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect(self.addr)
        s.send(message.encode())
        result = s.recv(1024)
        s.close()
        return result
    
    def reset(self):
        message = ':SYST:PRES \n'
        self.send_cmd(self, message)
        time.sleep(2)
        
    def set_start_freq(self,start_freq):
        message = ':SENS1:FREQ:STAR %f \n' %start_freq
        self.send_cmd(message)
    
    def get_start_freq(self):
        message = ':SENS1:FREQ:STAR? \n'
        result = self.query(message)
        print(result)
        return result

    def set_end_freq(self,stop_freq):
        message = ':SENS1:FREQ:STOP %f \n' %stop_freq
        self.send_cmd(message)
    
    def get_stop_freq(self):
        message = ':SENS1:FREQ:STOP? \n'
        result = self.query(message)
        print(result)
        return result

    def set_num_points(self,num_of_points=10000):
        message = ':SENS:SWE:POIN %f \n' %num_of_points
        self.send_cmd(message)
    
    def get_num_points(self):
        message = ':SENS:SWE:POIN? \n'
        result = self.query(message)
        print(result)
        return result

    def set_if_bandwidth(self,if_bandwidth=1000):
        message = ':SENS1:BAND %f \n' %if_bandwidth
        self.send_cmd(message)


    def get_if_bandwidth(self):
        message = ':SENS1:BAND? \n'
        result = self.query(message)
        print(result)
        return result

    def set_power_level(self,power_level=-20):
        message = ':SOUR1:POW %f \n' %power_level
        self.send_cmd(message)
        
    def get_power_level(self):
        message = ':SOUR1:POW? \n'
        result = self.query(message)
        print(result)
        return result

    def set_s21_parameter(self):
        message = ':CALC1:PAR1:DEF S21 \n' 
        print(message)
        self.send_cmd(message)
    
    def get_s21_parameter(self):
        message = ':CALC1:PAR1:DEF? \n'
        result = self.query(message)
        print(result)
        return result

    def get_sweep_time(self):
        message = ':SENS1:SWE:TIME? \n'
        result = self.query(message)
        print(result)
        return result

    def get_s_data(self):
        message = ':CALC1:DATA:FDAT? \n' 
        result = self.query(message)
        print(result)
        return result

    def set_data_format_REIM(self):
        message = ':CALC1:FORM POL \n'
        self.send_cmd(message)
    
    def set_data_format_LOGMAG(self):
        message = ':CALC1:FORM MLOG \n'
        self.send_cmd(message)
    
    def get_data_format(self):
        message = ':CALC1:FORM? \n'
        result = self.query(message)
        print(result)
        return result
    
    def get_freq_data(self):
        message = ':SENS1:FREQ:DATA? \n'
        result = self.query(message)
        print(result)
        return result
    
    def get_data_type(self):
        message = ':FORM:DATA? \n'
        result = self.query(message)
        print(result)
        return result
    
    def set_data_type(self, dtyp='ASC'):
        #REAL OR ASC
        message = ':FORM:DATA %s \n' %dtyp
        self.send_cmd(message)
        
    def write_s2p_file(self,file_path):
        message = ':MMEM:STOR:SNP:TYPE:S2P 1,2 \n'
        self.send_cmd(message)
        message = ':MMEM:STOR:SNP %s \n'
        self.send_cmd(message)
    
    def write_csv_file(self,file_path):
        message = ':MMEM:STOR:FDAT %s \n' % file_path
        print(message)
        self.send_cmd(message)
        
    def write_screen_image(self, file_path):
        message = ':MMEM:STOR:IMAG %s \n' % file_path
        print(message)
        self.send_cmd(message)
    
    def get_vna_info(self):
        message = ':MMEM:STOR:SNP:TYPE:S2P? \n'
        result = self.query(message)
        print(result)
        return result
    
    def set_active_trace(self,trace_num=1, channel_num=1):
        message = ':CALC1:PAR1:SEL'
        self.send_cmd(message)
        
    def get_error(self):
        message = ':SYST:ERR? \n'
        result = self.query(message)
        print(result)
        return result
    
    def normal_start_up(self):
        message = '*CLS \n'
        self.send_cmd(message)
    
        message = '*OPC? \n'
        self.send_cmd(message)
        
        #set our data type for recieving 
        self.set_data_type(dtyp='ASC')
        self.get_data_type()
        
        #set the number of points
        self.set_num_points(10000)
        self.get_num_points()
        
        #set the power level to -20
        self.set_power_level(power_level=-20)
        self.get_power_level()
    
        #set the vna to s21
        self.set_s21_parameter()
        
        #actiavte the trace 
        self.set_active_trace()
        
        #look at it in logmag
        self.set_data_format_LOGMAG()
        
    def get_freq_sweep(self,f_start, f_stop, voltage=0, if_bandwidth=1000,power_level=-20):
        self.set_start_freq(f_start)
        self.get_start_freq()
        
        self.set_end_freq(f_stop)
        self.get_stop_freq()
        
        self.set_if_bandwidth(if_bandwidth)
        self.get_if_bandwidth()
        
        #get ready to take data and set the format
        self.set_data_format_REIM()
        self.get_data_format()
        
        #get sweep time
        sweep_time = self.get_sweep_time()
        wait_time = int(float(sweep_time)) + 5
        
        print('waiting %s s for freq sweep to be done' % wait_time)
        
        time.sleep(wait_time)
        
        print('finished freq sweep from %s to %s Hz at BW %s Hz and %s dB power' %(f_start, f_stop, if_bandwidth, power_level))
        
        f_start_ghz = f_start*1e-9
        f_stop_ghz = f_stop*1e-9
        power_level_abs = abs(power_level)
        
        #save csv file
        timestamp = time.time()
        file_path = '"D:/State/20190413_MMBv1p_512box_flex3/%.2f-f_%.2f_to_%.2f-bw_%.1f-atten_%.1f-volts_%.3f.csv"' %(timestamp, f_start_ghz, f_stop_ghz, if_bandwidth, power_level_abs, voltage)
    
        message = ':MMEM:STOR:FDAT %s \n' % file_path
        self.send_cmd(message)
        print(message)
    
        time.sleep(2)
        
        #save s2p file
        file_path = '"D:/State/20190413_MMBv1p_512box_flex3/%.2f-f_%.2f_to_%.2f-bw_%.1f-atten_%.1f-volts_%.3f.s2p"' %(timestamp,f_start_ghz, f_stop_ghz, if_bandwidth, power_level_abs, voltage)
    
        message = ':MMEM:STOR:SNP:FORM RI \n'
        self.send_cmd(message)
    
        message = ':MMEM:STOR:SNP:TYPE:S2P 1,2 \n'
        self.send_cmd(message)
        
        message = ':MMEM:STOR:SNP %s \n' %file_path
        print(message)
        self.send_cmd(message)
        
        self.get_error()
        
        print('done saving data for sweep')
        
        time.sleep(2)
        
        

    











