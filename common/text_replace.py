"""
封装一个替换数据的方法：
1、替换用例中的参数
2、简化替换的流程

思路：
1、获取用例数据
2、判断该条用例数据是否需要替换
3、对数据进行替换
"""

import re
from common.config import my_config


class ConText:
    """用来临时保存接口之间依赖参数的类
    实现方式：反射机制
    """
    pass


def data_replace(data):
    """替换动态参数"""
    while re.search(r'#(\w+)#', data):
        res = re.search(r'#(\w+)#', data)
        # 提取要替换的内容
        r_data = res.group()
        # 获取要替换的字段
        key = res.group(1)
        try:
            # 从配置文件读取字段
            value = my_config.get('data', key)
        except Exception:
            # 从ConText类中读取
            value = getattr(ConText, key)
        # 替换
        data = re.sub(r_data, str(value), data)
    return data


# if __name__ == '__main__':
#     s1 = "{'mobilephone': '#phone#','pwd': '#pwd#'}"
#     print(data_replace(s1))
