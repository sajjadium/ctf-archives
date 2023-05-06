# RIOT at the Coffeebar

## Some help for running the setup
1. Use `./build.sh` to build the challenge docker container
2. Execute it with `./run.sh`

## Debugging
Using `./run-debug.sh` starts the container in debug mode.
You can use port 1337 for the usual serial connection.
The emulator listens on port 3333 for a GDB connection.
Logging from the emulator is available on stdout from the docker container.

To connect to the gdbserver use multiarch or arm-none-eabi GDB:
```
file docker/gnrc_networking.elf
target remote tcp:localhost:3333
```

## Firmware modifications
Run `./build.sh --firmware` to download the git repository and apply the patches.
Running `./build.sh --firmware` again will create a new image including any modifications.
To get back to the initial state use `./build.sh --clean-firmware`

Many files have `#define ENABLE_DEBUG 0` in the header.
Setting this to `1` will enable debugging output for a single file.
