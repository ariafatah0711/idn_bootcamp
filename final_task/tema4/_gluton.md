# gluton
- [https://github.com/mushorg/glutton](https://github.com/mushorg/glutton)
- [https://go-glutton.readthedocs.io/en/latest/setup/](https://go-glutton.readthedocs.io/en/latest/setup/)

Glutton adalah honeypot agnostik protokol yang mencegat lalu lintas jaringan, menerapkan aturan yang dapat disesuaikan, dan mencatat interaksi untuk membantu menganalisis aktivitas berbahaya.

## setup
### setup docker
```bash
git clone https://github.com/mushorg/glutton
cd glutton
docker build -t glutton .
# docker run --rm --cap-add=NET_ADMIN -it glutton
# docker run --rm --cap-add=NET_ADMIN --network host -it glutton
docker run --rm --cap-add=NET_ADMIN --network host -it glutton bin/server --interface enp0s8
```

### setup manual
```bash
git clone https://github.com/mushorg/glutton.git
cd glutton
make build
bin/server --version

# --interface, -i: string - Specifies the network interface (default: eth0)
# --ssh, -s: int - If set, it overrides the default SSH port
# --logpath, -l: string - Sets the file path for logging (default: /dev/null)
# --confpath, -c: string - Defines the path to the configuration directory (default: config/)
# --debug, -d: bool - Enables debug mode (default: false)
# --version: bool - Prints the version and exits
# --var-dir: string - Sets the directory for variable data storage (default: /var/lib/glutton)

bin/server --interface <network_interface> --debug
```

## testing
```bash

```
