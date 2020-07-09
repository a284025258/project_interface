import unittest
from lib.ddt import ddt, data
from common.read_excel import ReadExcel
from common.constant import DATA_DIR
from common.config import my_config
from common.my_logger import log
from common.http_requests import HttpSession
import os
from common.pdbc import PDBC
from common.text_replace import data_replace, ConText


@ddt
class AuditTestCase(unittest.TestCase):
    """审核测试用例类"""
    @classmethod
    def setUpClass(cls) -> None:
        cls.pdbc = PDBC()
        cls.http_session = HttpSession()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.pdbc.close()
        cls.http_session.close()
    read_excel = ReadExcel(os.path.join(DATA_DIR, 'cases.xlsx'), 'audit')
    # 通过对象获取数据
    cases = read_excel.read_data_obj()

    @data(*cases)
    def test_audit_case(self, case):
        """审核测试用例方法"""
        # 准备参数
        url = my_config.get('url', 'url') + case.url
        # 发生请求接口
        log.info(f'正在请求地址：{url}')
        # data_replace() 参数动态化处理
        response = self.http_session.request(url, case.method, eval(data_replace(case.param)))
        # 获取请求结果
        result = response.json()
        # 判断是否执行为加标测试用例
        if case.interface == 'add':
            # 加标，获取该条数据在loan表中的id
            loan_id = self.pdbc.find_one(data_replace("SELECT Max(Id) FROM loan WHERE MemberID= '#memberId#'"))
            # 将加标的loan表id，保存为临时变量
            setattr(ConText, 'loan_id', loan_id[0])
        # 断言
        try:
            self.assertEqual(case.expected_code, eval(result['code']))
            # 数据库校验
            if case.check_sql:
                # 获取审核状态
                status = self.pdbc.find_one(data_replace(case.check_sql))[0]
                self.assertEqual(status, eval(case.param)['status'])
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
