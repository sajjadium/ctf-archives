OPA totally transformed my policy management, ya know? It's like a separate thingy that lets me define and enforce policies in a super flexible way. I integrated it into my application stack without any kvetching, and I could update policies on the fly, no need for system restarts, ya get me? Testing and simulation became a piece of cake, I tell ya. And the OPA community? They're like family, always there to help out. OPA, it's a real game-changer, in terms of policy control and access management, you know what I'm saying?
The only problem is, I can't figure out how information is leaking from it.


# Opa Opa Opa Opa Hei

## Docker

Build: `docker compose build`

Start: `docker compose up -d`

Stop: `docker compose down`

Logs: `docker compose logs`

Run and get logs: `docker compose build && docker compose up -d && docker compose logs -f`

## Manually

### Build the opa client

```
go mod init example.com/opa
go get github.com/open-policy-agent/opa/sdk
go get github.com/sirupsen/logrus
go get github.com/sirupsen/logrus
go get github.com/pkg/errors
go get github.com/gorilla/mux
go get github.com/gorilla/handlers
go build opa.go
```

### Run the Opa Docker
```
docker run -p 8181:8181 openpolicyagent/opa run --server
```
