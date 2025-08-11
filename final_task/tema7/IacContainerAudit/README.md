
# via docker
```bash
docker build -t audit-test .
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v ./output:/app/outputs -v ./workspace:/app/workspace audit-test
```

# via hosted
```bash
chmod +x scan.sh
./scan.sh
```

# manual report
```bash
python3 scripts/reporter.py --outdir output
python3 -m http.server -d output/
```