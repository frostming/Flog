set -ex

cd $DEPLOY_DIR
git pull
docker-compose down
docker-compose pull web
docker-compose up -d
