# frostming.com

*一个简单的博客系统，由Flask驱动*

![](/resources/preview.png)

## 启动开发服务器

1. 安装 [pipenv](https://github.com/kennethreitz/pipenv)

```bash
$ pip install pipenv
```

2. 准备工作

```bash
$ pipenv install
$ pipenv install -d
$ pipenv run make compile
$ pipenv run flask db upgrade
```

3. 启动服务器

```bash
$ FLASK_APP=application.py pipenv run flask run
```
成功后，访问<http://localhost:5000>查看结果

## 部署到远程服务器

### 部署到Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

### 部署到云服务器

*敬请期待*

## 使用管理员后台

前往`$your_domain/admin`使用账号`admin`密码`admin`(默认)登录，然后就可以开始写文章了。
前往`$your_domain/admin/setting`配置页更改密码及其他设定。

## Markdown特性

Flog的Markdown语法遵循GitHub Flavored Markdown规范，支持脚注、表格、文章目录、数字公式等。

此外，Flog还支持图片排版，使用方法是将多个图片放在一起（不换行），将渲染为多列图片。例：
```
![](/images/image1.jpg) ![](/images/image2.jpg)
![](/images/image3.jpg) ![](/images/image4.jpg)
```
效果：

![](/resources/sample_images.png)

完整效果可见[我的博文](https://frostming.com/2018/01-04/from-2017-to-2018)。

## Flog使用以下组件

* CSS and JS framework: [Bootstrap4](http://getbootstrap.com/)
* Article CSS: [yue.css](https://github.com/lepture/yue.css)
* Mardown renderer: [Marko](https://github.com/frostming/marko)
* Markdown editor: [Simple MDE](https://github.com/sparksuite/simplemde-markdown-editor)
* Picture preview: [Photoswipe](http://photoswipe.com/)

## License

本项目使用[MIT License](/LICENSE)许可开源。
