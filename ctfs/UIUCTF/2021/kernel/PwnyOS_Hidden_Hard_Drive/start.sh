#!/bin/bash
qemu-system-i386 -snapshot -cdrom PwnyOS.iso -hda flag_drive.txt -monitor none -serial stdio -vga none -parallel none
