import os
import time
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import Chrome
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from common.filedir import SCREENSHOTDIR

class WebdriverOperator(object):
    def __init__(self, driver: Chrome):
        self.driver = driver

    def get_screenshot_as_file(self):
        """
        截屏保存
        :return: 返回路径
        """
        pic_name = str.split(str(time.time()), '.')[0] + str.split(str(time.time()), '.')[1] + '.png'
        screent_path = os.path.join(SCREENSHOTDIR, pic_name)
        self.driver.get_screenshot_as_file(screent_path)
        return screent_path

    def web_implicitly_wait(self, **kwargs):
        """
        隐式等待
        :param kwargs:
        :return:
        """
        try:
            s = kwargs['time']
        except KeyError:
            s = 10

        try:
            self.driver.implicitly_wait(s)
        except NoSuchElementException:
            return False, '隐式等待设置失败'
        return True, '隐式等待设置成功'

    def web_element_wait(self, **kwargs):
        """
        等待元素可见
        :param kwargs:
        :return:
        """
        try:
            type = kwargs['type']
            locator = kwargs['locator']
        except KeyError:
            return False, '未传需要等待元素的定位参数'

        try:
            s = kwargs['time']
            if s is None:
                s = 30
        except KeyError:
            s = 30

        try:
            if type == 'id':
                WebDriverWait(self.driver, s, 0.5).until(EC.visibility_of_element_located((By.ID, locator)))
            elif type == 'name':
                WebDriverWait(self.driver, s, 0.5).until(EC.visibility_of_element_located((By.NAME, locator)))
            elif type == 'class':
                WebDriverWait(self.driver, s, 0.5).until(EC.visibility_of_element_located((By.CLASS_NAME, locator)))
            elif type == 'xpath':
                WebDriverWait(self.driver, s, 0.5).until(EC.visibility_of_element_located((By.XPATH, locator)))
            elif type == 'css':
                WebDriverWait(self.driver, s, 0.5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, locator)))
            else:
                return False, '不能识别元素元素[' + type + ']'
        except TimeoutException:
            screenshot_path = self.get_screenshot_as_file()
            return False, '元素[' + locator + ']等待出现失败，已截图[' + screenshot_path + '].'
        return True, '元素[' + locator + ']等待出现成功'

    def element_input(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        try:
            type = kwargs['type']
            locator = kwargs['locator']
            text = kwargs['input']
        except KeyError:
            return False, '缺少参数'

        try:
            index = kwargs['index']
        except KeyError:
            index = 0

        isOk, result = self.element_find(type, locator, index)
        if not isOk:
            return isOk, result
        elem = result

        try:
            elem.send_keys(text)
        except Exception:
            screenshot_path = self.get_screenshot_as_file()
            return False, '元素[' + locator + ']输入[' + text + ']失败，已截图[' + screenshot_path + '].'
        return True, '元素[' + locator + ']输入[' + text + ']成功'

    def element_find(self, type, locator, index=None):
        """
        定位元素
        :param type:
        :param locator:
        :param index:
        :return:
        """
        time.sleep(1)
        if index is None:
            index = 0
        type = str.lower(type)
        try:
            if type == 'id':
                elem = self.driver.find_elements(by=By.ID, value=locator)[index]
            elif type == 'name':
                elem = self.driver.find_elements(by=By.NAME, value=locator)[index]
            elif type == 'class':
                elem = self.driver.find_elements(by=By.CLASS_NAME, value=locator)[index]
            elif type == 'xpath':
                elem = self.driver.find_elements(by=By.XPATH, value=locator)[index]
            elif type == 'css':
                elem = self.driver.find_elements(by=By.CSS_SELECTOR, value=locator)[index]
            else:
                return False, '不能识别元素元素[' + type + ']'
        except Exception as e:
            screenshot_path = self.get_screenshot_as_file()
            return False, '获取元素[' + type + ']失败，已截图[' + screenshot_path + '].'
        return True, elem

    def element_click(self, **kwargs):
        """
        点击元素
        :param kwargs:
        :return:
        """
        try:
            type = kwargs['type']
            locator = kwargs['locator']
        except KeyError:
            return False, '缺少参数'

        try:
            index = kwargs['index']
        except KeyError:
            index = 0

        isOk, result = self.element_find(type, locator, index)
        if not isOk:
            return isOk, result
        elem = result

        try:
            elem.click()
        except Exception:
            screenshot_path = self.get_screenshot_as_file()
            return False, '元素[' + locator + ']点击失败，已截图[' + screenshot_path + '].'
        return True, '元素[' + locator + ']点击成功'