# ddospot
- [https://github.com/aelth/ddospot](https://github.com/aelth/ddospot)

## setup
### setup manual
```bash
git clone https://github.com/aelth/ddospot
cd ddospot/ddospot
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### setup docker compose
```bash
git clone https://github.com/aelth/ddospot
cd ddospot

sed -i 's|FROM alpine:edge|FROM python:3.10-alpine|' ddospot/Dockerfile

sed -i 's|RUN pip3 install --upgrade pip|RUN pip3 install --upgrade pip --break-system-packages|' ddospot/Dockerfile
sed -i 's|pip3 install -r /ddospot/requirements.txt|pip3 install -r /ddospot/requirements.txt --break-system-packages|' ddospot/Dockerfile
sed -i 's|chown ddospot.ddospot -R /ddospot/\*|chown -R ddospot:ddospot /ddospot|' ddospot/Dockerfile

sed -i "s|subnet: 172.18.0.1/24|subnet: 172.18.0.0/24|" docker-compose.yml

docker compose build
docker compose up -d
```

- 0.0.0.0:19->19/udp
- 0.0.0.0:123->123/udp
- 0.0.0.0:161->161/udp
- 0.0.0.0:54->53/udp
- 0.0.0.0:1901->1900/udp

## testing
```bash
docker logs -f ddospot-ddospot-1
sudo nmap -sU 127.0.0.1
cat ddospot/logs/*
```

### Port 54/udp (DNS)
```bash
dig @127.0.0.1 -p 54 example.com
```

### Port 123/udp (NTP)
```bash
sudo apt install ntpdate
ntpdate -q 127.0.0.1
```

### Port 161/udp (SNMP)
```bash
snmpwalk -v2c -c public 127.0.0.1
```

### Port 19/udp (Chargen)
```bash
echo "test" | nc -u -w1 127.0.0.1 19
```

### Port 1901/udp (SSDP/UPnP)
```bash
echo -ne "M-SEARCH * HTTP/1.1\r\nHOST:239.255.255.250:1900\r\nMAN:\"ssdp:discover\"\r\nMX:1\r\nST:ssdp:all\r\n\r\n" | nc -u -w2 127.0.0.1 1901
```
