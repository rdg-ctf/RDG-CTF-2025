FROM golang:latest

WORKDIR /2fa

COPY . /2fa

RUN go mod tidy

EXPOSE 8080

CMD ["go", "run", "main.go"]
