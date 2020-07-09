import unittest
from lib.ddt import ddt, data
from common.read_excel import ReadExcel
from common.http_requests import HttpRequest
from common.my_logger import log
import os
from common.constant import DATA_DIR
from common.pdbc import PDBC
import random
from common.config import my_config
from common.text_replace import data_replace
from faker import Faker

@ddt
class LoginTestCase(unittest.TestCase):
    """登录测试用例类"""
    read_excel = ReadExcel(os.path.join(DATA_DIR, 'cases.xlsx'), 'login')
    # 通过字典获取数据
    # cases = read_excel.read_data()
    # 通过对象获取数据
    cases = read_excel.read_data_obj()

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    @classmethod
    def setUpClass(cls) -> None:
        cls.pdbc = PDBC()
        cls.http_request = HttpRequest()
        cls.fake = Faker(locale='zh_CN')

    @classmethod
    def tearDownClass(cls) -> None:
        cls.pdbc.close()

    '''@data读取数据，有多少条数据，生成多少条测试用例'''
    @data(*cases)
    def test_login_case(self, case):
        """登录接口测试用例"""
        # 准备测试用例数据
        method = case.method
        url = my_config.get('url', 'url') + case.url
        expected = eval(case.expected)
        # 随机生成一个手机号
        phone = self.random_phone()
        # 替换用例动态参数
        param = eval(data_replace(case.param).replace('*random_phone*', phone))
        # 发送请求接口，获取结果
        log.info(f'正在请求地址：{url}')
        response = self.http_request.request(url=url, method=method, data=param)
        result = response.json()
        # 断言预期和实际结果
        row = case.case_id + 1
        try:
            self.assertEqual(expected, result)
            if case.check_sql is not None:
                db_result = self.pdbc.find_count(case.check_sql)
                self.assertEqual(1, db_result)
        except AssertionError as e:
            print('该用例执行未通过')
            self.read_excel.write_data(row=row, column=9, value='未通过')
            print(f'预期结果：{expected}')
            print(f'实际结果：{result}')
            log.error(e)
            log.info('[{case.title}] --> 该用例执行未通过')
            raise e
        else:
            print('该用例执行通过')
            self.read_excel.write_data(row=row, column=9, value='通过')
            print(f'预期结果：{expected}')
            print(f'实际结果：{result}')
            log.info(f'[{case.title}] --> 该用例执行通过')

    def random_phone(self):
        """随机生成一个手机号"""
        phone = self.fake.phone_number()
        if self.pdbc.find_count(f"SELECT * FROM member WHERE MobilePhone = {phone}"):
            phone = self.random_phone()
        return phone
