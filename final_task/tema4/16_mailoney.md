# mailoney
- [https://github.com/phin3has/mailoney](https://github.com/phin3has/mailoney)

## setup
```bash
git clone https://github.com/phin3has/mailoney
cd mailoney
```

### setup docker
```bash
docker run -p 25:25 ghcr.io/phin3has/mailoney:latest
```

### setup docker compose
```bash
cat << EOF > docker-compose.yml
version: '3.8'

services:
  mailoney:
    image: ghcr.io/phin3has/mailoney:latest
    restart: unless-stopped
    ports:
      - "25:25"
    environment:
      - MAILONEY_BIND_IP=0.0.0.0
      - MAILONEY_BIND_PORT=25
      - MAILONEY_SERVER_NAME=mail.example.com
      - MAILONEY_LOG_LEVEL=INFO
      - MAILONEY_DB_URL=postgresql://postgres:postgres@db:5432/mailoney
    depends_on:
      - db

  db:
    image: postgres:15
    restart: unless-stopped
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=mailoney
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
EOF

docker compose up -d
```

### setup local (blm nyoba)
```bash
# Clone the repository
git clone https://github.com/phin3has/mailoney.git
cd mailoney

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package in development mode
pip install -e .

# Run Mailoney
python main.py
```

## testing
```bash
# test connection
telnet localhost 25
nc localhost 25

nc localhost 25
# copy paste dibawah ini
HELO test.com
MAIL FROM:<attacker@test.com>
RCPT TO:<victim@test.com>
DATA
This is a test message
.
QUIT
```

### log
```bash
docker compose logs -f mailoney

docker exec -it mailoney-db-1 psql -U postgres -d mailoney
# copy paste dibawah ini
SELECT * FROM smtp_sessions ORDER BY timestamp DESC LIMIT 5;
SELECT * FROM credentials ORDER BY timestamp DESC LIMIT 5;
```
