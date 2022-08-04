# Flog

_一个简单的博客系统，由 Flask 驱动_

<div align="center">

![](/static/images/flog.png)
</div>

## 功能特性

* 集成后台管理页面
* 完善的SEO优化
* 可选的，集成第三方登录的内置评论系统
* 支持接入Disqus, Google Analytics, 腾讯云对象存储
* Docker 部署
* Letsencrypt SSL证书
* 自由更改主题色

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

## 博客的运行与部署

请移步[本项目的Wiki页面](https://github.com/frostming/Flog/wiki)

## Flog 使用以下组件

- CSS and JS framework: [Bootstrap4](http://getbootstrap.com/)
- Mardown renderer: [Marko](https://github.com/frostming/marko)
- Markdown editor: [Simple MDE](https://github.com/sparksuite/simplemde-markdown-editor)
- Picture preview: [Photoswipe](http://photoswipe.com/)
- Vue-Element-Admin

## License

本项目使用[MIT License](/LICENSE)许可开源。
