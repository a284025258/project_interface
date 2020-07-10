import unittest
from lib.ddt import ddt, data
from common.read_excel import ReadExcel
from common.http_requests import http_request
from common.my_logger import log
import os
from common.constant import DATA_DIR
from common.pdbc import PDBC
import random
from common.config import my_config
from common.text_replace import data_replace
from faker import Faker

@ddt
class RegisterTestCase(unittest.TestCase):
    """注册测试用例类"""
    read_excel = ReadExcel(os.path.join(DATA_DIR, 'cases.xlsx'), 'register')
    # 通过字典获取数据
    # cases = read_excel.read_data()
    # 通过对象获取数据
    cases = read_excel.read_data_obj()

    def setUp(self) -> None:
        pass

    @classmethod
    def setUpClass(cls) -> None:
        cls.pdbc = PDBC()
        cls.fake = Faker(locale='zh_CN')

    @classmethod
    def tearDownClass(cls) -> None:
        cls.pdbc.close()

    '''@data读取数据，有多少条数据，生成多少条测试用例'''
    @data(*cases)
    def test_register_case(self, case):
        """登录接口测试用例"""
        # 准备测试用例数据
        # 随机生成一个8位用户名
        username = self.random_username()
        # 随机生成一个邮箱
        email = self.random_email()
        # 拼接url
        url = my_config.get('url', 'url') + case.url
        # 参数化注册的username, email
        case.param = case.param.replace('*username*', username)
        case.param = case.param.replace('*email*', email)
        # 将字符串参数，转换为字典
        param = eval(case.param)
        log.info(f'正在请求地址：{url}')
        # 发送请求接口
        response = http_request.request(url=url, method=case.method, data=param)
        # 获取响应内容
        result = response.json()
        # 断言预期和实际结果
        row = case.case_id + 1
        try:
            # 断言预期响应状态码与实际响应状态码
            self.assertEqual(case.expected_code, response.status_code)
            # 如果非正常注册，则需再断言响应内容
            if case.expected_code != 201:
                self.assertEqual(eval(case.expected_text), result)
            # 如果有check_sql不为空，则断言数据是否写入数据库
            if case.check_sql:
                db_result = self.pdbc.find_count(case.check_sql.replace('*username*', username))
                self.assertEqual(1, db_result)
        except AssertionError as e:
            # 将测试结果写回 Excel
            self.read_excel.write_data(row=row, column=10, value='未通过')
            log.error(e)
            log.info('[{case.title}] --> 该用例执行未通过')
            raise e
        else:
            # 将测试结果写回 Excel
            self.read_excel.write_data(row=row, column=10, value='通过')
            log.info(f'[{case.title}] --> 该用例执行通过')

    def random_username(self):
        """随机生成一个未注册的 8位 username """
        username = self.fake.user_name().ljust(6, '0')
        if self.pdbc.find_count(f"SELECT id FROM auth_user WHERE username = '{username}'"):
            phone = self.random_username()
        return username

    def random_email(self):
        """随机生成一个未注册的 email """
        email = self.fake.email()
        if self.pdbc.find_count(f"SELECT id FROM auth_user WHERE email = '{email}'"):
            phone = self.random_email()
        return email
