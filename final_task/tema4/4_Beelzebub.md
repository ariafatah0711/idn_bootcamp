# Beelzebub
- [https://github.com/mariocandela/beelzebub](https://github.com/mariocandela/beelzebub)

## setup
```bash
git clone https://github.com/mariocandela/beelzebub

sed -i 's/"22:22"/"2223:22"/' docker compose.yml
docker compose build
docker compose up -d
```

### with go
```bash
go mod download
go build
./beelzebub
```

### with helm
```bash
helm install beelzebub ./beelzebub-chart
helm upgrade beelzebub ./beelzebub-chart
```

## configuration
```bash
./beelzebub --confCore ./configurations/beelzebub.yaml --confServices ./configurations/services/
```

## testing
```bash
ssh root@<ip> -p 2222
# pass: root
ssh root@<ip> -p 2223
# pass: root
```

### command
- configurations/services => liat config

```bash
docker logs -f beelzebub 2>&1 | jq -R 'fromjson? | select(. != null) | .event'
```
