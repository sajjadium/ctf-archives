SOLANA_URL=https://github.com/solana-labs/solana/releases/download/v1.16.20/solana-release-x86_64-unknown-linux-gnu.tar.bz2
SOLANA_TAR=solana-release-x86_64-unknown-linux-gnu.tar.bz2
SOLANA_DIR=solana-release

export PATH := $(SOLANA_DIR):/bin:$(PATH)

.PHONY: all build

$(SOLANA_DIR):
	wget $(SOLANA_URL)
	tar -xvf $(SOLANA_TAR)

build: $(SOLANA_DIR)
	cargo build-bpf