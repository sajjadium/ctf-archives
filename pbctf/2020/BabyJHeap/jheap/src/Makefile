MODULE = jheap
MOD_MAIN = jheap/com.thekidofarcrania.heap.JHeap
DEPLOY = ../deploy
JSA = $(abspath $(DEPLOY)/lib/server/classes.jsa)

JCFLAGS=-h .
JFLAGS=-Xmx200m -XX:+UseG1GC -Xms200m #-XX:SharedArchiveFile=$(JSA) #-verbose:class
CPPFLAGS=-I java/include -I include -I include/linux
CFLAGS=-fPIC
LDFLAGS=


export DEBUG

ifdef DEBUG
	CPPFLAGS += -DDEBUG
#	CFLAGS += -g
#	LDFLAGS += -g
endif

.PHONY: all clean run debug java

all: .deploy $(JSA)

clean: 
	make -C java clean
	rm -rf $(DEPLOY) *.o libheap.so .deploy

java:
	@make -C java

.deploy $(DEPLOY): libheap.so java/lib/main.jar
	rm -rf $(DEPLOY); \
		jlink --module-path java/lib --add-modules $(MODULE) --launcher $(MODULE)=$(MOD_MAIN) \
			--output $(DEPLOY) --strip-debug --compress 2; \
		cp $< $(DEPLOY)/lib; \
		/bin/echo -e " \
			sed -i '2 { \n\
				i JLINK_VM_OPTIONS=\"$(JFLAGS)\" \n\
				d }' $(DEPLOY)/bin/jheap;" | sh; \
		touch .deploy

java/include/com_thekidofarcrania_heap_JHeap.h java/lib/main.jar: java

.INTERMEDIATE: .cls.lst
.cls.lst: .deploy
	$(DEPLOY)/bin/java $(JFLAGS) -Xshare:off -XX:DumpLoadedClassList=$@ \
		-m $(MOD_MAIN) < /dev/null > /dev/null || true

$(JSA): .cls.lst
	$(DEPLOY)/bin/java -Xshare:dump -XX:SharedClassListFile=$< $(JFLAGS) \
		-m $(MOD_MAIN) < /dev/null


heap.o: heap.c java/include/com_thekidofarcrania_heap_JHeap.h Makefile

libheap.so: heap.o 
	$(CC) -shared -o $@ $(LDFLAGS) $^

run: all
	java $(JFLAGS) JHeap

debug: all
	gdb java -ex "run $(JFLAGS) JHeap"
