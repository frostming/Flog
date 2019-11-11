set -ex

rsync -avz --delete static/ --include='cards/' --include='css/' --include='js/' --include='images/' \
    --include='iconfont/' --include="robots.txt" --include='dist/' --exclude='/*' \
    fming@frostming.com:/home/fming/frostming.com/static
rsync -avz nginx/ fming@frostming.com:/home/fming/frostming.com/nginx
rsync -avz --delete --exclude='*.pyc' Pipfile* ./docker-compose.yml Dockerfile flaskblog migrations start_server.sh fming@frostming.com:/home/fming/frostming.com/
ssh fming@frostming.com bash -s << EOF
cd /home/fming/frostming.com
sudo docker-compose build web
docker-compose down
docker-compose up -d
EOF
