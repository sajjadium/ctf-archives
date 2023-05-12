#!/bin/bash

socat tcp-listen:1337,reuseaddr,fork exec:$1