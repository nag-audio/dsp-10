#!/usr/bin/env python3
import socket
import sys
import time
import select
from smbus2 import SMBus

start_volume = 20
start_channel = 0

channels = [
    [0x00,0x00,0x00,0x04],
    [0x00,0x00,0x00,0x02]
]

volume = [
    [0x00,0x00,0x08,0x40],
    [0x00,0x00,0x0A,0x63],
    [0x00,0x00,0x0D,0x13],
    [0x00,0x00,0x10,0x76],
    [0x00,0x00,0x14,0xB9],
    [0x00,0x00,0x1A,0x17],
    [0x00,0x00,0x20,0xD9],
    [0x00,0x00,0x29,0x5A],
    [0x00,0x00,0x34,0x0F],
    [0x00,0x00,0x41,0x89],
    [0x00,0x00,0x52,0x81],
    [0x00,0x00,0x67,0xDE],
    [0x00,0x00,0x82,0xC3],
    [0x00,0x00,0xCF,0x3E],
    [0x00,0x01,0x04,0xE7],
    [0x00,0x01,0x9D,0x81],
    [0x00,0x02,0x08,0x92],
    [0x00,0x02,0x8F,0x5C],
    [0x00,0x03,0x39,0x0D],
    [0x00,0x04,0x0E,0xAD],
    [0x00,0x05,0x1B,0x9D],
    [0x00,0x06,0x6E,0x31],
    [0x00,0x08,0x18,0x6E],
    [0x00,0x0A,0x31,0x09],
    [0x00,0x0C,0xD4,0x95],
    [0x00,0x10,0x27,0x0B],
    [0x00,0x14,0x55,0xB6],
    [0x00,0x19,0x99,0x9A],
    [0x00,0x20,0x3A,0x7E],
    [0x00,0x28,0x92,0xC2],
    [0x00,0x33,0x14,0x27],
    [0x00,0x40,0x4D,0xE6],
    [0x00,0x50,0xF4,0x4E],
    [0x00,0x65,0xEA,0x5A],
    [0x00,0x80,0x4D,0xCE],
    [0x00,0xA1,0x86,0x6C],
    [0x00,0xCB,0x59,0x18],
    [0x01,0x00,0x00,0x00],
    [0x01,0x00,0x00,0x00],
    [0x01,0x00,0x00,0x00]
]

work_mode = True
current_volume = start_volume
current_channel = start_channel
ERROR = b'ERROR\n'
OK = b'OK\n'
last_time = time.perf_counter()
print("Current second: %d" % last_time)

def set_volume(idx):
    global current_volume
    vol = int(idx)
    if vol > 39: vol = 39
    iic = volume[vol]
    bus = SMBus(0)
    data = [0xF3]
    data.extend(iic)
    print('volume ch1',data)
    bus.write_i2c_block_data(0x3b, 0x09, data)
    data = [0xF2]
    data.extend(iic)
    print('volume ch2',data)
    bus.write_i2c_block_data(0x3b, 0x09, data)
    bus.close()
    current_volume = vol
    time.sleep(0.4)

def set_channel(idx):
    global current_channel
    vol = int(idx)
    if vol > 1: vol = 1
    iic = channels[vol]
    data = [0xA3]
    data.extend(iic)
    print('channel ',data)
    bus = SMBus(0)
    bus.write_i2c_block_data(0x3b, 0x15, data)
    bus.close()
    current_channel = vol

set_volume(start_volume)
set_channel(start_channel)

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sock.setblocking(0)

# Bind the socket to the port
server_address = ('', 10000)
print('starting up on [] port []'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while work_mode:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)
        connection.sendall(b'OK DSP\n')

        # Receive the data in small chunks and retransmit it
        while True:
            ready = select.select([connection], [], [], 15)
            if ready[0]:
                data = connection.recv(16)

                if data:
                    req = data.decode('utf-8');
                    req.lower()
                    req.strip()
                    print(req)
                    if req.startswith('setvol'):
                        setvol = req.split(' ')
                        if ( len(setvol) == 2 ):
                            set_volume(setvol[1])
                            connection.sendall(OK)
                        else:
                            connection.sendall(ERROR)
                    elif req.startswith('getvol'):
                        connection.sendall(bytes(str(current_volume)+'\n', encoding = 'utf-8'))
                        connection.sendall(OK)
                    elif req.startswith('setchan'):
                        params = req.split(' ')
                        if ( len(params) == 2 ):
                            set_channel(params[1])
                            connection.sendall(OK)
                        else:
                            connection.sendall(ERROR)
                    elif req.startswith('getchan'):
                        connection.sendall(bytes(str(current_channel)+'\n', encoding = 'utf-8'))
                        connection.sendall(OK)
                    elif req.startswith('exit'):
                        connection.close()
                        work_mode = False
                        break
                    else:
                        connection.sendall(ERROR)
                else:
                    print('no data from', client_address)
                    break
            else:
                #no data ready
                print('no data ready')
                connection.close()
                break

    finally:
        # Clean up the connection
        connection.close()
