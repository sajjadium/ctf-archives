FROM golang:1.17

WORKDIR /usr/src/app

COPY go.mod .
RUN go mod download && go mod verify

COPY main.go .
COPY go.sum .
RUN go build -v -o /usr/local/bin/app ./...

ENV KEY this_is_fake_key
ENV FLAG LINECTF{this_is_fake_flag}
ENV AMDIN_ID admin
ENV AMDIN_PW this_is_fake_pw

CMD ["app"]