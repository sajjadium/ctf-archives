Here's an improved version of our pasting service. Some weird stuff was happening in the previous version, so we added an integrity check for the pastes. Also, due to misuse, we began limiting the size of the pasted snippets (please don't paste Kali Linux ISOs, thanks).

To compile, Use the following commands:

gcc -c -std=c99 zlib/*.c  
g++ -c -std=c++14 snappaste.cc   
g++ -o snappaste *.o -pthread  

