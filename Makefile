sync:
	-find . -name "__pycache__" -exec rm -rf {} \;
	rsync -apPv . fming@frostming.com:/home/fming/frostming.com

restart:
	-sudo find . -name "__pycache__" -exec rm -rf {} \;
	docker-compose restart

deploy:
	$(MAKE) sync
	ssh fming@frostming.com make -C /home/fming/frostming.com restart

translate:
	pybabel extract -F flaskblog/babel.cfg -k lazy_gettext -o messages.pot flaskblog/
	pybabel update -i messages.pot -d flaskblog/translations
	rm messages.pot

compile:
	pybabel compile -d flaskblog/translations

.PHONY: sync restart deploy translate compile
