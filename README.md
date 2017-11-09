# Flog

*A simple and elegant blog engine powered by Flask*

## Start a development server

1. Install [pipenv](https://github.com/kennethreitz/pipenv)

```bash
$ pip install pipenv
```

2. Install requirements

```bash
$ pipenv install
```

3. Change the configurations in `flaskblog/themes/footstrap/_config.yml`

4. Initialize the app

```bash
$ export FLASK_APP=application.py
$ pipenv run flask init
$ pipenv run flask createadmin
# Input informations as the console prompts
```

5. Start the server

```bash
$ FLASK_APP=application.py pipenv run flask run
```

## Deploy the app to web server

`Procfile` is provided for deploying to Heroku, and you need to set environment variable `DATABASE_URL` to point to your DB URL.

## Credits

* CSS and JS framework: [Bootstrap4](http://getbootstrap.com/)
* Article CSS: [yue.css](https://github.com/lepture/yue.css)
* Mardown renderer: [mistune](https://github.com/lepture/mistune)
* Markdown editor: [Simple MDE](https://github.com/sparksuite/simplemde-markdown-editor)
* Picture preview: [Photoswipe](http://photoswipe.com/)

## License

This project is developed and owned by Frost Ming, and is allowed for only personal use.
