set -ex

docker tag flog $DOCKER_USERNAME/flog:latest
docker push $DOCKER_USERNAME/flog:latest
rsync -avz --delete static/ --include='cards/' --include='css/' --include='js/' --include='images/' \
    --include='iconfont/' --include="robots.txt" --include='dist/' --exclude='/*' \
    fming@frostming.com:/home/fming/frostming.com/static
rsync -avz nginx/ fming@frostming.com:/home/fming/frostming.com/nginx
rsync -avz ./docker-compose.yml fming@frostming.com:/home/fming/frostming.com/
ssh fming@frostming.com bash -s << EOF
cd /home/fming/frostming.com
docker pull $DOCKER_USERNAME/flog:latest
docker-compose down
docker-compose up -d
docker images|grep "<none>"|awk '{print $3}'|xargs -ti docker rmi {}
EOF
