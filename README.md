linkus-django
=============

linkus 技术列表
---------------
* python 2.7.2
* django 1.3.3
* mysql 5.1
* jquery 1.6.4
* ueditor 1.2.0
* jquery.fancybox-1.3.4.js
* jquery.Jcrop.min.js
* apache2.2
* modi-wsgi-3.4


一些杂感
--------------

### 最初采用 django 和 mysql主要是出于两点

1.django 开发速度快
2.对mysql 有相关使用经验


### mysql的优势

- 可以写出复杂的sql语句，某些应用逻辑可以交给数据库处理
- 开源，免费，入门简单，易操作


### django的优势

- 提供web开发全套服务orm,template,views,middleware,session,auth,filter
- 简洁的url配置
- 强大的模板标签
- 提供全局项目配置与调试


### mysql的劣势

- 数据库复杂度增加时，对其操作难度上升
- 数据结构不易扩展，不利于数据结构变化频繁的项目
- 集群和切片与mongodb相比过于复杂
- 关系型数据库天然的缺点


###django的劣势

- 模板语言不支持python，只能扩展标签库来完成复杂的操作
- orm层以及template层与其自身高度耦合，不方便扩展
- 对于小型项目过于沉重，学习成本高


## 个人喜欢django的地方
- 丰富的标签库
- 强大而且灵活的url配置，支持各种形式的参数的定义和提取
- milldeware,filter 在某些应用场景下非常有用
- 全局的配置
- 比较丰富的插件



