"""
注册模块
"""
import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait

from okmarts_ui_test.common.common import Common
from okmarts_ui_test.mode.get_code import Get_Code
from okmarts_ui_test.mysql.mysql import Mysql


class Regist:

    def __init__(self):
        Mysql().drop_table(user="root", pwd="OKmarts888.,", host="18.118.13.94", db="okmarts", port=3306,
                           sql='delete from users where userName like "a883774%";')

    def regist(self, Parameter, driver):
        casename = Parameter['casename']
        mode = Parameter['mode']
        data = Parameter['data'].split('\n')
        if casename == '用户名邮箱为空下一步操作置灰':
            useraccount = data[0].split('=')[-1]
        elif casename == '输入已存在的用户名注册失败':
            useraccount = '979172251@qq.com'
        else:
            useraccount = Common().random_email_account()

        assert_way = Parameter['assert_way']
        result = Parameter['result']
        driver.get('http://18.118.13.94:81/my/register')
        time.sleep(0.5)
        driver.find_element(by='id', value='register_step_1_userAccount').send_keys(useraccount)

        if casename == '不勾选用户协议注册失败':
            driver.find_element(by='class name', value='ant-checkbox').click()
        else:
            pass

        driver.find_element(by='xpath',
                            value='//*[@id="app"]/div/div[1]/div[2]/form/div[3]/div/div/span/div/button/a').click()  # 点击下一步发送验证码

        if casename == '用户名邮箱为空下一步操作置灰':
            text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                       value=f"{assert_way.split('=', 1)[1]}").get_attribute('disabled')
            print('通道1')
            print(text)
            assert text == result
        elif casename == '关闭验证码页面成功':
            time.sleep(3)
            # print(self.dr.find_element(by='class name', value='ant-modal-body').is_displayed())
            driver.find_element(by='class name', value='anticon.anticon-close.ant-modal-close-icon').click()
            time.sleep(0.5)
            assert driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                       value=f"{assert_way.split('=', 1)[1]}").is_displayed() is not result
        elif casename == '使用过期验证码验证失败':
            code = Get_Code().wangyi(username=useraccount, password='Qwe3541118', name='hydraulic', no=2)  # 获取验证码
            self.input_code(driver, code)
            time.sleep(2)
            text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                       value=f"{assert_way.split('=', 1)[1]}").text
            print('通道2')
            print(text)
            assert text == result
        elif casename == '输入错误验证码注册失败':
            self.input_code(driver, ['111111'])
            time.sleep(2)
            text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                       value=f"{assert_way.split('=', 1)[1]}").text
            print('通道3')
            print(text)
            assert text == result
        elif casename == '超时后再次发送验证码成功':
            time.sleep(63)
            driver.find_element(by='xpath', value='/html/body/div[2]/div/div[2]/div/div[2]/div/div/div[2]/a').click()
            time.sleep(3)
            text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                       value=f"{assert_way.split('=', 1)[1]}").text
            print('通道4')
            print(text)
            assert text == result
        elif casename in ['邮箱不含@弹出错误提示', '输入已存在的用户名注册失败', '不勾选用户协议注册失败']:
            time.sleep(1)
            text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                       value=f"{assert_way.split('=', 1)[1]}").text
            print('通道5')
            print(text)
            assert text == result
        elif casename == '注册完成后领取优惠卷成功':
            self.regist_mode1(useraccount, driver, data)
            try:
                driver.find_element(by='xpath', value='//*[@id="app"]/div/div[1]/div[5]/img').click()  # 点击礼物箱
            except NoSuchElementException:
                time.sleep(1)
                driver.find_element(by='xpath', value='//*[@id="app"]/div/div[1]/div[5]/img').click()  # 点击礼物箱 如果报错等待1S 再次点击
            time.sleep(0.2)
            driver.find_element(by='class name', value='bg-orange.ant-btn').click()  # 点击确定
            time.sleep(2)
            text = driver.find_element(by='xpath', value='/html/body/div[2]/span/div/div/div/span').text
            print(text)
            Common().login(driver,useraccount,password=data[1].split('=')[-1])
            WebDriverWait(driver,30,0.2).until(lambda x:x.find_element_by_css_selector('#app > div > div.global-header > div > div.menu-content > div.menu-right.flex > div:nth-child(1) > span'))
            driver.find_element(by='css selector', value='#app > div > div.global-header > div > div.menu-content > div.menu-right.flex > div:nth-child(1) > span').click()
            time.sleep(1.5)
            coupons_text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                               value=f"{assert_way.split('=', 1)[1]}").text
            print('通道6')
            print(coupons_text)
            assert text == 'success' and coupons_text == result
        elif casename == '领取优惠卷回退页面再次领取失败':
            self.regist_mode1(useraccount, driver, data)
            driver.find_element(by='xpath', value='//*[@id="app"]/div/div[1]/div[5]/img').click()  # 点击礼物箱
            time.sleep(0.2)
            driver.find_element(by='class name', value='bg-orange.ant-btn').click()  # 点击确定
            time.sleep(2)
            driver.back()
            time.sleep(2)
            driver.find_element(by='class name', value='bg-orange.ant-btn').click()  # 点击确定
            time.sleep(2)
            Common().login(driver,useraccount,password=data[1].split('=')[-1])   #登录
            driver.find_element(by='css selector', value='#app > div > div.global-header > div > div.menu-content > div.menu-right.flex > div:nth-child(1) > span > p').click()
            time.sleep(1.5)
            coupons_text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                               value=f"{assert_way.split('=', 1)[1]}").text
            print('通道7')
            print(coupons_text)
            assert coupons_text == result
        elif casename == '不进行验证注册失败':
            print('通道0')
            time.sleep(10)      #等待验证码发送至邮箱
            code = Get_Code().wangyi(username=useraccount, password='Qwe3541118', name='hydraulic', no=1)  # 获取验证码
            print(code[0])
            self.input_code(driver, code)
            time.sleep(2)
            driver.find_element(by='css selector',value='#app > div > div.login-form-wrap > '
                                                        'div.login-form.margin-bottom > form > div:nth-child(1) > div'
                                                        ' > div > span > span > input').send_keys(data[1].split('=')[-1]) # 输入密码

            time.sleep(0.5)
            driver.find_element(by="css selector",
                                value='#app > div > div.login-form-wrap > div.login-form.margin-bottom > form > '
                                      'div.btn-out.ant-row.ant-form-item > div > div > span > div > a').click()  # 点击下一步
            WebDriverWait(driver,30,0.2).until(lambda driver:driver.find_element(by='css selector',value='body > div.ant-message > span > div > div > div > span'))
            time.sleep(2)
            text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                       value=f"{assert_way.split('=', 1)[1]}").text
            print(f'text 为{text}')
            print(f'result 为{result}')
            assert text == result
        else:
            try:
                self.regist_mode1(useraccount, driver, data)
                text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                           value=f"{assert_way.split('=', 1)[1]}").text
                print('通道0')
                print(text)
                assert text == result
            except :
                raise AssertionError

    def input_code(self, driver, code):
        """
        注册界面输入验证码
        :param driver: 驱动
        :param code: 验证码 格式为 [111111]
        :return:
        """
        print(f'验证码为{code}')
        WebDriverWait(driver, 30, 0.2).until(lambda x: x.find_element_by_css_selector(
            'div[class="input-content"]>input[data-index="0"]'))  # 显示等待
        driver.find_element(by='css selector', value='div[class="input-content"]>input[data-index="0"]').send_keys(
            code[0][0])  # 验证码第1个
        driver.find_element(by='css selector', value='div[class="input-content"]>input[data-index="1"]').send_keys(
            code[0][1])  # 验证码第2个
        driver.find_element(by='css selector', value='div[class="input-content"]>input[data-index="2"]').send_keys(
            code[0][2])  # 验证码第3个
        driver.find_element(by='css selector', value='div[class="input-content"]>input[data-index="3"]').send_keys(
            code[0][3])  # 验证码第4个
        driver.find_element(by='css selector', value='div[class="input-content"]>input[data-index="4"]').send_keys(
            code[0][4])  # 验证码第5个
        driver.find_element(by='css selector', value='div[class="input-content"]>input[data-index="5"]').send_keys(
            code[0][5])  # 验证码第6个
        driver.find_element(by='css selector', value='div[class="input-content"]>input[data-index="5"]').click()
        driver.find_element(by='css selector', value='div[class="input-content"]>input[data-index="5"]').send_keys(
            code[0][5])  # 验证码第6个

    # 获取验证码 - 输入验证码 - 移动滑块 - 点击注册
    def regist_mode1(self, useraccount, driver, data):
        time.sleep(10)
        code = Get_Code().wangyi(username=useraccount, password='Qwe3541118', name='hydraulic', no=1)  # 获取验证码
        print(code[0])
        self.input_code(driver, code)
        WebDriverWait(driver, 30, 0.2).until(lambda x: x.find_element_by_xpath(
            '//*[@id="app"]/div/div/div[2]/form/div[2]/div/div/span/div/div[2]/div/div/i'))  # 显示等待
        huakuai = driver.find_element("xpath",
                                      value="""//*[@id="app"]/div/div/div[2]/form/div[2]/div/div/span/div/div[2]/div/div/i""")  # 定位滑块
        self.move_to_gap(huakuai, self.get_track(500), driver)  # 移动滑块

        driver.find_element(by='xpath',
                            value='//*[@id="app"]/div/div[1]/div[2]/form/div[1]/div/div/span/span/input').send_keys(
            data[1].split('=')[-1])     #输入密码
        time.sleep(1)

        driver.find_element(by="xpath",
                            value='//*[@id="app"]/div/div[1]/div[2]/form/div[3]/div/div/span/div/a').click()    #点击下一步
        time.sleep(2)

    def move_to_gap(self, slider, tracks, driver):  # 验证码模块
        ActionChains(driver).click_and_hold(slider).perform()
        for x in tracks:
            ActionChains(driver).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(0.5)
        ActionChains(driver).release().perform()

    def get_track(self, distance):  # 注册验证功能使用
        track = []  # 移动轨迹
        current = 0  # 当前位移
        mid = distance * 4 / 5  # 计算间隔
        t = 0.8  # 计算间隔
        v = 1  # 初速度
        while current < distance:
            if current < mid:  # 加速度为2
                a = 4
            else:
                a = -3
            v0 = v  # 当前速度
            v = v0 + a * t  # 移动距离
            move = v0 * t + 1 / 2 * a * t * t  # 当前位移
            current += move  # 加入轨迹
            track.append(round(move))
        return track
