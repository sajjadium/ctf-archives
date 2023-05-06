JCFLAGS=-h include
JFLAGS=-Xmx200m #-verbose:class

CLASSES = build/com/thekidofarcrania/heap/JHeap.class build/module-info.class
ENTRYPOINT = com.thekidofarcrania.heap.JHeap

ifdef DEBUG
endif

.PHONY: all run test clean debug

all: lib/main.jar

test: HeapTest.class all
	java $(JFLAGS) HeapTest $(CYCLES)

clean: 
	rm -rf lib/ build/ dist/ .dir.* include

$(CLASSES): Makefile

.dir.%:
	mkdir -p $*
	@touch $@

build/%.class: %.java 
	javac -d build/ $(JCFLAGS) $<

lib/main.jar: $(CLASSES) .dir.lib
	jar cef $(ENTRYPOINT) $@ -C build .
	
