"""
签到模块
"""
import time

from selenium.webdriver.support.wait import WebDriverWait

from okmarts_ui_test.common.common import Common


class Sign:

    def sign(self,driver,Parameter):
        casename = Parameter['casename']
        data = Parameter['data']
        print(data)
        assert_way = Parameter['assert_way']
        result = Parameter['result']

        driver.get('http://18.118.13.94:81/index')  # 打开首页
        WebDriverWait(driver, 20, 0.2).until(lambda x: x.find_element(by='xpath', value='//*[@id="app"]/div/div[1]/div/div[2]/div[3]/div[3]/span[1]'))
        time.sleep(1)
        if casename == '未登录状态签到栏显示正确':
            Common().Restore_environment(driver)
            text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                       value=f"{assert_way.split('=', 1)[1]}").text
            print(text)
            assert text == result
        elif casename == '已签到状态签到失败':

            Common().is_login(driver, useraccount='979172251@qq.com', password='a123456')
            try:
                driver.find_element(by='class name', value='atn-btn-orange.ant-btn').click()  # 点击签到
                time.sleep(1)
            except :
                pass
            time.sleep(2)
            text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                       value=f"{assert_way.split('=', 1)[1]}").text
            print(text)
            assert text == result
        else:
            useraccount,password = Common().random_account()
            print(useraccount)
            print(password)
            Common().is_login(driver,useraccount=useraccount,password=password)
            time.sleep(2)
            if casename == '页面存在签到栏正确显示':
                text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                           value=f"{assert_way.split('=', 1)[1]}").text
                print(text)
                assert text == result
            elif casename == '未签到状态签到成功':
                driver.find_element(by='class name',value='atn-btn-orange.ant-btn').click() #点击签到
                time.sleep(1)
                WebDriverWait(driver,10,0.2).until(lambda x:x.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                           value=f"{assert_way.split('=', 1)[1]}"))
                text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                           value=f"{assert_way.split('=', 1)[1]}").text
                print(text)
                assert text == result
        Common().Restore_environment(driver)

