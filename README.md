# Flog

*A simple and elegant blog engine powered by Flask*: [DEMO](https://flog-demo.herokuapp.com/)

![](preview.png)

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

6. Access the admin interface

Go to `$your_domain/admin` and login with the admin user name and password set in step 4.

7. Start writing a post!

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
