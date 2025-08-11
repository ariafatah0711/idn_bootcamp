docker build -t audit-test .
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v ./output:/app/outputs -v ./workspace:/app/workspace audit-test
python3 -m http.server -d output