from common.config import Config
from common.case import Case
from base.factory.browseroperator import BrowserOperator
from base.factory.webdriveroperator import WebdriverOperator

class Factory(object):
    def __init__(self):
        self.config = Config()
        self.config_fun = dict(self.config.items('Function'))
        # 浏览器操作对象
        self.bowser_opr = BrowserOperator()
        # 网页操作对象
        self.webdriver_opr = None

    def init_webdriver_opr(self, driver):
        self.webdriver_opr = WebdriverOperator(driver)

    def init_common_case(self, cases):
        """

        :param cases:
        :return:
        """
        cases_len = len(cases)
        index = 0
        for case in cases:
            if case['keyword'] == '调用用例':
                xlsx = Case()
                try:
                    case_name = case['locator']
                except KeyError:
                    return False, '调用用例没有提供用例名，请检查用例'
                isOk, result = xlsx.get_common_case(case_name)
                if isOk and type([]) == type(result):
                    isOk, result_1 = self.init_common_case(result)  # 递归
                elif not isOk:
                    return isOk, result
                list_rows = result[case_name]
                cases[index: index + 1] = list_rows
            index += 1
        if cases_len == index:
            return False, ''
        return True, cases

    def init_excute_case(self):
        print('---------初始化用例----------')
        xlsx = Case()
        isOk, result = xlsx.get_all_case()
        if not isOk:
            print(result)
            print('---------结束执行----------')
            exit()
        all_case = result
        excu_cases = []
        for case_dict in all_case:
            for key, cases in case_dict.items():
                isOk, result = self.init_common_case(cases)
                if isOk:
                    case_dict[key] = result
                else:
                    case_dict[key] = cases
                excu_cases.append(case_dict)
                print('---------调用示例完成----------')
        return True, excu_cases

    def get_base_function(self, function_name):
        try:
            function = getattr(self.bowser_opr, function_name)
        except Exception:
            try:
                function = getattr(self.webdriver_opr, function_name)
            except Exception:
                return False, '未找到注册方法[' + function_name + ']所对应的执行函数，请检查配置文件'
        return True, function

    def execute_keyword(self, **kwargs):
        """
        工厂函数，用例执行方法的入口
        :param kwargs:
        :return:
        """
        try:
            keyword = kwargs['keyword']
            if keyword is None:
                return False, '没有keyword，请检查用例'
        except KeyError:
            return False, '没有keyword，请检查用例'
        _isbrowser = False
        try:
            function_name = self.config_fun[keyword]
        except KeyError:
            return False, '方法key[' + keyword + ']未注册，请检查用例'

        # 获取基础类方法
        isOk, result = self.get_base_function(function_name)
        if isOk:
            function = result
        else:
            return isOk, result

        # 执行技术方法，如打开网页、点击、定位、隐式等待
        isOk, result = function(**kwargs)

        # 如果是打开网页，是浏览器初始化，需要将返回值传递给另一个基础类
        if '打开网页' == keyword and isOk:
            url = kwargs['locator']
            self.init_webdriver_opr(result)
            return isOk, '网页[' + url + ']打开成功'
        return isOk, result