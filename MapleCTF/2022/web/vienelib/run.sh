#!/bin/bash

cd /usr/src/vienelibrary/vieneclient
node app.js &

cd ../vieneserver
rails s -b 0.0.0.0