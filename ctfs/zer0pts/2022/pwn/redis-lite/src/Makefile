CFLAGS=-Wl,-z,relro,-z,now -pie -fstack-protector -O3
LIBS=-lpthread
CC=gcc
CMDDIR=./commands
SRCS=$(wildcard $(CMDDIR)/*.c)
OBJS=$(SRCS:.c=.o)

redis-lite-server: $(OBJS) resp.o redis.o main.o
	$(CC) $(CFLAGS) $(OBJS) resp.o redis.o main.o -o redis-lite-server $(LIBS)

resp.o: resp.c resp.h
	$(CC) $(CFLAGS) -c resp.c -o resp.o

redis.o: redis.c redis.h
	$(CC) $(CFLAGS) -c redis.c -o redis.o

main.o: main.c
	$(CC) $(CFLAGS) -c main.c -o main.o

$(CMDDIR)/%.o: $(CMDDIR)/%.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm *.o commands/*.o
