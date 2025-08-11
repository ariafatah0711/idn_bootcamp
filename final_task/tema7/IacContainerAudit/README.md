
# via docker
```bash
docker build -t audit-test .
docker run -v /var/run/docker.sock:/var/run/docker.sock -v ./output:/app/outputs audit-test
```

# via hosted
```bash
chmod +x scan.sh
./scan.sh
```