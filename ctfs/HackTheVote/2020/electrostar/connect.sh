#!/bin/bash
socat tcp:54.144.21.40:9000 FILE:`tty`,rawer,echo=0,icrnl=1,escape=0x03
