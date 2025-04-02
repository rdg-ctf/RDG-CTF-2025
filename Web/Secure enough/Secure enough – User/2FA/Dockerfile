FROM golang:latest

WORKDIR /2fa

COPY . /2fa

RUN go mod tidy

CMD ["go", "run", "main.go"]
