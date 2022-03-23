import time
import os
import win32gui
import win32con
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from common.config import Config
from common.filedir import FACTORYDIR
from pywinauto import application

class BrowserOperator(object):
    def __init__(self):
        self.config = Config()
        self.driver_path = os.path.join(FACTORYDIR, 'chromedriver.exe')
        self.driver_service = Service(self.driver_path)
        self.driver_type = str(self.config.get('Base', 'browser_type')).lower()

    def open_url(self, **kwargs):
        """
        打开网页
        :param kwargs:
        :return: 返回driver
        """
        try:
            url = kwargs['locator']
        except KeyError:
            return False, '没有URL参数'
        try:
            if self.driver_type == 'chrome':
                # 处理chrome弹出的info
                # chrome_options = webdriver.ChromeOptions()
                # chrome_options.add_argument('disable-infobars')
                # chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
                # self.driver = webdriver.Chrome(options=chrome_options, executable_path=self.driver_path)
                self.driver = webdriver.Chrome(service=self.driver_service)
                self.driver.maximize_window()
                self.driver.get(url)
            elif self.driver_type == 'ie':
                print('IE 浏览器')
            elif self.driver_type == 'firefox':
                print('火狐浏览器')
        except Exception as e:
            return False, e
        return True, self.driver

    def close_browser(self, **kwargs):
        """
        关闭浏览器
        :param kwargs:
        :return:
        """
        time.sleep(1)
        self.driver.quit()
        time.sleep(2)
        return True, '关闭浏览器成功'

    def upload_file(self, **kwargs):
        """
        上传文件
        :param kwargs:
        :return:
        """
        try:
            dialog_class = kwargs['type']
            file_dir = kwargs['locator']
            button_name = kwargs['index']
        except KeyError:
            return True, '没传对话框的标记或无效文件路径'

        if self.driver_type == 'chrome':
            title = '打开'
        elif self.driver_type == 'firefox':
            title = '文件上传'
        elif self.driver_type == 'ie':
            title = '选择要加载的文件'
        else:
            title = ''
        dialog = win32gui.FindWindow(dialog_class, title)
        if dialog == 0:
            return False, '传入对话框的class定位器有误'
        # 向下传递
        ComboBoxEx32 = win32gui.FindWindowEx(dialog, 0, 'ComboBoxEx32', None)  # 二级
        comboBox = win32gui.FindWindowEx(ComboBoxEx32, 2, 'ComboBox', None)  # 三级
        # 编辑按钮
        edit = win32gui.FindWindowEx(comboBox, 0, 'Edit', None)  # 四级
        # 打开按钮
        button = win32gui.FindWindowEx(dialog, 0, 'Button', button_name)  # 二级
        if button == 0:
            return False, '按钮text属性传值有误'
        # 输入文件绝对路径， 点击“打开”按钮
        win32gui.SendMessage(edit, win32con.WM_SETTEXT, None, file_dir)  # 发送文件路径
        time.sleep(1)
        win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button)  # 点击打开按钮
        return True, '文件上传成功'

# 测试代码
# bo = BrowserOperator()
# isOk, deiver = bo.open_url(locator='https://www.qq.com')
# time.sleep(5)
# deiver.find_elements(by=By.XPATH, value='//*[@id="sougouTxt"]')[0].send_keys('飞人')
# deiver.find_elements(by=By.XPATH, value='//*[@id="searchBtn"]')[0].click()
# bo.close_browser()


