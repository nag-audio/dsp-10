'''
Добавить:
    Работа через консоль
                    -filename-    -cmd- -arg1-          -arg2-          -arg3-
        0. python3 ./xml-fragmentation.pyc xload [filename]                                  - return pass/fail string   (XML to DSP upload)
            @python3 ./xml-fragmentation.pyc xload ./dsp-10.xml
        1. python3 ./xml-fragmentation.pyc adrrd [addr:int16] [length:DEC]                   - return string list        (direct read to I2C)
            @python3 ./xml-fragmentation.pyc adrrd 62816 2                   - return: 8192
        2. python3 ./xml-fragmentation.pyc adrwr [addr:int16] [DATA:32b int]               - return pass/fail string   (direct write to I2C)
            @python3 ./xml-fragmentation.pyc adrwr 45055 0x00, 0x00, 0x00, 0x61
        3. python3 ./xml-fragmentation.pyc xmlrd [TAG:string] [NAME:string]                  - return string list        (TAG of register/module/program) (NAME of DATA/)
        4. python3 ./xml-fragmentation.pyc xmlwr [TAG:string] [NAME:string] [DATA:byte list] - return pass/fail string 
'''

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
    print(f"Parsed: {round(parsed_time-start,1)}" + ' sec.')

    with SMBus(0) as bus:
        for cmd in command_list:
            if (cmd.is_delay()):
                time.sleep(DELAY)
                continue
            for index, fragment in enumerate(cmd.data):
                adau145x_write(cmd.address + 7*index, fragment.tolist(), bus)
        time.sleep(DELAY)
        adau145x_write(cmd.address + 7*index, fragment.tolist(), bus)
    

    #print(f"Write time: {stop-parsed_time}")
    
stop = time.time()
print(f"Bus write: {round(stop-start,1)}" + ' sec.')

with SMBus(0) as bus:
    # DAC run
    data = 0x87
    bus.write_byte_data(0x10, 0, data)
    # MUTE OFF
    stop = time.time()
    adau145x_write(0xF528, [0x00, 0x01], bus)
    
    '''
                <Name>IC 1.MP8_WRITE</Name>
            <Address>62760</Address>
            <AddrIncr>0</AddrIncr>
            <Size>2</Size>
            <Data>0x00, 0x00, </Data>
'''
    
