---
title: 在博客与笔记中使用Markdown
date: 2016-5-25 19:00:00
tags: [markdown, evernote, 个人博客, hexo]
image: http://soft.xiaoshujiang.com/img/d.png
---

## 博客的搭建
> 前段时间在 StackOverflow 与 Quora 上我接触到了 Markdown 标记语言，瞬时就被这种易用、美观、高逼格的东西所俘获，顿时深感之前在 QQ 空间之类的平台上写博的体验之差，往往调格式就要耗费很多的时间。于是就有了迁移到另一个博客平台的想法，用过的产品有：

<!--more-->
- [简书](http://www.jianshu.com)：包含社交功能的 Markdown 博客网站。
- [CmdMarkdown](https://www.zybuluo.com/mdeditor)：简单纯粹，功能强大，丰富语法支持，但是自带样式我不是很喜欢。
- PyCharm 的 Markdown 插件：HTML样式简陋，高级功能需付费。

这些我都不是特别满意，于是便萌生了干脆建一个个人博客的想法。通过多方考查，得到一个比较好的解决方案：Hexo + Github page。Github page 是基于静态页面的免费个人网站，而 Hexo 刚好就是基于 node.js 的静态博客，并且原生支持 Markdown 还有海量美观的模板。[^1x]

[^1x]: [HEXO+Github,搭建属于自己的博客 - 简书](http://www.jianshu.com/p/465830080ea9)

## 文章云存储

博客建好以后，那么问题来了：如何随时随地地把想法记录下来以待日后放进博客？这就需要一个云同步的平台，有以下几种选择：

- 将 markdown 文件托管到 GitHub
- 使用笔记应用存取 Markdown 文件

目前很多 markdown 编辑器都支持保存到 github 或者笔记应用，最终我选择了后者。原因是我只在家用的笔记本上配置了博客的环境，所以只能在家里更新博客。而且我总归需要一个笔记应用来存放笔记。

## 笔记应用

考察了 Onenote，有道云，印象笔记之后我最终选择了印象笔记。首先是因为界面美观，其次是支持丰富的扩展，在 Chrome 上的 [印象剪藏](https://www.yinxiang.com/webclipper/)也是相当好用，而相比而言有道云虽然界面简洁大方，但 Chrome 的扩展就大为不及了。

## Markdown 编辑器

那么下一步就是选用合适的编辑器了，有以下几点要求：

- 需要有网页端
- 支持保存到 Evernote
- 双栏预览功能
- 语法支持不能太少
- 界面不能太难看

综合以上考虑，[小书匠](http://soft.xiaoshujiang.com/)无疑是一个很好的选择，全平台支持，并且有网页版，支持保存到 dropbox, github, evernote 等。还自带图床，简直不要更赞。
![](http://soft.xiaoshujiang.com/img/bind.png)

好了，一切都搞定了，赶紧来试一下吧，把文章同步到印象笔记后，文章末尾会附上一个 md 源文件的链接，这样你在任何一台电脑上只要下载这个文件再导入小书匠就可以继续编辑了。
