import unittest
from lib.ddt import ddt, data
from common.read_excel import ReadExcel
from common.constant import DATA_DIR
from common.config import my_config
from common.my_logger import log
from common.http_requests import HttpSession
import os
from common.pdbc import PDBC
from common.text_replace import data_replace
from faker import Faker


@ddt
class AddProjectTestCase(unittest.TestCase):
    """添加项目测试用例类"""
    @classmethod
    def setUpClass(cls) -> None:
        cls.pdbc = PDBC()
        cls.http_session = HttpSession()
        cls.fake = Faker()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.pdbc.close()
        cls.http_session.close()

    read_excel = ReadExcel(os.path.join(DATA_DIR, 'cases.xlsx'), 'add_project')
    # 通过对象获取数据
    cases = read_excel.read_data_obj()

    @data(*cases)
    def test_add_project_case(self, case):
        """添加项目测试用例方法"""
        # 准备参数
        # 动态参数替换
        case.param.replace('*project_name*', self.fake.sentence()[:4] + '--项目')
        case.param.replace('*leader*', self.fake.name())
        case.param.replace('*tester*', self.fake.name())
        case.param.replace('*programmer*', self.fake.name())
        case.param.replace('*publish_app*', self.fake.sentence()[:4] + '--项目')
        case.param.replace('*desc*', self.fake.sentence())
        url = my_config.get('url', 'url') + case.url
        # 发生请求接口
        log.info(f'正在请求地址：{url}')
        # data_replace() 参数动态化处理 从配置文件读取 username 及 password 用于登录
        response = self.http_session.request(url, case.method, eval(data_replace(case.param)))
        # 断言
        try:
            self.assertEqual(case.expected_code, response.status_code)
        except AssertionError as e:
            # 将执行结果写入Excel
            self.read_excel.write_data(case.case_id + 1, 8, '未通过')
            print(f'预期结果：{case.expected_code}')
            print(f'实际结果：{response.status_code}')
            log.exception(e)
            log.info(f'[{case.title}] --> 该用例执行未通过')
            raise e
        else:
            self.read_excel.write_data(case.case_id + 1, 8, '通过')
            print(f'预期结果：{case.expected_code}')
            print(f'实际结果：{response.status_code}')
            log.info(f'[{case.title}] --> 该用例执行通过')
            pass
