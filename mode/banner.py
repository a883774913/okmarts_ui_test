"""
广告位
"""
import time

from selenium.webdriver.support.wait import WebDriverWait


class Banner:
    def banner(self, driver, Parameter):
        casename = Parameter['casename']
        data = Parameter['data']
        print(data)
        assert_way = Parameter['assert_way']
        result = Parameter['result']

        driver.get('http://18.118.13.94:81/index')  # 打开首页
        WebDriverWait(driver, 20, 0.2).until(lambda x: x.find_element(by='xpath', value='//*[@id="app"]/div/div[1]/div/div[2]/div[3]/div[3]/span[1]'))
        time.sleep(1)
        if casename == '点击广告位图片页面跳转到相关页面':
            result = eval(result)
            print(result)
            self.banner_mode1(driver, assert_way, result[0], number=1)
            self.banner_mode1(driver, assert_way, result[1], number=2)
            self.banner_mode1(driver, assert_way, result[2], number=3)
        if casename == '首页广告位点击页数可以跳转到指定广告位页面':

            driver.find_element(by='xpath', value=f'//*[@id="app"]/div/div[2]/div[1]/div/ul/li[1]/button').click()  # 点击第一页
            info = driver.find_element(by='xpath',value='//*[@id="app"]/div/div[2]/div[1]/div/div/div/div[2]').get_attribute("class")
            print(info)
            assert info == 'slick-slide slick-active slick-current'

            driver.find_element(by='xpath', value=f'//*[@id="app"]/div/div[2]/div[1]/div/ul/li[2]/button').click()  # 点击第2页
            info2 = driver.find_element(by='xpath', value='//*[@id="app"]/div/div[2]/div[1]/div/div/div/div[3]').get_attribute("class")
            assert info2 == 'slick-slide slick-active slick-current'

            driver.find_element(by='xpath', value=f'//*[@id="app"]/div/div[2]/div[1]/div/ul/li[3]/button').click()  # 点击第3页
            info3 = driver.find_element(by='xpath', value='//*[@id="app"]/div/div[2]/div[1]/div/div/div/div[4]').get_attribute("class")
            assert info3 == 'slick-slide slick-active slick-current'


    def banner_mode1(self, driver, assert_way, result, number):
        """
        点击相应导航栏页数，点击广告，获取页面商品名称进行断言
        :param driver:  驱动
        :param assert_way: 断言方式
        :param result: 断言结果
        :param number: 第几个广告
        :return:
        """
        driver.find_element(by='xpath', value=f'//*[@id="app"]/div/div[2]/div[1]/div/ul/li[{number}]/button').click()  # 点击第一页
        time.sleep(0.5)
        driver.find_element(by='css selector', value='#app > div > div.ui-container > div.banner.margin-bottom-sm.ant-carousel > div > div > div > '
                                                     'div.slick-slide.slick-active.slick-current > div > a').click()
        time.sleep(2)
        toHandle = driver.window_handles
        print(toHandle)
        driver.switch_to.window(toHandle[1])
        time.sleep(2)
        text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                   value=f"{assert_way.split('=', 1)[1]}").text
        print(text)
        assert text == result
        driver.close()  # 关闭页面
        driver.switch_to.window(toHandle[0])

    def banner_mode2(self,driver):
        driver.find_element(by='xpath', value=f'//*[@id="app"]/div/div[2]/div[1]/div/ul/li[1]/button').click()  # 点击第一页
        info = driver.find_element(by='xpath', value='//*[@id="app"]/div/div[2]/div[1]/div/div/div/div[2]').get_attribute("class")
        print(info)
        assert info == 'slick-slide slick-active slick-current'