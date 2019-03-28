deploy:
	git pull
	docker-compose down
	docker-compose pull web
	docker-compose up -d

translate:
	pybabel extract -F flaskblog/babel.cfg -k lazy_gettext -o messages.pot flaskblog/
	pybabel update -i messages.pot -d flaskblog/translations
	rm messages.pot

compile:
	pybabel compile -d flaskblog/translations

.PHONY: deploy translate compile
