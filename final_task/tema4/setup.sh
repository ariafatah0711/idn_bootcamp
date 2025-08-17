sudo apt update

# docker
sudo apt install docker

# docker compose
DOCKER_CONFIG=${DOCKER_CONFIG:-$HOME/.docker}
mkdir -p $DOCKER_CONFIG/cli-plugins
curl -SL https://github.com/docker/compose/releases/download/v2.29.0/docker compose-linux-x86_64 -o $DOCKER_CONFIG/cli-plugins/docker compose

chmod +x $DOCKER_CONFIG/cli-plugins/docker compose
# or
sudo chmod +x /usr/local/lib/docker/cli-plugins/docker compose

docker compose version
