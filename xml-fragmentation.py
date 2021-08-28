#!/usr/bin/env python3
import xml.etree.cElementTree as ET
import time
import array

from smbus2 import SMBus, i2c_msg

XML_FILE = 'dsp-10.xml'
adau_addr = 59  # 0x3b Адрес процессора на шине
DELAY = 0.010 # 10 milliseconds

class BaseObject:
    def __init__(self, name: str, address: int, addr_incr: int, size: int, data: list):
        self.name = name
        self.address = address
        self.addr_incr = addr_incr
        self.size = size
        self.data = data
    

    def __str__(self) -> str:
        return f'(name: {self.name},'\
            f' address: {self.address},'\
            f' address_increment: {self.addr_incr},'\
            f' size: {self.size})'
    

    def fragment_data(self, fragment_size=28) -> None:
        '''
        Divide our data list into parts of {fragment_size} values
        '''
        fragmented_size = 0
        fragmented_data = []
        initial_len = len(self.data)
        
        while initial_len - fragmented_size >= fragment_size:
            fragmented_data.append(self.data[fragmented_size:fragmented_size + fragment_size])
            fragmented_size += fragment_size

        fragmented_data.append(self.data[fragmented_size:])
        self.data = fragmented_data

    def is_delay(self) -> bool:
        return 'delay' in self.name.lower()


class Register(BaseObject):
    def __str__(self) -> str:
        return 'Register: ' + super.__str__


class Program(BaseObject):
    def __str__(self) -> str:
        return 'Program: ' + super.__str__


def parse_xml(xml_name: str) -> list:
    tree = ET.parse(XML_FILE)
    commands = []
    for node in tree.find('IC'):
        if node.tag == 'Register':
            commands.append(xml_node_to_register(node))
        elif node.tag == 'Program':
            commands.append(xml_node_to_program(node))
    return commands

    
def xml_node_to_object(node: ET.Element, cls: type):
    base_object = cls(
        node.find('Name').text,
        int(node.find('Address').text),
        int(node.find('AddrIncr').text),
        int(node.find('Size').text),
        array.array(
                'H', (int(x, 16) for x in node.find('Data').text.split(', ')[:-1]))
    )
    base_object.fragment_data()
    return base_object


def xml_node_to_register(node) -> Register:
    return xml_node_to_object(node, Register)


def xml_node_to_program(node) -> Program:
    return xml_node_to_object(node, Program)



def adau145x_write(reg_adr, adau_data_4B, bus: SMBus):
    bus.write_i2c_block_data(adau_addr, reg_adr >> 8, [
                             reg_adr & 255] + adau_data_4B)


def adau145x_read(reg_adr, length, bus: SMBus):
    write = i2c_msg.write(adau_addr, [reg_adr >> 8, reg_adr & 255])
    read = i2c_msg.read(adau_addr, length)
    bus.i2c_rdwr(write, read)
    return read.buf[:length]


if __name__ == '__main__':
    start = time.time()

    command_list = parse_xml(XML_FILE)
    parsed_time = time.time()
    print(f"Objects parsed: {parsed_time-start}")

    with SMBus(0) as bus:
        for cmd in command_list:
            if (cmd.is_delay):
                time.sleep(DELAY)
                continue
            for index, fragment in enumerate(cmd.data):
                adau145x_write(cmd.address + 7*index, fragment.tolist(), bus)
    #     # Чтение из шины
    #     for fragment in fragment_data:
    #         print(adau145x_read(register.address, register.size, bus))
    stop = time.time()
    print(f"Write time: {stop-parsed_time}")
    print(f"Delta: {stop-start}")
