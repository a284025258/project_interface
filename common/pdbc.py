import pymysql
from common.config import my_config

"""
封装需求：逻辑代码封装成方法，关键数据做参数化处理
"""


class PDBC(object):
    def __init__(self):
        self.conn = pymysql.connect(host=my_config.get("mysql", "host"),
                                    port=my_config.getint("mysql", "port"),
                                    user=my_config.get("mysql", "user"),
                                    password=my_config.get("mysql", "password"),
                                    database=my_config.get("mysql", "database"),
                                    charset=my_config.get("mysql", "charset"))
        self.cur = self.conn.cursor()

    def close(self):
        # 关闭游标
        self.cur.close()
        # 断开连接
        self.conn.close()

    def find_one(self, sql):
        """查询一条数据"""
        self.conn.commit()
        self.cur.execute(sql)
        return self.cur.fetchone()

    def find_all(self, sql):
        """查询多条数据"""
        self.conn.commit()
        self.cur.execute(sql)
        return self.cur.fetchall()

    def find_count(self, sql):
        self.conn.commit()
        """返回结果条数"""
        return self.cur.execute(sql)


# if __name__ == '__main__':
#     pdbc = PDBC()
#     result = pdbc.find_all("SELECT * FROM member WHERE MobilePhone = '13133333333'")
#     print(result)