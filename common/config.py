from configparser import ConfigParser
import os
from common.constant import CONF_DIR


class MyConfig(ConfigParser):
    def __init__(self):
        super().__init__()
        # self.read(filenames=os.path.join(CONF_DIR, 'conf.ini'), encoding='utf8')
        config = ConfigParser()
        config.read(filenames=os.path.join(CONF_DIR, 'env.ini'), encoding='utf8')
        # 获取开关的值
        env = config.getint('env', 'switch')
        # 根据开关的值读取不同环境配置文件
        # 1、正式环境 2、测试环境 3、预发布环境
        if env == 1:
            self.read(filenames=os.path.join(CONF_DIR, 'production.ini'), encoding='utf8')
        elif env == 2:
            self.read(filenames=os.path.join(CONF_DIR, 'conf.ini'), encoding='utf8')
        elif env == 3:
            self.read(filenames=os.path.join(CONF_DIR, 'pre.ini'), encoding='utf8')


my_config = MyConfig()

# 写入配置项
# 判断配置项是否存在
# if not my_config.has_section('test'):
#     my_config.add_section('test')
# # 写入配置内容
# my_config.set('test', 'name', 'Jax')
# with open(file='config.ini', mode='w', encoding='utf8') as fp:
#     my_config.write(fp)
