docker pull ghcr.io/foundry-rs/foundry:latest
docker build --target=relayer -t safe-bridge-relayer .
docker compose up --build
