import openpyxl
import os
from common.filedir import DATADIR
file = os.path.join(DATADIR, 'case.xlsx')

class Case(object):
    def __init__(self):
        self.sw = openpyxl.load_workbook(file)
        # print(self.sw)

    def open_xlsx(self, file):
        """
        打开文件
        :param file:
        :return:
        """
        self.sw = openpyxl.load_workbook(file)

    def get_all_case(self):
        """
        获取所有sheet页数据
        :return: list, 返回所有sheet页里的数据
        """
        sheet_list = []
        for sheet in self.sw:
            if 'common' != sheet.title.split('_')[0] and 'common' != sheet.title.split('-')[0] and sheet.title[0] is not '#':
                isOk, result = self.get_case(sheet)
                if isOk:
                    sheet_list.append(result)  # 得到的结果放在列表中
        if sheet_list is None:
            return False, '用例集为空'
        return True, sheet_list

    def get_case(self, sheet):
        """
        组合sheet页的数据
        :param sheet:
        :return: list, 返回组合数据
        """
        if sheet is None:
            return False, 'sheet页为空'
        datas = list(sheet.rows)
        if datas == []:
            return False, '用例[' + sheet.title + ']是空的'
        title = [i.value for i in datas[0]]
        rows = []
        sheet_dict = {}
        for i in datas[1:]:
            data = [v.value for v in i]
            row = dict(zip(title, data))
            try:
                if str(row['id'])[0] is not '#':
                    row['sheet'] = sheet.title
                    rows.append(row)
            except KeyError:
                raise e
                rows.append(row)
            sheet_dict[sheet.title] = rows
        return True, sheet_dict



    def get_common_case(self, case_name):
        """
        获取公共用例
        :param case_name:
        :return:
        """
        try:
            sheet = self.sw[case_name]
        except KeyError:
            return False, '未找到公共用例[' + case_name + ']'
        except DeprecationWarning:
            pass
        return self.get_case(sheet)

# xlsx = Case()
# # isOk, result = xlsx.get_all_case()
#
# isOk, result = xlsx.get_common_case('baidu')
# print(result)