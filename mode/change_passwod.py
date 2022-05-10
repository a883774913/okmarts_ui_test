"""修改密码模块"""
import random
import time

from selenium.webdriver import Keys
from selenium.webdriver.support.wait import WebDriverWait

from okmarts_ui_test.common.common import Common
from okmarts_ui_test.mode.get_code import Get_Code


class Change_Password:

    def change_password(self, driver, Parameter):
        casename = Parameter['casename']
        data = Parameter['data']
        assert_way = Parameter['assert_way']
        result = Parameter['result']
        driver.get('http://18.118.13.94:81/index')  # 打开首页
        WebDriverWait(driver, 20, 0.2).until(lambda x: x.find_element(by='xpath', value='//*[@id="app"]/div/div[1]/div/div[2]/div[3]/div[3]/span[1]'))
        time.sleep(1)
        useraccount = random.choice(['a979172251@163.com', 'a9791722511@126.com','a9791722511@163.com','a97917225111@163.com','a979172251@126.com'])
        print(useraccount)
        self.login_to_change_password(driver, useraccount, 'a123456')
        if casename == '点击change password页面跳转成功':
            print('通道1')
            text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}", value=f"{assert_way.split('=', 1)[1]}").text
            print(text)
            assert text == result
        elif casename == '不输入密码，验证码修改密码失败':
            print('通道2')
            text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}", value=f"{assert_way.split('=', 1)[1]}").get_attribute('disabled')
            print(text)
            assert text == result
        elif casename == '输入5位密码，修改密码失败':
            print('通道3')
            new_password = data.split('=')[-1]
            print(f'修改新密码为{new_password}')
            driver.find_element(by='id', value='horizontal_login_newPassword').send_keys(new_password)  # 输入新密码
            driver.find_element(by='css selector', value='#app > div > div.login-form-wrap > div.login-form.margin-bottom > form > div:nth-child(1) > div > div > span '
                                                         '> div > div:nth-child(2) > a').click()  # 点击发送验证码
            time.sleep(10)  # 等待10S
            print(useraccount)
            code = Get_Code().wangyi(useraccount, 'Qwe3541118', 'hydraulic', no=1)
            driver.find_element(by='id', value='horizontal_login_code').send_keys(Keys.CONTROL, 'a')  # 清空验证码栏
            driver.find_element(by='id', value='horizontal_login_code').send_keys(code)  # 输入验证码
            driver.find_element(by='class name', value='atn-btn-orange.ant-btn.ant-btn-lg.ant-btn-block').click()  # 点击提交
            text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}", value=f"{assert_way.split('=', 1)[1]}").text
            print(text)
            assert text == result
        elif casename == '输入错误验证码密码修改失败':
            print('通道4')
            new_password = data.split('=')[-1]
            print(f'修改新密码为{new_password}')
            driver.find_element(by='id', value='horizontal_login_newPassword').send_keys(new_password)  # 输入新密码
            driver.find_element(by='id', value='horizontal_login_code').send_keys(Keys.CONTROL, 'a')  # 输入验证码
            driver.find_element(by='id', value='horizontal_login_code').send_keys('000000')  # 输入验证码
            driver.find_element(by='class name', value='atn-btn-orange.ant-btn.ant-btn-lg.ant-btn-block').click()  # 点击提交
            WebDriverWait(driver, 10, 0.2).until(lambda x: x.find_element(by=f"{assert_way.split('=', 1)[0]}", value=f"{assert_way.split('=', 1)[1]}"))
            text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}", value=f"{assert_way.split('=', 1)[1]}").text
            print(text)
            assert text == result
        elif casename == '不输入验证码修改密码失败':
            driver.find_element(by='id',value='horizontal_login_newPassword').send_keys('a123456')
            text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}", value=f"{assert_way.split('=', 1)[1]}").get_attribute('disabled')
            print(text)
            assert text == result
        else:
            print('通道0')
            new_password = data.split('=')[-1]
            code = self.mode1(driver, new_password, useraccount)
            WebDriverWait(driver, 15, 0.2).until(lambda x: x.find_element(by='class name', value='r_text'))  # 等待首页显示
            driver.find_element(by='class name', value='r_text').click()    #点击头像
            time.sleep(2)
            Common().login(driver, useraccount, password=new_password)  # 登录操作
            time.sleep(2)
            text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}", value=f"{assert_way.split('=', 1)[1]}").text
            print(text)
            assert text != result          #使用修改后的账户可以登录成功则说明修改成功
            Common().Restore_environment(driver)  # 退出登录环境
            Common().change_password(driver, useraccount, 'a123456',code)    #还原密码
        Common().Restore_environment(driver)  # 退出登录环境

    def mode1(self, driver, new_password, useraccount):
        """
        修改密码页面 输入密码-发送验证码-输入验证码-提交
        :param driver:
        :param new_password:
        :param useraccount:
        :return:
        """
        print(f'修改新密码为{new_password}')
        driver.find_element(by='id', value='horizontal_login_newPassword').send_keys(new_password)  # 输入新密码
        driver.find_element(by='css selector', value='#app > div > div.login-form-wrap > div.login-form.margin-bottom > form > div:nth-child(1) > div > div > span '
                                                     '> div > div:nth-child(2) > a').click()  # 点击发送验证码
        n = 0
        while n < 3:
            WebDriverWait(driver,10,0.2).until(lambda x:x.find_element(by='css selector',value='body > div.ant-message > span > div > div > div > span'))
            info = driver.find_element(by='css selector', value='body > div.ant-message > span > div > div > div > span').text
            print(f'发送验证码信息为{info}')
            if info == 'Verification code has been sent. Please do not click again!':  # 验证码发送频繁
                time.sleep(61)
                driver.find_element(by='css selector',
                                    value='#app > div > div.login-form-wrap > div.login-form.margin-bottom > form > div:nth-child(1) > div > div > span '
                                          '> div > div:nth-child(2) > a').click()  # 再次点击验证码
            else:
                time.sleep(10)  # 等待10S
                print(useraccount)
                code = Get_Code().wangyi(useraccount, 'Qwe3541118', 'hydraulic', no=1)
                driver.find_element(by='id', value='horizontal_login_code').send_keys(Keys.CONTROL, 'a')  # 输入验证码
                driver.find_element(by='id', value='horizontal_login_code').send_keys(code)  # 输入验证码
                driver.find_element(by='class name', value='atn-btn-orange.ant-btn.ant-btn-lg.ant-btn-block').click()  # 点击提交
                WebDriverWait(driver, 10, 0.2).until(lambda x: x.find_element(by='xpath', value='/html/body/div[2]/span/div/div/div/span'))  # 显示等待
                text = driver.find_element(by='xpath', value='/html/body/div[2]/span/div/div/div/span').text  # 获取提示文本
                time.sleep(5)
                print(f'修改密码验证信息为{text}')
                if text == 'Verification code error':  # 如果验证码错误
                    driver.find_element(by='css selector',
                                        value='#app > div > div.login-form-wrap > div.login-form.margin-bottom > form > div:nth-child(1) > div > div > span '
                                              '> div > div:nth-child(2) > a').click()  # 再次点击验证码
                elif text == 'password update success':
                    break
        return code

    def login_to_change_password(self, driver, useraccount, password):
        """
        登录-点击头巾-点击修改密码
        :param driver: 驱动
        :param useraccount: 用户名
        :param password: okmars商城 密码
        :return:
        """
        Common().is_login(driver, useraccount, password)  # 登录
        time.sleep(2)
        driver.find_element(by='class name', value='r_text').click()  # 点击头像
        time.sleep(2)
        driver.find_element(by='class name', value='my_top_info').click()  # 点击第一个,进入密码修改页面
        time.sleep(2)
