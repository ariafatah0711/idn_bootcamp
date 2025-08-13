# C. glastopf (honeypot web)
- [github-glastpof](https://github.com/mushorg/glastopf)
- [dockerhub-honeynet/glastopf](https://hub.docker.com/r/honeynet/glastopf)
- [dockerhub-stingar/glastopf](https://hub.docker.com/r/stingar/glastopf)

## setup manual
```bash
git clone https://github.com/mushorg/glastopf
docker build -t glastpof .
# ubah base image menjadi FROM ubuntu:20.04ss
docker run honeynet/glastopf
```

## setup docker
```bash
docker run honeynet/glastopf
```
