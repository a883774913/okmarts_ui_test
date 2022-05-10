"""
忘记密码板块
"""
import random
import time

from selenium.webdriver.support.wait import WebDriverWait

from okmarts_ui_test.common.common import Common
from okmarts_ui_test.mode.get_code import Get_Code


class Forget_Password:


    def forget_password(self,driver,Parameter):
        casename = Parameter['casename']
        mode = Parameter['mode']
        data = Parameter['data'].split('\n')
        print(data)
        password = data[1].split('=')[-1]
        assert_way = Parameter['assert_way']
        result = Parameter['result']

        if casename in ['不输入邮箱号点击发送验证码失败','输入错误邮箱发送验证码失败']:
            userAccount = data[0].split('=')[-1]
        else :
            userAccount = random.choice(['a979172251@163.com', 'a9791722511@126.com', 'a9791722511@163.com', 'a97917225111@163.com', 'a979172251@126.com'])

        if casename in ['输入正确内容修改密码成功','不输入验证码下一步置灰','输入过期验证码点击下一步失败','输入6位字母+数字密码更改成功']:
            new_password = 'test' + f'{random.randint(11, 99)}'
        else:
            new_password = password

        print(f'new password 为 {new_password}')

        driver.get("http://18.118.13.94:81/index")
        time.sleep(1)
        Common().Restore_environment(driver)    #判断是否为登录状态
        time.sleep(1)
        driver.find_element(by='css selector', value='#app > div > div.global-header > div > div.menu-content > div.menu-right.flex > div:nth-child(1)').click()  # 点击头像
        time.sleep(1)
        driver.find_element(by='class name',value='login-form-forgot').click()      #点击忘记密码
        time.sleep(1)
        if casename == '不输入邮箱号点击发送验证码失败' or casename == '输入错误邮箱发送验证码失败':
            print('通道1')
            driver.find_element(by='id', value='horizontal_login_userName').send_keys(userAccount)  # 输入用户名
            driver.find_element(by='xpath',
                                value='//*[@id="app"]/div/div[1]/div[2]/form/div[2]/div/div/span/div/div[2]').click()  # 点击发送邮箱
            time.sleep(2)
            text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                       value=f"{assert_way.split('=', 1)[1]}").text
            print(text)
            assert text == result
        elif casename == '不输入邮箱修下一步置灰':
            print('通道2')
            text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                       value=f"{assert_way.split('=', 1)[1]}").get_attribute('disabled')
            print(text)
            print(type(text))
            print(result)
            print(type(result))
            assert text == result
        elif casename == '不输入验证码下一步置灰' :
            print('通道3')
            driver.find_element(by='id', value='horizontal_login_userName').send_keys(userAccount)  # 输入用户名
            driver.find_element(by='id', value='horizontal_login_newPassword').send_keys(new_password)  # 输入新密码
            text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                       value=f"{assert_way.split('=', 1)[1]}").get_attribute('disabled')
            print(text)
            print(type(text))
            print(result)
            print(type(result))
            assert text == result
        elif casename == '输入过期验证码点击下一步失败' :
            print('通道4')
            driver.find_element(by='id', value='horizontal_login_userName').send_keys(userAccount)  # 输入用户名
            driver.find_element(by='xpath',
                                value='//*[@id="app"]/div/div[1]/div[2]/form/div[2]/div/div/span/div/div[2]').click()  # 点击发送邮箱
            WebDriverWait(driver, 30, 0.2).until(lambda x: x.find_element_by_css_selector(
                "body > div.ant-message > span > div > div > div > span"))  # 显示等待
            time.sleep(60)
            code = Get_Code().wangyi(username=userAccount, password='Qwe3541118', name='hydraulic', no=1)  # 获取验证码
            driver.find_element(by='id', value='horizontal_login_code').send_keys(code[0])  # 输入验证码
            driver.find_element(by='id', value='horizontal_login_newPassword').send_keys(new_password)  # 输入新密码
            driver.find_element(by='class name',
                                value='atn-btn-orange.ant-btn.ant-btn-lg.ant-btn-block').click()  # 点击Confirm the changes
            WebDriverWait(driver, 30, 0.2).until(lambda x: x.find_element_by_xpath(
                "/html/body/div[2]/span/div/div/div/span"))  # 显示等待
            text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}", value=f"{assert_way.split('=', 1)[1]}").text
            print(text)
            assert text != result
        elif casename in ['输入正确内容修改密码成功','输入6位字母+数字密码更改成功','输入7位特殊字符密码修改成功','输入16位字母+数字更改成功','输入7位纯数字修改成功','输入7位英文小写密码修改成功','输入7位英文大写密码修改成功']:
            print('通道5')
            code = self.mode1(driver,userAccount,new_password)
            erro = 0
            while True:
                WebDriverWait(driver, 10, 0.1).until(
                    lambda x: x.find_element(by='css selector', value='body > div.ant-message > span > div > div > div > span'))  # 等待提示
                info = driver.find_element(by='css selector', value='body > div.ant-message > span > div > div > div > span').text
                print(f'提交后提示信息为{info}')
                if info == 'password update success':
                    print('修改成功等待跳转...')
                    WebDriverWait(driver, 20, 0.2).until(lambda x: x.find_element(by='css selector',
                                                                                  value='#app > div > div.global-header > div > div.menu-content > div.menu-right.flex > div:nth-child(1)'))  # 等待
                    break
                elif info == 'Verification code error':
                    erro += 1       #计算错误的次数
                    print(f'验证码错误，重新获取中，第{erro}次尝试中...')
                    if erro >= 3:
                        print(f'错误次数过多！！停止该轮测试')
                        assert False
                    else:
                        print('验证码错误,再次获取...')
                        driver.find_element(by='xpath', value='//*[@id="app"]/div/div[1]/div[2]/form/div[2]/div/div/span/div/div[2]').click()  # 点击发送邮箱
                        time.sleep(3)
                        code = Get_Code().wangyi(username=userAccount, password='Qwe3541118', name='hydraulic', no=1)  # 重新获取验证码
                        driver.find_element(by='id', value='horizontal_login_code').clear()  # 清除验证码
                        time.sleep(0.45)
                        driver.find_element(by='id', value='horizontal_login_code').send_keys(code[0])  # 输入验证码
                        driver.find_element(by='class name',
                                            value='atn-btn-orange.ant-btn.ant-btn-lg.ant-btn-block').click()  # 点击Confirm the changes   提交
            driver.find_element(by='css selector',
                            value='#app > div > div.global-header > div > div.menu-content > div.menu-right.flex > div:nth-child(1)').click()  # 点击按钮进入个人中心  #点击头像进行登录

            time.sleep(2)
            Common().login(driver,userAccount,password=new_password)     #登录操作
            time.sleep(2)
            text = driver.find_element(by=f"{assert_way.split('=',1)[0]}",value=f"{assert_way.split('=',1)[1]}").text
            print(text)
            assert text != result
            Common().Restore_environment(driver)
            Common().change_password(driver,userAccount,'a123456',code[0])
        else:
            print('通道0')
            code = self.mode1(driver,userAccount,new_password)
            time.sleep(2)
            text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}", value=f"{assert_way.split('=', 1)[1]}").text
            print(text)
            assert text == result
            Common().Restore_environment(driver)
            Common().change_password(driver,userAccount,'a123456',code[0])

    def mode1(self,driver,userAccount,new_password):
        """
        输入用户名-点击发送邮件-获取验证码-输入验证码-输入新密码-点击明文查看密码-点击提交
        :param driver: 驱动
        :param userAccount: 忘记密码的账户
        :param new_password: 新密码
        :return: code
        """
        driver.find_element(by='id', value='horizontal_login_userName').send_keys(userAccount)  # 输入用户名
        driver.find_element(by='xpath',
                            value='//*[@id="app"]/div/div[1]/div[2]/form/div[2]/div/div/span/div/div[2]').click()  # 点击发送邮箱
        WebDriverWait(driver, 30, 0.2).until(lambda x: x.find_element_by_css_selector(
            "body > div.ant-message > span > div > div > div > span"))  # 显示等待
        code_info = driver.find_element(by='css selector',
                                        value='body > div.ant-message > span > div > div > div > span').text
        print(f'发送验证码后提示信息为{code_info}')
        if code_info == 'Verification code has been sent. Please do not click again!':
            time.sleep(60)
            print('发送失败，等待一分钟再次发送')
            driver.find_element(by='xpath', value='//*[@id="app"]/div/div[1]/div[2]/form/div[2]/div/div/span/div/div[2]').click()  # 点击发送邮箱
        time.sleep(10)
        code = Get_Code().wangyi(username=userAccount, password='Qwe3541118', name='hydraulic', no=1)  # 获取验证码
        print(f'验证码获取成功：{code}')
        driver.find_element(by='id', value='horizontal_login_code').send_keys(code[0])  # 输入验证码
        driver.find_element(by='id', value='horizontal_login_newPassword').send_keys(new_password)  # 输入新密码
        time.sleep(1)
        driver.find_element(by='class name', value='anticon.anticon-eye-invisible.ant-input-password-icon').click()  # 点击明文查看密码

        driver.find_element(by='class name',
                            value='atn-btn-orange.ant-btn.ant-btn-lg.ant-btn-block').click()  # 点击Confirm the changes
        time.sleep(2)
        return code





