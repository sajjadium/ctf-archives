LOC=$(cat /dev/urandom | head | md5sum | cut -d " " -f 1)
mv ./flag.txt /$LOC