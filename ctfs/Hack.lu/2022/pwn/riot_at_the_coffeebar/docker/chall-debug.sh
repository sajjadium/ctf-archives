#!/bin/bash

SERIAL0=/tmp/serial0

cleanup() {
    kill "${EMULATOR_PID}"
    kill "${COFFE_PID}"
    rm "${SERIAL0}"
}

trap cleanup EXIT

# Hacky workaround
# Renode starts a telnet server if the gui is disabled
# use --console to disable the telnet server
# then sleep because closing stdin will exit the emulator
sleep 1337 | mono /opt/renode/bin/Renode.exe --disable-xwt --console chall-debug.resc &
EMULATOR_PID=$!

echo "Waiting for serial port"
# Start the terminal client after SERIAL0 is available. SERIAL0 can be a symlink.
while [ ! -L "${SERIAL0}" ]
do
    sleep 0.1
done

# start coffee machine emulator
./coffe.py /tmp/serial1 > /dev/null &
COFFE_PID=$!

echo "Serial connected"
# forward serial connection
socat TCP-Listen:$PORT "${SERIAL0}"

