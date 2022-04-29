"""
购物车模块
"""
import time

from selenium.webdriver.support.wait import WebDriverWait

from okmarts_ui_test.common.common import Common
from okmarts_ui_test.mysql.mysql import Mysql


class Shop_Car:

    def shop_car(self,driver,Parameter):
        casename = Parameter['casename']
        data = Parameter['data']
        print(data)
        assert_way = Parameter['assert_way']
        result = Parameter['result']

        driver.get('http://18.118.13.94:81/index')  # 打开首页
        WebDriverWait(driver,20,0.2).until(lambda x:x.find_element(by='xpath',value='//*[@id="app"]/div/div[1]/div/div[2]/div[3]/div[3]/span[1]'))
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
            Common().is_login(driver,useraccount='979172251@qq.com',password='a123456')
            time.sleep(2)
            if casename == '首页显示购物车图标，点击购物车，页面跳转到购物车页面':
                info = driver.find_element(by='xpath',value='//*[@id="app"]/div/div[1]/div/div[2]/div[3]/div[3]/span[1]').text      #检查是否存在购物车按钮
                print(info)
                goods_number = driver.find_element(by='class name',value='num').text
                print(goods_number)
                assert info == 'Cart'
                driver.find_element(by='xpath',value='//*[@id="app"]/div/div[1]/div/div[2]/div[3]/div[3]/span[1]').click()
                time.sleep(2)
                if goods_number == '0':
                    text = driver.find_element(by='xpath',value='//*[@id="app"]/div/div/div[2]/div[1]/a').text
                    print('不存在商品')
                    print(text)
                    assert text == 'The shopping cart is still empty for the time being, go pick a few items right away'
                else:
                    print('存在商品')
                    text = driver.find_element(by='xpath',value='//*[@id="app"]/div/div/div[2]/div[1]/div[1]/div[1]/div[1]/span').text
                    assert text == 'Shopping cart'
            if casename == '购物车内无商品时点击相关文字跳转到首页成功':
                goods_number = driver.find_element(by='class name', value='num').text       #判断购物车是否有商品
                print(goods_number)
                if goods_number != '0': #如果商品数量不为0，删除该账户购物车商品数据
                    Mysql().drop_table(user="root", pwd="OKmarts888.,", host="18.118.13.94", db="okmarts", port=3306,
                                       sql="DELETE FROM shopping_cart WHERE userid='1506910015154425856';")
                else:
                    text = driver.find_element(by='xpath', value='//*[@id="app"]/div/div/div[2]/div[1]/a').text
                    print('不存在商品')
                    print(text)
                    assert text == 'The shopping cart is still empty for the time being, go pick a few items right away'
                    driver.find_element(by='xpath', value='//*[@id="app"]/div/div/div[2]/div[1]/a').click()
                    time.sleep(2)
                    text = driver.find_element(by='class name',value='pointer.all').text
                    assert  text == 'Full catalog'
