FROM mluis/qemu-esp32:2023-09-16

COPY run_prod.sh /root/
COPY run_dbg.sh /root/
RUN rm -rf ./program
COPY every-italian-politician.elf /root/every-italian-politician.elf
COPY flash.bin /root/flash.bin
