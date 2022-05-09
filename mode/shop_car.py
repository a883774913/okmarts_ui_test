"""
购物车模块
"""
import random
import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

from okmarts_ui_test.common.common import Common
from okmarts_ui_test.mysql.mysql import Mysql


class Shop_Car:

    def shop_car(self, driver, Parameter):
        casename = Parameter['casename']
        data = Parameter['data']
        print(data)
        assert_way = Parameter['assert_way']
        result = Parameter['result']

        driver.get('http://18.118.13.94:81/index')  # 打开首页
        WebDriverWait(driver, 20, 0.2).until(lambda x: x.find_element(by='xpath', value='//*[@id="app"]/div/div[1]/div/div[2]/div[3]/div[3]/span[1]'))
        time.sleep(1)
        if casename == '未登录状态下点击购物车页面跳转到登录页面成功':
            Common().Restore_environment(driver)
            time.sleep(1)
            driver.find_element(by='xpath', value='//*[@id="app"]/div/div[1]/div/div[2]/div[3]/div[3]/span[1]').click()
            time.sleep(2)
            text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                       value=f"{assert_way.split('=', 1)[1]}").text
            print(text)
            assert text == result
        else:
            Common().is_login(driver, useraccount='979172251@qq.com', password='a123456')
            time.sleep(2)
            if casename == '首页显示购物车图标，点击购物车，页面跳转到购物车页面':
                info = driver.find_element(by='xpath', value='//*[@id="app"]/div/div[1]/div/div[2]/div[3]/div[3]/span[1]').text  # 检查是否存在购物车按钮
                print(info)
                goods_number = driver.find_element(by='class name', value='num').text       #获取购物车小图标显示数量
                print(goods_number)
                assert info == 'Cart'
                driver.find_element(by='xpath', value='//*[@id="app"]/div/div[1]/div/div[2]/div[3]/div[3]/span[1]').click()     #点击购物车
                time.sleep(2)
                if goods_number == '0':
                    text = driver.find_element(by='xpath', value='//*[@id="app"]/div/div/div[2]/div[1]/a').text
                    print('不存在商品')
                    print(text)
                    assert text == 'The shopping cart is still empty for the time being, go pick a few items right away'
                else:
                    print('存在商品')
                    text = driver.find_element(by='xpath', value='//*[@id="app"]/div/div/div[2]/div[1]/div[1]/div[1]/div[1]/span').text
                    assert text == 'Shopping cart'
            elif casename == '购物车内无商品时点击相关文字跳转到首页成功':
                goods_number = driver.find_element(by='class name', value='num').text  # 判断购物车是否有商品
                if goods_number != '0':  # 如果商品数量不为0，删除该账户购物车商品数据
                    print('存在商品，删除中')
                    Mysql().drop_table(user="root", pwd="OKmarts888.,", host="18.118.13.94", db="okmarts", port=3306,
                                       sql="DELETE FROM shopping_cart WHERE userid='1506910015154425856';")
                    time.sleep(1)
                else:
                    pass
                driver.find_element(by='class name', value='num').click()
                time.sleep(2)
                text = driver.find_element(by='xpath', value='//*[@id="app"]/div/div/div[2]/div[1]/a').text
                print(text)
                assert text == 'The shopping cart is still empty for the time being, go pick a few items right away'
                driver.find_element(by='xpath', value='//*[@id="app"]/div/div/div[2]/div[1]/a').click()
                time.sleep(2)
                text1 = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                            value=f"{assert_way.split('=', 1)[1]}").text
                assert text1 == result
            elif casename == '当商品添加数量为1时无法点击-号':
                Mysql().drop_table(user="root", pwd="OKmarts888.,", host="18.118.13.94", db="okmarts", port=3306,
                                   sql="DELETE FROM shopping_cart WHERE userid='1506910015154425856';")
                time.sleep(1)
                self.add_goods_to_shopcar(driver)  # 加入商品至购物车
                try:
                    info = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                               value=f"{assert_way.split('=', 1)[1]}").get_attribute("disabled")
                    print(info)
                    assert info == result
                except:
                    assert False
            elif casename == '购物车内包含商品时，购物车图标显示正确':
                goods_number = driver.find_element(by='class name', value='num').text  # 判断购物车是否有商品
                print(goods_number)
                if goods_number == '0':  # 如果商品数量为0
                    self.add_goods_to_shopcar(driver)
                    goods_number2 = driver.find_element(by='class name', value='num').text  # 判断购物车商品数量有无增加
                    print(goods_number2)
                    assert int(goods_number2) == int(goods_number) + 1
                elif goods_number == '99+':
                    driver.find_element(by='class name', value='num').click()  # 点击购物车
                    time.sleep(2)
                    driver.find_element(by='css selector', value='label[class="ant-checkbox-wrapper"]').click()  # 点击勾选全部
                    time.sleep(0.5)
                    driver.find_element(by='css selector', value='#app > div > div > div.ui-container > div.content.flex.space-between > div.auction-info > '
                                                                 'div.title-1.flex.align-center.space-between > div.action.text-blue > a').click()  # 点击删除
                    time.sleep(0.5)
                    driver.find_element(by='class name', value='ant-btn.ant-btn-primary.ant-btn-sm').click()  # 点击确认
                    time.sleep(3)
                    goods_number2 = driver.find_element(by='class name', value='num').text  # 判断购物车商品数量有无增加
                    print(goods_number2)
                    assert goods_number2 == '0'
                else:  # 否则则为0-99+ 中的值
                    driver.find_element(by='class name', value='num').click()  # 点击购物车
                    time.sleep(2)
                    driver.find_element(by='css selector', value='svg[p-id="3096"]').click()  # 点击加
                    time.sleep(3)
                    goods_number2 = driver.find_element(by='class name', value='num').text  # 判断购物车商品数量有无增加
                    print(goods_number2)
                    assert int(goods_number2) == int(goods_number) + 1
                    driver.find_element(by='css selector', value='svg[p-id="2909"]').click()  # 点击减
                    time.sleep(3)
                    goods_number3 = driver.find_element(by='class name', value='num').text  # 判断购物车商品数量有无减少
                    assert goods_number3 == goods_number
            elif casename == '购物车数量大于99时，购物车略缩图显示99+':
                self.add_goods_to_shopcar(driver)
                driver.find_element(by='class name', value='input.ant-input').send_keys(Keys.CONTROL, 'a')
                time.sleep(0.5)
                driver.find_element(by='class name', value='input.ant-input').send_keys('100')
                time.sleep(3)
                goods_number = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                                   value=f"{assert_way.split('=', 1)[1]}").text
                print(goods_number)
                assert goods_number == result
            elif casename == '在商品详情页点击ADD Car添加到购物车成功':
                goods_name = self.add_goods_to_shopcar(driver)
                infos = driver.find_elements(by='class name', value='title.text-black.margin-bottom-xs.pointer')
                n = 0
                for info in infos:
                    print(info.text)
                    if info.text == goods_name:
                        n = 1
                        break
                if n == 1:
                    assert True
                else:
                    assert False
            elif casename == '通过搜索出商品时，点击ADD Car添加到购物车成功':
                self.search_goods(driver, info=f'{random.randint(1, 10)}')
                number = random.randint(0, 11)
                print(number)
                target = driver.find_elements(by='class name', value='anticon.anticon-shopping-cart')[number]
                driver.execute_script("arguments[0].scrollIntoView();", target)  # 拖动到可见的元素去
                goods_name = driver.find_elements(by='class name', value='title.text-black.margin-bottom-xs ')[number].text  # 获取商品名称
                print(goods_name)
                driver.find_elements(by='css selector', value='div.btn-out > button[class="ant-btn"]')[number].click()  # 随机点击一个商品的加入购物车
                time.sleep(2)
                driver.find_element(by='class name', value='num').click()  # 点击购物车,进入购物车页面
                time.sleep(2)
                infos = driver.find_elements(by='class name', value='title.text-black.margin-bottom-xs.pointer')
                n = 0
                for info in infos:
                    print(info.text)
                    if info.text == goods_name:
                        n = 1
                        break
                if n == 1:
                    assert True
                else:
                    assert False
            elif casename == '勾选多个商品批量结算成功':
                Mysql().drop_table(user="root", pwd="OKmarts888.,", host="18.118.13.94", db="okmarts", port=3306,
                                   sql="DELETE FROM shopping_cart WHERE userid='1506910015154425856';")
                self.search_goods(driver, info=f'{random.randint(1, 10)}')
                for i in range(1, 11):
                    element = driver.find_elements(by='class name', value='ant-btn')[i]
                    element.click()
                    time.sleep(1)
                driver.find_element(by='class name', value='num').click()  # 点击购物车,进入购物车页面
                time.sleep(3)
                infos = driver.find_elements(by='class name', value='auction-part.flex.cart-item.align-center')  # 获取可以勾选的数据
                print(len(infos))  # 获取条数
                random_nos = random.sample(range(0, len(infos) - 1), 2)
                print(random_nos)
                name1 = driver.find_elements(by='class name', value='title.text-black.margin-bottom-xs.pointer')[random_nos[0]].text
                print(name1)
                price1 = float(driver.find_elements(by='class name', value='text-price.margin-right-xs')[random_nos[0]].text.replace('$', ''))
                driver.find_elements(by='class name', value='check-cart.ant-checkbox-wrapper')[random_nos[0]].click()  # 勾选第1个商品
                print(price1)
                name2 = driver.find_elements(by='class name', value='title.text-black.margin-bottom-xs.pointer')[random_nos[1]].text
                print(name2)
                price2 = float(driver.find_elements(by='class name', value='text-price.margin-right-xs')[random_nos[1]].text.replace('$', ''))
                print(price2)
                driver.find_elements(by='class name', value='check-cart.ant-checkbox-wrapper')[random_nos[1]].click()  # 勾选第2个商品
                total_price = float(
                    driver.find_element(by='css selector', value='#app > div > div > div.ui-container > div.content.flex.space-between > div.payTotal-out > div > '
                                                                 'div.item.margin-bottom-xs > span.text-price').text.replace('$', ''))
                print(total_price)
                assert total_price == price1 + price2
                driver.find_element(by='class name', value='atn-btn-orange.ant-btn.ant-btn-block').click()  # 点击结算
                time.sleep(1)
                text1 = driver.find_elements(by='class name', value='title.text-black.margin-bottom-xs')[0].text
                text2 = driver.find_elements(by='class name', value='title.text-black.margin-bottom-xs')[1].text
                assert text1, text2 in [name1, name2]
            elif casename == '点击ALL Choices 所有商品被勾选，点击删除删除成功':
                Mysql().drop_table(user="root", pwd="OKmarts888.,", host="18.118.13.94", db="okmarts", port=3306,
                                   sql="DELETE FROM shopping_cart WHERE userid='1506910015154425856';")
                self.search_goods(driver, info=f'{random.randint(1, 10)}')
                for i in range(1, 11):
                    element = driver.find_elements(by='class name', value='ant-btn')[i]
                    element.click()
                    time.sleep(1)
                driver.find_element(by='class name', value='num').click()  # 点击购物车,进入购物车页面
                time.sleep(3)
                driver.find_element(by='class name',value='ant-checkbox-input').click()        #点击全选
                time.sleep(1)
                driver.find_element(by='css selector',value='#app > div > div > div.ui-container > div.content.flex.space-between > div.auction-info > '
                                                            'div.title-1.flex.align-center.space-between > div.action.text-blue > a').click()
                time.sleep(0.5)
                driver.find_element(by='class name',value='ant-btn.ant-btn-primary.ant-btn-sm').click()
                time.sleep(2)

                text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                            value=f"{assert_way.split('=', 1)[1]}").text
                print(text)
                assert text == result



    def add_goods_to_shopcar(self, driver):
        """
        随机选择一个商品点击-加入购物车-进入购物车
        :param driver:  驱动
        :return: 将入购物车的商品名称
        """
        Common().huadong(driver, by='class name', value='title.text-tit-lg.margin-bottom-sm')  # 滑动页面至热销栏
        driver.find_elements(by='class name', value='gutter-row.ant-col.ant-col-6')[random.randint(0, 5)].click()  # 首页随机点击一个商品进入详情页
        time.sleep(2)
        WebDriverWait(driver,30,0.2).until(lambda x:x.find_element(by='class name', value='title.text-black.margin-bottom-sm'))
        goods_name = driver.find_element(by='class name', value='title.text-black.margin-bottom-sm').text
        print(f'goods_name为{goods_name}')
        driver.find_element(by='class name', value='atn-btn-orange.ant-btn.ant-btn-block').click()  # 点击加入购物车
        time.sleep(1)
        driver.find_element(by='class name', value='num').click()  # 点击购物车,进入购物车页面
        time.sleep(3)
        return goods_name

    # 搜索商品进入搜索页面并按照降序排列
    def search_goods(self, driver, info):
        """
        搜索商品进入搜索页面
        :param driver: 驱动
        :param info: 搜索的内容
        :return:
        """
        driver.find_element(by='class name', value='ant-input').send_keys(info)  # 搜索栏输入1
        driver.find_element(by='class name', value='ant-btn').click()  # 点击确定
        time.sleep(2)
        driver.find_element(by='xpath', value='//*[@id="app"]/div/div[2]/div[1]/div[2]/div[1]/div[3]/div/div/div/div').click()  # 点击排序
        time.sleep(0.5)
        driver.find_element(by='class name', value='ant-select-dropdown-menu-item').click()  # 选择倒序排列
        time.sleep(2)
