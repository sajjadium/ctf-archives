CHAL_NAME ?= warning
CHAL_PORT ?= 12345
CHAL_HOST ?= 172.17.0.1

FLAG ?= flag{warning_warning_will_robinson}


.PHONY: static
static:
	docker build static -t $(CHAL_NAME):static
	docker run -v $(PWD)/data:/binaries $(CHAL_NAME):static

.PHONY:build
build:
	docker build static -t $(CHAL_NAME):static
	docker build challenge -t $(CHAL_NAME):challenge

.PHONY:challenge
challenge:
	socat -v tcp-listen:$(CHAL_PORT),reuseaddr exec:"docker run --rm -i --cap-add=SYS_PTRACE -e FLAG=${FLAG} ${CHAL_NAME}\:challenge" > log 2>&1 &
	echo "To connect: nc localhost $(CHAL_PORT)"

.PHONY:shell
shell:
	docker run --rm -it --cap-add=SYS_PTRACE --entrypoint=/usr/bin/bash -e FLAG=${FLAG} ${CHAL_NAME}\:challenge
