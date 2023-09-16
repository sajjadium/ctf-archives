#!/bin/bash
socat TCP-LISTEN:9999,reuseaddr,fork EXEC:"./double_zer0_dilemma"