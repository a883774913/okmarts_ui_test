"""
广告位
"""
import time

from selenium.webdriver.support.wait import WebDriverWait

from okmarts_ui_test.common.common import Common


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
            time.sleep(0.5)
            self.banner_mode1(driver, assert_way, result[1], number=2)
            time.sleep(0.5)
            self.banner_mode1(driver, assert_way, result[2], number=3)
        if casename == '首页广告位点击页数可以跳转到指定广告位页面':
            self.banner_mode2(driver, n=1, result=result)
            time.sleep(0.5)
            self.banner_mode2(driver, n=2, result=result)
            time.sleep(0.5)
            self.banner_mode2(driver, n=3, result=result)

        elif casename == '首页侧栏广告位正确显示':
            text = driver.find_elements(by=f"{assert_way.split('=', 1)[0]}",
                                        value=f"{assert_way.split('=', 1)[1]}")[1].is_displayed()
            print(result)
            assert text is bool(result)
        elif casename == '点击侧栏广告位页面正确跳转':
            driver.find_elements(by='class name', value="part-right")[1].click()  # 点击首页侧栏广告位
            time.sleep(2)
            toHandle = driver.window_handles
            driver.switch_to.window(toHandle[1])
            text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}", value=f"{assert_way.split('=', 1)[1]}").text
            print(text)
            assert text == result
            driver.close()  # 关闭页面
            driver.switch_to.window(toHandle[0])
        elif casename == 'Category recommendation 广告位正确显示':
            Common().huadong(driver, by='class name', value='item-left')
            time.sleep(2)
            self.banner_mode3(driver, 0, assert_way, result)
            time.sleep(0.5)
            self.banner_mode3(driver, 1, assert_way, result)
            time.sleep(0.5)
            self.banner_mode3(driver, 2, assert_way, result)
        elif casename == '点击Category recommendation 广告位正确跳转':
            Common().huadong(driver, by='class name', value='item-left')
            result = eval(result)
            self.banner_mode4(driver, 1, assert_way, result[0])
            time.sleep(0.5)
            self.banner_mode4(driver, 2, assert_way, result[1])
            time.sleep(0.5)
            self.banner_mode4(driver, 3, assert_way, result[2])

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
        self.banner_mode5(driver, assert_way, result)

    def banner_mode2(self, driver, n, result):
        """
        点击首页banner中的切换广告按钮，获取当前展示广告的Class 值
        :param driver:
        :param n:
        :param result:
        :return:
        """
        driver.find_element(by='xpath', value=f'//*[@id="app"]/div/div[2]/div[1]/div/ul/li[{n}]/button').click()  # 点击第一页
        info = driver.find_element(by='xpath', value=f'//*[@id="app"]/div/div[2]/div[1]/div/div/div/div[{n + 1}]').get_attribute("class")
        print(info)
        assert info == result

    def banner_mode3(self, driver, n, assert_way, result):
        """
        判断类别推荐广告位是否存在
        :param driver: 驱动
        :param n: 第几个
        :return:
        """
        text1 = driver.find_elements(by=f"{assert_way.split('=', 1)[0]}",
                                     value=f"{assert_way.split('=', 1)[1]}")[n].is_displayed()
        print(text1)
        print(result)
        assert text1 == bool(result)

    def banner_mode4(self, driver, n, assert_way, result):
        time.sleep(2)
        driver.find_elements(by='class name', value='item-left')[n - 1].click()  # 点击第一个广告位
        self.banner_mode5(driver, assert_way, result)

    def banner_mode5(self, driver, assert_way, result):
        """
        用于mode1 mode4重复代码使用
        :param driver:
        :param assert_way:
        :param result:
        :return:
        """
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
