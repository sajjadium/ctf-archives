#!/bin/bash

service nginx start
sudo -u user socat TCP-L:3000,reuseaddr,fork EXEC:"/run_ps2pdf.sh"
