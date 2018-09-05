deploy:
	find . -name "*.pyc" -exec rm {} \;
	rsync -aPv . fming@frostming.com:/home/fming/frostming.com
	ssh fming@frostming.com make -C /home/fming/frostming.com restart

restart:
	docker-compose restart
