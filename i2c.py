#!/usr/bin/env python3

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
    
    
#print("DAC MODE: ", data)
#print(type(data))
#res = int(str(data1), 16)
#print("DAC MODE : " + str(int(str(data1), 16)))

##data = bus.read_byte_data(0x4d, 0x01)
##print('External temp: ', data)

#data = bus.write_byte_data(0x10, 0, 0x87)
#print('shot:',data)


bus.close()

