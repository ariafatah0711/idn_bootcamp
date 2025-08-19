# ciscoasa
- [https://github.com/Cymmetria/ciscoasa_honeypot](https://github.com/Cymmetria/ciscoasa_honeypot)
- [https://github.com/1337g/CVE-2018-0101-DOS-POC/blob/master/CVE-2018-0101POC.py](https://github.com/1337g/CVE-2018-0101-DOS-POC/blob/master/CVE-2018-0101POC.py)

- port 8443

## setup
```bash
git clone https://github.com/Cymmetria/ciscoasa_honeypot
cd ciscoasa_honeypot

pip install ike
python3 asa_server.py

# docker build -t ciscoasa .
```

> go to web http://<ip>:8443/

## testing
```bash
wget https://raw.githubusercontent.com/1337g/CVE-2018-0101-DOS-POC/refs/heads/master/CVE-2018-0101POC.py
python3 CVE-2018-0101POC.py http://192.168.1.10:8443/
```
