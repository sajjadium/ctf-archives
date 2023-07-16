BUILDER=simpleos

.PHONY: build clean

build: src steps mtools.conf build.zig
	docker build . -f build.dockerfile -t $(BUILDER)
	docker run -v "$(CURDIR):/chal" -w /chal -it --rm $(BUILDER) zig build disk

clean:
	-rm -rf disk.img zig-cache zig-out