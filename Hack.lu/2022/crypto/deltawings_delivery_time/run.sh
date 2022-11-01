gcc -O0 hmac.c algorithms/Blake2b/*.c algorithms/sha256/*.c -o hmac
chmod +x hmac
socat tcp-l:1337,reuseaddr,fork EXEC:"./hmac",pty,rawer,echo=0
