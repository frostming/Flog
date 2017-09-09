---
title: How does it work - with_metaclass
date: 2017-08-28 19:57:59
tags:
  - howdoesitworks
  - python
image: http://blog.edisonnation.com/wp-content/uploads/2015/10/HOW-DOES-IT-WORK.jpg
---
我在看源代码的时候，经常蹦出这一句：How does it work! 竟然有这种操作？本系列文章，试图剖析代码中发生的魔法。顺便作为自己的阅读笔记，以作提高。

先简单介绍下Python中的元类(metaclass)。元类就是创建类的类，对于元类来说，类是它的实例，`isinstance(cls, metaclass)`将返回`True`。Python中的所有类，都是`type`的实例，换句话说，`type`是元类的基类。使用`type`创建一个类的方法如下：
<!--more-->
```python
>>> type('MyClass', (), {})
<class '__main__.MyClass'>
```
`type`接受三个参数，第一个参数是类名称，第二个参数是继承的基类的元组，第三个参数是类的命名空间。上例中，我们创建了一个无基类（直接继承`object`），无初始命名空间的类`MyClass`。

*注：使用`type`创建的类和使用元类的类，都是新式类*

使用元类后，该类将由定义的元类实例化来创建。定义的方法在Python 2与Python 3中有所不同：
```python
# Python 2:
class MyClass(object):
    __metaclass__ = MyMeta

# Python 3:
class MyClass(metaclass=MyMeta):
    pass
```
如果你的项目需要兼容Python 2和Python 3，就需要使用一种方法，同时支持Python 2和Python 3。元类有两个基本特性：

* 元类实例化得到类
* 元类能被子类继承

根据这两个特性，我们不难得到解决方案：

* 用元类实例化得到一个临时类
* 定义类时继承这个临时类

我们可以写出一个`with_metaclass`函数：
```python
def with_metaclass(meta, *bases):
    """Compatible metaclass

    :param meta: the metaclass
    :param *bases: base classes
    """
    return meta('temp_class', bases, {})

# Testing:
class TestMeta(type):
    def __new__(cls, name, bases, d):
        d['a'] = 'xyz'
        return type.__new__(cls, name, bases, d)


class Foo(object):pass

class Bar(with_metaclass(TestMeta, Foo)): pass
```
我们就创建了一个以`TestMeta`为元类，继承`Foo`的类`Bar`。验证：
```python
>>> Bar.a
'xyz'
>>> Bar.__mro__
(<class '__main__.Bar'>, <class '__main__.temp_class'>, <class '__main__.Foo'>, <class 'object'>)
```
一切正常，但我们看到在`Bar`的mro里混进了一个临时类`temp_class`，你忽略它吧，有时会很麻烦。作为完美主义者，我想寻找一种解决办法，不要在mro中引入多余的类。

Python的`six`模块专门为解决Python 2to3兼容问题而生，模块里带有一个`with_metaclass`函数，我们来看它是怎么实现的：（为了debug，添加了一个print语句）
```python
def with_metaclass(meta, *bases):
    class metaclass(type):
        def __new__(cls, name, this_bases, d):
            print(cls, "new is called")
            return meta(name, bases, d)
    return type.__new__(metaclass, 'temp_class', (), {})

# Testing:
class TestMeta(type):
    def __new__(cls, name, bases, d):
        d['a'] = 'xyz'
        print(cls, "new is called")
        return type.__new__(cls, name, bases, d)
```
一时看不懂？没关系，我们来用用看，为了看清楚过程，我们分成两步执行：
```python
>>> temp = with_metaclass(TestMeta, Foo)
>>> class Bar(temp): pass
...
<class '__main__.with_metaclass.<locals>.metaclass'> new is called
<class '__main__.TestMeta'> new is called
>>> Bar.a
'xyz'
>>> Bar.__mro__
(<class '__main__.Bar'>, <class '__main__.Foo'>, <class 'object'>)
```
我们明明生成了一个临时类`temp_class`，但后来竟然消失了！下面来仔细分析函数的运行过程。首先我们看到，执行第一步生成临时类时，两个`__new__`都没有调用，而第二步定义类时，两个`__new__`都调用了。奥秘就在函数的返回语句`return type.__new__(metaclass, 'temp_class', (), {})`，它创建了一个临时类，具有如下属性：

* 名称为`temp_class`
* 是函数内部类`metaclass`的实例，它的元类是`metaclass`
* 没有基类
* 创建时仅调用了`type`的`__new__`的方法

这是一个**`metaclass`实例的不完全版本**。接下来，定义`Bar`时，`Bar`得到继承的元类`metaclass`，过程如下：
1. 实例化`metaclass`
2. 调用`metaclass.__new__`
3. 返回`meta(name, bases, d)`， `meta=TestMeta`，`bases=(Foo,)`
4. 调用`TestMeta.__new__`实例化得到`Bar`

`Bar`的基类由第3步得到，于是就去除了`temp_class`，这其实用到了闭包，`with_metaclass`返回的临时类中，本身无任何属性，但包含了元类和基类的所有信息，并在下一步定义类时将所有信息解包出来。

以上就是`with_metaclass`源代码的解析，通过这篇文章，相信能加深元类与闭包的理解。
