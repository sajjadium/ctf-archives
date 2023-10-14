#!/bin/sh

# Generate random flag name
random_flag_name="flag_$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 10 | head -n 1).txt"

# Specify flag content
flag_content="ISITDTU{test_flag}"

# Move flag file to root directory
echo "$flag_content" > /"$random_flag_name"

# Set permissions for flag file
chmod 744 /"$random_flag_name"

# Get the user
user=$(ls /home)

# Set permissions for /app directory
chmod 740 /app/*

# Change directory and run Flask
cd /app && flask run -h 0.0.0.0 -p 8080