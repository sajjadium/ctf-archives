CXX     ?= g++
RM      ?= rm -f
FLAGS   := -pthread -mavx2 -std=c++17 -DNDEBUG -Os -s -Wl,--sort-common,-O1,--as-needed,--build-id=none,-z,relro,-z,now -D_FORTIFY_SOURCE=2 -fstack-protector-all -fstack-clash-protection -fno-plt -Wno-ignored-attributes
TARGET  := stegernseer

%: %.cpp Makefile
	$(CXX) $(RELEASE) $(FLAGS) $< -o $@

clean:
	$(RM) $(TARGET)

.PHONY: clean

.DEFAULT_GOAL := $(TARGET)
