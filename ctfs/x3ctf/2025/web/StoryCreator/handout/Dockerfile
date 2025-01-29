FROM golang:1.22 AS bebuilder 
WORKDIR /source
COPY backend/go.mod backend/go.sum /source/
RUN go mod download
COPY backend/ .
RUN uname -a && go build -o server ./cmd/server

FROM node:22 AS febuilder 
WORKDIR /app
COPY frontend/package.json frontend/yarn.lock frontend/.yarnrc.yml /app/
COPY frontend/.yarn /app/.yarn
RUN yarn install --immutable
COPY frontend/ .
RUN yarn build

# FROM gcr.io/distroless/cc AS final
FROM debian:latest AS final
RUN apt-get -y update && apt-get -y install chromium && rm -rf /var/lib/apt/lists/*
COPY --from=bebuilder /source/server /server 
COPY --from=febuilder /app/dist /frontend
ENV FRONTEND_DIST /frontend/
# USER nonroot
CMD ["/server"]
