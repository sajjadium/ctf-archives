cat > flag.txt
while true ; do P=$(base64 /dev/urandom | tr  '[0-9BADKEY]' '-' |head -c 8) ; [ "$(echo -n $P | md5sum |cut -c-32)" == "$(echo -n $P | md5sum |cut -c-32 | grep -P '^(ba|57|5d|79){8}')" ] && break;done
rar a -hp$P flag.rar flag.txt
rm flag.txt
