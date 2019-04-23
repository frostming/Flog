# Flog

[![Build Status](https://travis-ci.org/frostming/Flog.svg?branch=master)](https://travis-ci.org/frostming/Flog)

_一个简单的博客系统，由 Flask 驱动_

![](/resources/preview.png)

## 开发本项目

1. 安装 [pipenv](https://github.com/kennethreitz/pipenv)

```bash
$ pip install pipenv
```

2. 常用命令

```bash
# 安装所有开发依赖
$ pipenv install -d
# 生成翻译文件
$ pipenv run make compile
# 升级DB
$ pipenv run flask db upgrade
```

### 后台开发

本项目管理后台使用前后端分离结构(Vue.js + Flask)，应当分别开发与调试，再进行联调。所以开发模式上存在以下几种组合：

1. 调试前端

   - 确保`static/env.development`中`VUE_APP_BASE_API = '/dev-api'`
   - 启动开发服务器：`cd static && npm run dev`
   - 此模式下所有后端请求将被 mock 拦截，<http://localhost:9527>将自动在浏览器中打开

2. 前后端联调

   - 确保`static/env.development`中`VUE_APP_BASE_API = 'http://127.0.0.1:5000/api`
   - 启动后端开发服务器：`FLASK_ENV=development pipenv run flask run`，地址为<http://127.0.0.1:5000>
   - 启动前端开发服务器：`cd static && npm run dev`，地址为<http://localhost:9527>
   - 此模式下前后端改动均能自动重启，且后端请求真实发至后端服务器

3. 准生产环境调试

   - 构建前端页面`cd static && npm run build:prod`，此时前端页面将以生产模式编译压缩
   - 启动后端开发服务器：`FLASK_ENV=development pipenv run flask run`
   - 此模式将模拟生产环境行为，后端服务器可更新，但前端不可以。

## 部署到远程服务器

### 部署到 Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

### 部署到云服务器

[Flask+Nginx 博客容器化部署](https://frostming.com/2018/09-11/flask-nginx-deployment)

## 使用管理员后台

前往`$your_domain/admin`使用账号`admin`密码`admin`(默认)登录，然后就可以开始写文章了。
前往`$your_domain/admin/setting`配置页更改密码及其他设定。

## Markdown 特性

Flog 的 Markdown 语法遵循 GitHub Flavored Markdown 规范，支持脚注、表格、文章目录、数字公式等。

此外，Flog 还支持图片排版，使用方法是将多个图片放在一起（不换行），将渲染为多列图片。例：

```
![](/images/image1.jpg) ![](/images/image2.jpg)
![](/images/image3.jpg) ![](/images/image4.jpg)
```

效果：

![](/resources/sample_images.png)

完整效果可见[我的博文](https://frostming.com/2018/01-04/from-2017-to-2018)。

## Flog 使用以下组件

- CSS and JS framework: [Bootstrap4](http://getbootstrap.com/)
- Article CSS: [yue.css](https://github.com/lepture/yue.css)
- Mardown renderer: [Marko](https://github.com/frostming/marko)
- Markdown editor: [Simple MDE](https://github.com/sparksuite/simplemde-markdown-editor)
- Picture preview: [Photoswipe](http://photoswipe.com/)
- Vue-Element-Admin

## License

本项目使用[MIT License](/LICENSE)许可开源。
