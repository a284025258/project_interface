import logging
from logging.handlers import TimedRotatingFileHandler
from common.config import my_config
from common.constant import LOGS_DIR
import os

# 读取配置文件日志收集器日志收集等级
logger_level = my_config.get('log', 'logger_level')
# 读取配置文件控制台输出渠道日志收集等级
sh_level = my_config.get('log', 'sh_level')
# 读取配置文件文件输出渠道日志收集等级
fh_level = my_config.get('log', 'fh_level')
# 读取配置文件日志保存地址
filename = my_config.get('log', 'filename')

class MyLogger(object):
    def __new__(cls, *args, **kwargs):
        """
        类直接调用，创建对象
        :param args:
        :param kwargs:
        :return:
        """
        # 创建日志收集器
        my_log = logging.getLogger('my_log')
        # 设置日志收集器日志收集等级
        my_log.setLevel(logger_level)
        # 创建输出渠道
        sh = logging.StreamHandler()
        sh.setLevel(sh_level)
        # 日志轮转 按天轮转 最长保留30天日志
        fh = TimedRotatingFileHandler(filename=os.path.join(LOGS_DIR, filename), when='D', encoding='utf8', backupCount=30)
        fh.setLevel(fh_level)
        # 将输出渠道添加到日志收集器
        my_log.addHandler(sh)
        my_log.addHandler(fh)
        # 设置日志格式
        format = '[%(asctime)s] - [%(filename)s --> line:%(lineno)d] - [%(levelname)s] : [%(message)s]'
        formatter = logging.Formatter(format)
        # 将格式对象绑定到输出渠道
        sh.setFormatter(formatter)
        fh.setFormatter(formatter)
        return my_log

log = MyLogger()

# if __name__ == '__main__':
#     log.debug('----------调试信息----------')
#     log.info('----------常规输出----------')
#     log.warning('----------警告信息----------')
#     log.error('----------报错信息----------')
#     log.critical('--------严重错误信息--------')