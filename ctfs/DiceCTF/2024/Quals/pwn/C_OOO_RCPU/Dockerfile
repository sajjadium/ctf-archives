FROM alpine:latest AS build-cpu
RUN apk add verilator verilator-dev make g++ musl-dev python3
COPY rtl ./
RUN verilator -sv --trace -cc *.sv  --exe --timing +1800-2017ext+sv -Wno-WIDTHTRUNC -Wno-WIDTHEXPAND --top-module cpu_entry --build --binary -I. -Ilists
RUN cp obj_dir/Vcpu_entry /cpu_entry

FROM pwn.red/jail
COPY --from=build-cpu / /srv
COPY flag.txt /srv/app/
COPY --from=build-cpu /cpu_entry /srv/app/
COPY run.sh /srv/app/run
COPY system_rom.rom /srv/app/

ENV JAIL_MEM=1G
env JAIL_PIDS=50
env JAIL_TMP_SIZE=8192
