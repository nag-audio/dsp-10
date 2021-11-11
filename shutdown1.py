#! /usr/bin/python3
# coding: utf-8
# v1.1 27.11.2021 +uuid

''' полезные команды
 pkill sigma_tcp
 pip3 install watchdog
 python3 /programs/shutdown1.py
 os.system('python3 /programs/XMLLoader/i2c_smbus2.py') это не нужно - входит в ХМЛ лоадер

'''
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from threading import Thread
import serial
import os, socket
from time import sleep
import uuid

#print('NAG-AUDIO DSP-10 deamon')

os.system('python3 /programs/XMLLoader/xml-loader.pyc') #инициализация ДСП и ЦАП!
sleep(0.1)
os.system('nohup /programs/XMLLoader/sigma_tcp i2c /dev/i2c-0 0x3b &')
#os.system('/programs/XMLLoader/sigma_tcp i2c /dev/i2c-0 0x3b')
sleep(0.1)
os.system('mpc play')



ser = serial.Serial("/dev/ttyS1", 115200, timeout=1)

def UART_port():
    n = 0
    k = 0
    while True:
        line = ser.readline()
        #print("\nLine", line)
        if line == (b'CAN. 0 SM_RUNNING_WAIT_TIMER TIMER ON\r\n'):
            #print("ShutDown timer go on")
            os.system('mpc pause')
            k = 1            
        elif line == (b'EXTI. 1 SM_RUNNING TIMER OFF PWR_ON\r\n'):
            if k==1:        
                os.system('mpc play')
            n = 0
            k = 2            
            #break
        elif line == (b'USHUTDOWN\r\n'):
            #print("\nSHUTDOWN COMMAND:", n)
            os.system('sudo shutdown now')
        else:
            n += 1
            #print("\nSeconds:", n)
         # print(line.rstrip())   USHUTDOWN

def broadcast_response():
    port = 5559
    bufferSize = 1024
    response_json = '{"mfq": "NAG",  "model": "DSP-10",  "pid": "23102021",  "hw": "1.0",  "sw": "1.0",  "uuid": "' + str(uuid.uuid1()) +'"}'
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('0.0.0.0', port))

    while True:
        data, addr = s.recvfrom(bufferSize)
        print ("request: ", data, ", from: ", addr)
        s.sendto(response_json.encode('utf-8'), addr)

if __name__ == '__main__':
    UART_Thread = Thread(target=UART_port)
    UART_Thread.start()

    XML_Thread = Thread(target=broadcast_response)
    XML_Thread.start()
