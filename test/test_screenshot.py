from base.factory.webdriveroperator import WebdriverOperator
from base.factory.browseroperator import BrowserOperator

bo = BrowserOperator()
isOk, driver = bo.open_url(locator='https://www.baidu.com')
wb = WebdriverOperator(driver)
isOk, result = wb.web_element_wait(type='xpath', locator='//*[@id="kw"]', time=0.001)
print(result)
isOk, result = wb.element_input(type='xpath', locator='//*[@id="kw"]', input='飞人', index=0)
print(result)
isOk, result = wb.element_click(type='xpath', locator='//*[@id="su"]', index=0)
print(result)