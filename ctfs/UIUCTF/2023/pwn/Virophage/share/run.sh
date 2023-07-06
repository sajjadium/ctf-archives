#!/bin/sh

exec 2>/dev/null
timeout 300 env -i HOME="$HOME" PATH="$PATH" PWD="$PWD" SHLVL="1" /home/virus/virus
