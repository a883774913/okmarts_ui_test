"""
优惠券模块
"""
import random
import time

from selenium.webdriver.support.wait import WebDriverWait

from okmarts_ui_test.common.common import Common


class Conpons:

    def conpons(self,driver,Parameter):
        casename = Parameter['casename']
        data = Parameter['data']
        print(data)
        assert_way = Parameter['assert_way']
        result = Parameter['result']

        driver.get('http://18.118.13.94:81/index')  # 打开首页
        WebDriverWait(driver, 20, 0.2).until(lambda x: x.find_element(by='xpath', value='//*[@id="app"]/div/div[1]/div/div[2]/div[3]/div[3]/span[1]'))
        time.sleep(1)
        Common().is_login(driver,useraccount='979172251@qq.com',password='a123456')     #登录
        time.sleep(1)
        driver.find_element(by='css selector', value='#app > div > div.global-header > div > div.menu-content > div.menu-right.flex > div:nth-child(1)').click()  # 点击头像
        time.sleep(2)
        if casename == '点击View details 跳转至优惠券页面成功':
            driver.find_element(by='css selector',value='#app > div > div.my-info > div.coupon-out > div > div.coupon-out.flex.align-center > '
                                                        'div.count.flex.margin-right-xs > div > a').click() #点击查看优惠券
            time.sleep(2)
            text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                       value=f"{assert_way.split('=', 1)[1]}").text
            print(text)
            assert text == result
        elif casename in ['选择UNused显示未使用优惠券','选择used显示已使用优惠券']:
            self.conpons_mode(driver,data)
        elif casename == '点击Points Mall，页面成功跳转到积分商城页面':
            driver.find_element(by='class name',value='pointsMall-out.text-center').click() #点击积分商城
            time.sleep(2)
            text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                       value=f"{assert_way.split('=', 1)[1]}").text
            print(text)
            assert text == result
        elif casename == '选择优惠券兑换成功':
            info = driver.find_element(by='css selector',value='#app > div > div.my-info > div.coupon-out > div > div.coupon-out.flex.align-center > '
                                                        'div.count.flex.margin-right-xs > div > p').text        #获取现有优惠券数量
            print(f'info为{info}')
            driver.find_element(by='class name',value='pointsMall-out.text-center').click()  #点击进入积分商城
            time.sleep(2)
            total_points = driver.find_element(by='class name',value='text-F8C334').text        #获取账户现有积分
            print(f'交易前有{total_points}个积分')
            infos = driver.find_elements(by='class name',value='ant-btn.ant-btn-block')
            print(infos)
            random.choice(infos).click()        #随机选择一个优惠券进行点击
            time.sleep(1)
            driver.find_element(by='class name',value='bg-orange.ant-btn').click()      #点击确定
            time.sleep(6)


    def conpons_mode(self,driver,data):
        """
        进入优惠券页面，点击used或者UNused进行查看，检测是否有错误
        :param driver: 驱动
        :param data: data为（used）或者（unused）
        :return:
        """
        driver.find_element(by='css selector', value='#app > div > div.my-info > div.coupon-out > div > div.coupon-out.flex.align-center > '
                                                     'div.count.flex.margin-right-xs > div > a').click()  # 点击查看优惠券
        total_used = 0
        total_unused = 0
        time.sleep(2)
        while True:
            n = len(driver.find_elements(by='class name', value="ant-col.ant-col-6"))  # 获取当页数据条数
            print(f'当页存在{n - 5}条数据')
            for i in range(1, n - 4):
                conpons = driver.find_elements(by='class name', value="ant-col.ant-col-6")[i].text
                if conpons == 'Used':
                    total_used += 1  # 计算使用过的优惠券条数
                elif conpons == 'Unused':
                    total_unused += 1  # 计算未使用优惠券的条数
            info = driver.find_element(by='css selector', value='li[title="Next Page"]').get_attribute("aria-disabled")  # 获取NEXT按钮属性，检测是否为最后一页
            print(info)
            if info is None:
                print('不是最后一页')
                driver.find_element(by='css selector', value='li[title="Next Page"]').click()  # 点击下一页
                time.sleep(2)
            else:
                print('当页为最后一页')
                break
        print(f'已使用数据有{total_used}条')
        print(f'未使用数据有{total_unused}条')
        driver.find_elements(by='class name', value='ant-select-selection-selected-value')[1].click()  # 点击筛选
        time.sleep(0.5)
        if data == 'used':
            local = 2
        else :
            local = 1
        driver.find_elements(by='class name', value='ant-select-dropdown-menu-item')[local].click()  # 点击used
        time.sleep(1)
        erro = 0  # 用于计算错误的个数
        num = 0  # 用于计算符合条件的个数
        while True:
            n2 = len(driver.find_elements(by='class name', value="ant-col.ant-col-6"))  # 获取当页显示优惠券数量
            print(f'当页存在{n2 - 5}条数据')
            for i in range(1, n2 - 4):
                conpons = driver.find_elements(by='class name', value="ant-col.ant-col-6")[i].text
                if conpons == data:
                    num += 1
                else:
                    print('存在条件外的优惠券')
                    erro += 1  # 存在错误
                    break
            if erro != 0:
                print('筛选功能存在异常')
                assert False
            else:
                pass
            info = driver.find_element(by='css selector', value='li[title="Next Page"]').get_attribute("aria-disabled")  # 获取NEXT按钮属性，检测是否为最后一页
            print(info)
            if info is None:
                print('不是最后一页')
                driver.find_element(by='css selector', value='li[title="Next Page"]').click()  # 点击下一页
                time.sleep(2)
            else:
                print('当页为最后一页')
                break
        if data == 'used':
            assert total_used == num
        else:
            assert total_unused == num