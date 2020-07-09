import openpyxl

class CaseData(object):
    def __init__(self, zip_obj):
        for i in zip_obj:
            # 通过反射机制为对象设置属性值
            setattr(self, i[0], i[1])

class ReadExcel(object):
    def __init__(self, file, sheet_name):
        """

        :param file: 文件路径及文件名
        :param sheet_name:
        """
        self.file = file
        self.sheet_name = sheet_name

    def open(self):
        """
        打开Excel文档指定sheet
        :return:
        """
        self.workbook = openpyxl.load_workbook(self.file)
        self.sheet = self.workbook[self.sheet_name]

    def read_data(self):
        """
        直接读取Excel表数据
        :return: 返回list数据列表
        """
        self.open()
        # 获取sheet所有数据
        rows = list(self.sheet.rows)
        # 获取表头数据
        title = [row.value for row in rows[0]]
        # 获取其他行数据
        cases = []
        for row in rows[1:]:
            data = [r.value for r in row]
            # title与每行数据打包并转化为字典类型
            case = dict(zip(title, data))
            cases.append(case)
        return cases

    def read_data_obj(self):
        """
        将表头与每行数据封装成一个对象属性
        :return: 返回表头每行与每行数据作为一个对象的对象列表
        """
        self.open()
        # 创建一个空列表，存放所有测试用例
        cases = []
        # 读取表单中的数据
        rows = list(self.sheet.rows)
        # 读取表头
        title = [row.value for row in rows[0]]
        # 读取表单其余数据
        for row in rows[1:]:
            # 获取表单其余数据
            data = [r.value for r in row]
            # 将表头与表单其余列数据进行打包得到zip对象
            zip_obj = zip(title, data)
            case_data = CaseData(zip_obj)
            # 将CaseData对象存入cases列表
            cases.append(case_data)
        return cases

    def write_data(self, row, column, value):
        """
        写入数据
        :param row:
        :param column:
        :param value:
        :return:
        """
        self.open()
        self.sheet.cell(row=row, column=column, value=value)
        self.workbook.save(self.file)
# if __name__ == '__main__':
#     read_excel = ReadExcel('../study_excel/cases.xlsx', 'login')
#     # cases = read_excel.read_data()
#     cases = read_excel.read_data_obj()
#     for i in cases:
#         print(i.case_id)
#         print(i.data)
#         print(i.expect)
#         print(i.method)
#     # print(cases)
