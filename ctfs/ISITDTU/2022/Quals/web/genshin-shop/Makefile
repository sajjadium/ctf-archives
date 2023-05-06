ifdef compose
DC := $(compose)
else
DC := docker compose
endif

ifndef branch
BRANCH = local
else
BRANCH = $(branch)
endif

ifndef tag
TAG = latest
else
TAG = $(tag)
endif

ifeq ($(BRANCH), local)
COMPOSE_FILE = "docker-compose.yml"
else
COMPOSE_FILE = "docker-compose.$(branch).yml"
REGISTRY = $(registry)/
endif

up:
	$(DC) -f $(COMPOSE_FILE) up -d

down:
	$(DC) -f $(COMPOSE_FILE) down

build:
	docker build --rm -f ".dockerfile/Dockerfile.bootstrap" -t $(REGISTRY)genshin-shop-bootstrap:$(TAG) "."

	docker build --rm -f ".dockerfile/Dockerfile.pnpm" -t $(REGISTRY)genshin-shop-pnpm:$(TAG) "."
	docker run --rm --name "genshin-shop-pnpm-builder" -v $(shell pwd)/web/node_modules:/mnt/pnpm/node_modules $(REGISTRY)genshin-shop-pnpm:$(TAG)
	
	docker build --rm -f ".dockerfile/Dockerfile.gateway" -t $(REGISTRY)genshin-shop-gateway:$(TAG) "."
	docker run --rm --name "genshin-shop-gateway-builder" -v $(shell pwd)/volume/gateway:/mnt/config $(REGISTRY)genshin-shop-gateway:$(TAG)
	
	docker build --rm -f ".dockerfile/Dockerfile.cdn" 		-t $(REGISTRY)genshin-shop-cdn:$(TAG) "."
	docker build --rm -f ".dockerfile/Dockerfile.api" 		-t $(REGISTRY)genshin-shop-api:$(TAG) "."

image:
	docker build -f ".dockerfile/Dockerfile.$(repo)" -t $(REGISTRY)genshin-shop-${repo}:$(TAG) "."