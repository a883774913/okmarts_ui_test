"""
个人中心资料修改
"""
import time

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
            text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                       value=f"{assert_way.split('=', 1)[1]}").text
            print(text)
            assert text == result

        elif casename == '勾选订阅成功':
            Common().huadong(driver,by='class name',value='ant-checkbox-wrapper.ant-checkbox-wrapper-checked') #滑动到指定位置
            elements = driver.find_elements(by='class name',value='ant-checkbox-wrapper.ant-checkbox-wrapper-checked')
            for element in elements:
                element.click()
            time.sleep(1)
            driver.find_element(by='xpath',value='//*[@id="app"]/div[1]/div[2]/div[2]/div/div[1]/div[2]/div[2]/button').click() #点击提交
            WebDriverWait(driver,30,0.2).until(lambda x:x.find_element(by='xpath',value='/html/body/div[2]/span'))
            text = driver.find_element(by='xpath',value='/html/body/div[2]/span').text
            print(text)
        else:
            first_name = data.split('\n')[0].split('=')[-1]
            last_name =  data.split('\n')[1].split('=')[-1]
            company = data.split('\n')[4].split('=')[-1]
            sex =data.split('\n')[2].split('=')[-1]
            time_info = data.split('\n')[3].split('=')[-1]

            driver.find_element(by='css selector',
                                value='#app > div > div.ui-container > div.content.edit-form-out > form > div:nth-child(1) > div > div > span > div '
                                      '> div:nth-child(1) > input').clear()  # 清空输入的名字
            if first_name=='null':
                #输入first name
                driver.find_element(by='css selector',value='#app > div > div.ui-container > div.content.edit-form-out > form > div:nth-child(1) > div > div > span > div '
                                                '> div:nth-child(1) > input').send_keys('')
            else:
                driver.find_element(by='css selector',
                                    value='#app > div > div.ui-container > div.content.edit-form-out > form > div:nth-child(1) > div > div > span > div '
                                          '> div:nth-child(1) > input').send_keys(Common().first_name())

            driver.find_element(by='xpath',
                                value='//*[@id="app"]/div/div[2]/div[1]/form/div[1]/div/div/span/div/div[2]/input').clear() #清空last name
            if last_name == 'null':
            #输入last name
                driver.find_element(by='xpath',value='//*[@id="app"]/div/div[2]/div[1]/form/div[1]/div/div/span/div/div[2]/input').send_keys('')
            else:
                driver.find_element(by='xpath', value='//*[@id="app"]/div/div[2]/div[1]/form/div[1]/div/div/span/div/div[2]/input').send_keys(Common().last_name())

            driver.find_elements(by='class name',value='ant-radio.ant-radio-checked')[int(sex)].click()        #点击性别
            time.sleep(1)
            if time_info == 'today':
                driver.find_element(by='xpath',value='//*[@id="app"]/div/div[2]/div[1]/form/div[3]/div[2]/div/span/span/div').click()           #点击日期弹出日期控件
                time.sleep(1)
                driver.find_element(by='xpath',value='/html/body/div[2]/div/div/div/div/div[2]/div[3]/span/a').click() #点击today
                time.sleep(1)
            else :
                driver.find_element(by='xpath',value='//*[@id="app"]/div/div[2]/div[1]/form/div[3]/div[2]/div/span/span/div/input').clear()
                time.sleep(0.3)
                driver.find_element(by='xpath',value='//*[@id="app"]/div/div[2]/div[1]/form/div[3]/div[2]/div/span/span/div/input').send_keys(time_info)

            driver.find_element(by='xpath',value='//*[@id="app"]/div/div[2]/div[1]/form/div[4]/div[2]/div/span/input').clear()#清空文本
            driver.find_element(by='xpath',value='//*[@id="app"]/div/div[2]/div[1]/form/div[4]/div[2]/div/span/input').send_keys(company)   #输入公司
            time.sleep(1)
            driver.find_element(by='class name',value='atn-btn-orange.ant-btn.ant-btn-primary').click()     #点击提交
            WebDriverWait(driver,20,0.2).until(lambda x:x.find_element(by='css selector',value='body > div.ant-message > span > div > div > div > span'))

            text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                       value=f"{assert_way.split('=', 1)[1]}").text
            print(text)
            assert text == result