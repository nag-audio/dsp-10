#!/usr/bin/env python3

from smbus2 import SMBus

bus = smbus.SMBus(0)
#read register 0x15A5
bus.write_byte_data(0x3b, 0x15, 0xA5)
data = [0x15, 0xA5]

print(bus.read_byte(0x3b))
print(bus.read_byte(0x3b))
print(bus.read_byte(0x3b))
print(bus.read_byte(0x3b))
#print(data)
#read register 0x15A4
bus.write_byte_data(0x3b, 0x15, 0xA4)
data = [0x15, 0xA4]
print(bus.read_byte(0x3b))
print(bus.read_byte(0x3b))
print(bus.read_byte(0x3b))
print(bus.read_byte(0x3b))
#print(data)
#read register 0x15A3
bus.write_byte_data(0x3b, 0x15, 0xA3)
data = [0x15, 0xA3]
print(bus.read_byte(0x3b))
print(bus.read_byte(0x3b))
print(bus.read_byte(0x3b))
print(bus.read_byte(0x3b))

data = [0xA5,0x00,0x04,0x0E,0xAD]
bus.write_i2c_block_data(0x3b, 0x15, data)
bus.write_byte_data(0x3b, 0x15, 0xA5)
data = [0x15, 0xA5]

print(bus.read_byte(0x3b))
print(bus.read_byte(0x3b))
print(bus.read_byte(0x3b))
print(bus.read_byte(0x3b))
#print(data)
#data = bus.read_i2c_block_data(0x3b, 0x15, 0x04)
#data = bus.read_i2c_block_data(0x3b, 0x15, 0x04)
#print('volume ch2', data)
bus.close()
