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
import decimal


@ddt
class RechargeAndWithdrawTestCase(unittest.TestCase):
    """充值和取现测试用例类"""
    @classmethod
    def setUpClass(cls) -> None:
        cls.pdbc = PDBC()
        cls.http_session = HttpSession()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.pdbc.close()
        cls.http_session.close()

    read_excel = ReadExcel(os.path.join(DATA_DIR, 'cases.xlsx'), 'recharge')
    # 通过对象获取数据
    cases = read_excel.read_data_obj()

    @data(*cases)
    def test_recharge_case(self, case):
        """充值测试用例方法"""
        # 准备参数
        if case.check_sql:
            # 充值之前余额 decimal类型
            start_money = self.pdbc.find_one(data_replace(case.check_sql))[0]
        url = my_config.get('url', 'url') + case.url
        # 发生请求接口
        log.info(f'正在请求地址：{url}')
        # data_replace() 参数动态化处理
        response = self.http_session.request(url, case.method, eval(data_replace(case.param)))
        # 获取请求结果
        result = response.json()
        # 断言
        try:
            self.assertEqual(case.expected_code, eval(result['code']))
            # 数据库校验
            if case.check_sql:
                # 充值之后余额 decimal类型
                end_money = self.pdbc.find_one(data_replace(case.check_sql))[0]
                # decimal.Decimal() 将数值字符串转化成decimal类型
                if case.interface == 'recharge':
                    self.assertEqual(end_money-start_money, decimal.Decimal(eval(case.param)['amount']))
                elif case.interface == 'withdraw':
                    self.assertEqual(start_money - end_money, decimal.Decimal(eval(case.param)['amount']))
        except AssertionError as e:
            # 将执行结果写入Excel
            self.read_excel.write_data(case.case_id + 1, 9, '未通过')
            log.exception(e)
            log.info(f'[{case.title}] --> 该用例执行未通过')
            raise e
        else:
            self.read_excel.write_data(case.case_id + 1, 9, '通过')
            log.info(f'[{case.title}] --> 该用例执行通过')
            pass


# @ddt
# class WithdrawTestCase(unittest.TestCase):
#     """取现测试用例类"""
#     read_excel = ReadExcel(os.path.join(DATA_DIR, 'cases.xlsx'), 'withdraw')
#     # 通过对象获取数据
#     cases = read_excel.read_data_obj()
#     # 创建http_session对象
#     http_session = HttpSession()
#
#     @data(*cases)
#     def test_withdraw_case(self, case):
#         """取现测试用例方法"""
#         # 准备参数
#         if case.check_sql:
#             # 取现之前余额 decimal类型
#             start_money = pdbc.find_one(data_replace(case.check_sql))[0]
#         url = my_config.get('url', 'url') + case.url
#         # 发生请求接口
#         log.info(f'正在请求地址：{url}')
#         # data_replace() 参数动态化处理
#         response = self.http_session.request(url, case.method, eval(data_replace(case.param)))
#         # 获取请求结果
#         result = response.json()
#         # 断言
#         try:
#             self.assertEqual(case.expected_code, eval(result['code']))
#             # 数据库校验
#             if case.check_sql:
#                 # 取现之后余额 decimal类型
#                 end_money = pdbc.find_one(data_replace(case.check_sql))[0]
#                 # decimal.Decimal() 将数值字符串转化成decimal类型
#                 self.assertEqual(start_money-end_money, decimal.Decimal(eval(case.param)['amount']))
#         except AssertionError as e:
#             # 将执行结果写入Excel
#             self.read_excel.write_data(case.case_id + 1, 9, '未通过')
#             log.exception(e)
#             log.info(f'[{case.title}] --> 该用例执行未通过')
#             raise e
#         else:
#             self.read_excel.write_data(case.case_id + 1, 9, '通过')
#             log.info(f'[{case.title}] --> 该用例执行通过')
#             pass