---
title: Python 有序字典的实现
date: 2016-07-07 20:16:20
tags: [python, 源码阅读]
---

最近在看 requests 源码的时候看到作者使用了 urllib3 中自己实现的`OrderedDict`类，收获颇多。自己实现一个数据结构往往是最需要算法和优化的地方，各种语法糖黑科技，相当的 Pythonic，看这种代码实在是一种享受。如果要我自己实现的话，自己会想到用一个有序存储的对象（如列表）去 hack 内部的实现，但这样有几个缺点：

1. 列表的插入、删除操作性能不如字典，复杂度是 O(N) 量级的。
2. 自定义类需要继承于`dict`，没有利用继承的方法特性。

来看看大神是怎么实现的吧。
<!--more-->

## `__init__`方法
```python
class OrderedDict(dict):
    def __init__(self, *args, **kwds):
        if len(args) > 1:
            raise TypeError('expected at most 1 arguments, got %d' % len(args))
        try:
            self.__root
        except AttributeError:
            self.__root = root = []                     # sentinel node
            root[:] = [root, root, None]
            self.__map = {}
        self.__update(*args, **kwds)
```
在[上一篇文章](http://frostming.github.io/2016/06/13/python-list/)中说到一些关于列表的坑，说到不要用`a=b=[]`这样的语句来初始化，其实也不全然，我们来看 7-8 行做了什么。第 7 行使`self.__root`和`root`同时指向一个空列表，相关于给`self.__root`起了一个短别名，关键是第 8 行：
```python
>>> root[:] = [root, root, None]
>>> root
[[...], [...], None]
```
什么鬼？没见过`[...]`这种的啊，我来看看
```python
>>> root[0]
[[...], [...], None]
>>> root[0] is root
True
```
What? 自己是自己的元素？简直是从前有座山山上有座庙啊，子子孙孙无穷尽啊。到底发生了什么事？Python 中万物皆指针，而`root[:]=...`的赋值是不改变指针指向的地址而是改变指向地址的内容。右边第一个和第二个元素是指向自己的指针，这样就构造了一个我中有我的列表。
![](http://o7u6qrlad.bkt.clouddn.com/1e6f8e56cb6cea791e53c29742da76c9.png)

再看命名，明白了，这是一个**双向链表**！列表的前两个元素分别指向上一个结点和下一个结点，第三个元素是结点的值。只用两行就初始化了一个链表，学到了。另外还初始化了一个字典，暂时不知道有什么用。

## `__setitem__`方法
```python
def __setitem__(self, key, value, dict_setitem=dict.__setitem__):
    'od.__setitem__(i, y) <==> od[i]=y'
    # Setting a new item creates a new link which goes at the end of the linked
    # list, and the inherited dictionary is updated with the new key/value pair.
    if key not in self:
        root = self.__root
        last = root[0]
        last[1] = root[0] = self.__map[key] = [last, root, key]
    dict_setitem(self, key, value)
```
关键的部分到了，这个魔法方法加了第三个参数来方便子类扩展。函数体部分，画一个图就明白了。
![](http://o7u6qrlad.bkt.clouddn.com/dc7661ce1072a03bfe45c6b33647def2.png)!

1. `root`的上一个结点就是末结点，保存为`last`。
2. 创建一个新结点，它的上结点和下结点分别设为`last`和`root`，结点的值为字典的键。
3. 将`last`的下结点和`root`的上结点指向该结点。
4. 将结点加入`__map`并加入字典。

这样创建就结点就变成了新的末结点了。从此也可看出，`root`是一个守护结点，本身并不存储值，但会简化算法。`__map` 是结点的哈希表，避免了从头开始寻找所需的结点。

## `__delitem__`方法
```python
def __delitem__(self, key, dict_delitem=dict.__delitem__):
    'od.__delitem__(y) <==> del od[y]'
    # Deleting an existing item uses self.__map to find the link which is
    # then removed by updating the links in the predecessor and successor nodes.
    dict_delitem(self, key)
    link_prev, link_next, key = self.__map.pop(key)
    link_prev[1] = link_next
    link_next[0] = link_prev
```
删除结点时，从哈希表中弹出该结点，然后将它的上结点和下结点相连，并从字典中删除。

实现了这三个方法，剩下的就好办了，`__iter__`只需从头开始遍历链表并取出键值就可以了。

## 总结
实现有序字典的关键在于选取一个合适的数据结构来存储顺序信息，这里作者使用了双向链表，然后把结点哈希。这样进行插入、删除操作的时间复杂度为 O(1) ，与`dict`类型一致，代价就是 O(2n) 的空间复杂度。
