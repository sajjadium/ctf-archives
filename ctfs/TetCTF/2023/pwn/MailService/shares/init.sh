#!/bin/bash

systemctl start mailserver
service xinetd restart
sleep infinity