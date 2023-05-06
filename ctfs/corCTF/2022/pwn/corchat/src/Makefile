CC = g++
CFLAGS  = -pthread
TARGET = corchat_server

all: $(TARGET)

$(TARGET): main.cpp server.cpp crusader.cpp parser.cpp
	$(CC) $(CFLAGS) -o $(TARGET) main.cpp server.cpp crusader.cpp parser.cpp

clean:
	$(RM) $(TARGET)
