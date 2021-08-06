#! /usr/bin/python3
# coding: utf-8
import serial
import time

ser = serial.Serial("/dev/ttyS1",115200,timeout=1)
while 1:
    time.sleep(1)
    print (ser.readline()) #How do I get the most recent line sent from the device?

