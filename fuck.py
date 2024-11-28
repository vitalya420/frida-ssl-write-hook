import base64
import time
from typing import Dict, Literal, TypedDict
import frida
import sys
import gzip

from http_ import is_completed_http_response, parse_http_response

def hexdump(data):
    for i in range(0, len(data), 16):
        chunk = data[i:i+16]
        hex_values = ' '.join(f'{b:02x}' for b in chunk)
        ascii_values = ''.join((chr(b) if 32 <= b < 127 else '.') for b in chunk)
        print(f'{i:04x}  {hex_values:<48}  {ascii_values}')


class Payload(TypedDict):
    func: Literal['SSL_read', 'SSL_write']
    ssl: str

class Message(TypedDict):
    type: Literal['send', 'error']
    payload: Payload


awaits_http_response: Dict[str, bytes] = {}

def on_message(message: Message, data: bytes):
    if message['type'] == 'send':
        if message['payload']['func'] == 'SSL_read':
            # print(f'dumped {len(data)} bytes from ssl read')
            if (key := message['payload']['ssl']) in awaits_http_response:
                awaits_http_response[key] = awaits_http_response[key] + data
                if is_completed_http_response(awaits_http_response[key]):
                    parse_http_response(awaits_http_response[key])
                    awaits_http_response.pop(key)
            elif data.startswith(b'HTTP/'):
                completed = is_completed_http_response(data)
                if not completed:
                    awaits_http_response[message['payload']['ssl']] = data

    #     if 'SSL_read' in message['payload']:
    #         byte_array = message['payload']['SSL_read']
    #         byte_data = bytes(byte_array)
    #         if byte_data.startswith(b'HTTP/'):
    #             parse_http_response(byte_data)
    #         else:
    #             # hexdump(byte_data)
    #             print('not http with len', len(byte_data), message['payload']['ssl'])

            



device = frida.get_usb_device()
pid = device.spawn('com.mcdonalds.mobileapp')
session = device.attach(pid)

with open('script.js') as f:
    script = session.create_script(f.read())

script.on('message', on_message)

script.load()
time.sleep(1)
device.resume(pid)
print('reading stdin')
sys.stdin.read()