# honeytrap
- [https://github.com/armedpot/honeytrap/](https://github.com/armedpot/honeytrap/)
- [https://github.com/4sp1r3/honeytrap](https://github.com/4sp1r3/honeytrap)

## setup
### setup docker (masih error setup di docker run error spawned gitu)
```bash
git clone https://github.com/4sp1r3/honeytrap
cd honeytrap

sed -i 's|FROM ubuntu:14.04.3|FROM debian:bullseye|' Dockerfile
sed -i -E \
  -e 's/python-lxml/python3-lxml/g' \
  -e 's/python-mysqldb/python3-mysqldb/g' \
  -e 's/python-requests/python3-requests/g' \
  -e 's/\bpython\b/python3/g' \
  Dockerfile

# Tambah python3-setuptools & python3-pip
sed -i -E \
  -e 's/python3-requests/& python3-setuptools python3-pip/' \
  -e 's|python3 setup.py install|pip3 install .|' \
  Dockerfile

docker build -t honeytrap .
docker run -it --rm --name honeytrap --net=host honeytrap
```
