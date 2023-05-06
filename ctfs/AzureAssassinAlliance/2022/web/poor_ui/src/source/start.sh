#!/bin/bash

pm2 start server.js
pm2 start adminbot.js
pm2 start flagbot.js
tail -f /dev/null