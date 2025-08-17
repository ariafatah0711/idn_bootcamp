# Community Honey Network (CHN)
- [https://github.com/CommunityHoneyNetwork/CHN-Server](https://github.com/CommunityHoneyNetwork/CHN-Server)
- [https://communityhoneynetwork.readthedocs.io/en/stable/](https://communityhoneynetwork.readthedocs.io/en/stable/)

## setup docker
```bash
git clone https://github.com/CommunityHoneyNetwork/CHN-Server
docker compose up -d
```
atau
```bash
git clone https://github.com/CommunityHoneyNetwork/CHN-Server
docker build -t chn .
docker run -d --name chnserver \
  -p 80:80 -p 443:443 \
  --link mongodb:mongodb \
  --link redis:redis \
  --link hpfeeds3:hpfeeds3 \
  -v ./config/collector:/etc/collector:z \
  -v ./storage/chnserver/sqlite:/opt/sqlite:z \
  -v ./certs:/tls:z \
  chn
```
