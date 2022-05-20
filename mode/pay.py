"""
支付
"""
import random
import time

from faker import Faker
from pykeyboard.windows import PyKeyboard
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver import Keys
from selenium.webdriver.support.wait import WebDriverWait

from okmarts_ui_test.common.common import Common
from okmarts_ui_test.mysql.mysql import Mysql


class Pay:


        def pay(self, driver, Parameter):
            faker = Faker('zh_CN')
            casename = Parameter['casename']
            data = Parameter['data']
            print(data)
            assert_way = Parameter['assert_way']
            result = Parameter['result']

            driver.get('http://18.118.13.94:81/index')  # 打开首页
            WebDriverWait(driver, 20, 0.2).until(lambda x: x.find_element(by='xpath', value='//*[@id="app"]/div/div[1]/div/div[2]/div[3]/div[3]/span[1]'))
            time.sleep(1)
            Common().is_login(driver, useraccount='979172251@qq.com', password='a123456')
            # self.get_conponse(driver)
            time.sleep(1)
            driver.find_element(by='class name', value='ant-input').send_keys('1')  # 搜索栏输入1
            time.sleep(1)
            driver.find_element(by='class name', value='ant-btn').click()  # 点击搜索
            time.sleep(3)
            try:
                driver.find_elements(by='class name', value='ant-select-selection-selected-value')[1].click()  # 点击排序按钮
                time.sleep(2)
                driver.find_elements(by='class name', value='ant-select-dropdown-menu-item')[0].click()  # 点击第一个 降序排列
                time.sleep(2)
            except ElementNotInteractableException:
                driver.find_elements(by='class name', value='ant-select-selection-selected-value')[1].click()  # 点击排序按钮
                time.sleep(2)
                driver.find_elements(by='class name', value='ant-select-dropdown-menu-item')[0].click()  # 点击第一个 降序排列
                time.sleep(2)
            if casename == '在购物车中点击结算进入到结算页面成功':
                driver.find_element(by='css selector', value='div[class="btn-out "] > button').click()  # 点击加入购物车
                time.sleep(2)
                driver.find_element(by='class name', value='item.flex ').click()  # 点击购物车跳转到购物车页面
                time.sleep(2)
                driver.find_element(by='class name', value='ant-checkbox-input').click()  # 点击全部勾选
                time.sleep(2)
                driver.find_element(by='class name', value='atn-btn-orange.ant-btn.ant-btn-block').click()  # 点击结算
                time.sleep(2)
                text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                           value=f"{assert_way.split('=', 1)[1]}").text
                print(text)
                assert text == result
            elif casename == '在商品详情页面点击立即购买进入到结算页面成功':
                driver.find_element(by='css selector', value='#app > div > div.ui-container > div.content.search-content.flex.space-between > div.result-list-out > '
                                                             'div.result-list > div:nth-child(1) > div.info > div.title.text-black.margin-bottom-xs > a').click()  # 点击第一个商品
                time.sleep(2)
                driver.find_elements(by='class name', value='atn-btn-orange.ant-btn.ant-btn-block')[1].click()  # 点击立即购买
                time.sleep(3)
                text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                           value=f"{assert_way.split('=', 1)[1]}").text
                print(text)
                assert text == result
            elif casename == '结算页面无地址存在点击立即支付弹出错误提示':
                Mysql().drop_table(user="root", pwd="OKmarts888.,", host="18.118.13.94", db="okmarts", port=3306,
                                   sql="delete from receiving_address where userid='1506910015154425856';")  # 删除979172251@qq.com 地址信息
                driver.find_element(by='css selector', value='#app > div > div.ui-container > div.content.search-content.flex.space-between > div.result-list-out > '
                                                             'div.result-list > div:nth-child(1) > div.info > div.title.text-black.margin-bottom-xs > a').click()  # 点击第一个商品
                WebDriverWait(driver, 30, 0.2).until(lambda x: x.find_element(by='class name', value='atn-btn-orange.ant-btn.ant-btn-block'))
                driver.find_elements(by='class name', value='atn-btn-orange.ant-btn.ant-btn-block')[1].click()  # 点击立即购买
                time.sleep(2)
                driver.find_element(by='class name', value='atn-btn-orange.canBtn2.ant-btn.ant-btn-block').click()  # 点击提交
                time.sleep(2)
                text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                           value=f"{assert_way.split('=', 1)[1]}").text
                print(text)
                assert text == result
            elif casename == '结算页面无地址点击添加添加成功':
                Mysql().drop_table(user="root", pwd="OKmarts888.,", host="18.118.13.94", db="okmarts", port=3306,
                                   sql="delete from receiving_address where userid='1506910015154425856';")  # 删除979172251@qq.com 地址信息
                driver.find_element(by='css selector', value='#app > div > div.ui-container > div.content.search-content.flex.space-between > div.result-list-out > '
                                                             'div.result-list > div:nth-child(1) > div.info > div.title.text-black.margin-bottom-xs > a').click()  # 点击第一个商品
                time.sleep(2)
                driver.find_elements(by='class name', value='atn-btn-orange.ant-btn.ant-btn-block')[1].click()  # 点击立即购买,跳转到结算页面
                time.sleep(2)
                self.add_address(driver, faker)
                text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                           value=f"{assert_way.split('=', 1)[1]}").text
                print(text)
                assert text == result
            elif casename == '不使用优惠卷进入结算进入结算支付页成功':
                driver.find_element(by='css selector', value='#app > div > div.ui-container > div.content.search-content.flex.space-between > div.result-list-out > '
                                                             'div.result-list > div:nth-child(1) > div.info > div.title.text-black.margin-bottom-xs > a').click()  # 点击第一个商品
                time.sleep(2)
                driver.find_elements(by='class name', value='atn-btn-orange.ant-btn.ant-btn-block')[1].click()  # 点击立即购买
                time.sleep(2)
                driver.find_elements(by='class name', value='ant-select-selection-selected-value')[1].click()  # 点击优惠券
                time.sleep(0.5)
                driver.find_elements(by='class name', value='ant-select-dropdown-menu-item.text-xs')[-1].click()  # 点击最后一个
                time.sleep(1)
                driver.find_element(by='class name', value='atn-btn-orange.canBtn2.ant-btn.ant-btn-block').click()  # 点击提交
                time.sleep(2)
                text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                           value=f"{assert_way.split('=', 1)[1]}").text
                print(text)
                assert text == result
            elif casename == '更换地址后点击立即结算支付成功':
                driver.find_element(by='css selector', value='#app > div > div.ui-container > div.content.search-content.flex.space-between > div.result-list-out > '
                                                             'div.result-list > div:nth-child(1) > div.info > div.title.text-black.margin-bottom-xs > a').click()  # 点击第一个商品
                time.sleep(2)
                driver.find_elements(by='class name', value='atn-btn-orange.ant-btn.ant-btn-block')[1].click()  # 点击立即购买
                time.sleep(2)
                try:
                    displayed = driver.find_element(by='class name', value='change.bg-white ').is_displayed()
                except NoSuchElementException:
                    displayed = False
                time.sleep(0.5)
                while not displayed:
                    self.add_address(driver, faker)  # 添加地址
                    try:
                        displayed = driver.find_element(by='class name', value='change.bg-white ').is_displayed()
                    except NoSuchElementException:
                        displayed = False
                driver.find_element(by='xpath', value='//*[@id="app"]/div/div[2]/div[1]/div[1]/div[2]/div[2]/a').click()  # 点击change address
                driver.find_elements(by='class name', value='ant-radio')[-1].click()
                time.sleep(0.5)
                driver.find_element(by='xpath', value='//*[@id="app"]/div/div[2]/div[1]/div[1]/div[2]/div[3]/a').click()  # 点击提交修改
                time.sleep(2)
                text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                           value=f"{assert_way.split('=', 1)[1]}").text
                print(text)
                assert text == result
                driver.find_element(by='class name', value='atn-btn-orange.canBtn2.ant-btn.ant-btn-block').click()  # 点击提交
                time.sleep(2)
                text2 = driver.find_element(by='class name', value='tit.text-center.text-black').text
                print(text2)
                assert text2 == 'Pay'
            elif casename == '结算完成后点击支付页面成功跳转到银联登录页面':
                self.pay_mode(driver,faker)
                driver.find_element(by='class name', value='atn-btn-orange.ant-btn').click()  # 点击提交
                WebDriverWait(driver, 30, 0.2).until(lambda x: x.find_element(by='id', value='email'))
                text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                           value=f"{assert_way.split('=', 1)[1]}").text
                print(text)
                assert text == result
            elif casename == '输入备注信息进行结算页面':
                self.pay_mode(driver,faker)
                text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                           value=f"{assert_way.split('=', 1)[1]}").text
                print(text)
                assert text == result
            elif casename == '存在地址数据点击结算进入结算支付页面成功':
                self.pay_mode(driver,faker)
                text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                           value=f"{assert_way.split('=', 1)[1]}").text
                print(text)
                assert text == result
            elif casename == '使用信用卡支付成功':
                self.pay_mode(driver,faker)
                driver.find_element(by='class name',value='atn-btn-orange.ant-btn').click()     #点击提交
                self.paypal_mode(driver)
                driver.find_element(by='id',value='payment-submit-btn').click()     #使用默认支付方式，点击确定
                WebDriverWait(driver,30,0.2).until(lambda x:x.find_element(by='class name',value='text-tit-lg.margin-bottom-xs'))
                text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                           value=f"{assert_way.split('=', 1)[1]}").text
                print(text)
                assert text == result
            elif casename == '第一个点击取消返回到okmarts取消支付跳转到首页成功':
                self.pay_mode(driver,faker)
                driver.find_element(by='class name', value='atn-btn-orange.ant-btn').click()    #点击提交
                time.sleep(4)
                driver.find_element(by='css selector',value='#hermione-container > div > main > div.CancelLink_container_27tB8.Hermione_cancelLink_2UjcA > a').click()
                time.sleep(5)
                text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                           value=f"{assert_way.split('=', 1)[1]}").text
                print(text)
                assert text == result
            elif casename == '第二个点击取消返回到okmarts取消支付跳转到首页成功':
                self.pay_mode(driver, faker)
                driver.find_element(by='class name', value='atn-btn-orange.ant-btn').click()  # 点击提交
                time.sleep(3)
                self.paypal_mode(driver)
                driver.find_element(by='xpath',value='//*[@id="hermione-container"]/div/main/div[11]/a').click()
                time.sleep(5)
                text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                           value=f"{assert_way.split('=', 1)[1]}").text
                print(text)
                assert text == result
            elif casename == '支付成功后点击back to homepage跳转到首页':
                self.pay_mode(driver, faker)
                driver.find_element(by='class name', value='atn-btn-orange.ant-btn').click()  # 点击提交
                self.paypal_mode(driver)
                time.sleep(2)
                try:
                    driver.find_element(by='id', value='payment-submit-btn').click()  # 使用默认支付方式，点击确定
                except NoSuchElementException:
                    time.sleep(1)
                    driver.find_element(by='id', value='payment-submit-btn').click()  # 使用默认支付方式，点击确定

                WebDriverWait(driver, 30, 0.2).until(lambda x: x.find_element(by='class name', value='text-tit-lg.margin-bottom-xs'))
                time.sleep(2)
                driver.find_element(by='class name',value='ant-btn.ant-btn-lg').click()         #点击返回首页
                time.sleep(3)
                text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                           value=f"{assert_way.split('=', 1)[1]}").text
                print(text)
                assert text == result


        def add_address(self, driver, faker):
            """
            添加地址，点击add address --> 输入信息 --> 点击确定
            :param faker:
            :param driver:  驱动
            :return:
            """

            driver.find_element(by='css selector', value='div[class="empty bg-white"] > a').click()  # 点击add address
            time.sleep(2)
            driver.find_element(by='id', value='coordinated_firstname').send_keys(faker.first_name())
            driver.find_element(by='id', value='coordinated_lastname').send_keys(faker.last_name())
            driver.find_element(by='id', value='coordinated_contactnumber').send_keys(faker.phone_number())
            driver.find_element(by='id', value='coordinated_area1').send_keys(faker.province())
            driver.find_element(by='id', value='coordinated_area2').send_keys(faker.city())
            driver.find_element(by='id', value='coordinated_area3').send_keys(faker.country_code())
            driver.find_element(by='id', value='coordinated_postalCode').send_keys(faker.postcode())
            driver.find_element(by='id', value='coordinated_addressLine').send_keys(faker.address())
            driver.find_element(by='class name',
                                value='atn-btn-orange.ant-btn.ant-btn-primary').click()  # 点击确定
            time.sleep(2)

        def pay_mode(self, driver,faker):
            """
            搜索栏点击第一个商品--详情页面点击立即构面 -- 点击提交
            :param driver:
            :return:
            """
            driver.find_element(by='css selector', value='#app > div > div.ui-container > div.content.search-content.flex.space-between > div.result-list-out > '
                                                         'div.result-list > div:nth-child(1) > div.info > div.title.text-black.margin-bottom-xs > a').click()  # 点击第一个商品
            WebDriverWait(driver,30,0.2).until(lambda x:x.find_element(by='class name',value='atn-btn-orange.ant-btn.ant-btn-block'))
            driver.find_elements(by='class name', value='atn-btn-orange.ant-btn.ant-btn-block')[1].click()  # 点击立即购买
            time.sleep(2)
            try:
                status = driver.find_element(by='class name', value='action.text-blue').is_displayed()
                print(status)
            except:
                self.add_address(driver, faker)
            time.sleep(1)
            driver.find_element(by='css selector', value='textarea[class="ant-input"]').send_keys(faker.text(max_nb_chars=200, ext_word_list=None))
            driver.find_element(by='class name', value='atn-btn-orange.canBtn2.ant-btn.ant-btn-block').click()  # 点击提交
            time.sleep(2)

        def paypal_mode(self,driver):
            """
            paypal页面 输入用户名 -- 输入密码 -- 点击登录
            :param driver:
            :return:
            """
            time.sleep(4)
            driver.find_element(by='id', value='email').send_keys('sb-uqrge14394857@personal.example.com')  # 输入账户名
            try:
                driver.find_element(by='id', value='btnNext').click()  # 点击下一步
            except NoSuchElementException:          #概率性不出现
                pass
            time.sleep(3)
            try:
                driver.find_element(by='id', value='password').send_keys('qwe3541118')  # 输入密码
            except ElementNotInteractableException:
                time.sleep(2)
                driver.find_element(by='id', value='password').send_keys('qwe3541118')  # 输入密码
            time.sleep(2)
            driver.find_element(by='id', value='btnLogin').click()  # 点击登录
            time.sleep(2)

        def get_conponse(self,driver):
            """
            去积分商城兑换优惠券 --回到首页
            :param driver:
            :return:
            """
            driver.find_element(by='class name',value='r_text').click() #点击头像
            time.sleep(2)
            driver.find_element(by='class name',value='pointsMall-out.text-center').click() #点击积分商城
            time.sleep(2)
            elements = driver.find_elements(by='class name',value='ant-btn.ant-btn-block')
            random.choice(elements).click()        #随机点击一个交换按钮
            time.sleep(1)
            driver.find_element(by='class name',value='bg-orange.ant-btn').click()      #点击交换
            time.sleep(1)
            pk = PyKeyboard()
            pk.press_key(pk.escape_key)
            pk.release_key(pk.escape_key)       #按压esc键快速关闭提示
            driver.find_element(by='class name',value='logo.pointer')       #点击LOGO 回到首页
            time.sleep(2)