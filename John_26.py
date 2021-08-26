#!/usr/bin/env python3
import xml.etree.cElementTree as ET
import datetime
from smbus2 import SMBus, i2c_msg


# имя файла
XML_FILE = 'dsp-10.xml'

# тэги по которым нужно искать
UPPER_TAG = 'IC/Register'
#UPPER_TAG = 'IC/Program'

TAG = 'Name'
TARGET_TAG = 'Data'
ADR_TAG = 'Address'

# Содержание тэга Name 
NAME = 'DM1 Data'

now = datetime.datetime.now()
adau_addr = 59 #0x3b Адрес процессора на шине

print ('uSec: %d' % now.microsecond)

def adau145x_write(reg_adr, adau_data_4B):
    with SMBus(0) as bus:
        bus.write_i2c_block_data(adau_addr, reg_adr >> 8, [reg_adr & 255] + adau_data_4B)
def adau145x_read(reg_adr, length):
    with SMBus(0) as bus:
        write = i2c_msg.write(adau_addr, [reg_adr >> 8, reg_adr & 255])
        read = i2c_msg.read(adau_addr, length)
        bus.i2c_rdwr(write, read)
        for i in range(length):
            print(read.buf[i])

def get_data_dict(adr: int, data: str):
    """
    Структура словаря:
    result_dict = {
        'address': int(),
        'data': [
            [...]
            [...]
        ]
    }
    """
    result_dict = dict()
    RANGE = 28     # bytes
    data = data.split(', ')
    new_data = list()
    counter = 0
    while len(data) > 0:
        new_data.append(list())
        for i in range(RANGE):
            try:
                print (str(i))
                num = int(data[i], 16) #
                new_data[counter].append(num)
            except:
                break
        counter += 1
        try:
            data = data[RANGE:]
        except:
            break
    if len(new_data[-1])==0:
        new_data.pop()
    result_dict['address'] = adr
    result_dict['data'] = new_data
    return result_dict

def get_xml_data(xml_file: str, upper_tag: str, tag: str, target_tag: str, adr_tag: str, name: str):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    for upper_t in root.findall(upper_tag):
        lower_t = upper_t.find(tag)
        if name == lower_t.text:
            adr = int(upper_t.find(adr_tag).text)
            data = upper_t.find(target_tag).text
    return adr, data


def print_hex(int_list: list):
    hex_list = list()
    for num in int_list:
        hex_list.append(hex(num))
    print(hex_list)

print('get_xml_data')
adr, data = get_xml_data(XML_FILE, UPPER_TAG, TAG, TARGET_TAG, ADR_TAG, NAME)
print('get_data_dict')
data = get_data_dict(adr, data)
# test_data28b = [0x0C, 0x02, 0xDC, 0xA, 0x0C, 0x03, 0xDC, 0xA, 0x0C, 0x04, 0xDC, 0xA, 0x0C, 0x05, 0xDC, 0xA, 0x0C, 0x06, 0xDC, 0xA, 0x0C, 0x07, 0xDC, 0xA, 0x0C, 0x08, 0xDC, 0xA]

# Пример использования:
print('target_address')
target_address = data['address']
print('hex_data')
hex_data = data['data'] #Список списков
print('adau145x_write')

for hex_list in hex_data:
    #print(hex_list)
    # ну или отправляем список data_list для записи
    #print_hex(hex_list)
    adau145x_write(target_address, hex_list)
    #print('send\n')
