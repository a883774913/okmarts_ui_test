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
            userAccount = random.choice(['a979172251@163.com', 'a9791722511@163.com', 'a97917225111@163.com'])

        if casename in ['输入正确内容修改密码成功','不输入验证码下一步置灰','输入过期验证码点击下一步失败','输入6位字母+数字密码更改成功']:
            new_password = 'test' + f'{random.randint(11, 99)}'
        else:
            new_password = password

        print(f'new password 为 {new_password}')

        driver.get("http://18.118.13.94:81/index")
        time.sleep(1)
        Common().Restore_environment(driver)    #判断是否为登录状态
        time.sleep(1)
        driver.find_element(by='xpath',value='//*[@id="app"]/div/div[1]/div/div[2]/div[3]/div[1]').click()  #点击头像进入登录页面
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
            assert text == result
        elif casename == '不输入验证码下一步置灰' :
            print('通道3')
            driver.find_element(by='id', value='horizontal_login_userName').send_keys(userAccount)  # 输入用户名
            driver.find_element(by='id', value='horizontal_login_newPassword').send_keys(new_password)  # 输入新密码
            text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                       value=f"{assert_way.split('=', 1)[1]}").get_attribute('disabled')
            print(text)
            assert text == result
        elif casename == '输入过期验证码点击下一步失败' :
            print('通道4')
            driver.find_element(by='id', value='horizontal_login_userName').send_keys(userAccount)  # 输入用户名
            driver.find_element(by='xpath',
                                value='//*[@id="app"]/div/div[1]/div[2]/form/div[2]/div/div/span/div/div[2]').click()  # 点击发送邮箱
            WebDriverWait(driver, 30, 0.2).until(lambda x: x.find_element_by_css_selector(
                "body > div.ant-message > span > div > div > div > span"))  # 显示等待
            time.sleep(80)
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

        elif casename in ['输入正确内容修改密码成功','输入6位字母+数字密码更改成功','输入16位字母+数字更改成功','输入修改过的密码更改失败']:
            print('通道5')
            driver.find_element(by='id',value='horizontal_login_userName').send_keys(userAccount)  #输入用户名
            driver.find_element(by='xpath',value='//*[@id="app"]/div/div[1]/div[2]/form/div[2]/div/div/span/div/div[2]').click() #点击发送邮箱
            WebDriverWait(driver,30,0.2).until(lambda x:x.find_element_by_css_selector("body > div.ant-message > span > div > div > div > span"))   #显示等待
            code_info = driver.find_element(by='css selector',value='body > div.ant-message > span > div > div > div > span').text
            if code_info == 'Verification code has been sent. Please do not click again!':
                time.sleep(60)
            else:
                time.sleep(10)
            code = Get_Code().wangyi(username=userAccount, password='Qwe3541118', name='hydraulic', no=1)  # 获取验证码
            driver.find_element(by='id',value='horizontal_login_code').send_keys(code[0])   #输入验证码
            driver.find_element(by='id',value='horizontal_login_newPassword').send_keys(new_password)       #输入新密码
            time.sleep(1)
            driver.find_element(by='class name',value='atn-btn-orange.ant-btn.ant-btn-lg.ant-btn-block').click()    #点击Confirm the changes
            time.sleep(5)
            driver.find_element(by='css selector',
                            value='#app > div > div.global-header > div > div.menu-content > div.menu-right.flex > div:nth-child(1)').click()  # 点击按钮进入个人中心  #点击头像进行登录
            time.sleep(1)
            Common().login(driver,userAccount,password=new_password)     #登录操作
            time.sleep(1)
            text = driver.find_element(by=f"{assert_way.split('=',1)[0]}",value=f"{assert_way.split('=',1)[1]}").text
            print(text)
            assert text != result
        elif casename == '更改密码成功后回退重新输入验证码':
            print('通道6')
            driver.find_element(by='id', value='horizontal_login_userName').send_keys(userAccount)  # 输入用户名
            driver.find_element(by='xpath',
                                value='//*[@id="app"]/div/div[1]/div[2]/form/div[2]/div/div/span/div/div[2]').click()  # 点击发送邮箱
            WebDriverWait(driver, 30, 0.2).until(lambda x: x.find_element_by_css_selector(
                "body > div.ant-message > span > div > div > div > span"))  # 显示等待
            code_info = driver.find_element(by='css selector',
                                            value='body > div.ant-message > span > div > div > div > span').text
            if code_info == 'Verification code has been sent. Please do not click again!':
                time.sleep(60)
                driver.find_element(by='xpath',
                                    value='//*[@id="app"]/div/div[1]/div[2]/form/div[2]/div/div/span/div/div[2]').click()  # 点击发送邮箱
                time.sleep(8)
            else:
                time.sleep(10)
            code = Get_Code().wangyi(username=userAccount, password='Qwe3541118', name='hydraulic', no=1)  # 获取验证码
            driver.find_element(by='id', value='horizontal_login_code').send_keys(code[0])  # 输入验证码
            driver.find_element(by='id', value='horizontal_login_newPassword').send_keys(new_password)  # 输入新密码
            driver.find_element(by='class name',
                                value='atn-btn-orange.ant-btn.ant-btn-lg.ant-btn-block').click()  # 点击Confirm the changes
            time.sleep(5)
            driver.back()       #回退页面
            time.sleep(2)
            info = driver.find_element(by='class name',value='title.text-tit-lg.margin-bottom-lg').text
            print(info)
            text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}", value=f"{assert_way.split('=', 1)[1]}").text
            print(text)
            assert text == result
        else:
            print('通道0')
            driver.find_element(by='id', value='horizontal_login_userName').send_keys(userAccount)  # 输入用户名
            driver.find_element(by='xpath',
                                value='//*[@id="app"]/div/div[1]/div[2]/form/div[2]/div/div/span/div/div[2]').click()  # 点击发送邮箱
            WebDriverWait(driver, 30, 0.2).until(lambda x: x.find_element_by_css_selector(
                "body > div.ant-message > span > div > div > div > span"))  # 显示等待
            code_info = driver.find_element(by='css selector',
                                            value='body > div.ant-message > span > div > div > div > span').text
            if code_info == 'Verification code has been sent. Please do not click again!':
                time.sleep(60)
            else:
                time.sleep(10)
            code = Get_Code().wangyi(username=userAccount, password='Qwe3541118', name='hydraulic', no=1)  # 获取验证码
            driver.find_element(by='id', value='horizontal_login_code').send_keys(code[0])  # 输入验证码
            driver.find_element(by='id', value='horizontal_login_newPassword').send_keys(new_password)  # 输入新密码
            driver.find_element(by='class name',
                                value='atn-btn-orange.ant-btn.ant-btn-lg.ant-btn-block').click()  # 点击Confirm the changes
            time.sleep(1)
            text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}", value=f"{assert_way.split('=', 1)[1]}").text
            print(text)
            assert text == result






