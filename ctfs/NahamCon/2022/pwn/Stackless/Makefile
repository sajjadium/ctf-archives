SOURCES=stackless.c
LDFLAGS:=-lseccomp
CFLAGS:=-Wall -z relro -z now
TARGET:=stackless
CC:=gcc

.PHONY: all clean $(TARGET)

all: $(TARGET)

clean:
	rm -f $(TARGET)

$(TARGET): $(SOURCES)
	$(CC) -o $(TARGET) $(CFLAGS) $(SOURCES) $(LDFLAGS)
