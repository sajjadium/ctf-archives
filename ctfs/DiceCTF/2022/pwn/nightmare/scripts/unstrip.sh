mkdir -p ./lib && cd ./lib

cp /usr/lib/debug/.build-id/b8/037b6260865346802321dd2256b8ad1d857e63.debug ./libc.so.6
cp /usr/lib/debug/.build-id/14/acb10bbdaefc6a64890c96417426ca820c0faa.debug ./ld-linux-x86-64.so.2

eu-unstrip /usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2 ./ld-linux-x86-64.so.2 
eu-unstrip /usr/lib/x86_64-linux-gnu/libc.so.6 ./libc.so.6
