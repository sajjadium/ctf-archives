#!/bin/bash

gcc device.c hypercall.c hypervisor.c interrupt.c util.c -o hypervisor -lssl -lcrypto
