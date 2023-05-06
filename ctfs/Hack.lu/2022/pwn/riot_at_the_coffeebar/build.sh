#!/bin/bash
DIR="$(dirname "$(readlink -f "$0")")"
GIT_DIR="$DIR/RIOT"

EXAMPLE_TARGET=gnrc_networking

set -e

# need root if user is not in docker group
if ! id -nGz | grep -qzxF "docker" && [[ "$EUID" != "0" ]]
then
    export DOCKER="sudo docker"
else
    export DOCKER=docker
fi

if [[ "$1" = "--firmware" || "$1" = "--clean-firmware" ]]; then
    # prepare git repo
    if [[ ! -e "$GIT_DIR" ]]; then
        git clone https://github.com/RIOT-OS/RIOT "$GIT_DIR"
        cd "$GIT_DIR"
        git checkout 2022.07
        # apply patch
        git apply "$DIR/chall.patch"
    fi

    cd "$GIT_DIR"
    if [[ "$1" = "--clean-firmware" ]]; then
        git reset --hard
        git clean -df
        git checkout 2022.07

        # apply patch
        git apply "$DIR/chall.patch"
    fi

    # prepare build vars
    export BUILD_IN_DOCKER=1
    export DOCKER_IMAGE=riot/riotbuild:2022.07
    # dwarf info for ghidra
    export DOCKER_ENVIRONMENT_CMDLINE="-e 'CFLAGS=-gdwarf-4 -gstrict-dwarf'"

    # compile targets
    make -C "examples/$EXAMPLE_TARGET/" -j$(nproc) BOARD=cc2538dk clean all

    cp examples/"$EXAMPLE_TARGET"/bin/cc2538dk/"$EXAMPLE_TARGET".elf "$DIR"/docker
fi

$DOCKER build -t riot-challenge "$DIR/docker"
