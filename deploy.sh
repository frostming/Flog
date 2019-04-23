set -ex

docker tag flog $DOCKER_USERNAME/flog:latest
docker push $DOCKER_USERNAME/flog:latest
rsync -aPr --delete ./static fming@frostming.com:/home/fming/frostming.com/static
rsync -aPr ./nginx fming@frostming.com:/home/fming/frostming.com/nginx
rsync -aP ./docker-compose.yml fming@frostming.com:/home/fming/frostming.com/
ssh fming@frostming.com bash -s << EOF
docker-compose down
docker-compose pull web
docker-compose up -d
EOF
