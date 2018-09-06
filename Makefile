sync:
	find . -name "*.pyc" -exec rm {} \;
	rsync -aPv . fming@frostming.com:/home/fming/frostming.com

restart:
	find . -name "*.pyc" -exec rm {} \;
	$(MAKE) translate
	docker-compose restart

deploy:
	$(MAKE) sync
	ssh fming@frostming.com make -C /home/fming/frostming.com restart

translate:
	pybabel extract -F flaskblog/babel.cfg -o messages.pot flaskblog/
	pybabel update -i messages.pot -d flaskblog/translations
	pybabel compile -d flaskblog/translations
