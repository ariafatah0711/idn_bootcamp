# dicompot
- [https://github.com/nsmfoo/dicompot](https://github.com/nsmfoo/dicompot)

## setup
```bash
git clone https://github.com/nsmfoo/dicompot.git
cd dicompot
docker build -t dicompot:latest .

docker run --rm --read-only --net="host" --name="dicompot" --detach --tty --interactive --publish=11112:11112 dicompot:latest

docker logs dicompot
```

## testing
```bash

```
