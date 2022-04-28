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
        data = Parameter['data']
        print(data)
        assert_way = Parameter['assert_way']
        result = Parameter['result']

        driver.get('http://18.118.13.94:81/index') #打开首页
        time.sleep(1)
        Common().is_login(driver,useraccount='979172251@qq.com',password='a123456')
        time.sleep(1)
        driver.find_element(by='css selector',value='#app > div > div.global-header > div > div.menu-content > div.menu-right.flex > div:nth-child(1)').click() #点击头像
        time.sleep(1)
        driver.find_element(by='css selector',value='#app > div > div.my-info > div.info.flex > div.info-right > div:nth-child(4)').click() #点击地址进入地址管理页面
        time.sleep(1)
        if casename == '点击Manage recipient information跳转到地址管理页面成功':
            print('通道1')
            text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                       value=f"{assert_way.split('=', 1)[1]}").text
            print(text)
            assert text == result
        elif casename == '点击set the address 设置默认地址成功':
            print('通道2')
            self.add_addressinfo(driver,data)
            number = len(driver.find_elements(by='class name',value='address-single.flex.align-center.space-between.margin-bottom'))
            n = 0
            while number < 2:     #如果地址数量小于2个，则循环添加
                self.add_addressinfo(driver,data)
                number = len(driver.find_elements(by='class name',
                                                  value='address-single.flex.align-center.space-between.margin-bottom'))
                n += 1
                if n == 3:
                    print('添加失败')
                    break
            time.sleep(4)
            driver.find_element(by='css selector',value='#app > div > div.ui-container > '
                                                        'div.content.flex.space-between > div > '
                                                        'div.address-list.margin-bottom > div:nth-child(2) > '
                                                        'div.select > a').click()  #点击第二个设置为默认地址
            time.sleep(2)
            text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                       value=f"{assert_way.split('=', 1)[1]}").text
            print(text)
            print(result)
            assert str(text) == result
        elif casename == '点击垃圾桶删除地址成功':
            print('通道3')
            self.add_addressinfo(driver,data)
            time.sleep(3)
            driver.find_element(by='css selector',value='#app > div > div.ui-container > '
                                                        'div.content.flex.space-between > div > '
                                                        'div.address-list.margin-bottom > '
                                                        'div.address-single.flex.align-center.space-between.margin-bottom.active > div.action.text-blue > a.text').click() #点击垃圾桶
            time.sleep(1)
            driver.find_element(by='css selector',value='body > div:nth-child(9) > div > div > div > '
                                                        'div.ant-popover-inner > div > div.ant-popover-buttons > '
                                                        'button.ant-btn.ant-btn-primary.ant-btn-sm').click()#点击确定
            WebDriverWait(driver,20,0.2).until(lambda x:x.find_element_by_css_selector('body > div.ant-message > span > div > div > div > span'))
            text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                       value=f"{assert_way.split('=', 1)[1]}").text
            print(text)
            print(result)
            assert str(text) == result
        elif '修改' in casename:
            print('通道4')
            data = eval(data)
            add_data = str(data[0])
            print(add_data)
            edit_data = str(data[1])
            print(edit_data)
            self.add_addressinfo(driver,add_data)
            time.sleep(2)
            self.edit_mode(driver,edit_data)
            time.sleep(2)
            text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                       value=f"{assert_way.split('=', 1)[1]}").text
            print(text)
            print(result)
            assert text == result
        else:
            print('通道0')
            self.add_addressinfo(driver, data)  #添加地址
            time.sleep(2)
            text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                       value=f"{assert_way.split('=', 1)[1]}").text
            print(text)
            print(result)
            assert text == result



    #怎加地址模块
    def add_addressinfo(self,driver,data):
        """
        增加地址数据
        :param driver: 驱动
        :param data: 字典
        :return:
        """
        data = eval(data)
        driver.find_element(by='css selector',
                            value='#app > div > div.ui-container > div.content.flex.space-between > div > div.address-list.margin-bottom > div > a').click()  # 点击新增地址
        time.sleep(1)
        driver.find_element(by='id', value='coordinated_firstname').send_keys(data['fistname'])
        driver.find_element(by='id', value='coordinated_lastname').send_keys(data['lastname'])
        driver.find_element(by='id', value='coordinated_contactnumber').send_keys(data['contactnumber'])
        driver.find_element(by='id', value='coordinated_area1').send_keys(data['coordinated_area1'])
        driver.find_element(by='id', value='coordinated_area2').send_keys(data['coordinated_area2'])
        driver.find_element(by='id', value='coordinated_area3').send_keys(data['coordinated_area3'])
        driver.find_element(by='id', value='coordinated_postalCode').send_keys(data['coordinated_postalCode'])
        driver.find_element(by='id', value='coordinated_addressLine').send_keys(data['coordinated_addressLine'])
        driver.find_element(by='class name',
                            value='atn-btn-orange.address_submit.ant-btn.ant-btn-primary').click()  # 点击确定
        time.sleep(1)

    #编辑模块
    def edit_mode(self,driver,data):
        data = eval(data)
        driver.find_element(by='xpath', value='//*[@id="app"]/div/div[2]/div[1]/div/div[2]/div[1]/div[4]/a[1]').click() #点击编辑

        js = """document.querySelector("input[id='coordinated_firstname']").value="";"""
        driver.execute_script(js)
        print(data['fistname'])
        if data['fistname'] == 'null':
            print('跳过')
            pass
        else:
            driver.find_element(by='id', value='coordinated_firstname').send_keys(data['fistname'])  #

        js = """document.querySelector("input[id='coordinated_lastname']").value="";"""
        driver.execute_script(js)
        print(data['lastname'])
        if data['lastname'] == 'null':
            print('跳过')
            pass
        else:
            driver.find_element(by='id', value='coordinated_lastname').send_keys(data['lastname'])  #

        js = """document.querySelector("input[id='coordinated_contactnumber']").value="";"""
        driver.execute_script(js)
        print(data['contactnumber'])
        if data['contactnumber'] == 'null':
            print('跳过')
            pass
        else:
            driver.find_element(by='id', value='coordinated_contactnumber').send_keys(data['contactnumber'])  #

        js = """document.querySelector("input[id='coordinated_area1']").value="";"""
        driver.execute_script(js)
        print(data['coordinated_area1'])
        if data['coordinated_area1'] == "null":
            print('跳过')
            pass
        else:
            driver.find_element(by='id', value='coordinated_area1').send_keys(data['coordinated_area1'])  #

        js = """document.querySelector("input[id='coordinated_area2']").value="";"""
        driver.execute_script(js)
        print(data['coordinated_area2'])
        if data['coordinated_area2'] == 'null':
            print('跳过')
            pass
        else:
            driver.find_element(by='id', value='coordinated_area2').send_keys(data['coordinated_area2'])  #

        js = """document.querySelector("input[id='coordinated_area3']").value="";"""
        driver.execute_script(js)
        print(data['coordinated_area3'])
        if data['coordinated_area3'] == 'null':
            print('跳过')
            pass
        else:
            driver.find_element(by='id', value='coordinated_area3').send_keys(data['coordinated_area3'])  #

        js = """document.querySelector("input[id='coordinated_postalCode']").value="";"""
        driver.execute_script(js)
        print(data['coordinated_postalCode'])
        if data['coordinated_postalCode'] == 'null':
            print('跳过')
            pass
        else:
            driver.find_element(by='id', value='coordinated_postalCode').send_keys(data['coordinated_postalCode'])  #

        driver.find_element(by='id', value='coordinated_addressLine').click()
        driver.find_element(by='id', value='coordinated_addressLine').clear() #清除内容
        print(data['coordinated_addressLine'])
        if data['coordinated_addressLine'] == 'null':
            print('跳过')
            pass
        else:
            driver.find_element(by='id', value='coordinated_addressLine').send_keys(data['coordinated_addressLine'])  #

        driver.find_element(by='class name',
                            value='atn-btn-orange.address_submit.ant-btn.ant-btn-primary').click()  # 点击确定
