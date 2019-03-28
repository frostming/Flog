set -ex

cd /home/fming/frostming.com
git pull
docker-compose down
docker-compose pull web
docker-compose up -d
