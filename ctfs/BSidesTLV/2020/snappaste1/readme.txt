We felt like there were not enough pasting services, so we created Snappaste! For better privacy, each pasted text can only be accessed once. We care about performance, and therefore we developed Snappaste in C++. We hope that we didn't introduce any security bugs :)

To compile, Use the following commands:

gcc -c -std=c99 zlib/*.c  
g++ -c -std=c++14 snappaste.cc   
g++ -o snappaste *.o -pthread  

