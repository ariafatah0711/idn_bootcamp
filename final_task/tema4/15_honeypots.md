# honeypots
- [https://github.com/qeeqbox/honeypots](https://github.com/qeeqbox/honeypots)

## setup
```bash
# git clone https://github.com/qeeqbox/honeypots

pip3 install honeypots
python3 -m honeypots --setup all
```

<!-- ### Usage Example - Auto configuration with default ports
```bash
sudo -E python3 -m honeypots --setup ssh --options capture_commands
python3 -m honeypots --setup ssh --auto
``` -->

## testing
```bash
nmap 127.0.0.1
# nmap -sV -A 127.0.0.1

mysql -h 127.0.0.1 -P 3306 -u root -p
vncviewer 127.0.0.1:5900

curl -x http://127.0.0.1:8080 http://example.com
curl -x http://127.0.0.1:8080 http://ariaf.my.id
```
