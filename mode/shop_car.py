"""
购物车模块
"""
import time

from selenium.webdriver.support.wait import WebDriverWait

from okmarts_ui_test.common.common import Common


class Shop_Car:

    def shop_car(self,driver,Parameter):
        casename = Parameter['casename']
        data = Parameter['data']
        print(data)
        assert_way = Parameter['assert_way']
        result = Parameter['result']

        driver.get('http://18.118.13.94:81/index')  # 打开首页
        WebDriverWait(driver,20,0.2).until(lambda x:x.find_element(by='xpath',value='//*[@id="app"]/div/div[1]/div/div[2]/div[3]/div[3]/span[1]'))
        time.sleep(1)

        Common().is_login(driver,useraccount='979172251@qq.com',password='a123456')
        time.sleep(2)
        if casename == '首页显示购物车图标，点击购物车，页面跳转到购物车页面':
            info = driver.find_element(by='xpath',value='//*[@id="app"]/div/div[1]/div/div[2]/div[3]/div[3]/span[1]').text
            print(info)
            goods_number = driver.find_element(by='xpath',value='//*[@id="app"]/div/div/div[1]/div/div[2]/div[3]/div[3]/span[2]').text
            print(goods_number)
            assert info == 'Cart'
            driver.find_element(by='xpath',value='//*[@id="app"]/div/div[1]/div/div[2]/div[3]/div[3]/span[1]').click()

