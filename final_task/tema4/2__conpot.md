# B. Conpot (ICS honeypot)
- [github-mushorg/conpot](https://github.com/mushorg/conpot)
- [dockerhub-honeynet/conpot](https://hub.docker.com/r/honeynet/conpot)

## setup
```bash
git clone https://github.com/mushorg/conpot.git
docker build -t conpot .
docker run -it --name conpot -p 80:8800 -p 102:10201 -p 502:5020  \
-p 161:16100/udp -p 47808:47808/udp -p 623:6230/udp -p 21:2121 \
-p 69:6969/udp -p 44818:44818 --network=bridge conpot

# Navigate to http://MY_IP_ADDRESS to confirm the setup.

# check with nmap
nmap <ip_server>
```

or with dockerhub
```bash
docker run -it --name conpot_hub -p 80:8800 -p 102:10201 -p 502:5020  \
-p 161:16100/udp -p 47808:47808/udp -p 623:6230/udp -p 21:2121 \
-p 69:6969/udp -p 44818:44818 --network=bridge honeynet/conpot:latest /bin/sh
```

Setelah masuk ke container:
```bash
conpot -f --template default
```
jika tidak bisa coba pake path dibawah ini
```bash
/home/conpot/.local/lib/python3.6/site-packages/conpot-0.6.0-py3.6.egg/bin/conpot \
-f -t /home/conpot/.local/lib/python3.6/site-packages/conpot-0.6.0-py3.6.egg/conpot/templates/default/
```

Navigate to http://MY_IP_ADDRESS to confirm the setup.
```nmap <ip_server>```

## testing
### Tes Modbus/TCP (port 502)
- [modbusdriver.com/modpoll.html](https://www.modbusdriver.com/modpoll.html)

#### modbus
```bash
wget https://www.modbusdriver.com/downloads/modpoll.tgz
tar xzf modpoll.tgz
cd modpoll/x86_64-linux-gnu
export PATH=$PWD:$PATH
```
jalankan
```bash
modpoll -m tcp -t 3 -r 1 -c 5 127.0.0.1
# Keterangan:
# -m tcp → pakai Modbus TCP
# -t 3 → tipe register: Holding Register
# -r 1 → mulai dari register 1
# -c 5 → baca 5 register
# 127.0.0.1 → IP honeypot (ubah ke IP Conpot kamu)
```

### Tes Siemens S7Comm (port 102)
#### nmap script s7-info
```bash
# script: /usr/share/nmap/scripts/s7-info.nse
nmap -p 102 --script s7-info 127.0.0.1 -d
```

### Tes SNMP (port 161/UDP)
#### snmpwalk
```bash
sudo apt install snmp
snmpwalk -v2c -c public 127.0.0.1
```

### Tes HTTP/Web Interface (port 80)
```bash
curl -v http://127.0.0.1
```

### Tes TFTP (port 69/UDP)
```bash
sudo apt install tftp
tftp 127.0.0.1

# setelah masuk gunakan perintah ini
? # untuk opsi help
get <nama_file> # untuk mendownload flle (biasanya tftp perlu tau nama file / path dari filenya)
put <nama_file> # untuk mengupload file (biasanya upload file)
```
