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
        url = my_config.get('url', 'url') + case.url
        # 随机生成一个 username
        username = self.random_username()
        # 替换用例随机生成的 username
        param = eval(data_replace(case.param).replace('*username*', username))
        # 发送请求接口，获取结果
        log.info(f'正在请求地址：{url}')
        response = self.http_request.request(url=url, method=case.method, data=param)
        result = response.json()
        # 断言预期和实际结果
        row = case.case_id + 1
        try:
            self.assertEqual(case.expected_code, response.status_code)
            if response.status_code != 200:
                self.assertEqual(eval(case.expected_text), result)
            if case.check_sql:
                db_result = self.pdbc.find_count(data_replace(case.check_sql))
                self.assertEqual(1, db_result)
        except AssertionError as e:
            print('该用例执行未通过')
            self.read_excel.write_data(row=row, column=10, value='未通过')
            print(f'预期结果：{case.expected_code}')
            print(f'实际结果：{response.status_code}')
            log.error(e)
            log.info('[{case.title}] --> 该用例执行未通过')
            raise e
        else:
            print('该用例执行通过')
            self.read_excel.write_data(row=row, column=10, value='通过')
            print(f'预期结果：{case.expected_code}')
            print(f'实际结果：{response.status_code}')
            log.info(f'[{case.title}] --> 该用例执行通过')

    def random_username(self):
        """随机生成一个未注册的 6位 username """
        username = self.fake.user_name().ljust(6, '0')
        if self.pdbc.find_count(f"SELECT id FROM auth_user WHERE username = '{username}'"):
            phone = self.random_username()
        return username
