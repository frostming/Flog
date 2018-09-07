# frostming.com

*A simple and elegant blog engine powered by Flask*

![](preview.png)

## Start a development server

1. Install [pipenv](https://github.com/kennethreitz/pipenv)

```bash
$ pip install pipenv
```

2. Preparation

```bash
$ pipenv install
$ pipenv install -d
$ pipenv run make compile
$ pipenv run flask db upgrade
```

3. Start the server

```bash
$ FLASK_APP=application.py pipenv run flask run
```

4. Access the admin interface

Go to `$your_domain/admin` and login with the admin user name and password.
Go to `$your_domain/admin/setting` to change the settings of your site.

5. Start writing a post!

## Deploy the app to web server

`Procfile` is provided for deploying to Heroku, and you need to set environment variable `DATABASE_URL` to point to your DB URL.

## Credits

* CSS and JS framework: [Bootstrap4](http://getbootstrap.com/)
* Article CSS: [yue.css](https://github.com/lepture/yue.css)
* Mardown renderer: [Marko](https://github.com/frostming/marko)
* Markdown editor: [Simple MDE](https://github.com/sparksuite/simplemde-markdown-editor)
* Picture preview: [Photoswipe](http://photoswipe.com/)

## License

The project is released under [MIT License](/LICENSE)
