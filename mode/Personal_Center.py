"""
个人中心资料修改
"""
import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

from okmarts_ui_test.common.common import Common


class Personal_Center:

    def person_center(self,driver,Parameter):
        casename = Parameter['casename']
        data = Parameter['data']
        print(data)
        assert_way = Parameter['assert_way']
        result = Parameter['result']

        driver.get('http://18.118.13.94:81/index')  # 打开首页
        time.sleep(1)
        Common().is_login(driver, useraccount='979172251@qq.com', password='a123456')  # 检测是否登录
        time.sleep(1)
        driver.find_element(by='css selector', value='#app > div > div.global-header > div > div.menu-content > div.menu-right.flex > div:nth-child(1)').click()  # 点击头像
        time.sleep(2)
        driver.find_element(by='class name', value='icon-edit').click()  # 点击修改图标
        time.sleep(2)
        if casename == '点击账户名称进入个人信息修改页面成功':
            print('通道1')
            text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                       value=f"{assert_way.split('=', 1)[1]}").text
            print(text)
            assert text == result
        elif casename == '勾选订阅成功':
            print('通道2')
            Common().huadong(driver,by='xpath',value='//*[@id="app"]/div/div[2]/div[2]/div/div[1]/div[1]') #滑动到指定位置
            time.sleep(0.5)
            driver.find_elements(by='class name',value='ant-checkbox-input')[0].click()
            driver.find_elements(by='class name', value='ant-checkbox-input')[1].click()
            driver.find_elements(by='class name', value='ant-checkbox-input')[2].click()
            time.sleep(0.5)
            driver.find_element(by='xpath',value='//*[@id="app"]/div[1]/div[2]/div[2]/div/div[1]/div[2]/div[2]/button').click() #点击提交
            time.sleep(1.5)
            text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                       value=f"{assert_way.split('=', 1)[1]}").text
            print(text)
            assert text == result
        elif casename == '通过个人中心修改邮箱入口进入成功':
            Common().huadong(driver,by='class name',value='form-out.form-out-1.flex.align-center.bg-white.space-between')
            time.sleep(1)
            driver.find_element(by='xpath',value='//*[@id="app"]/div[1]/div[2]/div[2]/div/div[2]/div[2]/div[2]/button').click() #点击send
            time.sleep(2)
            text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                       value=f"{assert_way.split('=', 1)[1]}").text
            print(text)
            assert text == result

        else:
            print('通道3')
            first_name = data.split('\n')[0].split('=')[-1]
            print(first_name)
            last_name =  data.split('\n')[1].split('=')[-1]
            print(last_name)
            company = data.split('\n')[4].split('=')[-1]
            print(company)
            sex =data.split('\n')[2].split('=')[-1]
            print(sex)
            time_info = data.split('\n')[3].split('=')[-1]
            print(time_info)
            driver.find_element(by='css selector',value='input[placeholder="firstName"]').send_keys(Keys.CONTROL,'a')
            driver.find_element(by='css selector', value='input[placeholder="firstName"]').send_keys(Keys.DELETE)
            time.sleep(0.5)
            if first_name=='null':
                #输入first name
                driver.find_element(by='css selector',value='#app > div > div.ui-container > div.content.edit-form-out > form > div:nth-child(1) > div > div > span > div '
                                                '> div:nth-child(1) > input').send_keys('')
            else:
                driver.find_element(by='css selector',
                                    value='#app > div > div.ui-container > div.content.edit-form-out > form > div:nth-child(1) > div > div > span > div '
                                          '> div:nth-child(1) > input').send_keys(Common().first_name())
            driver.find_element(by='css selector', value='input[placeholder="lastName"]').send_keys(Keys.CONTROL, 'a')
            driver.find_element(by='css selector', value='input[placeholder="lastName"]').send_keys(Keys.DELETE)
            time.sleep(0.5)
            if last_name == 'null':
            #输入last name
                driver.find_element(by='xpath',value='//*[@id="app"]/div/div[2]/div[1]/form/div[1]/div/div/span/div/div[2]/input').send_keys()
            else:
                driver.find_element(by='xpath', value='//*[@id="app"]/div/div[2]/div[1]/form/div[1]/div/div/span/div/div[2]/input').send_keys(Common().last_name())

            time.sleep(2)
            driver.find_elements(by='class name',value='ant-radio-input')[int(sex)].click()        #点击性别

            time.sleep(1)
            if time_info == 'today':
                driver.find_element(by='xpath',value='//*[@id="app"]/div/div[2]/div[1]/form/div[3]/div[2]/div/span/span/div').click()           #点击日期弹出日期控件
                time.sleep(0.2)
                WebDriverWait(driver,20,0.2).until(lambda x:x.find_element(by='class name',value='ant-calendar-today-btn '))
                time.sleep(0.2)
                driver.find_element(by='class name',value='ant-calendar-today-btn ').click() #点击today
                time.sleep(1)
            else :
                driver.find_element(by='css selector', value='input[placeholder="Pick your birthDay"]').click()
                # driver.find_element(by='selector',value='ant-calendar-picker-input.ant-input').click()
                time.sleep(0.2)
                driver.find_element(by='css selector', value='input[placeholder="Pick your birthDay"]').send_keys(Keys.CONTROL, 'a')
                driver.find_element(by='css selector', value='input[placeholder="Pick your birthDay"]').send_keys(Keys.DELETE)
                time.sleep(0.3)
                driver.find_element(by='xpath',value='//*[@id="app"]/div/div[2]/div[1]/form/div[3]/div[2]/div/span/span/div/input').send_keys(time_info)

            driver.find_element(by='xpath',value='//*[@id="app"]/div/div[2]/div[1]/form/div[4]/div[2]/div/span/input').send_keys(Keys.CONTROL, 'a')
            driver.find_element(by='xpath',value='//*[@id="app"]/div/div[2]/div[1]/form/div[4]/div[2]/div/span/input').send_keys(Keys.DELETE)
            time.sleep(0.5)
            driver.find_element(by='xpath',value='//*[@id="app"]/div/div[2]/div[1]/form/div[4]/div[2]/div/span/input').send_keys(company)   #输入公司
            time.sleep(1)
            driver.find_element(by='class name',value='atn-btn-orange.ant-btn.ant-btn-primary').click()     #点击提交
            WebDriverWait(driver,20,0.2).until(lambda x:x.find_element(by='css selector',value='body > div.ant-message > span > div > div > div > span'))
            text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                       value=f"{assert_way.split('=', 1)[1]}").text
            print(text)
            assert text == result