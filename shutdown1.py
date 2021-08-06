#! /usr/bin/python3
# coding: utf-8

from threading import Thread
import serial
import os
from time import sleep
from smbus2 import SMBus

with SMBus(0) as bus:
    # Read a byte from address 0x10, offset 0
    data = bus.read_byte_data(0x10, 0)
    print("CURRENT DAC MODE: ", data)
    

with SMBus(0) as bus:
    # Write a byte to address 0x10, offset 0
    data = 0x87
    bus.write_byte_data(0x10, 0, data)
    print("NEW DAC MODE: ", data)
    
    
bus.close()

os.system('mpc play')

# os.system('sudo ./volume.py')

# from serial import Serial

ser = serial.Serial("/dev/ttyS1", 115200, timeout=1)
print(ser.name)


#python3 ~/pyscript/app/shutdown1.py

def check_port():
    n = 0
    k = 0
    while True:
        line = ser.readline()
        print("\nLine", line)
        if line == (b'CAN. 0 SM_RUNNING_WAIT_TIMER TIMER ON\r\n'):
            print("ShutDown timer go on")
            os.system('mpc pause')
            k = 1            
        elif line == (b'EXTI. 1 SM_RUNNING TIMER OFF PWR_ON\r\n'):
            with SMBus(0) as bus:
                # Write a byte to address 0x10, offset 0
                data = 0x87
                bus.write_byte_data(0x10, 0, data)
                print("NEW DAC MODE: ", data)
            if k==1:        
                os.system('mpc play')
            n = 0
            k = 2            
            #def run_timer():
            #break
        elif line == (b'USHUTDOWN\r\n'):
            print("\nSHUTDOWN COMMAND:", n)
            os.system('sudo shutdown now')
        else:
            n += 1
            print("\nSeconds:", n)
            #sleep(1)


        # print(line.rstrip())   USHUTDOWN


if __name__ == '__main__':
    # timer = Thread(target=run_timer)
    # mdp_status = Thread(target=check_mdp)
    # checker = Thread(target=check_port)
    # checker.start()
    check_port()
