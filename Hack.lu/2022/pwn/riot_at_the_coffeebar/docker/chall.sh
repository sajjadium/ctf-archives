#!/bin/bash

TMPDIR="$(mktemp --directory)"
SERIAL0="${TMPDIR}/serial0"
SERIAL1="${TMPDIR}/serial1"

cleanup() {
    kill "${EMULATOR_PID}"
    kill "${COFFE_PID}"
    rm -rf "${TMPDIR}"
}

trap cleanup EXIT HUP INT TERM

# Hacky workaround
# Renode starts a telnet server if the gui is disabled
# use --console to disable the telnet server
# then sleep because closing stdin will exit the emulator
sleep 1337 | mono /opt/renode/bin/Renode.exe --disable-xwt --console chall.resc -e "emulation CreateUartPtyTerminal \"term\" \"${SERIAL0}\" true" -e "emulation CreateUartPtyTerminal \"coffe\" \"${SERIAL1}\" true" -e "include @/home/challuser/chall.resc" 2> /dev/null > /dev/null &
EMULATOR_PID=$!

echo "Waiting for serial port"
# Start the terminal client after SERIAL0 is available. SERIAL0 can be a symlink.
while [ ! -L "${SERIAL0}" ]
do
    sleep 0.1
done

# start coffee machine emulator
./coffe.py "${SERIAL1}" 2> /dev/null > /dev/null &
COFFE_PID=$!

echo "Serial connected"
# forward serial connection
socat - "${SERIAL0}"

