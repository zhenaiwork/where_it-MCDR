# Where_it-MCDR

`where_it`是一个查看服务器各个建筑&机器坐标的`MCDR`插件 它是用来解决生电服来新人不知道服务器到底有什么，都在那的问题。

[作者相关](https://space.bilibili.com/516691966?spm_id_from=333.1007.0.0)

# where-it 2.x

```python
	server.register_help_message('whall', '查询所有坐标')
	server.register_help_message('wh <name>', '查询指定名字的坐标')
	server.register_help_message('whadd <name> <x> <y> <z> <dimension>', '添加坐标，dimension为0,1,-1；0为主世界，1为末地，-1为地狱')
	server.register_help_message('whre <name>', '删除坐标')
	server.register_help_message('whaddhere <name> <player>', '获取玩家坐标并添加(需要rcon权限，应为奇葩的原因目前不可用)')
	server.register_help_message('gl <xx> <yy> <zz> <dimension>', '高亮一个坐标，dimension为0,1,-1；0为主世界，1为末地，-1为地狱')
```

使用方法全在上面的help了，这里只讲腐竹怎么怎么安装

## 安装

首先把py文件放在MCDR的插件目录下

然后创建一个`xxx.yaml`文件

打开py文件修改变量

```python
url = 'E:\server-demo\MCDReforged-master\config\config.yaml'
op = ['zhenai_', 'Happywater_']
```

其中url是你的 `xxx,yaml`的绝对路径用来存放坐标，op 是可以删除坐标的玩家（其他玩家可以添加坐标但不能删除）

