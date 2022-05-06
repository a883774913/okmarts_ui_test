"""
订单模块
"""
import re
import time

import pytest
from pykeyboard.windows import PyKeyboard
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait

from okmarts_ui_test.common.common import Common


class My_Order:

    def my_order(self, driver, Parameter):
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
        if casename == '点击个人中心Order record 订单成功显示':
            print('通道1')
            text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                       value=f"{assert_way.split('=', 1)[1]}").is_displayed()
            print(text)
            assert text == result
        elif casename == '点击订单中的商品名称跳转商品详情成功':
            print('通道2 ')
            goods_name = driver.find_element(by='xpath', value='//*[@id="app"]/div/div[3]/div[1]/div/div[1]/div[2]/div/div[2]/div[1]/div[1]/div/a').text
            print(goods_name)
            driver.find_element(by='xpath', value='//*[@id="app"]/div/div[3]/div[1]/div/div[1]/div[2]/div/div[2]/div[1]/div[1]/div/a').click()  # 点击商品名称
            time.sleep(2)
            buy_now = driver.find_elements(by='class name', value='atn-btn-orange.ant-btn.ant-btn-block')[1].text  # 获取buy_now
            # 文本 确认是在商品详情页面
            print(buy_now)
            assert buy_now == 'Buy now'

            goods_name1 = driver.find_element(by='class name', value='title.text-black.margin-bottom-sm').text  # 获取详情页面 商品名称
            assert goods_name == goods_name1
        elif casename == "点击查看物流查看成功":
            print('通道3')
            driver.find_element(by='xpath', value='//*[@id="app"]/div/div[3]/div[1]/div/div[1]/div[2]/div/div[2]/div[1]/div[4]/a').click()  # 点击物流按钮
            time.sleep(2)
            text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                       value=f"{assert_way.split('=', 1)[1]}").text
            print(text)
            assert text == result
        elif casename == '未支付订单点击未支付跳转到支付页面':
            print('通道4')
            n = 0  # 判断是否找到
            page = 0  # 判断所处页数
            while True:
                n = self.find_Unpaid(driver, n)
                page += 1
                print(f'n 为 {n} ')
                if n == 0:  # 如果循环后没有找到 点击下一页进行查找
                    print(f'第{page}未找到待支付订单数据')
                    # 查询该页面是否为最后一页
                    try:
                        # 移动到翻页处
                        Common().huadong(driver, by='class name', value='ant-pagination-item-link')
                        # 先判断下一页按钮状态 如果为true 说明是最后一页
                        info = driver.find_element(by='class name', value='ant-pagination-disabled.ant-pagination-next').get_attribute(
                            'aria-disabled')
                        if info == "true":
                            print('此页为最后一页')
                            break
                    except NoSuchElementException:
                        print('不是最后一页')
                        driver.find_element(by='css selector', value='li[class=" ant-pagination-next"]').click()  # 点击下一页
                        print('点击下一页')
                        time.sleep(2)
                else:  # 如果找到了-->
                    print(f'第{page}页存在待支付数据')
                    break
            if n == 0:
                print('该账户不存在待支付数据')
                pass
            else:
                time.sleep(2)
                # 获取待支付页面 断言文本
                text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                               value=f"{assert_way.split('=', 1)[1]}").text
                print(text)
                assert text == result
        elif casename == '点击order data可以根据订单时间进行排序':
            Common().huadong(driver, by='class name', value='text-tit-lg.flex')  # 滑动到订单最上方
            time.sleep(1)
            element = driver.find_element(by='css selector',
                                          value='#app > div > div.ui-container > div.content.my-center-form > div > div.record_out > div.table-out > div > div.title.flex.align-center > div:nth-child(2) > svg')
            info = element.get_attribute('p-id')
            self.assert_time_desc(driver, info)
            time.sleep(2)
            element.click()
            info2 = element.get_attribute('p-id')
            if info2 == info:
                print('点击后未发生变化，再次点击')
                element.click()  # 再次点击
                time.sleep(2)
                info3 = element.get_attribute('p-id')
                self.assert_time_desc(driver, info3)
            else:
                self.assert_time_desc(driver, info2)
        elif casename == '点击Total price可以根据订单金额进行排序':
            Common().huadong(driver, by='class name', value='text-tit-lg.flex')  # 滑动到订单最上方
            time.sleep(1)
            element = driver.find_element(by='css selector', value='#app > div > div.ui-container > div.content.my-center-form > div > div.record_out > div.table-out '
                                                                   '> div > div.title.flex.align-center > div:nth-child(3) > svg')
            info = element.get_attribute('p-id')
            self.assert_price_desc(driver, info)
            time.sleep(1)
            element.click()
            info2 = element.get_attribute('p-id')
            if info2 == info:
                print('点击后未发生变化')
                element.click()
                time.sleep(1)
                info3 = element.get_attribute('p-id')
                self.assert_price_desc(driver, info3)
            else:
                self.assert_price_desc(driver, info2)
        elif casename == '通过关键字及全文查找可以成功查询相同名称的订单':
            Common().huadong(driver, by='class name', value='text-tit-lg.flex')  # 滑动到订单最上方
            time.sleep(1)
            try:
                info = driver.find_element(by='css selector',
                                           value='#app > div > div.ui-container > div.content.my-center-form > div > div.record_out > div.table-out > div > '
                                                 'div.tableData > div:nth-child(1) > div.item.width-32.name > div > a').text
                print(info)
            except NoSuchElementException:
                print('未找到订单数据')
                raise AssertionError

            driver.find_element(by='xpath', value='//*[@id="app"]/div/div[3]/div[1]/div/div[1]/div[1]/div[2]/span/input').send_keys(info)  # 搜索栏输入名字
            driver.find_element(by='class name', value='anticon.anticon-search.ant-input-search-icon').click()  # 点击搜索按钮
            time.sleep(2)
            elements = driver.find_elements(by='css selector', value='div[class="item width-32 name"] > div > a')
            erro = 0
            for element in elements:
                print(element.text)
                if info in element.text:
                    pass
                else:
                    erro += 1
            if erro == 0:
                assert True
            else:
                assert False
        elif casename == '已签收订单点击退货申请进入退货页面成功':
            n = self.go_return_goods(driver)
            if n == 0:
                print('该账户不存在已签收数据')
                pass
            else:
                time.sleep(2)
                # 获取待支付页面 断言文本
                try:
                    text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                               value=f"{assert_way.split('=', 1)[1]}").text
                    print(text)
                    assert text == result
                except:
                    raise AssertionError
        elif '提交退货单' in casename:
            n = self.go_return_goods(driver)
            if n == 0:
                print('该账户不存在已签收数据')
                pytest.skip(msg="未找到相关数据")
            else:
                time.sleep(2)
                Reasons_for_return = data.split('\n')[0].split('=')[-1]
                print(Reasons_for_return)
                reason = data.split('\n')[1].split('=')[-1]
                print(reason)
                img = data.split('\n')[2].split('=')[-1]
                print(img)
                if Reasons_for_return == 'Quality issues':
                    pass
                elif Reasons_for_return =='Wrong order inform ation':
                    driver.find_elements(by='class name',value='ant-select-selection__rendered')[1].click()
                    time.sleep(1)
                    driver.find_elements(by="class name",value='ant-select-dropdown-menu-item')[1].click()   #点击第2个
                elif Reasons_for_return == 'Model error':
                    driver.find_elements(by='class name', value='ant-select-selection__rendered')[1].click()
                    time.sleep(1)
                    driver.find_elements(by="class name", value='ant-select-dropdown-menu-item')[2].click()  # 点击第3个
                elif Reasons_for_return == 'other':
                    driver.find_elements(by='class name', value='ant-select-selection__rendered')[1].click()
                    time.sleep(1)
                    driver.find_elements(by="class name", value='ant-select-dropdown-menu-item')[3].click()  # 点击第4个
                time.sleep(1)


                driver.find_element(by='class name',value='tuik_text').send_keys(reason)
                if img == 'null':
                    print('不上传图片')
                    pass
                else:
                    driver.find_element(by='class name',value='ant-upload').click() #点击上传
                    time.sleep(2)
                    pk = PyKeyboard()
                     # 实例化
                    pk.press_key(pk.shift_key)
                    pk.release_key(pk.shift_key)
                    pk.type_string(img)
                    time.sleep(2)
                    pk.press_key(pk.enter_key)  # 按压
                    pk.release_key(pk.enter_key)  # 释放
                    pk.press_key(pk.enter_key)  # 按压
                    pk.release_key(pk.enter_key) # 释放
                    time.sleep(2)
                    WebDriverWait(driver,30,0.2).until(lambda x: x.find_element(by='class name',value='ant-upload-list-item-thumbnail'))


                driver.find_element(by='class name',value='atn-btn-orange.ant-btn').click() #点击提交
                try:
                    WebDriverWait(driver, 20, 0.2).until(lambda x: x.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                                                                  value=f"{assert_way.split('=', 1)[1]}"))
                    time.sleep(0.2)
                    text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                               value=f"{assert_way.split('=', 1)[1]}").text
                    print(text)
                    assert text == result
                except NoSuchElementException:
                    raise AssertionError



    # 断言价格排序方法
    def assert_price_desc(self, driver, info):
        """
        断言价格排序方法
        :param driver: 驱动
        :param info: 判断升降序的值
        :return:
        """
        if info == '2035':  # 为降序
            price_1 = driver.find_elements(by='class name', value='item.width-17.text-orange')[0].text
            price_1 = float(price_1.replace('$', ''))
            price_2 = driver.find_elements(by='class name', value='item.width-17.text-orange')[1].text
            price_2 = float(price_2.replace('$', ''))
            try:
                assert price_1 > price_2
                print('降序测试通过')
            except AssertionError:
                print('降序测试失败')
        else:
            price_1 = driver.find_elements(by='class name', value='item.width-17.text-orange')[0].text
            price_1 = float(price_1.replace('$', ''))
            price_2 = driver.find_elements(by='class name', value='item.width-17.text-orange')[1].text
            price_2 = float(price_2.replace('$', ''))
            try:
                assert price_1 < price_2
                print('升序测试通过')
            except AssertionError:
                print('升序测试失败')

    # 断言时间排序方法
    def assert_time_desc(self, driver, info):
        """
        断言时间排序方法
        :param driver: 驱动
        :param info:  获取的定位文本
        :return:
        """
        if info == '2035':  # 为日期降序
            time_1 = driver.find_elements(by='class name', value='item.width-17.date')[0].text
            print(time_1)
            number1 = self.get_number(time_1)
            print(number1)
            time_2 = driver.find_elements(by='class name', value='item.width-17.date')[1].text
            print(time_2)
            number2 = self.get_number(time_2)
            print(number2)
            try:
                assert number1 > number2
                print('降序测试通过')
            except AssertionError:
                print('降序测试失败')
                raise AssertionError
        elif info == '2393':  # 日期升序
            time_1 = driver.find_elements(by='class name', value='item.width-17.date')[0].text
            print(time_1)
            number1 = self.get_number(time_1)
            print(number1)
            time_2 = driver.find_elements(by='class name', value='item.width-17.date')[1].text
            print(time_2)
            number2 = self.get_number(time_2)
            print(number2)
            try:
                assert number1 < number2
                print('升序测试通过')
            except AssertionError:
                print('升序测试失败')
                raise AssertionError

    # 提取字符串中的数字，组合为一个数字，便于比较
    def get_number(self, string):
        """
        将字符串转换为数字进行比较
        :param string:
        :return:
        """
        number_list = re.findall(pattern=('\d+'), string=string)
        num = ''
        for number in number_list:
            num += number
        time_info = int(num)
        return time_info

    # 寻找未支付订单,寻找到则点击按钮跳转到支付页面
    def find_Unpaid(self, driver, n):
        """
        寻找未支付订单，如果找到则点击，没找到则PASS
        :param driver:  驱动
        :param n: 用于计算找到待支付的订单
        :return: n,element
        """
        Common().huadong(driver, by='class name', value='text-tit-lg.flex')  # 滑动到订单最上方
        infos = driver.find_elements(by='class name', value='item.width-17.status')  # 获取当页订单数据
        print(len(infos))
        for info in infos:
            print(info.text)
            if info.text == '未支付':
                driver.execute_script("arguments[0].scrollIntoView();", info)  # 拖动到可见的元素去
                info.click()  # 点击该按钮
                n += 1
                break  # 打破循环
            else:
                pass
        return n

    # 寻找已签收订单
    def find_signed(self, driver, n):
        Common().huadong(driver, by='class name', value='text-tit-lg.flex')  # 滑动到订单最上方
        elements = driver.find_elements(by='css selector', value='div[class="item width-17 status"]')
        print(len(elements))  # 获取当页数据条数
        for i in range(len(elements)):
            print(i)
            status = elements[i].text
            print(status)
            if status == 'signed in Request Return':
                n += 1
                Common().huadong(driver,by='css selector',value=f'div[class="lines flex"]:nth-child({i+1}) > div[class="item width-17 status"] > button')
                time.sleep(1)
                driver.find_element(by='css selector',value=f'div[class="lines flex"]:nth-child({i+1}) > div[class="item width-17 status"] > button').click()   #点击按钮
                time.sleep(1.5)
                Common().huadong(driver,by='class name',value='ant-btn.ant-btn-primary.ant-btn-sm')
                driver.find_element(by='class name',value='ant-btn.ant-btn-primary.ant-btn-sm').click()   #点击确认
                time.sleep(2)
                break
            else :
                pass
        return n

    #寻找已签收订单-点击退货-确定-进入退货单页面
    def go_return_goods(self,driver):
        n = 0  # 判断是否找到
        page = 0  # 判断所处页数
        while True:
            n = self.find_signed(driver, n)
            print(n)
            page += 1
            if n == 0:  # 如果有n 为0  则未找到，
                print(f'第{page}页未找到相关数据')
                try:
                    # 移动到翻页处
                    Common().huadong(driver, by='class name', value='ant-pagination-item-link')
                    # 先判断下一页按钮状态 如果为true 说明是最后一页
                    info = driver.find_element(by='class name', value='ant-pagination-disabled.ant-pagination-next').get_attribute('aria-disabled')
                    if info == "true":
                        print('此页为最后一页')
                        break
                except NoSuchElementException:
                    print('不是最后一页')
                    driver.find_element(by='css selector', value='li[class=" ant-pagination-next"]').click()  # 点击下一页
                    print('点击下一页')
                    time.sleep(2)
            else:
                print(f'第{page}页存在已签收数据')
                break
        return n