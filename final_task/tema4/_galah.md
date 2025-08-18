# galah
- [https://github.com/0x4D31/galah](https://github.com/0x4D31/galah)

Galah adalah sebuah honeypot web yang memanfaatkan kecerdasan buatan untuk membalas permintaan HTTP.
- Dibuat oleh Adel "0x4D31" Karimi sebagai eksperimen pemanfaatan LLM dalam keamanan siber
- Galah mampu merespons interaksi secara dinamis dan konteksual, sehingga tampak lebih realistis daripada honeypot statis tradisional.

## setup
> butuh ram 4-8gb kkenya soalnya gw coba gak bisa di vm

### setup golang
```bash
git clone https://github.com/0x4D31/galah.git
cd galah
go mod download
mkdir bin
go build -o bin/galah ./cmd/galah
./bin/galah --help
```

### setup with docker
```bash
git clone https://github.com/0x4D31/galah.git
cd galah
mkdir logs
# export LLM_PROVIDER="openai"
# export LLM_MODEL="gpt-3.5-turbo"

cat << EOF > Dockerfile
FROM golang:1.22 AS builder

WORKDIR /app
COPY . .

# download deps
RUN go mod download

# build binary galah
RUN go build -o galah ./cmd/galah

# -------- runtime stage --------
FROM debian:bookworm-slim

WORKDIR /galah

# copy binary dari builder
COPY --from=builder /app/galah .

# bikin folder logs
RUN mkdir -p /galah/logs

ENTRYPOINT ["./galah"]
EOF

cat << EOF > Dockerfile
FROM golang:1.22 AS builder

WORKDIR /app

# copy go.mod & go.sum dulu
COPY go.mod go.sum ./

# download deps
RUN go mod download

# copy semua source
COPY . .

# build binary galah
RUN go build -o galah ./cmd/galah

# -------- runtime --------
FROM debian:bookworm-slim

WORKDIR /galah
COPY --from=builder /app/galah .
RUN mkdir -p /galah/logs

ENTRYPOINT ["./galah"]
EOF

export LLM_API_KEY="YOUR_OPENAI_API_KEY"
docker build -t galah-image .
# docker run -d --name galah-container -p 8080:8080 -v $(pwd)/logs:/galah/logs -e LLM_API_KEY galah-image -o logs/galah.json -p openai -m gpt-3.5-turbo-1106

docker run -d \
  --name galah-container \
  -p 8080:8080 \
  -v $(pwd)/logs:/galah/logs \
  -e LLM_API_KEY="sk-xxx" \
  galah-image \
  -o logs/galah.json -p openai -m gpt-3.5-turbo
```
