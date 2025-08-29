import json
import os
import re
from typing import Any, Tuple
from mcdreforged.api.all import *
from mcdreforged.api.rtext import *
from mcdreforged.api.types import ServerInterface, Info
from mcdreforged.api.command import SimpleCommandBuilder, Integer, Text, GreedyText


url = 'E:\server-demo\MCDReforged-master\config\config.yaml'
op = ['zhenai_', 'Happywater_']

PLUGIN_METADATA = {
    'id': 'where-it',
    'version':'2.0',
    'name': 'where_it'
}

# Configuration file path
# 配置文件路径
CONFIG_FILE = 'config/here.json'

# DO NOT change here!!! If you need to change the config value, pls change this in config file
# 这里别动！！！要改配置去配置文件里改
default_config = {
	'highlight_time': 15,
	'display_voxel_waypoint': True,
	'display_xaero_waypoint': True,
	'click_to_teleport': False
}

here_user = 0

dimension_display = {
	'0': 'createWorld.customize.preset.overworld',
	'-1': 'advancements.nether.root.title',
	'1': 'advancements.end.root.title'
}

dimension_color = {
	'0': RColor.dark_green,
	'-1': RColor.dark_red,
	'1': RColor.dark_purple
}


class Config:
	def __init__(self, file: str) -> None:
		self.file = file
		self.data = {}

	def __write_config(self, new_data = None):
		if isinstance(new_data, dict):
			self.data.update(new_data)
		with open(self.file, 'w', encoding='UTF-8') as f:
			json.dump(self.data, f, indent=4)

	def __get_config(self):
		with open(self.file, 'r', encoding='UTF-8') as f:
			self.data.update(json.load(f))

	def load(self, server: ServerInterface):
		if not os.path.isdir(os.path.dirname(self.file)):
			os.makedirs(os.path.dirname(self.file))
			server.logger.info('Config directory not found, created')
		if not os.path.isfile(self.file):
			self.__write_config(default_config)
			server.logger.info('Config file not found, using default')
		else:
			try:
				self.__get_config()
			except json.JSONDecodeError:
				self.__write_config(default_config)
				server.logger.info('Invalid config file, using default')

	def __getitem__(self, key: str) -> Any:
		ret = self.data.get(key)
		if ret is None and key in default_config.keys():
			ret = default_config[key]
			self.__write_config({key: ret})
		return ret


config = Config(CONFIG_FILE)


def process_coordinate(text: str) -> tuple:
	data = text[1:-1].replace('d', '').split(', ')
	data = [(x + 'E0').split('E') for x in data]
	return tuple([float(e[0]) * 10 ** int(e[1]) for e in data])


def process_dimension(text: str) -> str:
	return text.replace(re.match(r'[\w ]+: ', text).group(), '', 1)


def coordinate_text(x: float, y: float, z: float, dimension: str, opposite=False):
	dimension_coordinate_color = {
		'0': RColor.green,
		'-1': RColor.red,
		'1': RColor.light_purple
	}
	dimension_name = {
		'0': 'minecraft:overworld',
		'1': 'minecraft:the_end',
		'-1': 'minecraft:the_nether'
	}

	if opposite:
		dimension = '-1' if dimension == '0' else '0'
		x, z = (x / 8, z / 8) if dimension == '-1' else (x * 8, z * 8)

	pattern = RText('[{}, {}, {}]'.format(int(x), int(y), int(z)), dimension_coordinate_color[dimension])
	dim_text = RTextTranslation(dimension_display[dimension], color=dimension_color[dimension])

	return pattern.h(dim_text) if not config['click_to_teleport'] else pattern.h(
		dim_text + ': 点击以传送到' + pattern.copy()
		).c(RAction.suggest_command, 
		'/execute in {} run tp {} {} {}'.format(dimension_name[dimension], int(x), int(y), int(z)))


def display(server: ServerInterface, name: str, position: Tuple[float, float, float], dimension: str):
	x, y, z = position
	dimension_convert = {
		'minecraft:overworld': '0',
		'"minecraft:overworld"': '0',
		'minecraft:the_nether': '-1',
		'"minecraft:the_nether"': '-1',
		'minecraft:the_end': '1',
		'"minecraft:the_end"': '1'
	}
	
	if dimension in dimension_convert:  # convert from 1.16 format to pre 1.16 format
		dimension = dimension_convert[dimension]

	# text base
	texts = RTextList(
		'§e{}§r'.format(name),
		' @ ',
		RTextTranslation(dimension_display[dimension], color=dimension_color[dimension]),
		' ',
		coordinate_text(x, y, z, dimension)
	)

	# click event to add waypoint
	if config['display_voxel_waypoint']:
		texts.append( ' ',
			RText('[+V]', RColor.aqua).h('§bVoxelmap§r: 点此以高亮坐标点, 或者Ctrl点击添加路径点').c(
				RAction.run_command, '/newWaypoint [x:{}, y:{}, z:{}, dim:{}]'.format(
					int(x), int(y), int(z), dimension
				)))
	if config['display_xaero_waypoint']:
		texts.append( ' ',
			RText('[+X]', RColor.gold).h('§6Xaeros Minimap§r: 点击添加路径点').c(
				RAction.run_command, 'xaero_waypoint_add:{}:{}:{}:{}:{}:6:false:0:Internal_{}_waypoints'.format(
					name + "'s Location", name[0], int(x), int(y), int(z), dimension.replace('minecraft:', '').strip()
				)))

	# coordinate conversion between overworld and nether
	if dimension in ['0', '-1']:
		texts.append(
			' §7->§r ',
			coordinate_text(x, y, z, dimension, opposite=True)
			)

	server.say(texts)

	# highlight
	if config['highlight_time'] > 0:
		server.execute('effect give {} minecraft:glowing {} 0 true'.format(name, config['highlight_time']))


#上面借用狐狸的代码来帮我坐标高亮

def say(server: ServerInterface,key, value):
	name = str(key)
	position = value[0:3]
	dimension = str(value[3])
	display(server, name, position, dimension)



def gitdata():
    #读取url中的内容并把它转换成一个字典
    with open(url, 'r', encoding='utf-8') as f:
        red = f.read()
    #吧content转换成一个字典
    data = eval(red)
    return data

def whall(server: ServerInterface):
	data = gitdata()
	for key, value in data.items():
		say(server, key, value)

def add( server: ServerInterface, name, position, dimension):
	data = gitdata()
	if name in data.keys():
		server.say('名字重复了，如需修改请先删除原坐标')
	else:
		dimension = int(dimension)
		data[name] = position + [dimension]
		print(position + [dimension])
		with open(url, 'w', encoding='utf-8') as f:
			f.write(str(data))
		server.say('添加成功')
		dimension = str(dimension)
		display(server, name, position, dimension)

def wh( server: ServerInterface, name):
	data = gitdata()
	server.say('查询结果如下:')
	result = {key: value for key, value in data.items() if name in key}
	print(result)
	for key, value in result.items():
		say(server, key, value)

def rem(server: ServerInterface, name):
	data = gitdata()
	del data[name]
	with open(url, 'w', encoding='utf-8') as f:
		f.write(str(data))
	server.say('删除成功')

def addhere(server: ServerInterface, name, plname):
	#TODO让它能正常获取玩家坐标

	pos = server.rcon_query('data get entity ' + plname + ' Pos')
	di = server.rcon_query('data get entity ' + plname + ' Dimension')
	print(type(pos))
	try:
		coord_match = re.search(r'\[([-\d.d, ]+)\]', pos)
	except:
		server.say('获取坐标失败')
	if coord_match:
		coord_str = coord_match.group(1)
		# 分割字符串并移除'd'字符，然后转换为浮点数
		coords = [float(coord.replace('d', '')) for coord in coord_str.split(', ')]
		# 转换为整数
		coords_int = [int(coord) for coord in coords]
	else:
		coords_int = None

	# 从维度文本中提取维度
	dimension_match = re.search(r'"([^"]+)"', di)
	if dimension_match:
		dimension_str = dimension_match.group(1)
		# 定义维度映射字典
		dimension_map = {
			"minecraft:overworld": 0,
			"minecraft:the_nether": -1,
			"minecraft:the_end": 1
		}
		# 获取维度ID
		dimension_id = dimension_map.get(dimension_str)
	else:
		dimension_id = None

	# 输出结果
	print(coords_int, dimension_id)
	#add(server, name, coords_int, dimension_id)

def on_load(server: PluginServerInterface, prev_module):
	server.register_help_message('whall', '查询所有坐标')
	server.register_help_message('wh <name>', '查询指定名字的坐标')
	server.register_help_message('whadd <name> <x> <y> <z> <dimension>', '添加坐标，dimension为0,1,-1；0为主世界，1为末地，-1为地狱')
	server.register_help_message('whre <name>', '删除坐标')
	server.register_help_message('whaddhere <name> <player>', '获取玩家坐标并添加(需要rcon权限，应为奇葩的原因目前不可用)')
	server.register_help_message('gl <xx> <yy> <zz> <dimension>', '高亮一个坐标，dimension为0,1,-1；0为主世界，1为末地，-1为地狱')

def on_user_info(server, info):
    l = info.content
    list1 = l.split( )
    if list1[0] == 'whall':
        whall(server)
    if list1[0] == 'wh':
        wh(server, list1[1])
    if list1[0] == 'whadd':
        add(server, list1[1], [int(list1[2]), int(list1[3]), int(list1[4])], list1[5])
    if list1[0] == 'whaddhere':
        addhere(server, list1[1], list1[2])
    if list1[0] == 'whre' and info.player in op:
        rem(server, list1[1])
	#如果玩家不在op列表中，则不告知权限不足
    if list1[0] == 'whre' and info.player not in op:
        server.reply(info, '权限不足')
    if list1[0] == 'gl':
        display(server, 'gl', [int(list1[1]), int(list1[2]), int(list1[3])], list1[4])
