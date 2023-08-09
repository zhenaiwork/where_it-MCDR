# Where_it-MCDR

`where_it`是一个查看服务器各个建筑&机器坐标`MCDR`插件它是用来解决生电服来新人不知道服务器到底有什么，都在那的问题。

[作者相关](https://space.bilibili.com/516691966?spm_id_from=333.1007.0.0)



## 使用相关

`where_it`是一个服务端插件，对于客户端搭配  [Oh My MineCraft Client](https://github.com/plusls/oh-my-minecraft-client)  食用效果最佳。



在把`py`文件放入`MCDR`的插件目录下之后还需要修改`py`文件当中的`url`&`op`变量

其中`url`为你用来存放坐标的`txt`文件绝对路径，`op`为管理玩家的列表。

## 交互方式

`where_it`是通过命令的方式进行交互，其中所有玩家都可以使用的有`where`，管理在此之上还有`make`,`remove`。

## 指令的具体介绍

`where-it_all  `列出所有坐标

`where-it <name>  查找与<name>`相关的坐标



对于管理成员--------------

`make <维度> <name> <xx> <zz> `添加为name的坐标，地域和主世界的坐标会自动转换
01 末地，00 主世界，-1 地域

`remove-last `删除最后一个添加的坐标
