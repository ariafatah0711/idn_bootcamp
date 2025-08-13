# Modern Honey Network
- [https://github.com/pwnlandia/mhn](https://github.com/pwnlandia/mhn)

## setup with vagrant vm
```bash
git clone https://github.com/pwnlandia/mhn.git
vagrant up
```

## setup manual
```bash
git clone https://github.com/pwnlandia/mhn.git
cd mhn/
sudo ./install.sh
```
configuration
```bash
===========================================================
MHN Configuration
===========================================================
Do you wish to run in Debug mode?: y/n n
Superuser email: YOUR_EMAIL@YOURSITE.COM
Superuser password:
Server base url ["http://1.2.3.4"]:
Honeymap url ["http://1.2.3.4:3000"]:
Mail server address ["localhost"]:
Mail server port [25]:
Use TLS for email?: y/n n
Use SSL for email?: y/n n
Mail server username [""]:
Mail server password [""]:
Mail default sender [""]:
Path for log file ["mhn.log"]:
```

## setup docker
```bash
docker build -t mhn .
docker run -d -p 10000:10000 -p 80:80 -p 3000:3000 -p 8089:8089 \
--restart unless-stopped \
--name mhn \
-e SUPERUSER_EMAIL=root@localhost \
-e SUPERUSER_PASSWORD=password \
-e SERVER_BASE_URL="http://mhn" \
-e HONEYMAP_URL="http://mhn:3000" \
mhn
```
Environment variables
```bash
SUPERUSER_EMAIL
SUPERUSER_PASSWORD
SERVER_BASE_URL
HONEYMAP_URL
DEBUG_MODE
SMTP_HOST
SMTP_PORT
SMTP_TLS
SMTP_SSL
SMTP_USERNAME
SMTP_PASSWORD
SMTP_SENDER
MHN_LOG
```
