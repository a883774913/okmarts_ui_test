"""
地址管理模块
"""
import time

from selenium.webdriver.support.wait import WebDriverWait

from okmarts_ui_test.common.common import Common
from okmarts_ui_test.mysql.mysql import Mysql


class Address:
    def address(self,driver,Parameter):

        Mysql().drop_table(user="root", pwd="OKmarts888.,", host="18.118.13.94", db="okmarts", port=3306,
                           sql="delete from receiving_address where userid='1506910015154425856';")                         #每次运行前删除地址信息
        casename = Parameter['casename']
        mode = Parameter['mode']
        data = Parameter['data'].split('\n')
        print(data)
        assert_way = Parameter['assert_way']
        result = Parameter['result']

        driver.get('http://18.118.13.94:81/index') #打开首页
        time.sleep(1)
        driver.find_element(by='css selector',
                            value='#app > div > div.global-header > div > div.menu-content > div.menu-right.flex > div:nth-child(1)').click()  # 点击头像
        Common().login(driver,useraccount='979172251@qq.com',password='a123456')
        time.sleep(1)
        driver.find_element(by='css selector',value='#app > div > div.global-header > div > div.menu-content > div.menu-right.flex > div:nth-child(1)').click() #点击头像
        time.sleep(1)
        driver.find_element(by='css selector',value='#app > div > div.my-info > div.info.flex > div.info-right > div:nth-child(4)').click() #点击地址进入地址管理页面
        time.sleep(1)
        if casename == '点击Manage recipient information跳转到地址管理页面成功':
            text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                       value=f"{assert_way.split('=', 1)[1]}").text
            print(text)
            assert text == result
        else:
            driver.find_element(by='css selector',value='#app > div > div.ui-container > div.content.flex.space-between > div > div.address-list.margin-bottom > div > a').click()  #点击新增地址
            time.sleep(1)
            driver.find_element(by='id',value='coordinated_firstname').send_keys('first_name')
            driver.find_element(by='id',value='coordinated_lastname').send_keys('last_name')
            driver.find_element(by='id',value='coordinated_contactnumber').send_keys(13688888888)
            driver.find_element(by='id',value='coordinated_area1').send_keys('省')
            driver.find_element(by='id',value='coordinated_area2').send_keys('city')
            driver.find_element(by='id',value='coordinated_area3').send_keys('CN')
            driver.find_element(by='id',value='coordinated_postalCode').send_keys('code')
            driver.find_element(by='xpath',value='coordinated_addressLine').send_keys('Address details')
            driver.find_element(by='class name',value='atn-btn-orange.address_submit.ant-btn.ant-btn-primary').click()  #点击确定
            WebDriverWait(driver, 30, 0.2).until(lambda x: x.find_element_by_xpath(
                "/html/body/div[2]/span"))  # 显示等待
            text = driver.find_element(by='xpath',value='/html/body/div[2]/span').text
            print(text)
            assert text == 'success'


