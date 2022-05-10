"""
优惠券模块
"""
import random
import re
import time

from pykeyboard.windows import PyKeyboard
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait

from okmarts_ui_test.common.common import Common


class Conpons:

    def conpons(self, driver, Parameter):
        casename = Parameter['casename']
        data = Parameter['data']
        print(data)
        assert_way = Parameter['assert_way']
        result = Parameter['result']

        driver.get('http://18.118.13.94:81/index')  # 打开首页
        WebDriverWait(driver, 20, 0.2).until(lambda x: x.find_element(by='xpath', value='//*[@id="app"]/div/div[1]/div/div[2]/div[3]/div[3]/span[1]'))
        time.sleep(1)
        if casename == '使用积分不足账户兑换优惠券兑换失败':  # 特殊用例 使用不同账户进行测试
            useraccount, password = Common().random_account()
            # Common().is_login(driver, "979172251@qq.com", "a123456")
            Common().is_login(driver, useraccount, password)
            time.sleep(1)
            driver.find_element(by='css selector',
                                value='#app > div > div.global-header > div > div.menu-content > div.menu-right.flex > div:nth-child(1)').click()  # 点击头像
            time.sleep(2)
            driver.find_element(by='class name', value='pointsMall-out.text-center').click()  # 点击进入积分商城
            time.sleep(2)
            try:
                total_points = driver.find_element(by='class name', value='text-F8C334').text  # 获取账户现有积分
                print(f'当前账户含有{total_points}个积分')
                prices = driver.find_elements(by='class name', value='text-price')
                for i in range(len(prices)):
                    print(prices[i].text)
                    if int(prices[i].text) > int(total_points):  # 如果所需积分大于账户积分
                        driver.find_elements(by='class name', value='ant-btn.ant-btn-block')[i].click()  # 点击相应按钮
                        time.sleep(1)
                        driver.find_element(by='class name', value='bg-orange.ant-btn').click()  # 点击确定
                        time.sleep(2)
                        text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                                   value=f"{assert_way.split('=', 1)[1]}").text
                        print(text)
                        try:
                            assert text == result
                        finally:
                            break
            except NoSuchElementException:
                print(f'当前账户含有 0 积分')
                infos = driver.find_elements(by='class name', value='ant-btn.ant-btn-block')
                print(infos)
                print(len(infos))  # 获取优惠券个数
                number = random.randint(0, len(infos) - 1)
                driver.find_elements(by='class name', value='ant-btn.ant-btn-block')[number].click()
                time.sleep(1)
                driver.find_element(by='class name', value='bg-orange.ant-btn').click()  # 点击确定
                time.sleep(2)
                text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                           value=f"{assert_way.split('=', 1)[1]}").text
                print(text)
                assert text == result
        else:
            Common().is_login(driver, useraccount='979172251@qq.com', password='a123456')  # 登录
            time.sleep(1)
            driver.find_element(by='css selector',
                                value='#app > div > div.global-header > div > div.menu-content > div.menu-right.flex > div:nth-child(1)').click()  # 点击头像
            time.sleep(2)
            if casename == '点击View details 跳转至优惠券页面成功':
                driver.find_element(by='css selector', value='#app > div > div.my-info > div.coupon-out > div > div.coupon-out.flex.align-center > '
                                                             'div.count.flex.margin-right-xs > div > a').click()  # 点击查看优惠券
                time.sleep(2)
                text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                           value=f"{assert_way.split('=', 1)[1]}").text
                print(text)
                assert text == result
            elif casename in ['选择UNused显示未使用优惠券', '选择used显示已使用优惠券']:
                self.conpons_mode(driver, data)
            elif casename == '点击Points Mall，页面成功跳转到积分商城页面':
                driver.find_element(by='class name', value='pointsMall-out.text-center').click()  # 点击积分商城
                time.sleep(2)
                text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                           value=f"{assert_way.split('=', 1)[1]}").text
                print(text)
                assert result in text
            elif casename == '选择优惠券兑换成功':
                info = driver.find_element(by='css selector', value='#app > div > div.my-info > div.coupon-out > div > div.coupon-out.flex.align-center > '
                                                                    'div.count.flex.margin-right-xs > div > p').text  # 获取现有优惠券数量
                print(f'info为{info}')
                conponse_number = re.findall('\d+', string=info)[0]
                print(f'交易前存在{conponse_number}张优惠券')
                driver.find_element(by='class name', value='pointsMall-out.text-center').click()  # 点击进入积分商城
                time.sleep(2)
                total_points = driver.find_element(by='class name', value='text-F8C334').text  # 获取账户现有积分
                print(f'交易前有{total_points}个积分')
                infos = driver.find_elements(by='class name', value='ant-btn.ant-btn-block')
                print(infos)
                print(len(infos))  # 获取优惠券个数
                number = random.randint(0, len(infos) - 1)
                random_price = driver.find_elements(by='class name', value='text-price')[number].text  # 获取随机点击的优惠券所需积分
                print(f'兑换该优惠券需要{random_price}个积分')
                driver.find_elements(by='class name', value='ant-btn.ant-btn-block')[number].click()
                time.sleep(1)
                driver.find_element(by='class name', value='bg-orange.ant-btn').click()  # 点击确定
                time.sleep(1)
                pk = PyKeyboard()
                pk.press_key(pk.escape_key)
                pk.release_key(pk.escape_key)
                time.sleep(2)
                total_points2 = driver.find_element(by='class name', value='text-F8C334').text  # 获取账户现有积分
                print(f'兑换后积分为{total_points2}')
                assert int(total_points2) == int(total_points) - int(random_price)  # 断言目前的积分=兑换前积分-兑换所需积分
                driver.find_element(by='class name',
                                    value='r_text').click()  # 点击头像
                time.sleep(2)
                info2 = driver.find_element(by='css selector', value='#app > div > div.my-info > div.coupon-out > div > div.coupon-out.flex.align-center > '
                                                                     'div.count.flex.margin-right-xs > div > p').text  # 获取现有优惠券数量
                print(f'info2为{info2}')
                conponse_number2 = re.findall('\d+', string=info2)[0]
                print(f'兑换后优惠券数量为{conponse_number2}')
                assert int(conponse_number2) == int(conponse_number) + 1  # 断言 目前的优惠券数量 = 兑换前优惠券数量+1
            elif casename == '点击优惠券使用帮助查看页面成功':
                driver.find_element(by='class name', value='pointsMall-out.text-center').click()  # 点击进入积分商城
                time.sleep(2)
                driver.find_element(by='class name', value='help').click()
                time.sleep(2)
                text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                           value=f"{assert_way.split('=', 1)[1]}").text
                print(text)
                assert result in text
        Common().Restore_environment(driver)

    def conpons_mode(self, driver, data):
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
        if data == 'Used':
            local = 2
        else:
            local = 1
        driver.find_elements(by='class name', value='ant-select-dropdown-menu-item')[local].click()  # 点击used/UNused
        time.sleep(1)
        erro = 0  # 用于计算错误的个数
        num = 0  # 用于计算符合条件的个数
        while True:
            n2 = len(driver.find_elements(by='class name', value="ant-col.ant-col-6"))  # 获取当页显示优惠券数量
            print(f'当页存在{n2 - 5}条优惠券数据')
            for i in range(1, n2 - 4):
                conpons = driver.find_elements(by='class name', value="ant-col.ant-col-6")[i].text
                print(conpons)
                print(data)
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
            try:
                info = driver.find_element(by='css selector', value='li[title="Next Page"]').get_attribute("aria-disabled")  # 获取NEXT按钮属性，检测是否为最后一页
                print(info)
                if info is None:
                    print('不是最后一页')
                    driver.find_element(by='css selector', value='li[title="Next Page"]').click()  # 点击下一页
                    time.sleep(2)
                else:
                    print('当页为最后一页')
                    break
            except NoSuchElementException:
                print('当页为最后一页')
                break
        print(f'num为{num}')
        print(f'total_used为{total_used}')
        print(f'total_unused为{total_unused}')
        if data == 'Used':
            assert total_used == num
        else:
            assert total_unused == num
