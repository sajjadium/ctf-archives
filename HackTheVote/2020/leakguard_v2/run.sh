#!/bin/sh
exec timeout -s 9 120 env -i LD_PRELOAD=/home/candles/leakguard.so /home/candles/candles
