set -ex

docker tag flog $DOCKER_USERNAME/flog:latest
docker push $DOCKER_USERNAME/flog:latest
ssh fming@frostming.com make -C /home/fming/frostming.com
