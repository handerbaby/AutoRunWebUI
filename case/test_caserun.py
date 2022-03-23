import unittest
from common.factory import Factory
from common.log import Handlogging
from ddt import ddt, data

@ddt
class Test_caserun(unittest.TestCase):
    factory = Factory()
    isOk, excu_cases = factory.init_excute_case()


    @data(*excu_cases)
    def test_run(self, cases_dict):
        mylog = Handlogging().emplorlog()
        for key, cases in cases_dict.items():
            mylog.info('\n----------用例【%s】开始----------' % cases[0].get('sheet'))
            print('\n')
            for case in cases:
                isOk, result = self.factory.execute_keyword(**case)
                if isOk:
                    print(result)
                    mylog.info(result)
                else:
                    mylog.error(result)
                    raise Exception(result)
            mylog.info('\n----------用例【%s】结束----------' % cases[0].get('sheet'))
