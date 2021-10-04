client: base64.o service.hpp client.cpp host.cpp
	g++ -std=c++17 -o ../client base64.o client.cpp
	g++ -std=c++17 -o ../host base64.o host.cpp

base64.o: base64.h base64.c
	gcc -c -o base64.o base64.c

clean:
	rm -f *.o host client
