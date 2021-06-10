#!/usr/bin/env python3

import usb.core, usb.util, sys, base64, os, signal

def timeout_handler(signum,frame):
    print('your time is up', flush=True)
    sys.exit(0)

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(60)

filter_path = os.getenv('DEV_PATH')

print('Welcome to hxp\'s TotallyNotBadUSB --- your hardware flag store :>', flush=True)

for dev in usb.core.find(find_all=True, idVendor=0x16c0, idProduct=0x05dc):
    dev_path = str(dev.bus)+'-'+'.'.join([str(x) for x in dev.port_numbers])
    if (filter_path is None or filter_path == dev_path) and (dev.manufacturer == 'hxp.io' and dev.product == 'TotallyNotBadUSB'):
        break
else:
    print('usb device not found :(', flush=True)
    sys.exit(-1)

while True:
    try:
        cmd, index, *data = input('cmd: ').split(';', 2)
        index = int(index)
    except ValueError as e:
        continue


    if cmd == 'r':
        try:
            ret = dev.ctrl_transfer(usb.util.CTRL_TYPE_VENDOR | usb.util.CTRL_RECIPIENT_DEVICE | usb.util.CTRL_IN, 2, 0, index, 254)
            print(base64.b64encode(ret).decode(), flush=True)
        except:
            print('error :(', flush=True)
    elif cmd == 'w':
        try:
            ret = dev.ctrl_transfer(usb.util.CTRL_TYPE_VENDOR | usb.util.CTRL_RECIPIENT_DEVICE | usb.util.CTRL_OUT, 1, 0, index, base64.b64decode(data[0]))
        except:
            print('error :(', flush=True)
    elif cmd == 'q':
        break
