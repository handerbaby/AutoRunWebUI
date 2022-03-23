import os
import unittest
# import HtmlTestRunner
from BeautifulReport import BeautifulReport
from common.filedir import CASEDIR, REPORTDIR, LOGDIR

class Test_run(object):
    def __init__(self):
        self.suit = unittest.TestSuite()
        self.load = unittest.TestLoader()
        self.suit.addTest(self.load.discover(CASEDIR))
        # self.runner = HtmlTestRunner.HTMLTestRunner(output=REPORTDIR, report_title='UITest', report_name='MyTest', descriptions='测试报告生成')
        self.runner = BeautifulReport(self.suit)

    def excute(self):
        # self.runner.run(self.suit)
        self.runner.report(description='测试报告', filename='report.html', log_path=REPORTDIR)

if __name__ == '__main__':
    test_run = Test_run()
    test_run.excute()