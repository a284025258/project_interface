import os
"""
常量模块
获取项目相关目录的路径

项目路径
用例类所在路径
配置文件的路径
用例数据的路径
日志文件的路径
测试报告的路径
"""
# 获取指定文件父级目录绝对路径
# print(os.path.dirname(__file__))
# 项目路径
BASE_DIR = (os.path.dirname(os.path.dirname(__file__)))
# 用例类所在路径
CASES_DIR = os.path.join(BASE_DIR, 'testcases')
# 配置文件的路径
CONF_DIR = os.path.join(BASE_DIR, 'conf')
# 用例数据的路径
DATA_DIR = os.path.join(BASE_DIR, 'data')
# 日志文件的路径
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
# 测试报告的路径
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')