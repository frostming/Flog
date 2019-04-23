set -ex

docker tag flog $DOCKER_USERNAME/flog:latest
docker push $DOCKER_USERNAME/flog:latest
rsync -ar --delete ./static --include='cards/' --include='css/' --include='js/' --include='images/' \
    --include='iconfont/' --include="robots.txt" --exclude='/*' \
    fming@frostming.com:/home/fming/frostming.com/static
rsync -ar ./nginx fming@frostming.com:/home/fming/frostming.com/nginx
rsync -a ./docker-compose.yml fming@frostming.com:/home/fming/frostming.com/
ssh fming@frostming.com bash -s << EOF
docker-compose down
docker-compose pull web
docker-compose up -d
EOF
