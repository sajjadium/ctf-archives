#!/bin/bash
avrdude -c usbasp -p m8 -U hfuse:w:0xC9:m -U lfuse:w:0xEF:m -e -U flash:w:main.hex
avrdude -c usbasp -p m8 -U lock:w:0xFC:m -V
