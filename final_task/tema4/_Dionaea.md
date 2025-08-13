# Dionaea → Malware capture untuk protokol SMB, HTTP, FTP, dll.
- [https://github.com/DinoTools/dionaea?tab=readme-ov-file](https://github.com/DinoTools/dionaea?tab=readme-ov-file)
- [https://dionaea.readthedocs.io/en/latest/](https://dionaea.readthedocs.io/en/latest/)
- [https://hub.docker.com/r/dinotools/dionaea](https://hub.docker.com/r/dinotools/dionaea)

## setup
```bash
git clone https://github.com/DinoTools/dionaea.git
cd dionaea
```

### docker
```bash
docker run --rm -it -p 21:21 -p 42:42 -p 69:69/udp -p 80:80 -p 135:135 -p 443:443 \
-p 445:445 -p 1433:1433 -p 1723:1723 -p 1883:1883 -p 1900:1900/udp -p 3306:3306 \
-p 5060:5060 -p 5060:5060/udp -p 5061:5061 -p 11211:11211 dinotools/dionaea
```
