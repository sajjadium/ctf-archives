CPPFLAGS=-Wall
LDFLAGS=-Wl,-z,relro,-z,now
CXXFLAGS=
CXX=g++
CC=g++

DEPLOY = Makefile todo todo.cc string2.cc string2.h
DEPLOY_DIR = todo_deploy

.PHONY: all deploy
all: todo

clean: 
	rm -rf $(DEPLOY_DIR) *.o todo

deploy: todo.tar.gz

todo.tar.gz: $(DEPLOY)
	mkdir -p $(DEPLOY_DIR)
	cp $^ $(DEPLOY_DIR)
	tar -acvf $@ $(DEPLOY_DIR)


todo: todo.o string2.o

string2.cc: string2.h

todo.cc: string2.h
