sync:
	find . -name "*.pyc" -exec rm {} \;
	rsync -apPv . fming@frostming.com:/home/fming/frostming.com

restart:
	find . -name "*.pyc" -exec rm {} \;
	$(MAKE) compile
	docker-compose restart

deploy:
	$(MAKE) sync
	ssh fming@frostming.com make -C /home/fming/frostming.com restart

translate:
	pybabel extract -F flaskblog/babel.cfg -k lazy_gettext -o messages.pot flaskblog/
	pybabel update -i messages.pot -d flaskblog/translations

compile:
	pybabel compile -d flaskblog/translations
