#!/usr/bin/env python3
import xml.etree.cElementTree as ET
import time
import array

from smbus2 import SMBus, i2c_msg

XML_FILE = 'dsp-10.xml'
adau_addr = 59 #0x3b Адрес процессора на шине


class Register:
    def __init__(self, name: str, address: int, addr_incr: int, size: int, data: list):
        self.name = name
        self.address = address
        self.addr_incr = addr_incr
        self.size = size
        self.data = data
    def __str__(self) -> str:
        return self.__dict__.__str__()

class Program(Register):
    pass

def query_node(type: str, name: str):
    tree = ET.parse(XML_FILE)
    node = tree.find(f".//{type}/*[.='{name}']/..")
    params = {}
    for child in node:
        tag = child.tag
        if tag == 'Data':
            params['data'] = array.array('H', (int(x, 16) for x in child.text.split(', ')[:-1]))
        elif tag == 'Name':
            params[tag.lower()] = child.text
        elif tag == 'Address':
            params[tag.lower()] = int(child.text)
        elif tag == 'AddrIncr':
            params['addr_incr'] = int(child.text)
        elif tag == 'Size':
            params[tag.lower()] = int(child.text)
    return params

def query_register(name: str):
    return Register(**query_node('Register', name))

def query_program(name: str):
    return Program(**query_node('Program', name))

def adau145x_write(reg_adr, adau_data_4B, bus: SMBus):
    bus.write_i2c_block_data(adau_addr, reg_adr >> 8, [reg_adr & 255] + adau_data_4B)

def adau145x_read(reg_adr, length, bus: SMBus):
    write = i2c_msg.write(adau_addr, [reg_adr >> 8, reg_adr & 255])
    read = i2c_msg.read(adau_addr, length)
    bus.i2c_rdwr(write, read)
    return read.buf[:length]

def fragment_data(data: list):
    FRAGMENT_SIZE = 28     # bytes
    copyIndex = 0
    fragmented_data = []
    while copyIndex < len(data):
        if (len(data) - copyIndex ) > FRAGMENT_SIZE:
            fragmented_data.append(data[copyIndex:copyIndex+FRAGMENT_SIZE])
        else:
            fragmented_data.append(data[copyIndex:])
        copyIndex += FRAGMENT_SIZE
    return fragmented_data

if __name__ == '__main__':
    start = time.time()
    print(f"Start: {start}")

    register = query_register('DM1 Data')
    print(f"Register parsed: {time.time()-start}")
    fragmented_data = fragment_data(register.data)
    
    stop = time.time()
    print(f"Stop: {stop}")
    print(f"Delta: {stop-start}")
    
    with SMBus(0) as bus:
        # Запись в шину
        for index, fragment in enumerate(fragmented_data):
            print(f"Write fragment: [index: {index}, size: {len(fragment)} bytes]")
            adau145x_write(register.address + 7*index, fragment, bus)
    #     # Чтение из шины
    #     for fragment in fragment_data:
    #         print(adau145x_read(register.address, register.size, bus))
    
