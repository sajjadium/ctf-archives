# deployment vars
NAME := macchiato
REGISTRY :=
SUFFIX :=

# configurable vars:
# hports="8888 8889" make -e ...
CPORTS := 7010
HPORTS := $(CPORTS)
SERVICES := CHAL

# generate service -> port mappings: service_port := port
# this is necessary for docker compose string substitution via env variables
# also useful for containers requiring build args for setting ports on multiple services
$(foreach var, \
    $(shell \
				python -c "for s, p in zip('$(SERVICES)'.split(), '$(CPORTS)'.split()): print(f'{s}_CPORT:={p}')" \
    ), $(eval $(var)) \
)

# docker
DOCKER_CONTEXT := default
DOCKER_GLOBAL := --context $(DOCKER_CONTEXT)
DOCKER_RUNTIME := --memory=128m --cpus=0.2 --read-only --restart=always

# build vars
clean:
	docker container rm -f $(NAME)
	rm -f $(NAME).zip

build: Dockerfile
	docker $(DOCKER_GLOBAL) build -t $(NAME) \
		--build-arg name=$(NAME) \
		--build-arg port=$(CHAL_CPORT) \
		.

run:
	$(eval ports := $(shell python -c "for h, c in zip('$(HPORTS)'.split(), '$(CPORTS)'.split()): print(f' -p {h}:{c}')"))
	docker $(DOCKER_GLOBAL) run $(DOCKER_RUNTIME) -d --name $(NAME)$(SUFFIX) $(ports) $(REGISTRY)$(NAME)

dist:
	zip -r $(NAME).zip src Makefile Dockerfile solver-template.py
