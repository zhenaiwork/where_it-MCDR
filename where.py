import os
from mcdreforged.api.all import *
from mcdreforged.api.command import GreedyText
from typing import Optional

url = '/home/zhenai/MineCraftServer/MCDR/config.txt'
op = ['zhenai_', 'Happywater_']

PLUGIN_METADATA = {
    'id': 'where_it',
    'version':'1.0',
    'name': 'where_it'
}

def rem(source):
    printly(source, 'remove')

def list(source: CommandSource, comment: Optional[str]):
    data = read()
    printly(source,'------检索到关于-' + comment + '-的坐标----')
    for i in data:
        if comment in i :
            id = data.index(i)
            printly(source, data[id])
            printly(source, data[id+1])
            printly(source, data[id+2])


def list_all(source: CommandSource):
    data = read()
    for i in data:
        printly(source, i)
def read():
    
    f=open(url)
    txt=[]
    for line in f:
        txt.append(line.strip())
    #print(txt)
    return txt



def remove():
    def re1():
        file_old = open(url, 'rb+')
        m = 25
        file_old.seek(-m, os.SEEK_END)	 

        lines = file_old.readlines()	

        file_old.seek(-len(lines[-1]), os.SEEK_END)	

        file_old.truncate()  # 截断之后的数据 

        file_old.close()
    re1()
    re1()
    re1()
    re1()

def mak(source):
    printly(source, '坐标已添加')

def make(list1):
    #printly(source, comment)
    id = list1[1]
    name = list1[2]
    x = list1[3]
    z = list1[4]
    if id == '00':
        with open(url, "a") as file:
            x1 = int(x)//8
            z1 = int(z)//8
            data = id + ' ' + name + ':\n' + '    主世界：[' + str(x) + ', 72, ' + str(z) + ']\n' + '   下界：[' + str(x1) + ', 128, ' + str(z1) + ']\n'
            print(data)
            file.write(data)
    if id == '-1':
        with open(url, "a") as file:
            x1 = int(x)*8
            z1 = int(z)*8
            data = id + ' ' + name + ':\n' + '    主世界：[' + str(x1) + ', 72, ' + str(z1) + ']\n' + '   下界：[' + str(x) + ', 128, ' + str(z) + ']\n'
            print(data)
            file.write(data)
    if id == '01':
        with open(url, "a") as file:
            x1 = int(x)//8
            z1 = int(z)//8
            data = id + ' ' + name + ':\n' + '    末地：[' + str(x) + ', 72, ' + str(z) + ']\n\n'
            print(data)
            file.write(data)

def help(source: CommandSource):
    helpl = [
        'where-it_all  列出所有坐标',
        'where-it <name>  查找与<name>相关的坐标',
        '对于管理成员--------------',
        'make <维度> <name> <xx> <zz> 添加为name的坐标，地域和主世界的坐标会自动转换',
        '01 末地，00 主世界，-1 地域',
        'remove-last 删除最后一个添加的坐标'
    ]
    for i in helpl:
        printly(source, i)


def printly(source:CommandSource, msg):
    msg = '[where_it] ' + msg
    source.reply(msg)




def on_load(server: ServerInterface, old_module):
    server.register_command(Literal('where').runs(help))

    server.register_command(Literal('where-it').then(GreedyText('name')
                                                     .runs(lambda src, ctx:list(src, ctx['name']))))
    server.register_command(Literal('where-it_all').runs(list_all))

    server.register_command(Literal('remove-last').runs(rem))
    server.register_command(Literal('make').then(GreedyText('data').runs(mak)))
    server.register_help_message('where', '查看[where_it]帮助信息')

def on_user_info(server, info):
    l = info.content
    list1 = l.split( )
    if info.content == 'remove-last':
        if info.player in op:
            remove()
    if list1[0] == 'make':
        if info.player in op:
            make(list1)
        #print(list1)
